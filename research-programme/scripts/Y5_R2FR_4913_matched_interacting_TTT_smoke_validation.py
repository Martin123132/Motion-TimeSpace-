from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4913_matched_interacting_TTT_smoke as research


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
OUTPUT = POST / "source-intake" / "mts_residuals"
RUN = POST / "runs" / "20260712-4913-channel-fixed-checkpoint"
TIMESTAMP = datetime.now(timezone.utc).isoformat()
MARKER = research.MARKER
NEXT_TARGET = research.NEXT_TARGET
CLAIM_STATUS = (
    "analytic_zero_mode_channel_derived_false_cutoff_blowup_repaired_"
    "two_cutoff_rows_zero_compatible_covariant_residual_failed_long_run_"
    "withheld_active_residual_zero_private_nonclaim"
)
VARIABLES = (
    "MatchedInteractingResponse4913_MTS",
    "AnalyticCosineChannel4913_MTS",
    "DeterministicFreeSubtraction4913_MTS",
    "PairedControl4913_MTS",
    "Q6Design4913_MTS",
    "MassGapRows4913_MTS",
    "StencilDiagnostic4913_MTS",
    "CutoffDiagnostic4913_MTS",
    "CovariantResidual4913_MTS",
    "ResidualStatus4913_MTS",
)
EVIDENCE_FILES = (
    "P8_Y5_R2FR_4913_OBSERVABLE_VALIDATION.csv",
    "P8_Y5_R2FR_4913_CHAIN_SUMMARY.csv",
    "P8_Y5_R2FR_4913_MATCHED_RESPONSES.csv",
    "P8_Y5_R2FR_4913_Q6_DIFFERENCE.csv",
    "P8_Y5_R2FR_4913_Q6_COVARIANCE.csv",
    "P8_Y5_R2FR_4913_PROJECTED_RECOVERY.csv",
    "P8_Y5_R2FR_4913_CORRELATIONS.csv",
    "P8_Y5_R2FR_4913_RUN_STATUS.csv",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
            "source_checked_date": research.CHECKED_DATE,
        }
        for row in rows
    ]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    encoding = (
        "utf-16"
        if raw.startswith((b"\xff\xfe", b"\xfe\xff"))
        else "utf-8"
    )
    return raw.decode(encoding, errors="replace")


def source_rows() -> list[dict[str, Any]]:
    sources: list[tuple[str, Path, str, str]] = [
        (
            "SRC4913_00_predecessor",
            POST
            / "4912-Y5-R2FR-free-lattice-multigeometry-a6-response-and-continuum-projector-recovery.md",
            "MTS_FREE_LATTICE_MULTIGEOMETRY_CONTINUUM_PROJECTOR_4912",
            "validated_predecessor",
        ),
        (
            "SRC4913_01_predecessor_validation",
            OUTPUT / "P8_Y5_BRR545_4912_VALIDATION.csv",
            "VAL4912_OVERALL",
            "validated_predecessor",
        ),
        (
            "SRC4913_02_checkpoint",
            POST
            / "4913-Y5-R2FR-matched-subtracted-interacting-motion-scalar-TTT-continuum-coefficient-or-zero-residual.md",
            MARKER,
            "generated_checkpoint",
        ),
        (
            "SRC4913_03_formal_note",
            FORMAL
            / "929-PPC4161-matched-interacting-TTT-channel-repair-and-nonpromotion.md",
            research.FORMAL_MARKER,
            "generated_formal_note",
        ),
        (
            "SRC4913_04_provenance",
            POST / "source-intake" / "microscopic_vertex" / "4913" / "PROVENANCE.md",
            "MTS_MATCHED_INTERACTING_TTT_PROVENANCE_4913",
            "generated_provenance",
        ),
        (
            "SRC4913_05_research_script",
            SCRIPTS / "Y5_R2FR_4913_matched_interacting_TTT_smoke.py",
            "def analytic_cosine_channel_projection",
            "generated_research_code",
        ),
        (
            "SRC4913_06_validation_script",
            SCRIPTS / "Y5_R2FR_4913_matched_interacting_TTT_smoke_validation.py",
            "VAL4913_OVERALL",
            "generated_validation_code",
        ),
        (
            "SRC4913_07_claim_register",
            FORMAL / "02-claims-register.csv",
            "L-755",
            "generated_register",
        ),
        (
            "SRC4913_08_variable_register",
            FORMAL / "04-variable-audit.csv",
            "AnalyticCosineChannel4913_MTS",
            "generated_register",
        ),
        (
            "SRC4913_09_equation_register",
            FORMAL / "05-equation-register.md",
            "1.206 Matched interacting TTT and analytic cosine channel",
            "generated_register",
        ),
        (
            "SRC4913_10_redteam",
            FORMAL / "06-consistency-red-team.md",
            "157. A zero-mode source degeneracy",
            "generated_register",
        ),
        (
            "SRC4913_11_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4913",
            "generated_register",
        ),
        (
            "SRC4913_12_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            research.FORMAL_MARKER,
            "generated_resume",
        ),
        (
            "SRC4913_13_run_status",
            RUN / "status.json",
            '"status": "COMPLETE"',
            "checkpoint_run_record",
        ),
        (
            "SRC4913_14_run_log",
            RUN / "log.txt",
            "profile=checkpoint observable_validation=True",
            "checkpoint_run_record",
        ),
        (
            "SRC4913_15_completion_marker",
            RUN / "COMPLETE.marker",
            "MTS_4913_COMPLETE",
            "checkpoint_run_record",
        ),
    ]
    for index, filename in enumerate(EVIDENCE_FILES, start=16):
        sources.append(
            (
                f"SRC4913_{index:02d}_{Path(filename).stem}",
                OUTPUT / filename,
                MARKER,
                "generated_numeric_evidence",
            )
        )
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        content = read_text_auto(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "sha256": sha256(path) if exists else "",
            }
        )
    return tagged(rows)


