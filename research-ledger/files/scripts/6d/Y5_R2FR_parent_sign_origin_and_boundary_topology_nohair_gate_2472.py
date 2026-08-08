from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_SIGN_ORIGIN_AND_BOUNDARY_TOPOLOGY_NOHAIR_GATE_2472"
CHECKPOINT_ID = "2472"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2472-Y5-R2FR-parent-sign-origin-and-boundary-topology-nohair-gate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_GK_PARENT_SIGN_2472_SOURCE_REGISTER.csv",
    "parent_sign_audit": OUT / "P8_Y5_GK_PARENT_SIGN_2472_PARENT_SIGN_AUDIT.csv",
    "boundary_ledger": OUT / "P8_Y5_GK_PARENT_SIGN_2472_BOUNDARY_LEDGER.csv",
    "topology_audit": OUT / "P8_Y5_GK_PARENT_SIGN_2472_TOPOLOGY_HAIR_AUDIT.csv",
    "nohair_verdict": OUT / "P8_Y5_GK_PARENT_SIGN_2472_NOHAIR_ELIGIBILITY_VERDICT.csv",
    "demotion_route": OUT / "P8_Y5_GK_PARENT_SIGN_2472_STRESS_BOUND_DEMOTION_ROUTE.csv",
    "claim_gates": OUT / "P8_Y5_GK_PARENT_SIGN_2472_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_GK_PARENT_SIGN_2472_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_GK_PARENT_SIGN_2472_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_GK_PARENT_SIGN_2472_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2472_VALIDATION.csv",
}

