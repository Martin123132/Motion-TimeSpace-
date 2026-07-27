from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2622-Y5-R2FR-Lovelock-hypothesis-audit-metric-only-second-order-or-residual-bounds.md"

PREFIX = "P8_Y5_LOVELOCK_GATE_2622"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage_ledger": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "relative_theorem": RESIDUALS / f"{PREFIX}_RELATIVE_THEOREM_REGISTER.csv",
    "hypothesis_audit": RESIDUALS / f"{PREFIX}_HYPOTHESIS_AUDIT.csv",
    "parent_signature": RESIDUALS / f"{PREFIX}_PARENT_SIGNATURE_GAP_MATRIX.csv",
    "operator_selection": RESIDUALS / f"{PREFIX}_OPERATOR_SELECTION_VERDICT.csv",
    "residual_fallback": RESIDUALS / f"{PREFIX}_RESIDUAL_FALLBACK_MATRIX.csv",
    "countermodel": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2622_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2622_00_2621_handoff_doc",
        "description": "2621 selects Lovelock-hypothesis audit as the next target",
        "path": ROOT / "2621-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
        "needles": ["NEXT2621_0_primary", "LOVEL0CK_HYPOTHESIS_AUDIT_IS_NEXT", "VER2621_7_overall"],
    },
    {
        "source_id": "SRC2622_01_2621_validation",
        "description": "2621 validation passed",
        "path": RESIDUALS / "P8_Y5_BRR545_2621_VALIDATION.csv",
        "needles": ["VAL2621_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2622_02_2621_lovelock_audit",
        "description": "2621 initial Lovelock hypothesis audit",
        "path": RESIDUALS / "P8_Y5_SECTOR_VARIATION_GATE_2621_LOVEL0CK_HYPOTHESIS_AUDIT.csv",
        "needles": ["LOV2621_1_metric_only", "LOV2621_4_next"],
    },
    {
        "source_id": "SRC2622_03_2621_deltae_norm",
        "description": "2621 DeltaE symbolic norm pack",
        "path": RESIDUALS / "P8_Y5_SECTOR_VARIATION_GATE_2621_DELTAE_RESIDUAL_NORM_PACK.csv",
        "needles": ["NORM2621_0_total", "SYMBOLIC_BOUND_ONLY_NONCLAIM"],
    },
    {
        "source_id": "SRC2622_04_962_relative_R2FR",
        "description": "R2/fR relative zero theorem",
        "path": ROOT / "962-Y5-R10-R2-fR-zero-clause-proof-or-scalar-mode-bound-source-acquisition.md",
        "needles": ["R2Z962_5_relative_zero_theorem", "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED"],
    },
    {
        "source_id": "SRC2622_05_963_parent_signature",
        "description": "parent second-order/no-extra-scalar signature audit",
        "path": ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
        "needles": ["DO963_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS", "NES963_5_verdict"],
    },
    {
        "source_id": "SRC2622_06_964_minimality",
        "description": "parent no-higher-derivative/minimality theorem attempt",
        "path": ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
        "needles": ["MIN964_5_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS", "CM964_0_EH_plus_R2"],
    },
    {
        "source_id": "SRC2622_07_439_premise_ladder",
        "description": "EH-only exterior parent-premise ladder",
        "path": ROOT / "439-EH-only-exterior-parent-premise-ladder.md",
        "needles": ["P6_second_order_metric_equations", "conditional_theorem_shape", "local GR"],
    },
    {
        "source_id": "SRC2622_08_440_sector_reduction",
        "description": "metric-only second-order sector reduction attempt",
        "path": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
        "needles": ["metric_only_second_order_derived", "fail", "Every extra sector"],
    },
]


