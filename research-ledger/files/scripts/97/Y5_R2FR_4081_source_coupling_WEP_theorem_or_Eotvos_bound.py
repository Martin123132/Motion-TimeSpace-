from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4081-Y5-R2FR-source-coupling-WEP-theorem-or-Eotvos-bound.md"

DECISION = "SOURCE_COUPLING_WEP_THEOREM_CONDITIONAL_NOT_PARENT_SIGNED_MICROSCOPE_EOTVOS_BOUND_SOURCED"

MICROSCOPE_ETA_CENTRAL = -1.5e-15
MICROSCOPE_ETA_STAT = 2.3e-15
MICROSCOPE_ETA_SYST = 1.5e-15
MICROSCOPE_ETA_COMBINED_SIGMA = math.sqrt(MICROSCOPE_ETA_STAT**2 + MICROSCOPE_ETA_SYST**2)
MICROSCOPE_ETA_ENVELOPE = abs(MICROSCOPE_ETA_CENTRAL) + MICROSCOPE_ETA_COMBINED_SIGMA

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4081_00_4080_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4080_NEXT_TARGET.csv",
        "4081-Y5-R2FR-source-coupling-WEP-theorem-or-Eotvos-bound.md",
        "4080 selected source coupling/WEP theorem or Eotvos bound.",
    ),
    "SRC4081_01_4080_runner": (
        SOURCE_DIR / "P8_Y5_R2FR_4080_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
        "source coupling remain open",
        "4080 aggregate keeps source coupling open.",
    ),
    "SRC4081_02_same_coframe": (
        SOURCE_DIR / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "UOC519_1_universal_matter_pullback",
        "same-coframe parent clause contains universal matter pullback.",
    ),
    "SRC4081_03_readout": (
        SOURCE_DIR / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "UOC519_2_readout_uses_same_e",
        "same-coframe parent clause ties clocks, photons, rulers and orbits to e_obs.",
    ),
    "SRC4081_04_ward": (
        SOURCE_DIR / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "UOC519_4_diffeomorphism_Ward_identity",
        "same-coframe parent clause records Ward identity route.",
    ),
    "SRC4081_05_coframe_contract": (
        SOURCE_DIR / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        "CFC943_2_matter_functor",
        "R10 coframe contract states ordinary matter action as functor of descended e_obs.",
    ),
    "SRC4081_06_source_label": (
        SOURCE_DIR / "P8_EM_source_label_forgetting_EM_Hodge_status.csv",
        "source_label_forgetting_functor",
        "source-label forgetting route is exact conditional but not parent signed.",
    ),
    "SRC4081_07_min_blocks": (
        SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "A511_2_universal_matter",
        "minimum local GR action blocks include universal matter source clause.",
    ),
    "SRC4081_08_derived_chain": (
        SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv",
        "WEP/source-frame closure",
        "derived chain keeps WEP/source-frame closure open.",
    ),
    "SRC4081_09_motion_frame_action": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv",
        "CARRIES_FORWARD_SAME_COFRAME_GATE",
        "4072 carries same-coframe matter/EM/stress/clock gate forward.",
    ),
    "SRC4081_10_ppn_route": (
        FORMALIZATION / "121-local-PPN-repair-route.md",
        "epsilon_PPN_total",
        "PPN route supplies residual vocabulary.",
    ),
}

