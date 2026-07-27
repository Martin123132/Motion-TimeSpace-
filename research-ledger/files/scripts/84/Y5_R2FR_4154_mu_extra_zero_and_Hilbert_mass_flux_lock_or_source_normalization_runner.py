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
DOC_PATH = ROOT / "4154-Y5-R2FR-mu-extra-zero-and-Hilbert-mass-flux-lock-or-source-normalization-runner.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_MU_EXTRA_HILBERT_FLUX_4154"
CHECKPOINT_ID = "4154"
DECISION = "MU_EXTRA_ZERO_THEOREM_REDUCED_TO_CHANNEL_LOCKS_HILBERT_FLUX_UNSIGNED_SOURCE_NORMALIZATION_RUNNER_READY"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4154_00_4153_doc": (
        ROOT / "4153-Y5-R2FR-topological-kappa-parent-action-stress-test-or-adoption-packet.md",
        "Pure coupling drift now has a candidate mechanism",
        "4153 handoff to mu_extra and Hilbert mass flux.",
    ),
    "SRC4154_01_4153_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4153_NEXT_TARGET.csv",
        "attack the remaining Newton source blocker",
        "Machine-readable 4153 next-target row.",
    ),
    "SRC4154_02_mass_flux_contract": (
        SOURCE_DIR / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "MF8_retained_residual_fallback",
        "Mass-flux projector/Euler calibration contract.",
    ),
    "SRC4154_03_mu_owner_gate": (
        SOURCE_DIR / "P8_MU_EXTRA_ZERO_OWNER_GATE.csv",
        "MO8_all_channels_closed",
        "mu_extra zero owner gate.",
    ),
    "SRC4154_04_mu_channel_ledger": (
        SOURCE_DIR / "P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv",
        "domain_projector_mass",
        "mu_extra channel owner ledger, including EM/Poynting.",
    ),
    "SRC4154_05_mu_vector": (
        SOURCE_DIR / "P8_mu_extra_over_Geff_Meff_vector.csv",
        "EMV3501_10_em_poynting_hilbert_dressing",
        "mu_extra over G_eff M_eff vector.",
    ),
    "SRC4154_06_4151_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4151_EH_ONLY_NEWTON_THEOREM.csv",
        "mu_obs=G_eff M_H",
        "4151 measured-GM residual law.",
    ),
    "SRC4154_07_4153_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4153_STATUS.csv",
        "coupling_drift_closed_if_adopted",
        "4153 kappa adoption status.",
    ),
    "SRC4154_08_script": (
        SCRIPT_PATH,
        "MU_EXTRA_ZERO_THEOREM_REDUCED_TO_CHANNEL_LOCKS",
        "This generator records the 4154 mu_extra/mass-flux gate.",
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
        "P8_Y5_R2FR_4154_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4154_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4154_MU_EXTRA_ZERO_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4154_MU_EXTRA_ZERO_THEOREM.csv",
        "P8_Y5_R2FR_4154_HILBERT_MASS_FLUX_LOCK": SOURCE_DIR / "P8_Y5_R2FR_4154_HILBERT_MASS_FLUX_LOCK.csv",
        "P8_Y5_R2FR_4154_CHANNEL_ZERO_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4154_CHANNEL_ZERO_AUDIT.csv",
        "P8_Y5_R2FR_4154_SOURCE_NORMALIZATION_RUNNER_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4154_SOURCE_NORMALIZATION_RUNNER_ROWS.csv",
        "P8_Y5_R2FR_4154_NEWTON_GATE_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4154_NEWTON_GATE_STATUS.csv",
        "P8_Y5_R2FR_4154_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4154_DECISION_GATES.csv",
        "P8_Y5_R2FR_4154_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4154_STATUS.csv",
        "P8_Y5_R2FR_4154_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4154_NEXT_TARGET.csv",
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


def theorem_rows() -> List[dict]:
    return [
        {
            **common(),
            "theorem_id": "MZ4154_0_sum_rule",
            "statement": "measured monopole decomposition",
            "formula": "mu_obs=G_ref M_H + mu_extra = G_ref M_H (1+epsilon_mu), epsilon_mu=sum_i epsilon_i",
            "derivation": "The exterior Gauss-law monopole splits into the same-frame Hilbert mass term plus every non-Hilbert/boundary/domain/range/source-normalization channel.",
            "result": "MU_EXTRA_SUM_RULE_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "MZ4154_1_zero_condition",
            "statement": "mu_extra zero theorem",
            "formula": "mu_extra=0 iff every epsilon_i is theorem-zero, topological with zero derivative/source projection, or explicitly below its local gate",
            "derivation": "Ward ownership or conservation is insufficient; the monopole itself must vanish, be a harmless universal constant, or be scored.",
            "result": "CHANNELWISE_ZERO_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "MZ4154_2_mass_flux",
            "statement": "closed Hilbert mass flux condition",
            "formula": "d(Pi_M J_H)=0 => M_H(r2)-M_H(r1)=0 and dM_H/dt=0 for isolated stationary branch",
            "derivation": "Newton source normalization needs the Hilbert mass projector to be parent-owned and closed before readout, not fitted after orbital calibration.",
            "result": "HILBERT_FLUX_LOCK_DERIVED_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "MZ4154_3_EM_poynting",
            "statement": "ordinary EM/Poynting energy routing",
            "formula": "minimal Maxwell stress belongs in J_H/T_H; nonminimal or radiative leakage enters epsilon_EM_extra",
            "derivation": "Field energy is not ignored. Stationary closed-surface Poynting flux is part of the conserved Hilbert source; background-field or wave leakage must be a separate coefficient.",
            "result": "EM_STRESS_ROUTING_CLARIFIED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "MZ4154_4_Newton_status",
            "statement": "Newton gate after kappa",
            "formula": "kappa drift closed conditionally, but Newton requires mu_extra=0 and closed M_H",
            "derivation": "4153 can make G_ref constant if adopted. That still leaves source-normalization and mass-flux rows as the active Newton blockers.",
            "result": "NEWTON_STILL_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def mass_flux_rows() -> List[dict]:
    return [
        {
            **common(),
            "lock_id": "MFL4154_0_projector_origin",
            "requirement": "Pi_M is parent-derived before readout",
            "formula": "Pi_M: J_H -> H^2_abs(Sigma_ext)",
            "current_status": "CANDIDATE_ORIGIN_NOT_COMPLETED",
            "residual_if_failed": "mass projector remains closure-only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "MFL4154_1_same_frame_current",
            "requirement": "J_H is Hilbert/Ward matter+field source in same observed coframe",
            "formula": "J_H from delta S_matter/delta e_obs plus owned minimal field stresses",
            "current_status": "CONDITIONAL_FROM_PRIOR_STACK",
            "residual_if_failed": "source current fitted/readout-defined",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "MFL4154_2_flux_closure",
            "requirement": "Euler/Ward identity closes projected mass current",
            "formula": "d(Pi_M J_H)=0",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "residual_if_failed": "dln_MH_dt; radial_MH_flux",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "MFL4154_3_no_ad_hoc_multiplier",
            "requirement": "mass closure is not inserted just to force GM success",
            "formula": "lambda_M is gauge/topological/Ward/symplectic-owned",
            "current_status": "NOT_SATISFIED",
            "residual_if_failed": "closure counted as assumption only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "MFL4154_4_absolute_calibration",
            "requirement": "M_H normalization equals asymptotic/orbital monopole",
            "formula": "M_H=(4 pi G_ref)^-1 int_S2 Pi_M J_H and mu_obs=G_ref M_H",
            "current_status": "NOT_PARENT_DERIVED",
            "residual_if_failed": "closed mass flux is not measured Newtonian mass",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def channel_audit_rows() -> List[dict]:
    return [
        {
            **common(),
            "channel_id": "CH4154_0_radial",
            "channel": "radial_MH_flux",
            "zero_route": "d(Pi_M J_H)=0 in exterior annulus",
            "current_status": "CONDITIONAL_ZERO_ROUTE_NOT_INHERITED",
            "residual": "epsilon_radial_MH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "channel_id": "CH4154_1_boundary",
            "channel": "boundary_topological_monopole",
            "zero_route": "fixed topological boundary or parent-fixed universal calibration with zero derivatives",
            "current_status": "CONDITIONAL_HARMLESS_NOT_PARENT_FIXED",
            "residual": "epsilon_boundary",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "channel_id": "CH4154_2_domain",
            "channel": "domain_projector_mass",
            "zero_route": "projector/domain no-monopole/no-vector/no-shear theorem",
            "current_status": "CONDITIONAL_OPEN",
            "residual": "epsilon_domain_projector",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "channel_id": "CH4154_3_bulk_range",
            "channel": "bulk_X_Yukawa_tail",
            "zero_route": "positive source-free mass gap/no physical X pole or executable R10 curve pass",
            "current_status": "RETAINED_CURVE_OR_THEOREM_REQUIRED",
            "residual": "epsilon_bulk_X; alpha(lambda)",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "channel_id": "CH4154_4_nonEH",
            "channel": "nonEH_operator_potential",
            "zero_route": "EH-only exterior theorem or executable R11 vector below locks",
            "current_status": "RETAINED_OPERATOR_VECTOR_REQUIRED",
            "residual": "epsilon_nonEH_source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "channel_id": "CH4154_5_species_frame",
            "channel": "species_source_selector and frame_domain_pullback",
            "zero_route": "same source normalization for all compositions and one observed coframe/source pullback",
            "current_status": "RETAINED_COEFFICIENT_REQUIRED",
            "residual": "epsilon_species_A; epsilon_frame_domain",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "channel_id": "CH4154_6_EM",
            "channel": "EM_field_stress_and_flux",
            "zero_route": "minimal Maxwell stress included in M_H and stationary closed-surface Poynting flux vanishes",
            "current_status": "CONDITIONAL_ZERO_ROUTE_FOR_ORDINARY_EM_STRESS",
            "residual": "epsilon_EM_extra if nonminimal or radiative leakage",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "channel_id": "CH4154_7_calibration",
            "channel": "absolute_calibration_offset",
            "zero_route": "parent-fixed universal constant with all derivative channels zero",
            "current_status": "CONDITIONAL_HARMLESS_NOT_CLAIMED",
            "residual": "epsilon_calibration",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[dict]:
    return [
        {
            **common(),
            "runner_id": "SNR4154_0_epsilon_mu",
            "quantity": "epsilon_mu=sum_i epsilon_i",
            "required_input": "all channel epsilon_i values or theorem-zero certificates",
            "runner_state": "NOT_SCOREABLE_CHANNELS_UNSIGNED",
            "observable_links": "Newton; beta; gamma; alpha3; xi; Gdot; R10; R11",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "runner_id": "SNR4154_1_mass_flux",
            "quantity": "dln_MH_dt and partial_r ln M_H",
            "required_input": "Pi_M parent origin, d(Pi_M J_H)=0, no boundary/range/domain flux",
            "runner_state": "NOT_SCOREABLE_FLUX_UNSIGNED",
            "observable_links": "Gdot; orbital timing; radial source hair",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "runner_id": "SNR4154_2_EM_flux",
            "quantity": "epsilon_EM_extra",
            "required_input": "minimal Maxwell inclusion theorem or Poynting/cross-term coefficient",
            "runner_state": "CONDITIONAL_ZERO_OR_COEFFICIENT_REQUIRED",
            "observable_links": "Maxwell stress; clocks; local flux; PPN",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "runner_id": "SNR4154_3_beta",
            "quantity": "delta_beta_source",
            "required_input": "S_beta^source=0 after Newton normalization or numeric bound row",
            "runner_state": "DEFERRED_UNTIL_FIRST_ORDER_SOURCE_ROWS_CLOSE",
            "observable_links": "PPN beta",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def newton_gate_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "NG4154_0_kappa",
            "gate": "constant coupling",
            "current_result": "CONDITIONAL_MECHANISM_FROM_4153",
            "needed_for_pass": "adopt topological kappa packet safely",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "NG4154_1_mass",
            "gate": "closed Hilbert mass",
            "current_result": "UNSIGNED",
            "needed_for_pass": "d(Pi_M J_H)=0 and calibrated M_H readout",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "NG4154_2_mu_extra",
            "gate": "no extra source monopole",
            "current_result": "FAIL_CURRENT_PROMOTION",
            "needed_for_pass": "all epsilon_i theorem-zero/harmless/scored",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "NG4154_3_Newton",
            "gate": "Newton source branch",
            "current_result": "NOT_CLAIMED",
            "needed_for_pass": "constant G_ref, closed M_H, mu_extra=0, same-frame source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "NG4154_4_local_GR",
            "gate": "local GR branch",
            "current_result": "NOT_CLAIMED",
            "needed_for_pass": "Newton plus PPN beta/gamma/source/Y6/EM gates",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DEC4154_0_theorem",
            "question": "can mu_extra=0 be proven in one stroke?",
            "answer": "no; it reduces to channelwise zero/harmless/scored locks",
            "decision": "CHANNELWISE_MU_EXTRA_LOCK_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4154_1_mass_flux",
            "question": "is Hilbert mass flux closed from current corpus?",
            "answer": "not parent-derived; conditional only",
            "decision": "HILBERT_FLUX_LOCK_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4154_2_EM",
            "question": "where does Poynting/EM flux belong?",
            "answer": "minimal stationary EM belongs in Hilbert mass; nonminimal/radiative leakage becomes epsilon_EM_extra",
            "decision": "EM_STRESS_ROUTED_NOT_IGNORED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4154_3_next",
            "question": "best next target",
            "answer": "attack closed Hilbert/worldtube source measure and EM/Poynting flux routing together",
            "decision": "NEXT_WORLDTUBE_SOURCE_MEASURE_FLUX_LOCK",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "mu_extra_sum_rule_derived": "True",
            "mu_extra_zero_reduced_to_channel_locks": "True",
            "Hilbert_mass_flux_lock_derived_conditional": "True",
            "Hilbert_mass_flux_parent_signed": "False",
            "all_mu_extra_channels_closed": "False",
            "EM_Poynting_routing_clarified": "True",
            "source_normalization_runner_rows_emitted": "True",
            "Newton_claimed": "False",
            "local_gr_claimed": "False",
            "next_target": "4155-Y5-R2FR-worldtube-Hilbert-source-measure-and-Poynting-flux-lock.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4154_0",
            "target_doc": "4155-Y5-R2FR-worldtube-Hilbert-source-measure-and-Poynting-flux-lock.md",
            "target_script": "scripts/Y5_R2FR_4155_worldtube_Hilbert_source_measure_and_Poynting_flux_lock.py",
            "objective": "derive the worldtube/Hilbert source measure lock: prove ordinary matter plus minimal Maxwell field energy forms a closed source current with zero exterior Poynting/leakage flux, or emit explicit EM/source-flux residual coefficients",
            "success_gate": "Pi_M J_H is parent-owned and closed, stationary closed-surface Poynting flux is zero or explicitly bounded, nonminimal EM/MTS cross terms are absent or coefficient-scored, and no boundary/domain source-measure flux survives",
            "reason": "4154 shows mu_extra cannot close globally until the source measure and field-flux routing are parent-owned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4154 - `mu_extra` Zero And Hilbert Mass-Flux Lock Or Source-Normalization Runner

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4153 gives pure coupling drift a candidate mechanism: topological `kappa` can make `G_ref` constant if adopted safely.

That is not enough for Newton. The Newton source is still blocked unless the exterior monopole sees only the same-frame Hilbert mass:

`mu_obs=G_ref M_H`.

## `mu_extra` Theorem
The exact decomposition is:

`mu_obs=G_ref M_H + mu_extra = G_ref M_H (1+epsilon_mu)`.

with

`epsilon_mu=sum_i epsilon_i`.

Therefore:

`mu_extra=0`

only if every channel is theorem-zero, topological/harmless with zero source derivatives, or explicitly scored below its local gate.

Ward ownership is not enough. A conserved hidden monopole still shifts measured `GM`.

## Hilbert Mass-Flux Lock
The clean mass route is:

`d(Pi_M J_H)=0`.

Then:

`M_H(r2)-M_H(r1)=0`

and, for a stationary isolated source:

`dM_H/dt=0`.

Current status: this is a conditional lock, not parent-signed. The projector origin, flux closure, no-ad-hoc multiplier, and absolute asymptotic calibration remain open.

## EM / Poynting Routing
This checkpoint keeps the Poynting-vector intuition in the right place.

Ordinary minimal Maxwell field energy should be included in the Hilbert source:

`T_EM -> J_H`.

For a stationary closed worldtube, the closed-surface Poynting flux should vanish. If there is nonminimal MTS-EM coupling, background-field leakage, high-frequency wave/relic flux, or any cross term not included in `J_H`, it becomes:

`epsilon_EM_extra`.

So EM stress is not ignored; it is either owned by the Hilbert mass or scored as leakage.

## Current Verdict
| Gate | Result | Meaning |
|---|---|---|
| `mu_extra` sum rule | DERIVED | source-normalization split is explicit |
| `mu_extra=0` | NOT PROVED | requires channelwise locks |
| Hilbert mass flux | CONDITIONAL | `d(Pi_M J_H)=0` not parent-signed |
| EM/Poynting | ROUTED | owned Maxwell stress vs leakage split written |
| Newton | NOT CLAIMED | `M_H` and `mu_extra` still unsigned |
| local GR | NOT CLAIMED | beta, Y6, EM/current gates remain open |

## Outputs
- `{outputs["P8_Y5_R2FR_4154_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4154_MU_EXTRA_ZERO_THEOREM"]}`
- `{outputs["P8_Y5_R2FR_4154_HILBERT_MASS_FLUX_LOCK"]}`
- `{outputs["P8_Y5_R2FR_4154_CHANNEL_ZERO_AUDIT"]}`
- `{outputs["P8_Y5_R2FR_4154_SOURCE_NORMALIZATION_RUNNER_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4154_NEWTON_GATE_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4154_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4154_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4154_NEXT_TARGET"]}`

## Next Target
- `4155-Y5-R2FR-worldtube-Hilbert-source-measure-and-Poynting-flux-lock.md`
- Derive the worldtube/Hilbert source-measure lock and stationary Poynting-flux silence, or emit explicit EM/source-flux residual coefficients.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4154_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4154_MU_EXTRA_ZERO_THEOREM"], theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4154_HILBERT_MASS_FLUX_LOCK"], mass_flux_rows())
    write_csv(outputs["P8_Y5_R2FR_4154_CHANNEL_ZERO_AUDIT"], channel_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4154_SOURCE_NORMALIZATION_RUNNER_ROWS"], runner_rows())
    write_csv(outputs["P8_Y5_R2FR_4154_NEWTON_GATE_STATUS"], newton_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4154_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4154_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4154_NEXT_TARGET"], next_rows())
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
        "VAL4154_0_sources",
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
    add("VAL4154_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "mu_obs=G_ref M_H",
        "epsilon_mu=sum_i epsilon_i",
        "d(Pi_M J_H)=0",
        "epsilon_EM_extra",
        "4155-Y5-R2FR-worldtube-Hilbert-source-measure-and-Poynting-flux-lock.md",
    ]
    add("VAL4154_2_doc_tokens", "document records mu_extra theorem, mass-flux lock, EM/Poynting routing and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    theorem_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4154_MU_EXTRA_ZERO_THEOREM"]))
    theorem_tokens = ["MU_EXTRA_SUM_RULE_DERIVED", "CHANNELWISE_ZERO_REQUIRED", "HILBERT_FLUX_LOCK_DERIVED_CONDITIONAL", "EM_STRESS_ROUTING_CLARIFIED", "NEWTON_STILL_UNSIGNED"]
    add("VAL4154_3_theorem", "mu_extra zero theorem reduces to channel locks and mass-flux lock", all(token in theorem_text for token in theorem_tokens), "theorem tokens checked")

    flux_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4154_HILBERT_MASS_FLUX_LOCK"]))
    flux_tokens = ["CANDIDATE_ORIGIN_NOT_COMPLETED", "CONDITIONAL_NOT_PARENT_DERIVED", "NOT_SATISFIED", "NOT_PARENT_DERIVED"]
    add("VAL4154_4_flux", "Hilbert mass-flux lock records projector, current, closure and calibration gaps", all(token in flux_text for token in flux_tokens), "flux tokens checked")

    channel_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4154_CHANNEL_ZERO_AUDIT"]))
    channel_tokens = ["radial_MH_flux", "boundary_topological_monopole", "domain_projector_mass", "bulk_X_Yukawa_tail", "nonEH_operator_potential", "EM_field_stress_and_flux", "epsilon_EM_extra"]
    add("VAL4154_5_channels", "channel audit covers radial, boundary, domain, range, nonEH, source/frame, EM and calibration channels", all(token in channel_text for token in channel_tokens), "channel tokens checked")

    runner_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4154_SOURCE_NORMALIZATION_RUNNER_ROWS"]))
    runner_tokens = ["NOT_SCOREABLE_CHANNELS_UNSIGNED", "NOT_SCOREABLE_FLUX_UNSIGNED", "CONDITIONAL_ZERO_OR_COEFFICIENT_REQUIRED", "DEFERRED_UNTIL_FIRST_ORDER_SOURCE_ROWS_CLOSE"]
    add("VAL4154_6_runner", "source-normalization runner rows remain nonclaim and identify required inputs", all(token in runner_text for token in runner_tokens), "runner tokens checked")

    gate_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4154_NEWTON_GATE_STATUS"]))
    gate_tokens = ["CONDITIONAL_MECHANISM_FROM_4153", "UNSIGNED", "FAIL_CURRENT_PROMOTION", "NOT_CLAIMED"]
    add("VAL4154_7_newton_gate", "Newton gate distinguishes kappa progress from mass/mu_extra failures", all(token in gate_text for token in gate_tokens), "gate tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4154_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("mu_extra_sum_rule_derived") == "True"
        and status[0].get("mu_extra_zero_reduced_to_channel_locks") == "True"
        and status[0].get("Hilbert_mass_flux_lock_derived_conditional") == "True"
        and status[0].get("Hilbert_mass_flux_parent_signed") == "False"
        and status[0].get("all_mu_extra_channels_closed") == "False"
        and status[0].get("EM_Poynting_routing_clarified") == "True"
        and status[0].get("Newton_claimed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4154_8_status", "status records derived split, unsigned flux/channels, EM routing and no Newton/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4154_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4155-Y5-R2FR-worldtube-Hilbert-source-measure-and-Poynting-flux-lock.md"
    add("VAL4154_9_next", "next target attacks worldtube source measure and Poynting flux lock", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4154_10_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4154-Y5-R2FR" in item.name or "R2FR_4154" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4154_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4154_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4154_VALIDATION.csv"
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