def ensure_dirs() -> None:
    for path in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        rows.append(
            {
                "source_id": source["source_id"],
                "description": source["description"],
                "source_path": str(source["path"]),
                "exists": exists,
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": False,
            }
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    return [
        {
            "lineage_id": "LIN2622_0_current_handoff",
            "input_checkpoint": "2621",
            "what_it_gave": "sector-resolved DeltaE and selected Lovelock-hypothesis audit",
            "current_use": "test whether several residual sectors can be killed by the GR uniqueness route",
            "claim_status": "nonclaim_handoff",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2622_1_relative_R2FR_win",
            "input_checkpoint": "962",
            "what_it_gave": "nonlinear f(R)/R2 produces higher derivatives or scalar trace pole unless parent is exact second-order metric-only with no scalar",
            "current_use": "treat this as a real relative theorem, not as absolute MTS proof",
            "claim_status": "relative_theorem_parent_unsigned",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2622_2_signature_blocker",
            "input_checkpoint": "963-964",
            "what_it_gave": "parent second-order/no-extra-scalar/minimality signature remains unsigned",
            "current_use": "identify the exact missing parent lock for the Lovelock route",
            "claim_status": "absolute_parent_signature_missing",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2622_3_old_premise_ladder",
            "input_checkpoint": "439-440",
            "what_it_gave": "explicit EH-only exterior rungs and sector reduction failures",
            "current_use": "avoid pretending same-frame conservation or Ward identity alone implies EH",
            "claim_status": "premise_ladder_retained",
            "valid_for_claim": False,
        },
    ]


def relative_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "REL2622_0_lovelock_template",
            "theorem": "4D local metric-only second-order divergence-free LHS implies Einstein plus Lambda",
            "formal_statement": "If H_4D, H_metric_only, H_local, H_second_order, H_div_free, and H_boundary_silent hold, then E_munu=a G_munu + b g_munu.",
            "status": "REFERENCE_TEMPLATE_CONDITIONAL",
            "what_it_kills_if_parent_signed": "generic non-EH local metric operators in the compact ordinary exterior",
            "remaining_gap": "MTS has not signed the hypotheses",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "REL2622_1_R2FR_scalar_filter",
            "theorem": "R2/fR scalar-mode relative zero theorem",
            "formal_statement": "If the parent exterior branch is exactly local, metric-only, second-order, and has no retained scalar, then f_RR=0 locally and c_R2=c_fR=0.",
            "status": "RELATIVE_THEOREM_READY_PARENT_PREMISE_UNSIGNED",
            "what_it_kills_if_parent_signed": "R2/fR scalaron branch and finite scalar-mode Yukawa tail",
            "remaining_gap": "parent no-extra-scalar and no-integrated-out-tower signatures are unsigned",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "REL2622_2_no_hidden_tower_condition",
            "theorem": "integrating out fields must not regenerate non-EH operators",
            "formal_statement": "For every eliminated sector Z_A, S_eff[g]=S_parent[g,Z_A[g]] must not generate R2, Ricci2, Weyl2, f(R), or nonlocal kernels.",
            "status": "REQUIRED_GUARD_NOT_PROVED",
            "what_it_kills_if_parent_signed": "auxiliary scalar and memory-kernel countermodels",
            "remaining_gap": "no universal no-integrated-out-curvature-tower theorem",
            "valid_for_claim": False,
        },
    ]


