from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2632-Y5-R2FR-no-source-prefactor-parent-action-clause-or-PPN-component-basis-first-row.md"

PREFIX = "P8_Y5_SOURCE_PREF_GR_ROLLFORWARD_2632"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "coupling_rollforward": RESIDUALS / f"{PREFIX}_SOURCE_COUPLING_ROLLFORWARD.csv",
    "gr_frontier": RESIDUALS / f"{PREFIX}_LOCAL_GR_FRONTIER_MATRIX.csv",
    "residual_owners": RESIDUALS / f"{PREFIX}_RESIDUAL_OWNER_LEDGER.csv",
    "route_guards": RESIDUALS / f"{PREFIX}_ROUTE_GUARDS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2632_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2632_00_2631_current",
        "role": "current branch handoff selecting source-prefactor coupling",
        "path": ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md",
        "needles": [
            "SOURCE_PREFACTOR_COUPLING_IS_NEXT_BEST_LEAP",
            "PPNV2631_4_wR",
            "VAL2631_OVERALL",
        ],
    },
    {
        "source_id": "SRC2632_01_2631_validation",
        "role": "2631 validation pass",
        "path": RESIDUALS / "P8_Y5_BRR545_2631_VALIDATION.csv",
        "needles": ["VAL2631_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2632_02_1890_no_prefactor",
        "role": "no-source-prefactor theorem attempt and first Delta_w row",
        "path": ROOT / "1890-Y5-R2FR-no-source-prefactor-parent-action-clause-or-component-basis-first-source-row.md",
        "needles": [
            "NO_SOURCE_PREFACTOR_THEOREM_NOT_DERIVED",
            "FIRST_COMPONENT_ROW_STAGED_NONCLAIM",
            "VAL1890_OVERALL",
        ],
    },
    {
        "source_id": "SRC2632_03_1896_nohom_basis",
        "role": "parent no-Hom attempt and finite Delta_w basis",
        "path": ROOT / "1896-Y5-R2FR-parent-sort-disjointness-nohom-proof-or-finite-deltaw-basis.md",
        "needles": [
            "PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED",
            "DWB1896_1_preaction_species",
            "VAL1896_OVERALL",
        ],
    },
    {
        "source_id": "SRC2632_04_1899_action_owner_wep",
        "role": "action/current owner attempt and WEP input pack",
        "path": ROOT / "1899-Y5-R2FR-wep-source-worldtube-material-tensor-acquisition-or-action-owner-lemma.md",
        "needles": [
            "ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED",
            "WEP_INPUT_PACK_NOT_EXECUTABLE_NONCLAIM",
            "VAL1899_OVERALL",
        ],
    },
    {
        "source_id": "SRC2632_05_1938_matter_side",
        "role": "candidate Hilbert matter source conservation and Newtonian blocker",
        "path": ROOT / "1938-Y5-R2FR-Bianchi-Ward-conservation-and-Newtonian-limit-of-candidate-Hilbert-action.md",
        "needles": [
            "CANDIDATE_HILBERT_MATTER_SIDE_PASSES_CONSERVATION_NONCLAIM",
            "GRAVITY_OPERATOR_IS_NOW_THE_PRIMARY_BLOCKER",
            "VAL1938_OVERALL",
        ],
    },
    {
        "source_id": "SRC2632_06_1940_lovelock",
        "role": "EH uniqueness conditional route and R11 residual branch",
        "path": ROOT / "1940-Y5-R2FR-EH-uniqueness-Lovelock-gate-or-R11-residual-operator.md",
        "needles": [
            "EH_FORCED_ONLY_UNDER_LOVELOCK_ASSUMPTIONS",
            "R11_REMAINS_THE_EXPLICIT_NOVELTY_BRANCH",
            "VAL1940_OVERALL",
        ],
    },
    {
        "source_id": "SRC2632_07_2483_eh_coupling",
        "role": "EH coupling origin and kappa residual",
        "path": ROOT / "2483-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md",
        "needles": [
            "BLOCKED_PARENT_ORIGIN",
            "KRES2483_0_e_kappaG",
            "VAL2483_OVERALL",
        ],
    },
    {
        "source_id": "SRC2632_08_2485_normal_form",
        "role": "parent normal-form skeleton and coefficient slots",
        "path": ROOT / "2485-Y5-R2FR-parent-normal-form-field-symmetry-derivative-grammar.md",
        "needles": [
            "SKELETON_WRITTEN_NOT_PARENT_DERIVED",
            "NF2485_0_parent_action_skeleton",
            "VAL2485_OVERALL",
        ],
    },
    {
        "source_id": "SRC2632_09_2486_quotient",
        "role": "field-sort/quotient map signature and DObs blocker",
        "path": ROOT / "2486-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md",
        "needles": [
            "`Dq[v]=0` is not enough",
            "Residual Owner Split",
            "VAL2486_OVERALL",
        ],
    },
    {
        "source_id": "SRC2632_10_2489_ppn",
        "role": "current no-shadow/full PPN residual vector",
        "path": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
        "needles": [
            "GAMMA_ONLY_PASS_FORBIDDEN",
            "PPNV2489_7_total_abs",
            "VAL2489_OVERALL",
        ],
    },
]


