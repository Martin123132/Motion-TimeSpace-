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

CHECKPOINT = "4202"
CLAIM_ID = "L-043"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_TENSOR_OPERATOR_LT_4202"
DECISION = (
    "PARENT_TENSOR_OPERATOR_LT_COHERCIVITY_FORMULA_DERIVED_CONDITIONALLY_"
    "ZT_MT2_LAMBDAD_SOURCE_PACK_MISSING_NONCLAIM"
)
FORMAL_PATH = FORMAL / "218-PPC4161-parent-tensor-operator-LT-coercivity.md"
DOC_PATH = POST / "4202-Y5-R2FR-parent-tensor-operator-LT-or-first-Kperp-coefficient-source-pack.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_PARENT_TENSOR_OPERATOR_LT_COHERCIVITY_4202"
PACKET_MARKER = "PPC4161_PACKET_PARENT_TENSOR_OPERATOR_LT_COHERCIVITY_4202"
NEXT_TARGET = "4203-Y5-R2FR-ZT-MT2-lambdaD-source-or-no-physical-Kperp-pole.md"

SOURCES = {
    "SRC4202_00_4201_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4201_DECISION.csv",
        "numeric_score_ready",
        "4201 decision row says PPN inequality map exists but inputs are missing.",
    ),
    "SRC4202_01_4201_operator": (
        SOURCE_DIR / "P8_Y5_R2FR_4201_PARENT_OPERATOR_CONTRACT.csv",
        "LT4201_2_coercivity",
        "4201 parent operator contract.",
    ),
    "SRC4202_02_4201_ppn": (
        SOURCE_DIR / "P8_Y5_R2FR_4201_PPN_INEQUALITY_MAP.csv",
        "clock_delta_z",
        "4201 PPN inequality map.",
    ),
    "SRC4202_03_4200_energy": (
        SOURCE_DIR / "P8_Y5_R2FR_4200_ENERGY_IDENTITY.csv",
        "||K_perp||_E <= C_T",
        "4200 fallback energy inequality.",
    ),
    "SRC4202_04_73_energy": (
        FORMAL / "73-support-powers-kperp-lemma.md",
        "L_T K_perp = 0",
        "Original Kperp positive-operator route.",
    ),
    "SRC4202_05_1035_kernel_analogy": (
        POST / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
        "finite local mode with quadratic residue",
        "Green-kernel precedent: inverse becomes concrete only after Z/range/source normalization exist.",
    ),
    "SRC4202_06_217_formal": (
        FORMAL / "217-PPC4161-Kperp-finite-coefficient-vector.md",
        "C_T, S_T, B_T, I_T, Z_T, W_i^K",
        "4201 formal coefficient vector.",
    ),
}

PPN_BOUNDS = [
    ("delta_phi_fraction", "dimensionless", 1.0e-5),
    ("delta_gamma", "dimensionless", 1.0e-5),
    ("delta_beta", "dimensionless", 1.0e-4),
    ("alpha1", "dimensionless", 1.0e-4),
    ("alpha2", "dimensionless", 1.0e-5),
    ("eta_AB", "dimensionless", 1.0e-13),
    ("Gdot_over_G", "yr^-1", 4.0e-14),
    ("chi_local_leak_fraction", "dimensionless", 1.0e-5),
    ("clock_delta_z", "dimensionless", 1.0e-16),
]


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


