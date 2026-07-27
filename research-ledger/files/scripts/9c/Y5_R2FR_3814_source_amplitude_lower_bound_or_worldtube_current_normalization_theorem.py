from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3814"
BRANCH = "MTS_R2FR_Y5_SOURCE_AMPLITUDE_LOWER_BOUND_OR_WORLDTUBE_CURRENT_NORMALIZATION_THEOREM_3814"
PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3814-Y5-R2FR-source-amplitude-lower-bound-or-worldtube-current-normalization-theorem.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3814_source_amplitude_lower_bound_or_worldtube_current_normalization_theorem.py"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3813 = PCW / "3813-Y5-R2FR-Rbridge-matter-glue-no-source-slot-or-finite-source-normalizer-row.md"
P_2444 = PCW / "2444-Y5-R2FR-source-leg-S-Eq-owner-from-parent-current-or-local-product-closure.md"
P_2446 = PCW / "2446-Y5-R2FR-EH-baseline-plus-MTS-residual-current-pack-for-S-Eq.md"
P_2481 = PCW / "2481-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md"
P_2482 = PCW / "2482-Y5-R2FR-kappaG-parent-calibration-or-dynamic-worldtube-closure.md"
P_2568 = PCW / "2568-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md"
P_2569 = PCW / "2569-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md"

