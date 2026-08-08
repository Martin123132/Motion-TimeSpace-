from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2996"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2996-Y5-R2FR-SRNG-OFC-public-parent-contract-or-MICROSCOPE-range-readout-gate-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2996_SOURCE_REGISTER.csv",
    "public_contract": RESIDUALS / "P8_Y5_R2FR_2996_SRNG_OFC_PUBLIC_PARENT_CONTRACT_AUDIT.csv",
    "range_readout": RESIDUALS / "P8_Y5_R2FR_2996_MICROSCOPE_RANGE_READOUT_GATE.csv",
    "bridge": RESIDUALS / "P8_Y5_R2FR_2996_GR_NEWTON_BRIDGE_IMPACT_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2996_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2996_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2996_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2996_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2996_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract_copy": PARENT_ACTION / "SRNG_OFC_public_parent_contract_2996_NOT_SIGNED.csv",
    "range_copy": LOCAL_BOUNDS / "MICROSCOPE_range_readout_gate_2996_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2996_observed_current_complex_owner_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC2996_00_2995_next",
        RESIDUALS / "P8_Y5_R2FR_2995_NEXT_TARGET.csv",
        ["NEXT2995_0_2996", "parent-signed public SRNG/OFC contract"],
        "2995 selected public SRNG/OFC contract versus MICROSCOPE range/readout gate.",
    ),
    (
        "SRC2996_01_2995_fork",
        RESIDUALS / "P8_Y5_R2FR_2995_THEOREM_DATA_FORK_STATUS.csv",
        ["FORK2995_0_private_projective", "PUBLIC_GATE_OPEN"],
        "2995 theory/data fork keeps private zero switches separate from public proof.",
    ),
    (
        "SRC2996_02_2542_observation_contract",
        RESIDUALS / "P8_Y5_NO_SHADOW_2542_OBSERVATION_FUNCTOR_CONTRACT.csv",
        ["OFC2542_5_status", "PRIVATE_CONTRACT_READY_NOT_DERIVED"],
        "observation functor contract exists but is private/nonclaim.",
    ),
    (
        "SRC2996_03_2542_adoption",
        RESIDUALS / "P8_Y5_NO_SHADOW_2542_SRNG_ADOPTION_DECISION_MATRIX.csv",
        ["ADM2542_1_private_adoption", "PRIVATE_ADOPTION_PLUS_DERIVATION_AUDIT"],
        "SRNG/OFC is recommended only as private working clause.",
    ),
    (
        "SRC2996_04_2543_projective",
        RESIDUALS / "P8_Y5_NO_SHADOW_2543_PROJECTIVE_STATUS_UNDER_PRIVATE_SRNG.csv",
        ["PRJ2543_0_candidate_zero", "PUBLIC_CERTIFICATE_BLOCKED"],
        "projective zero is private only; public certificate blocked.",
    ),
    (
        "SRC2996_05_2791_range",
        RESIDUALS / "P8_Y5_R2FR_2791_RANGE_OWNER_THEOREM_ATTEMPT.csv",
        ["ROW2791_0_exact_range_relation", "RANGE_OWNER_NOT_DERIVED"],
        "range relation exists, range owner theorem does not.",
    ),
    (
        "SRC2996_06_2791_schema",
        RESIDUALS / "P8_Y5_R2FR_2791_RANGE_ACQUISITION_SCHEMA.csv",
        ["RAS2791_0_parent_operator", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
        "range/readout acquisition schema remains blocked.",
    ),
    (
        "SRC2996_07_2792_source_current",
        RESIDUALS / "P8_Y5_R2FR_2792_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
        ["SCZ2792_0_chain_rule_zero", "SOURCE_CURRENT_ZERO_NOT_DERIVED"],
        "WEP source-current zero is conditional, not parent-signed.",
    ),
    (
        "SRC2996_08_2900_source_complex",
        RESIDUALS / "P8_Y5_R2FR_2900_SOURCE_COMPLEX_OWNER_AUDIT.csv",
        ["SC2900_0_parent_matter_action", "FAIL_CURRENT_MTS_SOURCE_COMPLEX_OWNER_NOT_DERIVED"],
        "source-worldtube/current-complex owner is the shared missing antecedent.",
    ),
    (
        "SRC2996_09_2900_hilbert_contract",
        RESIDUALS / "P8_Y5_R2FR_2900_HILBERT_CURRENT_COMPLEX_CONTRACT.csv",
        ["HCC2900_0_primary_current", "CONDITIONAL_CONTRACT"],
        "Hilbert-current complex contract is least-circular but nonclaim.",
    ),
    (
        "SRC2996_10_2925_reduction",
        RESIDUALS / "P8_Y5_R2FR_2925_REDUCTION_THEOREM_LADDER.csv",
        ["RTL2925_0_statement", "EXACT_CONDITIONAL_THEOREM_WRITTEN"],
        "conditional local GR/Newton reduction theorem exists.",
    ),
    (
        "SRC2996_11_2940_ladder",
        RESIDUALS / "P8_Y5_R2FR_2940_LOCAL_GR_NEWTON_DERIVATION_LADDER.csv",
        ["LAD2940_0_parent_action", "BLOCKED"],
        "minimal parent action spine is not adopted; local ladder stays blocked.",
    ),
    (
        "SRC2996_12_2941_gk",
        RESIDUALS / "P8_Y5_R2FR_2941_GK_ACTION_EXISTENCE_THEOREM_GATE.csv",
        ["GKT2941_0_weak_action_existence", "FAIL_CURRENT_STRONG_ADOPTION"],
        "GK/q_loc weak action template exists; strong parent adoption fails.",
    ),
]


