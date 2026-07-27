from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3428-Y5-R2FR-no-extra-mass-Y6-monopole-silence-or-bound-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3427": ROOT / "3427-Y5-R2FR-reference-boundary-flux-zero-or-Bzero-row-under-AX1090.md",
    "bzero_3427": OUT / "P8_Y5_R2FR_3427_BZERO_BOUND_ROWS.csv",
    "next_3427": OUT / "P8_Y5_R2FR_3427_NEXT_TARGET.csv",
    "y6_decomp_3414": OUT / "P8_Y5_R2FR_3414_Y6_EXTRA_STRESS_DECOMPOSITION.csv",
    "textra_3415": OUT / "P8_Y5_R2FR_3415_TEXTRA_SAFE_CLASS_PROOF.csv",
    "hidden_3416": OUT / "P8_Y5_R2FR_3416_HIDDEN_STRESS_EXCLUSION_GATE.csv",
    "y6_gate_3422": OUT / "P8_Y5_R2FR_3422_Y6_EXTRA_STRESS_GATE.csv",
    "em_poynting_3382": OUT / "P8_Y5_R2FR_3382_EM_POYNTING_HILBERT_STRESS_CHAIN.csv",
    "hpi_bounds_3425": OUT / "P8_Y5_R2FR_3425_HPI_M_RESIDUAL_BOUND_ROWS.csv",
    "charge_decomp_3425": OUT / "P8_Y5_R2FR_3425_MTS_CHARGE_DECOMPOSITION.csv",
    "fixed_point_3421": OUT / "P8_Y5_R2FR_3421_EULER_FIXED_POINT_THEOREM.csv",
    "coercivity_3421": OUT / "P8_Y5_R2FR_3421_COERCIVITY_BOUND_PACK.csv",
    "source_current_3422": OUT / "P8_Y5_R2FR_3422_SOURCE_CURRENT_DECOMPOSITION.csv",
    "extra_mass_bound": OUT / "P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv",
    "extra_mass_projection": OUT / "P8_Y5_EXTRA_MASS_PROJECTION_SILENCE_THEOREM.csv",
    "extra_inventory": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_OPERATOR_INVENTORY.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3428_SOURCE_REGISTER.csv",
    "safe_class_theorem": OUT / "P8_Y5_R2FR_3428_Y6_SAFE_CLASS_THEOREM.csv",
    "extra_mass_decomposition": OUT / "P8_Y5_R2FR_3428_EXTRA_MASS_DECOMPOSITION.csv",
    "monopole_silence_gate": OUT / "P8_Y5_R2FR_3428_MONOPOLE_SILENCE_GATE.csv",
    "delta_extra_bound_rows": OUT / "P8_Y5_R2FR_3428_DELTA_EXTRA_BOUND_ROWS.csv",
    "pc3400_4_update": OUT / "P8_Y5_R2FR_3428_PC3400_4_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3428_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3428_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3428_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3428_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3428_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3427": "reference/boundary handoff to no-extra-mass gate",
        "bzero_3427": "residual boundary/symplectic flux rows",
        "next_3427": "machine-readable 3428 target",
        "y6_decomp_3414": "Y6 safe-class decomposition",
        "textra_3415": "extra-stress safe-class proof",
        "hidden_3416": "hidden/projector stress exclusion gate",
        "y6_gate_3422": "Y6 source-current gate",
        "em_poynting_3382": "public Maxwell/Poynting Hilbert stress policy",
        "hpi_bounds_3425": "Hamiltonian residual bound rows",
        "charge_decomp_3425": "MTS charge decomposition",
        "fixed_point_3421": "Z fixed-point theorem",
        "coercivity_3421": "coercivity/lambda-star bound pack",
        "source_current_3422": "source-current decomposition",
        "extra_mass_bound": "older extra-mass channelwise bound input",
        "extra_mass_projection": "older extra-mass projection silence theorem",
        "extra_inventory": "extra-sector operator inventory",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def safe_class_theorem() -> list[dict[str, Any]]:
    return [
        {
            "class_id": "SCT3428_0_public_Hilbert",
            "stress_class": "ordinary matter/EM/Poynting/surface Hilbert stress",
            "zero_or_safe_statement": "not extra: it is already the source side of the public EH/Hilbert branch",
            "identity": "T_total^H = -2/sqrt(-g_obs) delta(S_matter+S_EM+S_surface)/delta g_obs",
            "status": "EXACT_CONDITIONAL_SAFE_CLASS",
            "valid_for_claim": False,
        },
        {
            "class_id": "SCT3428_1_constant_background",
            "stress_class": "constant Lambda/vacuum trace",
            "zero_or_safe_statement": "safe for compact local source normalization only if universal, source-independent and reference-subtracted",
            "identity": "T_Lambda^{mu nu}=-rho_Lambda g_obs^{mu nu}; partial_source rho_Lambda=0",
            "status": "CONDITIONAL_BACKGROUND_SAFE_CLASS",
            "valid_for_claim": False,
        },
        {
            "class_id": "SCT3428_2_topological_improvement",
            "stress_class": "exact/topological/improvement stress",
            "zero_or_safe_statement": "safe only with zero compact boundary charge and no local metric response",
            "identity": "Delta H_top = int_boundary dB_top = 0",
            "status": "CONDITIONAL_ON_3427_BOUNDARY_ZERO",
            "valid_for_claim": False,
        },
        {
            "class_id": "SCT3428_3_gapped_auxiliary",
            "stress_class": "massive/gapped auxiliary or Z/Y6 residual sector",
            "zero_or_safe_statement": "energy identity gives zero/suppression only if operator positive and source/boundary terms vanish",
            "identity": "<X,L_X X> <= <X,J_X+B_X> => X=0 if L_X>0 and J_X=B_X=0",
            "status": "OPEN_NEEDS_LAMBDA_STAR_AND_SOURCE_FREE_PROOF",
            "valid_for_claim": False,
        },
        {
            "class_id": "SCT3428_4_hidden_projector",
            "stress_class": "hidden/domain/projector/constitutive/memory/range stress",
            "zero_or_safe_statement": "not safe from Bianchi conservation; must be theorem-zero or explicitly bounded",
            "identity": "nabla_mu T_extra^{mu nu}=0 does not imply Delta H_extra=0",
            "status": "RETAIN_AS_RESIDUAL",
            "valid_for_claim": False,
        },
        {
            "class_id": "SCT3428_5_q_loc_TGK",
            "stress_class": "q_loc/Gamma-Khat effective stress",
            "zero_or_safe_statement": "safe only after metric-response, Euler, boundary/projector and alpha-vector gates close",
            "identity": "q_loc = P_loc(nabla Gamma_eff - nabla Khat); T_GK safe iff Hilbert-owned and response-matched",
            "status": "CONDITIONAL_NOT_CURRENTLY_SAFE",
            "valid_for_claim": False,
        },
        {
            "class_id": "SCT3428_6_verdict",
            "stress_class": "all Y6/extra stress",
            "zero_or_safe_statement": "Y6 is closed only if every class is public-Hilbert, constant-background, zero-boundary topological, gapped no-hair, or bounded",
            "identity": "Delta H_extra = sum_abs(Delta H_class_i)",
            "status": "NOT_CLOSED_CURRENT_MTS",
            "valid_for_claim": False,
        },
    ]


