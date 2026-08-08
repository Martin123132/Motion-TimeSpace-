from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3016"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3016-Y5-R2FR-gamma-and-alpha3-PPN-kernel-first-derivation-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3016_00_3015_doc": ROOT / "3015-Y5-R2FR-PPN-kernel-from-local-closure-residual-envelope-under-AX1090.md",
    "SRC3016_01_3015_validation": RESIDUALS / "P8_Y5_BRR545_3015_VALIDATION.csv",
    "SRC3016_02_3015_kernel_contract": RESIDUALS / "P8_Y5_R2FR_3015_PPN_KERNEL_CONTRACT.csv",
    "SRC3016_03_3015_comparators": RESIDUALS / "P8_Y5_R2FR_3015_PPN_COMPARATOR_LINKS.csv",
    "SRC3016_04_3015_gm_guard": RESIDUALS / "P8_Y5_R2FR_3015_FIXED_GM_GUARD.csv",
    "SRC3016_05_3014_closure_envelope": RESIDUALS / "P8_Y5_R2FR_3014_LOCAL_CLOSURE_RESIDUAL_ENVELOPE.csv",
    "SRC3016_06_2489_common_frame_kernel": LOCAL_BOUNDS / "First_common_frame_PPN_response_kernel_2489_NONCLAIM.csv",
    "SRC3016_07_2513_source_weight_kernel": LOCAL_BOUNDS / "PPN_source_weight_response_kernel_2513_NONCLAIM.csv",
    "SRC3016_08_2513_measured_GM_guard": BETA_DOCS / "Measured_GM_no_absorb_guard_2513_NONCLAIM.csv",
    "SRC3016_09_2633_parent_normal_form": ROOT / "2633-Y5-R2FR-parent-normal-form-DObs-EH-current-branch-synthesis-or-full-PPN-residual-fill.md",
    "SRC3016_10_2748_weak_field_zero": ROOT / "2748-Y5-R2FR-parent-weak-field-zero-condition-derivation-or-demotion-under-AX1090.md",
    "SRC3016_11_2749_minimal_action": ROOT / "2749-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate-under-AX1090.md",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3016_SOURCE_REGISTER.csv",
    "gamma_kernel": RESIDUALS / "P8_Y5_R2FR_3016_GAMMA_KERNEL_DERIVATION.csv",
    "alpha3_audit": RESIDUALS / "P8_Y5_R2FR_3016_ALPHA3_ZERO_THEOREM_AUDIT.csv",
    "first_rows": RESIDUALS / "P8_Y5_R2FR_3016_PPN_FIRST_KERNEL_ROWS.csv",
    "fixed_gm_gamma": RESIDUALS / "P8_Y5_R2FR_3016_FIXED_GM_GAMMA_GUARD.csv",
    "blockers": RESIDUALS / "P8_Y5_R2FR_3016_BLOCKER_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3016_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3016_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3016_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3016_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3016_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "gamma_copy": LOCAL_BOUNDS / "gamma_kernel_first_derivation_3016_NONCLAIM.csv",
    "alpha3_copy": LOCAL_BOUNDS / "alpha3_source_current_zero_audit_3016_NONCLAIM.csv",
    "first_rows_copy": LOCAL_BOUNDS / "PPN_first_kernel_rows_3016_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3016_GAMMA_ALPHA3_SOURCE_CURRENT_NEXT.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_roles = {
    "SRC3016_00_3015_doc": "3015 handoff: PPN is the local-GR arena",
    "SRC3016_01_3015_validation": "3015 pass/fail status and no-claim guard",
    "SRC3016_02_3015_kernel_contract": "gamma and alpha3 kernel contract rows",
    "SRC3016_03_3015_comparators": "PPN comparator bounds for gamma and alpha3",
    "SRC3016_04_3015_gm_guard": "fixed measured-GM no-absorb policy",
    "SRC3016_05_3014_closure_envelope": "rank-zero closure envelope feeding PPN",
    "SRC3016_06_2489_common_frame_kernel": "conditional gamma conformal kernel",
    "SRC3016_07_2513_source_weight_kernel": "source-weight PPN response schema",
    "SRC3016_08_2513_measured_GM_guard": "measured-GM calibration rule",
    "SRC3016_09_2633_parent_normal_form": "single parent-normal-form local-GR gate",
    "SRC3016_10_2748_weak_field_zero": "weak-field qR/beta derivation failure and demotion",
    "SRC3016_11_2749_minimal_action": "minimal action ansatz and Euler/Ward gates",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

