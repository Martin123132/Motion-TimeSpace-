from __future__ import annotations

import csv
import math
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4800"
CLAIM_ID = "L-642"
MARKER = "PPC4161_LOCAL_RESIDUAL_BOUND_TO_PPN_R10_CLOCK_OR_PARENT_BC_ACTION_SOURCE_ROWS_4800"
PACKET_MARKER = "PPC4161_PACKET_LOCAL_RESIDUAL_BOUND_TO_PPN_R10_CLOCK_OR_PARENT_BC_ACTION_SOURCE_ROWS_4800"
DECISION = "LOCAL_RESIDUAL_TO_TEST_ARENA_GATE_INSTALLED_REQUIRED_TAU_COMPUTED_NONCLAIM"
NEXT_TARGET = "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md"

DOC_PATH = POST / "4800-Y5-R2FR-local-residual-bound-to-PPN-R10-clock-or-parent-BC-action-source-rows.md"
FORMAL_PATH = FORMAL / "816-PPC4161-local-residual-bound-to-PPN-R10-clock-or-parent-BC-action-source-rows.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "local_residual_to_test_rows_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4800_SOURCE_REGISTER.csv"
ARENA_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4800_ARENA_PROJECTION_INPUT.csv"
ARENA_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4800_ARENA_PROJECTION_OUTPUT.csv"
TAU_REQUIREMENTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4800_TAU_REQUIREMENTS.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4800_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4800_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4800_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4800_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4800_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4800_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4800_VALIDATION.csv"

LOCAL_RESIDUAL_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4799_LOCAL_RESIDUAL_ROLLUP_OUTPUT.csv"

ARENA_CLAUSES = (
    "residual_source_signed",
    "arena_projection_signed",
    "observable_mapping_signed",
    "units_signed",
    "bound_source_signed",
    "parent_BC_source_signed",
    "no_cancellation_signed",
)