WEB_SOURCES = [
    {
        "source_id": "WEB4081_0_microscope_prl",
        "title": "MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle",
        "authors": "Touboul et al. / MICROSCOPE Collaboration",
        "year": 2022,
        "url": "https://doi.org/10.1103/PhysRevLett.129.121102",
        "supporting_url": "https://arxiv.org/abs/2209.15487",
        "extracted_result": "eta(Ti,Pt) = [-1.5 +/- 2.3(stat) +/- 1.5(syst)] x 10^-15",
        "source_role": "finite external Eotvos/WEP source-coupling residual scale",
        "confidence": "peer_reviewed_PRL_and_arXiv_preprint",
    }
]

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4081_SOURCE_REGISTER.csv",
    "web_provenance": SOURCE_DIR / "P8_Y5_R2FR_4081_WEB_PROVENANCE.csv",
    "wep_theorem": SOURCE_DIR / "P8_Y5_R2FR_4081_SOURCE_COUPLING_WEP_THEOREM.csv",
    "eotvos_bound": SOURCE_DIR / "P8_Y5_R2FR_4081_EOTVOS_WEP_BOUND.csv",
    "runner_update": SOURCE_DIR / "P8_Y5_R2FR_4081_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4081_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4081_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4081_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4081_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4081_VALIDATION.csv",
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
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path),
                "exists_or_recorded": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    for source in WEB_SOURCES:
        rows.append(
            {
                "source_id": source["source_id"],
                "source_type": "web_source",
                "path_or_url": source["url"],
                "exists_or_recorded": True,
                "needle": source["extracted_result"],
                "needle_found": True,
                "role": source["source_role"],
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def web_provenance_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source in WEB_SOURCES:
        row = dict(source)
        row["timestamp_utc"] = current_timestamp
        row["valid_for_claim"] = False
        rows.append(row)
    return rows


def wep_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "WEP4081_0_same_hilbert_source",
            "statement": "If all ordinary matter species couple only to the same observed coframe e_obs and species constants are quotient-owned rather than MTS/domain/source fields, then the Hilbert stress from delta S_m/delta e_obs is the universal source current for local Newton/PPN readout.",
            "proof_sketch": "A single variational variable e_obs defines one stress tensor. Since masses and material constants are not functions of hidden MTS fields, no species-specific fifth-force source appears in the matter variation.",
            "result": "EXACT_CONDITIONAL_UNIVERSAL_HILBERT_SOURCE_THEOREM",
            "current_MTS_status": "SAME_COFRAME_AND_MATTER_FUNCTOR_NOT_PARENT_SIGNED",
            "residual_effect": "source_label_leak can be theorem-zeroed only if the same-coframe functor is parent-owned before readout.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "WEP4081_1_WEP_geodesic_limit",
            "statement": "For minimally coupled compact test bodies in the same e_obs geometry, the point-particle limit follows e_obs/geodesic motion independent of composition, up to spin, self-energy, tidal, and higher-multipole corrections.",
            "proof_sketch": "Diffeomorphism invariance gives the same-frame Ward identity. In the monopole limit of conserved stress, acceleration is determined by the connection of g_obs, not by composition labels.",
            "result": "EXACT_CONDITIONAL_WEP_LIMIT_THEOREM",
            "current_MTS_status": "CONDITIONAL_NOT_CURRENT_MTS_DERIVED",
            "residual_effect": "epsilon_WEP_source_coupling can be theorem-zeroed only after source functor and same-readout clauses close.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "WEP4081_2_no_shadow_source_frame",
            "statement": "Any source, clock, charge, or orbital frame that affects an experiment is observable and must descend through the same Q_obs/e_obs or be retained as a finite residual.",
            "proof_sketch": "A hidden conformal/disformal/source label can otherwise tune measured GM, clock rates, and free-fall independently, which is exactly the smuggling route the same-coframe clause forbids.",
            "result": "NO_SHADOW_SOURCE_FRAME_RULE_RETAINED",
            "current_MTS_status": "POLICY_CLAUSE_WRITTEN_THEOREM_OPEN",
            "residual_effect": "frame/source leaks must be bounded by WEP/Eotvos and source-current tests.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "WEP4081_3_current_failure_to_promote",
            "statement": "The current corpus does not yet parent-sign q, e_obs, matter functor, species-constant ownership, EM/charge normalization, and variation order together.",
            "proof_sketch": "UOC519, CFC943, and STAT3523 mark these as conditional or not parent-signed.",
            "result": "SOURCE_COUPLING_ROUTE_NOT_CLOSED",
            "current_MTS_status": "LOCAL_GR_NEWTON_MAXWELL_SOURCE_CLAIM_BLOCKED",
            "residual_effect": "use Eotvos/WEP finite bound as residual scale rather than public source-coupling claim.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def eotvos_bound_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "BOUND4081_0_MICROSCOPE_Eotvos_Ti_Pt",
            "quantity": "epsilon_WEP_source_coupling_Eotvos",
            "theory_map": "species-dependent source-frame or matter-functor leakage would produce nonzero differential acceleration; MICROSCOPE eta(Ti,Pt) bounds this WEP/source-coupling residual",
            "central_value": MICROSCOPE_ETA_CENTRAL,
            "stat_uncertainty": MICROSCOPE_ETA_STAT,
            "syst_uncertainty": MICROSCOPE_ETA_SYST,
            "combined_one_sigma": MICROSCOPE_ETA_COMBINED_SIGMA,
            "one_sigma_envelope_abs": MICROSCOPE_ETA_ENVELOPE,
            "units": "dimensionless_Eotvos_ratio",
            "source_id": "WEB4081_0_microscope_prl",
            "observable_link": "MICROSCOPE Ti/Pt differential free fall / Weak Equivalence Principle",
            "valid_for_claim": False,
            "claim_use": "finite WEP/source-coupling residual scale only; not proof that MTS satisfies WEP",
            "timestamp_utc": current_timestamp,
        }
    ]


