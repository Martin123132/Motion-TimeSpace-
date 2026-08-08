from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4089-Y5-R2FR-curvature-square-coefficient-map-or-projector-domain-stress-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "CURVATURE_SQUARE_COEFFICIENTS_STILL_UNMAPPED_PROJECTOR_DOMAIN_STRESS_ZERO_OR_COMPONENT_BOUND_GATE_FILLED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4089_00_4088_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4088_NEXT_TARGET.csv",
        "4089-Y5-R2FR-curvature-square-coefficient-map-or-projector-domain-stress-bound.md",
        "4088 selects curvature-square coefficient mapping or projector/domain stress bound.",
    ),
    "SRC4089_01_4088_cr2_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4088_CR2_MAPPING_AUDIT.csv",
        "NO_PARENT_NUMERIC_COEFFICIENT_FOUND",
        "4088 records that curvature-square coefficient maps remain parent-unowned.",
    ),
    "SRC4089_02_4088_spin2_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4088_RICCI_WEYL_SPIN2_EXECUTABLE_BOUND.csv",
        "B4088_3_spin2_combined_range",
        "4088 fills the Ricci/Weyl spin-2 standard bound template.",
    ),
    "SRC4089_03_4086_family_route": (
        SOURCE_DIR / "P8_Y5_R2FR_4086_R11_FAMILY_TO_PPN_ROUTE.csv",
        "projector_domain_stress",
        "4086 marks projector/domain stress as feeding gamma, beta, alpha_i, xi and zeta_i.",
    ),
    "SRC4089_04_4085_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_PPN_BOUND_TABLE.csv",
        "BND4085_0_gamma_cassini",
        "4085 supplies sourced PPN component bounds.",
    ),
    "SRC4089_05_4043_factor": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_PROJECTOR_STRESS_FACTORIZATION.csv",
        "PSF4043_0_projector_metric_variation",
        "4043 factorizes the projector/domain stress pieces and selected-branch zeros.",
    ),
    "SRC4089_06_4053_silence": (
        SOURCE_DIR / "P8_Y5_R2FR_4053_PROJECTOR_SILENCE_REDUCTION_THEOREM.csv",
        "Pi_PPN[q_loc]=0",
        "4053 reduces q_loc/projector silence to explicit parent clauses.",
    ),
    "SRC4089_07_4061_kernel": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_DOMAIN_PROJECTOR_KERNEL_THEOREM.csv",
        "K_domain_parent = 0",
        "4061 states selected-branch domain projector kernel zero else bound.",
    ),
    "SRC4089_08_domain_coefficients": (
        SOURCE_DIR / "P8_mu_extra_domain_projector_coefficients.csv",
        "W_domain_alpha3_epsilon_domain_flux",
        "Existing domain-projector coefficient template gives product forms for alpha_i and xi.",
    ),
    "SRC4089_09_projector_schema": (
        SOURCE_DIR / "P8_Y5_R2FR_3979_PROJECTOR_READY_SCHEMA.csv",
        "source_profile_row",
        "3979 gives the source-profile fields required for future real projector scoring.",
    ),
    "SRC4089_10_projector_feed": (
        SOURCE_DIR / "P8_Y5_R2FR_3979_PROJECTOR_BOUND_FEED_ROWS.csv",
        "epsilon_extra_MTS_l_ge_1",
        "3979 supplies the dimensionless projector residual interface.",
    ),
}


