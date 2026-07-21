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
SOURCE = POST / "source-intake" / "functional_rg" / "4941"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4941_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4941_typeII_direct_O4_zero_and_lower_quotient.py"
RESULT_JSON = SOURCE / "typeII_direct_O4_zero_and_lower_quotient_results.json"
IDENTITY_CSV = SOURCE / "typeII_direct_O4_tensor_identities.csv"
CHANNEL_CSV = SOURCE / "typeII_direct_O4_source_channels.csv"
BETA_SCAN_CSV = SOURCE / "endomorphism_beta_direct_source_scan.csv"
LOWER_CSV = SOURCE / "lower_scalar_essential_quotient.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4941-Y5-R2FR-natural-TypeII-direct-metric-scalar-O4-zero-proof-and-minimal-O4-parent-completion-gate.md"
FORMAL_NOTE = FORMAL / "957-PPC4161-natural-TypeII-direct-O4-zero-and-minimal-parent-completion.md"
RESULT_4940 = POST / "source-intake" / "functional_rg" / "4940" / "metric_kernel_O4_source_and_family_results.json"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT_MARKER = "MTS_4941_TYPEII_DIRECT_O4_ZERO_AND_LOWER_QUOTIENT"
CHECKPOINT_MARKER = "MTS_NATURAL_TYPEII_DIRECT_O4_ZERO_MINIMAL_PARENT_COMPLETION_4941"
FORMAL_MARKER = "PPC4161_NATURAL_TYPEII_DIRECT_O4_ZERO_MINIMAL_PARENT_4941"
PROVENANCE_MARKER = "MTS_NATURAL_TYPEII_DIRECT_O4_PROVENANCE_4941"
NEXT_TARGET = "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md"

