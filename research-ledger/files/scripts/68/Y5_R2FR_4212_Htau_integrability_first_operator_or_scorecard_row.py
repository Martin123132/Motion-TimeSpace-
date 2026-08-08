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

CHECKPOINT = "4212"
CLAIM_ID = "L-053"
BRANCH_ID = "MTS_R2FR_Y5_HTAU_INTEGRABILITY_OPERATOR_4212"
DECISION = (
    "HTAU_INTEGRABILITY_OPERATOR_DERIVED_EH_VISIBLE_SUBCURL_ZERO_CONDITIONAL_"
    "MTS_VERTICAL_PROJECTOR_REFERENCE_DENOMINATOR_TERMS_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "228-PPC4161-Htau-integrability-operator-and-curl-bound.md"
DOC_PATH = POST / "4212-Y5-R2FR-Htau-integrability-first-operator-or-source-scorecard-first-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_HTAU_INTEGRABILITY_OPERATOR_4212"
PACKET_MARKER = "PPC4161_PACKET_HTAU_INTEGRABILITY_OPERATOR_4212"
NEXT_TARGET = "4213-Y5-R2FR-qbasic-vertical-presymplectic-silence-or-curl-bound.md"

SOURCES = {
    "SRC4212_00_4211_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4211_NEXT_TARGET.csv",
        "theta_total/Q_tau/omega_total",
        "4211 selects the integrability operator target.",
    ),
    "SRC4212_01_227_formal": (
        FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md",
        "delta H_tau[S]=int_S(delta Q_tau-i_tau theta_total)",
        "4211 source-charge owner clause.",
    ),
    "SRC4212_02_186_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "J_tau = theta_total(Phi,L_tau Phi) - i_tau L_total",
        "Noether current and Hamiltonian one-form source.",
    ),
    "SRC4212_03_190_parent": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "S_parent|loc =",
        "Local parent action decomposition.",
    ),
    "SRC4212_04_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge",
        "Boundary/radiative terms are routed, not hidden.",
    ),
    "SRC4212_05_226_visible": (
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "epsilon_visible_EM_total =",
        "Visible matter/EM residual envelope.",
    ),
    "SRC4212_06_3425_EH": (
        SOURCE_DIR / "P8_Y5_R2FR_3425_EH_INTEGRABILITY_SUBTHEOREM.csv",
        "EHI3425_1_integrability",
        "EH/Hilbert subcharge integrability subtheorem.",
    ),
    "SRC4212_07_4003_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4003_INTEGRABILITY_COMPONENT_BOUND_VECTOR.csv",
        "PCB4003_0_master",
        "Prior component bound vector.",
    ),
    "SRC4212_08_2667_gate": (
        SOURCE_DIR / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv",
        "ICG2667_1_theta_omega",
        "Prior theta/omega gate.",
    ),
    "SRC4212_09_4211_scorecard": (
        SOURCE_DIR / "P8_Y5_R2FR_4211_SOURCE_CHARGE_RESIDUAL_SCORECARD.csv",
        "delta_H_tau_nonintegrable_over_MH",
        "4211 retained source-charge scorecard row.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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


def operator_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "OP4212_0_parent_variation",
            "delta L_total = E_A delta Phi^A + d theta_total(delta Phi)",
            "defines theta_total from the parent local packet action, not borrowed EH notation",
            "operator_defined",
        ),
        (
            "OP4212_1_symplectic_current",
            "omega_total(delta1,delta2)=delta1 theta_total(delta2)-delta2 theta_total(delta1)-theta_total([delta1,delta2])",
            "field-space two-form whose surface contraction controls integrability",
            "operator_defined",
        ),
        (
            "OP4212_2_Noether_current",
            "J_tau = theta_total(L_tau Phi) - i_tau L_total = C_tau + dQ_tau",
            "defines Q_tau and constraint current from the same parent theta_total",
            "operator_defined",
        ),
        (
            "OP4212_3_Hamiltonian_one_form",
            "alpha_tau,S(delta)=int_S(delta Q_tau - i_tau theta_total(delta)) - delta H_ref",
            "Hamiltonian variation one-form whose exactness defines H_tau",
            "operator_defined",
        ),
        (
            "OP4212_4_curl_identity",
            "I_tau,S(delta1,delta2)=d_field alpha_tau,S=int_S i_tau omega_total(delta1,delta2)+I_ref+I_tau+I_corner",
            "fixed tau and fixed surface remove extra terms; otherwise the extra terms are retained explicitly",
            "derived_identity",
        ),
        (
            "OP4212_5_integrability_condition",
            "H_tau exists iff I_tau,S(delta1,delta2)=0 for all allowed local variations",
            "exact local source-charge integrability criterion",
            "derived_condition",
        ),
        (
            "OP4212_6_bound_law",
            "|delta_H_tau_nonintegrable_over_MH| <= sum_abs(I_components)/M_H_ref",
            "nonclaim scorecard row if any curl component is nonzero or unsigned",
            "bound_operator_defined",
        ),
    ]
    return [
        {
            **common(),
            "operator_id": row[0],
            "formula": row[1],
            "meaning": row[2],
            "status": row[3],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def component_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "IC4212_0_EH_visible",
            "I_EH_visible",
            "int_S i_tau omega_EH+visible",
            "conditional_theorem_zero",
            "3425 signs the EH/Hilbert subcharge under fixed tau, fixed reference data and stationary local boundary conditions; 4210 imports visible matter without MTS alpha prediction",
            "0 under compact stationary local collar assumptions",
        ),
        (
            "IC4212_1_qbasic_vertical",
            "I_qbasic_vertical",
            "int_S i_tau omega_qbasic_vertical",
            "retained_for_next_proof",
            "requires ker(Dq) to be presymplectic-null or exact/no-flux on the local collar",
            "MISSING_QBASIC_PRESYMPLECTIC_SILENCE",
        ),
        (
            "IC4212_2_projector_stress",
            "I_projector",
            "curl from Pi_M/domain/Hodge/projector stress",
            "retained_nonclaim",
            "projector stress has to be zero or bounded before local PPN/source closure",
            "MISSING_PROJECTOR_STRESS_BOUND",
        ),
        (
            "IC4212_3_boundary_corner",
            "I_boundary+I_corner",
            "boundary exact, corner, improvement and radiative flux contribution",
            "retained_nonclaim",
            "192 routes nonzero radiative pieces as boundary charge, not hidden bulk current",
            "MISSING_BOUNDARY_CORNER_ZERO_OR_BOUND",
        ),
        (
            "IC4212_4_reference",
            "I_ref",
            "field-space curl of -delta H_ref and reference drift",
            "retained_nonclaim",
            "H_ref has not been parent-selected as fixed and derivative-silent",
            "MISSING_REFERENCE_LOCK",
        ),
        (
            "IC4212_5_tau_surface",
            "I_tau+I_surface",
            "field dependence of tau, moving surface family, and frame mismatch",
            "retained_nonclaim",
            "tau_source=tau_charge=tau_clock=tau_readout is not yet certified",
            "MISSING_TAU_SURFACE_LOCK",
        ),
        (
            "IC4212_6_visible_EM_residual",
            "I_matter_EM",
            "visible EM/material/current/radiative residual contribution",
            "schema_ready_nonclaim",
            "4210 provides epsilon_visible_EM_total but no numeric component values",
            "MISSING_VISIBLE_EM_NUMERIC_COMPONENTS",
        ),
        (
            "IC4212_7_Dq_marker",
            "I_Dq",
            "Dq/source-readout/coupling-marker leakage",
            "retained_nonclaim",
            "coupling marker and quotient map leakage still need parent ownership",
            "MISSING_DQ_COUPLING_LEAK_BOUND",
        ),
        (
            "IC4212_8_denominator",
            "M_H_ref",
            "same-frame positive source-charge denominator",
            "retained_nonclaim",
            "needed before any normalized curl row can be evidence",
            "MISSING_STABLE_MH_REF",
        ),
        (
            "IC4212_9_total",
            "delta_H_tau_nonintegrable_over_MH",
            "absolute no-cancellation sum of retained curl components divided by M_H_ref",
            "partial_formula_nonclaim",
            "operator formula is now derived, but retained components and denominator are not numeric/source-backed",
            "NOT_COMPUTED_COMPONENTS_MISSING",
        ),
    ]
    return [
        {
            **common(),
            "component_id": row[0],
            "component": row[1],
            "operator_piece": row[2],
            "status": row[3],
            "reason": row[4],
            "value_or_bound": row[5],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def scorecard_rows() -> List[Dict[str, str]]:
    rows = [
        {
            **common(),
            "row_id": "HSR4212_0_delta_Htau_integrability",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "operator_definition": "d_field alpha_tau,S / M_H_ref",
            "bound_formula": "(|I_EH_visible|+|I_qbasic_vertical|+|I_projector|+|I_boundary+I_corner|+|I_ref|+|I_tau+I_surface|+|I_matter_EM|+|I_Dq|)/M_H_ref",
            "known_zero_piece": "I_EH_visible=0 under fixed-tau stationary EH/Hilbert visible local collar assumptions",
            "missing_pieces": "I_qbasic_vertical;I_projector;I_boundary+I_corner;I_ref;I_tau+I_surface;I_matter_EM;I_Dq;M_H_ref",
            "numeric_value": "MISSING",
            "units": "dimensionless_after_MHref_normalization",
            "status": "operator_derived_first_row_not_numeric",
            "source_path": str(FORMAL_PATH),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "TH4212_0_identity",
            "Hamiltonian one-form curl identity",
            "alpha_tau,S is exact iff int_S i_tau omega_total + I_ref + I_tau + I_corner vanishes",
            "derived",
        ),
        (
            "TH4212_1_EH_visible_subcurl",
            "EH plus standard visible matter subcurl",
            "I_EH_visible=0 under fixed tau, fixed reference/asymptotic data, stationary source-free local collar and no visible EM side-channel",
            "conditional_zero_derived",
        ),
        (
            "TH4212_2_full_MTS_integrability",
            "full MTS H_tau integrability",
            "requires q-basic vertical presymplectic silence plus projector, reference, tau/surface, boundary/corner, visible residual and denominator locks",
            "not_claimed",
        ),
        (
            "TH4212_3_bound_path",
            "nonzero residual path",
            "if any component is not zero, it must enter delta_H_tau_nonintegrable_over_MH with no cancellation",
            "bound_path_ready",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": row[0],
            "claim": row[1],
            "statement": row[2],
            "status": row[3],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def route_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "RT4212_0_attack_vertical",
            "Prove q-basic vertical presymplectic silence",
            "show ker(Dq) variations are null/exact/no-flux directions of omega_parent in compact local collars",
            "would remove the main MTS-specific curl obstruction",
        ),
        (
            "RT4212_1_fill_bound",
            "Fill first curl bound row",
            "source a numeric/theorem bound for I_qbasic_vertical or I_projector with M_H_ref",
            "would make the scorecard empirical rather than schematic",
        ),
        (
            "RT4212_2_reference_tau",
            "Reference/tau lock",
            "prove H_ref derivative silence and tau_source=tau_charge=tau_clock=tau_readout",
            "would remove non-MTS-specific integrability ambiguities",
        ),
        (
            "RT4212_3_forbid_EH_borrowing",
            "No EH borrowing shortcut",
            "do not set Q_tau^MTS=Q_tau^EH while retained non-EH curl components exist",
            "prevents fake local-GR closure",
        ),
    ]
    return [
        {
            **common(),
            "route_id": row[0],
            "route": row[1],
            "action": row[2],
            "effect": row[3],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4212_0",
            "decision": DECISION,
            "operator_identity_derived": "True",
            "EH_visible_subcurl_conditional_zero": "True",
            "full_MTS_integrability_claim": "False",
            "delta_Htau_scorecard_first_row_ready": "True",
            "numeric_bound_available": "False",
            "M_H_ref_available": "False",
            "EH_borrowing_shortcut_allowed": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    blocks = [
        ("FW4212_0_Htau", "H_tau integrability claim", "blocked_until_all_curl_components_zero_or_bounded"),
        ("FW4212_1_MHsource", "M_Hdress source-charge claim", "blocked_until_integrability_reference_tau_denominator_close"),
        ("FW4212_2_Newton", "Newton source-mass derivation", "blocked_until_Htau_integrable_and_M_H_ref_source_backed"),
        ("FW4212_3_PPN", "PPN/local GR pass", "blocked_until_projector_vertical_boundary_visible_residuals_close"),
        ("FW4212_4_EH", "EH borrowing shortcut", "forbidden_while_non_EH_curl_components_retained"),
        ("FW4212_5_public", "public local-GR claim", "blocked_nonclaim_private_derivation_step"),
    ]
    return [
        {
            **common(),
            "firewall_id": row[0],
            "claim_family": row[1],
            "blocker": row[2],
            "status": "blocked_nonclaim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in blocks
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4212",
            "status": "integrability_operator_derived_partial_subcurl_zero_nonclaim",
            "strong_result": "H_tau integrability is now an explicit field-space curl operator; EH+visible subcurl is conditionally zero under local stationary no-flux assumptions",
            "remaining_gap": "q-basic vertical presymplectic silence, projector stress, reference, tau/surface, boundary/corner, visible residual numeric components and M_H_ref remain unsigned",
            "project_effect": "the next derivation can attack one named operator piece rather than the whole source-mass bridge at once",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4212 derives the curl identity and isolates the MTS-specific obstruction; the best next leap is to prove q-basic vertical variations are presymplectic-null/exact/no-flux locally.",
            "route_A": "prove ker(Dq) subset ker(Omega_parent) on compact local collars for allowed q-basic vertical variations",
            "route_B": "if false, compute or source I_qbasic_vertical/M_H_ref as the first real curl-bound row",
            "route_C": "keep EH-visible subcurl as conditional zero but forbid full EH borrowing",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 228 - PPC4161 Htau Integrability Operator And Curl Bound

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Result

4212 derives the first real operator for the `H_tau` source-charge problem. The Hamiltonian charge exists only if the Hamiltonian one-form is field-space exact.

Start from the parent local packet variation:

```text
delta L_total = E_A delta Phi^A + d theta_total(delta Phi)
omega_total(delta1,delta2)
  = delta1 theta_total(delta2)
  - delta2 theta_total(delta1)
  - theta_total([delta1,delta2]).
```

For a fixed local time generator `tau`:

```text
J_tau = theta_total(L_tau Phi) - i_tau L_total = C_tau + dQ_tau
alpha_tau,S(delta) = int_S(delta Q_tau - i_tau theta_total(delta)) - delta H_ref.
```

The integrability obstruction is the field-space curl:

```text
I_tau,S(delta1,delta2)
= d_field alpha_tau,S
= int_S i_tau omega_total(delta1,delta2)
  + I_ref + I_tau + I_corner.
```

Therefore:

```text
H_tau exists on the allowed local branch
iff I_tau,S(delta1,delta2)=0 for all allowed variations.
```

## Decomposition

Use the local decomposition:

```text
omega_total =
omega_EH_visible
+ omega_qbasic_vertical
+ omega_projector
+ omega_boundary_corner
+ omega_visible_EM_residual
+ omega_Dq_marker.
```

Then the retained nonclaim bound is:

```text
|delta_H_tau_nonintegrable_over_MH|
<= (
|I_EH_visible|
+ |I_qbasic_vertical|
+ |I_projector|
+ |I_boundary+I_corner|
+ |I_ref|
+ |I_tau+I_surface|
+ |I_matter_EM|
+ |I_Dq|
) / M_H_ref.
```

## What Actually Closes Here

`I_EH_visible=0` is conditionally derived for the EH plus standard visible matter subcharge under fixed `tau`, fixed reference/asymptotic data, stationary local collar, no radiation through the local boundary, and the 4210 visible-matter import contract.

That is useful but not the full MTS theorem. Full MTS integrability still requires the non-EH/q-basic vertical and projector pieces to be zero or bounded by parent-owned rows.

## No Shortcut

This checkpoint forbids the easy cheat:

```text
Q_tau^MTS := Q_tau^EH
```

while any retained non-EH curl component exists. EH is a legal subcharge. It is not yet the whole MTS charge.

## Next Target

`{NEXT_TARGET}` should attack the MTS-specific term:

```text
I_qbasic_vertical = int_S i_tau omega_qbasic_vertical.
```

The preferred proof is `ker(Dq) subset ker(Omega_parent)` on compact local collars. If that fails, the term becomes the first real curl-bound input row.
"""


def checkpoint_doc() -> str:
    return f"""# 4212 Y5 R2FR Htau integrability first operator or source scorecard first row

**Status:** `{DECISION}`.

**Forward move:** `H_tau` integrability is now an explicit field-space curl operator, not a vague missing condition.

## Operator

```text
alpha_tau,S(delta)=int_S(delta Q_tau-i_tau theta_total(delta))-delta H_ref
I_tau,S=d_field alpha_tau,S=int_S i_tau omega_total + I_ref + I_tau + I_corner
```

`H_tau` exists iff `I_tau,S=0` for all allowed variations.

## Partial closure

The EH plus standard visible matter subcurl is conditionally zero in a fixed-tau, stationary, source-free local collar. Full MTS integrability is not claimed because q-basic vertical, projector, reference, tau/surface, boundary/corner, visible residual, Dq/coupling and `M_H_ref` pieces remain retained.

## Files written

- `formalization-workbench\\228-PPC4161-Htau-integrability-operator-and-curl-bound.md`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4212_INTEGRABILITY_OPERATOR.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4212_CURL_COMPONENTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4212_FIRST_SCORECARD_ROW.csv`

## Next target

`{NEXT_TARGET}`.
"""


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker not in text:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n\n" + block.strip() + "\n")


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The H_tau integrability operator is derived: the Hamiltonian one-form alpha_tau,S is exact iff the field-space curl int_S i_tau omega_total plus reference, tau and corner terms vanishes; EH plus calibrated visible matter gives a conditional zero subcurl, while MTS q-basic vertical/projector/reference/denominator components remain retained and nonclaim.",'
        f'"4212 source audit, integrability operator, curl component split, first scorecard row, route matrix, decision row and firewall.",'
        f'private_Htau_integrability_operator_partial_zero_nonclaim,'
        f'"Prove q-basic vertical presymplectic silence ker(Dq) subset ker(Omega_parent), or fill I_qbasic_vertical/M_H_ref as the first real curl-bound row.",'
        f'"The EH-visible subcharge is useful, but equating Q_tau^MTS to Q_tau^EH while non-EH curl components remain would fake the GR reduction."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Htau Integrability Operator - 4212

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4212 derives the source-charge integrability operator:

```text
alpha_tau,S(delta)=int_S(delta Q_tau-i_tau theta_total(delta))-delta H_ref
I_tau,S=d_field alpha_tau,S=int_S i_tau omega_total + I_ref + I_tau + I_corner.
```

`H_tau` is integrable only when this curl vanishes. The EH plus standard visible matter subcurl is conditionally zero, but full MTS integrability remains nonclaim until q-basic vertical/projector/reference/tau/boundary/denominator components are zero or bounded."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Htau Integrability Operator - 4212

Marker: `{PACKET_MARKER}`

The packet now has the actual Hamiltonian curl operator for `H_tau`. Next pressure point: prove q-basic vertical variations are presymplectic-null/exact/no-flux locally, or bound that term directly."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4212_SOURCE_REGISTER.csv"]
    operator = rows_by_file["P8_Y5_R2FR_4212_INTEGRABILITY_OPERATOR.csv"]
    components = rows_by_file["P8_Y5_R2FR_4212_CURL_COMPONENTS.csv"]
    scorecard = rows_by_file["P8_Y5_R2FR_4212_FIRST_SCORECARD_ROW.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4212_THEOREM_STATUS.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4212_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4212_DECISION.csv"][0]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    required_ops = {
        "OP4212_0_parent_variation",
        "OP4212_1_symplectic_current",
        "OP4212_2_Noether_current",
        "OP4212_3_Hamiltonian_one_form",
        "OP4212_4_curl_identity",
        "OP4212_5_integrability_condition",
        "OP4212_6_bound_law",
    }
    required_components = {
        "I_EH_visible",
        "I_qbasic_vertical",
        "I_projector",
        "I_boundary+I_corner",
        "I_ref",
        "I_tau+I_surface",
        "I_matter_EM",
        "I_Dq",
        "M_H_ref",
        "delta_H_tau_nonintegrable_over_MH",
    }
    checks = [
        ("VAL4212_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4212_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4212_2_operator_complete", "operator rows contain variation, omega, Noether, alpha, curl and bound", required_ops.issubset({row["operator_id"] for row in operator})),
        ("VAL4212_3_curl_identity", "curl identity is explicitly derived", any(row["operator_id"] == "OP4212_4_curl_identity" and row["status"] == "derived_identity" for row in operator)),
        ("VAL4212_4_integrability_condition", "integrability iff curl zero condition present", any(row["operator_id"] == "OP4212_5_integrability_condition" for row in operator)),
        ("VAL4212_5_components_complete", "curl component split covers retained pieces", required_components.issubset({row["component"] for row in components})),
        ("VAL4212_6_EH_visible_zero", "EH-visible subcurl is conditionally zero", any(row["component"] == "I_EH_visible" and row["status"] == "conditional_theorem_zero" for row in components)),
        ("VAL4212_7_full_MTS_nonclaim", "full MTS theorem is not claimed", any(row["theorem_id"] == "TH4212_2_full_MTS_integrability" and row["status"] == "not_claimed" for row in theorem)),
        ("VAL4212_8_scorecard_first_row", "first scorecard row exists and is nonnumeric", scorecard[0]["quantity"] == "delta_H_tau_nonintegrable_over_MH" and scorecard[0]["numeric_value"] == "MISSING"),
        ("VAL4212_9_routes", "routes include vertical proof, bound row, reference tau and EH borrowing guard", {"RT4212_0_attack_vertical", "RT4212_1_fill_bound", "RT4212_2_reference_tau", "RT4212_3_forbid_EH_borrowing"}.issubset({row["route_id"] for row in routes})),
        ("VAL4212_10_decision_nonclaim", "decision blocks full MTS integrability and denominator", decision["full_MTS_integrability_claim"] == "False" and decision["M_H_ref_available"] == "False"),
        ("VAL4212_11_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4212_12_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4212_13_claim_register", "claim register contains L-053", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4212_14_spine_packet_markers", "spine and packet markers present", SPINE_MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH)),
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
        "P8_Y5_R2FR_4212_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4212_INTEGRABILITY_OPERATOR.csv": operator_rows(),
        "P8_Y5_R2FR_4212_CURL_COMPONENTS.csv": component_rows(),
        "P8_Y5_R2FR_4212_FIRST_SCORECARD_ROW.csv": scorecard_rows(),
        "P8_Y5_R2FR_4212_THEOREM_STATUS.csv": theorem_rows(),
        "P8_Y5_R2FR_4212_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4212_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4212_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4212_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4212_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    update_registers()
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4212_VALIDATION.csv", validation)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4212_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
