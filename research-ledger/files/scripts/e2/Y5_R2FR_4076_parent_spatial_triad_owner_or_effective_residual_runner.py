from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4076-Y5-R2FR-parent-spatial-triad-owner-or-effective-residual-runner.md"

DECISION = "TRIAD_GAUGE_REPRESENTATIVE_THEOREM_BUILT_PARENT_SPATIAL_METRIC_OWNER_OPEN_EFFECTIVE_RESIDUAL_RUNNER_INSTANTIATED"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4076_00_4075_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4075_NEXT_TARGET.csv",
        "4076-Y5-R2FR-parent-spatial-triad-owner-or-effective-residual-runner.md",
        "4075 selected the parent spatial triad owner or residual runner target.",
    ),
    "SRC4076_01_4075_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4075_DECISION_GATE.csv",
        "RADIAL_THETA_REPAIR_CONDITIONAL",
        "4075 made the radial repair positive but left full 4D Theta open.",
    ),
    "SRC4076_02_4075_reconstruction": (
        SOURCE_DIR / "P8_Y5_R2FR_4075_COFRAME_RECONSTRUCTION_THEOREM.csv",
        "FULL_4D_THETA_FAILS_WITHOUT_PARENT_TRIAD",
        "4075 identified the missing full triad/frame owner.",
    ),
    "SRC4076_03_4075_smuggling": (
        SOURCE_DIR / "P8_Y5_R2FR_4075_THETA_SMUGGLING_AUDIT.csv",
        "FULL_4D_THETA_FAILS_WITHOUT_PARENT_TRIAD",
        "4075 forbids calling a Gram-Schmidt triad derived without parent owner.",
    ),
    "SRC4076_04_4075_scorer": (
        SOURCE_DIR / "P8_Y5_R2FR_4075_EFFECTIVE_GR_RESIDUAL_SCORER.csv",
        "epsilon_theta_parent",
        "4075 provided the effective-GR residual scorer vocabulary.",
    ),
    "SRC4076_05_4071_gauge": (
        SOURCE_DIR / "P8_Y5_R2FR_4071_LOCAL_MOTION_FRAME_GAUGE_TEST.csv",
        "FORCES_OMEGA_CONDITIONALLY",
        "4071 showed local frame rotations force a spin/motion-frame connection conditionally.",
    ),
    "SRC4076_06_4071_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4071_CARTAN_ORIGIN_THEOREM_ATTEMPT.csv",
        "EXACT_CONDITIONAL_THEOREM",
        "4071 gave the exact conditional local Poincare gauge theorem.",
    ),
    "SRC4076_07_4072_action": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv",
        "FORMAL_CANDIDATE_NOT_CURRENT_MTS_DERIVED",
        "4072 keeps the motion-frame gauge action as candidate, not current derivation.",
    ),
    "SRC4076_08_4072_variation": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_GAUGE_VARIATION_AND_FIELD_STRENGTHS.csv",
        "GAUGE_COVARIANCE_CHECK_PASSES_FORMALLY",
        "4072 verifies formal gauge covariance of e and g.",
    ),
    "SRC4076_09_no_abs_frame": (
        PROJECT / "core-mts-framework" / "relativity" / "mbt-special-relativity-a-respectful-extension-of-einstein.md",
        "No Absolute Reference Frame",
        "MTS/MBT source gives no-preferred-frame motivation.",
    ),
    "SRC4076_10_observer_map": (
        ROOT / "10-observer-map-symplectic-contract.md",
        "all matter sectors couple to the same observer coframe",
        "observer map requires same coframe across sectors.",
    ),
    "SRC4076_11_same_coframe": (
        SOURCE_DIR / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "conditional_clause_written_not_current_MTS_derived",
        "same-coframe clause remains conditional rather than parent proved.",
    ),
    "SRC4076_12_r10_coframe": (
        SOURCE_DIR / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        "not_parent_signed_currently",
        "R10 coframe coupling contract is not parent signed.",
    ),
    "SRC4076_13_min_local_blocks": (
        SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "A511_6_metric_readout",
        "minimum local GR action blocks define metric readout residuals.",
    ),
    "SRC4076_14_ppn_repair": (
        FORMALIZATION / "121-local-PPN-repair-route.md",
        "epsilon_PPN_total",
        "PPN repair route supplies residual gate vocabulary.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4076_SOURCE_REGISTER.csv",
    "triad_quotient": SOURCE_DIR / "P8_Y5_R2FR_4076_TRIAD_GAUGE_QUOTIENT_THEOREM.csv",
    "parent_owner_test": SOURCE_DIR / "P8_Y5_R2FR_4076_PARENT_SPATIAL_METRIC_OWNER_TEST.csv",
    "residual_runner_rows": SOURCE_DIR / "P8_Y5_R2FR_4076_EFFECTIVE_RESIDUAL_RUNNER_ROWS.csv",
    "residual_runner_output": SOURCE_DIR / "P8_Y5_R2FR_4076_EFFECTIVE_RESIDUAL_RUNNER_OUTPUT.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4076_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4076_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4076_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4076_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4076_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def triad_quotient_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "TQ4076_0_triad_gauge_representative",
            "statement": "If the parent owns a clock/rest-space pair (n_mu, h_mu_nu) and local SO(3) frame rotations act as E^i_mu -> R^i_j(x) E^j_mu with all non-spin observables depending only on h_mu_nu = delta_ij E^i_mu E^j_nu, then the spatial triad E^i_mu is a gauge representative, not a separate physical field to be derived.",
            "proof_sketch": "Two triads related by R(x) in SO(3) give the same h_mu_nu. Matter, rods, clocks, scalar stress, and Maxwell Hodge data that depend only on g/h cannot distinguish the representatives. The physical parent object is therefore the equivalence class [E] or h, while E is a local section used for calculations.",
            "result": "TRIAD_BURDEN_REDUCED_TO_PARENT_SPATIAL_METRIC_PLUS_FRAME_GAUGE",
            "current_MTS_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "TQ4076_1_spin_and_orientation_caveat",
            "statement": "For spinors, chiral terms, torsion, or orientation-sensitive couplings, the parent must also own the spin structure, orientation, and induced spin connection; otherwise the triad gauge quotient is incomplete.",
            "proof_sketch": "Spinorial matter couples to a spin connection built from the frame. Local Lorentz covariance removes frame-gauge dependence only if the connection and spin lift are parent-defined before matter variation.",
            "result": "SPIN_ORIENTATION_GATE_RETAINED",
            "current_MTS_status": "OPEN_FOR_PARTICLE_QUANTUM_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "TQ4076_2_translation_connection_not_removed",
            "statement": "Demoting the spatial triad to gauge representative does not derive B^A. The translational/solder connection still needs parent ownership or effective-GR demotion.",
            "proof_sketch": "SO(3) rotations identify triad representatives at fixed h, but B^A carries the local translation-compensator shift required by e^A = D X^A + B^A. That inhomogeneous law is independent of the spatial rotation quotient.",
            "result": "B_DERIVATION_GATE_UNCHANGED",
            "current_MTS_status": "OPEN_FROM_4074",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "TQ4076_3_effective_use_rule",
            "statement": "Using a triad in calculations is not smuggling if the document labels it as a representative of an already parent-owned h/e_obs equivalence class; it is smuggling if h/e_obs is imported from GR and then called MTS-derived.",
            "proof_sketch": "Gauge representatives can be chosen freely after the gauge-invariant object is owned. They cannot establish ownership of that object.",
            "result": "NO_SMUGGLING_RULE_SHARPENED",
            "current_MTS_status": "RULE_AVAILABLE_OWNER_STILL_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def parent_owner_test_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "test_id": "OWN4076_0_no_absolute_frame",
            "object": "local SO(3)/Lorentz frame gauge",
            "evidence": "no absolute reference frame language plus 4071 local-frame theorem",
            "passes_currently": False,
            "verdict": "MOTIVATION_NOT_PARENT_ACTION_SIGNATURE",
            "next_requirement": "parent action invariant under local frame rotations before matter/EM variation",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "OWN4076_1_spatial_metric",
            "object": "h_mu_nu or spatial rest-space metric",
            "evidence": "observer-map contract and radial T,S cell",
            "passes_currently": False,
            "verdict": "RADIAL_COMPONENTS_CONDITIONAL_FULL_H_NOT_PARENT_SIGNED",
            "next_requirement": "derive h_mu_nu as descended observed rest-space object q(Phi)->e_obs/h before readout",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "OWN4076_2_same_coframe",
            "object": "single e_obs/h used by matter, EM, clocks, orbits",
            "evidence": "same-coframe and R10 coframe contracts",
            "passes_currently": False,
            "verdict": "CONDITIONAL_CLAUSE_NOT_CURRENT_MTS_DERIVED",
            "next_requirement": "quotient coframe descent plus matter functor parent signature",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "OWN4076_3_triad_representative",
            "object": "E^i_mu representative at fixed h_mu_nu",
            "evidence": "mathematical orthonormal frame theorem",
            "passes_currently": True,
            "verdict": "GAUGE_REPRESENTATIVE_ALLOWED_AFTER_H_OWNER",
            "next_requirement": "do not use E^i_mu to prove h_mu_nu ownership",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "OWN4076_4_spin_connection",
            "object": "omega^AB or spin lift",
            "evidence": "4071/4072 formal local motion-frame gauge branch",
            "passes_currently": False,
            "verdict": "FORMAL_CANDIDATE_NOT_CURRENT_MTS_DERIVED",
            "next_requirement": "parent-sign local Lorentz/Poincare gauge action or retain torsion/spin residuals",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def residual_runner_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "RUN4076_0",
            "quantity": "epsilon_frame_gauge_quotient",
            "source_input": "TQ4076_0",
            "score_class": "CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "numeric_score": "MISSING_PARENT_ACTION_SIGNATURE",
            "priority": "P0",
            "runner_action": "block_public_claim_keep_residual_live",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "row_id": "RUN4076_1",
            "quantity": "epsilon_spatial_metric_owner",
            "source_input": "OWN4076_1",
            "score_class": "BLOCKED",
            "numeric_score": "MISSING_FULL_H_MUNU_DESCENT",
            "priority": "P0",
            "runner_action": "require quotient observed rest-space theorem",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "row_id": "RUN4076_2",
            "quantity": "epsilon_theta_parent",
            "source_input": "P8_Y5_R2FR_4075_EFFECTIVE_GR_RESIDUAL_SCORER.csv",
            "score_class": "BLOCKED_BY_H_OWNER",
            "numeric_score": "NOT_NUMERIC",
            "priority": "P0",
            "runner_action": "cannot aggregate as evidence",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "row_id": "RUN4076_3",
            "quantity": "epsilon_B_derivation",
            "source_input": "P8_Y5_R2FR_4074_BFIELD_DERIVATION_ATTEMPT.csv",
            "score_class": "BLOCKED_BY_TRANSLATION_CONNECTION",
            "numeric_score": "NOT_NUMERIC",
            "priority": "P0",
            "runner_action": "requires B^A parent owner or effective demotion",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "row_id": "RUN4076_4",
            "quantity": "epsilon_reciprocal_lock",
            "source_input": "02-motion-load-local-GR-reduction.md",
            "score_class": "CONDITIONAL_ONLY",
            "numeric_score": "MISSING_PARENT_ORIGIN_OF_T2S1",
            "priority": "P0",
            "runner_action": "use gamma=1 only as conditional theorem",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "row_id": "RUN4076_5",
            "quantity": "epsilon_torsion_nonmetricity",
            "source_input": "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv",
            "score_class": "GATE_REQUIRED_NOT_PARENT_SIGNED",
            "numeric_score": "NOT_NUMERIC",
            "priority": "P0",
            "runner_action": "retain torsion/nonmetricity residual rows",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "row_id": "RUN4076_6",
            "quantity": "Delta_Hodge_EM",
            "source_input": "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
            "score_class": "DOWNSTREAM_CONSISTENCY_TEST",
            "numeric_score": "NOT_NUMERIC_IN_THIS_RUN",
            "priority": "P1",
            "runner_action": "score after e_obs owner/effective baseline fixed",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "row_id": "RUN4076_7",
            "quantity": "epsilon_clock_strain",
            "source_input": "P8_Y5_HILBERT_CURRENT_2467_CLOCK_COMPATIBILITY_GATE.csv",
            "score_class": "PARTIAL_STATIONARY_PASS_DYNAMIC_BLOCKED",
            "numeric_score": "NOT_NUMERIC_IN_THIS_RUN",
            "priority": "P1",
            "runner_action": "split stationary collar from dynamic clock branch",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def residual_runner_output_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "output_id": "OUT4076_0",
            "runner": "effective_GR_residual_runner",
            "aggregate_status": "P0_BLOCKED_NOT_NUMERIC",
            "numeric_aggregate_valid": False,
            "reason": "P0 rows contain parent-unsigned frame gauge, spatial metric owner, Theta parent, B derivation, reciprocal lock, and torsion/nonmetricity gates.",
            "allowed_use": "private triage of the next derivation or bound rows",
            "forbidden_use": "evidence that MTS passes local GR/PPN",
            "timestamp_utc": current_timestamp,
        },
        {
            "output_id": "OUT4076_1",
            "runner": "next_numeric_ready_condition",
            "aggregate_status": "NEEDS_REAL_BOUNDS_OR_THEOREM_ZEROS",
            "numeric_aggregate_valid": False,
            "reason": "No P0 gate has a sourced finite numeric residual or parent theorem-zero yet.",
            "allowed_use": "source-acquisition checklist for R10, PPN, clocks, EM Hodge, and orbital tests",
            "forbidden_use": "AIC/BIC-style comparison against GR",
            "timestamp_utc": current_timestamp,
        },
    ]


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4076_0",
            "decision": DECISION,
            "meaning": "the triad itself can be treated as gauge bookkeeping once h/e_obs is parent-owned; the real unresolved owner is the observed rest-space/coframe equivalence class and local frame gauge action",
            "forward_progress": "reduces full triad derivation to spatial metric/coframe-class ownership plus spin/orientation caveats",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "decision_id": "DEC4076_1",
            "decision": "EFFECTIVE_RESIDUAL_RUNNER_INSTANTIATED_BUT_NUMERIC_AGGREGATE_BLOCKED",
            "meaning": "the residual runner now has concrete rows, but all P0 local-GR evidence remains blocked or conditional",
            "forward_progress": "turns the current local-GR gap into a structured runner instead of another prose missing-list",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4076_0_triad_gauge",
            "claim": "spatial triad is gauge representative at fixed h_mu_nu",
            "claim_allowed": True,
            "scope": "conditional mathematical theorem",
            "reason": "SO(3)-related triads define the same spatial metric and non-spin observables",
            "not_allowed_as": "parent ownership of h_mu_nu or full local GR",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4076_1_parent_h",
            "claim": "MTS parent owns full spatial metric/coframe class",
            "claim_allowed": False,
            "scope": "parent local-GR derivation",
            "reason": "same-coframe, R10 coframe descent, and observer rest-space owner remain conditional",
            "not_allowed_as": "MTS-to-GR pass",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4076_2_runner",
            "claim": "effective residual runner is instantiated",
            "claim_allowed": True,
            "scope": "private nonclaim triage",
            "reason": "rows are generated but numeric aggregate is blocked",
            "not_allowed_as": "empirical local-GR evidence",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4076_0",
            "next_target": "4077-Y5-R2FR-observed-rest-space-descent-or-first-numeric-residual-bound.md",
            "script": "scripts/Y5_R2FR_4077_observed_rest_space_descent_or_first_numeric_residual_bound.py",
            "why": "attack the real owner now isolated: q(Phi)->(n_mu,h_mu_nu,e_obs) descent; if it fails, source one finite P0 residual bound instead of adding more symbolic rows",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4076_1",
            "next_target": "spin_orientation_caveat_later",
            "script": "defer_until_particle_quantum_branch",
            "why": "spin/orientation matters for particles, but local classical PPN can first use non-spin h/e_obs ownership",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_PARENT_SPATIAL_TRIAD_OWNER_OR_EFFECTIVE_RESIDUAL_RUNNER_4076",
            "checkpoint_id": 4076,
            "decision": DECISION,
            "status": "PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "4076 proves the triad can be a gauge representative once h/e_obs is parent-owned, isolates observed rest-space descent as the true bottleneck, and instantiates the effective residual runner with P0 gates blocked rather than numeric evidence.",
            "valid_for_claim": False,
            "github_action": False,
        }
    ]