def hypothesis_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "hypothesis_id": "HYP2622_0_4D",
            "hypothesis": "local tested branch is four-dimensional",
            "needed_evidence": "compact ordinary exterior/readout uses a 4D observed metric and no hidden dimension contributes to local operator",
            "current_verdict": "CONDITIONAL_PASS_FOR_LOCAL_TESTS_NOT_GLOBAL_PROOF",
            "evidence_strength": "moderate",
            "failure_mode": "global/cosmology branch may carry extra structure",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2622_1_observed_frame",
            "hypothesis": "one observed metric/coframe is selected before matter readout",
            "needed_evidence": "parent-selected observed frame and matter clock/light coupling in that same frame",
            "current_verdict": "PARTLY_STRUCTURED_PARENT_UNSIGNED",
            "evidence_strength": "partial",
            "failure_mode": "field redefinition can move residuals between geometry and matter/source sectors",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2622_2_metric_only",
            "hypothesis": "extra MTS/time/memory/projector/coframe variables are absent, gauge, auxiliary-harmless, or no-haired",
            "needed_evidence": "each nonmetric sector has zero Euler variation or cannot regenerate metric operators after elimination",
            "current_verdict": "FAIL_TO_BOUND",
            "evidence_strength": "blocked",
            "failure_mode": "memory/coframe/projector/nonlocal sectors remain live",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2622_3_second_order",
            "hypothesis": "field equations for the observed metric are at most second order",
            "needed_evidence": "R2/fR/Ricci2/Weyl2/nonlocal operators are forbidden, topological, decoupled, or coefficient-bounded",
            "current_verdict": "FAIL_TO_BOUND",
            "evidence_strength": "blocked",
            "failure_mode": "higher-curvature and nonlocal operators remain legal countermodels",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2622_4_divergence_free",
            "hypothesis": "complete LHS is Noether/Bianchi-compatible",
            "needed_evidence": "complete diffeomorphism-invariant parent action variation with no illegal dropped residual terms",
            "current_verdict": "PARTLY_STRUCTURED_NOT_SIGNED",
            "evidence_strength": "partial",
            "failure_mode": "dropping residual sectors can break the identity unless balanced",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2622_5_boundary_topological",
            "hypothesis": "boundary/topological pieces are harmless in the compact local branch",
            "needed_evidence": "fixed topology, compact-support variations, fixed-before-readout reference, and boundary silence",
            "current_verdict": "NONCLAIM_BOUND_REQUIRED",
            "evidence_strength": "blocked",
            "failure_mode": "boundary/reference terms can fake mass/potential readout",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2622_6_no_integrated_out_tower",
            "hypothesis": "eliminated sectors cannot regenerate higher-curvature or scalar-tensor operators",
            "needed_evidence": "no natural marker/scalar extension and no auxiliary sector whose solution feeds back as R2/fR/nonlocal terms",
            "current_verdict": "FAIL_TO_BOUND",
            "evidence_strength": "blocked",
            "failure_mode": "auxiliary scalar, marker-prefactor, and nonlocal memory countermodels remain legal",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2622_7_overall",
            "hypothesis": "Lovelock-style route closes local GR LHS",
            "needed_evidence": "all preceding hypotheses pass parent-signed",
            "current_verdict": "LOCAL_GR_LHS_NOT_CLOSED",
            "evidence_strength": "insufficient",
            "failure_mode": "metric-only, second-order, and no-integrated-out-tower are not proven",
            "valid_for_claim": False,
        },
    ]


def parent_signature_gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "gap_id": "GAP2622_0_minimal_quotient",
            "gap": "primitive quotient/no-natural-marker theorem",
            "why_needed": "forbids appending scalar or material marker fields that can multiply R",
            "current_status": "NOT_DERIVED",
            "if_failed": "retain scalar-tensor/f(R)-like coefficient rows",
            "valid_for_claim": False,
        },
        {
            "gap_id": "GAP2622_1_no_scalar_prefactor",
            "gap": "no quotient/class scalar multiplies EH prefactor",
            "why_needed": "F(sigma)R creates variable G, scalar PPN, WEP/clock, and R10 tails",
            "current_status": "CANDIDATE_CLAUSE_NOT_PARENT_SIGNED",
            "if_failed": "retain delta_AEH_scalar and finite scalar-mode bounds",
            "valid_for_claim": False,
        },
        {
            "gap_id": "GAP2622_2_no_integrated_out_tower",
            "gap": "eliminated auxiliary/projector/memory sectors do not generate curvature towers",
            "why_needed": "a second-order parent can still generate higher-curvature observed action after solving hidden fields",
            "current_status": "NOT_DERIVED",
            "if_failed": "retain R2/Ricci/Weyl/nonlocal operator coefficients",
            "valid_for_claim": False,
        },
        {
            "gap_id": "GAP2622_3_connection_compatibility",
            "gap": "Levi-Civita observed connection",
            "why_needed": "torsion/nonmetricity would evade metric-only Lovelock assumptions and affect clocks/light/spin",
            "current_status": "NOT_CLOSED_IN_THIS_BRANCH",
            "if_failed": "retain torsion/nonmetricity local operator rows",
            "valid_for_claim": False,
        },
    ]


