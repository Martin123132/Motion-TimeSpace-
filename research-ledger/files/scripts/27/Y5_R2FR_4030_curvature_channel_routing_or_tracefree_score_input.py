from __future__ import annotations

import csv
import hashlib
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main\post-checkpoint-work"
)
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4030-Y5-R2FR-curvature-channel-routing-or-tracefree-score-input.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4030_SOURCE_REGISTER.csv",
    "eh_routing": SOURCE_DIR / "P8_Y5_R2FR_4030_EH_CHANNEL_ROUTING.csv",
    "newton_coupling": SOURCE_DIR / "P8_Y5_R2FR_4030_NEWTON_COUPLING_RENORMALIZATION.csv",
    "curvature_residual": SOURCE_DIR / "P8_Y5_R2FR_4030_CURVATURE_RESIDUAL_SPLIT.csv",
    "score_inputs": SOURCE_DIR / "P8_Y5_R2FR_4030_TRACEFREE_SCORE_INPUTS.csv",
    "evaluator_cases": SOURCE_DIR / "P8_Y5_R2FR_4030_EVALUATOR_CASES.csv",
    "evaluator_results": SOURCE_DIR / "P8_Y5_R2FR_4030_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4030_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4030_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4030_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4030_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4030_VALIDATION.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def short_hash(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "SRC4030_0_4029_doc",
            "path": "4029-Y5-R2FR-phi-owner-sign-convention-or-tracefree-residual-bound-input.md",
            "needle": "phi*G_TF",
            "role": "selects the curvature channel as the leading obstruction",
        },
        {
            "source_id": "SRC4030_1_4029_residual",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4029_TRACEFREE_RESIDUAL_REDUCTION.csv",
            "needle": "DTF4029_2_surviving_obstruction",
            "role": "provides the reduced D_TF residual law",
        },
        {
            "source_id": "SRC4030_2_4029_energy",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4029_PHI_LOCAL_VACUUM_ENERGY_IDENTITY.csv",
            "needle": "LOCAL_VACUUM_PHI_SILENCE_DERIVED_CONDITIONALLY",
            "role": "supports delta_phi silence on compact local fixed branch",
        },
        {
            "source_id": "SRC4030_3_4021_witness",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4021_PARENT_LOCAL_ACTION_WITNESS.csv",
            "needle": "S_loc^{<=2PN}",
            "role": "provides EH local action witness with kappa_*",
        },
        {
            "source_id": "SRC4030_4_4021_newton",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4021_DERIVED_ZERO_LEMMAS.csv",
            "needle": "G_ref is calibrated",
            "role": "records the Newtonian readout stance: calibrated G, not numeric-G prediction",
        },
        {
            "source_id": "SRC4030_5_constant_kappa",
            "path": "source-intake/mts_residuals/P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv",
            "needle": "D_X kappa_eff = 0",
            "role": "provides conditional constant-coupling theorem route",
        },
        {
            "source_id": "SRC4030_6_kappa_gate",
            "path": "source-intake/mts_residuals/P8_CONSTANT_KAPPA_GATE_TESTS.csv",
            "needle": "G508_1_parent_adoption",
            "role": "prevents overclaiming constant kappa without parent adoption",
        },
        {
            "source_id": "SRC4030_7_charge_current",
            "path": "source-intake/mts_residuals/P8_charge_current_equality_DIRECT_ATTEMPT.csv",
            "needle": "C_xi^EH = kappa_eff",
            "role": "connects EH constraint source link to Newton/source normalization",
        },
    ]


