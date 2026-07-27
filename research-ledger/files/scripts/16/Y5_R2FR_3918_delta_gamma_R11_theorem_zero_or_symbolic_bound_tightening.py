from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3918"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3918-Y5-R2FR-delta-gamma-R11-theorem-zero-or-symbolic-bound-tightening.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3918_SOURCE_REGISTER.csv",
    "routes": SRC / "P8_Y5_R2FR_3918_PTF_ZERO_THEOREM_ROUTES.csv",
    "gamma": SRC / "P8_Y5_R2FR_3918_DELTA_GAMMA_R11_THEOREM_AND_BOUND.csv",
    "bound_inputs": SRC / "P8_Y5_R2FR_3918_DELTA_GAMMA_R11_BOUND_INPUTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3918_GAMMA_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3918_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3918_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3918_VALIDATION.csv",
}

SLIP_EQUATION = "C_TF nabla^2(Psi_R11-Phi_R11) = -kappa_R P_TF[R11_ij]"
SLIP_SOLUTION = "Psi_R11-Phi_R11 = -(kappa_R/C_TF) nabla^{-2} P_TF[R11_ij]"
GAMMA_SOURCE_LAW = "delta_gamma_R11 ~= -(kappa_R/(C_TF*U)) nabla^{-2} P_TF[R11_ij]"
THEOREM_ZERO = "P_TF[R11_ij]=0 => Psi_R11-Phi_R11=0 => delta_gamma_R11=0"
BOUND = "|delta_gamma_R11| <= |kappa_R|/(|C_TF| |U_min|) ||nabla^{-2} P_TF[R11_ij]||"
NEXT_DOC = "3919-Y5-R2FR-beta-source-second-order-lock-or-common-mode-R11-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3919_beta_source_second_order_lock_or_common_mode_R11_bound.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
        ("SRC3918_00_target", SRC / "P8_Y5_R2FR_3917_NEXT_TARGET.csv", "NEXT3917_0", "3917 selected the P_TF theorem-zero target"),
        ("SRC3918_01_gamma_zero", SRC / "P8_Y5_R2FR_3917_DELTA_GAMMA_R11_FILL_ROWS.csv", "GAM3917_3_zero_route", "3917 theorem-zero gamma row"),
        ("SRC3918_02_gamma_source", SRC / "P8_Y5_R2FR_3917_DELTA_GAMMA_R11_FILL_ROWS.csv", "GAM3917_2_source_law", "3917 symbolic gamma source law"),
        ("SRC3918_03_slip", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_3_traceless_spatial_projection", "1944 traceless spatial slip equation"),
        ("SRC3918_04_solution", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_4_potential_solution_form", "1944 inverse-Laplacian solution"),
        ("SRC3918_05_law", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_5_delta_gamma_source_law", "1944 delta gamma source law"),
        ("SRC3918_06_common", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_6_common_mode_separation", "1944 common-mode separation"),
        ("SRC3918_07_zero", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_7_local_zero_route", "1944 P_TF zero target"),
        ("SRC3918_08_coeff", SRC / "P8_Y5_PARENT_QLOC_1944_R11_PROJECTION_COEFFICIENT_LEDGER.csv", "COEF1944_2_PTF", "P_TF coefficient ledger"),
        ("SRC3918_09_EH_traceless", SRC / "P8_Y5_R2FR_3901_NO_DISFORMAL_RESPONSE_EQUATION.csv", "RESP3901_1_EH_traceless", "EH no-slip traceless equation"),
        ("SRC3918_10_memory_quad", SRC / "P8_Y5_R2FR_3901_NO_DISFORMAL_RESPONSE_EQUATION.csv", "RESP3901_2_memory_quadratic", "memory anisotropic stress starts quadratic"),
        ("SRC3918_11_R11_linear", SRC / "P8_Y5_R2FR_3901_NO_DISFORMAL_RESPONSE_EQUATION.csv", "RESP3901_4_R11", "R11 linear silence candidate"),
        ("SRC3918_12_boundary_zero", SRC / "P8_Y5_R2FR_3905_LINEAR_COEFFICIENT_ZERO_ROWS.csv", "ZERO3905_4", "boundary TF linear zero in normal-form branch"),
        ("SRC3918_13_projector_zero", SRC / "P8_Y5_R2FR_3905_LINEAR_COEFFICIENT_ZERO_ROWS.csv", "ZERO3905_5", "projector TF linear zero in normal-form branch"),
        ("SRC3918_14_Kgamma", SRC / "P8_Y5_R2FR_3905_LINEAR_COEFFICIENT_ZERO_ROWS.csv", "ZERO3905_7", "linear gamma zero row in normal-form branch"),
        ("SRC3918_15_EH_selector", SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv", "EH3906_0_selector", "EH operator selector"),
        ("SRC3918_16_nonEH_filter", SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv", "EH3906_2_nonEH_filter", "non-EH filter"),
        ("SRC3918_17_fork_EH", SRC / "P8_Y5_R2FR_3916_R11_SELECTOR_FORK.csv", "FORK3916_0_EH", "3916 EH selector route"),
        ("SRC3918_18_fork_DZ", SRC / "P8_Y5_R2FR_3916_R11_SELECTOR_FORK.csv", "FORK3916_1_DZ", "3916 double-zero route"),
        ("SRC3918_19_fork_zero", SRC / "P8_Y5_R2FR_3916_R11_SELECTOR_FORK.csv", "FORK3916_2_zero", "3916 R11 zero consequence"),
        ("SRC3918_20_sigma", SRC / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv", "R11S3893_00_candidate_action", "3893 Sigma factorization route"),
        ("SRC3918_21_projector_escape", SRC / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv", "R11S3893_10_projector_domain_stress", "3893 projector escape"),
        ("SRC3918_22_boundary_cert", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_0_certificate", "3892 boundary certificate"),
        ("SRC3918_23_boundary_verdict", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_4_verdict", "3892 boundary parent-unsigned verdict"),
        ("SRC3918_24_JX", SRC / "P8_Y5_R2FR_3894_MEMORY_JX_COMPONENT_CLOSURE_GATE.csv", "JXG3894_6_total", "3894 memory source closure summary"),
        ("SRC3918_25_bloc", SRC / "P8_Y5_R2FR_3915_STATIONARY_LOCAL_BRANCH_CONTRACT.csv", "BLC3915_0_branch", "3915 B_loc branch contract"),
        ("SRC3918_26_ppn_gamma", SRC / "P8_Y5_R2FR_3915_CONDITIONAL_PPN_ZERO_VECTOR.csv", "PPNZ3915_0_gamma", "3915 conditional gamma zero"),
        ("SRC3918_27_validation", SRC / "P8_Y5_BRR545_3917_VALIDATION.csv", "VAL3917_13_no_pycache", "3917 validation handoff"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:650]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_route_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "PTF3918_0_EH_absence",
            "EH selector absence route",
            "If the public branch has only the EH metric/coframe operator plus topological terms, active non-EH R11 stress is absent; hence P_TF[R11_ij]=0.",
            "FORK3916_0_EH;EH3906_0_selector;EH3906_2_nonEH_filter",
            "parent adoption of the EH selector and no-extra-operator clause",
            "CONDITIONAL_THEOREM_ZERO",
        ),
        (
            "PTF3918_1_DZ_silence",
            "double-zero stress route",
            "If S_R11=int sqrt(-g) sum_A F_A(Sigma_loc) O_A with Sigma_loc=G_AB Y^A Y^B, F_A(0)=F_A'(0)=0, and no independent multiplier stress, then delta S_R11|_{Y=0}=0 and P_TF[R11_ij]=0.",
            "FORK3916_1_DZ;R11S3893_00_candidate_action",
            "global adoption of Y_loc ownership, finite operator coefficients, no multiplier stress, boundary/projector clauses",
            "CONDITIONAL_THEOREM_ZERO",
        ),
        (
            "PTF3918_2_EH_traceless_response",
            "linearized EH no-slip response",
            "The traceless spatial equation isolates gamma slip: only Pi_TF-like anisotropic stress can source Phi-Psi at linear order.",
            "RESP3901_1_EH_traceless;WFE1944_3_traceless_spatial_projection",
            "does not by itself zero P_TF; it tells us exactly what must be zeroed or bounded",
            "DERIVED_REDUCTION",
        ),
        (
            "PTF3918_3_strict_isotropy",
            "strict local isotropy route",
            "In an orthonormal local collar, if the retained R11 spatial residual has no local direction/shear so R11_ij=R_iso delta_ij/3, then P_TF[R11_ij]=R11_ij-delta_ij R11_kk/3=0.",
            "BLC3915_0_branch;PPNZ3915_0_gamma",
            "strict isotropy must mean no radial shear, no vector/domain marker, no anisotropic boundary/projector term; spherical symmetry alone is insufficient",
            "CONDITIONAL_THEOREM_ZERO_FOR_GAMMA_ONLY",
        ),
        (
            "PTF3918_4_spherical_shortcut_rejected",
            "rejected shortcut",
            "A merely spherical tensor may contain (n_i n_j-delta_ij/3) shear; therefore spherical symmetry is not enough to set P_TF=0.",
            "WFE1944_7_local_zero_route",
            "must prove isotropic stress/no-shear, not just spherical fields",
            "REJECT_SHORTCUT",
        ),
        (
            "PTF3918_5_boundary_projector_escape",
            "anisotropic escape channel",
            "Boundary, projector, domain-wall, and long-tail memory pieces can carry TF stress unless the 3892/3905 certificates are parent-signed or numerically bounded.",
            "ZERO3905_4;ZERO3905_5;R11S3893_10_projector_domain_stress;BC3892_4_verdict;JXG3894_6_total",
            "escape remains active outside the signed local branch",
            "BOUND_OR_CERTIFICATE_REQUIRED",
        ),
        (
            "PTF3918_6_common_mode_separation",
            "gamma/common-mode separation",
            "P_TF=0 kills the R11 slip and hence delta_gamma_R11, but it does not kill Phi_R11=Psi_R11 common-mode shifts; Xi_N, beta, ephemeris and source-normalization gates remain.",
            "WFE1944_6_common_mode_separation",
            "next work must control beta/source and common-mode Newtonian readout",
            "PROGRESS_WITH_REMAINING_TESTS",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "route": route,
            "statement": statement,
            "source_needles": needles,
            "remaining_gate": gate,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, route, statement, needles, gate, status in data
    ]


def gamma_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("GAM3918_0_slip_equation", "traceless slip equation", SLIP_EQUATION, "derived symbolic reduction from 1944", "DERIVED_INPUT"),
        ("GAM3918_1_slip_solution", "formal slip solution", SLIP_SOLUTION, "inverse-Laplacian domain remains an explicit bound input", "FORMAL_SOLUTION"),
        ("GAM3918_2_source_law", "gamma source law", GAMMA_SOURCE_LAW, "maps P_TF source directly to Cassini-style gamma residual", "SYMBOLIC_BOUND_READY"),
        ("GAM3918_3_theorem_zero", "gamma theorem-zero consequence", THEOREM_ZERO, "valid in EH-absence, double-zero, or strict-isotropy/no-shear route", "CONDITIONAL_ZERO_FOR_GAMMA_R11"),
        ("GAM3918_4_bound", "fallback absolute bound", BOUND, "used when P_TF is not theorem-zero", "BOUND_FORMULA_TIGHTENED"),
        ("GAM3918_5_common_mode_guard", "not a full local-GR proof", "Phi_R11=Psi_R11 may survive as common mode even when delta_gamma_R11=0", "send common mode to Newton/ephemeris/beta gates", "NO_FULL_CLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "piece": piece,
            "formula_or_statement": formula,
            "meaning": meaning,
            "status": status,
            "numeric_value": "",
            "score_ready": status == "CONDITIONAL_ZERO_FOR_GAMMA_R11",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, formula, meaning, status in data
    ]


def bound_input_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BIN3918_0_kappa_R", "kappa_R", "dimensionless_or_action_normalized", "R11 coupling in residual equation", "source from parent non-EH/action coefficient or set zero by EH/DZ theorem", "required only on fallback branch"),
        ("BIN3918_1_C_TF", "C_TF", "dimensionless_operator_coefficient", "coefficient of nabla^2(Psi_R11-Phi_R11)", "source from weak-field gauge/operator normalization", "must be nonzero with sign convention fixed"),
        ("BIN3918_2_U_min", "U_min", "dimensionless_potential", "minimum absolute calibrated Newtonian potential on comparison domain", "source from local test geometry or solar-system model", "prevents denominator smuggling"),
        ("BIN3918_3_inv_laplace", "||nabla^{-2}||_domain", "length_squared_or_normalized_operator_norm", "Green-operator norm for selected boundary/domain", "source from domain boundary condition", "needed if P_TF not zero"),
        ("BIN3918_4_PTF_norm", "||P_TF[R11_ij]||", "operator_residual_norm", "anisotropic R11 source norm", "derive from parent operator or bound by local data", "central fallback input"),
        ("BIN3918_5_small_residual", "epsilon_gamma_linear", "dimensionless", "(|Phi_R11|+|Psi_R11|)/|U| control", "source from same fallback solution", "linearized gamma law requires epsilon << 1"),
        ("BIN3918_6_boundary", "boundary_condition", "domain_clause", "which inverse-Laplacian solution is being used", "source from boundary/topological/no-flux certificate", "open boundary/projector shear reopens P_TF"),
        ("BIN3918_7_common_mode", "Xi_N_common_mode", "dimensionless_or_GM_shift", "Phi_R11=Psi_R11 branch that gamma cannot see", "route to Newton/ephemeris/beta rather than gamma", "not required for gamma-zero but required for local GR"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "units": units,
            "role": role,
            "source_rule": source_rule,
            "status": "THEOREM_ZERO_BYPASSES_NUMERIC_FILL" if "set zero" in source_rule else "FALLBACK_INPUT_REQUIRED_IF_THEOREM_ZERO_FAILS",
            "notes": notes,
            "numeric_value": "",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, units, role, source_rule, notes in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3918_0_gamma",
            "decision": "delta_gamma_R11 has a conditional theorem-zero route",
            "formula": THEOREM_ZERO,
            "why": "the dangerous observable for Cassini is the traceless/STF part, not every scalar common-mode residual",
            "claim_status": "PRIVATE_CONDITIONAL_RESULT_NOT_PUBLIC_CLAIM",
            "next_action": "move beta/source and common-mode Newtonian readout next",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3918_1_fallback",
            "decision": "if any anisotropic escape survives, use the tightened symbolic bound",
            "formula": BOUND,
            "why": "this prevents another vague missing-row loop: the exact fallback inputs are now named",
            "claim_status": "NONCLAIM_BOUND_INTERFACE",
            "next_action": "fill or theorem-zero kappa_R, C_TF, U_min, inverse-Laplacian norm, P_TF norm",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3918_2_guard",
            "decision": "do not count P_TF zero as full local-GR",
            "formula": "P_TF=0 controls gamma only; common mode, beta, preferred-frame and conservation rows remain separate",
            "why": "this is how the route stays honest while still moving forward",
            "claim_status": "LOCAL_GR_STILL_BLOCKED",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3918_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive the beta/source second-order lock A_source=1,B_source=1 or bound the R11 common-mode Xi_N that gamma cannot see",
            "why_this_next": "3918 narrows gamma to STF anisotropic stress; the next real local-GR bottleneck is beta/source normalization and common-mode Newtonian readout",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "delta_gamma_R11 theorem-zero route constructed; fallback bound tightened; common-mode/beta remain next",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3918 - Delta Gamma R11 Theorem-Zero or Symbolic Bound Tightening

Timestamp: `{timestamp}`

## Result

The `delta_gamma_R11` route moved forward. The exact target is no longer vague:

`{SLIP_EQUATION}`

so

`{SLIP_SOLUTION}`

and therefore

`{GAMMA_SOURCE_LAW}`.

The clean theorem-zero result is:

`{THEOREM_ZERO}`.

## What Was Proved Conditionally

- EH absence route: if the local public branch is genuinely EH plus topological/zero residuals, active R11 anisotropic stress is absent.
- Double-zero route: if every relevant non-topological R11 family is `Sigma_loc`/double-zero selected, its first variation vanishes on `Y_loc=0`, so the TF source vanishes.
- Strict isotropy route: if the local residual stress has no direction/shear, `R11_ij=R_iso delta_ij/3`, hence `P_TF[R11_ij]=0`.
- Shortcut rejected: spherical symmetry alone is not enough, because a radial shear term can still have a traceless part.

## Meaning

This is a real narrowing of the local PPN problem: Cassini/gamma sees the traceless slip sector. A surviving scalar common mode with `Phi_R11=Psi_R11` can still affect Newton/ephemeris/beta, but it does not by itself move `gamma-1`.

Fallback if the theorem-zero route fails:

`{BOUND}`.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3918_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3918_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3918_PTF_ZERO_THEOREM_ROUTES.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3918_DELTA_GAMMA_R11_THEOREM_AND_BOUND.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3918_DELTA_GAMMA_R11_BOUND_INPUTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3918_GAMMA_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3918_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3918 - Delta Gamma R11 STF Zero Route

Timestamp: `{timestamp}`

- Derived target: `{SLIP_EQUATION}`.
- Gamma theorem-zero: `{THEOREM_ZERO}`.
- Key improvement: local gamma is controlled by the traceless/STF R11 stress, not by every possible scalar common-mode residual.
- Rejected shortcut: spherical symmetry alone does not kill the STF piece; strict isotropy/no-shear is required.
- Fallback bound: `{BOUND}`.
- Status: private conditional progress only; local-GR still needs beta/source normalization and common-mode Newtonian readout.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3918 - Delta Gamma R11 STF Zero Route"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    routes = theorem_route_rows(timestamp)
    gamma = gamma_rows(timestamp)
    bound_inputs = bound_input_rows(timestamp)
    decisions = decision_rows(timestamp)
    rows: list[dict[str, Any]] = []

    checks = [
        ("VAL3918_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3918_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3918_02_routes_present", len(routes) >= 7, "EH, DZ, isotropy, shortcut rejection, escape and common-mode routes emitted"),
        ("VAL3918_03_theorem_zero_present", any(row["status"].startswith("CONDITIONAL_THEOREM_ZERO") for row in routes), "conditional theorem-zero route emitted"),
        ("VAL3918_04_spherical_rejected", any(row["status"] == "REJECT_SHORTCUT" for row in routes), "spherical-only shortcut rejected"),
        ("VAL3918_05_gamma_zero_row", any(row["row_id"] == "GAM3918_3_theorem_zero" for row in gamma), "gamma theorem-zero consequence emitted"),
        ("VAL3918_06_bound_formula", any(row["row_id"] == "GAM3918_4_bound" and "kappa_R" in row["formula_or_statement"] for row in gamma), "fallback bound formula emitted"),
        ("VAL3918_07_bound_inputs", len(bound_inputs) == 8, "all fallback bound inputs listed"),
        ("VAL3918_08_common_mode_guard", any(row["row_id"] == "DEC3918_2_guard" for row in decisions), "common-mode guard emitted"),
        ("VAL3918_09_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (routes, gamma, bound_inputs, decisions) for row in group), "all new theorem/bound rows are nonclaim"),
        ("VAL3918_10_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3918_11_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3918_12_spine_written", SPINE_PATH.exists() and "3918 - Delta Gamma R11 STF Zero Route" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3918_13_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3918_14_script_compiles", True, "script compiles"),
        ("VAL3918_15_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    for row_id, passed, detail in checks:
        rows.append(
            {
                "row_id": row_id,
                "check": detail,
                "result": "PASS" if passed else "FAIL",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["routes"], theorem_route_rows(timestamp))
    write_csv(OUTPUTS["gamma"], gamma_rows(timestamp))
    write_csv(OUTPUTS["bound_inputs"], bound_input_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    write_csv(OUTPUTS["validation"], validation_rows(timestamp, source_rows))
    failed = [row for row in validation_rows(timestamp, source_rows) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3918 validation failed: {failed}")
    print(f"3918 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
