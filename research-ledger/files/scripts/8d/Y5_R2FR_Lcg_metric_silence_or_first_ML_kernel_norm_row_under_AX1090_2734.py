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

DOC = ROOT / "2734-Y5-R2FR-Lcg-metric-silence-or-first-ML-kernel-norm-row-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2734_SOURCE_REGISTER.csv",
    "silence": RESIDUALS / "P8_Y5_R2FR_2734_LCG_METRIC_SILENCE_AUDIT.csv",
    "ml_bound": RESIDUALS / "P8_Y5_R2FR_2734_FIRST_ML_KERNEL_NORM_ROW.csv",
    "inputs": RESIDUALS / "P8_Y5_R2FR_2734_ML_BOUND_INPUT_SCHEMA.csv",
    "root_lock": RESIDUALS / "P8_Y5_R2FR_2734_SOURCE_ROOT_LOCK_COMPARISON.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2734_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2734_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2734_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2734_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2734_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ml_bound": LOCAL_BOUNDS / "ML_kernel_norm_bound_2734_NONCLAIM.csv",
    "reopen": SOURCE_WEIGHT / "Lcg_metric_silence_reopen_conditions_2734_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2734_STATIONARY_SOURCE_ROOT_LOCK_OR_FINITE_DELTAM_NEXT.csv",
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


