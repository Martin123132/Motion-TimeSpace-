from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()

CHECKPOINT = "4218"
CLAIM_ID = "L-059"
BRANCH_ID = "MTS_R2FR_Y5_VISIBLE_EM_MATERIAL_CURL_ZERO_4218"
DECISION = (
    "VISIBLE_EM_MATERIAL_CURL_ZERO_CONDITIONALLY_DERIVED_FOR_STANDARD_VISIBLE_"
    "IMPORT_MTS_VISIBLE_DEFORMATION_RESIDUAL_BOUND_ROW_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "234-PPC4161-visible-EM-material-curl-zero-or-residual-bound.md"
DOC_PATH = POST / "4218-Y5-R2FR-visible-EM-material-curl-zero-or-residual-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_VISIBLE_EM_MATERIAL_CURL_ZERO_4218"
PACKET_MARKER = "PPC4161_PACKET_VISIBLE_EM_MATERIAL_CURL_ZERO_4218"
NEXT_TARGET = "4219-Y5-R2FR-Dq-source-readout-coupling-marker-zero-or-bound-row.md"

SOURCES = {
    "SRC4218_00_4217_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4217_NEXT_TARGET.csv",
        "4218-Y5-R2FR-visible-EM-material-curl-zero-or-residual-bound-row.md",
        "4217 selected visible EM/material/current residual as next retained obstruction.",
    ),
    "SRC4218_01_4212_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4212_CURL_COMPONENTS.csv",
        "I_matter_EM",
        "4212 retained the visible EM/material/current residual component.",
    ),
    "SRC4218_02_4210_import": (
        SOURCE_DIR / "P8_Y5_R2FR_4210_VISIBLE_MATTER_IMPORT_CONTRACT.csv",
        "VMI4210_1_action",
        "Standard visible matter import contract and one Hilbert source.",
    ),
    "SRC4218_03_4210_envelope": (
        SOURCE_DIR / "P8_Y5_R2FR_4210_ALPHA_RESIDUAL_ENVELOPE.csv",
        "ARE4210_0_wEM",
        "Visible-sector residual envelope rows to use if the zero selector fails.",
    ),
    "SRC4218_04_4207_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv",
        "PO4207_3_internal_exchange",
        "Maxwell-Hodge/Poynting owner and Lorentz exchange identity.",
    ),
    "SRC4218_05_4208_hodge": (
        SOURCE_DIR / "P8_Y5_R2FR_4208_HODGE_ZERO_CONTRACT.csv",
        "HZ4208_2_visible_EM_action_domain",
        "Visible EM action-domain/Hodge uniqueness gate.",
    ),
    "SRC4218_06_4209_normalization": (
        SOURCE_DIR / "P8_Y5_R2FR_4209_NORMALIZATION_IDENTITIES.csv",
        "NI4209_4_vertical_residual",
        "Charge-current normalization residual law.",
    ),
    "SRC4218_07_4083_charge": (
        SOURCE_DIR / "P8_Y5_R2FR_4083_CHARGE_CURRENT_NORMALIZATION_THEOREM.csv",
        "STANDARD_VISIBLE_EM_IMPORT_CONTRACT_READY_NONCLAIM",
        "Standard visible EM import and calibrated constants route.",
    ),
    "SRC4218_08_3620_total_current": (
        SOURCE_DIR / "P8_Y5_R2FR_3620_EM_TOTAL_SOURCE_CURRENT_CLOSURE.csv",
        "SCC3620_0_total_stress_identity",
        "Matter plus EM total Hilbert current closure identity.",
    ),
    "SRC4218_09_226_formal": (
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "epsilon_visible_EM_total",
        "Formal visible matter import and residual-envelope statement.",
    ),
    "SRC4218_10_233_formal": (
        FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md",
        "I_matter_EM",
        "4217 reduced curl status pointing to this obstruction.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("\n\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "VEM4218_0_target",
            "target residual",
            "I_matter_EM := int_S i_tau omega_visible_EM_residual",
            "definition_from_4212",
            "this is not total EM stress; it is only the extra visible-sector leakage left after the EH+visible subcharge",
        ),
        (
            "VEM4218_1_action_split",
            "standard-plus-residual split",
            "S_visible_parent = S_vis_standard[g_obs,A,psi,theta_obs] + DeltaS_MTS_visible",
            "selector_decomposition",
            "the safe branch sets the residual action to zero before variation, not after fitting",
        ),
        (
            "VEM4218_2_standard_hilbert_source",
            "standard visible Hilbert source",
            "T_H = -2/sqrt(-g_obs) delta S_vis_standard/delta g_obs",
            "imported_baseline_identity",
            "ordinary matter, EM, binding and improvements enter the same source once",
        ),
        (
            "VEM4218_3_maxwell_hodge_owner",
            "Maxwell-Hodge/Poynting owner",
            "S_MH[A,g_obs] -> T_EM^{mu nu}; S_i=-T_EM(n,e_i)=(E x B)_i",
            "conditional_owner_theorem",
            "Poynting is physical EM flux but not a second source after T_EM is included",
        ),
        (
            "VEM4218_4_internal_exchange",
            "matter-EM exchange cancellation",
            "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda",
            "ward_exchange_identity",
            "Lorentz force is internal exchange, so total visible Hilbert current is conserved in the baseline branch",
        ),
        (
            "VEM4218_5_charge_current_normalization",
            "calibrated charge/current route",
            "alpha_eff proportional to g_J^2/lambda_A; b_alpha=2D ln g_J-D ln lambda_A",
            "residual_law_and_baseline_calibration",
            "absolute alpha is not derived; calibrated visible EM is allowed for local-GR reduction",
        ),
        (
            "VEM4218_6_residual_symplectic_form",
            "visible residual symplectic form",
            "omega_visible_EM_residual = delta_1 theta_DeltaS(delta_2)-delta_2 theta_DeltaS(delta_1)-theta_DeltaS([delta_1,delta_2])",
            "derived_from_action_split",
            "if DeltaS_MTS_visible and readout variations vanish, the residual symplectic term vanishes",
        ),
        (
            "VEM4218_7_curl_zero",
            "conditional visible EM curl zero",
            "DeltaS_MTS_visible=0, D_X theta_obs=0, no chi_EM/C_XF2/C_JQ/b_alpha/dlambda/material/radiative side channel => I_matter_EM=0",
            "conditional_zero_theorem",
            "the zero is a local selector theorem, not a global derivation of Maxwell/QED from MTS",
        ),
        (
            "VEM4218_8_residual_bound",
            "fallback visible EM/material bound",
            "|I_matter_EM|/M_H_ref <= epsilon_visible_EM_total/M_H_ref",
            "bound_row_retained",
            "unknown visible-sector terms are scored by absolute no-cancellation components",
        ),
        (
            "VEM4218_9_nonclaim_guard",
            "claim firewall",
            "MTS_alpha_prediction=false; global_Maxwell_derivation=false; local_GR_claim=false",
            "nonclaim_guard",
            "the branch can use calibrated visible matter without pretending to predict matter constants",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "status": status,
            "effect": effect,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, statement, status, effect in rows
    ]


