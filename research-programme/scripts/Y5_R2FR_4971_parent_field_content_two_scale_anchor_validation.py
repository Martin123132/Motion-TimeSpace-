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
SOURCE = POST / "source-intake" / "functional_rg" / "4971"
RESIDUAL = POST / "source-intake" / "mts_residuals"
OUTPUT = RESIDUAL / "P8_Y5_BRR545_4971_VALIDATION.csv"
MARKER = "MTS_4971_PARENT_FIELD_CONTENT_TWO_SCALE_ANCHOR_VALIDATION"
CHECKPOINT_MARKER = "PPC4161_PARENT_FIELD_CONTENT_AMPLITUDE_ANCHOR_4971"
CHECKED_DATE = "2026-07-13"

RUNNER = (
    POST
    / "scripts"
    / "Y5_R2FR_4971_parent_field_content_and_two_scale_anchor_projector.py"
)
VALIDATOR = (
    POST
    / "scripts"
    / "Y5_R2FR_4971_parent_field_content_two_scale_anchor_validation.py"
)
FIELD_CONTENT = SOURCE / "Bern_R3_field_content_branches.csv"
MISMATCH = SOURCE / "C3_parent_field_content_mismatch.csv"
SPLICE = SOURCE / "C3_full_parent_splice_scan.csv"
TRANSPORT = SOURCE / "C3_full_parent_matching_transport.csv"
P8_PROJECTOR = SOURCE / "C3_two_scale_helicity_projector.csv"
IDENTIFIABILITY = SOURCE / "C3_local_anchor_identifiability.csv"
AMPLITUDE_PROJECTOR = SOURCE / "C3_finite_amplitude_projector.csv"
ANCHOR_SCALE = SOURCE / "C3_anchor_scale_contract.csv"
RESULT = SOURCE / "C3_parent_matching_and_anchor_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
ABREU_ARCHIVE = SOURCE / "src-2002.12374" / "arXiv-2002.12374v2-source.tar"
ABREU_MAIN = SOURCE / "src-2002.12374" / "source" / "main.tex"
ABREU_PPPP = (
    SOURCE
    / "src-2002.12374"
    / "source"
    / "anc"
    / "2loopRemainder"
    / "pppp_s-channel.m"
)
ABREU_MPPP = (
    SOURCE
    / "src-2002.12374"
    / "source"
    / "anc"
    / "2loopRemainder"
    / "mppp_s-channel.m"
)
ABREU_INTERFACE = (
    SOURCE
    / "src-2002.12374"
    / "source"
    / "anc"
    / "4gravitonAmplitudes.m"
)
CHECKPOINT = (
    POST
    / "4971-Y5-R2FR-parent-field-content-finite-amplitude-projector-and-two-scale-anchor-or-local-route-rejection.md"
)
FORMAL_NOTE = (
    FORMAL
    / "987-PPC4161-parent-field-content-amplitude-anchor-and-two-scale-projector.md"
)
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION = FORMAL / "07-unification-spine.md"