def runner_update_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "runner_id": "RUNUP4081_0_WEP_theorem",
            "quantity": "epsilon_source_label_leak",
            "old_score": "source coupling remain open",
            "new_score": "EXACT_CONDITIONAL_WEP_SOURCE_THEOREM_PARENT_UNSIGNED",
            "numeric_bound": "not_applicable_for_zero_theorem",
            "numeric_bound_units": "not_applicable",
            "aggregate_effect": "can become zero if same-coframe/matter-functor/species-constant clauses are parent signed",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4081_1_Eotvos_bound",
            "quantity": "epsilon_WEP_source_coupling_Eotvos",
            "old_score": "MISSING_WEP_BOUND",
            "new_score": "FINITE_EXTERNAL_MICROSCOPE_EOTVOS_SCALE",
            "numeric_bound": MICROSCOPE_ETA_ENVELOPE,
            "numeric_bound_units": "dimensionless_Eotvos_ratio",
            "aggregate_effect": "adds finite WEP/source-coupling residual scale; source theorem still not parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4081_2_aggregate",
            "quantity": "R_eff_GR",
            "old_score": "P0_G_DRIFT_AND_CALIBRATION_BOUNDED_STILL_BLOCKED",
            "new_score": "P0_WEP_BOUNDED_STILL_BLOCKED_BY_GEOMETRY_AND_EM",
            "numeric_bound": "not_applicable",
            "numeric_bound_units": "mixed",
            "aggregate_effect": "runner gains WEP scale; spatial metric, theta parent, B derivation, EM Hodge/Maxwell, and torsion normalization still block a local-GR/Maxwell claim",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4081_0",
            "decision": DECISION,
            "meaning": "universal Hilbert-source/WEP follows conditionally from one e_obs matter functor with source-blind species constants, but current MTS has not parent-signed the full functor; MICROSCOPE supplies a finite Eotvos residual scale",
            "forward_progress": "separates the source-coupling theorem from the empirical WEP leash",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "decision_id": "DEC4081_1",
            "decision": "SOURCE_COUPLING_NOW_BOUNDED_NOT_CLOSED",
            "meaning": "source/WEP leakage is no longer only symbolic, but the parent source functor is still an unsigned gate",
            "forward_progress": "adds a real finite P0 WEP row while preserving no-smuggling discipline",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4081_0_WEP_theorem",
            "claim": "same e_obs matter functor gives universal Hilbert source and WEP limit",
            "claim_allowed": True,
            "scope": "conditional mathematical theorem",
            "reason": "one variational coframe plus source-blind species constants gives one stress/source current",
            "not_allowed_as": "current MTS has derived universal source coupling",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4081_1_current_source",
            "claim": "current MTS parent signs universal source coupling",
            "claim_allowed": False,
            "scope": "parent local-GR/Newton/Maxwell source derivation",
            "reason": "same-coframe, matter functor, species constants, EM charge normalization, and variation order are not signed together",
            "not_allowed_as": "MTS-to-local-GR/Newton source pass",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4081_2_Eotvos_bound",
            "claim": "MICROSCOPE gives a finite WEP/Eotvos residual scale",
            "claim_allowed": True,
            "scope": "private nonclaim residual target",
            "reason": "eta(Ti,Pt) is constrained at the 10^-15 level",
            "not_allowed_as": "MTS satisfies WEP or source-coupling theorem",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4081_0",
            "next_target": "4082-Y5-R2FR-EM-Hodge-Maxwell-source-theorem-or-light-cone-bound.md",
            "script": "scripts/Y5_R2FR_4082_EM_Hodge_Maxwell_source_theorem_or_light_cone_bound.py",
            "why": "next goal-critical issue is Maxwell/EM stress: prove same e_obs Hodge/current source theorem or source finite light-cone/birefringence bounds",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4081_1",
            "next_target": "source_functor_parent_signature_later",
            "script": "fold_into_parent_action_work",
            "why": "source theorem is ready but needs parent action adoption, not another restatement",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_SOURCE_COUPLING_WEP_THEOREM_OR_EOTVOS_BOUND_4081",
            "checkpoint_id": 4081,
            "decision": DECISION,
            "status": "PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "4081 derives the conditional same-Hilbert-source/WEP theorem, keeps current MTS source coupling unsigned, and sources MICROSCOPE Eotvos/WEP as a finite residual scale.",
            "valid_for_claim": False,
            "github_action": False,
        }
    ]