def activation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "VEA4218_0_visible_import",
            "standard visible matter import active",
            "S_vis_standard is the calibrated observed matter/Maxwell/binding action of 4210",
            "required",
        ),
        (
            "VEA4218_1_same_hodge",
            "same observed metric/coframe/Hodge",
            "EM uses F wedge *_obs F with no independent chi_EM/background medium",
            "required",
        ),
        (
            "VEA4218_2_current_normalization",
            "fixed calibrated current and alpha route",
            "theta_obs constants are q-basic/readout constants; alpha is calibrated, not predicted",
            "required",
        ),
        (
            "VEA4218_3_internal_exchange",
            "matter and EM exchanged force cancels in total T_H",
            "Lorentz exchange is internal to the visible Hilbert source",
            "required",
        ),
        (
            "VEA4218_4_no_extra_operator",
            "no MTS-specific visible deformation",
            "w_EM, C_XF2, C_JQ, b_alpha, dlnlambda and material marker rows are zero in the selector",
            "required",
        ),
        (
            "VEA4218_5_radiation_routed",
            "radiative Poynting is routed, not hidden",
            "nonzero Phi_EM_rad is a boundary/Hamiltonian row, not I_matter_EM theorem-zero",
            "required",
        ),
        (
            "VEA4218_6_MHref_denominator",
            "same positive source denominator still required",
            "zero theorem does not prove M_H_ref positivity/stability",
            "retained_for_later",
        ),
    ]
    return [
        {
            **common(),
            "activation_id": activation_id,
            "clause": clause,
            "formal_role": role,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for activation_id, clause, role, status in rows
    ]


def residual_component_rows() -> List[Dict[str, str]]:
    rows = [
        ("R_w_EM", "delta_w_EM", "independent Maxwell stress/source multiplier", "abs(delta_w_EM) * ||T_EM||", "4210/4209"),
        ("R_XF2", "C_XF2", "hidden MTS coupling to F^2 or F wedge F", "abs(C_XF2 * projection_XF2)", "4210/4209"),
        ("R_JQ", "C_JQ", "charge/current normalization residual", "abs(C_JQ * projection_JQ)", "4210/4209/4083"),
        ("R_balpha", "b_alpha", "vertical drift of effective alpha", "abs(b_alpha * sensitivity_alpha)", "4210/4209"),
        ("R_dlambda", "dlnlambda_derivative", "derivative interaction from varying Maxwell kinetic normalization", "abs(dlnlambda_derivative * scale_length)", "4210/4209"),
        ("R_marker", "b_A/b_marker", "material/clock/EM constants fail to descend q-basicly", "abs(sum_A sensitivity_A b_A)", "4210"),
        ("R_Hodge", "Delta_Hodge_EM", "constitutive/Hodge mismatch", "||Delta_Hodge_EM||", "4208/4210"),
        ("R_rad_Poynting", "Delta_rad_Poynting", "open radiative EM/Poynting flux through collar", "abs(Phi_EM_rad)/(M_H c^2/window)", "4207/4210/4217"),
        ("R_internal_exchange", "Delta_internal_exchange", "matter-EM exchange not owned by one visible action", "||nabla_mu T_total_visible^{mu nu}||_exchange", "4207/3620"),
        ("R_cPoynt_extra", "c_Poynt_extra", "standalone Poynting source double count", "abs(c_Poynt_extra * int_boundary S_Poynting dot n dA)", "4207"),
        ("M_H_ref", "M_H_ref", "same-frame positive source-charge denominator", "MISSING_STABLE_MH_REF", "4212/4217"),
    ]
    return [
        {
            **common(),
            "component": component,
            "coefficient": coefficient,
            "meaning": meaning,
            "absolute_component": formula,
            "source_basis": source_basis,
            "numeric_value": "MISSING",
            "source_path": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "status": "valid_for_bound_schema_only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for component, coefficient, meaning, formula, source_basis in rows
    ]


def score_update_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "score_id": "VES4218_0_I_matter_EM",
            "quantity": "I_matter_EM",
            "value_or_bound": "0_under_VEM4218_selector",
            "status": "CONDITIONAL_ZERO_SELECTOR",
            "remaining_dependency": "",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "score_id": "VES4218_1_visible_EM_bound",
            "quantity": "I_matter_EM_bound",
            "value_or_bound": "(|R_w_EM|+|R_XF2|+|R_JQ|+|R_balpha|+|R_dlambda|+|R_marker|+|R_Hodge|+|R_rad_Poynting|+|R_internal_exchange|+|R_cPoynt_extra|)/M_H_ref",
            "status": "BOUND_ROW_RETAINED",
            "remaining_dependency": "numeric/source-backed residual components and M_H_ref",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "score_id": "VES4218_2_delta_Htau_update",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "value_or_bound": "(|I_Dq|)/M_H_ref after 4213-4218 selectors, with all selector caveats retained",
            "status": "FULL_SCORE_REQUIRES_DQ_AND_MHREF",
            "remaining_dependency": "I_Dq;M_H_ref",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def route_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "VER4218_0_activate_selector",
            "standard visible import selector",
            "use calibrated visible matter/Maxwell sector; residual action DeltaS_MTS_visible is zero",
            "I_matter_EM=0 conditionally",
        ),
        (
            "VER4218_1_bound_residual",
            "visible-sector deformation branch",
            "if any visible EM/material/current side channel survives, score the absolute residual envelope",
            "no theorem-zero credit",
        ),
        (
            "VER4218_2_alpha_quarantine",
            "fine-structure prediction branch",
            "do not treat calibrated alpha_EM as an MTS prediction",
            "global EM unification remains open",
        ),
        (
            "VER4218_3_no_double_count",
            "Poynting and Lorentz exchange accounting",
            "stationary bound EM energy is inside T_H; radiation is boundary flux",
            "no hidden background-force term",
        ),
        (
            "VER4218_4_next_Dq",
            "next source-charge obstruction",
            "after I_matter_EM, the retained numerator obstruction is I_Dq",
            "send to 4219",
        ),
    ]
    return [
        {
            **common(),
            "route_id": route_id,
            "route": route,
            "condition": condition,
            "effect": effect,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for route_id, route, condition, effect in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "visible_EM_residual_closed_inside_selector": "True",
            "residual_bound_row_retained": "True",
            "MTS_alpha_prediction_claim": "False",
            "global_Maxwell_derivation_claim": "False",
            "full_Htau_integrability_claim": "False",
            "local_GR_claim": "False",
            "remaining_numerator_obstruction": "I_Dq",
            "remaining_denominator_obstruction": "M_H_ref",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "VEF4218_0_no_global_Maxwell_claim",
            "MTS derives Maxwell/QED globally",
            "blocked",
            "4218 imports calibrated visible Maxwell only for local-GR reduction",
        ),
        (
            "VEF4218_1_no_alpha_prediction",
            "MTS predicts alpha_EM",
            "blocked",
            "4209/4210 keep alpha as calibrated unless a parent scale law exists",
        ),
        (
            "VEF4218_2_no_local_GR_claim",
            "local GR proven",
            "blocked",
            "I_Dq and M_H_ref remain unresolved after the visible EM residual closes",
        ),
        (
            "VEF4218_3_no_radiation_erasure",
            "radiative Poynting flux silently zero",
            "blocked",
            "nonzero flux is routed to boundary/Hamiltonian rows",
        ),
        (
            "VEF4218_4_no_cancellation",
            "unknown visible residuals cancel each other",
            "blocked",
            "fallback row uses absolute component envelope",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_claim": forbidden,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, status, reason in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "private_checkpoint": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "summary": "I_matter_EM conditionally closes as an extra-residual term under the standard visible import selector; bound rows remain if MTS-visible deformations survive.",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4218 conditionally closes the visible EM/material/current residual; the next retained numerator obstruction is Dq/source-readout/coupling-marker leakage.",
            "route_A": "derive I_Dq=0 from quotient naturality, q-basic readout constants and no source-coupling marker",
            "route_B": "if not zero, fill Dq/source-readout/coupling-marker bound row over M_H_ref",
            "route_C": "after I_Dq, attack stable positive M_H_ref denominator",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 234 - PPC4161 visible EM/material curl zero or residual bound

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Target

4212 retained:

```text
I_matter_EM.
```

This is not the ordinary Maxwell stress-energy itself. Ordinary visible matter and EM already enter the `I_EH_visible` subcharge through the standard Hilbert source. The target here is the extra MTS-visible-sector residual left after that import.

## Action Split

Use the local split:

```text
S_visible_parent
= S_vis_standard[g_obs,A,psi,theta_obs]
+ DeltaS_MTS_visible.
```

The standard imported action is:

```text
S_vis_standard
= S_matter[psi,g_obs,theta_obs]
+ S_Maxwell-Hodge[A,g_obs; alpha_EM_obs]
+ S_binding
+ dB_impr.
```

with calibrated/q-basic:

```text
theta_obs = {{m_A, charges, alpha_EM, hbar, c, material labels}}.
```

The Hilbert source is varied once:

```text
T_H = -2/sqrt(-g_obs) delta S_vis_standard/delta g_obs.
```

## Zero Theorem

Assume:

1. standard visible matter import is active;
2. Maxwell-Hodge uses the same observed metric/coframe/Hodge star;
3. charge/current normalization and material labels are calibrated q-basic constants, not hidden MTS fields;
4. matter-EM Lorentz exchange is internal to `T_H`;
5. no extra `w_EM`, `C_XF2`, `C_JQ`, `b_alpha`, `dlnlambda`, material marker, constitutive or standalone Poynting operator is present;
6. live radiative Poynting flux is boundary-routed, not put into a hidden bulk source.

Then:

```text
omega_visible_EM_residual = delta omega[DeltaS_MTS_visible] = 0,
I_matter_EM = int_S i_tau omega_visible_EM_residual = 0.
```

The meaning is precise: local GR may use calibrated visible matter exactly as GR does. It does **not** mean MTS has derived global Maxwell/QED or predicted `alpha_EM`.

## Fallback Bound

If any visible-sector deformation survives:

```text
|I_matter_EM|/M_H_ref
<= (|R_w_EM|
 + |R_XF2|
 + |R_JQ|
 + |R_balpha|
 + |R_dlambda|
 + |R_marker|
 + |R_Hodge|
 + |R_rad_Poynting|
 + |R_internal_exchange|
 + |R_cPoynt_extra|) / M_H_ref.
```

No cancellation between unknown visible-sector terms is allowed.

## Reduced Curl Status

Inside the 4213 through 4218 selectors, the reduced 4212 numerator drops:

```text
I_qbasic_vertical,
I_projector,
I_ref,
I_tau+I_surface+C_frame,
I_boundary+I_corner,
I_matter_EM.
```

The full source-charge theorem still requires:

- `I_Dq`;
- stable positive `M_H_ref`.

## Next Target

`{NEXT_TARGET}` should attack:

```text
I_Dq.
```
"""


def checkpoint_doc() -> str:
    return f"""# 4218 - visible EM/material curl zero or residual bound row

**Status:** `{DECISION}`.

## What changed

- Wrote `{FORMAL_PATH}`.
- Added source-backed CSV rows for the visible EM/material residual theorem, activation clauses, residual components, reduced curl update, route matrix, decision row and firewall.
- Updated `{CLAIMS_PATH}` with `{CLAIM_ID}` if absent.
- Updated `{SPINE_PATH}` and `{PACKET_PATH}` with `{SPINE_MARKER}` / `{PACKET_MARKER}`.

## Result

`I_matter_EM=0` is conditionally derived only inside the standard visible import selector:

```text
S_visible_parent = S_vis_standard + DeltaS_MTS_visible,
DeltaS_MTS_visible = 0
=> I_matter_EM = 0.
```

This keeps the honest distinction:

- calibrated visible Maxwell/matter may be used for local GR reduction;
- MTS does not yet predict `alpha_EM`;
- MTS does not yet globally derive Maxwell/QED;
- any visible-sector deformation reopens the absolute residual bound row.

## Next

`{NEXT_TARGET}` should attack `I_Dq`; after that the denominator `M_H_ref` remains the main source-charge obstruction.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},em_local_gr,'
        f'"The visible EM/material/current curl residual is conditionally closed inside the standard visible import selector: ordinary calibrated matter, Maxwell-Hodge stress, binding and Poynting flux enter one Hilbert source, while DeltaS_MTS-visible=0 gives I_matter_EM=0; if any visible MTS deformation survives, an absolute residual bound row is retained.",'
        f'"4218 source audit, visible EM residual theorem, activation clauses, residual components, curl score update, route matrix, decision row and firewall.",'
        f'private_visible_EM_material_curl_zero_conditional_nonclaim,'
        f'"Attack Dq/source-readout/coupling-marker leakage I_Dq, then stable positive M_H_ref.",'
        f'"This is a calibrated local-GR visible matter import, not a derivation of global Maxwell/QED or alpha_EM."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 visible EM/material curl zero - 4218

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4218 conditionally closes the 4212 visible EM/material residual:

```text
standard visible import + same Maxwell-Hodge Hilbert source + DeltaS_MTS_visible=0
=> I_matter_EM=0.
```

This is not a global Maxwell/QED or alpha derivation. It is the local-GR-calibrated visible matter route, with residual rows retained for any MTS-visible deformation."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet visible EM/material curl zero - 4218

Marker: `{PACKET_MARKER}`

The packet now has conditional zero theorems for `I_qbasic_vertical`, `I_projector`, `I_ref`, `I_tau+I_surface+C_frame`, `I_boundary+I_corner`, and `I_matter_EM`. Remaining source-charge obstructions: `I_Dq` and stable positive `M_H_ref`."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4218_SOURCE_REGISTER.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4218_VISIBLE_EM_THEOREM.csv"]
    activation = rows_by_file["P8_Y5_R2FR_4218_ACTIVATION_CLAUSES.csv"]
    residual = rows_by_file["P8_Y5_R2FR_4218_VISIBLE_EM_RESIDUAL_COMPONENTS.csv"]
    score = rows_by_file["P8_Y5_R2FR_4218_CURL_SCORE_UPDATE.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4218_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4218_DECISION.csv"][0]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    required_theorems = {
        "VEM4218_0_target",
        "VEM4218_1_action_split",
        "VEM4218_2_standard_hilbert_source",
        "VEM4218_3_maxwell_hodge_owner",
        "VEM4218_4_internal_exchange",
        "VEM4218_5_charge_current_normalization",
        "VEM4218_6_residual_symplectic_form",
        "VEM4218_7_curl_zero",
        "VEM4218_8_residual_bound",
        "VEM4218_9_nonclaim_guard",
    }
    required_components = {
        "R_w_EM",
        "R_XF2",
        "R_JQ",
        "R_balpha",
        "R_dlambda",
        "R_marker",
        "R_Hodge",
        "R_rad_Poynting",
        "R_internal_exchange",
        "R_cPoynt_extra",
        "M_H_ref",
    }
    checks = [
        ("VAL4218_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4218_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4218_2_theorem_complete", "visible EM theorem rows contain all clauses", required_theorems.issubset({row["theorem_id"] for row in theorem})),
        ("VAL4218_3_zero_clause", "I_matter_EM zero clause exists", any(row["theorem_id"] == "VEM4218_7_curl_zero" and row["status"] == "conditional_zero_theorem" for row in theorem)),
        ("VAL4218_4_nonclaim_guard", "global Maxwell and alpha claims remain false", any(row["theorem_id"] == "VEM4218_9_nonclaim_guard" for row in theorem)),
        ("VAL4218_5_activation_clauses", "activation clauses include visible import, Hodge, current, exchange, no-extra-operator, radiation and MHref", {"VEA4218_0_visible_import", "VEA4218_1_same_hodge", "VEA4218_2_current_normalization", "VEA4218_3_internal_exchange", "VEA4218_4_no_extra_operator", "VEA4218_5_radiation_routed", "VEA4218_6_MHref_denominator"}.issubset({row["activation_id"] for row in activation})),
        ("VAL4218_6_residual_components", "residual components cover visible EM envelope and MHref", required_components.issubset({row["component"] for row in residual})),
        ("VAL4218_7_score_update_zero", "curl score update records conditional I_matter_EM zero", any(row["quantity"] == "I_matter_EM" and row["value_or_bound"] == "0_under_VEM4218_selector" for row in score)),
        ("VAL4218_8_reduced_curl_remaining", "reduced curl names I_Dq and M_H_ref as remaining blockers", any(row["remaining_dependency"] == "I_Dq;M_H_ref" for row in score)),
        ("VAL4218_9_routes", "routes include selector, bound, alpha quarantine, double-count guard and Dq next", {"VER4218_0_activate_selector", "VER4218_1_bound_residual", "VER4218_2_alpha_quarantine", "VER4218_3_no_double_count", "VER4218_4_next_Dq"}.issubset({row["route_id"] for row in routes})),
        ("VAL4218_10_decision_nonclaim", "decision keeps global Maxwell, alpha, local-GR and full Htau claims false", decision["global_Maxwell_derivation_claim"] == "False" and decision["MTS_alpha_prediction_claim"] == "False" and decision["local_GR_claim"] == "False" and decision["full_Htau_integrability_claim"] == "False"),
        ("VAL4218_11_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4218_12_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4218_13_claim_register", "claim register contains L-059", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4218_14_spine_packet_next", "spine/packet markers and next target present", SPINE_MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH) and decision["next_target"] == NEXT_TARGET),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(bool(passed)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed in checks
    ]


def write_all() -> None:
    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8", newline="\n")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8", newline="\n")
    rows_by_file = {
        "P8_Y5_R2FR_4218_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4218_VISIBLE_EM_THEOREM.csv": theorem_rows(),
        "P8_Y5_R2FR_4218_ACTIVATION_CLAUSES.csv": activation_rows(),
        "P8_Y5_R2FR_4218_VISIBLE_EM_RESIDUAL_COMPONENTS.csv": residual_component_rows(),
        "P8_Y5_R2FR_4218_CURL_SCORE_UPDATE.csv": score_update_rows(),
        "P8_Y5_R2FR_4218_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4218_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4218_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4218_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4218_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    update_registers()
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4218_VALIDATION.csv", validation)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4218_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
