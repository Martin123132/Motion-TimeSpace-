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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2917"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2917-Y5-R2FR-disformal-PPN-kernel-or-cg-source-leg-provenance-fill-under-AX1090.md"

SRC_2916_DOC = ROOT / "2916-Y5-R2FR-Cshadow-cg-invariant-source-test-product-or-disformal-PPN-kernel-under-AX1090.md"
SRC_2916_NEXT = RESIDUALS / "P8_Y5_R2FR_2916_NEXT_TARGET.csv"
SRC_2916_SOURCE_LEG = RESIDUALS / "P8_Y5_R2FR_2916_QBAR_SOURCE_LEG_DECLARATION_GATE.csv"
SRC_2916_DISFORMAL = RESIDUALS / "P8_Y5_R2FR_2916_DISFORMAL_PPN_KERNEL_FALLBACK.csv"
SRC_944_FRAME = RESIDUALS / "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv"
SRC_945_BOUNDS = RESIDUALS / "P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv"
SRC_1038_ACQ = RESIDUALS / "P8_Y5_R10_1038_BETA_BOUND_SOURCE_ACQUISITION.csv"
SRC_2574_DIS = RESIDUALS / "P8_Y5_PPN_VECTOR_2574_DISFORMAL_COUPLING_ENDPOINT_KERNEL_ROWS.csv"
SRC_2574_REQ = RESIDUALS / "P8_Y5_PPN_VECTOR_2574_FULL_VECTOR_REQUIREMENTS.csv"
SRC_2631_VECTOR = RESIDUALS / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"
SRC_1883_VECTOR = RESIDUALS / "P8_Y5_PARENT_QLOC_1883_FULL_PPN_RESIDUAL_VECTOR.csv"
SRC_1883_BOUNDS = RESIDUALS / "P8_Y5_PARENT_QLOC_1883_PPN_BOUND_ROWS.csv"
SRC_753_EXTERNAL = RESIDUALS / "P8_Y5_R10_753_EXTERNAL_PPN_SOURCE_PACK.csv"
SRC_1141_ANCHORS = RESIDUALS / "P8_Y5_R10_1141_PPN_BOUND_ANCHOR_ROWS.csv"
SRC_2888_CSHADOW = RESIDUALS / "P8_Y5_R2FR_2888_CSHADOW_BOUND_ROW_NONCLAIM.csv"
SRC_2889_GUARD = RESIDUALS / "P8_Y5_R2FR_2889_FULL_PPN_GUARD_LEDGER.csv"
SRC_2891_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2891_FULL_PPN_BLOCKER_LEDGER.csv"
SRC_2892_UPDATE = RESIDUALS / "P8_Y5_R2FR_2892_FULL_PPN_BRANCH_UPDATE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2917_SOURCE_REGISTER.csv",
    "source_leg_retry": RESIDUALS / "P8_Y5_R2FR_2917_CG_SOURCE_LEG_RETRY_AUDIT.csv",
    "zero_audit": RESIDUALS / "P8_Y5_R2FR_2917_DISFORMAL_ZERO_PROOF_AUDIT.csv",
    "kernel": RESIDUALS / "P8_Y5_R2FR_2917_DISFORMAL_PPN_RESPONSE_KERNEL.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_2917_PPN_BOUND_ANCHOR_BINDING.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2917_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2917_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2917_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2917_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2917_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "source_leg_copy": PARENT_ACTION / "Cg_source_leg_retry_2917_NONCLAIM.csv",
    "kernel_copy": LOCAL_BOUNDS / "Disformal_PPN_kernel_2917_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2917_ALPHA3_SOURCE_CURRENT_OR_NO_DISFORMAL_SLOT_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


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
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
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


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2917_00_2916_doc", SRC_2916_DOC, "alpha_X(lambda);not a local-GR proof", "2916 product-law narrative and claim ceiling"),
        ("SRC2917_01_2916_next", SRC_2916_NEXT, "NEXT2916_0_2917;disformal;source leg", "machine-readable 2917 target"),
        ("SRC2917_02_2916_source_leg", SRC_2916_SOURCE_LEG, "SLG2916_5_verdict;SOURCE_LEG_GATE_FAILS_CURRENT_MTS", "source-leg failure inherited from 2916"),
        ("SRC2917_03_2916_disformal", SRC_2916_DISFORMAL, "DIS2916_4_fallback_verdict;DISFORMAL_PPN_KERNEL_STAGED_NONCLAIM", "2916 disformal fallback"),
        ("SRC2917_04_944_frame", SRC_944_FRAME, "FLB944_1_disformal;MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND", "frame-leak disformal component"),
        ("SRC2917_05_945_bound", SRC_945_BOUNDS, "BND945_4_disformal_value;MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND", "first b_dis missing-value row"),
        ("SRC2917_06_1038_acq", SRC_1038_ACQ, "BBA1038_3_PPN_common_frame_gamma;BBA1038_5_preferred_frame_flux", "PPN gamma/preferred-frame acquisition anchors"),
        ("SRC2917_07_2574_disformal", SRC_2574_DIS, "DPK2574_0_dR_alpha1_alpha2;DPK2574_1_flux_alpha3;DPK2574_2_endpoint_xi", "existing disformal endpoint PPN kernels"),
        ("SRC2917_08_2574_requirements", SRC_2574_REQ, "VREQ2574_5_dR;VREQ2574_8_total_no_cancellation", "full vector requirement rows"),
        ("SRC2917_09_2631_vector", SRC_2631_VECTOR, "PPNV2631_3_dR;MISSING_DISFORMAL_PREFERRED_FRAME_PROJECTION", "no-shadow full PPN vector d_R slot"),
        ("SRC2917_10_1883_vector", SRC_1883_VECTOR, "PPNV1883_3_dR_preferred_frame;MISSING_DISFORMAL_RESPONSE_KERNEL", "parent qloc retained PPN vector"),
        ("SRC2917_11_1883_bounds", SRC_1883_BOUNDS, "PBOUND1883_2_alpha1;PBOUND1883_4_alpha3;PBOUND1883_5_xi", "PPN bound comparator rows"),
        ("SRC2917_12_753_external", SRC_753_EXTERNAL, "EXT753_0_Will_2014_LRR;EXT753_2_Will_Nordtvedt_1972_PPN_I", "external PPN/preferred-frame provenance"),
        ("SRC2917_13_1141_anchors", SRC_1141_ANCHORS, "PPNBA1141_0_alpha1;PPNBA1141_2_alpha3", "source-locked preferred-frame anchor values"),
        ("SRC2917_14_2888_cshadow", SRC_2888_CSHADOW, "CSH2888_2_d_R_disformal;PREFERRED_FRAME_KERNEL_MISSING", "C_shadow disformal row"),
        ("SRC2917_15_2889_guard", SRC_2889_GUARD, "PPNG2889_2_preferred;MISSING_DISFORMAL_PREFERRED_FRAME_PROJECTION", "full PPN guard ledger"),
        ("SRC2917_16_2891_blockers", SRC_2891_BLOCKERS, "PPNB2891_4_preferred_endpoint;MISSING_PROJECTION_SILENCE_OR_FINITE_KERNEL", "latest preferred endpoint blocker"),
        ("SRC2917_17_2892_update", SRC_2892_UPDATE, "PPNU2892_4_readout_boundary;MISSING_PROJECTION_SILENCE_OR_FINITE_KERNELS", "latest branch update"),
    ]
    rows = []
    for source_id, path, anchors, role in specs:
        ok, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": ok,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def source_leg_retry_rows() -> list[dict[str, Any]]:
    specs = [
        ("SLR2917_0_source_leg_exists", "Qbar_XH or beta_s contains a declared source leg", "MISSING_SOURCE_LEG_DECLARATION", "required to allow any linear-looking c_g row"),
        ("SLR2917_1_source_path_units", "source leg has parent equation/source path/units", "MISSING_SOURCE_PATH_AND_UNITS", "prevents hiding normalization in Qbar_XH"),
        ("SLR2917_2_no_double_count", "Qbar_XH/beta_s/c_g factor ledger has no duplicate source leg", "MISSING_FACTOR_LEDGER", "prevents beta_s beta_t and linear shortcut double counting"),
        ("SLR2917_3_runner_policy", "alpha(lambda)=numeric*c_g remains rejected until all source-leg gates pass", "REJECT_LINEAR_CG_NOW", "keeps 1038/2916 quarantine active"),
        ("SLR2917_4_verdict", "current corpus has a claim-safe c_g source leg", "CG_SOURCE_LEG_RETRY_FAILS_CURRENT_MTS", "move to disformal PPN kernel rather than scoring c_g"),
    ]
    return [
        add_common(
            {
                "retry_id": retry_id,
                "requirement": requirement,
                "current_status": status,
                "effect": effect,
                "source_paths": f"{SRC_2916_SOURCE_LEG};{SRC_2916_DISFORMAL}",
                "gate_pass": False,
            }
        )
        for retry_id, requirement, status, effect in specs
    ]