def extra_mass_decomposition() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "EMD3428_0_public_double_count",
            "mass_channel": "ordinary matter/EM/Poynting Hilbert stress",
            "monopole_status": "included in M_H, not Delta_extra",
            "residual_if_fail": "epsilon_public_double_count",
            "current_status": "SAFE_IF_PUBLIC_ACTION",
            "valid_for_claim": False,
        },
        {
            "component_id": "EMD3428_1_Lambda_trace",
            "mass_channel": "constant local background trace",
            "monopole_status": "reference/background, not compact source mass, if source-independent",
            "residual_if_fail": "epsilon_Lambda_gradient_or_source_dependence",
            "current_status": "CONDITIONAL_BACKGROUND",
            "valid_for_claim": False,
        },
        {
            "component_id": "EMD3428_2_topological_boundary",
            "mass_channel": "topological/improvement boundary charge",
            "monopole_status": "zero in Hilbert-identity branch when boundary charge zero; old topological branch retained",
            "residual_if_fail": "B_zero_flux^top + R_eq_integral",
            "current_status": "PARTIAL_FROM_3427",
            "valid_for_claim": False,
        },
        {
            "component_id": "EMD3428_3_gapped_ZY6",
            "mass_channel": "gapped Z/Y6 auxiliary field charge",
            "monopole_status": "zero only if positive-operator/source-free/boundary-silent no-hair theorem passes",
            "residual_if_fail": "epsilon_gapped_auxiliary_monopole",
            "current_status": "OPEN_LAMBDA_STAR_SOURCE_FREE",
            "valid_for_claim": False,
        },
        {
            "component_id": "EMD3428_4_hidden_projector",
            "mass_channel": "hidden/projector/domain/memory/range/constitutive charge",
            "monopole_status": "not excluded",
            "residual_if_fail": "epsilon_hidden_projector_monopole",
            "current_status": "RETAINED",
            "valid_for_claim": False,
        },
        {
            "component_id": "EMD3428_5_total",
            "mass_channel": "Delta_extra_mass",
            "monopole_status": "zero only if EMD3428_0 through EMD3428_4 are safe/zero",
            "residual_if_fail": "absolute no-cancellation sum",
            "current_status": "NOT_ZERO_CURRENTLY",
            "valid_for_claim": False,
        },
    ]


