from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2811-Y5-R2FR-Ploc-norm-commutator-certificate-or-first-DeltaK00-source-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2811_SOURCE_REGISTER.csv",
    "norm_counterexample": MTS / "P8_Y5_R2FR_2811_PLOC_NORM_COUNTEREXAMPLE.csv",
    "orthogonal_theorem": MTS / "P8_Y5_R2FR_2811_PLOC_ORTHOGONAL_PROJECTOR_THEOREM.csv",
    "commutator": MTS / "P8_Y5_R2FR_2811_PLOC_COMMUTATOR_THEOREM_ATTEMPT.csv",
    "qbound": MTS / "P8_Y5_R2FR_2811_QDELTAK_BOUND_INTERFACE.csv",
    "deltak00": MTS / "P8_Y5_R2FR_2811_DELTAK00_SOURCE_REVIEW.csv",
    "gates": MTS / "P8_Y5_R2FR_2811_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2811_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2811_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2811_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2811_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "norm_counterexample_queue": RAB_QUEUE / "JR2811_PLOC_NORM_COUNTEREXAMPLE_NONCLAIM.csv",
    "orthogonal_theorem_queue": RAB_QUEUE / "JR2811_PLOC_ORTHOGONAL_PROJECTOR_THEOREM_NONCLAIM.csv",
    "commutator_queue": RAB_QUEUE / "JR2811_PLOC_COMMUTATOR_THEOREM_ATTEMPT_NONCLAIM.csv",
    "qbound_beta_doc": BETA_DOCS / "PLOC_QDELTAK_BOUND_INTERFACE_2811_NONCLAIM.csv",
    "local_bound_copy": LOCAL_BOUNDS / "Ploc_norm_commutator_bound_interface_2811_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_Ploc_norm_commutator_2811_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2811_CHAINMAP_OR_CBOUND_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sp(path: Path) -> str:
    return str(path)


