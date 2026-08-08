from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2542"
BRANCH_ID = "MTS_R2FR_DOWNSTREAM_OBSERVATION_FUNCTOR_OR_SRNG_ADOPTION_2542"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2542-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2542_SOURCE_REGISTER.csv",
    "naturality": RESIDUALS / "P8_Y5_NO_SHADOW_2542_DOWNSTREAM_NATURALITY_DERIVATION_AUDIT.csv",
    "contract": RESIDUALS / "P8_Y5_NO_SHADOW_2542_OBSERVATION_FUNCTOR_CONTRACT.csv",
    "adoption": RESIDUALS / "P8_Y5_NO_SHADOW_2542_SRNG_ADOPTION_DECISION_MATRIX.csv",
    "p4_status": RESIDUALS / "P8_Y5_NO_SHADOW_2542_P4_RESIDUAL_STATUS_AFTER_SRNG_ADOPTION.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2542_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2542_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2542_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2542_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2542_VALIDATION.csv",
}

BRANCH_COPIES = {
    "naturality": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Downstream_naturality_audit_2542_NONCLAIM.csv",
    "contract": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Observation_functor_contract_2542_PRIVATE_NONCLAIM.csv",
    "p4_status": POST_ROOT / "source-intake" / "local_bounds" / "P4_residual_status_after_SRNG_2542_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "BOUNDARY_PROJECTIVE2542_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    ("SRC2542_0_2541_doc", "2541-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md", "NEXT2541_0_selected", "2541 selected downstream observation functor route"),
    ("SRC2542_1_2541_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2541_VALIDATION.csv", "VAL2541_OVERALL,PASS", "2541 validation anchor"),
    ("SRC2542_2_2541_certificate", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv", "SRNG2541_6_verdict", "current SRNG certificate"),
    ("SRC2542_3_2541_theorem", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_SRNG_THEOREM_ATTEMPT.csv", "THM2541_3_SRNG_sum", "current SRNG theorem attempt"),
    ("SRC2542_4_2541_p4_status", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_P4_DELTA_STATUS_AFTER_SRNG.csv", "P4S2541_6_reduced_total", "current P4 status after SRNG"),
    ("SRC2542_5_2377_doc", "2377-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md", "DNF2377_7_verdict", "older downstream functor precedent"),
    ("SRC2542_6_2377_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2377_VALIDATION.csv", "VAL2377_OVERALL", "2377 validation anchor"),
    ("SRC2542_7_2377_naturality", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2377_DOWNSTREAM_NATURALITY_DERIVATION_AUDIT.csv", "DNF2377_7_verdict", "downstream naturality audit precedent"),
    ("SRC2542_8_2377_contract", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2377_OBSERVATION_FUNCTOR_CONTRACT.csv", "OFC2377_5_status", "observation functor contract precedent"),
    ("SRC2542_9_2377_adoption", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2377_SRNG_ADOPTION_DECISION_MATRIX.csv", "ADM2377_3_decision", "SRNG adoption decision precedent"),
    ("SRC2542_10_2377_p4_status", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2377_P4_RESIDUAL_STATUS_AFTER_SRNG_ADOPTION.csv", "P4A2377_4_reduced_total", "P4 residual status after private SRNG precedent"),
    ("SRC2542_11_2377_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2377_NEXT_TARGET.csv", "NEXT2377_0_selected", "boundary/projective next target precedent"),
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


def downstream_naturality_audit() -> list[dict[str, object]]:
    rows = [
        (
            "DNF2542_0_target",
            "derive SRNG from downstream observation functor naturality",
            "If observations are natural functors O_i: Sol(Q_obs)->Readout_i evaluated after the variational problem, then O_i cannot add Gamma_ind to S_parent.",
            "TARGET_SHARPENED",
            "turns readout silence from a clause into functorial bookkeeping",
            "must prove readouts are not hidden action/source terms",
        ),
        (
            "DNF2542_1_quotient_domain",
            "observed quotient domain",
            "q: Phi_parent -> Q_obs is fixed before readout, and e_obs/g_obs/omega_LC[e_obs] are functors of Q_obs.",
            "CONDITIONAL_FROM_PRIOR_CONTRACTS",
            "readouts can depend on observed fields without depending on representative/Gamma slots",
            "q and full observed coframe descent remain not parent-signed in active corpus",
        ),
        (
            "DNF2542_2_downstream_separation",
            "action/readout separation",
            "S_parent is varied over dynamical fields first; O_clock, O_light, O_orbit and detector readouts are maps on solutions, not extra action terms.",
            "EXACT_IF_PARENT_OBSERVATION_POLICY_SIGNED",
            "delta O_i/delta Gamma_ind is irrelevant to hypermomentum because O_i is not in S_parent",
            "instrument backreaction and marker/domain selection must be included as ordinary matter or residuals",
        ),
        (
            "DNF2542_3_naturality",
            "naturality under vertical/gauge maps",
            "For v in ker(Dq), O_i(q(Phi)) is invariant: delta_v O_i = D O_i[Dq(v)] = 0.",
            "EXACT_CONDITIONAL_CHAIN_RULE",
            "kills fake readout-frame dependence without fitting",
            "actual MTS vertical directions and no-shadow-frame clauses are still conditional",
        ),
        (
            "DNF2542_4_source_selector",
            "source/worldtube selector",
            "W_source=closure(supp J_H[tau]) is legal only when selected from the same Hilbert/coframe matter current before readout.",
            "CONDITIONAL_NOT_CLOSED",
            "prevents measured GM/source support from becoming a post-readout mask",
            "compactness, M_H_ref, tau/frame lock, boundary/reference and coupling descent are unsigned",
        ),
        (
            "DNF2542_5_orbit_readout",
            "test-body and orbit readout",
            "A trajectory readout is admissible only as a downstream limit of the same matter action; an independent autoparallel Gamma_ind law is a new coupling.",
            "EXACT_CONDITIONAL_FILTER",
            "blocks importing GR geodesics by words while keeping a derivable route",
            "finite-body marker/domain and test-body limit not yet written as parent data",
        ),
        (
            "DNF2542_6_boundary_projective_limit",
            "boundary and projective limitation",
            "Downstream functor naturality does not itself kill boundary/improvement flux or projective trace coupling.",
            "LIMIT_EXPLICIT",
            "stops SRNG from eating a separate residual channel",
            "Delta_boundary and Delta_projective require their own zero proof or P4 policy",
        ),
        (
            "DNF2542_7_verdict",
            "derive SRNG now",
            "DNF2542_1 through DNF2542_5 would derive SRNG for source/readout sectors if parent-signed together.",
            "PARTIAL_DERIVATION_NOT_CORPUS_CLOSED",
            "SRNG is grounded in a precise downstream-functor theorem shape",
            "current corpus has contracts and conditional lemmas, not full parent observation policy",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "derivation_piece": piece,
            "formal_statement": statement,
            "status": status,
            "proof_gain": gain,
            "obstruction": obstruction,
        }
        for row_id, piece, statement, status, gain, obstruction in rows
    ]


def observation_functor_contract() -> list[dict[str, object]]:
    rows = [
        ("OFC2542_0_domain", "observation functor domain", "Readouts are maps O_i: Sol(Q_obs, boundary data, theta)->Reported_i.", "readouts depend on solved observed fields, not hidden parent representatives", "CONTRACT_WRITTEN_NONCLAIM"),
        ("OFC2542_1_action_separation", "no readout in parent variation", "O_i is not an argument of S_parent and contributes no Euler-Lagrange or hypermomentum current.", "clock/light/orbit readout cannot create Delta_i unless promoted to apparatus matter or residual", "CONTRACT_WRITTEN_NONCLAIM"),
        ("OFC2542_2_vertical_invariance", "vertical invariance", "If Dq(v)=0, then delta_v O_i=0 for all ordinary readouts.", "readout frame dependence is forbidden unless it descends through Q_obs or is residualized", "EXACT_IF_Q_NATURALITY_SIGNED"),
        ("OFC2542_3_no_gamma_slot", "no independent Gamma in readout", "O_i may use g_obs/e_obs and omega_LC[e_obs], but not Gamma_ind as an independent probe variable.", "turns SRNG into a consequence of observation object language", "CONTRACT_WRITTEN_NONCLAIM"),
        ("OFC2542_4_apparatus_backreaction", "apparatus backreaction rule", "If an instrument changes the source, it is included in ordinary matter/source action before variation; if not, it remains downstream.", "prevents sneaking source-current physics into a measurement map", "CONTRACT_WRITTEN_NONCLAIM"),
        ("OFC2542_5_status", "contract status", "OFC2542 is suitable as a private working parent-observation clause, not as a public derivation.", "supports disciplined local-branch development while retaining proof debt", "PRIVATE_CONTRACT_READY_NOT_DERIVED"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "contract_piece": piece,
            "clause": clause,
            "effect": effect,
            "status": status,
        }
        for row_id, piece, clause, effect, status in rows
    ]


def adoption_decision_matrix() -> list[dict[str, object]]:
    rows = [
        (
            "ADM2542_0_derivation_route",
            "derive SRNG from q-natural downstream observation",
            "BEST_ROUTE_BUT_NOT_CLOSED",
            "requires parent-signed q, observation policy, same-frame/tau/source selector and no-shadow clauses",
            "future theorem target only",
        ),
        (
            "ADM2542_1_private_adoption",
            "adopt SRNG/OFC as private working parent-action/observation clause",
            "RECOMMENDED_PRIVATE_WORKING_CLAUSE",
            "it is minimal, non-fitted, and blocks Gamma/readout leakage without altering data by hand",
            "internal local-branch calculations with explicit nonclaim label",
        ),
        (
            "ADM2542_2_reject_or_unresolved",
            "do not adopt SRNG",
            "FALLBACK_TO_P4_COMPONENT_BOUNDS",
            "then Delta_source/clock/light/orbit must be bounded with units and projection maps",
            "P4 residual row fill only",
        ),
        (
            "ADM2542_3_decision",
            "dual track",
            "PRIVATE_ADOPTION_PLUS_DERIVATION_AUDIT",
            "use SRNG internally as a named clause while continuing to derive it; never count it as public GR/Newton proof",
            "next checkpoint may use SRNG-gated branch and separately attack boundary/projective residuals",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "option": option,
            "status": status,
            "reason": reason,
            "allowed_use": allowed,
        }
        for row_id, option, status, reason, allowed in rows
    ]


def p4_status_after_srng_adoption() -> list[dict[str, object]]:
    rows = [
        ("P4A2542_0_SRNG_effect", "Delta_source+Delta_clock+Delta_light+Delta_orbit", "THEOREM_ZERO_INSIDE_PRIVATE_BRANCH_ONLY", "REQUIRES_P4_BOUNDS", "false_inside_private_branch_true_publicly"),
        ("P4A2542_1_spin", "Delta_spin", "UNCHANGED", "UNCHANGED", "true"),
        ("P4A2542_2_boundary", "Delta_boundary", "STILL_REQUIRES_BOUNDARY_CERTIFICATE", "STILL_REQUIRES_BOUNDARY_CERTIFICATE", "true"),
        ("P4A2542_3_projective", "Delta_projective", "STILL_REQUIRES_PROJECTIVE_POLICY", "STILL_REQUIRES_PROJECTIVE_POLICY", "true"),
        ("P4A2542_4_reduced_total", "Delta_abs_private_SRNG_branch", "Delta_abs -> Delta_matter/private + Delta_spin + Delta_boundary + Delta_projective", "full Delta_abs component queue retained", "true"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "component": component,
            "status_if_private_SRNG_used": private_status,
            "status_if_SRNG_rejected": rejected_status,
            "still_live": still_live,
        }
        for row_id, component, private_status, rejected_status, still_live in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2542_0_naturality_derived", "downstream observation naturality derived from parent MTS", "FAIL", "conditional theorem only"),
        ("CG2542_1_SRNG_public", "SRNG is public active theorem", "FAIL", "private working clause only"),
        ("CG2542_2_source_readout_zero_public", "Delta_source/clock/light/orbit zero for public claim", "FAIL", "zero only inside private adopted branch"),
        ("CG2542_3_boundary_projective_closed", "boundary/projective residuals closed", "FAIL", "still live"),
        ("CG2542_4_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "connection subgate improved but not complete"),
        ("CG2542_5_github", "safe public evidence update", "FAIL", "no GitHub evidence update"),
    ]
    return [stamp({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect}) for row_id, gate, status, effect in rows]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2542_0_private_as_public", "private SRNG adoption proves local GR publicly", "false", "private adoption is a named working clause, not a derivation from parent MTS"),
        ("REF2542_1_readout_backreaction_ignored", "all measurement apparatus is downstream by definition", "false", "apparatus that changes the source must be included as matter/source before variation or residualized"),
        ("REF2542_2_boundary_eaten_by_SRNG", "SRNG removes boundary and projective terms", "false", "downstream observation naturality does not kill integration-boundary or projective trace channels"),
        ("REF2542_3_import_orbits", "orbit equations can be imported from GR geodesics", "false", "orbit readout must come from the Hilbert/coframe test-body limit or remain a P4 residual"),
    ]
    return [stamp({"row_id": row_id, "claim": claim, "allowed": allowed, "reason": reason}) for row_id, claim, allowed, reason in rows]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2542_0_selected",
            "selected",
            "2543-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md",
            "scripts/Y5_R2FR_boundary_projective_residual_split_under_private_SRNG_2543.py",
            "with SRNG available as a private working clause, split remaining connection residuals into spin, boundary/improvement and projective trace",
            "retain each as explicit P4 residual unless zero/projected-silent/gauge policy closes",
        ),
        (
            "NEXT2542_1_parallel",
            "parallel",
            "2543b-Y5-R2FR-parent-observation-policy-derivation.md",
            "scripts/Y5_R2FR_parent_observation_policy_derivation_2543b.py",
            "try to parent-sign q-natural downstream observation instead of private adoption",
            "if not closed, keep SRNG/OFC private-only",
        ),
        (
            "NEXT2542_2_fallback",
            "fallback",
            "2543c-Y5-R2FR-P4-source-readout-component-bounds-if-SRNG-rejected.md",
            "scripts/Y5_R2FR_P4_source_readout_component_bounds_if_SRNG_rejected_2543c.py",
            "fill Delta_source/clock/light/orbit units and bounds if SRNG is rejected",
            "keep nonclaim until sourced and same-frame",
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
    add("VAL2542_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2542_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2542_02_outputs_exist", all(path.exists() for path in generated), "all 2542 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2542_03_csv_parse", parse_ok, parse_detail)

    audit = read_csv(outputs["naturality"])
    contract = read_csv(outputs["contract"])
    adoption = read_csv(outputs["adoption"])
    p4 = read_csv(outputs["p4_status"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])

    add(
        "VAL2542_04_naturality_not_closed",
        any(row["row_id"] == "DNF2542_7_verdict" and row["status"] == "PARTIAL_DERIVATION_NOT_CORPUS_CLOSED" for row in audit),
        "downstream naturality remains conditional",
    )
    add(
        "VAL2542_05_observation_contract_written",
        any(row["row_id"] == "OFC2542_5_status" and row["status"] == "PRIVATE_CONTRACT_READY_NOT_DERIVED" for row in contract),
        "observation functor contract written as private nonclaim",
    )
    add(
        "VAL2542_06_private_adoption_selected",
        any(row["row_id"] == "ADM2542_3_decision" and row["status"] == "PRIVATE_ADOPTION_PLUS_DERIVATION_AUDIT" for row in adoption),
        "private SRNG/OFC adoption selected with derivation audit",
    )
    add(
        "VAL2542_07_boundary_projective_still_live",
        any(row["row_id"] == "P4A2542_2_boundary" and row["still_live"] == "true" for row in p4)
        and any(row["row_id"] == "P4A2542_3_projective" and row["still_live"] == "true" for row in p4),
        "boundary and projective residuals remain live",
    )
    add(
        "VAL2542_08_local_claims_block",
        any(row["row_id"] == "CG2542_4_local_GR_Newton" and row["gate_status"] == "FAIL" for row in gates),
        "local GR/Newton claim gate remains false",
    )
    add(
        "VAL2542_09_next_boundary_projective",
        any(row["row_id"] == "NEXT2542_0_selected" for row in next_rows),
        "boundary/projective residual split selected next",
    )
    add(
        "VAL2542_10_github_blocked",
        any(row["row_id"] == "CG2542_5_github" and row["gate_status"] == "FAIL" for row in gates),
        "public GitHub evidence update remains blocked",
    )

    copy_rows = read_csv(outputs["copies"])
    add("VAL2542_11_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2542_12_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2542_13_formalization_untouched", formal_ok, formal_detail)
    add("VAL2542_14_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2542_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2542 valid: downstream observation naturality remains conditional, SRNG/OFC private adoption selected, boundary/projective residuals remain live" if overall else "one or more validation gates failed",
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
    audit = read_csv(outputs["naturality"])
    contract = read_csv(outputs["contract"])
    adoption = read_csv(outputs["adoption"])
    p4 = read_csv(outputs["p4_status"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2542 - Downstream Observation Functor Naturality Or SRNG Adoption

## Result

The downstream observation route is now cleanly framed:

`O_i: Sol(Q_obs) -> Readout_i`

If clocks, light, orbits and detector readouts are natural functors of solved observed fields, evaluated after variation, they cannot add an independent `Gamma_ind` source to `S_parent`.

That is an excellent theorem shape, but it is not parent-signed in the active corpus. So the disciplined move is dual-track:

1. use `SRNG/OFC` as a private working observation clause, and
2. keep trying to derive it from q-natural downstream observation.

Inside the private SRNG branch, `Delta_source+Delta_clock+Delta_light+Delta_orbit` are switched off by contract only. Publicly, they remain proof debt. Boundary/improvement and projective trace remain live either way.

## Downstream Naturality Derivation Audit

{table(["row_id", "derivation_piece", "status", "obstruction"], audit)}

## Observation Functor Contract

{table(["row_id", "contract_piece", "status", "effect"], contract)}

## SRNG Adoption Decision Matrix

{table(["row_id", "option", "status", "allowed_use"], adoption)}

## P4 Residual Status After SRNG Adoption

{table(["row_id", "component", "status_if_private_SRNG_used", "still_live"], p4)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], gates)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["naturality"])}`
- `{rel(outputs["contract"])}`
- `{rel(outputs["adoption"])}`
- `{rel(outputs["p4_status"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is a useful branch-control result. We can now calculate inside a private SRNG/OFC branch without pretending it is public proof. The live public residuals are sharper: spin, boundary/improvement, and projective trace, with boundary/projective selected next.
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
    write_csv(OUTPUTS["naturality"], downstream_naturality_audit())
    write_csv(OUTPUTS["contract"], observation_functor_contract())
    write_csv(OUTPUTS["adoption"], adoption_decision_matrix())
    write_csv(OUTPUTS["p4_status"], p4_status_after_srng_adoption())
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