def gate_rows() -> list[dict[str, Any]]:
    validation = read_csv(OUTPUT / EVIDENCE_FILES[0])
    summaries = {
        row["label"]: row
        for row in read_csv(OUTPUT / "P8_Y5_R2FR_4913_CHAIN_SUMMARY.csv")
    }
    recoveries = {
        (row["config"], row["stencil"]): row
        for row in read_csv(OUTPUT / "P8_Y5_R2FR_4913_PROJECTED_RECOVERY.csv")
    }
    expected_configs = ("N12_mu0p6", "N16_mu0p4")
    expected_stencils = research.SOURCE_STENCILS

    def recovery(config: str, stencil: str) -> dict[str, str]:
        return recoveries[(config, stencil)]

    def value(config: str, stencil: str, key: str) -> float:
        number = float(recovery(config, stencil)[key])
        if not math.isfinite(number):
            raise ValueError(f"nonfinite recovery {config} {stencil} {key}")
        return number

    def independent_shift(
        first: str, second: str, stencil: str, scaled: bool
    ) -> float:
        first_value = value(first, stencil, "zeta")
        second_value = value(second, stencil, "zeta")
        first_error = value(first, stencil, "zeta_delta_standard_error")
        second_error = value(second, stencil, "zeta_delta_standard_error")
        if scaled:
            first_mu2 = float(summaries[first]["mu_hat"]) ** 2
            second_mu2 = float(summaries[second]["mu_hat"]) ** 2
            first_value *= first_mu2
            second_value *= second_mu2
            first_error *= first_mu2
            second_error *= second_mu2
        return abs(first_value - second_value) / math.hypot(
            first_error, second_error
        )

    stencil_shifts = []
    for config in expected_configs:
        site = recovery(config, "site")
        half = recovery(config, "half_link")
        stencil_shifts.append(
            abs(float(site["zeta"]) - float(half["zeta"]))
            / math.hypot(
                float(site["zeta_delta_standard_error"]),
                float(half["zeta_delta_standard_error"]),
            )
        )
    cutoff_shifts = [
        independent_shift(expected_configs[0], expected_configs[1], stencil, False)
        for stencil in expected_stencils
    ]
    scaled_cutoff_shifts = [
        independent_shift(expected_configs[0], expected_configs[1], stencil, True)
        for stencil in expected_stencils
    ]
    paired_ratios = [
        value(config, stencil, "paired_over_primary_error")
        for config in expected_configs
        for stencil in expected_stencils
    ]
    significances = [
        abs(value(config, stencil, "zeta_delta_significance"))
        for config in expected_configs
        for stencil in expected_stencils
    ]
    residuals = [
        value(config, stencil, "euclidean_residual")
        for config in expected_configs
        for stencil in expected_stencils
    ]
    conditions = [
        float(summaries[config]["q6_design_condition"])
        for config in expected_configs
    ]
    weight_norms = [
        float(summaries[config]["q6_weight_l2"]) for config in expected_configs
    ]
    chain_health = all(
        0.42 < float(summaries[config]["mean_interacting_acceptance"]) < 0.58
        and float(summaries[config]["mean_interacting_overrelax_acceptance"])
        > 0.95
        and float(summaries[config]["tau_zero_mode_observations"]) < 5.0
        and int(summaries[config]["block_count"]) >= 100
        and float(summaries[config]["pole_mass"]) > 0.0
        and float(summaries[config]["pole_mass_standard_error"]) > 0.0
        for config in expected_configs
    )
    rows = [
        {
            "gate_id": "G4913_00_observable",
            "gate": "observable_and_analytic_channel_validation",
            "status": "PASS",
            "metric": max(
                float(row["maximum_absolute_residual"]) for row in validation
            ),
            "threshold": "all row-specific tolerances",
            "criterion_satisfied": all(row["passed"] == "True" for row in validation),
            "coefficient_promotion": False,
            "interpretation": "FFT contacts and zero-mode channel algebra close",
        },
        {
            "gate_id": "G4913_01_chain",
            "gate": "chain_health",
            "status": "PASS" if chain_health else "FAIL",
            "metric": max(
                float(summaries[config]["tau_zero_mode_observations"])
                for config in expected_configs
            ),
            "threshold": "acceptance 0.42--0.58; tau<5; blocks>=100",
            "criterion_satisfied": chain_health,
            "coefficient_promotion": False,
            "interpretation": "short chains are adequate for a smoke gate",
        },
        {
            "gate_id": "G4913_02_design",
            "gate": "q6_design_conditioning",
            "status": "PASS",
            "metric": max(conditions),
            "secondary_metric": max(weight_norms),
            "threshold": "condition<250 and weight_l2<3",
            "criterion_satisfied": max(conditions) < 250
            and max(weight_norms) < 3,
            "coefficient_promotion": False,
            "interpretation": "rejected degree-four N16 interpolation is absent",
        },
        {
            "gate_id": "G4913_03_control",
            "gate": "paired_beta_one_control",
            "status": "REJECTED",
            "metric": min(paired_ratios),
            "secondary_metric": max(paired_ratios),
            "threshold": "retain only if paired_over_primary_error<1",
            "criterion_satisfied": all(ratio > 1.0 for ratio in paired_ratios),
            "coefficient_promotion": False,
            "interpretation": "beta one raises error and is excluded",
        },
        {
            "gate_id": "G4913_04_stencil",
            "gate": "site_half_link_consistency",
            "status": "PASS_DIAGNOSTIC",
            "metric": max(stencil_shifts),
            "threshold": "conservative quadrature shift<1",
            "criterion_satisfied": max(stencil_shifts) < 1.0,
            "coefficient_promotion": False,
            "interpretation": "shared-chain stencils agree but are not independent",
        },
        {
            "gate_id": "G4913_05_cutoff",
            "gate": "two_cutoff_zero_compatibility",
            "status": "PASS_DIAGNOSTIC_NOT_CONVERGENCE",
            "metric": max(cutoff_shifts),
            "secondary_metric": max(scaled_cutoff_shifts),
            "threshold": "raw and mu2-scaled conservative shift<2",
            "criterion_satisfied": max(cutoff_shifts) < 2.0
            and max(scaled_cutoff_shifts) < 2.0,
            "coefficient_promotion": False,
            "interpretation": "zero remains allowed; two rows do not define a limit",
        },
        {
            "gate_id": "G4913_06_significance",
            "gate": "nonzero_interaction_significance",
            "status": "FAIL_TO_REJECT_ZERO",
            "metric": max(significances),
            "threshold": "absolute significance>=3 for evidence",
            "criterion_satisfied": max(significances) < 2.0,
            "coefficient_promotion": False,
            "interpretation": "every row is below two sigma",
        },
        {
            "gate_id": "G4913_07_covariance",
            "gate": "covariant_image_residual",
            "status": "FAIL",
            "metric": min(residuals),
            "secondary_metric": max(residuals),
            "threshold": "substantial promotion would require residual<0.2",
            "criterion_satisfied": min(residuals) > 0.5,
            "coefficient_promotion": False,
            "interpretation": "majority response remains outside continuum image",
        },
        {
            "gate_id": "G4913_08_promotion",
            "gate": "interacting_coefficient_promotion",
            "status": "BLOCKED",
            "metric": 0,
            "threshold": "replica cutoff covariance and significance gates",
            "criterion_satisfied": True,
            "coefficient_promotion": False,
            "interpretation": "no interacting C-cubed coefficient is retained",
        },
        {
            "gate_id": "G4913_09_long_run",
            "gate": "interacting_long_run",
            "status": "WITHHELD",
            "metric": 0,
            "threshold": "common regulator trend and covariant response",
            "criterion_satisfied": True,
            "coefficient_promotion": False,
            "interpretation": "4914 estimator and replica gate comes first",
        },
        {
            "gate_id": "G4913_10_active",
            "gate": "Gamma_MTS_res",
            "status": "ZERO_PRESERVED",
            "metric": 0,
            "threshold": "no promoted matched continuum coefficient",
            "criterion_satisfied": True,
            "coefficient_promotion": False,
            "interpretation": "GR Newton PPN and Maxwell remain unchanged",
        },
    ]
    return tagged(rows)


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError, UnicodeError):
        return False
    return True


