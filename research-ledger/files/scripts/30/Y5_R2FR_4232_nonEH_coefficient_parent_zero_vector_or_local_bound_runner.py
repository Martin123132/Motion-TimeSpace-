from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4232"
CLAIM_ID = "L-073"
BRANCH = "MTS_R2FR_Y5_NONEH_COEFFICIENT_VECTOR_4232"
DECISION = "NONEH_R11_VECTOR_CONTRACT_DERIVED_TWO_PRIVATE_ZERO_ROUTES_FOUR_SURVIVOR_BOUND_ROUTES_PUBLIC_CLAIM_BLOCKED"
MARKER = "PPC4161_NONEH_R11_COEFFICIENT_VECTOR_4232"
PACKET_MARKER = "PPC4161_PACKET_NONEH_R11_COEFFICIENT_VECTOR_4232"
NEXT_TARGET = "4233-Y5-R2FR-cGamma-Kperp-two-survivor-zero-proof-or-bound-runner.md"

FORMAL_PATH = FORMAL / "248-PPC4161-nonEH-coefficient-parent-zero-vector-or-local-bound-runner.md"
DOC_PATH = POST / "4232-Y5-R2FR-nonEH-coefficient-parent-zero-vector-or-local-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4232_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4232_00_4231_next": SourceSpec(
        "SRC4232_00_4231_next",
        SOURCE_DIR / "P8_Y5_R2FR_4231_NEXT_TARGET.csv",
        "4232-Y5-R2FR-nonEH-coefficient-parent-zero-vector-or-local-bound-runner.md",
        "4231 explicitly selected the non-EH/R11 coefficient vector as the next local-GR blocker.",
    ),
    "SRC4232_01_palatini_selector": SourceSpec(
        "SRC4232_01_palatini_selector",
        FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md",
        "residual_EFT_bound_ledger_active = true",
        "Palatini/EH IR selector and residual EFT ledger.",
    ),
    "SRC4232_02_coeff_map": SourceSpec(
        "SRC4232_02_coeff_map",
        FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md",
        "all_coefficients_numeric_or_parent_zero = false",
        "Original residual coefficient map and public-claim blocker.",
    ),
    "SRC4232_03_same_coframe": SourceSpec(
        "SRC4232_03_same_coframe",
        FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md",
        "c_D_private_zero = true",
        "Private zero route for same-coframe/disformal leakage.",
    ),
    "SRC4232_04_kappa_lock": SourceSpec(
        "SRC4232_04_kappa_lock",
        FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md",
        "delta_kappa_private_zero = true",
        "Private zero route for source-coupling drift.",
    ),
    "SRC4232_05_cgamma_contract": SourceSpec(
        "SRC4232_05_cgamma_contract",
        FORMAL / "203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md",
        "c_Gamma_parent_zero = false",
        "c_Gamma support/projector zero contract remains unsigned.",
    ),
    "SRC4232_06_cgamma_bound": SourceSpec(
        "SRC4232_06_cgamma_bound",
        FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md",
        "|C_Gamma,a| <= B_a.",
        "Finite c_Gamma product-bound law.",
    ),
    "SRC4232_07_Kperp_operator": SourceSpec(
        "SRC4232_07_Kperp_operator",
        FORMAL / "218-PPC4161-parent-tensor-operator-LT-coercivity.md",
        "c_T = Z_T lambda_D + M_T^2",
        "Kperp/tensor coercivity denominator formula.",
    ),
    "SRC4232_08_Kperp_no_pole": SourceSpec(
        "SRC4232_08_Kperp_no_pole",
        FORMAL / "219-PPC4161-no-physical-Kperp-pole-theorem.md",
        "no independent MTS TT source projects onto it",
        "No-extra-pole theorem for static local Kperp if parent-signed.",
    ),
    "SRC4232_09_EH_coframe": SourceSpec(
        "SRC4232_09_EH_coframe",
        FORMAL / "221-PPC4161-EH-coframe-parent-signature-or-Kperp-score.md",
        "Six-Clause EH/Coframe Gate",
        "EH/coframe identity needed to remove Kperp as an independent source.",
    ),
    "SRC4232_10_boundary": SourceSpec(
        "SRC4232_10_boundary",
        FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md",
        "I_boundary + I_corner = 0.",
        "Boundary/corner zero route for no-flux local collars.",
    ),
    "SRC4232_11_Dq_coeff": SourceSpec(
        "SRC4232_11_Dq_coeff",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_coeff[v]=0.",
        "Coefficient/readout q-basicity condition.",
    ),
    "SRC4232_12_denominator": SourceSpec(
        "SRC4232_12_denominator",
        FORMAL / "246-PPC4161-MEH-total-epsilon-score-open-reference-virial-frame-gate.md",
        "E_nonEH_abs = 0 only inside the full private Palatini/EH IR selector.",
        "4230 selector-zero caveat for non-EH source energy.",
    ),
    "SRC4232_13_scorecard": SourceSpec(
        "SRC4232_13_scorecard",
        FORMAL / "247-PPC4161-private-local-GR-scorecard-refresh-and-nonEH-parent-adoption-gate.md",
        "nonEH/R11 coefficient vector;",
        "4231 public promotion blocker.",
    ),
    "SRC4232_14_R11_template": SourceSpec(
        "SRC4232_14_R11_template",
        SOURCE_DIR / "MTS_local_residual_predictions_TEMPLATE.csv",
        "R11_EH_operator_ledger",
        "Local residual template for non-EH operator ledger.",
    ),
}