def zero_audit_rows() -> list[dict[str, Any]]:
    specs = [
        ("ZDIS2917_0_no_disformal_slot", "parent matter action has no D(X)u_mu u_nu disformal matter metric slot", "MISSING_PARENT_MATTER_ACTION_NO_DISFORMAL_CLAUSE", "would set b_dis=0 before PPN projection"),
        ("ZDIS2917_1_vector_owner", "u_mu or preferred current is absent, pure gauge, or co-moving with no preferred-frame observable", "MISSING_VECTOR_CURRENT_OWNER_AND_GAUGE_PROOF", "would kill alpha1/alpha2 preferred-frame leakage"),
        ("ZDIS2917_2_same_metric_convention", "coframe/connection/matter measure descend to the same observed metric", "MISSING_MEASURE_COFRAME_CONNECTION_DESCENT", "prevents hidden frame mismatch"),
        ("ZDIS2917_3_boundary_domain_silence", "boundary/domain/support endpoints do not source xi or alpha3", "MISSING_BOUNDARY_DOMAIN_SILENCE", "would remove endpoint/source-current tails"),
        ("ZDIS2917_4_no_readout_absorption", "readout and measured GM are fixed before variation and cannot absorb d_R", "MISSING_FIXED_BEFORE_READOUT_TRANSFER", "prevents post-hoc cancellation"),
        ("ZDIS2917_5_verdict", "b_dis theorem zero for local PPN", "Z_BDIS_FALSE_UNSIGNED", "no theorem-zero claim; retain finite nonclaim kernel"),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "zero_clause": clause,
                "current_status": status,
                "if_proved": effect,
                "source_paths": f"{SRC_2574_REQ};{SRC_2631_VECTOR};{SRC_2888_CSHADOW}",
                "theorem_zero_adopted": False,
            }
        )
        for audit_id, clause, status, effect in specs
    ]


