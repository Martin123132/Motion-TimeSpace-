from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3886"
BRANCH = "MTS_R2FR_Y5_EH_ONLY_R11_SELECTOR_OR_EXECUTABLE_PPN_COEFFICIENT_VECTOR_3886"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3886-Y5-R2FR-EH-only-R11-selector-or-executable-PPN-coefficient-vector.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3885_NEXT = OUT / "P8_Y5_R2FR_3885_NEXT_TARGET.csv"
CSV_3885_THEOREM = OUT / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv"
CSV_3885_R11 = OUT / "P8_Y5_R2FR_3885_R11_OPERATOR_RESIDUAL_VECTOR.csv"
CSV_3885_PPN = OUT / "P8_Y5_R2FR_3885_PPN_PARAMETER_RESIDUAL_ROWS.csv"
CSV_3885_GATE = OUT / "P8_Y5_R2FR_3885_LOCAL_GR_PROMOTION_GATE.csv"
CSV_3885_VALIDATION = OUT / "P8_Y5_BRR545_3885_VALIDATION.csv"
CSV_DZ_PROOF = OUT / "P8_DOUBLE_ZERO_R11_VARIATION_PROOF.csv"
CSV_DZ_MAPPING = OUT / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv"
CSV_DZ_GATES = OUT / "P8_DOUBLE_ZERO_R11_GATES.csv"
CSV_DZ_PARENT = OUT / "P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv"
CSV_LOCAL_EH_SELECTOR = OUT / "P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv"
CSV_LOCAL_EH_DECISION = OUT / "P8_LOCAL_EH_R11_DECISION.csv"
CSV_R11_MIN_FILL = OUT / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"
CSV_R11_BOUNDARY_FILL = OUT / "P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv"
CSV_LOVELOCK = OUT / "P8_Y5_LOVELOCK_GATE_2622_OPERATOR_SELECTION_VERDICT.csv"
CSV_EH_DOM = OUT / "P8_Y5_EH_DOMINANCE_GATE_2620_OPERATOR_COEFFICIENT_PACK.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3886_SOURCE_REGISTER.csv",
    "selector": OUT / "P8_Y5_R2FR_3886_DOUBLE_ZERO_SELECTOR_DERIVATION_AUDIT.csv",
    "family": OUT / "P8_Y5_R2FR_3886_R11_FAMILY_SELECTOR_OR_FILL_MATRIX.csv",
    "coefficients": OUT / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv",
    "gate": OUT / "P8_Y5_R2FR_3886_LOCAL_GR_DECISION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3886_RUNNER_UPDATE.csv",
    "next": OUT / "P8_Y5_R2FR_3886_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3886_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3886_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3886_00_next", CSV_3885_NEXT, "NEXT3885_0", "3885 target selecting EH/R11 proof or executable vector"),
    ("SRC3886_01_ppn_theorem", CSV_3885_THEOREM, "PPT3885_0_target", "conditional GR PPN theorem target"),
    ("SRC3886_02_r11_vector", CSV_3885_R11, "R11V3885_0_total", "active R11 residual vector"),
    ("SRC3886_03_ppn_rows", CSV_3885_PPN, "PPN3885_0_gamma", "PPN coefficient residual rows"),
    ("SRC3886_04_local_gr_gate", CSV_3885_GATE, "LGG3885_5_local_GR", "local-GR no-claim gate"),
    ("SRC3886_05_3885_validation", CSV_3885_VALIDATION, "VAL3885_14_next_target", "3885 validation target"),
    ("SRC3886_06_double_zero_variation", CSV_DZ_PROOF, "V1_composite_delta_zero", "double-zero first-variation proof"),
    ("SRC3886_07_double_zero_mapping", CSV_DZ_MAPPING, "R2_fR_scalar_mode", "R11 family mapping"),
    ("SRC3886_08_double_zero_gates", CSV_DZ_GATES, "G0_Yloc_parent_owned", "known selector proof failures"),
    ("SRC3886_09_parent_clause", CSV_DZ_PARENT, "C2_R11_factorization", "candidate parent action clause"),
    ("SRC3886_10_selector_lemma", CSV_LOCAL_EH_SELECTOR, "L2_double_zero_sufficient", "double-zero sufficiency lemma"),
    ("SRC3886_11_selector_decision", CSV_LOCAL_EH_DECISION, "D2_actual_R11_rows", "actual rows not yet selected"),
    ("SRC3886_12_source_norm_fill", CSV_R11_MIN_FILL, "R11SN_4_nonEH_operator_potential", "source-normalization coefficient fill debt"),
    ("SRC3886_13_boundary_fill", CSV_R11_BOUNDARY_FILL, "F6_projector_stress", "projector/domain stress fill debt"),
    ("SRC3886_14_lovelock", CSV_LOVELOCK, "OPS2622_4_overall", "Lovelock/EH-selection verdict"),
    ("SRC3886_15_eh_dominance", CSV_EH_DOM, "OPC2620_7_total_DeltaE", "EH dominance operator coefficient pack"),
]

