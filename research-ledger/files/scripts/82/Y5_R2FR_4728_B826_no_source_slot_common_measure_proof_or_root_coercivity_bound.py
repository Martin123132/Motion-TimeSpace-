from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4728"
CLAIM_ID = "L-570"
MARKER = "PPC4161_B826_NO_SOURCE_SLOT_COMMON_MEASURE_OR_ROOT_COHERCIVITY_BOUND_4728"
PACKET_MARKER = "PPC4161_PACKET_B826_NO_SOURCE_SLOT_COMMON_MEASURE_OR_ROOT_COHERCIVITY_BOUND_4728"
DECISION = "R826_NO_SOURCE_SLOT_EXACT_CONDITIONAL_PARENT_OBJECT_LANGUAGE_UNSIGNED_HOM_AND_ROOT_COHERCIVITY_BOUNDS_RETAINED"
NEXT_TARGET = "4729-Y5-R2FR-R826-parent-object-language-exhaustion-or-first-Hom-bound-row.md"

DOC_PATH = POST / "4728-Y5-R2FR-B826-no-source-slot-common-measure-proof-or-root-coercivity-bound.md"
FORMAL_PATH = FORMAL / "744-PPC4161-B826-no-source-slot-common-measure-proof-or-root-coercivity-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4728_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4728_R826_NO_SOURCE_SLOT_THEOREM.csv"
CLAUSE_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4728_COMMON_MEASURE_CLAUSE_AUDIT.csv"
COUNTERMODEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4728_R826_COUNTERMODEL_AND_BOUND_ROWS.csv"
ROOT_COHERCIVITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4728_ROOT_COHERCIVITY_BRIDGE_ROWS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4728_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4728_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4728_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4728_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4728_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4728_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4728_0", POST / "CURRENT_LOCAL_RESUME.md", "4728-Y5-R2FR-B826-no-source-slot-common-measure-proof-or-root-coercivity-bound.md", "4727 handoff target."),
    ("SRC4728_1", POST / "4727-Y5-R2FR-Bmem-eff-component-zero-or-first-source-backed-B-row.md", "no-source-slot", "4727 identifies no-source-slot as next route."),
    ("SRC4728_2", SOURCE_DIR / "P8_Y5_R2FR_4727_NEXT_TARGET.csv", "4728-Y5-R2FR-B826-no-source-slot-common-measure-proof-or-root-coercivity-bound.md", "machine handoff into 4728."),
    ("SRC4728_3", SOURCE_DIR / "P8_Y5_R2FR_4727_B826_ROOT_LOCK_THEOREM.csv", "BRL4727_4_even_or_no_source_slot", "4727 exact no-source-slot route."),
    ("SRC4728_4", SOURCE_DIR / "P8_Y5_R2FR_4727_FIRST_B826_FINITE_SOURCE_ROW.csv", "B8264727_1_coercive_root_bound", "4727 finite coercive fallback row."),
    ("SRC4728_5", SOURCE_DIR / "P8_Y5_R2FR_4672_B826_EVEN_RESPONSE_WELD.csv", "WELD4672_3_no_source_slot_theorem", "4672 R826 no-source-slot theorem target."),
    ("SRC4728_6", SOURCE_DIR / "P8_Y5_R2FR_4672_FIRST_ZM_B826_BOUND_ROW_CONTRACT.csv", "BND4672_1_no_source_slot", "4672 owner-zero row contract."),
    ("SRC4728_7", SOURCE_DIR / "P8_Y5_R2FR_4704_VISIBLE_IMAGE_PROOF_ATTEMPT.csv", "VIP4704_0_exact_image_zero_theorem", "4704 visible coefficient image theorem."),
    ("SRC4728_8", SOURCE_DIR / "P8_Y5_R2FR_4704_PARENT_GENERATOR_OBJECT_LANGUAGE.csv", "OBJ4704_1_hidden_scalar_argument", "4704 object language/countertarget audit."),
    ("SRC4728_9", SOURCE_DIR / "P8_Y5_R2FR_4704_CLAIM_BLOCKERS.csv", "BLK4704_0_parent_scalar_functional_exhaustion", "4704 parent scalar-functional blocker."),
    ("SRC4728_10", SOURCE_DIR / "P8_Y5_R2FR_4707_EXACT_ZERO_CONTRACT_ROWS.csv", "ZERO4707_1_no_extra_F2_subcase", "4707 no-extra target theorem."),
    ("SRC4728_11", SOURCE_DIR / "P8_Y5_R2FR_4707_FACTORIZATION_SIGNATURE_AUDIT.csv", "FSIG4707_3_no_hidden_visible_F2", "4707 factorization signature audit."),
    ("SRC4728_12", SOURCE_DIR / "P8_Y5_R2FR_4707_READOUT_TAIL_BOUND_ROWS.csv", "TAIL4707_1_F2_Hom_tail", "4707 finite Hom/readout tail rows."),
    ("SRC4728_13", SOURCE_DIR / "P8_Y5_R2FR_4708_RADIOUT_NATURALITY_THEOREM_ROWS.csv", "RRN4708_1_observed_readout_zero", "4708 readout naturality theorem."),
    ("SRC4728_14", SOURCE_DIR / "P8_Y5_R2FR_4708_RADIOUT_COUNTERMODEL_ROWS.csv", "CEX4708_1_clock_readout_reentry", "4708 readout countermodel."),
    ("SRC4728_15", SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv", "ODT2659_1_exact_typed_theorem", "2659 exact typed domain theorem."),
    ("SRC4728_16", SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_COUNTERMODEL_LEDGER.csv", "CM2659_5_post_readout_selector", "2659 countermodel ledger."),
    ("SRC4728_17", SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_HOM_EXCLUSION_THEOREM_ATTEMPT.csv", "HOM2613_1_conditional_meta_theorem", "2613 no-source-only Hom meta-theorem."),
    ("SRC4728_18", SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_INVARIANT_ALGEBRA_HOM_AUDIT.csv", "IH2613_7_verdict", "2613 invariant algebra debts."),
    ("SRC4728_19", SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv", "SF2613_0_label_forgetting", "2613 label-forgetting source functor."),
    ("SRC4728_20", SOURCE_DIR / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_2_no_extra_mass_channel", "source measure extra-channel guard."),
    ("SRC4728_21", SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_2_MTS_transfer_condition", "worldtube source-measure transfer condition."),
    ("SRC4728_22", SOURCE_DIR / "P8_YLOC_NO_SOURCE_THEOREM.csv", "N3_zero_theorem", "generic local no-source theorem."),
    ("SRC4728_23", SOURCE_DIR / "P8_Y5_R2FR_4711_ROOT_NORMAL_EQUATION_CERTIFICATE.csv", "RNC4711_0_parent_residual_square_normal_equation", "root normal equation certificate."),
    ("SRC4728_24", SOURCE_DIR / "P8_Y5_R2FR_4712_ROOT_COHERCIVITY_SOURCE_PACK.csv", "RCP4712_4_lambdaRQ", "root coercivity source pack."),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    write_text(path, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path)
    raise KeyError(source_id)


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def theorem_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "NS4728_0_target",
            "R826 vertical derivative",
            "For v in ker(Dq_obs), D_v R_826=0 if R_826=Rbar_826(q_obs(Phi),theta_fixed) or R_826 is absent before parent variation.",
            "This is the exact no-source-slot target for B826.",
            "TARGET_SHARP",
            "SRC4728_5",
        ),
        (
            "NS4728_1_chain_rule",
            "q-basic response",
            "D_v Rbar_826(q_obs(Phi),theta_fixed)=D_q Rbar_826 Dq_obs[v]+D_theta Rbar_826 D_v theta_fixed=0.",
            "The proof is ordinary chain rule, not a smallness assumption.",
            "EXACT_IF_QBASIC_AND_FIXED_DATA",
            "SRC4728_15",
        ),
        (
            "NS4728_2_absent_target",
            "no coefficient target",
            "If the parent object language has no hidden/readout/material target into the 826 response coefficient, a nonconstant hidden map is ill-typed.",
            "This kills the derivative by removing the target object, not by tuning the coefficient.",
            "EXACT_CONDITIONAL_NO_HOM",
            "SRC4728_17",
        ),
        (
            "NS4728_3_common_measure",
            "common source/measure branch",
            "If source measure, current owner, boundary class and readout are downstream q-basic functors, source/worldtube choices cannot create R826 before variation.",
            "Common measure helps only if it is tied to parent variation order and boundary/domain silence.",
            "COMMON_MEASURE_CONDITIONAL",
            "SRC4728_19",
        ),
        (
            "NS4728_4_countermodel",
            "hidden/readout target survives",
            "R_826=Rbar(q_obs)+epsilon I_hid or R_826=Rbar(q_obs)+epsilon ReadoutSelector is legal unless the parent object language excludes that target.",
            "Covariance alone does not prove no-source-slot.",
            "COUNTERMODEL_RETAINED",
            "SRC4728_16",
        ),
        (
            "NS4728_5_result",
            "4728 verdict",
            "No-source-slot is an exact conditional theorem, but current evidence does not parent-sign parent object-language exhaustion, readout naturality, source measure, or boundary/domain silence.",
            "B826 remains nonclaim and finite Hom/root-coercivity rows must be retained.",
            "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "SRC4728_9",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "target": target,
            "statement": statement,
            "meaning": meaning,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for theorem_id, target, statement, meaning, status, source_id in specs
    ]


def clause_audit_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CLAUSE4728_0_parent_object_language",
            "visible/response object algebra",
            "R_826 coefficient target is in q^*A_Q plus fixed data only",
            "current evidence gives exact theorem shape but parent scalar-functional exhaustion is unsigned",
            "PARENT_OBJECT_LANGUAGE_UNSIGNED",
            "SRC4728_7",
        ),
        (
            "CLAUSE4728_1_no_hidden_visible_Hom",
            "hidden/material/readout Hom",
            "Hom_parent(H_hidden or ReadoutSelector, Coeff/R826)=0 or CommonConst",
            "hidden-visible Hom theorem remains conditional; legal countermodels survive",
            "NO_HOM_UNSIGNED",
            "SRC4728_15",
        ),
        (
            "CLAUSE4728_2_fixed_representation",
            "fixed constants",
            "theta_rep, charge/mass/clock/material constants are fixed representation data",
            "fixed-data clause is not parent-derived for all readout/material branches",
            "FIXED_DATA_UNSIGNED",
            "SRC4728_11",
        ),
        (
            "CLAUSE4728_3_variation_before_readout",
            "readout order",
            "readout/material/apparatus maps happen after parent variation and factor through q_obs",
            "4708 gives exact naturality shape but readout functor remains unsigned",
            "READOUT_NATURALITY_UNSIGNED",
            "SRC4728_13",
        ),
        (
            "CLAUSE4728_4_source_measure",
            "source/current/worldtube measure",
            "source functor forgets labels and uses one descended Hilbert/source current before readout",
            "source-measure and worldtube glue are conditional; extra mass/source channels remain possible",
            "SOURCE_MEASURE_UNSIGNED",
            "SRC4728_20",
        ),
        (
            "CLAUSE4728_5_boundary_domain",
            "boundary/domain silence",
            "boundary class, support, worldtube and domain selectors cannot become R826 arguments",
            "boundary/domain/projector channels remain open unless fixed no-flux and domain clauses are signed",
            "BOUNDARY_DOMAIN_UNSIGNED",
            "SRC4728_21",
        ),
        (
            "CLAUSE4728_6_local_no_source",
            "positive no-source theorem",
            "positive operator plus J=0 and B=0 gives local silence",
            "the theorem is useful only after J_R826/B_R826 are killed by the owner clauses above",
            "NO_SOURCE_THEOREM_CONDITIONAL",
            "SRC4728_22",
        ),
        (
            "CLAUSE4728_7_verdict",
            "same-branch clause pack",
            "all clauses must sign in one branch before B826 zero is promoted",
            "current branch keeps finite Hom/root-coercivity rows",
            "PACK_NOT_SIGNED",
            "SRC4728_12",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": clause_id,
            "clause": clause,
            "required_statement": required_statement,
            "current_evidence": current_evidence,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for clause_id, clause, required_statement, current_evidence, status, source_id in specs
    ]


def countermodel_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CMB4728_0_hidden_scalar_R826",
            "R_826=Rbar(q_obs)+epsilon I_hid",
            "hidden scalar coefficient target survives unless no-Hom/object-language exhaustion is signed",
            "H_R826 := sup |D_v R_826|",
            "MISSING_HOM_BOUND_VALUE",
            "SRC4728_8",
        ),
        (
            "CMB4728_1_readout_selector_R826",
            "R_826=Rbar(q_obs)+epsilon ReadoutSelector",
            "post-readout selector can re-enter unless variation-before-readout and readout naturality are signed",
            "B_readout_R826 := |D_v delta_R_readout|",
            "MISSING_READOUT_BOUND_VALUE",
            "SRC4728_14",
        ),
        (
            "CMB4728_2_worldtube_domain_R826",
            "R_826=Rbar(q_obs)+epsilon BoundaryClass/WorldtubeMask",
            "boundary/domain source measure can become a coefficient target unless fixed-domain/no-flux clauses sign",
            "B_domain_R826 := |D_v delta_R_domain|",
            "MISSING_DOMAIN_BOUND_VALUE",
            "SRC4728_21",
        ),
        (
            "CMB4728_3_finite_Rm_envelope",
            "R_m retained",
            "|R_m| <= H_R826 + B_readout_R826 + B_domain_R826 + B_source_R826 + higher_order",
            "feeds |B_826| <= |a_F| L_cg^-2 |R_m|",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "SRC4728_12",
        ),
        (
            "CMB4728_4_B826_bound",
            "finite B826",
            "|B_826| <= |a_F| L_cg^-2 (H_R826+B_readout_R826+B_domain_R826+B_source_R826+root_coercive_tail)",
            "first source-backed Hom row if no-source-slot proof fails",
            "FIRST_HOM_BOUND_ROW_REQUIRED",
            "SRC4728_4",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "counter_id": counter_id,
            "countermodel_or_row": countermodel,
            "why_it_survives": why_it_survives,
            "finite_bound": finite_bound,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for counter_id, countermodel, why_it_survives, finite_bound, status, source_id in specs
    ]


def root_coercivity_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "RCB4728_0_exact_root",
            "exact root route",
            "If S_R=1/2||R_826||_W^2 plus no linear/boundary/cokernel source, stationarity and coercivity imply R_826=0.",
            "needs parent residual-square action and no-source clauses",
            "EXACT_CONDITIONAL_ROOT_UNSIGNED",
            "SRC4728_23",
        ),
        (
            "RCB4728_1_gap",
            "coercive gap",
            "lambda_R826=Z_R826_min*lambda_1_R826 + M_R826_min^2 - Eta_R826 > 0",
            "gap variables are symbolic and unsourced",
            "SYMBOLIC_GAP_DERIVED_UNSOURCED",
            "SRC4728_24",
        ),
        (
            "RCB4728_2_finite_root",
            "finite root if sources survive",
            "||R_826||_W <= C_root(||J_root||+||B_root||+||Pi_coker R_826||)",
            "finite route is ready but needs numeric/source-backed rows",
            "FINITE_ROOT_BOUND_READY_INPUTS_MISSING",
            "SRC4728_23",
        ),
        (
            "RCB4728_3_B826_insert",
            "B826 coercive insertion",
            "|B_826| <= |a_F| L_cg^-2 C_root(||J_root||+||B_root||+||Pi_coker R_826||)",
            "coercive fallback if no-source-slot remains unsigned",
            "B826_COHERCIVE_INSERT_READY_NONCLAIM",
            "SRC4728_4",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": bridge_id,
            "target": target,
            "formula_or_statement": formula,
            "meaning": meaning,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for bridge_id, target, formula, meaning, status, source_id in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4728_0_sources_verified", "All 4728 source paths exist and needles are found.", True, "NONE"),
        ("GATE4728_1_no_source_theorem_shape", "R826 no-source-slot theorem is exact under q-basic/absent-target premises.", True, "THEOREM_SHAPE_ONLY"),
        ("GATE4728_2_parent_object_language_signed", "R826 target algebra is q-basic plus fixed data only.", False, "PARENT_OBJECT_LANGUAGE_UNSIGNED"),
        ("GATE4728_3_no_hidden_visible_Hom_signed", "Hidden/material/readout Hom into R826 coefficient target is absent.", False, "NO_HOM_UNSIGNED"),
        ("GATE4728_4_common_measure_signed", "source/worldtube/current measure cannot become an R826 argument.", False, "SOURCE_MEASURE_UNSIGNED"),
        ("GATE4728_5_readout_naturality_signed", "readout/radiative maps preserve q-basic factorization.", False, "READOUT_NATURALITY_UNSIGNED"),
        ("GATE4728_6_finite_Hom_values_sourced", "H_R826/readout/domain/source Hom bounds have numeric/source-backed rows.", False, "HOM_BOUND_VALUES_MISSING"),
        ("GATE4728_7_root_coercivity_values_sourced", "C_root/J_root/B_root/Pi_coker gap values are source-backed.", False, "ROOT_COHERCIVITY_INPUTS_MISSING"),
        ("GATE4728_8_B826_closed", "B826 is zero or finite-bound claim-grade.", False, "B826_RETAINED_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "condition": condition,
            "passed": passed,
            "blocker": blocker,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, condition, passed, blocker in specs
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4728_0_no_covariance_shortcut", "Do not claim no-source-slot from covariance alone; scalar hidden targets are covariant."),
        ("FW4728_1_no_readout_smuggle", "Do not move an R826 source into post-readout or apparatus maps and call the parent action clean."),
        ("FW4728_2_no_source_measure_smuggle", "Common source measure must be a parent variation fact, not an orbital/GM calibration shortcut."),
        ("FW4728_3_no_branch_mixing", "Do not mix EM/readout no-Hom theorems with memory B826 unless the same object-language branch is signed."),
        ("FW4728_4_no_bound_backsolve", "Do not infer Hom bounds from local tests; derive/source the coefficient rows first."),
        ("FW4728_5_no_local_global_confusion", "A strict local no-source branch must not erase cosmology/galaxy memory branches."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derivation_result": "R826 no-source-slot is an exact conditional chain-rule/type theorem if R826 is q-basic/fixed or has no parent target before variation",
            "nonclaim_result": "parent object-language exhaustion, no-Hom, common measure, readout naturality and boundary/domain silence remain unsigned",
            "finite_row_result": "H_R826/readout/domain/source Hom bounds plus root-coercivity bridge rows are staged nonclaim",
            "local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4728_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated under post-checkpoint-work and formalization-workbench only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4728_1_science_verdict",
            "status": "no_source_slot_exact_conditional_object_language_unsigned",
            "detail": "The proof shape is real, but the parent object-language signature remains the blocker; finite Hom/root-coercivity rows survive.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "4728 reduces B826 no-source-slot to parent object-language exhaustion. The next best move is to try to sign that exhaustion for R826 specifically or fill the first Hom bound row.",
            "first_task": "Attempt a parent object inventory for R826: allowed arguments q_obs, fixed representation data, common measure only; forbidden hidden/readout/material/domain coefficient targets.",
            "fallback_task": "If the inventory cannot be signed, create the first executable H_R826 finite Hom row feeding |B826|.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    ts: str,
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4728 - B826 No-Source-Slot Common Measure Proof or Root Coercivity Bound

Generated: `{ts}`

## Purpose

4728 attacks the cleanest `B_826` zero route from 4727: prove the 826 response has no independent source slot before variation, or keep a finite Hom/root-coercivity bound.

## What Actually Moved

- The no-source-slot proof is now exact as a conditional theorem: if `R_826=Rbar_826(q_obs(Phi),theta_fixed)` or `R_826` has no parent target before variation, then `D_v R_826=0` for `v in ker(Dq_obs)`.
- The proof is chain rule/type exclusion, not smallness.
- The theorem does not promote because the parent object language still has unsigned hidden/readout/material/domain target exclusions.
- Countermodels survive: `R_826=Rbar(q_obs)+epsilon I_hid`, readout selectors, or worldtube/domain masks.
- Therefore finite `H_R826` Hom rows and root-coercivity rows remain staged nonclaim.

## No-Source Theorem

{bullets(theorem, "theorem_id", "status")}

## Clause Audit

{bullets(clauses, "clause_id", "status")}

## Countermodels and Bounds

{bullets(countermodels, "counter_id", "status")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 744 - B826 No-Source-Slot Common Measure Proof or Root Coercivity Bound

Generated: `{ts}`

## Result

The no-source-slot theorem is exact but conditional:

`R_826=Rbar_826(q_obs(Phi),theta_fixed)` and `v in ker(Dq_obs)` imply `D_v R_826=0`.

Equivalently, if the parent object language has no hidden/readout/material/domain target for the 826 response coefficient before variation, a nonconstant vertical map into `R_826` is ill-typed.

## Current Verdict

The theorem is not claim-grade yet. Parent object-language exhaustion, no-Hom, common source measure, readout naturality and boundary/domain silence remain unsigned. The finite branch therefore keeps `H_R826`, readout/domain/source Hom bounds, and the root-coercivity insertion.

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(ts: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: `R_826` no-source-slot is an exact chain-rule/type theorem if the 826 response is q-basic/fixed or has no hidden/readout/material/domain target before variation.
- Current blocker: parent object-language exhaustion and common-measure/readout/boundary clauses remain unsigned, so `H_R826` and root-coercivity finite rows survive.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: converts the `B_826` no-source-slot route into a precise parent object-language signature test and finite Hom fallback, preventing covariance/readout/source-measure smuggling.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`{DOC_PATH.name}`

## Decision

`{DECISION}`

## What moved forward

- The `R_826` no-source-slot route is now an exact conditional theorem: q-basic/fixed response gives `D_v R_826=0`.
- The parent object-language/signature package needed for claim is explicit: no hidden/readout/material/domain target, common source measure, readout naturality and boundary/domain silence.
- Because that package is unsigned, `H_R826` Hom bounds and root-coercivity rows remain nonclaim.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4728 proves the exact conditional no-source-slot theorem for R826, but keeps B826 nonclaim because parent object-language exhaustion, common measure, readout and boundary/domain clauses remain unsigned.",
        "current_evidence": "Generated source register, R826 no-source-slot theorem, common-measure clause audit, countermodel/bound rows, root-coercivity bridge rows, gates, firewalls, decision, status, next target and validation.",
        "status": "R826_no_source_slot_conditional_object_language_unsigned_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Claiming no-source-slot from covariance or common measure while hidden/readout/material/domain coefficient targets remain legal.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "If a hidden/readout/domain R826 target survives, B826 remains a finite memory vertex source.",
        "title": "B826 no-source-slot common measure proof or root coercivity bound",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def parse_csv(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    root_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        THEOREM_CSV,
        CLAUSE_AUDIT_CSV,
        COUNTERMODEL_CSV,
        ROOT_COHERCIVITY_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    theorem_status = ";".join(row["status"] for row in theorem)
    clause_status = ";".join(row["status"] for row in clauses)
    counter_status = ";".join(row["status"] for row in countermodels)
    root_status = ";".join(row["status"] for row in root_rows)
    checks = [
        ("VAL4728_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4728 source paths exist"),
        ("VAL4728_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4728 source needles found"),
        ("VAL4728_2_exact_theorem_written", "EXACT_IF_QBASIC_AND_FIXED_DATA" in theorem_status and "EXACT_CONDITIONAL_NO_HOM" in theorem_status, "q-basic/no-Hom exact theorem rows written"),
        ("VAL4728_3_countermodels_retained", "COUNTERMODEL_RETAINED" in theorem_status and "MISSING_HOM_BOUND_VALUE" in counter_status, "hidden/readout/domain countermodels retained"),
        ("VAL4728_4_clause_pack_unsigned", "PARENT_OBJECT_LANGUAGE_UNSIGNED" in clause_status and "READOUT_NATURALITY_UNSIGNED" in clause_status and "SOURCE_MEASURE_UNSIGNED" in clause_status, "parent object/readout/source clauses remain unsigned"),
        ("VAL4728_5_root_bridge_nonclaim", "FINITE_ROOT_BOUND_READY_INPUTS_MISSING" in root_status and all(not bool(row["valid_for_claim"]) for row in root_rows), "root-coercivity bridge rows remain nonclaim"),
        ("VAL4728_6_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] not in {"GATE4728_0_sources_verified", "GATE4728_1_no_source_theorem_shape"}), "all broad claim gates remain closed; theorem-shape gate is not claim"),
        ("VAL4728_7_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4728_8_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4728_9_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-570"),
        ("VAL4728_10_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4729 next target"),
        ("VAL4728_11_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4728 CSV files parse cleanly"),
        ("VAL4728_12_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    overall = all(result for _check_id, result, _detail in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4728_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4728 B826 no-source-slot common-measure or root-coercivity validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    theorem = theorem_rows(ts)
    clauses = clause_audit_rows(ts)
    countermodels = countermodel_rows(ts)
    root_rows = root_coercivity_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(CLAUSE_AUDIT_CSV, clauses)
    write_csv(COUNTERMODEL_CSV, countermodels)
    write_csv(ROOT_COHERCIVITY_CSV, root_rows)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, theorem, clauses, countermodels, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, theorem, clauses, countermodels, root_rows, gates, ts))


if __name__ == "__main__":
    main()