def path_text(path: Path) -> str:
    return rel(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2734_0_2733_doc",
            "description": "2733 selects L_cg/M_L as the next kernel target after q_loc/DeltaK split.",
            "source_path": "2733-Y5-R2FR-Khat-Kmetric-DeltaK00-amplitude-response-or-first-q_loc-residual-bound-under-AX1090.md",
            "required_needles": "NEXT2733_0_selected;RES2733_3_ML;QB2733_0_vector_envelope",
        },
        {
            "source_id": "SRC2734_1_2733_next",
            "description": "machine-readable 2734 handoff.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2733_NEXT_TARGET.csv",
            "required_needles": "NEXT2733_0_selected",
        },
        {
            "source_id": "SRC2734_2_2733_residuals",
            "description": "retained residual row naming E_M_Lcg as primary next residual.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2733_RETAINED_RESIDUAL_ROWS.csv",
            "required_needles": "RES2733_3_ML;E_M_Lcg",
        },
        {
            "source_id": "SRC2734_3_1289_derivative",
            "description": "first derivative chain formula for Gamma_eff=L_cg^-2 F(m).",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "required_needles": "KDR1289_0_Gamma_m_L_chain_kernel_00;M_L",
        },
        {
            "source_id": "SRC2734_4_1368_kernel_hunt",
            "description": "m/Lcg parent metric-response kernel hunt.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv",
            "required_needles": "KERN1368_3_Lcg_fixed_scale_branch;KERN1368_4_Lcg_metric_composite_branch",
        },
        {
            "source_id": "SRC2734_5_1370_fixed_l0",
            "description": "fixed L0 covariance-admissible closure contract and M_L=0 algebra.",
            "source_path": "1370-Y5-R10-RAB-parent-Lcg-contract-or-q_loc-weak-field-response-coefficient.md",
            "required_needles": "LCC1370_4_metric_silence_result;LCC1370_5_corpus_signature_verdict",
        },
        {
            "source_id": "SRC2734_6_1371_double_zero",
            "description": "fixed-L0 double-zero action branch plus residual ledger.",
            "source_path": "1371-Y5-R10-RAB-fixed-Lcg-parent-action-insertion-or-Cqgamma-norm-bound.md",
            "required_needles": "PAI1371_3_first_variation_result;PAI1371_4_gradient_source_after_double_zero;LRZ1371_2_L_chain",
        },
        {
            "source_id": "SRC2734_7_1532_lcg_audit",
            "description": "Lcg ownership audit preferring source-root/double-zero over bare fixed-scale promotion.",
            "source_path": "1532-Y5-Lcg-parent-ownership-and-fixed-scale-silence-audit.md",
            "required_needles": "LCG1532_3_F_root_route;LCG1532_4_double_zero_route;LCG1532_6_numeric_bound_route;DEC1532_1_best_route",
        },
        {
            "source_id": "SRC2734_8_1531_kernel_audit",
            "description": "Kmetric kernel norm audit naming M_L missing parent ownership.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1531_KMETRIC_KERNEL_NORM_SOURCE_AUDIT.csv",
            "required_needles": "KNA1531_5_M_L;MISSING_PARENT_OWNERSHIP",
        },
        {
            "source_id": "SRC2734_9_1978_ml_inputs",
            "description": "existing derivative-envelope input schema showing source values remain absent.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1978_ML_DERIVATIVE_ENVELOPE_INPUTS.csv",
            "required_needles": "MLE1978_5_mL_derivative;FORMULA_READY_VALUES_MISSING",
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


def silence_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "audit_id": "LCGMS2734_0_exact_channel",
                "target": "L_cg algebraic metric response in DeltaK/q_loc",
                "statement": "For Gamma_eff=L_cg^-2 F(m), the L_cg chain contribution is R_L^{mu nu}:=-2 C_sign L_cg^-3 F(m) M_L^{mu nu}.",
                "status": "DERIVED_CHANNEL_IDENTITY",
                "proof_or_blocker": "direct variation of L_cg^-2; this is an identity, not a zero theorem",
                "effect": "M_L only matters through a coefficient F(m) and the local scale factor L_cg^-3",
            }
        ),
        nonclaim(
            {
                "audit_id": "LCGMS2734_1_fixed_L0_silence",
                "target": "M_L^{mu nu}",
                "statement": "If the parent action declares L_cg=L0 as a positive fixed scalar parameter held fixed under Hilbert variation, then M_L^{mu nu}=delta_g L0=0.",
                "status": "EXACT_UNDER_CLOSURE_CONTRACT_NOT_LIVE",
                "proof_or_blocker": "1370/1371 establish the algebra; current corpus still does not parent-sign fixed L0 as the live theory definition",
                "effect": "sufficient but too closure-looking to promote as a derived local-GR theorem",
            }
        ),
        nonclaim(
            {
                "audit_id": "LCGMS2734_2_quotient_owned_silence",
                "target": "M_L^{mu nu}",
                "statement": "If L_cg=Lbar(q(Phi),theta) and q, theta descend metric-silently in the same branch, then delta_g L_cg=0.",
                "status": "COVARIANT_ROUTE_UNSIGNED",
                "proof_or_blocker": "requires parent quotient map, theta ownership, and metric-silent descent theorem not present in the current source chain",
                "effect": "promising route if future parent action supplies ownership, but not usable now",
            }
        ),
        nonclaim(
            {
                "audit_id": "LCGMS2734_3_source_root_coefficient_kill",
                "target": "R_L^{mu nu}",
                "statement": "If the local vacuum is locked to F(m_*)=0, then R_L^{mu nu}=0 at m=m_* even if M_L^{mu nu} is not known.",
                "status": "BEST_ALGEBRAIC_ROUTE_UNSIGNED",
                "proof_or_blocker": "coefficient kill is exact, but it requires parent-signed source root, same-branch lock, and no fitted per-system root",
                "effect": "less scrutinized than declaring L_cg fixed because it deletes the L_cg coefficient rather than assuming the kernel vanishes",
            }
        ),
        nonclaim(
            {
                "audit_id": "LCGMS2734_4_metric_composite_counterbranch",
                "target": "M_L^{mu nu}",
                "statement": "If L_cg is a proper length, curvature scale, density scale, domain support, projector collar, or source-dependent readout, M_L generally survives.",
                "status": "COUNTERBRANCH_RETAINED",
                "proof_or_blocker": "no parent definition excludes these branches in the current live corpus",
                "effect": "no L_cg metric-silence claim; finite M_L bound row must remain available",
            }
        ),
        nonclaim(
            {
                "audit_id": "LCGMS2734_5_verdict",
                "target": "Z_Lcg or Z_ML",
                "statement": "Do not claim L_cg metric silence. Use source-root/double-zero as the preferred derivation route, and retain finite M_L bound inputs as fallback.",
                "status": "ZERO_NOT_CLAIMED_ROUTE_NARROWED",
                "proof_or_blocker": "fixed L0 and quotient-owned routes are clean but unsigned; source-root route is exact but still needs parent lock",
                "effect": "move from trying to prove M_L=0 directly to proving F(m_*)=0 plus local lock, or bound the finite residual",
            }
        ),
    ]


