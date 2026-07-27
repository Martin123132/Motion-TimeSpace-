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

CHECKPOINT = "4244"
CLAIM_ID = "L-085"
BRANCH = "MTS_R2FR_Y5_DQ_COMPONENT_ADOPTION_MATRIX_4244"
DECISION = "DQ_COMPONENT_THEOREMS_PRESENT_HL_ARGUMENT_ADOPTION_UNSIGNED_HPERP_BOUND_INPUT_FILL_SELECTED_NONCLAIM"
MARKER = "PPC4161_DQ_COMPONENT_ADOPTION_MATRIX_4244"
PACKET_MARKER = "PPC4161_PACKET_DQ_COMPONENT_ADOPTION_MATRIX_4244"
NEXT_TARGET = "4245-Y5-R2FR-HL-argument-qbasic-adoption-or-Dq-bound-first-input-row.md"

FORMAL_PATH = FORMAL / "260-PPC4161-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md"
DOC_PATH = POST / "4244-Y5-R2FR-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4244_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4244_00_4243_next": SourceSpec(
        "SRC4244_00_4243_next",
        POST / "4243-Y5-R2FR-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md",
        "4244-Y5-R2FR-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md",
        "4243 selected the Dq-component adoption target.",
    ),
    "SRC4244_01_4243_formal": SourceSpec(
        "SRC4244_01_4243_formal",
        FORMAL / "259-PPC4161-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md",
        "Hperp := (1 - Pi_kerDq) H_L",
        "4243 definition reducing Hperp to quotient-defect components.",
    ),
    "SRC4244_02_4243_component_matrix": SourceSpec(
        "SRC4244_02_4243_component_matrix",
        SOURCE_DIR / "P8_Y5_R2FR_4243_DQ_COMPONENT_BOUND_MATRIX.csv",
        "Dq_geom[H_L]",
        "4243 machine-readable component matrix.",
    ),
    "SRC4244_03_Dq_component_theorem": SourceSpec(
        "SRC4244_03_Dq_component_theorem",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_geom[v]=0,",
        "Componentwise Dq zero theorem for an admitted q-natural argument.",
    ),
    "SRC4244_04_Dq_bound": SourceSpec(
        "SRC4244_04_Dq_bound",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "|E_Dq_total|",
        "Fallback Dq absolute bound route.",
    ),
    "SRC4244_05_qnatural": SourceSpec(
        "SRC4244_05_qnatural",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "V_q := ker(Dq),",
        "Quotient vertical kernel theorem.",
    ),
    "SRC4244_06_qnatural_matter": SourceSpec(
        "SRC4244_06_qnatural_matter",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "S_matter = Sbar_m[psi, g_obs(q), A(q), theta(q)].",
        "Matter/readout descent theorem.",
    ),
    "SRC4244_07_qbasic_presymplectic": SourceSpec(
        "SRC4244_07_qbasic_presymplectic",
        FORMAL / "229-PPC4161-qbasic-vertical-presymplectic-silence.md",
        "Dq[v] = 0.",
        "q-basic vertical presymplectic silence theorem.",
    ),
    "SRC4244_08_projector": SourceSpec(
        "SRC4244_08_projector",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "P_loc=P_bar(q)",
        "Projector/coframe descent support.",
    ),
    "SRC4244_09_visible_EM": SourceSpec(
        "SRC4244_09_visible_EM",
        FORMAL / "234-PPC4161-visible-EM-material-curl-zero-or-residual-bound.md",
        "Maxwell-Hodge uses the same observed metric/coframe/Hodge star;",
        "Visible EM/material import support.",
    ),
    "SRC4244_10_poynting_owner": SourceSpec(
        "SRC4244_10_poynting_owner",
        FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md",
        "Poynting flow = energy transport",
        "Poynting/Hodge source-owner support.",
    ),
    "SRC4244_11_coeff_lock": SourceSpec(
        "SRC4244_11_coeff_lock",
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "D_A ln kappa_eff = 0.",
        "Calibrated source-coupling marker support.",
    ),
    "SRC4244_12_reference_lock": SourceSpec(
        "SRC4244_12_reference_lock",
        FORMAL / "231-PPC4161-reference-lock-curl-zero-or-bound.md",
        "D_source H_ref = D_readout H_ref = 0",
        "Reference/readout lock support.",
    ),
    "SRC4244_13_boundary": SourceSpec(
        "SRC4244_13_boundary",
        FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md",
        "I_boundary + I_corner = 0.",
        "Boundary/corner no-flux selector support.",
    ),
    "SRC4244_14_htau": SourceSpec(
        "SRC4244_14_htau",
        FORMAL / "228-PPC4161-Htau-integrability-operator-and-curl-bound.md",
        "omega_Dq_marker.",
        "Dq marker appears in the H_tau integrability obstruction.",
    ),
}


