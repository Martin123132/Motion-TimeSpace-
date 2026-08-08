from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2738-Y5-R2FR-worldtube-source-profile-and-inner-charge-template-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2738_SOURCE_REGISTER.csv",
    "core": RESIDUALS / "P8_Y5_R2FR_2738_WORLDTUBE_FIRST_PAIR_CORE_TEMPLATE.csv",
    "inner_trace": RESIDUALS / "P8_Y5_R2FR_2738_INNER_CHARGE_TRACE_BOUND_CONTRACT.csv",
    "arena_map": RESIDUALS / "P8_Y5_R2FR_2738_SHARED_ARENA_SUPPORT_MAP_TEMPLATE.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2738_FIRST_PAIR_PROFILE_RUNNER_NONCLAIM.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2738_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2738_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2738_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2738_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2738_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "first_pair_template": LOCAL_BOUNDS / "worldtube_first_pair_template_2738_NONCLAIM.csv",
    "inner_trace": SOURCE_WEIGHT / "inner_charge_trace_contract_2738_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2738_QNORM_CQM_DUAL_PAIRING_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
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
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2738_0_2737_doc",
            "description": "2737 first-pair bound and selected 2738 worldtube/profile target.",
            "source_path": "2737-Y5-R2FR-source-support-and-inner-charge-theorem-or-bound-under-AX1090.md",
            "required_needles": "FP2737_1_pair_bound;ENV2737_4_Nsrc;NEXT2737_0_2738;VAL2737_OVERALL",
        },
        {
            "source_id": "SRC2738_1_1547_doc",
            "description": "1547 shared compact-source template and no-retuning guard.",
            "source_path": "1547-Y5-compact-worldtube-profile-template-and-arena-map.md",
            "required_needles": "WTP1547_0_shared_core;MAP1547_0_R10;NRT1547_0_shared_theta;NEXT1547_0_1548",
        },
        {
            "source_id": "SRC2738_2_1548_doc",
            "description": "1548 symbolic profile candidates and source acquisition ledger.",
            "source_path": "1548-Y5-shared-worldtube-profile-symbolic-runner-or-source-data-acquisition.md",
            "required_needles": "SYM1548_0_smooth_bump_profile;ACQ1548_6_unit_pairing;ARUN1548_4_local_GR;NEXT1548_0_1549",
        },
        {
            "source_id": "SRC2738_3_1549_doc",
            "description": "1549 conditional variational source-current law and unit pairing theorem.",
            "source_path": "1549-Y5-Jq-unit-dimension-and-parent-source-variation-closure.md",
            "required_needles": "VAR1549_0_variational_definition;UNIT1549_5_product_law;PAIR1549_0_q_norm;NEXT1549_0_1550",
        },
        {
            "source_id": "SRC2738_4_1547_profile_csv",
            "description": "machine-readable compact worldtube profile template.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1547_COMPACT_PROFILE_TEMPLATE.csv",
            "required_needles": "WTP1547_0_shared_core;WTP1547_4_orbital;WTP1547_5_local_GR",
        },
        {
            "source_id": "SRC2738_5_1548_symbolic_csv",
            "description": "machine-readable symbolic source profile candidates.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1548_SHARED_SYMBOLIC_PROFILE_CANDIDATES.csv",
            "required_needles": "SYM1548_0_smooth_bump_profile;SYM1548_2_Hilbert_stress_projected_profile;SYM1548_4_current_verdict",
        },
        {
            "source_id": "SRC2738_6_1549_units_csv",
            "description": "machine-readable unit pairing identity.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1549_UNIT_PAIRING_THEOREM_CONDITIONAL.csv",
            "required_needles": "UNIT1549_0_action_pairing;UNIT1549_5_product_law;UNIT1549_6_claim_status",
        },
        {
            "source_id": "SRC2738_7_1549_variation_csv",
            "description": "machine-readable parent source variation law.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1549_VARIATIONAL_SOURCE_CURRENT_LAW.csv",
            "required_needles": "VAR1549_0_variational_definition;VAR1549_3_Hilbert_proxy_limit;VAR1549_5_current_verdict",
        },
        {
            "source_id": "SRC2738_8_1529_boundary",
            "description": "boundary/no-flux and zero-mode blockers for inner charge.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
            "required_needles": "BND1529_0_domain_certificate;BND1529_1_boundary_condition;BND1529_2_zero_mode_reference",
        },
        {
            "source_id": "SRC2738_9_positive_nohair",
            "description": "positive no-hair warning that inner boundary charge is not automatically zero.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
            "required_needles": "NH562_1_energy_identity;NH562_2_compact_source_inner_boundary;NH562_5_verdict",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def core_rows() -> list[dict[str, Any]]:
    specs = [
        ("CORE2738_0_Wsrc", "W_src", "shared compact worldtube/support domain", "one source support/excision/matching convention used before arena projection", "TEMPLATE_IMPORTED_REQUIRES_PARENT_PROFILE", "W_src support; regulator/excision; exterior matching surface; source path"),
        ("CORE2738_1_Jq", "J_q", "parent source current dual to q", "delta S_matter|_{psi,e_obs}=int_W dV_e J_A delta q^A + boundary", "CONDITIONAL_VARIATIONAL_LAW_NOT_PARENT_SIGNED", "explicit S_matter[q] or owned q(Phi) coupling projector"),
        ("CORE2738_2_qnorm", "E_q", "parent q-norm used by source and C_qm", "T_source_norm=sup_{||delta q||_E<=1}|int_W J_A delta q^A dV_e| and C_qm=||Dq[v_m]||_E", "MISSING_PARENT_NORM", "kinetic/operator-derived q norm; variation class; boundary treatment"),
        ("CORE2738_3_Tsource", "T_source_norm", "source strength in q-dual norm", "not orbital GM; derived from J_q and W_src only", "FORMULA_READY_INPUTS_MISSING", "J_q; W_src; E_q; dV_e; units"),
        ("CORE2738_4_UBmax", "U_B,max", "local source-support switch bound", "N_src <= U_B,max S_cg,total_norm", "MISSING_PARENT_OR_NUMERIC_BOUND", "source-backed bound or zero theorem in same branch/domain"),
        ("CORE2738_5_Scg_total", "S_cg,total_norm", "total compact-source coupling norm", "S_cg,total_norm <= S_cg,core + A_affine + A_block_shadow + A_extra_hidden", "TOTAL_GUARD_STAGED_VALUES_MISSING", "C_qm/Tsource/direct/source-normalization/boundary/affine/block/source-shadow values"),
        ("CORE2738_6_QmH", "Q_m^H", "inner compact-source memory/coupling boundary charge", "boundary functional on trace gamma(u) at partial W_src", "DEFINITION_STAGED_VALUE_MISSING", "source charge convention; boundary surface; dual norm"),
        ("CORE2738_7_Cinner", "C_inner", "trace/boundary operator norm", "||gamma(u)||_B <= C_inner E_m(u)", "TRACE_CONSTANT_REQUIRED", "domain, boundary regularity, E_m norm, trace space"),
        ("CORE2738_8_domain_zero", "N_inner,domain", "domain/support motion boundary work", "absolute boundary-dual contribution from moving support/excision", "MISSING_DOMAIN_BOUND", "worldtube domain motion theorem or finite norm"),
        ("CORE2738_9_zero_mode", "N_inner,zero_mode", "zero-mode/reference leakage", "absolute contribution from unremoved boundary/reference mode", "MISSING_ZERO_MODE_BOUND", "zero-mode/reference certificate or finite leakage norm"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "core_id": core_id,
                "symbol": symbol,
                "role": role,
                "definition_or_rule": rule,
                "current_status": status,
                "missing_to_promote": missing,
                "feeds": "N_pair <= U_B,max*S_cg,total_norm + C_inner*||Q_m^H|| + N_inner,domain + N_inner,zero_mode",
                "source_paths": "2737-Y5-R2FR-source-support-and-inner-charge-theorem-or-bound-under-AX1090.md; 1547-Y5-compact-worldtube-profile-template-and-arena-map.md; 1548-Y5-shared-worldtube-profile-symbolic-runner-or-source-data-acquisition.md; 1549-Y5-Jq-unit-dimension-and-parent-source-variation-closure.md",
                "numeric_value_present": False,
                "source_backed": False,
            }
        )
        for core_id, symbol, role, rule, status, missing in specs
    ]