def operator_derivation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "OP4202_0_projector_domain",
            "restrict to the transverse local tensor sector",
            "K_perp in T_loc with div K_perp=0 and longitudinal A_loc sector quotiented out",
            "prevents double-counting q_loc current ownership",
            "conditional_requires_parent_projector",
        ),
        (
            "OP4202_1_quadratic_action",
            "take a static quadratic tensor operator",
            "S_K^(2)=1/2 int_W sqrt(h) [Z_T |D K_perp|^2 + M_T^2 |K_perp|^2] - int_W sqrt(h) K_perp:S_T",
            "variation gives L_T K_perp=S_T plus boundary form",
            "derived_conditional_template",
        ),
        (
            "OP4202_2_operator",
            "Euler operator",
            "L_T K_perp = -Z_T Delta_T K_perp + M_T^2 K_perp",
            "static elliptic branch once Z_T>0 and boundary domain are signed",
            "derived_conditional",
        ),
        (
            "OP4202_3_poincare",
            "use local domain spectral gap",
            "||D K||^2 >= lambda_D ||K||^2 after boundary/kernel projection",
            "lambda_D is the first positive tensor-domain eigenvalue",
            "derived_math_requires_domain_certificate",
        ),
        (
            "OP4202_4_coercivity",
            "combine operator positivity and Poincare",
            "<K,L_T K> >= (Z_T lambda_D + M_T^2)||K||^2 - boundary_bad",
            "defines c_T := Z_T lambda_D + M_T^2 when boundary_bad=0/routed",
            "derived_conditional",
        ),
        (
            "OP4202_5_resolvent",
            "invert finite coercive operator",
            "||K_perp|| <= (||S_T||+||B_T||+||I_T||+||Z_Tmode||)/(Z_T lambda_D + M_T^2)",
            "so C_T <= 1/c_T with c_T=Z_T lambda_D+M_T^2",
            "derived_conditional_inputs_missing",
        ),
    ]
    return [
        {
            **common(),
            "derivation_id": derivation_id,
            "step": step,
            "formula": formula,
            "effect": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for derivation_id, step, formula, effect, status in rows
    ]


def coercivity_case_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "CASE4202_0_dirichlet_massless",
            "Dirichlet/decay boundary, no incoming modes, M_T^2=0",
            "c_T >= Z_T lambda_D",
            "finite if Z_T>0 and lambda_D>0",
            "valid_conditional_route",
        ),
        (
            "CASE4202_1_dirichlet_massive",
            "Dirichlet/decay boundary, positive mass gap",
            "c_T >= Z_T lambda_D + M_T^2",
            "strongest clean finite bound",
            "valid_conditional_route",
        ),
        (
            "CASE4202_2_neumann_massive",
            "Neumann/natural boundary with M_T^2>0",
            "c_T >= M_T^2 after boundary form is nonnegative",
            "finite even if lambda_D zero, but boundary hair may still feed B_T",
            "conditional_boundary_sensitive",
        ),
        (
            "CASE4202_3_neumann_massless",
            "Neumann/natural boundary with M_T^2=0",
            "c_T may vanish unless kernel/constant TT sector is projected out",
            "not safe without explicit kernel certificate",
            "fails_current_claim",
        ),
        (
            "CASE4202_4_hyperbolic_incoming",
            "radiative/hyperbolic tensor branch",
            "elliptic c_T inverse is not applicable",
            "must route I_T as incoming-mode norm instead of using static proof",
            "fails_static_LT_route",
        ),
    ]
    return [
        {
            **common(),
            "case_id": case_id,
            "domain_case": domain_case,
            "coercivity_formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for case_id, domain_case, formula, meaning, status in rows
    ]


def source_pack_rows() -> List[Dict[str, str]]:
    rows = [
        ("Z_T", "tensor kinetic residue", "positive dimension per K normalization", "coefficient of |D K_perp|^2 in parent second variation", "MISSING_PARENT_KINETIC_RESIDUE", "must be >0 or no elliptic bound"),
        ("M_T2", "tensor mass-gap/Hessian", "same units as Z_T lambda_D", "coefficient of |K_perp|^2 in parent second variation", "MISSING_PARENT_MASS_GAP_OR_NO_POLE", "can be zero if lambda_D>0, but positive is safer"),
        ("lambda_D", "first positive tensor-domain eigenvalue", "L^-2", "boundary/domain spectral certificate after kernel projection", "MISSING_DOMAIN_AND_KERNEL_CERTIFICATE", "Dirichlet/decay can supply positive gap; Neumann needs kernel removal"),
        ("c_T", "coercivity lower bound", "same units as M_T2", "c_T = Z_T lambda_D + M_T2", "SYMBOLIC_DERIVED_INPUTS_MISSING", "must be positive before C_T is finite"),
        ("C_T", "operator inverse norm", "1/c_T units", "C_T <= 1/c_T", "SYMBOLIC_DERIVED_INPUTS_MISSING", "converts obstruction norm to Kperp norm"),
        ("S_T", "transverse source norm", "K-source norm", "P_perp source/current/sector leakage", "MISSING_SOURCE_ZERO_OR_NORM", "zero theorem or finite absolute norm required"),
        ("B_T", "boundary obstruction norm", "K-boundary norm", "bad boundary form / nonzero surface data", "MISSING_ZB_OR_BOUNDARY_NORM", "Z_B/no-flux can set to zero only if parent signed"),
        ("I_T", "incoming tensor mode norm", "K norm", "radiative/hyperbolic homogeneous input", "MISSING_NO_INCOMING_OR_WAVE_NORM", "static proof cannot absorb it"),
        ("Z_Tmode", "zero-mode projection norm", "K norm", "projection onto ker L_T", "MISSING_KERNEL_CERTIFICATE", "not same as kinetic residue Z_T"),
    ]
    return [
        {
            **common(),
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "source_rule": source_rule,
            "current_status": current_status,
            "claim_guard": claim_guard,
            "numeric_value": "MISSING",
            "source_path": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for symbol, definition, units, source_rule, current_status, claim_guard in rows
    ]


def ppn_threshold_rows() -> List[Dict[str, str]]:
    rows = []
    for observable, units, bound in PPN_BOUNDS:
        rows.append(
            {
                **common(),
                "observable": observable,
                "bound_value": f"{bound:.12g}",
                "bound_units": units,
                "derived_threshold": f"|S_T|+|B_T|+|I_T|+|Z_Tmode| <= {bound:.12g} * (Z_T*lambda_D + M_T2) / |W_{observable}^K|",
                "equivalent_Knorm_threshold": f"||K_perp|| <= {bound:.12g} / |W_{observable}^K|",
                "current_status": "not_scoreable_ZT_MT2_lambdaD_W_missing",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def no_pole_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "NP4202_0_auxiliary_constraint",
            "K_perp is not an independent parent field but a constrained auxiliary eliminated algebraically",
            "no physical tensor pole; C_T row becomes not_applicable",
            "best_route_if_parent_action_supports_it",
        ),
        (
            "NP4202_1_pure_gauge_quotient",
            "K_perp lives entirely in ker(Dq) and does not affect observed coframe/metric",
            "W_i^K=0 for all local PPN observables",
            "requires observed-frame quotient proof",
        ),
        (
            "NP4202_2_EH_TT_not_new_field",
            "K_perp is just ordinary GR TT radiation already counted in the metric sector",
            "route to standard GR boundary/radiation treatment, not new MTS local residual",
            "requires no double-counting theorem",
        ),
        (
            "NP4202_3_current_status",
            "none of the no-pole routes is parent-signed",
            "finite LT/source-pack branch remains active",
            "current_state",
        ),
    ]
    return [
        {
            **common(),
            "route_id": route_id,
            "route": route,
            "effect_if_signed": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for route_id, route, effect, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "LT_formula_derived": "True",
            "coercivity_formula": "c_T = Z_T*lambda_D + M_T2",
            "operator_inverse_bound": "C_T <= 1/c_T",
            "parent_ZT_signed": "False",
            "parent_MT2_signed": "False",
            "domain_lambdaD_signed": "False",
            "numeric_score_ready": "False",
            "current_route_status": "conditional_LT_bound_derived_source_pack_missing",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4202_0_template_not_parent_action", "Quadratic L_T is a derived conditional template, not a parent-adopted action."),
        ("FW4202_1_ZT_vs_ZTmode", "Z_T kinetic residue and Z_Tmode zero-mode norm are different objects; do not collapse them."),
        ("FW4202_2_poincare_needs_domain", "lambda_D>0 requires boundary/domain and kernel certificates; it is not automatic."),
        ("FW4202_3_static_not_radiative", "Static elliptic inverse cannot absorb incoming hyperbolic tensor modes."),
        ("FW4202_4_no_score_without_weights", "PPN threshold formulas still need W_i^K and source norms before any pass."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": "4202 derives the LT coercivity/resolvent formula C_T<=1/(Z_T lambda_D+M_T2), but Z_T, M_T2, lambda_D, source norms and PPN weights remain missing.",
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "The operator inverse is now formula-level derived; the next step must source or prove the actual ingredients Z_T, M_T2, lambda_D and no-pole/zero-source alternatives.",
            "route_A": "prove no physical Kperp pole or observed quotient weight W_i^K=0",
            "route_B": "parent-sign Z_T>0, M_T2>=0 and lambda_D>0 with boundary/kernel certificate",
            "route_C": "fill finite source-pack rows and run PPN threshold comparison",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4202_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4202_LT_DERIVATION.csv": operator_derivation_rows(),
        "P8_Y5_R2FR_4202_COHERCIVITY_CASES.csv": coercivity_case_rows(),
        "P8_Y5_R2FR_4202_FIRST_SOURCE_PACK.csv": source_pack_rows(),
        "P8_Y5_R2FR_4202_PPN_THRESHOLD_MAP.csv": ppn_threshold_rows(),
        "P8_Y5_R2FR_4202_NO_PHYSICAL_POLE_ROUTES.csv": no_pole_rows(),
        "P8_Y5_R2FR_4202_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4202_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4202_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4202_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 218 - PPC4161 Parent Tensor Operator LT Coercivity

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint derives the useful `L_T` inverse formula but does not parent-sign the required coefficients or domain certificates.

## Coercivity Derivation

On the transverse local tensor sector:

```text
S_K^(2)=1/2 int_W sqrt(h) [Z_T |D K_perp|^2 + M_T^2 |K_perp|^2] - int_W sqrt(h) K_perp:S_T.
```

The static Euler operator is:

```text
L_T K_perp = -Z_T Delta_T K_perp + M_T^2 K_perp.
```

If the boundary form is zero/routed and the tensor-domain Poincare inequality holds:

```text
||D K||^2 >= lambda_D ||K||^2,
```

then:

```text
<K,L_TK> >= (Z_T lambda_D + M_T^2)||K||^2.
```

So:

```text
c_T = Z_T lambda_D + M_T^2,
C_T <= 1/c_T.
```

and:

```text
||K_perp|| <= (|S_T|+|B_T|+|I_T|+|Z_Tmode|)/(Z_T lambda_D + M_T^2).
```

## What This Achieves

The route is no longer “find some bound”. The parent theory must supply:

```text
Z_T, M_T^2, lambda_D, S_T, B_T, I_T, Z_Tmode, W_i^K.
```

or prove no physical `K_perp` pole / no observed projection.

## Verdict

4202 is a genuine derivation step: it identifies the exact denominator that can suppress `K_perp`. It is still not local GR because the denominator and source numerators are not parent-owned.
"""
    checkpoint = f"""# 4202 - Y5 R2FR Parent Tensor Operator LT Or First Kperp Coefficient Source Pack

Decision: `{DECISION}`

4202 derives the operator inverse route:

```text
C_T <= 1/(Z_T lambda_D + M_T^2).
```

Therefore every PPN row becomes:

```text
|S_T|+|B_T|+|I_T|+|Z_Tmode|
 <= bound_i (Z_T lambda_D + M_T^2)/|W_i^K|.
```

No claim is allowed yet because `Z_T`, `M_T^2`, `lambda_D`, source norms and projection weights are not supplied. But the next coefficient hunt is now mathematically sharp.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(checkpoint, encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker not in text:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n\n" + block.strip() + "\n")


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,"The parent tensor operator route now has a conditional coercivity formula '
        f'C_T<=1/(Z_T lambda_D+M_T2), converting K_perp PPN safety into source-pack inequalities; parent coefficients remain missing.",'
        f'"4202 source audit, LT derivation, coercivity cases, first source pack, PPN threshold map, no-physical-pole routes, decision row and firewall.",'
        f'private_LT_coercivity_formula_nonclaim_source_pack_missing,'
        f'"Source or derive Z_T, M_T2, lambda_D, source norms and W_i^K, or prove no physical Kperp pole.",'
        f'"A clean inverse formula could be mistaken for a numeric PPN pass unless the denominator and numerator source rows are parent-owned."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Parent Tensor Operator LT Coercivity - 4202

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4202 derives the conditional tensor inverse:

```text
c_T = Z_T lambda_D + M_T^2,
C_T <= 1/c_T.
```

The local PPN threshold rows now demand:

```text
|S_T|+|B_T|+|I_T|+|Z_Tmode| <= bound_i c_T/|W_i^K|.
```

This sharpens the route but remains nonclaim until `Z_T`, `M_T^2`, `lambda_D`, source norms and projection weights are parent-owned or source-backed."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Parent Tensor Operator LT Coercivity - 4202

Marker: `{PACKET_MARKER}`

Inside the private packet, `Kperp` suppression is now controlled by:

```text
Z_T lambda_D + M_T^2.
```

The packet remains nonclaim, but the next coefficient hunt has a real target: prove/source the tensor kinetic sign, mass gap, domain spectral gap, source norms and PPN projection weights."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4202_SOURCE_REGISTER.csv"]
    derivation = rows_by_file["P8_Y5_R2FR_4202_LT_DERIVATION.csv"]
    cases = rows_by_file["P8_Y5_R2FR_4202_COHERCIVITY_CASES.csv"]
    pack = rows_by_file["P8_Y5_R2FR_4202_FIRST_SOURCE_PACK.csv"]
    ppn = rows_by_file["P8_Y5_R2FR_4202_PPN_THRESHOLD_MAP.csv"]
    nopole = rows_by_file["P8_Y5_R2FR_4202_NO_PHYSICAL_POLE_ROUTES.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4202_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    pack_symbols = {row["symbol"] for row in pack}
    checks = [
        ("VAL4202_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4202_1_source_needles", "all source required text markers found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4202_2_derivation_formula", "LT derivation contains C_T inverse formula", any("Z_T lambda_D + M_T^2" in row["formula"] or "Z_T lambda_D + M_T2" in row["formula"] for row in derivation)),
        ("VAL4202_3_cases_cover_failure", "coercivity cases include hyperbolic fail and Neumann massless fail", any(row["case_id"] == "CASE4202_4_hyperbolic_incoming" for row in cases) and any(row["case_id"] == "CASE4202_3_neumann_massless" for row in cases)),
        ("VAL4202_4_source_pack_core", "source pack includes denominator and numerator symbols", {"Z_T", "M_T2", "lambda_D", "c_T", "C_T", "S_T", "B_T", "I_T", "Z_Tmode"}.issubset(pack_symbols)),
        ("VAL4202_5_ppn_threshold_rows", "PPN threshold map covers every bound", len(ppn) == len(PPN_BOUNDS)),
        ("VAL4202_6_no_pole_routes", "no physical pole alternatives are explicit", any(row["route_id"] == "NP4202_0_auxiliary_constraint" for row in nopole)),
        ("VAL4202_7_decision_nonclaim", "decision keeps numeric score false", decision[0]["numeric_score_ready"] == "False" and decision[0]["claim_allowed"] == "False"),
        ("VAL4202_8_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4202_9_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4202_10_claim_register", "claim register contains L-043", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4202_11_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4202_12_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
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
    rows_by_file = all_rows()
    write_docs()
    update_registers()
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4202_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4202 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4202_VALIDATION.csv'}")
    print("rows=13 validation checks")


if __name__ == "__main__":
    main()