COMPONENTS = [
    {
        "component": "Dq_geom[H_L]",
        "source_clause": "q-natural geometry/coframe components are silent for admitted q-basic vertical arguments.",
        "selector_source_ids": "SRC4244_03_Dq_component_theorem;SRC4244_05_qnatural;SRC4244_08_projector",
        "HL_argument_gate": "prove H_L preserves quotient geometry/coframe/readout geometry",
        "HL_argument_status": "MISSING_HL_AS_QBASIC_GEOM",
        "bound_symbol": "epsilon_geom",
        "residual_if_unsigned": "R_Dq_geom_HL",
    },
    {
        "component": "Dq_tau[H_L]",
        "source_clause": "fixed tau/reference terms are silent only when the time generator and reference are source/readout blind.",
        "selector_source_ids": "SRC4244_12_reference_lock;SRC4244_14_htau;SRC4244_03_Dq_component_theorem",
        "HL_argument_gate": "prove H_L preserves tau, H_ref and the local Hamiltonian collar",
        "HL_argument_status": "MISSING_HL_TAU_REFERENCE_ZERO",
        "bound_symbol": "epsilon_tau",
        "residual_if_unsigned": "R_Dq_tau_HL",
    },
    {
        "component": "Dq_matter[H_L]",
        "source_clause": "matter descent is silent for variations vertical to q and to calibrated matter/readout data.",
        "selector_source_ids": "SRC4244_06_qnatural_matter;SRC4244_07_qbasic_presymplectic;SRC4244_03_Dq_component_theorem",
        "HL_argument_gate": "prove H_L is vertical to matter pullback, masses, charges and source normalization",
        "HL_argument_status": "MISSING_HL_MATTER_DESCENT_ZERO",
        "bound_symbol": "epsilon_matter",
        "residual_if_unsigned": "R_Dq_matter_HL",
    },
    {
        "component": "Dq_source_readout[H_L]",
        "source_clause": "source/readout marker is silent for q-basic pullback sources and source-blind reference choices.",
        "selector_source_ids": "SRC4244_03_Dq_component_theorem;SRC4244_07_qbasic_presymplectic;SRC4244_12_reference_lock",
        "HL_argument_gate": "prove H_L does not move source readout, normalization or observer labels",
        "HL_argument_status": "MISSING_HL_SOURCE_READOUT_ZERO",
        "bound_symbol": "epsilon_source_readout",
        "residual_if_unsigned": "R_Dq_source_readout_HL",
    },
    {
        "component": "Dq_theta_marker[H_L]",
        "source_clause": "theta/material markers are silent when calibrated constants and material labels are q-basic.",
        "selector_source_ids": "SRC4244_05_qnatural;SRC4244_06_qnatural_matter;SRC4244_09_visible_EM",
        "HL_argument_gate": "prove H_L does not shift theta markers, material labels, alpha_EM or mass labels",
        "HL_argument_status": "MISSING_HL_THETA_MARKER_ZERO",
        "bound_symbol": "epsilon_theta_marker",
        "residual_if_unsigned": "R_Dq_theta_marker_HL",
    },
    {
        "component": "Dq_boundary_projector[H_L]",
        "source_clause": "boundary/projector terms are silent only inside the owned no-flux collar with fixed edge/corner data.",
        "selector_source_ids": "SRC4244_08_projector;SRC4244_13_boundary;SRC4244_03_Dq_component_theorem",
        "HL_argument_gate": "prove H_L preserves boundary projector, no-flux collar and corner/edge data",
        "HL_argument_status": "MISSING_HL_BOUNDARY_PROJECTOR_ZERO",
        "bound_symbol": "epsilon_boundary_projector",
        "residual_if_unsigned": "R_Dq_boundary_projector_HL",
    },
    {
        "component": "Dq_EM[H_L]",
        "source_clause": "standard visible EM is already Hilbert-source imported, but MTS EM/Hodge deformations remain explicit residuals.",
        "selector_source_ids": "SRC4244_09_visible_EM;SRC4244_10_poynting_owner;SRC4244_03_Dq_component_theorem",
        "HL_argument_gate": "prove H_L preserves Maxwell-Hodge import, constitutive relation and Poynting boundary routing",
        "HL_argument_status": "MISSING_HL_EM_HODGE_CONSTITUTIVE_ZERO",
        "bound_symbol": "epsilon_EM",
        "residual_if_unsigned": "R_Dq_EM_HL",
    },
    {
        "component": "Dq_coeff[H_L]",
        "source_clause": "calibrated coupling markers are silent only when kappa_eff and coefficient labels are parent locked.",
        "selector_source_ids": "SRC4244_11_coeff_lock;SRC4244_03_Dq_component_theorem;SRC4244_05_qnatural",
        "HL_argument_gate": "prove H_L does not move kappa_eff, Z0, coefficient labels or parent coupling markers",
        "HL_argument_status": "MISSING_HL_COEFFICIENT_MARKER_ZERO",
        "bound_symbol": "epsilon_coeff",
        "residual_if_unsigned": "R_Dq_coeff_HL",
    },
]


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
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


def csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + block.strip())


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "valid_for_claim": "False",
            }
        )
    return rows


def adoption_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for component in COMPONENTS:
        rows.append(
            {
                **common(),
                **component,
                "selector_component_status": "conditional_zero_clause_present",
                "HL_argument_required": "True",
                "zero_adoption_status": "blocked_by_HL_argument_unsigned",
                "bound_row_required": "True",
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "notes": "4244 adopts the component theorem only as a selector theorem; it does not insert H_L into the selector without proof.",
            }
        )
    return rows


def hl_argument_gate_rows() -> List[Dict[str, str]]:
    gates = [
        (
            "HL_FIELDSPACE_ADMISSIBILITY",
            "H_L must be an allowed parent field-space direction for every local branch variation.",
            "SRC4244_01_4243_formal",
            "MISSING_PARENT_ADMISSIBLE_HL_VARIATION_SIGNATURE",
            "would allow component tests to be evaluated on H_L rather than on a generic v",
        ),
        (
            "HL_TOTAL_QVERTICALITY",
            "H_L must lie in the kernel of the relevant quotient differential or be bounded away from it.",
            "SRC4244_05_qnatural;SRC4244_07_qbasic_presymplectic",
            "MISSING_Dq_HL_TOTAL_ZERO_OR_NORM_BOUND",
            "would close Hperp=0 if all component projections vanish",
        ),
        (
            "HL_GEOMETRY_COFAME_DESCENT",
            "H_L must preserve observed geometry/coframe/projector data in the local selector.",
            "SRC4244_08_projector",
            "MISSING_HL_GEOM_COFAME_DESCENT",
            "would adopt Dq_geom[H_L]=0",
        ),
        (
            "HL_SOURCE_MATTER_DESCENT",
            "H_L must preserve matter pullback, source readout, masses, charges and normalization.",
            "SRC4244_06_qnatural_matter",
            "MISSING_HL_SOURCE_MATTER_DESCENT",
            "would adopt Dq_matter and Dq_source_readout zeros",
        ),
        (
            "HL_BOUNDARY_COLLAR_SAFETY",
            "H_L must preserve no-flux local collar, boundary projector and corner/edge data.",
            "SRC4244_13_boundary",
            "MISSING_HL_BOUNDARY_COLLAR_CERTIFICATE",
            "would adopt Dq_boundary_projector[H_L]=0",
        ),
        (
            "HL_VISIBLE_EM_IMPORT_SAFETY",
            "H_L must preserve Maxwell-Hodge import, constitutive relation and Poynting boundary routing.",
            "SRC4244_09_visible_EM;SRC4244_10_poynting_owner",
            "MISSING_HL_EM_IMPORT_AND_HODGE_CERTIFICATE",
            "would adopt Dq_EM[H_L]=0",
        ),
        (
            "HL_COUPLING_MARKER_LOCK",
            "H_L must preserve kappa_eff, Z0 and parent coefficient/coupling marker labels.",
            "SRC4244_11_coeff_lock",
            "MISSING_HL_COUPLING_MARKER_LOCK",
            "would adopt Dq_coeff[H_L]=0",
        ),
        (
            "HL_BOUND_CONSTANT_OWNER",
            "C_S, C_perp, component weights and component norms must have source-owned values.",
            "SRC4244_02_4243_component_matrix;SRC4244_04_Dq_bound",
            "MISSING_CS_CPERP_WEIGHTS_EPSILON_SOURCES",
            "would turn the retained Hperp defect into a numeric local residual test",
        ),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "required_condition": required_condition,
            "source_support": source_support,
            "missing_piece": missing_piece,
            "current_status": "open_nonclaim",
            "effect_if_closed": effect_if_closed,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, required_condition, source_support, missing_piece, effect_if_closed in gates
    ]


