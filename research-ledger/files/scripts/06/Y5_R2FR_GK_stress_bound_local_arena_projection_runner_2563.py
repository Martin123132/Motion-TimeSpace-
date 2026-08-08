from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_GK_STRESS_BOUND_LOCAL_ARENA_PROJECTION_RUNNER_2563"
CHECKPOINT_ID = "2563"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2563-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2563_SOURCE_REGISTER.csv",
    "residual_parameters": OUT / "P8_Y5_NO_SHADOW_2563_RESIDUAL_PARAMETER_LEDGER.csv",
    "arena_projection": OUT / "P8_Y5_NO_SHADOW_2563_ARENA_PROJECTION_ROWS.csv",
    "baseline_guardrails": OUT / "P8_Y5_NO_SHADOW_2563_BASELINE_COMPARISON_GUARDRAILS.csv",
    "runner_schema": OUT / "P8_Y5_NO_SHADOW_2563_NONCLAIM_RUNNER_SCHEMA.csv",
    "missing_inputs": OUT / "P8_Y5_NO_SHADOW_2563_MISSING_INPUTS_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2563_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2563_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2563_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2563_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2563_VALIDATION.csv",
}

COPY_TARGETS = {
    "local_projection_schema": LOCAL_BOUNDS / "GK_stress_bound_arena_projection_2563_NONCLAIM.csv",
    "missing_inputs_queue": QUEUE / "JR2563_GK_STRESS_BOUND_MISSING_INPUTS_NONCLAIM.csv",
    "baseline_guardrails": LOCAL_BOUNDS / "GK_stress_bound_baseline_guardrails_2563_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2563_00_2562_doc",
        "source_path": ROOT / "2562-Y5-R2FR-parent-sign-origin-and-boundary-topology-nohair-gate.md",
        "needles": ["DEM2562_0_demote_current_metric_branch", "DEM2562_5_next_runner", "NEXT2562_0_selected", "VAL2562_OVERALL"],
        "role": "handoff selecting nonclaim stress-bound local arena projection",
    },
    {
        "source_id": "SRC2563_01_2562_demotion",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2562_STRESS_BOUND_DEMOTION_ROUTE.csv",
        "needles": ["DEM2562_1_bound_quantity", "DEM2562_2_needed_coefficients", "DEM2562_3_claim_ceiling", "NONCLAIM"],
        "role": "machine-readable demotion route and claim ceiling",
    },
    {
        "source_id": "SRC2563_02_2562_parent_sign",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2562_PARENT_SIGN_AUDIT.csv",
        "needles": ["PS2562_0_current_source", "MISSING_PARENT_SIGN_SOURCE", "PS2562_6_minimum_reopen"],
        "role": "parent-sign blocker for no-hair promotion",
    },
    {
        "source_id": "SRC2563_03_2562_boundary",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2562_BOUNDARY_LEDGER.csv",
        "needles": ["BD2562_6_current_status", "MISSING_JUMP_CONDITION", "MISSING_TAU_PROJECTOR_BOUNDARY"],
        "role": "boundary and worldtube blockers for local exterior silence",
    },
    {
        "source_id": "SRC2563_04_2562_topology",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2562_TOPOLOGY_HAIR_AUDIT.csv",
        "needles": ["TOP2562_1_harmonic_A", "TOP2562_3_topological_charge", "MISSING_TOPOLOGY_LEDGER"],
        "role": "topological hair blockers for q_loc equals zero implying stress silence",
    },
    {
        "source_id": "SRC2563_05_2561_bound",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2561_STRESS_BOUND_ROUTE.csv",
        "needles": ["BOUND2561_1_near_coercive_branch", "BOUND2561_3_negative_branch", "MISSING_PARENT_COEFFICIENTS"],
        "role": "operator stress-bound route inherited from quadratic sign audit",
    },
    {
        "source_id": "SRC2563_06_2473_precedent",
        "source_path": ROOT / "2473-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md",
        "needles": ["ARENA2473_R10", "SCHEMA2473_3_block_rule", "VAL2473_OVERALL"],
        "role": "earlier local-arena scaffold precedent rerun against the 2562 chain",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append(
            {
                **base_row(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": exists,
                "missing_needles": ";".join(missing),
                "source_pass": exists and not missing,
                "role": source["role"],
            }
        )
    return rows


def residual_parameter_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RPAR2563_0_EGK",
            "E_GK_bound",
            "C_T*stress_tail + C_B*boundary_flux + C_S*source_tail + C_X*negative_mode_defect + C_H*topology_hair_amplitude + C_P*projector_leak",
            "dimensionless_or_arena_normalized_energy",
            "aggregate nonclaim residual stress-energy norm",
            "MISSING_PARENT_AND_ARENA_NORMALIZATION",
        ),
        (
            "RPAR2563_1_CT",
            "C_T",
            "bulk GK stress-to-bound coefficient from parent operator",
            "arena_response_coefficient",
            "needed because q_loc equals zero does not silence all stress",
            "MISSING_PARENT_COEFFICIENT",
        ),
        (
            "RPAR2563_2_CB",
            "C_B",
            "boundary flux-to-stress coefficient",
            "arena_response_coefficient",
            "captures unsilenced exterior boundary data",
            "MISSING_BOUNDARY_THEOREM",
        ),
        (
            "RPAR2563_3_CS",
            "C_S",
            "source-tail and worldtube matching coefficient",
            "arena_response_coefficient",
            "captures noncompact matter/GK support leakage",
            "MISSING_JUMP_CONDITION",
        ),
        (
            "RPAR2563_4_CX",
            "C_X",
            "negative-mode or coercivity-defect coefficient",
            "operator_response_coefficient",
            "activates if c_AG squared approaches or exceeds m_A2 Z_G",
            "MISSING_PARENT_SIGNS",
        ),
        (
            "RPAR2563_5_CH",
            "C_H",
            "topological hair-to-stress coefficient",
            "topology_response_coefficient",
            "captures harmonic A or gamma zero-mode stress with q_loc equals zero",
            "MISSING_TOPOLOGY_LEDGER",
        ),
        (
            "RPAR2563_6_CP",
            "C_P",
            "projector-hidden residual-to-stress coefficient",
            "projector_response_coefficient",
            "prevents P_loc silence from hiding full stress leakage",
            "MISSING_PROJECTOR_DESCENT",
        ),
        (
            "RPAR2563_7_Cmetric",
            "C_metric",
            "local metric Green response mapping stress to observable deviation",
            "arena_specific_response",
            "needed for PPN, clocks and orbital readout",
            "MISSING_ARENA_PROJECTION",
        ),
        (
            "RPAR2563_8_ellJ",
            "ell_J",
            "parent current-exchange or screening scale controlling local leakage length",
            "length",
            "needed before mapping residuals into finite-range tests",
            "MISSING_PARENT_SCALE",
        ),
    ]
    return [
        {
            **base_row(),
            "parameter_id": parameter_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "role": role,
            "status": status,
        }
        for parameter_id, symbol, definition, units, role, status in rows
    ]