def operator_selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "operator_id": "OPS2622_0_EH_Lambda",
            "operator": "G_munu + Lambda g_munu",
            "selection_status": "TARGET_OPERATOR_CONDITIONAL",
            "selection_rule": "selected if Lovelock hypotheses all pass",
            "claim_status": "not_parent_proved",
            "valid_for_claim": False,
        },
        {
            "operator_id": "OPS2622_1_R2_fR",
            "operator": "R2/f(R) scalar curvature tower",
            "selection_status": "RELATIVE_ZERO_IF_PARENT_SIGNATURE_SIGNED",
            "selection_rule": "killed by exact metric-only second-order no-extra-scalar theorem",
            "claim_status": "boxed_not_killed",
            "valid_for_claim": False,
        },
        {
            "operator_id": "OPS2622_2_Ricci_Weyl",
            "operator": "Ricci^2/Weyl^2/higher curvature",
            "selection_status": "NONCLAIM_BOUND_REQUIRED",
            "selection_rule": "requires second-order operator exclusion or coefficient bounds",
            "claim_status": "retained",
            "valid_for_claim": False,
        },
        {
            "operator_id": "OPS2622_3_projector_memory_nonlocal",
            "operator": "projector/memory/nonlocal residual operators",
            "selection_status": "NONCLAIM_BOUND_REQUIRED",
            "selection_rule": "requires metric-only/no-integrated-out-tower proof or residual maps",
            "claim_status": "retained",
            "valid_for_claim": False,
        },
        {
            "operator_id": "OPS2622_4_overall",
            "operator": "E_LHS local branch",
            "selection_status": "EH_NOT_SELECTED_AS_MTS_THEOREM",
            "selection_rule": "hypothesis audit blocks promotion",
            "claim_status": "local_GR_not_claimed",
            "valid_for_claim": False,
        },
    ]


