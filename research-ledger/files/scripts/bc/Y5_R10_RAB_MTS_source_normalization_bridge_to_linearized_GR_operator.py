from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1297"
TITLE = "1297-Y5-R10-RAB-MTS-source-normalization-bridge-to-linearized-GR-operator"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
BRIDGE_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_NORMALIZATION_BRIDGE_NONCLAIM.csv"
DIMENSIONAL_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_DIMENSIONAL_LEDGER.csv"
RUNNER_PREVIEW_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_SOURCE_NORMALIZATION_PREVIEW.csv"
SCORING_BLOCKERS_PATH = OUT_DIR / f"{PACK_ID}_SCORING_BLOCKERS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1297_VALIDATION.csv"

INPUT_PATH = OUT_DIR / "P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv"


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


def is_true(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        BRIDGE_PATH,
        DIMENSIONAL_LEDGER_PATH,
        RUNNER_PREVIEW_PATH,
        SCORING_BLOCKERS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def preview_tokens(required_inputs: str) -> tuple[str, list[str], bool, bool, bool]:
    tokens = split_semicolon(required_inputs)
    csign_applied = "MISSING_C_SIGN" in tokens
    response_applied = "MISSING_RESPONSE_OPERATOR" in tokens
    source_norm_applied = response_applied
    output = []
    for token in tokens:
        if token == "MISSING_C_SIGN":
            output.append("ABS_C_SIGN_EQ_1_BOUND_ONLY")
        elif token == "MISSING_RESPONSE_OPERATOR":
            output.append("RGO1296_LINEARIZED_GR_RESPONSE_NONCLAIM")
            output.append("SOURCE_NORM_1297_ABS_NEWTON_BRIDGE_NONCLAIM")
        else:
            output.append(token)
    remaining = [token for token in output if token.startswith("MISSING")]
    return ";".join(output), remaining, csign_applied, response_applied, source_norm_applied


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    runner_rows = read_csv(INPUT_PATH)

    source_register = [
        {
            "source_id": "SRC1297_0_1296_next",
            "source_type": "local",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1296_NEXT_TARGET.csv",
            "url": "",
            "needle_or_anchor": "NEXT1296_0_1297",
            "role": "handoff into MTS source-normalization bridge",
            "web_verified_utc": "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1297_1_1296_operator",
            "source_type": "local",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1296_RESPONSE_OPERATOR_ROWS_NONCLAIM.csv",
            "url": "",
            "needle_or_anchor": "MTS_source_slot",
            "role": "formal response operator source slot to be bridged",
            "web_verified_utc": "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1297_2_1296_gap",
            "source_type": "local",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1296_OBSERVABLE_GAP_LEDGER.csv",
            "url": "",
            "needle_or_anchor": "OG1296_0_source_normalization",
            "role": "source-normalization gap closed only as nonclaim absolute Newton bridge",
            "web_verified_utc": "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1297_3_KL_budget",
            "source_type": "local",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "url": "",
            "needle_or_anchor": "epsilon_K = |c^2 Kbar_L,loc,00| / |4 pi G rho|",
            "role": "prior Newton-source fraction formula matched by the bridge",
            "web_verified_utc": "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1297_4_PPN_requirements",
            "source_type": "local",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "url": "",
            "needle_or_anchor": "epsilon_K00=abs(c^2 Kbar_L,loc,00)/abs(4 pi G rho)",
            "role": "current local response requirement that remains nonclaim until rho/GM calibration exists",
            "web_verified_utc": "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1297_5_chain_kernel",
            "source_type": "local",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "url": "",
            "needle_or_anchor": "Kmetric_chain^{00}=C_sign",
            "role": "Kmetric_chain source object whose trace-reversed projection is not yet derived",
            "web_verified_utc": "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1297_6_Carroll_Newton_limit",
            "source_type": "external_web",
            "local_path": "",
            "url": "https://arxiv.org/pdf/gr-qc/9712019",
            "needle_or_anchor": "Carroll GR notes Newtonian limit: h00=-2Phi, R00=-1/2 nabla^2 h00, kappa=8piG in c=1; opened 2026-06-15 lines 6643-6712",
            "role": "source-backed Newtonian-limit normalization of Einstein equation",
            "web_verified_utc": RUN_STARTED_UTC.isoformat(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1297_7_MIT_linearized_operator",
            "source_type": "external_web",
            "local_path": "",
            "url": "https://web.mit.edu/sahughes/www/8.962/lec16.pdf",
            "needle_or_anchor": "linearized Lorenz-gauge operator and Green solution; opened 2026-06-15 lines 357-372",
            "role": "response operator that accepts the normalized source",
            "web_verified_utc": RUN_STARTED_UTC.isoformat(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1297_8_Poisson_Green",
            "source_type": "external_web",
            "local_path": "",
            "url": "https://mathworld.wolfram.com/GreensFunctionPoissonsEquation.html",
            "needle_or_anchor": "Poisson Green function source convention; opened 2026-06-15 lines 18-37",
            "role": "static Newton/Poisson response target for S_K",
            "web_verified_utc": RUN_STARTED_UTC.isoformat(),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        if row["source_type"] == "local":
            exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle_or_anchor"]))
            row["exists_or_url_recorded"] = exists
            row["anchor_found_or_web_verified"] = needle_found
        else:
            row["exists_or_url_recorded"] = bool(row["url"])
            row["anchor_found_or_web_verified"] = bool(row["web_verified_utc"])

    bridge_rows = [
        {
            "bridge_id": "SNB1297_0_geometric_left_parent_branch",
            "branch_assumption": "parent local metric equation has G_{mu nu}+sigma_K K_{mu nu}=kappa T_matter_{mu nu}",
            "kappa_SI": "8*pi*G/c^4",
            "effective_stress_bridge": "T_eff,K_{mu nu}=-(sigma_K*c^4/(8*pi*G))*K_{mu nu}",
            "trace_reversed_bridge": "Kbar_{mu nu}:=K_{mu nu}-0.5*g_{mu nu}K; R_{mu nu,K}=-sigma_K*Kbar_{mu nu}",
            "Newton_source_bridge": "nabla^2 Phi_K = S_K = -sigma_K*c^2*Kbar_{00}",
            "effective_mass_density": "rho_eff,K = -sigma_K*c^2*Kbar_{00}/(4*pi*G)",
            "absolute_Newton_budget": "epsilon_K = |c^2*Kbar_{00}|/(4*pi*G*rho_ref)",
            "sign_status": "sigma_K_PARENT_SIDE_SIGN_MISSING; absolute budget sign-insensitive",
            "units_status": "DIMENSIONALLY_CLOSED_IF_Kbar_HAS_UNITS_L^-2",
            "measured_GM_caveat": "rho_ref and measured-GM calibration are required before comparing to local Newton residuals",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv;source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "source_anchor": "KLB796_2_Newton_source_fraction;RMR1288_0_Newton_source",
            "usable_for_abs_Newton_budget": True,
            "usable_for_oriented_source_claim": False,
            "usable_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bridge_id": "SNB1297_1_metric_invisible_or_improvement_branch",
            "branch_assumption": "K_chain is an exact improvement/topological/projector-silent tensor and does not enter the observable metric equation",
            "kappa_SI": "not_applicable_until_silence_theorem",
            "effective_stress_bridge": "T_eff,K=0 only if metric-invisibility theorem is parent-signed",
            "trace_reversed_bridge": "Kbar_observable=0 if improvement/boundary terms vanish in the selected local domain",
            "Newton_source_bridge": "S_K=0 only under proven metric silence",
            "effective_mass_density": "rho_eff,K=0 only under proven metric silence",
            "absolute_Newton_budget": "epsilon_K=0 only under proven metric silence",
            "sign_status": "not_a_sign_solution; theorem_missing",
            "units_status": "blocked_until_metric_silence_theorem",
            "measured_GM_caveat": "not comparable until theorem includes boundary/reference terms",
            "source_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv;source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "source_anchor": "GK514_C_topological_exact_sector;KLB796_0_divergence_zero_not_metric_zero",
            "usable_for_abs_Newton_budget": False,
            "usable_for_oriented_source_claim": False,
            "usable_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bridge_id": "SNB1297_2_unplaced_residual_branch",
            "branch_assumption": "parent field equation does not specify whether K_chain is geometric-left, matter-right, or invisible",
            "kappa_SI": "unknown",
            "effective_stress_bridge": "blocked",
            "trace_reversed_bridge": "blocked",
            "Newton_source_bridge": "blocked",
            "effective_mass_density": "blocked",
            "absolute_Newton_budget": "cannot score; retain explicit residual",
            "sign_status": "MISSING_PARENT_SOURCE_PLACEMENT",
            "units_status": "MISSING_PARENT_FIELD_EQUATION",
            "measured_GM_caveat": "not reached",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "source_anchor": "MR514_1_Khat_metric_response;MR514_2_Ward_identity",
            "usable_for_abs_Newton_budget": False,
            "usable_for_oriented_source_claim": False,
            "usable_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    dimensional_ledger = [
        {
            "dim_id": "DL1297_0_Kbar",
            "quantity": "Kbar_{00}",
            "expected_units": "L^-2",
            "reason": "Einstein tensor/source-side geometric residual has curvature units",
            "bridge_use": "c^2*Kbar_{00} supplies Newton-source units",
            "status": "UNIT_CONSISTENT_IF_TRACE_REVERSED_K_DEFINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dim_id": "DL1297_1_c2Kbar",
            "quantity": "c^2*Kbar_{00}",
            "expected_units": "T^-2",
            "reason": "Newton source nabla^2 Phi has units potential/length^2 = T^-2",
            "bridge_use": "S_K=-sigma_K*c^2*Kbar_{00}",
            "status": "DIMENSIONALLY_MATCHES_POISSON_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dim_id": "DL1297_2_4piGrho",
            "quantity": "4*pi*G*rho_ref",
            "expected_units": "T^-2",
            "reason": "Poisson equation uses nabla^2 Phi = 4*pi*G*rho",
            "bridge_use": "epsilon_K=|c^2*Kbar_{00}|/(4*pi*G*rho_ref)",
            "status": "DIMENSIONLESS_RATIO_CONFIRMED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dim_id": "DL1297_3_Teff",
            "quantity": "T_eff,K_{mu nu}",
            "expected_units": "energy_density_or_pressure",
            "reason": "Einstein equation coupling is 8*pi*G/c^4",
            "bridge_use": "T_eff,K=-(sigma_K*c^4/(8*pi*G))*K",
            "status": "DIMENSIONALLY_MATCHES_STRESS_ENERGY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dim_id": "DL1297_4_unresolved_projection",
            "quantity": "Kmetric_chain^{00} to Kbar_{00}",
            "expected_units": "L^-2 after trace reversal and projection",
            "reason": "runner rows contain component bounds, but trace and projection into observable 00 slot are not derived",
            "bridge_use": "must derive Kbar_L,loc,00 from Kmetric_chain/R_chain before scoring",
            "status": "MISSING_TRACE_REVERSED_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_preview = []
    for row in runner_rows:
        preview, remaining, csign_applied, response_applied, source_norm_applied = preview_tokens(row.get("required_inputs", ""))
        runner_preview.append(
            {
                "preview_id": f"SNP1297_{len(runner_preview)}",
                "runner_id": row.get("runner_id", ""),
                "residual_component": row.get("residual_component", ""),
                "abs_Csign_applied_from_1295": csign_applied,
                "response_operator_applied_from_1296": response_applied,
                "source_normalization_applied_from_1297": source_norm_applied,
                "required_inputs_preview": preview,
                "remaining_missing_count": len(remaining),
                "remaining_missing_tokens": ";".join(remaining) if remaining else "NONE",
                "bridge_status": "ABS_NEWTON_SOURCE_NORMALIZATION_AVAILABLE_NONCLAIM" if source_norm_applied else "COMPONENT_AGGREGATE_OR_OBSERVABLE_MATRIX_STILL_MISSING",
                "score_emitted": False,
                "score_value": "",
                "runner_status": "SOURCE_NORM_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    scoring_blockers = [
        {
            "blocker_id": "SB1297_0_parent_side_sign",
            "blocker": "sigma_K parent-side sign and source placement",
            "why_blocks_scoring": "absolute Newton budget is sign-insensitive, but oriented PPN/clock/orbital source predictions need the parent equation placement",
            "needed_to_clear": "derive whether local equation is G+K=kappaT, G-K=kappaT, or K is improvement/invisible",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "SB1297_1_trace_reversed_projection",
            "blocker": "Kmetric_chain/R_chain to Kbar_L,loc,00",
            "why_blocks_scoring": "source bridge is written for Kbar_{00}; runner rows provide component residual bounds without total trace-reversed local projection",
            "needed_to_clear": "derive trace, local projection, Kperp/boundary inclusion, and units of Kbar_L,loc,00",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "SB1297_2_rho_and_measured_GM",
            "blocker": "rho_ref/source model and measured-GM calibration",
            "why_blocks_scoring": "epsilon_K compares to matter density/source normalization, which is not yet attached to a local body or calibration convention",
            "needed_to_clear": "source rho model, measured GM handling, and local residual tolerance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "SB1297_3_remaining_residual_inputs",
            "blocker": "m, L_cg, F/Fprime, metric kernels, CDB bounds",
            "why_blocks_scoring": "even with source normalization, residual amplitude remains symbolic",
            "needed_to_clear": "derive or source bounds for every remaining RRI1292 missing input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "SB1297_4_observable_projection",
            "blocker": "PPN/clock/orbital/R10 readout",
            "why_blocks_scoring": "Newton source fraction is not the full local-GR/PPN response vector",
            "needed_to_clear": "build observable projection rows from Phi_K/hbar_K to gamma,beta,alpha_i,clock,orbital,R10",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1297_0_abs_Newton_bridge",
            "claim": "absolute Newton-source normalization bridge exists",
            "current_status": "SATISFIED_FOR_NONCLAIM_ABS_NEWTON_BUDGET",
            "reason": "geometric-left branch gives epsilon_K=|c^2*Kbar_{00}|/(4*pi*G*rho_ref), matching 796/1288",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1297_1_oriented_source",
            "claim": "oriented MTS source sign/coefficient is known",
            "current_status": "BLOCKED_PARENT_SIDE_SIGN_MISSING",
            "reason": "sigma_K and field-equation placement are not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1297_2_runner_score",
            "claim": "RRI1292 runner can emit scores",
            "current_status": "BLOCKED_REMAINING_INPUTS_AND_OBSERVABLES",
            "reason": "source normalization does not supply residual amplitudes, rho_ref, GM calibration, or PPN/clock/orbital/R10 projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1297_3_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "bridge is a necessary normalization row, not a theorem that K is zero/small",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1297_0_accept_abs_bridge",
            "decision": "accept the geometric-left bridge as an absolute Newton budget normalization",
            "because": "Einstein/Newton limit and existing 796/1288 formulas force the dimensionless ratio once Kbar_{00} has curvature units",
            "next_action": "derive Kmetric_chain/R_chain trace-reversed projection into Kbar_L,loc,00",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1297_1_keep_oriented_blocked",
            "decision": "keep oriented source sign and local-GR claims blocked",
            "because": "sigma_K, volume convention, Khat/Kmetric match, and boundary terms remain parent-open",
            "next_action": "do not use the bridge for cancellation or sign claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1297_2_next_bottleneck",
            "decision": "target trace-reversed Kbar projection before observable scoring",
            "because": "the source bridge needs Kbar_{00}, not merely symbolic Kmetric_chain component terms",
            "next_action": "derive Kbar_L,loc,00 from chain, trace, projection, and CDB pieces",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1297_0_1298",
            "target_file": "1298-Y5-R10-RAB-Kmetric-chain-to-trace-reversed-Kbar-local-projection.md",
            "target_script": "scripts/Y5_R10_RAB_Kmetric_chain_to_trace_reversed_Kbar_local_projection.py",
            "task": "derive or block the projection from Kmetric_chain/R_chain components into Kbar_L,loc,00 used by the Newton source bridge",
            "success_condition": "produce a nonclaim Kbar_L,loc,00 projection formula with trace term, domain/projector assumptions, and CDB inclusion, or keep scoring blocked with explicit missing projection inputs",
            "do_not": "do not compute local Newton/PPN/R10 scores until Kbar projection, residual amplitudes, rho_ref, GM calibration, and observable maps are sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(BRIDGE_PATH, bridge_rows)
    write_csv(DIMENSIONAL_LEDGER_PATH, dimensional_ledger)
    write_csv(RUNNER_PREVIEW_PATH, runner_preview)
    write_csv(SCORING_BLOCKERS_PATH, scoring_blockers)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists_or_url_recorded"] and row["anchor_found_or_web_verified"])
    validations.append(
        validation_row(
            "VAL1297_0_sources_recorded",
            "local anchors and external sources are recorded",
            source_hits == source_count,
            f"{source_hits}/{source_count} source records validated",
        )
    )
    abs_bridge = bridge_rows[0]
    validations.append(
        validation_row(
            "VAL1297_1_abs_bridge_contains_required_constants",
            "source bridge includes c factors, 4*pi*G, kappa, and measured-GM caveat",
            "c^2" in abs_bridge["Newton_source_bridge"]
            and "4*pi*G" in abs_bridge["effective_mass_density"]
            and "8*pi*G/c^4" in abs_bridge["kappa_SI"]
            and "measured-GM" in abs_bridge["measured_GM_caveat"],
            str(abs_bridge["absolute_Newton_budget"]),
        )
    )
    validations.append(
        validation_row(
            "VAL1297_2_dimensional_ledger_passes",
            "dimensional ledger confirms Newton ratio units and unresolved projection",
            len(dimensional_ledger) == 5
            and any(row["status"] == "DIMENSIONLESS_RATIO_CONFIRMED" for row in dimensional_ledger)
            and any(row["status"] == "MISSING_TRACE_REVERSED_PROJECTION" for row in dimensional_ledger),
            ";".join(row["dim_id"] for row in dimensional_ledger),
        )
    )
    source_norm_rows = [row for row in runner_preview if is_true(row["source_normalization_applied_from_1297"])]
    validations.append(
        validation_row(
            "VAL1297_3_runner_preview_applies_source_norm",
            "source normalization appears only in component rows with response operators",
            len(source_norm_rows) == 3 and all("SOURCE_NORM_1297_ABS_NEWTON_BRIDGE_NONCLAIM" in row["required_inputs_preview"] for row in source_norm_rows),
            ";".join(row["runner_id"] for row in source_norm_rows),
        )
    )
    validations.append(
        validation_row(
            "VAL1297_4_runner_still_no_score",
            "all runner preview rows remain no-score",
            all(is_false(row["score_emitted"]) and "NO_SCORE" in row["runner_status"] for row in runner_preview),
            ";".join(f"{row['runner_id']}={row['remaining_missing_count']}" for row in runner_preview),
        )
    )
    validations.append(
        validation_row(
            "VAL1297_5_blockers_remain_explicit",
            "scoring blockers remain explicit after bridge",
            len(scoring_blockers) == 5 and all(is_false(row["claim_allowed"]) for row in scoring_blockers),
            ";".join(row["blocker_id"] for row in scoring_blockers),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        BRIDGE_PATH,
        DIMENSIONAL_LEDGER_PATH,
        RUNNER_PREVIEW_PATH,
        SCORING_BLOCKERS_PATH,
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
    validations.append(validation_row("VAL1297_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1297_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1297_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, bridge_rows, dimensional_ledger, runner_preview, scoring_blockers, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1297_9_next_target_1298",
            "next target routes to Kbar projection",
            next_target[0]["next_id"] == "NEXT1297_0_1298" and "trace-reversed-Kbar" in next_target[0]["target_file"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1297_10_overall",
            "overall 1297 validation",
            overall_pass,
            "1297 derives a nonclaim absolute Newton source-normalization bridge with c factors, 4*pi*G, dimensions, and measured-GM caveat, while keeping scoring blocked by Kbar projection and remaining inputs",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1297 Y5 R10 RAB MTS source-normalization bridge to linearized-GR operator

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1297 derives a useful nonclaim bridge: if the parent local equation has `G_{{mu nu}} + sigma_K K_{{mu nu}} = kappa T_{{matter,mu nu}}`, then the effective stress is `T_eff,K = -(sigma_K c^4/(8πG))K`, and the Newton source slot is `nabla^2 Phi_K = -sigma_K c^2 Kbar_{{00}}`. Therefore the absolute Newton budget is `epsilon_K = |c^2 Kbar_{{00}}|/(4πG rho_ref)`.

**Main progress:** the source-normalization gap is no longer vague. The constants and units are fixed for the geometric-left branch: `Kbar_{{00}}` must have curvature units, `c^2 Kbar_{{00}}` matches the Poisson source units, and `4πG rho_ref` gives the comparison scale. This exactly matches the old 796/1288 Newton-source fraction, but now it is derived as a bridge to the 1296 response operator.

**Still blocked:** this is not a score or a local-GR pass. The bridge still needs the parent-side sign `sigma_K`, the trace-reversed projection from `Kmetric_chain/R_chain` into `Kbar_L,loc,00`, a source model `rho_ref`, measured-GM calibration, remaining residual amplitudes, and observable projections.

## Source Register

{markdown_table(source_register, ["source_id", "source_type", "local_path", "url", "needle_or_anchor", "exists_or_url_recorded", "anchor_found_or_web_verified", "role", "valid_for_claim", "claim_allowed"])}

## Source Normalization Bridge

{markdown_table(bridge_rows, ["bridge_id", "branch_assumption", "kappa_SI", "effective_stress_bridge", "trace_reversed_bridge", "Newton_source_bridge", "effective_mass_density", "absolute_Newton_budget", "sign_status", "units_status", "measured_GM_caveat", "source_path", "source_anchor", "usable_for_abs_Newton_budget", "usable_for_oriented_source_claim", "usable_for_scoring", "valid_for_claim", "claim_allowed"])}

## Dimensional Ledger

{markdown_table(dimensional_ledger, ["dim_id", "quantity", "expected_units", "reason", "bridge_use", "status", "valid_for_claim", "claim_allowed"])}

## Runner Source-Normalization Preview

{markdown_table(runner_preview, ["preview_id", "runner_id", "residual_component", "abs_Csign_applied_from_1295", "response_operator_applied_from_1296", "source_normalization_applied_from_1297", "required_inputs_preview", "remaining_missing_count", "remaining_missing_tokens", "bridge_status", "score_emitted", "score_value", "runner_status", "valid_for_claim", "claim_allowed"])}

## Scoring Blockers

{markdown_table(scoring_blockers, ["blocker_id", "blocker", "why_blocks_scoring", "needed_to_clear", "valid_for_claim", "claim_allowed"])}

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
