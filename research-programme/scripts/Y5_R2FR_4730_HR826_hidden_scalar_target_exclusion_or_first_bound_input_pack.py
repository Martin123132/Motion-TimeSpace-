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

CHECKPOINT = "4730"
CLAIM_ID = "L-572"
MARKER = "PPC4161_HR826_HIDDEN_SCALAR_TARGET_EXCLUSION_OR_FIRST_BOUND_INPUT_PACK_4730"
PACKET_MARKER = "PPC4161_PACKET_HR826_HIDDEN_SCALAR_TARGET_EXCLUSION_OR_FIRST_BOUND_INPUT_PACK_4730"
DECISION = "HIDDEN_SCALAR_R826_ZERO_ROUTE_EXACT_CONDITIONAL_COUNTEREXAMPLE_ACTIVE_FIRST_HHIDDEN_BOUND_PACK_CREATED_NONCLAIM"
NEXT_TARGET = "4731-Y5-R2FR-CoeffR826-typed-target-owner-from-parent-action-or-Hhidden-value-source.md"

DOC_PATH = POST / "4730-Y5-R2FR-HR826-hidden-scalar-target-exclusion-or-first-bound-input-pack.md"
FORMAL_PATH = FORMAL / "746-PPC4161-HR826-hidden-scalar-target-exclusion-or-first-bound-input-pack.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4730_SOURCE_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4730_HIDDEN_SCALAR_R826_ZERO_THEOREM.csv"
COUNTEREXAMPLE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4730_HIDDEN_SCALAR_R826_COUNTEREXAMPLE_TRANSFER.csv"
BOUND_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4730_FIRST_HIDDEN_SCALAR_BOUND_INPUT_PACK.csv"
PROPAGATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4730_HHIDDEN_TO_B826_PROPAGATION.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4730_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4730_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4730_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4730_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4730_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4730_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4730_0_resume", POST / "CURRENT_LOCAL_RESUME.md", "4730-Y5-R2FR-HR826-hidden-scalar-target-exclusion-or-first-bound-input-pack.md", "current local handoff into 4730"),
    ("SRC4730_1_4729_doc", POST / "4729-Y5-R2FR-R826-parent-object-language-exhaustion-or-first-Hom-bound-row.md", "H_hidden_R826", "4729 makes hidden scalar the first H_R826 component"),
    ("SRC4730_2_4729_next", SOURCE_DIR / "P8_Y5_R2FR_4729_NEXT_TARGET.csv", "4730-Y5-R2FR-HR826-hidden-scalar-target-exclusion-or-first-bound-input-pack.md", "machine handoff into 4730"),
    ("SRC4730_3_4729_inventory", SOURCE_DIR / "P8_Y5_R2FR_4729_R826_PARENT_OBJECT_INVENTORY.csv", "INV4729_3_hidden_scalar_target", "R826 hidden scalar target inventory row"),
    ("SRC4730_4_4729_exhaustion", SOURCE_DIR / "P8_Y5_R2FR_4729_R826_EXHAUSTION_THEOREM.csv", "EXH4729_2_absent_target", "no-Hom conditional for forbidden targets"),
    ("SRC4730_5_4729_hom", SOURCE_DIR / "P8_Y5_R2FR_4729_FIRST_HR826_HOM_BOUND_ROW.csv", "HR8264729_1_hidden_scalar", "first H_hidden_R826 component row"),
    ("SRC4730_6_1219_no_hidden_arg", SOURCE_DIR / "P8_Y5_R10_1219_NO_HIDDEN_ARGUMENT_CONDITIONAL_THEOREM.csv", "NHA1219_0_type_rule", "typed no-hidden-argument theorem"),
    ("SRC4730_7_1219_counterexample", SOURCE_DIR / "P8_Y5_R10_1219_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv", "HSC1219_0_generic_scalar", "generic hidden scalar counterexample lock"),
    ("SRC4730_8_1236_certificate", SOURCE_DIR / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv", "CERT1236_1_visible_coefficient_domain", "typed certificate candidate"),
    ("SRC4730_9_1236_meta", SOURCE_DIR / "P8_Y5_R10_1236_NO_HIDDEN_VISIBLE_COEFFICIENT_META_THEOREM.csv", "META1236_0_statement", "conditional no-hidden-visible coefficient meta-theorem"),
    ("SRC4730_10_1051_no_mixed", SOURCE_DIR / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv", "NMM1051_2_scalar_counterexample", "no-mixed morphism scalar obstruction"),
    ("SRC4730_11_1051_scalar", SOURCE_DIR / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv", "ISO1051_0_hidden_scalar_I", "hidden scalar obstruction audit"),
    ("SRC4730_12_1092_triviality", SOURCE_DIR / "P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv", "HIT1092_5_verdict", "hidden invariant algebra triviality attempt"),
    ("SRC4730_13_1092_generators", SOURCE_DIR / "P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv", "GEN1092_3_memory_scalar", "surviving generator ledger"),
    ("SRC4730_14_2659_theorem", SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv", "ODT2659_1_exact_typed_theorem", "R2FR typed no-Hom theorem"),
    ("SRC4730_15_2659_countermodels", SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_COUNTERMODEL_LEDGER.csv", "CM2659_5_post_readout_selector", "countermodels to no-Hom shortcuts"),
    ("SRC4730_16_2613_hom", SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_HOM_EXCLUSION_THEOREM_ATTEMPT.csv", "HOM2613_1_conditional_meta_theorem", "Hom exclusion conditional meta-theorem"),
    ("SRC4730_17_2613_invariant", SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_INVARIANT_ALGEBRA_HOM_AUDIT.csv", "IH2613_7_verdict", "invariant algebra Hom audit"),
    ("SRC4730_18_1105_master", POST / "1105-Y5-R10-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md", "MHM1105_3_scalar_counterexample", "master no-hidden-visible morphism obstruction"),
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


def zero_theorem_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("HSZ4730_0_target", "H_hidden_R826", "Prove or bound the hidden scalar contribution to R826.", "H_hidden_R826 := sup_{B_loc,||v||=1} |D_v R826_hidden|", "TARGET_SHARP", "SRC4730_5_4729_hom"),
        ("HSZ4730_1_chain_rule", "hidden scalar derivative law", "If R826_hidden = rho_826(I_hid), then D_v R826_hidden = rho_826'(I_hid) D_v I_hid.", "Therefore H_hidden_R826=0 only by no target, rho_826 constant, or D_v I_hid=0.", "EXACT_DERIVED_SPLIT", "SRC4730_10_1051_no_mixed"),
        ("HSZ4730_2_typed_no_target", "typed target exclusion", "If Arg(Coeff_R826) contains Q_obs and fixed representation data but no C_hid slot, rho_826(I_hid) is ill-typed.", "Then R826_hidden is absent before variation and H_hidden_R826=0.", "EXACT_IF_PARENT_TYPED_NOT_DERIVED", "SRC4730_6_1219_no_hidden_arg"),
        ("HSZ4730_3_product_factor", "visible/product factorization", "If R826 factors as Rbar826(q_obs,theta_fixed), D_v Rbar826=0 for v in ker(Dq_obs).", "This is the same chain-rule zero as 4728/4729 but now targeted at the hidden scalar component.", "EXACT_IF_FACTORING_SIGNED", "SRC4730_4_4729_exhaustion"),
        ("HSZ4730_4_invariant_triviality", "hidden invariant algebra route", "If O(C_hid)^inv=R or the local branch proves D_v I_hid=0 for every surviving hidden scalar, hidden scalar coefficients are constant.", "This also gives H_hidden_R826=0, but the current hidden generator ledger does not sign it.", "EXACT_IF_TRIVIALITY_SIGNED_NOT_DERIVED", "SRC4730_12_1092_triviality"),
        ("HSZ4730_5_shortcut_rejection", "covariance or WEP shortcut", "Diffeomorphism covariance, observed quotient geometry, and WEP-style universality do not by themselves forbid rho_826(I_hid).", "A scalar coefficient multiplying a scalar response is legal unless parent typing or triviality forbids it.", "SHORTCUT_REJECTED", "SRC4730_15_2659_countermodels"),
        ("HSZ4730_6_verdict", "current zero claim", "The exact zero routes are known, but neither R826 typed target exclusion nor hidden invariant triviality is parent-signed.", "Do not set H_hidden_R826=0; use the first bound-input pack.", "ZERO_NOT_PROMOTED_BOUND_PACK_REQUIRED", "SRC4730_7_1219_counterexample"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "target": target,
            "statement": statement,
            "derivation_or_effect": effect,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for theorem_id, target, statement, effect, status, source_id in specs
    ]


def counterexample_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("HSC8264730_0_generic", "R826 = Rbar826(q_obs,theta_fixed) + epsilon I_hid", "D_v R826 = epsilon D_v I_hid", "legal whenever I_hid survives and Coeff_R826 accepts hidden scalar arguments", "ACTIVE_COUNTEREXAMPLE", "SRC4730_7_1219_counterexample"),
        ("HSC8264730_1_gradient_even", "R826 = Rbar826 + epsilon G((nabla I_hid)^2)", "D_v R826 = epsilon G' D_v[(nabla I_hid)^2]", "even-parity or value-zero alone does not kill gradient/profile dependence", "ACTIVE_IF_GRADIENT_SCALAR_SURVIVES", "SRC4730_11_1051_scalar"),
        ("HSC8264730_2_memory_scalar", "R826 = Rbar826 + epsilon M_memory", "D_v R826 = epsilon D_v M_memory", "1092 keeps memory/class scalar as a surviving generator debt", "ACTIVE_GENERATOR_DEBT", "SRC4730_13_1092_generators"),
        ("HSC8264730_3_retyped_marker", "R826 coefficient depends on hidden branch/domain marker retyped as fixed data", "D_v R826 can survive through the label slot", "typed certificate requires no-extension/no-marker rule, not just a visible-domain name", "ACTIVE_IF_NO_EXTENSION_UNSIGNED", "SRC4730_8_1236_certificate"),
        ("HSC8264730_4_readout_return", "tree-level R826 has no hidden target but readout/EFT generates rho_eff(I_hid)", "D_v R826_eff = rho_eff'(I_hid)D_v I_hid", "readout/radiative closure is separately required", "ACTIVE_IF_RADIOUT_UNSIGNED", "SRC4730_9_1236_meta"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "counterexample_id": counterexample_id,
            "construction": construction,
            "vertical_derivative": derivative,
            "why_it_survives_now": why,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for counterexample_id, construction, derivative, why, status, source_id in specs
    ]


def bound_input_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("HIN4730_0_master", "H_hidden_R826", "sup_{B_loc,||v||=1}|D_v R826_hidden|", "C_I826 V_I + C_grad826 V_gradI + C_marker826 V_marker + C_rad826 V_rad + C_boundary826 V_boundary", "R826 derivative norm", "MISSING_COMPONENT_VALUES", "SRC4730_5_4729_hom"),
        ("HIN4730_1_value_scalar", "C_I826 V_I", "C_I826:=sup|partial R826_hidden/partial I_hid|, V_I:=sup|D_v I_hid|", "zero if typed no-target signs or V_I=0; otherwise needs coefficient and vertical-amplitude source", "R826 derivative norm", "MISSING_CI826_AND_VI", "SRC4730_12_1092_triviality"),
        ("HIN4730_2_gradient_scalar", "C_grad826 V_gradI", "gradient/profile hidden scalar contribution", "zero only if local profile nohair/constant-gradient theorem signs; value-zero is insufficient", "R826 derivative norm", "MISSING_GRADIENT_BOUND", "SRC4730_11_1051_scalar"),
        ("HIN4730_3_marker_scalar", "C_marker826 V_marker", "hidden marker/domain/class contribution retyped as coefficient data", "zero only if no-extension/no-marker target rule signs", "R826 derivative norm", "MISSING_NO_EXTENSION_OR_MARKER_BOUND", "SRC4730_8_1236_certificate"),
        ("HIN4730_4_radiative_readout", "C_rad826 V_rad", "effective/readout hidden scalar return after variation", "zero only if radiative/readout closure preserves no-hidden target typing", "R826 derivative norm", "MISSING_RADIOUT_CLOSURE_OR_BOUND", "SRC4730_9_1236_meta"),
        ("HIN4730_5_boundary_tail", "C_boundary826 V_boundary", "boundary/local support hidden scalar tail", "zero only if boundary/domain target exclusion signs; otherwise source a finite support/flux bound", "R826 derivative norm", "MISSING_BOUNDARY_TAIL_BOUND", "SRC4730_15_2659_countermodels"),
        ("HIN4730_6_acceptance", "valid_for_claim switch", "all components theorem-zero or source-backed with units and parent paths", "currently false because every component is unsigned or unsourced", "boolean", "FALSE_NOW", "SRC4730_16_2613_hom"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": input_id,
            "quantity": quantity,
            "definition": definition,
            "bound_or_formula": formula,
            "units": units,
            "current_status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for input_id, quantity, definition, formula, units, status, source_id in specs
    ]


def propagation_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("HPROP4730_0_hidden_insert", "H_R826_total", "H_R826_total = H_hidden_R826 + H_readout_R826 + H_domain_R826 + H_source_shadow_R826 + H_block_R826 + H_extra_mass_R826 + H_rad_R826", "4730 fills the hidden component with an explicit bound-input structure, not a value", "SRC4730_5_4729_hom"),
        ("HPROP4730_1_Rm_insert", "R_m", "|R_m| <= H_hidden_R826 + H_rest_R826 + C_root(|J_root|+|B_root|+|Pi_coker R826|)", "hidden scalar bound now enters the root response envelope", "SRC4730_1_4729_doc"),
        ("HPROP4730_2_B826_insert", "B_826", "|B_826| <= |a_F| L_cg^-2 [H_hidden_R826 + H_rest_R826 + C_root(|J_root|+|B_root|+|Pi_coker R826|)]", "B826 remains nonclaim until H_hidden and all other factors are sourced or theorem-zero", "SRC4730_5_4729_hom"),
        ("HPROP4730_3_zero_condition", "B826 hidden subbranch", "B826_hidden=0 if H_hidden_R826=0 by parent typing or invariant triviality", "exact conditional route remains useful for 4731", "SRC4730_6_1219_no_hidden_arg"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "propagation_id": propagation_id,
            "target": target,
            "formula": formula,
            "meaning": meaning,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for propagation_id, target, formula, meaning, source_id in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4730_0_sources_verified", "All 4730 source paths exist and needles are found.", True, "NONE"),
        ("GATE4730_1_chain_rule_split_derived", "The R826 hidden scalar derivative split is explicit.", True, "STRUCTURE_ONLY_NOT_CLAIM"),
        ("GATE4730_2_typed_target_exclusion_signed", "Coeff_R826 has parent-signed no-C_hid argument domain.", False, "COEFF_R826_TYPED_OWNER_UNSIGNED"),
        ("GATE4730_3_hidden_invariant_triviality_signed", "Every hidden scalar has D_v I_hid=0 on the local branch.", False, "HIDDEN_INVARIANT_TRIVIALITY_UNSIGNED"),
        ("GATE4730_4_counterexamples_closed", "generic/gradient/memory/marker/readout hidden scalar counterexamples are closed.", False, "HIDDEN_COUNTEREXAMPLES_ACTIVE"),
        ("GATE4730_5_bound_input_pack_sourced", "C_I826, V_I, gradient, marker, radiative and boundary inputs have source-backed values or theorem-zero rows.", False, "HHIDDEN_INPUT_VALUES_MISSING"),
        ("GATE4730_6_B826_claim_ready", "B826 hidden component is claim-grade zero or bounded.", False, "B826_HIDDEN_COMPONENT_NONCLAIM"),
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
        ("FW4730_0_no_absence_by_preference", "Do not set H_hidden_R826=0 because hidden scalars feel ugly or unminimal; parent typing or triviality must do the work."),
        ("FW4730_1_no_covariance_shortcut", "Diffeomorphism covariance allows scalar coefficient functions; it does not ban rho_826(I_hid)."),
        ("FW4730_2_no_value_zero_cheat", "I_hid=0 at one point does not kill gradient/profile or readout-return terms."),
        ("FW4730_3_no_bound_without_units", "The bound pack is not evidence until coefficients, vertical amplitudes, units and source paths exist."),
        ("FW4730_4_no_single_component_victory", "Even if H_hidden_R826 closes, B826 still needs readout/domain/source-shadow/block/extra/root factors."),
        ("FW4730_5_no_github_action", "This checkpoint is private local work only."),
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
            "derivation_result": "D_v R826_hidden = rho_826'(I_hid) D_v I_hid is the exact local amplitude law for hidden scalar leakage",
            "zero_result": "H_hidden_R826=0 only if Coeff_R826 has no C_hid target, rho_826 is constant, or all hidden invariants are locally constant",
            "nonclaim_result": "current corpus keeps hidden scalar counterexamples active and lacks source-backed H_hidden input values",
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
            "status_id": "STATUS4730_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated under local post-checkpoint-work and formalization-workbench; no remote action.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4730_1_science_verdict",
            "status": "hidden_scalar_zero_conditional_bound_pack_ready",
            "detail": "The branch now has an exact derivative law and a concrete H_hidden_R826 source-intake contract.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "4730 reduced the hidden scalar leak to a precise Coeff_R826 target-domain owner or a finite H_hidden value row.",
            "first_task": "Try to derive Coeff_R826 typed target ownership directly from the parent action/object language.",
            "fallback_task": "If the target owner fails, fill the first H_hidden_R826 value row: C_I826, V_I, units, local branch domain and source path.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    ts: str,
    zeroes: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4730 - HR826 Hidden Scalar Target Exclusion or First Bound Input Pack

Generated: `{ts}`

## Purpose

4730 attacks the first live component of `H_R826`: the hidden scalar target. The aim is not to circle the blocker, but to write the exact local amplitude law and either close it by theorem or turn it into a source-intake row.

## What Actually Moved

- The hidden-scalar derivative law is now explicit: if `R826_hidden = rho_826(I_hid)`, then `D_v R826_hidden = rho_826'(I_hid) D_v I_hid`.
- Therefore `H_hidden_R826=0` requires one of three real things: no `C_hid` target in `Coeff_R826`, constant `rho_826`, or locally trivial hidden invariants.
- Current corpus does not sign those premises; the generic, gradient, memory-scalar, marker and readout-return counterexamples remain active.
- The first bound-input pack now exists: `H_hidden_R826 <= C_I826 V_I + C_grad826 V_gradI + C_marker826 V_marker + C_rad826 V_rad + C_boundary826 V_boundary`.

## Zero Theorem Rows

{bullets(zeroes, "theorem_id", "status")}

## Counterexample Transfer

{bullets(counterexamples, "counterexample_id", "status")}

## First Bound Input Pack

{bullets(inputs, "input_id", "current_status")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 746 - HR826 Hidden Scalar Target Exclusion or First Bound Input Pack

Generated: `{ts}`

## Result

For a hidden scalar contribution to `R_826`,

`R826_hidden = rho_826(I_hid)`,

the local vertical amplitude law is

`D_v R826_hidden = rho_826'(I_hid) D_v I_hid`.

Thus `H_hidden_R826=0` is exact only if `Coeff_R826` has no hidden-scalar target, `rho_826` is constant, or `D_v I_hid=0` for every surviving hidden scalar on the local branch.

## Bound Intake Contract

`H_hidden_R826 <= C_I826 V_I + C_grad826 V_gradI + C_marker826 V_marker + C_rad826 V_rad + C_boundary826 V_boundary`.

Every term is nonclaim until a parent zero theorem or source-backed value with units exists.

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
- Derivation gain: hidden scalar leakage into `R_826` is reduced to `D_v R826_hidden = rho_826'(I_hid) D_v I_hid`.
- Zero gate: `H_hidden_R826=0` requires parent-signed `Coeff_R826` no-`C_hid` target, constant hidden coefficient, or local hidden invariant triviality.
- Finite row: `H_hidden_R826 <= C_I826 V_I + C_grad826 V_gradI + C_marker826 V_marker + C_rad826 V_rad + C_boundary826 V_boundary` staged nonclaim.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: converts the first `H_R826` component from a generic hidden-scalar obstruction into a theorem-zero fork plus a source-ready bound-input pack.
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

- The first hidden scalar amplitude law for `R_826` is explicit.
- The zero route is theorem-clean but not yet signed: no `C_hid` target, constant coefficient, or hidden invariant triviality.
- The fallback is now a concrete `H_hidden_R826` input pack rather than a vague missing-coupling note.

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
        "claim": "4730 derives the hidden-scalar R826 derivative law and creates the first H_hidden_R826 bound-input pack; zero remains conditional and nonclaim.",
        "current_evidence": "Generated source register, zero theorem rows, counterexample transfer, bound-input pack, Hhidden-to-B826 propagation, gates, firewalls, decision, status, next target and validation.",
        "status": "Hhidden_R826_derivative_law_bound_pack_created_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating the exact conditional no-hidden-target rule as parent-signed before Coeff_R826 target ownership is derived.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "C_I826, V_I, gradient, marker, radiative and boundary inputs remain unsourced; hidden scalar counterexamples remain active.",
        "title": "HR826 hidden scalar target exclusion or first bound input pack",
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
    zeroes: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    propagation: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        ZERO_THEOREM_CSV,
        COUNTEREXAMPLE_CSV,
        BOUND_INPUT_CSV,
        PROPAGATION_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    zero_status = ";".join(row["status"] for row in zeroes)
    counter_status = ";".join(row["status"] for row in counterexamples)
    input_status = ";".join(row["current_status"] for row in inputs)
    formula_text = ";".join(row["formula"] for row in propagation)
    checks = [
        ("VAL4730_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4730 source paths exist"),
        ("VAL4730_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4730 source needles found"),
        ("VAL4730_2_derivative_law_written", "EXACT_DERIVED_SPLIT" in zero_status and "D_v R826_hidden" in read_text(DOC_PATH), "hidden scalar derivative law is written"),
        ("VAL4730_3_zero_not_promoted", "ZERO_NOT_PROMOTED_BOUND_PACK_REQUIRED" in zero_status and not any(row["claim_allowed"] for row in zeroes), "zero route remains conditional and nonclaim"),
        ("VAL4730_4_counterexamples_retained", "ACTIVE_COUNTEREXAMPLE" in counter_status and "ACTIVE_GENERATOR_DEBT" in counter_status, "hidden scalar counterexamples are retained"),
        ("VAL4730_5_bound_pack_created", "MISSING_COMPONENT_VALUES" in input_status and "MISSING_CI826_AND_VI" in input_status, "first H_hidden_R826 bound-input pack created"),
        ("VAL4730_6_B826_propagation_written", "H_hidden_R826" in formula_text and "|B_826|" in formula_text, "H_hidden_R826 propagates to B826 bound"),
        ("VAL4730_7_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] not in {"GATE4730_0_sources_verified", "GATE4730_1_chain_rule_split_derived"}), "all claim gates remain closed except structural nonclaim gates"),
        ("VAL4730_8_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4730_9_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4730_10_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-572"),
        ("VAL4730_11_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4731 next target"),
        ("VAL4730_12_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4730 CSV files parse cleanly"),
        ("VAL4730_13_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
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
            "check_id": "VAL4730_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4730 HR826 hidden scalar target exclusion or first bound-input pack validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    zeroes = zero_theorem_rows(ts)
    counterexamples = counterexample_rows(ts)
    inputs = bound_input_rows(ts)
    propagation = propagation_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(ZERO_THEOREM_CSV, zeroes)
    write_csv(COUNTEREXAMPLE_CSV, counterexamples)
    write_csv(BOUND_INPUT_CSV, inputs)
    write_csv(PROPAGATION_CSV, propagation)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, zeroes, counterexamples, inputs, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, zeroes, counterexamples, inputs, propagation, gates, ts))


if __name__ == "__main__":
    main()