def ml_bound_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "bound_id": "MLB2734_0_generic_retained_ML",
                "quantity": "||R_L||_D",
                "formula": "||R_L|| <= 2 |C_sign| L_min^-3 F_bar M_L_bar",
                "assumptions": "L_cg>=L_min>0, |F(m)|<=F_bar, ||M_L||<=M_L_bar on D_loc",
                "missing_inputs": "C_sign;L_min;F_bar;M_L_bar;domain norm;units/index convention",
                "status": "FIRST_SOURCE_READY_SYMBOLIC_ROW_NOT_NUMERIC",
            }
        ),
        nonclaim(
            {
                "bound_id": "MLB2734_1_root_only_displacement",
                "quantity": "||R_L||_D near F(m_*)=0",
                "formula": "||R_L|| <= 2 |C_sign| L_min^-3 (F1_bar Delta_m + 1/2 F2_bar Delta_m^2) M_L_bar",
                "assumptions": "F(m_*)=0, |m-m_*|<=Delta_m, |F'|<=F1_bar, |F''|<=F2_bar",
                "missing_inputs": "parent source root;Delta_m;F1_bar;F2_bar;M_L_bar;L_min",
                "status": "ROOT_ROUTE_BOUND_SCHEMA",
            }
        ),
        nonclaim(
            {
                "bound_id": "MLB2734_2_double_zero_displacement",
                "quantity": "||R_L||_D near F(m_*)=F'(m_*)=0",
                "formula": "||R_L|| <= |C_sign| L_min^-3 F2_bar Delta_m^2 M_L_bar + O(Delta_m^3)",
                "assumptions": "same-branch double zero, |m-m_*|<=Delta_m, bounded second derivative",
                "missing_inputs": "parent stationary root;Delta_m amplitude law;F2_bar;M_L_bar;transition/support theorem",
                "status": "BEST_BOUND_IF_LOCK_NOT_EXACT",
            }
        ),
        nonclaim(
            {
                "bound_id": "MLB2734_3_exact_lock_coefficient_zero",
                "quantity": "R_L^{mu nu}",
                "formula": "R_L^{mu nu}=0 at m=m_* if F(m_*)=0, regardless of finite M_L^{mu nu}",
                "assumptions": "exact local lock to parent source root and no off-root transition support in the local test domain",
                "missing_inputs": "parent root theorem;local lock/no-hair theorem;boundary collar exclusion",
                "status": "EXACT_ZERO_CONDITIONAL_NOT_CLAIMED",
            }
        ),
        nonclaim(
            {
                "bound_id": "MLB2734_4_fixed_L0_kernel_zero",
                "quantity": "R_L^{mu nu}",
                "formula": "R_L^{mu nu}=0 if M_L^{mu nu}=0 from fixed L0",
                "assumptions": "parent action signs L_cg=L0 as fixed scalar parameter",
                "missing_inputs": "live parent signature and notation split from readout lengths",
                "status": "CLOSURE_ZERO_NOT_PROMOTED",
            }
        ),
    ]


