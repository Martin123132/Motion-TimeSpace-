from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3392-Y5-R2FR-fixed-PPN-readout-parent-clause-or-projector-ell-scale-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3392_SOURCE_REGISTER.csv",
    "corpus_readout_audit": OUT / "P8_Y5_R2FR_3392_CORPUS_READOUT_AUDIT.csv",
    "parent_clause": OUT / "P8_Y5_R2FR_3392_FIXED_PPN_PARENT_CLAUSE_CANDIDATE.csv",
    "theorem": OUT / "P8_Y5_R2FR_3392_PROJECTOR_COMMUTATOR_THEOREM.csv",
    "signature": OUT / "P8_Y5_R2FR_3392_PARENT_SIGNATURE_VERDICT.csv",
    "finite_carry": OUT / "P8_Y5_R2FR_3392_FINITE_ELL_SCALE_CARRYFORWARD_NONCLAIM.csv",
    "obstruction": OUT / "P8_Y5_R2FR_3392_REMAINING_CHANNEL_OBSTRUCTION_MAP.csv",
    "runner": OUT / "P8_Y5_R2FR_3392_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3392_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3392_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3392_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3392_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3392_00_3391_doc", ROOT / "3391-Y5-R2FR-Cassini-scale-source-pack-and-projector-constancy-theorem-under-AX1090.md", "3391 handoff"),
    ("SRC3392_01_3391_next", OUT / "P8_Y5_R2FR_3391_NEXT_TARGET.csv", "3391 next target"),
    ("SRC3392_02_3391_theorem", OUT / "P8_Y5_R2FR_3391_PPN_PROJECTOR_CONSTANCY_THEOREM.csv", "3391 conditional projector theorem"),
    ("SRC3392_03_3391_branch", OUT / "P8_Y5_R2FR_3391_PROJECTOR_BRANCH_COMPARISON.csv", "3391 exact/finite branch comparison"),
    ("SRC3392_04_3391_geometry", OUT / "P8_Y5_R2FR_3391_CASSINI_GEOMETRY_SOURCE_BACKED.csv", "source-backed Cassini geometry"),
    ("SRC3392_05_core_fundamental_action", REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md", "parent fundamental action"),
    ("SRC3392_06_core_motion_action", REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md", "parent motion action"),
    ("SRC3392_07_core_gravity", REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md", "parent gravity formulation"),
    ("SRC3392_08_observer_map", ROOT / "10-observer-map-symplectic-contract.md", "observer/readout contract context"),
    ("SRC3392_09_motion_load_local", ROOT / "02-motion-load-local-GR-reduction.md", "local GR reduction context"),
    ("SRC3392_10_kernel_commutator", OUT / "P8_Y5_R2FR_3387_KERNEL_PROJECTOR_COMMUTATOR_LAW.csv", "kernel projector commutator law"),
    ("SRC3392_11_local_ppn_framework", FW / "59-local-ppn-branch-framework.md", "read-only local PPN framework"),
    ("SRC3392_12_local_tensor_ansatz", FW / "61-local-ppn-tensor-ansatz.md", "read-only local tensor ansatz"),
]

AUDIT_PATTERNS = {
    "metric_from_smoothed_covariance": [r"smoothed covariance", r"coarse-grain", r"smooth"],
    "standard_matter_EH_action": [r"Einstein", r"L_matter", r"matter coupling", r"GR is the"],
    "PPN_gamma_readout": [r"PPN", r"gamma", r"beta"],
    "fixed_readout_language": [r"fixed readout", r"fixed observed frame", r"fixed.*projector", r"observable projector"],
    "gauge_or_frame_language": [r"gauge", r"tetrad", r"Fermi", r"frame"],
    "adaptive_ray_risk": [r"adaptive", r"ray", r"impact parameter", r"line of sight"],
    "commutator_language": [r"\[P,S\]", r"commutator", r"nabla P", r"∇P"],
    "explicit_P_PPN_signature": [r"P_PPN", r"P\\_PPN", r"PPN projector"],
}


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def to_float(value: str, default: float = float("nan")) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "read_or_write": "read_only_context" if str(path).startswith(str(FW)) else "post_checkpoint_or_core_source",
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def source_lines(path: Path) -> list[tuple[int, str]]:
    if not path.exists():
        return []
    if path.suffix.lower() == ".csv":
        rows = read_csv_rows(path)
        lines: list[tuple[int, str]] = []
        for index, row in enumerate(rows, start=2):
            lines.append((index, "; ".join(f"{key}={value}" for key, value in row.items())))
        return lines
    return list(enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1))


def corpus_readout_audit_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    hit_counts = {key: 0 for key in AUDIT_PATTERNS}
    for source_id, path, role in LOCAL_SOURCES:
        for line_number, line in source_lines(path):
            compact = " ".join(line.strip().split())
            if not compact:
                continue
            for category, patterns in AUDIT_PATTERNS.items():
                if hit_counts[category] >= 10:
                    continue
                if any(re.search(pattern, compact, flags=re.IGNORECASE) for pattern in patterns):
                    rows.append(
                        {
                            "audit_id": f"CRA3392_{category}_{hit_counts[category]}",
                            "category": category,
                            "source_id": source_id,
                            "source_path": str(path),
                            "source_role": role,
                            "line_number": str(line_number),
                            "snippet": compact[:420],
                            "supports_fixed_PPN_clause": "compatible" if category in {"metric_from_smoothed_covariance", "standard_matter_EH_action", "fixed_readout_language", "gauge_or_frame_language"} else "context_only",
                            "is_parent_signature": "false",
                            "valid_for_claim": "false",
                        }
                    )
                    hit_counts[category] += 1
                    break
    for category, count in hit_counts.items():
        if count == 0:
            rows.append(
                {
                    "audit_id": f"CRA3392_{category}_NO_HIT",
                    "category": category,
                    "source_id": "NO_HIT",
                    "source_path": "",
                    "source_role": "",
                    "line_number": "",
                    "snippet": f"No direct hit for {category}.",
                    "supports_fixed_PPN_clause": "no_direct_evidence",
                    "is_parent_signature": "false",
                    "valid_for_claim": "false",
                }
            )
    return rows


def parent_clause_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PC3392_0_fixed_ppn_readout",
            "clause": "PPN observables are extracted by a fixed linear readout P_PPN from the coarse-grained metric perturbation in one chosen local PPN/Fermi gauge patch.",
            "why_needed": "makes P_PPN a readout map rather than a dynamical x-dependent field",
            "adds_new_dynamics": "false",
            "adds_fit_parameter": "false",
            "parent_status": "CANDIDATE_NOT_YET_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PC3392_1_order_of_operations",
            "clause": "The scalar smoothing/coarse-graining S_ell acts on the metric/source fields before the fixed PPN observable coefficients are read out.",
            "why_needed": "prevents silently inserting an adaptive projector inside the smoothing kernel",
            "adds_new_dynamics": "false",
            "adds_fit_parameter": "false",
            "parent_status": "CANDIDATE_NOT_YET_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PC3392_2_no_adaptive_ray_projector",
            "clause": "Cassini impact-parameter/ray geometry belongs to the external observable model, not to a position-dependent parent projector P_PPN(x) inside S_ell.",
            "why_needed": "avoids the harsh adaptive-ray projector branch unless the parent theory explicitly chooses it",
            "adds_new_dynamics": "false",
            "adds_fit_parameter": "false",
            "parent_status": "CANDIDATE_NOT_YET_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PC3392_3_single_frame_patch",
            "clause": "The local tetrad/frame used for the PPN readout is fixed over the smoothing support by parallel transport to the chosen patch origin up to already-counted curvature corrections.",
            "why_needed": "separates true curvature response from gauge/readout drift",
            "adds_new_dynamics": "false",
            "adds_fit_parameter": "false",
            "parent_status": "CANDIDATE_NOT_YET_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "TH3392_0_commutator_identity",
            "statement": "[P_PPN,S_ell]f(x)=integral K_ell(x,y)[P_PPN(x)-P_PPN(y)]f(y)dV_y.",
            "proof_step": "subtract P_PPN(x) integral Kf and integral K P_PPN(y)f; collect the difference",
            "consequence": "all projector leakage is controlled by variation of P_PPN across the smoothing support",
            "status": "DERIVED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TH3392_1_exact_zero",
            "statement": "If P_PPN(x)=P_0 on support, then [P_PPN,S_ell]=0 exactly.",
            "proof_step": "the bracket P_PPN(x)-P_PPN(y) vanishes pointwise inside the integral",
            "consequence": "ell_s||nabla P||, ell_s^2||nabla^2P|| channels collapse to zero",
            "status": "DERIVED_CONDITIONAL_ON_PARENT_CLAUSE",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TH3392_2_fixed_readout_sufficient_condition",
            "statement": "A parent-fixed linear PPN observable readout in a single gauge/frame patch is sufficient for P_PPN(x)=P_0.",
            "proof_step": "linear readout coefficients are constants of the chosen observable map; spatial dependence belongs to h_{mu nu}, not to P_0",
            "consequence": "projector-gradient obstruction is removed without tuning ell_s",
            "status": "DERIVED_IF_PARENT_SIGNS_PC3392",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TH3392_3_finite_fallback",
            "statement": "If P_PPN varies, retain epsilon_projector <= C1 ell_s||nabla P|| + C2 ell_s^2||nabla^2P|| + moment + gauge.",
            "proof_step": "Taylor expand P(y) around x and bound the first/second kernel moments",
            "consequence": "carry 3391 ell_s ceilings until ell_s and constants are sourced",
            "status": "FINITE_BOUND_FALLBACK",
            "valid_for_claim": "false",
        },
    ]


