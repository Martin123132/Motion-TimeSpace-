from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3673"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ACTION_HESSIAN_STF_OPERATOR_LOCATION_3673"
DOC = ROOT / "3673-Y5-R2FR-parent-action-Hessian-STF-operator-location.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        rows = load_csv(path)
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3672", RESIDUALS / "P8_Y5_R2FR_3672_NEXT_TARGET.csv", "parent-action", "3672 selected parent action operator location"),
        ("doc_3672", ROOT / "3672-Y5-R2FR-geometric-vs-stress-source-normalization-decision.md", "not interchangeable", "geometric/stress no-merge rule"),
        ("decision_3672", RESIDUALS / "P8_Y5_R2FR_3672_NORMALIZATION_DECISION_ROWS.csv", "DEC3672_4_next_route", "geometric parent-owner hunt"),
        ("doc_3669", ROOT / "3669-Y5-R2FR-kH-Hessian-STF-parent-owner-or-linear-gamma-bound-row.md", "nonminimal Hessian", "nonminimal Hessian counterterm already identified"),
        ("routing_1177", RESIDUALS / "P8_Y5_R10_1177_METRIC_CHANNEL_ROUTING_ATTEMPT.csv", "MCR1177_2_metric_channel_reference", "tracefree metric channel routing"),
        ("owner_1178", RESIDUALS / "P8_Y5_R10_1178_PARENT_METRIC_CHANNEL_OWNER_ATTEMPT.csv", "PMO1178_0_metric_map_needed", "parent metric map missing"),
        ("transfer_1179", RESIDUALS / "P8_Y5_R10_1179_RECIPROCAL_TRANSFER_DERIVATION_ATTEMPT.csv", "RTT1179_4_transfer_underdetermination", "tracefree transfer underdetermined"),
        ("identity_1180", RESIDUALS / "P8_Y5_R10_1180_PARENT_Q_GEOMETRIC_IDENTITY_ATTEMPT.csv", "QID1180_5_verdict", "Q-to-metric identity not derived"),
        ("qsplit_1185", RESIDUALS / "P8_Y5_R10_1185_QLOC_RESPONSE_SPLIT_ATTEMPT.csv", "QRS1185_1_response_operator", "response map required"),
        ("lhs_956", RESIDUALS / "P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv", "LHG956_0_EH_core_selection", "left-hand EH gate map"),
        ("contract_990", RESIDUALS / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_1_gravity_operator", "minimal parent action contract"),
        ("minimality_964", RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv", "MIN964_4_descent_signature", "minimal/no-extra-scalar theorem attempt"),
        ("vertex_1048", RESIDUALS / "P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv", "PVS1048_0_field_domain", "allowed operator list needed"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def fxr_owner_derivation_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "FXR3673_0_target_operator",
            "target Hessian-STF operator",
            "The branch to locate is the geometric equation term P_TF[D_bD_bY] = k_H_geo P_TF[D_bD_bX_b] plus floors.",
            "O_H=P_TF[nabla_i nabla_j X]",
            "TARGET_LOCKED",
        ),
        (
            "FXR3673_1_variation_identity",
            "nonminimal curvature variation",
            "For S_H=(M_*^2/2) int sqrt(-g) A_H F(X) R, metric variation contributes A_H[F G_mn +(g_mn Box - nabla_m nabla_n)F].",
            "delta(S_H)/delta g^{mn} includes -A_H P_TF[nabla_i nabla_j F] in the spatial tracefree equation",
            "DERIVED_GEOMETRIC_OWNER_CANDIDATE",
        ),
        (
            "FXR3673_2_linearized_coefficient",
            "linear local coefficient",
            "Around X=X0 with F=F0+F0_prime deltaX, and after normalizing the EH coefficient, the tracefree Hessian coefficient is fixed by the nonminimal curvature slot.",
            "k_H_geo = - A_H F0_prime/(1 + A_H F0) in normalized EH units, sign convention up to E_mn side",
            "DERIVED_IF_FXR_SLOT_ALLOWED",
        ),
        (
            "FXR3673_3_ban_gives_zero",
            "minimal parent ban",
            "If the parent action is EH-only in the local exterior and forbids F(X)R, R f(X), improvement-stress, and metric-readout Hessian terms, then this Hessian-STF geometric coefficient is zero at linear order.",
            "no F(X)R/improvement/readout Hessian slot => k_H_geo=0 for this route",
            "ZERO_ROUTE_IF_PARENT_SIGNATURE_BANS_SLOT",
        ),
        (
            "FXR3673_4_ordinary_stress_check",
            "ordinary stress does not naturally give Hessian-STF",
            "A minimally coupled local scalar-like stress from first derivatives gives gradient-square STF, P_TF[nabla_i X nabla_j X], not P_TF[nabla_i nabla_j X]. Hessian-STF in stress usually enters as an improvement term equivalent to nonminimal curvature coupling.",
            "T_ij^TF[minimal X] ~ P_TF[nabla_iX nabla_jX]; Hessian-STF requires improvement/nonminimal owner",
            "STRESS_ROUTE_DEMOTED_TO_IMPROVEMENT_OR_BOUND",
        ),
        (
            "FXR3673_5_current_corpus_status",
            "current evidence status",
            "The corpus has metric-channel routing contracts and operator-list guardrails, but no source-backed row that either allows F(X)R with coefficient A_H F0_prime or bans it by parent signature.",
            "operator location reduced to F(X)R allowed-or-banned gate",
            "SHARPENED_NOT_CLOSED",
        ),
    ]
    return [
        {
            **base(ts),
            "derivation_id": derivation_id,
            "clause": clause,
            "statement": statement,
            "formula": formula,
            "status": status,
            "claim_allowed": False,
        }
        for derivation_id, clause, statement, formula, status in specs
    ]


def evidence_classification_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "ECL3673_0_metric_channel",
            "1177/1178 metric-channel routing",
            "supports geometric route as least-scrutiny tensor channel",
            "tracefree shear belongs naturally in metric/EH channel if Dg_Q exists",
            "SUPPORTS_GEOMETRIC_BUT_NOT_PARENT_SIGNED",
        ),
        (
            "ECL3673_1_transfer_orientation",
            "1179 reciprocal transfer",
            "blocks coefficient promotion",
            "scalar reciprocity does not fix metric vs inverse/coframe orientation or normalization",
            "UNDERDETERMINED",
        ),
        (
            "ECL3673_2_Q_identity",
            "1180 Q geometric identity",
            "blocks direct Q-to-metric ownership",
            "most consistent current reading keeps Q as independent routing/load field or scalar Qcoh, not signed tracefree metric identity",
            "IDENTITY_NOT_DERIVED",
        ),
        (
            "ECL3673_3_q_response",
            "1185 q_loc response split",
            "blocks q_loc-based source placement",
            "q_loc has scalar/STF content only after a response operator R_q is sourced",
            "RESPONSE_OPERATOR_MISSING",
        ),
        (
            "ECL3673_4_FXR_owner",
            "nonminimal F(X)R construction",
            "constructive geometric owner",
            "F(X)R exactly generates Hessian-STF in the metric equation, so this is the sharp operator-location throat",
            "DERIVED_CANDIDATE_OWNER",
        ),
        (
            "ECL3673_5_stress_route",
            "stress RHS route",
            "fallback only",
            "ordinary stress gives gradient-square STF; Hessian-STF stress requires improvement/nonminimal structure and should not be the default",
            "DEMOTED_TO_BOUND_OR_IMPROVEMENT",
        ),
        (
            "ECL3673_6_parent_signature",
            "990/964/1048 parent signature",
            "decisive missing evidence",
            "allowed local operator list and no-extra-scalar/minimality theorem are contracts, not signed parent action",
            "PARENT_SIGNATURE_MISSING",
        ),
    ]
    return [
        {
            **base(ts),
            "evidence_id": evidence_id,
            "source_cluster": source_cluster,
            "effect_on_decision": effect,
            "finding": finding,
            "status": status,
            "claim_allowed": False,
        }
        for evidence_id, source_cluster, effect, finding, status in specs
    ]