def disformal_kernel_rows() -> list[dict[str, Any]]:
    common_sources = f"{SRC_2574_DIS};{SRC_1883_BOUNDS};{SRC_753_EXTERNAL};{SRC_1141_ANCHORS}"
    specs = [
        (
            "DK2917_0_ansatz",
            "d_R;b_dis",
            "disformal matter metric slot",
            "metric_ansatz",
            "g_obs_mu_nu = A(C_R)^2 g_pub_mu_nu + D(C_R) u_mu u_nu",
            "D(C_R) parent coefficient, vector/current owner, units, same matter metric convention",
            "ANSATZ_CONTRACT_FILLED_PARENT_UNSIGNED",
            "PPN;clock;orbital",
        ),
        (
            "DK2917_1_alpha1_alpha2",
            "K_alpha1_d;K_alpha2_d",
            "preferred-frame boost response",
            "alpha1;alpha2",
            "|Delta alpha_i| <= |K_alpha_i_d| |d_R| + |K_alpha_i_J| |Dln(kappa_MTS ell_J)| + |tail_alpha_i|",
            "preferred-frame gauge, normalized u_mu/current, K_alpha_i_d, source-current normalization",
            "SOURCE_READY_TEMPLATE_KERNEL_MISSING_COEFFICIENTS",
            "PPN_preferred_frame",
        ),
        (
            "DK2917_2_alpha3",
            "K_alpha3_flux",
            "momentum/source-exchange preferred-frame flux",
            "alpha3",
            "|Delta alpha3| <= |K_alpha3_flux| |w_R + q_boundary + source_exchange + Dln_ell_J + Dln_kappa_MTS| + |tail_alpha3|",
            "momentum conservation descent, boundary flux silence or finite coefficient row, coupling owner",
            "SOURCE_CURRENT_KERNEL_MISSING_ULTRATIGHT_BOUND",
            "PPN_preferred_frame;source_normalization",
        ),
        (
            "DK2917_3_xi",
            "K_xi_endpoint;K_xi_domain",
            "preferred-location endpoint/domain leakage",
            "xi",
            "|Delta xi| <= |K_xi_endpoint| |epsilon_endpoint_R| + |K_xi_domain| |q_domain| + |K_xi_proj| |epsilon_projector|",
            "endpoint local projection kernel, domain/support vector, boundary no-hair theorem or finite input",
            "ENDPOINT_DOMAIN_KERNEL_MISSING",
            "PPN_preferred_location;orbital",
        ),
        (
            "DK2917_4_gamma_beta_readout",
            "K_readout;K_GM;K_beta_k",
            "readout/measured-GM and second-order source tail",
            "gamma_minus_1;beta_minus_1",
            "|Delta gamma_beta_readout| <= |K_readout C_readout| + |K_GM delta_GM_fit| + |K_beta_k Dln_kappa_MTS| + |K_beta_J Dln_ell_J|",
            "fixed-before-readout proof, GM calibration map, second-order source-normalized field equation",
            "READOUT_BETA_KERNEL_MISSING",
            "PPN;Newton_GM",
        ),
        (
            "DK2917_5_total_abs",
            "Delta_PPN_dis_abs",
            "no-cancellation disformal preferred-frame envelope",
            "alpha1;alpha2;alpha3;xi;gamma_minus_1;beta_minus_1",
            "Delta_PPN_dis_abs := sum_abs(DK2917_1..DK2917_4 active heads)",
            "all coefficients numeric/source-backed or theorem-zero in the same normalization; no cancellation identity otherwise",
            "SCHEMA_READY_VALUES_MISSING",
            "all_PPN;local_GR_Newton",
        ),
        (
            "DK2917_6_verdict",
            "b_dis PPN kernel",
            "2917 branch verdict",
            "all_PPN",
            "disformal/preferred-frame response kernel is source-ready as a template, not a prediction",
            "parent no-disformal theorem or finite d_R/K_alpha_i/K_xi/source-current coefficients",
            "DISFORMAL_PPN_KERNEL_FILLED_AS_SOURCE_READY_NONCLAIM",
            "PPN;local_GR_Newton",
        ),
    ]
    return [
        add_common(
            {
                "kernel_id": kernel_id,
                "symbol": symbol,
                "component": component,
                "observable_targets": observables,
                "response_or_bound": response,
                "required_inputs": required,
                "current_status": status,
                "arena_links": arena,
                "source_paths": common_sources,
                "promotion_allowed_now": False,
            }
        )
        for kernel_id, symbol, component, observables, response, required, status, arena in specs
    ]


