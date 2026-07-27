from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3915"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3915-Y5-R2FR-stationary-local-branch-contract-and-PPN-residual-vector.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3915_SOURCE_REGISTER.csv",
    "contract": SRC / "P8_Y5_R2FR_3915_STATIONARY_LOCAL_BRANCH_CONTRACT.csv",
    "ppn_zero": SRC / "P8_Y5_R2FR_3915_CONDITIONAL_PPN_ZERO_VECTOR.csv",
    "residual": SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv",
    "promotion": SRC / "P8_Y5_R2FR_3915_LOCAL_GR_PROMOTION_GATE.csv",
    "fallback": SRC / "P8_Y5_R2FR_3915_PPN_FALLBACK_PRIORITY.csv",
    "decision": SRC / "P8_Y5_R2FR_3915_BRANCH_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3915_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3915_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3915_VALIDATION.csv",
}

BRANCH_CONTRACT = "B_loc := product chart + EH public metric operator + no linear hidden/source shadow + q_src source quotient + stationary source collar + same-frame Hilbert/Maxwell source + no active R11/vector/projector/boundary residuals"
PPN_ZERO_VECTOR = "Delta_PPN_GR := (gamma-1, beta-1, alpha1, alpha2, alpha3, xi, zeta_i, Gdot/G)_loc = 0"
PPN_ENVELOPE = "Delta_PPN_abs <= |delta_gamma_R11|+|delta_gamma_readout|+|delta_gamma_frame|+|delta_gamma_source|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|delta_beta_boundary_domain|+|delta_beta_readout|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|+|Gdot/G|"
PROMOTION_RULE = "local-GR promotion requires B_loc parent adoption plus every PPN residual row theorem-zero or source-backed below bound; no cancellation and no orbital-GM absorption"
NEXT_TARGET = "3916-Y5-R2FR-R11-nonEH-selector-closure-or-PPN-coefficient-fill.md"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
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
        ("SRC3915_00_next", SRC / "P8_Y5_R2FR_3914_NEXT_TARGET.csv", "NEXT3914_0", "3914 selected branch-contract/PPN target"),
        ("SRC3915_01_stack", SRC / "P8_Y5_R2FR_3914_STATIONARY_SOURCE_COUPLING_STACK.csv", "STK3914_1_stack", "3914 source-coupling stack"),
        ("SRC3915_02_gdot", SRC / "P8_Y5_R2FR_3914_ZPOISSON_ZFRAME_CLOSURE_GATE.csv", "Z3914_2_Gdot_close", "3914 local Gdot close"),
        ("SRC3915_03_GR", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_0_GR", "3914 GR arena"),
        ("SRC3915_04_Newton", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_1_Newton", "3914 Newton arena"),
        ("SRC3915_05_Maxwell", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_2_Maxwell", "3914 Maxwell arena"),
        ("SRC3915_06_fallback_parent", SRC / "P8_Y5_R2FR_3914_ACTIVE_BRANCH_RESIDUAL_FALLBACK_MAP.csv", "FB3914_5_parent_adoption", "3914 parent adoption fallback"),
        ("SRC3915_07_ppn_readout", SRC / "P8_Y5_NO_SHADOW_2505_PPN_READOUT_VECTOR.csv", "PPN2505_2_beta_law", "EH PPN readout beta law"),
        ("SRC3915_08_ppn_gamma", SRC / "P8_Y5_NO_SHADOW_2505_PPN_READOUT_VECTOR.csv", "PPN2505_3_gamma_first_order", "EH gamma first-order row"),
        ("SRC3915_09_ppn_warning", SRC / "P8_Y5_NO_SHADOW_2505_PPN_READOUT_VECTOR.csv", "PPN2505_4_spatial_2PN_warning", "2PN gauge/readout warning"),
        ("SRC3915_10_nwf_ppn", SRC / "P8_Y5_GR_LEFT_HAND_GATE_2619_NEWTON_POISSON_WEAK_FIELD_ATTEMPT.csv", "NWF2619_3_ppn_gamma_beta", "PPN gamma/beta bridge"),
        ("SRC3915_11_pg9", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG9_second_order_source_stability", "second-order source stability warning"),
        ("SRC3915_12_3885_rows", SRC / "P8_Y5_R2FR_3885_PPN_PARAMETER_RESIDUAL_ROWS.csv", "PPN3885_8_total", "latest PPN parameter residual rows"),
        ("SRC3915_13_3885_theorem", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_0_target", "PPN theorem target"),
        ("SRC3915_14_3885_gamma", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_1_gamma", "gamma condition"),
        ("SRC3915_15_3885_beta", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_2_beta", "beta condition"),
        ("SRC3915_16_3885_pref", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_3_preferred_frame", "preferred-frame condition"),
        ("SRC3915_17_3886_coeff", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_00_delta_gamma_R11", "executable PPN coefficient skeleton"),
        ("SRC3915_18_3887_fill", SRC / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv", "FILL3887_1_gamma_R11", "R11 PPN coefficient fill pivot"),
        ("SRC3915_19_local_gates", SRC / "P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES.csv", "G482_local_GR_vector", "local GR promotion gate"),
        ("SRC3915_20_local_decision", SRC / "P8_LOCAL_GR_RESIDUAL_DECISION.csv", "D4_local_GR", "local GR no-claim decision"),
        ("SRC3915_21_R11_selector", SRC / "P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv", "L4_selector_theorem_target", "R11 selector theorem target"),
        ("SRC3915_22_R11_mapping", SRC / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv", "source_normalization_operator", "R11 operator mapping"),
        ("SRC3915_23_3653_contract", SRC / "P8_Y5_R2FR_3653_NEWTON_PPN_ZERO_VECTOR_THEOREM_ATTEMPT.csv", "NPG3653_2_PPN_coefficient_gate", "PPN zero vector condition"),
        ("SRC3915_24_validation", SRC / "P8_Y5_BRR545_3914_VALIDATION.csv", "VAL3914_14_no_pycache", "3914 validation handoff"),
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
                    excerpt = line[:500]
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


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    clauses = [
        ("BLC3915_0_branch", "branch definition", BRANCH_CONTRACT, "ASSEMBLED_CONDITIONAL_BRANCH_CONTRACT", "parent adoption remains the highest-level gap"),
        ("BLC3915_1_public_metric", "EH public metric operator", "S_Q=(2*kappa_*)^-1 int sqrt(-Q)(R-2Lambda_*) plus topological/zero residuals", "CONDITIONAL_FROM_3905_3906", "R11/non-EH selector must close"),
        ("BLC3915_2_source", "source coupling", "same-frame Hilbert/Maxwell T_vis sources Q_pub and q_src fixes source charge/readout", "CONDITIONAL_FROM_3914", "source-active branches fallback"),
        ("BLC3915_3_readout", "observed frame", "matter, light, clocks, EM stress, source charge and orbits use one q_pub/q_src observed frame", "CONDITIONAL_FROM_3914", "frame split fallback remains"),
        ("BLC3915_4_no_shadow", "no local vector/shadow marker", "no independent vector/domain/coframe/memory marker survives through O(U^2)", "CONDITIONAL_REQUIREMENT", "alpha_i/xi rows fallback if unsigned"),
        ("BLC3915_5_no_cancellation", "promotion policy", PROMOTION_RULE, "GUARD_ACTIVE", "no local-GR public claim from this checkpoint"),
    ]
    return [
        {
            "row_id": row_id,
            "clause": clause,
            "formula_or_requirement": formula,
            "status": status,
            "remaining_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, formula, status, gap in clauses
    ]


def ppn_zero_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PPNZ3915_0_gamma", "gamma_minus_1", "gamma-1=0", "EH-only same-readout gives Psi=Phi; 3914 closes source/readout/frame pieces", "R11/DeltaE must be zero/topological/double-zero"),
        ("PPNZ3915_1_beta", "beta_minus_1", "beta-1=0", "EH nonlinear completion gives B_source=A_source^2; 3914 closes source normalization", "second-order source/R11/boundary/readout pieces must vanish"),
        ("PPNZ3915_2_alpha1", "alpha1", "alpha1=0", "no independent local vector/domain/frame/memory marker in B_loc", "vector/preferred-frame selector must be parent-signed"),
        ("PPNZ3915_3_alpha2", "alpha2", "alpha2=0", "same no-vector/common-frame clause removes preferred-frame sector", "spin/rotation/domain terms remain fallback if unsigned"),
        ("PPNZ3915_4_alpha3", "alpha3", "alpha3=0", "Bianchi conservation plus stationary source collar removes self-acceleration/nonconservation channel", "boundary/domain alpha3 gates still fallback outside branch"),
        ("PPNZ3915_5_xi", "xi", "xi=0", "no preferred-location anisotropic/nonlocal kernel in the local collar", "anisotropy/STF/nonlocal selectors must remain zero"),
        ("PPNZ3915_6_zeta", "zeta_i", "zeta_i=0", "same-frame Hilbert stress plus Bianchi conservation removes non-Hilbert stress leakage", "extra stress/projector rows fallback if unsigned"),
        ("PPNZ3915_7_Gdot", "Gdot/G", "Gdot/G=0", "3914 stationary local Gdot stack closes", "dynamic/cosmological source evolution is separate"),
        ("PPNZ3915_8_total", "Delta_PPN_GR", PPN_ZERO_VECTOR, "all previous PPN rows zero in the branch", "not promoted unless the branch is parent-adopted and R11 selectors close"),
    ]
    return [
        {
            "row_id": row_id,
            "parameter": parameter,
            "conditional_value": value,
            "zero_reason": reason,
            "remaining_gate": gate,
            "status": "CONDITIONAL_ZERO_IN_BLOC",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, parameter, value, reason, gate in rows
    ]


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PPNR3915_0_gamma", "gamma_minus_1", "delta_gamma_R11 + delta_gamma_readout + delta_gamma_frame + delta_gamma_source", "abs(gamma-1) <= 2.3e-05 or theorem-zero", "FILL3887_1_gamma_R11"),
        ("PPNR3915_1_beta", "beta_minus_1", "delta_beta_source + delta_beta_R11 + delta_beta_q_loc + delta_beta_boundary_domain + delta_beta_readout", "abs(beta-1) <= 7.8e-05 or theorem-zero", "FILL3887_2_beta_source"),
        ("PPNR3915_2_alpha1", "alpha1", "alpha1_domain + alpha1_frame + alpha1_vector + alpha1_memory", "abs(alpha1) <= 1e-04 or theorem-zero", "COEF3886_06_alpha1"),
        ("PPNR3915_3_alpha2", "alpha2", "alpha2_domain + alpha2_frame + alpha2_vector + alpha2_memory", "abs(alpha2) <= 2e-09 or theorem-zero", "COEF3886_07_alpha2"),
        ("PPNR3915_4_alpha3", "alpha3", "alpha3_boundary + alpha3_domain + alpha3_flux + alpha3_nonconservation", "abs(alpha3) <= 4e-20 or theorem-zero", "FILL3887_0_boundary_alpha3"),
        ("PPNR3915_5_xi", "xi", "xi_domain + xi_boundary + xi_anisotropy + xi_nonlocal", "abs(xi) <= 4e-09 or theorem-zero", "COEF3886_09_xi"),
        ("PPNR3915_6_zeta", "zeta_i", "stress nonconservation / non-Hilbert source leakage components", "zeta_i=0 or stress vector bounded", "COEF3886_10_zeta_i"),
        ("PPNR3915_7_yukawa", "alpha(lambda)", "finite-range R11/bulk-X/source-normalization Yukawa profile", "abs(alpha_predicted(lambda)) <= alpha_bound(lambda)", "FILL3887_3_alpha_lambda"),
        ("PPNR3915_8_total", "Delta_PPN_abs", PPN_ENVELOPE, "every component zero/bounded with no cancellation", "PPN3885_8_total"),
    ]
    return [
        {
            "row_id": row_id,
            "parameter": parameter,
            "formula_or_decomposition": formula,
            "pass_rule": pass_rule,
            "fallback_source": fallback,
            "status": "EXECUTABLE_RESIDUAL_IF_BRANCH_FAILS",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, parameter, formula, pass_rule, fallback in rows
    ]


def promotion_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PROM3915_0_branch", "B_loc branch contract parent-adopted", "NOT_PROVED_GLOBAL", "local fixed-point branch only"),
        ("PROM3915_1_R11", "all active R11/non-EH operators absent/topological/double-zero or bounded", "OPEN_NEXT_TARGET", "dominant blocker"),
        ("PROM3915_2_PPN", "PPN zero vector theorem-zero or below sourced bounds", "CONDITIONAL_ONLY", "requires PROM3915_0 and PROM3915_1"),
        ("PROM3915_3_no_cancel", "no post-fit cancellation or orbital-GM absorption", "PASS_GUARD_ACTIVE", "policy retained"),
        ("PROM3915_4_public", "public local-GR claim", "FORBIDDEN_NOW", "conditional stack is strong but not final"),
    ]
    return [
        {
            "row_id": row_id,
            "requirement": requirement,
            "current_result": result,
            "reason": reason,
            "valid_for_local_GR_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, requirement, result, reason in rows
    ]


def fallback_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("FB3915_0_R11", "EH-only/R11 selector fails", "fill delta_gamma_R11, delta_beta_R11, projector stress and operator weak-field coefficients"),
        ("FB3915_1_beta_source", "second-order source response not locked", "fill A_source, B_source and delta_beta_source"),
        ("FB3915_2_vector", "no-vector/preferred-frame clause fails", "fill alpha1/alpha2/preferred-frame coefficients"),
        ("FB3915_3_alpha3", "boundary/domain/nonconservation alpha3 clause fails", "fill individual alpha3 product rows; no total cancellation"),
        ("FB3915_4_xi", "anisotropic/preferred-location clause fails", "fill xi STF/domain/nonlocal coefficients"),
        ("FB3915_5_zeta", "stress conservation/projector closure fails", "fill zeta_i and T_extra_munu rows"),
        ("FB3915_6_R10", "finite-range tail remains", "route to R10 alpha(lambda) real bound runner"),
    ]
    return [
        {
            "row_id": row_id,
            "failure_condition": condition,
            "fallback_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, condition, action in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3915_0_contract",
            "decision": "stationary local branch contract is now compact and explicit",
            "claim_status": "CONDITIONAL_BRANCH_CONTRACT_NOT_PUBLIC_CLAIM",
            "reason": "3914 source coupling plus EH/no-shadow/no-R11 clauses imply the GR PPN vector, but only if parent-adopted",
            "next_action": "attack R11/non-EH selector closure first",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3915_1_ppn",
            "decision": "PPN vector zero is conditionally derived, not promoted",
            "claim_status": "PPN_ZERO_ROUTE_WRITTEN_RESIDUAL_VECTOR_LIVE",
            "reason": "gamma/beta/alpha_i/xi/zeta/Gdot rows have theorem-zero routes and executable fallbacks",
            "next_action": "do not claim local GR until R11/operator and PPN rows are closed or bounded",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3915_2_next",
            "decision": "next target is R11/non-EH selector closure or coefficient fill",
            "claim_status": "NEXT_TARGET_SELECTED",
            "reason": "R11/non-EH operator silence is now the dominant blocker between conditional local branch and public PPN viability",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3915_0",
            "next_doc": NEXT_TARGET,
            "next_script": "scripts/Y5_R2FR_3916_R11_nonEH_selector_closure_or_PPN_coefficient_fill.py",
            "target": "derive active R11/non-EH operator silence from the product/EH branch selector and double-zero clauses, or fill the executable PPN coefficient rows starting with delta_gamma_R11 and delta_beta_source",
            "why_this_next": "3915 makes the local branch and PPN vector explicit; R11/non-EH operator silence is the dominant remaining local-GR blocker",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "result": "stationary local branch contract and conditional PPN zero vector written; executable PPN residual vector retained",
            "local_gr_claim": False,
            "ppn_claim": False,
            "newton_claim": False,
            "new_forward_progress": "the route from source-coupled Newton to local GR is now a compact branch contract plus a concrete PPN promotion gate",
            "primary_blocker": "R11/non-EH operator silence or coefficient fill",
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(sources: list[dict[str, Any]], timestamp: str) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3915 — Stationary Local Branch Contract and PPN Residual Vector

Timestamp: `{timestamp}`

## Result

This checkpoint converts the conditional local-source stack into a compact local branch contract and a PPN promotion gate.

Branch contract:
`{BRANCH_CONTRACT}`

Conditional PPN zero vector:
`{PPN_ZERO_VECTOR}`

Executable fallback envelope:
`{PPN_ENVELOPE}`

Promotion rule:
`{PROMOTION_RULE}`

## Meaning

- If `B_loc` is parent-adopted and every R11/non-EH/vector/projector/boundary/readout residual is theorem-zero, the GR PPN vector follows.
- This does **not** promote a public local-GR claim.
- If any clause fails, the executable residual vector is retained with no cancellation credit.
- The dominant next blocker is R11/non-EH operator silence or coefficient fill.

## Source Register

- Source rows found: `{found}/{len(sources)}`
- Register: `{rel(OUTPUTS['sources'])}`
- Validation: `{rel(OUTPUTS['validation'])}`

## Generated Tables

- `{rel(OUTPUTS['contract'])}`
- `{rel(OUTPUTS['ppn_zero'])}`
- `{rel(OUTPUTS['residual'])}`
- `{rel(OUTPUTS['promotion'])}`
- `{rel(OUTPUTS['fallback'])}`
- `{rel(OUTPUTS['decision'])}`
- `{rel(OUTPUTS['next'])}`

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3915 STATIONARY LOCAL PPN CONTRACT -->
## 3915 Stationary Local Branch Contract and PPN Gate

Timestamp: `{timestamp}`

Branch contract:
`{BRANCH_CONTRACT}`

Conditional PPN zero vector:
`{PPN_ZERO_VECTOR}`

Fallback envelope:
`{PPN_ENVELOPE}`

Promotion rule:
`{PROMOTION_RULE}`

Decision: the local GR route is now a compact conditional branch plus an executable PPN residual vector. No local-GR claim yet; R11/non-EH operator silence or coefficient fill is the next blocker.
<!-- END 3915 STATIONARY LOCAL PPN CONTRACT -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3915 STATIONARY LOCAL PPN CONTRACT -->"
    end = "<!-- END 3915 STATIONARY LOCAL PPN CONTRACT -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    ppn_zero: list[dict[str, Any]],
    residual: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL3915_0_sources", "all cited source paths and needles resolve", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} source rows found"))
    checks.append(("VAL3915_1_contract", "branch contract emitted", any(BRANCH_CONTRACT in row["formula_or_requirement"] for row in contract), rel(OUTPUTS["contract"])))
    checks.append(("VAL3915_2_ppn_zero", "conditional PPN zero vector emitted", any(PPN_ZERO_VECTOR in row["conditional_value"] for row in ppn_zero), rel(OUTPUTS["ppn_zero"])))
    checks.append(("VAL3915_3_residual", "executable PPN residual envelope emitted", any(PPN_ENVELOPE in row["formula_or_decomposition"] for row in residual), rel(OUTPUTS["residual"])))
    checks.append(("VAL3915_4_gamma_beta", "gamma and beta rows present", {"gamma_minus_1", "beta_minus_1"}.issubset({row["parameter"] for row in ppn_zero}) and {"gamma_minus_1", "beta_minus_1"}.issubset({row["parameter"] for row in residual}), rel(OUTPUTS["ppn_zero"])))
    checks.append(("VAL3915_5_preferred", "preferred-frame/location rows present", {"alpha1", "alpha2", "alpha3", "xi"}.issubset({row["parameter"] for row in ppn_zero}), rel(OUTPUTS["ppn_zero"])))
    checks.append(("VAL3915_6_promotion_no_claim", "promotion gates forbid local-GR claim", any(row["current_result"] == "FORBIDDEN_NOW" for row in promotion) and all(str(row.get("valid_for_local_GR_claim")) == "False" for row in promotion), rel(OUTPUTS["promotion"])))
    checks.append(("VAL3915_7_fallback", "PPN fallback priorities emitted", len(fallback) >= 7 and all(str(row.get("claim_allowed")) == "False" for row in fallback), rel(OUTPUTS["fallback"])))
    checks.append(("VAL3915_8_no_claim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim")) == "False" for row in contract + ppn_zero + residual + promotion + fallback + decision), "valid_for_claim false across generated rows"))
    checks.append(("VAL3915_9_next", "next target attacks R11/nonEH selector", "3916-Y5-R2FR-R11" in read_text(OUTPUTS["next"]), rel(OUTPUTS["next"])))
    checks.append(("VAL3915_10_doc", "3915 markdown checkpoint written", DOC_PATH.exists() and "Stationary Local Branch Contract" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3915_11_spine", "spine updated with 3915 block", SPINE_PATH.exists() and "BEGIN 3915 STATIONARY LOCAL PPN CONTRACT" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details: list[str] = []
    for path in csv_outputs:
        try:
            rows = read_csv_rows(path)
            parse_details.append(f"{path.name}:{len(rows)}")
            csv_parse_ok = csv_parse_ok and bool(rows)
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{type(exc).__name__}:{exc}")
    checks.append(("VAL3915_12_csv_parse", "all generated CSV outputs parse cleanly", csv_parse_ok, "; ".join(parse_details)))
    fwb_hits = list(FWB.rglob("*3915*")) if FWB.exists() else []
    checks.append(("VAL3915_13_no_formalization_workbench_edits", "no 3915 files generated in formalization-workbench", not fwb_hits, "; ".join(str(path) for path in fwb_hits[:10]) or "no formalization-workbench hits"))
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    checks.append(("VAL3915_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, "; ".join(str(path) for path in pycache_hits[:10]) or "no __pycache__"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    contract = contract_rows(timestamp)
    ppn_zero = ppn_zero_rows(timestamp)
    residual = residual_rows(timestamp)
    promotion = promotion_rows(timestamp)
    fallback = fallback_rows(timestamp)
    decision = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["ppn_zero"], ppn_zero)
    write_csv(OUTPUTS["residual"], residual)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["fallback"], fallback)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, contract, ppn_zero, residual, promotion, fallback, decision, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
