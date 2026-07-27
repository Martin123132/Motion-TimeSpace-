from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2552"
BRANCH_ID = "MTS_R2FR_MINIMAL_PARENT_CURRENT_CHAIN_PROMOTION_OR_DENOMINATOR_FINAL_BLOCK_2552"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SCRIPTS = ROOT / "scripts"

DOC = ROOT / "2552-Y5-R2FR-minimal-parent-current-chain-promotion-or-denominator-final-block.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2552_SOURCE_REGISTER.csv",
    "promotion_contract": OUT / "P8_Y5_NO_SHADOW_2552_CURRENT_CHAIN_PROMOTION_CONTRACT.csv",
    "sector_audit": OUT / "P8_Y5_NO_SHADOW_2552_SECTOR_OWNERSHIP_AUDIT.csv",
    "theta_qtau_verdict": OUT / "P8_Y5_NO_SHADOW_2552_THETA_QTAU_PROMOTION_VERDICT.csv",
    "denominator_final_block": OUT / "P8_Y5_NO_SHADOW_2552_DENOMINATOR_FINAL_BLOCK.csv",
    "reopen_material": OUT / "P8_Y5_NO_SHADOW_2552_REOPEN_MATERIAL_SPEC.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2552_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_NO_SHADOW_2552_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2552_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2552_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2552_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_promotion": QUEUE / "JR2552_CURRENT_CHAIN_PROMOTION_CONTRACT_NONCLAIM.csv",
    "queue_reopen": QUEUE / "JR2552_REOPEN_MATERIAL_SPEC_NONCLAIM.csv",
    "hamiltonian_final_block": HAMILTONIAN / "Hamiltonian_denominator_final_block_2552_NONCLAIM.csv",
    "local_final_block": LOCAL_BOUNDS / "Local_scoring_denominator_final_block_2552_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2552_00_2551_doc",
        "source_path": ROOT / "2551-Y5-R2FR-parent-Hamiltonian-charge-extraction-positivity-pack-or-denominator-block.md",
        "needles": ["DBL2551_0_pack_assembly", "DEC2551_2_next_best_target", "NEXT2551_0_selected", "VAL2551_OVERALL"],
        "role": "active handoff selecting minimal current-chain promotion gate",
    },
    {
        "source_id": "SRC2552_01_2551_pack_matrix",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2551_EXISTING_SOURCE_PACK_FIT_MATRIX.csv",
        "needles": ["CAND2551_1009_current_chain", "REQ2551_0_parent_action", "CONTRACT_COVERS_BUT_NOT_PROMOTED"],
        "role": "machine-readable pack fit matrix",
    },
    {
        "source_id": "SRC2552_02_1009_current_chain",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_9_total_parent_contract", "SVR1009_6_total_parent_switch_unsigned", "CG1009_5_Htau_MHref_local_GR", "V1009_SUMMARY"],
        "role": "minimal parent current-chain sector contract",
    },
    {
        "source_id": "SRC2552_03_1008_theta_qtau",
        "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "needles": ["PVA1008_6_verdict", "QTA1008_8_Q_total", "CG1008_1_Qtau_total", "V1008_SUMMARY"],
        "role": "theta/Q_tau extraction status",
    },
    {
        "source_id": "SRC2552_04_1010_gk_hard_block",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["GKT1010_6_verdict", "QRES1010_0_q_loc_vector", "CG1010_5_Htau_MHref_local_GR", "V1010_SUMMARY"],
        "role": "Gamma/Khat/q_loc hard non-EH sector blocker",
    },
    {
        "source_id": "SRC2552_05_min_action_blocks",
        "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "needles": ["A511_5_boundary_reference", "worldtube/source-measure equality shifts by boundary bookkeeping"],
        "role": "minimum action block source map",
    },
    {
        "source_id": "SRC2552_06_symbol_map",
        "source_path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "needles": ["q_loc^nu", "not_derived_zero; plateau_axiom_forbidden", "Pi_M"],
        "role": "symbol-to-action placement and q_loc residual status",
    },
    {
        "source_id": "SRC2552_07_variation_gates",
        "source_path": OUT / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        "needles": ["FV512_2_Gamma_Khat_q", "fail_for_current_claim"],
        "role": "first-variation gate status for Gamma/Khat/q_loc",
    },
]

