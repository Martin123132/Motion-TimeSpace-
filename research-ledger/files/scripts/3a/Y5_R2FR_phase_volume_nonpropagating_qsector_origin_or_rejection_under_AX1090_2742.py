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

DOC = ROOT / "2742-Y5-R2FR-phase-volume-nonpropagating-qsector-origin-or-rejection-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2742_SOURCE_REGISTER.csv",
    "origin": RESIDUALS / "P8_Y5_R2FR_2742_PHASE_VOLUME_ORIGIN_AUDIT.csv",
    "mapping": RESIDUALS / "P8_Y5_R2FR_2742_QSECTOR_MAPPING_NONCLAIM.csv",
    "obstructions": RESIDUALS / "P8_Y5_R2FR_2742_ORIGIN_OBSTRUCTION_LEDGER.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2742_ORIGIN_RUNNER_NONCLAIM.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2742_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2742_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2742_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2742_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2742_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "origin": SOURCE_WEIGHT / "phase_volume_qsector_origin_audit_2742_NONCLAIM.csv",
    "mapping": LOCAL_BOUNDS / "phase_volume_closure_mapping_2742_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2742_GAUGE_NOETHER_ZERO_CHARGE_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


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


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2742_0_2741_doc",
            "description": "2741 selects phase-volume/nonpropagating q-sector origin as the next theorem attempt.",
            "source_path": "2741-Y5-R2FR-minimal-parent-qsector-action-ansatz-or-rejection-under-AX1090.md",
            "required_needles": "NEXT2741_0_2742;ANS2741_5_phase_volume_nonpropagating_origin;VAL2741_OVERALL",
        },
        {
            "source_id": "SRC2742_1_1554_doc",
            "description": "prior phase-volume origin audit and obstruction ledger.",
            "source_path": "1554-Y5-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
            "required_needles": "ORG1554_0_radial_cell_rule;ORG1554_5_current_verdict;NEXT1554_0_1555",
        },
        {
            "source_id": "SRC2742_2_08_phase_volume",
            "description": "phase-volume reciprocity source file.",
            "source_path": "08-phase-volume-reciprocity-origin.md",
            "required_needles": "T sqrt(S) = 1;Generic volume preservation does not work;phase_volume_reciprocity_motivated_not_parent_derived",
        },
        {
            "source_id": "SRC2742_3_09_hamiltonian",
            "description": "Hamiltonian radial-cell derivation attempt.",
            "source_path": "09-hamiltonian-radial-cell-derivation.md",
            "required_needles": "J_tr = T sqrt(S);generic symplectic or Liouville phase-volume preservation does not derive p=1;hamiltonian_radial_cell_sharpened_not_parent_derived",
        },
        {
            "source_id": "SRC2742_4_1555_gauge_noether",
            "description": "prior gauge/Noether no-charge audit used to define the next live target.",
            "source_path": "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md",
            "required_needles": "GAUGE1555_4_first_class_constraint;RUN1555_3_current;NEXT1555_0_1556",
        },
        {
            "source_id": "SRC2742_5_1554_origin_csv",
            "description": "machine-readable 1554 phase-volume audit.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1554_PHASE_VOLUME_ORIGIN_AUDIT.csv",
            "required_needles": "ORG1554_0_radial_cell_rule;ORG1554_3_cell_current;ORG1554_5_current_verdict",
        },
        {
            "source_id": "SRC2742_6_2741_next_queue",
            "description": "live acquisition queue pointing into this checkpoint.",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR2741_PHASE_VOLUME_QSECTOR_ORIGIN_NEXT.csv",
            "required_needles": "NEXT2741_0_2742;phase-volume",
        },
        {
            "source_id": "SRC2742_7_2741_ansatz_csv",
            "description": "live minimal q-sector ansatz audit feeding this phase-volume route.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2741_MINIMAL_QSECTOR_ANSATZ_AUDIT.csv",
            "required_needles": "ANS2741_0_auxiliary_algebraic_positive_norm;ANS2741_5_phase_volume_nonpropagating_origin;NO_ACCEPTED_PARENT_ACTION",
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


def origin_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ORG2742_0_radial_cell_rule",
            "radial t-r observer-cell preservation",
            "J_tr=T sqrt(S)=1 <=> T^2 S=1 <=> q=R_AB=ln(T^2 S)=0",
            "selects p=1 exactly for S=(1-L)^(-p)",
            "MOTIVATED_NOT_PARENT_DERIVED",
            "separate radial cell preservation is precisely the missing parent theorem",
            "KEEP_AS_CANDIDATE_PRINCIPLE",
        ),
        (
            "ORG2742_1_generic_phase_volume",
            "generic Liouville/canonical phase-volume preservation",
            "J_q J_p=(T sqrt(S))*(1/(T sqrt(S)))=1",
            "preserves full canonical phase volume",
            "REJECTED_TOO_WEAK",
            "true for every p and therefore cannot select the GR lane",
            "REJECT_AS_DERIVATION",
        ),
        (
            "ORG2742_2_hamiltonian_null_route",
            "mass-shell/null Hamiltonian route",
            "E_local=E/T, p_local=p_r/sqrt(S), dr/dt=cT/sqrt(S)",
            "sharpens the observer-cell split",
            "REJECTED_TOO_WEAK",
            "Hamiltonian/Liouville and null propagation tolerate all p unless a separate cell law is added",
            "REJECT_AS_DERIVATION",
        ),
        (
            "ORG2742_3_nonpropagating_constraint",
            "hard nonpropagating reciprocal constraint",
            "S_lambda=int lambda_R ln(T^2 S) dV",
            "can enforce q=R_AB=0 without exterior gradient hair",
            "CLOSURE_ROUTE_NOT_PARENT_DERIVED",
            "lambda_R origin, positive q-norm, and matter-source variation are not supplied",
            "ALLOW_CLOSURE_ONLY",
        ),
        (
            "ORG2742_4_cell_current",
            "conserved radial observer-cell current",
            "partial_r(W partial_r R_AB)=0 => W partial_r R_AB=Q_R",
            "would make reciprocal strain a conserved-charge problem",
            "REJECTED_NO_CHARGE_OBSTRUCTION",
            "conservation gives constant Q_R, not Q_R=0; reciprocal hair remains possible",
            "REQUIRES_ZERO_CHARGE_THEOREM",
        ),
        (
            "ORG2742_5_motion_capacity_balance",
            "motion-capacity balance",
            "d ln T + d ln sqrt(S)=0 <=> d ln(T sqrt(S))=0",
            "most physical-looking story for why clock loss and routing gain compensate",
            "PROMISING_BUT_UNSIGNED",
            "needs a parent conservation law/no-charge theorem and coefficient extraction, not only interpretation",
            "KEEP_AS_ORIGIN_MOTIVATION",
        ),
        (
            "ORG2742_6_current_verdict",
            "accepted phase-volume q-sector origin",
            "none accepted",
            "prevents a hand-inserted auxiliary norm from being promoted",
            "NO_ACCEPTED_ORIGIN",
            "phase-volume motivates q=R_AB closure but does not derive parent action, E_q, J_q, or Q_R=0",
            "REJECT_PROMOTION",
        ),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "origin_id": origin_id,
                "candidate_origin": candidate,
                "mathematical_form": formula,
                "what_it_derives_or_motivates": derives,
                "current_status": status,
                "failure_or_limit": issue,
                "runner_result": runner,
                "accepted_parent_origin": False,
                "source_paths": "08-phase-volume-reciprocity-origin.md; 09-hamiltonian-radial-cell-derivation.md; 1554-Y5-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
            }
        )
        for origin_id, candidate, formula, derives, status, issue, runner in specs
    ]