def ensure_dirs() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        text = read_text(path)
        exists = path.exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def coupling_rollforward_rows() -> list[dict[str, Any]]:
    return [
        {
            "roll_id": "CROLL2632_0_2631_handoff",
            "topic": "source-prefactor coupling selected by current branch",
            "imported_status": "SOURCE_PREFACTOR_COUPLING_IS_NEXT_BEST_LEAP",
            "rollforward_verdict": "OLD_CHAIN_ALREADY_ATTACKED_THIS_ROUTE",
            "meaning": "2632 should not restart at w_A; it should import the 1890-1940 source-coupling chain.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CROLL2632_1_no_source_prefactor",
            "topic": "no pre-action w_A S_A theorem",
            "imported_status": "NO_SOURCE_PREFACTOR_THEOREM_NOT_DERIVED",
            "rollforward_verdict": "exact_conditional_not_parent_signed",
            "meaning": "The theorem is sharp, but matter-normalization owner/object-language/action-scale/readout stability remain unsigned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CROLL2632_2_finite_deltaw_basis",
            "topic": "finite Delta_w/source-weight basis",
            "imported_status": "FINITE_COMPONENT_BASIS_READY_NONCLAIM",
            "rollforward_verdict": "schema_ready_values_missing",
            "meaning": "Delta_w_species, current rescale, marker spurion, non-Hilbert current and mass-projector residuals are named but lack parent values/projections.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CROLL2632_3_action_current_owner",
            "topic": "single action/current owner for WEP/source weights",
            "imported_status": "ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED",
            "rollforward_verdict": "derivation_gap_narrowed",
            "meaning": "The conditional owner lemma is exact; parent hbar/measure/current ownership and no-Hom source coefficient exclusion are not jointly signed.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CROLL2632_4_wep_inputs",
            "topic": "WEP/MICROSCOPE source-weight test branch",
            "imported_status": "WEP_INPUT_PACK_NOT_EXECUTABLE_NONCLAIM",
            "rollforward_verdict": "testing_scaffold_not_prediction",
            "meaning": "The MICROSCOPE bound anchor is cached, but residual values, source worldtube, material tensor, readout/force map and tau_WEP are missing.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CROLL2632_5_matter_source_side",
            "topic": "candidate Hilbert matter source",
            "imported_status": "CANDIDATE_HILBERT_MATTER_SIDE_PASSES_CONSERVATION_NONCLAIM",
            "rollforward_verdict": "source_side_conditionally_clean",
            "meaning": "The chain earned something important: a candidate matter action with Ward conservation and universal Hilbert source structure.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CROLL2632_6_gravity_operator",
            "topic": "EH/Lovelock gravity operator",
            "imported_status": "EH_FORCED_ONLY_UNDER_LOVELOCK_ASSUMPTIONS",
            "rollforward_verdict": "gravity_operator_is_primary_blocker",
            "meaning": "With source side sharpened, local Newton/GR now hinges on parent-signed EH assumptions, kappa owner, residual silence and PPN map.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def gr_frontier_rows() -> list[dict[str, Any]]:
    return [
        {
            "frontier_id": "GRF2632_0_matter_source",
            "requirement": "single Hilbert matter source with no source-only weights",
            "current_evidence": "1938 candidate matter action passes Ward conservation conditionally",
            "status": "PASS_CONDITIONAL_NONCLAIM",
            "missing_for_claim": "MISSING_PARENT_ACTION_SIGNATURE;MISSING_PRESERVATION_CLAUSES",
            "next_action": "carry as candidate source side; stop redoing pure w_A arguments unless new parent action evidence appears",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "frontier_id": "GRF2632_1_EH_operator",
            "requirement": "EH/kappa local gravitational operator",
            "current_evidence": "1940 Lovelock assumptions force EH only conditionally; 2483 keeps EH origin blocked",
            "status": "BLOCKED_PARENT_EH_ORIGIN",
            "missing_for_claim": "MISSING_PARENT_FIELD_LIST;MISSING_DIFF_GENERATOR;MISSING_DERIVATIVE_GRAMMAR;MISSING_COEFFICIENT_OWNER",
            "next_action": "sign parent normal-form hypotheses or keep e_EH_import/e_kappaG residuals",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "frontier_id": "GRF2632_2_residual_silence",
            "requirement": "non-EH/R11/MTS residual sectors vanish or are locally bounded",
            "current_evidence": "1940 R11 residual family and 2485 coefficient slots remain live",
            "status": "BLOCKED_RESIDUAL_SECTOR_BOUNDS",
            "missing_for_claim": "MISSING_R11_DIVERGENCE_LAW;MISSING_WEAK_FIELD_PROJECTION;MISSING_LOCAL_BOUND",
            "next_action": "turn every non-EH violation into a named residual coefficient with PPN/Newton projection",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "frontier_id": "GRF2632_3_quotient_readout",
            "requirement": "q_parent and DObs_e make private representatives locally invisible",
            "current_evidence": "2486 says Dq[v]=0 is not enough; 2489 keeps no-shadow/PPN vector blocked",
            "status": "BLOCKED_DOBS_E_AND_NO_SHADOW",
            "missing_for_claim": "MISSING_Q_PARENT_SIGNATURE;MISSING_DOBS_E_KERNEL;MISSING_TERMINAL_PUBLIC_COFRAME",
            "next_action": "derive observed coframe/readout functor or retain DObs/readout-leak rows",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "frontier_id": "GRF2632_4_full_PPN",
            "requirement": "gamma,beta,preferred-frame/source/readout residual vector",
            "current_evidence": "2489/2631 full vector exists and gamma-only is forbidden",
            "status": "BLOCKED_VECTOR_VALUES_MISSING",
            "missing_for_claim": "MISSING_DELTA_P_QRHAT;MISSING_BETA_KERNEL;MISSING_DISFORMAL_KERNEL;MISSING_SOURCE_PREFACATOR_THEOREM;MISSING_ENDPOINT_READOUT",
            "next_action": "fill theorem-zero or finite source-backed values before any local-GR claim",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def residual_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "RES2632_0_Delta_w_eff",
            "residual": "Delta_w_eff",
            "owner_status": "finite source-weight residual branch retained",
            "source": str(ROOT / "1896-Y5-R2FR-parent-sort-disjointness-nohom-proof-or-finite-deltaw-basis.md"),
            "zero_condition": "parent no-Hom/source-prefactor/action-current owner all signed",
            "bound_condition": "parent values plus WEP/R10/PPN/clock/orbital projection kernels",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "RES2632_1_e_EH_import",
            "residual": "e_EH_import",
            "owner_status": "logic residual for importing EH before deriving it",
            "source": str(ROOT / "2484-Y5-R2FR-EH-uniqueness-hypotheses-or-parent-normal-form-blocker.md"),
            "zero_condition": "all EH uniqueness hypotheses are parent-signed",
            "bound_condition": "publish as effective leading-operator route with explicit residuals, not fundamental derivation",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "RES2632_2_e_kappaG",
            "residual": "e_kappaG",
            "owner_status": "coupling residual between parent kappa and measured G_ref",
            "source": str(ROOT / "2483-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md"),
            "zero_condition": "parent normal form supplies a1=1/(2*kappa_MTS) before tests",
            "bound_condition": "treat G_ref as empirical coupling only after declaring effective route",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "RES2632_3_DeltaE_MTS",
            "residual": "DeltaE_MTS",
            "owner_status": "sum of non-EH local operator sectors",
            "source": str(ROOT / "2485-Y5-R2FR-parent-normal-form-field-symmetry-derivative-grammar.md"),
            "zero_condition": "parent derivative grammar, vertical-null proof, residual-sector silence and boundary class close",
            "bound_condition": "source-backed Newton/PPN/R10/clock/orbit bounds per sector",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "RES2632_4_DObs_e_R",
            "residual": "DObs_e_R",
            "owner_status": "observed coframe/readout leak for R_AB/q/private representatives",
            "source": str(ROOT / "2486-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md"),
            "zero_condition": "DObs_e[v_X]=0 follows from q_parent and terminal public coframe",
            "bound_condition": "finite no-shadow/common-frame PPN residual vector",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "RES2632_5_R11",
            "residual": "R11_residual_operator",
            "owner_status": "novel non-EH gravity branch retained",
            "source": str(ROOT / "1940-Y5-R2FR-EH-uniqueness-Lovelock-gate-or-R11-residual-operator.md"),
            "zero_condition": "MTS signs Lovelock assumptions and residual silence",
            "bound_condition": "define divergence law plus weak-field Newtonian/PPN projection",
            "valid_for_claim": "False",
        },
    ]


def route_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "RG2632_0_no_restart_wA_loop",
            "forbidden_shortcut": "redoing w_A source-prefactor loop as if 1890-1940 did not exist",
            "reason": "the old chain already localized source coupling and moved the main blocker to parent gravity operator/normal form",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2632_1_no_EH_import",
            "forbidden_shortcut": "using EH/GR success as proof MTS derives EH",
            "reason": "EH candidate gives conditional Newtonian limit but parent origin and kappa owner are unsigned",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2632_2_no_gamma_only",
            "forbidden_shortcut": "using Cassini gamma or a single PPN component as local-GR proof",
            "reason": "full PPN vector retains beta, preferred-frame, source, endpoint and readout channels",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2632_3_no_syntax_by_decree",
            "forbidden_shortcut": "declaring no-Hom/no-source-prefactor by taste rather than parent grammar",
            "reason": "object-language typing is useful only after parent sorts and coefficient codomains are derived",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2632_4_no_fitted_G",
            "forbidden_shortcut": "using measured G/GM to hide source or coupling residuals",
            "reason": "G_ref can calibrate an effective route, but cannot prove kappa_MTS or remove relative source weights",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2632_0_internal_rollforward",
            "claim": "2632 may guide private current-branch work",
            "gate_status": "ALLOW_INTERNAL_NONCLAIM",
            "why": "it imports already-executed coupling/EH evidence and prevents duplicate source-prefactor circling",
            "gate_pass": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2632_1_source_side_clean",
            "claim": "source side is solved as a parent theorem",
            "gate_status": "BLOCKED",
            "why": "candidate Hilbert matter side is conservation-compatible but parent action/preservation clauses remain unsigned",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2632_2_EH_operator",
            "claim": "MTS derives EH/kappa local operator",
            "gate_status": "BLOCKED",
            "why": "Lovelock assumptions, parent normal form, coefficient owner and residual silence are not signed",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2632_3_Newton_GR",
            "claim": "MTS derives Newton/local GR/PPN",
            "gate_status": "BLOCKED",
            "why": "needs EH/kappa or R11 law, q/DObs silence, source normalization, and full PPN vector closure",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2632_4_testing",
            "claim": "WEP/PPN/R10 tests are executable MTS prediction rows",
            "gate_status": "BLOCKED",
            "why": "finite residual parent values and arena projection kernels are missing",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2632_0_source_prefactor_route",
            "decision": "SOURCE_PREFACTOR_CHAIN_IMPORTED_DO_NOT_RESTART",
            "rationale": "1890-1940 already attacked w_A, no-Hom, action/current owner, WEP input and matter-source conservation.",
            "next_action": "use the imported result rather than burning cycles redoing the coupling hunt.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2632_1_gain",
            "decision": "MATTER_SOURCE_SIDE_IS_CONDITIONALLY_USEFUL",
            "rationale": "The old chain did not prove local GR, but it did produce a candidate Hilbert matter source with Ward conservation and source-weight guardrails.",
            "next_action": "keep this as the matter-side spine while attacking the operator/readout side.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2632_2_main_gap",
            "decision": "PARENT_NORMAL_FORM_AND_DOBS_ARE_NOW_THE_GR_FRONTIER",
            "rationale": "EH/kappa can be obtained conditionally, but parent normal form, coefficient owner, residual silence and DObs/no-shadow remain unsigned.",
            "next_action": "build a current-branch synthesis of EH normal form, quotient/DObs and full PPN residual closure.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2632_3_public_claim",
            "decision": "NO_PUBLIC_LOCAL_GR_OR_PPN_CLAIM",
            "rationale": "2632 is a correction and roll-forward checkpoint; it proves progress, not completion.",
            "next_action": "continue derivation-first with explicit residual ledgers.",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2633-Y5-R2FR-parent-normal-form-DObs-EH-current-branch-synthesis-or-full-PPN-residual-fill.md",
            "script": "scripts/Y5_R2FR_parent_normal_form_DObs_EH_current_branch_synthesis_or_full_PPN_residual_fill_2633.py",
            "objective": "synthesize the current local-GR proof obligations into one parent-normal-form gate: EH/kappa origin, q_parent/DObs_e no-shadow, residual-sector silence, source normalization, and full PPN vector closure; if any clause fails, keep the explicit residual owner row.",
            "include": "2483 EH/coupling residuals; 2484 uniqueness hypotheses; 2485 normal form skeleton; 2486 q/DObs theorem; 2489 full PPN vector; 2631 source-prefactor vector; 2632 rollforward",
            "exclude": "source-prefactor rerun, EH import as proof, fitted G/GM, gamma-only pass, syntax-by-decree no-Hom, closure-only local GR",
            "selected": "True",
            "valid_for_claim": "False",
        },
        {
            "next_target": "2633b-Y5-R2FR-WEP-input-pack-executable-runner.md",
            "script": "scripts/Y5_R2FR_WEP_input_pack_executable_runner_2633b.py",
            "objective": "held empirical fallback: make WEP row executable only after parent residual values, source worldtube, material tensor, readout/force map and tau_WEP are sourced.",
            "include": "1898 WEP row v1; 1899 input pack; MICROSCOPE bound anchor; source-cache validation",
            "exclude": "using WEP bound as prediction, tau=1 shortcut, source-worldtube point-source shortcut without theorem",
            "selected": "False",
            "valid_for_claim": "False",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        (
            "COPY2632_coupling_rollforward",
            "source_coupling_rollforward",
            OUTPUTS["coupling_rollforward"],
            LOCAL_BOUNDS / "Source_coupling_rollforward_2632_NONCLAIM.csv",
        ),
        (
            "COPY2632_gr_frontier",
            "local_gr_frontier_matrix",
            OUTPUTS["gr_frontier"],
            LOCAL_BOUNDS / "Local_GR_frontier_matrix_2632_NONCLAIM.csv",
        ),
        (
            "COPY2632_residual_owners",
            "residual_owner_ledger",
            OUTPUTS["residual_owners"],
            LOCAL_BOUNDS / "Residual_owner_ledger_2632_NONCLAIM.csv",
        ),
        (
            "COPY2632_next",
            "next_target",
            OUTPUTS["next_target"],
            RAB_QUEUE / "JR2632_PARENT_NORMAL_FORM_DOBS_EH_SYNTHESIS_NEXT.csv",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, label, source_path, destination_path in copy_specs:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        rows.append(
            {
                "copy_id": copy_id,
                "label": label,
                "source_path": str(source_path),
                "destination_path": str(destination_path),
                "destination_exists": bool_text(destination_path.exists()),
                "csv_parses": bool_text(csv_parses(destination_path)),
                "row_count": len(read_csv(destination_path)) if destination_path.exists() else 0,
            }
        )
    return rows


def any_claim_promoted(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                return True
    return False


def blocked_row_promoted(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    markers = ("MISSING_", "BLOCKED", "UNSIGNED", "NOT_DERIVED", "NONCLAIM", "CLOSURE")
    for rows in rows_by_name.values():
        for row in rows:
            row_text = " ".join(str(value) for value in row.values())
            promoted = row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True"
            if promoted and any(marker in row_text for marker in markers):
                return True
    return False


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for name, path in OUTPUTS.items() if name != "validation"]
    source_rows = rows_by_name["source_register"]
    roll_rows = rows_by_name["coupling_rollforward"]
    gr_rows = rows_by_name["gr_frontier"]
    residual_rows = rows_by_name["residual_owners"]
    guard_rows = rows_by_name["route_guards"]
    gate_rows = rows_by_name["claim_gates"]
    decision_rows_local = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]

    checks: list[tuple[str, bool, str]] = [
        (
            "VAL2632_00_sources",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2632_01_rollforward",
            any(row["rollforward_verdict"] == "OLD_CHAIN_ALREADY_ATTACKED_THIS_ROUTE" for row in roll_rows)
            and any(row["imported_status"] == "CANDIDATE_HILBERT_MATTER_SIDE_PASSES_CONSERVATION_NONCLAIM" for row in roll_rows),
            "source-prefactor chain and matter-source gain are imported",
        ),
        (
            "VAL2632_02_source_not_promoted",
            all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in roll_rows),
            "source-coupling rows remain nonclaim",
        ),
        (
            "VAL2632_03_gr_frontier",
            any(row["frontier_id"] == "GRF2632_1_EH_operator" and "BLOCKED" in row["status"] for row in gr_rows)
            and any(row["frontier_id"] == "GRF2632_3_quotient_readout" and "DOBS" in row["status"] for row in gr_rows),
            "EH operator and DObs/no-shadow are explicit current blockers",
        ),
        (
            "VAL2632_04_residual_owners",
            {"Delta_w_eff", "e_EH_import", "e_kappaG", "DeltaE_MTS", "DObs_e_R", "R11_residual_operator"}.issubset(
                {row["residual"] for row in residual_rows}
            ),
            "residual owner ledger includes source, EH, coupling, operator, DObs and R11 residuals",
        ),
        (
            "VAL2632_05_no_restart_guard",
            any(row["guard_id"] == "RG2632_0_no_restart_wA_loop" and row["machine_status"] == "FORBIDDEN" for row in guard_rows),
            "w_A rerun loop is guarded against",
        ),
        (
            "VAL2632_06_claim_gates",
            all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gate_rows),
            "no claim gate promotes local GR/PPN/WEP",
        ),
        (
            "VAL2632_07_decision",
            any(row["decision"] == "PARENT_NORMAL_FORM_AND_DOBS_ARE_NOW_THE_GR_FRONTIER" for row in decision_rows_local),
            "decision selects parent normal form and DObs as current GR frontier",
        ),
        (
            "VAL2632_08_next_target",
            any(row["selected"] == "True" and "2633" in row["next_target"] for row in next_rows),
            "2633 parent-normal-form/DObs/EH synthesis selected",
        ),
        (
            "VAL2632_09_no_claim_flags",
            not any_claim_promoted(rows_by_name),
            "no generated claim-sensitive row is promoted",
        ),
        (
            "VAL2632_10_blocked_not_ready",
            not blocked_row_promoted(rows_by_name),
            "no blocked/unsigned/nonclaim row is marked claim-ready",
        ),
        (
            "VAL2632_11_branch_copies",
            all(row["destination_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows),
            "branch/local/queue copies exist and parse",
        ),
        (
            "VAL2632_12_formalization_untouched",
            not any(str(path).startswith(str(FORMALIZATION)) for path in generated_paths + [DOC_PATH]),
            "no 2632 outputs are written under formalization-workbench",
        ),
        (
            "VAL2632_13_csv_parse",
            all(csv_parses(path) for path in generated_paths),
            "all generated 2632 CSVs parse",
        ),
        (
            "VAL2632_14_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    rows = [
        {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2632_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2632 source-prefactor rollforward to parent-normal-form/DObs/EH frontier",
            "valid_for_claim": "False",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    sections = [
        ("Source Register", rows_by_name["source_register"]),
        ("Source Coupling Rollforward", rows_by_name["coupling_rollforward"]),
        ("Local GR Frontier Matrix", rows_by_name["gr_frontier"]),
        ("Residual Owner Ledger", rows_by_name["residual_owners"]),
        ("Route Guards", rows_by_name["route_guards"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decision Ledger", rows_by_name["decision"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Branch Copies", rows_by_name["branch_copies"]),
        ("Validation", rows_by_name["validation"]),
    ]
    body = [
        "# 2632 - Y5 R2/f(R) No-Source-Prefactor Parent Action Clause Or PPN Component-Basis First Row",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Status: `Y5_R2FR_2632_source_prefactor_chain_imported_GR_frontier_shifted_to_parent_normal_form_DObs_EH_nonclaim`",
        "",
        "Claim ceiling: no local-GR/Newton proof, no PPN/WEP/R10 pass, no EH import-as-proof, no source-prefactor theorem-zero claim, no fitted `G/GM`, no gamma-only pass, no GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2632 corrects the trajectory. 2631 selected source-prefactor coupling as the next live seam, but the older 1890-1940 chain already attacked that seam hard.",
        "",
        "That chain did not close local GR. It did do something valuable: it sharpened the matter/source side into a candidate Hilbert action with Ward conservation and explicit source-weight residuals. The main blocker then moved to the gravity/operator/readout side.",
        "",
        "The current frontier is therefore not another `w_A` loop. It is one parent-normal-form gate: derive EH/kappa from MTS primitives, prove or bound every non-EH residual, and prove `q_parent/DObs_e` no-shadow so the full PPN vector can close without a gamma-only shortcut.",
        "",
    ]
    for title, rows in sections:
        body.extend([f"## {title}", "", markdown_table(rows), ""])
    body.extend(
        [
            "## Plain-English Verdict",
            "",
            "This is good news in a very specific way. The coupling hunt was not wasted; it graduated the problem. We now have a plausible matter-source spine, but the theory still needs to earn the gravitational operator and readout/no-shadow side.",
            "",
            "So the next honest attack is 2633: put EH/kappa origin, parent normal form, `q_parent/DObs_e`, residual-sector silence, and the full PPN vector into one gate. If that gate closes, local GR gets serious. If it fails, the residual branch is explicit and testable instead of mystical.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(body), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "coupling_rollforward": coupling_rollforward_rows(),
        "gr_frontier": gr_frontier_rows(),
        "residual_owners": residual_owner_rows(),
        "route_guards": route_guard_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
