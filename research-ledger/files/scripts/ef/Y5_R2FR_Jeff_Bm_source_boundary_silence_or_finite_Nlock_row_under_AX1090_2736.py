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

DOC = ROOT / "2736-Y5-R2FR-Jeff-Bm-source-boundary-silence-or-finite-Nlock-row-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2736_SOURCE_REGISTER.csv",
    "jeff": RESIDUALS / "P8_Y5_R2FR_2736_JEFF_COMPONENT_NORM_LEDGER.csv",
    "bm": RESIDUALS / "P8_Y5_R2FR_2736_BM_COMPONENT_NORM_LEDGER.csv",
    "nlock": RESIDUALS / "P8_Y5_R2FR_2736_NLOCK_BOUND_ROW.csv",
    "silence": RESIDUALS / "P8_Y5_R2FR_2736_EXACT_SILENCE_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2736_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2736_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2736_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2736_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2736_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "nlock": LOCAL_BOUNDS / "Nlock_bound_2736_NONCLAIM.csv",
    "reopen": SOURCE_WEIGHT / "Jeff_Bm_exact_silence_reopen_conditions_2736_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2736_JEFF_BM_COMPONENT_NORM_NEXT.csv",
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
            "source_id": "SRC2736_0_2735_doc",
            "description": "2735 selects J_eff/B_m source-boundary silence or finite N_lock.",
            "source_path": "2735-Y5-R2FR-stationary-source-root-local-lock-or-finite-Delta-m-bound-under-AX1090.md",
            "required_needles": "NEXT2735_0_selected;BLK2735_0_Jeff;BLK2735_1_Bm;LOCK2735_3_field_amplitude_bound",
        },
        {
            "source_id": "SRC2736_1_1536_doc",
            "description": "1536 decomposes J_eff and B_m and writes the absolute N_lock envelope.",
            "source_path": "1536-Y5-Jeff-Bm-source-boundary-silence-or-bound.md",
            "required_needles": "JEFF1536_0_screened_source;BM1536_0_inner_charge;NLOCK1536_5_lock_norm;DEC1536_2_bound_route",
        },
        {
            "source_id": "SRC2736_2_1537_doc",
            "description": "1537 supplies component norm slots and prioritizes N_src/N_inner.",
            "source_path": "1537-Y5-Jeff-Bm-component-norm-input-pack.md",
            "required_needles": "NORM1537_0_N_src;NORM1537_7_N_inner;NLR1537_2_Nlock;DEC1537_3_next",
        },
        {
            "source_id": "SRC2736_3_1535_audit",
            "description": "1535 identifies J_eff and B_m as primary blockers.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1535_LOCKING_INPUT_SOURCE_AUDIT.csv",
            "required_needles": "LIA1535_4_Jeff;LIA1535_5_Bm;LIA1535_6_Cemb",
        },
        {
            "source_id": "SRC2736_4_1534_leakage",
            "description": "1534 provides the forcing and field-amplitude bound interface.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv",
            "required_needles": "LEAK1534_1_forcing_bound;LEAK1534_2_field_bound;LEAK1534_6_verdict",
        },
        {
            "source_id": "SRC2736_5_1536_jeff_csv",
            "description": "machine-readable J_eff component split.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1536_JEFF_COMPONENT_SPLIT.csv",
            "required_needles": "JEFF1536_0_screened_source;JEFF1536_6_source_current;JEFF1536_7_verdict",
        },
        {
            "source_id": "SRC2736_6_1536_bm_csv",
            "description": "machine-readable B_m component split.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1536_BM_COMPONENT_SPLIT.csv",
            "required_needles": "BM1536_0_inner_charge;BM1536_5_domain_motion;BM1536_6_verdict",
        },
        {
            "source_id": "SRC2736_7_1536_nlock_csv",
            "description": "machine-readable N_lock envelope contract.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv",
            "required_needles": "NLOCK1536_1_dual_norm;NLOCK1536_4_boundary_sum;NLOCK1536_5_lock_norm",
        },
        {
            "source_id": "SRC2736_8_1529_boundary",
            "description": "boundary certificate audit blocks no-flux/zero-mode shortcuts.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
            "required_needles": "BND1529_0_domain_certificate;BND1529_1_boundary_condition;BND1529_2_zero_mode_reference",
        },
        {
            "source_id": "SRC2736_9_gamma_expansion",
            "description": "Gamma source expansion showing source/drift/history/transition terms.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "required_needles": "GSE798_0_definition;GSE798_3_static_relaxation_source;GSE798_5_source_law_verdict",
        },
        {
            "source_id": "SRC2736_10_positive_nohair",
            "description": "positive operator no-hair attempt, including boundary-source warnings.",
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


def jeff_rows() -> list[dict[str, Any]]:
    specs = [
        ("N_SRC2736_0_N_src", "N_src", "J_src=U_B S_cg", "||U_B S_cg||_{E*}", "PRIMARY_MISSING", "U_B bound; S_cg norm; source projection; E* norm", "source"),
        ("N_SRC2736_1_N_drift_mL", "N_drift_mL", "J_drift_mL", "||J_drift_mL||_{E*}", "MISSING_ZERO_OR_NORM", "locked baseline theorem or finite m_L drift norm", "drift"),
        ("N_SRC2736_2_N_drift_Lcg", "N_drift_Lcg", "J_drift_Lcg", "||J_drift_Lcg||_{E*}", "MISSING_ZERO_OR_NORM", "L_cg silence/fixed-source branch or finite L_cg drift norm", "drift"),
        ("N_SRC2736_3_N_selector", "N_selector", "J_selector(Pi_B,mu_B,tau_L)", "||J_selector||_{E*}", "MISSING_ZERO_OR_NORM", "selector variation law or finite Pi_B/mu_B/tau_L norm", "selector"),
        ("N_SRC2736_4_N_history", "N_history", "J_history", "||J_history||_{E*}", "MISSING_ZERO_OR_NORM", "local history silence or finite memory-injection norm", "history"),
        ("N_SRC2736_5_N_transition", "N_transition", "J_transition", "||J_transition||_{E*}", "MISSING_ZERO_OR_NORM", "transition-current/K_perp norm", "transition"),
        ("N_SRC2736_6_N_mass_current", "N_mass_current", "J_mass_current", "||J_mass_current||_{E*}", "MISSING_ZERO_OR_NORM", "source-current/Meff closure residual norm", "source-current"),
    ]
    rows = [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "norm_id": norm_id,
                "symbol": symbol,
                "component": component,
                "norm_definition": norm_definition,
                "status": status,
                "missing_to_promote": missing,
                "category": category,
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1536_JEFF_COMPONENT_SPLIT.csv; 1537-Y5-Jeff-Bm-component-norm-input-pack.md",
                "zero_proved": False,
                "finite_bound_sourced": False,
                "numeric_value": "MISSING",
            }
        )
        for norm_id, symbol, component, norm_definition, status, missing, category in specs
    ]
    rows.append(
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "norm_id": "N_SRC2736_7_N_J_total",
                "symbol": "N_J",
                "component": "J_eff total",
                "norm_definition": "N_J <= N_src+N_drift_mL+N_drift_Lcg+N_selector+N_history+N_transition+N_mass_current",
                "status": "FORMULA_READY_COMPONENTS_MISSING",
                "missing_to_promote": "all J_eff component zero theorems or finite dual norms",
                "category": "aggregate-source",
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv",
                "zero_proved": False,
                "finite_bound_sourced": False,
                "numeric_value": "MISSING",
            }
        )
    )
    return rows