def inner_trace_rows() -> list[dict[str, Any]]:
    rows = [
        ("TR2738_0_boundary_pairing", "B_inner[u]", "B_inner[u]=<Q_m^H,gamma(u)>_{B*,B}", "DEFINITION_CONTRACT", "defines Q_m^H as the boundary functional dual to the trace of u", "Q_m^H source convention and boundary trace space"),
        ("TR2738_1_trace_bound", "trace inequality", "||gamma(u)||_B <= C_inner E_m(u)", "CONDITIONAL_TRACE_LAW", "standard functional step once domain/E_m/boundary regularity are declared", "C_inner/domain/regularity not sourced"),
        ("TR2738_2_inner_norm", "inner charge contribution", "|B_inner[u]| <= ||Q_m^H||_{B*} C_inner E_m(u)", "DERIVED_BOUND_FORM", "turns inner hair into a finite N_inner row without claiming zero", "||Q_m^H|| and C_inner missing"),
        ("TR2738_3_Ninner_charge", "N_inner,charge", "N_inner,charge <= C_inner ||Q_m^H||_{B*}", "FIRST_USABLE_BOUND_ROW_STAGED", "this is the clean mathematical interface for the inner charge", "numeric/source-backed Q_m^H and C_inner"),
        ("TR2738_4_zero_route", "exact inner silence", "Q_m^H=0 and all domain/zero-mode terms vanish", "NOT_PROVED", "positive no-hair and 1529 block automatic inner silence", "parent source-silence/no-flux/zero-mode theorem"),
        ("TR2738_5_first_pair_insert", "N_pair", "N_pair <= U_B,max S_cg,total_norm + C_inner ||Q_m^H||_{B*} + N_inner,domain + N_inner,zero_mode", "TRACE_REFINED_FIRST_PAIR_ROW", "2737 first-pair formula now has an explicit trace-dual meaning", "all numeric/source-backed inputs missing"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "trace_id": trace_id,
                "target": target,
                "formula_or_rule": formula,
                "status": status,
                "why_it_matters": why,
                "missing_to_promote": missing,
                "source_paths": "2737-Y5-R2FR-source-support-and-inner-charge-theorem-or-bound-under-AX1090.md; source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv; source-intake/mts_residuals/P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
                "zero_claim": False,
            }
        )
        for trace_id, target, formula, status, why, missing in rows
    ]


