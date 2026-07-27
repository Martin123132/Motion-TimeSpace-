from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4938"
OUTPUT_DIR = POST / "source-intake" / "mts_residuals"
OUTPUT = OUTPUT_DIR / "P8_Y5_BRR545_4938_VALIDATION.csv"

IDENTITY_SCRIPT = POST / "scripts" / "Y5_R2FR_4938_parent_scale_identity_audit.py"
TRANSFER_SCRIPT = POST / "scripts" / "Y5_R2FR_4938_critical_surface_scale_transfer.py"
CHECKPOINT = POST / "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md"
FORMAL_NOTE = FORMAL / "954-PPC4161-motion-Newton-scale-identity-and-two-scale-decision.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

GEOMETRIC_FRAMEWORK = ROOT / "core-mts-framework" / "field-theory" / "geometric-field-framework.md"
FUNDAMENTAL_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
MASS_GAP_4909 = POST / "4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md"
SCALE_REPAIR_4926 = POST / "4926-Y5-R2FR-known-massive-threshold-spectrum-and-motion-scale-normalization-or-low-energy-Wilson-posterior.md"
NORMALIZATION_4927 = POST / "4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue-and-EH-matching-or-one-Wilson-freeze.md"
CHECKPOINT_4937 = POST / "4937-Y5-R2FR-gravity-motion-functional-potential-Hessian-and-one-scale-fixed-function-gate.md"
SCALE_ROWS_4926 = POST / "source-intake" / "mts_residuals" / "P8_Y5_R2FR_4926_MOTION_SCALE_REPAIR_BRANCH.csv"
FIXED_GATE_4937 = POST / "source-intake" / "functional_rg" / "4937" / "functional_potential_fixed_gate_results.json"
C3_SOLVER = POST / "scripts" / "Y5_R2FR_4933_c3_direct_threshold_solver.py"
COMBINED_4933 = POST / "scripts" / "Y5_R2FR_4933_combined_c3_photon_stability.py"
PHOTON_4933 = POST / "scripts" / "Y5_R2FR_4933_photon_flow_reproduction.py"
DIRECT_4934 = POST / "scripts" / "Y5_R2FR_4934_direct_c3_cff_principal.py"
COMPLETED_4934_SCRIPT = POST / "scripts" / "Y5_R2FR_4934_completed_combined_flow.py"
COMPLETED_4934 = POST / "source-intake" / "functional_rg" / "4934" / "completed_combined_flow_results.json"
TRAJECTORY_4935 = POST / "source-intake" / "functional_rg" / "4935" / "completed_fixed_point_trajectory_results.json"

IDENTITY_JSON = SOURCE / "parent_scale_identity_audit_results.json"
CANDIDATE_CSV = SOURCE / "scale_identity_candidate_audit.csv"
MOTION_BOUND_CSV = SOURCE / "motion_scale_bound_translation.csv"
TRANSFER_JSON = SOURCE / "critical_surface_scale_lock_results.json"
SPECTRUM_CSV = SOURCE / "augmented_motion_stability_spectrum.csv"
GR_TRANSFER_CSV = SOURCE / "motion_scale_GR_transfer.csv"
UV_BOUND_CSV = SOURCE / "UV_scale_label_bound_translation.csv"

MARKER = "MTS_MOTION_NEWTON_TWO_SCALE_VALIDATION_4938"
CHECKPOINT_MARKER = "MTS_MOTION_NEWTON_SCALE_IDENTITY_OR_TWO_SCALE_GATE_4938"
FORMAL_MARKER = "PPC4161_MOTION_NEWTON_SCALE_IDENTITY_OR_TWO_SCALE_GATE_4938"
NEXT_TARGET = "4939-Y5-R2FR-two-scale-motion-O4-curved-flow-and-backreacted-GR-family-gate.md"
CHECKED_DATE = "2026-07-12"