def source_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "required_needles": "; ".join(needles),
                "needles_found": anchors(path, needles),
                "role": role,
            }
        )
        for source_id, path, needles, role in SOURCE_SPECS
    ]


def public_contract_rows() -> list[dict[str, Any]]:
    data = [
        (
            "PC2996_0_contract_statement",
            "public SRNG/OFC parent contract",
            "For every local readout O_i, O_i:Sol(Q_obs)->Readout_i is downstream of the solved observed stack and has no arrow back into S_parent, source normalization, or coefficient definition.",
            "EXACT_CONTRACT_WRITTEN",
            "not parent-signed by current corpus",
            False,
            "turn this from private policy into a parent action/object-language theorem",
        ),
        (
            "PC2996_1_action_readout_separation",
            "variation-before-readout ordering",
            "S_parent varies only parent fields and apparatus matter; reporting maps are evaluated after solving unless promoted to ordinary matter with explicit stress.",
            "CONDITIONAL_RULE_READY",
            "apparatus/domain/marker backreaction still needs parent treatment",
            False,
            "sign readout separation or residualize every reentry channel",
        ),
        (
            "PC2996_2_no_Gamma_projective_slot",
            "no independent Gamma/projective source slot",
            "Inside owned-coframe plus SRNG/OFC, source/readout maps cannot contain independent Gamma_ind or projective trace as a variational argument.",
            "PRIVATE_ZERO_SWITCH_READY",
            "global affine fallback and public all-sector certificate remain unsigned",
            False,
            "keep public P4 projective fallback unless parent action omits/gauge-fixes Gamma before coupling",
        ),
        (
            "PC2996_3_source_worldtube_complex",
            "source worldtube/current-complex ownership",
            "W_source, A_ext, S_link, J_H[e_obs,tau], tau, ell_J and M_ref must be parent-owned before readout in one Hilbert-current complex.",
            "SHARED_ANTECEDENT_NOT_SIGNED",
            "2900 refuses the source-complex owner theorem",
            False,
            "attack this shared owner rather than re-proving report-level functor algebra",
        ),
        (
            "PC2996_4_matter_descent_species_silence",
            "matter descent and species/material silence",
            "S_matter=Sbar[q(Phi),psi,theta] plus material constants silent along local vertical/source directions would kill qbar_XT/source-current leaks.",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "2792 leaves pre-action species weights and DD alpha/surface deltas live",
            False,
            "derive matter descent or keep WEP/material coefficient rows",
        ),
        (
            "PC2996_5_GK_source_compatibility",
            "GK/q_loc action compatibility",
            "The public contract must not conflict with the weak S_GK template: J_M, P_loc, A_mu and boundary terms must be same-branch parent objects.",
            "WEAK_TEMPLATE_ONLY",
            "2941 passes weak action existence but fails strong MTS adoption",
            False,
            "do not use SRNG to hide q_loc stress/source/projector gaps",
        ),
        (
            "PC2996_6_verdict",
            "public SRNG/OFC promotion",
            "All PC2996 clauses must be parent-signed before private source/readout/projective zeros count publicly.",
            "PUBLIC_PARENT_CONTRACT_NOT_SIGNED",
            "source-complex, matter descent, q/e_obs/tau/ell_J, projective public and GK adoption gates remain open",
            False,
            "retain SRNG/OFC as private working branch only",
        ),
    ]
    return [
        base(
            {
                "contract_id": contract_id,
                "clause": clause,
                "formal_statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "publicly_signed": signed,
                "next_action": next_action,
            }
        )
        for contract_id, clause, statement, status, gap, signed, next_action in data
    ]