def arena_projection_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ARENA2563_R10",
            "R10_short_range",
            "alpha_lambda_residual",
            "alpha_GK(lambda) <= K_R10(lambda,geometry)*E_GK_bound",
            "Eot-Wash style short-range inverse-square residual",
            "K_R10(lambda,geometry), lambda map, real bound curve, source normalization",
            "GR/Newton baseline must be run through same alpha-lambda parser with alpha_GR=0 after calibration",
            "valid_for_claim=false",
        ),
        (
            "ARENA2563_PPN",
            "PPN_solar_system",
            "gamma_minus_1_beta_minus_1_precession_preferred_frame",
            "norm(delta_PPN) <= K_PPN*C_metric*E_GK_bound + K_pf*projector_leak",
            "Cassini, ephemeris, perihelion, preferred-frame-style local metric residuals",
            "K_PPN, C_metric, boundary assumptions, topology class, metric gauge map",
            "GR PPN vector must be computed as the zero-residual control under same data conventions",
            "valid_for_claim=false",
        ),
        (
            "ARENA2563_CLOCK",
            "clock_redshift_time",
            "clock_rate_redshift_frequency_shift",
            "abs(delta_clock) <= K_clock*C_metric*E_GK_bound + K_tau*tau_projector_boundary_leak",
            "redshift, clock comparison and local time-sector leakage",
            "tau boundary term, clock observable kernel, units, source data",
            "GR redshift/control branch must be evaluated before blaming MTS for pipeline offsets",
            "valid_for_claim=false",
        ),
        (
            "ARENA2563_ORBITAL",
            "orbital_dynamics",
            "delta_acceleration_precession_range",
            "abs(delta_orbit) <= K_orb*C_metric*E_GK_bound",
            "planetary/lunar/binary orbit residual projection",
            "K_orb, source mass definition, orbital data, no fitted-GM circularity",
            "baseline must keep source mass and nuisance fitting identical across GR and MTS rows",
            "valid_for_claim=false",
        ),
        (
            "ARENA2563_WEP",
            "WEP_composition",
            "eta_composition_residual",
            "abs(eta_GK) <= K_WEP*species_leak*E_GK_bound",
            "composition-dependent acceleration residual",
            "species_leak, matter coupling descent, WEP data source",
            "metric-coupled GR control should give eta=0 within the same composition bookkeeping",
            "valid_for_claim=false",
        ),
        (
            "ARENA2563_LIGHT",
            "light_deflection_delay",
            "delta_deflection_delta_Shapiro",
            "abs(delta_light) <= K_light*C_metric*E_GK_bound",
            "lensing, Shapiro delay and null-geodesic local readout",
            "metric response tensor, null readout kernel, observational bound",
            "GR null-geodesic prediction must be the control before MTS residual scoring",
            "valid_for_claim=false",
        ),
    ]
    return [
        {
            **base_row(),
            "arena_id": arena_id,
            "arena": arena,
            "observable": observable,
            "projection_formula": formula,
            "test_role": test_role,
            "missing_inputs": missing_inputs,
            "baseline_guardrail": baseline_guardrail,
            "status": status,
        }
        for arena_id, arena, observable, formula, test_role, missing_inputs, baseline_guardrail, status in rows
    ]