SIGMA_DEFINITION = "Sigma_loc = G_AB(g,u,D) Y_loc^A Y_loc^B >= 0"
DOUBLE_ZERO_VARIATION = "delta Sigma_loc=0 at Y_loc^A=0 because delta Sigma_loc = delta G_AB Y^A Y^B + 2 G_AB Y^A delta Y^B"
R11_FACTOR_VARIATION = "delta[Sigma_loc c_A O_A] = c_A Sigma_loc delta O_A + c_A O_A delta Sigma_loc + Sigma_loc O_A delta c_A = 0 at Y_loc^A=0"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        cells = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_EH_only_R11_selector_or_executable_vector",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def selector_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        (
            "DZS3886_0_local_silence_multiplet",
            "Define Y_loc^A to contain every compact-local leak: domain vector, boundary flux, projector stress, source-normalization drift, nonlocal memory norm, bulk-X charge and non-EH selector marker.",
            "Y_loc^A={X_D,Qcoh_D,Phi_boundary^i,V_domain^i,S_TF_domain,Delta_mu_source,K_history,q_X,...}",
            "CONTRACT_COMPLETE_ENOUGH_TO_TEST",
            "parent Euler equations forcing Y_loc^A=0 are not derived",
        ),
        (
            "DZS3886_1_composite_selector",
            "Use a composite squared selector, not an independent switch.",
            SIGMA_DEFINITION,
            "DOUBLE_ZERO_CANDIDATE",
            "positivity and ownership of G_AB remain parent-action clauses",
        ),
        (
            "DZS3886_2_first_variation",
            "At the local-zero branch the first variation of the selector vanishes, so this is not a single-zero leakage trick.",
            DOUBLE_ZERO_VARIATION,
            "DERIVED_CONDITIONAL_ZERO",
            "only conditional on Y_loc^A=0 being an Euler consequence",
        ),
        (
            "DZS3886_3_R11_factor",
            "If every non-topological R11 family appears only through Sigma_loc c_A O_A with finite O_A and c_A, the whole non-EH first variation is silent locally.",
            R11_FACTOR_VARIATION,
            "DERIVED_CONDITIONAL_EH_ONLY_SELECTOR",
            "actual R11 rows are not yet all proven to use this parent factor",
        ),
        (
            "DZS3886_4_boundary_topological_escape",
            "Boundary/topological pieces are allowed only if exactly topological, scalar no-flux, or included in Y_loc so their first variation also double-zeros.",
            "delta S_top=0 or S_boundary=Sigma_loc c_B O_boundary or boundary flux component in Y_loc",
            "CONDITIONAL_ESCAPE_ROUTE",
            "boundary/no-flux theorem still open",
        ),
        (
            "DZS3886_5_Bianchi_stress",
            "Projector/domain/readout stresses cannot disappear by naming them; they must be included in T_H, be topological, or be Sigma_loc-selected so Bianchi closure survives.",
            "nabla_mu(G^mu_nu+DeltaE^mu_nu)=kappa_0 nabla_mu T_H^mu_nu with DeltaE^mu_nu=0 on branch",
            "CONDITIONAL_STRESS_CLOSURE",
            "projector/domain stress variation remains unproven",
        ),
        (
            "DZS3886_6_verdict",
            "3886 constructs a real local EH-only mechanism: double-zero selection can silence R11 to first variation. It still cannot claim local GR until Y_loc=0 and universal factorization are parent-derived.",
            "EH-only local branch = EH action + same Hilbert source + Sigma_loc-selected R11 + silent boundary terms",
            "MECHANISM_FOUND_BUT_NOT_PARENT_SIGNED",
            "next target is Y_loc Euler-zero proof or coefficient fill",
        ),
    ]
    return [
        {
            "audit_id": row_id,
            "claim_tested": claim,
            "derivation_or_condition": derivation,
            "result": result,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, claim, derivation, result, failure in raw_rows
    ]


def family_rows(timestamp: str) -> list[dict[str, object]]:
    source_rows = read_csv_rows(CSV_DZ_MAPPING)
    rows = []
    for index, source in enumerate(source_rows):
        family = source["operator_family"]
        candidate = source["candidate_factorized_form"]
        if family == "boundary_topological_terms":
            selector_status = "CONDITIONAL_ZERO_IF_TOPOLOGICAL_OR_SIGMA_BOUNDARY_PARENT_SIGNED"
            fill = "source c_boundary/c_GB or prove scalar no-flux/topological variation"
        elif family == "projector_domain_stress":
            selector_status = "CONDITIONAL_ZERO_IF_PROJECTOR_STRESS_INCLUDED_IN_YLOC_OR_TOPOLOGICAL"
            fill = "derive metric-independent PiM/projection or fill retained stress coefficient"
        else:
            selector_status = "CONDITIONAL_ZERO_IF_SIGMA_FACTOR_PARENT_SIGNED"
            fill = "prove parent coefficient proportional to Sigma_loc or fill numeric coefficient/bound"
        rows.append(
            {
                "family_id": f"R11F3886_{index:02d}_{family}",
                "operator_family": family,
                "coefficient_symbol": source["coefficient_symbol"],
                "affected_rows": source["affected_rows"],
                "required_selector_or_escape": source["required_parent_factorization"],
                "candidate_factorized_form": candidate,
                "3886_result": selector_status,
                "if_selector_fails_required_fill": fill,
                "current_status": "NOT_CLAIMED_PARENT_FACTOR_NOT_SIGNED",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def coefficient_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("COEF3886_00_delta_gamma_R11", "delta_gamma_R11", "dimensionless", "weak-field anisotropic/spatial-temporal potential split from DeltaE_munu", "gamma-1", "R3_gamma;R11", "MISSING_WEAK_FIELD_MAP_FOR_ALL_ACTIVE_R11_FAMILIES"),
        ("COEF3886_01_A_source", "A_source", "dimensionless_or_source_normalization", "linear source response in g00 potential", "beta source law; Newton normalization", "R4_beta;Newton_G", "MISSING_PARENT_SOURCE_NORMALIZATION"),
        ("COEF3886_02_B_source", "B_source", "dimensionless_or_source_normalization", "quadratic source response in g00 potential", "beta_eff=B_source/A_source^2", "R4_beta", "MISSING_PARENT_SECOND_ORDER_SOURCE_RESPONSE"),
        ("COEF3886_03_delta_beta_source", "delta_beta_source", "dimensionless", "B_source/A_source^2 - 1", "beta-1", "R4_beta", "EXECUTABLE_FORMULA_READY_INPUTS_MISSING"),
        ("COEF3886_04_delta_beta_R11", "delta_beta_R11", "dimensionless", "sum of second-order non-EH operator contributions", "beta-1", "R4_beta;R11", "MISSING_R11_WEAK_FIELD_COEFFICIENTS"),
        ("COEF3886_05_delta_beta_q_loc", "delta_beta_q_loc", "dimensionless", "local projection/bulk-X q_loc contribution through O(U^2)", "beta-1;R10", "R4_beta;R10", "MISSING_QLOC_SECOND_ORDER_PROFILE"),
        ("COEF3886_06_alpha1", "alpha1", "dimensionless", "domain/vector/frame/memory preferred-frame channel", "alpha1", "R5_alpha1", "MISSING_NO_VECTOR_SELECTOR_OR_NUMERIC_COEFFICIENT"),
        ("COEF3886_07_alpha2", "alpha2", "dimensionless", "domain/vector/frame/memory preferred-frame channel", "alpha2", "R6_alpha2", "MISSING_NO_VECTOR_SELECTOR_OR_NUMERIC_COEFFICIENT"),
        ("COEF3886_08_alpha3", "alpha3", "dimensionless", "boundary/domain/flux/nonconservation channel", "alpha3", "R7_alpha3", "MISSING_ALPHA3_CHANNEL_ZERO_OR_BOUNDS"),
        ("COEF3886_09_xi", "xi", "dimensionless", "preferred-location anisotropy/domain/boundary/nonlocal channel", "xi", "R8_xi", "MISSING_STF_ANISOTROPY_ZERO_OR_COEFFICIENT"),
        ("COEF3886_10_zeta_i", "zeta_i", "dimensionless", "stress nonconservation or non-Hilbert source leakage vector", "zeta_i", "PPN_conservation", "MISSING_TOTAL_STRESS_CONSERVATION_VECTOR"),
        ("COEF3886_11_alpha_lambda", "alpha(lambda)", "range_dependent", "finite-range R11/bulk-X/source-normalization Yukawa profile", "R10 alpha(lambda)", "R10", "MISSING_REAL_BOUND_CURVE_PLUS_PREDICTION_COEFFICIENTS"),
        ("COEF3886_12_R11_total", "DeltaE_munu", "curvature_operator_units", "sum_A c_A O_A_munu, or zero if all non-EH families Sigma_loc-selected/topological", "PPN;R10;clocks;orbits", "R11", "MISSING_UNIVERSAL_SELECTOR_OR_EXECUTABLE_COEFFICIENT_VECTOR"),
        ("COEF3886_13_projector_stress", "T_extra_munu_or_c_projector_domain_stress", "stress_units_or_dimensionless_residual", "retained projector/domain stress if not topological or Sigma_loc-selected", "gamma;beta;alpha_i;zeta_i", "R11", "MISSING_PROJECTOR_VARIATION_OR_BOUND"),
    ]
    return [
        {
            "coefficient_id": row_id,
            "symbol": symbol,
            "units": units,
            "definition_or_formula": definition,
            "feeds": feeds,
            "observable_link": observable,
            "current_status": status,
            "source_path": "source-intake\\mts_residuals\\P8_Y5_R2FR_3886_R11_FAMILY_SELECTOR_OR_FILL_MATRIX.csv",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, units, definition, feeds, observable, status in raw_rows
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("LGG3886_0_first_order_newton", "first-order Newton candidate", "3882-3884 constant coupling/same Hilbert source/PiM-Gauss/orbital readout ladder", "PASS_CANDIDATE_NONCLAIM"),
        ("LGG3886_1_double_zero_math", "double-zero selector variation", DOUBLE_ZERO_VARIATION, "PASS_CONDITIONAL_MECHANISM"),
        ("LGG3886_2_R11_variation", "Sigma_loc-selected R11 first variation", R11_FACTOR_VARIATION, "PASS_IF_PARENT_FACTOR_SIGNED"),
        ("LGG3886_3_Yloc_Euler", "Yloc Euler-zero", "parent equations force all Y_loc^A=0 in compact local vacuum/stationary domain", "FAIL_NOT_DERIVED"),
        ("LGG3886_4_universal_factorization", "universal R11 factorization", "every actual non-EH/R11 family uses Sigma_loc factor or exact topological escape", "FAIL_NOT_DERIVED_FOR_ACTUAL_ROWS"),
        ("LGG3886_5_boundary_projector_Bianchi", "boundary/projector/Bianchi closure", "boundary/projector/domain stresses either vanish, are topological, or remain conserved retained stresses", "FAIL_OPEN"),
        ("LGG3886_6_executable_vector", "executable coefficient vector", "if selector fails, every coefficient row has units/source/path/numeric weak-field map", "FAIL_SKELETON_ONLY"),
        ("LGG3886_7_local_GR", "local-GR promotion", "all selector, factorization, boundary/projector/Bianchi and coefficient-vector gates pass simultaneously", "BLOCKED_NO_CLAIM"),
    ]
    return [
        {
            "gate_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3886_0_selector", "EH_only_selector", "if Y_loc^A=0 and every R11 family is Sigma_loc-selected/topological, set DeltaE_munu^R11=0 through first variation", "CONDITIONAL_SELECTOR_IMPLEMENTED"),
        ("RUNU3886_1_no_single_zero", "selector_guard", "reject F(Z)=Z unless F_prime(0)=0 or another parent zero removes the variation", "DOUBLE_ZERO_REQUIRED"),
        ("RUNU3886_2_coefficient_vector", "PPN_R11_vector", "otherwise evaluate gamma,beta,alpha_i,xi,zeta_i,alpha(lambda),DeltaE_munu row-by-row with no cancellation credit", "SKELETON_READY"),
        ("RUNU3886_3_claim_guard", "local_GR_claim", "false until Yloc Euler, universal factorization, boundary/projector/Bianchi and executable vector gates close", "NO_LOCAL_GR_CLAIM"),
        ("RUNU3886_4_next", "next_attack", "derive Y_loc Euler-zero mechanism before more coefficient shopping, unless a family refuses factorization", "NEXT_3887"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3886_0",
            "target_checkpoint": "3887-Y5-R2FR-Yloc-Euler-zero-proof-or-R11-coefficient-fill.md",
            "script": "scripts/Y5_R2FR_3887_Yloc_Euler_zero_proof_or_R11_coefficient_fill.py",
            "objective": "derive the parent Euler equations or variational descent that forces Y_loc^A=0 in compact local domains; if that fails, begin filling the executable R11/PPN coefficient vector with real source-backed rows",
            "why_next": "3886 found the conditional double-zero mechanism, so the live missing theorem is no longer the algebra; it is the parent-owned local-zero equation for Y_loc and universal R11 factorization",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3886_0",
            "branch": BRANCH,
            "summary": "conditional EH-only/R11 double-zero selector mechanism constructed; local-GR still blocked because Y_loc Euler-zero, universal factorization, boundary/projector/Bianchi closure and executable coefficient rows are not parent-signed",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    selector: list[dict[str, object]],
    family: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3886 - EH-only R11 Selector or Executable PPN Coefficient Vector

Generated: `{timestamp}`

## Result

3886 makes the first real leap on the local-GR route: the local R11 problem has a candidate mechanism, not just a gap label.

Define:

`{SIGMA_DEFINITION}`

Then:

`{DOUBLE_ZERO_VARIATION}`

For any non-topological R11 term parent-written as `int sqrt(-g) Sigma_loc c_A O_A[g,psi]`:

`{R11_FACTOR_VARIATION}`

So the mechanism is mathematically useful: if `Y_loc^A=0` is a parent Euler consequence and every local non-EH family is either `Sigma_loc`-selected, absent, or exactly topological/boundary-silent, the compact local branch is EH-only to first variation.

But it is not yet a local-GR claim. The algebra is now the good bit; the remaining hard proof is parent ownership of `Y_loc^A=0`, universal factorization of the actual R11 rows, and boundary/projector/Bianchi silence.

## Selector Derivation Audit

{markdown_table(selector, ["audit_id", "claim_tested", "derivation_or_condition", "result", "remaining_failure"])}

## R11 Family Selector or Fill Matrix

{markdown_table(family, ["family_id", "operator_family", "coefficient_symbol", "3886_result", "if_selector_fails_required_fill", "current_status"])}

## Executable PPN/R11 Coefficient Skeleton

{markdown_table(coefficients, ["coefficient_id", "symbol", "units", "definition_or_formula", "feeds", "current_status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "requirement", "status", "claim_allowed"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is progress. 3886 does not merely say "R11 missing"; it extracts the exact mechanism that could make the local branch GR-like: a parent-owned double-zero selector. The next checkpoint should attack the Euler equation that makes `Y_loc^A=0`; if that cannot be derived, the theory must pay the harder price and fill the executable PPN/R11 coefficient vector with real numbers.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3886 EH ONLY R11 SELECTOR -->"
    end = "<!-- END 3886 EH ONLY R11 SELECTOR -->"
    block = f"""{start}

## 3886 - EH-only/R11 double-zero selector

Mechanism:

`{SIGMA_DEFINITION}`

`{DOUBLE_ZERO_VARIATION}`

`{R11_FACTOR_VARIATION}`

Status: conditional mechanism found. If the parent action derives `Y_loc^A=0` and writes all local non-EH/R11 families as `Sigma_loc`-selected, absent, or exactly topological/boundary-silent, the local compact branch is EH-only to first variation. This is the cleanest current bridge toward GR reduction, but it remains nonclaim because the parent Euler-zero and universal factorization clauses are not yet signed.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3886_DOUBLE_ZERO_SELECTOR_DERIVATION_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3886_R11_FAMILY_SELECTOR_OR_FILL_MATRIX.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3886_VALIDATION.csv`

Next gate: `3887`, derive `Y_loc^A=0` from parent Euler equations or fill the executable coefficient vector.

<!-- Generated by 3886 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    selector: list[dict[str, object]],
    family: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks.append(("VAL3886_0_sources", "all cited source paths exist and needles are found", resolved == len(sources), f"{resolved}/{len(sources)} sources resolved"))
    checks.append(("VAL3886_1_delta_sigma", "selector derivation contains delta Sigma_loc=0", any("delta Sigma_loc=0" in str(row["derivation_or_condition"]) for row in selector), "DZS3886_2"))
    checks.append(("VAL3886_2_R11_variation", "R11 factor variation is explicitly zero on local branch", any("delta[Sigma_loc c_A O_A]" in str(row["derivation_or_condition"]) and "= 0" in str(row["derivation_or_condition"]) for row in selector), "DZS3886_3"))
    required_families = {
        "boundary_topological_terms",
        "R2_fR_scalar_mode",
        "Ricci_Weyl_squared",
        "scalar_tensor_class_metric",
        "vector_preferred_frame",
        "torsion_nonmetricity",
        "bulk_X_force_law",
        "nonlocal_memory_kernel",
        "source_normalization_operator",
        "projector_domain_stress",
    }
    found_families = {str(row["operator_family"]) for row in family}
    checks.append(("VAL3886_3_family_coverage", "all 10 active R11 families are covered", required_families.issubset(found_families), f"{len(found_families)} families"))
    required_symbols = {"delta_gamma_R11", "A_source", "B_source", "delta_beta_source", "delta_beta_R11", "delta_beta_q_loc", "alpha1", "alpha2", "alpha3", "xi", "zeta_i", "alpha(lambda)", "DeltaE_munu"}
    found_symbols = {str(row["symbol"]) for row in coefficients}
    checks.append(("VAL3886_4_coefficient_skeleton", "executable coefficient skeleton covers PPN/R10/R11 components", required_symbols.issubset(found_symbols), f"{len(found_symbols)} symbols"))
    checks.append(("VAL3886_5_local_gr_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3886_7_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3886_7"))
    checks.append(("VAL3886_6_selector_nonclaim", "selector/family/coefficient rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [selector, family, coefficients, gate, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3886_7_runner_next", "runner selects Yloc Euler proof next", any(row["runner_field"] == "next_attack" and "Y_loc" in str(row["rule"]) for row in runner), "RUNU3886_4_next"))
    checks.append(("VAL3886_8_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "parent-owned double-zero selector" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3886_9_spine", "spine updated with 3886 block", SPINE_PATH.exists() and "BEGIN 3886 EH ONLY R11 SELECTOR" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3886_10_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3886*") if path.is_file() and ("3886-Y5" in path.name or "P8_Y5_R2FR_3886" in path.name or "P8_Y5_BRR545_3886" in path.name)]
    checks.append(("VAL3886_11_formalization_untouched", "no generated 3886 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3886_12_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3886_13_next_target", "next target attacks Yloc Euler-zero or coefficient fill", any("Yloc-Euler-zero" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3887 Yloc Euler"))
    checks.append(("VAL3886_14_mechanism_found", "status records conditional mechanism found", any("conditional EH-only/R11 double-zero selector mechanism constructed" in str(row["summary"]) for row in status_rows(timestamp)), "STATUS3886_0"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    selector = selector_rows(timestamp)
    family = family_rows(timestamp)
    coefficients = coefficient_rows(timestamp)
    gate = gate_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["selector"], selector)
    write_csv(OUTPUTS["family"], family)
    write_csv(OUTPUTS["coefficients"], coefficients)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, selector, family, coefficients, gate, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, selector, family, coefficients, gate, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_EH_ONLY_R11_SELECTOR_CONDITIONAL_MECHANISM")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
