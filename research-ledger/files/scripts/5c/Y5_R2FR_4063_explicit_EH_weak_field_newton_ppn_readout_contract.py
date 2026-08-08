from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4063-Y5-R2FR-explicit-EH-weak-field-newton-ppn-readout-contract.md"

DECISION = "EH_SAME_SOURCE_WEAK_FIELD_READOUT_CONTRACT_DERIVES_NEWTON_PPN_CONDITIONALLY"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4063_00_4062_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4062_NEXT_TARGET.csv",
        "explicitly derive the weak-field EH-to-Newton/PPN readout",
        "4062 selected explicit weak-field readout as the next target.",
    ),
    "SRC4063_01_4062_reduction": (
        SOURCE_DIR / "P8_Y5_R2FR_4062_NEWTON_GR_REDUCTION_CONTRACT.csv",
        "NRC4062_0_EH_source",
        "4062 names the EH 00 equation and same Hilbert source as the Newton gate.",
    ),
    "SRC4063_02_4062_calibration": (
        SOURCE_DIR / "P8_Y5_R2FR_4062_CNORM_NEWTON_G_CALIBRATION_LAW.csv",
        "G_N := c^4 kappa_eff/(8*pi)",
        "4062 fixes the calibrated universal coupling convention.",
    ),
    "SRC4063_03_4056_local_gr": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_CONDITIONAL_LOCAL_GR_THEOREM.csv",
        "LGT4056_2_PPN",
        "4056 states the conditional PPN zero vector under the parent packet.",
    ),
    "SRC4063_04_4056_packet": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_LOCAL_PARENT_ACTION_PACKET.csv",
        "S_EH[g_obs;kappa_*]",
        "4056 supplies the EH plus same-source matter/EM local packet.",
    ),
    "SRC4063_05_4056_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_PACKET_ADOPTION_GATE.csv",
        "ADOPT4056_5_public_claim",
        "4056 keeps public local-GR claim blocked until adoption/fallback rows pass.",
    ),
    "SRC4063_06_newton_stack": (
        SOURCE_DIR / "P8_source_normalized_Newton_branch_STACK.csv",
        "SN5_EH_to_Poisson_coefficient",
        "older Newton stack contains the coefficient check for EH to Poisson.",
    ),
    "SRC4063_07_source_norm_stack": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "S5_Newton_gate",
        "source-normalization stack records the older Newton promotion gate.",
    ),
    "SRC4063_08_4047_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4047_SELECTED_ZERO_THEOREM.csv",
        "CZT4047_4_total_zero",
        "4047 supplies c_norm derivative-hair silence for the selected branch.",
    ),
    "SRC4063_09_4061_cdb": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_DECISION_GATE.csv",
        "K_conn=K_domain=K_boundary=0",
        "4061 closes first-order connection/domain/boundary kernels in the selected branch.",
    ),
    "SRC4063_10_4060_chain": (
        SOURCE_DIR / "P8_Y5_R2FR_4060_DECISION_GATE.csv",
        "CHAIN_RESPONSE_FIRST_VARIATION_ZERO",
        "4060 closes the m/L_cg chain first variation in the parent normal-ordered branch.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4063_SOURCE_REGISTER.csv",
    "assumption_contract": SOURCE_DIR / "P8_Y5_R2FR_4063_WEAK_FIELD_ASSUMPTION_CONTRACT.csv",
    "newton_derivation": SOURCE_DIR / "P8_Y5_R2FR_4063_NEWTON_POISSON_DERIVATION.csv",
    "ppn_readout": SOURCE_DIR / "P8_Y5_R2FR_4063_PPN_READOUT_VECTOR.csv",
    "residual_fallback": SOURCE_DIR / "P8_Y5_R2FR_4063_RESIDUAL_FALLBACK_VECTOR.csv",
    "decision": SOURCE_DIR / "P8_Y5_R2FR_4063_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4063_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4063_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4063_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4063_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, source_tuple in SOURCES.items():
        path, needle, role = source_tuple
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def assumption_contract_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "assumption_id": "WFA4063_0_action",
            "requirement": "selected local parent packet reduces through <=2PN to EH plus minimally/same-source coupled matter and EM",
            "mathematical_form": "S_loc^{<=2PN}=S_EH[g_obs;kappa_eff]+S_matter[psi,g_obs]+S_EM[A,g_obs]+silent/topological/double-zero sectors",
            "if_satisfied": "field equation is G_{mu nu}[g_obs]+Lambda g_{mu nu}=kappa_eff T^H_{mu nu}+O(R_silent)",
            "if_failed": "weak-field readout is not a GR reduction; failed term enters residual fallback vector",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "assumption_id": "WFA4063_1_coupling",
            "requirement": "one calibrated universal coupling",
            "mathematical_form": "G_N := c^4 kappa_eff/(8*pi), D_t,r,lambda,A,frame G_N=0",
            "if_satisfied": "Newton coefficient is one constant common mode, not hidden derivative hair",
            "if_failed": "Gdot, inverse-square/range, WEP/species, and frame residual bounds activate",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "assumption_id": "WFA4063_2_source",
            "requirement": "same Hilbert source mass",
            "mathematical_form": "T^H_{00}=rho_H c^2+O(v^2 rho_H), M_H=int rho_H d^3x, mu_extra=0",
            "if_satisfied": "the mass sourcing curvature is the mass read by Newtonian/orbital tests",
            "if_failed": "source-charge, boundary, projector, memory, or nonEH monopole residuals activate",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "assumption_id": "WFA4063_3_frame",
            "requirement": "one observed frame/coframe",
            "mathematical_form": "g_obs=e_obs^T eta e_obs; matter, clocks, rods, photons, and source variation use e_obs",
            "if_satisfied": "geodesic/orbital readout uses the same potential that solves the field equation",
            "if_failed": "frame/WEP/clock residuals activate",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "assumption_id": "WFA4063_4_silent_sectors",
            "requirement": "q_loc, chain, connection, domain, boundary, memory, c_norm, and nonEH sectors do not contribute through the stated order",
            "mathematical_form": "R_silent=R_qloc+R_chain+R_CDB+R_mem+R_cnorm+R_nonEH=0",
            "if_satisfied": "EH weak-field theorem can be used without extra local-force slots",
            "if_failed": "corresponding 4060/4061/4062/4056 fallback row remains live",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def newton_derivation_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "step_id": "NPD4063_0_field_equation",
            "calculation": "vary S_EH[g_obs;kappa_eff]+S_matter with fixed kappa_eff",
            "formula": "G_{mu nu}^{(1)} = kappa_eff T^H_{mu nu} at leading weak-field order",
            "result": "the linearized observed metric is sourced only by the Hilbert stress",
            "status": "STANDARD_EH_VARIATION_IMPORTED_CONDITIONALLY",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "NPD4063_1_metric_ansatz",
            "calculation": "choose Newtonian potential convention Phi_N with acceleration a=-grad Phi_N",
            "formula": "g_00=-(1+2 Phi_N/c^2)+O(c^-4), g_ij=delta_ij+O(c^-2), T_00^H=rho_H c^2+O(rho v^2)",
            "result": "the 00 equation reads the nonrelativistic source density rho_H",
            "status": "WEAK_FIELD_CONVENTION_DECLARED",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "NPD4063_2_00_component",
            "calculation": "linearized EH 00 component in the Newtonian slow-motion limit",
            "formula": "G_00^{(1)} = 2 nabla^2 Phi_N/c^2 + O(c^-4)",
            "result": "2 nabla^2 Phi_N/c^2 = kappa_eff rho_H c^2",
            "status": "WEAK_FIELD_COEFFICIENT_EXPLICIT",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "NPD4063_3_poisson",
            "calculation": "insert G_N=c^4 kappa_eff/(8*pi)",
            "formula": "nabla^2 Phi_N = 4*pi*G_N*rho_H",
            "result": "Newton/Poisson equation follows with calibrated universal G_N",
            "status": "NEWTON_POISSON_LIMIT_CONDITIONAL",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "NPD4063_4_gauss_kepler",
            "calculation": "integrate Poisson over compact support and use no extra monopole",
            "formula": "surface_integral grad Phi_N.dS = 4*pi*G_N*M_H; outside support Phi_N=-G_N*M_H/r + const; a_r=-G_N*M_H/r^2",
            "result": "the orbital Kepler mass is the same Hilbert mass appearing in the field equation",
            "status": "GAUSS_AND_ORBITAL_READOUT_CONDITIONAL",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def ppn_readout_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "ppn_id": "PPN4063_0_gamma",
            "parameter": "gamma",
            "readout_formula": "g_ij=(1-2 gamma Phi_N/c^2) delta_ij+O(c^-4) in the same potential convention",
            "selected_branch_value": "1",
            "reason": "pure EH metric action with minimal same-frame matter has the GR spatial-curvature coefficient",
            "fallback_if_unsigned": "gamma_minus_1 bound from nonEH/operator/frame residuals",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "ppn_id": "PPN4063_1_beta",
            "parameter": "beta",
            "readout_formula": "g_00=-(1+2 Phi_N/c^2+2 beta Phi_N^2/c^4)+O(c^-6) up to sign convention for Phi_N",
            "selected_branch_value": "1",
            "reason": "EH nonlinearity fixes the GR second-order self-coupling when no extra scalar/source-normalization hair remains",
            "fallback_if_unsigned": "delta_beta_source bound from quadratic/nonEH/source residuals",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "ppn_id": "PPN4063_2_preferred_frame",
            "parameter": "alpha1, alpha2, alpha3",
            "readout_formula": "preferred-frame/vector PPN projections of local source/frame/domain currents",
            "selected_branch_value": "0,0,0",
            "reason": "same observed frame, q-basic domain/projector, no wall flux, and no hidden current in selected compact branch",
            "fallback_if_unsigned": "alpha_i absolute bound vector from frame/domain/current residuals",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "ppn_id": "PPN4063_3_conservation_anisotropy",
            "parameter": "xi, zeta_i",
            "readout_formula": "anisotropic/conservation-violation PPN projections of nonconserved stress or projector/domain leakage",
            "selected_branch_value": "0",
            "reason": "Hilbert same-source stress is conserved under diffeomorphism invariance and 4061 removes domain/boundary/projector kernels",
            "fallback_if_unsigned": "xi/zeta bound rows from projector/domain/conservation residuals",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "ppn_id": "PPN4063_4_gdot",
            "parameter": "Gdot/G",
            "readout_formula": "D_t ln G_N",
            "selected_branch_value": "0",
            "reason": "4062 routes only a constant calibrated coupling into Newton G and forbids derivative hair",
            "fallback_if_unsigned": "Gdot clock/orbital bound row",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "ppn_id": "PPN4063_5_master",
            "parameter": "Delta_PPN_abs",
            "readout_formula": "|gamma-1|+|beta-1|+sum|alpha_i|+|xi|+sum|zeta_i|+|Gdot/G|",
            "selected_branch_value": "0",
            "reason": "zero only if all 4063 assumptions and prior selected-branch silence clauses are parent-adopted together",
            "fallback_if_unsigned": "no-cancellation PPN residual vector",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def residual_fallback_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "RFB4063_0_nonEH",
            "if_clause_fails": "EH-only operator through <=2PN is rejected",
            "residual_formula": "R_nonEH = sum_i c_i O_i[g,Y]",
            "observable_map": "gamma-1, beta-1, alpha(lambda), orbital perihelion, light bending",
            "needed_inputs": "operator basis, coefficients, weak-field projection",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RFB4063_1_source_mismatch",
            "if_clause_fails": "Hilbert source mass differs from orbital/readout mass",
            "residual_formula": "mu_obs = G_N M_H + mu_extra",
            "observable_map": "Kepler GM, WEP, clocks, PPN zeta_i",
            "needed_inputs": "mu_extra decomposition and source-backed bounds",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RFB4063_2_frame",
            "if_clause_fails": "matter/clocks/photons/source variation do not use one observed frame",
            "residual_formula": "Delta_frame = ||e_source-e_obs|| + ||e_matter-e_obs|| + ||e_clock-e_obs||",
            "observable_map": "WEP, redshift, alpha_i, light propagation",
            "needed_inputs": "frame map and PPN/clock projection weights",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RFB4063_3_derivative_hair",
            "if_clause_fails": "G_N or M_H carries time/range/source/species/frame derivatives",
            "residual_formula": "Delta_deriv = |D ln G_N| + |D ln M_H|",
            "observable_map": "Gdot, R10 inverse-square, WEP/species, radial/orbital drift",
            "needed_inputs": "derivative convention and arena-specific bounds",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RFB4063_4_master",
            "if_clause_fails": "any weak-field readout assumption is unsigned",
            "residual_formula": "Delta_weakfield <= |R_nonEH|+|mu_extra|+Delta_frame+Delta_deriv+Delta_PPN_residual",
            "observable_map": "combined local GR/Newton/PPN no-cancellation score",
            "needed_inputs": "all residual rows above",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "decision": [
            {
                "decision_id": "DEC4063_0",
                "decision": DECISION,
                "private_result": "if the selected local parent packet is adopted, the EH weak-field calculation gives Poisson/Newton and GR PPN values with the same Hilbert source and calibrated G_N",
                "public_result": "blocked until formal adoption and fallback-score verification",
                "valid_for_public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4063_0",
                "claim": "selected parent branch conditionally derives Newton/Poisson from EH plus same Hilbert source",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "conditional on parent packet adoption and prior silence gates",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4063_1",
                "claim": "selected parent branch conditionally gives GR PPN values gamma=beta=1 and alpha_i=xi=zeta_i=0",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "standard EH/minimal-matter readout but still not formal public MTS theorem",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4063_2",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "formal adoption and fallback verification remain absent",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4063_3",
                "claim": "MTS predicts the numerical value of Newton's constant",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "G_N is calibrated as one universal constant, not predicted numerically",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4063_0",
                "next_doc": "4064-Y5-R2FR-formal-adoption-preflight-for-4060-4063-local-GR-chain.md",
                "next_script": "scripts/Y5_R2FR_4064_formal_adoption_preflight_for_4060_4063_local_GR_chain.py",
                "reason": "after explicit weak-field readout, run a preflight deciding whether 4060-4063 can be folded into formalization-workbench as one guarded local-GR chain",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4063",
                "status": "EXPLICIT_EH_WEAK_FIELD_NEWTON_PPN_READOUT_CONTRACT_READY_PRIVATE_NONCLAIM",
                "local_GR_claim": False,
                "public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
    }


def validate_sources(source_table: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in source_table if not row["exists"]]
    absent_needles = [row["source_id"] for row in source_table if not row["needle_found"]]
    if missing or absent_needles:
        return False, f"missing={missing}; absent_needles={absent_needles}"
    return True, "all cited source paths exist and needles are present"


def validate_csv_parse(paths: Iterable[Path]) -> Tuple[bool, str]:
    details: List[str] = []
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as input_file:
                parsed_rows = list(csv.DictReader(input_file))
            details.append(f"{path.name}:rows={len(parsed_rows)}")
    except Exception as exc:  # pragma: no cover
        return False, repr(exc)
    return True, "; ".join(details)


def validate_no_public_claim(row_groups: Iterable[List[Dict[str, object]]]) -> Tuple[bool, str]:
    offenders: List[str] = []
    for rows in row_groups:
        for row in rows:
            for key in ("valid_for_public_claim", "allowed_public", "public_claim", "local_GR_claim"):
                if key in row and str(row[key]).lower() == "true":
                    offenders.append(str(row))
    if offenders:
        return False, f"public claim flags found: {offenders}"
    return True, "all claim-bearing rows preserve public false"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    claims_ok, claims_detail = validate_no_public_claim(row_groups)
    compile_ok, compile_detail = validate_script_compile()
    formal_outputs = list(FORMALIZATION.rglob("*4063*")) if FORMALIZATION.exists() else []
    joined = str(row_groups)
    return [
        {"check_id": "VAL4063_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4063_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4063_02_no_public_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4063_03_newton_coefficient",
            "passed": "nabla^2 Phi_N = 4*pi*G_N*rho_H" in joined,
            "detail": "Poisson coefficient row is present",
        },
        {
            "check_id": "VAL4063_04_ppn_vector",
            "passed": all(marker in joined for marker in ("gamma", "beta", "alpha1, alpha2, alpha3", "xi, zeta_i")),
            "detail": "PPN gamma/beta/preferred-frame/conservation rows are present",
        },
        {
            "check_id": "VAL4063_05_no_numerical_G_claim",
            "passed": "not predicted numerically" in joined,
            "detail": "numerical G prediction remains explicitly forbidden",
        },
        {
            "check_id": "VAL4063_06_no_formalization_outputs",
            "passed": len(formal_outputs) == 0,
            "detail": "4063 writes only post-checkpoint/source-intake outputs" if not formal_outputs else str(formal_outputs),
        },
        {"check_id": "VAL4063_07_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4063 - Explicit EH Weak-Field Newton/PPN Readout Contract

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## Readout Result

4063 makes the conditional local-GR route explicit. If the selected local parent packet is adopted so that:

```text
G_mu_nu[g_obs] = kappa_eff T^H_mu_nu
G_N := c^4 kappa_eff/(8*pi)
```

with one observed frame, one same Hilbert source, and no first/second-order silent-sector leakage, then the weak-field 00 equation gives:

```text
G_00^(1) = 2 nabla^2 Phi_N/c^2
T_00^H = rho_H c^2
nabla^2 Phi_N = 4*pi*G_N*rho_H.
```

For compact support and no extra monopole:

```text
surface_integral grad Phi_N.dS = 4*pi*G_N*M_H
a_r = -G_N*M_H/r^2.
```

So Newton is not inserted as a plateau axiom in this branch; it is inherited from the EH weak-field equation with calibrated `G_N`.

## PPN Readout

Under the same EH/minimal same-source assumptions:

```text
gamma = 1
beta = 1
alpha1 = alpha2 = alpha3 = 0
xi = zeta_i = 0
Gdot/G = 0.
```

This is still conditional/private. If any assumption fails, the failed term goes to the residual fallback vector with no cancellation credit.

## What Remains

The next move is not another local term hunt. It is a formal-adoption preflight for the whole `4060-4063` chain: decide whether it can be folded into `formalization-workbench` as one guarded local-GR chain, or whether a named fallback scorer remains the honest state.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    assumptions = assumption_contract_rows(current_timestamp)
    newton = newton_derivation_rows(current_timestamp)
    ppn = ppn_readout_rows(current_timestamp)
    fallback = residual_fallback_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["assumption_contract"], assumptions)
    write_csv(OUTPUTS["newton_derivation"], newton)
    write_csv(OUTPUTS["ppn_readout"], ppn)
    write_csv(OUTPUTS["residual_fallback"], fallback)
    write_csv(OUTPUTS["decision"], static["decision"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["assumption_contract"],
        OUTPUTS["newton_derivation"],
        OUTPUTS["ppn_readout"],
        OUTPUTS["residual_fallback"],
        OUTPUTS["decision"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        assumptions,
        newton,
        ppn,
        fallback,
        static["decision"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, row_groups)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
