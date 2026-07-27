from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_STATIONARY_LOCAL_SOURCE_THEOREM_OR_DYNAMIC_EXCHANGE_CURRENT_2468"
CHECKPOINT_ID = "2468"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_STATIONARY_SOURCE_2468_SOURCE_REGISTER.csv",
    "theorem_hypotheses": OUT / "P8_Y5_STATIONARY_SOURCE_2468_THEOREM_HYPOTHESES.csv",
    "proof_steps": OUT / "P8_Y5_STATIONARY_SOURCE_2468_PROOF_STEPS.csv",
    "exterior_result": OUT / "P8_Y5_STATIONARY_SOURCE_2468_EXTERIOR_QLOC_RESULT.csv",
    "dynamic_exchange": OUT / "P8_Y5_STATIONARY_SOURCE_2468_DYNAMIC_EXCHANGE_LEDGER.csv",
    "scope_limits": OUT / "P8_Y5_STATIONARY_SOURCE_2468_SCOPE_LIMITS.csv",
    "promotion_verdict": OUT / "P8_Y5_STATIONARY_SOURCE_2468_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_STATIONARY_SOURCE_2468_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_STATIONARY_SOURCE_2468_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_STATIONARY_SOURCE_2468_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_STATIONARY_SOURCE_2468_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2468_VALIDATION.csv",
}

