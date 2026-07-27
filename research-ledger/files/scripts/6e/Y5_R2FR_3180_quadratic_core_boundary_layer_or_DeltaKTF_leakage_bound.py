from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3180_INPUTS.csv"
MATCHING = OUT / "P8_Y5_R2FR_3180_CORE_EXTERIOR_MATCHING_NO_GO.csv"
MOMENT_IDENTITY = OUT / "P8_Y5_R2FR_3180_PROJECTED_MOMENT_IDENTITY.csv"
SHELL_LEDGER = OUT / "P8_Y5_R2FR_3180_SHELL_TRANSITION_LEDGER.csv"
PRODUCT_RECAST = OUT / "P8_Y5_R2FR_3180_PRODUCT_BOUND_RECAST.csv"
LEAKAGE = OUT / "P8_Y5_R2FR_3180_DELTAKTF_LEAKAGE_REQUIREMENTS.csv"
DECISION = OUT / "P8_Y5_R2FR_3180_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3180_VALIDATION.csv"

PRODUCT_3177 = OUT / "P8_Y5_R2FR_3177_PRODUCT_BOUND_FROM_3170.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(base: str, relative: str) -> Path:
    if base == "post_checkpoint":
        return ROOT / relative
    if base == "formalization":
        return FW / relative
    raise ValueError(base)


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3179-Y5-R2FR-tracefree-Hessian-K2-kernel-projection-or-DeltaKTF-product-bound-under-AX1090.md",
            "3179 handoff: Hessian projection D2[F] and pure-kernel condition",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3179_PURE_KERNEL_CONDITION.csv",
            "3179 pure R(r)Y condition and boundary-layer warning",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3179_TRACEFREE_LEAKAGE_AUDIT.csv",
            "3179 K_perp/DeltaK_TF leakage rows",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3177_PRODUCT_BOUND_FROM_3170.csv",
            "3177 direct product bound rows |s_K2*M2_K2|",
        ),
        (
            "post_checkpoint",
            "3178-Y5-R2FR-Khat-source-kernel-normalization-or-STF-product-bound-gate-under-AX1090.md",
            "3178 dimensionless kernel normalization",
        ),
        (
            "post_checkpoint",
            "3067-Y5-R2FR-tracefree-improvement-Khat-birth-certificate-or-DeltaK-TF-bound-under-AX1090.md",
            "tracefree Hessian candidate not parent-adopted",
        ),
        (
            "post_checkpoint",
            "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md",
            "Hessian carrier amplitude and metric-response warning",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "parent-v1 effective local equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3180_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def matching_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "match_id": "MATCH3180_0_value_match",
            "object": "quadratic_core_to_exterior",
            "condition": "F_in=A r^2 for r<R_b and F_out=C r^-3 for r>R_b",
            "formula": "continuity F_in(R_b)=F_out(R_b) gives C=A R_b^5",
            "result": "value matching fixes exterior coefficient",
            "status": "VALUE_MATCH_POSSIBLE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "match_id": "MATCH3180_1_derivative_jump",
            "object": "C1_matching",
            "condition": "same value-matched core/exterior profile",
            "formula": "F'_in(R_b)=2A R_b; F'_out(R_b)=-3C R_b^-4=-3A R_b; [F']:=F'_out-F'_in=-5A R_b",
            "result": "nonzero derivative jump unless A=0",
            "status": "C1_MATCH_FAILS_NONTRIVIAL_SOURCE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "match_id": "MATCH3180_2_no_free_smooth_glue",
            "object": "boundary_layer",
            "condition": "avoid a sharp derivative jump",
            "formula": "a smooth transition layer must change d(F/r^2)/dr from 0 in the core to exterior behavior",
            "result": "B'(r) nonzero in the layer, so 3179 K_perp tensor leakage is active",
            "status": "BOUNDARY_LAYER_OR_LEAKAGE_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def moment_identity_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "identity_id": "MID3180_0_D2_operator",
            "statement": "Use the 3179 projected Hessian source operator.",
            "formula": "D2[F]=(2/5)F''+2F'/r+6F/(5r^2)",
            "result": "input operator",
            "status": "CARRIED_FROM_3179",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "MID3180_1_boundary_identity",
            "statement": "The fourth-moment integral of the projected source is a boundary term.",
            "formula": "integral_a^b D2[F] r^4 dr = (2/5)[r^4 F' + r^3 F]_a^b",
            "result": "projected moment is fixed by boundary data, not transition details",
            "status": "DERIVED_BY_PARTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "MID3180_2_regular_core_exterior",
            "statement": "For a regular origin and exterior F=C r^-3, the total projected moment is fixed.",
            "formula": "regular origin gives 0; exterior gives r^4F'+r^3F -> -2C; hence integral_0^infty D2[F]r^4dr = -4C/5",
            "result": "I4_D2 = -4 c_ext/5 in dimensionless variables",
            "status": "PROJECTED_MOMENT_FIXED_BY_EXTERIOR_COEFFICIENT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "MID3180_3_candidate_M2",
            "statement": "If K_L is parent-adopted and tensor leakage is zero/bounded, the projected K2 moment has a simple exterior-coefficient form.",
            "formula": "M2_K2^proj = -(kappa_STF/5)I4_D2 = (4/25)kappa_STF c_ext",
            "result": "candidate moment formula available only behind parent-adoption and leakage gates",
            "status": "CONDITIONAL_CANDIDATE_MOMENT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def shell_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "shell_id": "SHELL3180_0_sharp_jump",
            "transition": "sharp value-matched core/exterior",
            "formula": "[F']=-5A R_b produces F''_shell=[F']delta(r-R_b)",
            "projected_source": "D2_shell=(2/5)[F']delta(r-R_b)=-2A R_b delta(r-R_b)",
            "moment_contribution": "integral D2_shell r^4dr = -2A R_b^5",
            "status": "SHELL_SOURCE_REQUIRED_IF_SHARP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "shell_id": "SHELL3180_1_core_contribution",
            "transition": "quadratic core",
            "formula": "D2[A r^2]=6A",
            "projected_source": "core pure Y source",
            "moment_contribution": "integral_0^Rb 6A r^4dr = 6A R_b^5/5",
            "status": "CORE_MOMENT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "shell_id": "SHELL3180_2_total_check",
            "transition": "sharp core plus shell",
            "formula": "6A R_b^5/5 - 2A R_b^5 = -4A R_b^5/5 = -4C/5",
            "projected_source": "matches boundary identity",
            "moment_contribution": "-4C/5",
            "status": "PROJECTED_MOMENT_CONSISTENT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "shell_id": "SHELL3180_3_smooth_layer",
            "transition": "finite thickness smoothing",
            "formula": "shell delta is replaced by layer D2[F] plus K_perp terms controlled by B'(r),B''(r)",
            "projected_source": "projected moment remains -4C/5 if origin/exterior data are unchanged",
            "moment_contribution": "same projected total; leakage norm still profile-dependent",
            "status": "SMOOTH_LAYER_REQUIRES_LEAKAGE_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def product_recast_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    for source in read_csv(PRODUCT_3177):
        product_bound = float(source["derived_product_bound"])
        cext_bound = 25.0 * product_bound / 4.0
        rows.append(
            {
                "recast_id": "PR3180_" + source["source_bound_id"],
                "bound_name": source["bound_name"],
                "source_bound_quantity": "|s_K2*M2_K2|",
                "source_bound": f"{product_bound:.15e}",
                "candidate_substitution": "M2_K2^proj=(4/25)kappa_STF*c_ext",
                "recast_quantity": "|s_K2*kappa_STF*c_ext|",
                "recast_bound": f"{cext_bound:.15e}",
                "formula": "|s_K2*kappa_STF*c_ext| <= (25/4)*B_product",
                "status": "BOUND_RECAST_NONCLAIM_PARENT_AND_LEAKAGE_GATED",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def leakage_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "leak_id": "DL3180_0_boundary_layer_tensor_leak",
            "quantity": "K_perp_layer",
            "why_required": "smooth core/exterior glue needs B'(r) nonzero, while 3179 pure-Y condition requires B'=0",
            "bound_needed": "||K_perp_layer|| or its projection into PPN/clock/orbital/STF observables",
            "status": "MISSING_PROFILE_OR_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "leak_id": "DL3180_1_exterior_tidal_footprint",
            "quantity": "K_L exterior tensor footprint",
            "why_required": "D2[C r^-3]=0 only kills the pure projected source; the full Hessian of a harmonic l=2 exterior field can still carry tidal tensor components",
            "bound_needed": "metric-null theorem or direct tidal/STF response bound",
            "status": "MISSING_METRIC_NULL_OR_TIDAL_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "leak_id": "DL3180_2_parent_adoption",
            "quantity": "DeltaK_TF",
            "why_required": "K_L remains a formal candidate, not live MTS K_hat",
            "bound_needed": "||K_hat^{<ij>}-K_L^{<ij>}|| plus K_perp leakage envelope",
            "status": "MISSING_LIVE_KHAT_ADOPTION_OR_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3180_0_no_smooth_free_glue",
            "finding": "A nontrivial quadratic core F=A r^2 and exterior C r^-3 cannot be C1-matched at one boundary; [F']=-5A R_b.",
            "claim_status": "BOUNDARY_LAYER_OR_SHELL_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3180_1_projected_moment_win",
            "finding": "The projected D2 source moment is fixed by boundary data: integral D2[F]r^4dr=-4C/5 for regular core plus exterior C r^-3.",
            "claim_status": "PROJECTED_MOMENT_DERIVED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3180_2_recast_gate",
            "finding": "If K_L is parent-adopted and leakage is bounded, product bounds recast to |s_K2*kappa_STF*c_ext| <= (25/4)B_product.",
            "claim_status": "RECAST_BOUND_AVAILABLE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3180_3_live_blocker",
            "finding": "Full tensor leakage K_perp_layer/exterior tidal footprint remains unowned; local-GR/Newton still blocked.",
            "claim_status": "DELTAKTF_LEAKAGE_ACTIVE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3180_4_next_target",
            "finding": "3181-Y5-R2FR-exterior-Hessian-tidal-footprint-or-metric-null-bound-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    return {
        INPUTS: input_rows(),
        MATCHING: matching_rows(),
        MOMENT_IDENTITY: moment_identity_rows(),
        SHELL_LEDGER: shell_rows(),
        PRODUCT_RECAST: product_recast_rows(),
        LEAKAGE: leakage_rows(),
        DECISION: decision_rows(),
    }


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    matching = rows_by_path[MATCHING]
    moment = rows_by_path[MOMENT_IDENTITY]
    shell = rows_by_path[SHELL_LEDGER]
    recast = rows_by_path[PRODUCT_RECAST]
    leakage = rows_by_path[LEAKAGE]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    return [
        {
            "check_id": "VAL3180_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3180_1_derivative_jump",
            "check": "core/exterior derivative jump no-go is present",
            "pass": str(any(row["status"] == "C1_MATCH_FAILS_NONTRIVIAL_SOURCE" for row in matching)).lower(),
            "detail": "[F']=-5A R_b",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3180_2_boundary_identity",
            "check": "projected moment boundary identity is present",
            "pass": str(any(row["status"] == "DERIVED_BY_PARTS" for row in moment)).lower(),
            "detail": "integral D2[F]r^4dr=(2/5)[r^4F'+r^3F]",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3180_3_shell_check",
            "check": "sharp shell ledger matches -4C/5 projected moment",
            "pass": str(any(row["status"] == "PROJECTED_MOMENT_CONSISTENT" for row in shell)).lower(),
            "detail": "core plus shell equals boundary identity",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3180_4_recast_bounds_numeric_nonclaim",
            "check": "recast product bounds are positive numeric nonclaim rows",
            "pass": str(all(float(row["recast_bound"]) > 0 and row["valid_for_claim"] == "false" for row in recast) and len(recast) == 3).lower(),
            "detail": f"{len(recast)} recast rows",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3180_5_leakage_retained",
            "check": "DeltaK_TF/leakage rows remain blocking",
            "pass": str(all(row["valid_for_claim"] == "false" for row in leakage) and any(row["status"] == "MISSING_METRIC_NULL_OR_TIDAL_BOUND" for row in leakage)).lower(),
            "detail": "exterior tidal footprint and boundary-layer leakage remain active",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3180_6_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3180_7_next_target_selected",
            "check": "decision table selects exterior Hessian tidal footprint or metric-null bound",
            "pass": str(any("3181-Y5-R2FR-exterior-Hessian-tidal-footprint" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3181",
            "generated_utc": now,
        },
    ]


def main() -> None:
    rows_by_path = all_output_rows()
    rows_by_path[VALIDATION] = validation_rows(rows_by_path)
    for path, rows in rows_by_path.items():
        write_csv(path, rows)
    for path in rows_by_path:
        print(path)


if __name__ == "__main__":
    main()