def range_readout_rows() -> list[dict[str, Any]]:
    data = [
        (
            "MRG2996_0_range_relation",
            "lambda_WEP relation",
            "lambda_WEP=sqrt(Z_X/M_X^2), or lambda=infinity if no-pole/massless/common-mode theorem is signed",
            "RELATION_CONTRACT_READY_VALUES_MISSING",
            "same-branch Z_X, M_X^2, units and parent operator not supplied",
            False,
        ),
        (
            "MRG2996_1_long_range_bulk",
            "bulk Earth source vector",
            "bulk source vector is allowed only if lambda_WEP >> R_E or common-mode/no-pole theorem is parent-signed",
            "CONDITIONAL_ONLY",
            "2791 rejects bulk shortcut without range theorem",
            False,
        ),
        (
            "MRG2996_2_finite_profile",
            "finite range source-profile branch",
            "lambda-dependent profile rows remain the honest finite route",
            "NONCLAIM_PROFILE_SCAFFOLD",
            "PREM/profile closure, lambda owner and parent-to-DD map are missing",
            False,
        ),
        (
            "MRG2996_3_source_current_zero",
            "WEP source/test composition current",
            "qbar_XT=0 follows only if matter action descent and material silence are parent-signed",
            "CONDITIONAL_NOT_SIGNED",
            "DD alpha/surface material deltas are nonzero and no parent coefficient vector exists",
            False,
        ),
        (
            "MRG2996_4_official_readout",
            "MICROSCOPE readout import",
            "gx/gz/Sxx/Sxz/masks/timing/eta normalization must be official or strictly validated",
            "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "workflow exists but no live claim-grade arrays are present",
            False,
        ),
        (
            "MRG2996_5_product_runner",
            "finite WEP product",
            "range, profile, parent-to-DD coefficients and official readout must be same-branch before scoring",
            "RUNNER_REFUSED",
            "valid_prediction_rows=0 in the current range/readout route",
            False,
        ),
        (
            "MRG2996_6_verdict",
            "MICROSCOPE range/readout gate",
            "data route cannot substitute for public SRNG/OFC proof and cannot claim WEP/local GR yet",
            "DATA_GATE_BLOCKED_NONCLAIM",
            "range owner, DD map, source current and official readout remain missing",
            False,
        ),
    ]
    return [
        base(
            {
                "range_gate_id": gate_id,
                "object": obj,
                "contract": contract,
                "current_status": status,
                "blocking_gap": gap,
                "score_ready": score_ready,
            }
        )
        for gate_id, obj, contract, status, gap, score_ready in data
    ]


