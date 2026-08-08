from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4539"
CLAIM_ID = "L-381"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ADOPT_GP_HQNP_OR_EFFECTIVE_LOCAL_GR_FREEZE_4539"
MARKER = "PPC4161_PARENT_ADOPT_GR_PARITY_HQNP_SELECTOR_OR_FREEZE_EFFECTIVE_LOCAL_GR_BRANCH_4539"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ADOPT_GR_PARITY_HQNP_SELECTOR_OR_FREEZE_EFFECTIVE_LOCAL_GR_BRANCH_4539"
DECISION = "PARENT_ADOPTION_THEOREM_CONDITIONAL_CURRENT_CORPUS_FAILS_GLOBAL_SIGNATURE_EFFECTIVE_LOCAL_GR_BRANCH_FROZEN"
NEXT_TARGET = "4540-Y5-R2FR-parent-scale-law-for-IR-EH-selector-or-explicit-EFT-residual-envelope.md"

FORMAL_PATH = FORMAL / "555-PPC4161-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md"
DOC_PATH = POST / "4539-Y5-R2FR-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4539_SOURCE_REGISTER.csv"
ACTION_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4539_PARENT_ACTION_SELECTOR_CONTRACT.csv"
ADOPTION_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4539_PARENT_ADOPTION_AUDIT.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4539_CONDITIONAL_THEOREM_AND_FAILURE.csv"
FREEZE_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4539_EFFECTIVE_LOCAL_GR_FREEZE_CONTRACT.csv"
RESIDUAL_HANDOFF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4539_RESIDUAL_HANDOFF_MATRIX.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4539_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4539_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4539_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4539_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4539_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4539_00_4538_status",
            "label": "4538 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4538_STATUS.csv",
            "needle": "global_parent_action_adoption_proved",
            "role": "4538 identifies parent adoption as still false",
        },
        {
            "source_id": "SRC4539_01_4538_residual",
            "label": "4538 residual collapse",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4538_LOCAL_RESIDUAL_VECTOR_COLLAPSE.csv",
            "needle": "RV4538_5_global_parent_adoption",
            "role": "parent adoption is the main live residual",
        },
        {
            "source_id": "SRC4539_02_4537_rank",
            "label": "4537 GR-parity rank",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4537_COMPONENT_GRAPH_RANK_RESULTS.csv",
            "needle": "RR4537_2_GR_parity_adopted_branch",
            "role": "ordinary visible source-weight zero inside GR-parity branch",
        },
        {
            "source_id": "SRC4539_03_4174_selector",
            "label": "4174 parent selector clauses",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4174_PARENT_SELECTOR_CLAUSES.csv",
            "needle": "SEL4174_6_local_boundary_silence",
            "role": "selector clauses and global debts",
        },
        {
            "source_id": "SRC4539_04_4180_matrix",
            "label": "4180 parent adoption matrix",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4180_ADOPTION_MATRIX.csv",
            "needle": "ADM4180_0_EH_origin",
            "role": "EH origin/global adoption failure evidence",
        },
        {
            "source_id": "SRC4539_05_4180_status",
            "label": "4180 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4180_STATUS.csv",
            "needle": "global_parent_action_adoption_proved",
            "role": "minimal parent action written but unsigned clauses demoted",
        },
        {
            "source_id": "SRC4539_06_4183_AMF",
            "label": "4183 motion-frame adoption",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4183_STATUS.csv",
            "needle": "Palatini_EH_forced_by_A_MF_alone",
            "role": "A_MF consequences do not force Palatini/EH alone",
        },
        {
            "source_id": "SRC4539_07_4184_IR",
            "label": "4184 IR selector status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4184_STATUS.csv",
            "needle": "selector_assumptions_parent_derived",
            "role": "Palatini/EH selector theorem remains conditional",
        },
        {
            "source_id": "SRC4539_08_4184_axioms",
            "label": "4184 IR selector axiom set",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET.csv",
            "needle": "SEL4184_2_IR_order",
            "role": "IR order and no-extra-light-mode assumptions",
        },
        {
            "source_id": "SRC4539_09_4184_normal",
            "label": "4184 normal form classification",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4184_NORMAL_FORM_CLASSIFICATION.csv",
            "needle": "NFC4184_0_EC_Palatini",
            "role": "EC/Palatini selected only if selector clauses hold",
        },
        {
            "source_id": "SRC4539_10_4179_chain",
            "label": "4179 private local GR closure chain",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4179_LOCAL_GR_CLOSURE_CHAIN.csv",
            "needle": "LC4179_9_calibrated_G",
            "role": "private local chain stays useful but nonclaim",
        },
        {
            "source_id": "SRC4539_11_packet_180",
            "label": "packet 180 current local packet",
            "path": PACKET_PATH,
            "needle": "PPC4161_PACKET_GR_PARITY_LOCAL_SOURCE_UNIVERSALITY_ADOPTION_GATES_OR_INTERFACE_RESIDUALS_4538",
            "role": "4538 packet integration already installed",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "role": spec["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PAC4539_0_domain",
            "clause": "compact local collar C_loc and projector P_loc",
            "required_parent_statement": "P_loc is parent-owned, idempotent, fixed before readout and commutes with variation through <=2PN: delta(P_loc S_parent)=P_loc delta S_parent + boundary_zero.",
            "effect_if_signed": "local equations can be read before empirical material/orbital labels enter",
            "current_status": "not_globally_parent_signed",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PAC4539_1_action_split",
            "clause": "local action split",
            "required_parent_statement": "On C_loc, S_parent = S_GP-HQNP^loc + S_res^loc + S_global^out with P_loc delta S_res^loc=0 or bounded and P_loc delta S_global^out=0 through <=2PN.",
            "effect_if_signed": "private branch becomes a parent-derived local sector rather than an adopted effective sector",
            "current_status": "conditional_contract_only",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PAC4539_2_effective_local_action",
            "clause": "S_GP-HQNP^loc definition",
            "required_parent_statement": "S_GP-HQNP^loc = S_EH[g_obs,kappa_*] + S_SM^GRparity[g_obs,fields,c_i] + S_Maxwell-Hodge[g_obs,A] + S_top[kappa_*] + S_HQ_boundary[W_H,tau,H_ref].",
            "effect_if_signed": "single local action carries source universality, EM stress, calibrated coupling, Hamiltonian charge, Newton and PPN readout",
            "current_status": "defined_effective_branch",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PAC4539_3_no_reentry",
            "clause": "no source/readout reentry",
            "required_parent_statement": "SpeciesLabel, MaterialLabel, fitted orbital GM, clock readout and hidden representative labels have no morphism into active source coefficients after variation.",
            "effect_if_signed": "prevents the branch from being a post-hoc fitted source model",
            "current_status": "private_branch_signed_not_global",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PAC4539_4_IR_selector",
            "clause": "EH/Palatini principal block selector",
            "required_parent_statement": "A parent scale/normal-form theorem selects the parity-even linear-curvature EC/Palatini block and demotes extra invariants to zero/topological/heavy/bounded residuals.",
            "effect_if_signed": "turns effective-GR principal block into derived MTS local dynamics",
            "current_status": "conditional_not_parent_derived",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PAC4539_5_sector_interfaces",
            "clause": "global sector no-leak",
            "required_parent_statement": "P_loc P_gal = P_loc P_cos = 0 on C_loc and FLRW/galaxy/open-memory/radiative branches have exact support separation or no-flux projection through <=2PN.",
            "effect_if_signed": "lets local GR coexist with galaxy/cosmology sectors without erasing them or leaking them into Solar-system PPN",
            "current_status": "not_globally_parent_signed",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PAC4539_6_quotient_naturality",
            "clause": "variation descends through q",
            "required_parent_statement": "Representative vertical generators v in ker(Dq) are pure gauge before variation: P_loc DObar[Dq[v]]=0 and no physical source term is born from representative choice.",
            "effect_if_signed": "prevents hidden scalar/vector/projector force channels",
            "current_status": "private_selector_not_global",
            "valid_for_claim": "False",
        },
    ]