def baseline_guardrail_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BASE2563_0_same_pipeline",
            "Run GR/Newton baseline and MTS through the same parser, units, priors and nuisance treatment.",
            "If the baseline breaks too, the test pipeline is suspect rather than the theory branch alone.",
            "PASS_GUARDRAIL",
        ),
        (
            "BASE2563_1_no_fitted_GM_shortcut",
            "Do not absorb MTS residuals by redefining source mass, GM, clock offset or boundary data after readout.",
            "Prevents circular local compatibility.",
            "PASS_GUARDRAIL",
        ),
        (
            "BASE2563_2_no_MHref_reuse",
            "Do not reuse cosmology or galaxy reference masses as local source definitions unless derived for the arena.",
            "Prevents cross-sector patching.",
            "PASS_GUARDRAIL",
        ),
        (
            "BASE2563_3_no_plateau_axiom",
            "Do not impose q_loc plateau silence as an axiom inside the stress-bound branch.",
            "This branch exists because no-hair/plateau silence is not yet parent-proved.",
            "PASS_GUARDRAIL",
        ),
        (
            "BASE2563_4_claim_scale",
            "Scoring equal to or slightly better than baseline is meaningful only after sourced coefficients and identical model-selection accounting.",
            "Keeps the boxing-match logic honest without pretending small BIC wins are derivations.",
            "NONCLAIM_GUARDRAIL",
        ),
        (
            "BASE2563_5_data_blindness",
            "Choose kernels and signs from parent derivation or predeclared source acquisition, not from local-data success.",
            "Prevents empirical sign-fitting.",
            "PASS_GUARDRAIL",
        ),
    ]
    return [
        {
            **base_row(),
            "guardrail_id": guardrail_id,
            "rule": rule,
            "why_needed": why_needed,
            "status": status,
        }
        for guardrail_id, rule, why_needed, status in rows
    ]


