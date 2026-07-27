from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2888-Y5-R2FR-terminal-public-coframe-no-shadow-or-Cshadow-bound-row-under-AX1090.md"

SRC_2887_DOC = ROOT / "2887-Y5-R2FR-observed-coframe-functor-or-Cobs-source-row-under-AX1090.md"
SRC_2887_NEXT = RESIDUALS / "P8_Y5_R2FR_2887_NEXT_TARGET.csv"
SRC_2887_COBS = RESIDUALS / "P8_Y5_R2FR_2887_COBS_OPERATOR_NORM_ROW_NONCLAIM.csv"
SRC_2887_UPDATE = RESIDUALS / "P8_Y5_R2FR_2887_E_DQZ_COFRAME_COMPONENT_UPDATE.csv"
SRC_2887_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2887_VALIDATION.csv"

SRC_2488_ZERO = RESIDUALS / "P8_Y5_NO_SHADOW_2488_ZERO_THEOREM.csv"
SRC_2488_COUNTER = RESIDUALS / "P8_Y5_NO_SHADOW_2488_COUNTERMODEL_LEDGER.csv"
SRC_2488_KERNEL = RESIDUALS / "P8_Y5_NO_SHADOW_2488_RESPONSE_KERNEL_ACQUISITION.csv"
SRC_2489_PPN = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PPN_RESPONSE_KERNEL.csv"
SRC_2572_ZERO = RESIDUALS / "P8_Y5_NO_SHADOW_2572_ZERO_THEOREM.csv"
SRC_2572_COUPLING = RESIDUALS / "P8_Y5_NO_SHADOW_2572_COUPLING_SHADOW_AUDIT.csv"
SRC_2631_AUDIT = RESIDUALS / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_NO_SHADOW_GATE_AUDIT.csv"
SRC_2721_FINITE = RESIDUALS / "P8_Y5_R2FR_2721_FINITE_ENORM_ESHADOW_ROWS_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2888_SOURCE_REGISTER.csv",
    "certificate": RESIDUALS / "P8_Y5_R2FR_2888_TERMINAL_PUBLIC_COFRAME_NO_SHADOW_CERTIFICATE_AUDIT.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_2888_SHADOW_COUNTERMODEL_LEDGER.csv",
    "cshadow": RESIDUALS / "P8_Y5_R2FR_2888_CSHADOW_BOUND_ROW_NONCLAIM.csv",
    "kernels": RESIDUALS / "P8_Y5_R2FR_2888_RESPONSE_KERNEL_LINKS_NONCLAIM.csv",
    "update": RESIDUALS / "P8_Y5_R2FR_2888_E_DQZ_COFRAME_SHADOW_UPDATE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2888_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2888_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2888_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2888_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2888_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2888_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "cshadow_copy": SOURCE_WEIGHT / "RAB_CSHADOW_BOUND_ROW_2888_NONCLAIM.csv",
    "kernel_copy": LOCAL_BOUNDS / "RAB_CSHADOW_RESPONSE_KERNEL_LINKS_2888_NONCLAIM.csv",
    "counter_copy": BETA_DOCS / "RAB_SHADOW_COUNTERMODELS_2888_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2888_common_frame_bR_or_PPN_kernel_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2888_0_2887_doc", SRC_2887_DOC, "Status: `Y5_R2FR_2887_Obs_e_functor_unsigned_Cobs_Cshadow_rows_2888_next`;## Next Target", "2887 handoff"),
        ("SRC2888_1_2887_next", SRC_2887_NEXT, "NEXT2887_0_2888", "explicit 2888 target"),
        ("SRC2888_2_2887_cobs", SRC_2887_COBS, "COBS2887_2_shadow_frame_guard;C_shadow", "C_shadow staged row"),
        ("SRC2888_3_2887_update", SRC_2887_UPDATE, "EDQZ2887_0_component_update;C_shadow", "E_DqZ coframe shadow update"),
        ("SRC2888_4_2887_validation", SRC_2887_VALIDATION, "VAL2887_OVERALL", "2887 validation"),
        ("SRC2888_5_2488_zero", SRC_2488_ZERO, "ZTH2488_0_exact_conditional;ZTH2488_2_current_verdict", "terminal public coframe no-shadow theorem"),
        ("SRC2888_6_2488_counter", SRC_2488_COUNTER, "CM2488_0_common_weyl;CM2488_4_qshape_forgetting", "shadow countermodel ledger"),
        ("SRC2888_7_2488_kernel", SRC_2488_KERNEL, "KER2488_0_PPN_metric_bR;KER2488_4_absolute_envelope", "response kernel acquisition"),
        ("SRC2888_8_2489_ppn", SRC_2489_PPN, "PPNK2489_0_conformal_gamma_kernel;PPNK2489_3_disformal_preferred_frame_placeholder", "first common-frame PPN kernel"),
        ("SRC2888_9_2572_zero", SRC_2572_ZERO, "ZTH2572_0_exact_conditional_no_shadow;ZTH2572_3_current_verdict", "no-shadow action-domain theorem"),
        ("SRC2888_10_2572_coupling", SRC_2572_COUPLING, "CS2572_0_kappa_MTS;CS2572_4_no_absorption_guard", "coupling shadow audit"),
        ("SRC2888_11_2631_audit", SRC_2631_AUDIT, "NSG2631_1_terminal_public_coframe;NSG2631_4_verdict", "PPN vector no-shadow audit"),
        ("SRC2888_12_2721_finite", SRC_2721_FINITE, "FSN2721_6_E_shadow_species;SOURCE_READY_SCHEMA_NONCLAIM", "finite E_shadow schema row"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def certificate_rows() -> list[dict[str, Any]]:
    specs = [
        ("NSC2888_0_exact", "exact no-shadow theorem", "If terminal e_pub=E(Q_vis), no hidden metric/source/endpoint slot is in action/readout domain, and inherited maps have no independent hidden argument, then b_R=d_R=w_R=epsilon_endpoint_R=0.", "EXACT_CONDITIONAL_THEOREM", "2488/2572 prove the conditional functional-derivative theorem", "requires action-domain exclusion and coefficient owners"),
        ("NSC2888_1_terminal_coframe", "terminal public coframe", "ordinary matter, rods, clocks and photons use one terminal public coframe rather than a representative-dependent frame", "NOT_PARENT_SIGNED", "would set common Weyl/disformal coframe shadows to zero", "terminality/action-domain premise unsigned"),
        ("NSC2888_2_no_weyl_disformal", "no Weyl/disformal representative slot", "no A_R(C_R), D_R(C_R)u_mu u_nu or equivalent hidden representative slot is a legal observable argument", "CLOSURE_ONLY_COUNTERMODEL_RETAINED", "would kill b_R and d_R shadow heads", "2488 and 2631 retain countermodels"),
        ("NSC2888_3_no_source_prefactor", "no source-prefactor shadow", "no w_R(C_R) source-only/action prefactor survives before variation", "NO_SOURCE_PREFACTOR_NOT_DERIVED", "would kill source-shadow head w_R", "source-side no-prefactor route remains separate and unsigned"),
        ("NSC2888_4_no_endpoint", "no endpoint/boundary shadow", "boundary/reference/endpoint data are local-projector silent or separately bounded", "ENDPOINT_BOUNDARY_UNSIGNED", "would kill epsilon_endpoint_R", "endpoint/readout kernels remain missing"),
        ("NSC2888_5_coupling_shadow", "no visible-coupling shadow", "kappa_MTS, ell_J, constants and source support are q-basic, fixed before readout, and not inferred from same local tests", "COUPLING_OWNER_UNSIGNED", "would kill coupling/readout shadow tails", "2572 coupling audit keeps owner rows unsigned"),
        ("NSC2888_6_verdict", "terminal public coframe no-shadow certificate", "all no-shadow clauses close in one parent branch", "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS", "do not set C_shadow=0", "fill nonclaim C_shadow_abs envelope"),
    ]
    return [
        add_common(
            {
                "certificate_id": certificate_id,
                "clause": clause,
                "formal_statement": statement,
                "current_status": status,
                "if_signed": if_signed,
                "current_blocker": blocker,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for certificate_id, clause, statement, status, if_signed, blocker in specs
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    specs = [
        ("CM2888_0_common_weyl", "e_obs=exp(b_R C_R)e_pub", "universal coframe can depend on a hidden representative and shift metric/clock/PPN readout", "same-frame;WEP;covariance", "derive b_R=0 by action-domain exclusion or source b_R response row"),
        ("CM2888_1_common_disformal", "g_obs=A(C_R)^2g_pub+D(C_R)u_mu u_nu", "covariant preferred-frame/disformal dependence survives if current/domain vector is legal", "covariance;single-public-metric", "derive no disformal/current slot or source preferred-frame kernel"),
        ("CM2888_2_source_prefactor", "S_matter includes sum_A w_A(C_R)L_A", "source normalization can move while metric coframe remains common", "metric-only readout;Ward", "derive no source-only slot or source WEP/clock/R10 source-leg bounds"),
        ("CM2888_3_endpoint_boundary", "e_obs=E(Q_vis,Q_endpoint)", "boundary/reference endpoint data can leak after declaring a public coframe", "bulk coframe descent", "derive endpoint silence or source orbital/light-time kernel"),
        ("CM2888_4_qshape_forgetting", "Dq_shape[v_R]=0 while DObs_e[v_R] != 0", "cheap verticality in one quotient does not imply rods/clocks/photons forget it", "q_shape;label forgetting", "derive observed readout functor basicity or retain finite DObs rows"),
    ]
    return [
        add_common(
            {
                "countermodel_id": countermodel_id,
                "ansatz": ansatz,
                "why_it_survives": survives,
                "kills_shortcut": kills,
                "required_fix": fix,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for countermodel_id, ansatz, survives, kills, fix in specs
    ]


def cshadow_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "row_id": "CSH2888_0_C_shadow_abs",
                "symbol": "C_shadow_abs",
                "definition": "absolute no-cancellation envelope for representative Weyl/disformal/source/endpoint/coefficient shadows that bypass terminal Obs_e(Q_vis)",
                "formula": "C_shadow_abs := |b_R| + |d_R| + |w_R| + |epsilon_endpoint_R| + |epsilon_coupling_shadow| + |epsilon_readout_shadow|",
                "units": "dimensionless envelope before arena projection",
                "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "lower_bound": "0",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_paths": f"{SRC_2488_ZERO}; {SRC_2488_COUNTER}; {SRC_2488_KERNEL}; {SRC_2572_ZERO}; {SRC_2572_COUPLING}; {SRC_2721_FINITE}",
                "required_source_inputs": "no-shadow theorem or finite b_R,d_R,w_R,endpoint,coupling/readout shadow coefficients; units; fixed baseline; no-cancellation envelope",
                "projection_formula": "E_DqZ_coframe_total <= C_Obs_e*Dq_Z_norm*N_Z + C_shadow_abs + endpoint/readout tails",
                "current_status": "SOURCE_READY_ENVELOPE_VALUE_MISSING",
                "promotion_rule": "promote only if every head is theorem-zero or source-backed finite with no MISSING_* markers; do not use cancellations or fitted baselines",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "row_id": "CSH2888_1_b_R_common_weyl",
                "symbol": "b_R",
                "definition": "common Weyl shadow coefficient in e_obs=exp(b_R C_R)e_pub or sigma_R=b_R C_R",
                "formula": "gamma_eff=(1+s_R)/(1-s_R), s_R=b_R x_U; Cassini bounds s_R conditionally, not b_R alone",
                "units": "dimensionless coefficient after C_R profile normalization",
                "candidate_value": "MISSING_b_R_VALUE",
                "lower_bound": "MISSING_SOURCE_BACKED_LOWER_BOUND",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_paths": f"{SRC_2488_COUNTER}; {SRC_2489_PPN}",
                "required_source_inputs": "b_R parent coefficient or theorem-zero; x_U/C_R profile; no-other-PPN-channel proof; beta/vector guard",
                "projection_formula": "|gamma-1| <= K_PPN_b |b_R| + other absolute residual heads",
                "current_status": "CONDITIONAL_PPN_KERNEL_EXISTS_VALUE_MISSING",
                "promotion_rule": "Cassini bound is a comparator only until b_R and x_U are parent-sourced",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "row_id": "CSH2888_2_d_R_disformal",
                "symbol": "d_R",
                "definition": "common disformal/preferred-frame shadow coefficient",
                "formula": "g_obs=A(C_R)^2g_pub + D(C_R)u_mu u_nu; preferred-frame kernels needed",
                "units": "dimensionless after vector/current normalization",
                "candidate_value": "MISSING_d_R_VALUE",
                "lower_bound": "MISSING_SOURCE_BACKED_LOWER_BOUND",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_paths": f"{SRC_2488_COUNTER}; {SRC_2489_PPN}; {SRC_2631_AUDIT}",
                "required_source_inputs": "no disformal slot theorem or finite D(C_R) coefficient; vector normalization; alpha_i/xi projection",
                "projection_formula": "Delta alpha_i <= K_alpha_i_dR |d_R| + endpoint/domain tails",
                "current_status": "PREFERRED_FRAME_KERNEL_MISSING",
                "promotion_rule": "must be zeroed or bounded independently from b_R",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def kernel_rows() -> list[dict[str, Any]]:
    specs = [
        ("KER2888_0_PPN_metric", "PPN metric gamma/beta", "|delta gamma|+|delta beta| <= K_PPN_b|b_R| + K_PPN_d|d_R| + K_PPN_endpoint|epsilon_endpoint_R|", "MISSING_RESPONSE_KERNEL_OR_COMPONENT_VALUES", "best first local-GR probe of common frame leak"),
        ("KER2888_1_clock_WEP", "clock/WEP source normalization", "|delta clock|+|eta_WEP| <= K_clock_b|b_R| + K_WEP_w|w_R| + material_terms", "MISSING_MATERIAL_MAP_TAU_KERNEL", "tests source/clock shadows not seen in metric-only pass"),
        ("KER2888_2_orbital", "orbital/light-time", "|delta a|+|delta light_time| <= K_orb_b|b_R|+K_orb_d|d_R|+K_orb_end|epsilon_endpoint_R|", "MISSING_ORBITAL_ENDPOINT_KERNEL", "captures endpoint and light-time leakage"),
        ("KER2888_3_R10_guard", "R10 guarded branch", "source shadow can feed R10 only after finite-range operator and source/test charge split exist", "HELD_LATER_WRONG_ROUTE_GUARD", "prevents common-frame coupling from masquerading as R10 prediction"),
        ("KER2888_4_absolute", "all local arenas", "C_shadow_abs enters additively with no cancellation", "MISSING_NUMERIC_OR_THEOREM_ZERO_FOR_ALL_COMPONENTS", "local pass requires each head zeroed or bounded"),
    ]
    return [
        add_common(
            {
                "kernel_id": kernel_id,
                "arena": arena,
                "candidate_relation": relation,
                "current_status": status,
                "reason_for_priority": reason,
                "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "comparison_ready": False,
                "accepted_for_scoring": False,
            }
        )
        for kernel_id, arena, relation, status, reason in specs
    ]


def update_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "update_id": "EDQZ2888_0_shadow_update",
                "component_id": "DQC2886_0_E_DqZ_coframe",
                "symbol": "E_DqZ_coframe",
                "previous_status": "COMPONENT_SCHEMA_SHARPENED_COBS_VALUE_MISSING",
                "new_information": "C_shadow is refined into C_shadow_abs plus b_R/d_R component heads; no zero theorem or finite value is adopted",
                "updated_formula": "E_DqZ_coframe_total <= Pi_coframe*C_Obs_e*Dq_Z_norm*N_Z + C_shadow_abs + E_theta_coframe + E_readout_coframe + E_boundary_coframe",
                "current_value": "MISSING_COMPONENT_VALUES",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "current_status": "SHADOW_ENVELOPE_DEFINED_VALUES_MISSING",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2888_0_no_shadow", "terminal public coframe no-shadow theorem closes", "FAIL", "theorem is exact conditional only; action-domain/coefficient-owner premises remain unsigned"),
        ("GATE2888_1_cshadow_zero", "C_shadow_abs=0 is parent-derived", "FAIL", "common Weyl, disformal, source-prefactor and endpoint countermodels survive"),
        ("GATE2888_2_cshadow_bound", "C_shadow_abs has finite source-backed interval", "FAIL", "b_R,d_R,w_R,endpoint,coupling/readout values are missing"),
        ("GATE2888_3_kernel_score", "response kernels can score", "FAIL", "kernels lack component values and full-vector/no-cancellation closure"),
        ("GATE2888_4_local_claim", "local GR/Newton/PPN/WEP follows", "FAIL", "shadow row is nonclaim and other local residual gates remain open"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2888_0_shadow_runner",
                "status": "REFUSED_CSHADOW_VALUES_MISSING",
                "accepted_no_shadow_certificates": 0,
                "accepted_cshadow_rows": 0,
                "accepted_kernel_rows": 0,
                "reason": "C_shadow_abs is source-ready but contains missing component values; no no-shadow/local comparison is allowed",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2888_0_theorem", "NO_SHADOW_ZERO_NOT_DERIVED", "The conditional theorem is exact, but current evidence does not sign terminal coframe/action-domain exclusion and coefficient owners.", "do not set C_shadow=0"),
        ("DEC2888_1_row", "INSTALL_CSHADOW_ABS_ENVELOPE", "The surviving shadow risk is now an absolute no-cancellation envelope over b_R,d_R,w_R,endpoint,coupling/readout heads.", "use this as the finite nonclaim bound row"),
        ("DEC2888_2_next", "SELECT_bR_OR_PPN_KERNEL_NEXT", "b_R has the cleanest existing conditional PPN-gamma kernel, but b_R/x_U/no-other-channel inputs are missing.", "try b_R zero theorem or first common-frame PPN kernel row next"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "accepted_for_scoring": False,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2888_0_2889",
                "status": "selected_primary",
                "target_doc": "2889-Y5-R2FR-common-frame-bR-zero-or-first-PPN-kernel-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_common_frame_bR_zero_or_first_PPN_kernel_row_under_AX1090_2889.py",
                "mission": "try to derive b_R=0 from the terminal public coframe action-domain exclusion; if it fails, fill the first source-ready nonclaim common-Weyl PPN kernel row with b_R/x_U/no-other-channel blockers",
                "forbidden_shortcuts": "no b_R=0 from preferred frame language; no Cassini bound as MTS prediction without b_R and x_U; no gamma-only local-GR claim; no cancellation; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2888_0_cshadow_copy", OUTPUTS["cshadow"], BRANCH_OUTPUTS["cshadow_copy"], "source-weight copy of C_shadow_abs bound row"),
        ("BR2888_1_kernel_copy", OUTPUTS["kernels"], BRANCH_OUTPUTS["kernel_copy"], "local-bounds copy of shadow response kernel links"),
        ("BR2888_2_counter_copy", OUTPUTS["countermodels"], BRANCH_OUTPUTS["counter_copy"], "beta-source docs copy of shadow countermodels"),
        ("BR2888_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows = []
    for copy_id, source, destination, purpose in copy_specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_signed",
        "theorem_zero_adopted",
        "finite_value_present",
        "prediction_source_backed",
        "accepted_for_scoring",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "comparison_ready",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    certificate = rows_by_name["certificate"]
    countermodels = rows_by_name["countermodels"]
    cshadow = rows_by_name["cshadow"]
    kernels = rows_by_name["kernels"]
    update = rows_by_name["update"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2888_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2888_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2888_2_no_shadow_not_adopted", any(row["current_status"] == "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in certificate), "no-shadow zero theorem is not adopted"),
        ("VAL2888_3_countermodels_retained", len(countermodels) == 5 and all(row["valid_for_claim"] is False for row in countermodels), "shadow countermodels are retained"),
        ("VAL2888_4_cshadow_row", cshadow[0]["symbol"] == "C_shadow_abs" and cshadow[0]["candidate_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO", "C_shadow_abs source-ready row is staged"),
        ("VAL2888_5_components_missing", all("MISSING" in row["candidate_value"] or row["candidate_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO" for row in cshadow), "shadow component values remain missing"),
        ("VAL2888_6_kernels_nonclaim", len(kernels) == 5 and all(row["comparison_ready"] is False for row in kernels), "response kernel links are nonclaim"),
        ("VAL2888_7_component_updated", update[0]["current_status"] == "SHADOW_ENVELOPE_DEFINED_VALUES_MISSING", "E_DqZ coframe component includes shadow envelope"),
        ("VAL2888_8_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2888_9_runner_refused", runner[0]["status"] == "REFUSED_CSHADOW_VALUES_MISSING" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2888_10_next_target_2889", next_target[0]["next_id"] == "NEXT2888_0_2889" and next_target[0]["selected"] is True, "2889 target selected"),
        ("VAL2888_11_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2888_12_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2888_13_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2888_14_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2888_15_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2888_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2888_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2888_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2888 retained terminal public coframe no-shadow as exact conditional only, refused C_shadow=0, staged C_shadow_abs/b_R/d_R rows, and selected b_R zero or common-Weyl PPN kernel for 2889.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2888 - Y5 R2FR Terminal Public Coframe No-Shadow Or Cshadow Bound Row Under AX1090

Status: `Y5_R2FR_2888_no_shadow_conditional_Cshadow_abs_nonclaim_2889_bR_next`

## Private Verdict

2888 attacks the hidden-frame gremlin directly.

The clean theorem exists:

If ordinary readout has a terminal public coframe `e_pub=E(Q_vis)`, no representative Weyl/disformal/source/endpoint slot is in the action or readout domain, and inherited maps have no independent hidden argument, then `b_R=d_R=w_R=epsilon_endpoint_R=0`.

But this remains exact conditional structure, not a parent-signed MTS result. The old countermodels still survive: common Weyl, common disformal, source-prefactor, endpoint/boundary, and q-shape-forgetting leaks.

So `C_shadow=0` is not adopted. The fallback is now concrete: `C_shadow_abs = |b_R|+|d_R|+|w_R|+|epsilon_endpoint_R|+|epsilon_coupling_shadow|+|epsilon_readout_shadow|`, with no cancellation allowed.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## No-Shadow Certificate Audit

{md_table(rows_by_name["certificate"], ["certificate_id", "clause", "current_status", "if_signed", "current_blocker", "parent_signed", "valid_for_claim"])}

## Shadow Countermodels

{md_table(rows_by_name["countermodels"], ["countermodel_id", "ansatz", "why_it_survives", "kills_shortcut", "required_fix", "valid_for_claim"])}

## Cshadow Bound Rows

{md_table(rows_by_name["cshadow"], ["row_id", "symbol", "definition", "candidate_value", "upper_bound", "current_status", "valid_for_claim"])}

## Response Kernel Links

{md_table(rows_by_name["kernels"], ["kernel_id", "arena", "candidate_relation", "current_status", "comparison_ready", "valid_for_claim"])}

## E DqZ Coframe Shadow Update

{md_table(rows_by_name["update"], ["update_id", "symbol", "new_information", "updated_formula", "current_status", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_no_shadow_certificates", "accepted_cshadow_rows", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name = {
        "sources": source_register_rows(),
        "certificate": certificate_rows(),
        "countermodels": countermodel_rows(),
        "cshadow": cshadow_rows(),
        "kernels": kernel_rows(),
        "update": update_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows
    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2888_OVERALL")
    print(f"VAL2888_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
