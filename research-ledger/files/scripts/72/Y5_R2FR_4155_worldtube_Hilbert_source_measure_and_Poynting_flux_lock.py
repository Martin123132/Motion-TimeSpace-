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
DOC_PATH = ROOT / "4155-Y5-R2FR-worldtube-Hilbert-source-measure-and-Poynting-flux-lock.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_WORLDTUBE_HILBERT_POYNTING_4155"
CHECKPOINT_ID = "4155"
DECISION = "WORLDTUBE_HILBERT_SOURCE_MEASURE_AND_POYNTING_ONCE_LOCK_DERIVED_CONDITIONALLY_PIM_HTAU_GLUE_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4155_00_4154_doc": (
        ROOT / "4154-Y5-R2FR-mu-extra-zero-and-Hilbert-mass-flux-lock-or-source-normalization-runner.md",
        "EM / Poynting Routing",
        "4154 handoff to source-measure/Poynting lock.",
    ),
    "SRC4155_01_4154_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4154_NEXT_TARGET.csv",
        "worldtube/Hilbert source measure lock",
        "Machine-readable 4154 next-target row.",
    ),
    "SRC4155_02_once_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4127_POYNTING_ONCE_THEOREM.csv",
        "POT4127_2_no_extra_coefficient",
        "Poynting once-only theorem.",
    ),
    "SRC4155_03_no_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv",
        "PNT4038_4_result",
        "Stationary local Poynting no-flux theorem.",
    ),
    "SRC4155_04_em_stress": (
        SOURCE_DIR / "P8_Y5_R2FR_4000_EM_STRESS_POYNTING_THEOREM.csv",
        "EMP4000_3_internal_exchange_cancellation",
        "EM Hilbert stress and internal exchange theorem.",
    ),
    "SRC4155_05_worldtube_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_4011_HILBERT_WORLDTUBE_LOCK_THEOREM.csv",
        "HWT4011_6_full_lock_condition",
        "Hilbert worldtube lock theorem.",
    ),
    "SRC4155_06_source_measure": (
        SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "T510_2_MTS_transfer_condition",
        "Worldtube source measure theorem.",
    ),
    "SRC4155_07_3596_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_3596_WORLDTUBE_HILBERT_SOURCE_MEASURE_LOCK.csv",
        "WSL3596_6_conditional_lock_theorem",
        "Worldtube-Hilbert source measure lock.",
    ),
    "SRC4155_08_em_vector": (
        SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
        "EMF3502_1_radiative_poynting_flux",
        "EM/Poynting residual coefficient vector.",
    ),
    "SRC4155_09_script": (
        SCRIPT_PATH,
        "WORLDTUBE_HILBERT_SOURCE_MEASURE_AND_POYNTING_ONCE_LOCK",
        "This generator records the 4155 worldtube/Poynting lock.",
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
        "P8_Y5_R2FR_4155_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4155_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK": SOURCE_DIR / "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv",
        "P8_Y5_R2FR_4155_POYNTING_ONCE_LOCK": SOURCE_DIR / "P8_Y5_R2FR_4155_POYNTING_ONCE_LOCK.csv",
        "P8_Y5_R2FR_4155_FLUX_ZERO_OR_BOUND": SOURCE_DIR / "P8_Y5_R2FR_4155_FLUX_ZERO_OR_BOUND.csv",
        "P8_Y5_R2FR_4155_RESIDUAL_COEFFICIENT_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4155_RESIDUAL_COEFFICIENT_ROWS.csv",
        "P8_Y5_R2FR_4155_NEWTON_IMPACT_GATES": SOURCE_DIR / "P8_Y5_R2FR_4155_NEWTON_IMPACT_GATES.csv",
        "P8_Y5_R2FR_4155_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4155_DECISION_GATES.csv",
        "P8_Y5_R2FR_4155_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4155_STATUS.csv",
        "P8_Y5_R2FR_4155_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4155_NEXT_TARGET.csv",
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


def worldtube_source_rows() -> List[dict]:
    return [
        {
            **common(),
            "lock_id": "WT4155_0_dressed_source",
            "statement": "dressed Hilbert source measure",
            "formula": "M_H^dress[W;tau]=H_tau[S_outer]-H_tau[S_ref]=ell_M(Pi_M J_H_total)",
            "derivation": "The source mass used by the exterior Newton coefficient is the Hamiltonian/Hilbert source charge, not bare rest mass or an orbital readout label.",
            "status": "CONDITIONAL_DEFINITION_LOCK",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "WT4155_1_total_current",
            "statement": "total Hilbert current assembled once",
            "formula": "J_H_total=J_matter+J_EM+J_binding+dB_impr+J_rest_retained",
            "derivation": "Matter, minimal Maxwell field energy, binding, and exact improvements enter the same source current before readout; rest-sector terms must be zero/topological/bounded.",
            "status": "ONCE_ONLY_SOURCE_FUNCTIONAL_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "WT4155_2_noether_glue",
            "statement": "worldtube charge glue",
            "formula": "on shell J_tau=dQ_tau+C_tau; if C_tau=0 in exterior annulus then int_S2 Q_tau-int_S1 Q_tau=0",
            "derivation": "For an EH-style source-free exterior with controlled boundary flux, the dressed source charge is independent of linking surface.",
            "status": "GR_STYLE_GLUE_DERIVED_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "WT4155_3_support_lock",
            "statement": "Hilbert support/worldtube is parent-owned",
            "formula": "W_H=closure(supp J_H_total); D_v W_H=0 if J_H,tau,e_obs descend through q and support is compact regular",
            "derivation": "The source worldtube cannot be chosen after fitting orbits; it must be the support of the parent Hilbert current.",
            "status": "SUPPORT_LOCK_CONDITIONAL_WITH_REGULARITY_GUARD",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "WT4155_4_remaining_glue",
            "statement": "same-charge Pi_M/H_tau glue remains the bottleneck",
            "formula": "Q_M=ell_M(Pi_M J_H_total)=M_H^dress only if H_tau, Pi_M, tau, reference, frame and rest-sector silence are same-branch",
            "derivation": "The worldtube/Poynting source measure can be conditionally locked, but the mass projector and Hamiltonian charge still need same-branch parent glue.",
            "status": "PIM_HTAU_GLUE_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def poynting_once_rows() -> List[dict]:
    return [
        {
            **common(),
            "poynting_id": "PY4155_0_stress_identity",
            "statement": "Poynting is stress-current flux",
            "formula": "T_EM^{0i}=S_Poynting^i/c^2",
            "derivation": "The Poynting vector is the spatial energy-flux component of the EM Hilbert stress in the observed local frame.",
            "status": "EXACT_CONDITIONAL_LOCAL_FRAME_IDENTITY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "poynting_id": "PY4155_1_internal_exchange",
            "statement": "matter-EM internal exchange cancels in total source",
            "formula": "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda, nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda",
            "derivation": "Matter-only mass tubes are wrong for charged/bound systems; the conserved object is total matter+EM Hilbert stress.",
            "status": "INTERNAL_EXCHANGE_CANCELLATION_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "poynting_id": "PY4155_2_once_only",
            "statement": "no extra Poynting source coefficient",
            "formula": "M_trial=ell_M(Pi_M J_H_total)+c_Poynt_extra int_boundary S_Poynting dot n dA => c_Poynt_extra=0",
            "derivation": "Once J_H_total already contains EM stress flux, adding a second Poynting term double-counts the same source energy.",
            "status": "EXTRA_POYNTING_COEFFICIENT_ZERO_BY_SINGLE_SOURCE_FUNCTIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "poynting_id": "PY4155_3_bound_fields",
            "statement": "bound EM fields are inside M_H",
            "formula": "minimal stationary Maxwell stress -> J_H_total; epsilon_EM_bound=0 relative to M_H",
            "derivation": "Coulomb/magnetostatic bound energy gravitates as part of the dressed source measure, not as an extra MTS correction.",
            "status": "BOUND_FIELD_NOT_EXTRA_FLUX_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def flux_zero_or_bound_rows() -> List[dict]:
    return [
        {
            **common(),
            "flux_id": "FZ4155_0_poynting_identity",
            "target": "Phi_EM_rad",
            "formula": "D_tau E_EM[V]+int_boundary S_Poynting dot n dA = -int_V J dot E dV + improvements",
            "zero_condition": "stationary isolated exterior collar, no current crossing collar, no imposed incoming/background radiation",
            "result": "IDENTITY_AND_ZERO_CONDITION_RECORDED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "flux_id": "FZ4155_1_stationary_zero",
            "target": "Phi_EM_rad",
            "formula": "time_avg(Phi_EM_rad)=0 when time_avg(dU_EM/dt)=0 and time_avg(int J.E)=0",
            "zero_condition": "closed stationary isolated worldtube",
            "result": "CONDITIONAL_ZERO_BRANCH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "flux_id": "FZ4155_2_radiative_bound",
            "target": "epsilon_EM_extra",
            "formula": "|epsilon_EM_extra| <= (|Delta U_EM|+|W_matter|+|Phi_external|+|B_improvement|)/(|M_H| c^2)",
            "zero_condition": "not zero; finite radiative/nonstationary fallback",
            "result": "FINITE_FLUX_BOUND_TEMPLATE_VALUE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "flux_id": "FZ4155_3_cosmology_guard",
            "target": "global/cosmological flux",
            "formula": "local stationary Phi_EM_rad=0 does not imply cosmological/memory flux variables vanish",
            "zero_condition": "branch selector separates compact local source from FLRW/cosmology",
            "result": "GLOBAL_OVERKILL_GUARD",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> List[dict]:
    return [
        {
            **common(),
            "residual_id": "RC4155_0_radiative_flux",
            "quantity": "Phi_EM_rad/(G_ref M_H)",
            "when_active": "nonstationary, radiative, background or incoming EM flux crosses the source boundary",
            "required_input": "flux history or bound envelope for Delta U_EM, W_matter, Phi_external, B_improvement",
            "status": "RETAINED_FLUX_COEFFICIENT_REQUIRED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RC4155_1_nonminimal_XF2",
            "quantity": "C_XF2",
            "when_active": "MTS/motion/time/space scalar or tensor multiplies F^2 or F*F",
            "required_input": "parent exclusion theorem or coefficient with units and source path",
            "status": "RETAINED_OPERATOR_COEFFICIENT_REQUIRED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RC4155_2_Hodge_flow",
            "quantity": "Delta_Hodge_EM",
            "when_active": "EM Hodge/constitutive flow rule differs from observed gravitational coframe",
            "required_input": "observed Hodge parent signature or tensor residual",
            "status": "RETAINED_HODGE_FLOW_COEFFICIENT_REQUIRED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RC4155_3_double_count_guard",
            "quantity": "epsilon_EM_double_count",
            "when_active": "same EM flux is included in M_H and added again as separate force/source",
            "required_input": "forbid by single source functional; do not fit",
            "status": "SUBTERM_ELIMINATED_BY_DEFINITION_LOCK",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RC4155_4_worldtube_glue",
            "quantity": "epsilon_closed_source_failure",
            "when_active": "Pi_M/H_tau/tau/reference/frame/rest-sector same-branch glue remains unsigned",
            "required_input": "same-charge parent glue or finite residual vector",
            "status": "PIM_HTAU_GLUE_RETAINED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def impact_rows() -> List[dict]:
    return [
        {
            **common(),
            "impact_id": "NI4155_0_EM",
            "component": "ordinary EM/Poynting source accounting",
            "result": "CONDITIONALLY_CLOSED_ONCE_ONLY",
            "meaning": "minimal stationary EM energy is in M_H and no extra Poynting coefficient is allowed",
            "still_needed": "observed Hodge/current owner and nonminimal/radiative residual exclusions",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "NI4155_1_worldtube",
            "component": "worldtube source measure",
            "result": "CONDITIONAL_LOCK",
            "meaning": "source mass should be dressed Hilbert/Hamiltonian charge, not bare rest mass or orbital fit",
            "still_needed": "Pi_M/H_tau same-charge glue and absolute Gauss calibration",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "NI4155_2_Newton",
            "component": "Newton source normalization",
            "result": "PARTIAL_PROGRESS_NOT_PASS",
            "meaning": "EM/Poynting ambiguity narrowed; Newton still needs Pi_M/H_tau glue and mu_extra channel locks",
            "still_needed": "mu_extra=0, closed M_H, beta closure",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "NI4155_3_local_GR",
            "component": "local GR",
            "result": "NOT_CLAIMED",
            "meaning": "worldtube/Poynting is one source-measure block only",
            "still_needed": "PPN, Y6, R11, Maxwell ownership, and empirical robustness gates",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DEC4155_0_source",
            "question": "is source mass bare matter mass?",
            "answer": "no; it must be the dressed Hilbert/Hamiltonian source measure",
            "decision": "DRESSED_SOURCE_MEASURE_LOCK_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4155_1_poynting",
            "question": "does Poynting create an independent source coefficient?",
            "answer": "no for minimal stationary same-source branch; yes as explicit residual for radiative/nonminimal leakage",
            "decision": "POYNTING_ONCE_ONLY_OR_RESIDUAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4155_2_next",
            "question": "what is the next bottleneck?",
            "answer": "Pi_M/H_tau same-charge glue and Gauss calibration",
            "decision": "NEXT_PIM_HTAU_SAME_CHARGE_GLUE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "worldtube_source_measure_lock_derived_conditional": "True",
            "Poynting_once_only_lock_derived_conditional": "True",
            "stationary_Poynting_zero_branch_derived": "True",
            "radiative_flux_bound_rows_emitted": "True",
            "minimal_EM_inside_Hilbert_source": "True",
            "nonminimal_EM_owner_signed": "False",
            "PiM_Htau_same_charge_glue_signed": "False",
            "Newton_claimed": "False",
            "local_gr_claimed": "False",
            "next_target": "4156-Y5-R2FR-PiM-Htau-same-charge-glue-or-radial-source-residual.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4155_0",
            "target_doc": "4156-Y5-R2FR-PiM-Htau-same-charge-glue-or-radial-source-residual.md",
            "target_script": "scripts/Y5_R2FR_4156_PiM_Htau_same_charge_glue_or_radial_source_residual.py",
            "objective": "prove Pi_M and H_tau are the same parent source charge with fixed tau, reference, linking surface and Gauss/orbital calibration, or retain radial/source-measure residual rows",
            "success_gate": "Pi_M J_H_total equals the H_tau source charge before readout, linking-surface independence is parent-owned, reference subtraction is fixed, and Gauss/orbital 1/r readout uses the same charge",
            "reason": "4155 clarifies worldtube/Poynting accounting; the remaining mass-source bottleneck is same-charge glue between Pi_M and H_tau.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4155 - Worldtube Hilbert Source Measure And Poynting Flux Lock

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4154 showed that Newton still fails unless `M_H` is the right closed source charge and `mu_extra` does not hide field/source flux.

This checkpoint locks the source-measure and Poynting accounting as far as the current parent route allows.

## Worldtube Source Measure
The source mass is not bare matter mass and not an orbital fit.

The clean definition is:

`M_H^dress[W;tau]=H_tau[S_outer]-H_tau[S_ref]=ell_M(Pi_M J_H_total)`.

with

`J_H_total=J_matter+J_EM+J_binding+dB_impr+J_rest_retained`.

The worldtube is parent-owned:

`W_H=closure(supp J_H_total)`.

If `J_H`, `tau`, `e_obs`, support, linked surfaces, and references are all same-branch and q-basic, source/worldtube selector leakage vanishes conditionally.

## Poynting Once-Only Lock
The Poynting vector is not decorative and not an extra patch:

`T_EM^{{0i}}=S_Poynting^i/c^2`.

Matter and EM exchange internally:

`nabla_mu T_EM^{{mu nu}}=-F^{{nu lambda}}J_lambda`,

`nabla_mu T_matter^{{mu nu}}=+F^{{nu lambda}}J_lambda`.

Therefore the conserved object is total matter+EM Hilbert stress. A trial extra source

`M_trial=ell_M(Pi_M J_H_total)+c_Poynt_extra int_boundary S_Poynting dot n dA`

double-counts the same energy flux, so the once-only branch forces

`c_Poynt_extra=0`.

## Stationary No-Flux Branch
The Poynting identity is:

`D_tau E_EM[V]+int_boundary S_Poynting dot n dA = -int_V J dot E dV + improvements`.

For a stationary isolated exterior collar with no imposed incoming/background radiation:

`time_avg(Phi_EM_rad)=0`.

Bound Coulomb/magnetostatic energy is still in `M_H`; it is not zeroed out. Only net leakage through the boundary is zeroed.

## Residual Branch
If the source is radiative, nonstationary, background-driven, or nonminimal, retain:

`|epsilon_EM_extra| <= (|Delta U_EM|+|W_matter|+|Phi_external|+|B_improvement|)/(|M_H| c^2)`.

Also retain explicit rows for:

- `C_XF2`;
- `Delta_Hodge_EM`;
- `C_EM_readout`;
- `epsilon_closed_source_failure`.

## Current Verdict
| Gate | Result | Meaning |
|---|---|---|
| dressed source measure | CONDITIONAL LOCK | source mass is Hilbert/Hamiltonian charge |
| Poynting once-only | CONDITIONAL LOCK | minimal EM flux counted once inside `J_H_total` |
| stationary no-flux | CONDITIONAL ZERO | closed local stationary collar has no net Poynting leakage |
| radiative/nonminimal EM | RETAINED | explicit residual coefficients required |
| Pi_M/H_tau glue | UNSIGNED | next source-measure bottleneck |
| Newton/local GR | NOT CLAIMED | this closes only a source-accounting subproblem |

## Outputs
- `{outputs["P8_Y5_R2FR_4155_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK"]}`
- `{outputs["P8_Y5_R2FR_4155_POYNTING_ONCE_LOCK"]}`
- `{outputs["P8_Y5_R2FR_4155_FLUX_ZERO_OR_BOUND"]}`
- `{outputs["P8_Y5_R2FR_4155_RESIDUAL_COEFFICIENT_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4155_NEWTON_IMPACT_GATES"]}`
- `{outputs["P8_Y5_R2FR_4155_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4155_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4155_NEXT_TARGET"]}`

## Next Target
- `4156-Y5-R2FR-PiM-Htau-same-charge-glue-or-radial-source-residual.md`
- Prove `Pi_M J_H_total` and `H_tau` are the same parent source charge before readout, or retain radial/source-measure residual rows.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4155_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK"], worldtube_source_rows())
    write_csv(outputs["P8_Y5_R2FR_4155_POYNTING_ONCE_LOCK"], poynting_once_rows())
    write_csv(outputs["P8_Y5_R2FR_4155_FLUX_ZERO_OR_BOUND"], flux_zero_or_bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4155_RESIDUAL_COEFFICIENT_ROWS"], residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4155_NEWTON_IMPACT_GATES"], impact_rows())
    write_csv(outputs["P8_Y5_R2FR_4155_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4155_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4155_NEXT_TARGET"], next_rows())
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
        "VAL4155_0_sources",
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
    add("VAL4155_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "M_H^dress[W;tau]",
        "J_H_total=J_matter+J_EM+J_binding+dB_impr+J_rest_retained",
        "c_Poynt_extra=0",
        "epsilon_EM_extra",
        "4156-Y5-R2FR-PiM-Htau-same-charge-glue-or-radial-source-residual.md",
    ]
    add("VAL4155_2_doc_tokens", "document records worldtube source measure, Poynting once lock, residual branch and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    source_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK"]))
    source_tokens = ["CONDITIONAL_DEFINITION_LOCK", "ONCE_ONLY_SOURCE_FUNCTIONAL_CONDITIONAL", "GR_STYLE_GLUE_DERIVED_CONDITIONAL", "SUPPORT_LOCK_CONDITIONAL_WITH_REGULARITY_GUARD", "PIM_HTAU_GLUE_UNSIGNED"]
    add("VAL4155_3_worldtube", "worldtube source lock records dressed source, total current, Noether glue, support lock and remaining glue blocker", all(token in source_text for token in source_tokens), "worldtube tokens checked")

    poynting_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4155_POYNTING_ONCE_LOCK"]))
    poynting_tokens = ["EXACT_CONDITIONAL_LOCAL_FRAME_IDENTITY", "INTERNAL_EXCHANGE_CANCELLATION_CONDITIONAL", "EXTRA_POYNTING_COEFFICIENT_ZERO_BY_SINGLE_SOURCE_FUNCTIONAL", "BOUND_FIELD_NOT_EXTRA_FLUX_CONDITIONAL"]
    add("VAL4155_4_poynting", "Poynting once-lock records stress flux, exchange cancellation, no extra coefficient and bound-field inclusion", all(token in poynting_text for token in poynting_tokens), "Poynting tokens checked")

    flux_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4155_FLUX_ZERO_OR_BOUND"]))
    flux_tokens = ["IDENTITY_AND_ZERO_CONDITION_RECORDED", "CONDITIONAL_ZERO_BRANCH", "FINITE_FLUX_BOUND_TEMPLATE_VALUE_MISSING", "GLOBAL_OVERKILL_GUARD"]
    add("VAL4155_5_flux", "flux rows distinguish stationary zero, radiative bound and cosmology guard", all(token in flux_text for token in flux_tokens), "flux tokens checked")

    residual_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4155_RESIDUAL_COEFFICIENT_ROWS"]))
    residual_tokens = ["RETAINED_FLUX_COEFFICIENT_REQUIRED", "RETAINED_OPERATOR_COEFFICIENT_REQUIRED", "RETAINED_HODGE_FLOW_COEFFICIENT_REQUIRED", "SUBTERM_ELIMINATED_BY_DEFINITION_LOCK", "PIM_HTAU_GLUE_RETAINED"]
    add("VAL4155_6_residuals", "residual rows retain radiative, nonminimal, Hodge, double-count and worldtube-glue branches", all(token in residual_text for token in residual_tokens), "residual tokens checked")

    impact_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4155_NEWTON_IMPACT_GATES"]))
    impact_tokens = ["CONDITIONALLY_CLOSED_ONCE_ONLY", "CONDITIONAL_LOCK", "PARTIAL_PROGRESS_NOT_PASS", "NOT_CLAIMED"]
    add("VAL4155_7_impact", "impact rows distinguish EM/Poynting progress from Newton/local-GR claims", all(token in impact_text for token in impact_tokens), "impact tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4155_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("worldtube_source_measure_lock_derived_conditional") == "True"
        and status[0].get("Poynting_once_only_lock_derived_conditional") == "True"
        and status[0].get("stationary_Poynting_zero_branch_derived") == "True"
        and status[0].get("radiative_flux_bound_rows_emitted") == "True"
        and status[0].get("minimal_EM_inside_Hilbert_source") == "True"
        and status[0].get("nonminimal_EM_owner_signed") == "False"
        and status[0].get("PiM_Htau_same_charge_glue_signed") == "False"
        and status[0].get("Newton_claimed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4155_8_status", "status records conditional locks, retained nonminimal/glue blockers and no Newton/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4155_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4156-Y5-R2FR-PiM-Htau-same-charge-glue-or-radial-source-residual.md"
    add("VAL4155_9_next", "next target attacks Pi_M/H_tau same-charge glue", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4155_10_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4155-Y5-R2FR" in item.name or "R2FR_4155" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4155_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4155_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4155_VALIDATION.csv"
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
