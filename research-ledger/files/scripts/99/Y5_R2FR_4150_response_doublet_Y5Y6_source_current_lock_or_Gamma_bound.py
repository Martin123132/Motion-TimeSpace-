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
DOC_PATH = ROOT / "4150-Y5-R2FR-response-doublet-Y5Y6-source-current-lock-or-Gamma-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5Y6_RESPONSE_DOUBLET_SOURCE_CURRENT_LOCK_4150"
CHECKPOINT_ID = "4150"
DECISION = "Y5Y6_SOURCE_CURRENT_LOCK_CONDITIONS_DERIVED_EH_ONLY_AND_TOPOLOGICAL_STRESS_UNSIGNED_BOUND_BRANCH_RETAINED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4150_00_4149_doc": (
        ROOT / "4149-Y5-R2FR-Gamma-eff-extremum-source-zero-lock-or-phi-charge-bound.md",
        "Y5/Y6 source locks",
        "4149 handoff naming Y5/Y6 as the source-current blockers.",
    ),
    "SRC4150_01_4149_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4149_NEXT_TARGET.csv",
        "Y5 and Y6 source currents",
        "Machine-readable 4149 next-target row.",
    ),
    "SRC4150_02_4149_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4149_SOURCE_ZERO_AUDIT.csv",
        "HARD_FAIL_CURRENT",
        "4149 source-zero audit: Y5 hard fail and Y6 retained debt.",
    ),
    "SRC4150_03_response_ledger": (
        SOURCE_DIR / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
        "Y6_stress_Bianchi",
        "Response-doublet Euler source ledger for Y0-Y6 channels.",
    ),
    "SRC4150_04_source_normalization_stack": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "S5_Newton_gate",
        "Source-normalization theorem stack and Newton gate.",
    ),
    "SRC4150_05_local_residual_vector": (
        SOURCE_DIR / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
        "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "Local-GR residual vector row for R11/source-normalization.",
    ),
    "SRC4150_06_source_current_contract": (
        SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv",
        "SC8_second_order_source_stability",
        "Ward/source-current universality contract through beta order.",
    ),
    "SRC4150_07_Ward_owner_contract": (
        SOURCE_DIR / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "C7_second_order_source_closure",
        "Ward source-owner contract and second-order closure debt.",
    ),
    "SRC4150_08_script": (
        SCRIPT_PATH,
        "Y5Y6_SOURCE_CURRENT_LOCK_CONDITIONS_DERIVED_EH_ONLY",
        "This generator records the 4150 source-current lock attempt.",
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
        "P8_Y5_R2FR_4150_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4150_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4150_RESPONSE_CURRENT_LAW": SOURCE_DIR / "P8_Y5_R2FR_4150_RESPONSE_CURRENT_LAW.csv",
        "P8_Y5_R2FR_4150_Y5_SOURCE_NORMALIZATION_LOCK": SOURCE_DIR / "P8_Y5_R2FR_4150_Y5_SOURCE_NORMALIZATION_LOCK.csv",
        "P8_Y5_R2FR_4150_Y6_EXTRA_STRESS_LOCK": SOURCE_DIR / "P8_Y5_R2FR_4150_Y6_EXTRA_STRESS_LOCK.csv",
        "P8_Y5_R2FR_4150_SOURCE_CURRENT_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4150_SOURCE_CURRENT_AUDIT.csv",
        "P8_Y5_R2FR_4150_GAMMA_PHI_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4150_GAMMA_PHI_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4150_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4150_DECISION_GATES.csv",
        "P8_Y5_R2FR_4150_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4150_STATUS.csv",
        "P8_Y5_R2FR_4150_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4150_NEXT_TARGET.csv",
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


def response_current_law_rows() -> List[dict]:
    return [
        {
            **common(),
            "law_id": "RC4150_0_doublet_euler_equation",
            "statement": "response-doublet local branch equation",
            "formula": "L_AB Z^B=J_A+B_A+O(Z^2)",
            "derivation": "4149 gives an even Gamma owner, so the Gamma density contributes no linear force at Z=0. The remaining obstruction is the physical source-current J_A and boundary/collar current B_A.",
            "result": "SOURCE_CURRENT_ZERO_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "law_id": "RC4150_1_branch_shift",
            "statement": "unsigned source currents displace the doublet branch",
            "formula": "Z^A=(L^-1)^AB (J_B+B_B)+O((J+B)^2)",
            "derivation": "If any Y channel carries an exchange-even source current, the local branch is not Z=0; the double-zero Gamma tail is then evaluated on a shifted branch.",
            "result": "BOUND_BRANCH_IF_J_OR_B_NONZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "law_id": "RC4150_2_channel_decomposition",
            "statement": "source-current decomposition",
            "formula": "J_Z=J_Y0+J_Y1+J_Y2+J_Y3+J_Y4+J_Y5+J_Y6",
            "derivation": "The response-doublet route is promoted only if every physical channel is parent-odd/topological/EH-only, or if the nonzero channel is retained as an explicit residual bound.",
            "result": "CHANNELWISE_LOCK_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "law_id": "RC4150_3_gamma_tail_bound",
            "statement": "Gamma source after source-current displacement",
            "formula": "|J_Gamma| <= C_Gamma ||Z|| ||deltaZ|| + C_source ||delta source||",
            "derivation": "The double-zero law changes the leading risk from a first-order Gamma term to a source-current induced tail. That is real progress, but it is not a proof of local GR.",
            "result": "TAIL_BOUND_REPLACES_FIRST_VARIATION_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def y5_source_normalization_rows() -> List[dict]:
    return [
        {
            **common(),
            "lock_id": "Y5LOCK4150_0_problem",
            "channel": "Y5_source_normalization",
            "requirement": "measured-GM/source normalization must not be an independent active source current",
            "formula": "mu_obs=G_ref M_Hilbert + mu_extra",
            "derived_condition": "Y5 is silent only if mu_extra=0, or if mu_extra is a constant universal calibration with no local/range/time/species derivative.",
            "current_status": "FAIL_CURRENT_UNSIGNED",
            "residual_if_failed": "c_domain_source_normalization_operator; D_Geff_mismatch; measured-GM drift; delta_beta_source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "Y5LOCK4150_1_EH_only_route",
            "channel": "Y5_source_normalization",
            "requirement": "same-frame EH/Hilbert source only",
            "formula": "S=(1/2 kappa_*) int sqrt(-g_obs) R[g_obs] + S_matter[psi,g_obs]",
            "derived_condition": "If all observed masses, clocks, and source standards vary the same observed frame and kappa_* is constant, the Newtonian source normalization is EH-owned rather than a Z-current.",
            "current_status": "EH_ONLY_SOURCE_CONTRACT_DERIVED_NOT_PARENT_SIGNED",
            "residual_if_failed": "R11 source-normalization remains active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "Y5LOCK4150_2_no_absorption_rule",
            "channel": "Y5_source_normalization",
            "requirement": "do not hide physics by redefining measured GM",
            "formula": "partial_t mu_extra=partial_r mu_extra=partial_lambda mu_extra=partial_A mu_extra=0",
            "derived_condition": "A one-point calibration is legal; absorbing range/time/species/radial dependence into GM is not. Any derivative revives fifth-force, clock, orbital, or PPN rows.",
            "current_status": "NO_ABSORPTION_RULE_DERIVED_NOT_SATISFIED",
            "residual_if_failed": "Gdot/source-charge/R10/radial-hair residual rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "Y5LOCK4150_3_verdict",
            "channel": "Y5_source_normalization",
            "requirement": "Y5 current is zero or explicitly bounded",
            "formula": "J_Y5=delta_Z mu_extra|_{Z=0}=0",
            "derived_condition": "Current corpus gives the right contract but not the parent signature. Therefore Y5 cannot be promoted; it must become the next derivation target or remain a bound row.",
            "current_status": "Y5_LOCK_UNSIGNED",
            "residual_if_failed": "J_Y5 and c_domain_source_normalization_operator",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def y6_extra_stress_rows() -> List[dict]:
    return [
        {
            **common(),
            "lock_id": "Y6LOCK4150_0_problem",
            "channel": "Y6_stress_Bianchi",
            "requirement": "conserved extra stress must be invisible, topological, or explicitly bounded",
            "formula": "nabla_mu T_extra^{mu nu}=0 does not imply T_extra^{mu nu}=0",
            "derived_condition": "Bianchi conservation is a consistency condition, not a silence theorem. A conserved anisotropic/source stress can still change beta, gamma, alpha_i, xi, or clock/orbital observables.",
            "current_status": "RETAINED_DEBT",
            "residual_if_failed": "T_extra; projector/domain metric stress; beta/gamma/alpha_i residuals",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "Y6LOCK4150_1_topological_route",
            "channel": "Y6_stress_Bianchi",
            "requirement": "extra stress is an improvement/topological current with zero readout",
            "formula": "T_extra^{mu nu}=nabla_alpha nabla_beta U^{mu alpha nu beta}, Pi_PPN[T_extra]=0, and boundary projection=0",
            "derived_condition": "If the parent action writes Y6 only as a superpotential/improvement whose bulk and boundary PPN projections vanish, then Y6 is Bianchi-owned and locally silent.",
            "current_status": "TOPOLOGICAL_IMPROVEMENT_CONTRACT_DERIVED_NOT_PARENT_SIGNED",
            "residual_if_failed": "T_extra retained in local residual vector",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "Y6LOCK4150_2_isotropic_background_route",
            "channel": "Y6_stress_Bianchi",
            "requirement": "isotropic vacuum/background part is not mistaken for PPN silence",
            "formula": "T_extra^{mu nu}=-rho_Lambda g^{mu nu}+Delta T_extra^{mu nu}, require Pi_PPN[Delta T_extra]=0",
            "derived_condition": "A cosmological-constant-like background can be subtracted/calibrated, but local anisotropic gradients or finite-source pieces cannot be ignored.",
            "current_status": "BACKGROUND_ROUTE_CONDITIONAL",
            "residual_if_failed": "Delta T_extra PPN stress vector",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "lock_id": "Y6LOCK4150_3_verdict",
            "channel": "Y6_stress_Bianchi",
            "requirement": "Y6 current is zero/topological or explicitly bounded",
            "formula": "J_Y6=delta_Z int sqrt(-g) T_extra^{mu nu} h_{mu nu}|_{Z=0}=0",
            "derived_condition": "Current corpus gives no parent-owned superpotential or zero PPN projection. Therefore Y6 remains retained debt, not a live source-current lock.",
            "current_status": "Y6_LOCK_UNSIGNED",
            "residual_if_failed": "J_Y6 and T_extra",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def source_current_audit_rows() -> List[dict]:
    return [
        {
            **common(),
            "audit_id": "SCA4150_0_response_doublet",
            "gate": "Gamma double-zero suppresses only the Gamma first variation",
            "formula": "Gamma_eff+C=O(Z^2)",
            "current_status": "PASSED_FROM_4149",
            "residual_if_failed": "first-variation Gamma source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "SCA4150_1_JZ_zero",
            "gate": "total response-doublet source current is zero",
            "formula": "J_Z=J_Y5+J_Y6+J_other=0",
            "current_status": "SOURCE_CURRENT_ZERO_NOT_LIVE",
            "residual_if_failed": "Z branch shift and J_Gamma tail",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "SCA4150_2_boundary_zero",
            "gate": "compact boundary/collar current is zero",
            "formula": "B_Z=0",
            "current_status": "BOUNDARY_ZERO_UNSIGNED_FOR_THIS_ROUTE",
            "residual_if_failed": "boundary alpha3/source-normalization tails",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "SCA4150_3_Y5",
            "gate": "Y5 source-normalization is EH-only or bounded",
            "formula": "J_Y5=delta_Z mu_extra|_0=0",
            "current_status": "Y5_LOCK_UNSIGNED",
            "residual_if_failed": "c_domain_source_normalization_operator",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "SCA4150_4_Y6",
            "gate": "Y6 extra stress is topological/invisible or bounded",
            "formula": "Pi_PPN[T_extra]=0",
            "current_status": "Y6_LOCK_UNSIGNED",
            "residual_if_failed": "T_extra",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "SCA4150_5_verdict",
            "gate": "response-doublet branch promotes to local-GR source silence",
            "formula": "parent_signed(Gamma double-zero, J_Z=0, B_Z=0, Y5=0, Y6=0, PPN lock)",
            "current_status": "FAIL_CURRENT_PROMOTION",
            "residual_if_failed": "Gamma/phi/q_loc/source-normalization bound branch retained",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[dict]:
    return [
        {
            **common(),
            "bound_id": "B4150_0_JY5",
            "quantity": "J_Y5",
            "symbolic_bound": "|J_Y5| <= |delta_Z mu_extra|_0| + |partial_t mu_extra| + |partial_r mu_extra| + |partial_lambda mu_extra| + |partial_A mu_extra|",
            "feeds": "c_domain_source_normalization_operator; D_Geff_mismatch; delta_beta_source",
            "status": "MISSING_PARENT_EH_ONLY_SOURCE_LOCK",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "bound_id": "B4150_1_JY6",
            "quantity": "J_Y6",
            "symbolic_bound": "|J_Y6| <= ||Pi_PPN[T_extra]|| + ||boundary_projection(T_extra)|| + ||anisotropic_gradient(T_extra)||",
            "feeds": "T_extra; beta/gamma/alpha_i/xi residuals",
            "status": "MISSING_PARENT_TOPOLOGICAL_STRESS_LOCK",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "bound_id": "B4150_2_Z_shift",
            "quantity": "Z_branch_shift",
            "symbolic_bound": "||Z|| <= ||L^-1|| (||J_Y5||+||J_Y6||+||J_other||+||B_Z||) + O(||J+B||^2)",
            "feeds": "response-doublet branch displacement",
            "status": "BOUND_BRANCH",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "bound_id": "B4150_3_JGamma_tail",
            "quantity": "J_Gamma_tail",
            "symbolic_bound": "|J_Gamma| <= C_Gamma ||Z|| ||deltaZ|| + C_source ||delta source||",
            "feeds": "Q_phi; q_loc; local-GR residual vector",
            "status": "TAIL_BOUND_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "bound_id": "B4150_4_Qphi_q_loc",
            "quantity": "Q_phi and q_loc",
            "symbolic_bound": "|Q_phi|+||q_loc|| <= C_phi (|J_Gamma|+|J_Y5|+|J_Y6|+|B_Z|+|J_matter|)",
            "feeds": "PPN beta/source, clocks, orbital, R10/local-GR gates",
            "status": "RETAINED_LOCAL_GR_INTERFACE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "DG4150_0_Gamma",
            "question": "does the response-doublet construction remove the first-order Gamma source?",
            "answer": "yes, conditionally from 4149",
            "decision": "KEEP_RESPONSE_DOUBLET_ROUTE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "gate_id": "DG4150_1_Y5",
            "question": "is Y5 source-normalization EH-only or parent-zero?",
            "answer": "no current parent signature",
            "decision": "NEXT_TARGET_Y5_EH_ONLY_SOURCE_LOCK",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "gate_id": "DG4150_2_Y6",
            "question": "is Y6 extra stress topological/invisible?",
            "answer": "no current parent superpotential or zero PPN projection",
            "decision": "RETAIN_Y6_T_EXTRA_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "gate_id": "DG4150_3_local_GR",
            "question": "can local GR/Newton be claimed from this checkpoint?",
            "answer": "no",
            "decision": DECISION,
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "response_doublet_current_law_derived": "True",
            "Y5_EH_only_contract_derived": "True",
            "Y6_topological_stress_contract_derived": "True",
            "Y5_lock_parent_signed": "False",
            "Y6_lock_parent_signed": "False",
            "J_Z_zero_claimed": "False",
            "B_Z_zero_claimed": "False",
            "Gamma_bound_branch_retained": "True",
            "local_gr_claimed": "False",
            "next_target": "4151-Y5-R2FR-EH-only-source-normalization-lock-or-measured-GM-residual.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4150_0",
            "target_doc": "4151-Y5-R2FR-EH-only-source-normalization-lock-or-measured-GM-residual.md",
            "target_script": "scripts/Y5_R2FR_4151_EH_only_source_normalization_lock_or_measured_GM_residual.py",
            "objective": "attack the dominant Y5/Newton coupling blocker directly: prove same-frame EH-only source normalization with constant kappa and no mu_extra derivatives, or emit the measured-GM/source-normalization residual rows needed for testing",
            "success_gate": "parent-signed same-frame Hilbert source, constant universal kappa, no non-Hilbert source current, closed calibrated mass projector, and second-order beta source closure; otherwise explicit residuals remain nonclaim",
            "reason": "Y5 is the cleanest next route because it touches Newton's constant, measured GM, PPN beta/source normalization, R10, clocks, and orbital tests before Y6 stress can be cleanly interpreted.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4150 - Y5/Y6 Response-Doublet Source-Current Lock Or Gamma Bound

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
This checkpoint tries to push the 4149 response-doublet route forward instead of just naming the missing coupling.

4149 got a real structural win:

`Gamma_eff+C=O(Z^2)`

so the direct first variation of `Gamma_eff` can vanish at the exact local branch `Z=0`.

The remaining question is whether the physical branch is actually `Z=0`.

## Source-current law
For a response doublet,

`L_AB Z^B=J_A+B_A+O(Z^2)`.

Here:

- `J_A` is the bulk source current from the active channels;
- `B_A` is the boundary/collar source current;
- `Z=0` is an exact local branch only if `J_A=0` and `B_A=0`.

If the source current is not zero, the branch shifts:

`Z^A=(L^-1)^AB (J_B+B_B)+O((J+B)^2)`.

Then the 4149 double-zero is still useful, but it becomes a bound:

`|J_Gamma| <= C_Gamma ||Z|| ||deltaZ|| + C_source ||delta source||`.

That is progress, not a local-GR proof.

## Y5 source-normalization result
The Y5 channel is the coupling/`G`/measured-GM problem in disguise.

Write:

`mu_obs=G_ref M_Hilbert + mu_extra`.

Y5 is silent only if the source normalization is genuinely EH/Hilbert-owned in the same observed frame, with constant universal `kappa_*`, or if every non-EH source offset obeys:

`mu_extra=0`

or at least

`partial_t mu_extra=partial_r mu_extra=partial_lambda mu_extra=partial_A mu_extra=0`.

This is the exact no-absorption rule: a one-point calibration is allowed, but hiding time/range/species/radial physics inside measured GM is not.

Current status: the contract is now sharp, but the parent signature is not present. Therefore `Y5_source_normalization` remains `Y5_LOCK_UNSIGNED`, with `c_domain_source_normalization_operator`, `D_Geff_mismatch`, and `delta_beta_source` retained.

## Y6 extra-stress result
Bianchi conservation alone is not a silence theorem:

`nabla_mu T_extra^{{mu nu}}=0`

does not imply

`T_extra^{{mu nu}}=0`.

Y6 becomes locally silent only if the parent action makes it a topological/improvement stress:

`T_extra^{{mu nu}}=nabla_alpha nabla_beta U^{{mu alpha nu beta}}`,

with

`Pi_PPN[T_extra]=0`

and zero boundary projection, or if only an isotropic background piece survives and every local anisotropic/gradient part vanishes.

Current status: no parent-owned superpotential or zero PPN projection is present. Therefore `Y6_stress_Bianchi` remains retained debt, with `T_extra` retained.

## What actually moved
This checkpoint reduces the live obstruction to two exact contracts:

1. **Y5 / coupling / Newton source normalization:** prove same-frame EH-only source normalization with constant universal coupling, or keep measured-GM/source-normalization residuals.
2. **Y6 / extra stress:** prove topological/improvement stress with zero PPN and boundary projection, or keep `T_extra`.

The work is no longer "maybe the coupling is missing"; the coupling problem is now the explicit `Y5` theorem target.

## Current verdict
| Gate | Result | Meaning |
|---|---|---|
| Gamma double-zero | PASSED CONDITIONALLY | direct first variation suppressed by 4149 |
| response source current | NOT LIVE | requires `J_Z=0` and `B_Z=0` |
| Y5 source normalization | UNSIGNED | exact EH-only source contract derived, not parent-signed |
| Y6 extra stress | UNSIGNED | exact topological/invisible stress contract derived, not parent-signed |
| local GR/Newton | NOT CLAIMED | bound branch retained |

## Outputs
- `{outputs["P8_Y5_R2FR_4150_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4150_RESPONSE_CURRENT_LAW"]}`
- `{outputs["P8_Y5_R2FR_4150_Y5_SOURCE_NORMALIZATION_LOCK"]}`
- `{outputs["P8_Y5_R2FR_4150_Y6_EXTRA_STRESS_LOCK"]}`
- `{outputs["P8_Y5_R2FR_4150_SOURCE_CURRENT_AUDIT"]}`
- `{outputs["P8_Y5_R2FR_4150_GAMMA_PHI_BOUND_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4150_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4150_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4150_NEXT_TARGET"]}`

## Next Target
- `4151-Y5-R2FR-EH-only-source-normalization-lock-or-measured-GM-residual.md`
- Go straight at the coupling/Newton problem: derive the same-frame EH-only source normalization and constant universal `kappa_*`, or make the measured-GM/source-normalization residual executable for testing.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4150_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4150_RESPONSE_CURRENT_LAW"], response_current_law_rows())
    write_csv(outputs["P8_Y5_R2FR_4150_Y5_SOURCE_NORMALIZATION_LOCK"], y5_source_normalization_rows())
    write_csv(outputs["P8_Y5_R2FR_4150_Y6_EXTRA_STRESS_LOCK"], y6_extra_stress_rows())
    write_csv(outputs["P8_Y5_R2FR_4150_SOURCE_CURRENT_AUDIT"], source_current_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4150_GAMMA_PHI_BOUND_ROWS"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4150_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4150_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4150_NEXT_TARGET"], next_rows())
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
        "VAL4150_0_sources",
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
    add("VAL4150_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "L_AB Z^B=J_A+B_A",
        "Y5_source_normalization",
        "Y6_stress_Bianchi",
        "c_domain_source_normalization_operator",
        "T_extra",
        "4151-Y5-R2FR-EH-only-source-normalization-lock-or-measured-GM-residual.md",
    ]
    add("VAL4150_2_doc_tokens", "document records source-current law, Y5/Y6 contracts, retained bounds and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    law_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4150_RESPONSE_CURRENT_LAW"]))
    law_tokens = ["L_AB Z^B=J_A+B_A", "Z^A=(L^-1)^AB", "J_Z=J_Y0+J_Y1+J_Y2+J_Y3+J_Y4+J_Y5+J_Y6", "TAIL_BOUND_REPLACES_FIRST_VARIATION_BOUND"]
    add("VAL4150_3_current_law", "response current law and shifted-branch tail bound are recorded", all(token in law_text for token in law_tokens), "law tokens checked")

    y5_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4150_Y5_SOURCE_NORMALIZATION_LOCK"]))
    y5_tokens = ["Y5_source_normalization", "EH_ONLY_SOURCE_CONTRACT_DERIVED_NOT_PARENT_SIGNED", "NO_ABSORPTION_RULE_DERIVED_NOT_SATISFIED", "Y5_LOCK_UNSIGNED", "c_domain_source_normalization_operator"]
    add("VAL4150_4_Y5", "Y5 EH-only source-normalization contract is derived but unsigned", all(token in y5_text for token in y5_tokens), "Y5 tokens checked")

    y6_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4150_Y6_EXTRA_STRESS_LOCK"]))
    y6_tokens = ["Y6_stress_Bianchi", "TOPOLOGICAL_IMPROVEMENT_CONTRACT_DERIVED_NOT_PARENT_SIGNED", "BACKGROUND_ROUTE_CONDITIONAL", "Y6_LOCK_UNSIGNED", "T_extra"]
    add("VAL4150_5_Y6", "Y6 topological/invisible stress contract is derived but unsigned", all(token in y6_text for token in y6_tokens), "Y6 tokens checked")

    audit_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4150_SOURCE_CURRENT_AUDIT"]))
    audit_tokens = ["PASSED_FROM_4149", "SOURCE_CURRENT_ZERO_NOT_LIVE", "Y5_LOCK_UNSIGNED", "Y6_LOCK_UNSIGNED", "FAIL_CURRENT_PROMOTION"]
    add("VAL4150_6_audit", "audit records Gamma pass, J/B source-current blockers, Y5/Y6 blockers and no promotion", all(token in audit_text for token in audit_tokens), "audit tokens checked")

    bound_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4150_GAMMA_PHI_BOUND_ROWS"]))
    bound_tokens = ["J_Y5", "J_Y6", "Z_branch_shift", "J_Gamma_tail", "Q_phi and q_loc"]
    add("VAL4150_7_bounds", "bound rows cover Y5, Y6, branch shift, Gamma tail, phi and q_loc interface", all(token in bound_text for token in bound_tokens), "bound tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4150_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("response_doublet_current_law_derived") == "True"
        and status[0].get("Y5_EH_only_contract_derived") == "True"
        and status[0].get("Y6_topological_stress_contract_derived") == "True"
        and status[0].get("Y5_lock_parent_signed") == "False"
        and status[0].get("Y6_lock_parent_signed") == "False"
        and status[0].get("J_Z_zero_claimed") == "False"
        and status[0].get("B_Z_zero_claimed") == "False"
        and status[0].get("Gamma_bound_branch_retained") == "True"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4150_8_status", "status records derived contracts, unsigned Y5/Y6 locks, retained bounds and no local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4150_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4151-Y5-R2FR-EH-only-source-normalization-lock-or-measured-GM-residual.md"
    add("VAL4150_9_next", "next target attacks Y5 EH-only source normalization or measured-GM residuals", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4150_10_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4150-Y5-R2FR" in item.name or "R2FR_4150" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4150_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4150_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4150_VALIDATION.csv"
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