SCRIPTS = (IDENTITY_SCRIPT, TRANSFER_SCRIPT, Path(__file__))
EVIDENCE_CSV = (
    CANDIDATE_CSV,
    MOTION_BOUND_CSV,
    SPECTRUM_CSV,
    GR_TRANSFER_CSV,
    UV_BOUND_CSV,
)
HASH_LOCKS = {
    GEOMETRIC_FRAMEWORK: "b5a6d5ab7c3cca6484897f26e7dedba35ca67a00962c460d46bb6834ee41d3b9",
    FUNDAMENTAL_ACTION: "afbb6a6e86ee30ca790f829374b791b307ace0e20f175b1600632205f9aeff54",
    MASS_GAP_4909: "9d5d420a8c2cac6fc3d65352e2dec7c44f635b083a6840c18267a105a02a7ca3",
    SCALE_REPAIR_4926: "bbdd4a5b4928e1339730f05a10b9b6ea98ace83d30d78356b3c7294df14ea562",
    NORMALIZATION_4927: "512c200c0d5dfb32884404c0536678a6116ba4fa0d5103187012393746770926",
    CHECKPOINT_4937: "2cf1f25d7cf67ec9bb724381919a9ff6e78d5dabe355ec50178157309b29cce5",
    SCALE_ROWS_4926: "d27b69621f81e5590ebba74103b6cd5b7e19c0ca28476f0df0aae5aa7d50e533",
    FIXED_GATE_4937: "a965b75e5b5576e579bb4812b14a0e220a1b18b4e9653f4e83d714c4caf8a361",
    C3_SOLVER: "b0ff49318368f6b0b4f270603b364d14012462f2229e7bbb7858fe3b592f568a",
    COMBINED_4933: "5c80446a719d3820b5d08505c9c2d8b2e1389ec81266df2cdde60ca450a31df7",
    PHOTON_4933: "2858b5ea16085f2f5309ea7301d3a23b4868dd522905369e9ac3d95f2c9599d8",
    DIRECT_4934: "8299e6a2e6f53fc5da87ce8691602d7a3f7c77b08e8b7a48bd0c42f26a360fee",
    COMPLETED_4934_SCRIPT: "c5fded8ca210607972c5d12640cdfd3e88ea3de48f84d1b699a3b2a7e342e230",
    COMPLETED_4934: "c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978",
    TRAJECTORY_4935: "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
    IDENTITY_SCRIPT: "f8f6c7c5e1ad6c8e0c496d7e2651ddb1acc6a403f2c5d5ed126a5eae6c611baa",
    TRANSFER_SCRIPT: "33644e9e2856e361aef777e173bf2a2f564d29c89036a2285399cb4271c59b72",
    IDENTITY_JSON: "24140234550056d98de373742073190154e432012451fec7a02b962e3a4dcb48",
    CANDIDATE_CSV: "924ccf3b026c14b2bcc4e47a410b3a3477afd3cda3635808a698bc6577e95033",
    MOTION_BOUND_CSV: "e62cabda4191eeae491d5f6849e8a5992eff1278b9b5286468dbfe15ff56e4bc",
    TRANSFER_JSON: "544375b68725e8722507eea59414e91a3a76f2bad84c57ac3bdca1ae75a8a175",
    SPECTRUM_CSV: "e4a59708bc3fd10a6f02daa208cb2a0f661f588c02fedd1f5d3523e0b640a1d6",
    GR_TRANSFER_CSV: "407810e0612325eeb64704634be215a00d45e93dad12042156f60d9799f75716",
    UV_BOUND_CSV: "981233997ee8817fefe34a22bb5ab75ec28b387fff7df7ca1218ba3afc9cf24a",
    CHECKPOINT: "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4",
    FORMAL_NOTE: "152ee9713f61655caef4da5cd8a07ec0c1e3c0cab1326d015498a1d4a54710e4",
    PROVENANCE: "51a27bc3e8cc348761627637a9dbe6762076a1bb655eaff0896ed17720b72b31",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def add(
    checks: list[dict[str, Any]],
    check_id: str,
    requirement: str,
    expected: str,
    actual: Any,
    passed: bool,
) -> None:
    checks.append(
        {
            "validation_id": check_id,
            "requirement": requirement,
            "expected": expected,
            "actual": str(actual),
            "passed": passed,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    required = set(
        (
            *SCRIPTS,
            *HASH_LOCKS,
            CHECKPOINT,
            FORMAL_NOTE,
            PROVENANCE,
            CLAIMS,
            VARIABLES,
            EQUATIONS,
            RED_TEAM,
            SPINE,
            RESUME,
        )
    )
    missing = sorted(str(path) for path in required if not path.exists())
    add(checks, "VAL4938_00_paths", "all source and output paths exist", "[]", missing, not missing)

    syntax_errors = []
    for path in SCRIPTS:
        try:
            compile(read_text(path), str(path), "exec")
        except SyntaxError as error:
            syntax_errors.append(f"{path.name}:{error}")
    add(checks, "VAL4938_01_compile", "all three scripts compile", "[]", syntax_errors, not syntax_errors)

    hash_failures = []
    for path, expected in HASH_LOCKS.items():
        actual = digest(path) if path.exists() else "MISSING"
        if actual != expected:
            hash_failures.append(f"{path.name}:{actual}")
    add(
        checks,
        "VAL4938_02_hashes",
        "all source script artifact and document hashes match",
        f"{len(HASH_LOCKS)} matches",
        "OK" if not hash_failures else hash_failures,
        not hash_failures,
    )

    identity = load_json(IDENTITY_JSON)
    add(
        checks,
        "VAL4938_03_identity_checks",
        "all scale-identity audit checks pass",
        "all true",
        identity["checks"],
        all(identity["checks"].values()),
    )

    old = identity["old_field_coordinate_theorem"]
    old_ok = (
        old["fixed_harmonic_relation_ratio_under_orbit"] == "s**(2/3)"
        and "g_psi=lambda_old M_N^(-1/3)" in old["invariants"]
        and "I_M=g_psi G_N^(4/3)" in old["invariants"]
    )
    add(checks, "VAL4938_04_orbit", "field orbit preserves physical invariants", "invariants and s**(2/3)", old, old_ok)

    harmonic = identity["harmonic_formula_audit"]
    harmonic_ok = (
        harmonic["implied_physical_invariant"] == "I_M(p)=Phi_G^(4-p/3)"
        and not math.isclose(
            harmonic["examples"]["p=0_M_N_equals_M_Pl"],
            harmonic["examples"]["p=1_M_N_equals_gamma"],
            rel_tol=1.0e-12,
        )
        and "does not fix" in harmonic["decision"]
    )
    add(checks, "VAL4938_05_harmonic", "golden formula leaves normalization free", "I_M(p) family and unequal examples", harmonic, harmonic_ok)

    candidates = read_csv(CANDIDATE_CSV)
    selected = [row for row in candidates if row["result"] == "SELECTED_CURRENT_PARENT_STATUS"]
    candidate_ok = (
        len(candidates) == 7
        and len(selected) == 1
        and selected[0]["candidate"] == "explicit_two_scale_parent"
        and all(row["valid_for_full_MTS_claim"] == "False" for row in candidates)
    )
    add(checks, "VAL4938_06_candidates", "only explicit two-scale status is selected", "7 rows and one selected", selected, candidate_ok)

    identity_boundary = identity["claim_boundary"]
    identity_boundary_ok = (
        identity_boundary["field_coordinate_invariant_scale_ratio_derived"]
        and identity_boundary["explicit_second_essential_scale_required"]
        and not identity_boundary["golden_ratio_fixes_physical_motion_scale"]
        and not identity_boundary["gamma_fixes_physical_motion_scale"]
        and not identity_boundary["Einstein_residue_fixes_motion_scale"]
        and not identity_boundary["minimal_UV_surface_fixes_motion_scale"]
        and not identity_boundary["numeric_motion_scale_measured"]
        and not identity_boundary["full_MTS_trajectory_calculated"]
        and not identity_boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add(checks, "VAL4938_07_identity_boundary", "scale ratio is derived without value or local promotion", "ratio/two-scale true and selection/full/local false", identity_boundary, identity_boundary_ok)

    motion_bounds = read_csv(MOTION_BOUND_CSV)
    motion_bounds_ok = (
        len(motion_bounds) == 3
        and all(float(row["I_M_floor"]) > 0.0 for row in motion_bounds)
        and all(float(row["J_gap_floor"]) > 0.0 for row in motion_bounds)
        and all(float(row["m_gap_over_M_Pl_floor"]) > 0.0 for row in motion_bounds)
        and all(row["upper_bound"] == "NOT_DERIVED" for row in motion_bounds)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in motion_bounds)
    )
    add(checks, "VAL4938_08_bounds", "three compact floors are positive nonclaims", "3 positive rows and no upper bound", motion_bounds, motion_bounds_ok)

    transfer = load_json(TRANSFER_JSON)
    add(
        checks,
        "VAL4938_09_transfer_checks",
        "all scale-transfer internal checks pass",
        "all true",
        transfer["checks"],
        all(transfer["checks"].values()),
    )

    decision = transfer["decision"]
    decision_ok = (
        not decision["critical_surface_fixes_motion_scale"]
        and decision["two_relevant_directions"]
        and decision["GR_transfer_function_derived"]
        and not decision["GR_transfer_selects_value"]
        and decision["explicit_two_scale_parent_required"]
    )
    add(checks, "VAL4938_10_decision", "critical surface transports but does not select the scale", "two relevant and selection false", decision, decision_ok)

    block = transfer["block_triangular_theorem"]
    variants = block["variants"]
    block_ok = (
        block["matrix"] == "B_aug=[[B_gravity,c],[0,-theta_mass]]"
        and "det(zI-B_aug)=det(zI-B_gravity)(z+theta_mass)" in block["determinant"]
        and math.isclose(block["known_threshold_column"][0], -0.0009043189731243481, rel_tol=1.0e-13)
        and len(variants) == 3
        and all(row["relevant_directions"] == 2 for row in variants.values())
        and all(row["response_residual_infinity_norm"] < 2.0e-16 for row in variants.values())
    )
    add(checks, "VAL4938_11_block", "block theorem preserves two relevant modes", "exact determinant and residual below 2e-16", block, block_ok)

    spectrum = read_csv(SPECTRUM_CSV)
    spectrum_variants = {row["mass_variant"] for row in spectrum}
    spectrum_ok = len(spectrum) == 18 and len(spectrum_variants) == 3
    for variant in spectrum_variants:
        rows = [row for row in spectrum if row["mass_variant"] == variant]
        spectrum_ok = spectrum_ok and (
            len(rows) == 6
            and sum(row["relevant"] == "True" for row in rows) == 2
            and sum(row["motion_mass_mode"] == "True" for row in rows) == 1
            and all(row["valid_for_full_MTS_claim"] == "False" for row in rows)
        )
    add(checks, "VAL4938_12_spectrum", "each augmented spectrum has two relevant modes", "3 x 6 rows; one motion mode each", sorted(spectrum_variants), spectrum_ok)

    gr_rows = read_csv(GR_TRANSFER_CSV)
    mappings = {row["mapping"] for row in gr_rows}
    seeds = {float(row["relative_gravity_seed"]) for row in gr_rows}
    gr_ok = (
        len(gr_rows) == 10
        and len(mappings) == 2
        and len(seeds) == 5
        and all(row["termination"] == "IR_G_TARGET" for row in gr_rows)
        and all(abs(float(row["g_endpoint"]) - 1.0e-10) < 1.0e-22 for row in gr_rows)
        and all(float(row["w_endpoint_linear_probe"]) < 0.01 for row in gr_rows)
        and all(float(row["J_gap_endpoint"]) > 0.0 for row in gr_rows)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in gr_rows)
    )
    add(checks, "VAL4938_13_GR_transfer", "all ten trajectories reach controlled GR", "2 maps x 5 seeds and w below 0.01", {"mappings": mappings, "seeds": seeds}, gr_ok)

    summaries = transfer["GR_separatrix_transfer"]["summaries"]
    convergence_ok = (
        len(summaries) == 2
        and all(row["max_relative_difference"] < 5.0e-5 for row in summaries.values())
        and math.isclose(
            summaries["Wetterich_v_equals_plus_2lambda"]["smallest_seed_reference"],
            0.26209442081797163,
            rel_tol=1.0e-13,
        )
        and math.isclose(
            summaries["Wetterich_v_equals_minus_2lambda"]["smallest_seed_reference"],
            0.2617077068051851,
            rel_tol=1.0e-13,
        )
    )
    add(checks, "VAL4938_14_convergence", "both GR Jacobians are seed converged", "K values and drift below 5e-5", summaries, convergence_ok)

    uv_bounds = read_csv(UV_BOUND_CSV)
    uv_ok = (
        len(uv_bounds) == 6
        and all(float(row["J_gap_floor"]) > 0.0 for row in uv_bounds)
        and all(float(row["R_UV_floor_in_declared_eigenvector_normalization"]) > 0.0 for row in uv_bounds)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in uv_bounds)
    )
    add(checks, "VAL4938_15_UV_bounds", "six UV floor translations are positive nonclaims", "6 positive rows", uv_bounds, uv_ok)

    beta = transfer["physical_scale_beta"]
    beta_ok = (
        beta["exact_log_beta"] == "beta_J/J=beta_w/w+beta_g/g"
        and "beta_J=0" in beta["Gaussian_limit"]
        and "not RG closed" in beta["fractional_warning"]
    )
    add(checks, "VAL4938_16_beta", "physical beta transports J_gap without selecting it", "exact beta and RG warning", beta, beta_ok)

    boundary = transfer["claim_boundary"]
    boundary_ok = (
        boundary["coupled_scale_ratio_beta_derived"]
        and boundary["block_triangular_relevance_theorem_derived"]
        and boundary["known_threshold_rotation_calculated"]
        and boundary["linear_GR_transfer_calculated"]
        and not boundary["motion_scale_selected"]
        and not boundary["fully_backreacted_motion_trajectory"]
        and not boundary["full_MTS_fixed_point"]
        and not boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add(checks, "VAL4938_17_boundary", "transfer remains firewalled from value and local claims", "derived rows true and selection/full/local false", boundary, boundary_ok)

    checkpoint_text = read_text(CHECKPOINT)
    checkpoint_ok = (
        CHECKPOINT_MARKER in checkpoint_text
        and NEXT_TARGET in checkpoint_text
        and "explicit second essential scale                   = required;" in checkpoint_text
        and "motion scale value selected                       = false;" in checkpoint_text
        and "local GR/Newton/Maxwell promotion                  = false." in checkpoint_text
    )
    add(checks, "VAL4938_18_checkpoint", "checkpoint states decision and nonclaims", "marker next target and false boundaries", "OK" if checkpoint_ok else "missing", checkpoint_ok)

    formal_text = read_text(FORMAL_NOTE)
    formal_ok = (
        FORMAL_MARKER in formal_text
        and "critical-surface relevant count             = two;" in formal_text
        and "motion scale value                          = unselected;" in formal_text
        and "full MTS/local-GR promotion                 = false." in formal_text
    )
    add(checks, "VAL4938_19_formal", "formal note states count and boundaries", "two relevant and local false", "OK" if formal_ok else "missing", formal_ok)

    claim_matches = [row for row in read_csv(CLAIMS) if row["claim_id"] == "L-780"]
    claim_ok = (
        len(claim_matches) == 1
        and "explicit_two_essential_scale_parent_selected" in claim_matches[0]["status"]
        and NEXT_TARGET in claim_matches[0]["next_test"]
        and "LOCAL_GR_FALSE" in claim_matches[0]["notes"]
    )
    add(checks, "VAL4938_20_claim", "claim L-780 records the decision", "one row two-scale next 4939 local false", claim_matches, claim_ok)

    expected_variables = {
        "IM4938_MTS",
        "JGap4938_MTS",
        "OldFieldOrbit4938_MTS",
        "GoldenScaleAudit4938_MTS",
        "TwoScaleOwner4938_MTS",
        "AugmentedStability4938_MTS",
        "ThresholdColumn4938_MTS",
        "RUV4938_MTS",
        "GRScaleTransfer4938_MTS",
        "ScaleFloor4938_MTS",
        "PredictivityStatus4938_MTS",
    }
    found_variables = {row["symbol"] for row in read_csv(VARIABLES) if row["symbol"] in expected_variables}
    add(checks, "VAL4938_21_variables", "all eleven variables are registered", sorted(expected_variables), sorted(found_variables), found_variables == expected_variables)

    equation_text = read_text(EQUATIONS)
    equation_ok = (
        "## 1.231 Motion/Newton scale identity and explicit two-scale flow" in equation_text
        and "beta_J/J=beta_w/w+beta_g/g." in equation_text
        and "det(zI-B_g)(z+theta_mass)." in equation_text
    )
    add(checks, "VAL4938_22_equations", "equation 1.231 records beta and determinant", "section beta determinant", "OK" if equation_ok else "missing", equation_ok)

    red_text = read_text(RED_TEAM)
    red_ok = (
        "## 182. A dimensionless formula is not a scale prediction unless it survives field redundancy" in red_text
        and "do not infer scale locking from a rotated eigenvector" in red_text
        and "do not retune J_gap by arena" in red_text
        and "do not promote full MTS local GR Newton or Maxwell" in red_text
    )
    add(checks, "VAL4938_23_red_team", "red-team 182 records prohibitions", "rotation retuning and local prohibitions", "OK" if red_ok else "missing", red_ok)

    spine_text = read_text(SPINE)
    spine_ok = (
        "## PPC4161 checkpoint 4938 - explicit two-scale MTS spine" in spine_text
        and FORMAL_MARKER in spine_text
        and "full MTS/local-GR promotion                    = false;" in spine_text
    )
    add(checks, "VAL4938_24_spine", "spine carries two-scale nonclaim", "4938 marker and local false", "OK" if spine_ok else "missing", spine_ok)

    resume_text = read_text(RESUME)
    resume_ok = (
        CHECKPOINT.name in resume_text
        and FORMAL_MARKER in resume_text
        and NEXT_TARGET in resume_text
        and "Do not fit" in resume_text
        and "J_gap" in resume_text
        and "independently" in resume_text
    )
    add(checks, "VAL4938_25_resume", "resume points to 4938 and 4939", "checkpoint marker next target and no overcount", "OK" if resume_ok else "missing", resume_ok)

    evidence_failures = []
    for path in EVIDENCE_CSV:
        for index, row in enumerate(read_csv(path), start=2):
            claim_fields = [value for key, value in row.items() if key.startswith("valid_for")]
            if not claim_fields or any(value != "False" for value in claim_fields):
                evidence_failures.append(f"{path.name}:{index}:claim")
            if any("MISSING_" in value for value in row.values() if value):
                evidence_failures.append(f"{path.name}:{index}:missing")
    add(checks, "VAL4938_26_firewall", "all evidence remains private and complete", "no claim or missing failures", evidence_failures, not evidence_failures)

    malformed = []
    for path in (CLAIMS, VARIABLES, *EVIDENCE_CSV):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
        width = len(rows[0]) if rows else 0
        malformed.extend(
            f"{path.name}:{index}:{len(row)}!={width}"
            for index, row in enumerate(rows[1:], start=2)
            if len(row) != width
        )
    add(checks, "VAL4938_27_csv_shape", "all CSV rows have uniform widths", "[]", malformed, not malformed)

    provenance_text = read_text(PROVENANCE)
    provenance_ok = all(
        value in provenance_text
        for value in (
            HASH_LOCKS[GEOMETRIC_FRAMEWORK],
            HASH_LOCKS[FUNDAMENTAL_ACTION],
            HASH_LOCKS[CHECKPOINT_4937],
            HASH_LOCKS[C3_SOLVER],
            HASH_LOCKS[COMPLETED_4934],
            HASH_LOCKS[TRAJECTORY_4935],
            "P8_Y5_BRR545_4938_VALIDATION.csv",
            "valid_for_full_MTS_claim=false",
        )
    )
    add(checks, "VAL4938_28_provenance", "provenance records hashes output and firewall", "all provenance tokens", "OK" if provenance_ok else "missing", provenance_ok)

    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__") if path.exists())
    add(checks, "VAL4938_29_pycache", "no scripts pycache remains", "[]", pycache, not pycache)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    failures = [row for row in checks if not row["passed"]]
    print(f"{MARKER}_CHECKS={len(checks)}", flush=True)
    print(f"{MARKER}_FAILURES={len(failures)}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    for failure in failures:
        print(f"{MARKER}_FAIL={failure['validation_id']}:{failure['actual']}", flush=True)
    if failures:
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