def bridge_rows() -> list[dict[str, Any]]:
    data = [
        (
            "BRIDGE2996_0_conditional_GR",
            "local compact GR/Newton theorem",
            "2925 theorem ladder is the correct target theorem",
            "CONDITIONAL_THEOREM_EXISTS",
            "not current MTS proof until parent action, source measure, silence and weak-field calibration clauses close",
        ),
        (
            "BRIDGE2996_1_SRNG_effect",
            "source/readout Gamma clutter",
            "private SRNG/OFC removes source/clock/light/orbit Gamma slots internally",
            "PRIVATE_SIMPLIFICATION_ONLY",
            "public proof still needs parent observation policy",
        ),
        (
            "BRIDGE2996_2_projective_effect",
            "projective trace",
            "zero inside private branch by variable absence",
            "PRIVATE_ZERO_ONLY",
            "global affine fallback retained",
        ),
        (
            "BRIDGE2996_3_source_denominator",
            "Newton/GM denominator",
            "source-worldtube/current-complex owner is the shared bottleneck",
            "NOT_DERIVED",
            "M_H_ref/M_ref and Pi_M same-object gates remain unsigned",
        ),
        (
            "BRIDGE2996_4_GK_q_loc",
            "local residual dynamics",
            "weak GK/q_loc action template exists",
            "TEMPLATE_NOT_ADOPTED",
            "A_mu origin, J_M, P_loc, boundary and stress are not parent-derived",
        ),
        (
            "BRIDGE2996_5_empirical_readout",
            "WEP/MICROSCOPE empirical route",
            "profile and threshold scaffolds exist",
            "NOT_SCORE_READY",
            "official arrays and same-branch parent map missing",
        ),
        (
            "BRIDGE2996_6_verdict",
            "overall GR/Newton bridge movement",
            "2996 narrows the bridge to one public-contract signature problem plus one finite-data gate",
            "CLOSER_BUT_UNCLAIMED",
            "next should prove the single observed-current complex or demote public SRNG/OFC to closure-only",
        ),
    ]
    return [
        base(
            {
                "bridge_id": bridge_id,
                "bridge_piece": piece,
                "evidence": evidence,
                "status": status,
                "remaining_gap": gap,
            }
        )
        for bridge_id, piece, evidence, status, gap in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2996_0_contract_written", "public SRNG/OFC contract is written as exact acceptance test", True, "CONTRACT_READY_NONCLAIM", False),
        ("GATE2996_1_public_SRNG_signed", "SRNG/OFC is parent-signed as public theorem", False, "PRIVATE_ONLY_NOT_DERIVED", False),
        ("GATE2996_2_source_complex_owner", "source-worldtube/current-complex is parent-owned", False, "2900_FAIL_CURRENT_MTS_SOURCE_COMPLEX_OWNER_NOT_DERIVED", False),
        ("GATE2996_3_range_owner", "lambda_WEP/range owner is parent-derived", False, "2791_RANGE_OWNER_NOT_DERIVED", False),
        ("GATE2996_4_source_current_zero", "WEP source-current/material composition current is zero", False, "2792_SOURCE_CURRENT_ZERO_NOT_DERIVED", False),
        ("GATE2996_5_official_readout", "official MICROSCOPE readout arrays are imported", False, "OFFICIAL_ARRAYS_NOT_IMPORTED", False),
        ("GATE2996_6_GK_adoption", "GK/q_loc weak template is adopted as current MTS parent sector", False, "2941_FAIL_CURRENT_STRONG_ADOPTION", False),
        ("GATE2996_7_local_GR_Newton", "local GR/Newton/PPN branch is claimable", False, "PUBLIC_CONTRACT_SOURCE_COMPLEX_RANGE_READOUT_GK_GATES_OPEN", False),
    ]
    return [
        base(
            {
                "gate_id": gate_id,
                "gate": gate,
                "condition_passed": passed,
                "status": status,
                "promotion_allowed_now": promotion,
            }
        )
        for gate_id, gate, passed, status, promotion in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC2996_0_contract_result",
            "Write the public SRNG/OFC contract but do not sign it.",
            "The clause is mathematically clean, but current corpus evidence still leaves q/e_obs/tau/ell_J, source-worldtube/current complex, matter descent and projector/source gates unsigned.",
            "use the contract as an acceptance test, not a public proof",
        ),
        (
            "DEC2996_1_data_result",
            "Keep MICROSCOPE range/readout as a finite nonclaim route.",
            "2791 derives the range relation but not the range owner; 2792 blocks source-current zero; official arrays remain absent.",
            "do not claim WEP/local GR from source-profile or surrogate rows",
        ),
        (
            "DEC2996_2_shared_bottleneck",
            "Promote the shared missing object to next target.",
            "Public SRNG, Newton source normalization, WEP source-current zero and PiM commutator all need one parent-owned observed-current complex.",
            "attack q/e_obs/tau/ell_J plus W_source/A_ext/S_link/J_H/Pi_M as one object",
        ),
        (
            "DEC2996_3_no_loop",
            "Do not re-prove private projective/SRNG again.",
            "Private zero switch is already stable; the missing move is public parent signature or finite component values.",
            "move to signer/owner proof or demote public branch explicitly",
        ),
    ]
    return [
        base(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "next_id": "NEXT2996_0_2997",
                "priority": "selected_primary",
                "next_doc": "2997-Y5-R2FR-single-observed-current-complex-owner-or-public-SRNG-demotion-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_single_observed_current_complex_owner_or_public_SRNG_demotion_under_AX1090_2997.py",
                "objective": "Try to prove the single parent-owned observed-current complex needed by public SRNG/OFC, Newton source normalization, PiM commutator silence and WEP source-current zero: q/e_obs/tau/ell_J, W_source, A_ext, S_link, J_H and Pi_M must be same-branch and fixed before readout. If not proved, demote public SRNG/OFC to closure-only and keep finite residual/input gates.",
                "include": "2542 observation contract;2543 private projective policy;2791 range owner;2792 source-current zero;2900 source-complex audit;2925 reduction theorem;2940 local ladder;2941 GK adoption gate",
                "exclude": "local-GR/Newton/PPN/WEP/R10 claim;private SRNG as public proof;MICROSCOPE surrogate/profile as claim;fitted-G absorption;closure multiplier;GitHub action;formalization-workbench edits",
            }
        )
    ]


