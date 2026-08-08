from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3422-Y5-R2FR-source-current-zero-even-matter-readout-or-JZ-bound-row-under-AX1090.md"

ALPHA3_PRODUCT_LIMIT = 5.381673706808059e-15

SOURCES = {
    "doc_3421": ROOT / "3421-Y5-R2FR-Z-basis-physical-lock-and-Euler-source-free-local-branch-under-AX1090.md",
    "next_3421": OUT / "P8_Y5_R2FR_3421_NEXT_TARGET.csv",
    "source_gate_3421": OUT / "P8_Y5_R2FR_3421_SOURCE_CURRENT_ZERO_GATE.csv",
    "zlock_3421": OUT / "P8_Y5_R2FR_3421_Z_BASIS_PHYSICAL_LOCK_MATRIX.csv",
    "coercivity_3421": OUT / "P8_Y5_R2FR_3421_COERCIVITY_BOUND_PACK.csv",
    "fallback_3421": OUT / "P8_Y5_R2FR_3421_RESIDUAL_FALLBACK_ROWS.csv",
    "y5_coupling_3414": OUT / "P8_Y5_R2FR_3414_Y5_CALIBRATED_COUPLING_LAW.csv",
    "y6_decomp_3414": OUT / "P8_Y5_R2FR_3414_Y6_EXTRA_STRESS_DECOMPOSITION.csv",
    "textra_3415": OUT / "P8_Y5_R2FR_3415_TEXTRA_SAFE_CLASS_PROOF.csv",
    "hidden_stress_3416": OUT / "P8_Y5_R2FR_3416_HIDDEN_STRESS_EXCLUSION_GATE.csv",
    "euler_source_517": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
    "obstruction_517": OUT / "P8_RESPONSE_DOUBLET_OBSTRUCTION_LEDGER.csv",
    "theorem_1011": OUT / "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
    "qloc_bounds_1011": OUT / "P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv",
    "y5_owner_doc_1012": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
    "hilbert_equality_doc_1015": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
    "worldtube_doc_1016": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3422_SOURCE_REGISTER.csv",
    "even_matter_readout_theorem": OUT / "P8_Y5_R2FR_3422_EVEN_MATTER_READOUT_THEOREM.csv",
    "source_current_decomposition": OUT / "P8_Y5_R2FR_3422_SOURCE_CURRENT_DECOMPOSITION.csv",
    "y5_source_gate": OUT / "P8_Y5_R2FR_3422_Y5_SOURCE_NORMALIZATION_GATE.csv",
    "y6_stress_gate": OUT / "P8_Y5_R2FR_3422_Y6_EXTRA_STRESS_GATE.csv",
    "jz_bound_rows": OUT / "P8_Y5_R2FR_3422_JZ_BOUND_ROWS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3422_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3422_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3422_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3422_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3422_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def cell(value: Any) -> str:
        return str(value).replace("|", "/").replace("\n", " ")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3421": "fixed-point theorem handoff to source-current zero",
        "next_3421": "machine-readable 3422 target",
        "source_gate_3421": "J_Z/B_Z zero gates and Y5/Y6 blockers",
        "zlock_3421": "physical Z lock matrix naming matter/readout/Y5/Y6 channels",
        "coercivity_3421": "Z-norm bound schema if J_Z does not vanish",
        "fallback_3421": "fallback residuals for nonzero source current",
        "y5_coupling_3414": "universal calibrated coupling and Y5 residual policy",
        "y6_decomp_3414": "Y6 extra stress class decomposition",
        "textra_3415": "safe-class proof for public Hilbert stress and hidden/projector debt",
        "hidden_stress_3416": "hidden stress exclusion gates",
        "euler_source_517": "Y0-Y6 source-current obstruction ledger",
        "obstruction_517": "Y5/Y6/PPN/boundary response-doublet obstructions",
        "theorem_1011": "prior response-doublet source-current theorem attempt",
        "qloc_bounds_1011": "source-current fallback bound rows",
        "y5_owner_doc_1012": "Y5 source-normalization owner or bound implementation",
        "hilbert_equality_doc_1015": "topological-Hilbert equality/source-boundary gate",
        "worldtube_doc_1016": "parent Hilbert source worldtube selector",
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


def even_matter_readout_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "EMR3422_0_parent_split",
            "claim": "Split response variables into even quotient data R_even and odd residual data Z.",
            "mathematical_form": "R_even=(R_+ + R_-)/2; Z=(R_+-R_-)/2",
            "proof_status": "PASS_CONDITIONAL_FROM_RESPONSE_DOUBLET",
            "missing_to_promote": "parent doublets must cover every physical residual channel",
            "valid_for_claim": False,
        },
        {
            "step_id": "EMR3422_1_even_readout",
            "claim": "If matter/clocks/rods/photons/source readout depend only on e_obs(R_even), then delta_Z S_matter=0.",
            "mathematical_form": "S_matter=S_matter[psi,e_obs(R_even)] => delta S_matter/delta Z^A = 0",
            "proof_status": "EXACT_IF_QUOTIENT_EVEN_DESCENT_SIGNED",
            "missing_to_promote": "quotient-invariant matter action, same coframe, and source readout descent",
            "valid_for_claim": False,
        },
        {
            "step_id": "EMR3422_2_common_calibration",
            "claim": "A universal common source-coupling calibration is not a Z source current.",
            "mathematical_form": "kappa_MTS common mode is fixed once; only differential/non-universal offsets enter J_Z",
            "proof_status": "PASS_POLICY_FROM_3414",
            "missing_to_promote": "prove no source-dependent recalibration or species/readout weights",
            "valid_for_claim": False,
        },
        {
            "step_id": "EMR3422_3_Y5_exception",
            "claim": "Measured GM/source normalization is naturally exchange-even and is not killed by odd Z parity alone.",
            "mathematical_form": "delta_Z S_matter=0 does not imply delta_Z mu_obs=0 unless mu_obs descends from the same even Hilbert charge",
            "proof_status": "HARD_EXCEPTION_RETAINED",
            "missing_to_promote": "Hilbert source worldtube/source-measure closure or explicit bound",
            "valid_for_claim": False,
        },
        {
            "step_id": "EMR3422_4_Y6_exception",
            "claim": "Conserved extra stress may be exchange-even and nonzero while satisfying Bianchi/Ward identities.",
            "mathematical_form": "nabla_mu T_extra^{mu nu}=0 is not T_extra=0",
            "proof_status": "HARD_EXCEPTION_RETAINED",
            "missing_to_promote": "safe-class theorem, topological exactness, gapped no-hair, or stress bound",
            "valid_for_claim": False,
        },
        {
            "step_id": "EMR3422_5_verdict",
            "claim": "Even matter readout can kill direct matter J_Z, but not the full source-current gate by itself.",
            "mathematical_form": "J_Z_total=J_Z_matter_readout+J_Z_Y5+J_Z_Y6+J_Z_boundary+J_Z_projector",
            "proof_status": "PARTIAL_THEOREM_NOT_LOCAL_GR",
            "missing_to_promote": "Y5/Y6 and boundary/projector source-current zero or bound rows",
            "valid_for_claim": False,
        },
    ]