SOURCE_SPECS = [
    {
        "source_id": "SRC4800_00_4799_doc",
        "source_type": "local",
        "source_path": str(POST / "4799-Y5-R2FR-BC-primitive-owner-or-source-selector-parent-action.md"),
        "needle": "4.96e-7",
        "source_url": "",
        "role": "4799 local residual rollup handoff",
    },
    {
        "source_id": "SRC4800_01_4799_rollup",
        "source_type": "local",
        "source_path": str(LOCAL_RESIDUAL_SOURCE),
        "needle": "local_residual_rollup_from_4798_smoke",
        "source_url": "",
        "role": "machine-readable local residual bound",
    },
    {
        "source_id": "SRC4800_02_Cassini_gamma",
        "source_type": "web",
        "source_path": "",
        "needle": "gamma = 1 + (2.1 +/- 2.3) x 10(-5)",
        "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
        "role": "PPN gamma anchor from Cassini radio science",
    },
    {
        "source_id": "SRC4800_03_EotWash_R10",
        "source_type": "web",
        "source_path": "",
        "needle": "gravitational-strength Yukawa interactions to ranges < 38.6 micrometers",
        "source_url": "https://arxiv.org/abs/2002.11761",
        "role": "R10/Yukawa gravitational-strength anchor",
    },
    {
        "source_id": "SRC4800_04_Galileo_redshift",
        "source_type": "web",
        "source_path": "",
        "needle": "(+0.19 +/- 2.48) x 10^-5",
        "source_url": "https://arxiv.org/abs/1906.06161",
        "role": "clock/redshift local-position-invariance anchor",
    },
    {
        "source_id": "SRC4800_05_Mercury_MESSENGER",
        "source_type": "web",
        "source_path": "",
        "needle": "575.3100 +/- 0.0015 arcsec per century",
        "source_url": "https://www.osti.gov/biblio/22863119",
        "role": "orbital Mercury precession and beta/gamma anchor",
    },
    {
        "source_id": "SRC4800_06_runner",
        "source_type": "local",
        "source_path": str(RUNNER),
        "needle": "def arena_projection_row",
        "source_url": "",
        "role": "4800 executable runner",
    },
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


ARENA_CLAUSES = (
    "residual_source_signed",
    "arena_projection_signed",
    "observable_mapping_signed",
    "units_signed",
    "bound_source_signed",
    "parent_BC_source_signed",
    "no_cancellation_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "HAND_SWITCH",
    "LOCAL_FLRW_HAND_SWITCH",
    "BOUND_BY_DESIRE",
    "BOUND_ZERO_BY_ASSERTION",
    "OBSERVED_RESIDUAL_CANCEL",
    "EDGE_CANCELLATION",
    "POSTFIT_REFERENCE",
    "RETUNE_TO_PASS",
    "USE_BOUND_AS_SOURCE_COUPLING",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed"}


def missing_text(value: Any) -> bool:
    text = str(value or "").strip()
    return not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE", "NOT_COMPUTED"}


def parse_float(value: Any) -> float | None:
    if missing_text(value):
        return None
    try:
        number = float(str(value).strip())
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in (
            "arena_id",
            "source_id",
            "source_url",
            "source_title",
            "projection_source",
            "notes",
            "provenance",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in ARENA_CLAUSES if not bool_text(row.get(clause))]


def arena_projection_row(row: dict[str, Any]) -> dict[str, Any]:
    arena_id = str(row.get("arena_id", "")).strip() or "UNNAMED_ARENA"
    output: dict[str, Any] = {
        "arena_id": arena_id,
        "sector": row.get("sector", ""),
        "observable": row.get("observable", ""),
        "source_id": row.get("source_id", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "epsilon_local_abs": "MISSING_NUMERIC_VALUE",
                "observable_bound_abs": "MISSING_NUMERIC_VALUE",
                "tau_projection_abs": "MISSING_NUMERIC_VALUE",
                "tau_required_max_abs": "MISSING_NUMERIC_VALUE",
                "predicted_observable_abs": "MISSING_NUMERIC_VALUE",
                "numeric_bound_pass": False,
                "runner_status": "FAILED_ARENA_PROJECTION_GATE",
                "missing_arena_inputs": "FORBIDDEN_ARENA_PROJECTION_OR_CANCELLATION_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    epsilon = parse_float(row.get("epsilon_local_abs"))
    bound = parse_float(row.get("observable_bound_abs"))
    tau = parse_float(row.get("tau_projection_abs"))
    missing: list[str] = missing_clauses(row)
    if epsilon is None or epsilon < 0.0:
        missing.append("MISSING_epsilon_local_abs")
    if bound is None or bound < 0.0:
        missing.append("MISSING_observable_bound_abs")

    if epsilon is None or bound is None or epsilon < 0.0 or bound < 0.0:
        output.update(
            {
                "epsilon_local_abs": format_float(epsilon),
                "observable_bound_abs": format_float(bound),
                "tau_projection_abs": "MISSING_NUMERIC_VALUE",
                "tau_required_max_abs": "MISSING_NUMERIC_VALUE",
                "predicted_observable_abs": "MISSING_NUMERIC_VALUE",
                "numeric_bound_pass": False,
                "runner_status": "BLOCKED_MISSING_BOUND_OR_RESIDUAL_INPUTS",
                "missing_arena_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if epsilon <= 1.0e-30:
        predicted = 0.0 if tau is None else abs(tau) * epsilon
        output.update(
            {
                "epsilon_local_abs": format_float(epsilon),
                "observable_bound_abs": format_float(bound),
                "tau_projection_abs": format_float(tau),
                "tau_required_max_abs": "INFINITE_ZERO_RESIDUAL",
                "predicted_observable_abs": format_float(predicted),
                "numeric_bound_pass": predicted <= bound,
                "runner_status": "ZERO_RESIDUAL_CONDITIONAL_PARENT_THEOREM_NONCLAIM",
                "missing_arena_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    tau_required = bound / epsilon
    if tau is None:
        output.update(
            {
                "epsilon_local_abs": format_float(epsilon),
                "observable_bound_abs": format_float(bound),
                "tau_projection_abs": "MISSING_NUMERIC_VALUE",
                "tau_required_max_abs": format_float(tau_required),
                "predicted_observable_abs": "MISSING_NUMERIC_VALUE",
                "numeric_bound_pass": False,
                "runner_status": "REQUIRED_TAU_COMPUTED_PROJECTION_MISSING_NONCLAIM",
                "missing_arena_inputs": ";".join([*missing, "MISSING_tau_projection_abs"]),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    predicted = abs(tau) * epsilon
    numeric_pass = predicted <= bound
    if numeric_pass and missing:
        status = "NUMERIC_PASS_IF_GIVEN_TAU_BUT_PARENT_OR_MAPPING_UNSIGNED_NONCLAIM"
    elif numeric_pass:
        status = "NUMERIC_PASS_WITH_SIGNED_MAPPING_NONCLAIM_UNLESS_INPUT_VALID"
    else:
        status = "NUMERIC_FAIL_GIVEN_TAU"

    claim_allowed = bool_text(row.get("valid_for_claim")) and not missing and numeric_pass
    output.update(
        {
            "epsilon_local_abs": format_float(epsilon),
            "observable_bound_abs": format_float(bound),
            "tau_projection_abs": format_float(abs(tau)),
            "tau_required_max_abs": format_float(tau_required),
            "predicted_observable_abs": format_float(predicted),
            "numeric_bound_pass": numeric_pass,
            "runner_status": status,
            "missing_arena_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            "claim_allowed": claim_allowed,
        }
    )
    return output


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: local_residual_to_test_rows_runner.py <input.csv> <output.csv>", file=sys.stderr)
        return 2
    rows = [arena_projection_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace") if path_object.exists() else ""


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object)
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def parse_csv(path_object: Path) -> list[dict[str, str]]:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fields: list[str] | None = None) -> str:
    if not rows:
        return "\n"
    selected = fields or list(rows[0].keys())
    lines = [
        "| " + " | ".join(selected) + " |",
        "| " + " | ".join("---" for _ in selected) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in selected) + " |")
    return "\n".join(lines) + "\n"


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed"}


def format_float(value: float) -> str:
    return f"{value:.15e}"


def run_command(args: list[str]) -> None:
    subprocess.run(args, check=True, cwd=str(ROOT))


def local_residual_bound() -> float:
    rows = parse_csv(LOCAL_RESIDUAL_SOURCE)
    for row in rows:
        if row.get("rollup_id") == "local_residual_rollup_from_4798_smoke":
            return float(row["local_residual_bound_abs"])
    raise ValueError("missing local_residual_rollup_from_4798_smoke")


def clause_map(value: bool) -> dict[str, bool]:
    return {clause: value for clause in ARENA_CLAUSES}


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        source_type = spec["source_type"]
        path_text = spec["source_path"]
        path_object = Path(path_text) if path_text else None
        local_exists = path_object.exists() if path_object else False
        local_text = read_text(path_object) if path_object else ""
        web_present = bool(spec["source_url"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_type": source_type,
                "source_path": path_text,
                "source_url": spec["source_url"],
                "exists_or_url_present": local_exists if source_type == "local" else web_present,
                "needle": spec["needle"],
                "needle_found_for_local": (spec["needle"] in local_text) if source_type == "local" else "WEB_RECORDED_FROM_BROWSE",
                "role": spec["role"],
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def arena_input_rows(timestamp: str, epsilon: float) -> list[dict[str, Any]]:
    signed_source_only = clause_map(False)
    signed_source_only["residual_source_signed"] = True
    signed_source_only["bound_source_signed"] = True
    signed_source_only["units_signed"] = True
    signed_source_only["no_cancellation_signed"] = True

    unit_tau = dict(signed_source_only)
    unit_tau["arena_projection_signed"] = False
    unit_tau["observable_mapping_signed"] = False

    all_signed = clause_map(True)

    def row(
        arena_id: str,
        sector: str,
        observable: str,
        source_id: str,
        bound: float,
        bound_units: str,
        source_title: str,
        source_url: str,
        clauses: dict[str, bool],
        tau: float | str = "",
        epsilon_value: float | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "arena_id": arena_id,
            "sector": sector,
            "observable": observable,
            "epsilon_local_abs": format_float(epsilon if epsilon_value is None else epsilon_value),
            "observable_bound_abs": format_float(bound),
            "observable_bound_units": bound_units,
            "tau_projection_abs": tau,
            "source_id": source_id,
            "source_title": source_title,
            "source_url": source_url,
            "projection_source": "",
            "notes": notes,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        return payload

    cassini_title = "Bertotti, Iess, Tortora 2003 Cassini gamma: gamma-1 = (2.1 +/- 2.3)e-5"
    r10_title = "Lee et al. 2020 Eot-Wash: alpha=1 Yukawa excluded for lambda >= 38.6 micrometers"
    clock_title = "Delva et al. 2019 Galileo redshift: alpha_redshift = (+0.19 +/- 2.48)e-5"
    mercury_title = "Park et al. 2017 MESSENGER Mercury perihelion: beta-1 = (-2.7 +/- 3.9)e-5; total precession 575.3100 +/- 0.0015 arcsec/cy"

    mercury_fraction = 0.0015 / 575.3100

    rows = [
        row(
            "ppn_gamma_cassini_required_tau",
            "PPN",
            "abs(gamma-1)",
            "SRC4800_02_Cassini_gamma",
            2.3e-5,
            "dimensionless_1sigma_anchor",
            cassini_title,
            "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            signed_source_only,
            notes="required tau_PPN_gamma is computed; no claim until observer coframe/projection derives tau",
        ),
        row(
            "ppn_gamma_cassini_unit_tau_smoke",
            "PPN",
            "abs(gamma-1)",
            "SRC4800_02_Cassini_gamma",
            2.3e-5,
            "dimensionless_1sigma_anchor",
            cassini_title,
            "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            unit_tau,
            tau="1.0",
            notes="unit tau smoke: shows scale is not automatically fatal, but projection is unsigned",
        ),
        row(
            "ppn_beta_mercury_required_tau",
            "PPN",
            "abs(beta-1)",
            "SRC4800_05_Mercury_MESSENGER",
            3.9e-5,
            "dimensionless_1sigma_anchor",
            mercury_title,
            "https://www.osti.gov/biblio/22863119",
            signed_source_only,
            notes="Mercury beta anchor; source-action and beta mapping must be derived",
        ),
        row(
            "clock_redshift_galileo_required_tau",
            "clock",
            "abs(redshift_deviation_alpha)",
            "SRC4800_04_Galileo_redshift",
            2.48e-5,
            "dimensionless_1sigma_anchor",
            clock_title,
            "https://arxiv.org/abs/1906.06161",
            signed_source_only,
            notes="clock/readout mapping must distinguish observable proper-clock shift from internal process variables",
        ),
        row(
            "r10_yukawa_grav_strength_anchor_required_tau",
            "R10",
            "abs(alpha_Yukawa_at_lambda_38p6um)",
            "SRC4800_03_EotWash_R10",
            1.0,
            "dimensionless_95pct_gravity_strength_anchor",
            r10_title,
            "https://arxiv.org/abs/2002.11761",
            signed_source_only,
            notes="anchor only, not a digitized curve; full R10 claim still requires alpha(lambda) curve and MTS alpha projection",
        ),
        row(
            "orbital_mercury_total_precession_fraction_required_tau",
            "orbital",
            "fractional_total_precession_uncertainty",
            "SRC4800_05_Mercury_MESSENGER",
            mercury_fraction,
            "dimensionless_contextual_fraction",
            mercury_title,
            "https://www.osti.gov/biblio/22863119",
            signed_source_only,
            notes="contextual strict orbital fraction; not a direct MTS observable until orbital residual vector is derived",
        ),
        row(
            "conditional_parent_BC_no_flux_all_arenas",
            "all_local",
            "all_projected_local_residuals",
            "conditional_parent_BC_source_action",
            2.3e-5,
            "dimensionless_reference_bound",
            "conditional theorem row",
            "",
            all_signed,
            tau="1.0",
            epsilon_value=0.0,
            notes="if parent B_C/Phi_C no-flux and source/Ward theorem closes, projected local residual is zero",
        ),
        row(
            "forbidden_observed_cancellation_control",
            "control",
            "fake_pass_by_cancellation",
            "OBSERVED_RESIDUAL_CANCEL",
            2.3e-5,
            "dimensionless",
            "forbidden control",
            "OBSERVED_RESIDUAL_CANCEL",
            signed_source_only,
            tau="1.0",
            notes="must fail: no cancellation or post-fit bound-as-source coupling",
        ),
    ]
    return rows


def tau_requirement_rows(arena_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in arena_rows:
        if row.get("runner_status") in {
            "REQUIRED_TAU_COMPUTED_PROJECTION_MISSING_NONCLAIM",
            "NUMERIC_PASS_IF_GIVEN_TAU_BUT_PARENT_OR_MAPPING_UNSIGNED_NONCLAIM",
            "NUMERIC_PASS_WITH_SIGNED_MAPPING_NONCLAIM_UNLESS_INPUT_VALID",
            "NUMERIC_FAIL_GIVEN_TAU",
        }:
            rows.append(
                {
                    "requirement_id": f"TAU4800_{len(rows)}",
                    "arena_id": row["arena_id"],
                    "sector": row["sector"],
                    "observable": row["observable"],
                    "epsilon_local_abs": row["epsilon_local_abs"],
                    "observable_bound_abs": row["observable_bound_abs"],
                    "tau_required_max_abs": row["tau_required_max_abs"],
                    "tau_projection_abs": row["tau_projection_abs"],
                    "predicted_observable_abs": row["predicted_observable_abs"],
                    "numeric_bound_pass": row["numeric_bound_pass"],
                    "status": row["runner_status"],
                    "next_action": "derive_tau_from_observer_coframe_or_parent_BC_no_flux",
                    "valid_for_claim": False,
                }
            )
    return rows


def obstruction_rows(arena_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_id = {row["arena_id"]: row for row in arena_rows}
    return [
        {
            "update_id": "OBS4800_0_scale",
            "item": "current local residual scale",
            "status": "FINITE_RESIDUAL_READY_FOR_ARENA_MAPPING_NONCLAIM",
            "value_or_bound": by_id["ppn_gamma_cassini_required_tau"]["epsilon_local_abs"],
            "meaning": "the 4799 residual is now a number, not a fog bank",
        },
        {
            "update_id": "OBS4800_1_required_tau",
            "item": "PPN/clock/orbital tau window",
            "status": "O_1_TO_O_50_TAU_SURVIVES_ANCHORS_BUT_UNSIGNED",
            "value_or_bound": f"gamma_tau<={by_id['ppn_gamma_cassini_required_tau']['tau_required_max_abs']}; clock_tau<={by_id['clock_redshift_galileo_required_tau']['tau_required_max_abs']}; orbital_tau<={by_id['orbital_mercury_total_precession_fraction_required_tau']['tau_required_max_abs']}",
            "meaning": "unit-scale projection is not automatically fatal, but tau must be derived from the observer coframe/source map",
        },
        {
            "update_id": "OBS4800_2_R10",
            "item": "R10 alpha/lambda anchor",
            "status": "GRAVITY_STRENGTH_ANCHOR_EASY_FOR_CURRENT_SCALE_BUT_CURVE_AND_ALPHA_MAP_MISSING",
            "value_or_bound": by_id["r10_yukawa_grav_strength_anchor_required_tau"]["tau_required_max_abs"],
            "meaning": "R10 does not look like the tightest local blocker at this residual scale, but full curve and MTS alpha projection remain absent",
        },
    ]


def gate_rows(arena_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    all_claims_false = all(not bool_text(row.get("claim_allowed")) for row in arena_rows)
    unit_gamma = next(row for row in arena_rows if row["arena_id"] == "ppn_gamma_cassini_unit_tau_smoke")
    return [
        {
            "gate_id": "PG4800_0_required_tau",
            "claim": "required tau values are computable from 4799 residual and sourced anchors",
            "gate_pass": True,
            "reason": "epsilon_local and bound anchors are numeric; tau_required=bound/epsilon",
            "evidence": str(TAU_REQUIREMENTS_CSV),
        },
        {
            "gate_id": "PG4800_1_unit_tau_scale",
            "claim": "unit projection is not immediately excluded by the Cassini gamma anchor",
            "gate_pass": unit_gamma["numeric_bound_pass"] == "True",
            "reason": "4.96e-7 is below the 2.3e-5 Cassini gamma uncertainty anchor",
            "evidence": unit_gamma["predicted_observable_abs"],
        },
        {
            "gate_id": "PG4800_2_arena_projection",
            "claim": "MTS local residual has a derived observer-coframe projection into each arena",
            "gate_pass": False,
            "reason": "tau_PPN, tau_clock, tau_R10 and tau_orbital are required but not derived",
            "evidence": "arena_projection_signed=false on physical rows",
        },
        {
            "gate_id": "PG4800_3_local_claim",
            "claim": "local GR/Newton/PPN/R10/clock/orbital pass is allowed",
            "gate_pass": False,
            "reason": "all rows remain nonclaim until parent BC/source and arena projection are signed",
            "evidence": f"all_claims_false={all_claims_false}",
        },
    ]


def firewall_rows() -> list[dict[str, Any]]:
    return [
        {"firewall_id": "FW4800_0_no_bound_as_source", "rule": "An observational bound may compute a required tau but may not become the source coupling itself.", "status": "ACTIVE"},
        {"firewall_id": "FW4800_1_no_unit_tau_claim", "rule": "tau=1 smoke rows are scale checks only; they do not prove the observer/coframe projection.", "status": "ACTIVE"},
        {"firewall_id": "FW4800_2_no_anchor_curve_claim", "rule": "R10 alpha=1 at 38.6 micrometers is an anchor, not a digitized alpha(lambda) curve.", "status": "ACTIVE"},
        {"firewall_id": "FW4800_3_no_clock_confusion", "rule": "Clock observables must be proper readout shifts; internal process/traversal variables cannot be compared directly.", "status": "ACTIVE"},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4800_0_scale",
            "decision": "current_residual_scale_is_not_immediately_fatal_for_O1_projection",
            "reason": "unit tau smoke is below the PPN gamma, clock, R10 and strict Mercury total-precession anchors used here",
            "next_action": "derive tau projection instead of inventing more residual ledgers",
        },
        {
            "decision_id": "DEC4800_1_hard_gap",
            "decision": "observer_coframe_tau_projection_is_the_next_hard_gap",
            "reason": "bounds now ask for tau_PPN, tau_clock, tau_R10 and tau_orbital rather than another abstract missing source",
            "next_action": NEXT_TARGET,
        },
    ]


def status_rows(arena_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_id = {row["arena_id"]: row for row in arena_rows}
    return [
        {"status_id": "STATUS4800_0_gamma", "status": by_id["ppn_gamma_cassini_required_tau"]["runner_status"], "detail": f"tau_required={by_id['ppn_gamma_cassini_required_tau']['tau_required_max_abs']}"},
        {"status_id": "STATUS4800_1_clock", "status": by_id["clock_redshift_galileo_required_tau"]["runner_status"], "detail": f"tau_required={by_id['clock_redshift_galileo_required_tau']['tau_required_max_abs']}"},
        {"status_id": "STATUS4800_2_R10", "status": by_id["r10_yukawa_grav_strength_anchor_required_tau"]["runner_status"], "detail": f"tau_required={by_id['r10_yukawa_grav_strength_anchor_required_tau']['tau_required_max_abs']}"},
        {"status_id": "STATUS4800_3_selected_next", "status": "OBSERVER_COFRAME_TAU_PROJECTION_OR_PARENT_BC_NO_FLUX", "detail": NEXT_TARGET},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT4800_0_4801",
            "next_target": NEXT_TARGET,
            "trigger": "4800 computed required tau windows but physical arena projections remain unsigned",
            "required_inputs": "observer coframe, clock/readout map, R10 alpha projection, orbital residual vector, parent B_C no-flux/source theorem",
            "valid_for_claim": False,
        }
    ]


def validation_rows(sources: list[dict[str, Any]], arena_rows: list[dict[str, str]], tau_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row["arena_id"]: row for row in arena_rows}
    local_sources_ok = all(
        bool_text(row["exists_or_url_present"])
        and (bool_text(row["needle_found_for_local"]) or row["needle_found_for_local"] == "WEB_RECORDED_FROM_BROWSE")
        for row in sources
    )
    checks: list[tuple[str, str, bool, str]] = [
        ("VAL4800_0_sources", "all local sources exist and web source strings are recorded", local_sources_ok, str(SOURCE_REGISTER_CSV)),
        ("VAL4800_1_epsilon", "4799 residual epsilon is carried as 4.96e-7", by_id["ppn_gamma_cassini_required_tau"]["epsilon_local_abs"] == "4.960000000000000e-07", str(ARENA_OUTPUT_CSV)),
        ("VAL4800_2_gamma_tau", "Cassini gamma required tau computes", by_id["ppn_gamma_cassini_required_tau"]["tau_required_max_abs"] == "4.637096774193549e+01", str(ARENA_OUTPUT_CSV)),
        ("VAL4800_3_clock_tau", "Galileo redshift required tau computes", by_id["clock_redshift_galileo_required_tau"]["tau_required_max_abs"] == "5.000000000000000e+01", str(ARENA_OUTPUT_CSV)),
        ("VAL4800_4_R10_tau", "R10 gravitational-strength anchor required tau computes", by_id["r10_yukawa_grav_strength_anchor_required_tau"]["tau_required_max_abs"] == "2.016129032258064e+06", str(ARENA_OUTPUT_CSV)),
        ("VAL4800_5_unit_tau_nonclaim", "unit tau smoke numerically passes but remains nonclaim", by_id["ppn_gamma_cassini_unit_tau_smoke"]["numeric_bound_pass"] == "True" and by_id["ppn_gamma_cassini_unit_tau_smoke"]["claim_allowed"] == "False", str(ARENA_OUTPUT_CSV)),
        ("VAL4800_6_forbidden_fails", "observed cancellation control fails", by_id["forbidden_observed_cancellation_control"]["runner_status"] == "FAILED_ARENA_PROJECTION_GATE", str(ARENA_OUTPUT_CSV)),
        ("VAL4800_7_tau_rows", "tau requirement table is populated", len(tau_rows) >= 6, str(TAU_REQUIREMENTS_CSV)),
        ("VAL4800_8_claim", "claim register includes L-642 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH) and MARKER in read_text(CLAIMS_PATH), str(CLAIMS_PATH)),
        ("VAL4800_9_resume", "resume points at 4801", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)),
    ]
    rows = [
        {
            "check_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "evidence": evidence,
        }
        for check_id, description, passed, evidence in checks
    ]
    rows.append(
        {
            "check_id": "VAL4800_OVERALL",
            "description": "all 4800 local residual to arena projection checks pass",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "evidence": DECISION,
        }
    )
    return rows


def write_documents(
    timestamp: str,
    epsilon: float,
    sources: list[dict[str, Any]],
    arena_rows: list[dict[str, str]],
    tau_rows: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    firewalls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    content = f"""# 4800 - Local residual bound to PPN/R10/clock or parent BC action source rows

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4800 pushes the 4799 local residual into actual local-test arenas.

The key number remains:

```text
epsilon_loc = {epsilon:.3e}
```

For each local test arena, this checkpoint computes:

```text
predicted_observable = |tau_arena| epsilon_loc
tau_required_max = observable_bound / epsilon_loc
```

This is not yet a claim, because `tau_arena` must be derived from the observer coframe, clock/readout map, R10 Yukawa projection, or orbital residual vector.

## Main Takeaway

The current residual scale is not obviously fatal. A unit-scale projection is below the sourced PPN-gamma, clock-redshift, R10 gravitational-strength anchor, and strict Mercury total-precession-fraction anchors used here.

That does **not** mean MTS passes local tests. It means the next real mathematical job is sharper:

```text
derive tau_PPN, tau_clock, tau_R10, tau_orbital
```

or replace the whole finite-residual branch with a parent `B_C/Phi_C` no-flux/source-action theorem.

## Source Register

{markdown_table(sources, ["source_id", "source_type", "source_path", "source_url", "exists_or_url_present", "needle_found_for_local", "role"])}

## Arena Projection Output

{markdown_table(arena_rows, ["arena_id", "sector", "observable", "epsilon_local_abs", "observable_bound_abs", "tau_projection_abs", "tau_required_max_abs", "predicted_observable_abs", "numeric_bound_pass", "runner_status", "missing_arena_inputs", "anti_circularity_status"])}

## Tau Requirements

{markdown_table(tau_rows, ["arena_id", "sector", "observable", "tau_required_max_abs", "tau_projection_abs", "numeric_bound_pass", "status", "next_action"])}

## Obstruction Update

{markdown_table(obstructions)}

## Promotion Gates

{markdown_table(gates)}

## Firewalls

{markdown_table(firewalls)}

## Decision Ledger

{markdown_table(decisions)}

## Status

{markdown_table(statuses)}

## Validation

{markdown_table(validations)}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)

    formal_content = f"""# 816 - PPC4161 local residual bound to local-test arena rows

Marker: `{MARKER}`
Generated: `{timestamp}`

## Formal Update

4800 converts the 4799 local residual into required arena projection factors:

```text
predicted_observable_X = |tau_X| epsilon_loc
tau_X <= bound_X / epsilon_loc
epsilon_loc = {epsilon:.3e}
```

This does not prove local GR. It proves a narrower and more useful fact: the finite residual is now small enough that the local bridge lives or dies on deriving the observer-coframe/source projection factors, not on hand-waving about whether a residual exists.

See `{DOC_PATH}`.
"""
    write_text(FORMAL_PATH, formal_content)


def update_registers(timestamp: str) -> None:
    claim_line = (
        f'{CLAIM_ID},local_residual_to_test_rows_runner,'
        f'"4800 maps the 4799 finite local residual into PPN/R10/clock/orbital arena rows and computes required tau projection windows without claiming a pass.",'
        f'"Generated source register, arena projection input/output, tau requirements, obstruction update, gates, firewalls, decision, status, next target and validation.",'
        f'local_residual_to_arena_projection_private_nonclaim_required_tau_ready,'
        f'{NEXT_TARGET},'
        f'"Do not treat unit tau smoke rows, observational bounds, or R10 anchors as derived source couplings or local-GR evidence.",'
        f'local_gr,{DOC_PATH},{NEXT_TARGET},'
        f'unit tau claim; bound-as-source coupling; R10 anchor as full curve; clock/process confusion; observed cancellation,'
        f'"Local residual arena projection gate",'
        f'{MARKER}; {DECISION}; generated {timestamp}\n'
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            handle.write(claim_line)

    spine_block = f"""
## {MARKER}

4800 projects the finite local residual into local-test arena requirements:

```text
epsilon_loc = 4.96e-7
tau_required_X = bound_X / epsilon_loc
```

The important update is that the current residual scale is not automatically fatal for unit-order projection. The next hard derivation is the observer-coframe/source map that fixes `tau_PPN`, `tau_clock`, `tau_R10`, and `tau_orbital`, or a parent `B_C/Phi_C` no-flux theorem that sets `epsilon_loc=0`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""
## {PACKET_MARKER}

- Checkpoint: `{DOC_PATH}`
- Formal note: `{FORMAL_PATH}`
- Runner: `{RUNNER}`
- Claim row: `{CLAIM_ID}`
- Decision: `{DECISION}`
- Next: `{NEXT_TARGET}`
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4800-Y5-R2FR-local-residual-bound-to-PPN-R10-clock-or-parent-BC-action-source-rows.md`
Marker: `{MARKER}`

## Where we are

4800 mapped the 4799 finite local residual into sourced local-test anchors:

```text
epsilon_loc = 4.96e-7
predicted_observable_X = |tau_X| epsilon_loc
tau_required_X = bound_X / epsilon_loc
```

The scale result is encouraging but still nonclaim: unit-order projection is not immediately excluded by the anchors used here, but `tau_PPN`, `tau_clock`, `tau_R10`, and `tau_orbital` are not derived.

## Live blockers

- Derive observer-coframe/source projection factors instead of assuming `tau=1`.
- Keep clock observables distinct from internal process/traversal variables.
- Replace the finite residual branch with parent `B_C/Phi_C` no-flux and source-action theorem if possible.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, resume)


def main() -> int:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    write_text(RUNNER, RUNNER_TEXT)

    epsilon = local_residual_bound()
    sources = source_register(timestamp)
    arena_inputs = arena_input_rows(timestamp, epsilon)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(ARENA_INPUT_CSV, arena_inputs)

    python = sys.executable
    run_command([python, str(RUNNER), str(ARENA_INPUT_CSV), str(ARENA_OUTPUT_CSV)])

    arena_rows = parse_csv(ARENA_OUTPUT_CSV)
    tau_rows = tau_requirement_rows(arena_rows)
    obstructions = obstruction_rows(arena_rows)
    gates = gate_rows(arena_rows)
    firewalls = firewall_rows()
    decisions = decision_rows()
    statuses = status_rows(arena_rows)
    next_targets = next_target_rows()

    write_csv(TAU_REQUIREMENTS_CSV, tau_rows)
    write_csv(OBSTRUCTION_CSV, obstructions)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    update_registers(timestamp)
    validations = validation_rows(sources, arena_rows, tau_rows)
    write_csv(VALIDATION_CSV, validations)
    write_documents(timestamp, epsilon, sources, arena_rows, tau_rows, obstructions, gates, firewalls, decisions, statuses, validations)

    run_command([python, "-m", "py_compile", str(RUNNER), str(Path(__file__))])
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    if any(row["result"] != "PASS" for row in validations):
        print(f"{CHECKPOINT} validation failed: {VALIDATION_CSV}", file=sys.stderr)
        return 1
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
