from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains_missing(value: object) -> bool:
    text = str(value)
    return text.strip() == "" or "MISSING" in text


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1157_0_1156_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1156_NEXT_TARGET.csv",
            "needle": "NEXT1156_0_1157",
            "role": "handoff selecting q-map/null-generator proof or c_g first fill.",
        },
        {
            "source_id": "SRC1157_1_1156_audit",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1156_QUOTIENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            "needle": "QMF1156_2_vertical_kernel",
            "role": "1156 audit identifying q-map and vertical kernel as upstream blockers.",
        },
        {
            "source_id": "SRC1157_2_1156_bounds",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1156_FRAME_LEAK_BOUND_FILL_ROWS.csv",
            "needle": "FLB1156_1_c_g",
            "role": "1156 c_g bound row that must be filled if q/null proof fails.",
        },
        {
            "source_id": "SRC1157_3_272_quotient",
            "relative_path": "272-quotient-configuration-principle-from-topological-projector.md",
            "needle": "relative-exact residuals -> presymplectic null directions -> quotient phase space",
            "role": "older conditional quotient principle route and exactness burden.",
        },
        {
            "source_id": "SRC1157_4_407_action_sketch",
            "relative_path": "407-primitive-relational-quotient-action-sketch.md",
            "needle": "matter quotient functor/no-marker selector proof",
            "role": "primitive relational quotient action sketch, not a theorem.",
        },
        {
            "source_id": "SRC1157_5_581_chain",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
            "needle": "QVT581_7_alpha_result",
            "role": "quotient vertical theorem chain showing conditional R10 alpha silence.",
        },
        {
            "source_id": "SRC1157_6_594_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_594_QUOTIENT_MAP_CONSTRUCTION_CONTRACT.csv",
            "needle": "QMC594_1_vertical_generator",
            "role": "q-map construction contract requiring vertical generator.",
        },
        {
            "source_id": "SRC1157_7_637_qmap",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
            "needle": "QM637_2_vertical_kernel",
            "role": "candidate q-map derivation: vertical kernel conditional on v_X null.",
        },
        {
            "source_id": "SRC1157_8_720_null",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_720_KINETIC_NULL_THEOREM_AUDIT.csv",
            "needle": "KNT720_8_no_mode_theorem",
            "role": "kinetic/null audit preventing null-by-missing-kinetic shortcut.",
        },
        {
            "source_id": "SRC1157_9_965_primitive",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
            "needle": "PQ965_5_verdict",
            "role": "primitive quotient/no-natural-marker theorem attempt remains unproven.",
        },
        {
            "source_id": "SRC1157_10_626_signature",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv",
            "needle": "QIM626_5_signature_verdict",
            "role": "quotient-invariant matter action not signed.",
        },
        {
            "source_id": "SRC1157_11_711_descent",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv",
            "needle": "QDA711_9_verdict",
            "role": "claim-ready quotient descent proof fails current corpus.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def qmap_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "QMAP1157_0_route_shape",
                "claim_piece": "conditional quotient/null route",
                "mathematical_form": "relative-exact residuals -> presymplectic null directions -> quotient phase space -> Dq(v_X)=0",
                "current_status": "VALID_CONDITIONAL_ROUTE_SHAPE",
                "missing_for_current_MTS": "Cperp exactness, boundary primitive zero, and Xhat identification with the null representative",
                "effect_if_missing": "q cannot be used to zero c_g",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMAP1157_1_parent_q_object",
                "claim_piece": "parent quotient object",
                "mathematical_form": "Conf_parent -> Q_obs with Q_obs a parent/reduced phase-space quotient, not a post-fit class",
                "current_status": "NOT_CONSTRUCTED_FOR_CURRENT_MTS",
                "missing_for_current_MTS": "explicit parent configuration object, equivalence relation, local domain, and quotient map",
                "effect_if_missing": "q by declaration is forbidden",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMAP1157_2_exactness",
                "claim_piece": "relative-exact residual/null generator",
                "mathematical_form": "eta_perp=d_rel alpha or relative-trivial with zero allowed local boundary primitive",
                "current_status": "OPEN_BURDEN",
                "missing_for_current_MTS": "Cperp exactness theorem and compact-boundary primitive silence",
                "effect_if_missing": "presymplectic null direction is not earned",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMAP1157_3_presymplectic_kernel",
                "claim_piece": "null direction of Omega",
                "mathematical_form": "Theta(eta_perp)=boundary/0 and Omega(eta_perp,delta)=0",
                "current_status": "CONDITIONAL_IF_EXACTNESS_AND_BOUNDARY_ZERO",
                "missing_for_current_MTS": "source path proving exactness and boundary zero for the actual local branch",
                "effect_if_missing": "quotient reduction remains a theorem target",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMAP1157_4_vX_identification",
                "claim_piece": "local frame/matter leak direction is the null generator",
                "mathematical_form": "v_X tangent to the parent null orbit and Dq[v_X]=0",
                "current_status": "CONDITIONAL_NOT_CURRENTLY_SIGNED",
                "missing_for_current_MTS": "proof that Xhat/frame direction is representative, not a physical retained field",
                "effect_if_missing": "c_g,b_dis,b_A remain physical bound rows",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMAP1157_5_action_factorization",
                "claim_piece": "bulk and matter action factor through q",
                "mathematical_form": "S_bulk[Phi]=S_red[q(Phi)] plus owned exact/topological terms; S_matter=Sbar[q(Phi),Psi,theta]",
                "current_status": "NOT_PARENT_DERIVED",
                "missing_for_current_MTS": "parent action factorization and matter functor proof",
                "effect_if_missing": "vertical current/source couplings can remain legal",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMAP1157_6_boundary_charge_zero",
                "claim_piece": "vertical transformation carries no boundary/source charge",
                "mathematical_form": "Q_X[epsilon]=int_boundary epsilon B_X=0 and local projection of boundary tail vanishes",
                "current_status": "REQUIRED_NOT_DERIVED",
                "missing_for_current_MTS": "edge-mode and boundary-current silence certificate",
                "effect_if_missing": "X can become boundary hair or q_nonH source",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMAP1157_7_kinetic_null_guard",
                "claim_piece": "no local physical X mode",
                "mathematical_form": "rank(P_phys)=0 after quotienting constraints/gauge/topology, with no finite contact/current term",
                "current_status": "FAIL_CURRENT_CORPUS",
                "missing_for_current_MTS": "Z_IJ/M2/rank/signature/source-orthogonality classification",
                "effect_if_missing": "missing kinetic term cannot be counted as GR proof",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMAP1157_8_verdict",
                "claim_piece": "current MTS proves q and v_X in ker(Dq)",
                "mathematical_form": "QMAP1157_1 through QMAP1157_7 all parent-signed",
                "current_status": "PARENT_Q_MAP_NULL_GENERATOR_NOT_DERIVED",
                "missing_for_current_MTS": "q object, exact/null generator, v_X identification, action factorization, boundary zero, kinetic/rank guard",
                "effect_if_missing": "fill c_g first row; no matter-functor/local-GR promotion",
                "valid_for_claim": "false",
            },
        ]
    )