CSV_3813_PRODUCTS = OUT / "P8_Y5_R2FR_3813_SOURCE_PRODUCT_BOUND_ROWS.csv"
CSV_3813_NEXT = OUT / "P8_Y5_R2FR_3813_NEXT_TARGET.csv"
CSV_2444_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_2444_SOURCE_LEG_DERIVATION_CONTRACT.csv"
CSV_2444_CURRENT = OUT / "P8_Y5_PARENT_QLOC_2444_PARENT_SOURCE_CURRENT_AUDIT.csv"
CSV_2446_PACK = OUT / "P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv"
CSV_2446_ENVELOPE = OUT / "P8_Y5_PARENT_QLOC_2446_S_EQ_NO_CANCELLATION_ENVELOPE.csv"
CSV_2481_THEOREM = OUT / "P8_Y5_SOURCE_NORM_2481_THEOREM_ATTEMPT.csv"
CSV_2568_THEOREM = OUT / "P8_Y5_SOURCE_NORM_2568_THEOREM_ATTEMPT.csv"
CSV_2568_ENORM = OUT / "P8_Y5_SOURCE_NORM_2568_ENORM_COMPONENTS.csv"
CSV_2482_ENORM = OUT / "P8_Y5_KAPPAG_WORLD_2482_ENORM_COMPONENTS.csv"
CSV_2569_RESIDUAL = OUT / "P8_Y5_EH_COUPLING_2569_COUPLING_RESIDUAL_ROW.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3814_SOURCE_REGISTER.csv",
    "theorems": OUT / "P8_Y5_R2FR_3814_SOURCE_AMPLITUDE_BRANCH_THEOREMS.csv",
    "worldtube": OUT / "P8_Y5_R2FR_3814_WORLDTUBE_NORMALIZATION_AUDIT.csv",
    "policies": OUT / "P8_Y5_R2FR_3814_PRODUCT_BOUND_ISOLATION_POLICY.csv",
    "branch_matrix": OUT / "P8_Y5_R2FR_3814_BRANCH_DECISION_MATRIX.csv",
    "residual_updates": OUT / "P8_Y5_R2FR_3814_SOURCE_AMPLITUDE_RESIDUAL_UPDATES.csv",
    "gates": OUT / "P8_Y5_R2FR_3814_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3814_DECISION_ROWS.csv",
    "next_target": OUT / "P8_Y5_R2FR_3814_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3814_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3814_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3814_0_3813_doc", P_3813, "product bounds, not isolated coefficient bounds", "3813 product-bound handoff"),
    ("SRC3814_1_2444_doc", P_2444, "S_A^q[x_readout]", "2444 source leg definition contract"),
    ("SRC3814_2_2446_doc", P_2446, "S_Eq No-Cancellation Envelope", "2446 residual-current envelope"),
    ("SRC3814_3_2481_doc", P_2481, "M_H=Q_M/ell_J", "2481 stationary Hilbert/worldtube source-normalization branch"),
    ("SRC3814_4_2482_doc", P_2482, "kappa0=8*pi*G_ref/c^4", "2482 kappa/G and dynamic worldtube blockers"),
    ("SRC3814_5_2568_doc", P_2568, "M_H=Q_M/ell_J", "2568 modern Hilbert/worldtube source-normalization branch"),
    ("SRC3814_6_2569_doc", P_2569, "e_ellJ_owner", "2569 coupling/source-scale residual rows"),
    ("SRC3814_7_3813_products", CSV_3813_PRODUCTS, "PB3813_R_matter_glue_total", "3813 source-product rows to add isolation policy"),
    ("SRC3814_8_3813_next", CSV_3813_NEXT, "3814-Y5-R2FR-source-amplitude-lower-bound-or-worldtube-current-normalization-theorem.md", "3813 machine handoff"),
    ("SRC3814_9_2444_contract", CSV_2444_CONTRACT, "SLC2444_0_definition", "machine-readable source-leg contract"),
    ("SRC3814_10_2444_current", CSV_2444_CURRENT, "PCA2444_1_parent_L", "parent source-current blockers"),
    ("SRC3814_11_2446_pack", CSV_2446_PACK, "RCS2446_3_matter_source_glue", "MTS residual current pack"),
    ("SRC3814_12_2446_envelope", CSV_2446_ENVELOPE, "SEQE2446_0_definition", "S_Eq no-cancellation envelope"),
    ("SRC3814_13_2481_theorem", CSV_2481_THEOREM, "THM2481_1_mass_readout_cancels_ellJ", "Hilbert mass readout cancellation"),
    ("SRC3814_14_2568_theorem", CSV_2568_THEOREM, "THM2568_1_mass_readout_cancels_ellJ", "modern Hilbert mass readout cancellation"),
    ("SRC3814_15_2568_enorm", CSV_2568_ENORM, "ENORM2568_2_e_ellJ_owner", "source-normalization residual components"),
    ("SRC3814_16_2482_enorm", CSV_2482_ENORM, "EN2482_0_e_kappaG", "kappa/dynamic E_norm components"),
    ("SRC3814_17_2569_residual", CSV_2569_RESIDUAL, "KRES2569_4_e_ellJ_owner", "coupling/source-scale residual row"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        (
            "SAT3814_0_source_leg_definition",
            "The source amplitude is a projected parent current ratio, not a free constant.",
            "S_E^q[x] = P_arena[ integral G_q(x,y) J_q^E(y) dmu_y ] / N_E, with J_q^E = delta S_matter,E/delta q.",
            "This defines the object whose lower bound is needed; it also forbids setting S_E^q=1 by units.",
            "EXACT_CONTRACT_FROM_2444",
            "parent current, kernel, projection, q normalization and N_E are not fully owned",
        ),
        (
            "SAT3814_1_positive_mass_no_lower_bound",
            "Positive Hilbert/worldtube mass does not imply nonzero q-source amplitude.",
            "M_H = Q_M/ell_J = integral T_H^{mu nu} tau_nu dSigma_mu can be positive while partial_q ln M_H or P[G_q J_q] is zero at a q-stationary or q-silent source.",
            "A worldtube mass denominator can normalize Newtonian source mass, but cannot isolate coefficient residuals from abs(S_E^q)*epsilon products.",
            "EXACT_NO_GO",
            "none for the no-go; it is a guardrail against a false lower bound",
        ),
        (
            "SAT3814_2_zero_source_branch",
            "If the parent local-GR branch proves P_arena[G_q J_q^E]=0, all S_E^q-product local fifth-force rows vanish but coefficients are not bounded.",
            "For every retained product B_r >= |S_E^q epsilon_r|, S_E^q=0 makes the product zero independently of epsilon_r.",
            "This is a viable local-GR/silence route, but it is not a coefficient-isolation route.",
            "CONDITIONAL_ZERO_BRANCH",
            "parent source-current silence theorem and projection/readout silence",
        ),
        (
            "SAT3814_3_active_normalized_branch",
            "If the parent proves a positive lower certificate c_SE <= |S_E^q| in a shared arena, each product row can be isolated as |epsilon_r| <= B_r/c_SE.",
            "The lower certificate requires a nonzero source current, fixed sign/no-nodal-cancellation or a positive projection theorem, plus an owned normalization N_E.",
            "This is the only honest route from 3813 product bounds to isolated source-residual coefficients.",
            "CONDITIONAL_ACTIVE_BRANCH",
            "MISSING_PARENT_CSE_LOWER_BOUND",
        ),
        (
            "SAT3814_4_current_default",
            "The current corpus supports product-level residual policies, not an isolated lower bound.",
            "2446/2568/2569 retain e_kappaG, e_ellJ_owner, dynamic exchange, jump/support and source-shadow residuals; no c_SE row is present.",
            "3814 must keep all 3813 residual rows product-only until a zero-source theorem or active c_SE certificate is derived.",
            "CURRENT_VERDICT_PRODUCT_ONLY",
            "MISSING_CSE_LOWER_OR_SOURCE_SILENCE",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "theorem_id": theorem_id,
            "statement": statement,
            "derivation": derivation,
            "result": result,
            "status": status,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for theorem_id, statement, derivation, result, status, missing in rows
    ]


def worldtube_rows(timestamp: str) -> list[dict[str, Any]]:
    entries = [
        (
            "WTN3814_0_hilbert_mass_chain",
            "M_H = Q_M/ell_J = integral T_H tau dSigma",
            "positive source mass / non-fitted Newton denominator",
            "PASS_CONDITIONAL_CONTROL",
            "does not imply partial_q ln M_H nonzero",
            "Use as Newton source-mass normalization branch, not as c_SE lower bound.",
        ),
        (
            "WTN3814_1_exact_divergence_identity",
            "nabla_mu J_M^mu=(nabla ell_J)T tau + ell_J(nabla T)tau + ell_J T nabla tau",
            "localizes source-normalization leakage",
            "PASS_DERIVED_FROM_2568",
            "dynamic exchange current not parent-owned",
            "Retain e_clock_exchange/e_surface_drift/e_jump_support until dynamic worldtube closure.",
        ),
        (
            "WTN3814_2_stationary_control",
            "fixed ell_J, conserved Hilbert stress, Killing tau, compact support, no side/jump flux",
            "surface-independent Hilbert mass",
            "PASS_STATIONARY_CONDITIONAL",
            "stationary surface independence still does not make q-sensitivity nonzero",
            "Good control branch; not coefficient isolation.",
        ),
        (
            "WTN3814_3_coupling_scale",
            "kappa0/G_ref and ell_J ownership",
            "coupling/source-current scale",
            "BLOCKED_PARENT_OWNER",
            "e_kappaG and e_ellJ_owner retained by 2568/2569",
            "Cannot define c_SE from a fitted or imported coupling.",
        ),
        (
            "WTN3814_4_active_lower_certificate",
            "c_SE := inf_arena |P_arena[G_q J_q^E]/N_E|",
            "source-amplitude lower bound needed for product isolation",
            "MISSING_PARENT_CERTIFICATE",
            "requires nonzero current, positive projection/no-cancellation, owned N_E and shared arena",
            "Stage symbol c_SE_lower but do not use it numerically.",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "audit_id": audit_id,
            "object": obj,
            "role": role,
            "status": status,
            "blocker": blocker,
            "3814_policy": policy,
            "valid_for_claim": "false",
        }
        for audit_id, obj, role, status, blocker, policy in entries
    ]


def product_policy_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(CSV_3813_PRODUCTS):
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "policy_id": f"ISO3814_{row['product_bound_id']}",
                "source_product_bound_id": row["product_bound_id"],
                "symbol": row["symbol"],
                "residual_slot": row["residual_slot"],
                "arena": row["arena"],
                "product_bound": row["bound_value"],
                "product_units": row["bound_units"],
                "current_policy": "PRODUCT_ONLY_DEFAULT",
                "zero_branch_meaning": "if S_E^q=0 this product is silent but the residual coefficient is unconstrained",
                "active_branch_required_input": "c_SE_lower_bound",
                "isolated_bound_formula_if_cSE_signed": f"abs({row['symbol']}) <= {row['bound_value']} / c_SE_lower_bound",
                "c_SE_lower_bound_status": "MISSING_PARENT_LOWER_BOUND",
                "isolation_allowed_now": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def branch_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        (
            "BR3814_0_zero_source_silence",
            "P_arena[G_q J_q^E]=0",
            "all local S_E^q product rows vanish",
            "local-GR/source-silence route",
            "does not bound residual coefficients; requires parent source-current silence",
            "PROMISING_FOR_LOCAL_GR_NOT_COEFFICIENT_ISOLATION",
        ),
        (
            "BR3814_1_active_positive_source",
            "0 < c_SE <= |S_E^q|",
            "product rows become isolated coefficient bounds B/c_SE",
            "empirical residual-coefficient isolation route",
            "requires nonzero current, positive/no-cancellation projection and owned normalization",
            "NOT_AVAILABLE_CURRENT_CORPUS",
        ),
        (
            "BR3814_2_product_only",
            "S_E^q neither zero-proved nor lower-bounded",
            "only abs(S_E^q)*epsilon products are bounded",
            "current strict branch",
            "cannot claim local-GR or coefficient bounds from products alone",
            "ACTIVE_DEFAULT",
        ),
        (
            "BR3814_3_upper_only",
            "|S_E^q| <= C_upper without lower bound",
            "does not isolate epsilon because S_E^q may be arbitrarily small",
            "guardrail branch",
            "upper bounds alone are not useful for coefficient isolation",
            "REJECT_AS_ISOLATION_ROUTE",
        ),
        (
            "BR3814_4_worldtube_mass_positive",
            "M_H>0 from Hilbert/worldtube mass",
            "normalizes source mass but not q-source amplitude",
            "Newton source-mass control branch",
            "positive mass can coexist with zero q-derivative",
            "CONTROL_ONLY",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "branch_case_id": case_id,
            "condition": condition,
            "consequence": consequence,
            "use": use,
            "limitation": limitation,
            "current_status": status,
            "valid_for_claim": "false",
        }
        for case_id, condition, consequence, use, limitation, status in rows
    ]