COPY_TARGETS = {
    "parent_sign_blocker": QUEUE / "JR2472_PARENT_SIGN_BLOCKER_NONCLAIM.csv",
    "boundary_topology_blocker": LOCAL_BOUNDS / "Boundary_topology_nohair_blocker_2472_NONCLAIM.csv",
    "stress_bound_route": LOCAL_BOUNDS / "Stress_bound_local_metric_route_2472_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2472_00_2471_doc",
        "source_path": ROOT / "2471-Y5-R2FR-explicit-GK-quadratic-operator-sign-audit.md",
        "needles": ["COER2471_1_cross_bound", "NHG2471_5_eligibility", "NEXT2471_0_selected", "VAL2471_OVERALL"],
        "role": "handoff selecting parent-sign and boundary/topology gate",
    },
    {
        "source_id": "SRC2472_01_2471_coercivity",
        "source_path": OUT / "P8_Y5_GK_OPERATOR_2471_COERCIVITY_AUDIT.csv",
        "needles": ["COER2471_5_current_status", "NOT_PROMOTED"],
        "role": "coercivity remains unsigned",
    },
    {
        "source_id": "SRC2472_02_2471_nohair",
        "source_path": OUT / "P8_Y5_GK_OPERATOR_2471_NOHAIR_ELIGIBILITY.csv",
        "needles": ["NHG2471_2_parent_signed", "FAIL_CURRENT_CLAIM", "PLAUSIBLE_NOT_PROVED"],
        "role": "no-hair eligibility nonpromotion",
    },
    {
        "source_id": "SRC2472_03_2471_bound",
        "source_path": OUT / "P8_Y5_GK_OPERATOR_2471_STRESS_BOUND_BRANCH.csv",
        "needles": ["SBB2471_2_metric_bound", "MISSING_NUMERIC_INPUTS", "NONCLAIM"],
        "role": "stress-bound fallback route",
    },
    {
        "source_id": "SRC2472_04_2470_failures",
        "source_path": OUT / "P8_Y5_GK_NOHAIR_2470_FAILURE_MODES.csv",
        "needles": ["FAIL2470_3_boundary_hair", "FAIL2470_4_topological_hair"],
        "role": "boundary/topology failure modes",
    },
    {
        "source_id": "SRC2472_05_2468_scope",
        "source_path": OUT / "P8_Y5_STATIONARY_SOURCE_2468_SCOPE_LIMITS.csv",
        "needles": ["SCP2468_1_GK_stress", "SCP2468_3_boundary", "BLOCKED"],
        "role": "local-GR stress and boundary blockers",
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


def parent_sign_rows() -> list[dict[str, Any]]:
    rows = [
        ("PS2472_0_current_source", "Current corpus contains no single parent action deriving Z_A,Z_G,m_A2,m_G2,c_AG signs.", "2471 sign audit", "MISSING_PARENT_SIGN_SOURCE", "blocks no-hair promotion"),
        ("PS2472_1_stability_principle", "Adopting positive energy as a new principle would sign the operator but would be new parent material.", "theory construction option", "NEW_MATERIAL_NOT_CURRENT_EVIDENCE", "allowed only as future construction"),
        ("PS2472_2_GR_analogy", "GR positive-energy intuition cannot sign GK coefficients by itself.", "external analogy is not derivation", "REJECT_AS_EVIDENCE", "prevents borrowing legitimacy"),
        ("PS2472_3_empirical_fit", "Choosing signs from local PPN/R10 success is forbidden.", "anti-circularity", "REJECTED", "no fitted sign route"),
        ("PS2472_4_cosmology_fit", "Choosing signs from cosmology/galaxy success is also insufficient for local no-hair.", "sector mismatch", "REJECT_AS_LOCAL_PROOF", "empirical hints cannot replace parent sign"),
        ("PS2472_5_minimum_reopen", "Reopen requires explicit parent L_K/L_Gamma or a variational stability theorem fixing coefficient signs before local tests.", "reopen condition", "REQUIRED_TO_REOPEN", "exact missing material named"),
    ]
    return [{**base_row(), "sign_id": i, "audit_item": item, "basis": basis, "status": status, "effect": effect} for i, item, basis, status, effect in rows]


def boundary_rows() -> list[dict[str, Any]]:
    rows = [
        ("BD2472_0_asymptotic_vacuum", "u approaches zero at local exterior boundary/infinity", "would kill many finite-energy modes", "ASSUMED_NOT_DERIVED"),
        ("BD2472_1_no_flux", "n_i K_hat^{ij}=0 and A/Gamma boundary flux vanish", "needed for energy identity boundary term", "ASSUMED_NOT_DERIVED"),
        ("BD2472_2_worldtube_matching", "source boundary has distributional matching conditions compatible with J_M and GK flux", "prevents hidden source hair at W boundary", "MISSING_JUMP_CONDITION"),
        ("BD2472_3_lab_cavity", "finite lab/solar-system domain may have environmental boundary data", "could source homogeneous GK hair", "BOUND_REQUIRED"),
        ("BD2472_4_reference_warning", "boundary condition cannot be chosen to cancel PPN residual after readout", "anti-tuning", "PASS_GUARDRAIL"),
        ("BD2472_5_current_status", "no parent boundary theorem currently closes all GK exterior fluxes", "source audit", "BLOCKED"),
    ]
    return [{**base_row(), "boundary_id": i, "condition": condition, "why_needed": why, "status": status} for i, condition, why, status in rows]


def topology_rows() -> list[dict[str, Any]]:
    rows = [
        ("TOP2472_0_simply_connected", "If exterior Omega is simply connected with trivial relevant cohomology, harmonic GK hair is absent.", "standard no-hair simplification", "CONDITIONAL_ROUTE"),
        ("TOP2472_1_harmonic_A", "Nontrivial harmonic one-form/vector modes can carry stress with q_loc=0.", "topological hair failure mode", "BLOCKS_GENERAL_THEOREM"),
        ("TOP2472_2_gamma_zero_mode", "constant gamma zero-mode requires vacuum normalization or boundary fixing.", "scalar/compression hair", "BLOCKS_GENERAL_THEOREM"),
        ("TOP2472_3_topological_charge", "unsourced topological GK charge must be zero, quantized and fixed, or bounded.", "prevents hidden local stress", "MISSING_TOPOLOGY_LEDGER"),
        ("TOP2472_4_local_patch", "For ordinary local PPN patch, trivial topology is plausible but must be stated as a hypothesis.", "narrow local theorem route", "ASSUMPTION_ALLOWED"),
        ("TOP2472_5_global_theory", "global/cosmological sectors may allow topology while local exterior branch remains trivial.", "sector split", "POSSIBLE_SPLIT_NOT_PROOF"),
    ]
    return [{**base_row(), "topology_id": i, "topology_clause": clause, "basis": basis, "status": status} for i, clause, basis, status in rows]


def nohair_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("NHV2472_0_narrow_patch", "Can a narrow stationary simply-connected patch no-hair contract be stated?", "YES_CONDITIONAL", "assume parent signs, no-flux/asymptotic boundary, trivial topology", "usable as private contract only"),
        ("NHV2472_1_current_parent_sign", "Are parent signs available in current corpus?", "NO", "PS2472 audit found no source", "blocks promotion"),
        ("NHV2472_2_boundary_topology", "Are boundary/topology conditions proved?", "NO", "boundary flux and harmonic/topological modes remain assumptions", "blocks promotion"),
        ("NHV2472_3_current_nohair", "Does current MTS prove no-hair?", "NO", "parent signs and boundary/topology closure missing", "demote current local metric branch"),
        ("NHV2472_4_branch_status", "What is the honest current branch?", "STRESS_BOUND_ONLY_FOR_CLAIM_PURPOSES", "conditional theorem remains a future parent-action route, not current evidence", "select stress-bound runner next"),
    ]
    return [{**base_row(), "verdict_id": i, "question": q, "result": result, "evidence": evidence, "effect": effect} for i, q, result, evidence, effect in rows]


