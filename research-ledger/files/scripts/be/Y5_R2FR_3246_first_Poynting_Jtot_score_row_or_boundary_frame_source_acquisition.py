from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3246"
DOC = ROOT / "3246-Y5-R2FR-first-Poynting-Jtot-score-row-or-boundary-frame-source-acquisition-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3246_SOURCE_REGISTER.csv",
    "score": OUT / "P8_Y5_R2FR_3246_FIRST_POYNTING_JTOT_SCORE_ROW_NONCLAIM.csv",
    "acquisition": OUT / "P8_Y5_R2FR_3246_BOUNDARY_FRAME_FLUX_ACQUISITION_LEDGER.csv",
    "regime": OUT / "P8_Y5_R2FR_3246_POYNTING_REGIME_ZERO_OR_BOUND_CLASSIFIER.csv",
    "dry_run": OUT / "P8_Y5_R2FR_3246_SCORE_ROW_DRY_RUN.csv",
    "transfer": OUT / "P8_Y5_R2FR_3246_JTOT_AMPLITUDE_TRANSFER_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3246_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3246_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3246_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3246_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


REQUIRED_SCORE_FIELDS = [
    "score_id",
    "component_id",
    "boundary_id",
    "surface_class",
    "field_regime",
    "frame_u",
    "normal_n",
    "C_flux",
    "C_coll",
    "S_normal_norm_B",
    "T_EM_un_norm_collar",
    "eA_norm_B",
    "eA_norm_collar",
    "B_corner_flux",
    "units",
    "source_path",
    "computed_J_Poynting_bound",
    "zero_certificate",
    "status",
    "valid_for_claim",
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            low = line.lower()
            if any(needle in low for needle in lowered):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:220]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3246_3245",
            ROOT / "3245-Y5-R2FR-MAB-coercivity-and-first-Jtot-component-bound-under-AX1090.md",
            "immediate handoff: first Poynting Jtot component",
            ["Poynting", "JTC3245_0_selected", "C_flux_C_coll", "NEXT3245"],
        ),
        (
            "SRC3246_3234_doc",
            ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
            "finite Poynting flux derivation",
            ["Phi_Poynting", "T_EM(u,n)", "C_flux", "C_coll"],
        ),
        (
            "SRC3246_3234_functional",
            OUT / "P8_Y5_R2FR_3234_POYNTING_FLUX_FUNCTIONAL.csv",
            "machine Poynting functional rows",
            ["PF3234_0_functional", "T_EM(u,n)", "C_flux", "NO_F2_SHORTCUT_ACTIVE"],
        ),
        (
            "SRC3246_3234_bound",
            OUT / "P8_Y5_R2FR_3234_FINITE_FLUX_BOUND.csv",
            "machine finite flux bound rows",
            ["PB3234_0_boundary_flux", "PB3234_1_collar_source", "C_flux", "C_coll"],
        ),
        (
            "SRC3246_3200_schema",
            OUT / "P8_Y5_R2FR_3200_POYNTING_BOUND_RUNNER_SCHEMA.csv",
            "older runner schema for Poynting residual rows",
            ["PBR3200_00", "S_normal_bound", "tau_EM", "valid_for_claim"],
        ),
        (
            "SRC3246_3200_cases",
            OUT / "P8_Y5_R2FR_3200_POYNTING_ZERO_OR_BOUND_THEOREM.csv",
            "quiet/static/radiative regime classifier",
            ["quiet_static", "finite_bound_route", "radiative", "valid_for_claim"],
        ),
        (
            "SRC3246_3142_stress",
            OUT / "P8_Y5_R2FR_3142_POYNTING_STRESS_READOUT.csv",
            "conditional EM stress and Poynting readout",
            ["T_EM", "Poynting flux", "observed tetrad", "valid_for_claim"],
        ),
        (
            "SRC3246_3199_descent",
            OUT / "P8_Y5_R2FR_3199_POYNTING_MAXWELL_DESCENT_AUDIT.csv",
            "Maxwell descent/open gate guard",
            ["standard_or_parent_derived_T_EM", "tau_EM", "valid_for_claim"],
        ),
        (
            "SRC3246_3222_guards",
            OUT / "P8_Y5_R2FR_3222_STRESS_POYNTING_AND_READOUT_GUARDS.csv",
            "stress/readout guards",
            ["null_wave_guard", "current_normalization", "local_GR_boundary"],
        ),
        (
            "SRC3246_3232_audit",
            OUT / "P8_Y5_R2FR_3232_POYNTING_FLUX_ZERO_OR_BOUND_AUDIT.csv",
            "Poynting zero-or-bound audit",
            ["PY3232_0_definition", "F2 versus stress", "SUPPORT_ROUTE_NOT_SOURCE_SIGNED"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def score_rows() -> list[dict[str, Any]]:
    return [
        {
            "score_id": "PJS3246_0_first_component",
            "component_id": "JTC3245_0_selected",
            "boundary_id": "MISSING_PARENT_BOUNDARY_ID",
            "surface_class": "MISSING_BOUNDARY_COLLAR_WORLDTUBE_CLASS",
            "field_regime": "UNCLASSIFIED_REQUIRES_QUIET_STATIC_OR_FINITE_FLUX",
            "frame_u": "MISSING_OBSERVED_FRAME_U",
            "normal_n": "MISSING_BOUNDARY_NORMAL_N",
            "C_flux": "MISSING_C_FLUX",
            "C_coll": "MISSING_C_COLL",
            "S_normal_norm_B": "MISSING_NORM_S_EM_DOT_N_ON_B",
            "T_EM_un_norm_collar": "MISSING_NORM_T_EM_U_N_ON_COLLAR",
            "eA_norm_B": "MISSING_RESPONSE_BASIS_NORM_ON_B",
            "eA_norm_collar": "MISSING_RESPONSE_BASIS_NORM_ON_COLLAR",
            "B_corner_flux": "MISSING_CORNER_WORLDTUBE_REMAINDER",
            "units": "MISSING_COMMON_JTOT_UNITS",
            "source_path": "MISSING_SOURCE_PATH_FOR_NUMERIC_INPUTS",
            "computed_J_Poynting_bound": "NOT_COMPUTED_MISSING_INPUTS",
            "zero_certificate": "false",
            "status": "FILLABLE_SCORE_ROW_NONCLAIM",
            "valid_for_claim": "false",
        }
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "acq_id": "ACQ3246_0_boundary",
            "field": "boundary_id;surface_class",
            "needed_input": "parent-owned local boundary/collar/worldtube label and support class",
            "derivation_or_source_route": "derive from local test-domain definition or source from existing local arena runner",
            "claim_if_missing": "cannot choose the boundary after seeing flux",
            "priority": 1,
        },
        {
            "acq_id": "ACQ3246_1_frame",
            "field": "frame_u;normal_n",
            "needed_input": "observed tetrad/frame u and outward normal n",
            "derivation_or_source_route": "derive from observed coframe/public metric branch; must match T_EM readout",
            "claim_if_missing": "Poynting flux is frame/surface ambiguous",
            "priority": 2,
        },
        {
            "acq_id": "ACQ3246_2_flux_constants",
            "field": "C_flux;C_coll",
            "needed_input": "operator constants mapping boundary/collar flux norms into Jtot units",
            "derivation_or_source_route": "dual norm of response test function and collar embedding constant",
            "claim_if_missing": "no numerical Jtot component can be computed",
            "priority": 3,
        },
        {
            "acq_id": "ACQ3246_3_flux_norms",
            "field": "S_normal_norm_B;T_EM_un_norm_collar",
            "needed_input": "EM stress flux norms on the selected boundary/collar",
            "derivation_or_source_route": "quiet-static zero certificate, measured/source-backed EM field bounds, or finite arena model",
            "claim_if_missing": "component remains formula-only",
            "priority": 4,
        },
        {
            "acq_id": "ACQ3246_4_response_norm",
            "field": "eA_norm_B;eA_norm_collar",
            "needed_input": "response basis norm under the same Z normalization used by M_AB",
            "derivation_or_source_route": "M_AB/Z basis owner ledger and boundary trace inequality",
            "claim_if_missing": "cannot connect flux to response amplitude denominator",
            "priority": 5,
        },
        {
            "acq_id": "ACQ3246_5_units",
            "field": "units;source_path",
            "needed_input": "common action-density/Jtot units and source provenance",
            "derivation_or_source_route": "same unit convention as 3244/3245 amplitude transfer",
            "claim_if_missing": "row cannot be valid_for_claim",
            "priority": 6,
        },
    ]


def regime_rows() -> list[dict[str, Any]]:
    return [
        {
            "regime_id": "REG3246_0_quiet_static",
            "field_regime": "quiet_static_no_radiation_no_normal_magnetic_flux",
            "zero_condition": "H_radiative=0 and n dot(E x H_static)=0 on the parent-owned boundary",
            "finite_bound": "J_Poynting_bound=0 for this subchannel only",
            "caveat": "does not zero EM energy density, spatial stress, Coulomb coupling or full Jtot",
            "current_status": "CERTIFICATE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "regime_id": "REG3246_1_electrostatic",
            "field_regime": "electrostatic_bound_field",
            "zero_condition": "S_EM dot n=0 can hold while EM stress/energy remains nonzero",
            "finite_bound": "Poynting component may be zero; EM source-coupling still lives elsewhere",
            "caveat": "do not confuse Poynting silence with Maxwell/EM stress silence",
            "current_status": "CLASSIFIER_READY_NOT_SELECTED",
            "valid_for_claim": "false",
        },
        {
            "regime_id": "REG3246_2_crossed_fields",
            "field_regime": "static_crossed_or_circulating_field_momentum",
            "zero_condition": "normal projection vanishes by owned geometry or averaging",
            "finite_bound": "|n dot S| <= |E||H| and Phi <= C_flux||S_EM dot n||",
            "caveat": "requires sourced field bounds and boundary geometry",
            "current_status": "FINITE_BOUND_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "regime_id": "REG3246_3_radiative",
            "field_regime": "radiative_or_time_dependent_EM",
            "zero_condition": "none unless no-flux support is explicitly proven",
            "finite_bound": "J_Poynting_bound <= C_coll||T_EM(u,n)||_collar",
            "caveat": "using radiation flux to rescue static local GR is the wrong limit unless the test arena is radiative",
            "current_status": "LIVE_BOUND_REQUIRED",
            "valid_for_claim": "false",
        },
    ]


def dry_run_rows() -> list[dict[str, Any]]:
    row = score_rows()[0]
    missing_fields = [
        field
        for field in REQUIRED_SCORE_FIELDS
        if str(row.get(field, "")).startswith("MISSING") or str(row.get(field, "")).startswith("NOT_COMPUTED") or str(row.get(field, "")).startswith("UNCLASSIFIED")
    ]
    return [
        {
            "dry_run_id": "DRY3246_0_schema",
            "check": "required columns present",
            "passed": bool_str(all(field in row for field in REQUIRED_SCORE_FIELDS)),
            "evidence": ";".join(REQUIRED_SCORE_FIELDS),
            "claim_effect": "schema ready only",
        },
        {
            "dry_run_id": "DRY3246_1_missing",
            "check": "missing inputs detected",
            "passed": bool_str(bool(missing_fields)),
            "evidence": ";".join(missing_fields),
            "claim_effect": "blocks numeric promotion",
        },
        {
            "dry_run_id": "DRY3246_2_valid_flag",
            "check": "valid_for_claim remains false",
            "passed": bool_str(row["valid_for_claim"] == "false"),
            "evidence": row["valid_for_claim"],
            "claim_effect": "no empirical/local-GR claim",
        },
        {
            "dry_run_id": "DRY3246_3_zero",
            "check": "zero certificate not asserted",
            "passed": bool_str(row["zero_certificate"] == "false"),
            "evidence": row["zero_certificate"],
            "claim_effect": "no Poynting-zero shortcut",
        },
    ]


def transfer_rows() -> list[dict[str, Any]]:
    return [
        {
            "transfer_id": "XFER3246_0_component_bound",
            "target": "Poynting contribution to Jtot",
            "formula": "|J_A^Poynting| <= ||e_A||_B(C_flux||S_EM dot n||_B+B_corner_flux)+||e_A||_coll C_coll||T_EM(u,n)||_coll",
            "current_status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "transfer_id": "XFER3246_1_Jtot",
            "target": "Jtot total bound",
            "formula": "||Jtot|| <= ||J_bulk|| + |J_A^Poynting| + ||B_other|| + ||J_oddGamma||",
            "current_status": "PARTIAL_COMPONENT_INTERFACE_ONLY",
            "valid_for_claim": "false",
        },
        {
            "transfer_id": "XFER3246_2_amplitude",
            "target": "response amplitude",
            "formula": "||Z_*|| <= m0^{-1}||Jtot|| after M_AB coercivity is sourced",
            "current_status": "WAITING_ON_M0_AND_NUMERIC_COMPONENTS",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3246_0_score_schema",
            "claim": "first Poynting Jtot score-row schema exists",
            "condition_passed": "true",
            "status": "fillable row written",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3246_1_numeric_component",
            "claim": "first Poynting Jtot component is numeric/source-backed",
            "condition_passed": "false",
            "status": "boundary/frame/constants/flux norms/units missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3246_2_zero_component",
            "claim": "Poynting component is zero",
            "condition_passed": "false",
            "status": "quiet/static or exact no-flux certificate missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3246_3_amplitude_score",
            "claim": "Jtot amplitude score can be computed",
            "condition_passed": "false",
            "status": "needs numeric component plus m0 coercivity",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3246_4_local_GR",
            "claim": "local GR/Newton/PPN reduction",
            "condition_passed": "false",
            "status": "no numeric qloc/amplitude residual",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3246_0_real_fill_attempt",
            "decision": "The first Poynting Jtot score row is created but not promoted.",
            "because": "Existing files supply the formula, not the boundary/frame/flux constants needed for a number.",
            "next_action": "Acquire boundary/frame inputs or derive a quiet-static zero certificate.",
        },
        {
            "decision_id": "DEC3246_1_no_F2_shortcut",
            "decision": "Reject F^2=0 as a Poynting score substitute.",
            "because": "Earlier guards show null radiation can have nonzero stress/Poynting flux.",
            "next_action": "Keep stress-flux norm separate from scalar EM_F2 rows.",
        },
        {
            "decision_id": "DEC3246_2_best_next",
            "decision": "Next target should choose the actual local arena boundary and frame.",
            "because": "That is the first field in the score row; without it all later numbers are floating.",
            "next_action": "Build the parent-owned boundary/frame certificate or a nonclaim arena source row.",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3246_0_3247",
            "priority": "selected_primary",
            "next_doc": "3247-Y5-R2FR-parent-owned-boundary-frame-certificate-or-Poynting-arena-source-row-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3247_parent_owned_boundary_frame_certificate_or_Poynting_arena_source_row.py",
            "objective": "Try to derive or source the parent-owned boundary/collar/worldtube and observed frame u,n for the first Poynting Jtot score row; if unavailable, write the first arena-specific nonclaim source row.",
            "exclude": "do not choose boundary after seeing flux; do not claim Poynting zero from F2; do not edit formalization-workbench",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources_exist = all(row["exists"] == "true" for row in source_rows)
    sources_hit = all(row["evidence_hits"] not in {"MISSING_SOURCE", "NO_MATCH"} for row in source_rows)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    outputs_under_post = all(ROOT in path.parents for path in generated_csvs) and ROOT in DOC.parents
    formalization_3246 = list(FW.rglob("*3246*")) if FW.exists() else []
    formalization_clean = len(formalization_3246) == 0
    score = score_rows()[0]
    required_columns = all(field in score for field in REQUIRED_SCORE_FIELDS)
    missing_detected = any(str(score.get(field, "")).startswith(("MISSING", "NOT_COMPUTED", "UNCLASSIFIED")) for field in REQUIRED_SCORE_FIELDS)
    score_nonclaim = score["valid_for_claim"] == "false"
    zero_not_claimed = score["zero_certificate"] == "false"
    gates_block = all(row["claim_allowed"] == "false" for row in gate_rows())
    next_written = bool(next_rows())
    checks = [
        ("VAL3246_0_sources_exist", sources_exist, "all cited source paths exist", str(sources_exist)),
        ("VAL3246_1_source_hits", sources_hit, "source evidence hits are present", str(sources_hit)),
        ("VAL3246_2_csvs_parse", csvs_parse, "all generated CSV files parse", str(csvs_parse)),
        ("VAL3246_3_outputs_under_post_checkpoint", outputs_under_post, "all outputs are under post-checkpoint-work", str(outputs_under_post)),
        ("VAL3246_4_formalization_clean", formalization_clean, "no 3246 outputs in formalization-workbench", f"formalization_3246_count={len(formalization_3246)}"),
        ("VAL3246_5_required_columns", required_columns, "score row has all required columns", str(required_columns)),
        ("VAL3246_6_missing_detected", missing_detected, "score row exposes missing inputs", str(missing_detected)),
        ("VAL3246_7_score_nonclaim", score_nonclaim, "score row remains nonclaim", str(score_nonclaim)),
        ("VAL3246_8_zero_not_claimed", zero_not_claimed, "Poynting zero not asserted", str(zero_not_claimed)),
        ("VAL3246_9_claims_blocked", gates_block, "all claim gates remain nonclaim", str(gates_block)),
        ("VAL3246_10_next_written", next_written, "3247 next target written", str(next_written)),
        ("VAL3246_11_doc_written", DOC.exists(), "3246 markdown checkpoint exists", str(DOC.exists())),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": bool_str(passed),
            "requirement": requirement,
            "evidence": evidence_text,
        }
        for validation_id, passed, requirement, evidence_text in checks
    ]
    rows.append(
        {
            "validation_id": "VAL3246_OVERALL",
            "passed": bool_str(all(row["passed"] == "true" for row in rows)),
            "requirement": "3246 validation overall",
            "evidence": "all required validation rows passed",
        }
    )
    return rows


def build_doc(
    source_rows: list[dict[str, Any]],
    score: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    regime: list[dict[str, Any]],
    dry_run: list[dict[str, Any]],
    transfer: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3246 - First Poynting Jtot Score Row or Boundary/Frame Source Acquisition under AX1090",
            f"Generated: `{RUN_UTC}`",
            "Status: `Y5_R2FR_3246_first_Poynting_Jtot_score_row_schema_written_boundary_frame_flux_inputs_missing_nonclaim`",
            "Claim ceiling: `score_schema_only_no_numeric_Poynting_component_no_Poynting_zero_no_Jtot_score_no_amplitude_score_no_local_GR_claim`",
            "## Summary",
            "- `3246` attempts the first concrete `J_tot` score row, using the Poynting/collar flux component selected in `3245`.",
            "- The formula is now executable in shape: `|J_A^Poynting| <= ||e_A||_B(C_flux||S_EM dot n||_B+B_corner_flux)+||e_A||_coll C_coll||T_EM(u,n)||_collar`.",
            "- It is not numeric yet because the boundary/collar label, observed frame `u,n`, constants `C_flux/C_coll`, flux norms, response-basis norms, units and source path are not present.",
            "- The quiet-static zero route is also separated from the finite-flux route: Poynting can be zero in a quiet electrostatic limit, but that does not zero Maxwell stress, EM self-energy, Coulomb coupling, or full `J_tot`.",
            "- Next target is therefore not another theorem: it is the parent-owned boundary/frame certificate, or a specific arena source row.",
            "## First Poynting Jtot Score Row",
            md_table(score, REQUIRED_SCORE_FIELDS),
            "## Boundary/Frame/Flux Acquisition Ledger",
            md_table(acquisition, ["acq_id", "field", "needed_input", "derivation_or_source_route", "claim_if_missing", "priority"]),
            "## Poynting Regime Zero Or Bound Classifier",
            md_table(regime, ["regime_id", "field_regime", "zero_condition", "finite_bound", "caveat", "current_status", "valid_for_claim"]),
            "## Score Row Dry Run",
            md_table(dry_run, ["dry_run_id", "check", "passed", "evidence", "claim_effect"]),
            "## Jtot/Amplitude Transfer Update",
            md_table(transfer, ["transfer_id", "target", "formula", "current_status", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Next Target",
            md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude", "valid_for_claim"]),
            "## Source Register",
            md_table(source_rows, ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
            "## Generated Evidence",
            "\n".join(f"- `{path}`" for path in OUTPUTS.values()),
        ]
    )


def main() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    DOC.parent.mkdir(parents=True, exist_ok=True)

    source_rows = source_register()
    score = score_rows()
    acquisition = acquisition_rows()
    regime = regime_rows()
    dry_run = dry_run_rows()
    transfer = transfer_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["score"], score)
    write_csv(OUTPUTS["acquisition"], acquisition)
    write_csv(OUTPUTS["regime"], regime)
    write_csv(OUTPUTS["dry_run"], dry_run)
    write_csv(OUTPUTS["transfer"], transfer)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    generated_csvs = [
        OUTPUTS["sources"],
        OUTPUTS["score"],
        OUTPUTS["acquisition"],
        OUTPUTS["regime"],
        OUTPUTS["dry_run"],
        OUTPUTS["transfer"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, score, acquisition, regime, dry_run, transfer, gates, decisions, next_target, validation),
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, score, acquisition, regime, dry_run, transfer, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    failed = [row for row in validation if row["passed"] != "true"]
    if failed:
        raise SystemExit(f"3246 validation failed: {failed}")


if __name__ == "__main__":
    main()