def runner_schema_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SCHEMA2563_0_required_inputs",
            "inputs",
            "arena_id,observable,E_GK_bound,K_arena,C_metric,arena_bound,units,source_path,baseline_model,valid_for_claim",
            "all numeric rows need positive finite values, units and source paths",
            "NONCLAIM_SCHEMA",
        ),
        (
            "SCHEMA2563_1_prediction",
            "prediction",
            "residual_predicted = arena_formula(E_GK_bound,K_arena,C_metric,extra_leaks)",
            "compute only when every required coefficient is numeric and sourced",
            "NONCLAIM_SCHEMA",
        ),
        (
            "SCHEMA2563_2_baseline",
            "baseline",
            "baseline_residual,baseline_pipeline_status,baseline_data_convention",
            "MTS row cannot be interpreted unless baseline row also parses and reports",
            "PASS_GUARDRAIL",
        ),
        (
            "SCHEMA2563_3_pass_rule",
            "compatibility_rule",
            "abs(residual_predicted) <= arena_bound and baseline comparison is fair",
            "compatibility is not a local-GR derivation",
            "NONCLAIM_SCHEMA",
        ),
        (
            "SCHEMA2563_4_block_rule",
            "claim_block",
            "any MISSING marker, invalid units, missing baseline, fitted-GM flag or valid_for_claim=false gives claim_allowed=false",
            "default private safety rule",
            "PASS_GUARDRAIL",
        ),
        (
            "SCHEMA2563_5_future_zero_rule",
            "derivation_upgrade",
            "if parent no-hair later proves E_GK_bound=0 with signed coefficients, reroute to local-GR theorem branch",
            "keeps derivation route reopenable",
            "FUTURE_ONLY",
        ),
    ]
    return [
        {
            **base_row(),
            "schema_id": schema_id,
            "field_group": field_group,
            "schema": schema,
            "acceptance_rule": acceptance_rule,
            "status": status,
        }
        for schema_id, field_group, schema, acceptance_rule, status in rows
    ]