def bm_rows() -> list[dict[str, Any]]:
    specs = [
        ("N_BM2736_0_N_inner", "N_inner", "B_inner or Q_m^H", "boundary-dual norm of inner compact-source charge", "PRIMARY_MISSING", "inner monopole/source charge theorem or finite boundary norm", "inner-boundary"),
        ("N_BM2736_1_N_no_flux", "N_no_flux", "B_no_flux", "boundary-dual norm of no-flux violation", "MISSING_ZERO_OR_NORM", "boundary condition certificate or no-flux violation norm", "boundary-condition"),
        ("N_BM2736_2_N_zero_mode", "N_zero_mode", "B_zero_mode", "boundary-dual norm of zero-mode/reference leakage", "MISSING_ZERO_OR_NORM", "zero-mode certificate or reference leakage norm", "zero-mode"),
        ("N_BM2736_3_N_outer", "N_outer", "B_outer", "boundary-dual norm of outer/reference flux", "MISSING_ZERO_OR_NORM", "outer flux/fixed-reference norm", "outer-boundary"),
        ("N_BM2736_4_N_history_boundary", "N_history_boundary", "B_history", "boundary-dual norm of history boundary injection", "MISSING_ZERO_OR_NORM", "history boundary norm", "history-boundary"),
        ("N_BM2736_5_N_domain", "N_domain", "B_domain", "boundary-dual norm of domain/support motion", "MISSING_ZERO_OR_NORM", "domain/support variation norm", "domain"),
    ]
    rows = [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "norm_id": norm_id,
                "symbol": symbol,
                "component": component,
                "norm_definition": norm_definition,
                "status": status,
                "missing_to_promote": missing,
                "category": category,
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1536_BM_COMPONENT_SPLIT.csv; 1537-Y5-Jeff-Bm-component-norm-input-pack.md",
                "zero_proved": False,
                "finite_bound_sourced": False,
                "numeric_value": "MISSING",
            }
        )
        for norm_id, symbol, component, norm_definition, status, missing, category in specs
    ]
    rows.append(
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "norm_id": "N_BM2736_6_N_B_total",
                "symbol": "N_B",
                "component": "B_m total",
                "norm_definition": "N_B <= N_inner+N_no_flux+N_zero_mode+N_outer+N_history_boundary+N_domain",
                "status": "FORMULA_READY_COMPONENTS_MISSING",
                "missing_to_promote": "all B_m component zero theorems or finite boundary norms",
                "category": "aggregate-boundary",
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv",
                "zero_proved": False,
                "finite_bound_sourced": False,
                "numeric_value": "MISSING",
            }
        )
    )
    return rows