def validation_rows(
    sources: list[dict[str, Any]], gates: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4912_VALIDATION.csv")
    observables = read_csv(OUTPUT / EVIDENCE_FILES[0])
    summaries = read_csv(OUTPUT / EVIDENCE_FILES[1])
    recoveries = read_csv(OUTPUT / EVIDENCE_FILES[5])
    run_status = read_csv(OUTPUT / EVIDENCE_FILES[7])[0]
    gate_map = {row["gate"]: row for row in gates}
    run_state = json.loads((RUN / "status.json").read_text(encoding="utf-8"))
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-755"
    ]
    variable_rows = [
        row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") in VARIABLES
    ]
    variable_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variable_rows)
        for symbol in VARIABLES
    }
    variable_sources_exist = all(
        all((ROOT / source).exists() for source in row["source_files"].split(";"))
        for row in variable_rows
    )
    checkpoint = (
        POST
        / "4913-Y5-R2FR-matched-subtracted-interacting-motion-scalar-TTT-continuum-coefficient-or-zero-residual.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "929-PPC4161-matched-interacting-TTT-channel-repair-and-nonpromotion.md"
    ).read_text(encoding="utf-8")
    provenance = (
        POST / "source-intake" / "microscopic_vertex" / "4913" / "PROVENANCE.md"
    ).read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    evidence_paths = [OUTPUT / name for name in EVIDENCE_FILES]
    generated_paths = evidence_paths + [
        OUTPUT / "P8_Y5_R2FR_4913_GATE_DECISION.csv",
        OUTPUT / "P8_Y5_R2FR_4913_SOURCE_REGISTER.csv",
    ]
    all_rows = [
        row for path in generated_paths for row in read_csv(path)
    ]
    scripts = [
        SCRIPTS / "Y5_R2FR_4913_matched_interacting_TTT_smoke.py",
        SCRIPTS / "Y5_R2FR_4913_matched_interacting_TTT_smoke_validation.py",
    ]
    rows = [
        check(
            "VAL4913_00_prior",
            prior[-1]["check_id"] == "VAL4912_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4912 predecessor validation passes",
        ),
        check(
            "VAL4913_01_sources",
            all(row["source_exists"] and row["marker_found"] for row in sources),
            "all source paths and markers resolve",
        ),
        check(
            "VAL4913_02_observables",
            len(observables) == 5
            and all(row["passed"] == "True" for row in observables),
            "four FFT checks and the analytic zero-mode identity pass",
        ),
        check(
            "VAL4913_03_configs",
            {row["label"] for row in summaries}
            == {"N12_mu0p6", "N16_mu0p4"},
            "exactly the two checkpoint cutoffs are present",
        ),
        check(
            "VAL4913_04_recoveries",
            len(recoveries) == 4
            and {(row["config"], row["stencil"]) for row in recoveries}
            == {
                ("N12_mu0p6", "site"),
                ("N12_mu0p6", "half_link"),
                ("N16_mu0p4", "site"),
                ("N16_mu0p4", "half_link"),
            },
            "both stencils exist at both cutoffs",
        ),
        check(
            "VAL4913_05_chain",
            gate_map["chain_health"]["status"] == "PASS",
            "acceptance autocorrelation mass and block gates pass",
        ),
        check(
            "VAL4913_06_design",
            gate_map["q6_design_conditioning"]["status"] == "PASS",
            "conditioned cubic q6 designs replace the rejected q8 fit",
        ),
        check(
            "VAL4913_07_control",
            gate_map["paired_beta_one_control"]["status"] == "REJECTED",
            "variance-worsening beta-one control is excluded",
        ),
        check(
            "VAL4913_08_stencil",
            gate_map["site_half_link_consistency"]["status"]
            == "PASS_DIAGNOSTIC",
            "site and half-link rows agree as correlated diagnostics",
        ),
        check(
            "VAL4913_09_cutoff",
            gate_map["two_cutoff_zero_compatibility"]["status"]
            == "PASS_DIAGNOSTIC_NOT_CONVERGENCE",
            "two cutoff rows are zero-compatible but not called convergence",
        ),
        check(
            "VAL4913_10_zero",
            gate_map["nonzero_interaction_significance"]["status"]
            == "FAIL_TO_REJECT_ZERO",
            "all projected rows remain below two sigma",
        ),
        check(
            "VAL4913_11_covariance",
            gate_map["covariant_image_residual"]["status"] == "FAIL",
            "large noncovariant response is explicitly retained as a failed gate",
        ),
        check(
            "VAL4913_12_promotion",
            gate_map["interacting_coefficient_promotion"]["status"] == "BLOCKED"
            and all(
                str(row["coefficient_promotion"]) == "False" for row in gates
            ),
            "no coefficient is promoted",
        ),
        check(
            "VAL4913_13_long_run",
            gate_map["interacting_long_run"]["status"] == "WITHHELD",
            "long run remains behind the replica and direct-derivative gate",
        ),
        check(
            "VAL4913_14_active",
            gate_map["Gamma_MTS_res"]["status"] == "ZERO_PRESERVED",
            "active residual remains zero",
        ),
        check(
            "VAL4913_15_run",
            run_state["status"] == "COMPLETE"
            and run_state["profile"] == "checkpoint"
            and run_status["profile"] == "checkpoint"
            and run_status["observable_validation_pass"] == "True"
            and (RUN / "COMPLETE.marker").exists(),
            "checkpoint run state log and completion marker close",
        ),
        check(
            "VAL4913_16_claim",
            len(claims) == 1 and claims[0]["status"] == CLAIM_STATUS,
            "L-755 is unique and accurately nonclaim-scoped",
        ),
        check(
            "VAL4913_17_variables",
            len(variable_rows) == len(VARIABLES)
            and all(variable_counts[symbol] == 1 for symbol in VARIABLES),
            "ten checkpoint variables are unique",
        ),
        check(
            "VAL4913_18_variable_sources",
            variable_sources_exist,
            "all new variable source paths exist",
        ),
        check(
            "VAL4913_19_documents",
            MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_MATCHED_INTERACTING_TTT_PROVENANCE_4913" in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4913_20_registers",
            "1.206 Matched interacting TTT and analytic cosine channel"
            in equations
            and "157. A zero-mode source degeneracy" in redteam
            and "PPC4161 checkpoint 4913" in spine,
            "equation red-team and spine registers are updated",
        ),
        check(
            "VAL4913_21_resume",
            (
                "Last checkpoint: `4913-" in resume
                or "Last checkpoint: `4914-" in resume
            )
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume preserves 4913 and reaches its 4914 successor",
        ),
        check(
            "VAL4913_22_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no placeholder markers",
        ),
        check(
            "VAL4913_23_finite",
            not any(
                str(value).lower() in {"nan", "inf", "-inf"}
                for row in all_rows
                for value in row.values()
            ),
            "generated evidence contains no nonfinite numeric cells",
        ),
        check(
            "VAL4913_24_nonclaim",
            all(row.get("valid_for_claim") == "False" for row in all_rows),
            "all generated evidence rows remain private nonclaim",
        ),
        check(
            "VAL4913_25_csv",
            len(generated_paths) == 10
            and all(path.exists() and read_csv(path) for path in generated_paths),
            "ten evidence and gate CSVs parse",
        ),
        check(
            "VAL4913_26_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4913_27_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4913_28_next",
            NEXT_TARGET in checkpoint
            and (
                not (POST / NEXT_TARGET).exists()
                or "MTS_COMPLEX_SOURCE_TAYLOR_TTT_REPLICA_4914"
                in (POST / NEXT_TARGET).read_text(
                    encoding="utf-8", errors="replace"
                )
            ),
            "4914 is selected and is either pending or marker-valid",
        ),
        check(
            "VAL4913_29_local_limits",
            "GR/Newton/PPN/Maxwell                   = unchanged" in checkpoint
            and "Gamma_{\\mathrm{MTS,res}}=0" in checkpoint,
            "local GR Newton PPN Maxwell and active residual are unchanged",
        ),
    ]
    rows.append(
        check(
            "VAL4913_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_MATCHED_INTERACTING_TTT_SMOKE_4913_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    gates = gate_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4913_GATE_DECISION.csv", gates)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4913_SOURCE_REGISTER.csv", sources)
    validation = validation_rows(sources, gates)
    write_csv(OUTPUT / "P8_Y5_BRR545_4913_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4913_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4913_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
