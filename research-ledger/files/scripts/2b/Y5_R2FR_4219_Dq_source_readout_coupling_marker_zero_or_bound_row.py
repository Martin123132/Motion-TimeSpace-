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

CHECKPOINT = "4219"
CLAIM_ID = "L-060"
BRANCH_ID = "MTS_R2FR_Y5_DQ_SOURCE_READOUT_MARKER_ZERO_4219"
DECISION = (
    "DQ_SOURCE_READOUT_COUPLING_MARKER_ZERO_CONDITIONALLY_DERIVED_FOR_QNATURAL_"
    "COMPONENTWISE_ZERO_BOUND_ROW_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md"
DOC_PATH = POST / "4219-Y5-R2FR-Dq-source-readout-coupling-marker-zero-or-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_DQ_SOURCE_READOUT_MARKER_ZERO_4219"
PACKET_MARKER = "PPC4161_PACKET_DQ_SOURCE_READOUT_MARKER_ZERO_4219"
NEXT_TARGET = "4220-Y5-R2FR-MHref-positive-source-denominator-stability-or-bound-pack.md"

SOURCES = {
    "SRC4219_00_4218_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4218_NEXT_TARGET.csv",
        "4219-Y5-R2FR-Dq-source-readout-coupling-marker-zero-or-bound-row.md",
        "4218 selected Dq/source-readout/coupling-marker leakage as next obstruction.",
    ),
    "SRC4219_01_4212_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4212_CURL_COMPONENTS.csv",
        "I_Dq",
        "4212 retained the Dq/source-readout/coupling-marker curl component.",
    ),
    "SRC4219_02_193_qnaturality": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "D O_loc[v] = D Obar_loc[Dq[v]] = 0",
        "Formal quotient naturality vertical silence theorem.",
    ),
    "SRC4219_03_2643_parent_gate": (
        SOURCE_DIR / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv",
        "QVIS2643_0_chain_rule_theorem",
        "Common matter descent DqZ parent signature gate.",
    ),
    "SRC4219_04_2643_leak_bounds": (
        SOURCE_DIR / "P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv",
        "LEAK2643_1_Dq_Z_norm",
        "Dq and source-readout leak bound rows.",
    ),
    "SRC4219_05_4109_matrix_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4109_DQ_MATRIX_GATE.csv",
        "DQM4109_1_Dq_bound_law",
        "Dq matrix criterion and bound law.",
    ),
    "SRC4219_06_4120_norm": (
        SOURCE_DIR / "P8_Y5_R2FR_4120_DQXZ_NO_CANCELLATION_LEMMA.csv",
        "LEM4120_0_positive_norm",
        "Positive component norm/no-cancellation lemma.",
    ),
    "SRC4219_07_4120_formula": (
        SOURCE_DIR / "P8_Y5_R2FR_4120_FILLED_DQXZ_ROWS.csv",
        "DQL4120_0_Dq_Z_filled_formula",
        "Filled symbolic Dq X/Z component formulas.",
    ),
    "SRC4219_08_4121_chain": (
        SOURCE_DIR / "P8_Y5_R2FR_4121_SOURCE_CURRENT_LAW.csv",
        "SCL4121_0_general_chain_rule",
        "Source-current chain-rule law for readout leaks.",
    ),
    "SRC4219_09_3516_bound_template": (
        SOURCE_DIR / "P8_Y5_R2FR_3516_DQ_SOURCE_COORDINATE_LEAK_BOUND_TEMPLATE.csv",
        "QSL3516_0_E_Dq",
        "Dq source-coordinate leak bound template.",
    ),
    "SRC4219_10_3604_bound_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_3604_DQ_LEAK_BOUND_ROWS.csv",
        "DQB3604_0_total",
        "Actual q-map vertical basis Dq bound rows.",
    ),
    "SRC4219_11_234_formal": (
        FORMAL / "234-PPC4161-visible-EM-material-curl-zero-or-residual-bound.md",
        "I_Dq",
        "4218 reduced curl status pointing to this obstruction.",
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
            "DQT4219_0_target",
            "target residual",
            "I_Dq := int_S i_tau omega_Dq_marker",
            "definition_from_4212",
            "the term measures source/readout/coupling-marker leakage after the other numerator terms are closed",
        ),
        (
            "DQT4219_1_qnatural_chain",
            "quotient naturality",
            "O_loc=Obar_loc o q and Dq[v]=0 imply D O_loc[v]=0",
            "exact_chain_rule_theorem",
            "readout must factor through q before variation, not after a fitted local solution",
        ),
        (
            "DQT4219_2_variation_before_readout",
            "pre-variation descent",
            "delta_v S_red[q(Phi)]=<delta S_red/delta q,Dq[v]>=0",
            "conditional_zero_theorem",
            "a post-readout projection does not earn theorem-zero credit",
        ),
        (
            "DQT4219_3_component_norm",
            "componentwise Dq zero",
            "||Dq[v]||_q^2=sum_i w_i||Dq_i[v]||^2 with w_i>0, so zero requires every Dq_i[v]=0",
            "positive_norm_lemma",
            "geometry cannot cancel a source/readout or marker leak",
        ),
        (
            "DQT4219_4_source_current_chain",
            "source-current chain rule",
            "J_A_source=Pi_M^*[L_G partial_A G_obs + L_M partial_A M_obs + L_B partial_A B_obs + L_EM partial_A EM_obs]",
            "exact_chain_rule_form",
            "if all observed source/readout derivatives vanish, no source current is injected",
        ),
        (
            "DQT4219_5_marker_silence",
            "q-basic constants and material labels",
            "D_v theta_A=D_v m_A=D_v alpha_EM=D_v source_normalization=0",
            "selector_clause",
            "material markers cannot be hidden representative fields",
        ),
        (
            "DQT4219_6_boundary_projector",
            "boundary/projector readout",
            "boundary, H_ref, Pi_M, P_loc and corner data are fixed, exact, or already routed",
            "selector_clause",
            "Dq cannot reintroduce source dependence through a moving readout surface",
        ),
        (
            "DQT4219_7_curl_zero",
            "conditional Dq marker curl zero",
            "componentwise Dq[v]=0 plus q-basic source/readout constants and no source-only marker => I_Dq=0",
            "conditional_zero_theorem",
            "this closes the final 4212 numerator term only inside the explicit selector",
        ),
        (
            "DQT4219_8_bound_fallback",
            "fallback Dq bound",
            "|I_Dq|/M_H_ref <= epsilon_Dq_source_readout/M_H_ref",
            "bound_row_retained",
            "if any q component is unsigned/nonzero, the leakage is bounded rather than assumed away",
        ),
        (
            "DQT4219_9_nonclaim_guard",
            "claim firewall",
            "curl_numerator_closed_inside_selectors=True; local_GR_claim=false; M_H_ref_available=false",
            "nonclaim_guard",
            "the numerator route is not a source-normalization or Newton-constant theorem",
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
        ("DQA4219_0_parent_qmap", "parent q-map exists before tests", "q: Phi_parent -> Q_obs is declared before variation/readout", "required"),
        ("DQA4219_1_vertical_basis", "candidate vertical basis declared", "every allowed v is tested against the same Dq matrix", "required"),
        ("DQA4219_2_componentwise_zero", "all q components vanish", "geometry, tau, matter, source/readout, theta, boundary, EM and coefficient components are zero", "required"),
        ("DQA4219_3_qbasic_constants", "constants and material labels are q-basic", "masses, alpha, charges, hbar, c and material/source labels do not vary along v", "required"),
        ("DQA4219_4_no_source_marker", "no source-only coupling marker", "ordinary source action has no pre-variation source-only weight or marker slot", "required"),
        ("DQA4219_5_boundary_projector_routed", "boundary/projector readout fixed or routed", "moving boundary, H_ref, Pi_M and P_loc derivatives are absent or separate bound rows", "required"),
        ("DQA4219_6_no_post_readout_projection", "variation before readout", "no term is set zero by projecting after it has already coupled", "required"),
        ("DQA4219_7_MHref_denominator", "source denominator still required", "closing I_Dq does not prove stable positive M_H_ref", "retained_for_4220"),
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


def component_rows() -> List[Dict[str, str]]:
    rows = [
        ("DQC4219_0_geometry", "q_geom", "g_obs;e_obs;connection_obs", "Dq_geom[v]=0", "conditional_zero_required"),
        ("DQC4219_1_tau", "q_tau", "tau;clock branch;time readout", "Dq_tau[v]=0", "conditional_zero_required"),
        ("DQC4219_2_matter", "q_matter", "ordinary matter fields/constants", "Dq_matter[v]=0", "conditional_zero_required"),
        ("DQC4219_3_source_readout", "q_source_readout", "source mass;Hamiltonian mass;mu_obs", "Dq_source_readout[v]=0", "conditional_zero_required"),
        ("DQC4219_4_theta_marker", "q_theta_marker", "masses;charges;alpha;material labels", "Dq_theta_marker[v]=0", "conditional_zero_required"),
        ("DQC4219_5_boundary_projector", "q_boundary_projector", "boundary class;H_ref;Pi_M;P_loc;corner data", "Dq_boundary_projector[v]=0 or routed", "conditional_zero_required"),
        ("DQC4219_6_EM", "q_EM", "Maxwell-Hodge;T_EM;Poynting route", "Dq_EM[v]=0 or retained by 4218/boundary route", "conditional_zero_required"),
        ("DQC4219_7_coefficients", "q_coeff", "G_N/kappa/normalization/coefficient slots", "Dq_coeff[v]=0 or common calibrated slot", "conditional_zero_required"),
        ("DQC4219_8_operator", "q_operator", "P_loc;Pi_M;readout kernels", "operator fixed before variation or derivative scored", "conditional_zero_required"),
    ]
    return [
        {
            **common(),
            "component_id": component_id,
            "q_component": q_component,
            "meaning": meaning,
            "zero_condition": zero_condition,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for component_id, q_component, meaning, zero_condition, status in rows
    ]


def bound_component_rows() -> List[Dict[str, str]]:
    rows = [
        ("E_Dq_total", "epsilon_Dq_total", "max_i ||Dq[v_i]||_q/||v_i||", "overall component norm envelope"),
        ("E_q_parent", "epsilon_q_parent", "q(Phi)=Q_vis ownership defect", "parent q definition missing or altered after failures"),
        ("E_geom", "epsilon_geom", "||Dq_geom[v]||", "observed geometry/coframe derivative"),
        ("E_tau", "epsilon_tau", "||Dq_tau[v]||", "time/clock/tau readout derivative"),
        ("E_matter", "epsilon_matter", "||Dq_matter[v]||", "ordinary matter/constants descent defect"),
        ("E_source_readout", "epsilon_source_readout", "||Dq_source_readout[v]||", "source mass/Hamiltonian mass/readout derivative"),
        ("E_theta_marker", "epsilon_theta_marker", "||Dq_theta_marker[v]||", "material/source marker leak"),
        ("E_boundary_projector", "epsilon_boundary_projector", "||Dq_boundary_projector[v]||", "boundary/H_ref/Pi_M/P_loc derivative"),
        ("E_EM_readout", "epsilon_EM_readout", "||Dq_EM[v]||", "EM/Poynting/Hodge readout derivative"),
        ("E_coeff_marker", "epsilon_coeff_marker", "||Dq_coeff[v]||", "coefficient/coupling marker drift"),
        ("E_post_readout", "epsilon_post_readout", "||projection_after_coupling||", "post-readout projection cheat"),
        ("E_Y_transfer", "epsilon_Y_transfer", "||dYbar|| epsilon_Dq + E_Y", "source-coordinate transfer from Dq leak"),
        ("M_H_ref", "M_H_ref", "MISSING_STABLE_MH_REF", "same-frame positive source-charge denominator"),
    ]
    return [
        {
            **common(),
            "component": component,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "numeric_value": "MISSING",
            "source_path": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "status": "valid_for_bound_schema_only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for component, symbol, formula, meaning in rows
    ]


def score_update_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "score_id": "DQS4219_0_I_Dq",
            "quantity": "I_Dq",
            "value_or_bound": "0_under_DQT4219_selector",
            "status": "CONDITIONAL_ZERO_SELECTOR",
            "remaining_dependency": "",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "score_id": "DQS4219_1_Dq_bound",
            "quantity": "I_Dq_bound",
            "value_or_bound": "(|E_Dq_total|+|E_q_parent|+|E_geom|+|E_tau|+|E_matter|+|E_source_readout|+|E_theta_marker|+|E_boundary_projector|+|E_EM_readout|+|E_coeff_marker|+|E_post_readout|+|E_Y_transfer|)/M_H_ref",
            "status": "BOUND_ROW_RETAINED",
            "remaining_dependency": "numeric/source-backed Dq components and M_H_ref",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "score_id": "DQS4219_2_delta_Htau_update",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "value_or_bound": "0_under_4213_through_4219_selectors_if_M_H_ref_positive",
            "status": "NUMERATOR_CONDITIONALLY_CLOSED_MHREF_REMAINS",
            "remaining_dependency": "M_H_ref",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def route_rows() -> List[Dict[str, str]]:
    rows = [
        ("DQR4219_0_activate_selector", "componentwise q-natural selector", "all Dq components and marker/readout slots vanish before variation", "I_Dq=0 conditionally"),
        ("DQR4219_1_bound_Dq", "finite Dq leak branch", "any q component is nonzero/unsigned", "fill absolute Dq/source-readout bound row"),
        ("DQR4219_2_no_geometry_only", "reject geometry-only proof", "metric/coframe verticality without source/readout/theta/boundary silence", "not enough for local-GR source coupling"),
        ("DQR4219_3_no_post_readout", "reject post-readout projection", "projection applied after coupling/readout", "not theorem-zero"),
        ("DQR4219_4_next_MHref", "next source-charge obstruction", "4219 closes the last retained numerator term inside selectors", "send to M_H_ref denominator stability"),
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
            "Dq_marker_closed_inside_selector": "True",
            "Dq_bound_row_retained": "True",
            "curl_numerator_closed_inside_selectors": "True",
            "M_H_ref_available": "False",
            "full_Htau_integrability_claim": "False",
            "Newton_source_normalization_claim": "False",
            "local_GR_claim": "False",
            "remaining_numerator_obstruction": "none_inside_4213_4219_selectors",
            "remaining_denominator_obstruction": "M_H_ref",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("DQF4219_0_no_geometry_only_claim", "geometry/coframe Dq zero proves source coupling", "blocked", "source/readout, theta, boundary/projector, EM and coefficient components must vanish too"),
        ("DQF4219_1_no_post_readout_projection", "project away Dq after coupling", "blocked", "factorization must happen before variation/readout"),
        ("DQF4219_2_no_local_GR_claim", "local GR proven", "blocked", "stable positive M_H_ref and parent adoption remain open"),
        ("DQF4219_3_no_numeric_claim", "Dq finite bound is scoreable", "blocked", "no numeric/source-backed Dq matrix rows are supplied here"),
        ("DQF4219_4_no_cancellation", "Dq components cancel", "blocked", "positive component norm requires componentwise zero or absolute bound rows"),
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
            "summary": "I_Dq conditionally closes only when the full q/readout matrix is componentwise silent before variation; M_H_ref remains the next source-charge obstruction.",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4219 conditionally closes the last retained curl numerator term inside the selector chain; the remaining live local-GR/source-charge obstruction is stable positive M_H_ref.",
            "route_A": "derive M_H_ref as a same-frame positive Hamiltonian/source charge with fixed H_ref and no readout/imported-GM denominator",
            "route_B": "if not derivable, fill M_H_ref positivity/stability bound pack and denominator nonzero gate",
            "route_C": "only after M_H_ref is owned can the private local-GR/Newton source-charge theorem be summarized cleanly",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 235 - PPC4161 Dq source-readout coupling-marker zero or bound

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Target

4212 retained:

```text
I_Dq.
```

After 4213 through 4218, this is the last retained numerator obstruction in the private `H_tau` curl chain.

## Quotient-Natural Zero Route

Let:

```text
q: Phi_parent -> Q_obs,
V_q = ker(Dq),
v in V_q.
```

For any local observable/readout that factors before variation:

```text
O_loc = Obar_loc o q,
D O_loc[v] = D Obar_loc[Dq[v]] = 0.
```

The key is componentwise silence:

```text
||Dq[v]||_q^2
= sum_i w_i ||Dq_i[v]||^2,
w_i > 0.
```

Therefore `||Dq[v]||_q=0` only if every component is zero:

```text
Dq_geom[v]=0,
Dq_tau[v]=0,
Dq_matter[v]=0,
Dq_source_readout[v]=0,
Dq_theta_marker[v]=0,
Dq_boundary_projector[v]=0,
Dq_EM[v]=0,
Dq_coeff[v]=0.
```

Then:

```text
omega_Dq_marker = 0,
I_Dq = int_S i_tau omega_Dq_marker = 0.
```

This is not a geometry-only statement. The source mass, material constants, clock/EM standards, boundary/reference data and readout projectors must all be q-basic or separately routed.

## Bound Route

If any component is unsigned or nonzero:

```text
|I_Dq|/M_H_ref
<= (|E_Dq_total|
 + |E_q_parent|
 + |E_geom|
 + |E_tau|
 + |E_matter|
 + |E_source_readout|
 + |E_theta_marker|
 + |E_boundary_projector|
 + |E_EM_readout|
 + |E_coeff_marker|
 + |E_post_readout|
 + |E_Y_transfer|) / M_H_ref.
```

No cancellation between q-components is allowed.

## Reduced Curl Status

Inside the 4213 through 4219 selectors, every retained 4212 numerator term has a conditional zero route:

```text
I_qbasic_vertical,
I_projector,
I_ref,
I_tau+I_surface+C_frame,
I_boundary+I_corner,
I_matter_EM,
I_Dq.
```

The remaining local source-charge obstruction is no longer a numerator curl term. It is:

```text
M_H_ref.
```

## Next Target

`{NEXT_TARGET}` should prove or bound stable positive `M_H_ref`.
"""


def checkpoint_doc() -> str:
    return f"""# 4219 - Dq source-readout coupling-marker zero or bound row

**Status:** `{DECISION}`.

## What changed

- Wrote `{FORMAL_PATH}`.
- Added source-backed CSV rows for the Dq theorem, activation clauses, component matrix, bound components, curl score update, route matrix, decision row and firewall.
- Updated `{CLAIMS_PATH}` with `{CLAIM_ID}` if absent.
- Updated `{SPINE_PATH}` and `{PACKET_PATH}` with `{SPINE_MARKER}` / `{PACKET_MARKER}`.

## Result

`I_Dq=0` is conditionally derived only under the componentwise quotient-natural selector:

```text
O_loc = Obar_loc o q,
Dq_i[v]=0 for every geometry/source/readout/marker/boundary/EM/coefficient component
=> I_Dq=0.
```

This closes the last retained numerator obstruction inside the private selector chain. It does **not** prove local GR publicly because stable positive `M_H_ref` remains unowned.

## Next

`{NEXT_TARGET}` should attack the denominator/source-charge normalization: `M_H_ref`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The Dq/source-readout/coupling-marker curl residual is conditionally closed inside the full quotient-natural selector: when every geometry, tau, matter, source-readout, theta-marker, boundary/projector, EM and coefficient component of Dq vanishes before variation, I_Dq=0; otherwise an absolute Dq bound row is retained.",'
        f'"4219 source audit, Dq theorem, activation clauses, component matrix, bound components, curl score update, route matrix, decision row and firewall.",'
        f'private_Dq_source_readout_marker_zero_conditional_nonclaim,'
        f'"Derive or bound stable positive M_H_ref denominator/source charge.",'
        f'"Geometry-only Dq silence is not enough; source/readout and marker components must be q-basic before variation."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Dq source-readout marker zero - 4219

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4219 conditionally closes the final 4212 numerator obstruction:

```text
componentwise quotient naturality before variation
=> I_Dq=0.
```

The chain is now down to the denominator/source-charge problem: stable positive `M_H_ref`."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Dq source-readout marker zero - 4219

Marker: `{PACKET_MARKER}`

The packet now has conditional zero theorems for every retained 4212 numerator term through `I_Dq`. Remaining obstruction: stable positive `M_H_ref` and its no-imported-GM/source-normalization contract."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4219_SOURCE_REGISTER.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4219_DQ_THEOREM.csv"]
    activation = rows_by_file["P8_Y5_R2FR_4219_ACTIVATION_CLAUSES.csv"]
    components = rows_by_file["P8_Y5_R2FR_4219_DQ_COMPONENT_MATRIX.csv"]
    bound = rows_by_file["P8_Y5_R2FR_4219_DQ_BOUND_COMPONENTS.csv"]
    score = rows_by_file["P8_Y5_R2FR_4219_CURL_SCORE_UPDATE.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4219_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4219_DECISION.csv"][0]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    required_theorems = {
        "DQT4219_0_target",
        "DQT4219_1_qnatural_chain",
        "DQT4219_2_variation_before_readout",
        "DQT4219_3_component_norm",
        "DQT4219_4_source_current_chain",
        "DQT4219_5_marker_silence",
        "DQT4219_6_boundary_projector",
        "DQT4219_7_curl_zero",
        "DQT4219_8_bound_fallback",
        "DQT4219_9_nonclaim_guard",
    }
    required_components = {
        "q_geom",
        "q_tau",
        "q_matter",
        "q_source_readout",
        "q_theta_marker",
        "q_boundary_projector",
        "q_EM",
        "q_coeff",
        "q_operator",
    }
    required_bounds = {
        "E_Dq_total",
        "E_q_parent",
        "E_geom",
        "E_tau",
        "E_matter",
        "E_source_readout",
        "E_theta_marker",
        "E_boundary_projector",
        "E_EM_readout",
        "E_coeff_marker",
        "E_post_readout",
        "E_Y_transfer",
        "M_H_ref",
    }
    checks = [
        ("VAL4219_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4219_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4219_2_theorem_complete", "Dq theorem rows contain all clauses", required_theorems.issubset({row["theorem_id"] for row in theorem})),
        ("VAL4219_3_zero_clause", "I_Dq zero clause exists", any(row["theorem_id"] == "DQT4219_7_curl_zero" and row["status"] == "conditional_zero_theorem" for row in theorem)),
        ("VAL4219_4_component_matrix", "component matrix covers all q components", required_components.issubset({row["q_component"] for row in components})),
        ("VAL4219_5_activation_clauses", "activation clauses include qmap, basis, component zero, qbasic constants, no source marker, boundary/projector, no post-readout and MHref", {"DQA4219_0_parent_qmap", "DQA4219_1_vertical_basis", "DQA4219_2_componentwise_zero", "DQA4219_3_qbasic_constants", "DQA4219_4_no_source_marker", "DQA4219_5_boundary_projector_routed", "DQA4219_6_no_post_readout_projection", "DQA4219_7_MHref_denominator"}.issubset({row["activation_id"] for row in activation})),
        ("VAL4219_6_bound_components", "bound components cover Dq leaks and MHref", required_bounds.issubset({row["component"] for row in bound})),
        ("VAL4219_7_score_update_zero", "curl score update records conditional I_Dq zero", any(row["quantity"] == "I_Dq" and row["value_or_bound"] == "0_under_DQT4219_selector" for row in score)),
        ("VAL4219_8_numerator_closed", "score update marks numerator conditionally closed with MHref remaining", any(row["status"] == "NUMERATOR_CONDITIONALLY_CLOSED_MHREF_REMAINS" and row["remaining_dependency"] == "M_H_ref" for row in score)),
        ("VAL4219_9_routes", "routes include selector, bound, no geometry-only, no post-readout and MHref next", {"DQR4219_0_activate_selector", "DQR4219_1_bound_Dq", "DQR4219_2_no_geometry_only", "DQR4219_3_no_post_readout", "DQR4219_4_next_MHref"}.issubset({row["route_id"] for row in routes})),
        ("VAL4219_10_decision_nonclaim", "decision keeps local-GR and full Htau claims false while MHref unavailable", decision["M_H_ref_available"] == "False" and decision["local_GR_claim"] == "False" and decision["full_Htau_integrability_claim"] == "False"),
        ("VAL4219_11_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4219_12_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4219_13_claim_register", "claim register contains L-060", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4219_14_spine_packet_next", "spine/packet markers and next target present", SPINE_MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH) and decision["next_target"] == NEXT_TARGET),
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
        "P8_Y5_R2FR_4219_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4219_DQ_THEOREM.csv": theorem_rows(),
        "P8_Y5_R2FR_4219_ACTIVATION_CLAUSES.csv": activation_rows(),
        "P8_Y5_R2FR_4219_DQ_COMPONENT_MATRIX.csv": component_rows(),
        "P8_Y5_R2FR_4219_DQ_BOUND_COMPONENTS.csv": bound_component_rows(),
        "P8_Y5_R2FR_4219_CURL_SCORE_UPDATE.csv": score_update_rows(),
        "P8_Y5_R2FR_4219_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4219_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4219_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4219_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4219_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    update_registers()
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4219_VALIDATION.csv", validation)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4219_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