def source_current_decomposition() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "JZD3422_0_direct_matter",
            "source_current": "J_Z_matter_readout",
            "zero_route": "delta_Z S_matter=0 from quotient-even readout",
            "current_status": "CONDITIONAL_ZERO_IF_EVEN_DESCENT",
            "fallback": "epsilon_matter_readout_Z",
            "valid_for_claim": False,
        },
        {
            "component_id": "JZD3422_1_Y5_source",
            "source_current": "J_Z_Y5_source_normalization",
            "zero_route": "observed source strength is the same even Hilbert/worldtube charge with no extra offsets",
            "current_status": "FAIL_CURRENT_Y5_OWNER",
            "fallback": "epsilon_Y5_source_normalization",
            "valid_for_claim": False,
        },
        {
            "component_id": "JZD3422_2_Y6_stress",
            "source_current": "J_Z_Y6_extra_stress",
            "zero_route": "public Hilbert stress, constant local Lambda, topological exactness, or gapped source-free no-hair",
            "current_status": "RETAINED_Y6_STRESS_DEBT",
            "fallback": "epsilon_Y6_extra_stress",
            "valid_for_claim": False,
        },
        {
            "component_id": "JZD3422_3_boundary_projector",
            "source_current": "J_Z_boundary_projector",
            "zero_route": "3420 no-flux/fixed-reference/q-basic-projector theorem",
            "current_status": "CONDITIONAL_ON_3420_NOT_SIGNED",
            "fallback": "epsilon_boundary_projector",
            "valid_for_claim": False,
        },
        {
            "component_id": "JZD3422_4_species_frame",
            "source_current": "J_Z_species_frame",
            "zero_route": "one public metric/coframe; no species-dependent source charge or shadow frame",
            "current_status": "OPEN_FRAME_SPECIES_DESCENT",
            "fallback": "epsilon_species_frame",
            "valid_for_claim": False,
        },
        {
            "component_id": "JZD3422_5_total",
            "source_current": "J_Z_total",
            "zero_route": "all components JZD3422_0 through JZD3422_4 zero",
            "current_status": "NOT_ZERO_CURRENTLY",
            "fallback": "absolute J_Z_total bound row",
            "valid_for_claim": False,
        },
    ]


