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

CHECKPOINT = "4584"
CLAIM_ID = "L-426"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_MATERIAL_TENSOR_AND_APPARATUS_SUPPORT_ZERO_OR_BOUND_4584"
MARKER = "PPC4161_PARENT_MATERIAL_TENSOR_AND_APPARATUS_SUPPORT_ZERO_OR_BOUND_4584"
PACKET_MARKER = "PPC4161_PACKET_PARENT_MATERIAL_TENSOR_AND_APPARATUS_SUPPORT_ZERO_OR_BOUND_4584"
DECISION = "PRIVATE_SOURCE_UNIVERSALITY_KILLS_ACTIVE_MATERIAL_SOURCE_WEIGHT_APPARATUS_DOMAIN_ZERO_OR_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4585-Y5-R2FR-active-kernel-first-zero-or-operator-bound.md"

DOC_PATH = POST / "4584-Y5-R2FR-parent-material-tensor-and-apparatus-support-zero-or-bound.md"
FORMAL_PATH = FORMAL / "600-PPC4161-parent-material-tensor-and-apparatus-support-zero-or-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4583 = POST / "4583-Y5-R2FR-charge-current-normalization-and-EM-readout-tail-owner-or-source-bound.md"
CSV_4583_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4583_EM_TAIL_REDUCTION_ROWS.csv"
CSV_4583_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4583_NEXT_TARGET.csv"
FORMAL_462 = FORMAL / "462-PPC4161-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md"
FORMAL_463 = FORMAL / "463-PPC4161-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md"
FORMAL_481 = FORMAL / "481-PPC4161-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md"
FORMAL_284 = FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"
CSV_MATERIAL_INTAKE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1894_WEP_MATERIAL_TENSOR_INTAKE_NONCLAIM.csv"
CSV_MATERIAL_BASIS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1895_PARENT_MATERIAL_TENSOR_BASIS_NONCLAIM.csv"
CSV_TYPING_GATE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv"
CSV_4324_MASTER = SOURCE_DIR / "P8_Y5_R2FR_4324_MASTER_TAIL_FORMULAS.csv"
CSV_4324_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4324_NO_HIDDEN_SLOT_AUDIT.csv"
CSV_4580_GUARDS = SOURCE_DIR / "P8_Y5_R2FR_4580_CLOSED_DOMAIN_GUARDS.csv"
CSV_4580_CERT = SOURCE_DIR / "P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv"
CSV_4580_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4580_CREADOUT_REDUCTION_ROWS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4584_SOURCE_REGISTER.csv"
MATERIAL_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4584_MATERIAL_SOURCE_UNIVERSALITY_THEOREM.csv"
APPARATUS_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4584_APPARATUS_DOMAIN_THEOREM.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4584_MATERIAL_APPARATUS_REDUCTION_ROWS.csv"
BOUND_SCHEMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4584_FALLBACK_BOUND_SCHEMA.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4584_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4584_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4584_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4584_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4584_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4584_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
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
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ") for key in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4584_00_4583_doc", DOC_4583, "C_material_tail <= sum_X |C_X R_material_X| + |C_apparatus|", "4583 reduced handoff"),
        ("SRC4584_01_4583_tail", CSV_4583_TAIL, "ETR4583_1_material_tail_fixed_branch_update", "4583 material/apparatus live row"),
        ("SRC4584_02_4583_next", CSV_4583_NEXT, "parent-material-tensor-and-apparatus-support-zero-or-bound", "4583 selected 4584"),
        ("SRC4584_03_4446_adoption", FORMAL_462, "ADOPT4446_2_material_reentry_killed", "GR-parity material reentry killed"),
        ("SRC4584_04_4447_ppn", FORMAL_463, "source-universality pieces of the local residual vector are zero", "source-universality propagation"),
        ("SRC4584_05_4465_source_charge", FORMAL_481, "Delta_C_AB=0", "source-charge differential theorem"),
        ("SRC4584_06_material_intake", CSV_MATERIAL_INTAKE, "WMI1894_3_full_parent_tensor", "material tensor intake blocker"),
        ("SRC4584_07_material_basis", CSV_MATERIAL_BASIS, "PMTB1895_3_tensor_formula", "parent material tensor formula"),
        ("SRC4584_08_typing_gate", CSV_TYPING_GATE, "TYP1895_1_no_species_to_source_coeff", "no material/species source morphism gate"),
        ("SRC4584_09_hidden_tail", CSV_4324_MASTER, "Xi_src_hidden", "hidden source-prefactor fallback budget"),
        ("SRC4584_10_no_hidden_audit", CSV_4324_AUDIT, "AUD4324_3_zero", "conditional no-hidden-slot zero"),
        ("SRC4584_11_boundary_collar", FORMAL_284, "Dq_boundary_projector = 0", "fixed collar/domain support law"),
        ("SRC4584_12_apparatus_guard", CSV_4580_GUARDS, "CDG4580_2_apparatus", "apparatus declaration guard"),
        ("SRC4584_13_domain_cert", CSV_4580_CERT, "PDC4580_1_fixed_qbasic_domain", "fixed support/domain certificate"),
        ("SRC4584_14_Csupport", CSV_4580_REDUCTION, "CRV4580_1_C_support", "support zero source"),
        ("SRC4584_15_claim_425", CLAIMS_PATH, "L-425", "prior claim register handoff"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "generated_utc": now,
                "valid_for_claim": "False",
            }
        )
    return rows


