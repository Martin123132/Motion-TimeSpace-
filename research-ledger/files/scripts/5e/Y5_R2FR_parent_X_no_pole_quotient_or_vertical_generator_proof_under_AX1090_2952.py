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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2952"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2952-Y5-R2FR-parent-X-no-pole-quotient-or-vertical-generator-proof-under-AX1090.md"

SRC_2951_DOC = ROOT / "2951-Y5-R2FR-parent-X-field-owner-or-ZX-MX2-source-row-under-AX1090.md"
SRC_2951_NEXT = RESIDUALS / "P8_Y5_R2FR_2951_NEXT_TARGET.csv"
SRC_2951_OWNER = RESIDUALS / "P8_Y5_R2FR_2951_PARENT_X_OWNER_CONTRACT.csv"
SRC_2951_ROUTE = RESIDUALS / "P8_Y5_R2FR_2951_PARENT_X_ROUTE_TRIAGE.csv"
SRC_670_NOPOLE = RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv"
SRC_2670_ERASURE = RESIDUALS / "P8_Y5_R2FR_QUOTIENT_ERASURE_2670_ERASURE_CERTIFICATE_AUDIT.csv"
SRC_2671_VERTICAL = RESIDUALS / "P8_Y5_R2FR_VERTICAL_FIRST_CLASS_2671_CERTIFICATE_AUDIT.csv"
SRC_2589_KERNEL = RESIDUALS / "P8_Y5_VERTICAL_KERNEL_2589_CERTIFICATE_GATE.csv"
SRC_2590_QV = RESIDUALS / "P8_Y5_VERTICAL_QV_2590_EXTRACTION_CONTRACT.csv"
SRC_2591_SECTOR = RESIDUALS / "P8_Y5_VERTICAL_SECTOR_2591_VARIATION_LEDGER.csv"
SRC_2882_CERT = RESIDUALS / "P8_Y5_R2FR_2882_Q_OBJECT_VERTICALITY_CERTIFICATE.csv"
SRC_2892_GEN = RESIDUALS / "P8_Y5_R2FR_2892_VERTICAL_GENERATOR_CONSTRUCTION_ATTEMPT.csv"
SRC_2902_QV = RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_EXTRACTION_CONTRACT.csv"
SRC_2903_SECTOR = RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_VARIATION_LEDGER.csv"
SRC_1042_PREMISE = RESIDUALS / "P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv"
SRC_1042_IDENTITY = RESIDUALS / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2952_SOURCE_REGISTER.csv",
    "quotient": RESIDUALS / "P8_Y5_R2FR_2952_NOPOLE_QUOTIENT_AUDIT.csv",
    "vertical": RESIDUALS / "P8_Y5_R2FR_2952_VERTICAL_GENERATOR_AUDIT.csv",
    "join": RESIDUALS / "P8_Y5_R2FR_2952_NOPOLE_JOIN_CERTIFICATE.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_2952_PHYSICAL_X_DEMOTION_AND_SOURCE_PACK_ROUTE.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2952_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2952_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2952_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2952_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2952_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "quotient_copy": PARENT_ACTION / "no_pole_quotient_audit_2952_NOT_DERIVED.csv",
    "vertical_copy": PARENT_ACTION / "vertical_generator_audit_2952_NOT_DERIVED.csv",
    "demotion_copy": PARENT_ACTION / "physical_X_demotion_source_pack_route_2952_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2952_POSITIVE_PHYSICAL_X_HESSIAN_SOURCE_PACK_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


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
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2952_00_2951_doc", SRC_2951_DOC, "NEXT2951_0_2952;Validation overall: `True`", "2951 hard-fork handoff"),
        ("SRC2952_01_2951_next", SRC_2951_NEXT, "NEXT2951_0_2952", "machine-readable 2952 target"),
        ("SRC2952_02_2951_owner", SRC_2951_OWNER, "OWN2951_10_verdict", "parent X owner contract"),
        ("SRC2952_03_2951_route", SRC_2951_ROUTE, "ROUTE2951_0_absent_quotient;ROUTE2951_1_first_class_vertical", "selected no-pole routes"),
        ("SRC2952_04_670_nopole", SRC_670_NOPOLE, "NQ670_0_null_distribution;NQ670_8_no_pole_result", "older no-pole proof chain"),
        ("SRC2952_05_2670_erasure", SRC_2670_ERASURE, "QER2670_0_contract;QER2670_10_verdict", "absent quotient erasure audit"),
        ("SRC2952_06_2671_vertical", SRC_2671_VERTICAL, "VFC2671_1_parent_symplectic_package;VFC2671_9_verdict", "vertical first-class audit"),
        ("SRC2952_07_2589_kernel", SRC_2589_KERNEL, "VKC2589_0_vertical_basis;VKC2589_8_no_tautology", "vertical kernel certificate gate"),
        ("SRC2952_08_2590_qv", SRC_2590_QV, "VQC2590_0_parent_variation;VQC2590_7_verdict", "vertical Q_v extraction contract"),
        ("SRC2952_09_2591_sector", SRC_2591_SECTOR, "VSL2591_0_EH_reference;VSL2591_6_total", "vertical sector variation ledger"),
        ("SRC2952_10_2882_cert", SRC_2882_CERT, "CERT2882_0_exact_kernel_contract;CERT2882_9_joint_certificate", "q-object verticality certificate"),
        ("SRC2952_11_2892_generator", SRC_2892_GEN, "VGC2892_0_generator;VGC2892_5_verdict", "vertical generator construction attempt"),
        ("SRC2952_12_2902_qv", SRC_2902_QV, "VQC2902_0_parent_variation;VQC2902_7_verdict", "recent vertical Q_v extraction contract"),
        ("SRC2952_13_2903_sector", SRC_2903_SECTOR, "VSL2903_0_EH_reference;VSL2903_6_total", "recent vertical sector Q_v ledger"),
        ("SRC2952_14_1042_premise", SRC_1042_PREMISE, "NHP1042_0_LX_owner;NHP1042_6_verdict", "physical positive X fallback premise gates"),
        ("SRC2952_15_1042_identity", SRC_1042_IDENTITY, "NH1042_1_energy_identity;NH1042_5_verdict", "conditional positive X no-hair identity"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def quotient_rows() -> list[dict[str, Any]]:
    rows = [
        ("QNP2952_0_contract", "absent quotient no-pole route", "X is absent from physical tangent space before variation, not deleted after readout", "TARGET_EXACT", "2670 and 2951 select this as the cleanest local-GR route", False),
        ("QNP2952_1_parent_q_object", "parent q object", "q: Conf_parent -> Q_obs is canonical, domain-scoped, and parent-owned before matter/readout", "BLOCKED_Q_OBJECT_NOT_PARENT_SIGNED", "2882 says q object is not parent-signed; 2670 says q is conditional only", False),
        ("QNP2952_2_null_distribution", "integrable invariant N_X", "N_X is invariant, integrable, local-domain admissible, and contains the local X directions", "NOT_PARENT_SIGNED", "2670/670 leave field-space distribution, compact-domain admissibility and symmetry invariance unsigned", False),
        ("QNP2952_3_Dq_kernel", "Dq[v_X]=0", "Dq is computed against the actual observed stack, source/readout data, constants and boundary/projector maps", "BLOCKED_DQ_OPERATOR_NOT_COMPUTABLE", "2882 records exact conditional theorem but live Dq computation is missing", False),
        ("QNP2952_4_open_branch", "open-branch kernel", "Dq[v_X]=0 holds as a branch identity, not at a point or by symbol choice", "BLOCKED_OPEN_BRANCH_KERNEL_NOT_SIGNED", "2882 refuses pointwise/post-hoc verticality", False),
        ("QNP2952_5_action_descent", "action descent", "S_bulk[Phi]=S_red[q(Phi)] plus fixed boundary/topological terms before variation", "CONDITIONAL_ONLY", "670/2670 keep explicit parent Lagrangian and boundary/domain descent unsigned", False),
        ("QNP2952_6_matter_descent", "ordinary matter descent", "S_matter=Sbar_m[Obs(q(Phi)),psi,theta_A] and constants/material markers are Lie_vX silent", "GEOMETRY_CHAIN_RULE_CONDITIONAL_MARKERS_OPEN", "2670/2882 keep markers, constants, EM/clocks/masses and direct source slots open", False),
        ("QNP2952_7_geometry_extension", "measure/coframe/connection descent", "volume, observed coframe, metric connection and matter connection all factor through q", "UNSIGNED_GEOMETRY_FUNCTOR_EXTENSION", "2670 says connection/coframe descent is not signed for every matter/clock arena", False),
        ("QNP2952_8_boundary_projector", "boundary/projector silence", "Q_X=0/proper/exact, K_boundary=0, and Pi_M^H[Q_X]=0 on compact local branch", "BLOCKED_BOUNDARY_PROJECTOR_SILENCE", "2670/670 keep B_X primitive, weighted Stokes, projector orthogonality and cocycle open", False),
        ("QNP2952_9_degree_count", "degree/rank removal", "constraints remove the X pair and reduced Omega has no proper X stabilizer", "NOT_CHECKED", "2670/670 keep constraint rank, bracket closure and stabilizer theorem missing", False),
        ("QNP2952_10_countermodel_guard", "visible/full-metric countermodel", "if q observes hidden pieces separately, X is visible and not a quotient direction", "COUNTERMODEL_ACTIVE", "2882 and 2892 retain full-metric/direct-readout countermodels", False),
        ("QNP2952_11_verdict", "quotient no-pole proof", "QNP2952_1 through QNP2952_9 all close without triggering countermodels", "QUOTIENT_NOPOLE_NOT_DERIVED", "conditional theorem exists; parent q, Dq, matter, boundary and degree certificates do not close", False),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "clause": clause,
                "required_statement": required,
                "current_status": status,
                "evidence_summary": evidence,
                "theorem_zero_credit": credit,
                "demote_if_missing": audit_id != "QNP2952_0_contract",
            }
        )
        for audit_id, clause, required, status, evidence, credit in rows
    ]