def bound_anchor_rows() -> list[dict[str, Any]]:
    specs = [
        ("PBOUND2917_0_gamma", "gamma_minus_1", "2.3e-05", "dimensionless_abs", "Cassini_Shapiro_gamma_2003:R3_gamma", "BBA1038_3;PBOUND1883_0_gamma", "comparator only; requires full vector closure"),
        ("PBOUND2917_1_beta", "beta_minus_1", "7.8e-05", "dimensionless_abs", "Will_2014_PPN_beta_table:R4_beta", "BBA1038_4;PBOUND1883_1_beta", "second-order comparator only"),
        ("PBOUND2917_2_alpha1", "alpha1", "1e-04", "dimensionless_abs", "Will_2014_PPN_alpha1_table:R5_alpha1", "PPNBA1141_0_alpha1;PBOUND1883_2_alpha1", "preferred-frame comparator requires d_R response coefficient"),
        ("PBOUND2917_3_alpha2", "alpha2", "2e-09", "dimensionless_abs", "Will_2014_PPN_alpha2_table:R6_alpha2", "PPNBA1141_1_alpha2;PBOUND1883_3_alpha2", "sharp preferred-frame comparator"),
        ("PBOUND2917_4_alpha3", "alpha3", "4e-20", "dimensionless_abs", "Will_2014_PPN_alpha3_table:R7_alpha3", "PPNBA1141_2_alpha3;PBOUND1883_4_alpha3", "ultratight source-current/momentum comparator"),
        ("PBOUND2917_5_xi", "xi", "4e-09", "dimensionless_abs", "Will_2014_PPN_xi_table:R8_xi", "PBOUND1883_5_xi;BBA1038_5", "preferred-location endpoint/domain comparator"),
    ]
    return [
        add_common(
            {
                "bound_id": bound_id,
                "observable": observable,
                "upper_bound_abs": upper_bound,
                "units": units,
                "source_id": source_id,
                "local_anchor": local_anchor,
                "use_policy": use_policy,
                "source_paths": f"{SRC_1883_BOUNDS};{SRC_753_EXTERNAL};{SRC_1141_ANCHORS};{SRC_1038_ACQ}",
                "bound_source_backed": True,
                "mts_prediction_present": False,
            }
        )
        for bound_id, observable, upper_bound, units, source_id, local_anchor, use_policy in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2917_0_cg_source_leg", "linear c_g source-leg exception is open", "REJECTED_NONCLAIM", "source leg, units and no-double-count ledger remain missing", False),
        ("CG2917_1_bdis_zero", "b_dis=0 theorem-zero is proved", "BLOCKED_NONCLAIM", "no parent no-disformal-slot theorem signed", False),
        ("CG2917_2_disformal_kernel_score", "d_R/b_dis PPN kernel can be scored", "BLOCKED_NONCLAIM", "K_alpha_i, K_xi, source-current and readout coefficients missing", False),
        ("CG2917_3_alpha3", "alpha3 preferred-frame constraint is passed", "BLOCKED_NONCLAIM", "ultratight alpha3 source-current kernel missing", False),
        ("CG2917_4_local_GR_Newton", "local GR/Newton follows after 2917", "BLOCKED_NONCLAIM", "2917 fills a nonclaim kernel only; not a local-GR proof", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
            }
        )
        for gate_id, claim, status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2917_0_source_leg", "c_g_source_leg_not_recovered", "2916 source-leg requirements still fail: no declared source leg, units or factor ledger.", "keep c_g product law; no linear scoring"),
        ("DEC2917_1_zero_proof", "no_disformal_slot_theorem_not_proved", "A parent action could still kill b_dis, but current corpus lacks the exact no-disformal-slot/current-owner clause.", "retain b_dis as finite nonclaim component"),
        ("DEC2917_2_kernel", "disformal_PPN_kernel_now_explicit", "alpha1/alpha2, alpha3, xi and readout/beta channels are separated into no-cancellation rows.", "use this as the future PPN acquisition template"),
        ("DEC2917_3_next", "alpha3_source_current_is_sharpest_next_cut", "alpha3 has the tightest comparator and directly exposes source exchange, boundary flux, kappa and ell_J ownership.", "select 2918 alpha3/source-current or no-disformal-slot theorem"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2917_0_2918",
                "selection_status": "selected_primary",
                "target_file": "2918-Y5-R2FR-alpha3-source-current-kernel-or-no-disformal-slot-theorem-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_alpha3_source_current_kernel_or_no_disformal_slot_theorem_under_AX1090_2918.py",
                "task": "either prove the parent action has no disformal/preferred-frame slot through PPN order, or derive the alpha3 source-current kernel for w_R, q_boundary, source_exchange, Dln_kappa_MTS and Dln_ell_J",
                "success_condition": "Z_bdis=true from parent action, or a source-backed alpha3 response row with units, source paths, no fitted-GM absorption and no-cancellation accounting",
                "fallback_condition": "keep d_R/source-current nonclaim and move to beta/source-normalization second-order kernel",
                "guardrails": "no c_g linear shortcut; no cancellation between source-current heads; no local GR/Newton/PPN/R10 claim; no formalization-workbench edits; no GitHub",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("source_leg_retry_copy", OUTPUTS["source_leg_retry"], BRANCH_OUTPUTS["source_leg_copy"]),
        ("kernel_copy", OUTPUTS["kernel"], BRANCH_OUTPUTS["kernel_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source, destination in specs:
        if source.exists():
            shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "source_exists": source.exists(),
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination) if destination.exists() else False,
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    source_leg_rows_: list[dict[str, Any]],
    zero_rows_: list[dict[str, Any]],
    kernel_rows_: list[dict[str, Any]],
    bound_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_outputs_with_validation = [*csv_outputs, OUTPUTS["validation"]]
    source_leg_verdict = next(row for row in source_leg_rows_ if row["retry_id"] == "SLR2917_4_verdict")
    zero_verdict = next(row for row in zero_rows_ if row["audit_id"] == "ZDIS2917_5_verdict")
    kernel_verdict = next(row for row in kernel_rows_ if row["kernel_id"] == "DK2917_6_verdict")
    required_observables = {"alpha1", "alpha2", "alpha3", "xi", "gamma_minus_1", "beta_minus_1"}
    kernel_observables: set[str] = set()
    for row in kernel_rows_:
        kernel_observables.update(item for item in str(row["observable_targets"]).split(";") if item)
    bound_observables = {str(row["observable"]) for row in bound_rows_}
    generated_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]
    checks = [
        ("VAL2917_0_source_paths_exist", all(bool(row["path_exists"]) for row in source_rows), "all cited source paths exist"),
        ("VAL2917_1_source_anchors_found", all(bool(row["anchors_found"]) for row in source_rows), "all source anchors found"),
        ("VAL2917_2_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs_with_validation if path.exists()), "generated CSV outputs parse cleanly"),
        ("VAL2917_3_source_leg_still_rejected", source_leg_verdict["current_status"] == "CG_SOURCE_LEG_RETRY_FAILS_CURRENT_MTS", "linear c_g source-leg exception remains rejected"),
        ("VAL2917_4_zero_proof_unsigned", zero_verdict["current_status"] == "Z_BDIS_FALSE_UNSIGNED" and not bool(zero_verdict["theorem_zero_adopted"]), "b_dis theorem-zero is not adopted"),
        ("VAL2917_5_kernel_filled_nonclaim", kernel_verdict["current_status"] == "DISFORMAL_PPN_KERNEL_FILLED_AS_SOURCE_READY_NONCLAIM", "disformal PPN kernel filled as nonclaim template"),
        ("VAL2917_6_kernel_observables_complete", required_observables.issubset(kernel_observables), "kernel covers gamma, beta, alpha1, alpha2, alpha3 and xi"),
        ("VAL2917_7_bound_anchors_complete", required_observables.issubset(bound_observables), "PPN bound anchors bound to all required observables"),
        ("VAL2917_8_claim_gates_safe", all(not bool(row["claim_allowed"]) and not bool(row["valid_for_claim"]) and not bool(row["gate_pass"]) for row in claim_rows_), "no claim gate is open"),
        ("VAL2917_9_next_target_selected", next_rows_[0]["route_id"] == "NEXT2917_0_2918" and bool(next_rows_[0]["selected"]), "2918 alpha3/source-current target selected"),
        ("VAL2917_10_branch_copies_parse", all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_), "branch copies exist and parse"),
        ("VAL2917_11_no_formalization_outputs", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no generated output path is inside formalization-workbench"),
        ("VAL2917_12_doc_written", DOC.exists() if include_doc_check else True, "markdown checkpoint exists"),
    ]
    rows: list[dict[str, Any]] = [
        {
            "validation_id": validation_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for validation_id, status, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2917_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2917 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    source_leg_rows_: list[dict[str, Any]],
    zero_rows_: list[dict[str, Any]],
    kernel_rows_: list[dict[str, Any]],
    bound_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2917_OVERALL")
    text = f"""# 2917 - Y5/R2FR Disformal PPN Kernel Or Cg Source-Leg Provenance Fill Under AX1090

Status: `Y5_R2FR_2917_cg_source_leg_retry_failed_bdis_zero_unsigned_disformal_PPN_kernel_filled_nonclaim_alpha3_2918_next`

Claim ceiling: `no_linear_cg_score_no_bdis_zero_no_PPN_pass_no_local_GR_no_Newton_no_R10_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2917 tries the cleanest route first: rescue a legitimate `c_g` source leg. It fails in the present corpus because `Qbar_XH` or `beta_s` still has no declared source leg, units, source path, and no-double-count factor ledger.

The checkpoint then takes the disformal route. It does not prove `b_dis=0`; instead it writes the response kernel that a future parent action must satisfy:

`g_obs_mu_nu = A(C_R)^2 g_pub_mu_nu + D(C_R) u_mu u_nu`.

If the parent action has no disformal slot, no preferred current, and no endpoint/domain/readout leakage, this branch can collapse to zero. Current evidence does not prove that. Therefore `d_R/b_dis` remains a finite nonclaim component, routed mainly into `alpha1`, `alpha2`, `alpha3`, `xi`, and readout/beta tails.

The sharpest next cut is `alpha3`: it is the least forgiving place for hidden source exchange, boundary flux, `Dln_kappa_MTS`, and `Dln_ell_J`.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Cg Source-Leg Retry

{md_table(source_leg_rows_, ["retry_id", "requirement", "current_status", "effect", "gate_pass", "valid_for_claim"])}

## Disformal Zero-Proof Audit

{md_table(zero_rows_, ["audit_id", "zero_clause", "current_status", "if_proved", "theorem_zero_adopted", "valid_for_claim"])}

## Disformal PPN Response Kernel

{md_table(kernel_rows_, ["kernel_id", "symbol", "observable_targets", "response_or_bound", "required_inputs", "current_status", "valid_for_claim"])}

## PPN Bound Anchor Binding

{md_table(bound_rows_, ["bound_id", "observable", "upper_bound_abs", "units", "source_id", "use_policy", "bound_source_backed", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows_, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows_, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows_, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall["status"]}`.

## Interpretation

This checkpoint makes the coupling problem more concrete. The missing object is not just “a coupling” in the abstract; it is either a parent theorem that forbids the disformal/preferred-frame slot, or a source-current response kernel that survives PPN constraints.

That is good news structurally and bad news lazily: there is no safe shortcut through a naked `c_g` row, but there is now a precise next derivation target.

## Not Claimed

- no `c_g` source-leg exception is open;
- no `b_dis=0` theorem is proved;
- no PPN, R10, WEP, clock, orbital, local-GR or Newtonian reduction pass is claimed;
- no cancellation between `d_R`, source-current, endpoint, readout, `kappa_MTS`, or `ell_J` is allowed without a parent identity;
- no file in `formalization-workbench` is modified by this checkpoint;
- no public/GitHub action is implied.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    source_leg_rows_ = source_leg_retry_rows()
    zero_rows_ = zero_audit_rows()
    kernel_rows_ = disformal_kernel_rows()
    bound_rows_ = bound_anchor_rows()
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["source_leg_retry"], source_leg_rows_)
    write_csv(OUTPUTS["zero_audit"], zero_rows_)
    write_csv(OUTPUTS["kernel"], kernel_rows_)
    write_csv(OUTPUTS["bounds"], bound_rows_)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        source_leg_rows_,
        zero_rows_,
        kernel_rows_,
        bound_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        source_leg_rows_,
        zero_rows_,
        kernel_rows_,
        bound_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        source_leg_rows_,
        zero_rows_,
        kernel_rows_,
        bound_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        source_leg_rows_,
        zero_rows_,
        kernel_rows_,
        bound_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2917_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