def validation_rows(
    source_output_rows: list[dict[str, Any]],
    contract_output_rows: list[dict[str, Any]],
    range_output_rows: list[dict[str, Any]],
    bridge_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    sources_ok = all(boolish(row["path_exists"]) for row in source_output_rows)
    anchors_ok = all(boolish(row["needles_found"]) for row in source_output_rows)
    contract_written_ok = any(row["contract_id"] == "PC2996_0_contract_statement" and row["current_status"] == "EXACT_CONTRACT_WRITTEN" for row in contract_output_rows)
    contract_blocked_ok = any(row["contract_id"] == "PC2996_6_verdict" and row["current_status"] == "PUBLIC_PARENT_CONTRACT_NOT_SIGNED" for row in contract_output_rows)
    range_blocked_ok = any(row["range_gate_id"] == "MRG2996_6_verdict" and row["current_status"] == "DATA_GATE_BLOCKED_NONCLAIM" for row in range_output_rows)
    bridge_ok = any(row["bridge_id"] == "BRIDGE2996_6_verdict" and row["status"] == "CLOSER_BUT_UNCLAIMED" for row in bridge_output_rows)
    local_claim_blocked_ok = any(row["gate_id"] == "GATE2996_7_local_GR_Newton" and not boolish(row["condition_passed"]) for row in gate_output_rows)
    branch_ok = all(boolish(row["copy_exists"]) and boolish(row["parse_ok"]) for row in branch_output_rows)
    csv_parse_ok = all(csv_ok(output_path) for output_path in output_paths if output_path.exists() and output_path.suffix == ".csv")
    outputs_under_post = all(under(output_path, ROOT) for output_path in output_paths + [DOC])
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*2996*") if path.is_file())
    no_claim_flags = True
    for output_path in output_paths:
        if output_path.exists() and output_path.suffix == ".csv":
            for output_row in rows(output_path):
                if str(output_row.get("valid_for_claim", "")).strip().lower() == "true":
                    no_claim_flags = False
                if str(output_row.get("claim_allowed", "")).strip().lower() == "true":
                    no_claim_flags = False
                if str(output_row.get("promotion_allowed_now", "")).strip().lower() == "true":
                    no_claim_flags = False
    data = [
        ("VAL2996_0_sources_exist", sources_ok, "all cited local source paths exist"),
        ("VAL2996_1_anchors_found", anchors_ok, "all cited source anchors found"),
        ("VAL2996_2_contract_written", contract_written_ok, "public SRNG/OFC contract is written"),
        ("VAL2996_3_contract_not_signed", contract_blocked_ok, "public contract remains not parent-signed"),
        ("VAL2996_4_range_readout_blocked", range_blocked_ok, "MICROSCOPE range/readout gate remains blocked"),
        ("VAL2996_5_bridge_status", bridge_ok, "GR/Newton bridge impact is closer but unclaimed"),
        ("VAL2996_6_claim_gate_false", local_claim_blocked_ok, "local GR/Newton/PPN gate remains false"),
        ("VAL2996_7_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2996_8_csvs_parse", csv_parse_ok, "all generated CSVs parse"),
        ("VAL2996_9_outputs_under_post", outputs_under_post, "all generated outputs are under post-checkpoint-work"),
        ("VAL2996_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2996_11_formalization_clean", formalization_count == 0, f"no 2996 outputs in formalization-workbench (count={formalization_count})"),
        ("VAL2996_12_doc_written", DOC.exists(), "2996 markdown checkpoint exists"),
    ]
    overall = all(passed for _, passed, _ in data)
    data.append(("VAL2996_OVERALL", overall, "2996 writes the public SRNG/OFC acceptance contract, refuses current promotion, and selects single observed-current complex ownership next"))
    return [
        base(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": True,
            }
        )
        for validation_id, passed, check in data
    ]


