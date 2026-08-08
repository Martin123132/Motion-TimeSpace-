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

DOC = ROOT / "2735-Y5-R2FR-stationary-source-root-local-lock-or-finite-Delta-m-bound-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2735_SOURCE_REGISTER.csv",
    "root": RESIDUALS / "P8_Y5_R2FR_2735_STATIONARY_SOURCE_ROOT_LAW.csv",
    "lock": RESIDUALS / "P8_Y5_R2FR_2735_LOCAL_LOCK_AMPLITUDE_LAW.csv",
    "leakage": RESIDUALS / "P8_Y5_R2FR_2735_DOUBLE_ZERO_LEAKAGE_PROPAGATION.csv",
    "blockers": RESIDUALS / "P8_Y5_R2FR_2735_LOCKING_BLOCKER_PRIORITY.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2735_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2735_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2735_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2735_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2735_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "delta_m": LOCAL_BOUNDS / "Delta_m_lock_bound_2735_NONCLAIM.csv",
    "reopen": SOURCE_WEIGHT / "stationary_source_root_reopen_conditions_2735_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2735_JEFF_BM_SOURCE_BOUNDARY_NEXT.csv",
}


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
            "source_id": "SRC2735_0_2734_doc",
            "description": "2734 selects stationary source root/local lock or finite Delta_m bound.",
            "source_path": "2734-Y5-R2FR-Lcg-metric-silence-or-first-ML-kernel-norm-row-under-AX1090.md",
            "required_needles": "NEXT2734_0_selected;RLC2734_1_source_root_kill;MLB2734_2_double_zero_displacement",
        },
        {
            "source_id": "SRC2735_1_1291_strict_double_zero",
            "description": "strict double-zero parent clause and variation proof.",
            "source_path": "1291-Y5-R10-RAB-strict-double-zero-parent-clause-or-chain-kernel-residual-bound.md",
            "required_needles": "SDZ1291_1_strict_F_form;VP1291_1_metric_variation;ADG1291_1_parent_lock",
        },
        {
            "source_id": "SRC2735_2_1533_contract",
            "description": "vacuum-subtracted stationary source contract.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1533_PARENT_ACTION_DOUBLE_ZERO_CONTRACT.csv",
            "required_needles": "VAC1533_1_potential_source;VAC1533_4_local_lock;VAC1533_6_verdict",
        },
        {
            "source_id": "SRC2735_3_1533_derivation",
            "description": "conditional source-root and chain-silence derivation.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1533_DOUBLE_ZERO_DERIVATION.csv",
            "required_needles": "DZD1533_2_derivative;DZD1533_3_quadratic_leakage;DZD1533_4_chain_silence",
        },
        {
            "source_id": "SRC2735_4_1533_lock_requirements",
            "description": "local locking requirements after double-zero.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1533_LOCAL_LOCKING_REQUIREMENTS.csv",
            "required_needles": "LOCK1533_0_operator;LOCK1533_4_leakage_bound;LOCK1533_5_verdict",
        },
        {
            "source_id": "SRC2735_5_1534_nohair",
            "description": "positive-operator no-hair theorem shape.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1534_LOCAL_LOCKING_NOHAIR_THEOREM.csv",
            "required_needles": "NH1534_2_energy_identity;NH1534_3_exact_nohair;NH1534_6_verdict",
        },
        {
            "source_id": "SRC2735_6_1534_leakage",
            "description": "quadratic leakage bound contract.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv",
            "required_needles": "LEAK1534_1_forcing_bound;LEAK1534_3_F_bound;LEAK1534_5_Kchain_bound",
        },
        {
            "source_id": "SRC2735_7_1535_source_audit",
            "description": "input source audit identifying J_eff and B_m as primary blockers.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1535_LOCKING_INPUT_SOURCE_AUDIT.csv",
            "required_needles": "LIA1535_4_Jeff;LIA1535_5_Bm;LIA1535_8_Kchain",
        },
        {
            "source_id": "SRC2735_8_1535_priority",
            "description": "next input priority: source and boundary first.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1535_NEXT_INPUT_PRIORITY.csv",
            "required_needles": "PRI1535_0_first;J_eff and B_m;NEXT_1536_SOURCE_BOUNDARY_SILENCE_OR_BOUND",
        },
        {
            "source_id": "SRC2735_9_1372_qnorm",
            "description": "Q_norm decomposition that receives Delta_m/Delta_grad_m leakage.",
            "source_path": "1372-Y5-R10-RAB-fixed-L0-double-zero-local-residual-theorem-or-Qnorm-bound.md",
            "required_needles": "QNB1372_1_algebraic_quadratic_source;DEC1372_1_Qnorm_route",
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


def root_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "law_id": "SSR2735_0_parent_stationarity",
                "object": "parent local source potential",
                "formula": "V'(m_*)=0 and V''(m_*) finite/nonnegative at a stable local branch",
                "status": "DERIVED_IF_PARENT_V_EXISTS",
                "missing_to_promote": "actual parent V(m), m_* definition, stability/zero-mode convention, same-branch sign",
                "effect": "gives F'_vac(m_*)=0 after vacuum subtraction",
            }
        ),
        nonclaim(
            {
                "law_id": "SSR2735_1_vacuum_subtraction",
                "object": "F_vac(m)",
                "formula": "F_vac(m):=V(m)-V(m_*), hence F_vac(m_*)=0",
                "status": "IDENTITY_UNDER_PARENT_SUBTRACTION",
                "missing_to_promote": "parent-owned subtraction/background convention, not per-system fitted offset",
                "effect": "kills the M_L coefficient at exact local lock",
            }
        ),
        nonclaim(
            {
                "law_id": "SSR2735_2_double_zero",
                "object": "F_vac'(m_*)",
                "formula": "F_vac'(m_*)=V'(m_*)=0",
                "status": "CONDITIONAL_DOUBLE_ZERO_PROVED",
                "missing_to_promote": "stationarity must be live parent action, not a post-hoc root selection",
                "effect": "kills the M_m coefficient at exact local lock",
            }
        ),
        nonclaim(
            {
                "law_id": "SSR2735_3_taylor_leakage",
                "object": "finite off-root leakage",
                "formula": "F_vac(m_*+u)=1/2 V2 u^2 + O(u^3), F_vac'(m_*+u)=V2 u + O(u^2)",
                "status": "AMPLITUDE_LAW_DERIVED_CONDITIONAL",
                "missing_to_promote": "Delta_m/U_m bound, V2/V3 bounds, transition support control",
                "effect": "turns failed exact lock into a quadratic/linear leakage budget",
            }
        ),
        nonclaim(
            {
                "law_id": "SSR2735_4_verdict",
                "object": "source-root theorem status",
                "formula": "source-root math is clean, but the live claim is blocked by parent V and local lock inputs",
                "status": "CONDITIONAL_THEOREM_NOT_LIVE_CLAIM",
                "missing_to_promote": "parent potential plus J_eff/B_m/domain/operator inputs",
                "effect": "continue to lock amplitude rather than repeating double-zero algebra",
            }
        ),
    ]