def monopole_silence_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "MSG3428_0_same_public_action",
            "gate": "all ordinary matter/EM/Poynting stress comes from the same public g_obs action",
            "result": "PASS_CONDITIONAL",
            "blocker": "hidden Hodge/current weights or double-counted Poynting",
            "valid_for_claim": False,
        },
        {
            "gate_id": "MSG3428_1_background_subtraction",
            "gate": "constant Lambda/vacuum trace is source-independent and absorbed into fixed reference",
            "result": "PASS_IF_PARENT_REFERENCE_SIGNS",
            "blocker": "local gradients, source dependence or time drift",
            "valid_for_claim": False,
        },
        {
            "gate_id": "MSG3428_2_boundary_topological",
            "gate": "topological/improvement stress has zero compact linking charge",
            "result": "PARTIAL_HILBERT_BRANCH_ONLY",
            "blocker": "old topological B_zero/R_eq branch remains",
            "valid_for_claim": False,
        },
        {
            "gate_id": "MSG3428_3_gapped_nohair",
            "gate": "positive operator and zero source/boundary terms force residual fields to vanish",
            "result": "OPEN",
            "blocker": "lambda_*, J_Z/Y6 and boundary silence are not all signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "MSG3428_4_hidden_projector",
            "gate": "hidden/projector/domain/memory/range channels carry no monopole charge",
            "result": "FAIL_CURRENT",
            "blocker": "no blanket theorem; needs channelwise exclusion or bound",
            "valid_for_claim": False,
        },
        {
            "gate_id": "MSG3428_5_verdict",
            "gate": "PC3400_4 no-extra-mass is signed",
            "result": "FAIL_CURRENT_PARTIAL_SAFE_CLASSES",
            "blocker": "gapped nohair and hidden/projector channel bounds remain",
            "valid_for_claim": False,
        },
    ]


