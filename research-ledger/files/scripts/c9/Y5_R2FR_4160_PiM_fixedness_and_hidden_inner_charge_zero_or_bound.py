from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4160-Y5-R2FR-PiM-fixedness-and-hidden-inner-charge-zero-or-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_PIM_FIXEDNESS_HIDDEN_INNER_4160"
CHECKPOINT_ID = "4160"
DECISION = "PIM_FIXEDNESS_AND_HIDDEN_INNER_CHARGE_COLLAPSE_DERIVED_CONDITIONALLY_PACKET_ADOPTION_UNSIGNED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4160_00_4159_doc": (
        ROOT / "4159-Y5-R2FR-inner-Gauss-charge-matching-or-epsilon-kernel-bound.md",
        "Prove `delta Pi_M^C=0`",
        "4159 handoff to PiM fixedness and hidden inner charge.",
    ),
    "SRC4160_01_4159_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4159_NEXT_TARGET.csv",
        "delta Pi_M^C=0 and Phi_hidden_inner=0",
        "4159 machine-readable next target.",
    ),
    "SRC4160_02_4159_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4159_INNER_GAUSS_MATCH_THEOREM.csv",
        "HILBERT_INNER_CHARGE_ZERO_IF_PIM_FIXED",
        "4159 reduction to PiM fixedness plus hidden inner charge.",
    ),
    "SRC4160_03_4159_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4159_EPSILON_KERNEL_BOUND_ROWS.csv",
        "epsilon_Pi_inner",
        "4159 epsilon_kernel component bound rows.",
    ),
    "SRC4160_04_4156_glue": (
        SOURCE_DIR / "P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE.csv",
        "CMG4156_1_constraint_pushforward",
        "Pi_M^C defined as parent constraint-map pushforward.",
    ),
    "SRC4160_05_4156_gates": (
        SOURCE_DIR / "P8_Y5_R2FR_4156_ZERO_THEOREM_GATES.csv",
        "ZG4156_1_commutator",
        "Pi_M fixed chain-map gate.",
    ),
    "SRC4160_06_4061_domain": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_DOMAIN_PROJECTOR_KERNEL_THEOREM.csv",
        "DOM4061_0_q_basic_projector",
        "Domain/projector q-basic fixed branch.",
    ),
    "SRC4160_07_4043_domain": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_SELECTED_BRANCH_ZERO_THEOREM.csv",
        "PZS4043_0_selected_signature",
        "Selected domain/projector no-stress theorem.",
    ),
    "SRC4160_08_4061_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_BOUNDARY_REFERENCE_KERNEL_THEOREM.csv",
        "BND4061_3_result",
        "Boundary/reference kernel zero selected branch.",
    ),
    "SRC4160_09_4038_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv",
        "PNT4038_4_result",
        "Poynting residual zero in selected stationary local branch.",
    ),
    "SRC4160_10_4155_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_FLUX_ZERO_OR_BOUND.csv",
        "FZ4155_2_radiative_bound",
        "Radiative/nonstationary EM fallback bound.",
    ),
    "SRC4160_11_4056_packet": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_LOCAL_PARENT_ACTION_PACKET.csv",
        "LAP4056_6_boundary_projector_memory",
        "Candidate local packet side-channel clause.",
    ),
    "SRC4160_12_4056_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_PACKET_ADOPTION_GATE.csv",
        "ADOPT4056_4_side_channels",
        "Packet adoption gate for side-channel silence.",
    ),
    "SRC4160_13_script": (
        SCRIPT_PATH,
        DECISION,
        "This generator records the 4160 PiM/hidden-inner collapse attempt.",
    ),
}


