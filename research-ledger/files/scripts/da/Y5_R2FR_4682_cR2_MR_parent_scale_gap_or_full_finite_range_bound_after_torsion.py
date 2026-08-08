from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4682"
CLAIM_ID = "L-524"
MARKER = "PPC4161_CR2_MR_FINITE_RANGE_GATE_CURRENT_BRANCH_4682"
PACKET_MARKER = "PPC4161_PACKET_CR2_MR_FINITE_RANGE_GATE_CURRENT_BRANCH_4682"
DECISION = "CR2_MR_REDUCED_TO_EXTRA_MODE_ZERO_COMPONENTWISE_BODY_CHARGE_OR_FINITE_RANGE_BOUND_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4683-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md"

DOC_PATH = POST / "4682-Y5-R2FR-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md"
FORMAL_PATH = FORMAL / "698-PPC4161-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4681_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4681_NEXT_TARGET.csv"
CSV_4681_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4681_STATUS.csv"
CSV_4454_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4454_STATUS.csv"
CSV_4454_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4454_NEXT_TARGET.csv"
CSV_4594_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4594_CR2_ZERO_BOUND_THEOREM.csv"
CSV_4594_PROFILE = SOURCE_DIR / "P8_Y5_R2FR_4594_FINITE_RANGE_PROFILE_LAW.csv"
CSV_4594_BOUNDS = SOURCE_DIR / "P8_Y5_R2FR_4594_R10_ORBITAL_BOUND_INTERFACE.csv"
CSV_4594_SURVIVOR = SOURCE_DIR / "P8_Y5_R2FR_4594_SURVIVOR_UPDATE.csv"
CSV_4594_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4594_STATUS.csv"
CSV_4594_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4594_NEXT_TARGET.csv"
CSV_4594_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4594_VALIDATION.csv"
CSV_4595_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4595_STATUS.csv"
CSV_4595_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4595_OWNER_ZERO_SWITCH.csv"
CSV_4595_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4595_VALIDATION.csv"
FORMAL_610 = FORMAL / "610-PPC4161-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md"
FORMAL_611 = FORMAL / "611-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4682_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4682_CR2_ZERO_BOUND_THEOREM_IMPORT.csv"
PROFILE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4682_FINITE_RANGE_PROFILE_LAW.csv"
BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4682_R10_ORBITAL_BOUND_INTERFACE.csv"
EXIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4682_CR2_EXIT_CONDITIONS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4682_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4682_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4682_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4682_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4682_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4682_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4682_00_4681_next", CSV_4681_NEXT, "4682-Y5-R2FR-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md", "4681 selected current cR2/MR target."),
        ("SRC4682_01_4681_status", CSV_4681_STATUS, "cR2_MR", "4681 status retains cR2/MR as broad survivor."),
        ("SRC4682_02_4454_status", CSV_4454_STATUS, "lambda<38.6um_for_alpha1", "older cR2 mode map and short-range anchor."),
        ("SRC4682_03_4454_next", CSV_4454_NEXT, "cR2-parent-scale-signature-or-alpha-lambda-projection-row", "older parent-scale/projection handoff."),
        ("SRC4682_04_4594_theorem", CSV_4594_THEOREM, "TH4594_1_componentwise_zero", "componentwise cR2 zero/bound law."),
        ("SRC4682_05_4594_profile", CSV_4594_PROFILE, "FR4594_2_hidden_memory_fibre", "hidden/memory/fibre finite-range profile law."),
        ("SRC4682_06_4594_bounds", CSV_4594_BOUNDS, "B4594_0_R10_curve", "R10/orbital/PPN finite bound interface."),
        ("SRC4682_07_4594_survivor", CSV_4594_SURVIVOR, "SURV4594_2_cR2_MR", "post-cR2 survivor update."),
        ("SRC4682_08_4594_status", CSV_4594_STATUS, "CR2_MR_REDUCED_TO_PARENT_EXTRA_MODE_ZERO", "4594 decision/status."),
        ("SRC4682_09_4594_next", CSV_4594_NEXT, "memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate", "4594 selected memory/fibre owner target."),
        ("SRC4682_10_4594_validation", CSV_4594_VALIDATION, "VAL4594_18_next_memory_fibre", "4594 validation selected the next memory/fibre owner target."),
        ("SRC4682_11_4595_status", CSV_4595_STATUS, "MEMORY_FIBRE_BC_ZERO_SWITCH", "next owner gate already exists."),
        ("SRC4682_12_4595_owner", CSV_4595_OWNER, "ZS4595_0_common_operator", "memory/fibre zero switch source."),
        ("SRC4682_13_4595_validation", CSV_4595_VALIDATION, "VAL4595_OVERALL", "4595 validation passed."),
        ("SRC4682_14_formal610", FORMAL_610, "c_R2_eff_total = c_cell", "formal cR2 finite-range result."),
        ("SRC4682_15_formal611", FORMAL_611, "B_X=C_X=J_X=Q_boundary_X=0", "formal next memory/fibre zero switch."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4682_0_mode_decomposition",
            "claim": "After torsion narrowing, c_R2/M_R is a finite-range extra-mode problem, not a generic local-residual fog.",
            "derivation": "Import 4594: curvature-square terms map into scalar/tensor Yukawa channels with alpha_i and M_i; each channel is compared without cross-cancellation.",
            "zero_or_exit": "parent two-derivative/no-extra-mode selector sets all curvature-square propagating coefficients to zero",
            "finite_bound": "Phi/Phi_N = 1 + sum_i alpha_i exp(-M_i r)",
            "status": "CR2_MODE_DECOMPOSITION_IMPORTED_CURRENT_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4682_1_componentwise_zero",
            "claim": "Without a named parent identity, c_R2_eff_total closes only by componentwise zero/topological/boundary silence.",
            "derivation": "Use c_R2_eff_total=c_cell+c_bare+0.5 B^T L^-1 B+c_measure+c_boundary+c_marker.",
            "zero_or_exit": "c_cell=c_bare=c_measure=c_boundary=c_marker=0 and B_X=0 on every retained physical hidden/memory/fibre direction, or a parent Ward/topological identity proves the sum is identically zero",
            "finite_bound": "|c_R2_eff_total| <= sum absolute component bounds; no tuned cancellation credit",
            "status": "COMPONENTWISE_ZERO_OR_ABSOLUTE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4682_2_positive_hidden_obstruction",
            "claim": "Positive memory/fibre no-hair is not enough; the curvature-linear vertex must vanish.",
            "derivation": "If L is positive on the physical quotient, B^T L^-1 B=||L^-1/2 B||^2>=0 and equals zero only when B=0 on the physical subspace.",
            "zero_or_exit": "B_mem=B_h=0, plus C/J/boundary source charges zero if those fields couple to matter/source readout",
            "finite_bound": "0.5 B^T L^-1 B <= 0.5 ||B||^2/lambda_min(L) with source-backed B and lambda_min rows",
            "status": "NO_XR_VERTEX_REQUIRED_NOT_OPTIONAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4682_3_body_charge_zero",
            "claim": "Exterior source-free equations do not erase scalaron/body tails.",
            "derivation": "For (-Z_X nabla^2+M_X^2)X=rho_X, the exterior amplitude A_body is a weighted interior/boundary charge.",
            "zero_or_exit": "A_body=0 iff Q_X[body]+Q_boundary=0 under the selected Green-function convention",
            "finite_bound": "|A_body| <= [exp(R_body/lambda_X) int_body |rho_X| dV + |Q_boundary|]/(4*pi |Z_X|)",
            "status": "BODY_CHARGE_ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4682_4_empirical_range_bound",
            "claim": "If parent zero/body-charge zero fails, c_R2/M_R must be scored as a finite-range Yukawa/scalar-Hessian branch.",
            "derivation": "The alpha=1 short-range anchor is useful but not sufficient; claim-grade closure needs full alpha(lambda), orbital or PPN projection rows with MTS source charges.",
            "zero_or_exit": "M_i L_arena >> 1, or full source-backed alpha_i(lambda_i)/A_body projection lies below R10, orbital and PPN bounds",
            "finite_bound": "R10 |alpha_X(lambda)|<=alpha_bound(lambda); orbital |Delta a/a_N|=|alpha|(1+r/lambda)exp(-r/lambda); Hessian profile H_R formula",
            "status": "FINITE_RANGE_SCORE_SHAPE_READY_INPUTS_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def profile_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("FR4682_0_standard_yukawa", "curvature-square weak-field potential", "Phi/Phi_N = 1 + sum_i alpha_i exp(-M_i r)", "all alpha_i=0 or M_i L_arena >> 1 with source-backed lower M_i", "alpha_i;M_i;arena radius;source/test projection;no-cancellation convention"),
        ("FR4682_1_standard_R2_scalaron", "R2/fR scalaron", "R(r)=A_body exp(-m_R r)/r; H_R=|A_body| exp(-m_R r)(m_R^2/r+3m_R/r^2+3/r^3)", "c_R2_eff_total=0 or A_body=0", "A_body;m_R;MTS-to-mu normalization;screening/source convention"),
        ("FR4682_2_hidden_memory_fibre", "integrated-out memory/fibre scalar contribution", "Delta c_R2_hidden = 0.5 B^T L^-1 B; if L>0 then zero iff B=0", "B_mem=B_h=0 on physical quotient plus source/boundary charge silence", "Z_mem;M2_mem;B_mem;C_mem;J_mem;Q_boundary_mem;Z_h;M2_h;B_h;C_h;J_h;Q_boundary_h"),
        ("FR4682_3_anchor_only_short_range", "Eot-Wash alpha=1 anchor", "lambda < 38.6 um for alpha approx 1; M > 0.0051121 eV for a single gravitational-strength Yukawa", "not a zero theorem; anchor only", "claim-grade alpha(lambda) curve and MTS alpha_i(lambda_i) projection"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "profile_id": profile_id,
            "target": target,
            "formula": formula,
            "zero_condition": zero_condition,
            "needed_inputs": needed_inputs,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for profile_id, target, formula, zero_condition, needed_inputs in data
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("B4682_0_R10_curve", "R10 short-range inverse-square tests", "|alpha_X(lambda)| <= alpha_bound(lambda)", "FULL_CURVE_AND_MTS_PROJECTION_REQUIRED", "claim-grade alpha_bound(lambda); alpha_X mapping; lambda_X; source/test charges; units"),
        ("B4682_1_R10_anchor", "R10 alpha=1 anchor", "lambda<38.6um -> M>0.0051121eV for alpha=1 single-Yukawa", "ANCHOR_ONLY_NONCLAIM", "not valid for non-alpha=1 or multi-channel MTS projection without curve"),
        ("B4682_2_orbital_large_lambda", "orbital/inverse-square acceleration", "|Delta a/a_N|=|alpha|(1+r/lambda)exp(-r/lambda)", "FORMULA_READY_VALUES_UNSIGNED", "alpha; lambda; arena radius; ephemeris/orbital threshold; projection convention"),
        ("B4682_3_PPN_scalaron", "PPN beta/gamma scalaron branch", "standard template: mu <= 1.443476e15 m^2 and lambda_R <= 9.306372e7 m only if MTS-to-f(R) map is signed", "STANDARD_TEMPLATE_READY_MTS_NORMALIZATION_UNSIGNED", "N_MTS_to_fR; c_R2_eff_total; A_body/screening; source convention"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "arena": arena,
            "formula": formula,
            "status": status,
            "missing_inputs": missing_inputs,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, arena, formula, status, missing_inputs in data
    ]


def exit_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("EXIT4682_0_parent_no_extra_mode", "parent two-derivative/no-extra-light-mode selector", "all curvature-square propagating coefficients absent", "PARENT_SELECTOR_UNSIGNED", False),
        ("EXIT4682_1_componentwise_zero", "componentwise c_R2_eff_total zero", "c_cell,c_bare,c_measure,c_boundary,c_marker and B_X all zero, or named identity", "ZERO_COMPONENTS_UNSIGNED", False),
        ("EXIT4682_2_body_charge_zero", "scalaron/body-charge zero", "Q_X[body]+Q_boundary=0 under selected Green function", "BODY_CHARGE_UNSIGNED", False),
        ("EXIT4682_3_heavy_mass_gap", "parent heavy scale", "M_i L_arena >> 1 with sourced M_i lower bound", "MASS_GAP_UNSIGNED", False),
        ("EXIT4682_4_finite_bound", "finite R10/orbital/PPN bound", "source-backed alpha(lambda)/A_body below arena bounds", "BOUND_INTERFACE_READY_VALUES_MISSING", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "exit_id": exit_id,
            "exit_route": route,
            "condition": condition,
            "current_status": status,
            "claim_allowed": claim_allowed,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for exit_id, route, condition, status, claim_allowed in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4682_0_EH_principal", "EH principal / public parent adoption", "still public blocker", "retain parent selector/adoption gate"),
        ("SURV4682_1_cGamma", "c_Gamma local memory coupling", "unchanged finite survivor", "derive memory support/projector zero or source profile coefficients"),
        ("SURV4682_2_cR2_MR", "c_R2/M_R finite-range curvature-square branch", "reduced to extra-mode zero, componentwise c_R2_eff_total zero, body-charge zero, heavy mass gap or finite source-backed bound", NEXT_TARGET),
        ("SURV4682_3_memory_fibre_BC", "memory/fibre B,C,J,boundary owners", "selected next owner/zero-switch target", NEXT_TARGET),
        ("SURV4682_4_material_projection_global", "Lambda/material/projection/global parent", "unchanged blocker", "keep promotion firewall active"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4682": status,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, family, status, action in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4682_0", "Do not use the alpha=1 anchor as a full c_R2/M_R proof."),
        ("CTRL4682_1", "Do not use exterior source-free language to erase body charge."),
        ("CTRL4682_2", "Do not allow cancellation between c_cell, c_bare, B^T L^-1 B, measure, boundary and marker pieces."),
        ("CTRL4682_3", "Positive L_X helps only after B_X/C_X/J_X/Q_boundary_X source silence is signed or bounded."),
        ("CTRL4682_4", "Move next to memory/fibre B,C,J,boundary owner rows rather than looping c_R2 labels."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "rule": rule,
            "status": "ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for control_id, rule in controls
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "summary": "4682 imports the 4594 c_R2/M_R finite-range ladder into the current branch after torsion narrowing. The branch now has exact exits: parent no-extra-mode selector, componentwise c_R2_eff_total zero, body-charge zero, heavy parent mass gap, or finite R10/orbital/PPN bound. Positive memory/fibre operators do not erase B_X source vertices; the next target is the memory/fibre B,C,J,boundary owner zero-switch or first body-charge coefficient row.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "cR2_status": "finite-range extra-mode/body-charge gate",
            "strict_zero_exits": "two_derivative_selector;c_R2_eff_total=0;A_body=0;M_i L_arena>>1",
            "finite_bound_exits": "R10_alpha_curve;orbital_acceleration;PPN_scalaron;Hessian_AE",
            "next_owner_target": "memory/fibre B,C,J,Q_boundary zero switch",
            "local_GR_public_claim": False,
            "remaining_broad_survivors": "EH_public_adoption;cGamma;memory_fibre_BC_source_charge;Lambda_material_projection;global_parent",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4682_0",
            "target": NEXT_TARGET,
            "reason": "c_R2/M_R has been reduced to finite-range/body-charge exits; the live pressure is now memory/fibre B,C,J,boundary source owners.",
            "derive_first": "parent-sign B_mem_eff=C_mem=J_mem=Q_boundary_mem=0 and B_h=C_h=J_h=Q_boundary_h=0 from object-language/action-inventory exclusion",
            "fallback": "fill the first body-charge coefficient row: Z_X, M_X^2, B_X, C_X, J_X, Q_boundary_X and R10/PPN/orbital projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4682 - Y5/R2FR cR2/MR Parent Scale Gap or Full Finite-Range Bound After Torsion

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4682 imports the cR2/MR finite-range ladder into the current branch after the torsion narrowing.

```text
Phi/Phi_N = 1 + sum_i alpha_i exp(-M_i r)
c_R2_eff_total = c_cell + c_bare + 0.5 B^T L^-1 B
                 + c_measure + c_boundary + c_marker
```

For positive `L`, `B^T L^-1 B = ||L^-1/2 B||^2`, so a positive memory/fibre operator does not erase a nonzero source vertex. Exterior source-free equations also do not erase body charge.

The cR2/MR branch now closes only through:

```text
parent no-extra-mode selector,
componentwise c_R2_eff_total = 0,
body charge A_body = 0,
heavy mass gap M_i L_arena >> 1,
or source-backed R10/orbital/PPN finite bound.
```

## Source Register

{table(rows["sources"])}

## cR2 Theorem Import

{table(rows["theorems"])}

## Finite-Range Profile Law

{table(rows["profiles"])}

## R10 / Orbital / PPN Bound Interface

{table(rows["bounds"])}

## cR2 Exit Conditions

{table(rows["exits"])}

## Survivor Update

{table(rows["survivors"])}

## Controls

{table(rows["controls"])}

## Decision

{table(rows["decisions"])}

## Status

{table(rows["statuses"])}

## Next Target

{table(rows["next"])}

## Validation

{table(rows.get("validations", []))}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4682 - Y5/R2FR", "# 698 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4682 imports the c_R2/M_R finite-range ladder into the current branch after torsion narrowing. c_R2/M_R now closes only by parent no-extra-mode selector, componentwise c_R2_eff_total zero, body-charge zero, heavy mass gap, or source-backed R10/orbital/PPN finite bound; memory/fibre B,C,J,boundary source owners are selected next.",
                "current_evidence": "Generated source register, cR2 theorem import, finite-range profile law, R10/orbital/PPN bound interface, exit conditions, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Using alpha=1 anchor as a full proof, exterior source-free language as body-charge silence, positive L_X as source-vertex silence, or tuned cancellation among c_R2 components.",
                "sector": "local_gr",
                "evidence": str(DOC_PATH),
                "next_action": NEXT_TARGET,
            }
        )
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writerow(row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""## Local GR Parent-Derivation Update - Current cR2/MR Finite-Range Gate

Marker: `{MARKER}`

4682 imports the cR2/MR finite-range gate into the current branch:

```text
c_R2_eff_total = c_cell + c_bare + 0.5 B^T L^-1 B
               + c_measure + c_boundary + c_marker.
```

Closure requires a parent no-extra-mode selector, componentwise zero, body-charge zero, a heavy mass gap, or source-backed R10/orbital/PPN finite bound. Positive memory/fibre operators do not erase source vertices; the next target is the memory/fibre B,C,J,boundary zero switch.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current cR2/MR Finite-Range Gate

Marker: `{PACKET_MARKER}`

The packet now treats `c_R2/M_R` as a finite-range extra-mode/body-charge gate, not a vague residual. The next packet attack is memory/fibre `B_X,C_X,J_X,Q_boundary_X` ownership or first body-charge coefficient row.

- theorem csv: `{THEOREM_CSV.name}`
- bound csv: `{BOUND_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4682_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4682_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4682_2_componentwise_zero", any(row["theorem_id"] == "TH4682_1_componentwise_zero" for row in rows["theorems"]), "componentwise cR2 zero law present"),
        ("VAL4682_3_body_charge_law", any(row["theorem_id"] == "TH4682_3_body_charge_zero" for row in rows["theorems"]), "body-charge zero/bound law present"),
        ("VAL4682_4_finite_profiles", len(rows["profiles"]) == 4, "finite-range profile rows present"),
        ("VAL4682_5_bound_interfaces", len(rows["bounds"]) == 4, "R10/orbital/PPN bound interfaces present"),
        ("VAL4682_6_exit_conditions", len(rows["exits"]) == 5, "five cR2 exit routes written"),
        ("VAL4682_7_next_memory_fibre", rows["next"][0]["target"] == NEXT_TARGET, "next memory/fibre target selected"),
        ("VAL4682_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-524"),
        ("VAL4682_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4682_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4682_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4682_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4682_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4682_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4682_13_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4682_14_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4682_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "theorems": theorem_rows(timestamp),
        "profiles": profile_rows(timestamp),
        "bounds": bound_rows(timestamp),
        "exits": exit_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": control_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        THEOREM_CSV: rows["theorems"],
        PROFILE_CSV: rows["profiles"],
        BOUND_CSV: rows["bounds"],
        EXIT_CSV: rows["exits"],
        SURVIVOR_CSV: rows["survivors"],
        CONTROL_CSV: rows["controls"],
        DECISION_CSV: rows["decisions"],
        STATUS_CSV: rows["statuses"],
        NEXT_CSV: rows["next"],
    }
    for path, data in csv_map.items():
        write_csv(path, data)
    write_documents(rows)
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    rows["validations"] = validation_rows(rows, list(csv_map))
    write_csv(VALIDATION_CSV, rows["validations"])
    write_documents(rows)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
