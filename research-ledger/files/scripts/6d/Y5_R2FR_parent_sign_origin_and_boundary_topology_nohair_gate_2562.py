from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2562"
BRANCH_ID = "MTS_R2FR_PARENT_SIGN_ORIGIN_AND_BOUNDARY_TOPOLOGY_NOHAIR_GATE_2562"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2562-Y5-R2FR-parent-sign-origin-and-boundary-topology-nohair-gate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2562_SOURCE_REGISTER.csv",
    "parent_sign_audit": OUT / "P8_Y5_NO_SHADOW_2562_PARENT_SIGN_AUDIT.csv",
    "boundary_ledger": OUT / "P8_Y5_NO_SHADOW_2562_BOUNDARY_LEDGER.csv",
    "topology_audit": OUT / "P8_Y5_NO_SHADOW_2562_TOPOLOGY_HAIR_AUDIT.csv",
    "nohair_verdict": OUT / "P8_Y5_NO_SHADOW_2562_NOHAIR_ELIGIBILITY_VERDICT.csv",
    "demotion_route": OUT / "P8_Y5_NO_SHADOW_2562_STRESS_BOUND_DEMOTION_ROUTE.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2562_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2562_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2562_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2562_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2562_VALIDATION.csv",
}

COPY_TARGETS = {
    "parent_sign_blocker": QUEUE / "JR2562_PARENT_SIGN_BLOCKER_NONCLAIM.csv",
    "boundary_topology_blocker": LOCAL_BOUNDS / "Boundary_topology_nohair_blocker_2562_NONCLAIM.csv",
    "stress_bound_route": LOCAL_BOUNDS / "Stress_bound_local_metric_route_2562_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2562_00_2561_doc",
        "source_path": ROOT / "2561-Y5-R2FR-explicit-GK-quadratic-operator-sign-audit.md",
        "needles": ["COER2561_1_cross_bound", "NHG2561_7_current_claim", "NEXT2561_0_selected", "VAL2561_OVERALL"],
        "role": "active handoff selecting parent-sign and boundary/topology gate",
    },
    {
        "source_id": "SRC2562_01_2561_signs",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2561_DIMENSION_SIGN_TABLE.csv",
        "needles": ["SIGN2561_0_Z_A", "SIGN2561_4_c_AG", "MISSING_PARENT_SIGN"],
        "role": "healthy sign clauses remain parent-unsigned",
    },
    {
        "source_id": "SRC2562_02_2561_nohair",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2561_NOHAIR_ELIGIBILITY.csv",
        "needles": ["NHG2561_2_parent_sign", "NHG2561_3_boundary_topology", "BLOCKED_CURRENT_CLAIM"],
        "role": "no-hair eligibility nonpromotion",
    },
    {
        "source_id": "SRC2562_03_2561_bound",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2561_STRESS_BOUND_ROUTE.csv",
        "needles": ["BOUND2561_3_negative_branch", "BOUND2561_4_numeric_block", "MISSING_PARENT_COEFFICIENTS"],
        "role": "stress-bound fallback route",
    },
    {
        "source_id": "SRC2562_04_2560_failures",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2560_NOHAIR_FAILURE_MODES.csv",
        "needles": ["FAIL2560_3_boundary_hair", "FAIL2560_4_topological_hair", "FAIL2560_5_tau_projector_stress"],
        "role": "boundary/topology/tau failure modes",
    },
    {
        "source_id": "SRC2562_05_2560_metric",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2560_METRIC_IMPLICATIONS.csv",
        "needles": ["MET2560_1_current", "MET2560_2_bound_route", "BLOCKED_CURRENT_CLAIM"],
        "role": "local-GR metric and bound-route status",
    },
    {
        "source_id": "SRC2562_06_2472_precedent",
        "source_path": ROOT / "2472-Y5-R2FR-parent-sign-origin-and-boundary-topology-nohair-gate.md",
        "needles": ["PS2472_0_current_source", "DEM2472_0_demote_current_metric_branch", "VAL2472_OVERALL"],
        "role": "earlier parent-sign/boundary demotion precedent, re-run against 2561 chain",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for spec in SOURCE_SPECS:
        path = Path(spec["source_path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        exists = path.exists()
        rows.append(
            {
                **base_row(),
                "source_id": spec["source_id"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "missing_needles": ";".join(missing),
                "source_pass": bool_text(exists and not missing),
                "role": spec["role"],
            }
        )
    return rows


def parent_sign_rows() -> list[dict[str, Any]]:
    rows = [
        ("PS2562_0_current_source", "Current corpus contains no single parent action deriving Z_A,Z_G,m_A2,m_G2,c_AG signs.", "2561 sign audit", "MISSING_PARENT_SIGN_SOURCE", "blocks no-hair promotion"),
        ("PS2562_1_stability_principle", "Adopting positive energy as a new principle would sign the operator but would be new parent material.", "theory construction option", "NEW_MATERIAL_NOT_CURRENT_EVIDENCE", "allowed only as future construction"),
        ("PS2562_2_GR_analogy", "GR positive-energy intuition cannot sign GK coefficients by itself.", "external analogy is not derivation", "REJECT_AS_EVIDENCE", "prevents borrowing legitimacy"),
        ("PS2562_3_empirical_fit", "Choosing signs from local PPN/R10 success is forbidden.", "anti-circularity", "REJECTED", "no fitted sign route"),
        ("PS2562_4_cosmology_fit", "Choosing signs from cosmology/galaxy success is also insufficient for local no-hair.", "sector mismatch", "REJECT_AS_LOCAL_PROOF", "empirical hints cannot replace parent sign"),
        ("PS2562_5_operator_ansatz", "The 2561 quadratic operator is an audit ansatz, not a parent-sign source.", "operator status CANDIDATE_ONLY/NONCLAIM", "NOT_PARENT_EVIDENCE", "keeps ansatz useful but nonclaim"),
        ("PS2562_6_minimum_reopen", "Reopen requires explicit parent L_K/L_Gamma or a variational stability theorem fixing coefficient signs before local tests.", "reopen condition", "REQUIRED_TO_REOPEN", "exact missing material named"),
    ]
    return [
        {**base_row(), "sign_id": item, "audit_item": audit_item, "basis": basis, "status": status, "effect": effect}
        for item, audit_item, basis, status, effect in rows
    ]


def boundary_rows() -> list[dict[str, Any]]:
    rows = [
        ("BD2562_0_asymptotic_vacuum", "u approaches zero at local exterior boundary/infinity", "would kill many finite-energy modes", "ASSUMED_NOT_DERIVED"),
        ("BD2562_1_no_flux", "n_i K_hat^{ij}=0 and A/Gamma boundary flux vanish", "needed for energy identity boundary term", "ASSUMED_NOT_DERIVED"),
        ("BD2562_2_worldtube_matching", "source boundary has distributional matching conditions compatible with J_M and GK flux", "prevents hidden source hair at W boundary", "MISSING_JUMP_CONDITION"),
        ("BD2562_3_lab_cavity", "finite lab/solar-system domain may have environmental boundary data", "could source homogeneous GK hair", "BOUND_REQUIRED"),
        ("BD2562_4_tau_projector_boundary", "tau/P_loc boundary data must be parent-fixed or stress silent", "clock/projector can reintroduce local metric residual", "MISSING_TAU_PROJECTOR_BOUNDARY"),
        ("BD2562_5_reference_warning", "boundary condition cannot be chosen to cancel PPN residual after readout", "anti-tuning", "PASS_GUARDRAIL"),
        ("BD2562_6_current_status", "no parent boundary theorem currently closes all GK exterior fluxes", "source audit", "BLOCKED"),
    ]
    return [
        {**base_row(), "boundary_id": item, "condition": condition, "why_needed": why, "status": status}
        for item, condition, why, status in rows
    ]


def topology_rows() -> list[dict[str, Any]]:
    rows = [
        ("TOP2562_0_simply_connected", "If exterior Omega is simply connected with trivial relevant cohomology, harmonic GK hair is absent.", "standard no-hair simplification", "CONDITIONAL_ROUTE"),
        ("TOP2562_1_harmonic_A", "Nontrivial harmonic one-form/vector modes can carry stress with q_loc=0.", "topological hair failure mode", "BLOCKS_GENERAL_THEOREM"),
        ("TOP2562_2_gamma_zero_mode", "constant gamma zero-mode requires vacuum normalization or boundary fixing.", "scalar/compression hair", "BLOCKS_GENERAL_THEOREM"),
        ("TOP2562_3_topological_charge", "unsourced topological GK charge must be zero, quantized and fixed, or bounded.", "prevents hidden local stress", "MISSING_TOPOLOGY_LEDGER"),
        ("TOP2562_4_local_patch", "For ordinary local PPN patch, trivial topology is plausible but must be stated as a hypothesis.", "narrow local theorem route", "ASSUMPTION_ALLOWED"),
        ("TOP2562_5_global_theory", "global/cosmological sectors may allow topology while local exterior branch remains trivial.", "sector split", "POSSIBLE_SPLIT_NOT_PROOF"),
    ]
    return [
        {**base_row(), "topology_id": item, "topology_clause": clause, "basis": basis, "status": status}
        for item, clause, basis, status in rows
    ]


def nohair_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("NHV2562_0_narrow_patch", "Can a narrow stationary simply-connected patch no-hair contract be stated?", "YES_CONDITIONAL", "assume parent signs, no-flux/asymptotic boundary, trivial topology and tau/P silence", "usable as private contract only"),
        ("NHV2562_1_current_parent_sign", "Are parent signs available in current corpus?", "NO", "PS2562 audit found no source", "blocks promotion"),
        ("NHV2562_2_boundary_topology", "Are boundary/topology conditions proved?", "NO", "boundary flux, tau/P boundary and harmonic/topological modes remain assumptions", "blocks promotion"),
        ("NHV2562_3_current_nohair", "Does current MTS prove no-hair?", "NO", "parent signs and boundary/topology closure missing", "demote current local metric branch"),
        ("NHV2562_4_branch_status", "What is the honest current branch?", "STRESS_BOUND_ONLY_FOR_CLAIM_PURPOSES", "conditional theorem remains a future parent-action route, not current evidence", "select stress-bound runner next"),
        ("NHV2562_5_reopen_status", "Is the no-hair route dead?", "NO_REOPENABLE", "explicit sign/boundary/topology clauses now define what would reopen it", "keep as future derivation target"),
    ]
    return [
        {**base_row(), "verdict_id": item, "question": question, "result": result, "evidence": evidence, "effect": effect}
        for item, question, result, evidence, effect in rows
    ]


def demotion_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEM2562_0_demote_current_metric_branch", "Current local metric/no-hair branch is demoted to stress-bound only until parent signs and no-hair boundaries are supplied.", "no-hair not proved", "ACTIVE_FALLBACK"),
        ("DEM2562_1_bound_quantity", "Use delta_PPN <= C_metric norm(T_GK+T_tau/P+boundary) with defect terms from 2561.", "existing bound form", "BOUND_ROUTE"),
        ("DEM2562_2_needed_coefficients", "Need C_metric, C_T, C_B, C_S, negative_mode_defect, topology_hair_amplitude and arena projection coefficients.", "to compare to R10/PPN/clocks/orbital tests", "MISSING_NUMERIC_INPUTS"),
        ("DEM2562_3_claim_ceiling", "Stress-bound branch can show compatibility with local tests, not derivation of GR, unless bounds are derived and vanish in the GR limit.", "claim discipline", "NONCLAIM"),
        ("DEM2562_4_reopen_path", "If parent signs and boundary/topology are later supplied, no-hair theorem can be reopened.", "not dead, just unproved", "REOPENABLE"),
        ("DEM2562_5_next_runner", "Build a nonclaim local arena projection scaffold for R10, PPN, clocks and orbital tests.", "demoted branch needs empirical discipline", "SELECT_NEXT"),
    ]
    return [
        {**base_row(), "demotion_id": item, "route_clause": route_clause, "basis": basis, "status": status}
        for item, route_clause, basis, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2562_0_parent_sign", "GK signs are parent-derived.", "BLOCKED", "no source in current corpus", "false", "false"),
        ("GATE2562_1_boundary_topology", "boundary/topology no-hair is proved.", "BLOCKED", "conditions remain assumptions", "false", "false"),
        ("GATE2562_2_narrow_contract", "narrow simply-connected stationary patch contract exists.", "PASS_AS_CONDITIONAL_CONTRACT", "hypotheses can be stated clearly", "true", "false"),
        ("GATE2562_3_current_nohair", "current corpus proves no-hair.", "BLOCKED", "parent sign, boundary and topology gates fail", "false", "false"),
        ("GATE2562_4_stress_bound_fallback", "current local metric branch has a stress-bound fallback.", "PASS_AS_FALLBACK", "demotion route written", "true", "false"),
        ("GATE2562_5_local_GR_PPN", "local GR/PPN branch passes.", "BLOCKED", "only stress-bound nonclaim branch remains", "false", "false"),
        ("GATE2562_6_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", "true", "false"),
    ]
    return [
        {**base_row(), "gate_id": item, "claim": claim, "gate_status": status, "reason": reason, "gate_pass": gate_pass, "claim_promoted": promoted}
        for item, claim, status, reason, gate_pass, promoted in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2562_0_demote_for_now", "Demote current local metric/no-hair branch to stress-bound only.", "parent signs and boundary/topology closure are not current evidence", "prevents overclaim"),
        ("DEC2562_1_keep_future_route", "Keep no-hair as a reopenable future parent-action route.", "the conditional theorem shape is mathematically useful", "not discarded"),
        ("DEC2562_2_next_runner", "Build stress-bound local arena projection next.", "the active current branch needs empirical/local compatibility scaffolding", "2563 selected"),
        ("DEC2562_3_no_claim", "Do not claim local GR/PPN.", "current branch is bounded-residual only", "private nonclaim status retained"),
    ]
    return [
        {**base_row(), "decision_id": item, "decision": decision, "reason": reason, "effect": effect}
        for item, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2562_0_selected",
            "selection_status": "selected",
            "target_file": "2563-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md",
            "target_script": "scripts/Y5_R2FR_GK_stress_bound_local_arena_projection_runner_2563.py",
            "task": "turn the demoted stress-bound branch into a local arena projection scaffold for R10, PPN, clocks and orbital tests, without claiming a local-GR pass",
            "acceptance_target": "residual parameters, arena projection rows, missing coefficient ledger, nonclaim runner schema, baseline-comparison guardrails, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    copy_sources = {
        "parent_sign_blocker": OUTPUTS["parent_sign_audit"],
        "boundary_topology_blocker": OUTPUTS["boundary_ledger"],
        "stress_bound_route": OUTPUTS["demotion_route"],
    }
    rows = []
    for copy_id, source in copy_sources.items():
        target = COPY_TARGETS[copy_id]
        shutil.copyfile(source, target)
        rows.append(
            {
                **base_row(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": bool_text(source.exists()),
                "target_exists": bool_text(target.exists()),
            }
        )
    return rows


def csv_row_count(path: Path) -> int:
    if not path.exists() or path.stat().st_size == 0:
        return 0
    with path.open(newline="", encoding="utf-8") as handle:
        return max(sum(1 for _ in csv.DictReader(handle)), 0)


def formalization_status_detail() -> tuple[bool, str]:
    touched_paths = list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC, Path(__file__).resolve()]
    outside_formalization = [path for path in touched_paths if not is_relative_to(path, FORMALIZATION)]
    return len(outside_formalization) == len(touched_paths), f"declared_2562_paths_outside_formalization={len(outside_formalization)}/{len(touched_paths)}"


def validation_rows(
    sources: list[dict[str, Any]],
    signs: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    topology: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail})

    add("VAL2562_00_sources_exist", all(row["source_pass"] == "true" for row in sources), "all cited source paths exist and needles are present")
    add("VAL2562_01_parent_sign_blocked", any(row["sign_id"] == "PS2562_0_current_source" and row["status"] == "MISSING_PARENT_SIGN_SOURCE" for row in signs), "parent sign source missing")
    add("VAL2562_02_no_empirical_sign_fit", any(row["sign_id"] == "PS2562_3_empirical_fit" and row["status"] == "REJECTED" for row in signs), "empirical sign fitting rejected")
    add("VAL2562_03_boundary_blocked", any(row["boundary_id"] == "BD2562_6_current_status" and row["status"] == "BLOCKED" for row in boundary), "boundary closure blocked")
    add("VAL2562_04_topology_audit", any(row["topology_id"] == "TOP2562_1_harmonic_A" and row["status"] == "BLOCKS_GENERAL_THEOREM" for row in topology), "topological hair audit written")
    add("VAL2562_05_nohair_demoted", any(row["verdict_id"] == "NHV2562_4_branch_status" and row["result"] == "STRESS_BOUND_ONLY_FOR_CLAIM_PURPOSES" for row in verdicts), "current branch demoted to stress-bound for claims")
    add("VAL2562_06_demotion_route", any(row["demotion_id"] == "DEM2562_0_demote_current_metric_branch" and row["status"] == "ACTIVE_FALLBACK" for row in demotion), "stress-bound demotion route active")
    add("VAL2562_07_reopenable", any(row["demotion_id"] == "DEM2562_4_reopen_path" and row["status"] == "REOPENABLE" for row in demotion), "no-hair route remains reopenable")
    add("VAL2562_08_claim_gates_safe", all(row["claim_promoted"] == "false" for row in gates), "no claim gate allows local-GR/PPN claim")
    add("VAL2562_09_next_target_written", any(row["route_id"] == "NEXT2562_0_selected" and row["selection_status"] == "selected" for row in next_rows), "2563 stress-bound projection runner selected")
    add("VAL2562_10_branch_copies", all(row["source_exists"] == "true" and row["target_exists"] == "true" for row in branch_copies), "nonclaim branch copies exist")

    output_paths = list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]
    add("VAL2562_11_all_outputs_inside_post_checkpoint", all(is_relative_to(path, ROOT) for path in output_paths), "all 2562 outputs stay inside post-checkpoint-work")
    formalization_ok, formalization_detail = formalization_status_detail()
    add("VAL2562_12_formalization_workbench_not_targeted", formalization_ok, "declared 2562 outputs do not target formalization-workbench", formalization_detail)

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        add(f"VAL2562_OUTPUT_{key}", path.exists() and csv_row_count(path) > 0, f"{key} output exists and has rows", str(path))

    for copy_id, path in COPY_TARGETS.items():
        add(f"VAL2562_COPY_{copy_id}", path.exists() and csv_row_count(path) > 0, f"{copy_id} copy exists and has rows", str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2562_OVERALL", overall, "2562 blocks parent-sign/no-hair promotion and demotes current local metric route to stress-bound fallback")
    return rows


def escape_md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(escape_md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    signs: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    topology: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 2562 Y5 R2FR Parent Sign Origin And Boundary Topology No-hair Gate",
                "**Status:** parent-sign/no-hair promotion rejected for the current corpus. The narrow no-hair route remains mathematically useful, but the required coefficient signs, boundary conditions, topology exclusions, and tau/projector silence are not parent-derived. Therefore the current local metric branch is demoted to stress-bound only for claim purposes.",
                "**Meaning:** this is not a dead end; it is discipline. We now know exactly what would reopen the derivation route, and we also have the honest fallback: project the unsilenced GK stress into R10/PPN/clock/orbital arenas as a nonclaim residual bound.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
                "## Parent Sign Source Audit",
                markdown_table(signs, ["sign_id", "audit_item", "basis", "status", "effect"]),
                "## Boundary Ledger",
                markdown_table(boundary, ["boundary_id", "condition", "why_needed", "status"]),
                "## Topology Hair Audit",
                markdown_table(topology, ["topology_id", "topology_clause", "basis", "status"]),
                "## No-hair Eligibility Verdict",
                markdown_table(verdicts, ["verdict_id", "question", "result", "evidence", "effect"]),
                "## Stress-bound Demotion Route",
                markdown_table(demotion, ["demotion_id", "route_clause", "basis", "status"]),
                "## Claim Gates",
                markdown_table(gates, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_promoted"]),
                "## Decision Ledger",
                markdown_table(decisions, ["decision_id", "decision", "reason", "effect"]),
                "## Next Target",
                markdown_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
                "## Branch Copies",
                markdown_table(branch_copies, ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
                "## Validation",
                markdown_table(validations, ["check_id", "status", "notes", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    signs = parent_sign_rows()
    boundary = boundary_rows()
    topology = topology_rows()
    verdicts = nohair_verdict_rows()
    demotion = demotion_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["parent_sign_audit"], signs)
    write_csv(OUTPUTS["boundary_ledger"], boundary)
    write_csv(OUTPUTS["topology_audit"], topology)
    write_csv(OUTPUTS["nohair_verdict"], verdicts)
    write_csv(OUTPUTS["demotion_route"], demotion)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_copies = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validations = validation_rows(sources, signs, boundary, topology, verdicts, demotion, gates, decisions, next_rows, branch_copies)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, signs, boundary, topology, verdicts, demotion, gates, decisions, next_rows, branch_copies, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