def lock_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "lock_id": "LOCK2735_0_energy_identity",
                "quantity": "u:=m-m_*",
                "law": "E_m(u)^2=int_A[D_m|grad u|^2+M_scr^2 u^2]=<u,J_eff>+B_m",
                "status": "ENERGY_IDENTITY_INTERFACE",
                "missing_inputs": "D_m sign;M_scr^2 sign;domain/measure;zero-mode convention;J_eff;B_m",
                "consequence": "local lock is controlled by source and boundary forcing",
            }
        ),
        nonclaim(
            {
                "lock_id": "LOCK2735_1_exact_nohair",
                "quantity": "Delta_m",
                "law": "If J_eff=0, B_m=0, and the positive operator has no unsuppressed zero mode, then E_m(u)=0 and Delta_m=0.",
                "status": "EXACT_LOCK_CONDITIONAL_NOT_LIVE",
                "missing_inputs": "J_eff zero theorem;B_m no-flux theorem;operator positivity;zero-mode/domain certificate",
                "consequence": "would evaluate F_vac and F_vac' exactly at the double-zero root",
            }
        ),
        nonclaim(
            {
                "lock_id": "LOCK2735_2_finite_energy_bound",
                "quantity": "E_m(u)",
                "law": "If |<u,J_eff>+B_m| <= N_lock E_m(u), then E_m(u)<=N_lock.",
                "status": "FINITE_LOCK_BOUND_DERIVED",
                "missing_inputs": "H^-1/dual norm for J_eff;boundary norm for B_m",
                "consequence": "source/boundary terms dominate the finite lock amplitude",
            }
        ),
        nonclaim(
            {
                "lock_id": "LOCK2735_3_field_amplitude_bound",
                "quantity": "Delta_m or U_m",
                "law": "Delta_m <= U_m <= C_emb N_lock",
                "status": "AMPLITUDE_INTERFACE_DERIVED",
                "missing_inputs": "embedding/Poincare constant C_emb and domain/collar convention",
                "consequence": "feeds the double-zero Taylor leakage rows",
            }
        ),
        nonclaim(
            {
                "lock_id": "LOCK2735_4_verdict",
                "quantity": "local lock",
                "law": "Exact lock is not proved; finite Delta_m is not score-ready because N_lock and C_emb are missing.",
                "status": "LOCK_ROUTE_BLOCKED_BUT_FORMALIZED",
                "missing_inputs": "J_eff;B_m;C_emb;operator/domain values",
                "consequence": "next step must attack source/boundary silence or finite N_lock",
            }
        ),
    ]