def vertical_rows() -> list[dict[str, Any]]:
    rows = [
        ("VNP2952_0_contract", "first-class vertical route", "X is a gauge/constraint direction, not a local propagating or sourced field", "TARGET_EXACT", "2671 and 2951 select this as the active theorem-zero route", False),
        ("VNP2952_1_parent_omega", "parent Theta/Omega package", "delta L_parent=E delta Phi+dTheta_parent and Omega exists on all variables used by the branch", "MISSING_PARENT_OMEGA", "2671/2590/2902 all mark total parent action and Theta/Omega missing", False),
        ("VNP2952_2_DCX_operator", "explicit C_X and DC_X", "C_X and linearization DC_X are written from the parent action with fixed domain and boundary pairing", "MISSING_DCX_OPERATOR", "2671 says the adjoint side exists only formally; no operator is owned", False),
        ("VNP2952_3_raise_index", "v_X from Omega inverse", "v_X=Omega^{-1}[(DC_X)^dagger X] on the reduced domain", "CONDITIONAL_MAP_VALUES_MISSING", "2671 preserves the category correction: DCdagger is not itself v_X", False),
        ("VNP2952_4_field_action", "field-by-field vertical action", "v_X acts on metric/coframe, canonical variables, memory/projectors, matter lift and boundary/reference fields", "MISSING_FIELD_BY_FIELD_VERTICAL_ACTION", "2671/2882/2902 all keep full field action missing", False),
        ("VNP2952_5_momentum_map", "momentum map identity", "delta G_X=Omega(delta Phi,v_X) with G_X=int epsilon C_X+Q_X", "MOMENTUM_MAP_OWNER_NOT_DERIVED", "2671/2590 say Q_v and constraints are notation until extracted from parent Theta/Omega", False),
        ("VNP2952_6_boundary_charge", "proper/zero/exact boundary charge", "Q_X cancels boundary variation and is zero, proper gauge, or exact on the compact branch", "BOUNDARY_CHARGE_ZERO_NOT_DERIVED", "2671/2591/2903 retain boundary/reference ambiguity and edge charge leakage", False),
        ("VNP2952_7_bracket_closure", "first-class bracket closure", "{G_X[epsilon],G_X[eta]} closes weakly with no boundary cocycle", "BRACKET_CLOSURE_NOT_COMPUTED", "2671 and 670 keep bracket closure and cocycle checks missing", False),
        ("VNP2952_8_degree_count", "constraint rank and no stabilizer", "primary/secondary constraints remove the X pair and reduced Omega has no proper X stabilizer", "DEGREE_COUNT_NOT_CHECKED", "2671/2589 keep rank, bracket and stabilizer missing", False),
        ("VNP2952_9_sector_total", "sector-complete Q_v", "EH, boundary, extra, projector, matter/source and constraint pieces sum to a zero/proper total Q_v", "TOTAL_NOT_PROMOTED", "2591/2903 show sector ledgers but no sector-complete total Q_v extraction", False),
        ("VNP2952_10_no_tautology", "no projection-by-declaration", "q/v are not promoted merely by putting observed variables into q by hand", "PROJECTION_BY_DECLARATION_BLOCK_ACTIVE", "2589 guard active; useful but not a proof", False),
        ("VNP2952_11_verdict", "vertical first-class no-pole proof", "VNP2952_1 through VNP2952_9 all close in one parent branch", "VERTICAL_FIRST_CLASS_NOPOLE_NOT_DERIVED", "the route is mathematically exact but parent symplectic package, field map, charge, bracket and degree count remain missing", False),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "clause": clause,
                "required_statement": required,
                "current_status": status,
                "evidence_summary": evidence,
                "theorem_zero_credit": credit,
                "demote_if_missing": audit_id != "VNP2952_0_contract",
            }
        )
        for audit_id, clause, required, status, evidence, credit in rows
    ]