EXPECTED_HASHES = {
    POST
    / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md": "223514da350b0bbaed8e6fcd3582eeaab79ef698ea8c0ea5df2cace328de1876",
    POST
    / "4929-Y5-R2FR-MTS-matter-completed-C3-essential-flow-and-fixed-point-survival-or-one-Wilson-retention.md": "46302f298fcfa63633455cecf9977e3fb8d0384a1fe5bbf8ecd33b60e444e7ea",
    POST
    / "4933-Y5-R2FR-C3-CFF-F4-minimal-combined-natural-flow-and-0p239-stability-gate.md": "f075ccd1d0c4f28daf9685d99855f8dde10664e3eb62ce3d8e3b99d03fb38c38",
    POST
    / "source-intake"
    / "functional_rg"
    / "4957"
    / "functional_PX_O4_GR_trajectory.csv": "c60eee38379dc8cf1bb16833b2b5a849ecc0b5d7da0f74d9f0c9bd1bf9b46166",
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "p8_canonical_repaired_GR_connected_trajectory.csv": "b5984ba1c528aebd2099755561a8b578ec79751a3846be01032cc52e24e65957",
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "src-1701.02422"
    / "gr_simp.tex": "9448bff31da3e1e56e62e8fb6242a60c09afb90d1f7f25edaf3f23466ac0371e",
    POST
    / "source-intake"
    / "functional_rg"
    / "4929"
    / "src2312"
    / "ess_cubic.tex": "b23b0974509278be22c8917f531a2963d415184d9052e27860c65fad80943a1d",
    POST
    / "source-intake"
    / "functional_rg"
    / "4970"
    / "C3_p8_finite_matching_results.json": "9165acf171eb6e936f81e2ddc5fd2ca7f3be465d206e5cfd0d1704e12b371aa1",
    ABREU_ARCHIVE: "7631ad019ba1957f088216201ad8c7cda8baad3c35793c107a59e15310b5ee15",
    ABREU_MAIN: "11acdee89baad0298aafc5cc975be9d981d985bb37d2da86914281ca2c997fc8",
    ABREU_PPPP: "42128b16a7451b6213abd06c0eae9bfa649f5890df365c04f6209fd6b5630483",
    ABREU_MPPP: "6d426fbba39e4a02413fd17f5d4869a33c3cabb4263d88dd8e9e8e8a7a52c2a5",
    ABREU_INTERFACE: "d94df4a0a3b2a7452b15510d860904cfecf2bad9b49db5099db0b46fad3d5593",
    RUNNER: "126531dba926b3abc2809808a99573a5b788771d79d2a0696f46bf233141ef21",
    FIELD_CONTENT: "de37558cce41f97a37159ca4a2f28250df5b8ae37034b8154fa34a97b08c2bda",
    MISMATCH: "0d4dcf27ac003250e546dd96b92f6ce52b036f5c68ffc169b33e4154edc3f8bd",
    SPLICE: "01d53f278b1b55549b382a64a8faa9f83d8b2080934b0321cd92fe6c34c03bae",
    TRANSPORT: "96dd49d714c0b61fa95c2c63ef9ebc8e2cb32d739644b95164f413afe3fbb89e",
    P8_PROJECTOR: "c155389bda075609dbbcaf72fe23e3283395f7c3a5f5291f2ed42908a966be01",
    IDENTIFIABILITY: "d3b5bc38cc6832e09f5d5008138656ad785ca5d7319f4ecfd98c06e3bf66cd2d",
    AMPLITUDE_PROJECTOR: "12c8bfdfe28e5c5e16d3b348d70fbde335e03f7cf69c46fbe3c5a3524436dd27",
    ANCHOR_SCALE: "08c8ddeca1afe7ad992375e9b11dec6f10bc053b88df2a8347560f7bd3d1f48d",
    RESULT: "87461a2c25be6c9589384fa604d2b4bf85c529ffb40dc3f551643db2ddeb98b3",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def validation_row(
    index: int,
    requirement: str,
    observed: str,
    detail: object,
    passed: bool,
) -> dict[str, Any]:
    return {
        "check_id": f"VAL4971_{index:02d}",
        "requirement": requirement,
        "observed": observed,
        "detail": json.dumps(detail, sort_keys=True, default=str),
        "passed": bool(passed),
        "checkpoint_marker": MARKER,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }


def write_csv(rows: list[dict[str, Any]]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "check_id",
        "requirement",
        "observed",
        "detail",
        "passed",
        "checkpoint_marker",
        "valid_for_full_MTS_claim",
        "source_checked_date",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def finite_rows(rows: list[dict[str, str]], columns: tuple[str, ...]) -> bool:
    try:
        return all(
            math.isfinite(float(row[column]))
            for row in rows
            for column in columns
        )
    except (KeyError, TypeError, ValueError):
        return False


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    required_paths = [
        RUNNER,
        VALIDATOR,
        FIELD_CONTENT,
        MISMATCH,
        SPLICE,
        TRANSPORT,
        P8_PROJECTOR,
        IDENTIFIABILITY,
        AMPLITUDE_PROJECTOR,
        ANCHOR_SCALE,
        RESULT,
        PROVENANCE,
        CHECKPOINT,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        CLAIMS,
        VARIABLES,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
        *EXPECTED_HASHES,
    ]
    missing = sorted(str(path) for path in set(required_paths) if not path.exists())
    rows: list[dict[str, Any]] = []
    rows.append(
        validation_row(
            len(rows),
            "all 4971 source result document and register paths exist",
            f"{len(missing)} missing",
            missing,
            not missing,
        )
    )

    compile_failures: list[str] = []
    for script in (RUNNER, VALIDATOR):
        try:
            compile(script.read_text(encoding="utf-8"), str(script), "exec")
        except Exception as error:
            compile_failures.append(f"{script}: {error}")
    rows.append(
        validation_row(
            len(rows),
            "runner and validator compile without execution or bytecode",
            f"{len(compile_failures)} failures",
            compile_failures,
            not compile_failures,
        )
    )

    hash_failures: dict[str, dict[str, str]] = {}
    hash_results: dict[str, str] = {}
    for path, expected in EXPECTED_HASHES.items():
        if not path.exists():
            continue
        actual = digest(path)
        relative = path.relative_to(ROOT).as_posix()
        hash_results[relative] = actual
        if actual != expected:
            hash_failures[relative] = {"expected": expected, "actual": actual}
    rows.append(
        validation_row(
            len(rows),
            "all parent source amplitude runner and output hashes match",
            f"{len(hash_failures)} mismatches",
            hash_results,
            not missing and not hash_failures,
        )
    )

    field_content = read_csv(FIELD_CONTENT)
    mismatches = read_csv(MISMATCH)
    splices = read_csv(SPLICE)
    transports = read_csv(TRANSPORT)
    p8_projectors = read_csv(P8_PROJECTOR)
    identifiability = read_csv(IDENTIFIABILITY)
    amplitude_projectors = read_csv(AMPLITUDE_PROJECTOR)
    anchor_scales = read_csv(ANCHOR_SCALE)
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    rows.append(
        validation_row(
            len(rows),
            "4971 runner passes every internal check",
            f"all_checks_pass={result['all_checks_pass']}",
            result["checks"],
            result["all_checks_pass"] and not result["valid_for_full_MTS_claim"],
        )
    )

    inventory = {row["branch"]: row for row in field_content}
    rows.append(
        validation_row(
            len(rows),
            "eight field-content branches include the SM45 parent bracket",
            f"{len(field_content)} branches",
            {key: value["total_Nb_minus_Nf"] for key, value in inventory.items()},
            len(field_content) == 8
            and float(inventory["SM45"]["total_Nb_minus_Nf"]) == -60.0
            and float(inventory["SM45_PLUS_MOTION"]["total_Nb_minus_Nf"]) == -59.0,
        )
    )

    bridge_ok = all(
        math.isclose(
            float(row["beta_A_onshell"]),
            float(row["total_Nb_minus_Nf"]) / (7680.0 * math.pi**3),
            rel_tol=2e-15,
        )
        and math.isclose(
            float(row["beta_c_amplitude"]),
            -float(row["total_Nb_minus_Nf"]) / 240.0,
            rel_tol=2e-15,
        )
        for row in field_content
    )
    rows.append(
        validation_row(
            len(rows),
            "every state-count branch obeys the amplitude-to-Bern running bridge",
            f"bridge_ok={bridge_ok}",
            {},
            bridge_ok,
        )
    )

    expected_splice_keys = {
        (branch, scheme, order, gravity)
        for branch in ("SM45", "SM45_PLUS_MOTION")
        for scheme in ("dynamic_etaN", "reference_etaN0")
        for order in (6, 8)
        for gravity in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6)
    }
    observed_splice_keys = {
        (
            row["branch"],
            row["scheme"],
            int(row["polynomial_order"]),
            float(row["g_match"]),
        )
        for row in splices
    }
    rows.append(
        validation_row(
            len(rows),
            "all forty parent branch scheme order and scale splices exist",
            f"{len(splices)} rows",
            sorted(observed_splice_keys),
            len(splices) == 40 and observed_splice_keys == expected_splice_keys,
        )
    )

    transport_keys = {
        (
            row["branch"],
            row["scheme"],
            int(row["polynomial_order"]),
            float(row["target_g_match"]),
        )
        for row in transports
    }
    maximum_transport = max(
        abs(float(row[column]))
        for row in transports
        for column in ("A_endpoint_residual", "B_minus_endpoint_residual")
    )
    rows.append(
        validation_row(
            len(rows),
            "all forty transports restore parent endpoint invariance",
            f"rows={len(transports)}; max={maximum_transport:.12g}",
            {},
            len(transports) == 40
            and transport_keys == expected_splice_keys
            and maximum_transport <= 4e-11
            and math.isclose(
                maximum_transport,
                result["maximum_transport_endpoint_residual"],
                rel_tol=2e-14,
            ),
        )
    )

    expected_amplitude_ids = {
        "AMP4971_00_physical_coupling",
        "AMP4971_01_all_plus",
        "AMP4971_02_single_minus",
        "AMP4971_03_helicity_identity",
        "AMP4971_04_all_plus_finite_constant",
        "AMP4971_05_running_bridge",
        "AMP4971_06_RG_invariant_scale",
    }
    amplitude_by_id = {row["projector_id"]: row for row in amplitude_projectors}
    rows.append(
        validation_row(
            len(rows),
            "all seven finite amplitude projector clauses are present",
            f"{len(amplitude_projectors)} rows",
            sorted(amplitude_by_id),
            len(amplitude_projectors) == 7
            and set(amplitude_by_id) == expected_amplitude_ids,
        )
    )

    all_plus = amplitude_by_id["AMP4971_01_all_plus"]
    single_minus = amplitude_by_id["AMP4971_02_single_minus"]
    identity = amplitude_by_id["AMP4971_03_helicity_identity"]
    rows.append(
        validation_row(
            len(rows),
            "the exact all-plus single-minus and factor-ten projectors are locked",
            f"coefficients={all_plus['coupling_coefficient_in_stu_basis']},{single_minus['coupling_coefficient_in_stu_basis']},{identity['coupling_coefficient_in_stu_basis']}",
            result["finite_amplitude_projector"],
            float(all_plus["coupling_coefficient_in_stu_basis"]) == -60.0
            and float(single_minus["coupling_coefficient_in_stu_basis"]) == -6.0
            and float(identity["coupling_coefficient_in_stu_basis"]) == 10.0
            and result["finite_amplitude_projector"]["synthetic_inversion_exact"],
        )
    )

    finite_constant = amplitude_by_id[
        "AMP4971_04_all_plus_finite_constant"
    ]
    rows.append(
        validation_row(
            len(rows),
            "the finite c=0 Einstein subtraction constant is exact",
            finite_constant["coupling_coefficient_in_stu_basis"],
            {},
            math.isclose(
                float(finite_constant["coupling_coefficient_in_stu_basis"]),
                117617.0 / 21600.0,
                rel_tol=2e-15,
            ),
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "the amplitude source bundle is current v2 and directly extracted",
            f"archive_bytes={ABREU_ARCHIVE.stat().st_size}",
            {
                "archive": digest(ABREU_ARCHIVE),
                "all_plus": digest(ABREU_PPPP),
                "single_minus": digest(ABREU_MPPP),
            },
            ABREU_ARCHIVE.stat().st_size == 160914
            and "v2" in PROVENANCE.read_text(encoding="utf-8")
            and "no OCR" in PROVENANCE.read_text(encoding="utf-8"),
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "eight zero-offset anchor-scale rows remain diagnostic nonclaims",
            f"{len(anchor_scales)} rows",
            [row["lambda_over_mu_if_zero_offset"] for row in anchor_scales],
            len(anchor_scales) == 8
            and finite_rows(
                anchor_scales,
                (
                    "beta_A_onshell",
                    "A_functional_match",
                    "c_amplitude_if_zero_offset",
                    "lambda_over_mu_if_zero_offset",
                    "lambda_GeV_if_zero_offset",
                ),
            )
            and all(
                float(row["lambda_over_mu_if_zero_offset"]) > 0.0
                and row["status"]
                == "ZERO_OFFSET_SCALE_DIAGNOSTIC_NOT_A_MATCHING_RESULT"
                and row["valid_for_full_MTS_claim"].lower() == "false"
                for row in anchor_scales
            ),
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "all four two-scale projectors have full E6-p8 rank five",
            f"{len(p8_projectors)} rows",
            [
                {
                    "id": row["projector_id"],
                    "rank": row["full_two_scale_matrix_rank"],
                    "det": row["channel_determinant"],
                }
                for row in p8_projectors
            ],
            len(p8_projectors) == 4
            and all(
                int(row["full_two_scale_matrix_rank"]) == 5
                and int(row["full_two_scale_nullity"]) == 0
                and int(row["p8_two_scale_matrix_rank"]) == 4
                and abs(float(row["channel_determinant"])) > 1e-3
                for row in p8_projectors
            ),
        )
    )

    final_gate = identifiability[-1]
    rows.append(
        validation_row(
            len(rows),
            "the local-only route is rejected while the amplitude route is retained",
            final_gate["status"],
            final_gate,
            final_gate["status"]
            == "LOCAL_ONLY_ANCHOR_REJECTED_EXACT_AMPLITUDE_ROUTE_DERIVED"
            and "finite Wilsonian-to-amplitude conversion"
            in final_gate["result"],
        )
    )

    machine_paths = (
        FIELD_CONTENT,
        MISMATCH,
        SPLICE,
        TRANSPORT,
        P8_PROJECTOR,
        IDENTIFIABILITY,
        AMPLITUDE_PROJECTOR,
        ANCHOR_SCALE,
        RESULT,
    )
    machine_text = "\n".join(
        path.read_text(encoding="utf-8-sig") for path in machine_paths
    )
    placeholders = [
        token
        for token in ("MISSING_", "PLACEHOLDER", "TO_BE_CALCULATED")
        if token in machine_text
    ]
    rows.append(
        validation_row(
            len(rows),
            "new machine outputs contain no placeholder markers",
            f"{len(placeholders)} markers",
            placeholders,
            not placeholders,
        )
    )

    claim_flags = [
        row.get("valid_for_full_MTS_claim", "").lower()
        for dataset in (
            field_content,
            mismatches,
            splices,
            transports,
            p8_projectors,
            identifiability,
            amplitude_projectors,
            anchor_scales,
        )
        for row in dataset
    ]
    rows.append(
        validation_row(
            len(rows),
            "every generated CSV row remains nonclaim",
            f"{len(claim_flags)} flags",
            sorted(set(claim_flags)),
            claim_flags and all(flag == "false" for flag in claim_flags),
        )
    )

    marker_documents = (
        PROVENANCE,
        CHECKPOINT,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
    )
    marker_failures = [
        str(path)
        for path in marker_documents
        if CHECKPOINT_MARKER not in path.read_text(encoding="utf-8")
    ]
    rows.append(
        validation_row(
            len(rows),
            "checkpoint marker is propagated through every handoff document",
            f"{len(marker_failures)} failures",
            marker_failures,
            not marker_failures,
        )
    )

    claim_rows = read_csv(CLAIMS)
    claim = next((row for row in claim_rows if row.get("claim_id") == "L-813"), None)
    rows.append(
        validation_row(
            len(rows),
            "claims register contains the private nonclaim 4971 row",
            "L-813 present" if claim else "L-813 missing",
            claim or {},
            claim is not None
            and CHECKPOINT_MARKER in claim.get("notes", "")
            and "full MTS" in claim.get("risk", ""),
        )
    )

    required_variables = {
        "Nparent4971_MTS",
        "c_amp4971",
        "A_amp4971_MTS",
        "lambda_C34971",
        "P_E6_4971_MTS",
        "P_E8_2scale4971_MTS",
        "PredictivityStatus4971_MTS",
    }
    variable_rows = read_csv(VARIABLES)
    observed_variables = {
        row.get("symbol", "")
        for row in variable_rows
        if row.get("symbol", "") in required_variables
    }
    rows.append(
        validation_row(
            len(rows),
            "variable audit contains all seven 4971 coordinates and certificates",
            f"{len(observed_variables)}/7 present",
            sorted(observed_variables),
            observed_variables == required_variables,
        )
    )

    resume_head = "\n".join(RESUME.read_text(encoding="utf-8").splitlines()[:10])
    rows.append(
        validation_row(
            len(rows),
            "current resume points to checkpoint 4971",
            resume_head,
            {},
            "Last checkpoint: `4971-" in resume_head
            and CHECKPOINT_MARKER in resume_head,
        )
    )

    numeric_ok = finite_rows(
        splices,
        (
            "beta_A_onshell",
            "A_functional_match",
            "A_onshell_endpoint_zero_anchor",
            "B_minus_matched_endpoint_zero_anchor",
            "B_plus_matched_endpoint_zero_anchor",
        ),
    ) and finite_rows(
        p8_projectors,
        (
            "B_boundary_transfer_1",
            "B_primitive_transfer_1",
            "B_boundary_transfer_2",
            "B_primitive_transfer_2",
            "channel_determinant",
            "channel_condition_number",
        ),
    )
    rows.append(
        validation_row(
            len(rows),
            "all splice scale and projector numeric fields are finite",
            f"finite={numeric_ok}",
            {},
            numeric_ok,
        )
    )

    pycache = sorted(str(path) for path in (POST / "scripts").rglob("__pycache__"))
    rows.append(
        validation_row(
            len(rows),
            "post-checkpoint scripts contain no bytecode cache",
            f"{len(pycache)} directories",
            pycache,
            not pycache,
        )
    )

    verdict = result["absolute_anchor_verdict"]
    rows.append(
        validation_row(
            len(rows),
            "numeric lambda direct parent thresholds complete amplitude and full MTS remain unclaimed",
            verdict["status"],
            verdict,
            result["valid_for_full_MTS_claim"] is False
            and verdict["derived_from_current_local_running"] is False
            and verdict["free_object_after_4971"]
            == "one RG-invariant scale lambda, not an unspecified functional form",
        )
    )

    write_csv(rows)
    failed = [row["check_id"] for row in rows if not row["passed"]]
    print(f"{MARKER}_CHECKS={len(rows)}", flush=True)
    print(f"{MARKER}_PASSED={len(rows) - len(failed)}", flush=True)
    print(f"{MARKER}_FAILED={len(failed)}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    if failed:
        print(f"{MARKER}_FAILED_IDS={','.join(failed)}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
