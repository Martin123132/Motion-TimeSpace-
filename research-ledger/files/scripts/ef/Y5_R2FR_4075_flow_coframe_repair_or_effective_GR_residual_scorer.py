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
DOC_PATH = ROOT / "4075-Y5-R2FR-flow-coframe-repair-or-effective-GR-residual-scorer.md"

DECISION = "RADIAL_THETA_REPAIR_CONDITIONAL_FULL_4D_THETA_NOT_PARENT_SIGNED_EFFECTIVE_GR_RESIDUAL_SCORER_BUILT"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4075_00_4074_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4074_NEXT_TARGET.csv",
        "4075-Y5-R2FR-flow-coframe-repair-or-effective-GR-residual-scorer.md",
        "4074 selected the flow-coframe repair or residual scorer target.",
    ),
    "SRC4075_01_4074_signature": (
        SOURCE_DIR / "P8_Y5_R2FR_4074_FLOW_TO_SOLDER_SIGNATURE_TEST.csv",
        "FINITE_REPAIR_CONTRACT_IDENTIFIED",
        "4074 identified Theta^A as the finite repair contract.",
    ),
    "SRC4075_02_4074_derivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4074_BFIELD_DERIVATION_ATTEMPT.csv",
        "scalar_flow_cannot_be_B_compensator",
        "4074 proved scalar flow cannot be the B compensator.",
    ),
    "SRC4075_03_4074_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_4074_RESIDUAL_INTERFACE_UPDATE.csv",
        "epsilon_B_derivation",
        "4074 staged the effective residual interface.",
    ),
    "SRC4075_04_observer_map": (
        ROOT / "10-observer-map-symplectic-contract.md",
        "theta_0 = T c dt",
        "observer-map contract supplies radial clock/spatial coframe components.",
    ),
    "SRC4075_05_observer_requirements": (
        ROOT / "10-observer-map-symplectic-contract.md",
        "all matter sectors couple to the same observer coframe",
        "observer-map contract requires one coframe for all sectors.",
    ),
    "SRC4075_06_motion_load": (
        ROOT / "02-motion-load-local-GR-reduction.md",
        "T^2 S = 1",
        "motion-load local-GR branch supplies reciprocal routing condition.",
    ),
    "SRC4075_07_motion_load_status": (
        ROOT / "02-motion-load-local-GR-reduction.md",
        "parent origin of reciprocal routing = missing",
        "motion-load branch is conditional until reciprocal lock gets a parent origin.",
    ),
    "SRC4075_08_ppn_repair": (
        FORMALIZATION / "121-local-PPN-repair-route.md",
        "epsilon_PPN_total",
        "PPN repair file carries the residual-score vocabulary.",
    ),
    "SRC4075_09_testing_map": (
        FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "Local gravity / PPN",
        "testing map keeps local gravity as guardrail until GR-limit theorem exists.",
    ),
    "SRC4075_10_frame_theorem": (
        ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
        "not enough parent coframe/reference geometry",
        "R10 frame theorem blocks a parent-signed frame claim.",
    ),
    "SRC4075_11_em_hodge": (
        SOURCE_DIR / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
        "DHB3504_0_Delta_Hodge_EM",
        "EM/Hodge coframe mismatch remains a downstream residual.",
    ),
    "SRC4075_12_poynting": (
        SOURCE_DIR / "P8_EM_source_label_forgetting_EM_Hodge_status.csv",
        "Poynting_as_Maxwell_Hilbert_stress",
        "Poynting is downstream stress if Hodge/coframe are owned.",
    ),
    "SRC4075_13_clock_gate": (
        SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_CLOCK_COMPATIBILITY_GATE.csv",
        "MISSING_PARENT_CLOCK_EQUATION",
        "clock compatibility gate keeps dynamic clock strain open.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4075_SOURCE_REGISTER.csv",
    "theta_repair": SOURCE_DIR / "P8_Y5_R2FR_4075_THETA_REPAIR_ATTEMPT.csv",
    "reconstruction": SOURCE_DIR / "P8_Y5_R2FR_4075_COFRAME_RECONSTRUCTION_THEOREM.csv",
    "smuggling_audit": SOURCE_DIR / "P8_Y5_R2FR_4075_THETA_SMUGGLING_AUDIT.csv",
    "residual_scorer": SOURCE_DIR / "P8_Y5_R2FR_4075_EFFECTIVE_GR_RESIDUAL_SCORER.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4075_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4075_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4075_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4075_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4075_VALIDATION.csv",
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


def theta_repair_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "repair_id": "THETA4075_0_radial_observer_pair",
            "candidate": "Theta^0 = T c dt; Theta^1 = sqrt(S) dr",
            "input_data": "observer-map radial clock/spatial forms",
            "positive_result": "RADIAL_2D_THETA_CONDITIONAL_PASS",
            "remaining_gap": "only t-r sector; angular triad and local boosts are not supplied",
            "smuggling_risk": "LOW_FOR_RADIAL_2D_HIGH_FOR_FULL_4D",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "repair_id": "THETA4075_1_reciprocal_lock",
            "candidate": "T^2 S = 1",
            "input_data": "motion-load reciprocal clock/spatial routing",
            "positive_result": "PPN_GAMMA_ONE_IF_PARENT_LOCK_SIGNED",
            "remaining_gap": "reciprocal lock has no parent origin in current corpus",
            "smuggling_risk": "MEDIUM_IF_USED_AS_AXIOM",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "repair_id": "THETA4075_2_full_spatial_triad",
            "candidate": "Theta^i = E^i_mu dx^mu with h_mn = delta_ij E^i_m E^j_n",
            "input_data": "spatial metric/projector plus orientation plus local SO(3) gauge",
            "positive_result": "MATHEMATICAL_RECONSTRUCTION_EXISTS_LOCALLY",
            "remaining_gap": "E^i is a triad choice; MTS does not parent-own h_mn/orientation/SO(3) gauge from flow data alone",
            "smuggling_risk": "HIGH_UNLESS_PARENT_TRIAD_THEOREM_EXISTS",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "repair_id": "THETA4075_3_translation_split",
            "candidate": "B^A = Theta^A - D_omega X^A",
            "input_data": "Theta^A plus X^A plus omega^AB",
            "positive_result": "B_RECOVERY_IF_THETA_AND_CONNECTION_ARE_PARENT_OWNED",
            "remaining_gap": "X^A and omega^AB remain candidate gauge variables, not derived from MTS flow",
            "smuggling_risk": "HIGH_IF_USED_WITHOUT_GAUGE_ACTION_OWNER",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def reconstruction_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "REC4075_0_3plus1_local_coframe",
            "statement": "Given a nonzero clock one-form n_mu, positive spatial metric h_mu_nu on ker(n), orientation, and local SO(3) gauge freedom, one may locally choose E^i_mu such that h_mu_nu = delta_ij E^i_mu E^j_nu and define Theta^0 = c n, Theta^i = E^i.",
            "proof_sketch": "Choose a local orthonormal frame for the rank-three Riemannian bundle ker(n) by Gram-Schmidt or matrix square root; pair it with n to form a coframe.",
            "what_it_derives": "local coframe from clock plus spatial metric data",
            "what_it_does_not_derive": "the parent origin of n_mu, h_mu_nu, orientation, local SO(3)/boost gauge, omega^AB, or B^A transformation law",
            "status": "CONDITIONAL_MATHEMATICAL_THEOREM_NOT_MTS_PARENT_DERIVATION",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "REC4075_1_radial_weak_field",
            "statement": "In the radial observer cell, Theta^0 = T c dt and Theta^1 = sqrt(S) dr reconstruct ds^2_(t,r) = -(Theta^0)^2 + (Theta^1)^2; if T^2 S = 1 then the radial weak-field branch gives gamma = 1.",
            "proof_sketch": "Insert T^2 = 1 - 2U/c^2 and S = (1-L)^(-p); weak-field expansion gives S = 1 + 2pU/c^2 and gamma = p, while T^2 S = 1 fixes p = 1.",
            "what_it_derives": "radial metric coefficients and PPN gamma under reciprocal lock",
            "what_it_does_not_derive": "parent origin of reciprocal lock, full angular coframe, or B^A as translation compensator",
            "status": "RADIAL_CONDITIONAL_PASS_FULL_BRANCH_BLOCKED",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "REC4075_2_no_scalar_to_triad",
            "statement": "Clock/load scalar data determine at most norms or radial factors; they do not determine a full oriented spatial triad in a generic 3D rest space.",
            "proof_sketch": "A triad contains orientation and three independent one-forms up to SO(3), while scalar routing data give eigenvalues or radial coefficients only; anisotropic/shear/rotation information is absent.",
            "what_it_derives": "a dimension-count and covariance obstruction",
            "what_it_does_not_derive": "full Theta^A from scalar motion-load variables",
            "status": "FULL_4D_THETA_FAILS_WITHOUT_PARENT_TRIAD",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def smuggling_audit_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "SMUG4075_0_clock_form",
            "object": "clock one-form n_mu or tau_mu",
            "allowed_if": "defined by parent clock/action variation or bounded local inertial/stationary collar",
            "smuggled_if": "taken from GR metric proper time after the fact",
            "current_verdict": "PARTLY_CONDITIONAL_CLOCK_GATE_OPEN",
            "blocks_parent_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "audit_id": "SMUG4075_1_spatial_metric",
            "object": "h_mu_nu spatial rest metric",
            "allowed_if": "descends from parent observer map before matter/EM variation",
            "smuggled_if": "borrowed from the target GR metric or fitted PPN spatial coefficient",
            "current_verdict": "PARENT_SPATIAL_METRIC_NOT_SIGNED",
            "blocks_parent_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "audit_id": "SMUG4075_2_triads",
            "object": "E^i_mu spatial triad",
            "allowed_if": "local SO(3)/Lorentz frame gauge is owned by the parent action",
            "smuggled_if": "chosen by Gram-Schmidt from an already imported h_mu_nu and then called derived",
            "current_verdict": "FULL_4D_THETA_FAILS_WITHOUT_PARENT_TRIAD",
            "blocks_parent_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "audit_id": "SMUG4075_3_reciprocal_lock",
            "object": "T^2 S = 1",
            "allowed_if": "emerges from a parent conserved cell current, constraint multiplier, or true observer-splitting gauge redundancy",
            "smuggled_if": "imposed because Schwarzschild AB=1 or because gamma is already known",
            "current_verdict": "CONDITIONAL_USE_ONLY",
            "blocks_parent_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "audit_id": "SMUG4075_4_poynting",
            "object": "Poynting vector / EM stress",
            "allowed_if": "used as downstream Hodge/coframe residual after e_obs is fixed",
            "smuggled_if": "used to generate e_obs while relying on the Hodge star defined by e_obs",
            "current_verdict": "DOWNSTREAM_TEST_ONLY",
            "blocks_parent_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def residual_scorer_rows(current_timestamp: str) -> List[Dict[str, object]]:
    residuals = [
        ("RS4075_0", "epsilon_theta_parent", "1 until Theta^A is parent-owned; 0 only after coframe descent theorem", "local_GR;PPN;R10", "P0"),
        ("RS4075_1", "epsilon_B_derivation", "1 until B^A = Theta^A - D_omega X^A inherits the correct translation law from parent fields", "local_GR;PPN", "P0"),
        ("RS4075_2", "epsilon_reciprocal_lock", "absolute failure of parent proof for T^2 S = 1 or bounded deviation from reciprocal routing", "PPN;light_bending;orbital", "P0"),
        ("RS4075_3", "epsilon_torsion", "torsion mode amplitude or theorem-zero deficit in Einstein-Cartan to EH reduction", "PPN;spin;orbital", "P0"),
        ("RS4075_4", "epsilon_nonmetricity", "nonmetricity or disformal/coframe leakage relative to metric GR", "PPN;clock;R10", "P0"),
        ("RS4075_5", "epsilon_kappa_normalization", "unowned kappa_eff/Newton G normalization relative to measured G", "Newtonian;orbital;laboratory", "P0"),
        ("RS4075_6", "Delta_Hodge_EM", "EM Hodge/coframe mismatch including principal/skewon/axion/disformal components", "Maxwell;Poynting;light_cone", "P1"),
        ("RS4075_7", "epsilon_clock_strain", "dynamic tau/clock strain outside stationary or local inertial collars", "clocks;redshift;source_conservation", "P1"),
        ("RS4075_8", "source_label_leak", "non-universal source or charge label leakage before Hilbert variation", "WEP;Maxwell;source_coupling", "P1"),
        ("RS4075_9", "Qcoh_Noether_deformation", "observed-flow deformation residual away from parent-owned stationary Killing/no-flux branch", "local_GR;orbital;PPN", "P1"),
        ("RS4075_10", "Delta_ref_frame_profile_over_MH", "frame/coframe reference leakage for R10 and preferred-frame tests", "R10;WEP;preferred_frame", "P1"),
    ]
    rows: List[Dict[str, object]] = []
    for residual_id, quantity, definition, arena, priority in residuals:
        rows.append(
            {
                "residual_id": residual_id,
                "quantity": quantity,
                "definition": definition,
                "score_rule": "0=parent theorem closed; bounded numeric value=empirical residual; 1_or_BLOCKED=no parent owner",
                "aggregate_rule": "R_eff_GR = sqrt(sum_i w_i residual_i^2) with P0 gates reported separately",
                "arena": arena,
                "priority": priority,
                "current_status": "NONCLAIM_SCORER_ROW",
                "valid_for_claim": False,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4075_0",
            "decision": DECISION,
            "meaning": "the clock+spatial route gives a useful conditional radial coframe, but full 4D Theta^A still needs parent-owned spatial triad/frame gauge; use the residual scorer unless 4076 signs that owner",
            "forward_progress": "positive radial theorem, full 4D no-smuggling audit, and effective-GR residual scoring vector",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "decision_id": "DEC4075_1",
            "decision": "RESIDUAL_SCORER_IS_NOW_THE_SAFE_TESTING_BRIDGE",
            "meaning": "local tests can proceed as GR-baseline residual tests without pretending the coframe has been derived",
            "forward_progress": "R_eff_GR vector turns missing derivations into explicit, scoreable residuals",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4075_0_radial",
            "claim": "radial observer coframe can be reconstructed from T and S",
            "claim_allowed": True,
            "scope": "private conditional radial t-r cell only",
            "reason": "theta_0 and theta_1 are explicitly in the observer-map contract",
            "not_allowed_as": "full local GR derivation",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4075_1_full_theta",
            "claim": "full 4D Theta^A is derived from MTS flow",
            "claim_allowed": False,
            "scope": "full local GR parent derivation",
            "reason": "spatial triad, orientation, SO(3)/Lorentz gauge, and B^A transformation are not parent-signed",
            "not_allowed_as": "MTS derives GR",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4075_2_ppn_gamma",
            "claim": "gamma=1 follows if T^2 S = 1 is parent-derived",
            "claim_allowed": True,
            "scope": "conditional theorem",
            "reason": "weak-field expansion gives gamma=p and reciprocal lock gives p=1",
            "not_allowed_as": "empirical/local-GR pass until parent lock is sourced",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4075_3_effective_residuals",
            "claim": "effective GR residual scorer may be used privately",
            "claim_allowed": True,
            "scope": "private testing and triage",
            "reason": "it labels GR infrastructure as baseline rather than derived",
            "not_allowed_as": "public derivation claim",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4075_0",
            "next_target": "4076-Y5-R2FR-parent-spatial-triad-owner-or-effective-residual-runner.md",
            "script": "scripts/Y5_R2FR_4076_parent_spatial_triad_owner_or_effective_residual_runner.py",
            "why": "attack the exact remaining object: parent-owned spatial triad/SO(3)-Lorentz gauge; if it fails, instantiate the residual scorer with available local/EM/clock bounds",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4075_1",
            "next_target": "reciprocal_lock_parent_origin",
            "script": "defer_to_4076_or_parallel",
            "why": "T^2 S = 1 is the shortest route to gamma=1, but only if it comes from a parent constraint/current/gauge redundancy",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_FLOW_COFRAME_REPAIR_OR_EFFECTIVE_GR_RESIDUAL_SCORER_4075",
            "checkpoint_id": 4075,
            "decision": DECISION,
            "status": "PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "4075 gets a conditional radial Theta repair and gamma=1 route under T^2 S=1, but rejects full 4D Theta^A derivation without a parent-owned spatial triad/frame gauge; it builds the effective-GR residual scorer as the safe testing bridge.",
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
        except Exception as exc:  # pragma: no cover - validation path
            failures.append(f"{path.name}: {exc}")
    return not failures, "; ".join(failures) if failures else "all generated CSVs parse"


def validate_claim_scopes(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    bad_rows = [
        row["claim_id"]
        for row in rows
        if row["claim_allowed"] is True
        and row["scope"] not in {"private conditional radial t-r cell only", "conditional theorem", "private testing and triage"}
    ]
    return not bad_rows, f"bad_allowed_claim_scopes={bad_rows}"


def validate_no_public_claim(row_groups: List[List[Dict[str, object]]]) -> Tuple[bool, str]:
    text = str(row_groups)
    forbidden = [
        "public_claim': True",
        '"public_claim": True',
        "github_action': True",
        '"github_action": True',
        "full 4D Theta^A is derived from MTS flow', 'claim_allowed': True",
        "MTS derives GR",
    ]
    hits = [token for token in forbidden if token in text and token != "MTS derives GR"]
    public_derivation = "full 4D Theta^A is derived from MTS flow', 'claim_allowed': True" in text
    return not hits and not public_derivation, f"forbidden_public_claim_tokens={hits}; public_derivation={public_derivation}"


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
        {"check_id": "VAL4075_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4075_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4075_02_no_public_or_github_claim", "passed": no_public_ok, "detail": no_public_detail},
        {"check_id": "VAL4075_03_claim_scope", "passed": claim_scope_ok, "detail": claim_scope_detail},
        {
            "check_id": "VAL4075_04_radial_theta_positive",
            "passed": "RADIAL_2D_THETA_CONDITIONAL_PASS" in joined,
            "detail": "radial t-r Theta repair is conditionally positive",
        },
        {
            "check_id": "VAL4075_05_full_theta_blocked",
            "passed": "FULL_4D_THETA_FAILS_WITHOUT_PARENT_TRIAD" in joined,
            "detail": "full 4D coframe derivation stays blocked without parent triad",
        },
        {
            "check_id": "VAL4075_06_residual_scorer",
            "passed": "R_eff_GR = sqrt(sum_i w_i residual_i^2)" in joined and "epsilon_theta_parent" in joined,
            "detail": "effective-GR residual scorer is present",
        },
        {
            "check_id": "VAL4075_07_next_target",
            "passed": "4076-Y5-R2FR-parent-spatial-triad-owner-or-effective-residual-runner.md" in joined,
            "detail": "next target attacks parent spatial triad owner or residual runner",
        },
        {"check_id": "VAL4075_08_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4075 - Flow-Coframe Repair Or Effective GR Residual Scorer

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Result

4075 takes the `Theta^A` repair seriously rather than just saying "coframe missing".

The good news:

```text
Theta^0 = T c dt
Theta^1 = sqrt(S) dr
ds^2_(t,r) = -(Theta^0)^2 + (Theta^1)^2
```

is a clean conditional radial observer-cell coframe. Together with:

```text
T^2 S = 1
```

it gives the familiar weak-field PPN result:

```text
gamma = 1
```

because `S = (1-L)^(-p)` gives `gamma = p`, and reciprocal routing fixes `p = 1`.

## Where The Repair Fails

The full local GR branch needs four one-forms:

```text
Theta^A = (Theta^0, Theta^1, Theta^2, Theta^3)
```

A clock one-form plus radial routing only builds the `t-r` cell. To build full `Theta^A`, we need:

```text
n_mu
h_mu_nu on ker(n)
orientation
local SO(3)/Lorentz frame gauge
E^i_mu with h_mu_nu = delta_ij E^i_mu E^j_nu
omega^AB
B^A = Theta^A - D_omega X^A
```

The reconstruction theorem exists mathematically. But unless MTS owns those objects before borrowing GR, it is a tetrad import.

## The Exact Theorem

Given a nonzero clock one-form `n_mu` and a positive spatial metric `h_mu_nu` on `ker(n)`, one can locally choose a spatial triad `E^i_mu` such that:

```text
h_mu_nu = delta_ij E^i_mu E^j_nu
Theta^0 = c n
Theta^i = E^i
g_mu_nu = -Theta^0_mu Theta^0_nu + delta_ij Theta^i_mu Theta^j_nu
```

That proves a conditional coframe reconstruction theorem.

It does not prove MTS derives the coframe.

## Safe Testing Bridge

Until the parent spatial triad/frame gauge is signed, local tests should use:

```text
effective GR baseline + MTS residual scorer
```

with:

```text
R_eff_GR = sqrt(sum_i w_i residual_i^2)
```

and P0 residuals:

```text
epsilon_theta_parent
epsilon_B_derivation
epsilon_reciprocal_lock
epsilon_torsion
epsilon_nonmetricity
epsilon_kappa_normalization
```

plus downstream EM/clock/source/frame residuals:

```text
Delta_Hodge_EM
epsilon_clock_strain
source_label_leak
Qcoh_Noether_deformation
Delta_ref_frame_profile_over_MH
```

## Decision

4075 moves the work forward in a precise way:

```text
radial Theta repair = conditional pass
full 4D Theta derivation = blocked without parent triad/frame gauge
testing route = effective GR residual scorer, not public derivation claim
```

## Next

`4076` should attack the exact remaining object:

```text
parent-owned spatial triad / SO(3)-Lorentz frame gauge
```

If that cannot be derived, instantiate the residual scorer with the best available local, EM, clock, R10, and orbital bound rows.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    theta = theta_repair_rows(current_timestamp)
    reconstruction = reconstruction_rows(current_timestamp)
    smuggling = smuggling_audit_rows(current_timestamp)
    scorer = residual_scorer_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["theta_repair"], theta)
    write_csv(OUTPUTS["reconstruction"], reconstruction)
    write_csv(OUTPUTS["smuggling_audit"], smuggling)
    write_csv(OUTPUTS["residual_scorer"], scorer)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["theta_repair"],
        OUTPUTS["reconstruction"],
        OUTPUTS["smuggling_audit"],
        OUTPUTS["residual_scorer"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        theta,
        reconstruction,
        smuggling,
        scorer,
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