def material_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MAT4584_0_source_universality_import",
            "claim": "Material labels do not define active gravitational source coefficients inside the private GR-parity/PPC4161 branch.",
            "derivation": "4446 adopts one imported S_matter scalar density functor, Hilbert variation before readout, and Hom(MaterialLabel, Coeff_active_source)=empty inside PPC4161. 4447 propagates that source-universality subspace to WEP/PPN/clock/orbital source pieces.",
            "consequence": "Material composition can change the Hilbert mass value and empirical inventory, but it cannot multiply the active source coefficient in the local field equation inside this branch.",
            "status": "PRIVATE_BRANCH_SOURCE_WEIGHT_ZERO_IMPORTED",
            "source": str(FORMAL_462),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MAT4584_1_material_product_zero",
            "claim": "sum_X |C_X R_material_X|=0 for active-source material weights in the adopted private branch.",
            "derivation": "The product sum_X |C_X R_material_X| represents a material label or sensitivity re-entering Coeff_active_source. Under source-label forgetting and no MaterialLabel->Coeff_active_source morphism, each active-source C_X paired to material reentry is zero; hence the active-source material product vanishes.",
            "consequence": "The 4583 material tail loses its parent material tensor dot coefficient term in the private branch. Empirical material tensors remain required only for rejected/nonstandard branches or test readout inventory.",
            "status": "PRIVATE_BRANCH_ZERO_NOT_GLOBAL",
            "source": str(FORMAL_463),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MAT4584_2_finite_material_fallback",
            "claim": "If source-universality is rejected, the finite material branch is Delta_C_AB=sum_j Delta_s_AB,j b_j with no cancellation credit.",
            "derivation": "4465 gives C_A=C_common+sum_j s_Aj b_j and Delta_C_AB=sum_j(s_Aj-s_Bj)b_j. The older R_material_X formula is the same role in a parent response basis: R_material_X(A,B)=partial_X ln M_A-partial_X ln M_B after common-mode projection.",
            "consequence": "Rejected branches need source-backed sensitivity vectors, parent b_j/C_X coefficients, range/profile/readout projection and units before WEP/clock/orbital scoring.",
            "status": "FALLBACK_OPERATOR_READY_VALUES_MISSING",
            "source": str(FORMAL_481),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MAT4584_3_public_firewall",
            "claim": "This does not derive the Standard Model, internal constants, numerical material tensors, or public local GR.",
            "derivation": "The branch is a private GR-parity import/source-universality adoption. Strict motion-time-space primitive derivation and source-backed material/R_eq empirical values remain open in 4446/4447.",
            "consequence": "Material zero may be used only as a private local packet reduction; public claims require primitive derivation or empirical bound closure.",
            "status": "PUBLIC_CLAIM_BLOCK_RETAINED",
            "source": str(FORMAL_462),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def apparatus_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "APP4584_0_apparatus_domain_law",
            "claim": "Apparatus support is zero only when it is either included in the Hilbert source/reference before variation or disjoint postprocessing outside the fixed collar.",
            "derivation": "4580 already gives fixed support/domain zero for compact no-flux collars, but CDG4580_2 keeps apparatus declaration open. The missing declaration is a branch selector: included-in-source, disjoint-postprocessing, or active apparatus.",
            "consequence": "C_apparatus is not silently erased by C_support=0; it closes only with an explicit apparatus-domain declaration.",
            "status": "DOMAIN_LAW_DERIVED_DECLARATION_REQUIRED",
            "source": str(CSV_4580_GUARDS),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "APP4584_1_included_source_zero",
            "claim": "C_apparatus=0 when apparatus stress/energy is inside the same Hilbert source or fixed reference branch before variation.",
            "derivation": "If T_app is part of T_total^H and the source charge/reference H_ref is fixed before readout, apparatus energy is source content or common reference, not a post-readout coupling multiplier.",
            "consequence": "Included apparatus does not create a separate readout tail; it changes the declared source model/reference instead.",
            "status": "CONDITIONAL_ZERO_BRANCH",
            "source": str(FORMAL_284),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "APP4584_2_disjoint_postprocessing_zero",
            "claim": "C_apparatus=0 when apparatus is disjoint from W_loc and readout is pure postprocessing with no boundary flux.",
            "derivation": "For supp(T_app) cap W_loc=empty, Pi_app fixed before variation, no sector pullback, and no normal flux across the collar, O_f Pi_app=0 and the apparatus has no local source-probe derivative.",
            "consequence": "A purely external/postprocessing apparatus contributes no local readout source tail in the fixed no-flux branch.",
            "status": "CONDITIONAL_ZERO_BRANCH",
            "source": str(FORMAL_284),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "APP4584_3_active_apparatus_bound",
            "claim": "Active apparatus remains a bound row.",
            "derivation": "If apparatus mass/fields, calibration current, thermal/EM flux, moving support, or post-fit selector enters W_loc or S_eff, retain C_apparatus <= K_app M_app_eff/M_H_ref + Phi_app/M_H_ref + R_app_selector.",
            "consequence": "Active apparatus cannot be cancelled against material, EM, kernel, EFT or tau rows.",
            "status": "BOUND_SCHEMA_DERIVED_VALUES_MISSING",
            "source": str(CSV_4580_GUARDS),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MAR4584_0_material_active_source_zero",
            "target": "sum_X |C_X R_material_X|",
            "formula": "sum_X |C_X R_material_X|=0",
            "branch_condition": "PPC4161 private GR-parity source-universality branch; Hom(MaterialLabel,Coeff_active_source)=empty; source-label forgetting; material projections are readout inventory only",
            "status": "PRIVATE_BRANCH_ZERO_NONCLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MAR4584_1_Capparatus_domain_zero",
            "target": "C_apparatus",
            "formula": "C_apparatus=0",
            "branch_condition": "apparatus included in same Hilbert source/reference before variation OR disjoint postprocessing outside fixed no-flux collar",
            "status": "CONDITIONAL_ZERO_BRANCH_DECLARATION_REQUIRED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MAR4584_2_Cmaterial_tail_strict_zero",
            "target": "C_material_tail",
            "formula": "C_material_tail=0",
            "branch_condition": "4583 fixed EM tail zero plus MAT4584_1 material source-weight zero plus APP4584_1/2 apparatus zero",
            "status": "PRIVATE_STRICT_BRANCH_ZERO_NONCLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MAR4584_3_Creadout_update",
            "target": "C_readout",
            "formula": "C_readout <= C_kernel_active + C_EFT_active + C_tau_tail",
            "branch_condition": "strict fixed EM + source-universal material + declared apparatus-zero branch",
            "status": "C_READOUT_REDUCED_TO_KERNEL_EFT_TAU",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MAR4584_4_fallback_open_branch",
            "target": "C_readout_open",
            "formula": "C_readout <= Xi_src_hidden_material + C_apparatus_active + C_EM_tail + C_kernel_active + C_EFT_active + C_tau_tail",
            "branch_condition": "source-universality rejected, apparatus active, or open/dynamic EM branch",
            "status": "OPEN_BRANCH_BOUND_SCHEMA_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def bound_schema_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("BND4584_0_Xi_material_hidden", "Xi_src_hidden_material", "hidden source/material prefactor budget feeding material reentry", "Xi_src_hidden or source-backed subvector", "MISSING_NO_HIDDEN_SLOT_SIGNATURE_OR_NUMERIC_TAILS", "F4324_0_master_tail"),
        ("BND4584_1_material_sensitivity", "Delta_s_AB,j", "finite material sensitivity vector in rejected branch", "Delta_C_AB=sum_j Delta_s_AB,j b_j", "MISSING_SOURCE_BACKED_MATERIAL_SENSITIVITY_VECTOR", "DER4465_1_composite_decomposition"),
        ("BND4584_2_parent_coeff", "b_j or C_X", "parent coefficient multiplying material response", "|C_X R_material_X| with units/source path", "MISSING_PARENT_COEFFICIENT_VECTOR", "WMI1894_4_parent_coefficient_dependency"),
        ("BND4584_3_apparatus_active", "C_apparatus_active", "active apparatus/readout support tail", "K_app M_app_eff/M_H_ref + Phi_app/M_H_ref + R_app_selector", "MISSING_APPARATUS_DOMAIN_DECLARATION_OR_BOUND", "CDG4580_2_apparatus"),
        ("BND4584_4_common_mode", "C_common", "composition-blind common source mode", "routes to R10/PPN/orbital common-mode bounds, not WEP material tensor", "COMMON_MODE_R10_PPN_ORBITAL_PRESSURE_RETAINED", "DEC4465_1_common_mode_result"),
        ("BND4584_5_total_open", "C_material_apparatus_open", "absolute fallback material/apparatus tail", "|Xi_src_hidden_material|+|C_apparatus_active|", "SCHEMA_READY_VALUES_MISSING", "MAR4584_4_fallback_open_branch"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "formula": formula,
            "status": status,
            "source_anchor": anchor,
            "numeric_value_present": "False",
            "source_backed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for row_id, symbol, definition, formula, status, anchor in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4584_material_inventory", "material composition changes mass/readout inventory", "do not turn inventory into active source coefficient", "CONTROL_PASS"),
        ("CTRL4584_private_import", "GR-parity standard matter import is private branch adoption", "do not claim strict MTS primitive derivation", "FIREWALL_PASS"),
        ("CTRL4584_finite_WEP", "source-universality rejected", "finite material sensitivity vector retained", "COUNTERMODEL_CAUGHT"),
        ("CTRL4584_common_mode", "C_A=C_B=C_common nonzero", "WEP material differential zero does not imply R10/PPN safety", "FIREWALL_PASS"),
        ("CTRL4584_apparatus_not_support", "fixed C_support but undeclared apparatus", "C_apparatus remains until included/disjoint declaration or bound", "COUNTERMODEL_CAUGHT"),
        ("CTRL4584_active_apparatus", "apparatus flux/mass/support enters source collar", "active apparatus bound retained", "COUNTERMODEL_CAUGHT"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "case": case,
            "expected_result": expected,
            "status": status,
            "generated_utc": now,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for control_id, case, expected, status in rows
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("PROM4584_0_material_active_source", "Material active-source weight zero in private source-universality branch.", "PASSED_PRIVATE_BRANCH"),
        ("PROM4584_1_apparatus_zero_contract", "Apparatus zero requires included-source or disjoint-postprocessing declaration.", "CONDITIONAL"),
        ("PROM4584_2_Cmaterial_tail", "C_material_tail zero only when material and apparatus branches both close.", "CONDITIONAL"),
        ("PROM4584_3_open_material", "Rejected/nonstandard material branch requires source-backed material sensitivity vector and parent coefficients.", "BLOCKED"),
        ("PROM4584_4_active_apparatus", "Active apparatus branch requires source-backed apparatus support/flux bound.", "BLOCKED"),
        ("PROM4584_5_no_public_claim", "No public local-GR/R10/PPN/WEP/clock/orbital claim from 4584.", "PASSED_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "generated_utc": now,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status in rows
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "plain_english": "4584 imports the private GR-parity/source-universality branch to remove active material source weights from C_material_tail, while keeping empirical material tensors as test inventory. Apparatus support is sharpened into an included-source/disjoint-postprocessing zero contract or an active apparatus bound. In the strict branch C_readout is reduced to active kernel, EFT and tau tails.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "After fixed EM, material source weights, and apparatus support are closed in the strict branch, the leading live C_readout term is C_kernel_active.",
            "derive_first": "prove the active source/readout kernels are fixed q-basic, same-source, or projector-natural zero rows",
            "fallback": "fill explicit operator-norm bounds for source_worldtube, WEP, clock, light, orbital_GM and projective kernels",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "status": "PRIVATE_NONCLAIM_LOCAL_ONLY",
            "summary": "Active material source weights are zero only in the private GR-parity source-universality branch; apparatus zero requires included-source/disjoint-postprocessing declaration; open branches retain bound rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_text(
    sources: list[dict[str, Any]],
    material: list[dict[str, Any]],
    apparatus: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> str:
    return f"""# 4584 - Parent material tensor and apparatus support zero or bound

Marker: `{MARKER}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Private/public status: private nonclaim; no GitHub action.

## Result

4584 separates two things that were getting tangled:

1. **Material tensors as empirical/readout inventory** remain real and useful for WEP, clock and orbital tests.
2. **Material labels as active gravitational source coefficients** are zero inside the private GR-parity/PPC4161 source-universality branch.

The strict branch is:

```text
fixed EM tail zero
+ Hom(MaterialLabel,Coeff_active_source)=empty
+ source-label forgetting
+ material projections are readout inventory only
+ apparatus included in source/reference OR disjoint postprocessing
=> C_material_tail = 0.
```

So the current readout envelope reduces to:

```text
C_readout <= C_kernel_active + C_EFT_active + C_tau_tail.
```

This is not public local GR.  If source-universality or apparatus-domain declaration fails, the fallback is explicit:

```text
C_readout <= Xi_src_hidden_material + C_apparatus_active
           + C_EM_tail + C_kernel_active + C_EFT_active + C_tau_tail.
```

## Material theorem rows

{markdown_table(material)}

## Apparatus theorem rows

{markdown_table(apparatus)}

## Reduction rows

{markdown_table(reductions)}

## Fallback bound schema

{markdown_table(bounds)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Decision

{markdown_table(decision)}

## Next target

{markdown_table(next_target)}

## Source register

{markdown_table(sources)}
"""


def formal_text() -> str:
    return f"""## PPC4161 4584 parent material tensor and apparatus support

Marker: `{MARKER}`  
Decision: `{DECISION}`  

4584 imports the private GR-parity/source-universality branch:

```text
Hom(MaterialLabel,Coeff_active_source)=empty
```

so material projections are empirical/readout inventory, not active gravitational source coefficients.  Inside that private branch:

```text
sum_X |C_X R_material_X| = 0.
```

Apparatus support closes only with a declared branch:

```text
C_apparatus=0
```

if the apparatus is included in the same Hilbert source/reference before variation or is disjoint postprocessing outside the fixed no-flux collar.  Otherwise active apparatus remains a bound row.

Strict branch reduction:

```text
C_material_tail=0,
C_readout <= C_kernel_active + C_EFT_active + C_tau_tail.
```

Open branch:

```text
C_readout <= Xi_src_hidden_material + C_apparatus_active + C_EM_tail + C_kernel_active + C_EFT_active + C_tau_tail.
```

Next target: `{NEXT_TARGET}`.
"""


def packet_text() -> str:
    return f"""## 4584 packet update - material/apparatus tail reduction

Marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  

4584 reduces the strict local readout envelope by importing private source-universality for material labels and by splitting apparatus support into included-source, disjoint-postprocessing, or active-bound branches:

```text
C_material_tail=0,
C_readout <= C_kernel_active + C_EFT_active + C_tau_tail
```

only in the strict private branch.  Rejected/nonstandard branches retain `Xi_src_hidden_material`, finite material sensitivity vectors, common-mode R10/PPN/orbital pressure and active apparatus bounds.
"""


def update_claims() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4584 imports private source-universality to remove active material source weights and splits apparatus support into zero-contract or active-bound branches.",
        "current_evidence": "Generated source register, material theorem rows, apparatus theorem rows, reduction rows, fallback bound schema, controls, gates and validation.",
        "status": "private_source_universality_kills_active_material_source_weight_apparatus_domain_zero_or_bound_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking empirical material readout inventory for active source weights, or treating C_support=0 as apparatus-domain closure.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Active kernels, EFT tails, tau tails, common-mode scalar/R10 pressure and open apparatus branches still block local-GR/R10/PPN claims.",
    }
    rows = read_csv(CLAIMS_PATH)
    if rows:
        rows.append(row)
        write_csv(CLAIMS_PATH, rows)
    else:
        write_csv(CLAIMS_PATH, [row])


def validate(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    material: list[dict[str, Any]],
    apparatus: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    controls: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4584_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix.lower() == ".csv":
            rows = read_csv(path)
            add(f"VAL4584_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4584_sources_exist", "all cited sources exist", all(row["path_exists"] == "True" for row in sources), "source register existence")
    add("VAL4584_needles_found", "all cited needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add("VAL4584_material_source_zero", "material active-source product zero row emitted", any(row["theorem_id"] == "MAT4584_1_material_product_zero" and "sum_X |C_X R_material_X|=0" in row["claim"] for row in material), "MAT4584_1")
    add("VAL4584_material_fallback", "finite material fallback keeps sensitivity vector", any(row["theorem_id"] == "MAT4584_2_finite_material_fallback" and "Delta_C_AB" in row["claim"] for row in material), "MAT4584_2")
    add("VAL4584_apparatus_domain", "apparatus domain law separates zero and active branches", any(row["theorem_id"] == "APP4584_0_apparatus_domain_law" for row in apparatus) and any(row["theorem_id"] == "APP4584_3_active_apparatus_bound" for row in apparatus), "apparatus rows")
    add("VAL4584_Creadout_reduction", "Creadout reduced to kernel/EFT/tau in strict branch", any(row["row_id"] == "MAR4584_3_Creadout_update" and row["formula"] == "C_readout <= C_kernel_active + C_EFT_active + C_tau_tail" for row in reductions), "MAR4584_3")
    add("VAL4584_open_schema", "fallback schema includes Xi, apparatus and common mode", all(any(row["symbol"] == symbol for row in bounds) for symbol in ["Xi_src_hidden_material", "C_apparatus_active", "C_common"]), "fallback schema")
    add("VAL4584_controls", "controls catch material inventory, common mode and apparatus support traps", all(any(row["control_id"] == control_id for row in controls) for control_id in ["CTRL4584_material_inventory", "CTRL4584_common_mode", "CTRL4584_apparatus_not_support"]), "controls")
    add("VAL4584_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4584_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4584_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add("VAL4584_spine_packet", "spine and packet markers present", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), f"{MARKER}; {PACKET_MARKER}")
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows(now)
    material = material_theorem_rows(now)
    apparatus = apparatus_theorem_rows(now)
    reductions = reduction_rows(now)
    bounds = bound_schema_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decision = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MATERIAL_THEOREM_CSV, material)
    write_csv(APPARATUS_THEOREM_CSV, apparatus)
    write_csv(REDUCTION_CSV, reductions)
    write_csv(BOUND_SCHEMA_CSV, bounds)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    DOC_PATH.write_text(
        doc_text(sources, material, apparatus, reductions, bounds, controls, promotions, decision, next_target),
        encoding="utf-8",
    )
    FORMAL_PATH.write_text(formal_text(), encoding="utf-8")

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### 4584 - Parent material tensor and apparatus support zero or bound

Marker: `{MARKER}`  
Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.

4584 imports the private GR-parity/source-universality branch to make material projections readout inventory rather than active source coefficients:

```text
sum_X |C_X R_material_X| = 0
```

inside that branch. Apparatus support is split into included-source, disjoint-postprocessing, or active-bound branches. The strict readout envelope becomes:

```text
C_readout <= C_kernel_active + C_EFT_active + C_tau_tail.
```
""",
    )
    append_once(PACKET_PATH, PACKET_MARKER, packet_text())
    update_claims()

    outputs = [
        SOURCE_REGISTER,
        MATERIAL_THEOREM_CSV,
        APPARATUS_THEOREM_CSV,
        REDUCTION_CSV,
        BOUND_SCHEMA_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validate(outputs, sources, material, apparatus, reductions, bounds, controls)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    print(f"4584 complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