def adoption_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "AA4539_0_GRparity_source",
            "selector_piece": "ordinary visible source universality",
            "current_evidence": "4537 rank n-1 and no source-prefactor branch",
            "verdict": "private_branch_pass",
            "blocks_parent_adoption": "False",
            "next_action": "use as imported branch, do not reopen unless off-branch matter appears",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AA4539_1_HQNP_chain",
            "selector_piece": "same charge, Newton, PPN, local comparator",
            "current_evidence": "4170-4173 and 4179 chain",
            "verdict": "private_branch_pass",
            "blocks_parent_adoption": "False",
            "next_action": "carry as effective local-GR branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AA4539_2_EH_origin",
            "selector_piece": "EH/Palatini principal block from MTS parent",
            "current_evidence": "4180 ADM4180_0 not_adopted_global; 4183 A_MF alone does not force Palatini; 4184 selector assumptions not parent-derived",
            "verdict": "fails_global_parent_signature",
            "blocks_parent_adoption": "True",
            "next_action": "derive parent scale law/IR normal form or keep EFT residual envelope",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AA4539_3_boundary_no_flux",
            "selector_piece": "compact local collar boundary silence",
            "current_evidence": "4174 not globally proved; 4180 closure_or_superselection_until_support_theorem",
            "verdict": "private_or_closure_only",
            "blocks_parent_adoption": "True",
            "next_action": "derive support/no-flux theorem for P_loc against galaxy/cosmology/memory sectors",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AA4539_4_quotient_naturality",
            "selector_piece": "q-natural vertical silence",
            "current_evidence": "4174 not globally proved; 4180 adoption_axiom_or_closure_until_parent_category",
            "verdict": "private_or_closure_only",
            "blocks_parent_adoption": "True",
            "next_action": "derive parent q/category/functor or retain projector residual",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AA4539_5_global_unification",
            "selector_piece": "same parent owns local, galaxy, cosmology, time, EM and quantum sectors",
            "current_evidence": "4180 ADM4180_8 not_adopted_global",
            "verdict": "not_adopted_global",
            "blocks_parent_adoption": "True",
            "next_action": "build sector interface matrix after local effective branch is frozen",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AA4539_6_numeric_G",
            "selector_piece": "numeric Newton constant prediction",
            "current_evidence": "4178/4179/4180 calibrate G but do not predict its numerical value",
            "verdict": "not_required_for_structural_GR_but_not_predicted",
            "blocks_parent_adoption": "False",
            "next_action": "keep G_cal calibrated unless a parent scale theorem appears",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "TH4539_0_conditional_parent_adoption",
            "statement": "If PAC4539 clauses 0-6 are parent-signed, then P_loc delta S_parent gives PPC4161-GP-HQNP local equations plus zero/bounded residuals through <=2PN.",
            "proof_sketch": "The action split sends all active local variations into S_GP-HQNP^loc; GR-parity rank gives P_perp Delta_w=0; HQ charge fixes the source mass; EH weak-field gives Newton; PPN side channels vanish by same-coframe/no-flux/q-natural clauses.",
            "current_truth_status": "conditional_true_not_currently_proved",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4539_1_current_failure",
            "statement": "The current corpus cannot promote PPC4161-GP-HQNP to a globally parent-derived MTS local branch.",
            "proof_sketch": "A single failed required parent signature is enough. Current evidence gives at least four: EH/Palatini origin not parent-derived, IR selector assumptions not parent-derived, boundary/global no-flux not globally proved, quotient naturality not globally proved.",
            "current_truth_status": "proved_from_current_audit",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4539_2_effective_freeze",
            "statement": "Therefore the disciplined move is to freeze PPC4161-GP-HQNP as an effective local-GR branch rather than keep treating it as a nearly proven parent theorem.",
            "proof_sketch": "The branch is internally useful and test-compatible, but the missing signatures are root parent-action facts, not small algebraic details. Freezing preserves progress while preventing closure smuggling.",
            "current_truth_status": "adopted_private_working_policy",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def freeze_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "freeze_id": "FR4539_0_name",
            "rule": "Branch label",
            "allowed": "Use `PPC4161-GP-HQNP effective local-GR branch` for local correspondence work.",
            "forbidden": "Calling it a parent-derived full MTS->GR proof.",
            "valid_for_claim": "False",
        },
        {
            "freeze_id": "FR4539_1_allowed_use",
            "rule": "Allowed calculations",
            "allowed": "Newton, PPN, local source-coupling, EM stress accounting, R10/clock/WEP/orbital comparators inside compact ordinary-visible local collars.",
            "forbidden": "Using the branch for galaxy/cosmology/open-memory regimes without sector-interface equations.",
            "valid_for_claim": "False",
        },
        {
            "freeze_id": "FR4539_2_language",
            "rule": "Safe language",
            "allowed": "MTS contains a disciplined effective local-GR branch compatible with GR local limits under stated selector clauses.",
            "forbidden": "MTS has derived GR from first principles or predicted Newton's constant.",
            "valid_for_claim": "False",
        },
        {
            "freeze_id": "FR4539_3_reopen_rule",
            "rule": "Reopen residuals",
            "allowed": "If a future test leaves ordinary visible GR-parity matter or compact local collar assumptions, reactivate R_off/R_global-specific residual rows.",
            "forbidden": "Treating 4537 source universality as global hidden-sector universality.",
            "valid_for_claim": "False",
        },
        {
            "freeze_id": "FR4539_4_upgrade_rule",
            "rule": "Upgrade path",
            "allowed": "Upgrade from effective branch to parent theorem only if PAC4539 parent signatures are proven from the action.",
            "forbidden": "Upgrading because local comparator rows pass or because the branch is GR-like.",
            "valid_for_claim": "False",
        },
    ]