gamma_kernel = [
    base(
        {
            "gamma_id": "GAM3016_0_PPN_ratio_definition",
            "object": "gamma_eff_after_fixed_GM",
            "derivation": "write the weak-field observed metric as g00=-1+2 A_T U/c^2+O(c^-4), gij=(1+2 A_S U/c^2) delta_ij+O(c^-4); fixed measured GM defines U_obs=A_T U, so gamma_eff=A_S/A_T",
            "formula": "gamma_minus_1=(A_S-A_T)/A_T",
            "status": "DERIVED_ALGEBRAIC_KERNEL",
            "missing_for_claim": "MISSING_A_T_SOURCE_NORMALIZATION; MISSING_A_S_METRIC_RESPONSE; MISSING_READOUT_GAUGE",
        }
    ),
    base(
        {
            "gamma_id": "GAM3016_1_common_conformal_specialization",
            "object": "s_R_common_Weyl",
            "derivation": "for g_obs=exp(2 s_R U/c^2) g_GR, the coefficients are A_T=1-s_R and A_S=1+s_R",
            "formula": "gamma_minus_1=2 s_R/(1-s_R)",
            "status": "DERIVED_CONDITIONAL_SPECIAL_CASE_FROM_2489",
            "missing_for_claim": "MISSING_s_R_VALUE; MISSING_NO_OTHER_PPN_CHANNELS; MISSING_FULL_VECTOR_CLOSURE",
        }
    ),
    base(
        {
            "gamma_id": "GAM3016_2_small_residual_envelope",
            "object": "epsilon_S_minus_epsilon_T",
            "derivation": "let A_T=1+epsilon_T and A_S=1+epsilon_S after the common scalar GM quotient; then gamma_minus_1=(epsilon_S-epsilon_T)/(1+epsilon_T)",
            "formula": "|gamma_minus_1| <= |epsilon_S-epsilon_T|/(1-|epsilon_T|) for |epsilon_T|<1",
            "status": "BOUND_KERNEL_READY_VALUES_MISSING",
            "missing_for_claim": "MISSING_EPSILON_T_BOUND; MISSING_EPSILON_S_BOUND; MISSING_COMMON_MODE_QUOTIENT_PROOF",
        }
    ),
    base(
        {
            "gamma_id": "GAM3016_3_closure_projection",
            "object": "Pi_gamma[Delta_rankzero_source_abs_A]",
            "derivation": "the 3014/3015 closure vector can feed gamma only through the weak-field coefficient difference A_S-A_T plus readout/source tails",
            "formula": "|gamma_minus_1| <= |K_gamma_ST| Delta_A/(1-|epsilon_T|) + |K_gamma_readout Delta_readout| + |K_gamma_source Delta_w_eff|",
            "status": "PROJECTION_CONTRACT_WRITTEN_VALUES_MISSING",
            "missing_for_claim": "MISSING_K_GAMMA_ST; MISSING_DELTA_A_VALUE; MISSING_DELTA_READOUT_VALUE; MISSING_DELTA_W_EFF_VALUE",
        }
    ),
]