def leakage_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "leakage_id": "DLP2735_0_F_bound",
                "quantity": "F_bar",
                "formula": "F_bar <= 1/2 V2_max Delta_m^2 + 1/6 V3_max Delta_m^3",
                "status": "DOUBLE_ZERO_SOURCE_LEAKAGE_BOUND",
                "missing_inputs": "V2_max;V3_max;Delta_m",
                "maps_to": "M_L coefficient and volume/source leakage",
            }
        ),
        nonclaim(
            {
                "leakage_id": "DLP2735_1_Fprime_bound",
                "quantity": "F1_bar",
                "formula": "F1_bar <= V2_max Delta_m + 1/2 V3_max Delta_m^2",
                "status": "DERIVATIVE_LEAKAGE_BOUND",
                "missing_inputs": "V2_max;V3_max;Delta_m",
                "maps_to": "M_m coefficient and gradient-source leakage",
            }
        ),
        nonclaim(
            {
                "leakage_id": "DLP2735_2_ML_residual",
                "quantity": "||R_L||",
                "formula": "||R_L|| <= 2 |C_sign| L_min^-3 F_bar M_L_bar",
                "status": "ROLLED_FROM_2734",
                "missing_inputs": "C_sign;L_min;M_L_bar;units/index convention",
                "maps_to": "DeltaK/q_loc algebraic L_cg channel",
            }
        ),
        nonclaim(
            {
                "leakage_id": "DLP2735_3_Mm_residual",
                "quantity": "||R_m||",
                "formula": "||R_m|| <= |C_sign| L_min^-2 F1_bar M_m_bar",
                "status": "PAIR_BOUND_WITH_ML_CHANNEL",
                "missing_inputs": "C_sign;L_min;M_m_bar;units/index convention",
                "maps_to": "DeltaK/q_loc algebraic m channel",
            }
        ),
        nonclaim(
            {
                "leakage_id": "DLP2735_4_Qalg_feed",
                "quantity": "Q_alg",
                "formula": "Q_alg receives no-cancellation sum of R_m, R_L, volume leakage, and Delta_grad_m source terms before CDB/memory/projection pieces.",
                "status": "QLOC_FEED_SYMBOLIC_ONLY",
                "missing_inputs": "A_ref;Delta_grad_m;q_loc projection;CDB/memory residuals",
                "maps_to": "1372 Q_norm decomposition and future PPN/R10 lanes",
            }
        ),
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BLK2735_0_Jeff", "J_eff", "PRIMARY_SOURCE_BLOCKER", "controls exact no-hair and N_lock", "derive J_eff=0 from parent source silence or produce H^-1 norm"),
        ("BLK2735_1_Bm", "B_m", "PRIMARY_BOUNDARY_BLOCKER", "inner boundary/history flux can support nonzero u", "derive no-flux/boundary primitive silence or produce finite boundary norm"),
        ("BLK2735_2_domain", "domain/zero-mode/C_emb", "SECONDARY_AFTER_SOURCE_BOUNDARY", "needed to convert energy bound to Delta_m", "source domain/collar and Poincare/Sobolev constant"),
        ("BLK2735_3_operator", "D_m/M_scr^2", "SECONDARY_AFTER_DOMAIN", "needed for positive energy norm and no-hair", "source parent signs/gap or zero-mode-safe massless branch"),
        ("BLK2735_4_potential", "V2_max/V3_max", "AFTER_LOCK_AMPLITUDE", "needed once Delta_m exists", "source potential curvature/remainder bounds"),
        ("BLK2735_5_Kmetric_projection", "C_sign/L_min/M_m/M_L/projection", "PARALLEL_OR_LATER", "needed for scores but premature before N_lock", "same-frame Kmetric and observable projection normalization"),
    ]
    return [
        nonclaim(
            {
                "blocker_id": row_id,
                "symbol": symbol,
                "priority": priority,
                "why_it_matters": why,
                "next_action": action,
            }
        )
        for row_id, symbol, priority, why, action in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "decision_id": "DEC2735_0_source_root_status",
                "decision": "treat stationary source-root/double-zero as a strong conditional theorem target",
                "because": "the algebra derives F_vac(m_*)=F'_vac(m_*)=0 without requiring M_L=0",
                "effect": "do not re-run Lcg fixed-scale proof unless new parent signature appears",
            }
        ),
        nonclaim(
            {
                "decision_id": "DEC2735_1_lock_status",
                "decision": "do not claim exact local lock",
                "because": "J_eff, B_m, domain/zero-mode, and operator signs remain unsigned",
                "effect": "carry finite Delta_m law instead of pretending u=0",
            }
        ),
        nonclaim(
            {
                "decision_id": "DEC2735_2_best_next",
                "decision": "attack J_eff and B_m first",
                "because": "they decide both exact no-hair and the finite leakage norm N_lock",
                "effect": "next checkpoint should prove source/boundary silence or stage finite N_lock source rows",
            }
        ),
    ]


def gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("GATE2735_0_parent_V_live", "parent V(m) and source-root are live-signed", False, "current source-root law is conditional"),
        ("GATE2735_1_exact_lock", "Delta_m=0 exact local no-hair", False, "J_eff/B_m/operator/domain premises unsigned"),
        ("GATE2735_2_finite_Delta_m_score", "finite Delta_m bound can score", False, "N_lock and C_emb are missing"),
        ("GATE2735_3_double_zero_promoted", "algebraic double-zero can be promoted", False, "needs exact lock or scored leakage"),
        ("GATE2735_4_q_loc_zero", "q_loc^nu=0 follows", False, "hidden kernels, memory stress, projection, and finite lock remain open"),
        ("GATE2735_5_local_GR_or_test_claim", "local GR/Newton/PPN/R10 pass follows", False, "only symbolic nonclaim bounds exist"),
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
        for gate_id, claim, passed, reason in gates
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2735_0_selected",
                "status": "selected_primary",
                "target_doc": "2736-Y5-R2FR-Jeff-Bm-source-boundary-silence-or-finite-Nlock-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Jeff_Bm_source_boundary_silence_or_finite_Nlock_row_under_AX1090_2736.py",
                "mission": "derive J_eff=0 and B_m=0 for exact local lock, or construct finite source-backed N_lock rows feeding Delta_m",
                "acceptance": "one of: source silence theorem; boundary/no-flux theorem; finite dual/boundary norm row; or explicit blocker ledger",
                "forbidden": "claiming Delta_m=0 without J_eff/B_m; scoring local tests from symbolic N_lock; editing formalization-workbench; GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "copy_id": "BR2735_0_Delta_m_bound",
                "source_table": rel(OUTPUTS["lock"]),
                "copy_path": rel(BRANCH_OUTPUTS["delta_m"]),
                "purpose": "local-bound nonclaim Delta_m/energy-lock amplitude law",
                "exists": BRANCH_OUTPUTS["delta_m"].exists(),
            }
        ),
        nonclaim(
            {
                "copy_id": "BR2735_1_reopen",
                "source_table": rel(OUTPUTS["root"]),
                "copy_path": rel(BRANCH_OUTPUTS["reopen"]),
                "purpose": "source-weight conditions required to promote stationary source-root lock",
                "exists": BRANCH_OUTPUTS["reopen"].exists(),
            }
        ),
        nonclaim(
            {
                "copy_id": "BR2735_2_next_queue",
                "source_table": rel(OUTPUTS["next"]),
                "copy_path": rel(BRANCH_OUTPUTS["next_queue"]),
                "purpose": "RAB acquisition queue for J_eff/B_m source-boundary target",
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
    root: list[dict[str, Any]],
    lock: list[dict[str, Any]],
    leakage: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    root_ok = any(row["law_id"] == "SSR2735_2_double_zero" for row in root) and all(row["claim_allowed"] is False for row in root)
    lock_ok = any(row["lock_id"] == "LOCK2735_3_field_amplitude_bound" for row in lock) and all(row["valid_for_claim"] is False for row in lock)
    leakage_ok = any(row["leakage_id"] == "DLP2735_2_ML_residual" for row in leakage) and any(row["leakage_id"] == "DLP2735_3_Mm_residual" for row in leakage)
    priority_ok = blockers[0]["symbol"] == "J_eff" and blockers[1]["symbol"] == "B_m"
    gates_false = all(row["gate_passed"] is False and row["claim_allowed"] is False for row in gates)
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
        {"validation_id": "VAL2735_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2735_1_source_root_law", "passed": root_ok, "detail": "stationary source-root/double-zero law is written as conditional nonclaim theorem", "timestamp_utc": ts()},
        {"validation_id": "VAL2735_2_lock_amplitude_law", "passed": lock_ok, "detail": "Delta_m <= C_emb N_lock amplitude interface exists and remains nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2735_3_leakage_propagation", "passed": leakage_ok, "detail": "F/Fprime leakage propagates to both M_L and M_m residual rows", "timestamp_utc": ts()},
        {"validation_id": "VAL2735_4_primary_blockers", "passed": priority_ok, "detail": "J_eff and B_m are the first blockers", "timestamp_utc": ts()},
        {"validation_id": "VAL2735_5_claim_gates_false", "passed": gates_false, "detail": "no exact lock, q_loc-zero, local-GR, PPN, R10, or public claim is allowed", "timestamp_utc": ts()},
        {"validation_id": "VAL2735_6_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2735_7_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2735_8_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2735_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2735 derives the conditional stationary-root/local-lock amplitude law, keeps claims blocked, and selects J_eff/B_m source-boundary work next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2735 - Y5 R2/f(R): Stationary Source Root Local Lock Or Finite Delta-m Bound Under AX1090

Status: `Y5_R2FR_2735_stationary_root_lock_amplitude_law_selects_Jeff_Bm_next_nonclaim`

## Private Verdict

2735 gets the next piece into a usable theorem shape.

If the parent local source really is a stable potential `V(m)` and the source entering `Gamma_eff` is the vacuum-subtracted quantity `F_vac(m)=V(m)-V(m_*)`, then:

`F_vac(m_*)=0`, `F_vac'(m_*)=0`, and `F_vac(m_*+u)=1/2 V''(m_*)u^2+O(u^3)`.

That is the right route. It kills the `M_L` coefficient without pretending `L_cg` is fixed, and it kills the `M_m` coefficient without requiring `M_m=0`. But it only matters physically if the local exterior actually locks to `u=m-m_*`.

The lock law is now explicit:

`E_m(u)^2=<u,J_eff>+B_m`, so exact lock needs `J_eff=0` and `B_m=0`; finite lock needs `E_m(u)<=N_lock` and `Delta_m<=C_emb N_lock`.

No local-GR, Newton, PPN, R10, WEP, clock, orbital, `q_loc=0`, exact lock, or public claim follows from this checkpoint. The next target is source/boundary hair: `J_eff` and `B_m`.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Stationary Source Root Law

{markdown_table(data["root"], ["law_id", "object", "formula", "status", "missing_to_promote", "effect", "valid_for_claim"])}

## Local Lock Amplitude Law

{markdown_table(data["lock"], ["lock_id", "quantity", "law", "status", "missing_inputs", "consequence", "valid_for_claim"])}

## Double-Zero Leakage Propagation

{markdown_table(data["leakage"], ["leakage_id", "quantity", "formula", "status", "missing_inputs", "maps_to", "valid_for_claim"])}

## Locking Blocker Priority

{markdown_table(data["blockers"], ["blocker_id", "symbol", "priority", "why_it_matters", "next_action", "valid_for_claim"])}

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

This is one of those “not glamorous, but very real” steps. The double-zero route is not fantasy math; the algebra is good. The hard physics is whether ordinary local systems actually sit on the root or leak away from it. The source and boundary terms are the next pair of gremlins to put in a jar.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    root = root_rows()
    lock = lock_rows()
    leakage = leakage_rows()
    blockers = blocker_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["root"], root)
    write_csv(OUTPUTS["lock"], lock)
    write_csv(OUTPUTS["leakage"], leakage)
    write_csv(OUTPUTS["blockers"], blockers)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["delta_m"], lock)
    write_csv(BRANCH_OUTPUTS["reopen"], root)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, root, lock, leakage, blockers, gates)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "root": root,
        "lock": lock,
        "leakage": leakage,
        "blockers": blockers,
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
        raise SystemExit(f"2735 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