def residual_update_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        (
            "UP3814_0_abs_SEq",
            "abs(S_E^q)",
            "NOW_THE_MAIN_ISOLATION_BOTTLENECK",
            "BRANCH_SPLIT_ZERO_OR_ACTIVE_OR_PRODUCT_ONLY",
            "positive Hilbert mass denominator is not a q-source lower bound",
        ),
        (
            "UP3814_1_3813_products",
            "3813 source-product rows",
            "PRODUCT_BOUNDED_NOT_ISOLATED",
            "PRODUCT_ONLY_WITH_EXPLICIT_ISOLATION_POLICY",
            "each row now carries zero-branch meaning and active-branch c_SE formula",
        ),
        (
            "UP3814_2_worldtube_control",
            "Hilbert/worldtube mass branch",
            "CONTROL_ONLY",
            "VALID_SOURCE_MASS_NORMALIZATION_NOT_CSE_LOWER_BOUND",
            "useful for Newton source mass but not enough for residual coefficient isolation",
        ),
        (
            "UP3814_3_next_derivation",
            "source-current route",
            "MISSING_CSE_LOWER_OR_SOURCE_SILENCE",
            "SOURCE_CURRENT_SILENCE_OR_ACTIVE_CSE_CERTIFICATE_SELECTED",
            "the next step should decide whether local branch is q-silent or active-positive",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "update_id": update_id,
            "object": obj,
            "old_status": old,
            "new_status": new,
            "reason": reason,
            "valid_for_claim": "false",
        }
        for update_id, obj, old, new, reason in rows
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    policy_count = len(grouped["policies"])
    all_not_isolated = all(row["isolation_allowed_now"] == "false" for row in grouped["policies"])
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3814_0_positive_mass_no_fake_lower_bound",
            "requirement": "prove or record that positive Hilbert/worldtube mass does not imply nonzero q-source amplitude",
            "passed": "true",
            "evidence": "SAT3814_1 exact no-go and WTN3814 audit",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3814_1_product_policy_rows",
            "requirement": "every 3813 product row has an explicit residual-isolation policy",
            "passed": bool_text(policy_count == 12),
            "evidence": f"{policy_count} policy rows generated",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3814_2_no_over_isolation",
            "requirement": "no residual coefficient is isolated without c_SE lower bound",
            "passed": bool_text(all_not_isolated),
            "evidence": "all policy rows keep isolation_allowed_now=false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3814_3_zero_source_branch_defined",
            "requirement": "define the source-current silence branch separately from active lower-bound branch",
            "passed": "true",
            "evidence": "BR3814_0 and SAT3814_2 define zero-source branch",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3814_4_active_cSE_available",
            "requirement": "parent-owned c_SE lower bound exists",
            "passed": "false",
            "evidence": "c_SE_lower_bound_status remains MISSING_PARENT_LOWER_BOUND",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": "DEC3814_0_reject_false_lower_bound",
            "decision": "Do not use positive Hilbert/worldtube mass as a lower bound on abs(S_E^q).",
            "reason": "A positive source mass can have zero q-derivative or zero projected q-current.",
            "next_action": "derive source-current silence or active c_SE lower certificate directly",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": "DEC3814_1_keep_product_rows_honest",
            "decision": "Keep all 3813 residuals as product-only until c_SE exists.",
            "reason": "WEP bounds constrain abs(S_E^q)*epsilon; coefficient isolation needs a lower bound, not an upper or denominator positivity.",
            "next_action": "use the 3814 policy table for any future local residual runner",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": "DEC3814_2_next_target",
            "decision": "Make the next target source-current silence versus active-source certificate.",
            "reason": "The local-GR path likely wants q-source silence; the empirical coefficient-bound path needs c_SE>0. These are different branches and must not be mixed.",
            "next_action": "3815 should attempt the local source-current silence theorem first, with active c_SE as fallback",
            "valid_for_claim": "false",
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3815-Y5-R2FR-local-source-current-silence-or-active-cSE-certificate.md",
            "target_script": "scripts/Y5_R2FR_3815_local_source_current_silence_or_active_cSE_certificate.py",
            "objective": "Try the local-GR route first: prove P_arena[G_q J_q^E]=0 for the local source branch from parent current descent/projector/readout silence; if that fails, attempt an active positive c_SE certificate with no-nodal-cancellation and owned N_E.",
            "success_gate": "Either a parent-signed source-current silence theorem is produced, or a nonzero active-source lower certificate c_SE is created with all normalization/projection inputs declared; otherwise keep product-only residuals.",
            "avoid": "do not use positive mass as q-amplitude lower bound; do not set S_E^q=1; do not mix zero-source and active-source branches; do not edit formalization-workbench; do not use GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_SOURCE_AMPLITUDE_FALSE_LOWER_BOUND_REJECTED_PRODUCT_POLICY_RUNNER_BUILT",
            "summary": "3814 proves the guardrail that positive Hilbert/worldtube mass does not lower-bound abs(S_E^q), splits the local branch into zero-source, active-positive and product-only cases, and gives every 3813 source-product row an explicit isolation policy. The current corpus remains product-only until source-current silence or active c_SE is parent-signed.",
            "valid_for_claim": "false",
        }
    ]