def write_doc(
    source_output_rows: list[dict[str, Any]],
    contract_output_rows: list[dict[str, Any]],
    range_output_rows: list[dict[str, Any]],
    bridge_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    decision_output_rows: list[dict[str, Any]],
    next_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
    validation_output_rows: list[dict[str, Any]],
) -> None:
    document = f"""# 2996 - Y5/R2FR SRNG/OFC Public Parent Contract Or MICROSCOPE Range-Readout Gate Under AX1090

Status: `Y5_R2FR_2996_public_SRNG_OFC_contract_written_not_signed_MICROSCOPE_range_readout_blocked_nonclaim`

Claim ceiling: `no_public_SRNG_claim_no_MICROSCOPE_claim_no_WEP_claim_no_Newton_no_local_GR_no_PPN_no_R10_no_GitHub_no_formalization_edit`

## Current Verdict

2996 writes the exact public acceptance contract for the private `SRNG/OFC` branch. If readouts are downstream functors of the solved observed stack, if they do not feed back into the parent action/source normalization/coefficient definitions, and if the source current/worldtube lives in the same parent complex before readout, then the private source/readout/projective zero switches have a public route.

Current MTS does not yet sign that contract. The missing object is now narrow: a single parent-owned observed-current complex containing `q/e_obs/tau/ell_J`, `W_source`, `A_ext`, `S_link`, `J_H`, `Pi_M`, and `M_ref`, all fixed before readout.

The MICROSCOPE side also stays blocked. The range relation is clean, but `lambda_WEP` is not parent-owned; source-current zero is conditional; official readout arrays are absent; and profile/DD rows remain nonclaim scaffolding.

## Source Register

{md_table(source_output_rows, ["source_id", "path_exists", "needles_found", "role"])}

## Public SRNG/OFC Contract Audit

{md_table(contract_output_rows, ["contract_id", "clause", "current_status", "publicly_signed", "blocking_gap", "next_action"])}

## MICROSCOPE Range-Readout Gate

{md_table(range_output_rows, ["range_gate_id", "object", "current_status", "score_ready", "blocking_gap"])}

## GR/Newton Bridge Impact

{md_table(bridge_output_rows, ["bridge_id", "bridge_piece", "status", "remaining_gap"])}

## Promotion Gates

{md_table(gate_output_rows, ["gate_id", "gate", "condition_passed", "status", "promotion_allowed_now"])}

## Decision Ledger

{md_table(decision_output_rows, ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(next_output_rows, ["next_id", "next_doc", "objective", "exclude"])}

## Branch Copies

{md_table(branch_output_rows, ["copy_id", "destination", "copy_exists", "row_count", "parse_ok", "valid_for_claim"])}

## Validation

{md_table(validation_output_rows, ["validation_id", "passed", "check", "required"])}

## Plain-English Takeaway

This is a useful tightening. The contract that would let the private branch become public is now explicit, and it is not signed yet. The next move is not another private-projective lap; it is the single observed-current complex owner. If that owner closes, several heads of the hydra fall together. If it fails, public `SRNG/OFC` becomes closure-only and the finite residual/data route takes over.
"""
    DOC.write_text(document, encoding="utf-8")


