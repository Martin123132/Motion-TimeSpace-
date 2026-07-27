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
DOC_PATH = ROOT / "4156-Y5-R2FR-PiM-Htau-same-charge-glue-or-radial-source-residual.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_PIM_HTAU_SAME_CHARGE_GLUE_4156"
CHECKPOINT_ID = "4156"
DECISION = "PIM_HTAU_SAME_CHARGE_GLUE_REDUCED_TO_PARENT_CONSTRAINT_MAP_KERNEL_UNSIGNED_RADIAL_RESIDUAL_ROWS_READY"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4156_00_4155_doc": (
        ROOT / "4155-Y5-R2FR-worldtube-Hilbert-source-measure-and-Poynting-flux-lock.md",
        "Pi_M/H_tau glue",
        "4155 handoff to Pi_M/H_tau same-charge glue.",
    ),
    "SRC4156_01_4155_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_NEXT_TARGET.csv",
        "same parent source charge",
        "Machine-readable 4155 next-target row.",
    ),
    "SRC4156_02_4012_charge": (
        SOURCE_DIR / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv",
        "CHG4012_4_same_charge_equality",
        "Recent PiM/Htau charge lock theorem.",
    ),
    "SRC4156_03_3941_map": (
        SOURCE_DIR / "P8_Y5_R2FR_3941_PIM_HTAU_MAP_DERIVATION.csv",
        "MAP3941_2_constraint_pushforward",
        "Constructive parent constraint map route.",
    ),
    "SRC4156_04_3911_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_3911_PIM_HTAU_COMBINED_ZERO_OR_BOUND.csv",
        "COM3911_1_double_zero_branch",
        "Combined PiM/Htau zero-or-bound result.",
    ),
    "SRC4156_05_3532_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_3532_PIM_HTAU_ZERO_PROOF.csv",
        "ZP3532_1_RPiM_no_GM_laundering",
        "Earlier no-GM-laundering zero proof attempt.",
    ),
    "SRC4156_06_worldtube": (
        SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "T510_2_MTS_transfer_condition",
        "Worldtube source measure transfer theorem.",
    ),
    "SRC4156_07_4155_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_STATUS.csv",
        "PiM_Htau_same_charge_glue_signed",
        "4155 status naming same-charge glue as unsigned.",
    ),
    "SRC4156_08_script": (
        SCRIPT_PATH,
        "PIM_HTAU_SAME_CHARGE_GLUE_REDUCED_TO_PARENT_CONSTRAINT_MAP",
        "This generator records the 4156 PiM/Htau glue attempt.",
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
        "P8_Y5_R2FR_4156_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4156_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE": SOURCE_DIR / "P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE.csv",
        "P8_Y5_R2FR_4156_ZERO_THEOREM_GATES": SOURCE_DIR / "P8_Y5_R2FR_4156_ZERO_THEOREM_GATES.csv",
        "P8_Y5_R2FR_4156_RESIDUAL_VECTOR": SOURCE_DIR / "P8_Y5_R2FR_4156_RESIDUAL_VECTOR.csv",
        "P8_Y5_R2FR_4156_RADIAL_SOURCE_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4156_RADIAL_SOURCE_ROWS.csv",
        "P8_Y5_R2FR_4156_NEWTON_IMPACT": SOURCE_DIR / "P8_Y5_R2FR_4156_NEWTON_IMPACT.csv",
        "P8_Y5_R2FR_4156_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4156_DECISION_GATES.csv",
        "P8_Y5_R2FR_4156_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4156_STATUS.csv",
        "P8_Y5_R2FR_4156_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4156_NEXT_TARGET.csv",
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


def constraint_map_rows() -> List[dict]:
    return [
        {
            **common(),
            "glue_id": "CMG4156_0_target",
            "statement": "same-charge target",
            "formula": "Delta_PiM := M_H[Pi_M J_H_total] - (H_tau[S_outer]-H_ref)",
            "derivation": "The equality to prove is source charge equals exterior Hamiltonian charge before orbital/readout calibration.",
            "result": "TARGET_DEFINED_NO_GM_LAUNDERING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "glue_id": "CMG4156_1_constraint_pushforward",
            "statement": "non-circular Pi_M construction",
            "formula": "Pi_M^C := D_N[C_tau]|_{J_H[tau]}",
            "derivation": "Pi_M is constructed from the parent constraint Dirichlet-to-Neumann/boundary-charge map, not from fitted orbital GM.",
            "result": "CONSTRUCTIVE_ROUTE_SELECTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "glue_id": "CMG4156_2_chainmap",
            "statement": "projected current closure",
            "formula": "d(Pi_M^C J_H)=Pi_M^C dJ_H + [d,Pi_M^C]J_H",
            "derivation": "If Pi_M^C is fixed by the parent exterior constraint map and commutes with d on the Hilbert current complex, the commutator source vanishes.",
            "result": "CHAINMAP_ZERO_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "glue_id": "CMG4156_3_Htau_integrability",
            "statement": "Hamiltonian one-form exactness",
            "formula": "alpha_tau[delta Phi]=int_S(delta Q_tau-i_tau Theta_total)-delta H_ref; d_field alpha_tau=0",
            "derivation": "H_tau is a true charge only if the covariant phase-space one-form is exact after corner/reference/extra flux terms are handled.",
            "result": "HTAU_INTEGRABILITY_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "glue_id": "CMG4156_4_same_charge",
            "statement": "same-charge equality condition",
            "formula": "Pi_M^C J_H = J_M_top + dB_zero and M_H[Pi_M^C J_H]=H_tau[S_outer]-H_ref",
            "derivation": "The same-charge theorem holds only if the constraint map is unique, homogeneous mass kernels vanish, exact terms have zero linked-surface flux, and extra/EM/boundary fluxes are owned.",
            "result": "SAME_CHARGE_THEOREM_DERIVED_CONDITIONAL_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def zero_gate_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "ZG4156_0_kernel",
            "gate": "constraint Green-map uniqueness",
            "formula": "R_kernel=0; no homogeneous 1/r mass mode independent of J_H_total",
            "current_status": "UNSIGNED",
            "residual_if_failed": "R_kernel; radial source residual",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "ZG4156_1_commutator",
            "gate": "Pi_M chain-map fixedness",
            "formula": "[d,Pi_M^C]J_H=0",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_if_failed": "I_commutator",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "ZG4156_2_curl",
            "gate": "H_tau integrability",
            "formula": "C_curl=int_S i_tau omega_MTS + corner_tau + reference_curl = 0",
            "current_status": "UNSIGNED",
            "residual_if_failed": "C_curl; corner_tau",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "ZG4156_3_reference",
            "gate": "reference subtraction fixed and q-basic",
            "formula": "D_X(H_ref)=0 and M_H_ref=Mbar_H_ref(q(Phi))",
            "current_status": "UNSIGNED",
            "residual_if_failed": "C_ref; C_M",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "ZG4156_4_surface",
            "gate": "linked surface/domain/frame/units fixed before readout",
            "formula": "D_X(S_outer,S_ref,tau,frame,units)=0",
            "current_status": "UNSIGNED",
            "residual_if_failed": "C_domain; C_frame; C_units",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "ZG4156_5_rest_flux",
            "gate": "extra, EM, boundary, symplectic fluxes owned or bounded",
            "formula": "R_extra=R_symp=R_boundary=R_EM_flux=0 or finite residual rows",
            "current_status": "PARTIAL_FROM_4155_EM_ONLY",
            "residual_if_failed": "R_extra; R_symp; R_boundary; R_EM_flux",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_vector_rows() -> List[dict]:
    return [
        {
            **common(),
            "residual_id": "RV4156_0_charge_glue",
            "quantity": "epsilon_charge_glue",
            "formula": "epsilon_charge <= |C_M|+|C_curl|+|I_commutator|+|R_eq|+|C_ref|+|C_frame|+|C_units|+|R_kernel|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|+|epsilon_G_norm|+|epsilon_PPN_source|",
            "status": "FINITE_CHARGE_GLUE_VECTOR_DERIVED_NONCLAIM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RV4156_1_no_cancellation",
            "quantity": "no cancellation credit",
            "formula": "each residual subfactor must be theorem-zero or bounded independently unless a parent identity proves cancellation",
            "status": "DISCIPLINE_LOCK",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RV4156_2_GM_laundering_guard",
            "quantity": "no fitted GM definition of Pi_M",
            "formula": "mu_obs=G_ref M_H_ref(1+epsilon_mu), not M_H_ref:=mu_obs/G_ref",
            "status": "NO_GM_LAUNDERING_GUARD",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def radial_rows() -> List[dict]:
    return [
        {
            **common(),
            "radial_id": "RS4156_0_linking_surface",
            "quantity": "partial_r M_H",
            "formula": "M_H(S2)-M_H(S1)=int_A d(Pi_M^C J_H)",
            "zero_condition": "chain-map fixedness, source-free annulus, no homogeneous mass kernel, no boundary/range flux",
            "status": "CONDITIONAL_RADIAL_ZERO_NOT_PARENT_SIGNED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "radial_id": "RS4156_1_kernel",
            "quantity": "homogeneous 1/r kernel",
            "formula": "R_kernel captures exterior mass mode not sourced by J_H_total",
            "zero_condition": "constraint Green-map uniqueness and reference boundary condition",
            "status": "KERNEL_ZERO_UNSIGNED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "radial_id": "RS4156_2_range_flux",
            "quantity": "radial/range source hair",
            "formula": "partial_r ln mu_obs = partial_r ln M_H + partial_r ln(1+epsilon_mu)",
            "zero_condition": "same-charge glue plus mu_extra channel locks",
            "status": "RETAIN_RADIAL_SOURCE_RESIDUAL",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def impact_rows() -> List[dict]:
    return [
        {
            **common(),
            "impact_id": "IMP4156_0_Newton",
            "component": "Newton source normalization",
            "result": "PIM_HTAU_ROUTE_CONSTRUCTED_NOT_CLOSED",
            "meaning": "source mass can be the same object as exterior charge if parent constraint-map gates close",
            "still_needed": "kernel zero, H_tau integrability, fixed reference/surfaces, rest flux silence",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4156_1_mu_extra",
            "component": "mu_extra",
            "result": "SOURCE_GLUE_NARROWED",
            "meaning": "some mu_extra/radial ambiguity becomes same-charge residual vector rather than vague missing coupling",
            "still_needed": "channel locks from 4154",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4156_2_PPN",
            "component": "PPN",
            "result": "NOT_CLOSED",
            "meaning": "even same-charge Newton source needs beta/gamma/source stability gates",
            "still_needed": "delta_beta_source and R11/Y6 stress cleanup",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DEC4156_0_route",
            "question": "best non-circular Pi_M route",
            "answer": "construct Pi_M from the parent constraint/boundary-charge map",
            "decision": "PARENT_CONSTRAINT_MAP_ROUTE_SELECTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4156_1_zero",
            "question": "is Pi_M/H_tau same-charge equality proved live?",
            "answer": "no, kernel/integrability/reference/surface/rest flux gates remain unsigned",
            "decision": "SAME_CHARGE_ZERO_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4156_2_next",
            "question": "best next target",
            "answer": "derive kernel-zero / no homogeneous mass mode for the parent constraint Green map",
            "decision": "NEXT_CONSTRAINT_KERNEL_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "constraint_map_route_selected": "True",
            "same_charge_theorem_derived_conditional": "True",
            "chainmap_zero_conditional": "True",
            "Htau_integrability_conditional": "True",
            "kernel_zero_parent_signed": "False",
            "reference_surface_frame_signed": "False",
            "rest_flux_silence_signed": "False",
            "radial_source_residual_rows_emitted": "True",
            "Newton_claimed": "False",
            "local_gr_claimed": "False",
            "next_target": "4157-Y5-R2FR-constraint-Green-kernel-zero-or-homogeneous-mass-residual.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4156_0",
            "target_doc": "4157-Y5-R2FR-constraint-Green-kernel-zero-or-homogeneous-mass-residual.md",
            "target_script": "scripts/Y5_R2FR_4157_constraint_Green_kernel_zero_or_homogeneous_mass_residual.py",
            "objective": "prove the parent exterior constraint map has no homogeneous 1/r mass kernel independent of J_H_total under fixed reference/linking-surface conditions, or retain R_kernel as an explicit radial/source residual",
            "success_gate": "unique exterior Green/constraint solution with fixed boundary/reference data, no unsourced 1/r mode, no range/boundary/domain homogeneous source, and no orbital readout backfill",
            "reason": "4156 reduces same-charge glue to the parent constraint-map kernel and integrability gates; kernel zero is the sharp next bottleneck.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4156 - Pi_M/H_tau Same-Charge Glue Or Radial Source Residual

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4155 locked the source-measure/Poynting accounting conditionally. The remaining source-mass bottleneck is whether:

`M_H[Pi_M J_H_total]`

is the same object as

`H_tau[S_outer]-H_ref`.

## Non-Circular Route
Do not define `Pi_M` from fitted orbital `GM`.

Define the target:

`Delta_PiM := M_H[Pi_M J_H_total] - (H_tau[S_outer]-H_ref)`.

The selected route is:

`Pi_M^C := D_N[C_tau]|_{{J_H[tau]}}`.

That is, `Pi_M` is the parent constraint Dirichlet-to-Neumann / boundary-charge pushforward from Hilbert source current to exterior Hamiltonian charge.

## Same-Charge Theorem
The conditional theorem is:

`Pi_M^C J_H = J_M_top + dB_zero`

and

`M_H[Pi_M^C J_H]=H_tau[S_outer]-H_ref`

if:

- the parent exterior constraint map is unique;
- no homogeneous unsourced `1/r` mass kernel survives;
- `Pi_M^C` is a fixed chain map on the Hilbert current complex;
- `H_tau` is integrable as a covariant phase-space charge;
- reference subtraction is fixed and q-basic;
- linked surfaces, frame, units, and `tau` are parent-owned before readout;
- extra, boundary, symplectic, and EM fluxes are owned or bounded.

## Radial Residual Branch
The radial/source residual is:

`M_H(S2)-M_H(S1)=int_A d(Pi_M^C J_H)`.

If same-charge glue fails, retain:

`epsilon_charge <= |C_M|+|C_curl|+|I_commutator|+|R_eq|+|C_ref|+|C_frame|+|C_units|+|R_kernel|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|+|epsilon_G_norm|+|epsilon_PPN_source|`.

No cancellation credit is allowed unless a parent identity proves it.

## Current Verdict
| Gate | Result | Meaning |
|---|---|---|
| parent constraint-map route | SELECTED | non-circular `Pi_M` construction |
| chain-map closure | CONDITIONAL | `[d,Pi_M^C]J_H=0` if parent fixed |
| H_tau integrability | CONDITIONAL | curl/corner/reference terms must vanish |
| homogeneous mass kernel | UNSIGNED | next sharp blocker |
| radial source residual | EMITTED | no fitted-GM laundering |
| Newton/local GR | NOT CLAIMED | source glue still conditional |

## Outputs
- `{outputs["P8_Y5_R2FR_4156_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE"]}`
- `{outputs["P8_Y5_R2FR_4156_ZERO_THEOREM_GATES"]}`
- `{outputs["P8_Y5_R2FR_4156_RESIDUAL_VECTOR"]}`
- `{outputs["P8_Y5_R2FR_4156_RADIAL_SOURCE_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4156_NEWTON_IMPACT"]}`
- `{outputs["P8_Y5_R2FR_4156_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4156_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4156_NEXT_TARGET"]}`

## Next Target
- `4157-Y5-R2FR-constraint-Green-kernel-zero-or-homogeneous-mass-residual.md`
- Prove the exterior constraint Green map has no homogeneous unsourced `1/r` mass mode, or retain `R_kernel` as explicit radial/source residual.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4156_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE"], constraint_map_rows())
    write_csv(outputs["P8_Y5_R2FR_4156_ZERO_THEOREM_GATES"], zero_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4156_RESIDUAL_VECTOR"], residual_vector_rows())
    write_csv(outputs["P8_Y5_R2FR_4156_RADIAL_SOURCE_ROWS"], radial_rows())
    write_csv(outputs["P8_Y5_R2FR_4156_NEWTON_IMPACT"], impact_rows())
    write_csv(outputs["P8_Y5_R2FR_4156_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4156_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4156_NEXT_TARGET"], next_rows())
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
        "VAL4156_0_sources",
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
    add("VAL4156_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "Pi_M^C := D_N[C_tau]",
        "Delta_PiM",
        "homogeneous unsourced `1/r` mass kernel",
        "epsilon_charge <=",
        "4157-Y5-R2FR-constraint-Green-kernel-zero-or-homogeneous-mass-residual.md",
    ]
    add("VAL4156_2_doc_tokens", "document records constraint-map route, same-charge theorem, residual vector and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    glue_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE"]))
    glue_tokens = ["TARGET_DEFINED_NO_GM_LAUNDERING", "CONSTRUCTIVE_ROUTE_SELECTED", "CHAINMAP_ZERO_CONDITIONAL", "HTAU_INTEGRABILITY_CONDITIONAL", "SAME_CHARGE_THEOREM_DERIVED_CONDITIONAL_UNSIGNED"]
    add("VAL4156_3_glue", "constraint-map glue rows record target, route, chainmap, integrability and same-charge theorem", all(token in glue_text for token in glue_tokens), "glue tokens checked")

    gates_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4156_ZERO_THEOREM_GATES"]))
    gates_tokens = ["UNSIGNED", "CONDITIONAL_NOT_PARENT_SIGNED", "PARTIAL_FROM_4155_EM_ONLY", "R_kernel", "C_curl"]
    add("VAL4156_4_gates", "zero gates retain kernel, commutator, curl, reference, surface and rest-flux blockers", all(token in gates_text for token in gates_tokens), "gate tokens checked")

    residual_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4156_RESIDUAL_VECTOR"]))
    residual_tokens = ["FINITE_CHARGE_GLUE_VECTOR_DERIVED_NONCLAIM", "DISCIPLINE_LOCK", "NO_GM_LAUNDERING_GUARD"]
    add("VAL4156_5_residual", "finite residual vector and no-GM-laundering guard are recorded", all(token in residual_text for token in residual_tokens), "residual tokens checked")

    radial_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4156_RADIAL_SOURCE_ROWS"]))
    radial_tokens = ["CONDITIONAL_RADIAL_ZERO_NOT_PARENT_SIGNED", "KERNEL_ZERO_UNSIGNED", "RETAIN_RADIAL_SOURCE_RESIDUAL"]
    add("VAL4156_6_radial", "radial rows retain linking-surface, kernel and range/source hair branches", all(token in radial_text for token in radial_tokens), "radial tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4156_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("constraint_map_route_selected") == "True"
        and status[0].get("same_charge_theorem_derived_conditional") == "True"
        and status[0].get("chainmap_zero_conditional") == "True"
        and status[0].get("Htau_integrability_conditional") == "True"
        and status[0].get("kernel_zero_parent_signed") == "False"
        and status[0].get("radial_source_residual_rows_emitted") == "True"
        and status[0].get("Newton_claimed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4156_7_status", "status records selected route, conditional theorem, unsigned kernel and no Newton/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4156_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4157-Y5-R2FR-constraint-Green-kernel-zero-or-homogeneous-mass-residual.md"
    add("VAL4156_8_next", "next target attacks constraint Green kernel zero", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4156_9_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4156-Y5-R2FR" in item.name or "R2FR_4156" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4156_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4156_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4156_VALIDATION.csv"
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