def nlock_rows() -> list[dict[str, Any]]:
    rows = [
        ("NLOCK2736_0_energy_identity", "E_m(u)^2=<u,J_eff>+B_m", "imported local lock identity", "IMPORTED_CONDITIONAL_IDENTITY", "D_m/M_scr/domain/zero-mode plus J_eff/B_m closures"),
        ("NLOCK2736_1_dual_norm", "|<u,J_eff>| <= N_J E_m(u)", "source forcing controlled by absolute dual norm", "FORMULA_READY_COMPONENTS_MISSING", "J_eff component norms"),
        ("NLOCK2736_2_boundary_norm", "|B_m| <= N_B E_m(u)", "boundary forcing controlled by absolute boundary norm", "FORMULA_READY_COMPONENTS_MISSING", "B_m component norms"),
        ("NLOCK2736_3_component_sum", "N_J <= N_src+N_drift_mL+N_drift_Lcg+N_selector+N_history+N_transition+N_mass_current", "no cancellation among source pieces", "NO_CANCELLATION_ENVELOPE", "component rows numeric or theorem-zero"),
        ("NLOCK2736_4_boundary_sum", "N_B <= N_inner+N_no_flux+N_zero_mode+N_outer+N_history_boundary+N_domain", "no cancellation among boundary pieces", "NO_CANCELLATION_ENVELOPE", "component rows numeric or theorem-zero"),
        ("NLOCK2736_5_lock_norm", "E_m(u) <= N_lock := N_J + N_B", "finite local-lock leakage norm", "CONDITIONAL_NLOCK_ROW_STAGED", "N_J and N_B are not numeric/sourced"),
        ("NLOCK2736_6_amplitude", "Delta_m <= U_m <= C_emb N_lock", "feeds the stationary source-root leakage law", "AMPLITUDE_ROW_STAGED_NONCLAIM", "C_emb/domain constant and N_lock"),
        ("NLOCK2736_7_verdict", "N_lock is formula-ready, not score-ready", "finite route survives as plumbing but not evidence", "NOT_SCORE_READY", "primary blockers N_src and N_inner remain missing"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "bound_id": bound_id,
                "formula_or_rule": formula,
                "meaning": meaning,
                "status": status,
                "missing_to_promote": missing,
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv; source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv; 2735-Y5-R2FR-stationary-source-root-local-lock-or-finite-Delta-m-bound-under-AX1090.md",
            }
        )
        for bound_id, formula, meaning, status, missing in rows
    ]