def y5_source_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "Y5G3422_0_common_mode",
            "claim": "Universal calibrated G/kappa common mode is allowed.",
            "test": "same kappa_MTS for all ordinary Hilbert sources, fixed once before local tests",
            "current_result": "PASS_AS_CALIBRATION_POLICY",
            "if_fail": "epsilon_absolute_calibration_offset",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y5G3422_1_Hilbert_charge",
            "claim": "Measured GM equals one parent Hilbert/source worldtube charge.",
            "test": "mu_obs = Q_H[W_source,e_obs,tau] with W_source fixed before readout",
            "current_result": "BLOCKED_SOURCE_WORLDTUBE_NOT_SIGNED",
            "if_fail": "epsilon_source_charge",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y5G3422_2_no_relative_weights",
            "claim": "No species/material/readout relative source weights survive.",
            "test": "delta w_A=0 and no source-only slot after quotient descent",
            "current_result": "OPEN_SPECIES_SOURCE_CHARGE",
            "if_fail": "epsilon_species_source",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y5G3422_3_no_domain_mass_hair",
            "claim": "No radial/time/frame/range/domain/projector source-normalization hair survives.",
            "test": "all mu_extra components theorem-zero or bounded",
            "current_result": "OPEN_MULTI_CHANNEL_Y5_RESIDUAL",
            "if_fail": "epsilon_mu_extra",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y5G3422_4_verdict",
            "claim": "Y5 source current is zero.",
            "test": "Y5G3422_0 through Y5G3422_3 pass",
            "current_result": "FAIL_CURRENT_Y5_ZERO",
            "if_fail": "J_Z_Y5_source_normalization",
            "valid_for_claim": False,
        },
    ]


