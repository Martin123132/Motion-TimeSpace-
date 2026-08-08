from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2550"
BRANCH_ID = "MTS_R2FR_SAME_FRAME_HAMILTONIAN_DENOMINATOR_DERIVATION_OR_RETAIN_LOCAL_BOUND_BLOCK_2550"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SCRIPTS = ROOT / "scripts"

DOC = ROOT / "2550-Y5-R2FR-same-frame-Hamiltonian-denominator-derivation-or-retain-local-bound-block.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2550_SOURCE_REGISTER.csv",
    "denominator_contract": OUT / "P8_Y5_NO_SHADOW_2550_HAMILTONIAN_DENOMINATOR_CONTRACT.csv",
    "positivity_audit": OUT / "P8_Y5_NO_SHADOW_2550_POSITIVITY_AND_SAME_FRAME_AUDIT.csv",
    "candidate_rows": OUT / "P8_Y5_NO_SHADOW_2550_DENOMINATOR_CANDIDATE_ROWS.csv",
    "local_block": OUT / "P8_Y5_NO_SHADOW_2550_LOCAL_BOUND_SCORING_BLOCK.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2550_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_NO_SHADOW_2550_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2550_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2550_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2550_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_contract": QUEUE / "JR2550_HAMILTONIAN_DENOMINATOR_CONTRACT_NONCLAIM.csv",
    "queue_local_block": QUEUE / "JR2550_LOCAL_BOUND_SCORING_BLOCK_NONCLAIM.csv",
    "hamiltonian_candidates": HAMILTONIAN / "Hamiltonian_denominator_candidate_rows_2550_NONCLAIM.csv",
    "local_bound_block": LOCAL_BOUNDS / "Local_bound_scoring_block_2550_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2550_00_2549_doc",
        "source_path": ROOT / "2549-Y5-R2FR-first-Delta-ref-bound-value-runner-or-same-frame-denominator-source.md",
        "needles": ["DEN2549_0_live_MHref_schema", "RUN2549_live", "NEXT2549_0_selected", "VAL2549_OVERALL"],
        "role": "active handoff selecting same-frame Hamiltonian denominator derivation",
    },
    {
        "source_id": "SRC2550_01_2549_denominator_gate",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2549_DENOMINATOR_SOURCE_GATE.csv",
        "needles": ["DEN2549_0_live_MHref_schema", "DEN2549_2_rejected_orbital_GM", "BLOCKED_MISSING_STABLE_MH_REF"],
        "role": "machine-readable live denominator blockers",
    },
    {
        "source_id": "SRC2550_02_2549_runner",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2549_NO_CANCELLATION_RUNNER_RESULTS.csv",
        "needles": ["RUN2549_live", "BLOCKED_NOT_COMPUTED"],
        "role": "live finite Delta_ref runner refusal caused by missing denominator",
    },
    {
        "source_id": "SRC2550_03_2460_contract",
        "source_path": ROOT / "2460-Y5-R2FR-same-frame-Hamiltonian-denominator-derivation-or-retain-local-bound-block.md",
        "needles": ["HDC2460_0_charge_definition", "HDC2460_7_current_verdict", "VAL2460_OVERALL"],
        "role": "earlier exact same-frame Hamiltonian denominator contract",
    },
    {
        "source_id": "SRC2550_04_1006_MHref",
        "source_path": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        "needles": ["MHS1006_0_Htau_minus_Href", "CG1006_0_MHref_positive_same_frame", "ORBITAL_GM_SUBSTITUTION_REJECTED", "V1006_SUMMARY"],
        "role": "positive same-frame M_H_ref attempt and no-orbital-GM rule",
    },
    {
        "source_id": "SRC2550_05_1007_integrability",
        "source_path": ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
        "needles": ["HTA1007_6_integrability_verdict", "CG1007_3_MHref", "DEC1007_0_integrability_not_claimed", "V1007_SUMMARY"],
        "role": "H_tau integrability/fixed-reference blocker",
    },
    {
        "source_id": "SRC2550_06_1008_theta_Qtau",
        "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "needles": ["PVA1008_6_verdict", "QTA1008_8_Q_total", "CG1008_5_MHref", "V1008_SUMMARY"],
        "role": "parent theta/Q_tau extraction blocker",
    },
    {
        "source_id": "SRC2550_07_1009_current_chain",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_9_total_parent_contract", "CG1009_5_Htau_MHref_local_GR", "DEC1009_0_contract_not_parent_action", "V1009_SUMMARY"],
        "role": "sector action/current-chain contract blocker",
    },
    {
        "source_id": "SRC2550_08_1016_worldtube",
        "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["PSC1016_5_dressed_source_charge", "PST1016_1_source_measure_lemma", "CG1016_2_M_H_ref_claim", "V1016_SUMMARY"],
        "role": "source worldtube/Hamiltonian measure bridge blocker",
    },
    {
        "source_id": "SRC2550_09_1017_reference_lock",
        "source_path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["HRL1017_5_MHref_denominator", "MHR1017_0_M_H_ref_denominator", "CG1017_4_MHref_claim", "V1017_SUMMARY"],
        "role": "Hamiltonian PiM reference-lock blocker",
    },
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


