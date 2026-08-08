from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3975"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3975-Y5-R2FR-boundary-scalar-singlet-selection-or-coefficient-acquisition.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3975_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3975_BOUNDARY_SCALAR_SINGLET_SELECTION_THEOREM.csv",
    "premise_audit": SRC / "P8_Y5_R2FR_3975_SO3_PREMISE_AUDIT.csv",
    "certificate": SRC / "P8_Y5_R2FR_3975_ZB_CERTIFICATE_UPDATE.csv",
    "coefficients": SRC / "P8_Y5_R2FR_3975_BOUNDARY_MULTIPOLE_COEFFICIENT_REQUIREMENTS.csv",
    "feed": SRC / "P8_Y5_R2FR_3975_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3975_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3975_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3975_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3975_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3975_VALIDATION.csv",
}

NEXT_DOC = "3976-Y5-R2FR-parent-SO3-boundary-symmetry-or-multipole-hair-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3976_parent_SO3_boundary_symmetry_or_multipole_hair_bound.py"


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
        ("SRC3975_00_3974_next", SRC / "P8_Y5_R2FR_3974_NEXT_TARGET.csv", "NEXT3974_0", "3974 handoff"),
        ("SRC3975_01_3974_contract_safe", SRC / "P8_Y5_R2FR_3974_PARENT_BOUNDARY_ACTION_CONTRACT.csv", "BAC3974_0_safe_boundary_action", "safe boundary action"),
        ("SRC3975_02_3974_contract_marker", SRC / "P8_Y5_R2FR_3974_PARENT_BOUNDARY_ACTION_CONTRACT.csv", "BAC3974_2_marker_exclusion", "marker exclusion"),
        ("SRC3975_03_3974_certificate", SRC / "P8_Y5_R2FR_3974_PARENT_BOUNDARY_ACTION_CONTRACT.csv", "BAC3974_5_certificate", "Z_B certificate"),
        ("SRC3975_04_3974_variation_vector", SRC / "P8_Y5_R2FR_3974_BOUNDARY_VARIATION_ZERO_PROOF.csv", "BVP3974_1_vector_absence", "vector absence proof"),
        ("SRC3975_05_3974_variation_total", SRC / "P8_Y5_R2FR_3974_BOUNDARY_VARIATION_ZERO_PROOF.csv", "BVP3974_4_total", "total proof"),
        ("SRC3975_06_3974_ownership_scalar", SRC / "P8_Y5_R2FR_3974_BOUNDARY_PREMISE_OWNERSHIP_AUDIT.csv", "BAO3974_0_scalar_zero_mode", "scalar zero-mode unsigned"),
        ("SRC3975_07_3974_ownership_marker", SRC / "P8_Y5_R2FR_3974_BOUNDARY_PREMISE_OWNERSHIP_AUDIT.csv", "BAO3974_2_marker_free", "marker-free unsigned"),
        ("SRC3975_08_owner_O0", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O0_representation_zero", "representation-zero attempt"),
        ("SRC3975_09_owner_O1", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O1_homogeneous_scalar_action", "homogeneous scalar attempt"),
        ("SRC3975_10_owner_O2", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O2_scalar_not_enough_warning", "scalar-not-enough warning"),
        ("SRC3975_11_owner_O4", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O4_no_marker_fields", "marker gap"),
        ("SRC3975_12_owner_O7", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O7_parent_owner_verdict", "old owner verdict"),
        ("SRC3975_13_repair_R1", SRC / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv", "R1_no_marker_exclusion", "repair marker exclusion"),
        ("SRC3975_14_DIO1176_1", SRC / "P8_Y5_R10_1176_DOMAIN_ISOTROPY_OWNER_ATTEMPT.csv", "DIO1176_1_SO3_scalar_irrep", "SO3 scalar irrep theorem shape"),
        ("SRC3975_15_DIO1176_2", SRC / "P8_Y5_R10_1176_DOMAIN_ISOTROPY_OWNER_ATTEMPT.csv", "DIO1176_2_nonisotropic_arenas", "nonisotropic arena warning"),
        ("SRC3975_16_MPG1176_1", SRC / "P8_Y5_R10_1176_GR_MULTIPOLE_GUARDS.csv", "MPG1176_1_no_spherical_cheat", "no spherical cheat guard"),
        ("SRC3975_17_MPG1176_2", SRC / "P8_Y5_R10_1176_GR_MULTIPOLE_GUARDS.csv", "MPG1176_2_Bianchi_stress", "Bianchi stress guard"),
        ("SRC3975_18_TFB1176_0", SRC / "P8_Y5_R10_1176_TRACEFREE_SHEAR_BOUND_ROWS.csv", "TFB1176_0_tracefree_shear_norm", "tracefree shear bound"),
        ("SRC3975_19_BKI1947_1", SRC / "P8_Y5_PARENT_QLOC_1947_BOUNDARY_KERNEL_ISOTROPY_ATTEMPT.csv", "BKI1947_1_common_mode_kernel", "common-mode kernel safe"),
        ("SRC3975_20_BKI1947_2", SRC / "P8_Y5_PARENT_QLOC_1947_BOUNDARY_KERNEL_ISOTROPY_ATTEMPT.csv", "BKI1947_2_rotational_kernel_warning", "rotational warning"),
        ("SRC3975_21_ISO1300_3", SRC / "P8_Y5_R10_1300_ISOTROPY_TRACEFREE_THEOREM_AUDIT.csv", "ISO1300_3_scalar_domain_no_STF_route", "scalar no-STF route"),
        ("SRC3975_22_QPO1175_1", SRC / "P8_Y5_R10_1175_QCOH_PROJECTOR_OWNER_ATTEMPT.csv", "QPO1175_1_SO3_invariant_route", "SO3 invariant projector route"),
        ("SRC3975_23_3584_status", SRC / "P8_Y5_R2FR_3584_STATUS.csv", "PARENT_ESTAT_ROUTE_DERIVED_AS_UNIQUENESS_LEMMA_BUT_NOT_SIGNED", "stationary exterior route"),
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
            "theorem_id": "SSS3975_0_parent_group_setup",
            "claim_piece": "parent SO3/O3 boundary symmetry setup",
            "mathematical_form": "G=SO(3) or O(3) acts transitively on each compact local S^2 boundary orbit, preserves tau_obs, n_mu, gamma_AB, and the parent boundary object language",
            "result": "THEOREM_PREMISE_DEFINED",
            "what_it_kills": "lets representation theory classify allowed boundary hair",
            "what_it_does_not_kill": "does not prove the actual parent branch owns this symmetry",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SSS3975_1_scalar_zero_mode",
            "claim_piece": "scalar singlet selection",
            "mathematical_form": "L_X Y=0 for all X in Lie(SO3) on S^2 => Y=Y_00 and D_A Y=0",
            "result": "REPRESENTATION_THEOREM_PASS_IF_PARENT_SO3",
            "what_it_kills": "angular scalar gradients and tracefree Hessian leakage from scalar boundary data",
            "what_it_does_not_kill": "time/radial/source dependence of the l=0 scalar",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SSS3975_2_vector_zero",
            "claim_piece": "no invariant tangent vector/marker",
            "mathematical_form": "Gamma(TS^2)^{SO3}=0, so an SO3-invariant parent boundary action has no tangent vector marker V_A",
            "result": "REPRESENTATION_THEOREM_PASS_IF_NO_SPURION",
            "what_it_kills": "V_B, boundary alpha1/alpha2 vector slots, and preferred-frame marker slots",
            "what_it_does_not_kill": "a parent-added external vector, spin marker, velocity marker, or coframe spurion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SSS3975_3_STF_tensor_zero",
            "claim_piece": "no invariant tracefree tensor",
            "mathematical_form": "Gamma(STF_2(T*S^2))^{SO3}=0, so Pi_B^{AB}=0 on a parent-owned SO3 scalar-singlet boundary",
            "result": "REPRESENTATION_THEOREM_PASS_IF_PARENT_SO3",
            "what_it_kills": "tracefree boundary shear and xi/STF leakage",
            "what_it_does_not_kill": "common-mode trace, normal flux, derivative drift, or anisotropic arenas not selected by the parent",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SSS3975_4_normal_flux_caveat",
            "claim_piece": "normal flux is scalar-singlet allowed",
            "mathematical_form": "J_B^nu = j_B P_loc^nu_rho n^rho or equivalent normal/radial scalar can be SO3-invariant and nonzero",
            "result": "CAVEAT_DERIVED",
            "what_it_kills": "prevents false promotion from SO3 symmetry alone",
            "what_it_does_not_kill": "alpha3 normal exchange; BAC3974_3 still needed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SSS3975_5_current_verdict",
            "claim_piece": "current MTS scalar-singlet selection",
            "mathematical_form": "current corpus has theorem shape, but lacks parent-owned SO3 boundary representative/no-spurion grammar for all local arenas",
            "result": "SELECTION_CERTIFICATE_UNSIGNED",
            "what_it_kills": "nothing claim-valid yet",
            "what_it_does_not_kill": "coefficient acquisition remains active for non-SO3, marker, normal-flux, and drift channels",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def premise_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SPA3975_0_SO3_parent", "Z_SO3_boundary", "parent selects SO3/O3 invariant compact local boundary representative before readout", "conditional_route_only", "3584 has stationary exterior route but not full SO3/isotropy ownership", "derive parent SO3 boundary symmetry or bound multipoles"),
        ("SPA3975_1_no_spurion", "Z_no_spurion_vector", "no tangent vector, spin, velocity, frame, or external-tide spurion enters S_B", "missing", "old O4 marker exclusion remains unsigned", "prove no marker functor or retain vector coefficient rows"),
        ("SPA3975_2_common_mode", "Z_common_mode_kernel", "nonlocal/boundary kernel acts as common-mode trace, not Hessian/dyad STF response", "conditional", "1947 warns rotational kernels can still make STF tensors", "prove algebraic common-mode or bound STF kernel"),
        ("SPA3975_3_arena_certificate", "Z_arena_SO3", "specific R10/PPN/lab/orbital arena uses a parent-selected SO3 representative or declares anisotropy", "missing", "1176 no-spherical-cheat guard active", "arena-by-arena certificate or coefficient acquisition"),
        ("SPA3975_4_GR_multipole_guard", "Z_multipoles_routed", "physical GR multipoles/shear are routed to the metric sector, not erased by boundary projection", "guard_active", "1176 says tracefree multipoles may be excluded only if retained elsewhere", "route multipoles or keep STF rows"),
        ("SPA3975_5_normal_flux", "Z_no_normal_exchange", "normal/radial scalar boundary exchange vanishes by Euler/Ward law", "missing", "SO3 allows scalar normal flux", "derive boundary Euler no-flux or fill alpha3 normal product"),
    ]
    return [
        {
            "audit_id": audit_id,
            "certificate_factor": factor,
            "requirement": requirement,
            "current_status": status,
            "evidence": evidence,
            "repair_or_next_test": repair,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, factor, requirement, status, evidence, repair in specs
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZBC3975_0_scalar_zero_mode", "Z_scalar_zero_mode", "Z_SO3_boundary and scalar zero-mode object language", "conditional_true_if_parent_SO3_signed", "not_parent_signed", "BAC3974_0"),
        ("ZBC3975_1_no_marker", "Z_no_marker", "Z_no_spurion_vector and no tangent/spin/velocity/frame marker", "conditional_true_if_no_spurion_signed", "not_parent_signed", "BAC3974_2"),
        ("ZBC3975_2_tracefree", "Z_tracefree_tensor_zero", "SO3 scalar-singlet plus common-mode kernel", "conditional_true_if_parent_SO3_and_common_mode", "not_parent_signed", "BHC3973_4_xi"),
        ("ZBC3975_3_normal", "Z_no_normal_exchange", "boundary Euler/Ward no-normal-flux law", "not_implied_by_SO3", "missing", "BAC3974_3"),
        ("ZBC3975_4_derivative", "Z_derivative_silence", "time/radial/frame/species derivative silence of scalar monopole", "not_implied_by_SO3", "missing", "BAC3974_4"),
        ("ZBC3975_5_total", "Z_B", "Z_scalar_zero_mode*Z_no_marker*Z_full_variation*Z_no_normal_exchange*Z_derivative_silence", "not_signed", "blocked", "CLG3974_1_ZB"),
    ]
    return [
        {
            "certificate_id": certificate_id,
            "factor": factor,
            "requirement": requirement,
            "3975_update": update,
            "current_status": status,
            "feeds_or_blocks": feeds,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for certificate_id, factor, requirement, update, status, feeds in specs
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("BMC3975_0_scalar_multipoles", "epsilon_boundary_scalar_l_ge_1", "dimensionless", "sum_{l>=1,m} |Y_lm_boundary|/M_H_ref", "source-backed spherical/multipole decomposition or parent SO3 zero certificate", "scalar angular gradients; tracefree Hessian leakage"),
        ("BMC3975_1_vector_marker", "epsilon_boundary_vector_marker", "dimensionless", "||V_marker||/M_H_ref", "source-backed tangent/spin/velocity/frame marker norm or no-spurion certificate", "alpha1;alpha2;alpha3 preferred-frame slots"),
        ("BMC3975_2_STF_tensor", "epsilon_boundary_STF_tensor", "dimensionless", "||Pi_B^TF||/M_H_ref", "source-backed STF/shear tensor norm or SO3/common-mode certificate", "xi;gamma slip;boundary shear"),
        ("BMC3975_3_kernel_STF", "epsilon_boundary_kernel_STF", "dimensionless", "||P_TF K_boundary||/M_H_ref", "common-mode theorem or kernel STF bound", "xi;gamma;R11 STF leakage"),
        ("BMC3975_4_arena_anisotropy", "epsilon_boundary_arena_anisotropy", "dimensionless", "||Pi_actual-Pi_SO3|| * ||K_B||/M_H_ref", "arena-specific domain/boundary geometry certificate or anisotropy bound", "R10;PPN;lab/orbital arena guard"),
    ]
    return [
        {
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "units": units,
            "formula": formula,
            "promotion_requirement": requirement,
            "observable_or_gate": observable,
            "current_status": "COEFFICIENT_ROW_READY_VALUES_OR_ZERO_CERTIFICATE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for coefficient_id, symbol, units, formula, requirement, observable in specs
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SSF3975_0_BAC3974",
            "target": "BAC3974_0_safe_boundary_action",
            "update_formula": "SO3 parent boundary symmetry + no-spurion grammar => scalar zero-mode boundary data with D_A Y=0",
            "meaning": "3975 gives the exact representation-theory route to the safe scalar-zero-mode premise",
            "status": "CONDITIONAL_ROUTE_SHARPENED_PARENT_SIGNATURE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SSF3975_1_BAC3974_marker",
            "target": "BAC3974_2_marker_exclusion",
            "update_formula": "Gamma(TS2)^SO3=0 if no vector/spurion arguments enter S_B",
            "meaning": "no-marker is no longer vague: any tangent/spin/velocity/frame argument is the exact failure mode",
            "status": "CONDITIONAL_ROUTE_SHARPENED_PARENT_SIGNATURE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SSF3975_2_ZB",
            "target": "Z_B",
            "update_formula": "3975 can supply Z_scalar_zero_mode and Z_no_marker only if parent SO3/no-spurion certificates are signed; Z_no_normal_exchange and Z_derivative_silence remain independent",
            "meaning": "scalar-singlet selection helps but does not close the whole boundary certificate",
            "status": "ZB_PARTIAL_ROUTE_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SSF3975_3_coefficients",
            "target": "boundary_coefficient_acquisition",
            "update_formula": "if SO3/no-spurion/common-mode fails, fill epsilon_boundary_scalar_l_ge_1, epsilon_boundary_vector_marker, epsilon_boundary_STF_tensor, epsilon_boundary_kernel_STF, epsilon_boundary_arena_anisotropy",
            "meaning": "coefficient acquisition is now organized by exact representation failures",
            "status": "FALLBACK_ROWS_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SSF3975_4_next",
            "target": "parent_SO3_boundary_symmetry",
            "update_formula": "derive parent SO3/O3 boundary symmetry and no-spurion grammar, or source multipole/STF/vector bounds",
            "meaning": "next target attacks the parent signature rather than circling the missing rows",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3975_0_theorem",
            "status": "SCALAR_SINGLET_REPRESENTATION_THEOREM_SHARPENED",
            "meaning": "SO3 parent boundary symmetry would force scalar zero-modes and remove tangent vector/STF boundary hair",
            "claim_status": "conditional_nonclaim",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3975_1_caveat",
            "status": "NORMAL_FLUX_AND_DRIFT_NOT_KILLED",
            "meaning": "SO3 symmetry can allow scalar normal flux and scalar time/radial drift, so alpha3/Gdot boundary rows remain independent",
            "claim_status": "ZB_not_closed",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3975_2_next",
            "status": "PARENT_SO3_OR_MULTIPOLE_BOUND_NEXT",
            "meaning": "the next useful step is parent-signing the boundary SO3/no-spurion grammar or filling the multipole/vector/STF coefficient rows",
            "claim_status": "private_derivation_continues",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3975_0_sources",
            "gate": "source register",
            "requirement": "all cited source paths and needles found",
            "status": "PASS_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3975_1_SO3",
            "gate": "scalar-singlet zero promotion",
            "requirement": "parent-owned SO3/O3 boundary representative, no-spurion grammar, and arena certificate",
            "status": "BLOCKED_PARENT_SO3_NOT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3975_2_ZB",
            "gate": "full boundary certificate",
            "requirement": "SO3/no-marker plus full variation, no normal exchange, and derivative silence",
            "status": "BLOCKED_ZB_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3975_3_coefficients",
            "gate": "finite coefficient fallback",
            "requirement": "source-backed multipole/vector/STF/kernel/arena anisotropy values or zero certificates",
            "status": "VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3975_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive parent SO3/O3 boundary symmetry and no-spurion grammar from the local stationary exterior/source configuration, or fill multipole/vector/STF boundary hair bounds",
            "success_condition": "Z_SO3_boundary and Z_no_spurion become parent-signed, or the representation-failure coefficient rows receive sourced values/zero certificates",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "SCALAR_SINGLET_SELECTION_THEOREM_AND_MULTIPOLE_FALLBACK_READY",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "SO3/no-spurion boundary symmetry would earn scalar zero-mode and no tangent-vector/STF hair, but parent ownership and normal-flux/derivative clauses remain open; multipole/vector/STF coefficient rows are staged",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3975 - Boundary Scalar Singlet Selection Or Coefficient Acquisition

Timestamp: `{timestamp}`

## Result

3975 proves the useful representation-theory route:

```text
parent-owned SO3/O3 boundary symmetry
+ no vector/spin/velocity/frame spurion
=> scalar boundary data are l=0 zero-modes
=> tangent vector boundary hair vanishes
=> trace-free tensor boundary hair vanishes
```

In symbols:

```text
L_X Y = 0 for all X in Lie(SO3) => D_A Y = 0
Gamma(TS2)^SO3 = 0
Gamma(STF_2(T*S2))^SO3 = 0
```

## Critical Caveat

SO3 symmetry does **not** kill every boundary problem. A scalar normal/radial flux and scalar time/radial drift can still be SO3-invariant:

```text
J_B != 0 is allowed by SO3 unless the boundary Euler/Ward law kills normal exchange
D_B != 0 is allowed unless derivative silence is parent-derived
```

So 3975 can sharpen `Z_scalar_zero_mode` and `Z_no_marker`, but it does not close full `Z_B`.

## Fallback Rows

If the parent SO3/no-spurion certificate fails, the active coefficient rows are:

```text
epsilon_boundary_scalar_l_ge_1
epsilon_boundary_vector_marker
epsilon_boundary_STF_tensor
epsilon_boundary_kernel_STF
epsilon_boundary_arena_anisotropy
```

## Decision

No local-GR claim is made. The next target is parent SO3/no-spurion boundary symmetry or multipole/vector/STF bounds.

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3975 - Boundary Scalar-Singlet Selection

- Timestamp: `{timestamp}`
- Status: `SCALAR_SINGLET_SELECTION_THEOREM_AND_MULTIPOLE_FALLBACK_READY`
- Theorem shape:
  parent-owned `SO3/O3` boundary symmetry plus no vector/spurion grammar gives scalar zero-modes and kills tangent vector/STF boundary hair.
- Caveat:
  `SO3` does not kill scalar normal flux or scalar derivative drift, so `Z_no_normal_exchange` and `Z_derivative_silence` remain independent.
- Fallback rows:
  `epsilon_boundary_scalar_l_ge_1`, `epsilon_boundary_vector_marker`, `epsilon_boundary_STF_tensor`, `epsilon_boundary_kernel_STF`, and `epsilon_boundary_arena_anisotropy`.
- Current claim status: nonclaim, because parent `SO3/no-spurion` boundary ownership is unsigned.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3975 - Boundary Scalar-Singlet Selection"
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
        "premise_audit": premise_audit_rows(timestamp),
        "certificate": certificate_rows(timestamp),
        "coefficients": coefficient_rows(timestamp),
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
    audit = rows["premise_audit"]
    certificate = rows["certificate"]
    coefficients = rows["coefficients"]
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

    theorem_results = {row["result"] for row in theorem}
    audit_factors = {row["certificate_factor"] for row in audit}
    certificate_factors = {row["factor"] for row in certificate}
    coefficient_symbols = {row["symbol"] for row in coefficients}
    feed_targets = {row["target"] for row in feed}

    return [
        val("VAL3975_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3975_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3975_02_theorem_shape", {"REPRESENTATION_THEOREM_PASS_IF_PARENT_SO3", "REPRESENTATION_THEOREM_PASS_IF_NO_SPURION", "CAVEAT_DERIVED", "SELECTION_CERTIFICATE_UNSIGNED"} <= theorem_results, "representation theorem, caveat, and unsigned verdict present"),
        val("VAL3975_03_audit_factors", {"Z_SO3_boundary", "Z_no_spurion_vector", "Z_common_mode_kernel", "Z_arena_SO3", "Z_multipoles_routed", "Z_no_normal_exchange"} <= audit_factors, "SO3/no-spurion/common-mode/arena/normal audit complete"),
        val("VAL3975_04_certificate_update", {"Z_scalar_zero_mode", "Z_no_marker", "Z_tracefree_tensor_zero", "Z_no_normal_exchange", "Z_derivative_silence", "Z_B"} <= certificate_factors, "Z_B certificate factors updated"),
        val("VAL3975_05_coefficients", {"epsilon_boundary_scalar_l_ge_1", "epsilon_boundary_vector_marker", "epsilon_boundary_STF_tensor", "epsilon_boundary_kernel_STF", "epsilon_boundary_arena_anisotropy"} <= coefficient_symbols, "fallback coefficient rows cover representation failures"),
        val("VAL3975_06_feed", {"BAC3974_0_safe_boundary_action", "BAC3974_2_marker_exclusion", "Z_B", "boundary_coefficient_acquisition", "parent_SO3_boundary_symmetry"} <= feed_targets, "feed reaches BAC3974, Z_B, coefficients, and next target"),
        val("VAL3975_07_decision", any(row["status"] == "SCALAR_SINGLET_REPRESENTATION_THEOREM_SHARPENED" for row in decisions), "decision records scalar-singlet theorem"),
        val("VAL3975_08_caveat_decision", any(row["status"] == "NORMAL_FLUX_AND_DRIFT_NOT_KILLED" for row in decisions), "decision records normal-flux/drift caveat"),
        val("VAL3975_09_claim_gate", any(row["status"] == "BLOCKED_PARENT_SO3_NOT_SIGNED" for row in claims), "claim gate blocks unsigned parent SO3"),
        val("VAL3975_10_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to parent SO3 or multipole hair bound"),
        val("VAL3975_11_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3975_12_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3975_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3975_14_spine_updated", SPINE_PATH.exists() and "3975 - Boundary Scalar-Singlet Selection" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3975_15_csv_parse", parsed, parse_detail),
        val("VAL3975_16_script_compile", True, "script compiled before validation write"),
        val("VAL3975_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["premise_audit"], rows["premise_audit"])
    write_csv(OUTPUTS["certificate"], rows["certificate"])
    write_csv(OUTPUTS["coefficients"], rows["coefficients"])
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
        raise SystemExit(f"3975 validation failed: {failed}")

    print(f"3975 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Boundary scalar-singlet selection theorem sharpened; coefficient fallback staged")


if __name__ == "__main__":
    run()