alpha3_audit = [
    base(
        {
            "alpha3_id": "A3Z3016_0_PPN_meaning",
            "object": "alpha3 preferred-frame/nonconservation channel",
            "zero_condition": "alpha3=0 follows only if the local branch has no preferred vector slot and no source-current/momentum nonconservation projection",
            "current_evidence": "2513 and 3015 keep alpha3 tied to Delta_w_eff, J_NH and Q_edge",
            "status": "TARGET_ZERO_THEOREM_IDENTIFIED",
            "missing_for_claim": "MISSING_PARENT_SOURCE_CURRENT_OWNER",
        }
    ),
    base(
        {
            "alpha3_id": "A3Z3016_1_Ward_conservation_route",
            "object": "nabla_mu T_eff^{mu nu}=0",
            "zero_condition": "a fully varied diffeomorphism-covariant parent action plus same-frame matter descent gives the Ward identity needed to silence source-current exchange",
            "current_evidence": "2633 and 2749 provide conditional Ward gates, not a signed parent action",
            "status": "CONDITIONAL_THEOREM_UNSIGNED",
            "missing_for_claim": "MISSING_COMPLETE_PARENT_ACTION; MISSING_THETA_QTAU_CURRENT_CHAIN; MISSING_SAME_FRAME_MATTER_DESCENT",
        }
    ),
    base(
        {
            "alpha3_id": "A3Z3016_2_nonHilbert_current",
            "object": "J_NH",
            "zero_condition": "J_NH=0 or Pi_alpha3[J_NH]=0 in the compact local branch",
            "current_evidence": "local closure and GK ledgers retain non-Hilbert/source-current residuals",
            "status": "ZERO_NOT_SIGNED",
            "missing_for_claim": "MISSING_NO_HILBERT_CURRENT_THEOREM_OR_NUMERIC_BOUND",
        }
    ),
    base(
        {
            "alpha3_id": "A3Z3016_3_boundary_flux",
            "object": "Q_edge",
            "zero_condition": "boundary/reference flux has zero alpha3 projection or is bounded below 4e-20 after normalization",
            "current_evidence": "3015 alpha3 row and earlier boundary rows keep Q_edge live",
            "status": "BOUNDARY_ZERO_NOT_SIGNED",
            "missing_for_claim": "MISSING_BOUNDARY_NO_FLUX_THEOREM; MISSING_K_ALPHA3_BOUNDARY",
        }
    ),
    base(
        {
            "alpha3_id": "A3Z3016_4_source_weight",
            "object": "Delta_w_eff",
            "zero_condition": "relative source weights vanish after the one allowed common GM quotient",
            "current_evidence": "2513 measured-GM guard says relative weights survive fixed-GM calibration",
            "status": "RELATIVE_SOURCE_WEIGHT_STILL_LIVE",
            "missing_for_claim": "MISSING_UNIVERSAL_SOURCE_WEIGHT_THEOREM",
        }
    ),
    base(
        {
            "alpha3_id": "A3Z3016_5_total_alpha3_gate",
            "object": "alpha3_abs",
            "zero_condition": "alpha3_abs <= |C_exchange Delta_w_eff| + |C_NH J_NH| + |C_boundary Q_edge|, and all three terms must be theorem-zero or numerically below the 4e-20 budget",
            "current_evidence": "comparator exists but C coefficients and component amplitudes are missing",
            "status": "KERNEL_BOUND_FORM_READY_VALUES_MISSING",
            "missing_for_claim": "MISSING_C_ALPHA3_EXCHANGE; MISSING_C_ALPHA3_NH; MISSING_C_ALPHA3_BOUNDARY; MISSING_COMPONENT_VALUES",
        }
    ),
]

first_rows = [
    base(
        {
            "row_id": "PPN3016_0_gamma_first_kernel",
            "observable": "gamma_minus_1",
            "kernel_formula": "gamma_minus_1=(A_S-A_T)/A_T; conformal special case 2 s_R/(1-s_R)",
            "bound": "2.3e-05",
            "units": "dimensionless",
            "status": "FIRST_CONCRETE_KERNEL_FORMULA_NONCLAIM",
            "blocks_claim": "MISSING_A_S_A_T_OR_s_R_VALUES; MISSING_READOUT_GAUGE; MISSING_FULL_PPN_VECTOR",
        }
    ),
    base(
        {
            "row_id": "PPN3016_1_alpha3_zero_or_bound_kernel",
            "observable": "alpha3",
            "kernel_formula": "alpha3_abs <= |C_exchange Delta_w_eff| + |C_NH J_NH| + |C_boundary Q_edge|",
            "bound": "4e-20",
            "units": "dimensionless",
            "status": "ZERO_THEOREM_ROUTE_IDENTIFIED_VALUES_MISSING",
            "blocks_claim": "MISSING_WARD_SOURCE_CURRENT_ZERO; MISSING_BOUNDARY_NO_FLUX; MISSING_ALPHA3_COEFFICIENTS",
        }
    ),
    base(
        {
            "row_id": "PPN3016_2_pair_status",
            "observable": "gamma_plus_alpha3",
            "kernel_formula": "gamma can be coefficient-mapped; alpha3 demands source-current/no-flux conservation",
            "bound": "componentwise comparator only",
            "units": "dimensionless vector",
            "status": "PAIR_ADVANCED_NO_PPN_PASS",
            "blocks_claim": "MISSING_BETA_ALPHA1_ALPHA2_XI; MISSING_NUMERIC_VECTOR; NO_CANCELLATION_VECTOR_STILL_ACTIVE",
        }
    ),
]