HASH_LOCKS = {
    MAIN_SCRIPT: "5eab58fd2d6a9dfad505cf2ff830e098f7930d3992bf33f8d28001fd08b5537c",
    RESULT_JSON: "e234f85376912f5a9da919f32dd7db855d1ff45f39faa693a01a74677590b57f",
    IDENTITY_CSV: "052fb6470487777b09d617389e8b6a84cd0187648cd3fd04ccbf514a0d8f1fe3",
    CHANNEL_CSV: "afcdfd313c078268ebd4ac5c06fdbffea31d6053647e977119c6fa424a6243de",
    BETA_SCAN_CSV: "cbd3a18b0e538063ac6af5b2d54959d60f2ce03a4f50ee7978de272f4bcc88e9",
    LOWER_CSV: "62f83d1e254709fa6dd5141ad9132a3d9aac89894a30684f804bae508646e89f",
    CHECKPOINT: "f4c6f83668c5f904706747dcafb3d538068a038307ffc062e13fe3234a6b9543",
    FORMAL_NOTE: "5a9f9989a6d057a405773b5435de243d9a74d84a25b6f6248b857534ceb25b46",
    PROVENANCE: "7d4caf1247fb0972a622025cac53fb16aa0bd99dbc26d9ac87a15d4f6b16ce35",
    RESULT_4940: "4c4900dfe18f638801b1a0998ac40f9aa7d6eed9737c8c0a053b2cd2fa9d536a",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def add(
    checks: list[dict[str, Any]],
    validation_id: str,
    test: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    checks.append(
        {
            "validation_id": validation_id,
            "test": test,
            "expected": json.dumps(expected, sort_keys=True, default=str),
            "actual": json.dumps(actual, sort_keys=True, default=str),
            "passed": bool(passed),
            "checkpoint_marker": RESULT_MARKER,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []

    missing = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(checks, "VAL4941_01_paths", "all locked paths exist", [], missing, not missing)

    hash_failures = {
        str(path): {"expected": expected, "actual": digest(path)}
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4941_02_hashes", "all source and output hashes match", {}, hash_failures, not hash_failures)

    compile_failures: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(read_text(path), str(path), "exec")
        except Exception as exc:  # pragma: no cover
            compile_failures.append(f"{path.name}:{type(exc).__name__}:{exc}")
    add(checks, "VAL4941_03_compile", "main and validation scripts compile without bytecode", [], compile_failures, not compile_failures)

    result = json.loads(read_text(RESULT_JSON))
    add(checks, "VAL4941_04_marker", "result marker is exact", RESULT_MARKER, result.get("marker"), result.get("marker") == RESULT_MARKER)

    failed_internal = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4941_05_internal", "all symbolic calculation checks pass", [], failed_internal, not failed_internal)

    source_contract = result["source_contract"]
    add(checks, "VAL4941_06_source_contract", "all source-owned Hessian regulator and Litim clauses are found", "all true", source_contract, all(source_contract.values()))

    identities = read_csv(IDENTITY_CSV)
    identity_ok = (
        len(identities) == 10
        and all(row["passed"] == "True" for row in identities)
        and all(row["generic_Weyl_parameters"] == "10" for row in identities)
        and all(row["valid_for_full_MTS_claim"] == "False" for row in identities)
    )
    add(checks, "VAL4941_07_identities", "all ten generic-Weyl identities pass exactly", "10 rows all true with 10 parameters", {"rows": len(identities), "failed": [row["identity_id"] for row in identities if row["passed"] != "True"]}, identity_ok)

    expected_identity_ids = {f"ID4941_{index}_{suffix}" for index, suffix in enumerate(("Ricci", "Lanczos", "trace_KVX", "BKB", "VX_EC2", "VX_Omega2", "BCCB_h", "BCCB_scalar", "Q0z", "typeII"))}
    actual_identity_ids = {row["identity_id"] for row in identities}
    add(checks, "VAL4941_08_identity_set", "identity ledger contains every declared proof component", sorted(expected_identity_ids), sorted(actual_identity_ids), actual_identity_ids == expected_identity_ids)

    zero_residual_ids = {
        "ID4941_2_trace_KVX",
        "ID4941_3_BKB",
        "ID4941_4_VX_EC2",
        "ID4941_5_VX_Omega2",
        "ID4941_6_BCCB_h",
        "ID4941_7_BCCB_scalar",
        "ID4941_8_Q0z",
        "ID4941_9_typeII",
    }
    residual_map = {row["identity_id"]: row["residual"] for row in identities}
    zero_residual_ok = all(residual_map.get(identity_id) == "0" for identity_id in zero_residual_ids)
    add(checks, "VAL4941_09_zero_residuals", "all scalar tensor and threshold identities simplify to literal zero", "0 for eight scalar rows", {identity_id: residual_map.get(identity_id) for identity_id in sorted(zero_residual_ids)}, zero_residual_ok)

    direct = result["direct_trace_derivation"]
    direct_ok = (
        direct["all_direct_channels_closed"]
        and direct["natural_typeII_direct_source"] == 0.0
        and math.isclose(float(direct["typeI_D1_numeric_at_4940_g"]), 0.020829902306928584, abs_tol=1.0e-14)
        and "(beta_endo - 1)**2" in direct["general_endomorphism_interpolation"]
    )
    add(checks, "VAL4941_10_direct", "Type-II source is zero while Type-I comparator is nonzero", {"typeII": 0.0, "typeI": 0.020829902306928584, "closed": True}, direct, direct_ok)

    channels = read_csv(CHANNEL_CSV)
    channel_status = {row["channel_id"]: row["status"] for row in channels}
    channel_ok = (
        len(channels) == 7
        and channel_status.get("O4D4941_0_hh_density") == "EXACT_ZERO"
        and channel_status.get("O4D4941_1_hh_residual_endomorphism") == "EXACT_TYPEII_ZERO"
        and channel_status.get("O4D4941_2_mixed_density") == "EXACT_LITIM_ZERO"
        and channel_status.get("O4D4941_3_mixed_one_residual_C") == "EXACT_TYPEII_ZERO"
        and channel_status.get("O4D4941_4_mixed_two_residual_C") == "DERIVED_INTERPOLATION_TYPEII_ZERO"
        and channel_status.get("O4D4941_5_lower_essential_scalar") == "EXACT_TWO_LEG_ZERO"
        and channel_status.get("O4D4941_6_direct_sum") == "DIRECT_TRACE_CLOSED_ZERO"
    )
    add(checks, "VAL4941_11_channels", "all seven direct-source channels have the expected closed status", "seven exact statuses", channel_status, channel_ok)

    channel_claim_ok = all(row["valid_for_declared_minimal_O4_claim"] == "True" and row["valid_for_full_MTS_claim"] == "False" for row in channels)
    add(checks, "VAL4941_12_channel_scope", "channel rows promote only the declared minimal O4 claim", "minimal true and full MTS false", "OK" if channel_claim_ok else "bad scope", channel_claim_ok)

    beta_rows = read_csv(BETA_SCAN_CSV)
    beta_values = [float(row["beta_endomorphism"]) for row in beta_rows]
    beta_sources = [float(row["principal_direct_source"]) for row in beta_rows]
    beta_scan_ok = (
        beta_values == [0.0, 0.25, 0.5, 0.75, 1.0]
        and all(first >= second for first, second in zip(beta_sources, beta_sources[1:]))
        and math.isclose(beta_sources[0], 0.020829902306928584, abs_tol=1.0e-14)
        and beta_sources[-1] == 0.0
        and beta_rows[-1]["is_parent_natural_typeII"] == "True"
    )
    add(checks, "VAL4941_13_beta_scan", "endomorphism scan follows the squared suppression to the parent zero", "monotone five-row scan ending at zero", {"beta": beta_values, "sources": beta_sources}, beta_scan_ok)

    lower = result["four_derivative_essential_quotient"]
    lower_ok = (
        lower["coordinate"] == "c_essential=c+8pi g(ctilde+d)"
        and lower["essential_source"] == "16*g**2"
        and lower["two_scalar_O4_additive_Hessian"] == 0
    )
    add(checks, "VAL4941_14_lower", "lower scalar quotient source and two-leg zero are exact", {"coordinate": "c_essential=c+8pi g(ctilde+d)", "source": "16*g**2", "Hessian": 0}, lower, lower_ok)

    lower_rows = read_csv(LOWER_CSV)
    lower_csv_ok = len(lower_rows) == 3 and lower_rows[0]["quantity"] == "c_essential" and lower_rows[0]["source_at_c_ctilde_d_zero"] == "16 g^2" and lower_rows[0]["two_scalar_O4_Hessian"] == "0"
    add(checks, "VAL4941_15_lower_csv", "lower quotient evidence table records the essential coordinate", "three rows with c_essential first", lower_rows, lower_csv_ok)

    promoted = result["minimal_O4_completed_point"]
    previous = json.loads(read_text(RESULT_4940))["O4_completed_known_source_fixed_point"]
    promotion_ok = (
        promoted["identity_with_4940_point"]
        and promoted["coordinates"] == previous["coordinates"]
        and promoted["direct_RHS_source"] == 0.0
        and promoted["u_O4_zero_invariant"] is False
        and promoted["six_coordinate_relevant_directions"] == 1
        and promoted["family_rows_inherited"] == 45
    )
    add(checks, "VAL4941_16_promotion", "zero direct term promotes the 4940 point and family unchanged", "same coordinates direct zero one relevant 45 rows", promoted, promotion_ok)

    fixed_ok = (
        abs(float(promoted["coordinates"]["u_O4"]) + 0.0018050754086485139) < 1.0e-14
        and float(promoted["beta_residual_infinity_norm"]) < 1.0e-12
        and math.isclose(float(promoted["metric_kernel_source"]), 0.0072128143216457575, abs_tol=1.0e-14)
        and math.isclose(float(promoted["u_O4_zero_cancellation_target"]), -0.0072128143216457575, abs_tol=1.0e-14)
    )
    add(checks, "VAL4941_17_fixed", "promoted point keeps nonzero uO4 kernel source and failed cancellation target", "uO4 residual source and signed target", promoted, fixed_ok)

    boundary = result["claim_boundary"]
    boundary_ok = (
        boundary["direct_metric_scalar_RHS_trace_derived"]
        and boundary["direct_metric_scalar_RHS_trace_zero_in_declared_typeII_scheme"]
        and boundary["minimal_O4_parent_fixed_point_completed"]
        and boundary["minimal_O4_parent_family_completed"]
        and not boundary["u_O4_zero_invariant"]
        and not boundary["u_O4_adds_relevant_direction"]
        and not boundary["all_five_scalar_six_derivative_beta_functions_completed"]
        and not boundary["full_visible_matter_motion_fixed_point"]
        and not boundary["physical_PPN_clock_fifth_force_projection_derived"]
        and not boundary["full_MTS_fixed_point"]
        and not boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add(checks, "VAL4941_18_boundary", "minimal O4 completion remains separated from full MTS and local claims", "minimal true and larger claims false", boundary, boundary_ok)

    checkpoint_text = read_text(CHECKPOINT)
    checkpoint_ok = CHECKPOINT_MARKER in checkpoint_text and NEXT_TARGET in checkpoint_text and "direct RHS O4 trace in natural Type-II scheme   = derived exact zero;" in checkpoint_text and "local GR/Newton/Maxwell promotion               = false." in checkpoint_text
    add(checks, "VAL4941_19_checkpoint", "checkpoint records exact Type-II result and next local target", "marker direct zero local false next 4942", "OK" if checkpoint_ok else "missing", checkpoint_ok)

    formal_text = read_text(FORMAL_NOTE)
    formal_ok = FORMAL_MARKER in formal_text and "direct Type-II O4 trace          = exact zero;" in formal_text and "full MTS/local-GR promotion      = false." in formal_text
    add(checks, "VAL4941_20_formal", "formal note preserves scope and nonclaim", "marker direct zero local false", "OK" if formal_ok else "missing", formal_ok)

    claim_rows = [row for row in read_csv(CLAIMS) if row["claim_id"] == "L-783"]
    claim_ok = len(claim_rows) == 1 and NEXT_TARGET in claim_rows[0]["next_test"] and "DIRECT_RHS_TYPEII_ZERO" in claim_rows[0]["notes"] and "FULL_MTS_FALSE" in claim_rows[0]["notes"] and "LOCAL_GR_FALSE" in claim_rows[0]["notes"]
    add(checks, "VAL4941_21_claim", "claim L-783 is unique and correctly scoped", "one row with zero and two nonclaim markers", claim_rows, claim_ok)

    expected_variables = {
        "DirectO4TypeII4941_MTS",
        "EndomorphismBeta4941_MTS",
        "MixedBCCB4941_MTS",
        "LowerEssentialC4941_MTS",
        "O4CompletedPoint4941_MTS",
        "O4InvariantStatus4941_MTS",
        "TensorIdentityCertificate4941_MTS",
        "PredictivityStatus4941_MTS",
    }
    found_variables = {row["symbol"] for row in read_csv(VARIABLES) if row["symbol"] in expected_variables}
    add(checks, "VAL4941_22_variables", "all eight 4941 variables are registered", sorted(expected_variables), sorted(found_variables), found_variables == expected_variables)

    equation_text = read_text(EQUATIONS)
    equation_ok = "## 1.234 Natural Type-II direct O4 zero and minimal parent completion" in equation_text and "S_O4,direct(beta_endo,D)" in equation_text and "beta_c,ess|0" in equation_text
    add(checks, "VAL4941_23_equations", "equation 1.234 records direct and lower quotient formulas", "section and two formulas", "OK" if equation_ok else "missing", equation_ok)

    red_text = read_text(RED_TEAM)
    red_ok = "## 185. A direct zero may be regulator-owned without erasing the kernel source" in red_text and "do not export the natural Type-II direct zero" in red_text and "do not use S_direct=0 to erase" in red_text
    add(checks, "VAL4941_24_red_team", "red-team 185 blocks regulator and kernel overclaims", "section and two prohibitions", "OK" if red_ok else "missing", red_ok)

    spine_text = read_text(SPINE)
    spine_ok = "## PPC4161 checkpoint 4941 - direct O4 closure and minimal parent completion" in spine_text and FORMAL_MARKER in spine_text and "full MTS/local-GR promotion                    = false;" in spine_text
    add(checks, "VAL4941_25_spine", "spine records minimal completion and local boundary", "4941 marker and local false", "OK" if spine_ok else "missing", spine_ok)

    resume_text = read_text(RESUME)
    resume_ok = CHECKPOINT.name in resume_text and FORMAL_MARKER in resume_text and NEXT_TARGET in resume_text and "S_O4,direct=0" in resume_text and "beta_c,ess|0=16g^2" in resume_text
    add(checks, "VAL4941_26_resume", "resume records the direct zero lower quotient and next target", "checkpoint marker formulas target", "OK" if resume_ok else "missing", resume_ok)

    provenance_text = read_text(PROVENANCE)
    provenance_ok = PROVENANCE_MARKER in provenance_text and all(expected in provenance_text for path, expected in HASH_LOCKS.items() if path not in (PROVENANCE,)) and "valid_for_full_MTS_claim=False" in provenance_text
    add(checks, "VAL4941_27_provenance", "provenance records all locked hashes and firewall", "marker hashes full-MTS false", "OK" if provenance_ok else "missing", provenance_ok)

    evidence_failures: list[str] = []
    for path in (IDENTITY_CSV, CHANNEL_CSV, BETA_SCAN_CSV, LOWER_CSV):
        for index, row in enumerate(read_csv(path), start=2):
            if row.get("valid_for_full_MTS_claim") != "False":
                evidence_failures.append(f"{path.name}:{index}:claim")
            if any("MISSING_" in value for value in row.values() if value):
                evidence_failures.append(f"{path.name}:{index}:missing")
    add(checks, "VAL4941_28_firewall", "all evidence rows remain complete full-MTS nonclaims", [], evidence_failures, not evidence_failures)

    malformed: list[str] = []
    for path in (CLAIMS, VARIABLES, IDENTITY_CSV, CHANNEL_CSV, BETA_SCAN_CSV, LOWER_CSV):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
        width = len(rows[0]) if rows else 0
        malformed.extend(
            f"{path.name}:{index}:{len(row)}!={width}"
            for index, row in enumerate(rows[1:], start=2)
            if len(row) != width
        )
    add(checks, "VAL4941_29_csv_shape", "register and evidence CSV widths are uniform", [], malformed, not malformed)

    source_paths = [Path(path_text) for path_text in result["source_hashes"]]
    unresolved_sources = [str(path) for path in source_paths if not (ROOT / path).exists()]
    add(checks, "VAL4941_30_result_sources", "every source path serialized in the result exists", [], unresolved_sources, not unresolved_sources)

    pycache = sorted(str(path) for path in (POST / "scripts").glob("__pycache__") if path.exists())
    add(checks, "VAL4941_31_pycache", "no scripts pycache remains", [], pycache, not pycache)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    failures = [row for row in checks if not row["passed"]]
    print(f"{RESULT_MARKER}_VALIDATION_CHECKS={len(checks)}", flush=True)
    print(f"{RESULT_MARKER}_VALIDATION_FAILURES={len(failures)}", flush=True)
    print(f"{RESULT_MARKER}_VALIDATION_SHA256={digest(OUTPUT)}", flush=True)
    for failure in failures:
        print(f"{RESULT_MARKER}_VALIDATION_FAIL={failure['validation_id']}:{failure['actual']}", flush=True)
    if failures:
        return 1
    print(f"{RESULT_MARKER}_VALIDATION_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