def denominator_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "HDC2550_0_charge_definition",
            "clause": "Define the local-normalization denominator as a parent Hamiltonian/source charge, not as an observed orbital mass.",
            "formula": "M_H_ref := G_ref^{-1}(H_tau[S_outer]-H_ref[beta_ref]) = G_ref^{-1} int_S Q_tau^MTS - G_ref^{-1}H_ref",
            "must_be_signed_by": "parent action; fixed reference; same tau/coframe; source worldtube selector",
            "current_status": "DEFINITION_CONTRACT_ONLY",
        },
        {
            "contract_id": "HDC2550_1_parent_charge_extraction",
            "clause": "Extract theta_MTS, J_tau and Q_tau^MTS from the retained parent sectors.",
            "formula": "delta L_parent=E_A delta Phi^A+d theta_MTS; J_tau=theta_MTS(L_tau Phi)-i_tau L_parent=dQ_tau^MTS+C_tau",
            "must_be_signed_by": "sector variation ledger with no hidden stress/charge pieces",
            "current_status": "BLOCKED_BY_1008_1009",
        },
        {
            "contract_id": "HDC2550_2_integrability",
            "clause": "Show the Hamiltonian variation is finite, differentiable and path-independent.",
            "formula": "delta H_tau[S]=int_S(delta Q_tau^MTS-i_tau theta_MTS)-delta H_ref with field-space curl zero",
            "must_be_signed_by": "parent symplectic form and boundary-condition theorem",
            "current_status": "BLOCKED_BY_1007",
        },
        {
            "contract_id": "HDC2550_3_same_frame_lock",
            "clause": "Use one tau/coframe/readout frame for source, charge, clocks, rods and boundary.",
            "formula": "tau_source=tau_charge=tau_clock=tau_boundary=tau_readout and e_source=e_readout=e_obs",
            "must_be_signed_by": "frame-selector theorem and readout map",
            "current_status": "BLOCKED_BY_1016_1017",
        },
        {
            "contract_id": "HDC2550_4_fixed_reference",
            "clause": "Fix H_ref before source/readout variation and forbid counterterm absorption.",
            "formula": "D_readout H_ref=D_source H_ref=0 and no fitted H_ref or cancellation counterterm",
            "must_be_signed_by": "reference-lock certificate",
            "current_status": "BLOCKED_BY_1007_1017_2549",
        },
        {
            "contract_id": "HDC2550_5_source_worldtube_bridge",
            "clause": "Link the outer charge surface to a parent-selected compact source worldtube.",
            "formula": "W_source=closure(supp J_H[tau]); S_outer links W_source in a source-free exterior",
            "must_be_signed_by": "source measure/worldtube lemma",
            "current_status": "BLOCKED_BY_1016",
        },
        {
            "contract_id": "HDC2550_6_positivity",
            "clause": "Prove the same-frame charge is strictly positive for nonzero ordinary compact sources.",
            "formula": "int_S Q_tau^MTS - H_ref > 0 with extra/projector/boundary sectors zero or bounded",
            "must_be_signed_by": "parent energy/source positivity theorem plus extra-sector charge bound",
            "current_status": "MISSING_PARENT_ENERGY_POSITIVITY_THEOREM",
        },
        {
            "contract_id": "HDC2550_7_current_verdict",
            "clause": "Promote M_H_ref to a live positive denominator for local residual scoring.",
            "formula": "HDC2550_1 through HDC2550_6 all signed => M_H_ref>0 and same-frame",
            "must_be_signed_by": "one coherent parent Hamiltonian charge extraction/positivity pack",
            "current_status": "FAIL_CURRENT_CLAIM_BUT_EXACT_CONTRACT_WRITTEN",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def positivity_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("POS2550_0_theta_Qtau", "theta_MTS and Q_tau^MTS extracted from parent action", "MISSING_PARENT_THETA_QTAU_EXTRACTION", "without Q_tau there is no charge to make positive"),
        ("POS2550_1_integrability", "field-space curl of delta H_tau vanishes", "MISSING_HTAU_INTEGRABILITY", "path-dependent Hamiltonian one-form cannot define a denominator"),
        ("POS2550_2_fixed_reference", "H_ref fixed before readout/source variation", "MISSING_FIXED_REFERENCE_CERTIFICATE", "reference shift could fake positivity or shrink residuals"),
        ("POS2550_3_same_frame", "tau/coframe shared by charge, source and readout", "MISSING_TAU_COFRAME_LOCK", "frame mismatch makes normalized residual meaningless"),
        ("POS2550_4_worldtube", "charge surface links parent-selected compact source", "MISSING_PARENT_WORLDTUBE_SELECTOR", "denominator could be fitted to the wrong object"),
        ("POS2550_5_energy_condition", "ordinary source contribution is nonnegative and nonzero", "MISSING_PARENT_ENERGY_POSITIVITY_THEOREM", "positive denominator cannot be inferred from notation"),
        ("POS2550_6_extra_sector_silence", "extra/projector/boundary sectors do not add negative unbounded charge", "MISSING_EXTRA_SECTOR_CHARGE_BOUND", "retained sectors may spoil positivity"),
        ("POS2550_7_no_orbital_GM", "observed orbital GM is not used to fill denominator", "GUARDRAIL_PASS_ORBITAL_GM_REJECTED", "prevents importing Newton/GR into their own reduction proof"),
    ]
    return [
        {
            **metadata(),
            "audit_id": audit_id,
            "required_condition": required,
            "current_fill": current,
            "why_required": why,
            "status": "GUARDRAIL_PASS_NONCLAIM" if current.startswith("GUARDRAIL_PASS") else "BLOCKED_NONCLAIM",
        }
        for audit_id, required, current, why in rows
    ]


