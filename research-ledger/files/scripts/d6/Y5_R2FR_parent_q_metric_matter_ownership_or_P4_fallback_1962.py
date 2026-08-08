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

DOC_PATH = ROOT / "1962-Y5-R2FR-parent-q-metric-matter-ownership-or-P4-fallback.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1962_VALIDATION.csv"

SOURCES = {
    "1961_doc": {
        "path": ROOT / "1961-Y5-R2FR-parent-metric-only-variable-signature-or-P4-fill.md",
        "needles": ["MVS1961_0_target", "MVS1961_6_metric_only_verdict", "NEXT1961_0_primary"],
    },
    "1961_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1961_VALIDATION.csv",
        "needles": ["VAL1961_OVERALL", "PASS"],
    },
    "785_stack": {
        "path": ROOT / "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md",
        "needles": ["PMC785_5_matter_metric_only_coupling", "PMC785_6_parent_action_metric_ownership"],
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
        "needles": ["EHGate1339_3_Levi_Civita", "LOV1339_0_conditional_EH_selection", "R11V1339_1_torsion_nonmetricity"],
    },
    "956_left_hand_csv": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv",
        "needles": ["LHG956_0_EH_core_selection"],
    },
    "958_eh_selection_csv": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_958_EH_CORE_SELECTION_ATTEMPT.csv",
        "needles": ["EH958_5_verdict"],
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
                "purpose": "1962 parent q metric matter ownership or P4 fallback",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def ownership_theorem_rows() -> list[dict[str, object]]:
    entries = [
        (
            "OWN1962_0_target",
            "Close the local connection gate by parent-owning one observed quotient geometry and coupling all ordinary matter to it.",
            "Phi_parent -> q(Phi) -> e_obs -> g_obs=e_obs^T eta e_obs -> omega_LC[e_obs] -> S_matter",
            "TARGET_EXACT",
            "This is the cleanest route to EHGate1339_3_Levi_Civita.",
            "not a claim until the parent action/signature explicitly adopts the chain",
        ),
        (
            "OWN1962_1_q_map",
            "The quotient map is declared in the parent configuration data, not fitted after solutions are known.",
            "q: C_parent -> Q_obs; all local observable geometry factors through Q_obs",
            "UNSIGNED_PARENT_OBJECT",
            "944 has the contract, but not parent authority.",
            "sign q as an action-level map or constraint",
        ),
        (
            "OWN1962_2_owned_coframe_branch",
            "Use an observed coframe as the owned local geometry variable, or prove a rank-surjective multifield pregeometry map into it.",
            "e_obs in Vars_parent or e_obs=E[Phi^A] with rank(delta E/delta Phi^A)=16 modulo Lorentz/diffeomorphism gauge",
            "BEST_LEAP_CANDIDATE_NOT_SIGNED",
            "This avoids the scalar-only metric-rank trap flagged by 786.",
            "choose owned coframe branch or provide the multifield rank proof",
        ),
        (
            "OWN1962_3_connection_lock",
            "There is no independent observed connection in the local matter/source/readout branch.",
            "omega_obs := omega_LC[e_obs]; T^a=0; Q_rho_mu_nu=0 in the observed branch",
            "CONDITIONAL_ZERO_ROUTE",
            "If this is parent-signed, the P4 torsion/nonmetricity connection residual is zero by construction.",
            "must exclude Palatini, torsion, nonmetricity, and readout Gamma slots",
        ),
        (
            "OWN1962_4_matter_functor",
            "Every ordinary matter action uses only the observed coframe, induced spin connection, owned gauge fields, and constants.",
            "S_matter=sum_A S_A[Psi_A,e_obs,omega_LC[e_obs],A_owned,theta_A]",
            "UNSIGNED_MATTER_BLINDNESS",
            "This would make source current Hilbert/coframe current rather than a non-Hilbert representative current.",
            "must forbid direct psi/Gamma/q_loc/species-marker dependence",
        ),
        (
            "OWN1962_5_no_Gamma_variation",
            "Because Gamma/omega is not an independent observed variable, the observed hypermomentum current vanishes identically.",
            "Delta_lambda^{mu nu}:=-2 delta S_matter/delta Gamma^lambda_{mu nu}=0 when Gamma is absent from Vars_obs",
            "CONDITIONAL_THEOREM_CLEAN",
            "This is a real derivation path, not a plateau axiom.",
            "requires OWN1962_1..4 to be parent-signed",
        ),
        (
            "OWN1962_6_chain_rule_zero",
            "Vertical parent directions and representative changes cannot source local connection forces if all observed maps descend through q.",
            "v in ker(Dq) => L_v e_obs=L_v g_obs=L_v omega_LC=L_v S_matter=0",
            "CONDITIONAL_DESCENT_ZERO",
            "This is the quotient version of the local suppression mechanism.",
            "requires q descent and no hidden representative markers",
        ),
        (
            "OWN1962_7_verdict",
            "The proof is structurally clean but not closed in the current corpus.",
            "OWN1962_1..4 unsigned; OWN1962_5..6 conditional",
            "ZERO_PROOF_NOT_CLAIMED",
            "We have narrowed the missing piece to a parent signature choice: owned coframe branch or multifield rank proof.",
            "next step must either sign the parent ownership branch or instantiate P4 hypermomentum bounds",
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


def p4_fallback_rows() -> list[dict[str, object]]:
    entries = [
        (
            "P4H1962_0_trigger",
            "P4 hypermomentum fallback activates if OWN1962 parent ownership is not signed.",
            "independent_connection_hypermomentum",
            "ACTIVE_FALLBACK_NONCLAIM",
            "Delta_lambda^{mu nu} source/readout connection charge",
            "coefficient;units;matter_species;source_path;weak_field_projection;clock_light_orbit_map",
        ),
        (
            "P4H1962_1_zero_switch",
            "Hypermomentum zero is allowed only from variable absence, not from smallness intuition.",
            "Delta_lambda^{mu nu}=0",
            "REQUIRES_PARENT_VARIABLE_ABSENCE",
            "OWN1962_3 and OWN1962_4 must pass",
            "parent variable list plus no-Gamma matter/source/readout audit",
        ),
        (
            "P4H1962_2_bound_interface",
            "If a connection current survives, it must enter the local tests as a finite residual vector.",
            "epsilon_P4 <= K_hyper * ||Delta|| projected to R10/PPN/clock/orbit",
            "MISSING_NUMERIC_BOUND_INPUTS",
            "No local-GR pass can use this row yet.",
            "K_hyper;norm_definition;projection_matrix;arena_bounds;source_path",
        ),
        (
            "P4H1962_3_priority",
            "Do not spend more cycles on lower connection channels before this one is settled.",
            "hypermomentum precedes axial torsion and nonmetricity shear in the current gate order",
            "HIGHEST_PRIORITY_IF_FALLBACK",
            "This is the channel that directly decides LC/no-hypermomentum.",
            "resolve OWN1962 or source P4H1962 rows",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, channel, status, residual, required_inputs in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "channel": channel,
                "status": status,
                "residual": residual,
                "required_inputs": required_inputs,
            }
        )
        rows.append(row)
    return rows


def eh_impact_rows() -> list[dict[str, object]]:
    entries = [
        (
            "EHI1962_0_LC_gate",
            "EHGate1339_3_Levi_Civita",
            "would close if OWN1962_1..4 are parent-signed",
            "CONDITIONAL_PROGRESS",
            "connection/torsion/nonmetricity R11 family can be removed or demoted",
        ),
        (
            "EHI1962_1_metric_only_gate",
            "EHGate1339_1_metric_only_local_4D",
            "owned coframe branch supports metric-only local exterior if extra fields are silent or integrated out",
            "STILL_NEEDS_LOCAL_EXTERIOR_REDUCTION",
            "MTS sectors must not carry independent exterior stress/hair",
        ),
        (
            "EHI1962_2_second_order_gate",
            "EHGate1339_2_second_order",
            "not touched by the connection proof",
            "CENTRAL_BLOCKER_REMAINS",
            "R2/fR/Ricci2/Weyl2/nonlocal operators still require zero theorem or executable bounds",
        ),
        (
            "EHI1962_3_source_GM_gate",
            "EHGate1339_6_source_GM_transfer",
            "not touched by the connection proof",
            "SOURCE_CALIBRATION_REMAINS",
            "Hilbert/worldtube charge must equal measured orbital GM",
        ),
        (
            "EHI1962_4_best_route",
            "local GR bridge",
            "owned coframe + universal matter functor + second-order EH selection + GM transfer",
            "ROUTE_SHARPENED_NOT_CLAIMED",
            "this is the non-circling path from MTS to GR/Newton",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, condition, status, consequence in entries:
        row = base(row_id)
        row.update({"gate": gate, "condition": condition, "status": status, "consequence": consequence})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1962_0_target", "Parent q->coframe->matter ownership theorem is written.", "PASS_NONCLAIM", "contract theorem only"),
        ("CG1962_1_owned_coframe_route", "Owned observed coframe branch is the best-rank route.", "PASS_NONCLAIM", "branch not parent-signed"),
        ("CG1962_2_hypermomentum_zero", "Observed hypermomentum is zero.", "FAIL_BLOCKED", "requires no independent Gamma and matter blindness"),
        ("CG1962_3_Levi_Civita", "Observed connection is Levi-Civita.", "FAIL_BLOCKED", "ownership chain not parent-signed"),
        ("CG1962_4_EH_left_hand", "Local operator reduces to EH+Lambda.", "FAIL_BLOCKED", "second-order/no-extra-sector gates remain"),
        ("CG1962_5_Newton", "Newton/Poisson follows with measured GM.", "FAIL_BLOCKED", "EH and GM-transfer gates remain"),
        ("CG1962_6_P4_bound", "P4 fallback has numeric/source-backed residual bounds.", "FAIL_BLOCKED", "P4 hypermomentum inputs missing"),
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
            "DEC1962_0_verdict",
            "PARENT_OWNED_COFRAME_BRANCH_IS_BEST_ROUTE_NOT_YET_SIGNED",
            "The coframe branch is the least scrutinizable leap because it fixes the rank problem and makes LC/no-hypermomentum an actual variable-signature theorem.",
            "try to sign a minimal parent action with owned observed coframe and universal matter functor",
        ),
        (
            "DEC1962_1_if_rejected",
            "P4_HYPERMOMENTUM_BOUND_FALLBACK",
            "If MTS refuses owned coframe or rank-surjective pregeometry, then connection residuals are physical and must be bounded.",
            "build first numeric/source-backed P4 hypermomentum row",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1962_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md",
            "target_script": "scripts/Y5_R2FR_minimal_owned_coframe_parent_action_or_P4_hypermomentum_row_1963.py",
            "objective": "write the minimal parent action/signature that owns q,e_obs,matter functor and excludes independent Gamma, or stage the first P4 hypermomentum residual row",
            "acceptance_output": "parent action skeleton with explicit variables/couplings and no-Gamma theorem, or source-ready P4 hypermomentum bound schema",
            "nonclaim_rule": "no local-GR claim until EH second-order and GM-transfer gates also close",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1962_0_project_position")
    row.update(
        {
            "strongest_result": "The connection problem now has a concrete theorem route: owned observed coframe plus universal matter functor makes hypermomentum vanish by variable absence.",
            "what_improved": "The scalar-only metric emergence trap is bypassed by the owned-coframe/multifield-rank fork, which is a real leap toward local GR rather than another rephrasing.",
            "still_missing": "parent action signature, q ownership, matter blindness, no-Gamma readout, EH second-order selection, source GM transfer",
            "claim_status": "not a local-GR pass; best current route to the Levi-Civita gate",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1962_SOURCE_REGISTER.csv",
    "ownership": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1962_OWNERSHIP_THEOREM_ATTEMPT.csv",
    "p4": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1962_P4_HYPERMOMENTUM_FALLBACK.csv",
    "eh_impact": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1962_EH_GATE_IMPACT_LEDGER.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1962_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1962_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1962_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1962_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "OWNED_COFRAME_PARENT_ROUTE_1962_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1962_MINIMAL_OWNED_COFRAME_OR_P4_HYPERMOMENTUM_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1962_0_nonclaim_weight"),
            "artifact": "1962 parent q metric matter ownership theorem attempt",
            "weight": "BEST_THEOREM_ROUTE_NOT_EVIDENCE",
            "reason": "owned-coframe route can close LC/hypermomentum only after parent action adopts it",
        }
    ]
    queue = [
        {
            **base("AQ1962_0_minimal_parent_action"),
            "target": "minimal owned-coframe parent action",
            "needed_inputs": "Vars_parent, q map, e_obs ownership, omega_LC lock, matter functor, no-Gamma readout",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1962_1_p4_hypermomentum"),
            "target": "P4 hypermomentum fallback row",
            "needed_inputs": "Delta_lambda coefficient, units, source path, weak-field projection, R10/PPN/clock/orbit map",
            "priority": "FALLBACK_HIGHEST",
        },
    ]
    return {
        "source_register": source_register(),
        "ownership": ownership_theorem_rows(),
        "p4": p4_fallback_rows(),
        "eh_impact": eh_impact_rows(),
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
    patterns = ("1962-", "*_1962_*", "*Y5*1962*", "*VAL1962*", "*P8*1962*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1962_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    target_ok = any(row["row_id"] == "OWN1962_0_target" and row["status"] == "TARGET_EXACT" for row in tables["ownership"])
    rows.append(validation_row("VAL1962_01_target", "PASS" if target_ok else "FAIL", "ownership theorem target recorded"))

    coframe_ok = any(row["row_id"] == "OWN1962_2_owned_coframe_branch" and row["status"] == "BEST_LEAP_CANDIDATE_NOT_SIGNED" for row in tables["ownership"])
    rows.append(validation_row("VAL1962_02_owned_coframe", "PASS" if coframe_ok else "FAIL", "owned coframe branch selected as best route"))

    gamma_ok = any(row["row_id"] == "OWN1962_5_no_Gamma_variation" and row["status"] == "CONDITIONAL_THEOREM_CLEAN" for row in tables["ownership"])
    rows.append(validation_row("VAL1962_03_no_Gamma_theorem", "PASS" if gamma_ok else "FAIL", "no-Gamma hypermomentum theorem retained as conditional"))

    p4_ok = any(row["row_id"] == "P4H1962_0_trigger" and row["status"] == "ACTIVE_FALLBACK_NONCLAIM" for row in tables["p4"])
    rows.append(validation_row("VAL1962_04_p4_fallback", "PASS" if p4_ok else "FAIL", "P4 hypermomentum fallback remains active"))

    eh_ok = any(row["row_id"] == "EHI1962_0_LC_gate" and row["status"] == "CONDITIONAL_PROGRESS" for row in tables["eh_impact"])
    second_order_ok = any(row["row_id"] == "EHI1962_2_second_order_gate" and row["status"] == "CENTRAL_BLOCKER_REMAINS" for row in tables["eh_impact"])
    rows.append(validation_row("VAL1962_05_eh_gate_impact", "PASS" if eh_ok and second_order_ok else "FAIL", "LC gate impact recorded while EH blockers remain"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1962_2_hypermomentum_zero" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1962_06_claim_gates", "PASS" if gate_ok else "FAIL", "no claim gate promoted"))

    decision_ok = any(row["decision"] == "PARENT_OWNED_COFRAME_BRANCH_IS_BEST_ROUTE_NOT_YET_SIGNED" for row in tables["decision"])
    rows.append(validation_row("VAL1962_07_decision", "PASS" if decision_ok else "FAIL", "owned coframe branch selected"))

    next_ok = tables["next"][0]["target_doc"] == "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md"
    rows.append(validation_row("VAL1962_08_next_target", "PASS" if next_ok else "FAIL", "1963 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1962_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1962_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1962_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1962_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1962_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1962_OVERALL", overall, "1962 parent q metric matter ownership or P4 fallback"))
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
        ("Ownership Theorem Attempt", tables["ownership"]),
        ("P4 Hypermomentum Fallback", tables["p4"]),
        ("EH Gate Impact Ledger", tables["eh_impact"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1962 Y5 R2FR: Parent q-Metric-Matter Ownership Or P4 Fallback",
        "",
        "Private checkpoint. This is the non-circling bridge step: either make the local observed geometry a parent-owned coframe with universal matter coupling, or stop pretending the connection residual is zero and fill P4 hypermomentum bounds.",
        "",
        "Verdict: the owned-coframe route is the best current leap toward derived local GR. If the parent action signs q -> e_obs -> omega_LC[e_obs] -> S_matter and forbids independent Gamma/readout slots, observed hypermomentum vanishes by variable absence. The proof is clean but not claimed because the parent signature has not yet been written.",
        "",
        "Impact: this targets the Levi-Civita gate in the EH/Newton spine. It does not close the second-order EH operator gate or the measured-GM transfer gate.",
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
    print(f"VAL1962_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