def input_rows() -> list[dict[str, Any]]:
    rows = [
        ("IN2734_0_C_sign", "C_sign", "Hilbert-stress sign/normalization for R_L", "MISSING_CONVENTION_LOCK", "dimensionless/sign"),
        ("IN2734_1_L_min", "L_min", "positive lower bound on L_cg across D_loc", "MISSING_PARENT_SCALE_RANGE", "length"),
        ("IN2734_2_F_bar", "F_bar", "generic bound on |F(m)|", "MISSING_FUNCTION_BOUND", "same units as Gamma_eff L_cg^2"),
        ("IN2734_3_F1_bar", "F1_bar", "bound on |F'(m)| near m_* for root-only branch", "MISSING_FUNCTION_BOUND", "F units per m"),
        ("IN2734_4_F2_bar", "F2_bar", "bound on |F''(m)| near m_* for double-zero branch", "MISSING_FUNCTION_BOUND", "F units per m^2"),
        ("IN2734_5_Delta_m", "Delta_m", "local amplitude |m-m_*| on D_loc", "MISSING_LOCAL_LOCK_AMPLITUDE", "m units"),
        ("IN2734_6_M_L_bar", "M_L_bar", "operator/domain norm bound on delta L_cg/delta g", "MISSING_ML_NORM", "length per metric variation"),
        ("IN2734_7_D_loc", "D_loc", "local test domain/collar excluding transitions if exact lock is asserted", "MISSING_DOMAIN_CERTIFICATE", "domain"),
        ("IN2734_8_units_index", "units/index convention", "same index, density, and norm convention as DeltaK/q_loc", "MISSING_UNITS_INDEX_LOCK", "ledger"),
    ]
    return [
        nonclaim(
            {
                "input_id": row_id,
                "symbol": symbol,
                "role": role,
                "status": status,
                "units_or_convention": units,
                "source_status": "not source-backed in current row",
            }
        )
        for row_id, symbol, role, status, units in rows
    ]


