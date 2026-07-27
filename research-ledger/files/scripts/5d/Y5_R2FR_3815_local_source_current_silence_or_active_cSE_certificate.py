from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3815"
BRANCH = "MTS_R2FR_Y5_LOCAL_SOURCE_CURRENT_SILENCE_OR_ACTIVE_CSE_CERTIFICATE_3815"
PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3815-Y5-R2FR-local-source-current-silence-or-active-cSE-certificate.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3815_local_source_current_silence_or_active_cSE_certificate.py"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_2444 = PCW / "2444-Y5-R2FR-source-leg-S-Eq-owner-from-parent-current-or-local-product-closure.md"
P_2445 = PCW / "2445-Y5-R2FR-Jq-source-current-extraction-from-parent-L-or-Htau-source-charge-certificate.md"
P_2446 = PCW / "2446-Y5-R2FR-EH-baseline-plus-MTS-residual-current-pack-for-S-Eq.md"
P_2354 = PCW / "2354-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md"
P_2523 = PCW / "2523-Y5-R2FR-readout-projector-memory-reentry-zero-or-Jreadout-bound.md"
P_3691 = PCW / "3691-Y5-R2FR-vertical-q-map-source-current-orthogonality-or-JA-coefficient-acquisition.md"
P_3813 = PCW / "3813-Y5-R2FR-Rbridge-matter-glue-no-source-slot-or-finite-source-normalizer-row.md"
P_3814 = PCW / "3814-Y5-R2FR-source-amplitude-lower-bound-or-worldtube-current-normalization-theorem.md"

