from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2540"
BRANCH_ID = "MTS_R2FR_NOGAMMA_SLOT_MATTER_SOURCE_READOUT_AUDIT_2540"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2540-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2540_SOURCE_REGISTER.csv",
    "slots": RESIDUALS / "P8_Y5_NO_SHADOW_2540_GAMMA_SLOT_SECTOR_AUDIT.csv",
    "theorem": RESIDUALS / "P8_Y5_NO_SHADOW_2540_NO_GAMMA_THEOREM_STACK.csv",
    "p4": RESIDUALS / "P8_Y5_NO_SHADOW_2540_P4_DELTA_COMPONENT_QUEUE.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2540_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2540_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2540_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2540_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2540_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2540_VALIDATION.csv",
}

BRANCH_COPIES = {
    "slots": POST_ROOT / "source-intake" / "beta-source" / "docs" / "NoGamma_slot_sector_audit_2540_NONCLAIM.csv",
    "theorem": POST_ROOT / "source-intake" / "beta-source" / "docs" / "NoGamma_theorem_stack_2540_NONCLAIM.csv",
    "p4": POST_ROOT / "source-intake" / "local_bounds" / "P4_Delta_component_queue_2540_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "SOURCE_READOUT_NOGAMMA2540_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    ("SRC2540_0_2539_doc", "2539-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md", "NEXT2539_0_selected", "2539 selected no-Gamma slot audit"),
    ("SRC2540_1_2539_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2539_VALIDATION.csv", "VAL2539_OVERALL,PASS", "2539 validation anchor"),
    ("SRC2540_2_2539_no_gamma", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2539_NO_GAMMA_SLOT_AUDIT_SEED.csv", "NGS2539_6_verdict", "current no-Gamma slot seed"),
    ("SRC2540_3_2539_p4", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2539_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv", "P4R2539_0_hypermomentum_total", "current P4 hypermomentum fallback"),
    ("SRC2540_4_2375_doc", "2375-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md", "NGSA2375_9_verdict", "older no-Gamma sector audit precedent"),
    ("SRC2540_5_2375_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2375_VALIDATION.csv", "VAL2375_OVERALL", "2375 validation anchor"),
    ("SRC2540_6_2375_slots", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2375_GAMMA_SLOT_SECTOR_AUDIT.csv", "NGSA2375_9_verdict", "Gamma-slot sector audit precedent"),
    ("SRC2540_7_2375_theorem", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2375_NO_GAMMA_THEOREM_STACK.csv", "NGT2375_4_result", "no-Gamma theorem stack precedent"),
    ("SRC2540_8_2375_p4", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2375_P4_DELTA_COMPONENT_QUEUE.csv", "P4DQ2375_0_total", "P4 Delta component queue precedent"),
    ("SRC2540_9_2375_decision", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2375_DECISION_LEDGER.csv", "DEC2375_2_best_next", "decision precedent"),
    ("SRC2540_10_2375_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2375_NEXT_TARGET.csv", "NEXT2375_0_selected", "source/readout certificate next target precedent"),
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


def gamma_slot_sector_audit() -> list[dict[str, object]]:
    rows = [
        (
            "NGSA2540_0_stack_target",
            "total ordinary local branch",
            "Does S_total_ord contain an independent affine Gamma_ind argument anywhere in matter, source, clock, light, orbit, boundary or readout?",
            "EXACT_CONDITIONAL_THEOREM_STACK",
            "sector-by-sector parent argument list is not signed for source/readout/boundary/projective slots",
            "Delta_abs",
        ),
        (
            "NGSA2540_1_ordinary_matter",
            "ordinary matter",
            "Does ordinary matter use S_A[Psi_A,e_obs,omega_LC[e_obs],A_owned,theta_A] with no Gamma_ind?",
            "CONDITIONAL_SUPPORTED_BY_MUMC",
            "candidate source-blind/owned-coframe signature is private-not-derived and direct representative dependence still needs exclusion",
            "Delta_matter",
        ),
        (
            "NGSA2540_2_spinor_transport",
            "spinor and spin transport",
            "Is the spin connection omega_LC[e_obs] coframe-owned rather than an independent torsionful connection?",
            "CONDITIONAL_SPIN_GUARD_NOT_GLOBAL",
            "spin/torsion/nonmetricity alternatives are not parent-excluded for every ordinary sector",
            "Delta_spin",
        ),
        (
            "NGSA2540_3_EM_light",
            "EM and lightcone readout",
            "Does light/EM use owned gauge connection and metric null structure, not affine Gamma_ind?",
            "PARTIAL_GAUGE_OWNER_NOT_FULL_READOUT",
            "optical, Shapiro, ray and detector readout maps are not all written as downstream Gamma-free functionals",
            "Delta_light",
        ),
        (
            "NGSA2540_4_source_worldtube",
            "source mass and finite worldtube",
            "Does source support/GM/worldtube action contain no Gamma_ind, boundary torsion or source-only connection current?",
            "UNSIGNED_PRIMARY_LEAK_PATH",
            "finite-source boundary and measured-GM support map can still re-enter as non-Hilbert source current",
            "Delta_source",
        ),
        (
            "NGSA2540_5_clock_readout",
            "clock and frequency readout",
            "Are clocks downstream matter/gauge functionals of e_obs/g_obs and theta, not independent Gamma probes?",
            "UNSIGNED_READOUT_SLOT",
            "atomic clock, frequency transfer, synchronization and detector model argument lists are not parent-signed",
            "Delta_clock",
        ),
        (
            "NGSA2540_6_orbital_readout",
            "test-body and orbital readout",
            "Is orbital motion derived from the same LC/coframe action rather than an independent autoparallel Gamma_ind law?",
            "UNSIGNED_READOUT_SLOT",
            "geodesic/autoparallel choice and finite-body marker map remain explicit parent clauses to sign",
            "Delta_orbit",
        ),
        (
            "NGSA2540_7_boundary_domain",
            "boundary/domain/improvement terms",
            "Are boundary, domain and improvement terms either exact/projected silent or Gamma-free?",
            "UNSIGNED_PARALLEL_GATE",
            "worldtube flux, marker boundaries and improvement currents still need zero theorem or finite envelope",
            "Delta_boundary",
        ),
        (
            "NGSA2540_8_projective_trace",
            "projective trace",
            "Is the projective mode gauge, fixed, or unobservable in all source/readout sectors?",
            "UNSIGNED_PARALLEL_CAVEAT",
            "projective certificate/policy remains outside this no-Gamma proof",
            "Delta_projective",
        ),
        (
            "NGSA2540_9_verdict",
            "all sectors",
            "Can 2540 promote no-Gamma/no-hypermomentum for the whole local branch?",
            "NOT_PARENT_SIGNED_RETAIN_P4_COMPONENTS",
            "matter branch is promising, but source/readout/boundary/projective slots are still unsigned",
            "Delta_abs",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "sector": sector,
            "slot_question": question,
            "evidence_status": status,
            "open_gap": gap,
            "p4_component": component,
        }
        for row_id, sector, question, status, gap, component in rows
    ]


def no_gamma_theorem_stack() -> list[dict[str, object]]:
    rows = [
        (
            "NGT2540_0_variational_absence",
            "variable-absence lemma",
            "For an action S[y] whose domain excludes Gamma_ind, the functional derivative delta S / delta Gamma_ind is zero/vacuous in the reduced variable space.",
            "EXACT_MATH_CONDITIONAL",
            "sector action domain must actually exclude Gamma_ind",
        ),
        (
            "NGT2540_1_coframe_chain_rule",
            "coframe-owned connection lemma",
            "If omega_obs=omega_LC[e_obs], variation of omega is induced by variation of e_obs and is counted in the metric/coframe field equation, not an independent Gamma equation.",
            "EXACT_MATH_CONDITIONAL",
            "spinor and transport sectors must be explicitly written with omega_LC[e_obs]",
        ),
        (
            "NGT2540_2_sector_sum",
            "sector-sum lemma",
            "If each sector derivative delta S_i/delta Gamma_ind vanishes, then Delta_abs is zero without cancellation because every summand is individually zero.",
            "EXACT_MATH_CONDITIONAL",
            "all sector slots must be signed, not merely ordinary matter",
        ),
        (
            "NGT2540_3_no_reentry",
            "readout no-reentry lemma",
            "A readout map does not source Gamma if it is downstream of the variational problem and does not define an extra source-labelled action/current.",
            "CONDITIONAL_CONTRACT_NEEDED",
            "clock, light, orbit, boundary and marker maps need explicit downstream/no-current clauses",
        ),
        (
            "NGT2540_4_result",
            "2540 theorem result",
            "The no-Gamma theorem is mathematically sharp but remains a conditional branch until source/readout/boundary/projective slots are parent-signed or P4-bounded.",
            "CONDITIONAL_THEOREM_NOT_CORPUS_PROMOTED",
            "source/readout argument-list certificate or P4 component map",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "lemma": lemma,
            "statement": statement,
            "proof_status": status,
            "missing_parent_input": missing,
        }
        for row_id, lemma, statement, status, missing in rows
    ]


def p4_delta_component_queue() -> list[dict[str, object]]:
    rows = [
        (
            "P4DQ2540_0_total",
            "Delta_abs",
            "||Delta_matter|| + ||Delta_spin|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary|| + ||Delta_projective||",
            "all no-Gamma sector slots parent-signed",
            "MISSING_COMPONENT_ZERO_PROOFS_OR_BOUNDS",
            "hypermomentum norm or normalized arena-specific envelope",
        ),
        (
            "P4DQ2540_1_matter",
            "Delta_matter",
            "||delta S_matter / delta Gamma_ind||",
            "ordinary matter has no Gamma_ind slot",
            "ZERO_IF_PRIVATE_MUMC_BRANCH_ADOPTED_ELSE_BOUND",
            "hypermomentum norm",
        ),
        (
            "P4DQ2540_2_spin",
            "Delta_spin",
            "||spin/torsion/nonmetricity connection current||",
            "spin connection is omega_LC[e_obs] and no Einstein-Cartan/metric-affine branch is active",
            "MISSING_SPIN_BRANCH_EXCLUSION_OR_BOUND",
            "spin-current or normalized torsion envelope",
        ),
        (
            "P4DQ2540_3_source",
            "Delta_source",
            "||delta S_source/worldtube/GM / delta Gamma_ind||",
            "source support and GM calibration are downstream Hilbert/coframe functionals",
            "MISSING_SOURCE_WORLDTUBE_ARGUMENT_LIST",
            "source-current or normalized GM envelope",
        ),
        (
            "P4DQ2540_4_clock",
            "Delta_clock",
            "||delta S_clock/readout / delta Gamma_ind||",
            "clock model is downstream of Gamma-free matter/gauge action",
            "MISSING_CLOCK_ARGUMENT_LIST",
            "clock frequency residual envelope",
        ),
        (
            "P4DQ2540_5_light",
            "Delta_light",
            "||delta S_light/ray/detector / delta Gamma_ind||",
            "light propagation/readout uses owned EM and g_obs/LC null structure only",
            "MISSING_LIGHT_READOUT_ARGUMENT_LIST",
            "lightcone/Shapiro/deflection residual envelope",
        ),
        (
            "P4DQ2540_6_orbit",
            "Delta_orbit",
            "||delta S_orbit/test-body/readout / delta Gamma_ind||",
            "orbital readout is Hilbert matter motion in g_obs, not independent autoparallel law",
            "MISSING_ORBIT_ARGUMENT_LIST",
            "orbital/PPN residual envelope",
        ),
        (
            "P4DQ2540_7_boundary_projective",
            "Delta_boundary + Delta_projective",
            "||boundary/improvement Gamma current|| + ||projective trace coupling||",
            "compact support/improvement silence plus projective gauge/fixed/unobservable certificate",
            "MISSING_BOUNDARY_AND_PROJECTIVE_CERTIFICATE",
            "source-current or normalized projective envelope",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "component": component,
            "formal_definition": definition,
            "zero_switch": zero_switch,
            "status": status,
            "units": units,
        }
        for row_id, component, definition, zero_switch, status, units in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        (
            "DEC2540_0_theorem_result",
            "no-Gamma theorem is exact as a conditional sector-sum lemma",
            "variable absence plus coframe-owned connection gives zero hypermomentum without cancellation",
            "this is the right derivation route, not a numerical patch",
            "CONDITIONAL_MATH_READY",
        ),
        (
            "DEC2540_1_no_promotion",
            "do not promote Levi-Civita/no-hypermomentum yet",
            "source, clock, light, orbit, boundary and projective slots are not parent-signed",
            "retain P4 component queue and no public/local-GR claim",
            "RETAIN_P4_COMPONENTS",
        ),
        (
            "DEC2540_2_best_next",
            "write source/readout no-Gamma action-argument certificate next",
            "one explicit argument-list contract could close several leak paths at once",
            "if certificate fails, fill P4 Delta_source/clock/light/orbit units and maps",
            "SELECT_SOURCE_READOUT_ARGUMENT_LIST_NEXT",
        ),
        (
            "DEC2540_3_public_policy",
            "no GitHub evidence update from this checkpoint",
            "2540 is a private derivation/fallback gate, not a publishable GR-reduction result",
            "keep working in post-checkpoint-work",
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
        ("CG2540_0_no_gamma_active", "no-Gamma branch parent-signed for all sectors", "FAIL", "conditional theorem only"),
        ("CG2540_1_no_hypermomentum", "Delta_lambda^{mu nu}=0 for ordinary local branch", "FAIL", "source/readout slots unsigned"),
        ("CG2540_2_Levi_Civita", "Gamma_obs=LC(g_obs), T=0, Q=0 derived", "FAIL", "needs no-Gamma plus EH/Palatini/projective closure"),
        ("CG2540_3_P4_score", "P4 Delta components have numeric units/maps/bounds", "FAIL", "component queue only"),
        ("CG2540_4_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "connection and EH/GM gates still open"),
        ("CG2540_5_github_public_update", "safe to push as public evidence", "FAIL", "private checkpoint only"),
    ]
    return [stamp({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect}) for row_id, gate, status, effect in rows]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2540_0_conditional_as_active", "the no-Gamma theorem is now active in MTS", "false", "the theorem shape is proved but the sector argument list is not parent-signed"),
        ("REF2540_1_matter_closes_readout", "ordinary matter no-Gamma automatically closes clocks, light and orbits", "false", "readout maps can re-enter as source-labelled currents unless explicitly downstream/Gamma-free"),
        ("REF2540_2_ignore_source_worldtube", "source/worldtube Gamma slot can be ignored", "false", "Newton/GM matching depends on source support and finite-boundary behavior"),
        ("REF2540_3_p4_as_pass", "the P4 queue is an empirical pass", "false", "P4 rows still lack component values, units, projection kernels and arena bounds"),
        ("REF2540_4_github", "publish this as GR reduction evidence", "false", "2540 is a private structural audit; it does not close local GR/Newton"),
    ]
    return [stamp({"row_id": row_id, "claim": claim, "allowed": allowed, "reason": reason}) for row_id, claim, allowed, reason in rows]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2540_0_selected",
            "selected",
            "2541-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md",
            "scripts/Y5_R2FR_source_readout_noGamma_action_argument_certificate_2541.py",
            "explicitly list source, clock, light, orbit, boundary and readout action arguments and prove none contain Gamma_ind",
            "if any slot remains open, convert it to a P4 Delta component with units and projection map",
        ),
        (
            "NEXT2540_1_fallback",
            "fallback",
            "2541b-Y5-R2FR-P4-Delta-component-values-units-map.md",
            "scripts/Y5_R2FR_P4_Delta_component_values_units_map_2541b.py",
            "fill Delta_source/clock/light/orbit/boundary/projective components, units, weak-field map and arena bounds",
            "keep nonclaim until all source paths and same-frame projections are present",
        ),
        (
            "NEXT2540_2_parallel",
            "parallel",
            "2541c-Y5-R2FR-projective-trace-certificate-or-policy.md",
            "scripts/Y5_R2FR_projective_trace_certificate_or_policy_2541c.py",
            "prove projective trace is gauge, fixed, or unobservable across source/readout sectors",
            "otherwise retain projective residual policy",
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
    add("VAL2540_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2540_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2540_02_outputs_exist", all(path.exists() for path in generated), "all 2540 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2540_03_csv_parse", parse_ok, parse_detail)

    slots = read_csv(outputs["slots"])
    theorem = read_csv(outputs["theorem"])
    p4 = read_csv(outputs["p4"])
    decisions = read_csv(outputs["decision"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])

    add(
        "VAL2540_04_conditional_theorem_stack",
        any(row["row_id"] == "NGT2540_4_result" and row["proof_status"] == "CONDITIONAL_THEOREM_NOT_CORPUS_PROMOTED" for row in theorem),
        "conditional theorem result recorded without promotion",
    )
    add(
        "VAL2540_05_sector_slots_present",
        len(slots) >= 10 and any(row["row_id"] == "NGSA2540_9_verdict" for row in slots),
        "major matter/source/readout slots present",
    )
    add(
        "VAL2540_06_no_promotion",
        any(row["row_id"] == "NGSA2540_9_verdict" and row["evidence_status"].startswith("NOT_PARENT_SIGNED") for row in slots),
        "no-Gamma branch not promoted",
    )
    add(
        "VAL2540_07_p4_components_present",
        len(p4) >= 8 and any(row["row_id"] == "P4DQ2540_0_total" for row in p4),
        "P4 component queue covers matter/source/readout/boundary",
    )
    add(
        "VAL2540_08_next_certificate_selected",
        any(row["row_id"] == "DEC2540_2_best_next" and row["status"] == "SELECT_SOURCE_READOUT_ARGUMENT_LIST_NEXT" for row in decisions)
        and any(row["row_id"] == "NEXT2540_0_selected" for row in next_rows),
        "source/readout argument-list certificate selected next",
    )
    add(
        "VAL2540_09_local_claims_block",
        any(row["row_id"] == "CG2540_4_local_GR_Newton" and row["gate_status"] == "FAIL" for row in gates),
        "local GR/Newton claim gate remains false",
    )
    add(
        "VAL2540_10_github_blocked",
        any(row["row_id"] == "CG2540_5_github_public_update" and row["gate_status"] == "FAIL" for row in gates),
        "public GitHub evidence update remains blocked",
    )

    copy_rows = read_csv(outputs["copies"])
    add("VAL2540_11_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2540_12_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2540_13_formalization_untouched", formal_ok, formal_detail)
    add("VAL2540_14_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2540_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2540 valid: no-Gamma theorem sharpened as conditional sector-sum audit, P4 components retained, source/readout argument certificate selected next" if overall else "one or more validation gates failed",
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
    slots = read_csv(outputs["slots"])
    theorem = read_csv(outputs["theorem"])
    p4 = read_csv(outputs["p4"])
    decisions = read_csv(outputs["decision"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2540 - noGamma Slot Matter Source Readout Audit

## Result

The no-Gamma route is mathematically clean but not yet active.

The conditional theorem is:

If every ordinary/local sector has no independent `Gamma_ind` argument, then every `delta S_i / delta Gamma_ind` vanishes by variable absence, and `Delta_abs=0` without cancellation.

The ordinary matter branch is promising inside the private MUMC/owned-coframe branch, but the source/worldtube, clock, light, orbit, boundary and projective trace slots are not parent-signed. Therefore Levi-Civita/no-hypermomentum/local-GR are **not** promoted here.

The useful gain is that the next target is now concrete: write the source/readout action-argument certificate. If that certificate fails, the same rows become P4 component bounds.

## Gamma Slot Sector Audit

{table(["row_id", "sector", "evidence_status", "open_gap", "p4_component"], slots)}

## no-Gamma Theorem Stack

{table(["row_id", "lemma", "proof_status", "missing_parent_input"], theorem)}

## P4 Delta Component Queue

{table(["row_id", "component", "status", "zero_switch"], p4)}

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
- `{rel(outputs["slots"])}`
- `{rel(outputs["theorem"])}`
- `{rel(outputs["p4"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is the cleanest version of the connection route so far. We are no longer arguing vaguely about whether MTS "has GR"; we are auditing the action arguments sector by sector. If the next certificate closes, the spin/torsion connection gate gets much cleaner. If it fails, P4 becomes the honest residual branch.
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
    write_csv(OUTPUTS["slots"], gamma_slot_sector_audit())
    write_csv(OUTPUTS["theorem"], no_gamma_theorem_stack())
    write_csv(OUTPUTS["p4"], p4_delta_component_queue())
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
