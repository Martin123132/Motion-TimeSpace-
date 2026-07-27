from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1298"
TITLE = "1298-Y5-R10-RAB-Kmetric-chain-to-trace-reversed-Kbar-local-projection"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PROJECTION_PATH = OUT_DIR / f"{PACK_ID}_KBAR_PROJECTION_FORMULA_NONCLAIM.csv"
TRACE_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_SPATIAL_TRACE_REQUIREMENTS.csv"
BOUND_PREVIEW_PATH = OUT_DIR / f"{PACK_ID}_KBAR_BOUND_PREVIEW_NONCLAIM.csv"
RUNNER_PREVIEW_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_PROJECTION_PREVIEW.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1298_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        PROJECTION_PATH,
        TRACE_REQUIREMENTS_PATH,
        BOUND_PREVIEW_PATH,
        RUNNER_PREVIEW_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1298_0_1297_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1297_NEXT_TARGET.csv",
            "needle": "NEXT1297_0_1298",
            "role": "handoff into Kbar local projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1298_1_1297_bridge",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1297_SOURCE_NORMALIZATION_BRIDGE_NONCLAIM.csv",
            "needle": "Kbar_{mu nu}:=K_{mu nu}-0.5*g_{mu nu}K",
            "role": "trace-reversed source slot required by the Newton bridge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1298_2_1297_dimensional",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1297_DIMENSIONAL_LEDGER.csv",
            "needle": "MISSING_TRACE_REVERSED_PROJECTION",
            "role": "explicit unresolved projection from Kmetric_chain to Kbar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1298_3_chain_kernel",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "needle": "Kmetric_chain^{00}=C_sign",
            "role": "available 00 chain component to project",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1298_4_bound_ledger",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "needle": "R_chain^{00}=R_m^{00}+R_L^{00}+R_cdb^{00}",
            "role": "current component residual vector only supplies 00 branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1298_5_Newton_requirement",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "needle": "MISSING_KBAR_L_LOC_00",
            "role": "Newton source row explicitly waits on Kbar_L,loc,00",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1298_6_KL_budget",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "needle": "K_L can shift weak-field metric coefficients",
            "role": "trace-reversed projection matters for local metric response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1298_7_metric_response_contract",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "K_hat is exactly the metric response of Gamma_eff",
            "role": "blocks projection claim until Khat/Kmetric and derivative/boundary terms close",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    projection_rows = [
        {
            "projection_id": "KTP1298_0_trace_reverse_identity",
            "object": "Kbar_{00}",
            "formula": "Kbar_{00}=K_{00}-0.5*g_{00}K, with K=g^{alpha beta}K_{alpha beta}",
            "local_flat_signature_branch": "for eta=(-,+,+,+), Kbar_{00}=0.5*(K^{00}+K^{11}+K^{22}+K^{33}) after local index conversion",
            "source_inputs": "trace-reversal identity from 1297 source bridge",
            "derived_status": "FORMAL_PROJECTION_IDENTITY_DERIVED_NONCLAIM",
            "missing_for_scoring": "MISSING_SPATIAL_TRACE_KII;MISSING_INDEX_CONVENTION_LOCK;MISSING_LOCAL_PROJECTOR_DOMAIN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "projection_id": "KTP1298_1_chain_projection",
            "object": "Kbar_L,loc,00 from Kmetric_chain",
            "formula": "Kbar_L,loc,00=P_loc[0.5*(K_chain^{00}+sum_i K_chain^{ii})]+Delta_projector_boundary",
            "local_flat_signature_branch": "K_chain^{00}=R_m^{00}+R_L^{00}+R_cdb^{00}; spatial trace needs analogous R_m^{ii}, R_L^{ii}, R_cdb^{ii}",
            "source_inputs": "1289 00 kernel; 1291 residual vector; 1297 Newton source bridge",
            "derived_status": "FORMAL_LOCAL_PROJECTION_FORMULA_DERIVED_NONCLAIM",
            "missing_for_scoring": "MISSING_R_m_ii_BOUND;MISSING_R_L_ii_BOUND;MISSING_R_cdb_ii_BOUND;MISSING_PROJECTOR_BOUNDARY_TERM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "projection_id": "KTP1298_2_trace_free_shortcut_test",
            "object": "possible Kbar_L,loc,00 shortcut",
            "formula": "if parent proves spatial trace sum_i K_chain^{ii}=K_chain^{00} or K trace relation, Kbar_00 may reduce to a multiple of K^{00}",
            "local_flat_signature_branch": "no such trace/isotropy relation is currently sourced",
            "source_inputs": "requires parent action or symmetry theorem, not present in 1289/1291",
            "derived_status": "SHORTCUT_BLOCKED_NO_TRACE_THEOREM",
            "missing_for_scoring": "MISSING_TRACE_THEOREM;MISSING_ISOTROPY_OR_TRACEFREE_BRANCH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    trace_requirements = [
        {
            "requirement_id": "STR1298_0_m_spatial_trace",
            "component": "sum_i R_m^{ii}",
            "needed_bound": "sum_i |L_cg^-2 F_prime(m) M_m^{ii}| or parent trace theorem",
            "why_needed": "Kbar_00 includes spatial trace as well as 00 component",
            "status": "MISSING_SPATIAL_M_KERNEL_TRACE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "STR1298_1_Lcg_spatial_trace",
            "component": "sum_i R_L^{ii}",
            "needed_bound": "sum_i |2 L_cg^-3 F(m) M_L^{ii}| or parent trace theorem",
            "why_needed": "L_cg chain can source the spatial trace even if R_L^{00} is bounded",
            "status": "MISSING_SPATIAL_LCG_KERNEL_TRACE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "STR1298_2_cdb_spatial_trace",
            "component": "sum_i R_cdb^{ii}",
            "needed_bound": "connection/domain/boundary spatial trace or no-flux/improvement theorem",
            "why_needed": "CDB terms can enter Kbar_00 through the trace",
            "status": "MISSING_SPATIAL_CDB_TRACE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "STR1298_3_projector_domain",
            "component": "P_loc and Delta_projector_boundary",
            "needed_bound": "commutator/domain/boundary term introduced by local projection",
            "why_needed": "local projection may not commute with trace reversal or boundary restriction",
            "status": "MISSING_PROJECTOR_DOMAIN_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "STR1298_4_index_convention",
            "component": "covariant/contravariant 00 and ii conversion",
            "needed_bound": "fixed local signature, frame, and index placement",
            "why_needed": "current rows use superscript 00 while Kbar bridge is written with lower-index source slot",
            "status": "MISSING_INDEX_CONVENTION_LOCK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_preview = [
        {
            "bound_id": "KBP1298_0_abs_Kbar_bound",
            "bound_formula": "|Kbar_L,loc,00| <= 0.5*(|K_chain^{00}| + sum_i |K_chain^{ii}|) + |Delta_projector_boundary|",
            "known_piece": "|K_chain^{00}| bounded symbolically by KRB1291_0+KRB1291_1+KRB1291_2",
            "missing_piece": "sum_i |K_chain^{ii}| and Delta_projector_boundary",
            "current_status": "BOUND_FORM_DERIVED_BUT_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "KBP1298_1_Newton_budget_after_projection",
            "bound_formula": "epsilon_K <= |c^2|/(4*pi*G*rho_ref) * [0.5*(|K_chain^{00}|+sum_i|K_chain^{ii}|)+|Delta_projector_boundary|]",
            "known_piece": "1297 supplies c^2/(4*pi*G*rho_ref) normalization; 1291 supplies 00 symbolic bounds",
            "missing_piece": "rho_ref, measured-GM calibration, spatial trace bounds, residual amplitudes",
            "current_status": "NEWTON_BUDGET_FORM_DERIVED_BUT_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_preview = [
        {
            "preview_id": "KRP1298_0_m_chain",
            "runner_id": "RRI1292_0_m_chain",
            "projection_update": "00 component contributes to Kbar but cannot alone define Kbar_00",
            "new_required_inputs": "MISSING_R_m_ii_BOUND;MISSING_TRACE_REVERSED_PROJECTION;MISSING_PROJECTOR_DOMAIN_BOUND",
            "remaining_old_inputs": "MISSING_L_cg_VALUE;MISSING_m_PROFILE;MISSING_F_PRIME_BOUND;MISSING_M_m_00_BOUND",
            "score_emitted": False,
            "runner_status": "PROJECTION_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "preview_id": "KRP1298_1_Lcg_chain",
            "runner_id": "RRI1292_1_Lcg_chain",
            "projection_update": "00 component contributes to Kbar but spatial Lcg trace is required",
            "new_required_inputs": "MISSING_R_L_ii_BOUND;MISSING_TRACE_REVERSED_PROJECTION;MISSING_PROJECTOR_DOMAIN_BOUND",
            "remaining_old_inputs": "MISSING_L_cg_VALUE;MISSING_LCG_LOWER_BOUND;MISSING_m_PROFILE;MISSING_F_BOUND;MISSING_M_L_00_BOUND",
            "score_emitted": False,
            "runner_status": "PROJECTION_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "preview_id": "KRP1298_2_cdb_chain",
            "runner_id": "RRI1292_2_cdb_chain",
            "projection_update": "CDB terms enter both 00 and spatial trace slots",
            "new_required_inputs": "MISSING_R_cdb_ii_BOUND;MISSING_TRACE_REVERSED_PROJECTION;MISSING_PROJECTOR_DOMAIN_BOUND",
            "remaining_old_inputs": "MISSING_K_CONN_BOUND;MISSING_K_DOMAIN_BOUND;MISSING_K_BOUNDARY_BOUND;MISSING_NO_FLUX_SOURCE",
            "score_emitted": False,
            "runner_status": "PROJECTION_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "preview_id": "KRP1298_3_chain_vector",
            "runner_id": "RRI1292_3_chain_vector",
            "projection_update": "full vector needs aggregate Kbar projection and observable matrix",
            "new_required_inputs": "MISSING_FULL_KBAR_PROJECTION;MISSING_OBSERVABLE_RESPONSE_MATRIX",
            "remaining_old_inputs": "MISSING_ALL_COMPONENT_INPUTS;MISSING_LOCAL_RESPONSE_LIMITS",
            "score_emitted": False,
            "runner_status": "PROJECTION_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1298_0_projection_formula",
            "claim": "formal Kbar_00 projection formula exists",
            "current_status": "SATISFIED_FOR_NONCLAIM_FORMULA",
            "reason": "trace reversal gives Kbar_00=0.5*(K00+Kii) in the local flat signature branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1298_1_Kbar_numeric_bound",
            "claim": "Kbar_L,loc,00 bound is scoreable",
            "current_status": "BLOCKED_SPATIAL_TRACE_MISSING",
            "reason": "current runner only has 00 symbolic bounds and no spatial trace kernels/theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1298_2_Newton_budget",
            "claim": "Newton source residual epsilon_K can be evaluated",
            "current_status": "BLOCKED_RHO_GM_AND_AMPLITUDES_MISSING",
            "reason": "Kbar projection, rho_ref, measured-GM calibration, and residual amplitudes are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1298_3_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "projection formula is necessary but not enough for smallness or silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1298_0_trace_reversal_matters",
            "decision": "do not identify Kbar_00 with K^{00}",
            "because": "local trace reversal adds the spatial trace term",
            "next_action": "derive spatial trace kernels or a parent trace/isotropy theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1298_1_keep_score_blocked",
            "decision": "keep Newton source score blocked",
            "because": "the projection formula introduces new required spatial trace and projector/domain inputs",
            "next_action": "fill spatial trace requirements before rho/GM scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1298_0_1299",
            "target_file": "1299-Y5-R10-RAB-spatial-trace-kernel-bound-or-trace-theorem.md",
            "target_script": "scripts/Y5_R10_RAB_spatial_trace_kernel_bound_or_trace_theorem.py",
            "task": "derive a spatial-trace relation for Kmetric_chain, or acquire nonclaim bounds for R_m^{ii}, R_L^{ii}, and R_cdb^{ii}",
            "success_condition": "either prove a parent trace/isotropy theorem reducing Kbar_00 to known pieces, or produce explicit spatial-trace missing-input rows that keep scoring blocked",
            "do_not": "do not treat 00 component bounds as Newton source bounds without spatial trace control",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(PROJECTION_PATH, projection_rows)
    write_csv(TRACE_REQUIREMENTS_PATH, trace_requirements)
    write_csv(BOUND_PREVIEW_PATH, bound_preview)
    write_csv(RUNNER_PREVIEW_PATH, runner_preview)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1298_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1298_1_projection_formula_present",
            "trace-reversed Kbar projection formula is present",
            any("0.5*(K^{00}+K^{11}+K^{22}+K^{33})" in row["local_flat_signature_branch"] for row in projection_rows),
            "Kbar_00 local flat branch derived",
        )
    )
    validations.append(
        validation_row(
            "VAL1298_2_spatial_trace_requirements",
            "spatial trace requirements are explicit",
            len(trace_requirements) == 5 and all("MISSING" in row["status"] for row in trace_requirements),
            ";".join(row["requirement_id"] for row in trace_requirements),
        )
    )
    validations.append(
        validation_row(
            "VAL1298_3_bound_preview_non_scoreable",
            "Kbar and Newton-budget bounds remain non-scoreable",
            len(bound_preview) == 2 and all("NOT_SCOREABLE" in row["current_status"] for row in bound_preview),
            ";".join(row["bound_id"] for row in bound_preview),
        )
    )
    validations.append(
        validation_row(
            "VAL1298_4_runner_still_no_score",
            "runner preview rows remain no-score",
            len(runner_preview) == 4 and all(is_false(row["score_emitted"]) and "NO_SCORE" in row["runner_status"] for row in runner_preview),
            ";".join(row["runner_id"] for row in runner_preview),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        PROJECTION_PATH,
        TRACE_REQUIREMENTS_PATH,
        BOUND_PREVIEW_PATH,
        RUNNER_PREVIEW_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1298_5_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1298_6_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1298_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, projection_rows, trace_requirements, bound_preview, runner_preview, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1298_8_next_target_1299",
            "next target routes to spatial trace bound or trace theorem",
            next_target[0]["next_id"] == "NEXT1298_0_1299" and "spatial-trace" in next_target[0]["target_file"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1298_9_overall",
            "overall 1298 validation",
            overall_pass,
            "1298 derives the Kbar_00 projection formula, proves the 00 component alone is insufficient, keeps scoring blocked, and routes to spatial-trace bounds/theorem",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1298 Y5 R10 RAB Kmetric-chain to trace-reversed Kbar local projection

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1298 derives the missing projection formula and catches a serious trap: the Newton bridge needs `Kbar_L,loc,00`, not raw `K^{{00}}`. In the local flat `(-,+,+,+)` branch, trace reversal gives `Kbar_{{00}} = 0.5*(K^{{00}} + K^{{11}} + K^{{22}} + K^{{33}})`.

**Main progress:** the source-normalized Newton budget can now be written as a proper bound form: `epsilon_K <= |c^2|/(4πG rho_ref) * [0.5*(|K_chain^{{00}}| + sum_i |K_chain^{{ii}}|) + |Delta_projector_boundary|]`. This is not scoreable yet, but it is the correct target rather than accidentally treating the 00 component as the full source.

**Still blocked:** current runner rows bound only the symbolic `00` channel. The spatial trace kernels, trace/isotropy theorem, projector/domain term, index convention, `rho_ref`, measured-GM calibration, and residual amplitudes remain missing.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Kbar Projection Formula

{markdown_table(projection_rows, ["projection_id", "object", "formula", "local_flat_signature_branch", "source_inputs", "derived_status", "missing_for_scoring", "valid_for_claim", "claim_allowed"])}

## Spatial Trace Requirements

{markdown_table(trace_requirements, ["requirement_id", "component", "needed_bound", "why_needed", "status", "valid_for_claim", "claim_allowed"])}

## Kbar Bound Preview

{markdown_table(bound_preview, ["bound_id", "bound_formula", "known_piece", "missing_piece", "current_status", "valid_for_claim", "claim_allowed"])}

## Runner Projection Preview

{markdown_table(runner_preview, ["preview_id", "runner_id", "projection_update", "new_required_inputs", "remaining_old_inputs", "score_emitted", "runner_status", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