PPN_BOUNDS = {
    "gamma_minus_1": ("2.3e-5", "dimensionless", "BND4085_0_gamma_cassini"),
    "beta_minus_1": ("8.0e-5", "dimensionless", "BND4085_1_beta_perihelion"),
    "alpha1": ("4.0e-5", "dimensionless", "BND4085_3_alpha1_pulsar_companion"),
    "alpha2": ("2.0e-9", "dimensionless", "BND4085_4_alpha2"),
    "alpha3": ("4.0e-20", "dimensionless", "BND4085_5_alpha3"),
    "xi": ("4.0e-9", "dimensionless", "BND4085_6_xi"),
    "zeta1": ("2.0e-2", "dimensionless", "BND4085_7_zeta1"),
    "zeta2": ("4.0e-5", "dimensionless", "BND4085_8_zeta2"),
    "zeta3": ("1.0e-8", "dimensionless", "BND4085_9_zeta3"),
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
        for row in rows:
            writer.writerow(row)


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
            "source_id": "SRC4089_11_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4089 projector/domain stress bound gate.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def coefficient_map_audit_rows() -> List[dict]:
    return [
        {
            "audit_id": "CMA4089_0_R2_scalar",
            "family": "R2_fR_scalar_mode",
            "standard_template_status": "4087_BOUND_TEMPLATE_FILLED",
            "parent_coefficient_status": "MTS_c_R2_TO_mu_MAP_MISSING",
            "decision": "do_not_promote",
            "next_action": "map c_R2 units/sign/normalization or prove absent/double-zero",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "audit_id": "CMA4089_1_Ricci_Weyl",
            "family": "Ricci_Weyl_squared",
            "standard_template_status": "4088_SPIN2_BOUND_TEMPLATE_FILLED",
            "parent_coefficient_status": "MTS_c_Ricci_or_c_Weyl_TO_lambda_Weyl_MAP_MISSING",
            "decision": "do_not_promote",
            "next_action": "map c_Ricci/c_Weyl units/sign/normalization or prove topological/absent/double-zero",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "audit_id": "CMA4089_2_route",
            "family": "projector_domain_stress",
            "standard_template_status": "live_4086_family",
            "parent_coefficient_status": "selected_zero_conditional_else_product_bounds_required",
            "decision": "attack_projector_domain_stress_bound",
            "next_action": "roll up exact zero clauses and create componentwise product bounds",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def projector_zero_theorem_rows() -> List[dict]:
    return [
        {
            "theorem_id": "PD4089_0_stress_split",
            "piece": "projector/domain stress factorization",
            "statement": "The live projector/domain stress decomposes into metric projector variation, domain/support motion, constraint multiplier, wall/boundary flux and extra readout denominator pieces.",
            "formula": "T_proj = T_P + T_domain + T_chi + T_wall + T_denominator",
            "zero_condition": "all 4043 pieces vanish in the selected q-basic/topological collar",
            "result": "FACTOR_SPLIT_IMPORTED",
            "status": "CONDITIONAL_ZERO_OR_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "PD4089_1_qbasic_zero",
            "piece": "metric-independent projector",
            "statement": "If the parent projector is q-basic/topological and source-silent before readout, then delta_g P_D=0 and D_D P_D=0, so the metric-variation and domain-motion stress kernels vanish.",
            "formula": "delta_g P_D = 0 and D_D P_D = 0 => T_P=T_domain=0",
            "zero_condition": "parent owns P_D as a fixed topological/readout label, not a dynamical stress carrier",
            "result": "EXACT_CONDITIONAL_PROJECTOR_METRIC_DOMAIN_ZERO",
            "status": "CONDITIONAL_PARENT_OWNERSHIP_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "PD4089_2_wall_constraint_zero",
            "piece": "wall and constraint stress",
            "statement": "If the selected compact collar has no active selector multiplier, no wall flux, no STF wall stress and no second projector denominator, then the remaining projector/domain stress pieces vanish.",
            "formula": "chi_local=lambda_local=Phi_D=tau_wall_TF=0 and same Hilbert denominator => T_chi=T_wall=T_denominator=0",
            "zero_condition": "4061 selected branch clauses adopted before variation/readout",
            "result": "EXACT_CONDITIONAL_WALL_CONSTRAINT_DENOMINATOR_ZERO",
            "status": "CONDITIONAL_PARENT_OWNERSHIP_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "PD4089_3_ppn_zero_consequence",
            "piece": "PPN projection",
            "statement": "If the zero clauses hold, the projector/domain branch contributes no gamma, beta, alpha_i, xi or zeta_i residual through the local <=2PN branch.",
            "formula": "Pi_PPN[T_proj] = 0",
            "zero_condition": "PD4089_1 and PD4089_2 both signed",
            "result": "EXACT_CONDITIONAL_PROJECTOR_DOMAIN_PPN_ZERO",
            "status": "CONDITIONAL_NOT_PUBLIC_PROOF",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "PD4089_4_failure_to_bounds",
            "piece": "fallback",
            "statement": "If any projector zero clause is rejected, every surviving stress product must be scored componentwise against 4085 bounds with no cancellation credit.",
            "formula": "|W_j epsilon_j| <= B_j for each j in {gamma,beta,alpha_i,xi,zeta_i}",
            "zero_condition": "none; fallback branch",
            "result": "PROJECTOR_DOMAIN_COMPONENT_BOUND_GATE",
            "status": "EXECUTABLE_BOUND_ROUTE_SELECTED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def component_bound_rows() -> List[dict]:
    specs = [
        ("PDB4089_0_gamma", "gamma_minus_1", "W_proj_gamma * epsilon_projector_TF", "projector/domain tracefree spatial stress", "PROJ4086_1_gamma"),
        ("PDB4089_1_beta", "beta_minus_1", "W_proj_beta * epsilon_projector_00_2PN", "projector/source-denominator second-order 00 stress", "PROJ4086_2_beta"),
        ("PDB4089_2_alpha1", "alpha1", "W_domain_alpha1 * epsilon_domain_vector", "domain vector/preferred-frame drift", "PROJ4086_3_preferred_frame"),
        ("PDB4089_3_alpha2", "alpha2", "W_domain_alpha2 * epsilon_domain_vector", "domain vector/preferred-frame spin/precession channel", "PROJ4086_3_preferred_frame"),
        ("PDB4089_4_alpha3", "alpha3", "W_domain_alpha3 * epsilon_domain_flux", "domain flux/self-acceleration channel", "PROJ4086_3_preferred_frame"),
        ("PDB4089_5_xi", "xi", "W_domain_xi * epsilon_domain_anisotropy", "preferred-location/domain anisotropy", "PROJ4086_3_preferred_frame"),
        ("PDB4089_6_zeta1", "zeta1", "W_proj_zeta1 * epsilon_source_leak_1", "conservation/source-current leak 1", "PROJ4086_4_conservation"),
        ("PDB4089_7_zeta2", "zeta2", "W_proj_zeta2 * epsilon_source_leak_2", "conservation/source-current leak 2", "PROJ4086_4_conservation"),
        ("PDB4089_8_zeta3", "zeta3", "W_proj_zeta3 * epsilon_source_leak_3", "conservation/source-current leak 3", "PROJ4086_4_conservation"),
    ]
    rows: List[dict] = []
    for bound_id, observable, product, meaning, projection in specs:
        bound_value, units, source_id = PPN_BOUNDS[observable]
        rows.append(
            {
                "bound_id": bound_id,
                "observable": observable,
                "projector_product": product,
                "meaning": meaning,
                "bound_value": bound_value,
                "bound_units": units,
                "unit_coefficient_epsilon_bound": bound_value,
                "pass_rule": f"abs({product}) <= {bound_value}",
                "projection_source": projection,
                "bound_source": source_id,
                "current_status": "PRODUCT_BOUND_READY_COEFFICIENT_OR_ZERO_CERTIFICATE_REQUIRED",
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def absolute_score_rows() -> List[dict]:
    return [
        {
            "score_id": "PDS4089_0_abs_vector",
            "score": "Delta_projector_abs",
            "formula": "sum_j abs(W_j epsilon_j)",
            "rule": "diagnostic only; each component must pass individually before any local-GR use",
            "status": "NO_CANCELLATION_GUARD",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "score_id": "PDS4089_1_hardest_bound",
            "score": "hardest_projector_component",
            "formula": "alpha3 bound = 4.0e-20 is the harshest component if domain flux channel is live",
            "rule": "a live alpha3 projector flux needs an exact zero theorem or an exceptionally tiny sourced product",
            "status": "ALPHA3_PRESSURE_IDENTIFIED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "score_id": "PDS4089_2_zero_preferred",
            "score": "best_route",
            "formula": "prove q-basic/topological projector ownership instead of numerically fitting alpha3",
            "rule": "because alpha3 is so tight, the lower-scrutiny route is parent zero, not small free coefficient",
            "status": "ROUTE_SELECTION",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def r11_update_rows() -> List[dict]:
    return [
        {
            "update_id": "R11UP4089_0",
            "operator_family": "R2_fR_scalar_mode",
            "previous_status": "FILLED_STANDARD_FR_SCALAR_GAMMA_BETA_BOUND_TEMPLATE",
            "new_status": "PARENT_COEFFICIENT_MAP_STILL_MISSING",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "update_id": "R11UP4089_1",
            "operator_family": "Ricci_Weyl_squared",
            "previous_status": "FILLED_STANDARD_WEYL_SPIN2_GAMMA_BETA_BOUND_TEMPLATE",
            "new_status": "PARENT_COEFFICIENT_MAP_STILL_MISSING",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "update_id": "R11UP4089_2",
            "operator_family": "projector_domain_stress",
            "previous_status": "LIVE_PROJECTOR_STRESS_BRANCH_IF_TOPOLOGICAL_OWNERSHIP_UNSIGNED",
            "new_status": "EXACT_CONDITIONAL_ZERO_OR_COMPONENTWISE_PPN_BOUND_GATE_FILLED",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4089_0_main",
            "decision": DECISION,
            "meaning": "Curvature-square families have standard templates but no MTS coefficient map. Projector/domain stress now has a clean exact-zero route and a componentwise fallback bound table.",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_required_move": "Try to parent-sign q-basic/topological projector ownership; if not, fill actual W_j epsilon_j products, starting with alpha3 flux because it is the harshest bound.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4089_1_best_route",
            "decision": "PROJECTOR_ZERO_PROOF_BEATS_NUMERIC_ALPHA3_TUNING",
            "meaning": "The alpha3 projector bound is 4e-20. A free small number here will look tuned; a parent theorem that the projector is metric-independent/topological is the cleaner route.",
            "claim_status": "ROUTE_SELECTION",
            "next_required_move": "Derive or reject absolute q-basic projector ownership in the parent action.",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4089_0_projector_zero",
            "claim": "Projector/domain stress is zero in MTS local branch",
            "allowed": "False",
            "why_not": "4089 gives exact conditional zero clauses, but parent q-basic/topological ownership is still not public-claim signed.",
            "minimum_unlock": "Parent action proves delta_g P_D=0, D_D P_D=0, no wall/constraint stress, and same Hilbert denominator before readout.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4089_1_projector_bound",
            "claim": "Projector/domain stress passes PPN bounds",
            "allowed": "False",
            "why_not": "Componentwise product bounds are ready, but no sourced W_j epsilon_j values exist.",
            "minimum_unlock": "Fill every live product with source path, units, same-frame normalization, and no-cancellation proof.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4089_2_local_GR",
            "claim": "MTS reduces to local GR",
            "allowed": "False",
            "why_not": "Projector branch is only one R11/source/readout sector; other gates remain live.",
            "minimum_unlock": "All 4086 R11 family rows zeroed/bounded plus source/readout/conservation gates.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4089_3_forward_progress",
            "claim": "4089 advances the framework",
            "allowed": "True_private_checkpoint",
            "why_not": "Private derivation/bound gate only.",
            "minimum_unlock": "N/A",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4089_0",
            "next_target": "4090-Y5-R2FR-parent-qbasic-projector-ownership-or-alpha3-product-fill.md",
            "script": "scripts/Y5_R2FR_4090_parent_qbasic_projector_ownership_or_alpha3_product_fill.py",
            "why": "4089 shows the clean route is projector zero, while the fallback's harshest live product is alpha3 at 4e-20. Next either prove q-basic/topological parent ownership or fill the alpha3 product row.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4089_1",
            "next_target": "curvature_square_parent_coefficient_map_parallel",
            "script": "defer_until_parent_action_coefficient_sources_selected",
            "why": "R2 and Weyl bounds are ready but cannot promote until actual MTS coefficient normalizations are found.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4089",
            "status": "private_nonclaim_checkpoint_complete",
            "decision": DECISION,
            "public_claim": "False",
            "github_action": "False",
            "formalization_workbench_modified_by_script": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def validation_rows(output_paths: Iterable[Path]) -> List[dict]:
    paths = list(output_paths)
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        add(
            f"VAL4089_SRC_{source_id}",
            "local source exists and contains needle",
            bool(exists and contains),
            f"{path} | needle={needle} | role={role}",
        )

    for path in paths:
        rows = parse_csv(path)
        add(
            f"VAL4089_CSV_{path.stem}",
            "generated CSV parses and is non-empty",
            bool(rows),
            f"{path} rows={len(rows)}",
        )

    theorem_results = {row["result"] for row in projector_zero_theorem_rows()}
    add(
        "VAL4089_ZERO_AND_BOUND_ROUTES",
        "projector zero route and fallback bound route are both present",
        "EXACT_CONDITIONAL_PROJECTOR_DOMAIN_PPN_ZERO" in theorem_results and "PROJECTOR_DOMAIN_COMPONENT_BOUND_GATE" in theorem_results,
        f"results={sorted(theorem_results)}",
    )

    bound_rows = component_bound_rows()
    required_observables = set(PPN_BOUNDS)
    present_observables = {row["observable"] for row in bound_rows}
    all_positive = all(float(row["bound_value"]) > 0.0 for row in bound_rows)
    add(
        "VAL4089_COMPONENT_BOUND_COVERAGE",
        "component bound rows cover gamma beta alpha xi zeta with positive sourced bounds",
        required_observables.issubset(present_observables) and all_positive,
        f"missing={sorted(required_observables - present_observables)}; all_positive={all_positive}",
    )

    alpha3_row = next(row for row in bound_rows if row["observable"] == "alpha3")
    add(
        "VAL4089_ALPHA3_HARDEST_BOUND",
        "alpha3 projector flux bound is explicitly present",
        alpha3_row["bound_value"] == "4.0e-20",
        f"alpha3_bound={alpha3_row['bound_value']}",
    )

    outputs_inside_post_checkpoint = all(is_under(path, ROOT) for path in paths) and is_under(DOC_PATH, ROOT)
    outputs_outside_formalization = all(not is_under(path, FORMALIZATION) for path in paths) and not is_under(DOC_PATH, FORMALIZATION)
    add(
        "VAL4089_SCOPE",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        bool(outputs_inside_post_checkpoint and outputs_outside_formalization),
        f"doc={DOC_PATH}; csv_count={len(paths)}",
    )

    no_claim = all(row.get("valid_for_claim", "False") != "True" for row in component_bound_rows())
    no_claim = no_claim and all(row.get("valid_for_claim", "False") != "True" for row in projector_zero_theorem_rows())
    no_claim = no_claim and all(row.get("allowed") != "True" for row in claim_gate_rows() if row["claim_id"] != "CLAIM4089_3_forward_progress")
    add(
        "VAL4089_NO_LOCAL_GR_CLAIM",
        "4089 remains a private nonclaim checkpoint",
        no_claim,
        "claim gates keep projector/local-GR claims false until parent zero or product values exist",
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4089_SCRIPT_COMPILES", "generator script compiles", compile_ok, compile_detail)

    return checks


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4089 - Curvature Square Coefficient Map Or Projector Domain Stress Bound

- Timestamp: `{TIMESTAMP}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public local-GR/projector pass claim: `false`
- GitHub action: `false`

## Result

4089 confirms that the curvature-square standard bound templates from 4087 and 4088 still do **not** have parent-owned MTS coefficient maps.

So the useful route is the projector/domain stress branch:

```text
Route A: prove selected projector/domain stress is exactly zero.
Route B: if not, each surviving product must pass its own PPN bound.
```

## Exact Zero Route

The selected branch is zero if the parent owns the projector as a q-basic/topological readout label:

```text
delta_g P_D = 0
D_D P_D = 0
chi_local = lambda_local = 0
Phi_D = 0
tau_wall_TF = 0
same Hilbert denominator
```

Then:

```text
T_proj = T_P + T_domain + T_chi + T_wall + T_denominator = 0
Pi_PPN[T_proj] = 0
```

That would silence projector contributions to gamma, beta, alpha_i, xi and zeta_i.

## Fallback Bound Route

If the zero route fails, the branch becomes componentwise:

```text
|W_gamma epsilon_projector_TF| <= 2.3e-5
|W_beta epsilon_projector_00_2PN| <= 8.0e-5
|W_alpha1 epsilon_domain_vector| <= 4.0e-5
|W_alpha2 epsilon_domain_vector| <= 2.0e-9
|W_alpha3 epsilon_domain_flux| <= 4.0e-20
|W_xi epsilon_domain_anisotropy| <= 4.0e-9
|W_zeta1 epsilon_source_leak_1| <= 2.0e-2
|W_zeta2 epsilon_source_leak_2| <= 4.0e-5
|W_zeta3 epsilon_source_leak_3| <= 1.0e-8
```

No component is allowed to cancel another. The `alpha3` row is the brutal one: a live domain-flux channel wants an exact zero theorem, not a fitted small number.

## What Improved

This is not just another blocker ledger. The projector branch now has:

```text
exact zero theorem clauses
explicit failure-to-bound route
componentwise numerical PPN thresholds
hardest-channel identification
next target selected
```

## Decision

```text
curvature-square coefficient maps = still missing
projector zero route = exact conditional
projector fallback = componentwise bound table
local GR claim = still false
next = parent q-basic projector ownership or alpha3 product fill
```

## Next

```text
4090-Y5-R2FR-parent-qbasic-projector-ownership-or-alpha3-product-fill.md
```
""",
        encoding="utf-8",
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    outputs = {
        "P8_Y5_R2FR_4089_SOURCE_REGISTER.csv": source_register_rows(),
        "P8_Y5_R2FR_4089_CURVATURE_SQUARE_MAP_AUDIT.csv": coefficient_map_audit_rows(),
        "P8_Y5_R2FR_4089_PROJECTOR_ZERO_THEOREM.csv": projector_zero_theorem_rows(),
        "P8_Y5_R2FR_4089_PROJECTOR_COMPONENT_BOUND_VECTOR.csv": component_bound_rows(),
        "P8_Y5_R2FR_4089_PROJECTOR_ABSOLUTE_SCORE_GUARD.csv": absolute_score_rows(),
        "P8_Y5_R2FR_4089_R11_VECTOR_UPDATE.csv": r11_update_rows(),
        "P8_Y5_R2FR_4089_DECISION_GATE.csv": decision_rows(),
        "P8_Y5_R2FR_4089_CLAIM_GATE.csv": claim_gate_rows(),
        "P8_Y5_R2FR_4089_NEXT_TARGET.csv": next_target_rows(),
        "P8_Y5_R2FR_4089_STATUS.csv": status_rows(),
    }

    output_paths: List[Path] = []
    for name, rows in outputs.items():
        path = SOURCE_DIR / name
        write_csv(path, rows)
        output_paths.append(path)

    write_doc()

    validation = validation_rows(output_paths)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4089_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    shutil.rmtree(SCRIPT_PATH.parent / "__pycache__", ignore_errors=True)

    failures = [row for row in validation if row["passed"] != "True"]
    if failures:
        for failure in failures:
            print(f"VALIDATION_FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)

    print(f"4089 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