def validate_sources(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in rows if not row["exists_or_recorded"]]
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


def validate_numeric_bounds(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    failures: List[str] = []
    for row in rows:
        for key in ["stat_uncertainty", "syst_uncertainty", "combined_one_sigma", "one_sigma_envelope_abs"]:
            try:
                value = float(row[key])
                if value <= 0:
                    failures.append(f"{row['bound_id']}:{key} not positive")
            except Exception:
                failures.append(f"{row['bound_id']}:{key} not numeric")
        if row["valid_for_claim"] is not False:
            failures.append(f"{row['bound_id']}:valid_for_claim not false")
    return not failures, "; ".join(failures) if failures else "Eotvos bounds numeric and nonclaim"


def validate_claim_scopes(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    allowed_scopes = {"conditional mathematical theorem", "private nonclaim residual target"}
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
        "current MTS parent signs universal source coupling', 'claim_allowed': True",
        "MICROSCOPE gives a finite WEP/Eotvos residual scale', 'claim_allowed': True, 'scope': 'parent local-GR/Newton/Maxwell source derivation",
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
    bounds: List[Dict[str, object]],
    claims: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    bounds_ok, bounds_detail = validate_numeric_bounds(bounds)
    no_public_ok, no_public_detail = validate_no_public_claim(row_groups)
    claim_scope_ok, claim_scope_detail = validate_claim_scopes(claims)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4081_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4081_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4081_02_numeric_bounds", "passed": bounds_ok, "detail": bounds_detail},
        {"check_id": "VAL4081_03_no_public_or_github_claim", "passed": no_public_ok, "detail": no_public_detail},
        {"check_id": "VAL4081_04_claim_scope", "passed": claim_scope_ok, "detail": claim_scope_detail},
        {
            "check_id": "VAL4081_05_WEP_theorem_conditional",
            "passed": "EXACT_CONDITIONAL_UNIVERSAL_HILBERT_SOURCE_THEOREM" in joined
            and "SOURCE_COUPLING_ROUTE_NOT_CLOSED" in joined,
            "detail": "source/WEP theorem exists but remains parent unsigned",
        },
        {
            "check_id": "VAL4081_06_Eotvos_bound",
            "passed": "FINITE_EXTERNAL_MICROSCOPE_EOTVOS_SCALE" in joined and "epsilon_WEP_source_coupling_Eotvos" in joined,
            "detail": "finite MICROSCOPE Eotvos/WEP bound is present",
        },
        {
            "check_id": "VAL4081_07_next_target",
            "passed": "4082-Y5-R2FR-EM-Hodge-Maxwell-source-theorem-or-light-cone-bound.md" in joined,
            "detail": "next target moves to EM Hodge/Maxwell source theorem",
        },
        {"check_id": "VAL4081_08_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4081 - Source Coupling WEP Theorem Or Eotvos Bound

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Source-Coupling Theorem

If all ordinary matter sees one observed coframe:

```text
S_m = sum_A S_A[psi_A, e_obs; m_A, q_A, ...]
partial_Phi m_A = partial_D m_A = partial_source m_A = 0
```

then variation with respect to that same `e_obs` defines one Hilbert source:

```text
T_a^mu := e_obs^{-1} delta S_m / delta e_obs^a_mu
```

and the same-frame Ward identity gives conserved stress in the same geometry. In the compact test-body monopole limit, free fall is composition independent.

So the WEP/source-coupling theorem is exact, but conditional.

## Why It Is Not Promoted

The current corpus still marks these as unsigned:

```text
q(Phi) -> e_obs descent
matter functor parent signature
species constants quotient/superselection owner
same clock/photon/orbit/source frame
EM charge/current normalization
variation order before orbital calibration
```

So current MTS does not yet claim universal source coupling.

## Eotvos Bound

MICROSCOPE gives:

```text
eta(Ti,Pt) = [{MICROSCOPE_ETA_CENTRAL:.1e} +/- {MICROSCOPE_ETA_STAT:.1e}(stat) +/- {MICROSCOPE_ETA_SYST:.1e}(syst)]
combined sigma = {MICROSCOPE_ETA_COMBINED_SIGMA:.3e}
one-sigma absolute envelope = {MICROSCOPE_ETA_ENVELOPE:.3e}
```

This becomes:

```text
epsilon_WEP_source_coupling_Eotvos <= {MICROSCOPE_ETA_ENVELOPE:.3e}
```

as a finite residual scale, not a theory pass.

## Runner Update

The runner now has finite scales for:

```text
Cassini gamma / reciprocal lock
alpha_1 preferred-frame leakage
Gdot/G drift
CODATA G calibration
MICROSCOPE WEP/source coupling
```

and a finite torsion scale with normalization pending.

Still open:

```text
spatial metric owner
theta parent
B^A derivation core
EM Hodge / Maxwell source coupling
torsion normalization map
```

## Decision

```text
same-Hilbert-source theorem = exact conditional
current source-coupling claim = false
MICROSCOPE Eotvos bound = sourced residual scale
```

## Sources

- MICROSCOPE Collaboration, `MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle`, DOI `10.1103/PhysRevLett.129.121102`, arXiv `2209.15487`.

## Next

`4082` should attack Maxwell/EM stress:

```text
same e_obs Hodge/current theorem
```

or source finite light-cone / birefringence / EM-Hodge residual bounds.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    web_provenance = web_provenance_rows(current_timestamp)
    theorem = wep_theorem_rows(current_timestamp)
    bounds = eotvos_bound_rows(current_timestamp)
    runner = runner_update_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["web_provenance"], web_provenance)
    write_csv(OUTPUTS["wep_theorem"], theorem)
    write_csv(OUTPUTS["eotvos_bound"], bounds)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["web_provenance"],
        OUTPUTS["wep_theorem"],
        OUTPUTS["eotvos_bound"],
        OUTPUTS["runner_update"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        web_provenance,
        theorem,
        bounds,
        runner,
        decisions,
        claims,
        next_targets,
        statuses,
    ]
    validation = validation_rows(sources, generated_csvs, row_groups, bounds, claims)
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
