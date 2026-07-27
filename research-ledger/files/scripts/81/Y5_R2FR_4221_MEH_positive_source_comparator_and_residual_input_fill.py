from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4221"
CLAIM_ID = "L-062"
BRANCH = "MTS_R2FR_Y5_MEH_POSITIVE_SOURCE_COMPARATOR_GATE_4221"
DECISION = "MEH_POSITIVE_LOWER_BOUND_LAW_DERIVED_RESIDUAL_INPUTS_FILLED_AS_SCHEMA_PARENT_SIGNATURE_VALUES_MISSING_NONCLAIM"
MARKER = "PPC4161_MEH_POSITIVE_SOURCE_COMPARATOR_GATE_4221"
PACKET_MARKER = "PPC4161_PACKET_MEH_POSITIVE_SOURCE_COMPARATOR_GATE_4221"
NEXT_TARGET = "4222-Y5-R2FR-positive-energy-sector-signature-matrix-or-negative-energy-bound-fill.md"

FORMAL_PATH = FORMAL / "237-PPC4161-MEH-positive-source-comparator-and-residual-input-fill.md"
DOC_PATH = POST / "4221-Y5-R2FR-MEH-positive-source-comparator-and-residual-input-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4221_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4221_00_4220_next": SourceSpec(
        "SRC4221_00_4220_next",
        SOURCE_DIR / "P8_Y5_R2FR_4220_NEXT_TARGET.csv",
        "4221-Y5-R2FR-MEH-positive-source-comparator-and-residual-input-fill.md",
        "4220 selected the positive M_EH comparator as the next denominator obstruction.",
    ),
    "SRC4221_01_4220_law": SourceSpec(
        "SRC4221_01_4220_law",
        FORMAL / "236-PPC4161-MHref-positive-source-denominator-stability-or-bound-pack.md",
        "M_H_ref >= M_EH",
        "Current denominator law requiring positive M_EH and residual control.",
    ),
    "SRC4221_02_3944_comparator": SourceSpec(
        "SRC4221_02_3944_comparator",
        SOURCE_DIR / "P8_Y5_R2FR_3944_MEH_COMPARATOR_THEOREM.csv",
        "MEH3944_3_positive_energy",
        "Older comparator theorem fixing M_EH as source-energy comparator.",
    ),
    "SRC4221_03_3945_positive": SourceSpec(
        "SRC4221_03_3945_positive",
        SOURCE_DIR / "P8_Y5_R2FR_3945_MEH_POSITIVE_COMPARATOR_THEOREM.csv",
        "PEC3945_2_positive_energy_sufficient_conditions",
        "Older conditional positivity theorem for M_EH.",
    ),
    "SRC4221_04_3945_first_row": SourceSpec(
        "SRC4221_04_3945_first_row",
        SOURCE_DIR / "P8_Y5_R2FR_3945_MEH_FIRST_SOURCE_ROW.csv",
        "FSR3945_0_local_stationary_total_source",
        "First symbolic source row for local stationary total source branch.",
    ),
    "SRC4221_05_3946_gate": SourceSpec(
        "SRC4221_05_3946_gate",
        SOURCE_DIR / "P8_Y5_R2FR_3946_MEH_POSITIVITY_CERTIFICATE_GATE.csv",
        "MPG3946_3_energy_condition",
        "MEH positivity gate showing missing energy certificate.",
    ),
    "SRC4221_06_3947_bound": SourceSpec(
        "SRC4221_06_3947_bound",
        SOURCE_DIR / "P8_Y5_R2FR_3947_MEH_SIGN_BOUND_CANDIDATE.csv",
        "MBC3947_0_MEH_sign_bound",
        "Earlier sign-bound candidate requiring E_pos and epsilon values.",
    ),
    "SRC4221_07_3948_energy": SourceSpec(
        "SRC4221_07_3948_energy",
        SOURCE_DIR / "P8_Y5_R2FR_3948_MEH_ENERGY_CONDITION_GATE.csv",
        "MEG3948_1_signature_matrix",
        "Energy-condition gate showing missing sector signature matrix.",
    ),
    "SRC4221_08_186_glue": SourceSpec(
        "SRC4221_08_186_glue",
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "M_H^dress[W_H;tau]",
        "Hamiltonian worldtube mass readout glue.",
    ),
    "SRC4221_09_187_newton": SourceSpec(
        "SRC4221_09_187_newton",
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "int_W rho_H dV",
        "Poisson/Gauss/Newton readout from Hamiltonian charge.",
    ),
    "SRC4221_10_194_coupling": SourceSpec(
        "SRC4221_10_194_coupling",
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi)",
        "Calibrated source coupling guard against numerical-G overclaim.",
    ),
    "SRC4221_11_227_contract": SourceSpec(
        "SRC4221_11_227_contract",
        FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md",
        "`M_H_ref` is positive",
        "Parent charge-owner contract requiring positive same-frame source denominator.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source in SOURCE_SPECS.values():
        text = read_text(source.path)
        rows.append(
            {
                **common(),
                "source_id": source.source_id,
                "path": str(source.path),
                "exists": str(source.path.exists()),
                "required_text": source.required_text,
                "required_text_found": str(source.required_text in text),
                "role": source.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def law_rows() -> List[Dict[str, str]]:
    data = [
        (
            "MEL4221_0_same_frame_object",
            "same-frame M_EH comparator",
            "M_EH[tau,W_source] := c^-2 E_total[tau,W_source]",
            "definition",
            "The comparator is the total source energy mass in the same tau/coframe/worldtube branch as M_H_ref.",
            "exact_conditional",
        ),
        (
            "MEL4221_1_total_energy_split",
            "positive minus controlled residual split",
            "E_total = E_plus - E_neg_abs - E_open_abs - E_ref_abs - E_vir_abs - E_nonEH_abs - E_frame_abs",
            "derived_ledger_identity",
            "The sign problem is made additive: every possible sign-destroying contribution is named instead of hidden.",
            "derived_schema",
        ),
        (
            "MEL4221_2_lower_bound",
            "M_EH lower-bound law",
            "M_EH >= c^-2 E_plus*(1 - epsilon_E)",
            "triangle_inequality_bound",
            "epsilon_E=(E_neg_abs+E_open_abs+E_ref_abs+E_vir_abs+E_nonEH_abs+E_frame_abs)/E_plus.",
            "derived_lower_bound_law",
        ),
        (
            "MEL4221_3_strict_positive_gate",
            "strict positivity gate",
            "E_plus>0 and epsilon_E<1 => M_EH>0",
            "strict_sign_condition",
            "This is the actual source-comparator gate needed by 4220; it does not use orbital GM.",
            "claim_ready_only_after_inputs",
        ),
        (
            "MEL4221_4_Komar_Tolman_guard",
            "pressure/stress trap guard",
            "M_Komar/Tolman = M_EH + Delta_vir + Delta_boundary + Delta_nonEH",
            "active_mass_bridge",
            "Pressure terms cancel only under a total closed stationary virial identity or enter epsilon_E as residuals.",
            "conditional_bridge",
        ),
        (
            "MEL4221_5_EM_Poynting_guard",
            "EM/Poynting ownership",
            "E_EM_closed >= 0, Phi_Poynting_open -> E_open_abs",
            "Maxwell_Hodge_source_guard",
            "Poynting helps only as owned Hilbert EM energy or as a boundary flux residual; it is not a second force.",
            "conditional_bridge",
        ),
        (
            "MEL4221_6_denominator_import",
            "feed back into 4220 denominator",
            "M_H_ref >= c^-2 E_plus*(1-epsilon_E)*(1-epsilon_abs)",
            "composed_lower_bound",
            "Combines the 4220 denominator law with the 4221 M_EH lower-bound law.",
            "derived_composed_gate_values_missing",
        ),
    ]
    return [
        {
            **common(),
            "law_id": law_id,
            "claim_piece": claim_piece,
            "formula": formula,
            "derivation_type": derivation_type,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for law_id, claim_piece, formula, derivation_type, derivation, status in data
    ]


def sector_signature_rows() -> List[Dict[str, str]]:
    data = [
        (
            "MES4221_0_visible_matter_rest",
            "visible matter rest/internal energy",
            "E_visible_rest",
            "positive in standard import branch",
            "requires source support and same-frame density row",
            "CONDITIONAL_STANDARD_IMPORT",
        ),
        (
            "MES4221_1_Maxwell_Hodge",
            "descended Maxwell-Hodge field",
            "E_EM=(2*mu0)^-1 int(|E|^2+c^2|B|^2)dV",
            "positive on closed support with observed Hodge signature",
            "open Poynting flux routed to E_open_abs",
            "CONDITIONAL_STANDARD_IMPORT",
        ),
        (
            "MES4221_2_binding_stabilizer",
            "binding/stabilizer sector",
            "E_binding+E_stabilizer",
            "not sign-fixed by current parent action",
            "needs no-ghost/bounded-below signature or negative-energy bound",
            "MISSING_PARENT_SIGNATURE",
        ),
        (
            "MES4221_3_motion_time_space_core",
            "MTS core/action residual sector",
            "E_MTS_core",
            "not sign-fixed by current parent action",
            "needs kinetic/Hessian signature and constraint-stability row",
            "MISSING_PARENT_SIGNATURE",
        ),
        (
            "MES4221_4_topological_boundary",
            "topological/boundary/reference sector",
            "E_ref_abs+E_open_abs",
            "zero only under fixed source-blind reference and no open flux",
            "else finite residual row",
            "BOUND_OR_ZERO_REQUIRED",
        ),
        (
            "MES4221_5_pressure_virial",
            "Komar/Tolman pressure/stress sector",
            "E_vir_abs",
            "zero only under closed stationary total-source virial identity",
            "else finite pressure/stress residual row",
            "BOUND_OR_ZERO_REQUIRED",
        ),
    ]
    return [
        {
            **common(),
            "sector_id": sector_id,
            "sector": sector,
            "energy_piece": energy_piece,
            "sign_status": sign_status,
            "required_evidence": required_evidence,
            "gate_status": gate_status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for sector_id, sector, energy_piece, sign_status, required_evidence, gate_status in data
    ]


def residual_input_rows() -> List[Dict[str, str]]:
    data = [
        (
            "MER4221_0_E_plus",
            "E_plus",
            "strict positive same-frame source energy",
            "visible rest + closed Maxwell-Hodge + any signed positive parent sectors",
            "MISSING_NUMERIC_OR_THEOREM_ROW",
            "energy",
        ),
        (
            "MER4221_1_E_neg_abs",
            "E_neg_abs",
            "absolute negative-sector bound",
            "sum of all unsigned/bounded-below parent sectors",
            "MISSING_SIGNATURE_OR_BOUND",
            "energy",
        ),
        (
            "MER4221_2_E_open_abs",
            "E_open_abs",
            "open/radiative flux leakage",
            "Poynting/radiative/gravity flux through nonclosed source domain",
            "MISSING_ZERO_OR_BOUND",
            "energy",
        ),
        (
            "MER4221_3_E_ref_abs",
            "E_ref_abs",
            "reference subtraction leakage",
            "source-dependent H_ref or reference mismatch",
            "MISSING_REFERENCE_CERTIFICATE_OR_BOUND",
            "energy",
        ),
        (
            "MER4221_4_E_vir_abs",
            "E_vir_abs",
            "pressure/stress virial leakage",
            "Tolman/Komar stress term not cancelled by closed stationary total-source virial identity",
            "MISSING_VIRIAL_ZERO_OR_BOUND",
            "energy",
        ),
        (
            "MER4221_5_E_nonEH_abs",
            "E_nonEH_abs",
            "non-EH parent source leakage",
            "extra MTS source terms not absorbed into EH/Hilbert branch",
            "MISSING_PARENT_SIGNATURE_OR_BOUND",
            "energy",
        ),
        (
            "MER4221_6_E_frame_abs",
            "E_frame_abs",
            "same-frame/coframe mismatch",
            "tau/n/coframe/source-surface mismatch contribution",
            "MISSING_FRAME_LOCK_ZERO_OR_BOUND",
            "energy",
        ),
        (
            "MER4221_7_epsilon_E",
            "epsilon_E",
            "MEH sign ratio",
            "(E_neg_abs+E_open_abs+E_ref_abs+E_vir_abs+E_nonEH_abs+E_frame_abs)/E_plus",
            "COMPUTED_AFTER_INPUTS",
            "dimensionless",
        ),
        (
            "MER4221_8_M_EH_lower",
            "M_EH_lower",
            "positive comparator lower bound",
            "c^-2*E_plus*(1-epsilon_E)",
            "COMPUTED_AFTER_INPUTS",
            "mass",
        ),
    ]
    return [
        {
            **common(),
            "input_id": input_id,
            "quantity": quantity,
            "meaning": meaning,
            "formula_or_source": formula_or_source,
            "current_status": current_status,
            "units": units,
            "source_path": "MISSING_SOURCE_ROW" if current_status.startswith("MISSING") else "computed_from_input_rows",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for input_id, quantity, meaning, formula_or_source, current_status, units in data
    ]


def bound_candidate_rows() -> List[Dict[str, str]]:
    rows = [
        {
            **common(),
            "candidate_id": "MEB4221_0_MEH_sign_bound",
            "quantity": "M_EH_lower",
            "formula": "c^-2*E_plus*(1-epsilon_E)",
            "acceptance_condition": "E_plus>0 and epsilon_E<1 in the same tau/coframe/worldtube/source branch",
            "current_value": "MISSING_E_PLUS_AND_EPSILON_E_VALUES",
            "derived": "True",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "candidate_id": "MEB4221_1_composed_MHref_sign_bound",
            "quantity": "M_H_ref_lower",
            "formula": "c^-2*E_plus*(1-epsilon_E)*(1-epsilon_abs)",
            "acceptance_condition": "E_plus>0, epsilon_E<1, epsilon_abs<1, all residuals source-backed",
            "current_value": "MISSING_E_PLUS_EPSILON_E_AND_EPSILON_ABS_VALUES",
            "derived": "True",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "candidate_id": "MEB4221_2_DEC_shortcut",
            "quantity": "Z_positive_energy",
            "formula": "parent no-ghost/DEC/positive-Hamiltonian theorem => E_neg_abs=0 and E_plus=E_total>0",
            "acceptance_condition": "field-by-field parent kinetic/Hessian/constraint signatures signed",
            "current_value": "MISSING_PARENT_SIGNATURE_MATRIX",
            "derived": "False",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "M_EH_lower_bound_law_derived": "True",
            "positive_comparator_claim": "False",
            "E_plus_available": "False",
            "epsilon_E_computable": "False",
            "M_EH_positive_available": "False",
            "composed_MHref_bound_available": "False",
            "local_GR_claim": "False",
            "remaining_gap": "parent_energy_signature_matrix_or_negative_energy_bound_values",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        ("MEF4221_0_no_orbital_GM", "infer E_plus or M_EH from orbital GM", "blocked", "orbital data remains a later test, not source evidence"),
        ("MEF4221_1_no_rest_mass_only", "use bare rest mass without field/binding/stress audit", "blocked", "total source energy includes EM, binding, stabilizer, pressure and tails"),
        ("MEF4221_2_no_pressure_delete", "delete Tolman/Komar pressure term", "blocked", "requires closed stationary total-source virial identity or residual row"),
        ("MEF4221_3_no_Poynting_double_count", "treat Poynting as an extra force and as Hilbert EM energy", "blocked", "Poynting is owned EM flux or boundary residual, not both"),
        ("MEF4221_4_no_positive_placeholder", "declare M_EH>0 without E_plus/epsilon_E evidence", "blocked", "requires positive-energy theorem or source-backed lower bound"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move, status, reason in data
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "MES4221_STATUS",
            "decision": DECISION,
            "summary": "M_EH positivity is reduced to a concrete positive-energy lower-bound law with named residual input rows; source values/signature matrix are still missing.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "4221 derives the MEH lower-bound law but cannot score it until E_plus and the negative/open/reference/stress residuals are signed or bounded.",
            "derive_first": "field-by-field parent kinetic/Hessian/constraint-stability signature matrix for total Hilbert source sectors",
            "fill_second": "E_plus, E_neg_abs, E_open_abs, E_ref_abs, E_vir_abs, E_nonEH_abs and E_frame_abs source rows",
            "fallback": "if signatures cannot be proven, fill conservative bounds and keep denominator/local-GR unavailable",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 237 - PPC4161 M_EH Positive Source Comparator And Residual Input Fill

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Purpose

4220 reduced stable denominator positivity to:

```text
M_H_ref >= M_EH(1-epsilon_abs).
```

So 4221 attacks the first live factor directly: the sign of `M_EH`.

## Same-frame comparator

The comparator is not orbital `GM`, not a fitted mass, and not a rest-mass shortcut:

```text
M_EH[tau,W_source] := c^-2 E_total[tau,W_source].
```

`E_total` is the total Hilbert-source energy in the same `tau`, coframe, worldtube and source-surface branch as `M_H_ref`.

## Lower-bound derivation

Split the total source energy into a strictly positive part and every sign-damaging channel:

```text
E_total
= E_plus
- E_neg_abs
- E_open_abs
- E_ref_abs
- E_vir_abs
- E_nonEH_abs
- E_frame_abs.
```

Define:

```text
epsilon_E :=
(E_neg_abs + E_open_abs + E_ref_abs + E_vir_abs + E_nonEH_abs + E_frame_abs)/E_plus.
```

Then:

```text
M_EH >= c^-2 E_plus(1-epsilon_E).
```

Therefore:

```text
E_plus > 0 and epsilon_E < 1
=> M_EH > 0.
```

This is the usable comparator law. It does not claim the values exist yet.

## Pressure and Poynting guards

The Komar/Tolman pressure term is not deleted. It must either vanish by a closed stationary total-source virial theorem or enter `E_vir_abs`.

The Poynting vector is also not a secret extra force. Closed/stationary Maxwell-Hodge energy contributes to `E_plus`; open radiative flux contributes to `E_open_abs`.

## Composed denominator law

Combining 4220 and 4221 gives:

```text
M_H_ref >= c^-2 E_plus(1-epsilon_E)(1-epsilon_abs).
```

That is a real way forward: prove/sign the source energy sector or fill conservative residual bounds.

## Current status

The lower-bound law is derived, but the input rows are still not claim-grade:

- `E_plus` lacks a same-frame positive source/support row;
- `E_neg_abs` lacks a parent no-ghost or bounded-below signature matrix;
- `E_open_abs` needs closed-domain zero or flux bound;
- `E_ref_abs` needs fixed reference silence or bound;
- `E_vir_abs` needs virial zero or pressure/stress bound;
- `E_nonEH_abs` needs parent-sector signature/bound;
- `E_frame_abs` needs same-frame lock zero or bound.

## Next target

`{NEXT_TARGET}` should either prove the parent energy-signature matrix or fill the first conservative negative-energy/open-flux bound rows.
"""


def checkpoint_doc() -> str:
    return f"""# 4221 - M_EH Positive Source Comparator And Residual Input Fill

**Status:** `{DECISION}`.

## What moved

This checkpoint turns the vague `M_EH>0` demand into a scoreable lower-bound law:

```text
M_EH >= c^-2 E_plus(1-epsilon_E).
```

with:

```text
epsilon_E=(E_neg_abs+E_open_abs+E_ref_abs+E_vir_abs+E_nonEH_abs+E_frame_abs)/E_plus.
```

Thus:

```text
E_plus>0 and epsilon_E<1 => M_EH>0.
```

## Why this is a forward move

The old route only said "need positive energy." The new route states exactly which source rows must be filled and how they are combined. It also prevents three common cheats:

- orbital `GM` cannot define the source mass;
- Tolman/Komar pressure cannot be ignored;
- Poynting flux cannot be both hidden force and Hilbert EM energy.

## Generated rows

- `P8_Y5_R2FR_4221_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4221_MEH_COMPARATOR_LAW.csv`
- `P8_Y5_R2FR_4221_SECTOR_SIGNATURE_MATRIX.csv`
- `P8_Y5_R2FR_4221_RESIDUAL_INPUT_SCHEMA.csv`
- `P8_Y5_R2FR_4221_BOUND_CANDIDATE.csv`
- `P8_Y5_R2FR_4221_DECISION.csv`
- `P8_Y5_R2FR_4221_CLAIM_FIREWALL.csv`
- `P8_Y5_R2FR_4221_STATUS.csv`
- `P8_Y5_R2FR_4221_NEXT_TARGET.csv`

## Decision

No local-GR/Newton denominator claim is made. The law is derived, but the values/signature rows are not filled.

Next: `{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The M_EH positive source comparator is reduced to a strict lower-bound law: M_EH >= c^-2 E_plus(1-epsilon_E), hence M_EH>0 if E_plus>0 and epsilon_E<1; the route names negative/open/reference/virial/non-EH/frame residuals instead of using orbital GM or a bare rest-mass shortcut.",'
        f'"4221 source audit, comparator law, sector signature matrix, residual input schema, bound candidate, decision row and firewall.",'
        f'private_MEH_positive_comparator_lower_bound_nonclaim,'
        f'"Prove the parent energy-sector signature matrix or fill conservative E_plus/epsilon_E source rows.",'
        f'"This is a sign-gate reduction, not a local-GR denominator pass; no M_EH, M_H_ref, Newton or PPN claim follows until inputs are source-backed and epsilon_E<1."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 96. M_EH Positive Source Comparator Gate

Marker: `{MARKER}`

4221 reduces the live denominator sign problem to:

```text
M_EH >= c^-2 E_plus(1-epsilon_E).
```

and therefore:

```text
E_plus>0 and epsilon_E<1 => M_EH>0.
```

This is stronger than a missing-row note: the remaining work is now an explicit parent energy-signature or conservative residual-bound problem. No local-GR/Newton claim is made.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - M_EH Positive Comparator Gate

Marker: `{PACKET_MARKER}`

The denominator branch now has:

```text
M_H_ref >= c^-2 E_plus(1-epsilon_E)(1-epsilon_abs).
```

The packet remains private/nonclaim until `E_plus>0`, `epsilon_E<1`, and `epsilon_abs<1` are all source-backed in the same tau/coframe/worldtube branch.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4221_SOURCE_REGISTER.csv"]
    laws = rows_by_file["P8_Y5_R2FR_4221_MEH_COMPARATOR_LAW.csv"]
    sectors = rows_by_file["P8_Y5_R2FR_4221_SECTOR_SIGNATURE_MATRIX.csv"]
    residuals = rows_by_file["P8_Y5_R2FR_4221_RESIDUAL_INPUT_SCHEMA.csv"]
    bounds = rows_by_file["P8_Y5_R2FR_4221_BOUND_CANDIDATE.csv"]
    decisions = rows_by_file["P8_Y5_R2FR_4221_DECISION.csv"]
    firewalls = rows_by_file["P8_Y5_R2FR_4221_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4221_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]
    decision = decisions[0]

    checks = [
        ("VAL4221_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4221_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4221_2_lower_bound_law",
            "law rows include lower-bound and strict positivity gate",
            {"MEL4221_2_lower_bound", "MEL4221_3_strict_positive_gate", "MEL4221_6_denominator_import"}.issubset({row["law_id"] for row in laws}),
        ),
        (
            "VAL4221_3_sector_matrix",
            "sector matrix names visible, EM, binding, MTS core, boundary and virial sectors",
            {"MES4221_0_visible_matter_rest", "MES4221_1_Maxwell_Hodge", "MES4221_2_binding_stabilizer", "MES4221_3_motion_time_space_core", "MES4221_4_topological_boundary", "MES4221_5_pressure_virial"}.issubset({row["sector_id"] for row in sectors}),
        ),
        (
            "VAL4221_4_residual_inputs",
            "residual schema covers E_plus, epsilon_E and M_EH_lower",
            {"E_plus", "E_neg_abs", "E_open_abs", "E_ref_abs", "E_vir_abs", "E_nonEH_abs", "E_frame_abs", "epsilon_E", "M_EH_lower"}.issubset({row["quantity"] for row in residuals}),
        ),
        (
            "VAL4221_5_bound_candidates",
            "bound candidates include MEH and composed MHref route",
            {"MEB4221_0_MEH_sign_bound", "MEB4221_1_composed_MHref_sign_bound", "MEB4221_2_DEC_shortcut"}.issubset({row["candidate_id"] for row in bounds}),
        ),
        (
            "VAL4221_6_decision_nonclaim",
            "decision keeps MEH/MHref/local-GR unavailable",
            decision["M_EH_positive_available"] == "False" and decision["local_GR_claim"] == "False" and decision["composed_MHref_bound_available"] == "False",
        ),
        (
            "VAL4221_7_firewall",
            "firewall blocks orbital GM, pressure deletion, Poynting double count and positive placeholders",
            {"MEF4221_0_no_orbital_GM", "MEF4221_2_no_pressure_delete", "MEF4221_3_no_Poynting_double_count", "MEF4221_4_no_positive_placeholder"}.issubset({row["firewall_id"] for row in firewalls}),
        ),
        (
            "VAL4221_8_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4221_9_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4221_10_claim_register", "claim register contains L-062", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4221_11_spine_packet", "spine and packet contain 4221 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4221_12_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4221_13_script_exists", "generator script exists", (SCRIPTS / "Y5_R2FR_4221_MEH_positive_source_comparator_and_residual_input_fill.py").exists()),
        (
            "VAL4221_14_status",
            "status records nonclaim lower-bound reduction",
            rows_by_file["P8_Y5_R2FR_4221_STATUS.csv"][0]["decision"] == DECISION,
        ),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
        }
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4221_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4221_MEH_COMPARATOR_LAW.csv": law_rows(),
        "P8_Y5_R2FR_4221_SECTOR_SIGNATURE_MATRIX.csv": sector_signature_rows(),
        "P8_Y5_R2FR_4221_RESIDUAL_INPUT_SCHEMA.csv": residual_input_rows(),
        "P8_Y5_R2FR_4221_BOUND_CANDIDATE.csv": bound_candidate_rows(),
        "P8_Y5_R2FR_4221_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4221_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4221_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4221_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)

    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8")
    update_registers()
    validation_rows = validate(rows_by_file)
    write_csv(VALIDATION_PATH, validation_rows)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={VALIDATION_PATH}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