def bound_input_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = [
        {
            **common(),
            "quantity": "C_S",
            "definition": "operator norm converting ||Hperp|| into |S_A Hperp^A|",
            "formula_role": "|S_A Hperp^A| <= C_S ||Hperp||",
            "units": "source_norm_per_Hnorm",
            "numeric_value": "MISSING",
            "source_status": "MISSING_SOURCE_OPERATOR_NORM",
            "source_path": "",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "quantity": "C_perp",
            "definition": "right-inverse/projection norm bounding Hperp by component Dq defect norm",
            "formula_role": "||Hperp|| <= C_perp E_Dq,H",
            "units": "Hnorm_per_Dqnorm",
            "numeric_value": "MISSING",
            "source_status": "MISSING_PROJECTION_NORM",
            "source_path": "",
            "valid_for_claim": "False",
        },
    ]
    for component in COMPONENTS:
        symbol = component["bound_symbol"]
        rows.append(
            {
                **common(),
                "quantity": symbol,
                "definition": f"norm bound for {component['component']}",
                "formula_role": f"||{component['component']}|| <= {symbol}",
                "units": "component_Dq_norm",
                "numeric_value": "MISSING",
                "source_status": component["HL_argument_status"],
                "source_path": "",
                "valid_for_claim": "False",
            }
        )
        rows.append(
            {
                **common(),
                "quantity": "w_" + symbol.replace("epsilon_", ""),
                "definition": f"positive weight for {component['component']} in E_Dq,H",
                "formula_role": "E_Dq,H^2 = sum_i w_i epsilon_i^2",
                "units": "dimension-balancing_weight",
                "numeric_value": "MISSING",
                "source_status": "MISSING_COMPONENT_WEIGHT",
                "source_path": "",
                "valid_for_claim": "False",
            }
        )
    return rows