def common() -> Dict[str, str]:
    return {"timestamp_utc": STAMP, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def vector_rows() -> List[Dict[str, str]]:
    rows = [
        {
            "coefficient_id": "NEH4232_0_cD",
            "coefficient": "c_D",
            "operator_family": "same-coframe/disformal leak",
            "zero_condition": "one observed coframe/Hodge metric for matter, EM, clocks and rods; no hidden disformal representative",
            "current_private_status": "private_selector_zero",
            "current_public_status": "not_global_parent_signed",
            "derived_or_bound_result": "c_D=0 inside the private same-coframe/Hilbert/Maxwell-Hodge selector",
            "survives_4232": "False",
            "first_bound_route_if_reopened": "WEP + clock + EM lightcone/Hodge residual",
            "source_paths": "formalization-workbench/202-PPC4161-same-coframe-source-memory-zero-law.md; formalization-workbench/224-PPC4161-Hodge-deformation-zero-or-constitutive-bound.md",
            "next_action": "Keep as private zero; promote publicly only with global same-coframe parent action.",
        },
        {
            "coefficient_id": "NEH4232_1_deltaKappa",
            "coefficient": "delta_kappa",
            "operator_family": "source-coupling drift",
            "zero_condition": "single source-blind kappa_eff/G_cal plus Hilbert source measure and no source/readout dependent coupling",
            "current_private_status": "private_selector_zero",
            "current_public_status": "not_global_parent_signed",
            "derived_or_bound_result": "delta_kappa=0 inside the private topological-kappa plus Hilbert-source selector",
            "survives_4232": "False",
            "first_bound_route_if_reopened": "orbital GM + clock/Gdot + WEP source-charge residual",
            "source_paths": "formalization-workbench/202-PPC4161-same-coframe-source-memory-zero-law.md; formalization-workbench/222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md",
            "next_action": "Keep as private zero; public promotion requires source-blind coupling in the parent action.",
        },
        {
            "coefficient_id": "NEH4232_2_cGamma",
            "coefficient": "c_Gamma",
            "operator_family": "local memory hair",
            "zero_condition": "Gamma_mem vertical/readout-only, compact-support silent, ordinary-source silent, boundary-routed, and tensor-no-hair",
            "current_private_status": "not_zero",
            "current_public_status": "not_zero",
            "derived_or_bound_result": "|C_Gamma,a|<=B_a product law exists; parent-zero proof remains unsigned",
            "survives_4232": "True",
            "first_bound_route_if_reopened": "Gdot/G, alpha3, xi, WEP, clock, R10 product bounds",
            "source_paths": "formalization-workbench/203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md; formalization-workbench/204-PPC4161-finite-cGamma-product-bound-law.md",
            "next_action": "Either prove the support/no-hair clauses or fill profile_a/J_a rows and score the product bounds.",
        },
        {
            "coefficient_id": "NEH4232_3_cT_Kperp",
            "coefficient": "c_T / Kperp",
            "operator_family": "torsion-square or independent transverse tensor residual",
            "zero_condition": "Kperp is ordinary EH TT/gauge/radiation/vertical/boundary only, with no independent MTS tensor source projection",
            "current_private_status": "conditional_no_extra_pole_unsigned",
            "current_public_status": "not_zero",
            "derived_or_bound_result": "finite tensor denominator c_T=Z_T lambda_D+M_T^2 is derived; source numerators and EH/coframe identity are unsigned",
            "survives_4232": "True",
            "first_bound_route_if_reopened": "PPN gamma/beta/vector/clock inequalities using W_i^K C_T(|S_T|+|B_T|+|I_T|+|Z_Tmode|)",
            "source_paths": "formalization-workbench/218-PPC4161-parent-tensor-operator-LT-coercivity.md; formalization-workbench/219-PPC4161-no-physical-Kperp-pole-theorem.md; formalization-workbench/221-PPC4161-EH-coframe-parent-signature-or-Kperp-score.md",
            "next_action": "Prove EH/coframe identity or fill the first independent tensor source-pack rows.",
        },
        {
            "coefficient_id": "NEH4232_4_cR2_MR",
            "coefficient": "c_R2 / M_R",
            "operator_family": "curvature-square finite-range tail",
            "zero_condition": "Palatini/EH IR selector forbids unsuppressed curvature-square modes or supplies a heavy/screened mass scale outside local tests",
            "current_private_status": "selector_excluded_but_scale_not_parent_sourced",
            "current_public_status": "not_zero_or_numeric",
            "derived_or_bound_result": "finite-range tail is isolated as a residual EFT coefficient, not silently absorbed into EH",
            "survives_4232": "True",
            "first_bound_route_if_reopened": "R10 inverse-square/Yukawa curve plus PPN gamma/beta finite-range envelope",
            "source_paths": "formalization-workbench/200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md; formalization-workbench/201-PPC4161-extra-invariant-residual-coefficient-map.md",
            "next_action": "Derive M_R heavy/screened scale or attach source-backed alpha(lambda) curve rows.",
        },
        {
            "coefficient_id": "NEH4232_5_cbdy",
            "coefficient": "c_bdy",
            "operator_family": "unrouted boundary/edge charge",
            "zero_condition": "differentiability-owned boundary, fixed corner data, compact no-flux collar, no source crossing, live radiation routed as Hamiltonian flux",
            "current_private_status": "private_no_flux_zero_conditional",
            "current_public_status": "not_global_zero",
            "derived_or_bound_result": "I_boundary+I_corner=0 in the no-flux local collar; radiative/open/edge flux remains a bound row",
            "survives_4232": "True",
            "first_bound_route_if_reopened": "alpha3, Gdot/G, orbital energy balance, clock/redshift flux leakage",
            "source_paths": "formalization-workbench/233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md; formalization-workbench/235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
            "next_action": "Keep no-flux collar zero for private local branch; build flux rows for global/open systems.",
        },
        {
            "coefficient_id": "NEH4232_6_R11_aggregate",
            "coefficient": "C_R11",
            "operator_family": "aggregate non-EH operator ledger",
            "zero_condition": "Z_D Z_kappa Z_Gamma Z_T Z_R2 Z_bdy = 1 or every surviving term has source-backed local bounds",
            "current_private_status": "partial_private_zero_plus_survivors",
            "current_public_status": "blocked",
            "derived_or_bound_result": "public R11 pass is false; private denominator E_nonEH_abs=0 is a selector-zero, not global coefficient ownership",
            "survives_4232": "True",
            "first_bound_route_if_reopened": "joint local residual runner with no cross-channel cancellation",
            "source_paths": "formalization-workbench/246-PPC4161-MEH-total-epsilon-score-open-reference-virial-frame-gate.md; formalization-workbench/247-PPC4161-private-local-GR-scorecard-refresh-and-nonEH-parent-adoption-gate.md",
            "next_action": "Reduce the surviving vector to c_Gamma and Kperp first, while retaining c_R2 and boundary rows as R10/flux debt.",
        },
    ]
    return [{**common(), **row, "claim_allowed": "False", "valid_for_claim": "False"} for row in rows]


def certificate_rows() -> List[Dict[str, str]]:
    rows = [
        ("Z_D", "c_D=0", "same observed coframe/Hodge metric and no disformal representative", "True", "False", "Public parent action has not globally adopted the same-coframe selector."),
        ("Z_kappa", "delta_kappa=0", "source-blind kappa_eff, single Hilbert measure and calibrated G bridge", "True", "False", "Global source-coupling law is not parent-signed outside the private selector."),
        ("Z_Gamma", "c_Gamma=0", "vertical/support/no-source/boundary/tensor-no-hair memory theorem", "False", "False", "4187 support/no-hair clauses remain unsigned; product bounds are active."),
        ("Z_T", "c_T/Kperp extra source=0", "EH/coframe identity plus no independent MTS tensor pole", "False", "False", "Kperp placement theorem exists but EH/coframe identity is not parent-signed."),
        ("Z_R2", "c_R2/M_R local tail=0 or heavy", "Palatini/EH selector supplies no light curvature-square mode or a sourced heavy/screened scale", "False", "False", "Residual EFT coefficient has no parent numeric scale or R10 envelope yet."),
        ("Z_bdy", "c_bdy=0 in local collar", "fixed differentiability-owned no-flux boundary/corner data", "True", "False", "The compact collar zero is conditional; radiative/open/global boundaries remain flux rows."),
        ("Z_R11_all", "C_R11=0", "all above clauses true, or every survivor bounded with source-backed numerators", "False", "False", "Surviving c_Gamma, Kperp/c_T, c_R2/M_R and boundary/global rows block public promotion."),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "zero_statement": statement,
            "required_parent_condition": condition,
            "current_private_truth": private_truth,
            "current_public_truth": public_truth,
            "blocking_reason": blocker,
            "derived_consequence": "If true, the matching non-EH residual coefficient is removed without an empirical fit; if false, the bound-runner row must be filled.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, statement, condition, private_truth, public_truth, blocker in rows
    ]


def theorem_rows() -> List[Dict[str, str]]:
    rows = [
        {
            "theorem_id": "THM4232_0_vector_zero",
            "statement": "Let C_R11=(c_D,delta_kappa,c_Gamma,c_T,c_R2/M_R,c_bdy). Public local-GR/R11 zero requires each component to be parent-zero/symmetry-forbidden/heavy-screened/boundary-routed, not merely absent inside a selected private denominator.",
            "formula": "C_R11=0 iff Z_D=Z_kappa=Z_Gamma=Z_T=Z_R2=Z_bdy=1.",
            "current_result": "false publicly; partially true privately",
        },
        {
            "theorem_id": "THM4232_1_selector_not_public",
            "statement": "The 4230 result E_nonEH_abs=0 inside the full private Palatini/EH selector is a local selector theorem, not a public parent coefficient theorem.",
            "formula": "E_nonEH_abs|private=0 does not imply C_R11|parent=0.",
            "current_result": "prevents overclaim while preserving the useful private pass",
        },
        {
            "theorem_id": "THM4232_2_bound_runner",
            "statement": "If any component survives, each observed arena must satisfy a no-cancellation inequality against sourced local bounds.",
            "formula": "|sum_i J_ai profile_ai c_i| <= B_a with rows reported per coefficient before any aggregate score.",
            "current_result": "runner schema written; source numerators not yet claim-grade",
        },
    ]
    return [{**common(), **row, "claim_allowed": "False", "valid_for_claim": "False"} for row in rows]


def bound_schema_rows() -> List[Dict[str, str]]:
    rows = [
        ("BND4232_0_cGamma_Gdot", "c_Gamma", "Gdot/G", "|c_Gamma D_t Xi_0| <= 2.42e-14 yr^-1", "D_t Xi_0 profile or parent stationarity", "profile missing", "False"),
        ("BND4232_1_cGamma_alpha3_xi", "c_Gamma", "PPN alpha3/xi", "|c_Gamma profile_PPN| <= B_alpha3, B_xi", "PPN channel projection from Gamma_mem", "profile missing", "False"),
        ("BND4232_2_Kperp_PPN", "c_T/Kperp", "PPN gamma/beta/vector/clock", "|W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_Tmode|) <= B_i", "Z_T, M_T^2, lambda_D, source norms, W_i^K", "coefficient pack missing", "False"),
        ("BND4232_3_R2_R10", "c_R2/M_R", "R10/Yukawa/inverse-square", "alpha(lambda; c_R2,M_R) <= alpha_bound(lambda)", "M_R, c_R2, mapped force envelope, real alpha(lambda) curve", "curve and coefficients missing", "False"),
        ("BND4232_4_boundary_flux", "c_bdy", "Gdot/orbital/clock/alpha3", "|Flux_boundary|/M_H_ref <= B_flux,a", "radiative/source-crossing/open-memory flux rows", "global flux rows missing", "False"),
        ("BND4232_5_cD_guard", "c_D", "WEP/clock/EM guard", "eta, clock and Hodge residuals vanish only under same-coframe parent selector", "global same-coframe action-domain certificate", "private zero only", "False"),
        ("BND4232_6_deltaKappa_guard", "delta_kappa", "orbital/WEP/clock guard", "|D_A ln kappa_eff| and source-charge drift <= arena bounds", "source-blind coupling and Hilbert source measure certificate", "private zero only", "False"),
        ("BND4232_7_R11_aggregate", "C_R11", "operator ledger", "score only after every component is zero or bounded separately", "all component rows", "blocked", "False"),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "coefficient": coefficient,
            "arena": arena,
            "bound_formula": formula,
            "required_input": required_input,
            "current_status": status,
            "executable_now": executable,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, coefficient, arena, formula, required_input, status, executable in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "cD_private_zero": "True",
            "delta_kappa_private_zero": "True",
            "cGamma_public_zero_or_bound": "False",
            "Kperp_public_zero_or_bound": "False",
            "R2_public_zero_or_bound": "False",
            "boundary_global_zero_or_bound": "False",
            "public_R11_pass": "False",
            "private_selector_R11_zero": "partial_selector_zero_only",
            "next_highest_pressure": "c_Gamma and Kperp/tensor are the first two live local PPN/Gdot blockers; c_R2/R10 and boundary flux remain retained debts.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        ("FW4232_0", "Do not state public local GR is derived from 4232.", "4232 writes a coefficient contract; it does not parent-sign the surviving coefficients."),
        ("FW4232_1", "Do not treat E_nonEH_abs|private=0 as C_R11|parent=0.", "The former is a selector-zero; the latter is global coefficient ownership."),
        ("FW4232_2", "Do not use aggregate cancellation between coefficients.", "Each coefficient must be zero or bounded separately before an aggregate R11 score."),
        ("FW4232_3", "Do not pass R10 from anchor-only or symbolic rows.", "c_R2/M_R needs a real curve/envelope and sourced coefficient map."),
        ("FW4232_4", "Do not erase radiation, Poynting or boundary flow.", "Live flux is a Hamiltonian/boundary row, not a hidden bulk force and not silent zero."),
    ]
    return [
        {
            **common(),
            "rule_id": rule_id,
            "forbidden_claim": forbidden,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for rule_id, forbidden, reason in rules
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4232 reduces the non-EH/R11 blocker to a concrete vector: c_D and delta_kappa are privately zero; c_Gamma, Kperp/c_T, c_R2/M_R and global boundary flux remain as zero-proof-or-bound rows.",
            "public_local_GR_claim": "False",
            "global_parent_adoption": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "After 4232 the first genuinely local survivors are c_Gamma memory hair and Kperp/tensor leakage; both feed PPN/Gdot/clock arenas before R10 can be meaningful.",
            "derive_first": "try to prove Gamma_mem support/no-hair and Kperp no-extra-pole/EH-coframe identity in the same local projector",
            "fill_second": "if either survives, run a two-survivor bound runner with separate c_Gamma and Kperp profiles and no cross-channel cancellation",
            "fallback": "retain c_R2/M_R for R10 curve acquisition and c_bdy for global/open boundary flux rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 248 - PPC4161 Non-EH Coefficient Parent-Zero Vector Or Local Bound Runner

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4232 turns the loose phrase "non-EH/R11 blocker" into an actual vector:

```text
C_R11 := (c_D, delta_kappa, c_Gamma, c_T/Kperp, c_R2/M_R, c_bdy).
```

The exact promotion rule is:

```text
C_R11 = 0
iff
Z_D Z_kappa Z_Gamma Z_T Z_R2 Z_bdy = 1.
```

If any `Z_i` fails, that component is not allowed to disappear into prose. It must enter a local bound row:

```text
|J_ai profile_ai c_i| <= B_a,
```

reported per coefficient before any aggregate R11 score.

## What Actually Closed

Inside the private compact selector:

```text
c_D = 0,
delta_kappa = 0.
```

These are real private derivation wins: same observed coframe/Hodge ownership kills the disformal leak, and the source-blind calibrated Hilbert coupling kills `delta_kappa`.

## What Still Survives

The live vector after 4232 is:

```text
c_Gamma,
c_T/Kperp,
c_R2/M_R,
c_bdy outside compact no-flux collars.
```

`c_Gamma` already has a finite product law. `Kperp` already has a tensor denominator formula and a no-extra-pole theorem shape. `c_R2/M_R` is isolated as the finite-range/R10 tail. `c_bdy` is zero only in the fixed no-flux local collar; open/radiative/global flux is retained as a row.

## Important Separation

4230 gave:

```text
E_nonEH_abs|private selector = 0.
```

4232 does **not** convert that into:

```text
C_R11|parent = 0.
```

That distinction matters. The private selector can reproduce local GR structure, but public/global promotion needs parent-owned coefficient zeros or source-backed local bounds.

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4232 - Non-EH Coefficient Parent-Zero Vector Or Local Bound Runner

**Status:** `{DECISION}`.

## Forward Move

This checkpoint converts the public local-GR blocker into a concrete coefficient vector:

```text
C_R11 = (c_D, delta_kappa, c_Gamma, c_T/Kperp, c_R2/M_R, c_bdy).
```

Two components are privately killed:

```text
c_D = 0,
delta_kappa = 0.
```

Four components survive as zero-proof-or-bound rows:

```text
c_Gamma,
c_T/Kperp,
c_R2/M_R,
c_bdy outside the compact no-flux collar.
```

## Why This Is Progress

This is no longer a vague missing-coupling complaint. The exact rule is now:

```text
public R11 pass = every component parent-zero/heavy/screened/boundary-routed
                  OR every surviving component separately source-bounded.
```

No aggregate cancellation is allowed.

## Files Written

- `formalization-workbench\\248-PPC4161-nonEH-coefficient-parent-zero-vector-or-local-bound-runner.md`
- `post-checkpoint-work\\source-intake\\mts_residuals\\P8_Y5_R2FR_4232_NON_EH_VECTOR.csv`
- `post-checkpoint-work\\source-intake\\mts_residuals\\P8_Y5_R2FR_4232_PARENT_ZERO_CERTIFICATE.csv`
- `post-checkpoint-work\\source-intake\\mts_residuals\\P8_Y5_R2FR_4232_LOCAL_BOUND_RUNNER_SCHEMA.csv`
- `post-checkpoint-work\\source-intake\\mts_residuals\\P8_Y5_BRR545_4232_VALIDATION.csv`

## Nonclaim Firewall

No public local-GR, PPN, R10, WEP, clock, orbital, EM, or numerical-G claim follows from 4232. This is a coefficient-vector theorem and runner schema.

## Next

`{NEXT_TARGET}`
"""


def update_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    rows = csv_rows(path)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The non-EH/R11 blocker is now a concrete coefficient vector: c_D and delta_kappa are privately zero, while c_Gamma, c_T/Kperp, c_R2/M_R and global boundary flux must be parent-zero/heavy-screened/boundary-routed or source-bounded before public local-GR promotion.",
            "current_evidence": "4232 source register, non-EH vector table, parent-zero certificate, theorem rows, local bound-runner schema, decision and firewall.",
            "status": "private_noneh_vector_contract_nonclaim_public_r11_blocked",
            "next_test": "Derive c_Gamma and Kperp/tensor zero in the same local projector, or run a two-survivor local residual bound runner with sourced profiles and no cross-channel cancellation.",
            "key_risk": "Confusing private selector E_nonEH_abs=0 with public/global R11 coefficient zero would overclaim the local-GR reduction.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 Non-EH/R11 Coefficient Vector Gate

Marker: `{MARKER}`

4232 turns the public local-GR blocker into a coefficient vector:

```text
C_R11 = (c_D, delta_kappa, c_Gamma, c_T/Kperp, c_R2/M_R, c_bdy).
```

The private selector already kills `c_D` and `delta_kappa`. The surviving local pressure is `c_Gamma` memory hair and `Kperp/c_T` tensor leakage, with `c_R2/M_R` retained for R10 finite-range tests and `c_bdy` retained outside compact no-flux collars. Public promotion remains blocked until every component is parent-zero/heavy/screened/boundary-routed or separately source-bounded.
"""
    packet_block = f"""
## Packet Update - Non-EH/R11 Coefficient Vector Gate

Marker: `{PACKET_MARKER}`

The packet now distinguishes selector-zero source energy from public coefficient ownership:

```text
E_nonEH_abs|private = 0
does not imply
C_R11|parent = 0.
```

Within the private compact selector, `c_D=0` and `delta_kappa=0`. The live local-GR bound problem is now the two-survivor pair `c_Gamma` and `Kperp/c_T`; `c_R2/M_R` and `c_bdy` remain retained as R10/finite-range and boundary-flux debts. No public local-GR claim is made.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    src = source_rows()
    add("VAL4232_0_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in src), "source register")
    add("VAL4232_1_needles_found", "all required source strings found", all(r["required_text_found"] == "True" for r in src), "source register")

    vector = vector_rows()
    expected = {"c_D", "delta_kappa", "c_Gamma", "c_T / Kperp", "c_R2 / M_R", "c_bdy", "C_R11"}
    got = {row["coefficient"] for row in vector}
    add("VAL4232_2_vector_complete", "coefficient vector covers every residual family", got == expected, ",".join(sorted(got)))
    add("VAL4232_3_private_zero_pair", "c_D and delta_kappa are private zero only", all(any(row["coefficient"] == coeff and row["current_private_status"] == "private_selector_zero" and row["current_public_status"] == "not_global_parent_signed" for row in vector) for coeff in ("c_D", "delta_kappa")), "vector rows")
    add("VAL4232_4_survivors_retained", "surviving coefficients remain active", all(any(row["coefficient"] == coeff and row["survives_4232"] == "True" for row in vector) for coeff in ("c_Gamma", "c_T / Kperp", "c_R2 / M_R", "c_bdy")), "vector rows")

    cert = certificate_rows()
    add("VAL4232_5_certificate_blocks_public", "aggregate public R11 certificate is false", any(row["clause_id"] == "Z_R11_all" and row["current_public_truth"] == "False" for row in cert), "certificate rows")

    schema = bound_schema_rows()
    arenas = {row["arena"] for row in schema}
    add("VAL4232_6_bound_schema_local_arenas", "bound schema includes PPN/Gdot/R10/boundary/operator rows", {"Gdot/G", "PPN gamma/beta/vector/clock", "R10/Yukawa/inverse-square", "operator ledger"}.issubset(arenas), ",".join(sorted(arenas)))
    add("VAL4232_7_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for group in (src, vector, cert, theorem_rows(), schema, decision_rows(), firewall_rows(), status_rows(), next_target_rows()) for row in group), "all generated row groups")

    add("VAL4232_8_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4232_9_claim_register", "claims register contains L-073", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4232_10_spine_marker", "spine contains 4232 marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4232_11_packet_marker", "packet contains 4232 marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4232_12_next_target", "next target selected", NEXT_TARGET in next_target_rows()[0]["next_target"], NEXT_TARGET)
    add("VAL4232_13_decision_public_false", "decision keeps public R11 pass false", decision_rows()[0]["public_R11_pass"] == "False", DECISION)
    add("VAL4232_14_script_exists", "generator script exists", Path(__file__).exists(), str(Path(__file__)))
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4232_SOURCE_REGISTER.csv",
        "vector": SOURCE_DIR / "P8_Y5_R2FR_4232_NON_EH_VECTOR.csv",
        "certificate": SOURCE_DIR / "P8_Y5_R2FR_4232_PARENT_ZERO_CERTIFICATE.csv",
        "theorem": SOURCE_DIR / "P8_Y5_R2FR_4232_THEOREM_ROWS.csv",
        "schema": SOURCE_DIR / "P8_Y5_R2FR_4232_LOCAL_BOUND_RUNNER_SCHEMA.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4232_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4232_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4232_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4232_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["vector"], vector_rows())
    write_csv(paths["certificate"], certificate_rows())
    write_csv(paths["theorem"], theorem_rows())
    write_csv(paths["schema"], bound_schema_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next"], next_target_rows())
    update_claim_register()
    update_spine_and_packet()
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"Decision: {DECISION}")
    print(f"Formal: {FORMAL_PATH}")
    print(f"Checkpoint: {DOC_PATH}")
    print(f"Validation: {VALIDATION_PATH}")
    print(f"Validation rows: {len(csv_rows(VALIDATION_PATH))}; failed: {len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
