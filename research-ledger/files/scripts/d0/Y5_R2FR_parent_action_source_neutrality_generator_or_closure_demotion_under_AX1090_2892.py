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

DOC = ROOT / "2892-Y5-R2FR-parent-action-source-neutrality-generator-or-closure-demotion-under-AX1090.md"

SRC_2891_DOC = ROOT / "2891-Y5-R2FR-no-boundary-charge-source-descent-or-qRhat-row-under-AX1090.md"
SRC_2891_NEXT = RESIDUALS / "P8_Y5_R2FR_2891_NEXT_TARGET.csv"
SRC_2891_THEOREM = RESIDUALS / "P8_Y5_R2FR_2891_NO_BOUNDARY_SOURCE_THEOREM_ATTEMPT.csv"
SRC_2891_INTEGRAL = RESIDUALS / "P8_Y5_R2FR_2891_SOURCE_NEUTRALITY_INTEGRAL_LAW.csv"
SRC_2891_QRHAT = RESIDUALS / "P8_Y5_R2FR_2891_QRHAT_INPUT_ROW_NONCLAIM.csv"
SRC_2891_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2891_VALIDATION.csv"

SRC_07_CONSTRAINT = ROOT / "07-nonpropagating-reciprocity-constraint.md"
SRC_10_CONTRACT = ROOT / "10-observer-map-symplectic-contract.md"
SRC_12_NOETHER = ROOT / "12-gauge-noether-origin-audit.md"
SRC_2882_DOC = ROOT / "2882-Y5-R2FR-q-object-vertical-generator-certificate-or-Dq-leak-row-under-AX1090.md"
SRC_2886_QVIS = RESIDUALS / "P8_Y5_R2FR_2886_QVIS_PARENT_SIGNATURE_AUDIT.csv"
SRC_2887_OBS = RESIDUALS / "P8_Y5_R2FR_2887_OBSERVED_COFRAME_FUNCTOR_AUDIT.csv"
SRC_2888_NOSHADOW = RESIDUALS / "P8_Y5_R2FR_2888_TERMINAL_PUBLIC_COFRAME_NO_SHADOW_CERTIFICATE_AUDIT.csv"
SRC_2890_PROFILE = RESIDUALS / "P8_Y5_R2FR_2890_XU_DELTA_P_PROFILE_LAW.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2892_SOURCE_REGISTER.csv",
    "schema": RESIDUALS / "P8_Y5_R2FR_2892_PARENT_ACTION_SOURCE_NEUTRALITY_SCHEMA.csv",
    "generator": RESIDUALS / "P8_Y5_R2FR_2892_VERTICAL_GENERATOR_CONSTRUCTION_ATTEMPT.csv",
    "closure": RESIDUALS / "P8_Y5_R2FR_2892_CLOSURE_DEMOTION_LEDGER.csv",
    "qrhat": RESIDUALS / "P8_Y5_R2FR_2892_QRHAT_STATUS_UPDATE.csv",
    "ppn": RESIDUALS / "P8_Y5_R2FR_2892_FULL_PPN_BRANCH_UPDATE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2892_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2892_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2892_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2892_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2892_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2892_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "schema_copy": SOURCE_WEIGHT / "RAB_PARENT_ACTION_SOURCE_NEUTRALITY_SCHEMA_2892_NONCLAIM.csv",
    "qrhat_copy": LOCAL_BOUNDS / "RAB_QRHAT_STATUS_UPDATE_2892_NONCLAIM.csv",
    "ppn_copy": BETA_DOCS / "RAB_FULL_PPN_BRANCH_UPDATE_2892_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2892_beta_source_or_finite_qrhat_NEXT.csv",
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
        ("SRC2892_0_2891_doc", SRC_2891_DOC, "NEXT2891_0_2892;source-neutrality integral contract", "2891 handoff"),
        ("SRC2892_1_2891_next", SRC_2891_NEXT, "NEXT2891_0_2892", "explicit 2892 target"),
        ("SRC2892_2_2891_theorem", SRC_2891_THEOREM, "NBT2891_2_source_neutrality;NO_BOUNDARY_SOURCE_DESCENT_NOT_PARENT_SIGNED_CURRENT_CORPUS", "source neutrality theorem attempt"),
        ("SRC2892_3_2891_integral", SRC_2891_INTEGRAL, "SNL2891_1_source_integral;EXACT_CONDITIONAL_ZERO_CHAIN", "source integral law"),
        ("SRC2892_4_2891_qrhat", SRC_2891_QRHAT, "QR2891_0_live_qRhat_source_row;QRHAT_SOURCE_ROW_BLOCKED_NONCLAIM", "q_R_hat status"),
        ("SRC2892_5_2891_validation", SRC_2891_VALIDATION, "VAL2891_OVERALL", "2891 validation"),
        ("SRC2892_6_07_constraint", SRC_07_CONSTRAINT, "S_constraint = integral lambda_R R_AB;parent origin is still open", "nonpropagating closure route"),
        ("SRC2892_7_10_contract", SRC_10_CONTRACT, "A future parent action may pass only if;source_neutrality", "observer-map parent contract"),
        ("SRC2892_8_12_noether", SRC_12_NOETHER, "gauge_noether_origin_not_derived_closure_only;first-class parent constraint", "Noether/gauge rejection"),
        ("SRC2892_9_2882_qv", SRC_2882_DOC, "CERT2882_1_parent_q_object;CERT2882_2_field_by_field_vX", "q/v certificate failure"),
        ("SRC2892_10_2886_qvis", SRC_2886_QVIS, "QVS2886_0_exact_signature;QVIS_PARENT_SIGNATURE_NOT_SIGNED", "Q_vis parent signature audit"),
        ("SRC2892_11_2887_obs", SRC_2887_OBS, "OFA2887_0_target;OFA2887_1_exact_kernel", "observed coframe functor audit"),
        ("SRC2892_12_2888_noshadow", SRC_2888_NOSHADOW, "NSC2888_0_exact;NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS", "terminal no-shadow audit"),
        ("SRC2892_13_2890_profile", SRC_2890_PROFILE, "XDP2890_4_verdict;PROFILE_LAW_DERIVED_VALUE_AND_ZERO_BLOCKED", "profile consequence"),
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