def common() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def write_csv(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4160_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4160_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4160_PIM_FIXEDNESS_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4160_PIM_FIXEDNESS_THEOREM.csv",
        "P8_Y5_R2FR_4160_HIDDEN_INNER_CHARGE_VECTOR": SOURCE_DIR / "P8_Y5_R2FR_4160_HIDDEN_INNER_CHARGE_VECTOR.csv",
        "P8_Y5_R2FR_4160_EPSILON_KERNEL_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4160_EPSILON_KERNEL_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4160_FIRST_ORDER_COLLAPSE_GATE": SOURCE_DIR / "P8_Y5_R2FR_4160_FIRST_ORDER_COLLAPSE_GATE.csv",
        "P8_Y5_R2FR_4160_NEWTON_IMPACT": SOURCE_DIR / "P8_Y5_R2FR_4160_NEWTON_IMPACT.csv",
        "P8_Y5_R2FR_4160_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4160_STATUS.csv",
        "P8_Y5_R2FR_4160_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4160_NEXT_TARGET.csv",
    }


def source_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        text = read_text(path) if exists and path.is_file() else ""
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "role": role,
                "exists": str(exists),
                "needle_found": str(bool(exists and needle in text)),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def pim_fixedness_rows() -> List[dict]:
    return [
        {
            **common(),
            "theorem_id": "PF4160_0_definition",
            "claim_piece": "Pi_M^C definition",
            "formula": "Pi_M^C := D_N[C_tau]_{L_ext,B_ext,Sigma_ext,tau,frame,units}|_{J_H[tau]}",
            "derivation": "Pi_M^C is not a fitted mass mask; it is the parent constraint Dirichlet-to-Neumann/boundary-charge map with its operator, boundary package, domain and readout frame specified.",
            "result": "PIM_AS_PARENT_MAP_RESTATED",
            "proof_status": "definition_from_4156",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "PF4160_1_variation",
            "claim_piece": "fixedness variation",
            "formula": "delta Pi_M^C = Pi_L[delta L_ext]+Pi_B[delta B_ext]+Pi_D[delta Sigma_ext]+Pi_tau[delta tau]+Pi_f[delta frame,delta units]+Pi_ro[delta readout]",
            "derivation": "The only allowed same-source variation of Pi_M^C comes from changing the parent map itself. If all map-defining data are fixed before readout, the projector variation vanishes.",
            "result": "PIM_VARIATION_DECOMPOSITION_DERIVED",
            "proof_status": "formal_map_differential",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "PF4160_2_zero",
            "claim_piece": "Pi_M fixedness theorem",
            "formula": "delta L_ext=delta B_ext=delta Sigma_ext=delta tau=delta frame=delta units=delta readout=0 => delta Pi_M^C=0",
            "derivation": "Under the selected single-packet local branch, operator, boundary/reference, domain/projector, generator, frame/units and readout firewall are parent-owned, so Pi_M^C cannot wiggle between same-source solutions.",
            "result": "PIM_FIXEDNESS_ZERO_CONDITIONAL",
            "proof_status": "conditional_packet_unsigned",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "PF4160_3_commutator",
            "claim_piece": "chain-map consequence",
            "formula": "delta Pi_M^C=0 and [d,Pi_M^C]=0 => d(Pi_M^C J_H)=Pi_M^C dJ_H",
            "derivation": "Fixedness removes same-source projector leakage; chain-map ownership removes the projected-current commutator already isolated in 4156.",
            "result": "PIM_CHAINMAP_COLLAPSE_CONDITIONAL",
            "proof_status": "conditional_on_4156_chainmap_gate",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "PF4160_4_bound",
            "claim_piece": "projector fallback",
            "formula": "epsilon_Pi_inner <= |Pi_L delta L|+|Pi_B delta B|+|Pi_D delta Sigma|+|Pi_tau delta tau|+|Pi_f delta frame_units|+|Pi_ro delta readout| normalized by M_H_ref",
            "derivation": "If fixedness is not adopted, every way Pi_M can move becomes a no-cancellation bound component rather than a hidden fitted source normalization.",
            "result": "PIM_BOUND_VECTOR_READY_VALUES_MISSING",
            "proof_status": "bound_ready_not_score_ready",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def hidden_inner_rows() -> List[dict]:
    return [
        {
            **common(),
            "hidden_id": "HI4160_0_split",
            "channel": "total hidden inner charge",
            "formula": "Phi_hidden_inner=Phi_boundary+Phi_domain+Phi_symp+Phi_EM_extra+Phi_incoming+Phi_rest",
            "zero_route": "each channel is zero by parent packet adoption or kept as a bound component",
            "current_status": "SPLIT_DERIVED",
            "residual_if_failed": "epsilon_hidden_inner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "hidden_id": "HI4160_1_boundary",
            "channel": "boundary/reference/corner",
            "formula": "Phi_boundary=0 if source-blind GHY/exact/topological boundary and fixed H_ref/no-flux collar are adopted",
            "zero_route": "4038/4061 selected boundary branch",
            "current_status": "CONDITIONAL_SELECTED_BRANCH_NOT_PACKET_SIGNED",
            "residual_if_failed": "epsilon_boundary_inner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "hidden_id": "HI4160_2_domain",
            "channel": "domain/projector/wall",
            "formula": "Phi_domain=0 if q-basic fixed domain/projector, no wall flux and no source support refit",
            "zero_route": "4043/4061 selected domain branch",
            "current_status": "CONDITIONAL_SELECTED_BRANCH_NOT_PACKET_SIGNED",
            "residual_if_failed": "epsilon_domain_inner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "hidden_id": "HI4160_3_EM",
            "channel": "nonminimal or radiative EM",
            "formula": "Phi_EM_extra=0 for minimal stationary bound EM already inside J_H_total; radiative/nonminimal leakage is bounded separately",
            "zero_route": "4038/4155 Poynting once-only and no-flux branch",
            "current_status": "CONDITIONAL_SELECTED_BRANCH_NOT_PACKET_SIGNED",
            "residual_if_failed": "epsilon_EM_extra_inner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "hidden_id": "HI4160_4_symp",
            "channel": "symplectic/corner/H_tau curl",
            "formula": "Phi_symp=0 if H_tau one-form is exact and corner/reference curl terms vanish",
            "zero_route": "4156 H_tau integrability gate",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_if_failed": "epsilon_symp_inner; C_curl",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "hidden_id": "HI4160_5_incoming",
            "channel": "incoming/free monopole",
            "formula": "Phi_incoming=0 if the local reset excludes externally supplied source-free Schwarzschild/Newton mass modes",
            "zero_route": "no-incoming local reset certificate",
            "current_status": "UNSIGNED",
            "residual_if_failed": "epsilon_incoming_mass",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "hidden_id": "HI4160_6_result",
            "channel": "hidden inner charge result",
            "formula": "all hidden channels zero => Phi_hidden_inner=0",
            "zero_route": "single parent packet adoption plus H_tau integrability plus no-incoming certificate",
            "current_status": "CONDITIONAL_COLLAPSE_PACKET_UNSIGNED",
            "residual_if_failed": "epsilon_hidden_inner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[dict]:
    return [
        {
            **common(),
            "bound_id": "EK4160_0_Pi",
            "quantity": "epsilon_Pi_inner",
            "formula": "epsilon_Pi_inner <= epsilon_Pi_operator + epsilon_Pi_boundary + epsilon_Pi_domain + epsilon_Pi_tau + epsilon_Pi_frame_units + epsilon_Pi_readout",
            "current_value": "FORMULA_READY_COMPONENT_VALUES_MISSING",
            "needed_source": "operator/boundary/domain/tau/frame/readout fixedness certificate or numeric bounds",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "EK4160_1_hidden",
            "quantity": "epsilon_hidden_inner",
            "formula": "epsilon_hidden_inner <= epsilon_boundary_inner + epsilon_domain_inner + epsilon_symp_inner + epsilon_EM_extra_inner + epsilon_incoming_mass + epsilon_rest_inner",
            "current_value": "FORMULA_READY_COMPONENT_VALUES_MISSING",
            "needed_source": "side-channel zero certificates or source-backed bounds",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "EK4160_2_total",
            "quantity": "epsilon_kernel_4160",
            "formula": "epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch",
            "current_value": "BOUND_FORMULA_READY_VALUES_MISSING",
            "needed_source": "PiM fixedness/bound, hidden charge bound, same surface/tau/frame/units bound",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def collapse_gate_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "CG4160_0_conditional_collapse",
            "statement": "first-order homogeneous kernel collapse",
            "formula": "delta J_H_total=0; delta Pi_M^C=0; Phi_hidden_inner=0; same S/tau/frame/units; outer ref fixed => a_hom=0",
            "result": "FIRST_ORDER_KERNEL_COLLAPSE_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "CG4160_1_not_live",
            "statement": "why not live",
            "formula": "packet adoption, H_tau integrability and no-incoming certificate are not fully parent-signed",
            "result": "PUBLIC_LOCAL_GR_CLAIM_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "CG4160_2_next",
            "statement": "next sharp target",
            "formula": "adopt local parent packet clauses as one action theorem or source numeric bounds for EK4160_0..2",
            "result": "NEXT_PACKET_ADOPTION_OR_NUMERIC_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def impact_rows() -> List[dict]:
    return [
        {
            **common(),
            "impact_id": "IMP4160_0_source",
            "component": "source coupling",
            "result": "SOURCE_COUPLING_GAP_REDUCED_TO_PARENT_PACKET_ADOPTION",
            "meaning": "the first-order kernel no longer needs an unspecified coupling if the local packet fixes Pi_M and hidden channels",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4160_1_Newton",
            "component": "Newton",
            "result": "CONDITIONAL_FIRST_ORDER_NEWTON_SOURCE_NORMALIZATION_PATH",
            "meaning": "with same J_H_total, fixed Pi_M, zero hidden inner charge and 4158 outer reference, a_hom=0 conditionally",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4160_2_testing",
            "component": "empirical route",
            "result": "BOUND_RUNNER_INPUTS_NOW_EXPLICIT",
            "meaning": "if packet adoption is rejected, epsilon_kernel is testable through named PiM, hidden and surface mismatch components",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "PiM_variation_decomposition_derived": "True",
            "PiM_fixedness_zero_conditional": "True",
            "hidden_inner_charge_split_derived": "True",
            "first_order_kernel_collapse_conditional": "True",
            "packet_adoption_parent_signed": "False",
            "Htau_integrability_parent_signed": "False",
            "no_incoming_monopole_signed": "False",
            "epsilon_kernel_bound_rows_emitted": "True",
            "numeric_epsilon_kernel_bound_populated": "False",
            "Newton_claimed": "False",
            "local_gr_claimed": "False",
            "next_target": "4161-Y5-R2FR-local-parent-packet-adoption-or-first-epsilon-kernel-score.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4160_0",
            "target_doc": "4161-Y5-R2FR-local-parent-packet-adoption-or-first-epsilon-kernel-score.md",
            "target_script": "scripts/Y5_R2FR_4161_local_parent_packet_adoption_or_first_epsilon_kernel_score.py",
            "objective": "turn the selected 4038/4043/4054/4056/4061/4155 branches into one formally adopted local parent packet, or populate the first source-backed epsilon_kernel score row",
            "success_gate": "one action packet signs PiM fixedness, hidden inner charge silence, H_tau integrability and no-incoming/no-backfill clauses; otherwise EK4160 component rows receive source-backed numeric/bound values",
            "reason": "4160 derives the conditional first-order kernel collapse; the remaining blocker is not algebra but formal packet adoption or quantitative bounds.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4160 - PiM Fixedness And Hidden Inner Charge Zero Or Bound

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4159 reduced the homogeneous kernel problem to:

`epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch`.

4160 tries to collapse `epsilon_Pi_inner` and `epsilon_hidden_inner`.

## Pi_M Fixedness
Use the non-circular definition:

`Pi_M^C := D_N[C_tau]_{{L_ext,B_ext,Sigma_ext,tau,frame,units}}|_{{J_H[tau]}}`.

Its same-source variation decomposes as:

`delta Pi_M^C = Pi_L[delta L_ext]+Pi_B[delta B_ext]+Pi_D[delta Sigma_ext]+Pi_tau[delta tau]+Pi_f[delta frame,delta units]+Pi_ro[delta readout]`.

Therefore:

`delta L_ext=delta B_ext=delta Sigma_ext=delta tau=delta frame=delta units=delta readout=0 => delta Pi_M^C=0`.

This is not an assumption that the projector is quiet. It is the exact contract the parent packet must satisfy.

## Hidden Inner Charge
The hidden inner flux splits as:

`Phi_hidden_inner=Phi_boundary+Phi_domain+Phi_symp+Phi_EM_extra+Phi_incoming+Phi_rest`.

Selected branches already stage conditional zeros:

- `Phi_boundary=0` from source-blind boundary/reference plus fixed `H_ref` and no-flux collar;
- `Phi_domain=0` from q-basic fixed domain/projector and no wall flux;
- `Phi_EM_extra=0` for minimal stationary bound EM already inside `J_H_total`;
- `Phi_symp=0` only if `H_tau` integrability/corner terms are signed;
- `Phi_incoming=0` only if a no-incoming/free-monopole certificate is signed.

So:

`Phi_hidden_inner=0`

is conditionally derivable under one adopted local parent packet plus `H_tau` integrability and no-incoming clauses.

## Conditional First-Order Collapse
Combining 4158, 4159 and 4160:

`delta J_H_total=0; delta Pi_M^C=0; Phi_hidden_inner=0; same S/tau/frame/units; outer ref fixed => a_hom=0`.

That gives a conditional first-order Newton source-normalization route. It is still not a public local-GR claim because packet adoption, `H_tau` integrability and no-incoming are not fully parent-signed.

## Bound Fallback
If the packet is not adopted, keep:

`epsilon_Pi_inner <= epsilon_Pi_operator + epsilon_Pi_boundary + epsilon_Pi_domain + epsilon_Pi_tau + epsilon_Pi_frame_units + epsilon_Pi_readout`,

`epsilon_hidden_inner <= epsilon_boundary_inner + epsilon_domain_inner + epsilon_symp_inner + epsilon_EM_extra_inner + epsilon_incoming_mass + epsilon_rest_inner`,

and

`epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch`.

No component is score-ready yet without source-backed values.

## Verdict
This is the best current local-GR route:

1. same source kills the Hilbert part;
2. fixed parent `Pi_M^C` kills projector leakage;
3. hidden inner channels vanish if the selected local packet is adopted;
4. 4158 then kills `a_hom`.

The remaining work is formal packet adoption or first numeric `epsilon_kernel` scoring.

## Outputs
- `{outputs["P8_Y5_R2FR_4160_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4160_PIM_FIXEDNESS_THEOREM"]}`
- `{outputs["P8_Y5_R2FR_4160_HIDDEN_INNER_CHARGE_VECTOR"]}`
- `{outputs["P8_Y5_R2FR_4160_EPSILON_KERNEL_BOUND_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4160_FIRST_ORDER_COLLAPSE_GATE"]}`
- `{outputs["P8_Y5_R2FR_4160_NEWTON_IMPACT"]}`
- `{outputs["P8_Y5_R2FR_4160_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4160_NEXT_TARGET"]}`

## Next Target
- `4161-Y5-R2FR-local-parent-packet-adoption-or-first-epsilon-kernel-score.md`
- Either adopt the selected local parent packet as one formal action theorem, or populate source-backed `epsilon_kernel` component bounds.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4160_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4160_PIM_FIXEDNESS_THEOREM"], pim_fixedness_rows())
    write_csv(outputs["P8_Y5_R2FR_4160_HIDDEN_INNER_CHARGE_VECTOR"], hidden_inner_rows())
    write_csv(outputs["P8_Y5_R2FR_4160_EPSILON_KERNEL_BOUND_ROWS"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4160_FIRST_ORDER_COLLAPSE_GATE"], collapse_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4160_NEWTON_IMPACT"], impact_rows())
    write_csv(outputs["P8_Y5_R2FR_4160_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4160_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, requirement: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "requirement": requirement,
                "passed": str(bool(passed)),
                "detail": detail,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    add(
        "VAL4160_0_sources",
        "all cited source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']} exists={row['exists']} needle={row['needle_found']}" for row in sources),
    )

    csv_ok = True
    csv_detail: List[str] = []
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            csv_detail.append(f"{name}:{len(rows)}")
            csv_ok = csv_ok and bool(rows)
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{name}:ERR {exc!r}")
    add("VAL4160_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "delta Pi_M^C = Pi_L[delta L_ext]",
        "Phi_hidden_inner=Phi_boundary+Phi_domain+Phi_symp+Phi_EM_extra+Phi_incoming+Phi_rest",
        "delta J_H_total=0; delta Pi_M^C=0; Phi_hidden_inner=0",
        "epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch",
        "4161-Y5-R2FR-local-parent-packet-adoption-or-first-epsilon-kernel-score.md",
    ]
    add("VAL4160_2_doc_tokens", "document records PiM variation, hidden split, collapse theorem, bounds and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    pim_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4160_PIM_FIXEDNESS_THEOREM"]))
    pim_tokens = ["PIM_AS_PARENT_MAP_RESTATED", "PIM_VARIATION_DECOMPOSITION_DERIVED", "PIM_FIXEDNESS_ZERO_CONDITIONAL", "PIM_CHAINMAP_COLLAPSE_CONDITIONAL", "PIM_BOUND_VECTOR_READY_VALUES_MISSING"]
    add("VAL4160_3_pim", "PiM theorem rows derive fixedness and fallback vector", all(token in pim_text for token in pim_tokens), "PiM tokens checked")

    hidden_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4160_HIDDEN_INNER_CHARGE_VECTOR"]))
    hidden_tokens = ["SPLIT_DERIVED", "epsilon_boundary_inner", "epsilon_domain_inner", "epsilon_EM_extra_inner", "epsilon_symp_inner", "epsilon_incoming_mass", "CONDITIONAL_COLLAPSE_PACKET_UNSIGNED"]
    add("VAL4160_4_hidden", "hidden charge rows split boundary, domain, EM, symp and incoming channels", all(token in hidden_text for token in hidden_tokens), "hidden tokens checked")

    bounds_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4160_EPSILON_KERNEL_BOUND_ROWS"]))
    bound_tokens = ["epsilon_Pi_inner", "epsilon_hidden_inner", "epsilon_kernel_4160", "BOUND_FORMULA_READY_VALUES_MISSING"]
    add("VAL4160_5_bounds", "bound rows retain PiM, hidden and total epsilon_kernel components", all(token in bounds_text for token in bound_tokens), "bound tokens checked")

    collapse_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4160_FIRST_ORDER_COLLAPSE_GATE"]))
    collapse_tokens = ["FIRST_ORDER_KERNEL_COLLAPSE_CONDITIONAL", "PUBLIC_LOCAL_GR_CLAIM_BLOCKED", "NEXT_PACKET_ADOPTION_OR_NUMERIC_BOUND"]
    add("VAL4160_6_collapse", "collapse gate records conditional first-order route and no live claim", all(token in collapse_text for token in collapse_tokens), "collapse tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4160_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("PiM_variation_decomposition_derived") == "True"
        and status[0].get("PiM_fixedness_zero_conditional") == "True"
        and status[0].get("hidden_inner_charge_split_derived") == "True"
        and status[0].get("first_order_kernel_collapse_conditional") == "True"
        and status[0].get("packet_adoption_parent_signed") == "False"
        and status[0].get("numeric_epsilon_kernel_bound_populated") == "False"
        and status[0].get("Newton_claimed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4160_7_status", "status records conditional collapse, unsigned packet and no Newton/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4160_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4161-Y5-R2FR-local-parent-packet-adoption-or-first-epsilon-kernel-score.md"
    add("VAL4160_8_next", "next target is packet adoption or first epsilon_kernel score", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4160_9_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4160-Y5-R2FR" in item.name or "R2FR_4160" in item.name or "P8_Y5_R2FR_4160" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4160_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4160_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4160_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