def row_bullet(row: dict[str, Any], key_fields: list[str]) -> str:
    label = " ".join(f"`{row[field]}`" for field in key_fields if row.get(field))
    rest = "; ".join(
        f"{key}: {value}"
        for key, value in row.items()
        if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"}
    )
    return f"- {label}: {rest}"


def write_markdown(grouped: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3814 - Source Amplitude Lower Bound Or Worldtube Current Normalization Theorem",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_SOURCE_AMPLITUDE_FALSE_LOWER_BOUND_REJECTED_PRODUCT_POLICY_RUNNER_BUILT`.",
        "",
        "3814 resolves an important fork: a positive Hilbert/worldtube mass is not a lower bound on `abs(S_E^q)`. A body can have positive mass while its q-source current, q-derivative, or projected q-current is zero. So using mass positivity to isolate the 3813 product rows would be a fake proof.",
        "",
        "The correct split is now explicit. The zero-source branch can help local GR because `S_E^q=0` makes local fifth-force products silent, but it does not bound the residual coefficients. The active-positive branch can isolate coefficients only after a parent-owned `c_SE <= abs(S_E^q)` certificate with no-nodal-cancellation and owned normalization `N_E`. The current strict branch remains product-only.",
        "",
        "No local-GR, WEP, Newton, PPN, clock, R10, EM, or calibrated source-coupling claim is made.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Source Amplitude Branch Theorems", "theorems", ["theorem_id"]),
        ("Worldtube Normalization Audit", "worldtube", ["audit_id"]),
        ("Product Bound Isolation Policy", "policies", ["policy_id", "symbol"]),
        ("Branch Decision Matrix", "branch_matrix", ["branch_case_id"]),
        ("Residual Updates", "residual_updates", ["update_id"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decision Rows", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
        lines.append("")
    DOC_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    lines = text.splitlines()
    if lines and lines[0].startswith("# Local GR Coupling Spine - Current State After "):
        lines[0] = "# Local GR Coupling Spine - Current State After 3814"
        text = "\n".join(lines) + "\n"

    paragraph = (
        "`3814` resolves the source-amplitude isolation fork. Positive Hilbert/worldtube mass is not a lower bound on `abs(S_E^q)`: a source can have positive mass while the q-current or projected q-derivative is zero. "
        "The local branch is now split into source-current silence, active-positive `c_SE`, and product-only cases. Source silence can support local-GR/fifth-force suppression but does not bound residual coefficients; active coefficient isolation requires a parent-owned `c_SE <= abs(S_E^q)` certificate; the current corpus remains product-only with explicit isolation policies for every 3813 row."
    )
    if "`3814` resolves the source-amplitude isolation fork" not in text:
        marker = "`3813` fuses the no-source-only matter grammar"
        idx = text.find(marker)
        if idx >= 0:
            next_blank = text.find("\n\n", idx)
            if next_blank >= 0:
                text = text[: next_blank + 2] + paragraph + "\n\n" + text[next_blank + 2 :]

    bullet = "- `3814 source-amplitude fork`: positive worldtube mass is rejected as a fake `S_E^q` lower bound; every source-product row now has zero-source, active-cSE, and product-only policy branches."
    if bullet not in text:
        anchor = "- `3813 matter-glue branch`: `R_matter_glue` now has an exact conditional zero theorem and finite WEP source-product rows; the remaining blocker is isolating products through `abs(S_E^q)`."
        text = text.replace(anchor, anchor + "\n" + bullet)

    nonclaim = "- The 3814 source-amplitude fork is nonclaim: no `c_SE` lower certificate exists, and source silence/product-only branches must not be advertised as isolated coefficient bounds."
    if nonclaim not in text:
        anchor = "- The 3813 matter-glue branch is nonclaim: theorem-zero clauses are not parent-signed, and source-product rows do not isolate residual coefficients without a parent-owned `abs(S_E^q)` lower/normalization theorem."
        text = text.replace(anchor, anchor + "\n" + nonclaim)

    old_target = (
        "`3814-Y5-R2FR-source-amplitude-lower-bound-or-worldtube-current-normalization-theorem.md`\n\n"
        "Target: attack the isolation bottleneck exposed by 3813. Derive a parent-owned lower/nonzero theorem or normalization rule for `abs(S_E^q)`, preferably from the worldtube current definition and denominator, or state the exact finite residual product level that remains.\n\n"
        "This is the best next move because many source residuals are now product-bounded with WEP units. The next decisive question is whether those products can be isolated without setting `S_E^q=1` by hand."
    )
    new_target = (
        "`3815-Y5-R2FR-local-source-current-silence-or-active-cSE-certificate.md`\n\n"
        "Target: try the local-GR route first by proving `P_arena[G_q J_q^E]=0` for the local source branch from parent current descent, projector silence, and readout silence. If that fails, attempt an active positive `c_SE` certificate with no-nodal-cancellation and owned `N_E`.\n\n"
        "This is the best next move because 3814 shows positive source mass cannot isolate products. The theory must now choose cleanly between q-source silence, active source amplitude, or honest product-only residuals."
    )
    if old_target in text:
        text = text.replace(old_target, new_target)

    artifacts = [
        "P8_Y5_R2FR_3814_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_3814_SOURCE_AMPLITUDE_BRANCH_THEOREMS.csv",
        "P8_Y5_R2FR_3814_WORLDTUBE_NORMALIZATION_AUDIT.csv",
        "P8_Y5_R2FR_3814_PRODUCT_BOUND_ISOLATION_POLICY.csv",
        "P8_Y5_R2FR_3814_BRANCH_DECISION_MATRIX.csv",
        "P8_Y5_R2FR_3814_SOURCE_AMPLITUDE_RESIDUAL_UPDATES.csv",
        "P8_Y5_R2FR_3814_CLAIM_GATES.csv",
        "P8_Y5_R2FR_3814_DECISION_ROWS.csv",
        "P8_Y5_R2FR_3814_NEXT_TARGET.csv",
        "P8_Y5_R2FR_3814_STATUS.csv",
        "P8_Y5_BRR545_3814_VALIDATION.csv",
    ]
    for artifact in artifacts:
        entry = f"- `source-intake\\mts_residuals\\{artifact}`"
        if entry not in text:
            text = text.rstrip() + "\n" + entry + "\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache() -> None:
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            read_csv(path)
    fwb_hits = list(FWB.rglob("*3814*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH, SPINE_PATH] if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3814 markdown document written"),
        ("positive_mass_no_lower_bound", any(row["theorem_id"] == "SAT3814_1_positive_mass_no_lower_bound" and row["status"] == "EXACT_NO_GO" for row in grouped["theorems"]), "false lower bound route is rejected"),
        ("policy_rows_cover_3813", len(grouped["policies"]) == 12, "all 3813 source-product rows have policies"),
        ("no_policy_overisolates", all(row["isolation_allowed_now"] == "false" for row in grouped["policies"]), "no coefficient is isolated without c_SE"),
        ("zero_and_active_branches_split", any(row["branch_case_id"] == "BR3814_0_zero_source_silence" for row in grouped["branch_matrix"]) and any(row["branch_case_id"] == "BR3814_1_active_positive_source" for row in grouped["branch_matrix"]), "zero and active source branches both explicit"),
        ("active_cse_missing_gate", any(row["gate_id"] == "GATE3814_4_active_cSE_available" and row["passed"] == "false" for row in grouped["gates"]), "active c_SE is not smuggled in"),
        ("claims_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("spine_updated", "Current State After 3814" in spine_text and "3815-Y5-R2FR-local-source-current-silence-or-active-cSE-certificate.md" in spine_text, "live spine updated to 3814 and 3815 target"),
        ("formalization_clean", not fwb_hits, "no 3814 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script/spine contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorems": theorem_rows(timestamp),
        "worldtube": worldtube_rows(timestamp),
        "policies": product_policy_rows(timestamp),
        "branch_matrix": branch_matrix_rows(timestamp),
        "residual_updates": residual_update_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gate_rows(timestamp, grouped)
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    write_markdown(grouped)
    update_spine()
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
