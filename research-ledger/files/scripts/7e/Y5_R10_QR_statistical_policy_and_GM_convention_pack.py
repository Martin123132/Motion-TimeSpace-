from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1244"
TITLE = "1244-Y5-R10-QR-statistical-policy-and-GM-convention-pack"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
GM_CONVENTION_PATH = OUT_DIR / f"{PACK_ID}_GM_CONVENTION_PACK.csv"
STAT_POLICY_PATH = OUT_DIR / f"{PACK_ID}_PPN_GAMMA_STATISTICAL_POLICY.csv"
BOUND_DERIVATION_PATH = OUT_DIR / f"{PACK_ID}_QR_BOUND_DERIVATION_NONCLAIM.csv"
RUNNER_POLICY_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_POLICY_FEED.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1244_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1244_0_1243_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1243_NEXT_TARGET.csv",
            "needle": "NEXT1243_0_1244",
            "purpose": "1243 handoff to GM convention and statistical policy pack",
        },
        {
            "source_id": "SRC1244_1_1243_hunt",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1243_SOURCE_HUNT_LEDGER.csv",
            "needle": "HUNT1243_2_GM_policy",
            "purpose": "GM policy source-hunt row",
        },
        {
            "source_id": "SRC1244_2_1243_stat",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1243_SOURCE_HUNT_LEDGER.csv",
            "needle": "HUNT1243_3_statistical_policy",
            "purpose": "statistical policy source-hunt row",
        },
        {
            "source_id": "SRC1244_3_1240_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_BOUND_INPUT_SCHEMA.csv",
            "needle": "QB1240_3_pass_rule",
            "purpose": "pass-rule schema requiring N_sigma and uncertainty policy",
        },
        {
            "source_id": "SRC1244_4_1240_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            "needle": "QMAP1240_2_dimensionless_qR",
            "purpose": "q_R_hat normalization",
        },
        {
            "source_id": "SRC1244_5_1240_comparator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_PPN_COMPARATOR_LEDGER.csv",
            "needle": "COMP1240_0_gamma_Cassini",
            "purpose": "Cassini gamma comparator",
        },
        {
            "source_id": "SRC1244_6_1181_source",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "needle": "SRC1181W_0_Cassini_gamma",
            "purpose": "Cassini gamma provenance and uncertainty",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    gm_convention = [
        {
            "convention_id": "GM1244_0_qR_definition",
            "quantity": "q_R_hat",
            "convention": "q_R_hat = Q_R c^2/(G M_source)",
            "required_future_row": "finite q_R_hat candidates must declare whether they supply q_R_hat directly or raw Q_R plus G M_source",
            "status": "CONVENTION_DECLARED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "convention_id": "GM1244_1_source_body",
            "quantity": "M_source",
            "convention": "for Cassini gamma comparator rows, the default source body is the solar-system central mass used by the cited gamma analysis; future rows must name the source body explicitly",
            "required_future_row": "source_body=Sun or explicit alternative with reason",
            "status": "CONVENTION_DECLARED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "convention_id": "GM1244_2_measured_GM",
            "quantity": "G M_source",
            "convention": "use measured/dynamical GM from the same weak-field comparator convention; do not infer GM from MTS q_R fitting",
            "required_future_row": "GM_source_value or directly_dimensionless_q_R_hat plus provenance",
            "status": "CONVENTION_DECLARED_SOURCE_STILL_REQUIRED_FOR_RAW_QR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "convention_id": "GM1244_3_coordinate",
            "quantity": "r and U",
            "convention": "weak-field map assumes areal-radial matching and U=GM/r in the same convention used by QMAP1240",
            "required_future_row": "coordinate_convention=areal_radial_weak_field or explicit mapping correction",
            "status": "CONVENTION_DECLARED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    stat_policy = [
        {
            "policy_id": "STAT1244_0_default_smoke",
            "policy_name": "strict_one_sigma_nonclaim_smoke",
            "observable": "gamma_minus_1",
            "central_value": "2.1e-5",
            "sigma": "2.3e-5",
            "N_sigma": 1,
            "pass_rule": "abs(gamma_minus_1_QR) <= 1 * 2.3e-5",
            "use": "strict smoke/refusal policy only; not a discovery or publication criterion",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv", "SRC1181W_0_Cassini_gamma"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "policy_id": "STAT1244_1_center_handling",
            "policy_name": "residual_about_GR_zero",
            "observable": "gamma_minus_1_QR",
            "central_value": "0 expected for closure GR baseline; observed central value is recorded but not fitted",
            "sigma": "2.3e-5",
            "N_sigma": 1,
            "pass_rule": "compare finite residual magnitude to uncertainty guardrail, not to a fitted offset",
            "use": "prevents using the observed central offset as an MTS fit target",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1240_PPN_COMPARATOR_LEDGER.csv", "COMP1240_0_gamma_Cassini"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "policy_id": "STAT1244_2_alt_policy",
            "policy_name": "looser_two_or_three_sigma",
            "observable": "gamma_minus_1",
            "central_value": "2.1e-5",
            "sigma": "2.3e-5",
            "N_sigma": "2_or_3_only_if_explicitly_labelled",
            "pass_rule": "allowed only as sensitivity branch, never replacing strict smoke",
            "use": "future robustness/sensitivity branch",
            "source": "same comparator; branch must be labelled separately",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    q_bound_abs = 2 * 1 * 2.3e-5
    bound_derivation = [
        {
            "derive_id": "QBD1244_0_projection",
            "input": "gamma_minus_1_QR = -q_R_hat/2",
            "policy": "strict_one_sigma_nonclaim_smoke",
            "result": "abs(q_R_hat) <= 2*N_sigma*sigma_gamma",
            "numeric_guardrail": q_bound_abs,
            "units": "dimensionless",
            "status": "NONCLAIM_GUARDRAIL_DERIVED_FROM_SCHEMA",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derive_id": "QBD1244_1_missing_qR",
            "input": "q_R_hat",
            "policy": "strict_one_sigma_nonclaim_smoke",
            "result": "q_R_hat value remains missing",
            "numeric_guardrail": "MISSING_QR_VALUE",
            "units": "dimensionless",
            "status": "NO_NUMERIC_MTS_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_policy_feed = [
        {
            "feed_id": "RPF1244_0_policy",
            "target_runner": "1241 Q_R nonclaim smoke runner",
            "N_sigma": 1,
            "sigma_gamma": "2.3e-5",
            "q_R_hat_abs_guardrail": q_bound_abs,
            "GM_convention_status": "DECLARED_CONTRACT_ONLY",
            "q_R_hat_status": "MISSING_QR_VALUE_UNCHANGED",
            "feed_status": "POLICY_READY_QR_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    decisions = [
        {
            "decision_id": "DEC1244_0_policy_filled",
            "decision": "fill N_sigma/sigma_gamma policy for future smoke runner",
            "because": "1241 refused numeric q_R_hat rows without statistical policy",
            "next_action": "future finite q_R_hat rows can now be rejected for value/source rather than missing policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1244_1_GM_convention_filled",
            "decision": "declare GM/source convention requirements",
            "because": "q_R_hat normalization is meaningless without source mass convention",
            "next_action": "future finite rows must name source body and GM provenance or provide directly dimensionless q_R_hat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1244_2_qR_still_missing",
            "decision": "do not fabricate q_R_hat",
            "because": "1244 only fills policy and convention prerequisites",
            "next_action": "feed policy into smoke runner while keeping q_R_hat missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1244_0_policy",
            "claim": "nonclaim statistical policy exists",
            "status": "PASS_NONCLAIM",
            "reason": "strict one-sigma smoke policy and guardrail are declared",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1244_1_GM_convention",
            "claim": "GM convention contract exists",
            "status": "PASS_NONCLAIM",
            "reason": "q_R_hat normalization and future source-body/GM requirements are declared",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1244_2_qR_value",
            "claim": "q_R_hat value exists",
            "status": "BLOCKED",
            "reason": "runner policy feed keeps q_R_hat_status=MISSING_QR_VALUE_UNCHANGED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1244_3_local_GR",
            "claim": "local GR/Newton pass",
            "status": "BLOCKED",
            "reason": "policy/convention plumbing is not a Q_R theorem or finite value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1244_0_1245",
            "target_file": "1245-Y5-R10-PPN-QR-policy-fed-smoke-runner-and-source-hunt-update.md",
            "target_script": "scripts/Y5_R10_PPN_QR_policy_fed_smoke_runner_and_source_hunt_update.py",
            "task": "feed the 1244 statistical policy and GM convention into the 1241 Q_R smoke runner, verify the only remaining refusal is missing q_R_hat/source theorem, and update the source-hunt ledger",
            "success_condition": "runner no longer fails for missing policy, still refuses missing q_R_hat, and no local-GR/PPN claim is promoted",
            "do_not_do": "do not fabricate q_R_hat, do not run long jobs, and do not claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        GM_CONVENTION_PATH,
        STAT_POLICY_PATH,
        BOUND_DERIVATION_PATH,
        RUNNER_POLICY_FEED_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(GM_CONVENTION_PATH, gm_convention)
    write_csv(STAT_POLICY_PATH, stat_policy)
    write_csv(BOUND_DERIVATION_PATH, bound_derivation)
    write_csv(RUNNER_POLICY_FEED_PATH, runner_policy_feed)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    gm_declared = len(gm_convention) == 4 and all(row["status"].startswith("CONVENTION_DECLARED") for row in gm_convention)
    strict_policy = any(
        row["policy_id"] == "STAT1244_0_default_smoke" and str(row["N_sigma"]) == "1" and row["sigma"] == "2.3e-5"
        for row in stat_policy
    )
    q_bound_ok = any(
        row["derive_id"] == "QBD1244_0_projection" and abs(float(row["numeric_guardrail"]) - 4.6e-5) < 1e-12
        for row in bound_derivation
    )
    q_missing_unchanged = runner_policy_feed[0]["q_R_hat_status"] == "MISSING_QR_VALUE_UNCHANGED"
    claim_gates_ok = all(
        row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            gm_convention,
            stat_policy,
            bound_derivation,
            runner_policy_feed,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    next_is_1245 = next_target[0]["target_file"].startswith("1245-Y5-R10-PPN-QR-policy")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1244_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1244_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1244_2_GM_convention",
            "GM/source convention rows are declared",
            gm_declared,
            f"gm_rows={len(gm_convention)}",
        ),
        validation_row(
            "VAL1244_3_stat_policy",
            "strict one-sigma nonclaim policy is declared",
            strict_policy,
            "N_sigma=1 sigma_gamma=2.3e-5",
        ),
        validation_row(
            "VAL1244_4_q_bound",
            "q_R_hat guardrail derives from gamma schema",
            q_bound_ok,
            "abs(q_R_hat)<=4.6e-5 strict smoke guardrail",
        ),
        validation_row(
            "VAL1244_5_qR_missing",
            "q_R_hat remains missing",
            q_missing_unchanged,
            runner_policy_feed[0]["q_R_hat_status"],
        ),
        validation_row(
            "VAL1244_6_claim_gates",
            "claim gates remain blocked/nonclaim",
            claim_gates_ok,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1244_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1244_8_next_target_1245",
            "next target is policy-fed Q_R smoke runner",
            next_is_1245,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1244_9_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1244_10_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1244_11_overall",
            "overall 1244 validation",
            all(row["status"] == "PASS" for row in validation),
            "1244 declares GM convention and nonclaim PPN gamma statistical policy while leaving q_R_hat missing",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1244 fills the non-theory prerequisites for future finite `q_R_hat` scoring: GM/source convention and a strict one-sigma nonclaim gamma policy. It still does **not** supply `q_R_hat`.",
        "",
        "**Main progress:** future `q_R_hat` rows now have a declared normalization and pass policy. The strict smoke guardrail is `abs(q_R_hat) <= 4.6e-5`, derived from `gamma_minus_1_QR=-q_R_hat/2` and `sigma_gamma=2.3e-5`.",
        "",
        "**No-claim guard:** no `Q_R=0`, finite `Q_R` pass, PPN pass, local-GR pass, WEP/R10 pass, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## GM Convention Pack",
        markdown_table(gm_convention, list(gm_convention[0].keys())),
        "",
        "## PPN Gamma Statistical Policy",
        markdown_table(stat_policy, list(stat_policy[0].keys())),
        "",
        "## QR Bound Derivation Nonclaim",
        markdown_table(bound_derivation, list(bound_derivation[0].keys())),
        "",
        "## Runner Policy Feed",
        markdown_table(runner_policy_feed, list(runner_policy_feed[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