def missing_input_rows() -> list[dict[str, Any]]:
    rows = [
        ("MISS2563_0_parent_signs", "Z_A,Z_G,m_A2,m_G2,c_AG", "parent signs and coercivity condition", "MISSING_PARENT_SIGN_SOURCE", "blocks no-hair promotion and numeric E_GK"),
        ("MISS2563_1_bulk_stress", "C_T", "bulk stress normalization", "MISSING_PARENT_COEFFICIENT", "needed for every arena"),
        ("MISS2563_2_boundary", "C_B,boundary_flux,no_flux theorem", "boundary contribution", "MISSING_BOUNDARY_THEOREM", "prevents silent exterior assumption"),
        ("MISS2563_3_source_tail", "C_S,source_tail,jump_conditions", "worldtube/source leakage", "MISSING_JUMP_CONDITION", "needed for lab and orbital source models"),
        ("MISS2563_4_negative_mode", "C_X,negative_mode_defect", "operator-sign failure contribution", "MISSING_PARENT_SIGNS", "needed if coercivity is not proved"),
        ("MISS2563_5_topology", "C_H,topology_hair_amplitude,cohomology_class", "harmonic/topological hair contribution", "MISSING_TOPOLOGY_LEDGER", "needed for q_loc equals zero not implying stress zero"),
        ("MISS2563_6_projector", "C_P,projector_leak,tau_projector_boundary_leak", "projection-hidden residual", "MISSING_PROJECTOR_DESCENT", "needed for clocks and stress silence"),
        ("MISS2563_7_metric_response", "C_metric,metric_response_tensor,gauge_map", "stress-to-observable map", "MISSING_ARENA_PROJECTION", "needed for PPN/clocks/orbits/light"),
        ("MISS2563_8_arena_kernels", "K_R10,K_PPN,K_clock,K_orb,K_WEP,K_light", "observable kernels", "MISSING_ARENA_KERNELS", "needed for any data comparison"),
        ("MISS2563_9_bound_data", "arena_bound,data_source,units", "external bound rows", "MISSING_BOUND_DATA", "needed for pass/fail compatibility"),
        ("MISS2563_10_baselines", "baseline_residual,baseline_pipeline_status", "GR/Newton control rows", "MISSING_BASELINE_CONTROL", "needed to avoid pipeline-only failures"),
    ]
    return [
        {
            **base_row(),
            "missing_id": missing_id,
            "symbol_or_input": symbol_or_input,
            "meaning": meaning,
            "status": status,
            "effect": effect,
        }
        for missing_id, symbol_or_input, meaning, status, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2563_0_source_handoff", "2562 demotion handoff is sourced.", "PASS", "source register passes", True, False),
        ("GATE2563_1_projection_schema", "local arena projection scaffold exists.", "PASS_AS_SCHEMA", "arena rows and runner schema written", True, False),
        ("GATE2563_2_baseline_guardrails", "baseline comparison guardrails exist.", "PASS_GUARDRAIL", "GR/Newton controls required before interpretation", True, False),
        ("GATE2563_3_numeric_claim", "stress-bound rows are numerically claimable.", "BLOCKED", "parent coefficients and arena kernels missing", False, False),
        ("GATE2563_4_local_compatibility", "MTS is compatible with local arenas.", "BLOCKED", "no sourced numeric projection run yet", False, False),
        ("GATE2563_5_local_GR_derivation", "local GR/PPN is derived.", "BLOCKED", "stress-bound fallback cannot replace no-hair proof", False, False),
        ("GATE2563_6_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private checkpoint only", True, False),
    ]
    return [
        {
            **base_row(),
            "gate_id": gate_id,
            "claim": claim,
            "gate_status": gate_status,
            "reason": reason,
            "gate_pass": gate_pass,
            "claim_allowed": claim_allowed,
        }
        for gate_id, claim, gate_status, reason, gate_pass, claim_allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2563_0_accept_demotion", "Treat current local metric branch as stress-bound only.", "2562 blocked parent-sign/no-hair promotion", "no local-GR claim"),
        ("DEC2563_1_build_scoreboard", "Create local arena projection rows before data scoring.", "R10/PPN/clocks/orbits need different kernels", "prevents one-size-fits-all residual"),
        ("DEC2563_2_require_baseline", "Require matched GR/Newton baseline controls.", "pipeline failures must not be attributed only to MTS", "fair-comparison discipline"),
        ("DEC2563_3_keep_reopenable", "Keep no-hair route as future derivation upgrade.", "explicit parent signs/boundaries could still close E_GK=0", "not dead, just not current evidence"),
        ("DEC2563_4_next", "Build a dry-run placeholder rejection runner next.", "schema is ready but all claim rows must block", "2564 selected"),
    ]
    return [
        {
            **base_row(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "effect": effect,
        }
        for decision_id, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2563_0_selected",
            "selection_status": "selected",
            "target_file": "2564-Y5-R2FR-GK-stress-bound-dry-run-and-baseline-control-runner.md",
            "target_script": "scripts/Y5_R2FR_GK_stress_bound_dry_run_and_baseline_control_runner_2564.py",
            "task": "implement dry-run arithmetic over the 2563 schema with toy nonclaim rows, missing-input rejection, bad-unit rejection, fitted-GM rejection and matched-baseline control checks",
            "acceptance_target": "dry-run CSV, rejection ledger, baseline-control ledger, claim gates and no formalization-workbench artifacts",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["arena_projection"], COPY_TARGETS["local_projection_schema"])
    shutil.copyfile(OUTPUTS["missing_inputs"], COPY_TARGETS["missing_inputs_queue"])
    shutil.copyfile(OUTPUTS["baseline_guardrails"], COPY_TARGETS["baseline_guardrails"])
    source_map = {
        "local_projection_schema": OUTPUTS["arena_projection"],
        "missing_inputs_queue": OUTPUTS["missing_inputs"],
        "baseline_guardrails": OUTPUTS["baseline_guardrails"],
    }
    return [
        {
            **base_row(),
            "copy_id": copy_id,
            "source_path": str(source_map[copy_id]),
            "target_path": str(target),
            "source_exists": source_map[copy_id].exists(),
            "target_exists": target.exists(),
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    add("VAL2563_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited source paths exist and required needles are present")
    add("VAL2563_01_parameters_written", len(data["parameters"]) >= 9 and all(row["status"].startswith("MISSING") for row in data["parameters"]), "residual parameter ledger written as nonclaim missing-input scaffold")
    add("VAL2563_02_arenas_written", len(data["arenas"]) >= 6 and all(row["status"] == "valid_for_claim=false" for row in data["arenas"]), "arena projection rows written as nonclaim")
    add("VAL2563_03_baseline_guardrails", len(data["baseline"]) >= 6 and all("GUARDRAIL" in row["status"] for row in data["baseline"]), "baseline-comparison guardrails written")
    add("VAL2563_04_schema_guardrails", any(row["schema_id"] == "SCHEMA2563_4_block_rule" and row["status"] == "PASS_GUARDRAIL" for row in data["schema"]), "claim blocking schema written")
    add("VAL2563_05_missing_ledger", len(data["missing"]) >= 11 and all(row["status"].startswith("MISSING") for row in data["missing"]), "missing input ledger active")
    add("VAL2563_06_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR or local compatibility claim")
    add("VAL2563_07_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2563_0_selected", "2564 dry-run and baseline-control runner selected")
    add("VAL2563_08_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2563-Y5", "P8_Y5_NO_SHADOW_2563", "P8_Y5_BRR545_2563", "JR2563")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2563_09_no_formalization_artifacts", not formal_hits, "no 2563 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2563_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2563_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2563_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2563_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2563_OVERALL", all(row["status"] == "PASS" for row in rows), "2563 builds nonclaim stress-bound local arena projection scaffold with matched-baseline guardrails")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2563 Y5 R2FR GK Stress-bound Local Arena Projection Runner",
        "",
        "**Status:** nonclaim projection scaffold written. The 2562 parent-sign/no-hair gate demoted the current local metric branch to stress-bound only, so 2563 builds the honest local test scoreboard for R10, PPN, clocks, orbital dynamics, WEP and light-propagation readouts.",
        "",
        "**Meaning:** this still does not derive local GR. It turns the unsilenced GK stress problem into explicit residual variables, arena kernels, baseline controls and claim gates so the next runner can test plumbing without smuggling in a plateau or no-hair axiom.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Residual Parameter Ledger",
        markdown_table(data["parameters"], ["parameter_id", "symbol", "definition", "units", "role", "status"]),
        "",
        "## Arena Projection Rows",
        markdown_table(data["arenas"], ["arena_id", "arena", "observable", "projection_formula", "test_role", "missing_inputs", "baseline_guardrail", "status"]),
        "",
        "## Baseline Comparison Guardrails",
        markdown_table(data["baseline"], ["guardrail_id", "rule", "why_needed", "status"]),
        "",
        "## Nonclaim Runner Schema",
        markdown_table(data["schema"], ["schema_id", "field_group", "schema", "acceptance_rule", "status"]),
        "",
        "## Missing Inputs Ledger",
        markdown_table(data["missing"], ["missing_id", "symbol_or_input", "meaning", "status", "effect"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "parameters": residual_parameter_rows(),
        "arenas": arena_projection_rows(),
        "baseline": baseline_guardrail_rows(),
        "schema": runner_schema_rows(),
        "missing": missing_input_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["residual_parameters"], data["parameters"])
    write_csv(OUTPUTS["arena_projection"], data["arenas"])
    write_csv(OUTPUTS["baseline_guardrails"], data["baseline"])
    write_csv(OUTPUTS["runner_schema"], data["schema"])
    write_csv(OUTPUTS["missing_inputs"], data["missing"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