def schema_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PAS2892_0_parent_fields",
            "parent field split",
            "Phi=(Q_vis,R; Psi_matter; theta_pub; constants), with R=C_R/R_AB as a representative reciprocal direction",
            "Q_vis and theta_pub must be parent primitives or constructed before matter/readout",
            "NOT_PARENT_SIGNED",
            "current Q_vis/coframe audits keep constructor unsigned",
        ),
        (
            "PAS2892_1_quotient_action",
            "quotient-invariant ordinary matter action",
            "S_matter=Sbar[Q_vis,Psi_matter,theta_pub(Q_vis)] and contains no R, partial R, endpoint R, or source-prefactor R argument",
            "delta_vR S_matter=0, so ordinary matter contributes no J_R",
            "EXACT_CONDITIONAL_SCHEMA",
            "requires action-domain/no-shadow exclusion to be parent-signed",
        ),
        (
            "PAS2892_2_no_pole_parent",
            "no kinetic/source pole for R",
            "S_parent has no independent W_R(partial R)^2/2 or J_R R term for the ordinary-source branch",
            "prevents a conserved Q_R hair channel from being generated",
            "EXACT_CONDITIONAL_SCHEMA",
            "looks like closure unless parent grammar explains why R is quotient/auxiliary",
        ),
        (
            "PAS2892_3_boundary",
            "zero/proper boundary charge",
            "allowed local source class has no reciprocal edge charge and no reference-subtraction R tail",
            "Q_R is not a physical boundary charge",
            "EXACT_CONDITIONAL_SCHEMA",
            "boundary term and source class are not derived",
        ),
        (
            "PAS2892_4_coupling_owner",
            "fixed-before-readout coupling ownership",
            "kappa_MTS, ell_J, H_core source equation and GM convention are functions of Q_vis or parent constants only, not R",
            "prevents finite q_R_hat from being hidden by source-normalization/coupling rescaling",
            "REQUIRED_SCHEMA_NOT_SIGNED",
            "coupling owner remains unsigned",
        ),
        (
            "PAS2892_5_result",
            "sufficient source-neutrality package",
            "PAS2892_1 through PAS2892_4 imply Pi_R=Q_R=q_R_hat=delta_p=x_U_CR=0 for ordinary local sources",
            "would close the first-order reciprocal PPN profile",
            "SUFFICIENT_CONDITIONAL_PARENT_ACTION_SCHEMA",
            "schema is not yet a parent derivation",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for schema_id, clause, construction, if_signed, status, blocker in specs:
        rows.append(
            add_common(
                {
                    "schema_id": schema_id,
                    "clause": clause,
                    "construction": construction,
                    "if_signed": if_signed,
                    "current_status": status,
                    "current_blocker": blocker,
                    "schema_constructed": True,
                    "parent_signed": False,
                    "theorem_zero_adopted": False,
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                }
            )
        )
    return rows


def generator_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "VGC2892_0_generator",
            "v_R field-space direction",
            "delta R=epsilon, delta Q_vis=0, delta theta_pub=0, delta Psi_matter=0, delta constants=0",
            "Dq[v_R]=0 and delta_vR S_matter=0 if Q_vis/theta_pub are parent-owned",
            "EXACT_CONDITIONAL_GENERATOR",
            "parent field chart and Q_vis constructor missing",
        ),
        (
            "VGC2892_1_bulk_equation",
            "bulk reciprocal equation",
            "if R is absent/auxiliary in the quotient action, E_R is a constraint/no-pole equation rather than a propagating source equation",
            "no exterior Q_R integration mode exists in the ordinary-source branch",
            "EXACT_CONDITIONAL_NO_POLE",
            "absence of R pole is not parent-derived",
        ),
        (
            "VGC2892_2_matter_source",
            "ordinary source current",
            "J_R^matter := delta S_matter/delta R = <delta Sbar/delta Q_vis,DQ_vis[v_R]> + direct_R_terms",
            "J_R^matter=0 when DQ_vis[v_R]=0 and direct_R_terms are excluded",
            "EXACT_CONDITIONAL_SOURCE_NEUTRALITY",
            "direct R source/readout/shadow terms survive as countermodels",
        ),
        (
            "VGC2892_3_boundary_charge",
            "Hamiltonian/boundary generator",
            "G_R[epsilon] has no physical surface charge if R is quotient/auxiliary and no R boundary density is in the action",
            "Q_R=0 rather than a superselection hair",
            "EXACT_CONDITIONAL_BOUNDARY_ZERO",
            "boundary density owner not supplied",
        ),
        (
            "VGC2892_4_countermodel",
            "visible R countermodel",
            "if matter/readout observes T and S or J_q separately, then R_AB=ln(T^2S) is visible and v_R is not vertical",
            "source neutrality construction fails",
            "COUNTERMODEL_ACTIVE",
            "must derive terminal public coframe/Q_vis before calling R vertical",
        ),
        (
            "VGC2892_5_verdict",
            "parent generator construction",
            "candidate generator is mathematically sufficient but not parent-signed by current corpus",
            "do not claim q_R_hat=0 as derived",
            "CONSTRUCTION_CONDITIONAL_CLOSURE_IF_USED_NOW",
            "would be closure in a nicer suit unless Q_vis/no-shadow origin is derived",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for generator_id, target, construction, consequence, status, blocker in specs:
        rows.append(
            add_common(
                {
                    "generator_id": generator_id,
                    "target": target,
                    "construction": construction,
                    "consequence": consequence,
                    "current_status": status,
                    "current_blocker": blocker,
                    "conditional_piece_proved": status.startswith("EXACT"),
                    "countermodel_active": status == "COUNTERMODEL_ACTIVE",
                    "parent_signed": False,
                    "theorem_zero_adopted": False,
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                }
            )
        )
    return rows


def closure_rows() -> list[dict[str, Any]]:
    specs = [
        ("CDEM2892_0_lambdaR", "lambda_R R_AB constraint", "works algebraically but parent origin remains open", "closure_benchmark_only"),
        ("CDEM2892_1_quotient_action", "declaring R absent from all matter/readout domains", "sufficient if parent-derived, closure-smuggling if imposed after the fact", "conditional_schema_not_claim"),
        ("CDEM2892_2_qrhat_zero", "q_R_hat=0 row", "allowed only as parent-zero theorem or explicit closure benchmark", "not_installed_as_prediction"),
        ("CDEM2892_3_local_GR", "local GR/Newton reduction", "not derived until beta/source/readout/full PPN vector also close", "blocked"),
    ]
    return [
        add_common(
            {
                "demotion_id": demotion_id,
                "object": obj,
                "reason": reason,
                "new_status": status,
                "closure_only_if_used_now": True,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for demotion_id, obj, reason, status in specs
    ]


def qrhat_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "update_id": "QRU2892_0_qrhat_zero_status",
                "symbols": "q_R_hat;delta_p;x_U_CR",
                "conditional_zero_formula": "source-neutral quotient action + zero boundary charge => q_R_hat=delta_p=x_U_CR=0",
                "current_value": "MISSING_PARENT_ZERO_OR_NUMERIC_QRHAT",
                "current_status": "ZERO_ROUTE_DEMOTED_TO_CLOSURE_UNLESS_PARENT_QVIS_SIGNED",
                "finite_fallback": "requires source-backed Q_R or q_R_hat with q_R_hat=Q_R c^2/(G M_source)",
                "relations": "x_U_CR=-q_R_hat; delta_p=-q_R_hat/2",
                "source_path": "MISSING_PARENT_ACTION_SOURCE_NEUTRALITY_CERTIFICATE_OR_FINITE_QRHAT_ROW",
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
    ]


def ppn_rows() -> list[dict[str, Any]]:
    specs = [
        ("PPNU2892_0_qrhat", "q_R_hat/delta_p/x_U_CR", "closure-demoted zero route; finite row missing", "MISSING_PARENT_QVIS_SOURCE_NEUTRALITY_OR_FINITE_QRHAT"),
        ("PPNU2892_1_bR", "b_R/common Weyl shadow", "still missing value/zero", "MISSING_NO_SHADOW_ACTION_DOMAIN_OR_SOURCE_COEFFICIENT"),
        ("PPNU2892_2_beta", "beta_minus_1", "next best derivation target", "MISSING_SECOND_ORDER_SOURCE_NORMALIZED_KERNEL"),
        ("PPNU2892_3_source_coupling", "kappa_MTS/ell_J/H_core/w_R", "coupling owner remains blocker", "MISSING_PARENT_COUPLING_OWNER"),
        ("PPNU2892_4_readout_boundary", "endpoint/readout/boundary/q_loc", "not killed by q_R_hat algebra", "MISSING_PROJECTION_SILENCE_OR_FINITE_KERNELS"),
        ("PPNU2892_5_total_abs", "Delta_PPN_abs", "full no-cancellation envelope remains unscored", "MISSING_ALL_COMPONENT_VALUES_OR_THEOREM_ZEROS"),
    ]
    return [
        add_common(
            {
                "branch_update_id": branch_id,
                "component": component,
                "current_status": status,
                "missing_for_claim": missing,
                "next_role": "primary" if branch_id == "PPNU2892_2_beta" else "blocked_component",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for branch_id, component, status, missing in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2892_0_schema", "sufficient parent-action source-neutrality schema is written", "PASS_NONCLAIM", "quotient-invariant matter and no-pole clauses are explicit"),
        ("GATE2892_1_parent_qvis", "Q_vis/terminal coframe/no-shadow origin is parent-signed", "FAIL", "2886/2887/2888 keep these premises unsigned"),
        ("GATE2892_2_generator", "v_R is a live field-by-field parent generator", "FAIL", "2882 keeps q/v certificate unsigned"),
        ("GATE2892_3_boundary", "zero reciprocal boundary charge is parent-derived", "FAIL", "boundary density/reference class missing"),
        ("GATE2892_4_qrhat_zero", "q_R_hat=0 can be installed as prediction", "FAIL", "would be closure if used now"),
        ("GATE2892_5_finite", "finite q_R_hat row exists", "FAIL", "no source-backed Q_R/q_R_hat row exists"),
        ("GATE2892_6_local_gr", "local GR/Newton/PPN follows", "FAIL", "beta/source/readout/full-vector channels remain open"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "parent_signed": False,
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
                "runner_id": "RUN2892_0_parent_action_source_neutrality_runner",
                "status": "REFUSED_CONSTRUCTION_NOT_PARENT_SIGNED",
                "accepted_parent_action_schemas": 0,
                "accepted_zero_theorems": 0,
                "accepted_finite_rows": 0,
                "reason": "schema is sufficient but conditional; Q_vis, v_R, terminal coframe, no-shadow, boundary and coupling owner are not parent-signed",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2892_0_schema", "KEEP_MINIMAL_SOURCE_NEUTRALITY_SCHEMA", "it is the exact contract a future parent action must satisfy", "use it as the parent-action target, not as evidence"),
        ("DEC2892_1_zero", "DEMOTE_QRHAT_ZERO_TO_CLOSURE_IF_USED_NOW", "the construction only closes after unsigned Q_vis/no-shadow/boundary/coupling clauses are granted", "do not install q_R_hat=0 as a prediction"),
        ("DEC2892_2_finite", "FINITE_QRHAT_ROW_STILL_MISSING", "no raw Q_R or source-backed q_R_hat value exists", "keep finite route as blocker rather than fabricate a number"),
        ("DEC2892_3_next", "MOVE_TO_BETA_SOURCE_NORMALIZED_KERNEL", "the parent source-neutrality route has hit closure-only without new parent evidence; local GR also needs beta", "derive beta/source-normalized second-order kernel next"),
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
                "next_id": "NEXT2892_0_2893",
                "status": "selected_primary",
                "target_doc": "2893-Y5-R2FR-beta-source-normalized-second-order-kernel-or-finite-local-vector-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_beta_source_normalized_second_order_kernel_or_finite_local_vector_under_AX1090_2893.py",
                "mission": "derive the beta/source-normalized second-order local PPN kernel without using gamma/q_R_hat closure; if it fails, stage finite beta/source/readout vector rows with no-cancellation guards",
                "forbidden_shortcuts": "no beta=1 from gamma; no GR Schwarzschild import; no q_R_hat closure as proof; no cancellation; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2892_1_held_parent_action",
                "status": "held_until_new_parent_evidence",
                "target_doc": "2893b-Y5-R2FR-Qvis-parent-origin-reentry-if-new-source.md",
                "target_script": "scripts/Y5_R2FR_Qvis_parent_origin_reentry_if_new_source_2893b.py",
                "mission": "retry Q_vis/no-shadow parent origin only if new parent action evidence appears",
                "forbidden_shortcuts": "do not re-audit same unsigned clauses without new source evidence",
                "selected": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2892_0_schema_copy", OUTPUTS["schema"], BRANCH_OUTPUTS["schema_copy"], "source-weight copy of parent action source-neutrality schema"),
        ("BR2892_1_qrhat_copy", OUTPUTS["qrhat"], BRANCH_OUTPUTS["qrhat_copy"], "local-bounds copy of q_R_hat closure-demotion update"),
        ("BR2892_2_ppn_copy", OUTPUTS["ppn"], BRANCH_OUTPUTS["ppn_copy"], "beta-source docs copy of full PPN branch update"),
        ("BR2892_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows: list[dict[str, Any]] = []
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
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    schema = rows_by_name["schema"]
    generator = rows_by_name["generator"]
    closure = rows_by_name["closure"]
    qrhat = rows_by_name["qrhat"]
    ppn = rows_by_name["ppn"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2892_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2892_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2892_2_schema_constructed", any(row["current_status"] == "SUFFICIENT_CONDITIONAL_PARENT_ACTION_SCHEMA" for row in schema), "sufficient parent-action schema is written"),
        ("VAL2892_3_generator_conditional", any(row["current_status"] == "EXACT_CONDITIONAL_SOURCE_NEUTRALITY" for row in generator), "vertical generator/source neutrality construction is exact conditional"),
        ("VAL2892_4_countermodel_retained", any(row["current_status"] == "COUNTERMODEL_ACTIVE" for row in generator), "visible-R countermodel remains active"),
        ("VAL2892_5_closure_demoted", all(row["closure_only_if_used_now"] is True for row in closure), "q_R_hat zero route is closure-only if used now"),
        ("VAL2892_6_qrhat_not_installed", qrhat[0]["current_status"] == "ZERO_ROUTE_DEMOTED_TO_CLOSURE_UNLESS_PARENT_QVIS_SIGNED" and "MISSING" in qrhat[0]["current_value"], "q_R_hat zero is not installed"),
        ("VAL2892_7_ppn_next_beta", any(row["branch_update_id"] == "PPNU2892_2_beta" and row["next_role"] == "primary" for row in ppn), "beta/source kernel is selected as next local branch target"),
        ("VAL2892_8_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2892_9_runner_refused", runner[0]["status"] == "REFUSED_CONSTRUCTION_NOT_PARENT_SIGNED" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2892_10_next_target_2893", next_target[0]["next_id"] == "NEXT2892_0_2893" and next_target[0]["selected"] is True, "2893 beta/source-normalized target selected"),
        ("VAL2892_11_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2892_12_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2892_13_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2892_14_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2892_15_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2892_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2892_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2892_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2892 constructed the sufficient parent-action source-neutrality schema, refused to parent-sign it from current evidence, demoted q_R_hat=0 to closure-only if used now, and selected beta/source-normalized second-order local PPN work for 2893.",
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
    text = f"""# 2892 - Y5 R2FR Parent Action Source Neutrality Generator Or Closure Demotion Under AX1090

Status: `Y5_R2FR_2892_parent_action_schema_constructed_not_signed_qRhat_zero_closure_only_beta_2893_next`

## Private Verdict

2892 takes the leap attempt seriously.

There is a clean sufficient parent-action schema:

`S_matter=Sbar[Q_vis,Psi,theta_pub(Q_vis)]`, with `v_R: delta R=epsilon`, `delta Q_vis=0`, `delta theta_pub=0`, `delta Psi=0`, and no direct `R`, `partial R`, source-prefactor, endpoint, boundary, or coupling shadow slot.

Under that schema, `delta_vR S_matter=0`, ordinary matter carries no reciprocal charge, the source integral from 2891 gives `Pi_R=0`, and the no-pole/zero-boundary condition gives `Q_R=q_R_hat=delta_p=x_U_CR=0`.

That is the good construction. The problem is ownership: the current corpus still does not parent-sign `Q_vis`, the field-by-field generator, terminal public coframe, no-shadow action domain, zero boundary charge, or coupling owner. Therefore using this construction now would be closure in cleaner notation, not a derived local-GR theorem.

So `q_R_hat=0` is demoted to closure-only unless a future parent action signs the schema. The next productive local route is beta/source-normalized second order, because local GR still needs more than gamma/q_R_hat.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Parent Action Source Neutrality Schema

{md_table(rows_by_name["schema"], ["schema_id", "clause", "current_status", "if_signed", "current_blocker", "valid_for_claim"])}

## Vertical Generator Construction Attempt

{md_table(rows_by_name["generator"], ["generator_id", "target", "current_status", "consequence", "current_blocker", "valid_for_claim"])}

## Closure Demotion Ledger

{md_table(rows_by_name["closure"], ["demotion_id", "object", "reason", "new_status", "closure_only_if_used_now", "valid_for_claim"])}

## qRhat Status Update

{md_table(rows_by_name["qrhat"], ["update_id", "symbols", "conditional_zero_formula", "current_value", "current_status", "valid_for_claim"])}

## Full PPN Branch Update

{md_table(rows_by_name["ppn"], ["branch_update_id", "component", "current_status", "missing_for_claim", "next_role", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_parent_action_schemas", "accepted_zero_theorems", "reason", "runner_ready", "valid_for_claim"])}

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
        "schema": schema_rows(),
        "generator": generator_rows(),
        "closure": closure_rows(),
        "qrhat": qrhat_rows(),
        "ppn": ppn_rows(),
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
    overall = next(row for row in validation if row["validation_id"] == "VAL2892_OVERALL")
    print(f"VAL2892_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