def operator_location_decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "OLD3673_0_location_result",
            "operator location result",
            "Hessian-STF is naturally geometric if and only if the parent action allows a nonminimal curvature/improvement slot such as F(X)R; otherwise the minimal local branch zeros it.",
            "GEOMETRIC_BINARY_NOT_SOURCE_CLOSED",
        ),
        (
            "OLD3673_1_geometric_if_allowed",
            "allowed F(X)R branch",
            "If F(X)R is allowed, k_H_geo is not a mystery coupling: it is the normalized derivative of that curvature prefactor.",
            "ALLOW_BRANCH_BOUND_REQUIRED",
        ),
        (
            "OLD3673_2_zero_if_banned",
            "banned F(X)R branch",
            "If the parent signature bans F(X)R/improvement/readout Hessian slots and keeps local exterior EH-only, then k_H_geo=0 for this branch.",
            "BAN_BRANCH_CAN_PROVE_ZERO",
        ),
        (
            "OLD3673_3_stress_demoted",
            "stress branch demotion",
            "Do not use Sigma_H as the primary route for a Hessian-STF term unless an explicit improved stress tensor or matter-sector nonminimal coupling is sourced.",
            "STRESS_BRANCH_RETAINED_NONPRIMARY",
        ),
        (
            "OLD3673_4_no_claim",
            "claim status",
            "The current corpus has not signed either allowed coefficient or ban theorem, so local-GR/Cassini/PPN claims stay blocked.",
            "NONCLAIM_GATES_RETAINED",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "detail": detail,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, detail, status in specs
    ]