def arena_map_rows() -> list[dict[str, Any]]:
    specs = [
        ("ARENA2738_0_R10", "R10", "alpha_R10(lambda) <= Pi_R10(lambda;W_src,theta_src) * N_pair", "lambda-scale source/test geometry; material convention; Pi_R10 kernel; bound curve for comparison", "MISSING_ARENA_KERNEL"),
        ("ARENA2738_1_PPN", "PPN", "Delta_PPN <= Pi_PPN(W_src,gauge,theta_src)*(N_pair+N_rest)", "weak-field response matrix; gauge convention; source multipoles; Kmetric map", "MISSING_PPN_RESPONSE"),
        ("ARENA2738_2_clock", "clock", "|delta ln nu| <= Pi_clock(W_src,readout,theta_src)*(N_pair+N_rest)", "clock sensitivity; constants split; no-shadow-clock frame; calibration boundary", "MISSING_CLOCK_KERNEL"),
        ("ARENA2738_3_orbital", "orbital", "|delta a/a| <= Pi_orbital(W_src,theta_src)*(N_pair+N_rest)", "source measure/flux closure; exterior matching; orbital readout map", "MISSING_ORBITAL_KERNEL"),
        ("ARENA2738_4_local_GR", "local_GR", "residual_local <= Pi_local(W_src,theta_src)*(N_pair+N_rest)", "Kmetric conversion; hidden-kernel terms; PPN residual vector; source/boundary closure", "BLOCKED_NO_CLAIM"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "arena_id": arena_id,
                "arena": arena,
                "projection_contract": contract,
                "required_inputs": required,
                "current_status": status,
                "shared_profile_rule": "theta_src is fixed once; arenas may only supply Pi_arena projections",
                "forbidden_shortcut": "do not redefine W_src, T_source_norm, Q_m^H, or U_B,max per arena; do not import orbital GM as source norm",
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1547_ARENA_MAP_REQUIREMENTS.csv; source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1548_ARENA_SYMBOLIC_RUNNER_NONCLAIM.csv",
            }
        )
        for arena_id, arena, contract, required, status in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN2738_0_core_inputs", "all core inputs present", "REFUSED_INPUTS_MISSING", "W_src/J_q/E_q/Tsource/U_B/S_cg_total/Q_m^H/C_inner/domain/zero-mode are not source-backed"),
        ("RUN2738_1_trace_bound", "inner trace bound", "PASS_FORMULA_NONCLAIM", "B_inner trace-dual bound is mathematically staged but value-missing"),
        ("RUN2738_2_first_pair", "N_pair computable", "REFUSED_NOT_COMPUTABLE", "first-pair formula has no numeric/source-backed components"),
        ("RUN2738_3_no_orbital_import", "orbital GM shortcut", "PASS_GUARD", "orbital GM remains comparison output only"),
        ("RUN2738_4_no_retuning", "shared theta_src", "PASS_GUARD", "single profile rule is retained from 1547/1548"),
        ("RUN2738_5_arena_scores", "R10/PPN/clock/orbital/local_GR scoring", "REFUSED_ARENA_KERNELS_MISSING", "Pi_arena kernels and legal source profile are missing"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "runner_id": runner_id,
                "check": check,
                "runner_result": result,
                "reason": reason,
                "accepted_for_scoring": False,
                "passes_for_claim": False,
            }
        )
        for runner_id, check, result, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2738_0_template", "Promote 1547/1548 into the live 2737 first-pair branch.", "the old profile template now directly feeds N_pair and N_lock", "worldtube/profile work is no longer generic scaffolding"),
        ("DEC2738_1_trace", "Use the trace-dual form for Q_m^H.", "it is the cleanest way to make inner charge finite without claiming it vanishes", "N_inner has a mathematically auditable norm interface"),
        ("DEC2738_2_no_score", "Do not score N_pair yet.", "all required source/profile/norm/charge values are missing", "all local and arena gates stay blocked"),
        ("DEC2738_3_next", "Next target is parent q-norm/C_qm dual-pairing closure.", "T_source_norm, C_qm, and S_cg,total all need the same parent q norm", "2739 should try to derive E_q or demote the route to explicit missing-input closure"),
    ]
    return [nonclaim({"decision_id": decision_id, "decision": decision, "because": because, "effect": effect}) for decision_id, decision, because, effect in rows]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2738_0_template", "worldtube first-pair template", True, "PASS_NONCLAIM", "fillable W_src/J_q/U_B/Q_m^H/C_inner rows exist"),
        ("GATE2738_1_trace_bound", "inner trace-dual bound", True, "PASS_NONCLAIM", "C_inner||Q_m^H|| boundary contribution is derived as a formula"),
        ("GATE2738_2_numeric_profile", "numeric/source-backed N_pair", False, "BLOCKED", "core values are missing"),
        ("GATE2738_3_unit_norm", "q-norm/C_qm/Tsource unit closure", False, "BLOCKED", "parent q norm and Dq[v_m] norm missing"),
        ("GATE2738_4_arena_scores", "R10/PPN/clock/orbital scores", False, "BLOCKED_NO_CLAIM", "arena kernels and source profile values missing"),
        ("GATE2738_5_local_GR", "local GR/Newton recovery", False, "BLOCKED_NO_CLAIM", "N_pair/N_rest/Nlock/local projection not score-ready"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "claim_allowed": False,
                "reason": reason,
            }
        )
        for gate_id, claim, passed, status, reason in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2738_0_2739",
                "status": "selected_primary",
                "target_doc": "2739-Y5-R2FR-parent-qnorm-Cqm-dual-pairing-closure-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_qnorm_Cqm_dual_pairing_closure_under_AX1090_2739.py",
                "mission": "derive or select the parent-owned q norm E_q used by both T_source_norm and C_qm; decide whether S_cg,total becomes unit-closed or remains an explicit missing-input closure",
                "acceptance": "parent kinetic/operator norm, variation class, Dq[v_m] norm, boundary term handling, and units; or a precise blocker ledger",
                "forbidden": "do not choose an arena-convenient norm; do not mix source and C_qm norms; do not claim R10/PPN/local GR",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2738_0_first_pair_template", "source_table": rel(OUTPUTS["core"]), "copy_path": rel(BRANCH_OUTPUTS["first_pair_template"]), "purpose": "local-bound nonclaim worldtube first-pair template", "exists": BRANCH_OUTPUTS["first_pair_template"].exists()}),
        nonclaim({"copy_id": "BR2738_1_inner_trace", "source_table": rel(OUTPUTS["inner_trace"]), "copy_path": rel(BRANCH_OUTPUTS["inner_trace"]), "purpose": "source-weight trace-dual inner charge contract", "exists": BRANCH_OUTPUTS["inner_trace"].exists()}),
        nonclaim({"copy_id": "BR2738_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for q-norm/Cqm dual-pairing closure", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    core: list[dict[str, Any]],
    inner_trace: list[dict[str, Any]],
    arena_map: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    core_ok = len(core) >= 10 and any(row["symbol"] == "Q_m^H" for row in core) and any(row["symbol"] == "E_q" for row in core)
    trace_ok = any(row["trace_id"] == "TR2738_3_Ninner_charge" for row in inner_trace) and any(row["trace_id"] == "TR2738_5_first_pair_insert" for row in inner_trace)
    arena_ok = len(arena_map) == 5 and all(row["valid_for_claim"] is False for row in arena_map)
    runner_ok = any(row["runner_result"] == "PASS_FORMULA_NONCLAIM" for row in runner) and all(row["accepted_for_scoring"] is False for row in runner)
    gates_ok = any(row["claim_gate_id"] == "GATE2738_1_trace_bound" and row["gate_passed"] is True for row in gates) and all(row["claim_allowed"] is False for row in gates)
    next_ok = next_target[0]["selected"] is True and "qnorm-Cqm" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_ok = formalization_recent_count() == 0
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2738_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2738_1_core_template", "passed": core_ok, "detail": "first-pair core template includes Q_m^H and parent q-norm rows", "timestamp_utc": ts()},
        {"validation_id": "VAL2738_2_inner_trace_contract", "passed": trace_ok, "detail": "trace-dual inner charge contract and first-pair insert are written", "timestamp_utc": ts()},
        {"validation_id": "VAL2738_3_arena_map", "passed": arena_ok, "detail": "shared arena support maps are present and nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2738_4_runner_refuses_score", "passed": runner_ok, "detail": "runner accepts formula-only trace progress but refuses scoring", "timestamp_utc": ts()},
        {"validation_id": "VAL2738_5_claim_gates", "passed": gates_ok, "detail": "only nonclaim/template gates pass; all claim gates remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2738_6_next_target", "passed": next_ok, "detail": "next target is parent q-norm/Cqm dual pairing", "timestamp_utc": ts()},
        {"validation_id": "VAL2738_7_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2738_8_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2738_9_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2738_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2738 binds the shared worldtube/source-profile template to the live first-pair branch, derives the trace-dual inner charge bound form, and selects q-norm/Cqm closure next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2738 - Y5 R2/f(R): Worldtube Source Profile And Inner Charge Template Under AX1090

Status: `Y5_R2FR_2738_worldtube_first_pair_template_trace_inner_charge_bound_nonclaim`

## Private Verdict

2738 pulls the older worldtube/profile machinery into the live local-GR route.

The first-pair contract is now:

`N_pair <= U_B,max S_cg,total_norm + C_inner ||Q_m^H||_{{B*}} + N_inner,domain + N_inner,zero_mode`.

The useful new mathematical move is the trace-dual inner-charge form:

`B_inner[u]=<Q_m^H,gamma(u)>_{{B*,B}}`,

`||gamma(u)||_B <= C_inner E_m(u)`,

so

`|B_inner[u]| <= C_inner ||Q_m^H||_{{B*}} E_m(u)`.

That gives the inner charge a real norm interface instead of a vague boundary gremlin. Still: no score, no local-GR claim, no R10/PPN/clock/orbital claim. The values and parent q-norm are missing.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Worldtube First-Pair Core Template

{markdown_table(data["core"], ["core_id", "symbol", "role", "definition_or_rule", "current_status", "missing_to_promote", "feeds", "valid_for_claim"])}

## Inner Charge Trace Bound Contract

{markdown_table(data["inner_trace"], ["trace_id", "target", "formula_or_rule", "status", "why_it_matters", "missing_to_promote", "zero_claim", "valid_for_claim"])}

## Shared Arena Support Map Template

{markdown_table(data["arena_map"], ["arena_id", "arena", "projection_contract", "required_inputs", "current_status", "shared_profile_rule", "forbidden_shortcut", "valid_for_claim"])}

## First-Pair Profile Runner

{markdown_table(data["runner"], ["runner_id", "check", "runner_result", "reason", "accepted_for_scoring", "passes_for_claim", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "because", "effect", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "claim_allowed", "valid_for_claim", "reason"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is exactly the sort of bridge we need if MTS is going to reduce to GR rather than just gesture at it. The source is now a shared object, the boundary charge has a trace norm, and the next missing piece is brutally specific: the parent q-norm that both `T_source_norm` and `C_qm` must use.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    core = core_rows()
    inner_trace = inner_trace_rows()
    arena_map = arena_map_rows()
    runner = runner_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["core"], core)
    write_csv(OUTPUTS["inner_trace"], inner_trace)
    write_csv(OUTPUTS["arena_map"], arena_map)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["first_pair_template"], core)
    write_csv(BRANCH_OUTPUTS["inner_trace"], inner_trace)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, core, inner_trace, arena_map, runner, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "core": core,
        "inner_trace": inner_trace,
        "arena_map": arena_map,
        "runner": runner,
        "decisions": decisions,
        "gates": gates,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2738 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