def silence_rows() -> list[dict[str, Any]]:
    rows = [
        ("SIL2736_0_Jsrc_zero", "J_src=0", "BLOCKED", "U_B=0/source silence or zero exterior projection of S_cg is not parent-signed"),
        ("SIL2736_1_Jdrift_zero", "J_drift_mL=J_drift_Lcg=0", "BLOCKED", "locked baseline/L_cg drift silence is not parent-signed"),
        ("SIL2736_2_Jselector_history_transition_zero", "J_selector=J_history=J_transition=0", "BLOCKED", "selector, history, and transition-current silence remain conditional"),
        ("SIL2736_3_Jmass_current_zero", "J_mass_current=0", "BLOCKED", "source-current/Meff flux closure is not parent-derived"),
        ("SIL2736_4_Binner_zero", "B_inner=0 or Q_m^H=0", "BLOCKED", "inner compact-source charge can support exterior hair"),
        ("SIL2736_5_Bnoflux_zero", "B_no_flux=0", "BLOCKED", "no parent boundary-condition certificate"),
        ("SIL2736_6_Bzeromode_outer_domain_zero", "B_zero_mode=B_outer=B_domain=0", "BLOCKED", "zero-mode, outer-reference flux, and moving-domain work remain open"),
        ("SIL2736_7_exact_lock", "J_eff=0 and B_m=0", "NOT_PROVED", "at least one source and one boundary clause remain unsigned"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "silence_id": silence_id,
                "target": target,
                "status": status,
                "reason": reason,
                "source_paths": "1536-Y5-Jeff-Bm-source-boundary-silence-or-bound.md; 1537-Y5-Jeff-Bm-component-norm-input-pack.md",
                "silence_proved": False,
            }
        )
        for silence_id, target, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2736_0_exact_silence", "Do not claim J_eff=0 or B_m=0.", "source and boundary zero clauses remain unsigned", "exact local lock remains blocked"),
        ("DEC2736_1_finite_route", "Keep the finite N_lock route.", "the absolute-sum envelope is derivable from the energy identity and component split", "leakage can become scoreable once component norms are sourced"),
        ("DEC2736_2_no_cancellation", "Use absolute sums only.", "source/boundary cancellations would be fragile and less defensible", "route is conservative and lower-scrutiny"),
        ("DEC2736_3_next", "Go after N_src and N_inner first.", "1537 identifies them as the first physical blockers", "next target is source support and inner compact-source charge"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "effect": effect,
            }
        )
        for decision_id, decision, because, effect in rows
    ]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2736_0_exact_lock", "exact local lock Delta_m=0", False, "J_eff/B_m silence not proved"),
        ("GATE2736_1_finite_Nlock", "finite numeric N_lock", False, "component norms are placeholders"),
        ("GATE2736_2_q_loc_zero", "q_loc^nu -> 0", False, "local projection map and N_lock are not numeric"),
        ("GATE2736_3_local_GR", "local GR/Newton/PPN recovery", False, "pre-lock, hidden-kernel, and projection gates remain open"),
        ("GATE2736_4_R10_WEP_clock_orbital", "R10/WEP/clock/orbital pass", False, "no sourced local residual amplitude"),
        ("GATE2736_5_public_claim", "public or GitHub claim", False, "private nonclaim derivation checkpoint"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "claim_allowed": False,
                "reason": reason,
            }
        )
        for gate_id, claim, passed, reason in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2736_0_2737",
                "status": "selected_primary",
                "target_doc": "2737-Y5-R2FR-source-support-and-inner-charge-theorem-or-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_source_support_and_inner_charge_theorem_or_bound_under_AX1090_2737.py",
                "mission": "derive or bound N_src=||U_B S_cg||_{E*} and N_inner from the compact-source boundary charge Q_m^H; decide whether the first N_lock inputs can become theorem-zero or finite-bound rows",
                "acceptance": "one of: U_B/source-projection silence; sourced finite S_cg norm; inner charge zero theorem; finite boundary-dual Q_m^H norm; or explicit blocker ledger",
                "forbidden": "do not claim U_B=0, Q_m^H=0, local GR, PPN, R10, WEP, clock, or orbital pass without parent proof and numeric/source-backed rows",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "copy_id": "BR2736_0_Nlock_bound",
                "source_table": rel(OUTPUTS["nlock"]),
                "copy_path": rel(BRANCH_OUTPUTS["nlock"]),
                "purpose": "local-bound nonclaim N_lock formula row for later Delta_m propagation",
                "exists": BRANCH_OUTPUTS["nlock"].exists(),
            }
        ),
        nonclaim(
            {
                "copy_id": "BR2736_1_reopen",
                "source_table": rel(OUTPUTS["silence"]),
                "copy_path": rel(BRANCH_OUTPUTS["reopen"]),
                "purpose": "source-weight reopen conditions for exact J_eff/B_m silence",
                "exists": BRANCH_OUTPUTS["reopen"].exists(),
            }
        ),
        nonclaim(
            {
                "copy_id": "BR2736_2_next_queue",
                "source_table": rel(OUTPUTS["next"]),
                "copy_path": rel(BRANCH_OUTPUTS["next_queue"]),
                "purpose": "RAB acquisition queue for source-support and inner-charge work",
                "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            }
        ),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    jeff: list[dict[str, Any]],
    bm: list[dict[str, Any]],
    nlock: list[dict[str, Any]],
    silence: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    jeff_ok = len(jeff) == 8 and any(row["symbol"] == "N_src" and row["status"] == "PRIMARY_MISSING" for row in jeff)
    bm_ok = len(bm) == 7 and any(row["symbol"] == "N_inner" and row["status"] == "PRIMARY_MISSING" for row in bm)
    nlock_ok = any(row["bound_id"] == "NLOCK2736_5_lock_norm" for row in nlock) and any(row["bound_id"] == "NLOCK2736_6_amplitude" for row in nlock)
    silence_blocked = all(row["silence_proved"] is False and row["claim_allowed"] is False for row in silence)
    gates_false = all(row["gate_passed"] is False and row["claim_allowed"] is False for row in gates)
    next_ok = next_target[0]["selected"] is True and "source-support-and-inner-charge" in next_target[0]["target_doc"]
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
        {"validation_id": "VAL2736_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2736_1_jeff_component_ledger", "passed": jeff_ok, "detail": "J_eff ledger has all component norm rows and N_src remains primary missing", "timestamp_utc": ts()},
        {"validation_id": "VAL2736_2_bm_component_ledger", "passed": bm_ok, "detail": "B_m ledger has all component norm rows and N_inner remains primary missing", "timestamp_utc": ts()},
        {"validation_id": "VAL2736_3_nlock_bound_row", "passed": nlock_ok, "detail": "N_lock and Delta_m amplitude rows are staged as nonclaim formulas", "timestamp_utc": ts()},
        {"validation_id": "VAL2736_4_exact_silence_blocked", "passed": silence_blocked, "detail": "exact source-boundary silence is not claimed", "timestamp_utc": ts()},
        {"validation_id": "VAL2736_5_claim_gates_false", "passed": gates_false, "detail": "no local-GR, PPN, R10, WEP, clock, orbital, q_loc-zero, or public claim is allowed", "timestamp_utc": ts()},
        {"validation_id": "VAL2736_6_next_target", "passed": next_ok, "detail": "next target is source support and inner charge rather than repeating component schema", "timestamp_utc": ts()},
        {"validation_id": "VAL2736_7_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2736_8_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2736_9_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2736_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2736 rejects exact J_eff/B_m silence for now, stages a conservative finite N_lock row, and selects source support plus inner charge next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2736 - Y5 R2/f(R): J_eff / B_m Source-Boundary Silence Or Finite Nlock Row Under AX1090

Status: `Y5_R2FR_2736_exact_silence_blocked_finite_Nlock_row_staged_nonclaim`

## Private Verdict

2736 does **not** prove exact local silence. The clean local-GR route would need `J_eff=0` and `B_m=0`; that is still unsigned because the screened compact-source support term and the inner compact-source boundary charge remain open.

But this is not wheel-spinning. The fallback is now a conservative, no-cancellation leakage contract:

`E_m(u)^2=<u,J_eff>+B_m`,

`|<u,J_eff>| <= N_J E_m(u)`, `|B_m| <= N_B E_m(u)`,

`N_lock=N_J+N_B`, so `E_m(u)<=N_lock` and `Delta_m<=U_m<=C_emb N_lock`.

The first two physical pieces to attack are now sharp: `N_src=||U_B S_cg||_{{E*}}` and `N_inner` from the compact-source boundary charge `Q_m^H`. If either can be theorem-zero or tightly bounded, the local branch becomes genuinely scoreable instead of symbolic.

No local-GR, Newton, PPN, R10, WEP, clock, orbital, `q_loc=0`, exact lock, or public claim follows from this checkpoint.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## J_eff Component Norm Ledger

{markdown_table(data["jeff"], ["norm_id", "symbol", "component", "norm_definition", "status", "missing_to_promote", "zero_proved", "finite_bound_sourced", "numeric_value", "valid_for_claim"])}

## B_m Component Norm Ledger

{markdown_table(data["bm"], ["norm_id", "symbol", "component", "norm_definition", "status", "missing_to_promote", "zero_proved", "finite_bound_sourced", "numeric_value", "valid_for_claim"])}

## Nlock Bound Row

{markdown_table(data["nlock"], ["bound_id", "formula_or_rule", "meaning", "status", "missing_to_promote", "valid_for_claim"])}

## Exact Silence Gate

{markdown_table(data["silence"], ["silence_id", "target", "status", "reason", "silence_proved", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "because", "effect", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim", "gate_passed", "claim_allowed", "valid_for_claim", "reason"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This checkpoint says: the castle gate is the coupling/source support plus boundary charge. We did not magically make them vanish. We did pin them to two named beasts. Next step is not another loop around the same hill; it is directly testing whether `U_B S_cg` and `Q_m^H` can be killed or bounded.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    jeff = jeff_rows()
    bm = bm_rows()
    nlock = nlock_rows()
    silence = silence_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["jeff"], jeff)
    write_csv(OUTPUTS["bm"], bm)
    write_csv(OUTPUTS["nlock"], nlock)
    write_csv(OUTPUTS["silence"], silence)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["nlock"], nlock)
    write_csv(BRANCH_OUTPUTS["reopen"], silence)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, jeff, bm, nlock, silence, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "jeff": jeff,
        "bm": bm,
        "nlock": nlock,
        "silence": silence,
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
        raise SystemExit(f"2736 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