def fxr_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "GATEFXR3673_0_field_domain",
            "parent field/operator domain",
            "Declare whether X or Xhat can appear inside the gravitational curvature prefactor.",
            "MISSING_ALLOWED_OPERATOR_LIST",
            "without this, F(X)R is legal as a countermodel",
        ),
        (
            "GATEFXR3673_1_coefficient_owner",
            "nonminimal coefficient owner",
            "If allowed, source A_H, F0, and F0_prime from parent variables, not from Cassini/PPN fit.",
            "MISSING_IF_ALLOWED",
            "turns k_H_geo into a parent coefficient",
        ),
        (
            "GATEFXR3673_2_ban_theorem",
            "minimality/no-extra-scalar theorem",
            "If banned, prove no F(X)R, no R f(X), no improvement stress, no readout Hessian re-entry, and no integrated-out equivalent.",
            "MISSING_IF_BANNED",
            "turns k_H_geo=0 into a derivation",
        ),
        (
            "GATEFXR3673_3_Bianchi",
            "Bianchi/conservation closure",
            "Allowed F(X)R must include the X equation/current so total divergence closes; banned route must show no hidden stress is left behind.",
            "MISSING_CURRENT_CHAIN",
            "prevents fake geometry-stress movement",
        ),
        (
            "GATEFXR3673_4_observable_floors",
            "PPN/readout floors",
            "Even after the F(X)R decision, boundary kernels, q_loc response, k_G, C_other_gamma, and f_EM/Z_X remain separate gates.",
            "MISSING_FLOOR_BOUNDS",
            "prevents local-GR overclaim",
        ),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "required_showing": required_showing,
            "status": status,
            "why_it_matters": why_it_matters,
            "claim_allowed": False,
        }
        for gate_id, gate, required_showing, status, why_it_matters in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3673_0_FXR_derivation", "F(X)R Hessian-STF owner derivation", "PASS_CONDITIONAL_DERIVATION", "variation identity derives the candidate geometric owner"),
        ("CG3673_1_operator_location", "operator location source-backed", "BLOCKED_PARENT_SIGNATURE", "allowed/banned F(X)R slot not parent-signed"),
        ("CG3673_2_stress_route", "stress route primary", "DEMOTED_NONPRIMARY", "ordinary stress does not naturally give Hessian-STF"),
        ("CG3673_3_kH_zero", "k_H_geo zero theorem", "BLOCKED_UNTIL_BAN_THEOREM", "needs no-FXR/improvement/readout theorem"),
        ("CG3673_4_gamma_claim", "Cassini/local-GR claim", "BLOCKED_NONCLAIM", "coefficient/floors/source normalization remain unsigned"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "HESSIAN_STF_LOCATION_REDUCED_TO_FXR_ALLOW_OR_BAN_GATE",
            "summary": "3673 derives that the Hessian-STF branch is naturally owned by a nonminimal geometric/improvement slot such as F(X)R. This sharpens the coupling problem: either source and bound k_H_geo from that slot, or parent-ban the slot and derive k_H_geo=0.",
            "claim_ceiling": "no k_H zero, Cassini/gamma, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": "ordinary stress is demoted as the primary Hessian-STF owner; the next proof target is an allowed/forbidden F(X)R parent signature",
            "next_missing_piece": "parent action operator list deciding F(X)R/improvement/readout Hessian slots",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3673_0",
            "target_doc": "3674-Y5-R2FR-nonminimal-FXR-owner-or-ban-gate.md",
            "target_script": "scripts/Y5_R2FR_3674_nonminimal_FXR_owner_or_ban_gate.py",
            "objective": "decide the F(X)R gate: either derive/source the nonminimal curvature coefficient that owns k_H_geo, or prove the parent local exterior action bans F(X)R/improvement/readout Hessian slots and hence k_H_geo=0",
            "success_gate": "F(X)R is source-owned with coefficient rows or explicitly forbidden by a parent signature; otherwise k_H_geo remains a bounded nonclaim branch",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    evidence: list[dict[str, object]],
    decisions: list[dict[str, object]],
    fxr_gates: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3673 - Parent action Hessian-STF operator location",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "The key move: a linear Hessian-STF metric term is not generic stress fog. It is exactly the trace-free part generated by a nonminimal curvature/improvement slot.",
        "",
        "For a candidate parent term",
        "",
        "`S_H=(M_*^2/2) int sqrt(-g) A_H F(X) R`,",
        "",
        "metric variation contributes",
        "",
        "`A_H[F G_mn + (g_mn Box - nabla_m nabla_n)F]`.",
        "",
        "Therefore the spatial trace-free equation contains",
        "",
        "`-A_H P_TF[nabla_i nabla_j F]`.",
        "",
        "Linearized around `X0`, after EH normalization:",
        "",
        "`k_H_geo = - A_H F0_prime/(1 + A_H F0)` up to the chosen equation-side sign convention.",
        "",
        "So the branch is now binary: if `F(X)R` or an equivalent improvement/readout Hessian slot is allowed, `k_H_geo` must be sourced and bounded; if that slot is parent-banned, this route gives `k_H_geo=0`.",
        "",
        "Ordinary minimally-coupled stress is not the clean primary owner because it gives gradient-square STF, not Hessian-STF, unless an improvement/nonminimal term is introduced.",
        "",
        "## Derivation rows",
    ]
    for row in derivations:
        lines.append(f"- `{row['derivation_id']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Evidence classification"])
    for row in evidence:
        lines.append(f"- `{row['evidence_id']}`: {row['status']} - {row['finding']}")
    lines.extend(["", "## Operator-location decision"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['detail']}")
    lines.extend(["", "## F(X)R gate rows"])
    for row in fxr_gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    evidence: list[dict[str, object]],
    decisions: list[dict[str, object]],
    fxr_gates: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + derivations + evidence + decisions + fxr_gates + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3673*", "3673-Y5-R2FR-*", "P8_Y5*3673*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3673_0_sources_exist", all(row["exists"] for row in sources), "every cited source exists")
    add("VAL3673_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3673_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3673 outputs written")
    add("VAL3673_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3673_4_fxr_derivation", {"FXR3673_1_variation_identity", "FXR3673_2_linearized_coefficient", "FXR3673_3_ban_gives_zero"}.issubset({str(row["derivation_id"]) for row in derivations}), "F(X)R owner and ban derivation rows present")
    add("VAL3673_5_stress_demoted", any(row["derivation_id"] == "FXR3673_4_ordinary_stress_check" and row["status"] == "STRESS_ROUTE_DEMOTED_TO_IMPROVEMENT_OR_BOUND" for row in derivations), "ordinary stress route demoted")
    add("VAL3673_6_evidence_coverage", {"ECL3673_0_metric_channel", "ECL3673_1_transfer_orientation", "ECL3673_2_Q_identity", "ECL3673_4_FXR_owner"}.issubset({str(row["evidence_id"]) for row in evidence}), "metric routing and F(X)R evidence covered")
    add("VAL3673_7_location_binary", any(row["decision_id"] == "OLD3673_0_location_result" and row["status"] == "GEOMETRIC_BINARY_NOT_SOURCE_CLOSED" for row in decisions), "operator location reduced to allow-or-ban binary")
    add("VAL3673_8_fxr_gates", {"GATEFXR3673_0_field_domain", "GATEFXR3673_1_coefficient_owner", "GATEFXR3673_2_ban_theorem", "GATEFXR3673_3_Bianchi"}.issubset({str(row["gate_id"]) for row in fxr_gates}), "F(X)R gate requirements present")
    add("VAL3673_9_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3673_10_claim_gates", any(row["claim_gate_id"] == "CG3673_4_gamma_claim" and row["status"] == "BLOCKED_NONCLAIM" for row in gates), "gamma/local-GR claim remains blocked")
    add("VAL3673_11_doc_written", "F(X)R" in doc_text and "k_H_geo" in doc_text and "binary" in doc_text, "doc records F(X)R binary")
    add("VAL3673_12_no_formalization_leak", not leaks, "no 3673 checkpoint files in formalization-workbench")
    add("VAL3673_13_next_target", next_target[0]["target_doc"].startswith("3674-") and "FXR" in next_target[0]["target_doc"], "3674 F(X)R target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    derivations = fxr_owner_derivation_rows(ts)
    evidence = evidence_classification_rows(ts)
    decisions = operator_location_decision_rows(ts)
    fxr_gates = fxr_gate_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3673_SOURCE_REGISTER.csv",
        "derivations": RESIDUALS / "P8_Y5_R2FR_3673_FXR_OWNER_DERIVATION_ROWS.csv",
        "evidence": RESIDUALS / "P8_Y5_R2FR_3673_OPERATOR_LOCATION_EVIDENCE_CLASSIFICATION.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3673_OPERATOR_LOCATION_DECISION_ROWS.csv",
        "fxr_gates": RESIDUALS / "P8_Y5_R2FR_3673_FXR_ALLOW_OR_BAN_GATE_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3673_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3673_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3673_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3673_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["derivations"], derivations)
    write_csv(outputs["evidence"], evidence)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["fxr_gates"], fxr_gates)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, derivations, evidence, decisions, fxr_gates, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, derivations, evidence, decisions, fxr_gates, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3673 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3673 checkpoint with {len(validation)} validation checks; Hessian-STF reduced to F(X)R allow-or-ban gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
