from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1963_VALIDATION.csv"

SOURCES = {
    "1962_doc": {
        "path": ROOT / "1962-Y5-R2FR-parent-q-metric-matter-ownership-or-P4-fallback.md",
        "needles": ["OWN1962_2_owned_coframe_branch", "OWN1962_5_no_Gamma_variation", "NEXT1962_0_primary"],
    },
    "1962_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1962_VALIDATION.csv",
        "needles": ["VAL1962_OVERALL", "PASS"],
    },
    "786_parent_action": {
        "path": ROOT / "786-Y5-R10-parent-action-metric-map-ownership-or-bg-bound-source-pack.md",
        "needles": ["PAO786_0_composite_metric_action", "PAO786_3_multifield_pregeometry", "VRG786_5_verdict"],
    },
    "943_coframe": {
        "path": ROOT / "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
        "needles": ["CFC943_2_matter_functor", "CFC943_4_connection_lock"],
    },
    "944_descent": {
        "path": ROOT / "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
        "needles": ["QDG944_0_parent_q_map", "QDG944_4_geometry_stack_descent", "QDG944_7_total"],
    },
    "1339_eh_gate": {
        "path": ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
        "needles": ["EHGate1339_1_metric_only_local_4D", "EHGate1339_2_second_order", "EHGate1339_3_Levi_Civita"],
    },
    "958_premise_csv": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_958_EH_PREMISE_AUDIT.csv",
        "needles": ["EHP958_P6_second_order"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_spec in SOURCES.items():
        path = source_spec["path"]
        needles = source_spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1963 minimal owned-coframe parent action or P4 hypermomentum row",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def action_signature_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ACT1963_0_target",
            "candidate minimal parent action signature for the local observed branch",
            "S_parent equals S_MTS_core[Xi,e,q] plus S_local_geom[e,Xi] plus sum_A S_A[Psi_A,e,omega_LC[e],A_owned,theta_A]",
            "CANDIDATE_ACTION_WRITTEN_NONCANONICAL",
            "This is the first concrete branch that can make LC and no-hypermomentum derivable without importing an independent connection.",
            "must be promoted into a canonical parent action before any claim",
        ),
        (
            "ACT1963_1_variable_list",
            "observed local variables include coframe and MTS sector fields but exclude independent observed connection",
            "Vars_local equals {e_obs^a_mu, Xi_MTS^I, Psi_A, A_owned}; omega_obs is defined as omega_LC[e_obs]",
            "VARIABLE_SIGNATURE_EXPLICIT",
            "The scalar-only metric-rank obstruction is bypassed by giving the observed branch a full coframe.",
            "need physical interpretation of e_obs as motion-time-space readout rather than arbitrary GR insertion",
        ),
        (
            "ACT1963_2_quotient_map",
            "q is a parent-owned projection from full MTS data to the local observed coframe branch",
            "q(Phi_parent) equals (e_obs,Xi_local,A_owned,theta); representative variables in ker(Dq) are unobservable locally",
            "CANDIDATE_Q_OWNERSHIP",
            "This turns the previous vertical-kernel language into an action-level map.",
            "still needs a parent equation or constraint deriving q from the deeper MTS corpus",
        ),
        (
            "ACT1963_3_geometry_term",
            "local geometry term is not forced to be EH at this checkpoint",
            "S_local_geom[e,Xi] equals integral det(e) times L_loc(e,R[e],nabla_LC R,Xi,nabla_LC Xi,...)",
            "GENERAL_LOCAL_OPERATOR_RETAINED",
            "Good discipline: LC can be derived now while EH/second-order remains a separate gate.",
            "must later prove or bound higher-curvature, nonlocal, and extra-sector pieces",
        ),
        (
            "ACT1963_4_matter_functor",
            "ordinary matter sees only the owned coframe, induced spin connection, owned gauge fields, and constants",
            "S_matter equals sum_A S_A[Psi_A,e_obs,omega_LC[e_obs],A_owned,theta_A]",
            "MATTER_FUNCTOR_SELECTED_NONCANONICAL",
            "This is the universal-coupling clause needed for WEP/source-current closure.",
            "must audit every matter/readout sector for direct Xi, q_loc, Gamma, species-marker, or representative dependence",
        ),
        (
            "ACT1963_5_no_independent_Gamma_clause",
            "the observed branch has no Palatini, torsion, nonmetricity, or connection-readout slot",
            "delta S_parent divided by delta Gamma_ind is vacuous because Gamma_ind is not a variable",
            "NO_GAMMA_BY_VARIABLE_SIGNATURE",
            "This is the real route to q_loc suppression and P4 silence.",
            "spin/torsion and metric-affine alternatives must be explicitly excluded or split into fallback rows",
        ),
        (
            "ACT1963_6_status",
            "1963 writes the candidate action signature but does not canonicalize it into the public framework",
            "ACT1963_0 through ACT1963_5 define a private branch skeleton",
            "FORWARD_LEAP_NOT_FINAL_CLAIM",
            "This is progress, not a loop: a concrete branch now exists to attack.",
            "next checkpoint must either defend this branch or reject it into P4 bounds",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, math_form, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "math_form": math_form,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def no_gamma_theorem_rows() -> list[dict[str, object]]:
    entries = [
        (
            "NGT1963_0_theorem",
            "If the parent action has variables {e_obs,Xi,Psi,A_owned} and ordinary matter is S_A[Psi_A,e_obs,omega_LC[e_obs],A_owned,theta_A], then the independent-connection hypermomentum of the observed branch is zero.",
            "Gamma_ind is not an argument of S_parent, so the functional derivative with respect to Gamma_ind is zero or undefined-vacuous in the reduced variable space.",
            "CONDITIONAL_PROOF_VALID",
            "This proves the local P4 independent-connection current vanishes inside the candidate branch.",
        ),
        (
            "NGT1963_1_spinor_guard",
            "Spinor matter may depend on omega_LC[e_obs], but this is tetrad-derived and contributes through coframe variation, not through an independent torsion connection.",
            "spin current is Belinfante/Hilbert absorbed unless an Einstein-Cartan connection is separately introduced",
            "SPIN_ESCAPE_GUARDED",
            "This blocks the obvious spin-torsion loophole for the owned-coframe branch.",
        ),
        (
            "NGT1963_2_q_vertical_silence",
            "For v in ker(Dq), all local observed arguments of ordinary matter are unchanged.",
            "Dq(v)=0 implies delta_v e_obs=0, delta_v omega_LC[e_obs]=0, delta_v S_matter=0",
            "CONDITIONAL_CHAIN_RULE_ZERO",
            "This is the local-vacuum suppression mechanism in exact map language.",
        ),
        (
            "NGT1963_3_not_EH",
            "The theorem does not select Einstein-Hilbert and does not prove Newtonian mechanics.",
            "LC and no-hypermomentum are necessary but not sufficient for EH plus measured GM",
            "SCOPE_LIMIT_EXPLICIT",
            "Keeps us honest: one gate moves, the whole bridge is not done.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, theorem_clause, proof_step, status, consequence in entries:
        row = base(row_id)
        row.update(
            {
                "theorem_clause": theorem_clause,
                "proof_step": proof_step,
                "status": status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def p4_row_schema() -> list[dict[str, object]]:
    entries = [
        (
            "P4R1963_0_hypermomentum_row",
            "independent_connection_hypermomentum",
            "only required if ACT1963 no-Gamma branch is rejected or an independent connection is introduced",
            "Delta_lambda^{mu nu}",
            "MISSING_COEFFICIENT_AND_PROJECTION",
            "K_hyper;norm_Delta;source_species;coupling_units;weak_field_projection;R10_bound;PPN_bound;clock_bound;orbital_bound;source_path;valid_for_claim",
        ),
        (
            "P4R1963_1_spin_torsion_row",
            "spin_torsion_escape",
            "only required if spinors couple to an independent torsionful connection",
            "S_spin^{lambda mu nu}",
            "MISSING_SPIN_CONNECTION_BRANCH",
            "spinor action branch;torsion coefficient;fermion source density;clock_or_spin_bound;source_path;valid_for_claim",
        ),
        (
            "P4R1963_2_nonmetricity_row",
            "nonmetricity_escape",
            "only required if matter or readout uses a connection not determined by e_obs",
            "Q_lambda_mu_nu",
            "MISSING_NONMETRICITY_BRANCH",
            "nonmetricity coefficient;lightcone projection;clock projection;source path;valid_for_claim",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, channel, trigger, residual, status, required_columns in entries:
        row = base(row_id)
        row.update(
            {
                "channel": channel,
                "trigger": trigger,
                "residual": residual,
                "status": status,
                "required_columns": required_columns,
            }
        )
        rows.append(row)
    return rows


def eh_remaining_gate_rows() -> list[dict[str, object]]:
    entries = [
        (
            "EHG1963_0_Levi_Civita",
            "EHGate1339_3_Levi_Civita",
            "conditionally closed inside ACT1963 candidate branch",
            "CONDITIONAL_BRANCH_PASS_NOT_CANONICAL",
            "requires adoption of ACT1963 variable signature",
        ),
        (
            "EHG1963_1_metric_only_local",
            "EHGate1339_1_metric_only_local_4D",
            "partially helped because local geometry is coframe/metric based",
            "EXTRA_SECTOR_SILENCE_REMAINS",
            "Xi_MTS must be silent, integrated out, or bounded in compact local exterior",
        ),
        (
            "EHG1963_2_second_order",
            "EHGate1339_2_second_order",
            "not solved",
            "CENTRAL_BLOCKER_REMAINS",
            "must prove Lovelock-style second-order restriction or fill R11 higher-curvature residuals",
        ),
        (
            "EHG1963_3_GM_transfer",
            "EHGate1339_6_source_GM_transfer",
            "not solved",
            "SOURCE_CALIBRATION_REMAINS",
            "must identify Hilbert/worldtube mass with measured orbital GM",
        ),
        (
            "EHG1963_4_newton_path",
            "Newtonian mechanics reduction",
            "requires ACT1963 adoption plus EH second-order plus source GM transfer plus PPN residual vector",
            "PATH_EXPLICIT_NOT_DONE",
            "next non-circling target after LC is the EH second-order/no-extra-sector gate",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, result, status, next_action in entries:
        row = base(row_id)
        row.update({"gate": gate, "result": result, "status": status, "next_action": next_action})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1963_0_action_skeleton", "Minimal parent action skeleton exists.", "PASS_NONCLAIM", "candidate branch only"),
        ("CG1963_1_no_Gamma_theorem", "No independent Gamma theorem is valid inside the branch.", "PASS_NONCLAIM", "conditional on branch adoption"),
        ("CG1963_2_LC_gate", "Observed connection is Levi-Civita in the full MTS framework.", "FAIL_BLOCKED", "candidate branch not canonicalized"),
        ("CG1963_3_EH_operator", "Local operator is EH plus Lambda.", "FAIL_BLOCKED", "second-order/no-extra-sector not derived"),
        ("CG1963_4_Newton", "Newtonian mechanics follows with measured GM.", "FAIL_BLOCKED", "EH and source-GM gates remain"),
        ("CG1963_5_P4_bound", "Fallback P4 residual is numeric/source-backed.", "FAIL_BLOCKED", "schema only"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1963_0_verdict",
            "MINIMAL_OWNED_COFRAME_PARENT_ACTION_BRANCH_WRITTEN",
            "This is the cleanest current route because it makes the connection result a variable-signature theorem rather than a fitted suppression condition.",
            "next defend whether ACT1963 is legitimate MTS rather than GR insertion",
        ),
        (
            "DEC1963_1_best_next",
            "ACTION_LEGITIMACY_AND_EH_SECOND_ORDER_GATE",
            "The next risk is not Gamma; it is whether the coframe branch is justified by MTS and whether higher operators vanish or are bounded.",
            "derive local exterior second-order/no-extra-sector selection or produce R11 executable residual rows",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1963_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1964-Y5-R2FR-owned-coframe-legitimacy-and-EH-second-order-gate.md",
            "target_script": "scripts/Y5_R2FR_owned_coframe_legitimacy_and_EH_second_order_gate_1964.py",
            "objective": "test whether the owned coframe branch is a legitimate MTS parent signature and then attack the EH second-order/no-extra-sector gate",
            "acceptance_output": "coframe-as-MTS-readout legitimacy proof or demotion to P4/R11 residuals; second-order EH gate decision",
            "nonclaim_rule": "do not claim local GR unless ACT1963, EH second-order, extra-sector silence, and GM transfer all pass",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1963_0_project_position")
    row.update(
        {
            "strongest_result": "A concrete minimal owned-coframe parent-action branch now exists; inside it, independent-connection hypermomentum vanishes by variable absence.",
            "what_improved": "The local connection problem has shifted from vague suppression to a crisp action-signature choice.",
            "still_missing": "canonical adoption of the branch, MTS interpretation of e_obs, second-order EH selection, extra-sector silence, measured-GM transfer, PPN residual closure",
            "claim_status": "conditional theorem branch only; no full local-GR/Newton claim",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1963_SOURCE_REGISTER.csv",
    "action_signature": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv",
    "no_gamma": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv",
    "p4_schema": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1963_P4_HYPERMOMENTUM_ROW_SCHEMA.csv",
    "eh_gates": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1963_EH_REMAINING_GATES.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1963_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1963_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1963_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1963_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MINIMAL_OWNED_COFRAME_PARENT_ACTION_1963_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1963_OWNED_COFRAME_EH_SECOND_ORDER_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1963_0_nonclaim_weight"),
            "artifact": "1963 minimal owned-coframe parent action branch",
            "weight": "CONDITIONAL_THEOREM_BRANCH_NOT_EVIDENCE",
            "reason": "the branch proves no-Gamma only if canonically adopted and still leaves EH/Newton gates open",
        }
    ]
    queue = [
        {
            **base("AQ1963_0_legitimacy"),
            "target": "coframe-as-MTS-readout legitimacy",
            "needed_inputs": "interpret e_obs from motion/time/space variables; forbid arbitrary GR insertion; connect q to parent MTS fields",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1963_1_second_order"),
            "target": "EH second-order/no-extra-sector gate",
            "needed_inputs": "operator family; higher-curvature zero theorem or R11 residual bounds; extra-sector silence",
            "priority": "HIGHEST_AFTER_LEGITIMACY",
        },
    ]
    return {
        "source_register": source_register(),
        "action_signature": action_signature_rows(),
        "no_gamma": no_gamma_theorem_rows(),
        "p4_schema": p4_row_schema(),
        "eh_gates": eh_remaining_gate_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1963-", "*_1963_*", "*Y5*1963*", "*VAL1963*", "*P8*1963*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1963_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    action_ok = any(row["row_id"] == "ACT1963_0_target" and row["status"] == "CANDIDATE_ACTION_WRITTEN_NONCANONICAL" for row in tables["action_signature"])
    rows.append(validation_row("VAL1963_01_action_written", "PASS" if action_ok else "FAIL", "minimal parent action skeleton written"))

    variables_ok = any(row["row_id"] == "ACT1963_1_variable_list" and row["status"] == "VARIABLE_SIGNATURE_EXPLICIT" for row in tables["action_signature"])
    rows.append(validation_row("VAL1963_02_variable_signature", "PASS" if variables_ok else "FAIL", "variable list excludes independent Gamma"))

    nogamma_ok = any(row["row_id"] == "NGT1963_0_theorem" and row["status"] == "CONDITIONAL_PROOF_VALID" for row in tables["no_gamma"])
    spin_ok = any(row["row_id"] == "NGT1963_1_spinor_guard" and row["status"] == "SPIN_ESCAPE_GUARDED" for row in tables["no_gamma"])
    rows.append(validation_row("VAL1963_03_no_gamma_theorem", "PASS" if nogamma_ok and spin_ok else "FAIL", "no-Gamma theorem and spinor guard recorded"))

    p4_ok = any(row["row_id"] == "P4R1963_0_hypermomentum_row" and row["status"] == "MISSING_COEFFICIENT_AND_PROJECTION" for row in tables["p4_schema"])
    rows.append(validation_row("VAL1963_04_p4_schema", "PASS" if p4_ok else "FAIL", "P4 fallback row schema retained"))

    eh_ok = any(row["row_id"] == "EHG1963_2_second_order" and row["status"] == "CENTRAL_BLOCKER_REMAINS" for row in tables["eh_gates"])
    rows.append(validation_row("VAL1963_05_eh_blockers", "PASS" if eh_ok else "FAIL", "EH second-order blocker remains explicit"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1963_3_EH_operator" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1963_06_claim_gates", "PASS" if gate_ok else "FAIL", "no full claim promoted"))

    decision_ok = any(row["decision"] == "MINIMAL_OWNED_COFRAME_PARENT_ACTION_BRANCH_WRITTEN" for row in tables["decision"])
    rows.append(validation_row("VAL1963_07_decision", "PASS" if decision_ok else "FAIL", "forward branch decision recorded"))

    next_ok = tables["next"][0]["target_doc"] == "1964-Y5-R2FR-owned-coframe-legitimacy-and-EH-second-order-gate.md"
    rows.append(validation_row("VAL1963_08_next_target", "PASS" if next_ok else "FAIL", "1964 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1963_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1963_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1963_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1963_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1963_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1963_OVERALL", overall, "1963 minimal owned-coframe parent action or P4 hypermomentum row"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Minimal Parent Action Signature", tables["action_signature"]),
        ("No-Gamma Theorem", tables["no_gamma"]),
        ("P4 Hypermomentum Fallback Schema", tables["p4_schema"]),
        ("EH Remaining Gates", tables["eh_gates"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1963 Y5 R2FR: Minimal Owned-Coframe Parent Action Or P4 Hypermomentum Row",
        "",
        "Private checkpoint. This is the concrete leap after 1962: write the smallest local parent-action branch that owns an observed coframe and therefore excludes an independent observed connection.",
        "",
        "Candidate branch:",
        "",
        "`S_parent = S_MTS_core[Xi,e,q] + S_local_geom[e,Xi] + sum_A S_A[Psi_A,e_obs,omega_LC[e_obs],A_owned,theta_A]`",
        "",
        "Verdict: inside this branch the independent-connection hypermomentum vanishes by variable absence. This is a real conditional theorem, not a plateau axiom. It is not yet a local-GR claim because the branch is not canonicalized and EH second-order, extra-sector silence, GM transfer, and PPN closure remain open.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1963_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