fixed_gm_gamma = [
    base(
        {
            "guard_id": "FGG3016_0_common_scale",
            "rule": "one common scalar in A_T and A_S can be absorbed into U_obs=G_obs M_obs/r, but the ratio A_S/A_T remains observable",
            "mathematical_form": "A_T -> 1 by measured-GM convention; gamma_eff=A_S/A_T",
            "status": "EXACT_RATIO_GUARD",
            "blocks": "claiming gamma is closed by fitting GM",
        }
    ),
    base(
        {
            "guard_id": "FGG3016_1_relative_difference",
            "rule": "epsilon_S-epsilon_T survives fixed-GM calibration",
            "mathematical_form": "gamma_minus_1=(epsilon_S-epsilon_T)/(1+epsilon_T)",
            "status": "LIVE_GAMMA_RESIDUAL",
            "blocks": "absorbing spatial/time coefficient mismatch into source mass",
        }
    ),
    base(
        {
            "guard_id": "FGG3016_2_gamma_only_forbidden",
            "rule": "even a small gamma residual is not a local-GR pass without beta and preferred-frame rows",
            "mathematical_form": "Delta_PPN_abs is componentwise",
            "status": "FULL_VECTOR_GUARD_ACTIVE",
            "blocks": "gamma-only victory lap",
        }
    ),
]

blockers = [
    base(
        {
            "blocker_id": "BLK3016_0_gamma_values",
            "blocking_condition": "MISSING_GAMMA_COEFFICIENT_VALUES",
            "precise_missing_object": "A_T, A_S, or s_R from a parent-signed weak-field response map",
            "next_attack": "derive the weak-field source/readout coefficient split from the parent normal-form gate",
        }
    ),
    base(
        {
            "blocker_id": "BLK3016_1_gamma_readout",
            "blocking_condition": "MISSING_READOUT_GAUGE",
            "precise_missing_object": "observed coframe and PPN gauge/readout map before comparison",
            "next_attack": "lock DObs/source frame before numerical gamma scoring",
        }
    ),
    base(
        {
            "blocker_id": "BLK3016_2_alpha3_Ward",
            "blocking_condition": "MISSING_SOURCE_CURRENT_CONSERVATION_THEOREM",
            "precise_missing_object": "parent Ward identity that kills Delta_w_eff, J_NH and source exchange in alpha3 projection",
            "next_attack": "attempt source-current Ward owner proof under the 2749 minimal action ansatz",
        }
    ),
    base(
        {
            "blocker_id": "BLK3016_3_alpha3_boundary",
            "blocking_condition": "MISSING_BOUNDARY_NO_FLUX_ALPHA3",
            "precise_missing_object": "Q_edge=0 or K_alpha3_boundary*Q_edge bounded under 4e-20",
            "next_attack": "separate boundary flux theorem-zero from source-current theorem-zero",
        }
    ),
    base(
        {
            "blocker_id": "BLK3016_4_rest_vector",
            "blocking_condition": "MISSING_REMAINING_PPN_COMPONENTS",
            "precise_missing_object": "beta, alpha1, alpha2 and xi kernels still not derived",
            "next_attack": "after gamma/alpha3 owner gates, continue beta second-order and preferred-frame matrix",
        }
    ),
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3016_0_sources_exist",
            "gate": "all cited source paths exist",
            "result": all(boolish(row["exists"]) for row in source_register),
            "notes": "3016 cites only local private ledgers",
        }
    ),
    base(
        {
            "gate_id": "GATE3016_1_gamma_formula",
            "gate": "gamma algebraic kernel is written",
            "result": True,
            "notes": "gamma_eff=A_S/A_T and conformal specialization are explicit",
        }
    ),
    base(
        {
            "gate_id": "GATE3016_2_gamma_claim",
            "gate": "gamma prediction can be claimed",
            "result": False,
            "notes": "A_T/A_S or s_R values, readout gauge, and full vector closure are missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3016_3_alpha3_zero",
            "gate": "alpha3 theorem-zero is parent-signed",
            "result": False,
            "notes": "source-current Ward owner and boundary no-flux theorem are unsigned",
        }
    ),
    base(
        {
            "gate_id": "GATE3016_4_fixed_GM_guard",
            "gate": "fixed measured-GM guard remains active",
            "result": True,
            "notes": "A_S/A_T ratio survives common GM quotient",
        }
    ),
    base(
        {
            "gate_id": "GATE3016_5_PPN_local_GR_claim",
            "gate": "PPN/local-GR pass claim allowed",
            "result": False,
            "notes": "first kernels advanced but no numeric/theorem-zero PPN vector exists",
        }
    ),
]