def candidate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "candidate_id": "MHD2550_0_Htau_minus_Href_live",
            "quantity": "M_H_ref",
            "definition": "G_ref^-1*(H_tau[S_outer]-H_ref)",
            "required_inputs": "H_tau;H_ref;G_ref;tau_id;coframe_id;surface_outer;reference_rule;units;source_path;equation_ref",
            "current_value": "MISSING_H_TAU_AND_H_REF",
            "units": "MISSING_UNITS",
            "same_frame": "false",
            "positive": "false",
            "valid_for_claim": "false",
            "blockers": "MISSING_THETA_QTAU;MISSING_INTEGRABILITY;MISSING_FIXED_REFERENCE;MISSING_TAU_COFRAME_LOCK;MISSING_POSITIVITY",
        },
        {
            "candidate_id": "MHD2550_1_surface_charge_live",
            "quantity": "M_H_ref",
            "definition": "G_ref^-1*int_S Q_tau^MTS with fixed reference subtraction",
            "required_inputs": "Q_tau^MTS;surface_class;fixed_reference;boundary_flux;G_ref;units;source_path;equation_ref",
            "current_value": "MISSING_Q_TAU_MTS_AND_REFERENCE_LOCK",
            "units": "MISSING_UNITS",
            "same_frame": "false",
            "positive": "false",
            "valid_for_claim": "false",
            "blockers": "MISSING_QTAU_TOTAL;MISSING_BOUNDARY_REFERENCE_LOCK;MISSING_EXTRA_SECTOR_CHARGE_BOUND",
        },
        {
            "candidate_id": "MHD2550_2_worldtube_source_charge_live",
            "quantity": "M_H_ref",
            "definition": "G_ref^-1*int_{W_source} J_H[tau] plus fixed boundary terms",
            "required_inputs": "J_H;tau_id;e_obs;W_source;surface_link;fixed_boundary_terms;G_ref;units;source_path",
            "current_value": "MISSING_SOURCE_MEASURE_BRIDGE",
            "units": "MISSING_UNITS",
            "same_frame": "false",
            "positive": "false",
            "valid_for_claim": "false",
            "blockers": "MISSING_PARENT_WORLDTUBE_SELECTOR;MISSING_SOURCE_MEASURE_EQUALITY;MISSING_TAU_LOCK",
        },
        {
            "candidate_id": "MHD2550_3_orbital_GM_substitution",
            "quantity": "GM_orbit/G_ref",
            "definition": "observed orbital mass readout",
            "required_inputs": "not allowed before Newton/GR derivation",
            "current_value": "REJECTED",
            "units": "mass",
            "same_frame": "false",
            "positive": "unknown",
            "valid_for_claim": "false",
            "blockers": "ORBITAL_GM_SUBSTITUTION_REJECTED_AS_CIRCULAR",
        },
    ]
    return [{**metadata(), **row, "claim_allowed": "false"} for row in rows]