SECTORS = [
    ("PCS2552_0_EH_core", "EH anchor", "theta_EH and Q_tau^EH", "baseline_anchor_not_total_parent", "EH_ANCHOR_REJECTED_AS_TOTAL_PARENT_ACTION"),
    ("PCS2552_1_kappa_topological", "kappa/topological", "d kappa_eff=0 and no local coupling drift", "candidate_not_adopted", "MISSING_PARENT_ADOPTION"),
    ("PCS2552_2_universal_matter", "universal matter", "Hilbert current and universal source coupling", "conditional_source_input", "MISSING_MATTER_DESCENT_AND_SOURCE_WARD"),
    ("PCS2552_3_boundary_reference", "boundary/reference", "theta_boundary and Q_tau^boundary", "fixed_reference_missing", "MISSING_FIXED_REFERENCE_BEFORE_READOUT"),
    ("PCS2552_4_Gamma_Khat_extra", "Gamma/Khat/q_loc", "T_GK, Euler closure, double-zero local residual", "hard_fail_current_claim", "MISSING_S_GK_HELMHOLTZ_EULER_DOUBLE_ZERO"),
    ("PCS2552_5_domain_projector_selector", "domain/projector selector", "local selector/projector stress zero or retained", "partial_clause_not_parent_closed", "MISSING_SELECTOR_STRESS_AND_BOUNDARY_CLOSURE"),
    ("PCS2552_6_mass_projector_PiM", "Pi_M/source-measure", "d(Pi_M J_H)=0 or exact residual", "not_parent_derived", "MISSING_PIM_PARENT_ORIGIN_AND_VARIATION"),
    ("PCS2552_7_memory_response_doublet", "memory response doublet", "local double-zero with cosmological activation allowed", "partial_candidate_not_matched", "MISSING_FULL_DOUBLET_VARIATION_AND_PPN_LOCK"),
    ("PCS2552_8_worldtube_source_glue", "worldtube/source glue", "M_source[W]=int_S Q_M[tau] before orbital fitting", "core_missing_piece", "MISSING_WORLDTUBE_SOURCE_GLUE"),
]

PROMOTION_REQUIREMENTS = [
    ("PCC2552_0_single_action_source", "one explicit S_parent source", "single source/equation owns the retained field list, not stitched CSV contracts"),
    ("PCC2552_1_field_list", "complete field and variation list", "g_obs, coframe/tau, matter, Gamma/Khat variables, projector/domain, boundary/reference and source worldtube variables"),
    ("PCC2552_2_sector_variations", "each retained sector has first variation", "delta S_i=E_i delta Phi_i+d theta_i plus stress/source contribution"),
    ("PCC2552_3_theta_sum", "theta_MTS=sum theta_i is explicit", "no missing theta_extra/theta_projector/theta_boundary/theta_matter pieces"),
    ("PCC2552_4_Qtau_sum", "J_tau=dQ_tau^MTS+C_tau is explicit", "all Q_tau pieces and constraints are zero, bounded or sourced"),
    ("PCC2552_5_fixed_reference", "boundary/reference fixed before readout", "no fitted H_ref, counterterm, or reference-only normalization"),
    ("PCC2552_6_hard_sector_closure", "Gamma/Khat/q_loc sector is variational or retained", "S_GK, metric response, Helmholtz, Euler/double-zero, or explicit residual policy"),
    ("PCC2552_7_source_bridge", "Pi_M/worldtube/source measure is parent-owned or retained", "source charge bridge cannot be observed-GM or fitted mass"),
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: bool) -> str:
    return "true" if value else "false"


def metadata(valid_for_claim: bool = False, claim_allowed: bool = False) -> dict[str, str]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": truth(valid_for_claim),
        "claim_allowed": truth(claim_allowed),
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def cell(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def table(columns: list[str], rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def inside_root(path: Path) -> bool:
    resolved = path.resolve()
    root = ROOT.resolve()
    return resolved == root or root in resolved.parents


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                **metadata(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": truth(path.exists()),
                "needles": ";".join(source["needles"]),
                "missing_needles": ";".join(missing),
                "source_pass": truth(path.exists() and not missing),
                "role": source["role"],
            }
        )
    return rows


def promotion_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            **metadata(),
            "contract_id": contract_id,
            "required_clause": clause,
            "acceptance_rule": rule,
            "current_status": "MISSING_OR_CONTRACT_ONLY",
            "promote_clause": "false",
        }
        for contract_id, clause, rule in PROMOTION_REQUIREMENTS
    ]