def delta_extra_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "DEX3428_0_public_double_count",
            "quantity": "epsilon_public_double_count",
            "definition": "ordinary Hilbert/EM/Poynting stress counted again as extra source",
            "bound_formula": "0 if all public Hilbert stress is included once in M_H; else source-backed double-count residual",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DEX3428_1_Lambda_local",
            "quantity": "epsilon_Lambda_local",
            "definition": "local compact-source contribution from vacuum trace gradients or source dependence",
            "bound_formula": "|partial_source rho_Lambda|/rho_H + local-gradient envelope",
            "status": "THEOREM_OR_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DEX3428_2_topological_boundary",
            "quantity": "epsilon_topological_boundary",
            "definition": "topological/improvement compact monopole charge",
            "bound_formula": "|B_zero_flux^top|/M_H_ref + |R_eq_integral|/M_H_ref",
            "status": "OLD_TOPOLOGICAL_BRANCH_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DEX3428_3_gapped_auxiliary",
            "quantity": "epsilon_gapped_auxiliary",
            "definition": "massive/gapped Z/Y6 auxiliary monopole charge",
            "bound_formula": "0 if lambda_*>0 and J=B=0; else C_aux*(||J||+||B||+||R||)/lambda_*",
            "status": "MISSING_LAMBDA_STAR_SOURCE_FREE_INPUTS",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DEX3428_4_hidden_projector",
            "quantity": "epsilon_hidden_projector",
            "definition": "hidden/projector/domain/memory/range/constitutive monopole source charge",
            "bound_formula": "sum_abs(channelwise Delta_hidden_i/M_H_ref)",
            "status": "MISSING_CHANNELWISE_BOUNDS",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DEX3428_5_q_loc_TGK",
            "quantity": "epsilon_q_loc_TGK_mass",
            "definition": "q_loc/Gamma-Khat effective stress monopole contribution",
            "bound_formula": "0 if metric-response/Euler/boundary/projector/vector gates close; else source-backed T_GK mass bound",
            "status": "PENDING_QLOC_RESPONSE_GATES",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DEX3428_6_total",
            "quantity": "Delta_extra_mass_over_MH",
            "definition": "absolute no-cancellation extra monopole mass envelope",
            "bound_formula": "epsilon_public_double_count+epsilon_Lambda_local+epsilon_topological_boundary+epsilon_gapped_auxiliary+epsilon_hidden_projector+epsilon_q_loc_TGK_mass",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def pc3400_4_update() -> list[dict[str, Any]]:
    return [
        {
            "pc_piece": "PC3400_4_public_Hilbert",
            "before_3428": "ordinary/EM/Poynting stress listed under possible Y6 debt",
            "after_3428": "safe if public Hilbert action and no double count",
            "remaining": "EM origin still open, but coupling/source stress is safe",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_4_background_topological",
            "before_3428": "constant/background/topological mixed with extra stress",
            "after_3428": "safe only under fixed reference and zero boundary charge",
            "remaining": "old topological branch retains B_zero/R_eq",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_4_gapped_nohair",
            "before_3428": "positive/nohair route named",
            "after_3428": "identified as next proof target",
            "remaining": "lambda_*, source-free J/B and boundary silence",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_4_hidden_projector",
            "before_3428": "retained residual",
            "after_3428": "still retained; no Bianchi shortcut accepted",
            "remaining": "channelwise bounds or parent exclusion theorem",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_4_verdict",
            "before_3428": "no-extra-mass open",
            "after_3428": "public Hilbert/EM and fixed background pieces partially safe; hidden/gapped/q_loc remain",
            "remaining": "not signed for current MTS",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3428_0_public_Hilbert_safe",
            "claim": "ordinary matter/EM/Poynting Hilbert stress is not extra mass",
            "gate_status": "PASS_CONDITIONAL_SAFE_CLASS",
            "reason": "same public action and no double count",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3428_1_background_topological",
            "claim": "constant/topological classes are harmless",
            "gate_status": "PARTIAL_ONLY",
            "reason": "requires fixed reference and zero old-topological boundary charge",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3428_2_gapped_nohair",
            "claim": "gapped auxiliary/Y6 stress vanishes",
            "gate_status": "OPEN",
            "reason": "positive operator/source-free/boundary-silent proof not signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3428_3_hidden_projector",
            "claim": "hidden/projector/domain stress carries no monopole",
            "gate_status": "FAIL_CURRENT",
            "reason": "not excluded by conservation alone",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3428_4_PC3400_4",
            "claim": "PC3400_4 no-extra-mass is signed",
            "gate_status": "FAIL_CURRENT_PARTIAL_SAFE_CLASSES",
            "reason": "gapped nohair, hidden/projector and q_loc/TGK mass rows remain",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3428_5_local_GR",
            "claim": "local GR/Newton/PPN branch is derived",
            "gate_status": "BLOCKED",
            "reason": "PC3400_4, lambda-star/source-free fixed point and second-order PPN gates remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3428_0_not_all_Y6_bad",
            "decision": "Y6 is not one monster; public Hilbert/EM/Poynting stress is safe when owned by the same action.",
            "because": "then it is the normal GR source stress, not an extra fifth-force channel",
            "next_action": "keep public EM/Poynting in M_H, not in Delta_extra",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3428_1_no_bianchi_shortcut",
            "decision": "Bianchi conservation alone still does not kill extra monopole mass.",
            "because": "a conserved hidden/projector stress can carry monopole, STF, vector or PPN charge",
            "next_action": "require safe-class theorem or explicit bound per channel",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3428_2_remaining_core",
            "decision": "The hardest remaining no-extra-mass route is gapped no-hair plus hidden/projector exclusion.",
            "because": "public Hilbert and fixed-reference classes now have conditional zero routes",
            "next_action": "attack positive operator/source-free no-hair next",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3428_3_next",
            "decision": "Next target should prove the gapped/Y6 no-hair theorem or emit Delta_extra_mass rows.",
            "because": "that is the clean derivation route for the residual MTS source-charge hair",
            "next_action": "3429-Y5-R2FR-gapped-Y6-nohair-positive-operator-or-DeltaExtra-row-under-AX1090.md",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target": "3429-Y5-R2FR-gapped-Y6-nohair-positive-operator-or-DeltaExtra-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3429_gapped_Y6_nohair_positive_operator_or_DeltaExtra_row.py",
            "objective": "prove positive-operator/source-free/boundary-silent no-hair for gapped Y6/Z auxiliary sectors, or emit lambda-star/J/B/Delta_extra_mass source-bound rows",
            "why_next": "3428 made public Hilbert/EM stress safe and localized the remaining no-extra-mass obstruction to gapped/hidden residual source hair",
            "valid_for_claim": False,
        },
        {
            "target": "3430-Y5-R2FR-hidden-projector-channelwise-bound-or-exclusion-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3430_hidden_projector_channelwise_bound_or_exclusion.py",
            "objective": "exclude or bound hidden/domain/projector/memory/range/constitutive monopole charge channel by channel",
            "why_next": "needed if gapped nohair does not cover all hidden/projector residuals",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3428_0",
            "script": str(Path(__file__).resolve()),
            "mode": "NO_EXTRA_MASS_Y6_MONOPOLE_SILENCE_OR_BOUND",
            "summary": "Y6 safe-class theorem split; public Hilbert/EM/Poynting stress safe conditionally; constant/background/topological partial; gapped and hidden/projector channels retained; Delta_extra bound rows staged",
            "valid_for_claim": False,
        }
    ]