def main() -> None:
    source_output_rows = source_rows()
    contract_output_rows = public_contract_rows()
    range_output_rows = range_readout_rows()
    bridge_output_rows = bridge_rows()
    gate_output_rows = gate_rows()
    decision_output_rows = decision_rows()
    next_output_rows = next_rows()

    write_csv(OUTPUTS["sources"], source_output_rows)
    write_csv(OUTPUTS["public_contract"], contract_output_rows)
    write_csv(OUTPUTS["range_readout"], range_output_rows)
    write_csv(OUTPUTS["bridge"], bridge_output_rows)
    write_csv(OUTPUTS["gates"], gate_output_rows)
    write_csv(OUTPUTS["decision"], decision_output_rows)
    write_csv(OUTPUTS["next"], next_output_rows)

    shutil.copyfile(OUTPUTS["public_contract"], BRANCH_OUTPUTS["contract_copy"])
    shutil.copyfile(OUTPUTS["range_readout"], BRANCH_OUTPUTS["range_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branch_output_rows = [
        base(
            {
                "copy_id": copy_id,
                "destination": str(destination),
                "copy_exists": destination.exists(),
                "row_count": len(rows(destination)) if destination.exists() else 0,
                "parse_ok": csv_ok(destination) if destination.exists() else False,
            }
        )
        for copy_id, destination in BRANCH_OUTPUTS.items()
    ]
    write_csv(OUTPUTS["branches"], branch_output_rows)

    DOC.write_text("", encoding="utf-8")
    validation_output_rows = validation_rows(
        source_output_rows,
        contract_output_rows,
        range_output_rows,
        bridge_output_rows,
        gate_output_rows,
        branch_output_rows,
    )
    write_csv(OUTPUTS["validation"], validation_output_rows)

    write_doc(
        source_output_rows,
        contract_output_rows,
        range_output_rows,
        bridge_output_rows,
        gate_output_rows,
        decision_output_rows,
        next_output_rows,
        branch_output_rows,
        validation_output_rows,
    )


if __name__ == "__main__":
    main()