def build_source_register(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        full = ROOT / spec["path"]
        text = read_text(full)
        rows.append(
            {
                **spec,
                "absolute_path": str(full),
                "exists": full.exists(),
                "needle_found": spec["needle"] in text,
                "sha256_16": short_hash(full),
                "timestamp_utc": ts,
            }
        )
    return rows


def build_eh_routing(ts: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "EHR4030_0_combined_action",
            "object": "EH plus improvement channel",
            "formula": "I_EH+I_imp=int sqrt|g|[(1/(2*kappa_*))+c_I*phi]R",
            "meaning": "the phi*G term is not automatically a fifth-force residual; its constant part belongs to the EH operator coefficient",
            "status": "ROUTING_FORMULA_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "route_id": "EHR4030_1_split_phi",
            "object": "fixed branch split",
            "formula": "phi=phi_*+delta_phi",
            "meaning": "phi_* renormalizes the local Einstein-Hilbert coefficient; delta_phi is the physical scalar-tensor hair",
            "status": "CONSTANT_AND_HAIR_SPLIT",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "route_id": "EHR4030_2_observed_kappa",
            "object": "observed Newton coupling",
            "formula": "1/(2*kappa_obs)=1/(2*kappa_*)+c_I*phi_*",
            "meaning": "kappa_obs=1/(1/kappa_*+2*c_I*phi_*); G_obs=c^4*kappa_obs/(8*pi)",
            "status": "NEWTON_COUPLING_RENORMALIZATION_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "route_id": "EHR4030_3_curvature_routing",
            "object": "trace-free curvature term",
            "formula": "2*c_I*phi*G_TF = EH_renormalization(phi_*) + 2*c_I*delta_phi*G_TF",
            "meaning": "constant phi_* is calibrated with EH/Newton; only delta_phi*G_TF remains in D_TF",
            "status": "CURVATURE_CHANNEL_REDUCED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_newton_coupling(ts: str) -> list[dict[str, object]]:
    return [
        {
            "coupling_id": "NC4030_0_not_numeric_prediction",
            "statement": "MTS need not numerically derive the laboratory value of G at this stage; GR also treats it as a coupling calibrated by source response",
            "mathematical_form": "G_obs=c^4/(8*pi)/(1/kappa_*+2*c_I*phi_*)",
            "discipline": "this is a derived relation between parent constants and the measured local coupling, not a claim of numeric prediction",
            "status": "CALIBRATION_STANCE_CLARIFIED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "coupling_id": "NC4030_1_constancy_condition",
            "statement": "observed G is locally constant if kappa_* and phi_* live in global/fixed sectors and delta_phi has no local fixed-branch hair",
            "mathematical_form": "D_X ln G_obs=0 if D_X kappa_*=D_X phi_*=0 and delta_phi=0",
            "discipline": "local drift/species/range residuals remain active unless these sector clauses are adopted",
            "status": "CONDITIONAL_CONSTANT_G_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "coupling_id": "NC4030_2_bianchi_guard",
            "statement": "a spacetime-varying kappa_eff cannot be hidden; Bianchi identity turns it into exchange/source nonconservation unless compensated",
            "mathematical_form": "nabla_mu[(1/kappa_eff)G^{mu nu}]=0 implies source exchange when nabla_mu kappa_eff != 0",
            "discipline": "delta_phi hair must be zero, routed, or scored",
            "status": "BIANCHI_GUARD_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_curvature_residual(ts: str) -> list[dict[str, object]]:
    return [
        {
            "residual_id": "CURV4030_0_reduced_DTF",
            "component": "D_TF",
            "formula": "D_TF=(1-c_I)K_L + 2*c_I*delta_phi*G_TF + D_phiF + D_owner + D_boundary + D_adoption + D_kappa_sector",
            "removed_piece": "2*c_I*phi_*G_TF is absorbed into kappa_obs/EH channel",
            "survives": "delta_phi*G_TF plus adoption and boundary/source-sector residuals",
            "status": "CURVATURE_RESIDUAL_SPLIT_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "CURV4030_1_local_exterior",
            "component": "solar-system exterior branch",
            "formula": "if T_H=0 exterior and EH equation holds with constant kappa_obs, then G_TF=0 and delta_phi=0 gives D_TF=0",
            "removed_piece": "exterior vacuum curvature obstruction",
            "survives": "source boundary matching and interior/source-normalization residuals",
            "status": "EXTERIOR_ZERO_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "CURV4030_2_source_region",
            "component": "inside/near matter sources",
            "formula": "G_TF=kappa_obs*T_TF plus non-EH residuals, so delta_phi*G_TF is bounded by |delta_phi|*|T_TF| and source-channel maps",
            "removed_piece": "none inside source unless delta_phi=0 or source routing is proven",
            "survives": "A_delta_phiG/L_phiG and C_beta_TF",
            "status": "SOURCE_REGION_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "CURV4030_3_nonclaim",
            "component": "claim gate",
            "formula": "curvature routing is sufficient only under parent adoption of kappa/phi sectors and same-source Hilbert current",
            "removed_piece": "mathematical overclaim",
            "survives": "live adoption row and PPN score inputs",
            "status": "NO_LOCAL_GR_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_score_inputs(ts: str) -> list[dict[str, object]]:
    return [
        {
            "input_id": "SCORE4030_0_reduced_tracefree_bound",
            "quantity": "A_TF/L_TF",
            "formula": "A_TF/L_TF <= |1-c_I|A_KL/L_KL + 2|c_I|A_delta_phiG/L_phiG + A_phiF/L_phiF + A_boundary/L_boundary + A_adoption/L_adoption + A_kappa/L_kappa",
            "needed_for_score": "numeric/source-backed amplitudes plus C_beta_TF",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "input_id": "SCORE4030_1_delta_phiG",
            "quantity": "A_delta_phiG/L_phiG",
            "formula": "A_delta_phiG/L_phiG <= A_delta_phi*A_GTF/L_GTF or zero if delta_phi=0 by local fixed-branch theorem",
            "needed_for_score": "delta_phi amplitude from phi owner branch and source/exterior G_TF arena",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "input_id": "SCORE4030_2_newton_bridge",
            "quantity": "kappa_obs",
            "formula": "kappa_obs=1/(1/kappa_*+2*c_I*phi_*)",
            "needed_for_score": "same-source Hilbert current and constant-sector adoption; no numeric-G prediction required",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "input_id": "SCORE4030_3_ppn_projector",
            "quantity": "delta_beta_TF",
            "formula": "delta_beta_TF=C_beta_TF*(A_TF/L_TF)",
            "needed_for_score": "derive C_beta_TF from weak-field metric equation after EH renormalization",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_cases(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4030_0_all_constant",
            "input_condition": "c_I=1, phi=phi_*, constant sectors adopted, same-source EH current",
            "expected_verdict": "CURVATURE_CHANNEL_ROUTED_TO_EH_NEWTON_COUPLING",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4030_1_current",
            "input_condition": "current source hierarchy after 4030",
            "expected_verdict": "CURVATURE_CHANNEL_REDUCED_NOT_LIVE_ADOPTED",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4030_2_score",
            "input_condition": "delta_phi or source curvature survives",
            "expected_verdict": "TRACEFREE_SCORE_INPUTS_DEFINED_NOT_NUMERIC",
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_results(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4030_0_all_constant",
            "verdict": "CURVATURE_CHANNEL_ROUTED_TO_EH_NEWTON_COUPLING_IF_ADOPTED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4030",
            "next_action": "then continue to boundary/adoption/source-current closure",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4030_1_current",
            "verdict": "CURVATURE_CHANNEL_REDUCED_NOT_LIVE_ADOPTED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4030",
            "next_action": "4031 should derive the weak-field C_beta_TF projector or prove delta_phi=0 on the exterior collar",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4030_2_score",
            "verdict": "TRACEFREE_SCORE_INPUTS_DEFINED_NOT_NUMERIC",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4030",
            "next_action": "source A_delta_phiG/L_phiG and C_beta_TF if theorem route fails",
            "timestamp_utc": ts,
        },
    ]


def build_decisions(ts: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC4030_0_EH_route",
            "decision": "route constant phi_*G_TF into the EH/Newton coupling rather than counting it as a fifth-force residual",
            "status": "CURVATURE_ROUTE_ADVANCED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4030_1_G_relation",
            "decision": "record kappa_obs=1/(1/kappa_*+2*c_I*phi_*) as a derived coupling relation, not a numeric prediction of G",
            "status": "NEWTON_BRIDGE_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4030_2_residual",
            "decision": "retain delta_phi*G_TF, boundary/adoption and kappa-sector failures as explicit residuals",
            "status": "NO_CLOSURE_SMUGGLING",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4030_3_next",
            "decision": "move to 4031-Y5-R2FR-exterior-collar-deltaphi-zero-or-CbetaTF-projector.md",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_claims(ts: str) -> list[dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4030_0_curvature_closed",
            "claim": "phi*G_TF obstruction is fully closed",
            "allowed": False,
            "reason": "constant part is routed, but delta_phi/source/adoption terms remain",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4030_1_G_predicted",
            "claim": "MTS predicts the numerical value of Newton's constant",
            "allowed": False,
            "reason": "4030 derives a coupling relation and calibration route only",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4030_2_ppn_pass",
            "claim": "PPN/local-GR branch passes",
            "allowed": False,
            "reason": "C_beta_TF and full source/adoption closure are still missing",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4030_3_public_claim",
            "claim": "public q_loc/local-GR claim",
            "allowed": False,
            "reason": "checkpoint remains private nonclaim",
            "timestamp_utc": ts,
        },
    ]


def build_next_target(ts: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NEXT4030_0",
            "next_doc": "4031-Y5-R2FR-exterior-collar-deltaphi-zero-or-CbetaTF-projector.md",
            "next_script": "scripts/Y5_R2FR_4031_exterior_collar_deltaphi_zero_or_CbetaTF_projector.py",
            "why": "after EH routing, the fastest path is either prove delta_phi=0 on the exterior collar or derive the weak-field beta projector",
            "fallback": "if exterior theorem fails, create numeric schema for A_delta_phiG/L_phiG and C_beta_TF",
            "timestamp_utc": ts,
        }
    ]


def build_status(ts: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS4030_0",
            "checkpoint": "4030",
            "headline": "constant phi curvature channel routed into EH/Newton coupling; delta_phi residual retained",
            "verdict": "CURVATURE_CHANNEL_REDUCED_NOT_LIVE_ADOPTED",
            "claim_allowed": False,
            "formalization_workbench_modified": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: list[dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    return f"""# 4030 - Curvature Channel Routing Or Tracefree Score Input

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

The surviving `phi*G_TF` term from 4029 is not all the same kind of physics. Combine the Einstein-Hilbert and improvement terms:

`I_EH+I_imp=int sqrt|g|[(1/(2*kappa_*))+c_I*phi]R`.

Split

`phi=phi_*+delta_phi`.

Then the constant branch defines the observed coupling

`1/(2*kappa_obs)=1/(2*kappa_*)+c_I*phi_*`,

so

`kappa_obs=1/(1/kappa_*+2*c_I*phi_*)` and `G_obs=c^4*kappa_obs/(8*pi)`.

This means constant `phi_*G_TF` is not a new force; it is part of the EH/Newton coupling calibration. The physical residual is the hair:

`2*c_I*delta_phi*G_TF`.

## Reduced Trace-Free Residual

After EH routing,

`D_TF=(1-c_I)K_L + 2*c_I*delta_phi*G_TF + D_phiF + D_owner + D_boundary + D_adoption + D_kappa_sector`.

This is a narrower obstruction than 4029.

## Newton Constant Stance

4030 does not claim to predict the numerical value of `G`. It derives how the local observed coupling is built from parent constants. That is compatible with the GR/Newton ladder: the theory must reduce to Newton with a calibrated coupling, while separately proving the coupling is constant/universal or bounding drift.

## Current Verdict

- Current evaluator result: `CURVATURE_CHANNEL_REDUCED_NOT_LIVE_ADOPTED`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4030`.
- Source needles found: `{found}/{len(sources)}`.

## Next Target

- `4031-Y5-R2FR-exterior-collar-deltaphi-zero-or-CbetaTF-projector.md`
- `scripts/Y5_R2FR_4031_exterior_collar_deltaphi_zero_or_CbetaTF_projector.py`
"""


def add_validation(rows: list[dict[str, object]], check_id: str, passed: bool, detail: str, ts: str) -> None:
    rows.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts})


def build_validation_rows(
    ts: str,
    sources: list[dict[str, object]],
    eh_routing: list[dict[str, object]],
    coupling: list[dict[str, object]],
    residual: list[dict[str, object]],
    score_inputs: list[dict[str, object]],
    results: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_target: list[dict[str, object]],
    compile_ok: bool,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    route_ids = {str(row["route_id"]) for row in eh_routing}
    coupling_ids = {str(row["coupling_id"]) for row in coupling}
    residual_ids = {str(row["residual_id"]) for row in residual}
    input_ids = {str(row["input_id"]) for row in score_inputs}
    verdicts = {str(row["verdict"]) for row in results}

    add_validation(rows, "VAL4030_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", ts)
    add_validation(rows, "VAL4030_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found", ts)
    add_validation(rows, "VAL4030_02_combined_action", "EHR4030_0_combined_action" in route_ids, "combined EH+improvement action row present", ts)
    add_validation(rows, "VAL4030_03_phi_split", "EHR4030_1_split_phi" in route_ids, "phi split row present", ts)
    add_validation(rows, "VAL4030_04_kappa_obs", "EHR4030_2_observed_kappa" in route_ids, "kappa_obs relation row present", ts)
    add_validation(rows, "VAL4030_05_curvature_route", "EHR4030_3_curvature_routing" in route_ids, "curvature routing row present", ts)
    add_validation(rows, "VAL4030_06_not_numeric_G", "NC4030_0_not_numeric_prediction" in coupling_ids, "numeric-G nonclaim row present", ts)
    add_validation(rows, "VAL4030_07_bianchi_guard", "NC4030_2_bianchi_guard" in coupling_ids, "Bianchi guard row present", ts)
    add_validation(rows, "VAL4030_08_reduced_DTF", "CURV4030_0_reduced_DTF" in residual_ids, "reduced D_TF residual row present", ts)
    add_validation(rows, "VAL4030_09_source_region", "CURV4030_2_source_region" in residual_ids, "source-region bound row present", ts)
    add_validation(rows, "VAL4030_10_tracefree_score", "SCORE4030_0_reduced_tracefree_bound" in input_ids, "trace-free score input row present", ts)
    add_validation(rows, "VAL4030_11_projector", "SCORE4030_3_ppn_projector" in input_ids, "PPN projector row present", ts)
    add_validation(rows, "VAL4030_12_no_score_ready", all(str(row.get("score_ready", "False")) == "False" for row in score_inputs), "score inputs not claim-ready", ts)
    add_validation(rows, "VAL4030_13_current_verdict", "CURVATURE_CHANNEL_REDUCED_NOT_LIVE_ADOPTED" in verdicts, "current evaluator verdict present", ts)
    add_validation(rows, "VAL4030_14_no_claims", all(str(row.get("allowed", "False")) == "False" for row in claims), "all claim gates remain false", ts)
    add_validation(rows, "VAL4030_15_next_decision", any("4031" in str(row["decision"]) for row in decisions), "4031 next decision present", ts)
    add_validation(rows, "VAL4030_16_next_target", bool(next_target and "4031" in str(next_target[0]["next_doc"])), "next target row present", ts)
    add_validation(rows, "VAL4030_17_doc_written", DOC_PATH.exists() and "What Actually Moved" in read_text(DOC_PATH), "checkpoint doc written", ts)
    add_validation(rows, "VAL4030_18_no_formalization_output", "formalization-workbench" not in str(DOC_PATH) and all("formalization-workbench" not in str(path) for path in OUTPUTS.values()), "no output targets formalization-workbench", ts)
    add_validation(rows, "VAL4030_19_script_compiles", compile_ok, "script compiles", ts)
    add_validation(rows, "VAL4030_20_private_nonclaim", all(str(row.get("valid_for_claim", "False")) == "False" for row in eh_routing + coupling + residual + score_inputs + decisions), "all rows remain nonclaim", ts)
    return rows


def main() -> None:
    ts = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = build_source_register(ts)
    eh_routing = build_eh_routing(ts)
    coupling = build_newton_coupling(ts)
    residual = build_curvature_residual(ts)
    score_inputs = build_score_inputs(ts)
    cases = build_evaluator_cases(ts)
    results = build_evaluator_results(ts)
    decisions = build_decisions(ts)
    claims = build_claims(ts)
    next_target = build_next_target(ts)
    status = build_status(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["eh_routing"], eh_routing)
    write_csv(OUTPUTS["newton_coupling"], coupling)
    write_csv(OUTPUTS["curvature_residual"], residual)
    write_csv(OUTPUTS["score_inputs"], score_inputs)
    write_csv(OUTPUTS["evaluator_cases"], cases)
    write_csv(OUTPUTS["evaluator_results"], results)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(
        ts,
        sources,
        eh_routing,
        coupling,
        residual,
        score_inputs,
        results,
        decisions,
        claims,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4030 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