def residual_budget_rows() -> List[Dict[str, str]]:
    eps_terms = " + ".join(f"w_{c['bound_symbol'].replace('epsilon_', '')} {c['bound_symbol']}^2" for c in COMPONENTS)
    return [
        {
            **common(),
            "budget_id": "HPERP_COMPONENT_BOUND",
            "formula": f"|S_A Hperp^A| <= C_S C_perp sqrt({eps_terms})",
            "current_status": "symbolic_bound_only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "budget_id": "STRONG_LOCAL_GATE",
            "formula": "C_S C_perp E_Dq,H <= 0.1678939074330212*(mu_Xi T_res)/|c_Gamma|",
            "current_status": "requires numeric C_S, C_perp, E_Dq,H, mu_Xi, T_res and c_Gamma",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "budget_id": "ZERO_ROUTE",
            "formula": "all_i Dq_i[H_L]=0 => E_Dq,H=0 => Hperp=0 => S_A Hperp^A=0",
            "current_status": "not adopted because H_L-specific component zeros are unsigned",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4244",
            "decision": DECISION,
            "scoreable_now": "False",
            "zero_claim_allowed": "False",
            "reason": "The componentwise Dq zero theorem exists for admitted q-basic selector arguments, but H_L has not been proved to satisfy those argument gates.",
            "selected_route": "Attempt H_L q-basic adoption first; if any component fails, source epsilon_i, C_S and C_perp as a real Hperp residual bound.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    gates = [
        ("FW4244_0_no_local_GR_claim", "No local-GR reduction claim from component theorem alone."),
        ("FW4244_1_no_HL_smuggling", "Do not replace a generic q-basic v by H_L without an H_L argument certificate."),
        ("FW4244_2_no_geometry_only_shortcut", "Geometry/coframe silence does not imply matter, EM, source-readout or coefficient silence."),
        ("FW4244_3_no_numeric_bound_without_sources", "A symbolic epsilon_i ledger is not a numeric PPN/R10/local residual pass."),
        ("FW4244_4_no_public_claim", "Private checkpoint only; no GitHub/public claim action."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in gates
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4244 upgrades the Dq route from a missing list into an adoption matrix: component selector theorems exist, H_L-specific adoption is unsigned, and every open component has an explicit epsilon_i bound row.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "task": "Try to prove H_L is q-basic/admitted for each Dq component; otherwise fill the first real epsilon_i/C_S/C_perp bound row.",
            "reason": "This is the least smuggly route: derive the zero if possible, or keep the local branch honest with a sourced residual.",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> List[List[Dict[str, str]]]:
    return [
        source_rows(),
        adoption_rows(),
        hl_argument_gate_rows(),
        bound_input_rows(),
        residual_budget_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    ]


def formal_doc() -> str:
    return f"""
# 260 - PPC4161 Dq component zero adoption or Hperp bound input fill

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4244 does **not** claim `Hperp=0`, local GR, PPN safety, R10 safety, or any public result.

## Problem

4243 proved the useful reduction

```text
Hperp := (1 - Pi_kerDq) H_L,
E_Dq,H^2 := sum_i w_i ||Dq_i[H_L]||^2,
|S_A Hperp^A| <= C_S C_perp E_Dq,H.
```

So the clean zero route is:

```text
all_i Dq_i[H_L]=0
=> E_Dq,H=0
=> Hperp=0
=> S_A Hperp^A=0.
```

The danger is smuggling. Existing files prove many component zeros for an admitted q-basic/selector-safe argument `v`; they do not automatically prove that the actual local leakage direction `H_L` is such an argument.

## Adoption Rule

For each component,

```text
selector theorem for v + H_L argument certificate
=> Dq_i[H_L]=0.
```

Without the second premise the component remains an explicit residual:

```text
||Dq_i[H_L]|| <= epsilon_i.
```

## Component Verdict

The selector theorems are present conditionally, but every `H_L` argument certificate is still unsigned:

```text
Dq_geom[H_L]              -> MISSING_HL_AS_QBASIC_GEOM
Dq_tau[H_L]               -> MISSING_HL_TAU_REFERENCE_ZERO
Dq_matter[H_L]            -> MISSING_HL_MATTER_DESCENT_ZERO
Dq_source_readout[H_L]    -> MISSING_HL_SOURCE_READOUT_ZERO
Dq_theta_marker[H_L]      -> MISSING_HL_THETA_MARKER_ZERO
Dq_boundary_projector[H_L]-> MISSING_HL_BOUNDARY_PROJECTOR_ZERO
Dq_EM[H_L]                -> MISSING_HL_EM_HODGE_CONSTITUTIVE_ZERO
Dq_coeff[H_L]             -> MISSING_HL_COEFFICIENT_MARKER_ZERO
```

Therefore 4244 selects the honest route:

```text
|S_A Hperp^A|
<= C_S C_perp sqrt(sum_i w_i epsilon_i^2).
```

This is progress because the missing piece is no longer "the coupling" or "Hperp" in fog form. It is a finite list of H_L argument certificates or source-backed component bounds.

## Next Target

`{NEXT_TARGET}` should try to prove the `H_L` argument certificates first. If that fails for any component, it should fill the first real component-bound row rather than declaring the branch dead or closing it by assertion.
"""


def checkpoint_doc() -> str:
    return f"""
# 4244 - Dq component zero adoption or Hperp bound input fill

**Status:** `{DECISION}`.

## What changed

4244 separates two things that were easy to blur:

1. the componentwise theorem says `Dq_i[v]=0` for admitted q-basic/selector-safe `v`;
2. the local branch needs `Dq_i[H_L]=0` for the actual leakage direction.

The first exists conditionally. The second is not yet signed.

## Result

No local-GR claim is made. Instead, the branch now has an explicit finite residual ledger:

```text
|S_A Hperp^A|
<= C_S C_perp sqrt(sum_i w_i epsilon_i^2),
epsilon_i >= ||Dq_i[H_L]||.
```

## Files written

- `{FORMAL_PATH}`
- `P8_Y5_R2FR_4244_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4244_DQ_COMPONENT_ADOPTION_MATRIX.csv`
- `P8_Y5_R2FR_4244_HL_ARGUMENT_GATES.csv`
- `P8_Y5_R2FR_4244_HPERP_BOUND_INPUT_FILL.csv`
- `P8_Y5_R2FR_4244_RESIDUAL_BUDGET.csv`
- `P8_Y5_R2FR_4244_DECISION.csv`
- `P8_Y5_R2FR_4244_CLAIM_FIREWALL.csv`
- `P8_Y5_R2FR_4244_STATUS.csv`
- `P8_Y5_R2FR_4244_NEXT_TARGET.csv`

## Next target

`{NEXT_TARGET}`
"""


def update_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    if CLAIM_ID in read_text(path):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "4244 separates conditional Dq component selector theorems from H_L-specific adoption. All eight Dq_i[H_L] components remain nonclaim until H_L argument certificates or source-backed epsilon_i bounds are supplied.",
        "current_evidence": "4244 source register, Dq component adoption matrix, H_L argument gates, Hperp bound input fill, residual budget, decision and firewall.",
        "status": "private_Dq_component_adoption_matrix_nonclaim",
        "next_test": "Prove H_L is admitted/q-basic for each Dq component, or source the first real epsilon_i, C_S and C_perp rows.",
        "key_risk": "Using q-basic component theorems for a generic v as if they already applied to H_L would smuggle the Hperp zero.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 Dq Component Adoption Matrix

Marker: `{MARKER}`

4244 turns the Hperp/Dq route into an explicit adoption gate:

```text
Dq_i[v]=0 for admitted q-basic v
+ H_L admitted for component i
=> Dq_i[H_L]=0.
```

Since the `H_L` argument certificates are not yet parent-signed, the retained local source row is:

```text
|S_A Hperp^A| <= C_S C_perp sqrt(sum_i w_i epsilon_i^2).
```

This keeps the route derivation-first while preventing a hidden plateau/closure axiom.
"""
    packet_block = f"""
## Packet Update - Dq Component Adoption Matrix

Marker: `{PACKET_MARKER}`

The local cGamma/Hperp branch now has a finite Dq adoption matrix. Component theorems exist conditionally, but H_L-specific adoption remains unsigned, so every component is carried as an explicit nonclaim epsilon row.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    adoption = adoption_rows()
    gates = hl_argument_gate_rows()
    bounds = bound_input_rows()
    budget = residual_budget_rows()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4244_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4244_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4244_2_eight_components", "eight Dq components are audited", len(adoption) == 8, "adoption matrix")
    add("VAL4244_3_selector_present", "all components have conditional selector clauses", all(row["selector_component_status"] == "conditional_zero_clause_present" for row in adoption), "adoption matrix")
    add("VAL4244_4_HL_unsigned", "all H_L argument gates remain missing/open", all(row["HL_argument_status"].startswith("MISSING_") for row in adoption), "adoption matrix")
    add("VAL4244_5_no_adopted_zero", "no Dq_i[H_L] zero is adopted", all(row["zero_adoption_status"] == "blocked_by_HL_argument_unsigned" for row in adoption), "adoption matrix")
    add("VAL4244_6_gate_rows", "H_L argument gates include coupling, EM, boundary and norm owners", {"HL_COUPLING_MARKER_LOCK", "HL_VISIBLE_EM_IMPORT_SAFETY", "HL_BOUNDARY_COLLAR_SAFETY", "HL_BOUND_CONSTANT_OWNER"}.issubset({row["gate_id"] for row in gates}), "H_L gates")
    add("VAL4244_7_bound_inputs", "bound inputs include C_S, C_perp and eight epsilons", {"C_S", "C_perp"}.issubset({row["quantity"] for row in bounds}) and sum(row["quantity"].startswith("epsilon_") for row in bounds) == 8, "bound input fill")
    add("VAL4244_8_budget_formula", "residual budget contains C_S C_perp sqrt formula", any("C_S C_perp sqrt" in row["formula"] for row in budget), "residual budget")
    add("VAL4244_9_decision_nonclaim", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4244_10_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4244_11_claim_register", "claims register contains L-085", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4244_12_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4244_13_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4244_14_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4244_15_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4244_SOURCE_REGISTER.csv",
        "adoption": SOURCE_DIR / "P8_Y5_R2FR_4244_DQ_COMPONENT_ADOPTION_MATRIX.csv",
        "gates": SOURCE_DIR / "P8_Y5_R2FR_4244_HL_ARGUMENT_GATES.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4244_HPERP_BOUND_INPUT_FILL.csv",
        "budget": SOURCE_DIR / "P8_Y5_R2FR_4244_RESIDUAL_BUDGET.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4244_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4244_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4244_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4244_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["adoption"], adoption_rows())
    write_csv(paths["gates"], hl_argument_gate_rows())
    write_csv(paths["bounds"], bound_input_rows())
    write_csv(paths["budget"], residual_budget_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next"], next_target_rows())
    update_claim_register()
    update_spine_and_packet()
    write_csv(VALIDATION_PATH, validation_rows())
    failed_rows = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"Decision: {DECISION}")
    print(f"Formal: {FORMAL_PATH}")
    print(f"Checkpoint: {DOC_PATH}")
    print(f"Validation: {VALIDATION_PATH}")
    print(f"Validation rows: {len(csv_rows(VALIDATION_PATH))}; failed: {len(failed_rows)}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAILED {failed_row['check_id']}: {failed_row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