def sector_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            **metadata(),
            "sector_id": sector_id,
            "sector": sector,
            "needed_current": needed,
            "current_status": status,
            "hard_blocker": blocker,
            "theta_contribution_owned": "true" if sector_id == "PCS2552_0_EH_core" else "false",
            "Qtau_contribution_owned": "true" if sector_id == "PCS2552_0_EH_core" else "false",
            "promote_sector": "false",
            "valid_for_claim": "false",
        }
        for sector_id, sector, needed, status, blocker in SECTORS
    ]


def theta_qtau_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "verdict_id": "TQV2552_0_conditional_sum",
            "question": "If all sector variations were owned, would theta_MTS and Q_tau^MTS be defined?",
            "result": "YES_CONDITIONAL",
            "evidence": "delta S_parent=sum_i delta S_i => theta_MTS=sum_i theta_i; J_tau=dQ_tau^MTS+C_tau if each sector supplies charge/constraint pieces",
            "claim_status": "PASS_AS_CONTRACT_ONLY",
        },
        {
            "verdict_id": "TQV2552_1_current_promotion",
            "question": "Does current MTS promote theta_MTS and Q_tau^MTS?",
            "result": "NO",
            "evidence": "only EH anchor has owned theta/Q shape; boundary, Gamma/Khat, projector, worldtube, response and matter/source pieces are partial or blocked",
            "claim_status": "FAIL_CURRENT_CLAIM",
        },
        {
            "verdict_id": "TQV2552_2_hardest_block",
            "question": "What prevents denominator progress first?",
            "result": "GAMMA_KHAT_QLOC_AND_PIM_WORLDTUBE",
            "evidence": "Gamma/Khat lacks S_GK/Helmholtz/Euler/double-zero; Pi_M/worldtube lacks parent source-measure bridge",
            "claim_status": "LOCAL_DENOMINATOR_BLOCKER",
        },
        {
            "verdict_id": "TQV2552_3_denominator_availability",
            "question": "Is M_H_ref/N_E available from current corpus?",
            "result": "NO_UNAVAILABLE_UNTIL_NEW_PARENT_ACTION_MATERIAL",
            "evidence": "minimal current-chain promotion fails; 2551 pack remains partial; 2549 live runner remains blocked",
            "claim_status": "FINAL_BLOCK_FOR_CURRENT_CORPUS",
        },
    ]
    return [{**metadata(), **row, "valid_for_claim": "false", "claim_allowed": "false"} for row in rows]


def denominator_final_block_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "block_id": "DFB2552_0_MHref_unavailable",
            "object": "M_H_ref/N_E",
            "block_status": "UNAVAILABLE_UNTIL_NEW_PARENT_ACTION_MATERIAL",
            "reason": "theta_MTS and Q_tau^MTS are not promoted from the minimal current-chain action",
            "resume_condition": "single parent action source with owned sector variations, theta/Q pieces, fixed reference, and source bridge",
            "claim_allowed": "false",
        },
        {
            "block_id": "DFB2552_1_finite_Delta_ref_scoring",
            "object": "Delta_ref_boundary_leak_over_M_H_ref",
            "block_status": "BLOCKED_FOR_CURRENT_CORPUS",
            "reason": "denominator unavailable; component values also missing",
            "resume_condition": "valid denominator plus sourced metric/tau/counterterm/topology leak values",
            "claim_allowed": "false",
        },
        {
            "block_id": "DFB2552_2_zero_reference_route",
            "object": "D_a Delta_ref=0",
            "block_status": "CLOSURE_ONLY_FOR_CURRENT_CORPUS",
            "reason": "parent fixed-boundary contract not signed and denominator/reference ownership unavailable",
            "resume_condition": "one parent action signs fixed beta_ref plus Hamiltonian denominator clauses",
            "claim_allowed": "false",
        },
        {
            "block_id": "DFB2552_3_local_GR_Newton_PPN",
            "object": "local GR/Newton/PPN branch",
            "block_status": "BLOCKED_FOR_CURRENT_CORPUS",
            "reason": "no theorem-zero route and no finite normalized residual route",
            "resume_condition": "new parent current-chain material or a non-Hamiltonian local-GR route with its own normalization",
            "claim_allowed": "false",
        },
    ]
    return [{**metadata(), **row, "valid_for_claim": "false"} for row in rows]