def residual_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "fallback_id": "RFB2622_0_scalar_tower",
            "residual": "c_R2,c_fR,delta_AEH_scalar",
            "trigger": "metric-only/no-extra-scalar/no-marker proof fails",
            "required_bound_inputs": "scalar mass/coupling, R10 alpha(lambda), PPN gamma/beta, WEP/clock maps",
            "status": "NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "fallback_id": "RFB2622_1_higher_curvature",
            "residual": "c_Ricci2,c_Weyl2,c_boxR",
            "trigger": "second-order operator exclusion fails",
            "required_bound_inputs": "operator basis, units, wave/PPN/R10/cosmology maps",
            "status": "NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "fallback_id": "RFB2622_2_extra_fields",
            "residual": "c_projector,c_memory,c_frame,c_nonlocal",
            "trigger": "metric-only/no-integrated-out-tower proof fails",
            "required_bound_inputs": "frame-lock, commutator norms, kernel decay, preferred-frame maps",
            "status": "NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "fallback_id": "RFB2622_3_boundary_connection",
            "residual": "c_boundary,c_torsion,c_nonmetricity",
            "trigger": "boundary silence or Levi-Civita compatibility fails",
            "required_bound_inputs": "boundary reference certificate, spin/light/clock/torsion maps",
            "status": "NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2622_0_EH_plus_R2",
            "failure_mode": "local 4D diffeo-invariant metric theory with EH plus small R2",
            "mathematical_form": "S=S_EH+epsilon int sqrt(-g) R^2",
            "retained": True,
            "why_survives": "metric-only and divergence-free do not by themselves enforce second-order equations if R2 is allowed",
            "what_kills_it": "parent second-order/no-extra-scalar theorem or sourced scalar-mode bound",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2622_1_auxiliary_scalar_tower",
            "failure_mode": "auxiliary scalar appears harmless before elimination but generates R2",
            "mathematical_form": "S=S_EH+int sqrt(-g)(-M^2 phi^2/2+beta phi R)",
            "retained": True,
            "why_survives": "solving phi can generate beta^2 R^2/(2M^2)",
            "what_kills_it": "no-integrated-out-curvature-tower theorem",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2622_2_marker_prefactor",
            "failure_mode": "quotient-invariant marker scalar multiplies R",
            "mathematical_form": "S=int sqrt(-g) F(sigma_marker) R + S_sigma",
            "retained": True,
            "why_survives": "primitive quotient/no-natural-marker theorem is not derived",
            "what_kills_it": "minimal quotient theorem or scalar-prefactor bound rows",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2622_3_nonlocal_memory",
            "failure_mode": "memory kernel creates nonlocal scalar response",
            "mathematical_form": "S=S_EH+int sqrt(-g) R Box^{-1} R or compact kernel analogue",
            "retained": True,
            "why_survives": "memory/nonlocal sector is live in 2621",
            "what_kills_it": "locality reduction or kernel-bound theorem",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2622_4_verdict",
            "failure_mode": "Lovelock route remains conditional",
            "mathematical_form": "hypotheses H_metric_only, H_second_order, H_no_tower fail-to-bound",
            "retained": True,
            "why_survives": "2622 does not parent-sign the decisive hypotheses",
            "what_kills_it": "2623 primitive quotient/no-marker/no-integrated-out-tower closure",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2622_0_lovelock_hypotheses",
            "claim": "Lovelock-style hypotheses hold for MTS local branch",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_METRIC_ONLY_SECOND_ORDER_NO_TOWER_UNSIGNED",
        },
        {
            "gate_id": "GATE2622_1_EH_operator_selected",
            "claim": "EH plus Lambda is selected by parent theorem",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_OPERATOR_SELECTION_NOT_PROVED",
        },
        {
            "gate_id": "GATE2622_2_R2FR_zero",
            "claim": "R2/fR scalar branch is theorem-zero in MTS",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_SECOND_ORDER_NO_EXTRA_SCALAR_UNSIGNED",
        },
        {
            "gate_id": "GATE2622_3_local_GR",
            "claim": "local GR/Newton branch is derived",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_LOVELOCK_AND_SOURCE_NORMALIZATION_GATES_OPEN",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2622_0_relative_win",
            "decision": "R2FR_AND_LOVELOCK_RELATIVE_THEOREMS_ARE_USEFUL",
            "reason": "if parent hypotheses are signed, EH selection and R2/fR zero follow cleanly",
            "next_action": "do not throw away these theorems; attack the parent hypotheses directly",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2622_1_absolute_block",
            "decision": "LOCAL_GR_NOT_CLAIMED",
            "reason": "metric-only, second-order, and no-integrated-out-tower hypotheses remain unsigned",
            "next_action": "keep DeltaE residual coefficients retained",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2622_2_best_next",
            "decision": "PRIMITIVE_QUOTIENT_NO_MARKER_NO_TOWER_IS_NEXT",
            "reason": "this is the exact parent lock that could make the Lovelock/R2FR relative theorem absolute",
            "next_action": "build 2623 primitive quotient/no-natural-marker/no-integrated-out-tower audit or residual-bound fallback",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2622_0_primary",
            "selection_status": "selected",
            "target_doc": "2623-Y5-R2FR-primitive-quotient-no-natural-marker-no-integrated-out-tower-or-residual-bounds.md",
            "target_script": "scripts/Y5_R2FR_primitive_quotient_no_natural_marker_no_integrated_out_tower_or_residual_bounds_2623.py",
            "objective": "prove the primitive quotient/no-natural-marker/no-integrated-out-tower theorem that would parent-sign metric-only second-order EH selection, or retain scalar/higher-curvature residual bounds",
            "acceptance_gate": "no marker scalar, no scalar EH prefactor, and no eliminated sector can regenerate R2/fR/Ricci/Weyl/nonlocal operators; otherwise residual rows remain nonclaim",
            "claim_policy": "no local-GR or R2/fR zero claim unless these parent locks close",
            "valid_for_claim": False,
        },
        {
            "route_id": "NEXT2622_1_fallback",
            "selection_status": "held_fallback",
            "target_doc": "2623b-Y5-R2FR-operator-coefficient-source-bound-pack.md",
            "target_script": "scripts/Y5_R2FR_operator_coefficient_source_bound_pack_2623b.py",
            "objective": "source coefficient bounds for residual operators if primitive quotient/minimality proof fails",
            "acceptance_gate": "each coefficient has units, source path, observable map, and valid_for_claim=false until numeric/source-backed",
            "claim_policy": "fallback only; derivation route remains preferred",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "relative": relative_theorem_rows(),
        "hypotheses": hypothesis_audit_rows(),
        "gaps": parent_signature_gap_rows(),
        "operators": operator_selection_rows(),
        "fallback": residual_fallback_rows(),
        "countermodel": countermodel_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
        "branch_copies": [],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_parse(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return True, sum(1 for _ in csv.DictReader(handle))
    except Exception:
        return False, 0


def copy_outputs() -> list[dict[str, Any]]:
    specs = [
        ("COPY2622_hypothesis_audit", "hypothesis_audit", OUTPUTS["hypothesis_audit"], LOCAL_BOUNDS / "Lovelock_hypothesis_audit_2622_NONCLAIM.csv"),
        ("COPY2622_relative_theorem", "relative_theorem", OUTPUTS["relative_theorem"], LOCAL_BOUNDS / "Lovelock_relative_theorem_register_2622_NONCLAIM.csv"),
        ("COPY2622_parent_signature", "parent_signature", OUTPUTS["parent_signature"], LOCAL_BOUNDS / "Parent_signature_gap_matrix_2622_NONCLAIM.csv"),
        ("COPY2622_residual_fallback", "residual_fallback", OUTPUTS["residual_fallback"], LOCAL_BOUNDS / "Residual_fallback_matrix_2622_NONCLAIM.csv"),
        ("COPY2622_next_target", "next_target", OUTPUTS["next_target"], RAB_QUEUE / "JR2622_PRIMITIVE_QUOTIENT_NO_MARKER_NEXT.csv"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_key, source, target in specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        parsed, row_count = csv_parse(target)
        rows.append(
            {
                "copy_id": copy_id,
                "source_key": source_key,
                "copy_path": str(target),
                "copy_exists": target.exists(),
                "csv_parse": parsed,
                "row_count": row_count,
                "valid_for_claim": False,
            }
        )
    return rows


def sources_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(row["exists"] and row["needles_present"] for row in rows_map["sources"])


def relative_theorems_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    ids = {row["theorem_id"] for row in rows_map["relative"]}
    return {"REL2622_0_lovelock_template", "REL2622_1_R2FR_scalar_filter"}.issubset(ids) and all(
        not bool(row["valid_for_claim"]) for row in rows_map["relative"]
    )


def hypothesis_audit_complete(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    ids = {row["hypothesis_id"] for row in rows_map["hypotheses"]}
    required = {f"HYP2622_{index}_{suffix}" for index, suffix in [
        (0, "4D"),
        (1, "observed_frame"),
        (2, "metric_only"),
        (3, "second_order"),
        (4, "divergence_free"),
        (5, "boundary_topological"),
        (6, "no_integrated_out_tower"),
        (7, "overall"),
    ]}
    return required.issubset(ids)


def local_gr_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["hypothesis_id"] == "HYP2622_7_overall"
        and row["current_verdict"] == "LOCAL_GR_LHS_NOT_CLOSED"
        and not bool(row["valid_for_claim"])
        for row in rows_map["hypotheses"]
    )


def decisive_hypotheses_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    decisive = {"HYP2622_2_metric_only", "HYP2622_3_second_order", "HYP2622_6_no_integrated_out_tower"}
    rows = [row for row in rows_map["hypotheses"] if row["hypothesis_id"] in decisive]
    return len(rows) == 3 and all(row["current_verdict"] == "FAIL_TO_BOUND" for row in rows)


def parent_gaps_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["gap_id"] == "GAP2622_2_no_integrated_out_tower" for row in rows_map["gaps"]) and all(
        not bool(row["valid_for_claim"]) for row in rows_map["gaps"]
    )


def operator_selection_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["operator_id"] == "OPS2622_4_overall"
        and row["selection_status"] == "EH_NOT_SELECTED_AS_MTS_THEOREM"
        for row in rows_map["operators"]
    )


def residual_fallback_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return len(rows_map["fallback"]) >= 4 and all(row["status"] == "NONCLAIM_BOUND_REQUIRED" for row in rows_map["fallback"])


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["countermodel_id"] == "CM2622_4_verdict" and bool(row["retained"]) for row in rows_map["countermodel"])


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(not bool(row["claim_allowed"]) and row["status"] == "BLOCKED" for row in rows_map["claim_gates"])


def generated_rows_have_no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_like_keys = {"valid_for_claim", "claim_allowed", "score_ready", "claim_ready", "public_claim_allowed"}
    for rows in rows_map.values():
        for row in rows:
            for field, value in row.items():
                if field in claim_like_keys and bool(value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            joined = " ".join(str(value) for value in row.values())
            if "MISSING_" in joined and bool(row.get("valid_for_claim", False)):
                return False
            if "MISSING_" in joined and str(row.get("current_status", "")).upper() == "READY":
                return False
    return True


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["decision_id"] == "DEC2622_2_best_next"
        and row["decision"] == "PRIMITIVE_QUOTIENT_NO_MARKER_NO_TOWER_IS_NEXT"
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["route_id"] == "NEXT2622_0_primary" and row["selection_status"] == "selected" for row in rows_map["next"])


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2622*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def csv_parse_all() -> bool:
    return all(csv_parse(path)[0] for key, path in OUTPUTS.items() if key != "validation" and path.exists())


def branch_copies_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return bool(rows_map["branch_copies"]) and all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"])


def check_row(check_id: str, passed: bool, detail: str, blocker: str = "") -> dict[str, Any]:
    return {
        "check_id": check_id,
        "result": "PASS" if passed else "FAIL",
        "detail": detail if passed else blocker,
        "valid_for_claim": False,
    }


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = [
        check_row("VAL2622_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present", "one or more cited source paths or needles missing"),
        check_row("VAL2622_01_relative_theorems_retained", relative_theorems_retained(rows_map), "relative Lovelock/R2FR theorem rows retained as nonclaim", "relative theorem rows missing or promoted"),
        check_row("VAL2622_02_hypothesis_audit_complete", hypothesis_audit_complete(rows_map), "all Lovelock hypothesis rows are present", "hypothesis audit incomplete"),
        check_row("VAL2622_03_local_gr_not_promoted", local_gr_not_promoted(rows_map), "local GR LHS remains unclosed/nonclaim", "local GR was promoted"),
        check_row("VAL2622_04_decisive_hypotheses_blocked", decisive_hypotheses_blocked(rows_map), "metric-only, second-order, and no-tower hypotheses fail-to-bound", "decisive hypotheses not marked blocked"),
        check_row("VAL2622_05_parent_gaps_retained", parent_gaps_retained(rows_map), "parent signature gaps retained", "parent signature gap rows missing or promoted"),
        check_row("VAL2622_06_operator_selection_nonclaim", operator_selection_nonclaim(rows_map), "EH operator not selected as MTS theorem", "operator selection was promoted"),
        check_row("VAL2622_07_residual_fallback_retained", residual_fallback_retained(rows_map), "residual fallback rows retained as nonclaim bounds", "residual fallback rows missing or promoted"),
        check_row("VAL2622_08_countermodel_retained", countermodel_retained(rows_map), "Lovelock countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL2622_09_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim", "one or more claim gates opened"),
        check_row("VAL2622_10_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL2622_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row("VAL2622_12_formalization_untouched", no_formalization_artifacts(), "no 2622 outputs found under formalization-workbench", "2622 outputs found under formalization-workbench"),
        check_row("VAL2622_13_decision_next", decision_next(rows_map), "decision selects primitive quotient/no-marker/no-tower route", "decision route missing"),
        check_row("VAL2622_14_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL2622_15_branch_copies", branch_copies_pass(rows_map), "branch/local/queue copies exist and parse", "branch copies missing or malformed"),
        check_row("VAL2622_16_csv_parse", csv_parse_all(), "all generated 2622 CSVs parse", "one or more generated 2622 CSVs fail to parse"),
        check_row("VAL2622_17_pycache_absent", pycache_absent(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
    ]
    overall = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2622_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2622 Lovelock hypothesis audit metric-only second-order or residual bounds",
            "valid_for_claim": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validations: list[dict[str, Any]]) -> str:
    sections = [
        "# 2622 - Lovelock Hypothesis Audit Metric Only Second Order Or Residual Bounds",
        "## Summary\n"
        "- 2622 tests the lowest-scrutiny GR route: make the local MTS branch satisfy the hypotheses that select Einstein plus Lambda.\n"
        "- The relative theorem stack is genuinely useful: if the parent branch is local, 4D, metric-only, second-order, divergence-free, and has no hidden scalar/tower, EH selection and R2/fR zero follow conditionally.\n"
        "- Current evidence does not parent-sign the decisive hypotheses: metric-only, second-order, and no-integrated-out-tower remain fail-to-bound.\n"
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "description", "source_path", "exists", "needles_present"]),
        "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "what_it_gave", "current_use", "claim_status"]),
        "## Relative Theorem Register\n" + markdown_table(rows_map["relative"], ["theorem_id", "theorem", "formal_statement", "status", "what_it_kills_if_parent_signed", "remaining_gap"]),
        "## Hypothesis Audit\n" + markdown_table(rows_map["hypotheses"], ["hypothesis_id", "hypothesis", "needed_evidence", "current_verdict", "evidence_strength", "failure_mode"]),
        "## Parent Signature Gap Matrix\n" + markdown_table(rows_map["gaps"], ["gap_id", "gap", "why_needed", "current_status", "if_failed"]),
        "## Operator Selection Verdict\n" + markdown_table(rows_map["operators"], ["operator_id", "operator", "selection_status", "selection_rule", "claim_status"]),
        "## Residual Fallback Matrix\n" + markdown_table(rows_map["fallback"], ["fallback_id", "residual", "trigger", "required_bound_inputs", "status"]),
        "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "failure_mode", "mathematical_form", "retained", "why_survives", "what_kills_it"]),
        "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "claim_allowed", "status", "blocker"]),
        "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
        "## Next Target\n" + markdown_table(rows_map["next"], ["route_id", "selection_status", "target_doc", "target_script", "objective", "acceptance_gate", "claim_policy"]),
        "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
        "## Validation\n" + markdown_table(validations, ["check_id", "result", "detail", "valid_for_claim"]),
        "## Verdict\n"
        "This is a useful narrowing, not a pass. The good news is that the GR route is now mathematically crisp: sign the parent hypotheses and EH/R2FR selection follows conditionally. The hard news is that the decisive parent locks are still unsigned. The next best derivation target is the primitive quotient/no-natural-marker/no-integrated-out-tower theorem, because that is what can stop hidden scalar or curvature towers from re-entering the local branch.",
    ]
    return "\n\n".join(sections) + "\n"


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["relative_theorem"], rows_map["relative"])
    write_csv(OUTPUTS["hypothesis_audit"], rows_map["hypotheses"])
    write_csv(OUTPUTS["parent_signature"], rows_map["gaps"])
    write_csv(OUTPUTS["operator_selection"], rows_map["operators"])
    write_csv(OUTPUTS["residual_fallback"], rows_map["fallback"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["claim_gates"], rows_map["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], rows_map["decisions"])
    write_csv(OUTPUTS["next_target"], rows_map["next"])
    rows_map["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_map["branch_copies"])
    validations = validation_rows(rows_map)
    write_csv(OUTPUTS["validation"], validations)
    DOC_PATH.write_text(build_markdown(rows_map, validations), encoding="utf-8")
    print(f"2622 validation {validations[-1]['result']}")
    print(f"doc={DOC_PATH}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