def ensure_dirs() -> None:
    directories = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def build_sources() -> list[dict[str, Any]]:
    local_sources = [
        ("2810_next", MTS / "P8_Y5_R2FR_2810_NEXT_TARGET.csv", "authoritative 2811 target"),
        ("2810_ploc_unit", MTS / "P8_Y5_R2FR_2810_PLOC_UNIT_CERTIFICATE.csv", "P_loc unit-only predecessor"),
        ("2810_qdelta_units", MTS / "P8_Y5_R2FR_2810_QDELTAK_UNIT_UPDATE.csv", "q_DeltaK unit predecessor"),
        ("2810_deltak00", MTS / "P8_Y5_R2FR_2810_DELTAK00_SOURCE_ATTEMPT.csv", "DeltaK00 source attempt predecessor"),
        ("2809_derivative", MTS / "P8_Y5_R2FR_2809_DELTAK_DERIVATIVE_BOUND_INTERFACE.csv", "DeltaK derivative bound predecessor"),
        ("2809_components", MTS / "P8_Y5_R2FR_2809_DELTAK_COMPONENT_BOUND_TABLE.csv", "DeltaK component split predecessor"),
        ("2485_field_sort", LOCAL_BOUNDS / "Parent_field_sort_table_2485_NONCLAIM.csv", "P_loc as projector/readout map"),
        ("2570_quotient_sort", LOCAL_BOUNDS / "Parent_field_sort_quotient_attempt_2570_NONCLAIM.csv", "fixed-before-variation P_loc obstruction"),
        ("2523_readout_reentry", LOCAL_BOUNDS / "Readout_reentry_audit_2523_NONCLAIM.csv", "fixed projector and commutator countermodel"),
        ("2603_sigma_delta", LOCAL_BOUNDS / "SigmaX_tail_law_bridge_2603_NONCLAIM.csv", "Delta_K projected-divergence schema"),
        ("2407_projector_commutator_doc", WORK / "2407-Y5-R2FR-projector-PiM-commutator-variation-zero-or-operator-coefficient-bound.md", "conditional fixed chain-map theorem and projector stress audit"),
        ("1014_commutator_doc", WORK / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md", "older commutator theorem/bound guardrail"),
        ("1019_projector_orthogonality_doc", WORK / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md", "projector orthogonality route and failure clauses"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role in local_sources:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": sp(path),
                "exists_or_reachable": path.exists(),
                "contains_text": bool(text.strip()) if path.exists() else False,
                "role": role,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_norm_counterexample_rows() -> list[dict[str, Any]]:
    shear = 10.0
    euclidean_operator_norm = math.sqrt(1.0 + shear * shear)
    rows = [
        {
            "case_id": "NCE2811_0_idempotent_not_norm_one",
            "matrix": f"[[1,{shear:g}],[0,0]]",
            "property_checked": "P^2=P",
            "result": "true",
            "operator_norm_2": f"{euclidean_operator_norm:.12g}",
            "lesson": "idempotence alone allows non-orthogonal projectors with norm greater than one",
            "status": "COUNTEREXAMPLE_PROVES_SHORTCUT_INVALID",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        },
        {
            "case_id": "NCE2811_1_projector_bound_rule",
            "matrix": "generic idempotent P_loc",
            "property_checked": "||P_loc||",
            "result": "C_Ploc retained",
            "operator_norm_2": "MISSING_PARENT_INNER_PRODUCT_AND_ORTHOGONALITY",
            "lesson": "future q_DeltaK bounds must carry C_Ploc unless the parent proves orthogonal projection",
            "status": "BOUND_CONSTANT_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        },
    ]
    return rows


def build_orthogonal_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OPT2811_0_target",
            "orthogonal projector theorem",
            "If a fixed positive parent inner product <.,.>_loc exists and P_loc^2=P_loc=P_loc^dagger, then ||P_loc||=1 on im(P_loc) and <=1 globally.",
            "standard finite/local Hilbert bundle projector theorem",
            "TARGET_SHARP",
            "would set C_Ploc=1 only under the signed premises",
        ),
        (
            "OPT2811_1_inner_product",
            "fixed local inner product",
            "<X,Y>_loc is parent-owned, positive on the residual bundle, and selected before readout/domain fitting",
            "2485/2570 retain projector/readout ownership but do not sign a fixed inner product",
            "MISSING_PARENT_INNER_PRODUCT",
            "C_Ploc remains free",
        ),
        (
            "OPT2811_2_self_adjoint",
            "self-adjointness",
            "P_loc=P_loc^dagger in the same inner product",
            "no current source proves the local readout projector is orthogonal rather than oblique",
            "MISSING_SELF_ADJOINT_PROJECTOR",
            "cannot promote norm-one",
        ),
        (
            "OPT2811_3_domain_lock",
            "domain/support lock",
            "the projector domain, local collar, source worldtube, and observed coframe are fixed before variation",
            "2523/2570 keep fixedness as a missing signature",
            "MISSING_DOMAIN_LOCK",
            "domain motion can create projector stress/commutator terms",
        ),
        (
            "OPT2811_4_verdict",
            "norm-one certificate",
            "C_Ploc=1",
            "conditional theorem is clean, but the parent premises are not signed",
            "FAIL_CURRENT_CLAIM",
            "retain C_Ploc>=1 or source/bound it",
        ),
    ]
    return [
        {
            "theorem_id": row[0],
            "item": row[1],
            "statement": row[2],
            "evidence": row[3],
            "status": row[4],
            "consequence": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_commutator_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "COM2811_0_product_rule",
            "projected derivative identity",
            "nabla(P_loc X)=P_loc nabla X + (nabla P_loc)X plus connection/domain representation terms",
            "exact obstruction form; matches 2523/2407 product-rule guardrails",
            "EXACT_OBSTRUCTION_ACTIVE",
            "commutator must be zeroed or bounded",
        ),
        (
            "COM2811_1_chainmap_zero",
            "fixed chain-map zero theorem",
            "if P_loc is a parent-selected chain map on the physical residual/current complex, then [nabla,P_loc]X=0 on that complex",
            "2407 proves the algebraic route conditionally for Pi_M-style projectors",
            "CONDITIONAL_THEOREM_CLEAN",
            "would set C_comm=0 only on the signed physical complex",
        ),
        (
            "COM2811_2_covariant_parallel",
            "parallel projector route",
            "nabla_lambda P_loc^nu_rho=0 on the local collar in the same connection used in q_DeltaK",
            "not supplied by current parent action or local collar frame",
            "MISSING_PARALLEL_PROJECTOR",
            "retain C_comm",
        ),
        (
            "COM2811_3_domain_dependency",
            "domain/readout dependency",
            "if P_loc depends on source support, Hodge data, boundary/reference surfaces, or observer coframe, nabla P_loc and delta P_loc terms survive",
            "2523 and 2407 explicitly keep these as live residuals",
            "COUNTERMODEL_ACTIVE",
            "cannot declare [P_loc,nabla]=0 by notation",
        ),
        (
            "COM2811_4_verdict",
            "commutator-zero certificate",
            "[P_loc,nabla]Delta_K=0",
            "conditional zero theorem exists but physical current complex/domain lock is unsigned",
            "ZERO_NOT_PROVED",
            "carry C_comm||Delta_K|| in q_DeltaK bound",
        ),
    ]
    return [
        {
            "commutator_id": row[0],
            "item": row[1],
            "statement": row[2],
            "evidence": row[3],
            "status": row[4],
            "consequence": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_qbound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QB2811_0_CPloc",
            "C_Ploc := ||P_loc||",
            "dimensionless >=1 unless an orthogonal projector theorem signs C_Ploc=1",
            "NORM_CONSTANT_RETAINED",
        ),
        (
            "QB2811_1_Ccomm",
            "C_comm := ||nabla P_loc|| plus connection/domain representation terms",
            "inverse-length or appropriate connection scale; zero only if P_loc is covariantly fixed",
            "COMMUTATOR_CONSTANT_RETAINED",
        ),
        (
            "QB2811_2_component_derivatives",
            "D_Delta := C_t||partial_t Delta_K^{0nu}||+C_r||partial_r Delta_K^{rnu}||+C_ang||partial_ang Delta_K||+C_conn||Gamma_conn||||Delta_K||",
            "force-density envelope from 2809 derivative split",
            "COMPONENT_VALUES_MISSING",
        ),
        (
            "QB2811_3_commutator_term",
            "C_comm ||Delta_K||",
            "force-density contribution from projector derivative/domain leakage",
            "BOUND_FORM_ONLY",
        ),
        (
            "QB2811_4_total",
            "||q_DeltaK|| <= C_Ploc D_Delta + C_comm ||Delta_K||",
            "first cleaner bound interface after unit certificate; nonnumeric because components/constants missing",
            "DERIVED_BOUND_INTERFACE_NONNUMERIC",
        ),
        (
            "QB2811_5_score_gate",
            "acceleration/PPN score",
            "still requires Delta_K components, C_Ploc/C_comm values or zero theorems, zeta/body measure, and no measured-G absorption guard",
            "NOT_SCORE_READY",
        ),
    ]
    return [
        {
            "bound_id": row[0],
            "quantity": row[1],
            "bound_or_definition": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_deltak00_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DK002811_0_current_state",
            "Delta_K^{00}",
            "definition exists but no K_hat^{00} component source exists in the 2808-2810 chain",
            "MISSING_COMPONENT_SOURCE",
            "do not guess it",
        ),
        (
            "DK002811_1_Kmetric_side",
            "K_metric^{00}",
            "K_metric^{00}=Gamma_eff g^{00}-T_GK^{00} remains conditional on an explicit Gamma_eff functional and metric variation",
            "CONDITIONAL_EXPRESSION_ONLY",
            "derive from parent action if available",
        ),
        (
            "DK002811_2_Khat_side",
            "K_hat^{00}",
            "no source-backed K_hat energy component was found in the current target inputs",
            "MISSING_KHAT00",
            "hunt original corpus or derive from L_parent",
        ),
        (
            "DK002811_3_verdict",
            "DeltaK00 route",
            "2811 does not improve DeltaK00 directly; it improves the P_loc/operator side of the q_DeltaK bound",
            "UNCHANGED_BLOCKER",
            "next work can choose K_hat^{00} sourcing if P_loc proof stalls",
        ),
    ]
    return [
        {
            "review_id": row[0],
            "quantity": row[1],
            "finding": row[2],
            "status": row[3],
            "next_action": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2811_0_norm_shortcut_rejected", "idempotence alone proves ||P_loc||=1", False, "explicit oblique idempotent counterexample has norm greater than one"),
        ("CG2811_1_conditional_norm_theorem", "orthogonal projector theorem is written", True, "clean conditional theorem exists but premises are unsigned"),
        ("CG2811_2_norm_one_claim", "C_Ploc=1 is claim-ready", False, "fixed positive inner product and self-adjoint P_loc are missing"),
        ("CG2811_3_conditional_commutator_theorem", "fixed chain-map/parallel projector theorem is written", True, "conditional route exists"),
        ("CG2811_4_commutator_zero_claim", "[P_loc,nabla]=0 is claim-ready", False, "physical complex/domain lock/covariant fixedness are missing"),
        ("CG2811_5_qDelta_bound_interface", "q_DeltaK bound interface is improved", True, "C_Ploc and C_comm are now explicit"),
        ("CG2811_6_DeltaK00_component", "DeltaK00 is sourced", False, "K_hat^{00} remains missing"),
        ("CG2811_7_local_claim", "local-GR/WEP/PPN/orbital claim can be made", False, "operator constants and Delta_K components remain unresolved"),
        ("CG2811_8_nonclaim_pack", "2811 nonclaim proof/bound pack is ready", True, "next target is chain-map equality or finite C-bound acquisition"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim": row[1],
            "gate_pass": row[2],
            "reason": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2811_0_no_free_norm",
            "The norm-one shortcut is mathematically rejected.",
            "An oblique idempotent can have arbitrarily large operator norm.",
            "keep C_Ploc unless orthogonality is parent-signed",
        ),
        (
            "DEC2811_1_conditional_clean",
            "The exact theorem we need is now written.",
            "A parent-fixed positive inner product plus P_loc=P_loc^dagger would give norm one.",
            "hunt the parent inner product/self-adjoint projector signature",
        ),
        (
            "DEC2811_2_commutator_clean",
            "The commutator route is also now sharp.",
            "A fixed chain map/covariantly parallel P_loc kills [P_loc,nabla], but current evidence keeps domain/readout leakage active.",
            "prove physical chain-map equality or carry C_comm",
        ),
        (
            "DEC2811_3_bound_progress",
            "q_DeltaK has a cleaner nonnumeric bound.",
            "The envelope now separates C_Ploc from C_comm and Delta_K component derivatives.",
            "turn either C_Ploc/C_comm or DeltaK00 into a sourced row next",
        ),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2811_0_2812",
            "next_target": "2812-Y5-R2FR-Ploc-chainmap-equality-or-Cploc-Ccomm-source-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Ploc_chainmap_equality_or_Cploc_Ccomm_source_bound_under_AX1090_2812.py",
            "objective": "try to prove the physical local projector is a parent-selected orthogonal chain map on the same residual/current complex; if not, create source-ready C_Ploc and C_comm bound rows",
            "include": "parent inner product; P_loc self-adjointness; physical current complex; chain-map equality; covariantly fixed local collar; C_Ploc/C_comm units; Delta_K component derivative interface",
            "exclude": "norm-one from idempotence; commutator-zero from notation; hiding projector stress in measured G/GM; proxy scoring; local-GR/WEP/PPN/orbital claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["norm_counterexample"], BRANCH_OUTPUTS["norm_counterexample_queue"], "norm_counterexample_queue"),
        (OUTPUTS["orthogonal_theorem"], BRANCH_OUTPUTS["orthogonal_theorem_queue"], "orthogonal_theorem_queue"),
        (OUTPUTS["commutator"], BRANCH_OUTPUTS["commutator_queue"], "commutator_queue"),
        (OUTPUTS["qbound"], BRANCH_OUTPUTS["qbound_beta_doc"], "qbound_beta_doc"),
        (OUTPUTS["qbound"], BRANCH_OUTPUTS["local_bound_copy"], "local_bound_copy"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2811_{label}",
                "source": sp(source),
                "destination": sp(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def local_path_tokens(value: Any) -> list[Path]:
    if not value:
        return []
    paths: list[Path] = []
    for token in str(value).split(";"):
        token = token.strip()
        if not token or token == "MISSING" or token.startswith("http"):
            continue
        candidate = Path(token)
        if not candidate.is_absolute():
            candidate = WORK / candidate
        if candidate.suffix or candidate.drive:
            paths.append(candidate)
    return paths


def cited_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            for key in ("source_path", "source_paths", "source", "destination", "path_or_url"):
                paths.extend(local_path_tokens(row.get(key)))
    return all(path.exists() for path in paths)


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    counterexample = sections["norm_counterexample"][0]
    checks = [
        ("VAL2811_0_sources_exist", all(row["exists_or_reachable"] for row in sections["sources"]), "all source-register local paths exist"),
        ("VAL2811_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register entries contain text/source evidence"),
        ("VAL2811_2_idempotent_counterexample", counterexample["result"] == "true" and float(counterexample["operator_norm_2"]) > 1.0, "idempotent-not-norm-one counterexample is numeric"),
        ("VAL2811_3_norm_claim_blocked", any(row["theorem_id"] == "OPT2811_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["orthogonal_theorem"]), "norm-one claim is blocked"),
        ("VAL2811_4_commutator_claim_blocked", any(row["commutator_id"] == "COM2811_4_verdict" and row["status"] == "ZERO_NOT_PROVED" for row in sections["commutator"]), "commutator-zero claim is blocked"),
        ("VAL2811_5_qbound_interface_present", any(row["bound_id"] == "QB2811_4_total" and row["status"] == "DERIVED_BOUND_INTERFACE_NONNUMERIC" for row in sections["qbound"]), "C_Ploc/C_comm q_DeltaK bound interface is present"),
        ("VAL2811_6_DeltaK00_still_missing", any(row["review_id"] == "DK002811_3_verdict" and row["status"] == "UNCHANGED_BLOCKER" for row in sections["deltak00"]), "DeltaK00 remains explicitly unsourced"),
        ("VAL2811_7_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2811_8_next_target_2812", any(row["next_id"] == "NEXT2811_0_2812" for row in sections["next"]), "next target is 2812"),
        ("VAL2811_9_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2811_10_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2811_11_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2811_12_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2811_13_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2811_14_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2811_15_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2811_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2811_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2811 rejects the idempotent-to-norm-one shortcut, writes conditional orthogonal/chain-map theorems, and retains C_Ploc/C_comm in a nonnumeric q_DeltaK bound.",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2811 - Y5 R2FR Ploc Norm Commutator Certificate Or First DeltaK00 Source Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2811 gets a real mathematical cleanup: the shortcut `P_loc^2=P_loc`, therefore `||P_loc||=1`, is false. An oblique idempotent projector can have norm greater than one, so `C_Ploc` must stay live unless the parent action signs an orthogonal projector structure.",
        "",
        "The clean conditional theorem is now explicit: if a fixed positive parent inner product exists and `P_loc=P_loc^dagger` on the same residual bundle, then `C_Ploc=1`. If `P_loc` is also a parent-selected chain map or covariantly parallel on the local collar, then `[P_loc,nabla]` vanishes on the physical complex.",
        "",
        "Current MTS evidence does not sign those premises. The useful result is therefore not a local-GR pass; it is a sharper nonnumeric residual bound `||q_DeltaK|| <= C_Ploc D_Delta + C_comm ||Delta_K||`, with the exact missing constants exposed.",
        "",
        "## Norm Counterexample",
        markdown_table(sections["norm_counterexample"], ["case_id", "matrix", "property_checked", "result", "operator_norm_2", "status"]),
        "",
        "## Orthogonal Projector Theorem Attempt",
        markdown_table(sections["orthogonal_theorem"], ["theorem_id", "item", "statement", "status", "consequence"]),
        "",
        "## Commutator Theorem Attempt",
        markdown_table(sections["commutator"], ["commutator_id", "item", "statement", "status", "consequence"]),
        "",
        "## q_DeltaK Bound Interface",
        markdown_table(sections["qbound"], ["bound_id", "quantity", "bound_or_definition", "status"]),
        "",
        "## DeltaK00 Source Review",
        markdown_table(sections["deltak00"], ["review_id", "quantity", "finding", "status", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "norm_counterexample": build_norm_counterexample_rows(),
        "orthogonal_theorem": build_orthogonal_theorem_rows(),
        "commutator": build_commutator_rows(),
        "qbound": build_qbound_rows(),
        "deltak00": build_deltak00_rows(),
    }
    sections["gates"] = build_gate_rows()
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