def local_block_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "block_id": "LBS2550_0_finite_Delta_ref_scoring",
            "scored_object": "Delta_ref_boundary_leak_over_M_H_ref",
            "required_before_reopen": "valid positive same-frame M_H_ref plus sourced metric/tau/counterterm/topology leak values",
            "current_status": "BLOCKED_DENOMINATOR_MISSING",
            "effect": "RUN2549_live remains NOT_COMPUTED",
            "claim_allowed": "false",
        },
        {
            "block_id": "LBS2550_1_zero_reference_route",
            "scored_object": "D_a Delta_ref=0",
            "required_before_reopen": "one parent action signs fixed reference, tau/coframe, boundary, denominator and positivity clauses",
            "current_status": "CLOSURE_ONLY_FOR_CURRENT_MTS",
            "effect": "cannot substitute for finite denominator",
            "claim_allowed": "false",
        },
        {
            "block_id": "LBS2550_2_local_GR_PPN",
            "scored_object": "local GR/Newton/PPN branch",
            "required_before_reopen": "denominator plus finite residual values below local bounds, or a parent theorem-zero route",
            "current_status": "BLOCKED",
            "effect": "no local-GR pass from 2550",
            "claim_allowed": "false",
        },
    ]
    return [{**metadata(), **row, "valid_for_claim": "false"} for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2550_0_contract_written", "Exact sufficient contract for positive same-frame Hamiltonian denominator is written.", "PASS_AS_CONTRACT", "HDC2550 lists charge, extraction, integrability, same-frame, reference, source and positivity clauses", "true", "false"),
        ("GATE2550_1_parent_charge_extracted", "Current corpus extracts theta_MTS/Q_tau^MTS and H_tau.", "BLOCKED", "1008/1009 keep parent current-chain extraction nonclaim", "false", "false"),
        ("GATE2550_2_positive_same_frame_denominator", "M_H_ref/N_E is positive and same-frame for current MTS.", "BLOCKED", "integrability, fixed reference, tau/coframe lock, worldtube bridge and positivity theorem are missing", "false", "false"),
        ("GATE2550_3_orbital_GM", "Orbital GM may fill M_H_ref.", "REFUSED", "it is a circular readout import for a Newton/GR reduction proof", "true", "false"),
        ("GATE2550_4_local_bound_scoring", "Finite Delta_ref local bound scoring may proceed.", "BLOCKED", "no valid denominator exists", "false", "false"),
        ("GATE2550_5_local_GR", "Local GR/Newton/PPN branch passes.", "BLOCKED", "denominator and local residual values remain nonclaim", "false", "false"),
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
            "decision_id": "DEC2550_0_exact_but_unsigned",
            "decision": "Keep the Hamiltonian denominator theorem as an exact contract, not a current claim.",
            "reason": "the contract is mathematically sharp but the corpus lacks theta/Q_tau extraction, integrability and positivity",
            "effect": "M_H_ref remains blocked for live scoring",
        },
        {
            "decision_id": "DEC2550_1_local_bound_block_retained",
            "decision": "Retain the local finite-bound scoring block.",
            "reason": "without a denominator, any numerical residual would be normalization theater",
            "effect": "RUN2549_live remains the correct refusal behavior",
        },
        {
            "decision_id": "DEC2550_2_no_orbital_shortcut",
            "decision": "Continue refusing orbital GM, fitted mass, or reference-only normalization.",
            "reason": "the theory must derive Newton/GR rather than importing their readout",
            "effect": "future denominator rows must be Hamiltonian/source-charge rows",
        },
        {
            "decision_id": "DEC2550_3_next_target",
            "decision": "Attack parent Hamiltonian charge extraction and positivity together.",
            "reason": "a positive M_H_ref needs both a real Q_tau and a positivity/source-worldtube bridge",
            "effect": "2551 should build the minimal charge-extraction/positivity source pack or keep denominator blocked",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **metadata(),
            "route_id": "NEXT2550_0_selected",
            "selection_status": "selected",
            "target_file": "2551-Y5-R2FR-parent-Hamiltonian-charge-extraction-positivity-pack-or-denominator-block.md",
            "target_script": "scripts/Y5_R2FR_parent_Hamiltonian_charge_extraction_positivity_pack_or_denominator_block_2551.py",
            "task": "try to assemble a parent-source pack for theta_MTS/Q_tau^MTS, fixed H_ref, tau/coframe lock, worldtube source bridge and positivity; otherwise keep denominator/local scoring blocked",
            "acceptance_target": "one coherent charge-extraction and positivity pack with source paths, or explicit denominator block ledger for all local residual scoring",
            "guardrails": "no EH-only import; no orbital-GM denominator; no fitted reference; no reference-only zero; no local-GR claim; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue_contract", OUTPUTS["denominator_contract"], COPY_TARGETS["queue_contract"]),
        ("queue_local_block", OUTPUTS["local_block"], COPY_TARGETS["queue_local_block"]),
        ("hamiltonian_candidates", OUTPUTS["candidate_rows"], COPY_TARGETS["hamiltonian_candidates"]),
        ("local_bound_block", OUTPUTS["local_block"], COPY_TARGETS["local_bound_block"]),
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
    return list(FORMALIZATION.rglob("*2550*"))