def parent_signature_rows(audit_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    core_ids = {"SRC3392_05_core_fundamental_action", "SRC3392_06_core_motion_action", "SRC3392_07_core_gravity"}
    core_metric = any(row["source_id"] in core_ids and row["category"] == "metric_from_smoothed_covariance" for row in audit_rows)
    core_eh = any(row["source_id"] in core_ids and row["category"] == "standard_matter_EH_action" for row in audit_rows)
    explicit_ppn = any(row["source_id"] in core_ids and row["category"] == "explicit_P_PPN_signature" and row["source_id"] != "NO_HIT" for row in audit_rows)
    fixed_readout = any(row["source_id"] in core_ids and row["category"] == "fixed_readout_language" and row["source_id"] != "NO_HIT" for row in audit_rows)
    commutator = any(row["source_id"] in core_ids and row["category"] == "commutator_language" and row["source_id"] != "NO_HIT" for row in audit_rows)
    parent_signed = explicit_ppn and fixed_readout and commutator
    return [
        {
            "signature_id": "SIG3392_0_core_compatibility",
            "question": "Does the parent core make a fixed PPN readout plausible?",
            "result": "YES_COMPATIBLE" if core_metric and core_eh else "WEAK_COMPATIBILITY",
            "evidence": f"core_metric_smoothing={bool_text(core_metric)}; core_EH_matter={bool_text(core_eh)}",
            "claim_effect": "compatibility only; no exact-zero promotion",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG3392_1_explicit_parent_signature",
            "question": "Does the parent core explicitly sign P_PPN fixed readout and commutator zero?",
            "result": "NO_CURRENT_PARENT_SIGNATURE" if not parent_signed else "PARENT_SIGNED",
            "evidence": f"explicit_P_PPN={bool_text(explicit_ppn)}; fixed_readout={bool_text(fixed_readout)}; commutator={bool_text(commutator)}",
            "claim_effect": "projector exact zero remains conditional" if not parent_signed else "projector exact zero may promote after remaining channels",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG3392_2_candidate_clause_admissibility",
            "question": "Would adding PC3392 be a physics closure or just a readout convention?",
            "result": "ADMISSIBLE_READOUT_CONVENTION_NONCLAIM",
            "evidence": "PC3392 adds no dynamics and no fitted parameter; it selects how PPN observables are extracted from the already-smoothed metric",
            "claim_effect": "can be proposed as parent clause, but must be adopted before scoring",
            "valid_for_claim": "false",
        },
    ]


def finite_carry_rows() -> list[dict[str, str]]:
    branch_rows = read_csv_rows(OUT / "P8_Y5_R2FR_3391_PROJECTOR_BRANCH_COMPARISON.csv")
    branch_map = {row.get("branch_id", ""): row for row in branch_rows}
    geometry_rows = read_csv_rows(OUT / "P8_Y5_R2FR_3391_CASSINI_GEOMETRY_SOURCE_BACKED.csv")
    rows: list[dict[str, str]] = []
    for row in geometry_rows:
        rows.append(
            {
                "carry_id": f"FC3392_{row.get('source_row', '')}",
                "source_row": row.get("source_row", ""),
                "threshold_source": row.get("threshold_source", ""),
                "exact_fixed_readout_projector": "zero_if_PC3392_parent_signed",
                "curvature_projector_ell_s_ceiling_m": row.get("ell_s_max_from_curvature_projector_grad_C1eq1_m", ""),
                "adaptive_ray_projector_ell_s_ceiling_m": row.get("ell_s_max_from_adaptive_ray_projector_grad_C1eq1_m", ""),
                "boundary_collar_ell_s_ceiling_m": row.get("ell_s_max_from_boundary_m", ""),
                "branch_preference": "exact_fixed_readout_first; curvature finite second; adaptive ray only if parent forces it",
                "claim_status": "NONCLAIM_CARRYFORWARD",
                "valid_for_claim": "false",
            }
        )
    rows.append(
        {
            "carry_id": "FC3392_SUMMARY",
            "source_row": "strictest_branch_summary",
            "threshold_source": "3391_branch_comparison",
            "exact_fixed_readout_projector": branch_map.get("BR3391_0_exact_fixed_projector", {}).get("mathematical_result", ""),
            "curvature_projector_ell_s_ceiling_m": branch_map.get("BR3391_1_finite_curvature_projector", {}).get("strictest_ell_s_ceiling_m", ""),
            "adaptive_ray_projector_ell_s_ceiling_m": branch_map.get("BR3391_2_adaptive_ray_projector", {}).get("strictest_ell_s_ceiling_m", ""),
            "boundary_collar_ell_s_ceiling_m": branch_map.get("BR3391_3_boundary_collar", {}).get("strictest_ell_s_ceiling_m", ""),
            "branch_preference": "fixed readout is the only clean route that avoids a tiny ell_s demand",
            "claim_status": "NONCLAIM_SUMMARY",
            "valid_for_claim": "false",
        }
    )
    return rows


def obstruction_rows() -> list[dict[str, str]]:
    return [
        {
            "obstruction_id": "OBS3392_0_projector",
            "channel": "projector commutator",
            "current_state": "conditional exact-zero theorem exists; parent signature missing",
            "clean_close": "adopt PC3392 fixed PPN readout in parent framework",
            "finite_fallback": "carry curvature/adaptive ell_s ceilings",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3392_1_boundary_flux",
            "channel": "physical boundary flux/Poynting/reference/worldtube",
            "current_state": "not handled by projector theorem",
            "clean_close": "return to 3376 flux package and prove zero/no-through-flow in local Cassini domain",
            "finite_fallback": "absolute source-backed flux envelope below remaining boundary budget",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3392_2_kernel_moment",
            "channel": "kernel first moment/anisotropic moment",
            "current_state": "not closed",
            "clean_close": "choose normalized isotropic zero-moment kernel before scoring",
            "finite_fallback": "source epsilon_kernel_moment below quarter budget",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3392_3_gauge_readout",
            "channel": "gauge/readout drift",
            "current_state": "partly reduced by PC3392 but not fully closed",
            "clean_close": "single frame/gauge patch plus readout-after-smoothing clause",
            "finite_fallback": "source epsilon_gauge_readout below quarter budget",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    signature_map = {row["signature_id"]: row for row in rows_by_name["signature"]}
    summary = next(row for row in rows_by_name["finite_carry"] if row["carry_id"] == "FC3392_SUMMARY")
    return [
        {
            "run_id": "RUN3392_0_corpus_audit",
            "test": "parent readout corpus audit",
            "result": "PASS_AUDIT_EXECUTED_NONCLAIM",
            "detail": f"audit_rows={len(rows_by_name['corpus_readout_audit'])}; {signature_map['SIG3392_1_explicit_parent_signature']['result']}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3392_1_parent_clause",
            "test": "minimal fixed PPN parent clause candidate",
            "result": "PASS_CANDIDATE_CLAUSE_WRITTEN",
            "detail": "PC3392 adds no dynamics or fitted parameters, but is not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3392_2_commutator_theorem",
            "test": "projector commutator exact-zero theorem",
            "result": "PASS_DERIVED_CONDITIONAL",
            "detail": "constant P_PPN implies [P,S]=0 exactly",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3392_3_finite_carry",
            "test": "finite ell_s fallback carryforward",
            "result": "PASS_FINITE_CARRY_NONCLAIM",
            "detail": f"curvature ceiling={summary['curvature_projector_ell_s_ceiling_m']} m; adaptive ray ceiling={summary['adaptive_ray_projector_ell_s_ceiling_m']} m",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3392_4_firewall",
            "test": "prevent local PPN/local GR claim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "projector channel is sharpened, not promoted; flux/moment/gauge still block local-GR claim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool, rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    sig = {row["signature_id"]: row for row in rows_by_name["signature"]}
    parent_signed = sig["SIG3392_1_explicit_parent_signature"]["result"] == "PARENT_SIGNED"
    return [
        {
            "gate_id": "GATE3392_0_sources",
            "claim": "all 3392 local source files exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "local/core/read-only formalization context parsed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3392_1_parent_signature",
            "claim": "fixed P_PPN readout is already parent-signed",
            "gate_pass": bool_text(parent_signed),
            "reason": sig["SIG3392_1_explicit_parent_signature"]["evidence"],
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3392_2_candidate_clause",
            "claim": "candidate fixed readout clause is available",
            "gate_pass": "true",
            "reason": "PC3392 clauses written; they add no dynamics or fitted parameter",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3392_3_projector_exact_zero",
            "claim": "projector commutator may be scored as exact zero",
            "gate_pass": "false",
            "reason": "exact theorem is conditional and parent signature is absent in current corpus",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3392_4_finite_bound",
            "claim": "finite projector branch passes Cassini pressure",
            "gate_pass": "false",
            "reason": "ell_s and constants are not parent/source supplied",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3392_5_local_ppn",
            "claim": "local PPN/local-GR branch passes",
            "gate_pass": "false",
            "reason": "projector remains conditional; flux/moment/gauge channels remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    summary = next(row for row in rows_by_name["finite_carry"] if row["carry_id"] == "FC3392_SUMMARY")
    return [
        {
            "decision_id": "DEC3392_0_progress",
            "decision": "The projector problem is no longer vague: it is a parent-readout clause decision.",
            "because": "A fixed PPN readout gives an exact commutator zero; an adaptive or drifting readout forces small ell_s ceilings.",
            "next_action": "adopt or reject PC3392 explicitly in the parent framework before scoring",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3392_1_current_parent_status",
            "decision": "Current core corpus is compatible with PC3392 but does not explicitly sign it.",
            "because": "core action has smoothed metric/standard matter/EH language, but no explicit P_PPN fixed-readout/commutator clause.",
            "next_action": "keep exact projector zero as conditional, not a claim",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3392_2_fallback_pressure",
            "decision": "If PC3392 is rejected, local PPN survival demands finite smoothing-scale control.",
            "because": f"curvature branch carries ell_s <= {summary['curvature_projector_ell_s_ceiling_m']} m; adaptive ray branch carries ell_s <= {summary['adaptive_ray_projector_ell_s_ceiling_m']} m.",
            "next_action": "source ell_s or avoid adaptive-ray P by parent clause",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3392_3_best_next",
            "decision": "Next best move is closing the remaining non-projector channels.",
            "because": "Even with PC3392 adopted later, local-GR still needs boundary flux, moment and gauge/readout closure.",
            "next_action": "build 3393 boundary flux/moment/gauge closure pack",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3393-Y5-R2FR-boundary-flux-moment-gauge-closure-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3393_boundary_flux_moment_gauge_closure_pack.py",
            "objective": "close or bound the remaining Cassini local branch channels: physical boundary flux/Poynting/reference/worldtube, kernel first-moment/anisotropy, and gauge/readout drift",
            "why_next": "3392 reduces the projector channel to a parent clause/fallback, leaving flux, moment and gauge as the next blockers",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3394-Y5-R2FR-parent-readout-clause-integration-audit-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3394_parent_readout_clause_integration_audit.py",
            "objective": "if/when parent docs are allowed to be updated, integrate PC3392 and verify it does not conflict with cosmology, galaxy, EM, or quantum readouts",
            "why_next": "PC3392 is admissible but not parent-signed; integration should be separate from private nonclaim scoring",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3392*")
        if hit.name.startswith(("3392-Y5", "P8_Y5_R2FR_3392", "P8_Y5_BRR545_3392", "Y5_R2FR_3392"))
    ] if FW.exists() else []
    audit_categories = {row["category"] for row in rows_by_name["corpus_readout_audit"]}
    clause_ids = {row["clause_id"] for row in rows_by_name["parent_clause"]}
    theorem_statuses = {row["status"] for row in rows_by_name["theorem"]}
    signature_results = {row["result"] for row in rows_by_name["signature"]}
    finite_has_summary = any(row["carry_id"] == "FC3392_SUMMARY" for row in rows_by_name["finite_carry"])
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    checks = [
        ("VAL3392_0_sources_exist_parse", "all cited 3392 source paths exist and parse", source_ok, ""),
        ("VAL3392_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3392_2_corpus_audit", "corpus audit covers readout/projector categories", set(AUDIT_PATTERNS).issubset(audit_categories), f"categories={len(audit_categories)}"),
        ("VAL3392_3_parent_clause", "candidate fixed PPN parent clause is written", {"PC3392_0_fixed_ppn_readout", "PC3392_1_order_of_operations", "PC3392_2_no_adaptive_ray_projector", "PC3392_3_single_frame_patch"}.issubset(clause_ids), ""),
        ("VAL3392_4_theorem", "projector theorem covers identity, exact zero and finite fallback", {"DERIVED", "DERIVED_CONDITIONAL_ON_PARENT_CLAUSE", "DERIVED_IF_PARENT_SIGNS_PC3392", "FINITE_BOUND_FALLBACK"}.issubset(theorem_statuses), ""),
        ("VAL3392_5_signature_verdict", "signature verdict separates compatibility from parent signature", {"YES_COMPATIBLE", "NO_CURRENT_PARENT_SIGNATURE", "ADMISSIBLE_READOUT_CONVENTION_NONCLAIM"}.issubset(signature_results), ""),
        ("VAL3392_6_finite_carry", "finite ell-scale fallback carried forward", finite_has_summary and len(rows_by_name["finite_carry"]) >= 9, f"rows={len(rows_by_name['finite_carry'])}"),
        ("VAL3392_7_obstruction_map", "remaining flux/moment/gauge channels mapped", len(rows_by_name["obstruction"]) >= 4, f"rows={len(rows_by_name['obstruction'])}"),
        ("VAL3392_8_runner", "runner records audit, clause, theorem, finite carry and firewall", {"PASS_AUDIT_EXECUTED_NONCLAIM", "PASS_CANDIDATE_CLAUSE_WRITTEN", "PASS_DERIVED_CONDITIONAL", "PASS_FINITE_CARRY_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3392_9_gates", "gates block parent signature, exact projector, finite pass and local PPN claim", gate_map.get("GATE3392_2_candidate_clause") == "true" and gate_map.get("GATE3392_1_parent_signature") == "false" and gate_map.get("GATE3392_3_projector_exact_zero") == "false" and gate_map.get("GATE3392_5_local_ppn") == "false", ""),
        ("VAL3392_10_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3392_11_write_scope_outside_formalization", "no 3392 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
        ("VAL3392_12_next_target", "next target moves to boundary flux/moment/gauge closure pack", rows_by_name["next"][0]["target_id"].startswith("3393-Y5-R2FR-boundary-flux"), ""),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3392_13_overall", "3392 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    summary = next(row for row in rows_by_name["finite_carry"] if row["carry_id"] == "FC3392_SUMMARY")
    lines = [
        "# 3392 - Y5/R2FR fixed PPN readout parent clause or projector ell-scale bound under AX1090",
        "",
        "## Summary",
        "- 3392 audits the actual parent/readout corpus for the fixed `P_PPN` clause suggested by 3391.",
        "- Result: the parent core is compatible with fixed PPN readout, but it does not explicitly sign `P_PPN` as a fixed projector or sign `[P,S]=0`.",
        "- The exact theorem is now written cleanly: if `P_PPN(x)=P_0` on the smoothing support, then `[P_PPN,S_ell]=0` exactly.",
        "- The minimal parent clause `PC3392` is admissible because it adds no dynamics and no fitted parameter; it is an order-of-operations/readout convention.",
        f"- Until `PC3392` is parent-signed, finite fallback remains: curvature branch `ell_s <= {summary['curvature_projector_ell_s_ceiling_m']} m`; adaptive-ray branch `ell_s <= {summary['adaptive_ray_projector_ell_s_ceiling_m']} m`.",
        "- Therefore the projector channel is sharpened but not claimed closed; remaining blockers are boundary flux, kernel moment and gauge/readout drift.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Corpus Readout Audit",
        md_table(rows_by_name["corpus_readout_audit"]),
        "## Fixed PPN Parent Clause Candidate",
        md_table(rows_by_name["parent_clause"]),
        "## Projector Commutator Theorem",
        md_table(rows_by_name["theorem"]),
        "## Parent Signature Verdict",
        md_table(rows_by_name["signature"]),
        "## Finite Ell-Scale Carryforward",
        md_table(rows_by_name["finite_carry"]),
        "## Remaining Channel Obstruction Map",
        md_table(rows_by_name["obstruction"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    corpus_audit = corpus_readout_audit_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "corpus_readout_audit": corpus_audit,
        "parent_clause": parent_clause_rows(),
        "theorem": theorem_rows(),
        "signature": parent_signature_rows(corpus_audit),
        "finite_carry": finite_carry_rows(),
        "obstruction": obstruction_rows(),
    }
    rows_by_name["runner"] = runner_rows(rows_by_name)
    rows_by_name["gates"] = gate_rows(source_ok, rows_by_name)
    rows_by_name["decision"] = decision_rows(rows_by_name)
    rows_by_name["next"] = next_rows()
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