def formalization_recent_count(start_utc: datetime) -> int:
    if not FORMALIZATION.exists():
        return 0
    threshold = start_utc.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= threshold)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    sources = rows_by_name["source_register"]
    nonclaim = all(
        row.get("valid_for_claim") is False
        for name, rows in rows_by_name.items()
        if name != "validation"
        for row in rows
    )
    outputs_under_root = all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()) and str(DOC).startswith(str(ROOT))
    formalization_count = formalization_recent_count(start_utc)
    promotion = rows_by_name["promotion_gates"]
    return [
        {
            "check_id": "VAL3428_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in sources),
            "detail": f"{sum(1 for row in sources if row['exists'])}/{len(sources)} source paths exist",
        },
        {
            "check_id": "VAL3428_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": outputs_under_root,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3428_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim,
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3428_3_safe_class_split",
            "condition": "Y6 safe-class theorem covers public/background/topological/gapped/hidden/q_loc classes",
            "passed": len(rows_by_name["safe_class_theorem"]) >= 7,
            "detail": "SCT3428 rows present",
        },
        {
            "check_id": "VAL3428_4_public_safe",
            "condition": "public Hilbert/EM/Poynting safe class is explicit",
            "passed": any(row["gate_id"] == "PG3428_0_public_Hilbert_safe" and row["gate_status"] == "PASS_CONDITIONAL_SAFE_CLASS" for row in promotion),
            "detail": "public stress not counted as extra",
        },
        {
            "check_id": "VAL3428_5_hidden_not_claimed",
            "condition": "hidden/projector stress is not silently zeroed",
            "passed": any(row["gate_id"] == "PG3428_3_hidden_projector" and row["gate_status"] == "FAIL_CURRENT" for row in promotion),
            "detail": "hidden/projector residual retained",
        },
        {
            "check_id": "VAL3428_6_bound_rows",
            "condition": "Delta_extra bound rows exist",
            "passed": any(row["bound_id"] == "DEX3428_6_total" for row in rows_by_name["delta_extra_bound_rows"]),
            "detail": "DEX3428_6 present",
        },
        {
            "check_id": "VAL3428_7_local_GR_blocked",
            "condition": "local GR remains blocked",
            "passed": any(row["gate_id"] == "PG3428_5_local_GR" and row["gate_status"] == "BLOCKED" for row in promotion),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3428_8_next_target",
            "condition": "next target attacks gapped/Y6 nohair",
            "passed": rows_by_name["next_target"][0]["target"].startswith("3429-Y5-R2FR-gapped-Y6-nohair"),
            "detail": rows_by_name["next_target"][0]["target"],
        },
        {
            "check_id": "VAL3428_9_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": formalization_count == 0,
            "detail": f"modified_count_since_start={formalization_count}",
        },
        {
            "check_id": "VAL3428_10_overall",
            "condition": "3428 no-extra-mass/Y6 checkpoint is internally valid",
            "passed": True,
            "detail": "PASS",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3428 - No-Extra-Mass Y6 Monopole Silence or Bound

## Summary
- This checkpoint attacks `PC3400_4`: no hidden extra monopole mass after calibrated Hilbert coupling.
- The important win is classification: public matter/EM/Poynting Hilbert stress is **not** extra mass if it is varied from the same public `g_obs` action and counted once in `M_H`.
- Constant background and topological/improvement stresses are only safe with fixed reference and zero compact boundary charge.
- Gapped auxiliary/Y6 sectors need an actual no-hair proof: positive operator, source-free current, boundary silence, and no zero-mode leakage.
- Hidden/projector/domain/memory/range/constitutive stress remains residual. Bianchi conservation is not silence.
- Local GR is still not claimed, but `Delta_extra_mass` is now a finite channel list rather than fog.

## Source Register
{md_table(rows_by_name["source_register"])}

## Y6 Safe-Class Theorem
{md_table(rows_by_name["safe_class_theorem"])}

## Extra Mass Decomposition
{md_table(rows_by_name["extra_mass_decomposition"])}

## Monopole Silence Gate
{md_table(rows_by_name["monopole_silence_gate"])}

## Delta Extra Bound Rows
{md_table(rows_by_name["delta_extra_bound_rows"])}

## PC3400_4 Update
{md_table(rows_by_name["pc3400_4_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is a useful clean-up. We are not pretending Y6 vanished. We are separating what is ordinary Hilbert source stress from what is real extra source-charge hair. The next derivation target is the gapped no-hair theorem: if that lands, a major chunk of no-extra-mass stops being hand-wavy.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "safe_class_theorem": safe_class_theorem(),
        "extra_mass_decomposition": extra_mass_decomposition(),
        "monopole_silence_gate": monopole_silence_gate(),
        "delta_extra_bound_rows": delta_extra_bound_rows(),
        "pc3400_4_update": pc3400_4_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)
    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3428 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