decision = [
    base(
        {
            "decision_id": "DEC3016_0_gamma_status",
            "decision": "gamma now has an exact weak-field coefficient-ratio kernel",
            "rationale": "fixed GM calibrates A_T, but gamma is the ratio A_S/A_T; this prevents fitted-GM hiding of the observable residual",
            "consequence": "gamma is no longer just a placeholder, but remains nonclaim until A_T/A_S/readout values are parent-signed",
        }
    ),
    base(
        {
            "decision_id": "DEC3016_1_alpha3_status",
            "decision": "alpha3 is the live conservation/source-current trap",
            "rationale": "the 4e-20 comparator is so tight that finite residuals are unlikely to be safe without a theorem-zero or very strong source-backed bound",
            "consequence": "next work should attack the source-current Ward owner before broad PPN scoring",
        }
    ),
    base(
        {
            "decision_id": "DEC3016_2_project_status",
            "decision": "3016 is real progress but not a PPN pass",
            "rationale": "one kernel became algebraic and one zero theorem became precise; neither provides a valid prediction row today",
            "consequence": "continue derivation-first, with a hard nonclaim ceiling",
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3016_0_3017",
            "target_doc": "3017-Y5-R2FR-source-current-Ward-owner-for-alpha3-or-gamma-coefficient-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_source_current_Ward_owner_for_alpha3_or_gamma_coefficient_fill_under_AX1090_3017.py",
            "mission": "try to parent-sign the source-current Ward/no-flux conditions that would force alpha3=0; if that fails, fill the gamma coefficient input contract A_T/A_S/s_R and keep alpha3 as explicit nonclaim residual",
            "success_condition": "either alpha3 gets a signed theorem-zero route from parent conservation, or the precise missing Ward/current/boundary clauses are recorded and gamma coefficient acquisition becomes the next concrete fill",
            "forbidden": "no alpha3 claim from comparator alone; no fitted-GM shortcut; no gamma-only local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["gamma_kernel"], gamma_kernel)
write_csv(OUTPUTS["alpha3_audit"], alpha3_audit)
write_csv(OUTPUTS["first_rows"], first_rows)
write_csv(OUTPUTS["fixed_gm_gamma"], fixed_gm_gamma)
write_csv(OUTPUTS["blockers"], blockers)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("gamma_copy", "gamma_kernel"),
    ("alpha3_copy", "alpha3_audit"),
    ("first_rows_copy", "first_rows"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3016_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = (
    source_register
    + gamma_kernel
    + alpha3_audit
    + first_rows
    + fixed_gm_gamma
    + blockers
    + promotion_gates
    + decision
    + next_target
)

validation_rows = [
    {
        "validation_id": "VAL3016_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": OUTPUTS["sources"].name,
    },
    {
        "validation_id": "VAL3016_01_csv_parse",
        "passed": all(csv_ok(path) for path in all_csv),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all generated CSV artifacts import with csv.DictReader",
    },
    {
        "validation_id": "VAL3016_02_gamma_kernel_written",
        "passed": any(row["gamma_id"] == "GAM3016_0_PPN_ratio_definition" for row in gamma_kernel)
        and any("2 s_R/(1-s_R)" in row["formula"] for row in gamma_kernel),
        "requirement": "gamma weak-field coefficient-ratio and conformal special case are written",
        "evidence": OUTPUTS["gamma_kernel"].name,
    },
    {
        "validation_id": "VAL3016_03_alpha3_zero_audit_written",
        "passed": any(row["alpha3_id"] == "A3Z3016_5_total_alpha3_gate" for row in alpha3_audit)
        and all(not boolish(row.get("valid_for_claim")) for row in alpha3_audit),
        "requirement": "alpha3 source-current zero/bound theorem audit exists and remains nonclaim",
        "evidence": OUTPUTS["alpha3_audit"].name,
    },
    {
        "validation_id": "VAL3016_04_fixed_GM_ratio_guard_active",
        "passed": any(row["guard_id"] == "FGG3016_0_common_scale" for row in fixed_gm_gamma)
        and any(row["gate_id"] == "GATE3016_4_fixed_GM_guard" and boolish(row["result"]) for row in promotion_gates),
        "requirement": "fixed measured-GM cannot absorb gamma ratio residual",
        "evidence": OUTPUTS["fixed_gm_gamma"].name,
    },
    {
        "validation_id": "VAL3016_05_claims_blocked",
        "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows)
        and any(row["gate_id"] == "GATE3016_5_PPN_local_GR_claim" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "PPN/local-GR claims remain blocked",
        "evidence": OUTPUTS["gates"].name,
    },
    {
        "validation_id": "VAL3016_06_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "all 3016 generated ledgers",
    },
    {
        "validation_id": "VAL3016_07_branch_copies_exist",
        "passed": all(boolish(row["exists"]) for row in branch_rows),
        "requirement": "branch copies and acquisition queue exist",
        "evidence": OUTPUTS["branches"].name,
    },
    {
        "validation_id": "VAL3016_08_outputs_scoped",
        "passed": all(under(path, ROOT) for path in all_generated),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3016_09_formalization_not_targeted",
        "passed": not any(under(path, FORMALIZATION) for path in all_generated),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3016_10_next_target_selected",
        "passed": next_target[0]["target_doc"].startswith("3017-Y5_R2FR".replace("_", "-")) is False
        or next_target[0]["target_doc"].startswith("3017-Y5-R2FR-source-current-Ward-owner"),
        "requirement": "next target selects source-current Ward owner or gamma coefficient fill",
        "evidence": OUTPUTS["next"].name,
    },
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3016_99_overall",
        "passed": overall_pass,
        "requirement": "all 3016 validation checks pass",
        "evidence": "aggregate of VAL3016_00 through VAL3016_10",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3016 - Gamma and Alpha3 PPN Kernel First Derivation under AX1090

Status: `Y5_R2FR_3016_gamma_kernel_derived_alpha3_zero_theorem_unsigned`

## Verdict

3016 is a real step toward the GR/Newton reduction, but it is not a PPN pass.

The `gamma` row now has a concrete weak-field kernel. If the observed metric is

`g00=-1+2 A_T U/c^2+O(c^-4)` and `gij=(1+2 A_S U/c^2) delta_ij+O(c^-4)`,

then the fixed measured-`GM` convention defines `U_obs=A_T U`, so

`gamma_eff=A_S/A_T`, and therefore `gamma-1=(A_S-A_T)/A_T`.

The common conformal special case imported from 2489 is

`gamma-1=2 s_R/(1-s_R)`.

That is progress: `gamma` is no longer just a placeholder. But `A_T`, `A_S`, `s_R`, readout gauge, and full-vector closure are still missing, so no `gamma` or local-GR claim is allowed.

The `alpha3` row is sharper and nastier. It is not a coefficient-ratio problem; it is a conservation/source-current problem. The local branch needs a parent-signed Ward/no-flux theorem that kills `Delta_w_eff`, `J_NH`, and `Q_edge`, or it must carry the componentwise residual bound

`|alpha3| <= |C_exchange Delta_w_eff| + |C_NH J_NH| + |C_boundary Q_edge|`.

Because the comparator is `4e-20`, this is the pressure point. The best next move is source-current Ward ownership, not broad scoring.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Gamma Kernel Derivation

{md_table(gamma_kernel, ["gamma_id", "object", "formula", "status", "missing_for_claim"])}

## Alpha3 Zero-Theorem Audit

{md_table(alpha3_audit, ["alpha3_id", "object", "zero_condition", "status", "missing_for_claim"])}

## First PPN Rows

{md_table(first_rows, ["row_id", "observable", "kernel_formula", "bound", "status", "blocks_claim"])}

## Fixed GM Gamma Guard

{md_table(fixed_gm_gamma, ["guard_id", "rule", "mathematical_form", "status", "blocks"])}

## Blocker Ledger

{md_table(blockers, ["blocker_id", "blocking_condition", "precise_missing_object", "next_attack"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["gamma_kernel"]}`
- `{OUTPUTS["alpha3_audit"]}`
- `{OUTPUTS["first_rows"]}`
- `{OUTPUTS["fixed_gm_gamma"]}`
- `{OUTPUTS["blockers"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["gamma_copy"]}`
- `{BRANCH_OUTPUTS["alpha3_copy"]}`
- `{BRANCH_OUTPUTS["first_rows_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No PPN/local-GR pass claim.
- No fitted-`GM` absorption of the `A_S/A_T` gamma ratio.
- No `alpha3` claim without a parent-signed Ward/source-current/no-flux theorem or source-backed numeric bound.
- No gamma-only local-GR claim.
- No hidden cancellation across PPN components.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