def mapping_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "MAP2742_0_scalar_q",
            "q := R_AB = ln(T^2 S)",
            "scalar reciprocal closure variable",
            "CONDITIONAL_SYMBOLIC_MAP",
            "good scalar lane map, but not a full q^A family and not tracefree/PPN complete",
        ),
        (
            "MAP2742_1_radial_cell_equivalence",
            "T sqrt(S)=1 <=> q=0",
            "maps phase-cell rule into q-sector closure",
            "ALGEBRAIC_EQUIVALENCE_ONLY",
            "equivalence is exact, but the variational reason for imposing it is missing",
        ),
        (
            "MAP2742_2_multiplier_closure",
            "S_lambda=int lambda_q q dV",
            "forces q=0 without making q a propagating exterior field",
            "CLOSURE_ONLY",
            "multiplier origin and boundary differentiability are not parent-signed",
        ),
        (
            "MAP2742_3_auxiliary_norm_candidate",
            "S_aux=1/2 int mu_q^2 q^2 dV",
            "would supply algebraic E_q and avoid gradient hair",
            "NOT_PARENT_DERIVED",
            "mu_q^2/G_AB coefficient is still inserted unless phase-volume derives it",
        ),
        (
            "MAP2742_4_source_current",
            "J_q=delta S_matter/delta q",
            "needed for T_source_norm and q-sector source bounds",
            "MISSING_PARENT_COUPLING",
            "phase-volume alone does not define matter variation with respect to q",
        ),
        (
            "MAP2742_5_same_norm_Cqm",
            "C_qm=||Dq[v_m]||_E",
            "needed for N_pair and local residual bounds",
            "MISSING_PARENT_NORM",
            "no accepted E_q exists from phase-volume alone",
        ),
        (
            "MAP2742_6_local_scope",
            "R_AB=0 closure benchmark",
            "can be tested as assumed local closure only",
            "BENCHMARK_ONLY",
            "does not prove derived GR/Newton or PPN beta/conservation/matter universality",
        ),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "map_id": map_id,
                "qsector_object": obj,
                "role": role,
                "current_status": status,
                "blocker": blocker,
                "accepted_for_claim": False,
                "source_paths": "2741-Y5-R2FR-minimal-parent-qsector-action-ansatz-or-rejection-under-AX1090.md; 1554-Y5-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
            }
        )
        for map_id, obj, role, status, blocker in specs
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    specs = [
        ("OBS2742_0_generic_volume", "generic phase-volume preservation is too broad", "canonical phase-volume cancellation works for every p", "REJECTED"),
        ("OBS2742_1_separate_cell_theorem", "separate radial observer-cell theorem missing", "J_tr=1 is exactly the extra principle to prove", "OPEN"),
        ("OBS2742_2_lambda_origin", "lambda_R multiplier origin missing", "constraint is closure-only unless parent action supplies multiplier/constraint", "OPEN"),
        ("OBS2742_3_positive_norm", "positive q-norm E_q missing", "multiplier enforces q=0 but does not supply the same-norm source envelope", "OPEN"),
        ("OBS2742_4_matter_source", "matter q-source missing", "no parent S_matter[q] or J_q variation", "OPEN"),
        ("OBS2742_5_no_charge", "zero-charge theorem missing", "cell current gives Q_R constant, not Q_R=0", "OPEN"),
        ("OBS2742_6_tracefree_ppn", "scalar q=R_AB is not full local metric control", "gamma/beta/conservation/matter-universality still require separate gates", "OPEN"),
        ("OBS2742_7_no_GR_import", "proof must not import Schwarzschild AB=1", "using GR vacuum equations would make the reduction circular", "PASS_GUARD_NONCLAIM"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "obstruction_id": oid,
                "obstruction": obstruction,
                "reason": reason,
                "current_status": status,
                "source_paths": "08-phase-volume-reciprocity-origin.md; 09-hamiltonian-radial-cell-derivation.md; 1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md",
            }
        )
        for oid, obstruction, reason, status in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2742_0_radial_cell", "radial t-r cell selects p=1", "PASS_CONDITIONAL_NONCLAIM", "algebra works exactly, but origin is unsigned"),
        ("RUN2742_1_generic_phase_volume", "generic phase-volume derives p=1", "REFUSED_REJECTED_TOO_WEAK", "Liouville/canonical preservation is p-blind"),
        ("RUN2742_2_hamiltonian_null", "Hamiltonian or null motion derives p=1", "REFUSED_REJECTED_TOO_WEAK", "mass-shell structure sharpens variables but does not impose separate radial cell"),
        ("RUN2742_3_constraint", "nonpropagating constraint derives q=0", "PASS_CLOSURE_NONCLAIM", "valid closure form, not parent-derived"),
        ("RUN2742_4_auxiliary_norm", "phase-volume derives algebraic q-norm coefficient", "REFUSED_MISSING_COEFFICIENT_ORIGIN", "mu_q/G_AB not derived"),
        ("RUN2742_5_cell_current", "cell current kills reciprocal charge", "REFUSED_NO_CHARGE_OBSTRUCTION", "Q_R hair remains unless a zero-charge theorem exists"),
        ("RUN2742_6_source_norm", "phase-volume supplies J_q and C_qm", "REFUSED_MISSING_PARENT_COUPLING_AND_NORM", "source current and same-norm object absent"),
        ("RUN2742_7_score_status", "local GR/Newton score", "REFUSED_NOT_SCORE_READY", "no parent origin accepted and no local claim allowed"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "runner_id": rid,
                "check": check,
                "current_status": status,
                "reason": reason,
                "accepted_for_scoring": False,
            }
        )
        for rid, check, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2742_0_result",
            "Phase-volume origin is clarified but not closed.",
            "MOTIVATED_NOT_DERIVED",
            "radial cell rule selects p=1 exactly, but the separate-cell theorem is not parent-derived",
        ),
        (
            "DEC2742_1_keep_closure",
            "Keep q=R_AB closure explicit and quarantined.",
            "CLOSURE_ONLY",
            "it avoids exterior hair but lacks lambda/norm/source/no-charge origin",
        ),
        (
            "DEC2742_2_best_next",
            "Try the live gauge/Noether zero-charge route next.",
            "NEXT_2743_GAUGE_NOETHER_ZERO_CHARGE",
            "only a true first-class/no-charge theorem can promote Q_R=0 without inserting R_AB=0",
        ),
        (
            "DEC2742_3_no_claim",
            "Do not claim local GR/Newton reduction from phase-volume alone.",
            "NO_LOCAL_CLAIM",
            "PPN gamma/beta, conservation, and matter-universality remain downstream gates",
        ),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "rationale": rationale}) for did, decision, result, rationale in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2742_0_origin_audit", "phase-volume origin audit", True, "PASS_NONCLAIM", "origin routes and obstructions are explicit"),
        ("GATE2742_1_radial_cell", "radial cell selects p=1", True, "PASS_CONDITIONAL_NONCLAIM", "algebraic selection only"),
        ("GATE2742_2_parent_origin", "parent phase-volume theorem", False, "BLOCKED", "separate radial cell conservation not derived"),
        ("GATE2742_3_qnorm", "positive q-norm E_q", False, "BLOCKED", "constraint/phase-volume route does not supply E_q"),
        ("GATE2742_4_source", "J_q matter source", False, "BLOCKED", "matter q-variation missing"),
        ("GATE2742_5_zero_charge", "Q_R=0 no-charge theorem", False, "BLOCKED", "cell-current conservation permits nonzero Q_R"),
        ("GATE2742_6_local_tests", "local arena claims", False, "BLOCKED_NO_CLAIM", "no local scoring from phase-volume motivation"),
        ("GATE2742_7_GR_Newton", "derived GR/Newton limit", False, "BLOCKED_NO_CLAIM", "lambda/norm/source/tracefree gates remain open"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gid,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "claim_allowed": False,
                "reason": reason,
            }
        )
        for gid, claim, passed, status, reason in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2742_0_2743",
                "status": "selected_primary",
                "target_doc": "2743-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-or-closure-demotion-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_gauge_noether_zero_charge_qsector_origin_or_closure_demotion_under_AX1090_2743.py",
                "mission": "attempt the first-class/no-charge route for q=R_AB, using the existing 1555 contract as prior evidence, or demote the route to explicit closure benchmark",
                "acceptance": "produce parent symplectic/generator/boundary-charge/bracket/degree/matter-map evidence, or record exact missing clauses and select closure PPN benchmark next",
                "forbidden": "do not use coordinate gauge or Schwarzschild AB=1 as proof; do not delete boundary charge by hand; do not claim GR/Newton reduction",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2742_0_origin", "source_table": rel(OUTPUTS["origin"]), "copy_path": rel(BRANCH_OUTPUTS["origin"]), "purpose": "source-weight phase-volume qsector origin audit", "exists": BRANCH_OUTPUTS["origin"].exists()}),
        nonclaim({"copy_id": "BR2742_1_mapping", "source_table": rel(OUTPUTS["mapping"]), "copy_path": rel(BRANCH_OUTPUTS["mapping"]), "purpose": "local-bound qsector closure mapping quarantine", "exists": BRANCH_OUTPUTS["mapping"].exists()}),
        nonclaim({"copy_id": "BR2742_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for gauge/Noether zero-charge origin", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    origin: list[dict[str, Any]],
    mapping: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    origin_ok = any(row["origin_id"] == "ORG2742_0_radial_cell_rule" for row in origin) and any(row["origin_id"] == "ORG2742_6_current_verdict" and row["current_status"] == "NO_ACCEPTED_ORIGIN" for row in origin)
    mapping_ok = any(row["map_id"] == "MAP2742_0_scalar_q" for row in mapping) and any(row["map_id"] == "MAP2742_6_local_scope" and row["current_status"] == "BENCHMARK_ONLY" for row in mapping)
    obstruction_ok = any(row["obstruction_id"] == "OBS2742_5_no_charge" and row["current_status"] == "OPEN" for row in obstructions)
    runner_ok = any(row["runner_id"] == "RUN2742_0_radial_cell" and row["current_status"] == "PASS_CONDITIONAL_NONCLAIM" for row in runner) and any(row["runner_id"] == "RUN2742_7_score_status" and "REFUSED" in row["current_status"] for row in runner)
    gates_ok = any(row["claim_gate_id"] == "GATE2742_1_radial_cell" and row["gate_passed"] is True for row in gates) and all(row["claim_allowed"] is False for row in gates)
    no_claim_flags_ok = all(row.get("valid_for_claim") is False and row.get("claim_allowed") is False for block in [origin, mapping, obstructions, runner, gates] for row in block)
    next_ok = next_target[0]["selected"] is True and "2743" in next_target[0]["target_doc"] and "gauge-noether" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
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
        {"validation_id": "VAL2742_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2742_1_origin_audit", "passed": origin_ok, "detail": "phase-volume audit records radial-cell success but no accepted origin", "timestamp_utc": ts()},
        {"validation_id": "VAL2742_2_mapping", "passed": mapping_ok, "detail": "q=R_AB mapping is explicit and local use is benchmark-only", "timestamp_utc": ts()},
        {"validation_id": "VAL2742_3_obstructions", "passed": obstruction_ok, "detail": "no-charge and same-norm obstructions recorded", "timestamp_utc": ts()},
        {"validation_id": "VAL2742_4_runner_refuses_score", "passed": runner_ok, "detail": "runner accepts only conditional/closure nonclaim rows and refuses local scoring", "timestamp_utc": ts()},
        {"validation_id": "VAL2742_5_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "claim gates keep all prediction/claim flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2742_6_next_target", "passed": next_ok, "detail": "next target is live gauge/Noether zero-charge or closure demotion", "timestamp_utc": ts()},
        {"validation_id": "VAL2742_7_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2742_8_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2742_9_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2742_10_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2742_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2742 clarifies phase-volume as a strong p=1 motivation, rejects it as a parent q-sector derivation, and selects the no-charge route next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2742 - Y5 R2/f(R): Phase-Volume Nonpropagating q-sector Origin Or Rejection Under AX1090

Status: `Y5_R2FR_2742_phase_volume_origin_rejected_as_parent_derivation_radial_cell_retained_private`

## Private Verdict

2742 gives the phase-volume route its cleanest shot and keeps the useful part.

The useful part is exact:

`J_tr=T sqrt(S)=1 <=> T^2 S=1 <=> q=R_AB=ln(T^2 S)=0`.

For `S=(1-L)^(-p)`, that selects the GR scalar lane `p=1`. That is not nothing; it is one of the better-looking pieces of the local route.

But it is not yet a parent derivation. Generic Liouville/phase-volume preservation is too weak because the full canonical cell cancels for every `p`. The Hamiltonian/null scaffold sharpens the variables but also does not impose the separate radial cell. A constraint `int lambda_R q dV` works only as closure unless the parent action supplies `lambda_R`, a positive `E_q`, a matter source `J_q`, and a no-charge theorem `Q_R=0`.

So the move is: keep `q=R_AB=0` as an explicit benchmark closure, do not claim local GR/Newton, and take one more derivation shot through the gauge/Noether zero-charge contract.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Phase-Volume Origin Audit

{markdown_table(data["origin"], ["origin_id", "candidate_origin", "mathematical_form", "what_it_derives_or_motivates", "current_status", "failure_or_limit", "runner_result", "accepted_parent_origin", "valid_for_claim"])}

## q-sector Mapping

{markdown_table(data["mapping"], ["map_id", "qsector_object", "role", "current_status", "blocker", "accepted_for_claim", "valid_for_claim"])}

## Obstruction Ledger

{markdown_table(data["obstructions"], ["obstruction_id", "obstruction", "reason", "current_status", "valid_for_claim"])}

## Origin Runner

{markdown_table(data["runner"], ["runner_id", "check", "current_status", "reason", "accepted_for_scoring", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "rationale", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "claim_allowed", "valid_for_claim", "reason"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is a good honest checkpoint. The phase-volume idea has real bite because it lands exactly on `p=1`; the problem is that it has not yet earned the right to be a parent law. The next door is the zero-charge door: if the parent theory can make `Q_R=0` a theorem, the local branch starts looking serious. If not, we demote this route to a benchmark closure and test it without pretending it is derived.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    origin = origin_rows()
    mapping = mapping_rows()
    obstructions = obstruction_rows()
    runner = runner_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["origin"], origin)
    write_csv(OUTPUTS["mapping"], mapping)
    write_csv(OUTPUTS["obstructions"], obstructions)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["origin"], origin)
    write_csv(BRANCH_OUTPUTS["mapping"], mapping)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, origin, mapping, obstructions, runner, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "origin": origin,
        "mapping": mapping,
        "obstructions": obstructions,
        "runner": runner,
        "decisions": decisions,
        "gates": gates,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2742 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