def join_rows() -> list[dict[str, Any]]:
    rows = [
        ("JOIN2952_0_conditional_theorem", "conditional no-pole theorem", "if parent q object, v_X in ker(Dq), action/matter descent, proper boundary charge, bracket closure and degree count all hold, then no physical X pole contributes", "CONDITIONAL_THEOREM_VALID", True, False),
        ("JOIN2952_1_quotient_route", "absent quotient branch", "QNP2952_1..9 close and countermodels are excluded", "FAILED_CURRENT_CERTIFICATE", False, False),
        ("JOIN2952_2_vertical_route", "first-class vertical branch", "VNP2952_1..9 close and projection-by-declaration is avoided", "FAILED_CURRENT_CERTIFICATE", False, False),
        ("JOIN2952_3_no_pole_claim", "K_X=qbar_XT=Qbar_XH=0 by no-pole theorem", "one no-pole route closes with matter/source/boundary extension", "NOT_CLAIMED", False, False),
        ("JOIN2952_4_local_GR_effect", "local GR/Newton recovery via erased X sector", "no X Green function, no source/test charge and no edge charge remain", "NOT_CLAIMED", False, False),
        ("JOIN2952_5_verdict", "2952 hard-fork verdict", "no-pole route is not proved; demote to positive physical X Hessian/source-pack route", "NOPOLE_NOT_DERIVED_DEMOTE_TO_PHYSICAL_X", False, False),
    ]
    return [
        add_common(
            {
                "join_id": join_id,
                "object": obj,
                "required_condition": required,
                "current_status": status,
                "conditional_math_available": conditional,
                "certificate_pass": passed,
            }
        )
        for join_id, obj, required, status, conditional, passed in rows
    ]