def residual_handoff_rows() -> list[dict[str, Any]]:
    return [
        {
            "handoff_id": "RH4539_0_EH_IR",
            "live_residual": "E_EH_IR",
            "meaning": "EH/Palatini principal block and IR order/no-light-mode selector are not parent-derived",
            "route": NEXT_TARGET,
            "status": "PRIMARY_NEXT_TARGET",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "handoff_id": "RH4539_1_boundary",
            "live_residual": "E_boundary_global",
            "meaning": "global sector no-flux/support separation into compact local collar is not parent-proved",
            "route": "sector projector/no-flux theorem or bounded transition-current rows",
            "status": "OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "handoff_id": "RH4539_2_quotient",
            "live_residual": "E_q_naturality",
            "meaning": "q-natural vertical silence is private/closure unless parent category/functor is derived",
            "route": "parent quotient functor proof or projector residual bounds",
            "status": "OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "handoff_id": "RH4539_3_global",
            "live_residual": "E_global_unification",
            "meaning": "local effective branch is not yet integrated with galaxy/cosmology/time/quantum sectors under one parent action",
            "route": "sector interface matrix after EH/IR selector is stabilized",
            "status": "OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "handoff_id": "RH4539_4_empirical",
            "live_residual": "E_emp_raw",
            "meaning": "4173 comparator rows pass privately but raw/data-curve validation remains incomplete",
            "route": "digitized R10 curve plus raw local validation pack",
            "status": "OPEN_NOT_THEORY_ROOT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "handoff_id": "RH4539_5_offbranch",
            "live_residual": "E_off",
            "meaning": "hidden/nonstandard matter and readout reentry outside ordinary visible GR-parity branch",
            "route": "finite C_src/Delta_w projection rows or stronger no-extension theorem",
            "status": "RETAIN_BOUND_ROUTE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4539_0_conditional_theorem",
            "gate": "conditional parent adoption theorem",
            "status": "PASS_CONDITIONAL",
            "meaning": "the exact contract is now written",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4539_1_current_parent_adoption",
            "gate": "current parent action signs all clauses",
            "status": "FAIL_UNSIGNED",
            "meaning": "EH/IR selector, boundary global no-flux, quotient naturality and global sector adoption are not signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4539_2_effective_branch",
            "gate": "effective local-GR branch",
            "status": "FROZEN_FOR_PRIVATE_WORK",
            "meaning": "safe as a disciplined local correspondence/test branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4539_3_public_local_GR",
            "gate": "public local-GR derivation claim",
            "status": "BLOCKED_NONCLAIM",
            "meaning": "must wait for parent signatures or publish as conditional/effective branch only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4539_4_full_unified_field_theory",
            "gate": "full unified field theory",
            "status": "BLOCKED",
            "meaning": "local effective branch does not yet unify galaxy/cosmology/time/quantum sectors",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4539_0",
            "decision": DECISION,
            "meaning": "4539 makes the parent-adoption test exact. The branch is strong enough to freeze as effective local GR, but current evidence does not parent-sign the root selector. This is progress because the work now knows where not to keep circling: attack the EH/IR scale law or keep residual EFT bounds explicit.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4539_0",
            "target": NEXT_TARGET,
            "objective": "try to derive the parent scale/normal-form law that selects the EH/Palatini principal block and suppresses extra local invariants",
            "derive_first": "look for an MTS scale hierarchy or motion-frame normal-form argument that makes linear curvature the unique low-energy local term",
            "fallback": "if not derivable, write explicit EFT residual envelopes from torsion, curvature-squared, disformal and memory couplings into PPN/R10/clock arenas",
            "avoid": "re-arguing source coupling or GR-parity rank unless the test leaves the effective local branch",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "result": DECISION,
            "conditional_parent_adoption_theorem_written": "True",
            "current_parent_adoption_proved": "False",
            "effective_local_GR_branch_frozen": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "primary_live_residual": "E_EH_IR",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    action_contract: list[dict[str, Any]],
    adoption_audit: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    freeze: list[dict[str, Any]],
    handoff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4539_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    contract_ids = {row["contract_id"] for row in action_contract}
    contract_ok = all(cid in contract_ids for cid in ["PAC4539_1_action_split", "PAC4539_2_effective_local_action", "PAC4539_4_IR_selector", "PAC4539_5_sector_interfaces"])
    checks.append({"validation_id": "VAL4539_01_action_contract", "status": "PASS" if contract_ok else "FAIL", "detail": "parent action selector contract includes split, effective action, IR selector and sector interfaces"})

    audit_blocks = [row for row in adoption_audit if row.get("blocks_parent_adoption") == "True"]
    audit_ok = len(audit_blocks) >= 3 and any(row["audit_id"] == "AA4539_2_EH_origin" for row in audit_blocks)
    checks.append({"validation_id": "VAL4539_02_adoption_audit", "status": "PASS" if audit_ok else "FAIL", "detail": "current parent adoption fails for explicit root clauses"})

    theorem_ok = any(row["theorem_id"] == "TH4539_1_current_failure" and row["current_truth_status"] == "proved_from_current_audit" for row in theorem)
    checks.append({"validation_id": "VAL4539_03_failure_theorem", "status": "PASS" if theorem_ok else "FAIL", "detail": "current failure theorem is explicit, not vague"})

    freeze_ok = any(row["freeze_id"] == "FR4539_0_name" for row in freeze) and any("first principles" in row["forbidden"] for row in freeze)
    checks.append({"validation_id": "VAL4539_04_freeze_contract", "status": "PASS" if freeze_ok else "FAIL", "detail": "effective local-GR freeze contract blocks overclaiming"})

    handoff_ok = any(row["handoff_id"] == "RH4539_0_EH_IR" and row["status"] == "PRIMARY_NEXT_TARGET" for row in handoff)
    checks.append({"validation_id": "VAL4539_05_handoff", "status": "PASS" if handoff_ok else "FAIL", "detail": "EH/IR selector is selected as primary next target"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    parent_fail = any(row["claim_gate_id"] == "CG4539_1_current_parent_adoption" and row["status"] == "FAIL_UNSIGNED" for row in gates)
    checks.append({"validation_id": "VAL4539_06_claim_firewall", "status": "PASS" if gates_ok and parent_fail else "FAIL", "detail": "all claim gates stay nonclaim and parent adoption fails unsigned"})

    csv_paths = [
        SOURCE_REGISTER,
        ACTION_CONTRACT_CSV,
        ADOPTION_AUDIT_CSV,
        THEOREM_CSV,
        FREEZE_CONTRACT_CSV,
        RESIDUAL_HANDOFF_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        try:
            if not read_csv(path):
                csv_ok = False
                details.append(f"{path.name}:empty")
        except Exception as exc:
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4539_07_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4539_08_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4539_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4539 parent-adoption theorem attempt and effective local-GR freeze"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    action_contract: list[dict[str, Any]],
    adoption_audit: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    freeze: list[dict[str, Any]],
    handoff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4539 - parent adopt GR-parity/HQNP selector or freeze as effective local-GR branch

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4538 said the local source-coupling fog has collapsed inside the private `PPC4161-GP-HQNP` branch. 4539 now asks the hard question:

```text
Is PPC4161-GP-HQNP actually selected by the MTS parent action,
or is it an effective local-GR branch we should use honestly as such?
```

The exact parent-action contract is now:

```text
S_parent | C_loc
  = S_GP-HQNP^loc[g_obs,theta,fields;kappa_*,c_i,W_H,tau,H_ref]
  + S_res^loc
  + S_global^out,

P_loc delta S_res^loc = 0 or bounded through <=2PN,
P_loc delta S_global^out = 0 through <=2PN.
```

The conditional theorem is valid: if the parent signs every selector clause below, the branch becomes a parent-derived local GR/Newton/PPN limit with calibrated `G_cal`. Current evidence does **not** sign every clause. The root failures are not small missing CSV cells: EH/Palatini IR selection, global boundary/no-flux, quotient naturality, and full sector unification remain unsigned.

So the disciplined result is:

```text
PPC4161-GP-HQNP is frozen as an effective local-GR branch.
```

That is still useful. It preserves the GR/Newton/PPN correspondence branch and the local empirical comparator path, while forbidding a false claim that MTS has fully derived GR from the parent action.

## Parent Action Selector Contract

{markdown_table(action_contract)}

## Parent Adoption Audit

{markdown_table(adoption_audit)}

## Theorem And Failure

{markdown_table(theorem)}

## Effective Local-GR Freeze Contract

{markdown_table(freeze)}

## Residual Handoff Matrix

{markdown_table(handoff)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Status

{markdown_table(status)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_adoption",
        "claim": "4539 writes the exact parent-action selector contract for PPC4161-GP-HQNP and proves the current corpus does not sign it globally; the branch is frozen as an effective local-GR branch rather than promoted as a parent-derived GR theorem.",
        "current_evidence": "Generated source register, parent action selector contract, adoption audit, conditional theorem/failure rows, effective local-GR freeze contract, residual handoff matrix, claim gates, status and validation CSVs.",
        "status": "effective_local_GR_branch_frozen_parent_adoption_unsigned_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Overclaiming the effective GR branch as a first-principles MTS derivation of GR, or pretending local comparator passes sign the parent action.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "EH/IR selector, boundary no-flux, quotient naturality and global sector interfaces remain active residuals.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    action_contract = action_contract_rows()
    adoption_audit = adoption_audit_rows()
    theorem = theorem_rows()
    freeze = freeze_contract_rows()
    handoff = residual_handoff_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_CONTRACT_CSV, action_contract)
    write_csv(ADOPTION_AUDIT_CSV, adoption_audit)
    write_csv(THEOREM_CSV, theorem)
    write_csv(FREEZE_CONTRACT_CSV, freeze)
    write_csv(RESIDUAL_HANDOFF_CSV, handoff)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, action_contract, adoption_audit, theorem, freeze, handoff, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, action_contract, adoption_audit, theorem, freeze, handoff, gates, decisions, next_target, status, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4539 Parent Adopt GR-Parity/HQNP Selector Or Freeze Effective Local GR Branch

Marker: `{MARKER}`  
4539 writes the exact parent-action contract for upgrading `PPC4161-GP-HQNP` from private/effective local GR to a parent-derived MTS local sector. The conditional theorem is clean, but the current corpus fails global signature: EH/Palatini IR selector, boundary/global no-flux, quotient naturality and full sector adoption remain unsigned. The branch is therefore frozen honestly as an effective local-GR branch for private correspondence and testing. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4539 Packet Integration - Effective Local-GR Branch Freeze

Marker: `{PACKET_MARKER}`  
`PPC4161-GP-HQNP` is now frozen as an effective local-GR branch, not promoted as a full parent-action theorem. The packet can use it for local Newton/PPN/source/EM comparator work, while the parent-action adoption burden moves to EH/IR scale selection, global no-flux, quotient naturality and sector interfaces.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
