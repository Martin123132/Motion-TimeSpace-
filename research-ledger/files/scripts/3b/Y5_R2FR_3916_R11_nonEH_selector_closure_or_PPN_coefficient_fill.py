from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3916"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3916-Y5-R2FR-R11-nonEH-selector-closure-or-PPN-coefficient-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3916_SOURCE_REGISTER.csv",
    "fork": SRC / "P8_Y5_R2FR_3916_R11_SELECTOR_FORK.csv",
    "families": SRC / "P8_Y5_R2FR_3916_R11_FAMILY_CLOSURE_MATRIX.csv",
    "ppn": SRC / "P8_Y5_R2FR_3916_PPN_COEFFICIENT_IMPACT.csv",
    "fill": SRC / "P8_Y5_R2FR_3916_COEFFICIENT_FILL_QUEUE.csv",
    "promotion": SRC / "P8_Y5_R2FR_3916_LOCAL_GR_PROMOTION_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3916_BRANCH_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3916_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3916_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3916_VALIDATION.csv",
}

EH_ROUTE = "EH-selector route: S_Q is local, diffeo invariant, second-order, Q is the only public metric/coframe, and no independent scalar/vector/tensor operator slots exist; therefore active R11/non-EH operator coefficients are absent or topological"
DZ_ROUTE = "double-zero route: S_R11=integral sqrt(-g) sum_A F_A(Sigma_loc) O_A with Sigma_loc=G_AB Y_loc^A Y_loc^B, F_A(0)=F_A'(0)=0, and no independent multiplier stress; therefore delta S_R11|_{Sigma_loc=0}=0"
R11_ZERO = "DeltaE_R11^{mu nu}=0 and all R11-fed PPN coefficients vanish inside B_loc if either EH_ROUTE or DZ_ROUTE is parent-owned"
R11_FALLBACK = "if neither route is parent-owned for a family, fill its weak-field coefficient row and score gamma,beta,alpha_i,xi,zeta_i with no cancellation"
NEXT_TARGET = "3917-Y5-R2FR-PPN-coefficient-fill-runner-or-parent-adoption-ledger.md"


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
        ("SRC3916_00_next", SRC / "P8_Y5_R2FR_3915_NEXT_TARGET.csv", "NEXT3915_0", "3915 selected R11 target"),
        ("SRC3916_01_contract", SRC / "P8_Y5_R2FR_3915_STATIONARY_LOCAL_BRANCH_CONTRACT.csv", "BLC3915_1_public_metric", "3915 public metric clause"),
        ("SRC3916_02_ppn_total", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_8_total", "3915 PPN residual envelope"),
        ("SRC3916_03_promotion", SRC / "P8_Y5_R2FR_3915_LOCAL_GR_PROMOTION_GATE.csv", "PROM3915_1_R11", "3915 R11 promotion blocker"),
        ("SRC3916_04_EH_selector", SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv", "EH3906_0_selector", "3906 EH operator selector"),
        ("SRC3916_05_EH_filter", SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv", "EH3906_2_nonEH_filter", "3906 non-EH filter"),
        ("SRC3916_06_normal", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_2_interactions", "3905 no linear hidden/source shadow"),
        ("SRC3916_07_L2", SRC / "P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv", "L2_double_zero_sufficient", "double-zero sufficiency lemma"),
        ("SRC3916_08_L4", SRC / "P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv", "L4_selector_theorem_target", "R11 selector theorem target"),
        ("SRC3916_09_audit", SRC / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv", "source_normalization_operator", "R11 operator audit"),
        ("SRC3916_10_mapping", SRC / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv", "source_normalization_operator", "double-zero operator mapping"),
        ("SRC3916_11_gates", SRC / "P8_DOUBLE_ZERO_R11_GATES.csv", "G2_all_R11_factorized", "double-zero factorization gate"),
        ("SRC3916_12_gates_stress", SRC / "P8_DOUBLE_ZERO_R11_GATES.csv", "G4_stress_Bianchi_closed", "stress/Bianchi gate"),
        ("SRC3916_13_parent_clause", SRC / "P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv", "C2_R11_factorization", "R11 parent factorization clause"),
        ("SRC3916_14_parent_guard", SRC / "P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv", "C3_no_independent_multiplier", "no independent multiplier guard"),
        ("SRC3916_15_coeff_gamma", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_00_delta_gamma_R11", "delta gamma R11 coefficient"),
        ("SRC3916_16_coeff_beta", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_04_delta_beta_R11", "delta beta R11 coefficient"),
        ("SRC3916_17_coeff_total", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_12_R11_total", "R11 total coefficient"),
        ("SRC3916_18_projector", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_13_projector_stress", "projector stress coefficient"),
        ("SRC3916_19_fill_gamma", SRC / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv", "FILL3887_1_gamma_R11", "gamma R11 fill pivot"),
        ("SRC3916_20_fill_beta", SRC / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv", "FILL3887_2_beta_source", "beta source fill pivot"),
        ("SRC3916_21_fill_stress", SRC / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv", "FILL3887_5_projector_stress", "projector stress fill pivot"),
        ("SRC3916_22_validation", SRC / "P8_Y5_BRR545_3915_VALIDATION.csv", "VAL3915_14_no_pycache", "3915 validation handoff"),
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


def fork_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("FORK3916_0_EH", "EH-selector closure route", EH_ROUTE, "CONDITIONAL_ROUTE_STRONG_IF_3906_ADOPTED", "requires parent adoption of EH operator selector"),
        ("FORK3916_1_DZ", "double-zero selector closure route", DZ_ROUTE, "CONDITIONAL_ROUTE_STRONG_IF_FACTORISATION_DERIVED", "requires Y_loc ownership, Sigma_loc positivity, all R11 families factorized, no multiplier stress"),
        ("FORK3916_2_zero", "R11 zero consequence", R11_ZERO, "CONDITIONAL_R11_ZERO_IF_ROUTE_SIGNED", "not valid for claim until a route is parent-owned"),
        ("FORK3916_3_fallback", "coefficient fill route", R11_FALLBACK, "EXECUTABLE_FALLBACK", "use if any family lacks EH absence/topological/double-zero proof"),
    ]
    return [
        {
            "row_id": row_id,
            "route": route,
            "formula_or_statement": statement,
            "status": status,
            "remaining_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, route, statement, status, gap in rows
    ]


def family_rows(timestamp: str) -> list[dict[str, Any]]:
    families = [
        ("R11F3916_0_boundary", "boundary_topological_terms", "topological/boundary scalar no-flux or double-zero boundary selector", "alpha3;xi;boundary"),
        ("R11F3916_1_R2", "R2_fR_scalar_mode", "absent/infinite-mass/no-coupling or c_R2(Sigma_loc)=O(Sigma_loc^2)", "gamma;beta;R10"),
        ("R11F3916_2_RicciWeyl", "Ricci_Weyl_squared", "Gauss-Bonnet/topological combination or double-zero curvature-squared coefficient", "gamma;beta;xi"),
        ("R11F3916_3_scalar_tensor", "scalar_tensor_class_metric", "fixed scalar/class field or double-zero scalar coupling", "gamma;beta;R10"),
        ("R11F3916_4_vector", "vector_preferred_frame", "no-vector selector or double-zero vector coefficient", "alpha1;alpha2;alpha3;xi"),
        ("R11F3916_5_torsion", "torsion_nonmetricity", "Levi-Civita/no-independent-connection or double-zero torsion/nonmetricity", "gamma;preferred-frame"),
        ("R11F3916_6_bulkX", "bulk_X_force_law", "source charge zero plus double-zero coupling or finite-range bound", "R10;gamma;beta"),
        ("R11F3916_7_nonlocal", "nonlocal_memory_kernel", "compact-local kernel silence or double-zero kernel norm", "alpha3;xi;Gdot;R10"),
        ("R11F3916_8_source_norm", "source_normalization_operator", "3914 source coupling zero plus double-zero source-normalization operator", "beta;alpha_i;source"),
        ("R11F3916_9_projector", "projector_domain_stress", "topological/metric-independent projector or bounded retained stress", "gamma;beta;alpha_i;zeta"),
    ]
    return [
        {
            "row_id": row_id,
            "operator_family": family,
            "closure_route": route,
            "feeds": feeds,
            "EH_selector_status": "ZERO_IF_3906_EH_SELECTOR_PARENT_ADOPTED",
            "double_zero_status": "CONTRACT_READY_NOT_PARENT_DERIVED",
            "fallback_status": "FILL_COEFFICIENT_IF_NOT_CLOSED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, family, route, feeds in families
    ]


def ppn_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PPNI3916_0_gamma", "delta_gamma_R11", "0 if all active R11 families close by EH/DZ route", "otherwise fill weak-field anisotropic/spatial-temporal potential split"),
        ("PPNI3916_1_beta", "delta_beta_R11", "0 if all second-order R11/source families close by EH/DZ route", "otherwise fill second-order non-EH operator contributions"),
        ("PPNI3916_2_alpha_i", "alpha1,alpha2,alpha3", "0 if vector/domain/boundary/fux/nonconservation families close", "otherwise fill preferred-frame and alpha3 product rows individually"),
        ("PPNI3916_3_xi", "xi", "0 if anisotropic/STF/nonlocal families close", "otherwise fill preferred-location coefficient row"),
        ("PPNI3916_4_zeta", "zeta_i", "0 if projector/stress/non-Hilbert leakage closes", "otherwise fill stress vector"),
        ("PPNI3916_5_total", "DeltaE_R11_munu", R11_ZERO, "otherwise use PPNR3915_8 envelope plus COEF3886 rows"),
    ]
    return [
        {
            "row_id": row_id,
            "coefficient": coeff,
            "conditional_impact": impact,
            "fallback_impact": fallback,
            "status": "CONDITIONAL_ZERO_OR_FILL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, coeff, impact, fallback in rows
    ]


def fill_rows(timestamp: str) -> list[dict[str, Any]]:
    fills = [
        ("FILL3916_0_delta_gamma_R11", "delta_gamma_R11", "gamma_minus_1", "first coefficient fill if EH-only/R11 factorization fails", "FILL3887_1_gamma_R11"),
        ("FILL3916_1_delta_beta_R11", "delta_beta_R11", "beta_minus_1", "fill after gamma or together with second-order source law", "COEF3886_04_delta_beta_R11"),
        ("FILL3916_2_delta_beta_source", "delta_beta_source", "beta_minus_1", "fill A_source/B_source if source residual-lock fails", "FILL3887_2_beta_source"),
        ("FILL3916_3_vector_pref", "alpha1,alpha2", "preferred_frame", "fill if no-vector selector fails", "COEF3886_06_alpha1;COEF3886_07_alpha2"),
        ("FILL3916_4_alpha3", "alpha3", "preferred_frame_conservation", "fill individual alpha3 channels; no total cancellation", "FILL3887_0_boundary_alpha3"),
        ("FILL3916_5_projector_stress", "T_extra_munu_or_c_projector_domain_stress", "zeta_i;gamma;beta;alpha_i", "fill if topological projector proof fails", "FILL3887_5_projector_stress"),
        ("FILL3916_6_alpha_lambda", "alpha(lambda)", "R10", "fill real bound curve/prediction if finite-range tail survives", "FILL3887_3_alpha_lambda"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "observable": obs,
            "priority_reason": reason,
            "source_anchor": anchor,
            "numeric_value": "",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, obs, reason, anchor in fills
    ]


def promotion_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PROM3916_0_EH_selector", "EH selector route", "CONDITIONAL_NOT_PARENT_GLOBAL", "closes R11 only if 3906 branch adopted"),
        ("PROM3916_1_double_zero", "double-zero route", "CONTRACT_READY_NOT_DERIVED", "fails until G0/G2/G4 gates pass"),
        ("PROM3916_2_coefficients", "coefficient fallback", "READY_AS_QUEUE_NOT_SCORED", "numeric/source rows still missing"),
        ("PROM3916_3_local_GR", "public local-GR claim", "FORBIDDEN_NOW", "R11 route conditional and/or coefficients unfilled"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "current_result": result,
            "reason": reason,
            "valid_for_local_GR_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, result, reason in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3916_0_fork",
            "decision": "R11/non-EH silence now has two clean closure routes and one coefficient fallback route",
            "claim_status": "CONDITIONAL_ROUTE_OR_FILL_NOT_PUBLIC_CLAIM",
            "reason": "EH selector can remove active families; double-zero can suppress retained families; otherwise coefficient rows are queued",
            "next_action": "either parent-adoption ledger for EH/DZ route or fill first PPN coefficient rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3916_1_no_promotion",
            "decision": "do not promote local GR/PPN",
            "claim_status": "NO_LOCAL_GR_CLAIM",
            "reason": "neither EH route nor double-zero route is globally parent-owned, and coefficients are not numeric",
            "next_action": "3917 should make this either an adoption ledger or executable fill runner",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3916_2_next",
            "decision": "next target is PPN coefficient fill runner or parent adoption ledger",
            "claim_status": "NEXT_TARGET_SELECTED",
            "reason": "the derivation path is maximally compressed; remaining progress needs either parent ownership evidence or coefficient data rows",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3916_0",
            "next_doc": NEXT_TARGET,
            "next_script": "scripts/Y5_R2FR_3917_PPN_coefficient_fill_runner_or_parent_adoption_ledger.py",
            "target": "choose between an explicit parent-adoption ledger for EH/DZ R11 silence and the first executable PPN coefficient fill rows; default to gamma_R11 and beta_source if no stronger parent evidence appears",
            "why_this_next": "3916 compresses R11 into a fork; now the project needs either parent ownership evidence or actual coefficient rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "result": "R11/non-EH blocker compressed into EH-selector route, double-zero route, or coefficient-fill queue",
            "local_gr_claim": False,
            "ppn_claim": False,
            "new_forward_progress": "dominant PPN blocker is now a precise fork rather than a vague missing local-GR residual",
            "primary_blocker": "parent adoption evidence or executable PPN coefficient rows",
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(sources: list[dict[str, Any]], timestamp: str) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3916 — R11/non-EH Selector Closure or PPN Coefficient Fill

Timestamp: `{timestamp}`

## Result

This checkpoint compresses the dominant local-GR blocker into a clean fork.

EH route:
`{EH_ROUTE}`

Double-zero route:
`{DZ_ROUTE}`

R11 zero consequence:
`{R11_ZERO}`

Fallback:
`{R11_FALLBACK}`

## Meaning

- If the EH selector is parent-adopted, active non-EH/R11 families are absent or topological.
- If retained R11 families are parent-factorized by a double-zero local selector, their first variation vanishes on the local branch.
- If neither route is parent-owned, the project must fill executable PPN coefficient rows.
- No local-GR/PPN claim is promoted here.

## Source Register

- Source rows found: `{found}/{len(sources)}`
- Register: `{rel(OUTPUTS['sources'])}`
- Validation: `{rel(OUTPUTS['validation'])}`

## Generated Tables

- `{rel(OUTPUTS['fork'])}`
- `{rel(OUTPUTS['families'])}`
- `{rel(OUTPUTS['ppn'])}`
- `{rel(OUTPUTS['fill'])}`
- `{rel(OUTPUTS['promotion'])}`
- `{rel(OUTPUTS['decision'])}`
- `{rel(OUTPUTS['next'])}`

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3916 R11 NONEH SELECTOR FORK -->
## 3916 R11/non-EH Selector Fork

Timestamp: `{timestamp}`

EH route:
`{EH_ROUTE}`

Double-zero route:
`{DZ_ROUTE}`

R11 zero consequence:
`{R11_ZERO}`

Fallback:
`{R11_FALLBACK}`

Decision: R11/non-EH local-GR obstruction is compressed into two conditional closure routes or a coefficient-fill queue. No PPN/local-GR promotion yet.
<!-- END 3916 R11 NONEH SELECTOR FORK -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3916 R11 NONEH SELECTOR FORK -->"
    end = "<!-- END 3916 R11 NONEH SELECTOR FORK -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    fork: list[dict[str, Any]],
    families: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    fill: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL3916_0_sources", "all cited source paths and needles resolve", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} source rows found"))
    checks.append(("VAL3916_1_EH_route", "EH selector route emitted", any(EH_ROUTE in row["formula_or_statement"] for row in fork), rel(OUTPUTS["fork"])))
    checks.append(("VAL3916_2_DZ_route", "double-zero route emitted", any(DZ_ROUTE in row["formula_or_statement"] for row in fork), rel(OUTPUTS["fork"])))
    checks.append(("VAL3916_3_R11_zero", "R11 zero consequence emitted", any(R11_ZERO in row["formula_or_statement"] for row in fork) and any(R11_ZERO in row["conditional_impact"] for row in ppn), rel(OUTPUTS["ppn"])))
    checks.append(("VAL3916_4_families", "R11 family matrix emitted", len(families) >= 10 and {"vector_preferred_frame", "source_normalization_operator", "projector_domain_stress"}.issubset({row["operator_family"] for row in families}), rel(OUTPUTS["families"])))
    checks.append(("VAL3916_5_fill_queue", "coefficient fill queue emitted", len(fill) >= 7 and {"delta_gamma_R11", "delta_beta_R11", "T_extra_munu_or_c_projector_domain_stress"}.issubset({row["symbol"] for row in fill}), rel(OUTPUTS["fill"])))
    checks.append(("VAL3916_6_no_promotion", "promotion gates forbid local-GR claim", any(row["current_result"] == "FORBIDDEN_NOW" for row in promotion) and all(str(row.get("valid_for_local_GR_claim")) == "False" for row in promotion), rel(OUTPUTS["promotion"])))
    checks.append(("VAL3916_7_no_claim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim")) == "False" for row in fork + families + ppn + fill + promotion + decision), "valid_for_claim false across generated rows"))
    checks.append(("VAL3916_8_next", "next target is PPN fill/adoption ledger", "3917-Y5-R2FR-PPN" in read_text(OUTPUTS["next"]), rel(OUTPUTS["next"])))
    checks.append(("VAL3916_9_doc", "3916 markdown checkpoint written", DOC_PATH.exists() and "R11/non-EH Selector" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3916_10_spine", "spine updated with 3916 block", SPINE_PATH.exists() and "BEGIN 3916 R11 NONEH SELECTOR FORK" in read_text(SPINE_PATH), rel(SPINE_PATH)))
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
    checks.append(("VAL3916_11_csv_parse", "all generated CSV outputs parse cleanly", csv_parse_ok, "; ".join(parse_details)))
    fwb_hits = list(FWB.rglob("*3916*")) if FWB.exists() else []
    checks.append(("VAL3916_12_no_formalization_workbench_edits", "no 3916 files generated in formalization-workbench", not fwb_hits, "; ".join(str(path) for path in fwb_hits[:10]) or "no formalization-workbench hits"))
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    checks.append(("VAL3916_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, "; ".join(str(path) for path in pycache_hits[:10]) or "no __pycache__"))
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
    fork = fork_rows(timestamp)
    families = family_rows(timestamp)
    ppn = ppn_rows(timestamp)
    fill = fill_rows(timestamp)
    promotion = promotion_rows(timestamp)
    decision = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["fork"], fork)
    write_csv(OUTPUTS["families"], families)
    write_csv(OUTPUTS["ppn"], ppn)
    write_csv(OUTPUTS["fill"], fill)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, fork, families, ppn, fill, promotion, decision, timestamp)
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