def y6_stress_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "Y6G3422_0_public_Hilbert",
            "stress_class": "ordinary matter/EM/Poynting/surface Hilbert stress",
            "zero_or_safe_route": "not a hidden J_Z source if varied from the same public observed action before readout",
            "current_result": "SAFE_CLASS_CONDITIONAL",
            "if_fail": "hidden_public_double_count_stress",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y6G3422_1_constant_Lambda",
            "stress_class": "constant local vacuum trace",
            "zero_or_safe_route": "source-independent constant background subtracted from compact-system Newton/PPN branch",
            "current_result": "CONDITIONAL_BACKGROUND_SUBTRACTION",
            "if_fail": "epsilon_Lambda_local_trace",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y6G3422_2_topological",
            "stress_class": "topological/improvement stress",
            "zero_or_safe_route": "exact/topological with zero compact linking/boundary charge",
            "current_result": "OPEN_BOUNDARY_CHARGE",
            "if_fail": "epsilon_topological_stress",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y6G3422_3_gapped_nohair",
            "stress_class": "massive auxiliary stress",
            "zero_or_safe_route": "positive operator, source-free and boundary-silent implies no-hair/suppression",
            "current_result": "OPEN_SOURCE_FREE_AND_LAMBDA_STAR",
            "if_fail": "epsilon_gapped_auxiliary_stress",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y6G3422_4_hidden_projector",
            "stress_class": "hidden/domain/projector/constitutive stress",
            "zero_or_safe_route": "theorem-zero or explicit absolute bound",
            "current_result": "RETAINED_RESIDUAL",
            "if_fail": "epsilon_hidden_projector_stress",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y6G3422_5_verdict",
            "stress_class": "all Y6 extra stress",
            "zero_or_safe_route": "Y6G3422_0 through Y6G3422_4 all safe, zero or bounded",
            "current_result": "Y6_ZERO_NOT_CLOSED",
            "if_fail": "J_Z_Y6_extra_stress",
            "valid_for_claim": False,
        },
    ]