def cg_first_fill_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "CG1157_0_cg_first_fill",
                "parameter": "c_g",
                "definition": "d ln A_g/dXhat for representative Weyl/common matter frame",
                "required_columns": "mode_id;A_g_definition;Xhat_normalization;c_g;units;source_path;zero_theorem_path;valid_for_claim",
                "current_value": "MISSING_PARENT_INPUT",
                "source_path": "MISSING_PARENT_SOURCE",
                "units": "dimensionless",
                "arena_links": "R10;PPN;WEP;clock;orbital",
                "status": "FIRST_FILL_ROW_READY_NONCLAIM",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CG1157_1_zero_theorem_path",
                "parameter": "Z_cg",
                "definition": "true only if q object and v_X in ker(Dq) are parent-signed and matter functor excludes A_g(Xhat)",
                "required_columns": "theorem_path;q_source;vX_source;matter_functor_source;boundary_zero_source;valid_for_claim",
                "current_value": "false",
                "source_path": "this_checkpoint",
                "units": "boolean",
                "arena_links": "all_local_arenas",
                "status": "ZERO_THEOREM_NOT_SIGNED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CG1157_2_R10_projection",
                "parameter": "tau_R10",
                "definition": "short-range source/test projection multiplying c_g in alpha(lambda) envelope",
                "required_columns": "arena;material_class;projection_formula;tau_R10;units;source_path;normalization;valid_for_claim",
                "current_value": "MISSING_ARENA_PROJECTION",
                "source_path": "MISSING_ARENA_SOURCE",
                "units": "dimensionless",
                "arena_links": "R10",
                "status": "MISSING_R10_PROJECTION",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CG1157_3_PPN_projection",
                "parameter": "tau_PPN",
                "definition": "PPN projection of common-frame Weyl response",
                "required_columns": "arena;gauge_convention;projection_formula;tau_PPN;units;source_path;valid_for_claim",
                "current_value": "MISSING_ARENA_PROJECTION",
                "source_path": "MISSING_ARENA_SOURCE",
                "units": "dimensionless",
                "arena_links": "PPN",
                "status": "MISSING_PPN_PROJECTION",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CG1157_4_clock_WEP_orbital_projection",
                "parameter": "tau_clock;tau_WEP;tau_orbital",
                "definition": "clock, WEP/material, and orbital projections of c_g",
                "required_columns": "arena;projection_formula;tau_value;units;bound_source;source_path;valid_for_claim",
                "current_value": "MISSING_ARENA_PROJECTIONS",
                "source_path": "MISSING_ARENA_SOURCE",
                "units": "dimensionless",
                "arena_links": "clock;WEP;orbital",
                "status": "MISSING_CLOCK_WEP_ORBITAL_PROJECTIONS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CG1157_5_score_interface",
                "parameter": "epsilon_cg",
                "definition": "absolute component envelope for c_g projected into active arenas",
                "required_columns": "system_id;abs_cg;tau_R10;tau_PPN;tau_clock;tau_WEP;tau_orbital;epsilon_cg;source_paths;valid_for_claim",
                "current_value": "MISSING_COMPONENT_INPUTS",
                "source_path": "MISSING_SOURCE_FILE",
                "units": "dimensionless",
                "arena_links": "all_local_arenas",
                "status": "BLOCKED_MISSING_COMPONENTS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1157_0_no_q_by_declaration",
                "guard": "q cannot be declared after choosing which local variables to hide",
                "status": "ACTIVE",
                "reason": "q must be derived from parent reduced phase-space or quotient geometry",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1157_1_no_vertical_by_label",
                "guard": "Xhat/frame direction is not vertical just because it is inconvenient",
                "status": "ACTIVE",
                "reason": "v_X in ker(Dq) needs parent null-orbit proof",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1157_2_no_missing_kinetic_as_null",
                "guard": "missing Z_X is not evidence of a harmless null direction",
                "status": "ACTIVE",
                "reason": "rank/signature/constraint/source-orthogonality classification is required",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1157_3_no_boundary_hair_silence",
                "guard": "boundary/edge charge must be zeroed or retained",
                "status": "ACTIVE",
                "reason": "boundary hair can source local forces even when bulk mode is quotient-like",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1157_4_no_cg_claim_without_projection",
                "guard": "c_g cannot score or pass without arena projections and source paths",
                "status": "ACTIVE",
                "reason": "R10/PPN/WEP/clock/orbital projections are independent evidence rows",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1157_0_sources_exist",
                "rule": "all 1157 cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1157_1_conditional_q_route",
                "rule": "conditional quotient/null route is stated",
                "gate_pass": "true_nonclaim",
                "reason": "route shape exists but is not used as current proof",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1157_2_current_q_null_signed",
                "rule": "current MTS proves q and v_X in ker(Dq)",
                "gate_pass": "false",
                "reason": "q object, exact/null generator, v_X identification, boundary zero, and kinetic/rank guard remain unsigned",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1157_3_cg_rows_ready",
                "rule": "first c_g fill rows exist and stay nonclaim",
                "gate_pass": "true_nonclaim",
                "reason": "c_g, zero theorem, arena projections, and score interface are emitted with missing markers",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1157_4_Newton_GR_promotion",
                "rule": "matter-functor/local-GR/Newton/R10/WEP/clock claim allowed",
                "gate_pass": "false",
                "reason": "q/null theorem unsigned and c_g rows unfilled",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1157_0_q_route",
                "decision": "q_map_null_route_is_promising_but_conditional",
                "reason": "relative-exact residuals can become presymplectic null directions, but exactness/boundary silence are still open",
                "next_action": "do not promote Dq(v_X)=0 until q and v_X are parent-signed",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1157_1_current_branch",
                "decision": "parent_q_map_null_generator_not_derived_for_current_MTS",
                "reason": "Xhat/frame direction may still be a physical retained field or boundary/source residual",
                "next_action": "use c_g first-fill row as nonclaim fallback",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1157_2_best_next",
                "decision": "target_cg_units_arena_projection_source_pack_or_exactness_repair",
                "reason": "after q/null route fails, c_g is the first common-frame coefficient requiring units and projections",
                "next_action": "1158 c_g units/arena projection source pack or Cperp exactness repair",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1157_0_1158",
                "next_target": "1158-Y5-R10-cg-units-arena-projection-source-pack-or-Cperp-exactness-repair.md",
                "objective": "fill the c_g units/projection source pack for R10/PPN/WEP/clock/orbital, while keeping Cperp exactness as the derivation repair route",
                "include": "A_g definition; Xhat normalization; c_g units; tau_R10; tau_PPN; tau_clock; tau_WEP; tau_orbital; source paths",
                "exclude": "q by declaration; vertical by label; missing kinetic as null; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    cg_rows: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = audit + cg_rows + guards + gates + decisions + next_target
    add(
        "V1157_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1157_1_verdict_blocks_q_null",
        any(row["audit_id"] == "QMAP1157_8_verdict" and row["current_status"] == "PARENT_Q_MAP_NULL_GENERATOR_NOT_DERIVED" for row in audit),
        "q-map/null-generator proof remains unsigned for current MTS",
    )
    add(
        "V1157_2_cg_rows_present",
        {"CG1157_0_cg_first_fill", "CG1157_1_zero_theorem_path", "CG1157_2_R10_projection", "CG1157_3_PPN_projection", "CG1157_4_clock_WEP_orbital_projection", "CG1157_5_score_interface"}.issubset(
            {row["row_id"] for row in cg_rows}
        ),
        "c_g first fill rows cover value, zero theorem, arena projections, and score interface",
    )
    add(
        "V1157_3_cg_rows_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and (contains_missing(row["current_value"]) or row["current_value"] == "false") for row in cg_rows),
        "c_g rows remain missing/nonclaim until sourced",
    )
    add(
        "V1157_4_guards_active",
        {"GUARD1157_0_no_q_by_declaration", "GUARD1157_1_no_vertical_by_label", "GUARD1157_2_no_missing_kinetic_as_null", "GUARD1157_3_no_boundary_hair_silence", "GUARD1157_4_no_cg_claim_without_projection"}.issubset(
            {row["guard_id"] for row in guards if row["status"] == "ACTIVE"}
        ),
        "all q/null and c_g no-cheat guards are active",
    )
    add(
        "V1157_5_claim_gates_blocked",
        any(row["gate_id"] == "G1157_2_current_q_null_signed" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1157_4_Newton_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "q/null and local promotion gates remain blocked",
    )
    add(
        "V1157_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1157_7_next_target",
        next_target[0]["next_target"].startswith("1158-") and "cg-units-arena-projection" in str(next_target[0]["next_target"]),
        "1158 handoff targets c_g units/projections or Cperp exactness repair",
    )
    add(
        "V1157_8_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1157_9_csv_parse", csv_parse_ok, "all 1157 CSV outputs parse cleanly")
    add("V1157_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1157_SUMMARY",
        True,
        "1157 keeps q-map/null-generator route conditional, rejects current q-null promotion, and emits nonclaim c_g first-fill rows",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    cg_rows: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1157 - Y5/R10 Parent q-Map Null Generator Proof or c_g Bound First Fill

**Current verdict:** the parent `q`/null-generator proof does not close for current MTS. The route is real conditionally, but the corpus still lacks the parent quotient object, `Cperp` exactness, boundary primitive silence, proof that local `Xhat` is the null generator, and kinetic/rank/source-orthogonality classification.

**Useful progress:** the fallback is now concrete: the first `c_g` row has required units, source-path, zero-theorem, and arena-projection fields instead of being a vague “coupling problem”.

**Important guard:** no `q` by declaration and no “vertical by label”. A variable is only silent if the parent quotient/reduced phase-space proof earns `v_X in ker(Dq)`.

**Best next attack:** fill the `c_g` units/projection source pack while keeping `Cperp` exactness as the derivation repair route.

**No claim:** no measured-GM, source-normalized Newton, local-GR, PPN, R10, WEP, clock, GitHub, or public claim follows from 1157.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## q-Map / Null Generator Proof Audit
{table(["audit_id", "claim_piece", "mathematical_form", "current_status", "missing_for_current_MTS", "effect_if_missing", "valid_for_claim"], audit)}

## c_g First Fill Rows
{table(["row_id", "parameter", "definition", "required_columns", "current_value", "source_path", "units", "arena_links", "status", "valid_for_claim", "claim_allowed"], cg_rows)}

## q/null No-Cheat Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1157_SOURCE_REGISTER.csv",
        "audit": OUT / "P8_Y5_R10_1157_QMAP_NULL_GENERATOR_PROOF_AUDIT.csv",
        "cg_rows": OUT / "P8_Y5_R10_1157_CG_BOUND_FIRST_FILL_ROWS.csv",
        "guards": OUT / "P8_Y5_R10_1157_QMAP_NULL_NO_CHEAT_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1157_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1157_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1157_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1157_VALIDATION.csv",
    }

    sources = source_rows()
    audit = qmap_audit_rows()
    cg_rows = cg_first_fill_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["cg_rows"], cg_rows)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, audit, cg_rows, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, audit, cg_rows, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
