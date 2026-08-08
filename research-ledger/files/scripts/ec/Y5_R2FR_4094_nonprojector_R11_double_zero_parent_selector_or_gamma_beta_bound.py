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
DOC_PATH = ROOT / "4094-Y5-R2FR-nonprojector-R11-double-zero-parent-selector-or-gamma-beta-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "NONPROJECTOR_R11_DOUBLE_ZERO_THEOREM_FORMALIZED_BUT_YLOC_SOURCE_ZERO_AND_FACTOR_MAPPING_UNSIGNED"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4094_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4093_NEXT_TARGET.csv",
        "4094-Y5-R2FR-nonprojector-R11-double-zero-parent-selector-or-gamma-beta-bound.md",
        "4093 selects nonprojector R11 double-zero or gamma/beta bound.",
    ),
    "SRC4094_01_parent_clause": (
        SOURCE_DIR / "P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv",
        "C2_R11_factorization",
        "488 parent clause for Sigma_loc factorization of R11 families.",
    ),
    "SRC4094_02_variation": (
        SOURCE_DIR / "P8_DOUBLE_ZERO_R11_VARIATION_PROOF.csv",
        "V2_R11_variation",
        "488 variation proof that delta(Sigma_loc O_A)=0 when Y_loc=0.",
    ),
    "SRC4094_03_operator_mapping": (
        SOURCE_DIR / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv",
        "R2_fR_scalar_mode",
        "488 operator mapping covers R11 families and factorization contracts.",
    ),
    "SRC4094_04_gates": (
        SOURCE_DIR / "P8_DOUBLE_ZERO_R11_GATES.csv",
        "G2_all_R11_factorized",
        "488 gate showing all-R11 factorization remains fail-for-claim.",
    ),
    "SRC4094_05_y_euler": (
        SOURCE_DIR / "P8_YLOC_EULER_SYSTEM.csv",
        "Y5_source_normalization",
        "489/Yloc Euler components and local-source blockers.",
    ),
    "SRC4094_06_no_source": (
        SOURCE_DIR / "P8_YLOC_NO_SOURCE_THEOREM.csv",
        "N3_zero_theorem",
        "Positive Euler/no-source theorem that would force Y_loc=0.",
    ),
    "SRC4094_07_source_debt": (
        SOURCE_DIR / "P8_YLOC_SOURCE_DEBT_LEDGER.csv",
        "S3_source_normalization_current",
        "Yloc source-current and boundary debt ledger.",
    ),
    "SRC4094_08_source_decision": (
        SOURCE_DIR / "P8_YLOC_SOURCE_CURRENT_DECISION.csv",
        "no_linear_source_symmetry_target",
        "Yloc source-current decision selects no-linear-source symmetry as the next theorem target.",
    ),
    "SRC4094_09_4086_lemma": (
        SOURCE_DIR / "P8_Y5_R2FR_4086_AUX_DOUBLE_ZERO_LEMMA.csv",
        "NO_SINGLE_ZERO_SHORTCUT",
        "4086 auxiliary double-zero lemma and anti-single-zero guard.",
    ),
    "SRC4094_10_4087_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4087_R2_SCALAR_EXECUTABLE_BOUND.csv",
        "B4087_3_combined_range",
        "4087 standard f(R)/R2 scalar bound template.",
    ),
    "SRC4094_11_4088_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4088_RICCI_WEYL_SPIN2_EXECUTABLE_BOUND.csv",
        "B4088_3_spin2_combined_range",
        "4088 Ricci/Weyl spin-2 bound template.",
    ),
    "SRC4094_12_4093_r11": (
        SOURCE_DIR / "P8_Y5_R2FR_4093_R11_RESIDUAL_FAMILY_AUDIT.csv",
        "R11A4093_2_R2_fR_scalar",
        "4093 R11 residual-family audit.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
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


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4094_13_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4094 nonprojector R11 double-zero/gamma-beta gate.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def double_zero_theorem_rows() -> List[dict]:
    return [
        {
            "theorem_id": "DZ4094_0_sigma_definition",
            "statement": "Let Y_loc^A be the compact-local silence multiplet and Sigma_loc=G_AB Y_loc^A Y_loc^B with positive G_AB.",
            "formula": "Sigma_loc=G_AB Y^A Y^B >= 0",
            "result_if_Y_zero": "Sigma_loc=0",
            "public_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "DZ4094_1_double_zero_variation",
            "statement": "If Y_loc^A=0, then delta Sigma_loc=0 for arbitrary first variations.",
            "formula": "delta Sigma_loc = delta G_AB Y^A Y^B + 2G_AB Y^A delta Y^B = 0",
            "result_if_Y_zero": "no first-variation source from Sigma_loc",
            "public_status": "EXACT_CONDITIONAL_DOUBLE_ZERO_STEP",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "DZ4094_2_R11_factorization",
            "statement": "If every non-topological R11 operator has coefficient C_i=Sigma_loc * cbar_i or higher order, its local metric variation vanishes on Y_loc=0.",
            "formula": "delta[Sigma_loc cbar_i O_i] = Sigma_loc cbar_i delta O_i + cbar_i O_i delta Sigma_loc = 0",
            "result_if_Y_zero": "Pi_PPN[DeltaE_R11]_{<=2PN}=0 for factorized families",
            "public_status": "SUFFICIENT_THEOREM_FORMALIZED_NOT_PARENT_MAPPED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "DZ4094_3_gamma_beta_consequence",
            "statement": "If parent normal form, EH selector, Y_loc=0, and R11 factorization all hold, the nonprojector R11 obstruction to gamma/beta disappears.",
            "formula": "PNF4092 + EH4086 + Y_loc=0 + C_i~Sigma_loc => gamma_R11=beta_R11=0",
            "result_if_Y_zero": "R11 no longer blocks gamma=beta=1",
            "public_status": "CONDITIONAL_UNLOCK_NOT_PUBLIC_CLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "DZ4094_4_failure",
            "statement": "If Y_loc source currents, boundary terms, or family factorization are unsigned, the family remains a residual bound problem.",
            "formula": "not(Y=0 and all C_i~Sigma_loc) => use componentwise PPN/R10 bounds",
            "result_if_Y_zero": "not_applicable",
            "public_status": "CURRENT_CORPUS_REMAINS_NONCLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def r11_selector_matrix_rows() -> List[dict]:
    return [
        {
            "family_id": "R11DZ4094_0_R2_fR",
            "operator_family": "R2_fR_scalar_mode",
            "factorized_route": "c_R2_or_c_fR = Sigma_loc * cbar_R2 or absent/double-zero auxiliary scalar",
            "would_clear": "gamma_minus_1; beta_minus_1; alpha(lambda); R11",
            "fallback_bound": "standard f(R) template: lambda_R <= 1.337698985573e-01 R_sun if mapped to mu",
            "current_result": "MTS parent coefficient map still missing",
            "status": "ZERO_ROUTE_OR_BOUND_TEMPLATE_READY_NOT_CLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11DZ4094_1_Ricci_Weyl",
            "operator_family": "Ricci_Weyl_squared",
            "factorized_route": "Gauss-Bonnet/topological split or c_Ricci/c_Weyl = Sigma_loc * cbar_quad",
            "would_clear": "gamma_minus_1; xi; wave_sector; R11",
            "fallback_bound": "standard spin-2 template: lambda_W <= 1.163177981108e-01 R_sun if mapped to Zhu/Li convention",
            "current_result": "MTS parent Ricci/Weyl coefficient map still missing",
            "status": "ZERO_ROUTE_OR_BOUND_TEMPLATE_READY_NOT_CLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11DZ4094_2_scalar_tensor",
            "operator_family": "scalar_tensor_class_metric",
            "factorized_route": "F_phi_C constant with first derivatives zero or F_phi_C-F0 = Sigma_loc*cbar_phi",
            "would_clear": "gamma_minus_1; beta_minus_1; Gdot_over_G; alpha(lambda); R11",
            "fallback_bound": "Brans-Dicke/scalar-range style envelope needed if scalar hair survives",
            "current_result": "no parent scalar fixed/source-free theorem yet",
            "status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11DZ4094_3_torsion_nonmetricity",
            "operator_family": "torsion_nonmetricity",
            "factorized_route": "Levi-Civita branch by algebraic connection equation or c_T/c_Q = Sigma_loc*cbar_conn",
            "would_clear": "WEP; clocks; lightcone; spin/source; gamma; R11",
            "fallback_bound": "connection residual rows needed if independent torsion/nonmetricity survives",
            "current_result": "connection reduction not parent-signed",
            "status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11DZ4094_4_bulk_X",
            "operator_family": "bulk_X_force_law",
            "factorized_route": "q_X=0 by source-neutrality or q_X/c_X = Sigma_loc*cbar_X with positive mass gap",
            "would_clear": "alpha(lambda); gamma_minus_1; beta_minus_1; source_eta; R11",
            "fallback_bound": "R10 alpha(lambda) curve and PPN source map required if finite-range X survives",
            "current_result": "bulk source charge/mass gap not parent-signed",
            "status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11DZ4094_5_memory",
            "operator_family": "nonlocal_memory_kernel",
            "factorized_route": "compact-local kernel norm K_loc = Sigma_loc*Kbar or local-vacuum kernel silence",
            "would_clear": "alpha3; Gdot_over_G; alpha(lambda); hysteresis; R11",
            "fallback_bound": "kernel norm/source-history residual needed if local memory survives",
            "current_result": "compact-local kernel silence not parent-signed",
            "status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11DZ4094_6_source_normalization",
            "operator_family": "source_normalization_operator",
            "factorized_route": "Delta_mu_source in Y_loc and c_source = Sigma_loc*cbar_mu; constant common calibration allowed only if derivative-free",
            "would_clear": "beta_source; zeta_i; Gdot; radial/source hair; R11",
            "fallback_bound": "radial, boundary, bulk, species, time-drift and calibration rows required if source hair survives",
            "current_result": "domain projector piece improved by 4091/4092; nonprojector source-normalization channels live",
            "status": "PARTIAL_ZERO_ROUTE_REMAINDER_LIVE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11DZ4094_7_boundary",
            "operator_family": "boundary_topological_terms",
            "factorized_route": "topological/exact boundary or boundary flux component included in Y_loc with no-source/no-flux theorem",
            "would_clear": "zeta_i; beta; alpha3; xi; Gdot; source calibration",
            "fallback_bound": "boundary stress/source-normalization products required if no-flux theorem fails",
            "current_result": "fixed boundary reference helps but boundary source/no-flux is not public-signed",
            "status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def yloc_source_gate_rows() -> List[dict]:
    return [
        {
            "gate_id": "YSG4094_0_positive_operator",
            "required": "each Y_loc component has positive compact-local Euler operator",
            "evidence": "P8_YLOC_NO_SOURCE_THEOREM N0-N3",
            "status": "CONDITIONAL_SUFFICIENT",
            "blocks_if_fail": "Y_loc=0 cannot be derived",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "YSG4094_1_zero_source_current",
            "required": "J_Y=0 for every Y_loc component",
            "evidence": "P8_YLOC_SOURCE_DEBT_LEDGER S0-S4",
            "status": "OPEN",
            "blocks_if_fail": "Sigma_loc may be nonzero and R11 families remain live",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "YSG4094_2_zero_boundary_flux",
            "required": "B_Y=0/no-flux boundary for every Y_loc component",
            "evidence": "P8_YLOC_SOURCE_DEBT_LEDGER S0; boundary debt",
            "status": "OPEN",
            "blocks_if_fail": "boundary/source terms can feed alpha3, zeta and beta",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "YSG4094_3_no_linear_source_symmetry",
            "required": "parent symmetry forbids linear source terms in Y_loc equations",
            "evidence": "P8_YLOC_SOURCE_CURRENT_DECISION D1_possible_rescue",
            "status": "NEXT_TARGET",
            "blocks_if_fail": "must fill closure/numeric source-current rows",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "YSG4094_4_all_R11_factorized",
            "required": "every non-topological R11 family is absent/topological or multiplied by Sigma_loc",
            "evidence": "P8_DOUBLE_ZERO_R11_GATES G2_all_R11_factorized",
            "status": "OPEN",
            "blocks_if_fail": "gamma/beta/R11 remains residual-bound route",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def gamma_beta_decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "GB4094_0_conditional_unlock",
            "question": "Does Sigma_loc double-zero close the nonprojector R11 obstruction to gamma/beta?",
            "answer": "yes_if_Yloc_zero_and_all_R11_factorized",
            "formula": "Y_loc=0 and C_i=Sigma_loc*cbar_i => Pi_gamma,beta[DeltaE_R11]=0",
            "current_status": "CONDITIONAL_NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "GB4094_1_current_bound_route",
            "question": "Can current corpus claim gamma/beta because of this?",
            "answer": "no",
            "formula": "Yloc source currents and all-family factorization remain unsigned",
            "current_status": "PUBLIC_GAMMA_BETA_CLAIM_FALSE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "GB4094_2_existing_numeric_templates",
            "question": "Are any nonprojector gamma/beta families already bound-ready?",
            "answer": "standard_templates_only",
            "formula": "R2/fR lambda_R <= 0.1337698985573 R_sun; Weyl spin2 lambda_W <= 0.1163177981108 R_sun, only after MTS coefficient mapping",
            "current_status": "BOUND_TEMPLATES_READY_NOT_PARENT_COEFFICIENT_CLAIMS",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4094_0_double_zero_theorem",
            "claim": "Sigma_loc factorization is sufficient to silence nonprojector R11 if Y_loc=0",
            "allowed": "True",
            "reason": "delta Sigma_loc=0 and Sigma_loc=0 make delta(Sigma_loc O_i)=0",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4094_1_Yloc_zero",
            "claim": "current MTS parent derives Y_loc=0",
            "allowed": "False",
            "reason": "Yloc source currents and boundary terms are still open",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4094_2_all_R11_silenced",
            "claim": "all nonprojector R11 families are silenced",
            "allowed": "False",
            "reason": "all-family factorization/absence/topological maps are not parent-signed",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4094_3_gamma_beta_public",
            "claim": "public gamma=beta=1 from R11 silence",
            "allowed": "False",
            "reason": "R11 double-zero is conditional and coefficient/bound rows are nonclaim",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4094_0",
            "next_target": "4095-Y5-R2FR-Yloc-no-linear-source-symmetry-or-source-current-bound.md",
            "script": "scripts/Y5_R2FR_4095_Yloc_no_linear_source_symmetry_or_source_current_bound.py",
            "why": "4094 shows nonprojector R11 silence reduces to Y_loc=0 plus all-family Sigma_loc factorization. The hardest next pin is forbidding J_Y/B_Y linear source terms, otherwise R11 remains residual-bound.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4094_1",
            "next_target": "R2_Weyl_parent_coefficient_mapping_if_Yloc_symmetry_fails",
            "script": "defer_until_Yloc_no_linear_source_route_rejected",
            "why": "If the theorem route fails, map MTS R2/Weyl coefficients to existing 4087/4088 bound templates first.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4094_0_theorem",
            "decision": "keep Sigma_loc double-zero as the best R11 theorem route",
            "meaning": "It is mathematically sufficient and avoids fitting tiny gamma/beta residuals if parent-owned.",
            "result": "nonprojector R11 obstruction reduced to Yloc source-zero and factorization gates",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4094_1_claim_status",
            "decision": "do not promote gamma/beta or R11 silence",
            "meaning": "Yloc source currents, boundary fluxes and all-family factorization are still unsigned.",
            "result": "public local-GR remains false",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4094_2_next",
            "decision": "attack no-linear-source symmetry next",
            "meaning": "A Y_loc -> -Y_loc or equivalent parent object-language symmetry is the cleanest way to make the Euler equations homogeneous.",
            "result": "4095 target selected",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4094",
            "decision": DECISION,
            "double_zero_theorem": "sufficient_conditional",
            "Yloc_zero_public": "False",
            "R11_silence_public": "False",
            "gamma_beta_public": "False",
            "next_required_gate": "Yloc_no_linear_source_symmetry_or_source_current_bound",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def write_doc() -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 4094 - Nonprojector R11 Double-Zero Parent Selector Or Gamma/Beta Bound",
                "",
                "## Purpose",
                "",
                "4093 showed that the parent normal form fixes the source denominator and projector-domain block, but does not by itself close `gamma`, `beta`, or `zeta`. 4094 attacks the nonprojector `R11` obstruction directly.",
                "",
                f"- Decision: `{DECISION}`",
                "- Public R11 silence claim: `false`",
                "- Public `gamma=beta=1` claim: `false`",
                "",
                "## The Theorem Route",
                "",
                "The clean mechanism is still alive:",
                "",
                "```text",
                "Sigma_loc = G_AB Y_loc^A Y_loc^B",
                "Y_loc^A = 0  =>  Sigma_loc = 0 and delta Sigma_loc = 0",
                "C_i = Sigma_loc cbar_i",
                "delta(C_i O_i) = Sigma_loc cbar_i delta O_i + cbar_i O_i delta Sigma_loc = 0",
                "```",
                "",
                "So if the parent action proves `Y_loc=0` and every non-topological R11 family is absent/topological or multiplied by `Sigma_loc`, then the nonprojector R11 contribution to `gamma` and `beta` vanishes through the local PPN order being scored.",
                "",
                "## Why It Still Does Not Claim",
                "",
                "The proof hinges on two unsigned locks:",
                "",
                "- `Y_loc=0`: needs positive Euler equations plus `J_Y=0` and `B_Y=0` for each local-silence component.",
                "- all-family factorization: every non-topological R11 coefficient must be absent/topological or proportional to `Sigma_loc`.",
                "",
                "The current corpus has a good mathematical mechanism, but it has not yet parent-derived those two locks.",
                "",
                "## Bound Route If Theorem Fails",
                "",
                "Two high-priority bound templates already exist:",
                "",
                "- standard `R2/f(R)` scalar template: `lambda_R <= 0.1337698985573 R_sun` after MTS coefficient mapping;",
                "- standard Ricci/Weyl spin-2 template: `lambda_W <= 0.1163177981108 R_sun` after MTS coefficient mapping.",
                "",
                "These are not MTS claims yet because the actual parent coefficient maps are missing.",
                "",
                "## Decision",
                "",
                "Do not demote the double-zero route. It is mathematically strong enough to keep pursuing. The next target is the `Y_loc` no-linear-source symmetry: if a parent symmetry forbids `J_Y` and `B_Y`, the R11 lock moves much closer to closing.",
                "",
                "## Outputs",
                "",
                "- `P8_Y5_R2FR_4094_SOURCE_REGISTER.csv`",
                "- `P8_Y5_R2FR_4094_DOUBLE_ZERO_THEOREM.csv`",
                "- `P8_Y5_R2FR_4094_R11_SELECTOR_MATRIX.csv`",
                "- `P8_Y5_R2FR_4094_YLOC_SOURCE_GATE.csv`",
                "- `P8_Y5_R2FR_4094_GAMMA_BETA_DECISION.csv`",
                "- `P8_Y5_R2FR_4094_CLAIM_GATE.csv`",
                "- `P8_Y5_R2FR_4094_NEXT_TARGET.csv`",
                "- `P8_Y5_BRR545_4094_VALIDATION.csv`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4094_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4094_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4094_DOUBLE_ZERO_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4094_DOUBLE_ZERO_THEOREM.csv",
        "P8_Y5_R2FR_4094_R11_SELECTOR_MATRIX": SOURCE_DIR / "P8_Y5_R2FR_4094_R11_SELECTOR_MATRIX.csv",
        "P8_Y5_R2FR_4094_YLOC_SOURCE_GATE": SOURCE_DIR / "P8_Y5_R2FR_4094_YLOC_SOURCE_GATE.csv",
        "P8_Y5_R2FR_4094_GAMMA_BETA_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4094_GAMMA_BETA_DECISION.csv",
        "P8_Y5_R2FR_4094_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4094_DECISION_GATE.csv",
        "P8_Y5_R2FR_4094_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4094_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4094_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4094_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4094_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4094_STATUS.csv",
    }


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4094_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4094_DOUBLE_ZERO_THEOREM"], double_zero_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4094_R11_SELECTOR_MATRIX"], r11_selector_matrix_rows())
    write_csv(outputs["P8_Y5_R2FR_4094_YLOC_SOURCE_GATE"], yloc_source_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4094_GAMMA_BETA_DECISION"], gamma_beta_decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4094_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4094_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4094_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4094_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        rows.append(
            {
                "check_id": f"VAL4094_SRC_{source_id}",
                "check": "local source exists and contains needle",
                "passed": bool_string(contains),
                "detail": f"{path} | needle={needle} | role={role}",
                "timestamp_utc": TIMESTAMP,
            }
        )

    for name, path in outputs.items():
        try:
            parsed = parse_csv(path)
            ok = len(parsed) > 0
            detail = f"{path} rows={len(parsed)}"
        except Exception as exc:
            ok = False
            detail = f"{path} parse_error={exc}"
        rows.append(
            {
                "check_id": f"VAL4094_CSV_{name}",
                "check": "generated CSV parses and is non-empty",
                "passed": bool_string(ok),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    theorem = parse_csv(outputs["P8_Y5_R2FR_4094_DOUBLE_ZERO_THEOREM"])
    theorem_text = "\n".join(str(row) for row in theorem)
    theorem_ok = all(needle in theorem_text for needle in ["delta Sigma_loc=0", "delta[Sigma_loc cbar_i O_i]", "CURRENT_CORPUS_REMAINS_NONCLAIM"])
    rows.append(
        {
            "check_id": "VAL4094_DOUBLE_ZERO_THEOREM",
            "check": "double-zero theorem states sufficiency and nonclaim failure route",
            "passed": bool_string(theorem_ok),
            "detail": "requires delta Sigma, R11 factorization and nonclaim failure",
            "timestamp_utc": TIMESTAMP,
        }
    )

    matrix = parse_csv(outputs["P8_Y5_R2FR_4094_R11_SELECTOR_MATRIX"])
    matrix_text = "\n".join(str(row) for row in matrix)
    matrix_ok = all(
        needle in matrix_text
        for needle in [
            "R2_fR_scalar_mode",
            "Ricci_Weyl_squared",
            "scalar_tensor_class_metric",
            "torsion_nonmetricity",
            "bulk_X_force_law",
            "nonlocal_memory_kernel",
            "source_normalization_operator",
            "boundary_topological_terms",
        ]
    )
    rows.append(
        {
            "check_id": "VAL4094_R11_MATRIX_COVERAGE",
            "check": "R11 selector matrix covers nonprojector families and source-normalization/boundary remainders",
            "passed": bool_string(matrix_ok),
            "detail": f"matrix_rows={len(matrix)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    yloc = parse_csv(outputs["P8_Y5_R2FR_4094_YLOC_SOURCE_GATE"])
    yloc_text = "\n".join(str(row) for row in yloc)
    yloc_ok = all(needle in yloc_text for needle in ["J_Y=0", "B_Y=0", "NEXT_TARGET", "all_R11_factorized"])
    rows.append(
        {
            "check_id": "VAL4094_YLOC_GATE",
            "check": "Yloc gate keeps source, boundary and factorization pins explicit",
            "passed": bool_string(yloc_ok),
            "detail": "requires J_Y, B_Y, no-linear-source target, all-R11 factorization",
            "timestamp_utc": TIMESTAMP,
        }
    )

    gb = parse_csv(outputs["P8_Y5_R2FR_4094_GAMMA_BETA_DECISION"])
    gb_text = "\n".join(str(row) for row in gb)
    gb_ok = all(needle in gb_text for needle in ["yes_if_Yloc_zero", "PUBLIC_GAMMA_BETA_CLAIM_FALSE", "0.1337698985573", "0.1163177981108"])
    rows.append(
        {
            "check_id": "VAL4094_GAMMA_BETA_DECISION",
            "check": "gamma/beta decision separates conditional unlock from current false public claim and bound templates",
            "passed": bool_string(gb_ok),
            "detail": "checks conditional unlock, false claim and numeric templates",
            "timestamp_utc": TIMESTAMP,
        }
    )

    claim_rows = parse_csv(outputs["P8_Y5_R2FR_4094_CLAIM_GATE"])
    no_public = all(row.get("public_claim") == "False" and row.get("valid_for_claim") == "False" for row in claim_rows)
    rows.append(
        {
            "check_id": "VAL4094_NO_PUBLIC_CLAIM",
            "check": "4094 does not promote public Yloc/R11/gamma-beta/local-GR claim",
            "passed": bool_string(no_public),
            "detail": "all public claims remain false",
            "timestamp_utc": TIMESTAMP,
        }
    )

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    rows.append(
        {
            "check_id": "VAL4094_SCOPE",
            "check": "outputs stay in post-checkpoint-work and not formalization-workbench",
            "passed": bool_string(in_scope and not formalization_touched),
            "detail": f"doc={DOC_PATH}; csv_count={len(outputs)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = f"py_compile failed: {exc}"
    rows.append(
        {
            "check_id": "VAL4094_SCRIPT_COMPILES",
            "check": "generator script compiles",
            "passed": bool_string(compile_ok),
            "detail": compile_detail,
            "timestamp_utc": TIMESTAMP,
        }
    )

    return rows


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4094_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(f"4094 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