def demotion_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEM2952_0_physical_X_selected", "physical X route", "since neither absent quotient nor vertical first-class route closes, treat X as physical until proven otherwise", "SELECTED_AS_NEXT_DISCIPLINE", "no local-GR claim; build real Hessian/source pack"),
        ("DEM2952_1_positive_sourcefree_target", "positive source-free no-hair route", "derive parent L_X, field normalization, Z_X>0, M_X^2>0, J_X=0, Phi_boundary=0 and no kernel", "BEST_PHYSICAL_GR_REDUCTION_ROUTE", "if closed, X=0 locally without empirical fifth-force fitting"),
        ("DEM2952_2_sourced_residual_fallback", "finite residual branch", "if source-free/no-hair fails, source Z_X, M_X^2, lambda_X, K_X, Qbar_XH, qbar_XT and absolute tails", "EMPIRICAL_FALLBACK", "score R10/WEP/PPN/clocks/orbital arenas only after source-backed rows exist"),
        ("DEM2952_3_no_coefficient_scoring_yet", "scoring guard", "do not score alpha(lambda), I_X, PPN or local-GR while Z/M/source/boundary rows are placeholders", "GUARD_ACTIVE", "prevents cardboard-sword victories"),
        ("DEM2952_4_next", "2953 target", "attempt positive physical X Hessian/source-zero pack; if it fails, emit the finite residual source-pack queue", "NEXT_SELECTED", "moves forward instead of re-running quotient/vertical certificates"),
    ]
    return [
        add_common(
            {
                "demotion_id": demotion_id,
                "route": route,
                "statement": statement,
                "current_status": status,
                "next_effect": effect,
            }
        )
        for demotion_id, route, statement, status, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2952_0_quotient_no_pole", "absent quotient no-pole proof closes", False, "QUOTIENT_NOPOLE_NOT_DERIVED"),
        ("CG2952_1_vertical_no_pole", "first-class vertical no-pole proof closes", False, "VERTICAL_NOPOLE_NOT_DERIVED"),
        ("CG2952_2_QKT_zero", "K_X/qbar_XT/Qbar_XH are theorem-zero by no-pole", False, "NO_ZERO_CREDIT"),
        ("CG2952_3_parent_X_owner", "parent X owner acquired", False, "PARENT_X_OWNER_NOT_ACQUIRED"),
        ("CG2952_4_ZX_MX2", "Z_X/M_X^2 score-ready", False, "COEFFICIENTS_NOT_SCORE_READY"),
        ("CG2952_5_local_GR", "local GR/Newton reduction claim allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2952_6_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2952_0_result", "no-pole proof not derived", "both selected theorem-zero routes have exact conditional math but miss parent-owned q/v/action/matter/boundary/degree certificates", "do not claim K_X=0, qbar_XT=0, Qbar_XH=0 or local GR"),
        ("DEC2952_1_quotient_status", "absent quotient route fails current certificate", "q object, Dq computation, open-branch kernel, matter-marker descent, boundary/projector silence and degree count are unsigned", "do not call X a readout artefact yet"),
        ("DEC2952_2_vertical_status", "first-class vertical route fails current certificate", "parent Omega, DC_X, field-by-field generator, momentum map, boundary charge, bracket closure and degree count are missing", "do not call X gauge yet"),
        ("DEC2952_3_demote", "demote to physical X until proven otherwise", "this is the stricter and less-cheatable route after no-pole fails", "build positive Hessian/source-zero source pack next"),
        ("DEC2952_4_next", "build 2953 positive physical X Hessian/source-pack", "it attacks the same GR-reduction goal but through an owned physical operator rather than a quotient shortcut", "derive or source L_X, Z_X, M_X^2, J_X, Phi_boundary and kernel policy"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2952_0_2953",
                "priority": "selected_primary",
                "next_doc": "2953-Y5-R2FR-positive-physical-X-Hessian-source-pack-or-residual-demotion-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_positive_physical_X_Hessian_source_pack_or_residual_demotion_under_AX1090_2953.py",
                "objective": "Treat X as physical until proven otherwise. Try to derive or source a parent L_X with field normalization, Z_X>0, M_X^2>0, zero-mode policy, J_X=0, and Phi_boundary=0. If any premise fails, emit the finite residual source-pack queue without scoring placeholders.",
                "include": "parent L_X;field normalization;second variation;Z_X sign;M_X^2 gap;lambda_X;zero-mode policy;J_X channel zeros;Phi_boundary zero;finite residual source-pack queue",
                "exclude": "quotient no-pole re-run;vertical no-pole re-run;alpha(lambda) scoring;I_X scoring;EH-only substitution;orbital-GM denominator;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("quotient_copy", OUTPUTS["quotient"], BRANCH_OUTPUTS["quotient_copy"]),
        ("vertical_copy", OUTPUTS["vertical"], BRANCH_OUTPUTS["vertical_copy"]),
        ("demotion_copy", OUTPUTS["demotion"], BRANCH_OUTPUTS["demotion_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2952_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2952_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2952_2_quotient_verdict_blocked", any(row["audit_id"] == "QNP2952_11_verdict" and row["theorem_zero_credit"] is False for row in all_rows["quotient"]), "quotient no-pole verdict is blocked", True),
        ("VAL2952_3_vertical_verdict_blocked", any(row["audit_id"] == "VNP2952_11_verdict" and row["theorem_zero_credit"] is False for row in all_rows["vertical"]), "vertical no-pole verdict is blocked", True),
        ("VAL2952_4_join_demotes", any(row["join_id"] == "JOIN2952_5_verdict" and row["certificate_pass"] is False for row in all_rows["join"]), "join certificate demotes to physical X", True),
        ("VAL2952_5_physical_X_selected", any(row["demotion_id"] == "DEM2952_0_physical_X_selected" for row in all_rows["demotion"]), "physical X route is selected as next discipline", True),
        ("VAL2952_6_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates are blocked", True),
        ("VAL2952_7_next_target_written", any(row["next_id"] == "NEXT2952_0_2953" for row in all_rows["next"]), "2953 next target selected", True),
        ("VAL2952_8_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2952_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2952_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2952_11_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2952 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(
        add_common(
            {
                "validation_id": "VAL2952_OVERALL",
                "passed": overall,
                "check": "2952 validation overall",
                "required": True,
            }
        )
    )
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2952 - Y5 R2FR: parent X no-pole quotient or vertical-generator proof under AX1090

Status: `Y5_R2FR_2952_no_pole_not_derived_demote_to_positive_physical_X_source_pack`

Claim ceiling: `no_quotient_no_pole_no_vertical_no_pole_no_KX_zero_no_qbarXT_zero_no_QbarXH_zero_no_parent_X_owner_no_ZX_no_MX2_no_local_GR_no_Newton_no_R10_no_PPN_no_public_claim`

2952 tries the clean route first: erase the local `X` pole before variation by proving that `X` is either absent from the parent quotient or first-class vertical. The result is strict:

- The conditional no-pole theorem is mathematically valid: a parent-owned quotient/vertical certificate with action, matter, boundary, bracket, and degree closure would erase the physical `X` pole.
- Current MTS does not yet own that certificate: the quotient route lacks parent `q`, live `Dq`, open-branch kernel, matter-marker descent, boundary/projector silence, and degree count.
- The vertical route also does not close: parent `Theta/Omega`, `DC_X`, actual `v_X`, momentum map, boundary charge, bracket closure, and sector-complete `Q_v` remain missing.
- Therefore `X` must now be treated as physical until proven otherwise; the next work should attack the positive `L_X` Hessian/source-zero route, with finite residual rows as the honest fallback.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## No-Pole Quotient Audit

{md_table(all_rows["quotient"], ["audit_id", "clause", "current_status", "theorem_zero_credit", "evidence_summary"])}

## Vertical Generator Audit

{md_table(all_rows["vertical"], ["audit_id", "clause", "current_status", "theorem_zero_credit", "evidence_summary"])}

## No-Pole Join Certificate

{md_table(all_rows["join"], ["join_id", "object", "current_status", "conditional_math_available", "certificate_pass"])}

## Physical X Demotion And Source-Pack Route

{md_table(all_rows["demotion"], ["demotion_id", "route", "current_status", "next_effect"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "quotient": quotient_rows(),
        "vertical": vertical_rows(),
        "join": join_rows(),
        "demotion": demotion_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2952 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