def validate_sources(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in rows if not row["exists"]]
    needles = [row["source_id"] for row in rows if not row["needle_found"]]
    return not missing and not needles, f"missing={missing}; needle_missing={needles}"


def validate_csv_parse(paths: List[Path]) -> Tuple[bool, str]:
    failures: List[str] = []
    for path in paths:
        try:
            with path.open("r", newline="", encoding="utf-8") as input_file:
                rows = list(csv.DictReader(input_file))
            if not rows:
                failures.append(f"{path.name}: empty")
        except Exception as exc:  # pragma: no cover
            failures.append(f"{path.name}: {exc}")
    return not failures, "; ".join(failures) if failures else "all generated CSVs parse"


def validate_claim_scopes(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    allowed_scopes = {"conditional mathematical theorem", "private nonclaim triage"}
    bad_rows = [
        row["claim_id"]
        for row in rows
        if row["claim_allowed"] is True and row["scope"] not in allowed_scopes
    ]
    return not bad_rows, f"bad_allowed_claim_scopes={bad_rows}"


def validate_no_public_claim(row_groups: List[List[Dict[str, object]]]) -> Tuple[bool, str]:
    text = str(row_groups)
    forbidden = [
        "public_claim': True",
        '"public_claim": True',
        "github_action': True",
        '"github_action": True',
        "MTS parent owns full spatial metric/coframe class', 'claim_allowed': True",
        "numeric_aggregate_valid': True",
    ]
    hits = [token for token in forbidden if token in text]
    return not hits, f"forbidden_public_claim_tokens={hits}"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
    claims: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    no_public_ok, no_public_detail = validate_no_public_claim(row_groups)
    claim_scope_ok, claim_scope_detail = validate_claim_scopes(claims)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4076_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4076_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4076_02_no_public_or_github_claim", "passed": no_public_ok, "detail": no_public_detail},
        {"check_id": "VAL4076_03_claim_scope", "passed": claim_scope_ok, "detail": claim_scope_detail},
        {
            "check_id": "VAL4076_04_triad_gauge_theorem",
            "passed": "TRIAD_BURDEN_REDUCED_TO_PARENT_SPATIAL_METRIC_PLUS_FRAME_GAUGE" in joined,
            "detail": "triad burden is reduced to h/e_obs ownership plus frame gauge",
        },
        {
            "check_id": "VAL4076_05_parent_h_open",
            "passed": "RADIAL_COMPONENTS_CONDITIONAL_FULL_H_NOT_PARENT_SIGNED" in joined,
            "detail": "full spatial metric/coframe owner remains open",
        },
        {
            "check_id": "VAL4076_06_runner_instantiated",
            "passed": "P0_BLOCKED_NOT_NUMERIC" in joined and "epsilon_spatial_metric_owner" in joined,
            "detail": "effective residual runner rows and blocked aggregate are present",
        },
        {
            "check_id": "VAL4076_07_next_target",
            "passed": "4077-Y5-R2FR-observed-rest-space-descent-or-first-numeric-residual-bound.md" in joined,
            "detail": "next target attacks observed rest-space descent or first numeric bound",
        },
        {"check_id": "VAL4076_08_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4076 - Parent Spatial Triad Owner Or Effective Residual Runner

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Result

4076 sharpens the full-coframe bottleneck.

The spatial triad itself does **not** have to be a new physical thing if the parent already owns the spatial rest metric/coframe class:

```text
h_mu_nu = delta_ij E^i_mu E^j_nu
E^i_mu -> R^i_j(x) E^j_mu
R(x) in SO(3)
```

All SO(3)-related triads give the same `h_mu_nu`. Therefore `E^i_mu` can be treated as a gauge representative, not a separately derived physical field.

That is real progress: the missing target is smaller now.

## What Still Must Be Owned

The parent must still own:

```text
n_mu              clock/rest one-form
h_mu_nu           spatial rest metric
[E^i_mu]          local SO(3) frame-equivalence class
e_obs             same observed coframe for matter, EM, clocks, and orbits
omega^AB          spin/frame connection if spinors, torsion, or local Lorentz transport are active
B^A               translation/solder compensator if the full Cartan route is claimed
```

So the burden changes from:

```text
derive every triad leg as a physical object
```

to:

```text
derive q(Phi) -> (n_mu, h_mu_nu, e_obs) plus local frame gauge invariance
```

## No-Smuggling Rule

Using a triad in calculations is allowed only after `h_mu_nu` or `e_obs` is parent-owned or explicitly effective.

Forbidden move:

```text
borrow h_mu_nu from GR
choose E^i_mu by Gram-Schmidt
call E^i_mu an MTS derivation of GR
```

Allowed move:

```text
parent owns h_mu_nu/e_obs
choose E^i_mu as local gauge representative
prove observables are SO(3)/Lorentz invariant
```

## Residual Runner

4076 also instantiates the effective-GR residual runner. It is not numeric evidence yet:

```text
aggregate_status = P0_BLOCKED_NOT_NUMERIC
```

The P0 blocked rows are:

```text
epsilon_frame_gauge_quotient
epsilon_spatial_metric_owner
epsilon_theta_parent
epsilon_B_derivation
epsilon_reciprocal_lock
epsilon_torsion_nonmetricity
```

This is the safe bridge to testing: local GR can be used as the baseline, while each MTS departure is either theorem-zeroed or bounded.

## Decision

```text
triad gauge theorem = built
parent full h/e_obs owner = still open
effective residual runner = instantiated but aggregate blocked
```

This is better than the previous state because the full tetrad problem is no longer one giant fog bank. The next target is the observed rest-space/coframe descent theorem.

## Next

`4077` should attack:

```text
q(Phi) -> (n_mu, h_mu_nu, e_obs)
```

If that cannot be derived, stop adding symbolic gates and source the first finite P0 residual bound instead.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    triad = triad_quotient_rows(current_timestamp)
    owner = parent_owner_test_rows(current_timestamp)
    runner_rows = residual_runner_rows(current_timestamp)
    runner_output = residual_runner_output_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["triad_quotient"], triad)
    write_csv(OUTPUTS["parent_owner_test"], owner)
    write_csv(OUTPUTS["residual_runner_rows"], runner_rows)
    write_csv(OUTPUTS["residual_runner_output"], runner_output)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["triad_quotient"],
        OUTPUTS["parent_owner_test"],
        OUTPUTS["residual_runner_rows"],
        OUTPUTS["residual_runner_output"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        triad,
        owner,
        runner_rows,
        runner_output,
        decisions,
        claims,
        next_targets,
        statuses,
    ]
    validation = validation_rows(sources, generated_csvs, row_groups, claims)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