def reopen_material_rows() -> list[dict[str, Any]]:
    rows = [
        ("MAT2552_0_action_source", "explicit parent action density", "S_parent=sum S_i with field list and dimensions", "must include all retained sectors or explicitly demote omitted sectors"),
        ("MAT2552_1_variation_pack", "sector first-variation pack", "delta S_i=E_i delta Phi_i+d theta_i for each sector", "must name theta_i, stress/source terms and boundary terms"),
        ("MAT2552_2_charge_pack", "Noether/Hamiltonian charge pack", "J_tau=dQ_tau^MTS+C_tau with every C_tau zero/bounded/sourced", "must not use EH charge as full MTS charge"),
        ("MAT2552_3_GK_pack", "Gamma/Khat variational pack", "S_GK or retained q_loc residual with Helmholtz/Euler/double-zero status", "must close or explicitly bound the hard local sector"),
        ("MAT2552_4_source_pack", "Pi_M/worldtube/source-measure pack", "parent source worldtube, same-frame J_H, Pi_M map and fixed linking surfaces", "must not use orbital GM or fitted masks"),
        ("MAT2552_5_reference_pack", "fixed reference/counterterm pack", "H_ref/B_ref fixed before readout with no cancellation tuning", "must include source path/equation ref and improvement convention"),
    ]
    return [
        {
            **metadata(),
            "material_id": material_id,
            "needed_material": material,
            "minimal_form": form,
            "acceptance_rule": rule,
            "status": "REQUIRED_TO_REOPEN",
            "valid_for_claim": "false",
        }
        for material_id, material, form, rule in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2552_0_conditional_current_chain", "If every sector is parent-owned, theta_MTS and Q_tau^MTS follow by summing sector variations.", "PASS_AS_CONTRACT", "the current-chain identity is mathematically correct as a contract", "true", "false"),
        ("GATE2552_1_current_chain_promoted", "Current corpus promotes the minimal parent current-chain action.", "BLOCKED", "sector variations, theta/Q pieces, hard GK sector and PiM/worldtube bridge remain unsigned", "false", "false"),
        ("GATE2552_2_theta_Qtau", "theta_MTS and Q_tau^MTS are owned current theorem objects.", "BLOCKED", "1008/1009 keep total charge extraction nonclaim", "false", "false"),
        ("GATE2552_3_denominator", "M_H_ref/N_E denominator is available.", "FINAL_BLOCK_CURRENT_CORPUS", "denominator depends on unpromoted theta/Q_tau and source bridge", "false", "false"),
        ("GATE2552_4_local_GR", "Local GR/Newton/PPN branch passes.", "BLOCKED", "no theorem-zero route and no normalized finite residual route", "false", "false"),
    ]
    return [
        {
            **metadata(),
            "gate_id": gate_id,
            "claim": claim,
            "gate_status": status,
            "reason": reason,
            "gate_pass": passed,
            "claim_allowed": allowed,
        }
        for gate_id, claim, status, reason, passed, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2552_0_no_promotion",
            "decision": "Do not promote the minimal parent current-chain action from current evidence.",
            "reason": "it is a contract-shaped sector map, not a single parent action with owned variations",
            "effect": "theta_MTS/Q_tau^MTS remain nonclaim",
        },
        {
            "decision_id": "DEC2552_1_denominator_final_block",
            "decision": "Mark the Hamiltonian denominator unavailable for the current corpus.",
            "reason": "M_H_ref depends on theta/Q_tau, H_tau integrability, fixed reference and source bridge",
            "effect": "finite Delta_ref and local-GR scoring cannot proceed on this route until new parent-action material appears",
        },
        {
            "decision_id": "DEC2552_2_reopen_conditions",
            "decision": "Record exact reopen material instead of circling the same blocker.",
            "reason": "the missing pieces are now named enough to avoid repeated denominator audits",
            "effect": "future work can either supply MAT2552 rows or choose a different local-GR route",
        },
        {
            "decision_id": "DEC2552_3_next_route",
            "decision": "Pivot to local-GR route triage and non-Hamiltonian options.",
            "reason": "the Hamiltonian denominator branch is blocked under current evidence but the broader GR-reduction goal remains active",
            "effect": "next checkpoint should rank route options rather than repeat M_H_ref gates",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **metadata(),
            "route_id": "NEXT2552_0_selected",
            "selection_status": "selected",
            "target_file": "2553-Y5-R2FR-local-GR-route-triage-after-Hamiltonian-denominator-block.md",
            "target_script": "scripts/Y5_R2FR_local_GR_route_triage_after_Hamiltonian_denominator_block_2553.py",
            "task": "rank remaining local-GR/Newton reduction routes after the Hamiltonian denominator block: new parent-action construction, q_loc residual bounds, non-Hamiltonian normalization, or empirical-only deferral",
            "acceptance_target": "route table with prerequisites, claim ceiling, quickest falsifiable test path, and next derivation target",
            "guardrails": "do not reopen M_H_ref without MAT2552 material; no orbital-GM denominator; no theorem-zero from closure; no local-GR claim; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue_promotion", OUTPUTS["promotion_contract"], COPY_TARGETS["queue_promotion"]),
        ("queue_reopen", OUTPUTS["reopen_material"], COPY_TARGETS["queue_reopen"]),
        ("hamiltonian_final_block", OUTPUTS["denominator_final_block"], COPY_TARGETS["hamiltonian_final_block"]),
        ("local_final_block", OUTPUTS["denominator_final_block"], COPY_TARGETS["local_final_block"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            {
                **metadata(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": truth(source.exists()),
                "target_exists": truth(target.exists()),
            }
        )
    return rows


def csv_parse_status(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:
        return False, 0, repr(exc)


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    artifact_markers = (
        "2552-Y5",
        "_2552_",
        "_2552.",
        "JR2552",
        "P8_Y5_NO_SHADOW_2552",
        "P8_Y5_BRR545_2552",
        "Y5_R2FR_minimal_parent_current_chain_promotion_or_denominator_final_block_2552",
    )
    return [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in artifact_markers)
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    promotion_rows: list[dict[str, Any]],
    sector_rows: list[dict[str, Any]],
    verdict_rows: list[dict[str, Any]],
    final_block_rows: list[dict[str, Any]],
    material_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail})

    add("VAL2552_00_sources_exist", all(row["source_pass"] == "true" for row in source_rows), "all cited source paths exist and needles are present", ";".join(row["source_id"] for row in source_rows if row["source_pass"] != "true"))
    add("VAL2552_01_promotion_contract_complete", len(promotion_rows) == len(PROMOTION_REQUIREMENTS), "current-chain promotion contract requirements are complete", str(len(promotion_rows)))
    add("VAL2552_02_no_promotion_clauses", all(row["promote_clause"] == "false" for row in promotion_rows), "no current-chain requirement is promoted from current evidence")
    add("VAL2552_03_sector_audit_complete", len(sector_rows) == len(SECTORS), "sector ownership audit covers minimal parent sectors", str(len(sector_rows)))
    add("VAL2552_04_sector_claims_blocked", all(row["promote_sector"] == "false" for row in sector_rows), "all non-EH sector promotions remain blocked")
    add("VAL2552_05_theta_qtau_final_block", any(row["claim_status"] == "FINAL_BLOCK_FOR_CURRENT_CORPUS" for row in verdict_rows), "theta/Q_tau verdict blocks current denominator")
    add("VAL2552_06_denominator_final_block", any(row["block_status"] == "UNAVAILABLE_UNTIL_NEW_PARENT_ACTION_MATERIAL" for row in final_block_rows), "Hamiltonian denominator is marked unavailable until new material")
    add("VAL2552_07_reopen_material_written", len(material_rows) >= 6 and all(row["status"] == "REQUIRED_TO_REOPEN" for row in material_rows), "reopen material specification is written")
    add("VAL2552_08_claim_gates_safe", all(row["claim_allowed"] == "false" for row in gate_rows) and any(row["gate_id"] == "GATE2552_4_local_GR" and row["gate_status"] == "BLOCKED" for row in gate_rows), "local-GR/PPN/Newton claims remain blocked")
    add("VAL2552_09_next_target_written", len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2552_0_selected", "2553 route triage target selected")
    add("VAL2552_10_branch_copies", len(branch_rows) == 4 and all(row["target_exists"] == "true" for row in branch_rows), "nonclaim branch copies exist")
    add("VAL2552_11_no_formalization_artifacts", not formalization_hits(), "no 2552 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_hits()))
    add("VAL2552_12_all_outputs_inside_post_checkpoint", all(inside_root(path) for path in list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]), "all 2552 outputs stay inside post-checkpoint-work")
    add("VAL2552_13_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent after cleanup")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2552_CSV_{path.stem}", ok, f"CSV parses with {count} rows" if ok else "CSV parse failed", detail or str(path))

    for key, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2552_COPY_CSV_{key}", ok, f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed", detail or str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2552_OVERALL", overall, "2552 refuses current-chain promotion, final-blocks Hamiltonian denominator for current corpus, and selects local route triage")
    return [{**metadata(), **row} for row in rows]


def write_doc(
    sources: list[dict[str, Any]],
    promotion_rows: list[dict[str, Any]],
    sector_rows: list[dict[str, Any]],
    verdict_rows: list[dict[str, Any]],
    final_block_rows: list[dict[str, Any]],
    material_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = "\n\n".join(
        [
            "# 2552 Y5 R2FR Minimal Parent Current-chain Promotion Or Denominator Final Block",
            "**Result:** minimal parent current-chain promotion attempted and refused for the current corpus. The conditional identity is fine: if one parent action owns every sector, then `theta_MTS=sum theta_i` and `Q_tau^MTS=sum Q_i` are legitimate. But the current evidence does not promote the sector chain, so the Hamiltonian denominator is unavailable until new parent-action material is supplied.",
            "**Private reading:** this is where we stop circling the denominator. It is not dead as a future route, but it cannot be spent as current proof-credit. The next intelligent move is route triage: either build new parent-action material, bound `q_loc` directly, or find a different normalization path.",
            "## Source Register\n" + table(["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"], sources),
            "## Current-chain Promotion Contract\n" + table(["contract_id", "required_clause", "acceptance_rule", "current_status", "promote_clause"], promotion_rows),
            "## Sector Ownership Audit\n" + table(["sector_id", "sector", "needed_current", "current_status", "hard_blocker", "theta_contribution_owned", "Qtau_contribution_owned", "promote_sector"], sector_rows),
            "## Theta/Q_tau Promotion Verdict\n" + table(["verdict_id", "question", "result", "evidence", "claim_status"], verdict_rows),
            "## Denominator Final Block\n" + table(["block_id", "object", "block_status", "reason", "resume_condition", "claim_allowed"], final_block_rows),
            "## Reopen Material Specification\n" + table(["material_id", "needed_material", "minimal_form", "acceptance_rule", "status"], material_rows),
            "## Claim Gates\n" + table(["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"], gates),
            "## Decision Ledger\n" + table(["decision_id", "decision", "reason", "effect"], decisions),
            "## Next Target\n" + table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], next_rows),
            "## Branch Copies\n" + table(["copy_id", "source_path", "target_path", "source_exists", "target_exists"], branch_rows),
            "## Validation\n" + table(["check_id", "status", "notes", "detail"], validations),
        ]
    )
    DOC.write_text(doc + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    promotion = promotion_contract_rows()
    sectors = sector_audit_rows()
    verdicts = theta_qtau_verdict_rows()
    final_blocks = denominator_final_block_rows()
    materials = reopen_material_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["promotion_contract"], promotion)
    write_csv(OUTPUTS["sector_audit"], sectors)
    write_csv(OUTPUTS["theta_qtau_verdict"], verdicts)
    write_csv(OUTPUTS["denominator_final_block"], final_blocks)
    write_csv(OUTPUTS["reopen_material"], materials)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(sources, promotion, sectors, verdicts, final_blocks, materials, gates, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, promotion, sectors, verdicts, final_blocks, materials, gates, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