def validation_rows(
    source_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    candidate_rows_value: list[dict[str, Any]],
    block_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail})

    add("VAL2550_00_sources_exist", all(row["source_pass"] == "true" for row in source_rows), "all cited source paths exist and needles are present", ";".join(row["source_id"] for row in source_rows if row["source_pass"] != "true"))
    add("VAL2550_01_contract_written", len(contract_rows) >= 8 and any(row["contract_id"] == "HDC2550_7_current_verdict" for row in contract_rows), "same-frame Hamiltonian denominator contract is complete")
    add("VAL2550_02_contract_not_promoted", any(row["current_status"] == "FAIL_CURRENT_CLAIM_BUT_EXACT_CONTRACT_WRITTEN" for row in contract_rows), "contract is explicitly not promoted to current theorem")
    add("VAL2550_03_positivity_audit_blocks", len(audit_rows) >= 8 and all(row["status"] in {"BLOCKED_NONCLAIM", "GUARDRAIL_PASS_NONCLAIM"} for row in audit_rows), "positivity/same-frame audit keeps blockers explicit")
    add("VAL2550_04_candidate_rows_nonclaim", len(candidate_rows_value) >= 4 and all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in candidate_rows_value), "denominator candidates remain nonclaim")
    add("VAL2550_05_local_scoring_blocked", len(block_rows) >= 3 and all(row["claim_allowed"] == "false" for row in block_rows), "local finite-bound scoring remains blocked")
    add("VAL2550_06_claim_gates_safe", all(row["claim_allowed"] == "false" for row in gate_rows) and any(row["gate_id"] == "GATE2550_5_local_GR" and row["gate_status"] == "BLOCKED" for row in gate_rows), "local-GR/PPN/Newton claims remain blocked")
    add("VAL2550_07_next_target_written", len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2550_0_selected", "2551 parent Hamiltonian charge extraction/positivity target selected")
    add("VAL2550_08_branch_copies", len(branch_rows) == 4 and all(row["target_exists"] == "true" for row in branch_rows), "nonclaim branch copies exist")
    add("VAL2550_09_no_formalization_artifacts", not formalization_hits(), "no 2550 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_hits()))
    add("VAL2550_10_all_outputs_inside_post_checkpoint", all(inside_root(path) for path in list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]), "all 2550 outputs stay inside post-checkpoint-work")
    add("VAL2550_11_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent after cleanup")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2550_CSV_{path.stem}", ok, f"CSV parses with {count} rows" if ok else "CSV parse failed", detail or str(path))

    for key, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2550_COPY_CSV_{key}", ok, f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed", detail or str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2550_OVERALL", overall, "2550 writes exact Hamiltonian denominator contract and retains local scoring block because denominator is unsigned")
    return [{**metadata(), **row} for row in rows]


def write_doc(
    sources: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    blocks: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = "\n\n".join(
        [
            "# 2550 Y5 R2FR Same-frame Hamiltonian Denominator Derivation Or Retain Local Bound Block",
            "**Result:** exact denominator contract reinstalled on the active 2549 chain, but not promoted. A positive same-frame `M_H_ref/N_E` would require parent charge extraction, Hamiltonian integrability, fixed reference, tau/coframe lock, source-worldtube bridge and positivity. Current MTS does not yet sign those clauses, so finite local `Delta_ref` scoring remains blocked.",
            "**Private reading:** this is not a defeat; it is the correct choke point. The local-GR route is now blocked for one clear reason instead of a fog of many reasons: the normalization denominator must be derived from the parent Hamiltonian/source charge. Orbital `GM` remains refused because it would smuggle the Newtonian answer into the derivation.",
            "## Source Register\n" + table(["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"], sources),
            "## Hamiltonian Denominator Contract\n" + table(["contract_id", "clause", "formula", "must_be_signed_by", "current_status"], contract_rows),
            "## Positivity And Same-frame Audit\n" + table(["audit_id", "required_condition", "current_fill", "why_required", "status"], audit_rows),
            "## Denominator Candidate Rows\n" + table(["candidate_id", "quantity", "definition", "required_inputs", "current_value", "units", "same_frame", "positive", "valid_for_claim", "blockers"], candidates),
            "## Local Bound Scoring Block\n" + table(["block_id", "scored_object", "required_before_reopen", "current_status", "effect", "claim_allowed"], blocks),
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
    contract_rows = denominator_contract_rows()
    audit_rows = positivity_audit_rows()
    candidates = candidate_rows()
    blocks = local_block_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["denominator_contract"], contract_rows)
    write_csv(OUTPUTS["positivity_audit"], audit_rows)
    write_csv(OUTPUTS["candidate_rows"], candidates)
    write_csv(OUTPUTS["local_block"], blocks)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(sources, contract_rows, audit_rows, candidates, blocks, gates, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, contract_rows, audit_rows, candidates, blocks, gates, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
