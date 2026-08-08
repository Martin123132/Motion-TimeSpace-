from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3976"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3976-Y5-R2FR-parent-SO3-boundary-symmetry-or-multipole-hair-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3976_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3976_PARENT_SO3_BOUNDARY_SYMMETRY_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_3976_SO3_PARENT_SIGNATURE_AUDIT.csv",
    "bounds": SRC / "P8_Y5_R2FR_3976_MULTIPOLE_HAIR_BOUND_ROWS.csv",
    "certificate": SRC / "P8_Y5_R2FR_3976_Z_SO3_CERTIFICATE_UPDATE.csv",
    "feed": SRC / "P8_Y5_R2FR_3976_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3976_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3976_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3976_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3976_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3976_VALIDATION.csv",
}

NEXT_DOC = "3977-Y5-R2FR-source-boundary-angular-moment-silence-or-multipole-profile-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3977_source_boundary_angular_moment_silence_or_multipole_profile_bound.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3976_00_3975_next", SRC / "P8_Y5_R2FR_3975_NEXT_TARGET.csv", "NEXT3975_0", "3975 handoff"),
        ("SRC3976_01_3975_parent_setup", SRC / "P8_Y5_R2FR_3975_BOUNDARY_SCALAR_SINGLET_SELECTION_THEOREM.csv", "SSS3975_0_parent_group_setup", "SO3 setup"),
        ("SRC3976_02_3975_scalar_zero", SRC / "P8_Y5_R2FR_3975_BOUNDARY_SCALAR_SINGLET_SELECTION_THEOREM.csv", "SSS3975_1_scalar_zero_mode", "scalar zero-mode theorem"),
        ("SRC3976_03_3975_vector_zero", SRC / "P8_Y5_R2FR_3975_BOUNDARY_SCALAR_SINGLET_SELECTION_THEOREM.csv", "SSS3975_2_vector_zero", "vector zero theorem"),
        ("SRC3976_04_3975_STF_zero", SRC / "P8_Y5_R2FR_3975_BOUNDARY_SCALAR_SINGLET_SELECTION_THEOREM.csv", "SSS3975_3_STF_tensor_zero", "STF zero theorem"),
        ("SRC3976_05_3975_verdict", SRC / "P8_Y5_R2FR_3975_BOUNDARY_SCALAR_SINGLET_SELECTION_THEOREM.csv", "SSS3975_5_current_verdict", "unsigned verdict"),
        ("SRC3976_06_3975_SO3_audit", SRC / "P8_Y5_R2FR_3975_SO3_PREMISE_AUDIT.csv", "SPA3975_0_SO3_parent", "SO3 parent audit"),
        ("SRC3976_07_3975_no_spurion", SRC / "P8_Y5_R2FR_3975_SO3_PREMISE_AUDIT.csv", "SPA3975_1_no_spurion", "no spurion audit"),
        ("SRC3976_08_3975_common_mode", SRC / "P8_Y5_R2FR_3975_SO3_PREMISE_AUDIT.csv", "SPA3975_2_common_mode", "common mode audit"),
        ("SRC3976_09_3975_arena", SRC / "P8_Y5_R2FR_3975_SO3_PREMISE_AUDIT.csv", "SPA3975_3_arena_certificate", "arena audit"),
        ("SRC3976_10_3975_coeff_scalar", SRC / "P8_Y5_R2FR_3975_BOUNDARY_MULTIPOLE_COEFFICIENT_REQUIREMENTS.csv", "BMC3975_0_scalar_multipoles", "scalar multipole coefficient"),
        ("SRC3976_11_3975_coeff_vector", SRC / "P8_Y5_R2FR_3975_BOUNDARY_MULTIPOLE_COEFFICIENT_REQUIREMENTS.csv", "BMC3975_1_vector_marker", "vector marker coefficient"),
        ("SRC3976_12_3975_coeff_STF", SRC / "P8_Y5_R2FR_3975_BOUNDARY_MULTIPOLE_COEFFICIENT_REQUIREMENTS.csv", "BMC3975_2_STF_tensor", "STF coefficient"),
        ("SRC3976_13_3975_feed", SRC / "P8_Y5_R2FR_3975_FEED_UPDATE.csv", "SSF3975_4_next", "3975 next feed"),
        ("SRC3976_14_3584_stationary", SRC / "P8_Y5_R2FR_3584_STATUS.csv", "PARENT_ESTAT_ROUTE_DERIVED_AS_UNIQUENESS_LEMMA_BUT_NOT_SIGNED", "stationary exterior route"),
        ("SRC3976_15_1176_SO3", SRC / "P8_Y5_R10_1176_DOMAIN_ISOTROPY_OWNER_ATTEMPT.csv", "DIO1176_1_SO3_scalar_irrep", "SO3 scalar irrep"),
        ("SRC3976_16_1176_noniso", SRC / "P8_Y5_R10_1176_DOMAIN_ISOTROPY_OWNER_ATTEMPT.csv", "DIO1176_2_nonisotropic_arenas", "nonisotropic arenas"),
        ("SRC3976_17_1176_no_cheat", SRC / "P8_Y5_R10_1176_GR_MULTIPOLE_GUARDS.csv", "MPG1176_1_no_spherical_cheat", "no spherical cheat"),
        ("SRC3976_18_1176_Bianchi", SRC / "P8_Y5_R10_1176_GR_MULTIPOLE_GUARDS.csv", "MPG1176_2_Bianchi_stress", "Bianchi stress guard"),
        ("SRC3976_19_1176_tracefree", SRC / "P8_Y5_R10_1176_TRACEFREE_SHEAR_BOUND_ROWS.csv", "TFB1176_0_tracefree_shear_norm", "tracefree shear norm"),
        ("SRC3976_20_1947_common", SRC / "P8_Y5_PARENT_QLOC_1947_BOUNDARY_KERNEL_ISOTROPY_ATTEMPT.csv", "BKI1947_1_common_mode_kernel", "common-mode kernel"),
        ("SRC3976_21_1947_warning", SRC / "P8_Y5_PARENT_QLOC_1947_BOUNDARY_KERNEL_ISOTROPY_ATTEMPT.csv", "BKI1947_2_rotational_kernel_warning", "rotational warning"),
        ("SRC3976_22_1300_scalar_noSTF", SRC / "P8_Y5_R10_1300_ISOTROPY_TRACEFREE_THEOREM_AUDIT.csv", "ISO1300_3_scalar_domain_no_STF_route", "scalar no-STF route"),
        ("SRC3976_23_1175_SO3", SRC / "P8_Y5_R10_1175_QCOH_PROJECTOR_OWNER_ATTEMPT.csv", "QPO1175_1_SO3_invariant_route", "SO3 invariant projector"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "SO3T3976_0_target",
            "claim_piece": "parent SO3 boundary symmetry",
            "mathematical_form": "E[Phi]=0 is covariant, boundary/source data B are SO3-invariant, no SO3-breaking spurion is in the parent object language, and the exterior boundary-value problem is unique modulo gauge",
            "derived_result": "for every R in SO3, R.Phi solves the same parent problem as Phi, hence R.Phi=gauge(Phi), so L_X Phi=0 modulo gauge",
            "status": "CONDITIONAL_UNIQUENESS_THEOREM_SHAPE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SO3T3976_1_source_moments",
            "claim_piece": "source angular moment silence",
            "mathematical_form": "Q_lm^source=0, B_lm^boundary=0, and E_lm^external=0 for all l>=1 before local readout",
            "derived_result": "source/boundary/external data are compatible with SO3; scalar-singlet route can activate",
            "status": "REQUIRED_NOT_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SO3T3976_2_no_spurion",
            "claim_piece": "no vector/frame/tidal spurion",
            "mathematical_form": "partial S_B/partial v_A=partial S_B/partial s_A=partial S_B/partial E_AB^TF=0 unless the corresponding coefficient row is retained",
            "derived_result": "no parent object can carry a preferred tangent direction or STF marker into the boundary action",
            "status": "REQUIRED_NOT_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SO3T3976_3_common_mode_kernel",
            "claim_piece": "boundary/nonlocal kernel common-mode",
            "mathematical_form": "K_AB(x,x')=K_0(x,x') gamma_AB, not f(r,r') n_A n_B or Hessian/dyad STF response",
            "derived_result": "P_TF K_B=0 and kernel-induced xi/gamma-slip hair is removed",
            "status": "SUFFICIENT_IF_PARENT_SIGNED_NOT_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SO3T3976_4_counterguard",
            "claim_piece": "stationary/spherical shortcut rejection",
            "mathematical_form": "stationarity or a chosen spherical averaging surface alone does not imply Q_lm=B_lm=E_lm=0 or common-mode K_AB",
            "derived_result": "prevents local PPN/R10 quietness by spherical cheat",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SO3T3976_5_current_verdict",
            "claim_piece": "current parent SO3 promotion",
            "mathematical_form": "current corpus has the uniqueness theorem shape but does not parent-sign angular moment silence, no-spurion grammar, common-mode kernel, or arena certificates",
            "derived_result": "Z_SO3_boundary remains false/unsigned; multipole bounds remain active",
            "status": "SO3_PARENT_SIGNATURE_NOT_CLOSED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SO3A3976_0_covariance", "parent exterior equations covariant under SO3/O3", "partial", "3584 gives K-invariant stationarity route, but SO3 angular group is not parent-signed", "derive SO3 action on parent boundary data"),
        ("SO3A3976_1_source_moments", "source angular moments vanish or are ordinary GR multipoles routed elsewhere", "missing", "no parent row sets Q_lm^source=0 for l>=1", "derive angular-moment silence or fill source multipole profile"),
        ("SO3A3976_2_boundary_moments", "boundary/corner angular moments vanish", "missing", "3975 staged epsilon_boundary_scalar_l_ge_1 and STF rows", "fill boundary multipole coefficients or prove no boundary angular data"),
        ("SO3A3976_3_external_tides", "external tidal/STF environment absent or routed to metric/GR sector", "missing", "1176 no-spherical-cheat and multipole guards remain active", "arena-specific tidal certificate or bound"),
        ("SO3A3976_4_no_spurion", "no tangent/vector/spin/frame spurion in S_B", "missing", "3975 no-spurion route is conditional", "prove no marker functor or keep vector_marker coefficient"),
        ("SO3A3976_5_common_kernel", "boundary/nonlocal kernels are algebraic common-mode", "conditional", "1947 common-mode safe but rotational kernel warning active", "prove common-mode or bound kernel STF"),
        ("SO3A3976_6_uniqueness", "exterior solution unique modulo gauge under the selected data", "conditional", "3584 uniqueness pattern exists but is unsigned", "derive operator uniqueness/no homogeneous radiative kernel"),
        ("SO3A3976_7_arena", "R10/PPN/lab/orbital arena uses parent-selected SO3 representative", "missing", "real arenas need not be SO3", "arena certificate or anisotropy bound"),
    ]
    return [
        {
            "audit_id": audit_id,
            "premise": premise,
            "current_status": status,
            "evidence": evidence,
            "repair_or_bound": repair,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, premise, status, evidence, repair in specs
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("MHB3976_0_source_multipole", "epsilon_source_l_ge_1", "sum_{l>=1,m} |Q_lm^source|/M_H_ref", "dimensionless", "source multipole profile or theorem Q_lm^source=0", "SO3A3976_1_source_moments"),
        ("MHB3976_1_boundary_multipole", "epsilon_boundary_scalar_l_ge_1", "sum_{l>=1,m} |Y_lm_boundary|/M_H_ref", "dimensionless", "boundary spherical harmonic profile or theorem B_lm=0", "BMC3975_0_scalar_multipoles"),
        ("MHB3976_2_vector_marker", "epsilon_boundary_vector_marker", "||V_marker||/M_H_ref", "dimensionless", "no-spurion theorem or tangent/spin/frame marker norm", "BMC3975_1_vector_marker"),
        ("MHB3976_3_STF_tensor", "epsilon_boundary_STF_tensor", "||Pi_B^TF||/M_H_ref", "dimensionless", "STF tensor norm or SO3/common-mode certificate", "BMC3975_2_STF_tensor"),
        ("MHB3976_4_kernel_STF", "epsilon_boundary_kernel_STF", "||P_TF K_boundary||/M_H_ref", "dimensionless", "common-mode kernel proof or kernel STF response bound", "BMC3975_3_kernel_STF"),
        ("MHB3976_5_arena_anisotropy", "epsilon_boundary_arena_anisotropy", "||Pi_actual-Pi_SO3|| ||K_B||/M_H_ref", "dimensionless", "arena geometry certificate or anisotropy envelope", "BMC3975_4_arena_anisotropy"),
        ("MHB3976_6_total_SO3_failure", "epsilon_SO3_failure_abs", "epsilon_source_l_ge_1+epsilon_boundary_scalar_l_ge_1+epsilon_boundary_vector_marker+epsilon_boundary_STF_tensor+epsilon_boundary_kernel_STF+epsilon_boundary_arena_anisotropy", "dimensionless", "all active multipole/vector/STF rows sourced or zero-certified", "Z_SO3_boundary"),
    ]
    return [
        {
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "required_input_or_theorem": requirement,
            "feeds_or_blocks": feeds,
            "current_status": "BOUND_ROW_READY_VALUES_OR_ZERO_CERTIFICATE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, symbol, formula, units, requirement, feeds in specs
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZSO3976_0_SO3", "Z_SO3_boundary", "covariant exterior + SO3 source/boundary data + no spurion + uniqueness", "conditional_theorem_ready", "not_parent_signed", "Z_scalar_zero_mode"),
        ("ZSO3976_1_no_spurion", "Z_no_spurion_vector", "no tangent/spin/frame/tidal spurion in parent S_B", "required", "missing", "Z_no_marker"),
        ("ZSO3976_2_common_mode", "Z_common_mode_kernel", "K_AB=K0 gamma_AB", "sufficient_condition_ready", "not_parent_signed", "Z_tracefree_tensor_zero"),
        ("ZSO3976_3_arena", "Z_arena_SO3", "specific test arena has parent-selected SO3 representative or finite anisotropy bound", "required", "missing", "PPN/R10/lab/orbital gates"),
        ("ZSO3976_4_total", "Z_scalar_zero_mode", "Z_SO3_boundary and scalar object language", "unchanged_conditional", "not_parent_signed", "BAC3974_0"),
        ("ZSO3976_5_bound_fallback", "epsilon_SO3_failure_abs", "no-cancellation sum of active SO3 failure rows", "fallback_ready", "values_missing", "Delta_PPN_source_abs"),
    ]
    return [
        {
            "certificate_id": certificate_id,
            "factor": factor,
            "requirement": requirement,
            "3976_update": update,
            "current_status": status,
            "feeds_or_blocks": feeds,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for certificate_id, factor, requirement, update, status, feeds in specs
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SO3F3976_0_ZSO3",
            "target": "Z_SO3_boundary",
            "update_formula": "covariant parent exterior + SO3 source/boundary/external data + no-spurion grammar + uniqueness => Z_SO3_boundary=1",
            "meaning": "SO3 promotion is now a precise theorem route rather than a spherical assumption",
            "status": "CONDITIONAL_THEOREM_READY_PARENT_SIGNATURE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SO3F3976_1_ZB",
            "target": "Z_B",
            "update_formula": "Z_SO3_boundary can help Z_scalar_zero_mode/Z_no_marker, but Z_no_normal_exchange and Z_derivative_silence remain independent",
            "meaning": "even a future SO3 proof would not by itself finish the boundary certificate",
            "status": "PARTIAL_CERTIFICATE_FEED_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SO3F3976_2_PPN",
            "target": "Delta_PPN_source_abs",
            "update_formula": "SO3 failure rows feed alpha_i, xi, gamma/STF slip, beta/source hair, and arena-specific local residuals through epsilon_SO3_failure_abs",
            "meaning": "multipole hair now has a compact no-cancellation envelope for local tests",
            "status": "PPN_FEED_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SO3F3976_3_next",
            "target": "source_boundary_angular_moment_silence",
            "update_formula": "derive Q_lm^source=B_lm^boundary=E_lm^external=0 for l>=1 or fill their profiles",
            "meaning": "the next derivation attacks the highest-leverage missing premise in the SO3 route",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3976_0_theorem",
            "status": "PARENT_SO3_UNIQUENESS_THEOREM_SHAPE_WRITTEN",
            "meaning": "SO3 follows if the parent exterior problem is covariant, SO3 data are parent-owned, no spurion exists, and uniqueness modulo gauge holds",
            "claim_status": "conditional_nonclaim",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3976_1_no_promotion",
            "status": "SO3_PARENT_SIGNATURE_NOT_CLOSED",
            "meaning": "stationarity/spherical averaging alone is rejected; source/boundary/external angular-moment silence and common-mode kernel are unsigned",
            "claim_status": "Z_SO3_blocked",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3976_2_bound",
            "status": "MULTIPOLE_HAIR_BOUND_ROWS_CREATED",
            "meaning": "if SO3 fails, source, boundary, vector, STF, kernel, and arena anisotropy rows now form epsilon_SO3_failure_abs",
            "claim_status": "values_or_zero_certificates_missing",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3976_0_sources",
            "gate": "source register",
            "requirement": "all cited source paths and needles found",
            "status": "PASS_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3976_1_SO3",
            "gate": "SO3 promotion",
            "requirement": "parent-signed covariant exterior, SO3 data, no spurion, common-mode kernel, uniqueness, and arena certificate",
            "status": "BLOCKED_PARENT_SIGNATURE_INCOMPLETE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3976_2_bounds",
            "gate": "multipole bound promotion",
            "requirement": "numeric/source-backed or theorem-zero source, boundary, vector, STF, kernel, and arena rows",
            "status": "VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3976_3_local_GR",
            "gate": "local GR",
            "requirement": "SO3/multipoles plus normal exchange, derivative silence, PiM/domain, EH/readout/source-coupling gates",
            "status": "LOCAL_GR_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3976_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive source/boundary/external angular-moment silence Q_lm=B_lm=E_lm=0 for l>=1 from the parent local branch, or fill the multipole profile bound rows",
            "success_condition": "the highest-pressure SO3 premise is parent-signed, or epsilon_source_l_ge_1 and epsilon_boundary_scalar_l_ge_1 receive source-backed/theorem-zero values",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PARENT_SO3_THEOREM_SHAPE_AND_MULTIPOLE_BOUND_ROWS_READY",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "SO3 boundary symmetry is reduced to parent covariant uniqueness plus SO3 source/boundary/no-spurion/common-mode data; current corpus does not sign those premises, so multipole hair bound rows remain active",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3976 - Parent SO3 Boundary Symmetry Or Multipole Hair Bound

Timestamp: `{timestamp}`

## Result

3976 writes the non-smuggled route to `SO3`:

```text
parent covariant exterior equations
+ SO3-invariant source/boundary/external data
+ no vector/frame/tidal spurion in the boundary object language
+ common-mode boundary/nonlocal kernel
+ uniqueness modulo gauge
=> parent SO3 boundary symmetry
```

Then 3975 can fire:

```text
Z_SO3_boundary => Z_scalar_zero_mode and Z_no_marker
```

## Current Verdict

The theorem shape is useful, but not signed. Stationarity or a chosen spherical averaging surface is not enough.

The missing pressure point is:

```text
Q_lm^source = B_lm^boundary = E_lm^external = 0 for l >= 1
```

plus no-spurion/common-mode kernel ownership.

## Bound Fallback

If `SO3` is not parent-signed, the local branch keeps:

```text
epsilon_SO3_failure_abs =
  epsilon_source_l_ge_1
+ epsilon_boundary_scalar_l_ge_1
+ epsilon_boundary_vector_marker
+ epsilon_boundary_STF_tensor
+ epsilon_boundary_kernel_STF
+ epsilon_boundary_arena_anisotropy
```

No local-GR claim is made.

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3976 - Parent SO3 Boundary Symmetry Or Multipole Hair Bound

- Timestamp: `{timestamp}`
- Status: `PARENT_SO3_THEOREM_SHAPE_AND_MULTIPOLE_BOUND_ROWS_READY`
- Theorem route:
  covariant exterior equations plus `SO3` source/boundary data, no spurion, common-mode kernel, and uniqueness modulo gauge imply parent `SO3` boundary symmetry.
- Current claim status: nonclaim, because angular moment silence and common-mode/no-spurion ownership are unsigned.
- Fallback:
  `epsilon_SO3_failure_abs = epsilon_source_l_ge_1 + epsilon_boundary_scalar_l_ge_1 + epsilon_boundary_vector_marker + epsilon_boundary_STF_tensor + epsilon_boundary_kernel_STF + epsilon_boundary_arena_anisotropy`.
- Important guard:
  stationarity or spherical averaging alone is not a proof.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3976 - Parent SO3 Boundary Symmetry Or Multipole Hair Bound"
    block = spine_block(timestamp)
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def all_rows(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    sources = source_register_rows(timestamp)
    return {
        "sources": sources,
        "theorem": theorem_rows(timestamp),
        "audit": audit_rows(timestamp),
        "bounds": bound_rows(timestamp),
        "certificate": certificate_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    theorem = rows["theorem"]
    audit = rows["audit"]
    bounds = rows["bounds"]
    certificate = rows["certificate"]
    feed = rows["feed"]
    decisions = rows["decision"]
    claims = rows["claim_gate"]
    next_target = rows["next"]

    def val(validation_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }

    parsed = True
    parse_detail = "generated CSV files parse cleanly"
    for path in generated_csvs:
        try:
            read_csv(path)
        except Exception as exc:
            parsed = False
            parse_detail = f"{path} failed to parse: {exc}"
            break

    theorem_statuses = {row["status"] for row in theorem}
    audit_premises = {row["premise"] for row in audit}
    bound_symbols = {row["symbol"] for row in bounds}
    certificate_factors = {row["factor"] for row in certificate}
    feed_targets = {row["target"] for row in feed}

    return [
        val("VAL3976_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3976_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3976_02_theorem_shape", {"CONDITIONAL_UNIQUENESS_THEOREM_SHAPE", "GUARD_ACTIVE", "SO3_PARENT_SIGNATURE_NOT_CLOSED"} <= theorem_statuses, "SO3 uniqueness theorem, guard, and unsigned verdict present"),
        val("VAL3976_03_audit_complete", {"source angular moments vanish or are ordinary GR multipoles routed elsewhere", "boundary/corner angular moments vanish", "external tidal/STF environment absent or routed to metric/GR sector", "boundary/nonlocal kernels are algebraic common-mode"} <= audit_premises, "SO3 parent signature audit covers source, boundary, external, and kernel premises"),
        val("VAL3976_04_bounds", {"epsilon_source_l_ge_1", "epsilon_boundary_scalar_l_ge_1", "epsilon_boundary_vector_marker", "epsilon_boundary_STF_tensor", "epsilon_boundary_kernel_STF", "epsilon_boundary_arena_anisotropy", "epsilon_SO3_failure_abs"} <= bound_symbols, "multipole/vector/STF fallback bound rows present"),
        val("VAL3976_05_certificate", {"Z_SO3_boundary", "Z_no_spurion_vector", "Z_common_mode_kernel", "Z_arena_SO3", "epsilon_SO3_failure_abs"} <= certificate_factors, "Z_SO3 certificate and fallback update present"),
        val("VAL3976_06_feed", {"Z_SO3_boundary", "Z_B", "Delta_PPN_source_abs", "source_boundary_angular_moment_silence"} <= feed_targets, "feeds reach SO3, Z_B, PPN, and next target"),
        val("VAL3976_07_decision", any(row["status"] == "PARENT_SO3_UNIQUENESS_THEOREM_SHAPE_WRITTEN" for row in decisions), "decision records SO3 theorem shape"),
        val("VAL3976_08_no_promotion", any(row["status"] == "SO3_PARENT_SIGNATURE_NOT_CLOSED" for row in decisions), "decision blocks SO3 promotion"),
        val("VAL3976_09_claim_gate", any(row["status"] == "BLOCKED_PARENT_SIGNATURE_INCOMPLETE" for row in claims), "claim gate blocks incomplete parent signature"),
        val("VAL3976_10_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to angular moment silence or profile bound"),
        val("VAL3976_11_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3976_12_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3976_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3976_14_spine_updated", SPINE_PATH.exists() and "3976 - Parent SO3 Boundary Symmetry Or Multipole Hair Bound" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3976_15_csv_parse", parsed, parse_detail),
        val("VAL3976_16_script_compile", True, "script compiled before validation write"),
        val("VAL3976_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["audit"], rows["audit"])
    write_csv(OUTPUTS["bounds"], rows["bounds"])
    write_csv(OUTPUTS["certificate"], rows["certificate"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3976 validation failed: {failed}")

    print(f"3976 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Parent SO3 theorem shape and multipole fallback rows assembled")


if __name__ == "__main__":
    run()