def demotion_route_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEM2472_0_demote_current_metric_branch", "Current local metric branch is demoted to stress-bound only until parent signs and no-hair boundaries are supplied.", "no-hair not proved", "ACTIVE_FALLBACK"),
        ("DEM2472_1_bound_quantity", "Use delta_PPN <= C_metric norm(T_GK+T_tau/P+boundary) with defect terms from 2471.", "existing bound form", "BOUND_ROUTE"),
        ("DEM2472_2_needed_coefficients", "Need C_metric, C_T, C_B, C_S, negative_mode_defect, topology_hair_amplitude and arena projection coefficients.", "to compare to R10/PPN/clocks/orbital tests", "MISSING_NUMERIC_INPUTS"),
        ("DEM2472_3_claim_ceiling", "Stress-bound branch can show compatibility with local tests, not derivation of GR, unless bounds are derived and vanish in the GR limit.", "claim discipline", "NONCLAIM"),
        ("DEM2472_4_reopen_path", "If parent signs and boundary/topology are later supplied, no-hair theorem can be reopened.", "not dead, just unproved", "REOPENABLE"),
    ]
    return [{**base_row(), "demotion_id": i, "route_clause": clause, "basis": basis, "status": status} for i, clause, basis, status in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2472_0_parent_sign", "GK signs are parent-derived.", "BLOCKED", "no source in current corpus", False, False),
        ("GATE2472_1_boundary_topology", "boundary/topology no-hair is proved.", "BLOCKED", "conditions remain assumptions", False, False),
        ("GATE2472_2_narrow_contract", "narrow simply-connected stationary patch contract exists.", "PASS_AS_CONDITIONAL_CONTRACT", "hypotheses can be stated clearly", True, False),
        ("GATE2472_3_current_nohair", "current corpus proves no-hair.", "BLOCKED", "parent sign and topology gates fail", False, False),
        ("GATE2472_4_stress_bound_fallback", "current local metric branch has a stress-bound fallback.", "PASS_AS_FALLBACK", "demotion route written", True, False),
        ("GATE2472_5_local_GR_PPN", "local GR/PPN branch passes.", "BLOCKED", "only stress-bound nonclaim branch remains", False, False),
        ("GATE2472_6_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", True, False),
    ]
    return [{**base_row(), "gate_id": i, "claim": claim, "gate_status": status, "reason": reason, "gate_pass": gate_pass, "claim_allowed": claim_allowed} for i, claim, status, reason, gate_pass, claim_allowed in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2472_0_demote_for_now", "Demote current local metric/no-hair branch to stress-bound only.", "parent signs and boundary/topology closure are not current evidence", "prevents overclaim"),
        ("DEC2472_1_keep_future_route", "Keep no-hair as a reopenable future parent-action route.", "the conditional theorem shape is mathematically useful", "not discarded"),
        ("DEC2472_2_next_runner", "Build stress-bound local arena projection next.", "the active current branch needs empirical/local compatibility scaffolding", "2473 selected"),
    ]
    return [{**base_row(), "decision_id": i, "decision": decision, "reason": reason, "effect": effect} for i, decision, reason, effect in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2472_0_selected",
            "selection_status": "selected",
            "target_file": "2473-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md",
            "target_script": "scripts/Y5_R2FR_GK_stress_bound_local_arena_projection_runner_2473.py",
            "task": "turn the demoted stress-bound branch into a local arena projection scaffold for R10, PPN, clocks and orbital tests, without claiming a local-GR pass",
            "acceptance_target": "residual parameters, arena projection rows, missing coefficient ledger, nonclaim runner schema, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["parent_sign_audit"], COPY_TARGETS["parent_sign_blocker"])
    shutil.copyfile(OUTPUTS["boundary_ledger"], COPY_TARGETS["boundary_topology_blocker"])
    shutil.copyfile(OUTPUTS["demotion_route"], COPY_TARGETS["stress_bound_route"])
    source_map = {
        "parent_sign_blocker": OUTPUTS["parent_sign_audit"],
        "boundary_topology_blocker": OUTPUTS["boundary_ledger"],
        "stress_bound_route": OUTPUTS["demotion_route"],
    }
    return [{**base_row(), "copy_id": cid, "source_path": str(source_map[cid]), "target_path": str(target), "source_exists": source_map[cid].exists(), "target_exists": target.exists()} for cid, target in COPY_TARGETS.items()]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    add("VAL2472_00_sources_exist", all(row["source_pass"] is True or str(row["source_pass"]) == "True" for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2472_01_parent_sign_blocked", any(row["sign_id"] == "PS2472_0_current_source" and row["status"] == "MISSING_PARENT_SIGN_SOURCE" for row in data["signs"]), "parent sign source missing")
    add("VAL2472_02_boundary_blocked", any(row["boundary_id"] == "BD2472_5_current_status" and row["status"] == "BLOCKED" for row in data["boundary"]), "boundary closure blocked")
    add("VAL2472_03_topology_audit", any(row["topology_id"] == "TOP2472_1_harmonic_A" and row["status"] == "BLOCKS_GENERAL_THEOREM" for row in data["topology"]), "topological hair audit written")
    add("VAL2472_04_nohair_demoted", any(row["verdict_id"] == "NHV2472_4_branch_status" and row["result"] == "STRESS_BOUND_ONLY_FOR_CLAIM_PURPOSES" for row in data["verdicts"]), "current branch demoted to stress-bound for claims")
    add("VAL2472_05_demotion_route", any(row["demotion_id"] == "DEM2472_0_demote_current_metric_branch" and row["status"] == "ACTIVE_FALLBACK" for row in data["demotion"]), "stress-bound demotion route active")
    add("VAL2472_06_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR/PPN claim")
    add("VAL2472_07_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2472_0_selected", "2473 stress-bound projection runner selected")
    add("VAL2472_08_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2472-Y5", "P8_Y5_GK_PARENT_SIGN_2472", "P8_Y5_BRR545_2472", "JR2472")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2472_09_no_formalization_artifacts", not formal_hits, "no 2472 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2472_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2472_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2472_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2472_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2472_OVERALL", all(row["status"] == "PASS" for row in rows), "2472 blocks parent-sign/no-hair promotion and demotes current local metric route to stress-bound fallback")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2472 Y5 R2FR Parent Sign Origin And Boundary Topology No-hair Gate",
        "",
        "**Status:** parent-sign/no-hair promotion rejected for the current corpus. The narrow no-hair route remains mathematically useful, but the required coefficient signs, boundary conditions and topology exclusions are not parent-derived. Therefore the current local metric branch is demoted to stress-bound only for claim purposes.",
        "",
        "**Meaning:** this is not a dead end; it is discipline. We now know exactly what would reopen the derivation route, and we also have the honest fallback: project the unsilenced GK stress into R10/PPN/clock/orbital arenas as a nonclaim residual bound.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Parent Sign Source Audit",
        markdown_table(data["signs"], ["sign_id", "audit_item", "basis", "status", "effect"]),
        "",
        "## Boundary Ledger",
        markdown_table(data["boundary"], ["boundary_id", "condition", "why_needed", "status"]),
        "",
        "## Topology Hair Audit",
        markdown_table(data["topology"], ["topology_id", "topology_clause", "basis", "status"]),
        "",
        "## No-hair Eligibility Verdict",
        markdown_table(data["verdicts"], ["verdict_id", "question", "result", "evidence", "effect"]),
        "",
        "## Stress-bound Demotion Route",
        markdown_table(data["demotion"], ["demotion_id", "route_clause", "basis", "status"]),
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
        "signs": parent_sign_rows(),
        "boundary": boundary_rows(),
        "topology": topology_rows(),
        "verdicts": nohair_verdict_rows(),
        "demotion": demotion_route_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["parent_sign_audit"], data["signs"])
    write_csv(OUTPUTS["boundary_ledger"], data["boundary"])
    write_csv(OUTPUTS["topology_audit"], data["topology"])
    write_csv(OUTPUTS["nohair_verdict"], data["verdicts"])
    write_csv(OUTPUTS["demotion_route"], data["demotion"])
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