CSV_2444_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_2444_SOURCE_LEG_DERIVATION_CONTRACT.csv"
CSV_2444_CURRENT = OUT / "P8_Y5_PARENT_QLOC_2444_PARENT_SOURCE_CURRENT_AUDIT.csv"
CSV_2445_JQ = OUT / "P8_Y5_PARENT_QLOC_2445_JQ_SOURCE_CURRENT_EXTRACTION_ATTEMPT.csv"
CSV_2445_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_2445_SOURCE_CURRENT_CERTIFICATE_SCHEMA.csv"
CSV_2446_PACK = OUT / "P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv"
CSV_2354_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2354_CHAINMAP_ZERO_AUDIT.csv"
CSV_2354_ANTECEDENTS = OUT / "P8_Y5_PARENT_QLOC_2354_CHAINMAP_ANTECEDENT_STATUS.csv"
CSV_2523_AUDIT = OUT / "P8_Y5_NO_SHADOW_2523_READOUT_REENTRY_AUDIT.csv"
CSV_2523_GATE = OUT / "P8_Y5_NO_SHADOW_2523_COMMUTATOR_GATE.csv"
CSV_3691_ORTHO = OUT / "P8_Y5_R2FR_3691_SOURCE_ORTHOGONALITY_ROWS.csv"
CSV_3691_VERTICAL = OUT / "P8_Y5_R2FR_3691_VERTICAL_QMAP_GATE_ROWS.csv"
CSV_3813_CONTRACT = OUT / "P8_Y5_R2FR_3813_MATTER_GLUE_ZERO_THEOREM_CONTRACT.csv"
CSV_3814_BRANCH = OUT / "P8_Y5_R2FR_3814_BRANCH_DECISION_MATRIX.csv"
CSV_3814_POLICY = OUT / "P8_Y5_R2FR_3814_PRODUCT_BOUND_ISOLATION_POLICY.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3815_SOURCE_REGISTER.csv",
    "zero_audit": OUT / "P8_Y5_R2FR_3815_ZERO_SOURCE_SILENCE_THEOREM_AUDIT.csv",
    "chainmap": OUT / "P8_Y5_R2FR_3815_PROJECTED_CURRENT_CHAINMAP_AUDIT.csv",
    "active_cse": OUT / "P8_Y5_R2FR_3815_ACTIVE_CSE_CERTIFICATE_ATTEMPT.csv",
    "branches": OUT / "P8_Y5_R2FR_3815_BRANCH_RUNNER_DECISION.csv",
    "carryforward": OUT / "P8_Y5_R2FR_3815_PRODUCT_POLICY_CARRYFORWARD.csv",
    "gates": OUT / "P8_Y5_R2FR_3815_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3815_DECISION_ROWS.csv",
    "next_target": OUT / "P8_Y5_R2FR_3815_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3815_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3815_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3815_0_2444_doc", P_2444, "S_A^q[x_readout]", "source-leg definition: projected q-current over source normalizer"),
    ("SRC3815_1_2444_contract", CSV_2444_CONTRACT, "SLC2444_2_universal_zero_route", "machine contract for universal source-current zero route"),
    ("SRC3815_2_2444_current", CSV_2444_CURRENT, "PCA2444_1_parent_L", "parent current blockers for S_Eq ownership"),
    ("SRC3815_3_2445_doc", P_2445, "JQX2445_3_qblind_zero_route", "q-blind matter action route"),
    ("SRC3815_4_2445_jq", CSV_2445_JQ, "JQX2445_3_qblind_zero_route", "machine J_q extraction attempt"),
    ("SRC3815_5_2445_schema", CSV_2445_SCHEMA, "SCS2445_3_zero_theorem", "zero theorem schema for source current"),
    ("SRC3815_6_2446_pack", CSV_2446_PACK, "RCS2446_2_projector_domain", "residual-current families that must vanish or be bounded"),
    ("SRC3815_7_2354_doc", P_2354, "source-worldtube/projector chain-map", "worldtube/projector chain-map theorem source"),
    ("SRC3815_8_2354_audit", CSV_2354_AUDIT, "CMA2354_2_fixed_topological_route", "fixed topological projector conditional zero theorem"),
    ("SRC3815_9_2354_antecedents", CSV_2354_ANTECEDENTS, "ANT2354_8_verdict", "chain-map antecedent status"),
    ("SRC3815_10_2523_doc", P_2523, "J_readout=0 theorem", "readout/projector re-entry theorem source"),
    ("SRC3815_11_2523_audit", CSV_2523_AUDIT, "JRZ2523_2_fixed_projector_clause", "fixed projector/readout silence clause"),
    ("SRC3815_12_2523_gate", CSV_2523_GATE, "JRG2523_8_theorem", "readout zero theorem gate"),
    ("SRC3815_13_3691_doc", P_3691, "constraint-first route", "vertical q-map/source-current orthogonality source"),
    ("SRC3815_14_3691_ortho", CSV_3691_ORTHO, "SO3691_6_verdict", "matter/source orthogonality rows"),
    ("SRC3815_15_3691_vertical", CSV_3691_VERTICAL, "VQ3691_5_constraint_first", "vertical generator route"),
    ("SRC3815_16_3813_contract", CSV_3813_CONTRACT, "ZC3813_5_zero_theorem_result", "matter-glue no-source-slot zero theorem contract"),
    ("SRC3815_17_3814_doc", P_3814, "Positive Hilbert/worldtube mass does not imply nonzero q-source amplitude", "3814 no-go for positive mass as source-amplitude lower bound"),
    ("SRC3815_18_3814_branch", CSV_3814_BRANCH, "BR3814_0_zero_source_silence", "3814 source-branch decision matrix"),
    ("SRC3815_19_3814_policy", CSV_3814_POLICY, "MISSING_PARENT_LOWER_BOUND", "3814 product policy carryforward"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "exists": bool_text(exists),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def zero_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    rows = [
        {
            **base,
            "audit_id": "ZST3815_0_target",
            "clause": "local projected source-current silence",
            "formal_condition": "P_arena[G_q J_q^E]=0 before local scoring",
            "proof_attempt": "Use S_E^q=P_arena[G_q J_q^E]/N_E from 2444 and force the numerator to zero rather than lower-bound it.",
            "current_status": "TARGET_DEFINED",
            "blocking_gap": "target needs all descent, projector, readout and residual-current clauses in one parent branch",
            "effect_if_signed": "all local products proportional to S_E^q vanish in the source-silence branch",
        },
        {
            **base,
            "audit_id": "ZST3815_1_qblind_matter_descent",
            "clause": "ordinary matter q-blind descent",
            "formal_condition": "S_matter,E=Sbar_matter[g_obs,psi_E,theta_rep] with no independent q-source slot",
            "proof_attempt": "Then J_q^E=delta S_matter,E/delta q=0 by the chain rule at fixed observed matter data.",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocking_gap": "2445 still marks source-scalar exclusion and matter-spectrum owner conditional",
            "effect_if_signed": "ordinary matter does not source the local q channel",
        },
        {
            **base,
            "audit_id": "ZST3815_2_vertical_orthogonality",
            "clause": "vertical q-map/source orthogonality",
            "formal_condition": "v in ker(Dq) and all observed source/readout/boundary components are q-basic",
            "proof_attempt": "If the parent source current only varies along q-basic data, the vertical contribution to J_A vanishes.",
            "current_status": "MISSING_PARENT_Q_MAP_AND_GENERATOR",
            "blocking_gap": "3691 selects the constraint-first route but does not parent-own q, Omega, boundary charge or Dq[v]=0",
            "effect_if_signed": "hidden vertical motions cannot re-enter the source current",
        },
        {
            **base,
            "audit_id": "ZST3815_3_projector_chainmap",
            "clause": "projected current chain-map silence",
            "formal_condition": "delta Pi_M=0 and [d,Pi_M]J_H=0 on the fixed source worldtube/domain",
            "proof_attempt": "Use the exact product-rule obstruction from 2354: only a fixed topological/chain-map projector kills the commutator.",
            "current_status": "EXACT_CONDITIONAL_CHAINMAP_UNSIGNED",
            "blocking_gap": "parent selector, fixed domain, physical-current complex, exterior silence and tau/M_H_ref remain unsigned",
            "effect_if_signed": "projector/domain selection cannot create a fake source-current residual",
        },
        {
            **base,
            "audit_id": "ZST3815_4_readout_silence",
            "clause": "readout/projector re-entry silence",
            "formal_condition": "R_A is pure postprocessing and Pi_A,W_source,P_loc,e_obs are fixed before variation",
            "proof_attempt": "2523 gives the fixed-projector lemma, so the readout term is zero only for genuine post-solution reporting maps.",
            "current_status": "EXACT_CONDITIONAL_READOUT_UNSIGNED",
            "blocking_gap": "local readouts still include projectors, source worldtubes, material kernels, fitted-source maps or effective maps",
            "effect_if_signed": "readout cannot rebuild a source coefficient after the q-current is zeroed",
        },
        {
            **base,
            "audit_id": "ZST3815_5_matter_glue",
            "clause": "no source-only matter-glue slots",
            "formal_condition": "single action-density line, connected ordinary matter functor, species-blind measure/current and source-label forgetting",
            "proof_attempt": "3813 constructs the exact zero theorem for R_matter_glue and source-only visible leakage.",
            "current_status": "THEOREM_CONSTRUCTED_NOT_PARENT_SIGNED",
            "blocking_gap": "the clauses exist but are not all parent-owned in the strict corpus",
            "effect_if_signed": "source-only spurions cannot survive as composition-dependent local forces",
        },
        {
            **base,
            "audit_id": "ZST3815_6_residual_current_pack",
            "clause": "all MTS residual-current families vanish or are source-bounded",
            "formal_condition": "RCS2446_0 through RCS2446_6 are theorem-zero or finite source-backed rows in the same arena",
            "proof_attempt": "2446 names every residual family that can keep S_E^q alive after the EH/q-blind comparator is zero.",
            "current_status": "OPEN_RESIDUALS_RETAINED",
            "blocking_gap": "boundary, extra non-EH, projector/domain, matter/source glue, coupling, PPN tail and visible-coefficient guards remain open",
            "effect_if_signed": "EH/q-blind comparator silence would extend to the MTS local source branch",
        },
        {
            **base,
            "audit_id": "ZST3815_7_verdict",
            "clause": "source-current silence theorem",
            "formal_condition": "ZST3815_1 through ZST3815_6 pass in one parent branch",
            "proof_attempt": "The implication is exact: J_q^E=0 plus linear fixed projection implies P_arena[G_qJ_q^E]=0.",
            "current_status": "ZERO_SOURCE_SILENCE_NOT_CLAIMED",
            "blocking_gap": "several exact clauses are conditional, but not parent-signed together",
            "effect_if_signed": "local source branch closes by silence rather than by coefficient fitting",
        },
    ]
    return rows


def chainmap_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    return [
        {
            **base,
            "chain_id": "PCM3815_0_algebra",
            "object": "projected q-source numerator",
            "statement": "For fixed linear P_arena and G_q, P_arena[G_q J_q^E]=0 follows immediately from J_q^E=0.",
            "status": "EXACT_LEMMA",
            "residual_if_failed": "none if J_q^E=0; otherwise component residuals below",
            "next_input_needed": "parent-signed J_q^E=0 or component bounds",
        },
        {
            **base,
            "chain_id": "PCM3815_1_kernel_projection_fixedness",
            "object": "G_q, P_arena, local domain",
            "statement": "If G_q, P_arena and the local domain vary with q, the projection of a nominal source can acquire delta G_q, delta P_arena or domain terms.",
            "status": "FIXEDNESS_UNSIGNED",
            "residual_if_failed": "R_projector_domain + J_Ploc_comm + boundary/domain leakage",
            "next_input_needed": "source-backed fixed projection theorem or finite commutator row",
        },
        {
            **base,
            "chain_id": "PCM3815_2_worldtube_selector",
            "object": "source worldtube W_E",
            "statement": "W_E must be selected before readout and fixed under allowed local variations, or side-flux/support drift becomes a source-current residual.",
            "status": "WORLD_TUBE_OWNER_UNSIGNED",
            "residual_if_failed": "E_worldtube + J_worldtube_comm + I_domain",
            "next_input_needed": "parent source support owner, compact support and zero side-flux",
        },
        {
            **base,
            "chain_id": "PCM3815_3_hilbert_equality",
            "object": "Hilbert/source equality",
            "statement": "The measured local source must be the same Hilbert current used in the q variation before material/readout projection.",
            "status": "HILBERT_SOURCE_EQUALITY_UNSIGNED",
            "residual_if_failed": "R_eq + epsilon_nonHilbert_current + epsilon_current_rescaling",
            "next_input_needed": "common Hilbert current owner and no non-Hilbert bypass",
        },
        {
            **base,
            "chain_id": "PCM3815_4_readout_commutator",
            "object": "readout/source projection maps",
            "statement": "delta(Pi_A J)=Pi_A delta J only when delta Pi_A=0; otherwise the readout commutator is a real source coefficient.",
            "status": "COMMUTATOR_OPEN",
            "residual_if_failed": "J_readout + epsilon_source_reentry",
            "next_input_needed": "pure postprocessing proof or finite J_readout component rows",
        },
        {
            **base,
            "chain_id": "PCM3815_5_decision",
            "object": "projected current chain",
            "statement": "The local silence proof is mathematically short but source-rich: it now reduces to signing q-blind matter descent plus fixed projection/readout chain-map.",
            "status": "BEST_NEXT_PROOF_ROUTE_IDENTIFIED",
            "residual_if_failed": "strict product-only rows remain active",
            "next_input_needed": "3816 parent q-blind matter descent/action template or residual q-matter source term",
        },
    ]


def active_cse_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    return [
        {
            **base,
            "cse_id": "CSE3815_0_definition",
            "object": "c_SE",
            "formula": "c_SE := inf_E |P_arena[G_q J_q^E]/N_E| over the scored local source class",
            "requirement": "a positive lower bound in the same arena and normalization used by WEP/R10/PPN/clock/orbit rows",
            "current_status": "DEFINITION_ONLY",
            "why_not_enough": "a definition gives no positivity and does not prevent nodal cancellation",
        },
        {
            **base,
            "cse_id": "CSE3815_1_positive_mass_no_go",
            "object": "M_H or worldtube mass",
            "formula": "M_H>0 does not imply |P_arena[G_qJ_q^E]/N_E|>0",
            "requirement": "q-current amplitude, not merely ordinary source mass",
            "current_status": "EXACT_NO_GO_FROM_3814",
            "why_not_enough": "a positive mass can be completely q-blind",
        },
        {
            **base,
            "cse_id": "CSE3815_2_nonzero_current",
            "object": "J_q^E",
            "formula": "J_q^E not identically zero and sourced by a parent Lagrangian or Hamiltonian charge",
            "requirement": "explicit nonzero current term with source path and units",
            "current_status": "MISSING_PARENT_CURRENT",
            "why_not_enough": "2445 did not extract J_q beyond a contract and EH comparator",
        },
        {
            **base,
            "cse_id": "CSE3815_3_no_cancellation",
            "object": "projected source profile",
            "formula": "P_arena[G_qJ_q^E] has fixed sign or a sourced absolute lower envelope on the source class",
            "requirement": "no-nodal-cancellation theorem or measured/source-backed profile lower bound",
            "current_status": "MISSING_NO_CANCELLATION_CERTIFICATE",
            "why_not_enough": "upper/product envelopes do not give lower bounds",
        },
        {
            **base,
            "cse_id": "CSE3815_4_normalization",
            "object": "N_E",
            "formula": "N_E is positive, parent-owned and identical across the local scored arena",
            "requirement": "same Hamiltonian/source mass convention and no orbital-GM shortcut",
            "current_status": "MISSING_OWNED_N_E",
            "why_not_enough": "normalizing by an observed source mass does not own the q-source amplitude",
        },
        {
            **base,
            "cse_id": "CSE3815_5_verdict",
            "object": "active c_SE certificate",
            "formula": "0 < c_SE <= |S_E^q|",
            "requirement": "CSE3815_2 through CSE3815_4 pass with source paths",
            "current_status": "ACTIVE_CSE_CERTIFICATE_NOT_AVAILABLE",
            "why_not_enough": "the current corpus has no parent-owned positive q-source lower bound",
        },
    ]


def branch_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    return [
        {
            **base,
            "runner_case_id": "BR3815_0_zero_source_branch",
            "condition": "ZST3815_1..6 all parent-signed in one branch",
            "result": "P_arena[G_qJ_q^E]=0 and S_E^q products vanish",
            "current_decision": "CONDITIONAL_EXACT_NOT_PARENT_SIGNED",
            "allowed_use_now": "use as the preferred local-GR derivation route",
            "forbidden_use_now": "claim local-GR/source silence",
        },
        {
            **base,
            "runner_case_id": "BR3815_1_active_cSE_branch",
            "condition": "0<c_SE<=|S_E^q| with nonzero current, no cancellation and owned N_E",
            "result": "3814 products would isolate residual coefficients as B/c_SE",
            "current_decision": "MISSING_ACTIVE_CSE_CERTIFICATE",
            "allowed_use_now": "keep the certificate schema",
            "forbidden_use_now": "divide WEP/R10/PPN products by an assumed source amplitude",
        },
        {
            **base,
            "runner_case_id": "BR3815_2_product_only_default",
            "condition": "zero branch unsigned and active c_SE unsigned",
            "result": "only product bounds abs(S_E^q)*epsilon are controlled",
            "current_decision": "ACTIVE_STRICT_DEFAULT",
            "allowed_use_now": "nonclaim residual discipline and source-product tests",
            "forbidden_use_now": "local-GR, WEP, R10, PPN, clock or orbital pass claim",
        },
        {
            **base,
            "runner_case_id": "BR3815_3_next_proof_jump",
            "condition": "prioritize the smallest signable missing clause",
            "result": "attempt parent q-blind matter descent/action template before more broad audits",
            "current_decision": "MOVE_TO_3816_QBLIND_ACTION_DESCENT",
            "allowed_use_now": "build the parent action clause or its finite residual row",
            "forbidden_use_now": "repeat a generic missing-input ledger",
        },
    ]


def carryforward_rows(timestamp: str) -> list[dict[str, Any]]:
    policies = read_csv(CSV_3814_POLICY)
    rows: list[dict[str, Any]] = []
    for row in policies:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "policy_id": row["policy_id"].replace("ISO3814_", "CF3815_"),
                "source_product_bound_id": row["source_product_bound_id"],
                "symbol": row["symbol"],
                "residual_slot": row["residual_slot"],
                "arena": row["arena"],
                "product_bound": row["product_bound"],
                "product_units": row["product_units"],
                "3815_zero_branch_policy": "if source-current silence is parent-signed, this product is zero but the isolated coefficient is not measured",
                "3815_active_branch_policy": row["isolated_bound_formula_if_cSE_signed"],
                "current_policy": "PRODUCT_ONLY_DEFAULT_CARRIED_FORWARD",
                "c_SE_status": "MISSING_ACTIVE_CSE_CERTIFICATE",
                "zero_source_status": "CONDITIONAL_EXACT_NOT_PARENT_SIGNED",
                "isolation_allowed_now": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    all_sources = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    return [
        {
            **base,
            "gate_id": "GATE3815_0_sources",
            "claim": "all cited source paths exist and source needles are found",
            "gate_status": "PASS_NONCLAIM" if all_sources else "FAIL",
            "reason": "source-backed runner is reproducible" if all_sources else "one or more source paths/needles are missing",
            "gate_pass": bool_text(all_sources),
        },
        {
            **base,
            "gate_id": "GATE3815_1_zero_source_silence_signed",
            "claim": "P_arena[G_qJ_q^E]=0 is parent-signed for local sources",
            "gate_status": "BLOCKED",
            "reason": "q-blind matter, vertical q-map, projector chain-map, readout silence and residual-current closure are not signed together",
            "gate_pass": "false",
        },
        {
            **base,
            "gate_id": "GATE3815_2_active_cSE_available",
            "claim": "0<c_SE<=|S_E^q| is available",
            "gate_status": "BLOCKED",
            "reason": "no nonzero current, no-cancellation theorem or owned N_E lower certificate exists",
            "gate_pass": "false",
        },
        {
            **base,
            "gate_id": "GATE3815_3_product_only_guard",
            "claim": "3814 product-only guard remains active",
            "gate_status": "PASS_NONCLAIM",
            "reason": "all carryforward rows keep isolation_allowed_now=false",
            "gate_pass": "true",
        },
        {
            **base,
            "gate_id": "GATE3815_4_local_claims",
            "claim": "local-GR/WEP/R10/PPN/clock/orbit pass",
            "gate_status": "BLOCKED",
            "reason": "zero-source and active-cSE branches are not claim-ready",
            "gate_pass": "false",
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    return [
        {
            **base,
            "decision_id": "DEC3815_0_keep_zero_route",
            "decision": "keep the source-current silence route as the preferred local-GR path",
            "because": "it would reduce local extra forces by theorem rather than by fitting small coefficients",
            "next_action": "try to parent-sign q-blind ordinary matter descent in 3816",
        },
        {
            **base,
            "decision_id": "DEC3815_1_refuse_active_shortcut",
            "decision": "do not create a positive c_SE from source mass or normalization convention",
            "because": "3814 proves positive ordinary mass does not imply positive q-current amplitude",
            "next_action": "only reopen active c_SE with a real nonzero current/no-cancellation certificate",
        },
        {
            **base,
            "decision_id": "DEC3815_2_carry_products",
            "decision": "carry every 3814 product policy forward unchanged",
            "because": "strict current evidence controls products, not isolated residual coefficients",
            "next_action": "keep product rows as nonclaim empirical discipline while deriving the parent action route",
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3816-Y5-R2FR-parent-qblind-matter-descent-action-template-or-finite-qmatter-source-row.md",
            "target_script": "scripts/Y5_R2FR_3816_parent_qblind_matter_descent_action_template_or_finite_qmatter_source_row.py",
            "objective": "Do the smallest real derivation jump: write the parent action clause under which ordinary matter depends on q only through observed metric/coframe/representation data, prove J_q^ordinary=0 by chain rule, or emit a finite q-matter source residual row C_qmatter with arena units.",
            "success_gate": "Either a parent-owned q-blind matter descent theorem is signed for ordinary local sources, or every failed clause is converted into a finite source-current row rather than another broad missing-input note.",
            "avoid": "do not re-audit all local tests; do not use positive mass as c_SE; do not claim local GR; do not edit formalization-workbench; do not use GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_ZERO_SOURCE_THEOREM_CONTRACT_AND_ACTIVE_CSE_REFUSAL_RUNNER_BUILT",
            "summary": "3815 converts the 3814 branch split into an executable local source-current runner: the zero-source route is an exact conditional theorem, the active c_SE route is blocked unless a nonzero current/no-cancellation/owned-normalizer certificate exists, and all 3814 product policies remain product-only. The next real derivation target is q-blind ordinary matter descent or a finite q-matter source residual row.",
            "valid_for_claim": "false",
        }
    ]


def write_markdown(grouped: dict[str, list[dict[str, Any]]]) -> None:
    status = grouped["status"][0]
    validation = grouped.get("validation", [])
    validation_pass = all(row.get("result") == "PASS" for row in validation) if validation else False
    carry_count = len(grouped["carryforward"])
    text = f"""# 3815 - Local Source-Current Silence Or Active c_SE Certificate

## Status

- Status: `{status["status"]}`
- Claim level: private, nonclaim, source-backed theorem runner.
- Validation pass: `{bool_text(validation_pass)}`
- Carried product policies: `{carry_count}` rows from 3814, all still `isolation_allowed_now=false`.

## What Was Actually Proved

The useful theorem is short:

```text
S_E^q[x] = P_arena[ G_q(x,y) J_q^E(y) dmu_y ] / N_E
J_q^E = delta S_matter,E / delta q

If J_q^E=0 and P_arena,G_q,N_E are fixed linear local objects,
then P_arena[G_q J_q^E]=0 and S_E^q=0.
```

That is the clean local-GR branch. It does not require inventing a small coupling; it makes the local q-source silent. The catch is that the clauses needed to sign `J_q^E=0` and fixed projection are still conditional in the current corpus.

## Zero-Source Silence Audit

| Clause | Current status | Blocking gap |
|---|---|---|
| q-blind ordinary matter descent | `EXACT_CONDITIONAL_NOT_PARENT_SIGNED` | source-scalar exclusion and matter-spectrum owner remain conditional |
| vertical q-map/source orthogonality | `MISSING_PARENT_Q_MAP_AND_GENERATOR` | q, Omega, boundary charge and `Dq[v]=0` not owned together |
| projector chain-map silence | `EXACT_CONDITIONAL_CHAINMAP_UNSIGNED` | parent selector, fixed domain, chain-map complex and exterior silence unsigned |
| readout silence | `EXACT_CONDITIONAL_READOUT_UNSIGNED` | local readouts can still include projectors/worldtubes/material kernels/effective maps |
| matter-glue source slots | `THEOREM_CONSTRUCTED_NOT_PARENT_SIGNED` | exact 3813 contract exists but is not strict-parent signed |
| residual-current pack | `OPEN_RESIDUALS_RETAINED` | 2446 residual families still need zero or finite rows |

## Active c_SE Attempt

Define

```text
c_SE := inf_E |P_arena[G_q J_q^E] / N_E|
```

The active branch fails as a claim because the corpus does not provide:

- a parent-owned nonzero `J_q^E`;
- a no-nodal-cancellation/lower-envelope theorem;
- an owned positive `N_E` in the same arena;
- a shared projection/kernel certificate.

3814 already blocks the tempting shortcut: positive Hilbert/worldtube mass is not a lower bound on `abs(S_E^q)`. A massive source may simply be q-blind.

## Branch Decision

| Branch | Decision now | Meaning |
|---|---|---|
| Zero-source branch | conditional exact, not claimed | best local-GR route if parent action descent closes |
| Active `c_SE` branch | blocked | cannot isolate coefficients without a real lower certificate |
| Product-only branch | active strict default | WEP/R10/PPN/clock/orbit rows remain nonclaim product constraints |

## Next Target

`3816-Y5-R2FR-parent-qblind-matter-descent-action-template-or-finite-qmatter-source-row.md`

The next move is not another broad sweep. It is the smallest hard derivation jump: write the parent action clause under which ordinary matter depends on `q` only through observed metric/coframe/representation data, prove `J_q^ordinary=0` by chain rule, or emit a finite `C_qmatter` source-current residual row with units.

## Machine Outputs

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3815_SOURCE_REGISTER.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3815_ZERO_SOURCE_SILENCE_THEOREM_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3815_PROJECTED_CURRENT_CHAINMAP_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3815_ACTIVE_CSE_CERTIFICATE_ATTEMPT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3815_BRANCH_RUNNER_DECISION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3815_PRODUCT_POLICY_CARRYFORWARD.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3815_CLAIM_GATES.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3815_DECISION_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3815_NEXT_TARGET.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3815_STATUS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3815_VALIDATION.csv`
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace(
        "# Local GR Coupling Spine - Current State After 3814",
        "# Local GR Coupling Spine - Current State After 3815",
    )
    new_para = (
        "`3815` converts the source-amplitude fork into a local source-current runner. The clean route is now exact but conditional: if ordinary matter is q-blind before readout, the q-current `J_q^E` vanishes, and fixed linear projection gives `P_arena[G_qJ_q^E]=0`. The active-positive route is refused unless a real `0<c_SE<=abs(S_E^q)` certificate supplies nonzero current, no nodal cancellation and owned `N_E`; positive mass alone is explicitly not enough. Therefore the strict current branch remains product-only, and the next derivation jump is parent q-blind matter descent or a finite q-matter source row.\n"
    )
    if "`3815` converts the source-amplitude fork" not in text:
        anchor = (
            "`3814` resolves the source-amplitude isolation fork. Positive Hilbert/worldtube mass is not a lower bound on `abs(S_E^q)`: a source can have positive mass while the q-current or projected q-derivative is zero. The local branch is now split into source-current silence, active-positive `c_SE`, and product-only cases. Source silence can support local-GR/fifth-force suppression but does not bound residual coefficients; active coefficient isolation requires a parent-owned `c_SE <= abs(S_E^q)` certificate; the current corpus remains product-only with explicit isolation policies for every 3813 row.\n"
        )
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + new_para)
        else:
            text += "\n" + new_para

    history_entry = (
        "- `3815-Y5-R2FR-local-source-current-silence-or-active-cSE-certificate.md`: turns the 3814 branch split into a theorem runner, keeps source-current silence as the clean local-GR route, rejects active `c_SE` without a real current/no-cancellation certificate, and selects q-blind matter descent as the next derivation target."
    )
    if history_entry not in text:
        marker = "## Next Target"
        if marker in text:
            text = text.replace(marker, history_entry + "\n\n" + marker, 1)
        else:
            text += "\n" + history_entry + "\n"

    old_target = (
        "`3815-Y5-R2FR-local-source-current-silence-or-active-cSE-certificate.md`\n\n"
        "Target: try the local-GR route first by proving `P_arena[G_q J_q^E]=0` for the local source branch from parent current descent, projector silence, and readout silence. If that fails, attempt an active positive `c_SE` certificate with no-nodal-cancellation and owned `N_E`.\n\n"
        "This is the best next move because 3814 shows positive source mass cannot isolate products. The theory must now choose cleanly between q-source silence, active source amplitude, or honest product-only residuals."
    )
    new_target = (
        "`3816-Y5-R2FR-parent-qblind-matter-descent-action-template-or-finite-qmatter-source-row.md`\n\n"
        "Target: do the smallest real derivation jump exposed by 3815. Write the parent action clause under which ordinary matter depends on `q` only through observed metric/coframe/representation data, prove `J_q^ordinary=0` by chain rule, or emit a finite `C_qmatter` source-current residual row with arena units.\n\n"
        "This is the best next move because local-GR source silence now reduces to one signable parent-action question rather than another broad residual sweep."
    )
    if old_target in text:
        text = text.replace(old_target, new_target)

    artifacts = [
        "P8_Y5_R2FR_3815_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_3815_ZERO_SOURCE_SILENCE_THEOREM_AUDIT.csv",
        "P8_Y5_R2FR_3815_PROJECTED_CURRENT_CHAINMAP_AUDIT.csv",
        "P8_Y5_R2FR_3815_ACTIVE_CSE_CERTIFICATE_ATTEMPT.csv",
        "P8_Y5_R2FR_3815_BRANCH_RUNNER_DECISION.csv",
        "P8_Y5_R2FR_3815_PRODUCT_POLICY_CARRYFORWARD.csv",
        "P8_Y5_R2FR_3815_CLAIM_GATES.csv",
        "P8_Y5_R2FR_3815_DECISION_ROWS.csv",
        "P8_Y5_R2FR_3815_NEXT_TARGET.csv",
        "P8_Y5_R2FR_3815_STATUS.csv",
        "P8_Y5_BRR545_3815_VALIDATION.csv",
    ]
    for artifact in artifacts:
        entry = f"- `source-intake\\mts_residuals\\{artifact}`"
        if entry not in text:
            text = text.rstrip() + "\n" + entry + "\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache() -> None:
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            read_csv(path)
    fwb_hits = list(FWB.rglob("*3815*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH, SPINE_PATH] if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3815 markdown document written"),
        ("zero_theorem_not_claimed", any(row["audit_id"] == "ZST3815_7_verdict" and row["current_status"] == "ZERO_SOURCE_SILENCE_NOT_CLAIMED" for row in grouped["zero_audit"]), "zero source theorem remains conditional"),
        ("active_cse_blocked", any(row["cse_id"] == "CSE3815_5_verdict" and row["current_status"] == "ACTIVE_CSE_CERTIFICATE_NOT_AVAILABLE" for row in grouped["active_cse"]), "active c_SE certificate is refused"),
        ("product_policy_carried", len(grouped["carryforward"]) == 12 and all(row["isolation_allowed_now"] == "false" for row in grouped["carryforward"]), "all 3814 product policies carried without isolation"),
        ("branch_default_product_only", any(row["runner_case_id"] == "BR3815_2_product_only_default" and row["current_decision"] == "ACTIVE_STRICT_DEFAULT" for row in grouped["branches"]), "strict product-only default remains active"),
        ("claim_gates_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("next_target_selected", grouped["next_target"][0]["target_doc"].startswith("3816-Y5-R2FR-parent-qblind-matter-descent"), "3816 q-blind matter descent target selected"),
        ("spine_updated", "Current State After 3815" in spine_text and "3816-Y5-R2FR-parent-qblind-matter-descent-action-template-or-finite-qmatter-source-row.md" in spine_text, "live spine updated to 3815 and 3816 target"),
        ("formalization_clean", not fwb_hits, "no 3815 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script/spine contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "zero_audit": zero_audit_rows(timestamp),
        "chainmap": chainmap_rows(timestamp),
        "active_cse": active_cse_rows(timestamp),
        "branches": branch_rows(timestamp),
        "carryforward": carryforward_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gate_rows(timestamp, grouped)
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    write_markdown(grouped)
    update_spine()
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
