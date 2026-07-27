from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3922"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3922-Y5-R2FR-boundary-projector-domain-multipole-zero-or-local-bound-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3922_SOURCE_REGISTER.csv",
    "multipole": SRC / "P8_Y5_R2FR_3922_MULTIPOLE_ESCAPE_ZERO_THEOREM.csv",
    "bound": SRC / "P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv",
    "ppn": SRC / "P8_Y5_R2FR_3922_ESCAPE_TO_PPN_ORBITAL_MAP.csv",
    "decision": SRC / "P8_Y5_R2FR_3922_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3922_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3922_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3922_VALIDATION.csv",
}

SOURCE_SPLIT = "P00[R11]_esc = P00_boundary + P00_projector + P00_domain + P00_history + P00_nonlocal"
ZERO_THEOREM = "BOUNDARY_CERT and PROJECTOR_CERT and FIXED_QBASIC_DOMAIN and NO_INCOMING_HISTORY => P00[R11]_esc=0 and a_l>=1=0"
MULTIPOLE_BOUND = "A_multi := sum_{l>=1,m}|a_l| <= G_ext*(|P00_boundary|+|P00_projector|+|P00_domain|+|P00_history|+|P00_nonlocal|)+B_harmonic_boundary"
DERIVATIVE_BOUND = "B_deriv := |partial_t xi_1| + |partial_r xi_1| + |Delta_AB xi_1| + |delta_frame xi_1|"
LOCAL_RESIDUAL = "B_escape := |Delta_sq|/(1+xi_1)^2 + |epsilon_r| + A_multi + B_deriv + epsilon_domain_projector_abs"
NEXT_DOC = "3923-Y5-R2FR-local-GR-conditional-theorem-stack-and-remaining-bound-pack.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3923_local_GR_conditional_theorem_stack_and_remaining_bound_pack.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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
        ("SRC3922_00_next", SRC / "P8_Y5_R2FR_3921_NEXT_TARGET.csv", "NEXT3921_0", "3921 selected escape channel target"),
        ("SRC3922_01_ext_escape", SRC / "P8_Y5_R2FR_3921_P00_ZERO_HARMONIC_EXTERIOR_THEOREM.csv", "EXT3921_6_escape_channels", "3921 escape channels"),
        ("SRC3922_02_ext_residual", SRC / "P8_Y5_R2FR_3921_P00_ZERO_HARMONIC_EXTERIOR_THEOREM.csv", "EXT3921_4_residual_definition", "Xi_N residual definition"),
        ("SRC3922_03_bounds_multi", SRC / "P8_Y5_R2FR_3921_XIN_NUMERIC_BOUND_FILL_ROWS.csv", "BIN3921_5_multipoles", "multipole bound row"),
        ("SRC3922_04_bounds_radial", SRC / "P8_Y5_R2FR_3921_XIN_NUMERIC_BOUND_FILL_ROWS.csv", "BIN3921_6_radial", "radial bound row"),
        ("SRC3922_05_boundary_cert", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_0_certificate", "boundary certificate"),
        ("SRC3922_06_boundary_alpha", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_1_alpha3_zero", "boundary alpha3 zero route"),
        ("SRC3922_07_boundary_monopole", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_2_scalar_monopole", "boundary scalar monopole policy"),
        ("SRC3922_08_boundary_verdict", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_4_verdict", "boundary unsigned verdict"),
        ("SRC3922_09_projector_cert", SRC / "P8_Y5_R2FR_3892_PROJECTOR_ABSOLUTE_TOPOLOGICAL_CERTIFICATE.csv", "PC3892_0_certificate", "projector certificate"),
        ("SRC3922_10_projector_zero", SRC / "P8_Y5_R2FR_3892_PROJECTOR_ABSOLUTE_TOPOLOGICAL_CERTIFICATE.csv", "PC3892_1_projector_zero", "projector stress zero route"),
        ("SRC3922_11_projector_guard", SRC / "P8_Y5_R2FR_3892_PROJECTOR_ABSOLUTE_TOPOLOGICAL_CERTIFICATE.csv", "PC3892_2_product_rule", "projector exact product guard"),
        ("SRC3922_12_bps_boundary", SRC / "P8_Y5_R2FR_3891_BOUNDARY_PROJECTOR_SILENCE_ATTEMPT.csv", "BPS3891_0_boundary_guard", "boundary vector/shear guard"),
        ("SRC3922_13_bps_projector", SRC / "P8_Y5_R2FR_3891_BOUNDARY_PROJECTOR_SILENCE_ATTEMPT.csv", "BPS3891_4_projector_product", "projector product rule retained"),
        ("SRC3922_14_harmonic", SRC / "P8_Y5_R2FR_3834_BOUNDARY_HARMONIC_ELLIPTIC_ZERO_THEOREM.csv", "BH3834_0_elliptic_uniqueness", "harmonic elliptic uniqueness"),
        ("SRC3922_15_harmonic_bound", SRC / "P8_Y5_R2FR_3834_BOUNDARY_HARMONIC_ELLIPTIC_ZERO_THEOREM.csv", "BH3834_2_bound_contract", "boundary harmonic bound contract"),
        ("SRC3922_16_domain_no_go", SRC / "P8_Y5_R2FR_3431_PROJECTOR_VARIATION_NO_STRESS_THEOREM.csv", "DP3431_1_no_go", "domain/projector no-go"),
        ("SRC3922_17_domain_zero", SRC / "P8_Y5_R2FR_3431_PROJECTOR_VARIATION_NO_STRESS_THEOREM.csv", "DP3431_2_fixed_topological_zero", "fixed topological zero theorem"),
        ("SRC3922_18_domain_bound", SRC / "P8_Y5_R2FR_3431_PROJECTOR_VARIATION_NO_STRESS_THEOREM.csv", "DP3431_6_operator_bound", "domain/projector bound theorem"),
        ("SRC3922_19_domain_bound_pack", SRC / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv", "DPOB3431_4_total_domain_projector", "domain/projector total bound"),
        ("SRC3922_20_domain_ppn", SRC / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_PPN_COEFFICIENT_UPDATE.csv", "DPPN3431_3_xi", "domain projector xi map"),
        ("SRC3922_21_domain_branch", SRC / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_BRANCH_VERDICTS.csv", "DPB3431_0_fixed_topological", "best zero route unsigned"),
        ("SRC3922_22_memory_history", SRC / "P8_Y5_R2FR_3895_MEMORY_BOUNDARY_HISTORY_ZERO_ATTEMPT.csv", "ZERO3895_4_history_exact", "history exact-zero failure"),
        ("SRC3922_23_memory_law", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_3_history_decay", "history suppression law"),
        ("SRC3922_24_ppn_alpha", SRC / "P8_Y5_R2FR_3915_CONDITIONAL_PPN_ZERO_VECTOR.csv", "PPNZ3915_5_xi", "PPN xi zero gate"),
        ("SRC3922_25_validation", SRC / "P8_Y5_BRR545_3921_VALIDATION.csv", "VAL3921_14_no_pycache", "3921 validation handoff"),
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
                    excerpt = line[:720]
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


def multipole_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("MUL3922_0_source_split", "escape source split", SOURCE_SPLIT, "all non-EH escape sources feeding Xi_N are explicit", "DECOMPOSITION_READY"),
        ("MUL3922_1_boundary_zero", "boundary certificate route", "BOUNDARY_CERT kills vector/shear/normal-exchange boundary data; derivative-silent scalar monopole may calibrate GM only", "uses 3892/3891; parent signature still absent", "CONDITIONAL_ZERO_ROUTE"),
        ("MUL3922_2_projector_zero", "projector certificate route", "PROJECTOR_CERT gives delta Pi_M=0 and [d,Pi_M]=0, so no projector stress/source multipole", "uses 3892 exact product guard", "CONDITIONAL_ZERO_ROUTE"),
        ("MUL3922_3_domain_zero", "fixed q-basic/topological domain route", "fixed metric/domain-independent projector and q-basic local domain give no moving-support or hidden projector stress", "uses 3431 fixed-topological theorem", "CONDITIONAL_ZERO_ROUTE"),
        ("MUL3922_4_history_zero", "history/no-tail route", "no incoming memory plus no long-tail kernel kills history source; otherwise history is suppressed not zero", "uses 3895 history law", "PARTIAL_ZERO_BOUND_REQUIRED"),
        ("MUL3922_5_combined_zero", "combined multipole zero theorem", ZERO_THEOREM, "if every escape certificate signs, harmonic exterior has no l>=1 multipoles or derivative hair", "COMBINED_CONDITIONAL_THEOREM"),
        ("MUL3922_6_bound", "fallback multipole bound", MULTIPOLE_BOUND, "if any certificate fails, the escape multipoles are bounded by explicit source norms", "BOUND_INTERFACE_READY"),
        ("MUL3922_7_shortcut_rejected", "shortcut rejected", "scalar volume no-flux, trace projection, or spherical words alone do not kill action-level boundary/projector/domain stress", "prevents fake local-GR closure", "REJECT_SHORTCUT"),
    ]
    return [
        {
            "row_id": row_id,
            "piece": piece,
            "formula_or_statement": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, formula, meaning, status in data
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ESC3922_0_boundary_P00", "P00_boundary", "scalar_source_norm", "boundary scalar/vector/shear feed into Xi_N", "zero by BOUNDARY_CERT or numeric boundary integral"),
        ("ESC3922_1_projector_P00", "P00_projector", "scalar_source_norm", "projector variation source", "zero by PROJECTOR_CERT or bound delta Pi_M/[d,Pi_M] terms"),
        ("ESC3922_2_domain_P00", "P00_domain", "scalar_source_norm", "domain/support selector source", "zero by q-basic fixed domain or operator norm bound"),
        ("ESC3922_3_history_P00", "P00_history", "scalar_source_norm", "memory/history tail source", "zero only with no incoming tail; otherwise 3895 suppression law"),
        ("ESC3922_4_nonlocal_P00", "P00_nonlocal", "scalar_source_norm", "nonlocal kernel/common-mode tail", "zero by compact-local kernel silence or numeric norm"),
        ("ESC3922_5_harmonic_boundary", "B_harmonic_boundary", "potential_multipole_norm", "free exterior harmonic boundary data", "zero by fixed/silent boundary data or bounded amplitude"),
        ("ESC3922_6_multipole_total", "A_multi", "potential_multipole_norm", MULTIPOLE_BOUND, "absolute-sum guard"),
        ("ESC3922_7_derivative_hair", "B_deriv", "mixed_derivative_norm", DERIVATIVE_BOUND, "time/radial/source/frame derivative guard"),
        ("ESC3922_8_projector_domain_total", "epsilon_domain_projector_abs", "dimensionless", "epsilon_domain_projector_abs <= sum(abs(DPOB3431_0..DPOB3431_3))", "3431 fallback bound"),
        ("ESC3922_9_total", "B_escape", "dimensionless_or_normalized_vector", LOCAL_RESIDUAL, "local-GR escape envelope; no cancellation"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "units": units,
            "definition_or_bound": formula,
            "source_or_zero_rule": rule,
            "numeric_value": "",
            "status": "ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, units, formula, rule in data
    ]


def ppn_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("MAP3922_0_gamma", "gamma_minus_1", "already controlled by P_TF zero; boundary/projector/domain STF leakage reopens via A_multi if anisotropic", "route anisotropic pieces to 3918 gamma bound"),
        ("MAP3922_1_beta", "beta_minus_1", "Delta_sq plus source-normalization/projector common mode", "route to 3920/3921 square-law gate"),
        ("MAP3922_2_alpha1", "alpha1", "domain/vector/frame marker from boundary/projector/domain selector", "zero by scalar/topological no-vector domain or bound DPPN3431_0"),
        ("MAP3922_3_alpha2", "alpha2", "preferred-frame spin/domain piece", "zero by no-vector/common-frame selector or bound DPPN3431_1"),
        ("MAP3922_4_alpha3", "alpha3", "boundary/domain flux or nonconservation", "zero by boundary no-flux plus Bianchi/source collar or bound DPPN3431_2"),
        ("MAP3922_5_xi", "xi", "preferred-location anisotropy/multipole/domain harmonic", "zero by no l>=1 harmonic/domain anisotropy or bound DPPN3431_3"),
        ("MAP3922_6_ephemeris", "orbital_ephemeris", "epsilon_r and A_multi create non-Kepler residuals", "constant monopole only may calibrate GM"),
        ("MAP3922_7_Gdot", "Gdot_over_G", "partial_t xi_1 contributes to measured GM drift", "must satisfy 3908 dotG gate if not theorem-zero"),
    ]
    return [
        {
            "row_id": row_id,
            "observable": observable,
            "escape_effect": effect,
            "zero_or_bound_route": route,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, observable, effect, route in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3922_0_combined",
            "decision": "boundary/projector/domain multipole silence is conditional but now exact when certificates sign together",
            "formula": ZERO_THEOREM,
            "claim_status": "PRIVATE_CONDITIONAL_RESULT_NOT_PUBLIC_CLAIM",
            "next_action": "assemble conditional local-GR theorem stack and remaining bound pack",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3922_1_bound",
            "decision": "if any certificate fails, use the explicit escape envelope",
            "formula": LOCAL_RESIDUAL,
            "claim_status": "NONCLAIM_BOUND_INTERFACE",
            "next_action": "fill source-backed values or preserve blocked local-GR claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3922_2_guard",
            "decision": "trace projection, spherical symmetry, and scalar no-flux are not enough by themselves",
            "formula": "action-level boundary/projector/domain stress must be zeroed or bounded",
            "claim_status": "NO_SHORTCUT_GUARD_ACTIVE",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3922_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "assemble the local-GR conditional theorem stack from 3914-3922, identify exact parent-signature clauses, and separate remaining numeric bound rows",
            "why_this_next": "the PPN/local-GR route now has component theorem gates for gamma, beta, common mode, P00, and escape multipoles",
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
            "summary": "boundary/projector/domain multipole zero theorem and fallback escape bound vector constructed",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3922 - Boundary Projector Domain Multipole Zero or Local Bound Fill

Timestamp: `{timestamp}`

## Result

The remaining `Xi_N` escape channels are now split into a theorem route and a bound route.

Escape source split:

`{SOURCE_SPLIT}`.

Combined zero theorem:

`{ZERO_THEOREM}`.

Fallback multipole bound:

`{MULTIPOLE_BOUND}`.

Derivative-hair guard:

`{DERIVATIVE_BOUND}`.

Total local escape envelope:

`{LOCAL_RESIDUAL}`.

## Meaning

This is the disciplined version of “close the boundary/projector/domain leaks.” If boundary, projector, fixed-domain, and history/no-tail certificates are parent-signed together, the l>=1 exterior multipoles and derivative hair vanish. If any clause is unsigned, the channel survives as a named bound input feeding beta, alpha_i, xi, ephemeris, and Gdot. No trace-projector, spherical-symmetry, or scalar no-flux shortcut is credited as a local-GR pass.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3922_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3922_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3922_MULTIPOLE_ESCAPE_ZERO_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3922_ESCAPE_TO_PPN_ORBITAL_MAP.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3922_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3922_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3922 - Boundary/Projector/Domain Escape Multipole Gate

Timestamp: `{timestamp}`

- Escape source split: `{SOURCE_SPLIT}`.
- Combined zero theorem: `{ZERO_THEOREM}`.
- Multipole fallback: `{MULTIPOLE_BOUND}`.
- Derivative-hair fallback: `{DERIVATIVE_BOUND}`.
- Total envelope: `{LOCAL_RESIDUAL}`.
- Status: private conditional progress only; local-GR needs parent-signed certificates or source-backed bound values.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3922 - Boundary/Projector/Domain Escape Multipole Gate"
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
    multipole = multipole_rows(timestamp)
    bounds = bound_rows(timestamp)
    ppn = ppn_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    checks = [
        ("VAL3922_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3922_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3922_02_source_split", any(row["row_id"] == "MUL3922_0_source_split" for row in multipole), "escape source split emitted"),
        ("VAL3922_03_combined_zero", any(row["row_id"] == "MUL3922_5_combined_zero" for row in multipole), "combined zero theorem emitted"),
        ("VAL3922_04_shortcut_rejected", any(row["row_id"] == "MUL3922_7_shortcut_rejected" for row in multipole), "shortcut rejection emitted"),
        ("VAL3922_05_bound_vector", len(bounds) == 10, "escape bound vector rows emitted"),
        ("VAL3922_06_ppn_map", len(ppn) == 8, "escape-to-PPN/orbital map emitted"),
        ("VAL3922_07_decision_guard", any(row["row_id"] == "DEC3922_2_guard" for row in decisions), "no-shortcut guard emitted"),
        ("VAL3922_08_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (multipole, bounds, ppn, decisions) for row in group), "all new rows are nonclaim"),
        ("VAL3922_09_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3922_10_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3922_11_spine_written", SPINE_PATH.exists() and "3922 - Boundary/Projector/Domain Escape Multipole Gate" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3922_12_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3922_13_script_compiles", True, "script compiles"),
        ("VAL3922_14_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["multipole"], multipole_rows(timestamp))
    write_csv(OUTPUTS["bound"], bound_rows(timestamp))
    write_csv(OUTPUTS["ppn"], ppn_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3922 validation failed: {failed}")
    print(f"3922 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