def jz_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "JZB3422_0_total",
            "quantity": "||J_Z_total||",
            "definition": "absolute sum of all nonzero Z-source currents",
            "bound_formula": "||J_Z_total|| <= |J_matter|+|J_Y5|+|J_Y6|+|J_boundary|+|J_species_frame|",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "JZB3422_1_matter_readout",
            "quantity": "||J_Z_matter_readout||",
            "definition": "variation of matter/clocks/rods/photons/source readout with respect to Z",
            "bound_formula": "0 if quotient-even descent theorem passes; otherwise source-backed norm",
            "status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "row_id": "JZB3422_2_Y5",
            "quantity": "||J_Z_Y5_source_normalization||",
            "definition": "source-normalization/measured-GM drift driving the Z equation",
            "bound_formula": "epsilon_Y5_source_normalization with same-frame units and source path",
            "status": "MISSING_Y5_OWNER_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "JZB3422_3_Y6",
            "quantity": "||J_Z_Y6_extra_stress||",
            "definition": "extra-stress source current not public/topological/gapped/zero",
            "bound_formula": "epsilon_Y6_extra_stress with PPN/source-stress map",
            "status": "MISSING_Y6_SAFE_CLASS_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "JZB3422_4_to_Znorm",
            "quantity": "||Z|| contribution from J_Z",
            "definition": "source-current contribution to fixed-point residual amplitude",
            "bound_formula": "||Z||_J <= 2 lambda_*^-1 ||J_Z_total||",
            "status": "MISSING_LAMBDA_STAR_AND_JZ_VALUE",
            "valid_for_claim": False,
        },
        {
            "row_id": "JZB3422_5_to_alpha3",
            "quantity": "alpha3 contribution from J_Z",
            "definition": "q_loc alpha-vector effect induced by nonzero source-current fixed point",
            "bound_formula": f"|alpha3_JZ| <= Q_PROXY*C_alphaZ*2*lambda_*^-1*||J_Z_total|| and total vector budget <= {ALPHA3_PRODUCT_LIMIT}",
            "status": "MISSING_RESPONSE_OPERATOR_AND_VALUES",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3422_0_even_readout",
            "gate": "delta_Z S_matter=0 from even quotient matter/readout",
            "current_result": "PASS_CONDITIONAL_THEOREM",
            "promotes_if": "same public coframe/metric and source readout descent are parent-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3422_1_Y5_zero",
            "gate": "Y5 source-normalization current vanishes",
            "current_result": "FAIL_CURRENT_Y5_ZERO",
            "promotes_if": "Hilbert source worldtube/source-measure closure and no relative source weights",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3422_2_Y6_zero",
            "gate": "Y6 extra-stress current is safe, zero or bounded",
            "current_result": "BLOCKED_Y6_RETAINED_DEBT",
            "promotes_if": "all Y6 safe classes pass or bounded residuals are sourced",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3422_3_JZ_zero",
            "gate": "total source current J_Z is zero",
            "current_result": "NOT_PROMOTED",
            "promotes_if": "direct matter, Y5, Y6, boundary/projector and species/frame currents vanish",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3422_4_JZ_bound",
            "gate": "if not zero, J_Z bound is score-ready",
            "current_result": "FORMULA_READY_VALUES_MISSING",
            "promotes_if": "all JZB3422 rows have numeric/source-backed values or theorem-zero switches",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3422_5_local_GR",
            "gate": "local GR/Newton/PPN branch is derived",
            "current_result": "BLOCKED",
            "promotes_if": "J_Z/B_Z zero or bounded, lambda_* known, q_loc/source/stress envelopes closed",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3422_0_partial_win",
            "finding": "Even matter/readout descent is a real zero theorem for direct matter J_Z.",
            "evidence": "If S_matter depends only on e_obs(R_even), delta_Z S_matter=0.",
            "action": "Keep this as a parent-action requirement, not a closure assumption.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3422_1_Y5_hard",
            "finding": "Y5 source normalization is not killed by exchange-odd doublet symmetry.",
            "evidence": "Measured GM/source strength can be exchange-even and still observable.",
            "action": "Attack Hilbert source worldtube/source-measure closure next.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3422_2_Y6_hard",
            "finding": "Y6 extra stress is not killed by conservation or Bianchi identity alone.",
            "evidence": "Conserved extra stress can be metric-visible while divergence-free.",
            "action": "Retain Y6 safe-class/bound rows unless public/topological/gapped conditions pass.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3422_3_next",
            "finding": "The next best strike is Y5 Hilbert source closure before lambda-star numerics.",
            "evidence": "lambda_* only helps after J_Z is zeroed or expressed as a source-backed norm; Y5 is the largest J_Z blocker.",
            "action": "Build 3423 Y5 Hilbert-source worldtube closure or J_Z_Y5 bound row.",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3423-Y5-R2FR-Y5-Hilbert-source-worldtube-closure-or-JZmu-bound-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3423_Y5_Hilbert_source_worldtube_closure_or_JZmu_bound_row.py",
            "objective": "prove measured GM/source normalization is the same parent Hilbert worldtube charge with no relative source weights, or emit J_Z_Y5 source-normalization bound rows",
            "why_next": "3422 shows even matter readout only partially zeros J_Z; Y5 is the largest remaining source-current obstruction to Newton/local-GR recovery",
            "valid_for_claim": False,
        },
        {
            "target_id": "3424-Y5-R2FR-positive-operator-lambda-star-or-Znorm-bound-runner-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3424_positive_operator_lambda_star_or_Znorm_bound_runner.py",
            "objective": "prove lambda_*>0 after gauge quotient or stage coercivity inputs for the nonzero J_Z bound branch",
            "why_next": "needed after J_Z components are zeroed or sourced",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3422_0",
            "script": str(Path(__file__).resolve()),
            "mode": "SOURCE_CURRENT_ZERO_EVEN_MATTER_READOUT_OR_JZ_BOUND",
            "result": "direct even matter readout theorem written; Y5/Y6 remain source-current blockers; J_Z bound rows staged nonclaim",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    all_sources_exist = all(row["exists"] for row in source_rows)
    scope_ok = all(str(path).startswith(str(ROOT)) and "formalization-workbench" not in str(path) for path in OUTPUTS.values())
    nonclaim = all(
        str(row.get("valid_for_claim", False)).lower() == "false"
        for key, rows in generated.items()
        if key != "validation"
        for row in rows
    )
    even_theorem = any(row["step_id"] == "EMR3422_1_even_readout" for row in generated["even_matter_readout_theorem"])
    y5_fail = any(row["gate_id"] == "Y5G3422_4_verdict" and row["current_result"] == "FAIL_CURRENT_Y5_ZERO" for row in generated["y5_source_gate"])
    y6_block = any(row["gate_id"] == "Y6G3422_5_verdict" and row["current_result"] == "Y6_ZERO_NOT_CLOSED" for row in generated["y6_stress_gate"])
    jz_total = any(row["row_id"] == "JZB3422_0_total" for row in generated["jz_bound_rows"])
    local_gr_blocked = any(row["gate_id"] == "PG3422_5_local_GR" and row["current_result"] == "BLOCKED" for row in generated["promotion_gates"])
    next_y5 = generated["next_target"][0]["target_id"].startswith("3423-Y5-R2FR-Y5-Hilbert-source")

    rows = [
        {
            "check_id": "VAL3422_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all_sources_exist,
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3422_1_scope",
            "check": "all outputs stay under post-checkpoint-work",
            "passed": scope_ok,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3422_2_all_nonclaim",
            "check": "3422 does not claim local GR",
            "passed": nonclaim,
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3422_3_even_theorem",
            "check": "even matter readout theorem exists",
            "passed": even_theorem,
            "detail": "EMR3422_1 present",
        },
        {
            "check_id": "VAL3422_4_Y5_visible",
            "check": "Y5 source-normalization blocker remains visible",
            "passed": y5_fail,
            "detail": "Y5 zero not claimed",
        },
        {
            "check_id": "VAL3422_5_Y6_visible",
            "check": "Y6 extra-stress blocker remains visible",
            "passed": y6_block,
            "detail": "Y6 zero not claimed",
        },
        {
            "check_id": "VAL3422_6_JZ_bounds",
            "check": "J_Z bound rows are staged",
            "passed": jz_total,
            "detail": "JZB3422_0_total present",
        },
        {
            "check_id": "VAL3422_7_local_GR_blocked",
            "check": "local GR remains blocked",
            "passed": local_gr_blocked,
            "detail": "Y5/Y6/J_Z/lambda gates remain open",
        },
        {
            "check_id": "VAL3422_8_next_target",
            "check": "next target attacks Y5 Hilbert source closure",
            "passed": next_y5,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3422_9_overall",
            "check": "3422 source-current/even-readout checkpoint is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3422 - Source-Current Zero, Even Matter Readout, or JZ Bound Row",
            "## Summary\n"
            "- This checkpoint separates a real partial theorem from the remaining hard blockers.\n"
            "- If matter, clocks, rods, photons, and source readout depend only on the even quotient data `e_obs(R_even)`, then `delta_Z S_matter=0`; direct matter readout does not drive the Z Euler equation.\n"
            "- This does not close local GR. Y5 measured-GM/source normalization can be exchange-even and observable, so it is not killed by odd `Z` parity.\n"
            "- Y6 extra stress can be conserved and still metric-visible; Bianchi/Ward conservation is not silence.\n"
            "- If Y5/Y6/source-current zero fails, the branch must use explicit `J_Z` bound rows and propagate them through `||Z|| <= 2 lambda_*^-1 ||J_Z_total||`.\n"
            "- Next best strike is Y5 Hilbert-source worldtube closure, because Newton/local-GR recovery cannot be clean while measured source normalization is floating.",
            "## Source Register\n" + md_table(generated["source_register"]),
            "## Even Matter Readout Theorem\n" + md_table(generated["even_matter_readout_theorem"]),
            "## Source-Current Decomposition\n" + md_table(generated["source_current_decomposition"]),
            "## Y5 Source-Normalization Gate\n" + md_table(generated["y5_source_gate"]),
            "## Y6 Extra-Stress Gate\n" + md_table(generated["y6_stress_gate"]),
            "## JZ Bound Rows\n" + md_table(generated["jz_bound_rows"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "We got a useful partial zero theorem: even quotient matter readout kills direct matter `J_Z`. "
            "But the local-GR branch still hinges on Y5 source normalization and Y6 extra stress. The next target is therefore the Hilbert-source worldtube/GM closure, not more alpha arithmetic.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "even_matter_readout_theorem": even_matter_readout_theorem(),
        "source_current_decomposition": source_current_decomposition(),
        "y5_source_gate": y5_source_gate(),
        "y6_stress_gate": y6_stress_gate(),
        "jz_bound_rows": jz_bound_rows(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3422 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