COPY_TARGETS = {
    "stationary_theorem_contract": LOCAL_BOUNDS / "Stationary_local_source_theorem_2468_NONCLAIM.csv",
    "dynamic_exchange_ledger": QUEUE / "JR2468_DYNAMIC_CLOCK_EXCHANGE_LEDGER_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2468_00_2467_doc",
        "source_path": ROOT / "2467-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
        "needles": ["DIV2467_1_full_divergence", "WTG2467_1_stationary_surface", "NEXT2467_0_selected", "VAL2467_OVERALL"],
        "role": "handoff selecting stationary theorem/dynamic exchange split",
    },
    {
        "source_id": "SRC2468_01_2467_divergence",
        "source_path": OUT / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv",
        "needles": ["DIV2467_4_Killing_clock", "BLOCKED_CURRENT_THEOREM"],
        "role": "derived divergence and stationary clock condition",
    },
    {
        "source_id": "SRC2468_02_2467_worldtube",
        "source_path": OUT / "P8_Y5_HILBERT_CURRENT_2467_WORLDTUBE_SURFACE_GATE.csv",
        "needles": ["WTG2467_1_stationary_surface", "WTG2467_4_external_vacuum", "PASS_GUARDRAIL"],
        "role": "surface independence and external vacuum handoff",
    },
    {
        "source_id": "SRC2468_03_2464_qloc",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2464_QLOC_DERIVATION_ATTEMPT.csv",
        "needles": ["QDER2464_2_project_local", "QDER2464_3_vacuum_zero", "NONCLAIM"],
        "role": "q_loc projection law from candidate action",
    },
    {
        "source_id": "SRC2468_04_2465_stress",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2465_STRESS_TENSOR_EXPOSURE.csv",
        "needles": ["STR2465_4_GR_limit_gate", "BLOCKED_CURRENT_CLAIM"],
        "role": "stress tensor blocker retained after q_loc theorem",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {"timestamp_utc": stamp(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append({**base_row(), "source_id": source["source_id"], "source_path": str(path), "exists": exists, "missing_needles": ";".join(missing), "source_pass": exists and not missing, "role": source["role"]})
    return rows


def theorem_hypotheses_rows() -> list[dict[str, Any]]:
    rows = [
        ("HYP2468_0_action_contract", "ACT2464_A q_loc current-law action is used as a formal contract", "needed for q_loc=P_loc J_M", "CONDITIONAL_INPUT"),
        ("HYP2468_1_hilbert_current", "J_M^nu=ell_J T_matter^{nu rho} tau_rho", "source current from Hilbert stress-energy", "CONDITIONAL_INPUT"),
        ("HYP2468_2_parent_scale_fixed", "ell_J is constant and fixed before local readout", "prevents fitted coupling drift", "ASSUMED_NOT_PROVED"),
        ("HYP2468_3_matter_shell", "nabla_mu T_matter^{mu nu}=0 in the stationary source region including distributional matching", "needed for current conservation", "ASSUMED_NOT_PROVED"),
        ("HYP2468_4_stationary_clock", "nabla_(mu tau_nu)=0 in the source plus exterior collar", "kills Hilbert-current clock strain", "ASSUMED_LOCAL_STATIONARY"),
        ("HYP2468_5_compact_support", "T_matter=0 outside worldtube W except bounded tails", "needed for exterior J_M=0", "ASSUMED_OR_BOUND_REQUIRED"),
        ("HYP2468_6_projector_owned", "P_loc is fixed or parent-owned in the collar", "prevents projection from hiding residuals", "ASSUMED_NOT_PROVED"),
        ("HYP2468_7_boundary_silent", "A/Gamma/Khat boundary flux is zero or bounded", "needed for clean local vacuum statement", "ASSUMED_NOT_PROVED"),
    ]
    return [{**base_row(), "hypothesis_id": i, "hypothesis": h, "why_needed": why, "status": st} for i, h, why, st in rows]


def proof_step_rows() -> list[dict[str, Any]]:
    rows = [
        ("PRF2468_0_divergence", "Using 2467, nabla.J = (nabla ell)Ttau + ell(nabla T)tau + ell T nabla tau.", "exact product rule", "PASS"),
        ("PRF2468_1_stationary_reduction", "Under fixed ell, matter shell, symmetric T and Killing tau, nabla.J=0.", "HYP2468_2-4", "PASS_CONDITIONAL"),
        ("PRF2468_2_surface_independence", "For any two hypersurfaces cutting W, Q[Sigma_2]-Q[Sigma_1]=int_V nabla.J + side_flux = 0.", "Gauss law plus no side leakage", "PASS_CONDITIONAL"),
        ("PRF2468_3_exterior_current_zero", "Outside W, T=0 so J_M=ell T tau=0.", "compact support/exterior vacuum", "PASS_CONDITIONAL"),
        ("PRF2468_4_projected_q_zero", "With q_loc^nu=P_loc^nu_rho J_M^rho, exterior J_M=0 implies q_loc^nu=0.", "ACT2464_A projection contract", "PASS_CONDITIONAL"),
        ("PRF2468_5_F1_zero", "The first local residual coefficient F1 vanishes in the stationary exterior because q_loc itself vanishes there.", "smooth local expansion", "PASS_CONDITIONAL"),
        ("PRF2468_6_not_full_GR", "Metric stress, ell_J origin and dynamic clock exchange are not proved.", "remaining gates", "NONCLAIM_LIMIT"),
    ]
    return [{**base_row(), "proof_id": i, "proof_step": step, "basis": basis, "status": st} for i, step, basis, st in rows]


def exterior_result_rows() -> list[dict[str, Any]]:
    rows = [
        ("EXT2468_0_stationary_q_zero", "q_loc^nu -> 0 in stationary compact-source exterior", "conditional theorem contract", "CONDITIONAL_THEOREM_CONTRACT"),
        ("EXT2468_1_F1_zero", "F1=0 in the same exterior collar", "follows because q_loc=0 before expansion", "CONDITIONAL_THEOREM_CONTRACT"),
        ("EXT2468_2_Delta_m_bound", "abs(Delta m/m) <= C[epsilon_J+epsilon_B+epsilon_tau]/M_source", "tails, boundary flux and non-Killing clock strain bound leakage", "BOUND_FORM_ONLY"),
        ("EXT2468_3_surface_mass", "M_source=int T^{mu nu}tau_nu dSigma_mu is surface-independent under theorem hypotheses", "Hilbert worldtube bridge", "CONDITIONAL_THEOREM_CONTRACT"),
        ("EXT2468_4_claim_limit", "No full Newton/PPN/local-GR pass", "T_GK stress, parent scale and dynamic clock exchange remain unresolved", "NONCLAIM"),
    ]
    return [{**base_row(), "result_id": i, "result": result, "basis": basis, "status": st} for i, result, basis, st in rows]


def dynamic_exchange_rows() -> list[dict[str, Any]]:
    rows = [
        ("DYN2468_0_clock_leak", "L_tau=ell_J T^{mu nu}nabla_(mu tau_{nu)}+(nabla_mu ell_J)T^{mu nu}tau_nu", "generic dynamic clock leakage", "FORM_DERIVED"),
        ("DYN2468_1_exchange_required", "Need I_tau+I_A=-L_tau for exact dynamic conservation", "A-equation integrability", "MISSING_PARENT_EXCHANGE"),
        ("DYN2468_2_tau_equation", "tau/coframe variation must produce the exchange law or a Killing/stationary constraint", "parent clock action", "MISSING_PARENT_CLOCK_ACTION"),
        ("DYN2468_3_cosmology_allowed", "Cosmological memory can keep L_tau nonzero on FLRW scales while local stationary collars close", "sector split", "POSSIBLE_SPLIT"),
        ("DYN2468_4_no_dynamic_claim", "Dynamic MTS/time-sector local-GR theorem is not proved", "exchange identity absent", "BLOCKED"),
    ]
    return [{**base_row(), "dynamic_id": i, "statement": s, "basis": b, "status": st} for i, s, b, st in rows]


def scope_limit_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCP2468_0_parent_scale", "ell_J still not parent-derived", "blocks numeric local predictions", "BLOCKED"),
        ("SCP2468_1_GK_stress", "q_loc=0 does not imply T_GK^{mu nu}=0", "blocks local metric/PPN pass", "BLOCKED"),
        ("SCP2468_2_projector", "P_loc still assumed fixed/parent-owned", "projection may hide residual components", "BLOCKED"),
        ("SCP2468_3_boundary", "boundary silence assumed", "must become condition or bound", "BLOCKED"),
        ("SCP2468_4_value", "stationary theorem is still valuable", "turns local q_loc silence from plateau axiom into conditional Euler/source theorem", "PROGRESS"),
    ]
    return [{**base_row(), "scope_id": i, "limit": limit, "effect": effect, "status": st} for i, limit, effect, st in rows]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2468_0_stationary_theorem", "Is a stationary local-source q_loc theorem available?", "YES_CONDITIONAL", "proof closes under explicit hypotheses", "promote to private conditional theorem contract"),
        ("PV2468_1_dynamic_theorem", "Is the dynamic clock/source theorem available?", "NO", "exchange current missing", "dynamic route blocked"),
        ("PV2468_2_Newton", "Is Newton/local GR derived?", "NO", "metric stress, scale and projector gates unresolved", "no public/local-GR claim"),
        ("PV2468_3_overall", "Overall 2468 verdict", "CONDITIONAL_LOCAL_QLOC_ZERO_DERIVED_STRESS_GATE_NEXT", "we have a real stationary q_loc zero route, but not full GR", "next target is GK stress silence/local metric equation"),
    ]
    return [{**base_row(), "verdict_id": i, "question": q, "result": r, "evidence": e, "effect": eff} for i, q, r, e, eff in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2468_0_stationary_q_zero", "Stationary compact-source exterior gives q_loc=0.", "PASS_AS_CONDITIONAL_THEOREM", "explicit hypotheses and proof steps written", True, False),
        ("GATE2468_1_F1_zero", "F1=0 in stationary exterior.", "PASS_AS_CONDITIONAL_THEOREM", "q_loc vanishes before expansion", True, False),
        ("GATE2468_2_dynamic_clock", "Generic dynamic clock closure.", "BLOCKED", "exchange current not parent-derived", False, False),
        ("GATE2468_3_local_GR", "Local GR/Newton/PPN branch passes.", "BLOCKED", "GK stress/local metric equation still open", False, False),
        ("GATE2468_4_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", True, False),
    ]
    return [{**base_row(), "gate_id": i, "claim": c, "gate_status": st, "reason": r, "gate_pass": gp, "claim_allowed": ca} for i, c, st, r, gp, ca in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2468_0_keep_stationary_theorem", "Keep the stationary q_loc theorem contract.", "it is a real conditional derivation, not a plateau axiom", "use as local-source branch scaffold"),
        ("DEC2468_1_do_not_overclaim", "Do not claim full local GR.", "q_loc silence is not metric stress silence", "claim gates stay blocked"),
        ("DEC2468_2_next_stress_gate", "Move next to GK stress/local metric equation.", "after q_loc zero, the next GR blocker is whether the extra sector gravitates locally", "2469 selected"),
    ]
    return [{**base_row(), "decision_id": i, "decision": d, "reason": r, "effect": e} for i, d, r, e in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2468_0_selected",
            "selection_status": "selected",
            "target_file": "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md",
            "target_script": "scripts/Y5_R2FR_GK_stress_silence_and_local_metric_equation_gate_2469.py",
            "task": "test whether the vertical-generator/Gamma-Khat sector has locally silent stress under the stationary q_loc theorem, or whether extra stress blocks GR/PPN even when q_loc=0",
            "acceptance_target": "stress tensor exposure, stealth/screening hypotheses, local metric equation gate, PPN residual source terms, and honest demotion if stress remains unsilenced",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["proof_steps"], COPY_TARGETS["stationary_theorem_contract"])
    shutil.copyfile(OUTPUTS["dynamic_exchange"], COPY_TARGETS["dynamic_exchange_ledger"])
    source_map = {"stationary_theorem_contract": OUTPUTS["proof_steps"], "dynamic_exchange_ledger": OUTPUTS["dynamic_exchange"]}
    return [{**base_row(), "copy_id": cid, "source_path": str(source_map[cid]), "target_path": str(target), "source_exists": source_map[cid].exists(), "target_exists": target.exists()} for cid, target in COPY_TARGETS.items()]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    add("VAL2468_00_sources_exist", all(row["source_pass"] is True or str(row["source_pass"]) == "True" for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2468_01_hypotheses_explicit", len(data["hypotheses"]) >= 8, "stationary theorem hypotheses explicit")
    add("VAL2468_02_q_zero_proof", any(row["proof_id"] == "PRF2468_4_projected_q_zero" and row["status"] == "PASS_CONDITIONAL" for row in data["proofs"]), "q_loc zero proof step present")
    add("VAL2468_03_F1_zero", any(row["result_id"] == "EXT2468_1_F1_zero" and row["status"] == "CONDITIONAL_THEOREM_CONTRACT" for row in data["exterior"]), "F1 zero conditional result present")
    add("VAL2468_04_dynamic_blocked", any(row["dynamic_id"] == "DYN2468_4_no_dynamic_claim" and row["status"] == "BLOCKED" for row in data["dynamic"]), "dynamic exchange route remains blocked")
    add("VAL2468_05_stress_next", any(row["scope_id"] == "SCP2468_1_GK_stress" and row["status"] == "BLOCKED" for row in data["scope"]), "GK stress blocker retained")
    add("VAL2468_06_overall_verdict", any(row["verdict_id"] == "PV2468_3_overall" and row["result"] == "CONDITIONAL_LOCAL_QLOC_ZERO_DERIVED_STRESS_GATE_NEXT" for row in data["verdicts"]), "overall verdict selects stress gate next")
    add("VAL2468_07_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR/Newton claim")
    add("VAL2468_08_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2468_0_selected", "2469 stress silence gate selected")
    add("VAL2468_09_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2468-Y5", "P8_Y5_STATIONARY_SOURCE_2468", "P8_Y5_BRR545_2468", "JR2468")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2468_10_no_formalization_artifacts", not formal_hits, "no 2468 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2468_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2468_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2468_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2468_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2468_OVERALL", all(row["status"] == "PASS" for row in rows), "2468 proves a conditional stationary q_loc zero/F1 zero theorem and keeps full local GR blocked")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2468 Y5 R2FR Stationary Local-source Theorem Or Dynamic Exchange Current",
        "",
        "**Status:** narrow theorem contract achieved, not full local GR. Under explicit stationary compact-source hypotheses, the Hilbert-current route gives surface-independent source charge, exterior `J_M=0`, exterior `q_loc=0`, and therefore `F1=0`. This is not a plateau axiom; it is conditional Euler/source machinery.",
        "",
        "**Important boundary:** the dynamic MTS/time-sector route remains blocked because a generic clock field leaks `nabla.J` unless a parent exchange current is derived. Also, `q_loc=0` does not yet prove `T_GK^{mu nu}=0`, so the next hard gate is the local metric/stress equation.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Theorem Hypotheses",
        markdown_table(data["hypotheses"], ["hypothesis_id", "hypothesis", "why_needed", "status"]),
        "",
        "## Proof Steps",
        markdown_table(data["proofs"], ["proof_id", "proof_step", "basis", "status"]),
        "",
        "## Exterior q_loc Result",
        markdown_table(data["exterior"], ["result_id", "result", "basis", "status"]),
        "",
        "## Dynamic Exchange Ledger",
        markdown_table(data["dynamic"], ["dynamic_id", "statement", "basis", "status"]),
        "",
        "## Scope Limits",
        markdown_table(data["scope"], ["scope_id", "limit", "effect", "status"]),
        "",
        "## Promotion Verdict",
        markdown_table(data["verdicts"], ["verdict_id", "question", "result", "evidence", "effect"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register(),
        "hypotheses": theorem_hypotheses_rows(),
        "proofs": proof_step_rows(),
        "exterior": exterior_result_rows(),
        "dynamic": dynamic_exchange_rows(),
        "scope": scope_limit_rows(),
        "verdicts": promotion_verdict_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["theorem_hypotheses"], data["hypotheses"])
    write_csv(OUTPUTS["proof_steps"], data["proofs"])
    write_csv(OUTPUTS["exterior_result"], data["exterior"])
    write_csv(OUTPUTS["dynamic_exchange"], data["dynamic"])
    write_csv(OUTPUTS["scope_limits"], data["scope"])
    write_csv(OUTPUTS["promotion_verdict"], data["verdicts"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