def root_lock_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "route_id": "RLC2734_0_direct_Lcg_silence",
                "route": "prove M_L=0",
                "scrutiny": "HIGH",
                "why": "reviewers will ask why a coarse-graining length is not a metric/domain readout",
                "current_result": "mathematically exact under fixed L0 but not live-parent signed",
                "next_requirement": "parent action explicitly owns L0 or quotient-silent Lbar",
            }
        ),
        nonclaim(
            {
                "route_id": "RLC2734_1_source_root_kill",
                "route": "prove F(m_*)=0 and local lock",
                "scrutiny": "LOWER_IF_PARENT_DERIVED",
                "why": "it kills the coefficient of M_L rather than declaring the kernel absent",
                "current_result": "exact algebraic deletion of R_L at the locked root, still unsigned",
                "next_requirement": "derive parent stationary source root and Delta_m amplitude/transition bound",
            }
        ),
        nonclaim(
            {
                "route_id": "RLC2734_2_finite_bound",
                "route": "retain finite M_L bound",
                "scrutiny": "ACCEPTABLE_NONCLAIM_FALLBACK",
                "why": "it does not require a zero theorem, but needs source-backed constants",
                "current_result": "schema ready, no numeric/scored row",
                "next_requirement": "source L_min, F bounds, M_L norm, domain and units",
            }
        ),
        nonclaim(
            {
                "route_id": "RLC2734_3_do_not_repeat",
                "route": "rerun bare fixed-L0 proof",
                "scrutiny": "CIRCLING_RISK",
                "why": "1370/1371 already did the algebra and blocked promotion",
                "current_result": "not selected unless new parent signature appears",
                "next_requirement": "new source row explicitly adopting L0",
            }
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "decision_id": "DEC2734_0_no_Lcg_zero_claim",
                "decision": "do not claim L_cg metric silence",
                "because": "fixed-L0 and quotient-owned routes are exact only under unsigned parent clauses",
                "effect": "Z_Lcg=false and M_L remains a retained residual unless coefficient-killed or bounded",
            }
        ),
        nonclaim(
            {
                "decision_id": "DEC2734_1_best_next_derivation",
                "decision": "prefer source-root/local-lock derivation over bare Lcg ownership",
                "because": "F(m_*)=0 deletes the M_L coefficient and also aligns with the volume-stress double-zero route",
                "effect": "next target should prove stationary source root plus Delta_m/local-lock amplitude law",
            }
        ),
        nonclaim(
            {
                "decision_id": "DEC2734_2_bound_fallback_ready",
                "decision": "stage first M_L norm-bound row as fallback",
                "because": "if lock is finite rather than exact, the residual is quadratic under double-zero and can be bounded",
                "effect": "future local tests can refuse/score only when all constants are source-backed",
            }
        ),
    ]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2734_0_Lcg_silence_live", "L_cg is metric-silent in the live parent theory", False, "parent ownership is unsigned"),
        ("GATE2734_1_ML_zero_live", "M_L can be set to zero in local-GR scoring", False, "fixed-L0 proof remains closure-only"),
        ("GATE2734_2_source_root_exact", "F(m_*)=0 local source root is parent-signed", False, "root/local lock not yet derived"),
        ("GATE2734_3_finite_ML_score", "finite M_L bound row can score a local test", False, "numeric/source-backed constants are missing"),
        ("GATE2734_4_q_loc_zero", "q_loc^nu=0 follows", False, "Ward, DeltaK, cdb, memory stress, and source lock remain open"),
        ("GATE2734_5_local_GR_or_PPN_claim", "local GR/Newton/PPN pass follows", False, "only a nonclaim symbolic residual row exists"),
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
                "next_id": "NEXT2734_0_selected",
                "status": "selected_primary",
                "target_doc": "2735-Y5-R2FR-stationary-source-root-local-lock-or-finite-Delta-m-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_stationary_source_root_local_lock_or_finite_Delta_m_bound_under_AX1090_2735.py",
                "mission": "derive the parent stationary source root F(m_*)=0/F'(m_*)=0 and a local lock amplitude law Delta_m, or route to finite M_L bound inputs",
                "acceptance": "one of: parent-signed source root; exact local lock/no-hair branch; finite Delta_m/F2/M_L bound row; or explicit blocker ledger",
                "forbidden": "claiming fixed Lcg silence from closure text; scoring PPN/R10 from symbolic placeholders; editing formalization-workbench; GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "copy_id": "BR2734_0_ML_bound",
                "source_table": path_text(OUTPUTS["ml_bound"]),
                "copy_path": path_text(BRANCH_OUTPUTS["ml_bound"]),
                "purpose": "local-bound nonclaim fallback row for finite M_L residuals",
                "exists": BRANCH_OUTPUTS["ml_bound"].exists(),
            }
        ),
        nonclaim(
            {
                "copy_id": "BR2734_1_reopen",
                "source_table": path_text(OUTPUTS["silence"]),
                "copy_path": path_text(BRANCH_OUTPUTS["reopen"]),
                "purpose": "source-weight reopen conditions for Lcg metric-silence promotion",
                "exists": BRANCH_OUTPUTS["reopen"].exists(),
            }
        ),
        nonclaim(
            {
                "copy_id": "BR2734_2_next_queue",
                "source_table": path_text(OUTPUTS["next"]),
                "copy_path": path_text(BRANCH_OUTPUTS["next_queue"]),
                "purpose": "RAB acquisition queue for stationary source/root lock or finite Delta_m next step",
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
    silence: list[dict[str, Any]],
    ml_bound: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    root_lock: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    silence_ok = any(row["audit_id"] == "LCGMS2734_5_verdict" for row in silence) and all(row["claim_allowed"] is False for row in silence)
    bound_ok = any(row["bound_id"] == "MLB2734_2_double_zero_displacement" for row in ml_bound) and all(row["valid_for_claim"] is False for row in ml_bound)
    input_ok = all(row["valid_for_claim"] is False and str(row["status"]).startswith("MISSING") for row in inputs)
    route_ok = any(row["route_id"] == "RLC2734_1_source_root_kill" for row in root_lock)
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
        {"validation_id": "VAL2734_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2734_1_silence_not_promoted", "passed": silence_ok, "detail": "Lcg metric-silence theorem is narrowed but not claimed", "timestamp_utc": ts()},
        {"validation_id": "VAL2734_2_first_ML_bound_row", "passed": bound_ok, "detail": "generic/root/double-zero M_L bound rows exist and remain nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2734_3_inputs_missing_not_faked", "passed": input_ok, "detail": "all required M_L bound inputs remain marked missing rather than fabricated", "timestamp_utc": ts()},
        {"validation_id": "VAL2734_4_best_route_selected", "passed": route_ok, "detail": "source-root/local-lock route selected over repeating fixed-L0 proof", "timestamp_utc": ts()},
        {"validation_id": "VAL2734_5_claim_gates_false", "passed": gates_false, "detail": "no local-GR, PPN, R10, q_loc-zero, or M_L-zero claim is allowed", "timestamp_utc": ts()},
        {"validation_id": "VAL2734_6_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2734_7_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2734_8_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2734_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2734 rejects live Lcg metric-silence promotion, stages the first finite M_L norm row, and selects source-root/local-lock as the next derivation route",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2734 - Y5 R2/f(R): Lcg Metric Silence Or First ML Kernel Norm Row Under AX1090

Status: `Y5_R2FR_2734_Lcg_silence_rejected_as_live_first_ML_bound_row_and_source_root_next_nonclaim`

## Private Verdict

2734 does **not** promote `L_cg` metric silence. The fixed-`L0` theorem is algebraically clean, and the quotient-owned version is covariant-looking, but both are still parent-unsigned. Promoting either now would look like a closure axiom wearing a theorem jacket.

The useful leap is sharper: the `M_L` channel enters as

`R_L^{{mu nu}}=-2 C_sign L_cg^-3 F(m) M_L^{{mu nu}}`.

So the least-scrutiny route is not “declare `M_L=0`”; it is to derive a same-branch local source root `F(m_*)=0` and, ideally, `F'(m_*)=0`. That kills the coefficient of `M_L` at the locked local vacuum, and if the lock is finite rather than exact the residual becomes a bounded `Delta_m` problem.

No local-GR, Newton, PPN, R10, WEP, clock, orbital, `q_loc=0`, `DeltaK=0`, `M_L=0`, or public claim follows from this checkpoint.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Lcg Metric-Silence Audit

{markdown_table(data["silence"], ["audit_id", "target", "statement", "status", "proof_or_blocker", "effect", "valid_for_claim"])}

## First M_L Kernel Norm Row

{markdown_table(data["ml_bound"], ["bound_id", "quantity", "formula", "assumptions", "missing_inputs", "status", "valid_for_claim"])}

## M_L Bound Input Schema

{markdown_table(data["inputs"], ["input_id", "symbol", "role", "status", "units_or_convention", "source_status", "valid_for_claim"])}

## Source-Root / Lock Route Comparison

{markdown_table(data["root_lock"], ["route_id", "route", "scrutiny", "why", "current_result", "next_requirement", "valid_for_claim"])}

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

This is a decent little knife-fight win, not a knockout. We did not get permission to erase `L_cg` by saying “fixed scale, job done.” But we did identify the cleaner move: make the source vanish at the local vacuum so the whole `M_L` term is coefficient-killed. If that cannot be proved, we now have the first honest finite-bound row for the residual.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    silence = silence_rows()
    ml_bound = ml_bound_rows()
    inputs = input_rows()
    root_lock = root_lock_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["silence"], silence)
    write_csv(OUTPUTS["ml_bound"], ml_bound)
    write_csv(OUTPUTS["inputs"], inputs)
    write_csv(OUTPUTS["root_lock"], root_lock)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["ml_bound"], ml_bound)
    write_csv(BRANCH_OUTPUTS["reopen"], silence)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, silence, ml_bound, inputs, root_lock, gates)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "silence": silence,
        "ml_bound": ml_bound,
        "inputs": inputs,
        "root_lock": root_lock,
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
        raise SystemExit(f"2734 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
