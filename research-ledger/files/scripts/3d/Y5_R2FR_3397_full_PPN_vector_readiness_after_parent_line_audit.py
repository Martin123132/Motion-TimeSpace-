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
DOC = ROOT / "3397-Y5-R2FR-full-PPN-vector-readiness-after-parent-line-audit-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3397_SOURCE_REGISTER.csv",
    "handoff_status": OUT / "P8_Y5_R2FR_3397_PARENT_LINE_HANDOFF_STATUS.csv",
    "ppn_vector_contract": OUT / "P8_Y5_R2FR_3397_FULL_PPN_VECTOR_CONTRACT.csv",
    "dependency_matrix": OUT / "P8_Y5_R2FR_3397_PPN_DEPENDENCY_MATRIX.csv",
    "input_schema": OUT / "P8_Y5_R2FR_3397_PPN_INPUT_SCHEMA_NONCLAIM.csv",
    "readiness_gate": OUT / "P8_Y5_R2FR_3397_PPN_READINESS_GATE.csv",
    "scoring_firewall": OUT / "P8_Y5_R2FR_3397_PPN_SCORING_FIREWALL.csv",
    "runner": OUT / "P8_Y5_R2FR_3397_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3397_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3397_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3397_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3397_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3397_00_3396_doc", ROOT / "3396-Y5-R2FR-minimal-parent-line-integration-or-source-normalization-demotion-under-AX1090.md", "3396 parent-line handoff"),
    ("SRC3397_01_3396_next", OUT / "P8_Y5_R2FR_3396_NEXT_TARGET.csv", "3396 next target"),
    ("SRC3397_02_3396_gate", OUT / "P8_Y5_R2FR_3396_INTEGRATION_GATE.csv", "parent-line integration gate"),
    ("SRC3397_03_3396_terms", OUT / "P8_Y5_R2FR_3396_PARENT_TERM_COVERAGE_MATRIX.csv", "parent term coverage"),
    ("SRC3397_04_3395_residual", OUT / "P8_Y5_R2FR_3395_COUPLING_RESIDUAL_CONTRACT_NONCLAIM.csv", "source normalization residual contract"),
    ("SRC3397_05_3395_implications", OUT / "P8_Y5_R2FR_3395_NEWTON_PPN_IMPLICATIONS.csv", "Newton/PPN implications"),
    ("SRC3397_06_3394_gate", OUT / "P8_Y5_R2FR_3394_ADMISSIBLE_PACKAGE_GATE.csv", "local Cassini hygiene package"),
    ("SRC3397_07_2177_ppn", OUT / "P8_Y5_PARENT_QLOC_2177_PPN_SOURCE_CONVENTION_GATE.csv", "prior PPN source convention gate"),
    ("SRC3397_08_2576_coeff", OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv", "Newton/PPN coefficient law"),
    ("SRC3397_09_3377_doc", ROOT / "3377-Y5-R2FR-weak-field-source-normalization-or-Gref-kappa-bound-under-AX1090.md", "prior weak-field source normalization theorem"),
]

PPN_PARAMETERS = [
    ("gamma", "spatial curvature per unit Newtonian potential", "first_order_metric_shape"),
    ("beta", "nonlinearity in time-time potential", "second_order_metric_shape"),
    ("alpha1", "preferred-frame vector sector 1", "preferred_frame"),
    ("alpha2", "preferred-frame vector sector 2", "preferred_frame"),
    ("alpha3", "preferred-frame/self-acceleration sector", "preferred_frame_conservation"),
    ("zeta1", "non-conservation/source-stress sector 1", "conservation"),
    ("zeta2", "non-conservation/source-stress sector 2", "conservation"),
    ("zeta3", "non-conservation/source-stress sector 3", "conservation"),
    ("zeta4", "non-conservation/source-stress sector 4", "conservation"),
    ("xi", "preferred-location/anisotropic potential sector", "preferred_location"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def handoff_status_rows() -> list[dict[str, str]]:
    integration_gate = {row.get("gate_id", ""): row for row in read_csv_rows(OUT / "P8_Y5_R2FR_3396_INTEGRATION_GATE.csv")}
    package_gate = {row.get("gate_id", ""): row for row in read_csv_rows(OUT / "P8_Y5_R2FR_3394_ADMISSIBLE_PACKAGE_GATE.csv")}
    return [
        {
            "status_id": "HS3397_0_core_compatibility",
            "input": "3396 core compatibility",
            "status": integration_gate.get("IG3396_0_core_compatibility", {}).get("gate_result", "MISSING"),
            "meaning_for_PPN": "core skeleton can host source-normalization line",
            "scoring_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "status_id": "HS3397_1_parent_signature",
            "input": "3396 missing parent terms",
            "status": integration_gate.get("IG3396_1_missing_parent_terms", {}).get("gate_result", "MISSING"),
            "meaning_for_PPN": "source normalization is not parent-owned; PPN scoring blocked",
            "scoring_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "status_id": "HS3397_2_local_hygiene",
            "input": "3394 local package",
            "status": package_gate.get("PKG3394_0_minimal_package_coherence", {}).get("gate_result", "MISSING"),
            "meaning_for_PPN": "projector/moment/Poynting/gauge hygiene is coherent but conditional",
            "scoring_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "status_id": "HS3397_3_current_readiness",
            "input": "combined handoff",
            "status": "READINESS_ONLY_SCORING_BLOCKED",
            "meaning_for_PPN": "define vector and inputs now; do not compare to empirical PPN bounds yet",
            "scoring_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def ppn_vector_contract_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    formulas = {
        "gamma": "gamma-1 = R_gamma_shape + R_source_linear + R_readout_projector",
        "beta": "beta-1 = kappa_v/2 + R_source_second_order + R_boundary_second_order",
        "alpha1": "alpha1 = R_frame_source + R_vector_readout + R_momentum_flux",
        "alpha2": "alpha2 = R_frame_metric + R_preferred_frame + R_spin_or_rotation_source",
        "alpha3": "alpha3 = R_momentum_nonconservation + R_self_acceleration",
        "zeta1": "zeta1 = R_stress_nonconservation_1 + R_source_scale_drift",
        "zeta2": "zeta2 = R_stress_nonconservation_2 + R_Htau_mismatch",
        "zeta3": "zeta3 = R_stress_nonconservation_3 + R_boundary_reference",
        "zeta4": "zeta4 = R_pressure_source_mismatch + R_matter_descent",
        "xi": "xi = R_preferred_location + R_anisotropic_kernel + R_external_potential_readout",
    }
    for parameter, meaning, sector in PPN_PARAMETERS:
        rows.append(
            {
                "ppn_id": f"PPN3397_{parameter}",
                "parameter": parameter,
                "sector": sector,
                "meaning": meaning,
                "residual_template": formulas[parameter],
                "needed_before_scoring": "MPL3395 parent adoption or finite source-normalization residual bounds; 3394 package adoption or finite local-hygiene residuals",
                "current_status": "SCHEMA_READY_SCORING_BLOCKED",
                "valid_for_claim": "false",
            }
        )
    return rows


def dependency_matrix_rows() -> list[dict[str, str]]:
    dependency_map = {
        "gamma": ["MPL3395", "delta_kappa", "delta_ellJ", "epsilon_Gref_match", "PC3392_projector", "gauge_readout"],
        "beta": ["MPL3395", "delta_KC", "kappa_v", "boundary_reference", "source_quadratic", "readout_quadratic"],
        "alpha1": ["MPL3395", "single_frame_patch", "momentum_source_current", "preferred_frame_silence"],
        "alpha2": ["MPL3395", "single_frame_patch", "metric_frame_lock", "preferred_frame_silence"],
        "alpha3": ["MPL3395", "momentum_conservation", "source_current_descent", "self_acceleration_silence"],
        "zeta1": ["MPL3395", "stress_energy_conservation", "delta_ellJ", "matter_descent"],
        "zeta2": ["MPL3395", "H_tau_match", "epsilon_Gref_match", "stress_energy_conservation"],
        "zeta3": ["MPL3395", "boundary_reference", "B_zero_flux", "Delta_symp"],
        "zeta4": ["MPL3395", "pressure_source_descent", "matter_descent", "ell_J"],
        "xi": ["MPL3395", "radial_even_kernel", "no_preferred_location", "external_potential_readout"],
    }
    rows: list[dict[str, str]] = []
    for parameter, dependencies in dependency_map.items():
        for dep in dependencies:
            rows.append(
                {
                    "dependency_id": f"DEP3397_{parameter}_{dep}",
                    "parameter": parameter,
                    "dependency": dep,
                    "source_checkpoint": "3395/3396" if dep in {"MPL3395", "delta_kappa", "delta_ellJ", "epsilon_Gref_match", "delta_KC", "kappa_v", "ell_J", "H_tau_match"} else "3394/local-package-or-future-source",
                    "current_status": "OPEN_OR_CONDITIONAL",
                    "blocks_scoring": "true",
                    "valid_for_claim": "false",
                }
            )
    return rows


def input_schema_rows() -> list[dict[str, str]]:
    base_rows = read_csv_rows(OUT / "P8_Y5_R2FR_3395_COUPLING_RESIDUAL_CONTRACT_NONCLAIM.csv")
    rows = []
    for row in base_rows:
        rows.append(
            {
                "input_id": f"IN3397_{row.get('symbol', '')}",
                "symbol": row.get("symbol", ""),
                "definition": row.get("definition", ""),
                "required_for": "source-normalized Newton/PPN vector",
                "current_status": row.get("current_status", "OPEN"),
                "claim_status": "NONCLAIM_INPUT_REQUIRED",
                "valid_for_claim": "false",
            }
        )
    extra = [
        ("R_alpha_pref_frame", "preferred-frame residual vector feeding alpha_i", "alpha1;alpha2;alpha3"),
        ("R_zeta_conservation", "stress-energy/source-current nonconservation residual vector feeding zeta_i", "zeta1;zeta2;zeta3;zeta4"),
        ("R_xi_location", "preferred-location / anisotropic external-potential residual", "xi"),
        ("R_boundary_reference_PPN", "B_zero_flux/Delta_symp/reference drift as PPN stress/source residual", "beta;zeta3"),
        ("R_local_package", "finite replacement if 3394 local package is not parent-adopted", "gamma;xi;alpha_i"),
    ]
    for symbol, definition, required_for in extra:
        rows.append(
            {
                "input_id": f"IN3397_{symbol}",
                "symbol": symbol,
                "definition": definition,
                "required_for": required_for,
                "current_status": "MISSING_FINITE_BOUND_OR_PARENT_ZERO",
                "claim_status": "NONCLAIM_INPUT_REQUIRED",
                "valid_for_claim": "false",
            }
        )
    return rows


def readiness_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "readiness_id": "READY3397_0_vector_defined",
            "gate": "full PPN vector schema is defined",
            "gate_pass": "true",
            "reason": "gamma, beta, alpha1-3, zeta1-4 and xi are represented",
            "allows_scoring": "false",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "READY3397_1_parent_line_adopted",
            "gate": "MPL3395 parent line adopted",
            "gate_pass": "false",
            "reason": "3396 staged an adoption packet but did not modify/sign parent docs",
            "allows_scoring": "false",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "READY3397_2_source_residuals_available",
            "gate": "finite source-normalization residual rows exist",
            "gate_pass": "false",
            "reason": "delta_kappa, delta_ellJ, epsilon_Gref_match, delta_KC and kappa_v remain nonclaim without numeric bounds",
            "allows_scoring": "false",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "READY3397_3_local_package_adopted",
            "gate": "3394 local hygiene package adopted or finite replacement supplied",
            "gate_pass": "false",
            "reason": "package is coherent/admissible but not parent-signed",
            "allows_scoring": "false",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "READY3397_4_empirical_bounds_sourced",
            "gate": "current empirical PPN bounds sourced",
            "gate_pass": "false",
            "reason": "3397 intentionally defines readiness only; no public PPN bound comparison is attempted",
            "allows_scoring": "false",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "READY3397_5_overall",
            "gate": "full PPN vector scoring readiness",
            "gate_pass": "false",
            "reason": "schema ready, ownership/bounds missing",
            "allows_scoring": "false",
            "valid_for_claim": "false",
        },
    ]


def scoring_firewall_rows() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "FW3397_0_no_gamma_only_claim",
            "forbidden_claim": "gamma shape proves local GR",
            "reason": "2177 already says gamma/beta shape is conditional; source convention and full vector remain open",
            "allowed_repair": "parent-line adoption or finite source residual rows, then full vector scoring",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "FW3397_1_no_beta_without_kappav",
            "forbidden_claim": "beta=1 from reciprocal readout alone",
            "reason": "2576 defines beta-1=kappa_v/2; kappa_v ledger must close or be bounded",
            "allowed_repair": "derive/bound kappa_v with source, PiM, boundary, readout, operator and coupling components",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "FW3397_2_no_preferred_frame_silence_by_assumption",
            "forbidden_claim": "alpha_i vanish because no preferred frame was intended",
            "reason": "alpha_i require explicit frame/source-current/tau/readout silence or finite vector bound",
            "allowed_repair": "single-frame/Fermi package plus source-current conservation theorem",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "FW3397_3_no_conservation_silence_by_Bianchi",
            "forbidden_claim": "zeta_i vanish automatically",
            "reason": "MTS extra stress, boundary/reference and source-current descent must be shown compatible with stress-energy conservation",
            "allowed_repair": "derive same Hilbert source descent and boundary/reference closure",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "FW3397_4_no_empirical_comparison_yet",
            "forbidden_claim": "PPN vector passes empirical bounds",
            "reason": "no current empirical bounds or numeric MTS residual rows are used in 3397",
            "allowed_repair": "3398 finite source-normalization bound pack, then source current PPN-bound table",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    vector_count = len(rows_by_name["ppn_vector_contract"])
    scoring_ready = any(row["readiness_id"] == "READY3397_5_overall" and row["gate_pass"] == "true" for row in rows_by_name["readiness_gate"])
    return [
        {
            "run_id": "RUN3397_0_vector_contract",
            "test": "full PPN vector contract",
            "result": "PASS_VECTOR_DEFINED_NONCLAIM",
            "detail": f"parameters={vector_count}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3397_1_dependency_matrix",
            "test": "PPN dependency matrix",
            "result": "PASS_DEPENDENCIES_MAPPED",
            "detail": f"dependencies={len(rows_by_name['dependency_matrix'])}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3397_2_readiness_gate",
            "test": "PPN scoring readiness",
            "result": "BLOCKED_SCORING_NOT_READY" if not scoring_ready else "PASS_READY",
            "detail": "parent-line adoption, source residual bounds, local package adoption and empirical bounds are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3397_3_firewall",
            "test": "PPN overclaim firewall",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "gamma-only, beta-without-kappa_v, preferred-frame silence and empirical comparison claims are blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3397_0_vector_defined",
            "claim": "full PPN vector schema exists",
            "gate_pass": "true",
            "reason": "gamma, beta, alpha_i, zeta_i and xi rows exist",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3397_1_parent_adoption",
            "claim": "source normalization parent line is adopted",
            "gate_pass": "false",
            "reason": "3396 integration-ready packet is not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3397_2_source_bounds",
            "claim": "finite source-normalization bounds exist",
            "gate_pass": "false",
            "reason": "3398 is needed for delta_kappa/delta_ellJ/epsilon_Gref_match/delta_KC/kappa_v",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3397_3_empirical_PPN",
            "claim": "MTS PPN vector is compared to empirical bounds",
            "gate_pass": "false",
            "reason": "3397 is readiness only, not a data-bound comparison",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3397_4_local_GR",
            "claim": "local GR/PPN passes",
            "gate_pass": "false",
            "reason": "full vector is defined but scoring is blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3397_0_progress",
            "decision": "The full PPN vector is now explicitly staged.",
            "because": "gamma, beta, alpha_i, zeta_i and xi each have a residual template and dependency list.",
            "next_action": "do not score it until source normalization is adopted or bounded",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3397_1_current_block",
            "decision": "Current block is not PPN algebra; it is source-normalization ownership.",
            "because": "3396 core compatibility is positive, but parent signature and finite residual rows are missing.",
            "next_action": "build finite source-normalization bound pack",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3397_2_no_gamma_shortcut",
            "decision": "Do not claim local GR from gamma shape.",
            "because": "beta, preferred-frame, conservation and preferred-location sectors can fail even when gamma looks right.",
            "next_action": "full vector only after 3398/parent adoption",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3397_3_best_next",
            "decision": "Next target should be finite source-normalization bounds.",
            "because": "without adoption, the only honest path forward is bounding delta_kappa, delta_ellJ, epsilon_Gref_match, delta_KC and kappa_v.",
            "next_action": "build 3398 parent-line finite source-normalization bound pack",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3398-Y5-R2FR-parent-line-finite-source-normalization-bound-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3398_parent_line_finite_source_normalization_bound_pack.py",
            "objective": "produce finite nonclaim bound rows for delta_kappa, delta_ellJ, epsilon_Gref_match, delta_KC, Delta_Newton_v_coupled and kappa_v so the PPN vector can later be scored without parent-line adoption",
            "why_next": "3397 defines the full vector but blocks scoring; finite source-normalization bounds are the missing input if adoption remains deferred",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3399-Y5-R2FR-full-PPN-vector-source-bound-runner-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3399_full_PPN_vector_source_bound_runner.py",
            "objective": "after 3398 finite bounds or parent adoption, run a nonclaim PPN vector scorer against sourced empirical bounds",
            "why_next": "the vector contract is ready, but it needs numeric residual inputs first",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3397*")
        if hit.name.startswith(("3397-Y5", "P8_Y5_R2FR_3397", "P8_Y5_BRR545_3397", "Y5_R2FR_3397"))
    ] if FW.exists() else []
    parameters = {row["parameter"] for row in rows_by_name["ppn_vector_contract"]}
    dependency_params = {row["parameter"] for row in rows_by_name["dependency_matrix"]}
    input_symbols = {row["symbol"] for row in rows_by_name["input_schema"]}
    readiness_overall = next(row for row in rows_by_name["readiness_gate"] if row["readiness_id"] == "READY3397_5_overall")
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3397_0_sources_exist_parse", "all cited 3397 source paths exist and parse", source_ok, ""),
        ("VAL3397_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3397_2_vector_contract", "PPN vector contract covers gamma, beta, alpha_i, zeta_i and xi", {"gamma", "beta", "alpha1", "alpha2", "alpha3", "zeta1", "zeta2", "zeta3", "zeta4", "xi"}.issubset(parameters), f"parameters={len(parameters)}"),
        ("VAL3397_3_dependency_matrix", "dependency matrix covers every PPN parameter", parameters.issubset(dependency_params), f"dependency_params={len(dependency_params)}"),
        ("VAL3397_4_input_schema", "input schema includes source-normalization and vector-specific residuals", {"delta_kappa", "delta_ellJ", "epsilon_Gref_match", "delta_KC", "Delta_Newton_v_coupled", "kappa_v", "R_alpha_pref_frame", "R_zeta_conservation", "R_xi_location"}.issubset(input_symbols), ""),
        ("VAL3397_5_readiness_blocks_scoring", "readiness gate blocks scoring overall", readiness_overall["gate_pass"] == "false" and readiness_overall["allows_scoring"] == "false", ""),
        ("VAL3397_6_firewall", "scoring firewall blocks gamma-only, beta-only, preferred-frame, conservation and empirical claims", len(rows_by_name["scoring_firewall"]) >= 5, f"rows={len(rows_by_name['scoring_firewall'])}"),
        ("VAL3397_7_runner", "runner records vector, dependencies, readiness block and firewall", {"PASS_VECTOR_DEFINED_NONCLAIM", "PASS_DEPENDENCIES_MAPPED", "BLOCKED_SCORING_NOT_READY", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3397_8_gates", "gates pass vector definition but block adoption, bounds, empirical PPN and local GR", gate_map.get("GATE3397_0_vector_defined") == "true" and gate_map.get("GATE3397_1_parent_adoption") == "false" and gate_map.get("GATE3397_2_source_bounds") == "false" and gate_map.get("GATE3397_3_empirical_PPN") == "false" and gate_map.get("GATE3397_4_local_GR") == "false", ""),
        ("VAL3397_9_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3397_10_write_scope_outside_formalization", "no 3397 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
        ("VAL3397_11_next_target", "next target moves to finite source-normalization bound pack", rows_by_name["next"][0]["target_id"].startswith("3398-Y5-R2FR-parent-line-finite-source-normalization"), ""),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3397_12_overall", "3397 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3397 - Y5/R2FR full PPN vector readiness after parent-line audit under AX1090",
        "",
        "## Summary",
        "- 3397 defines the full local PPN vector gate without pretending the theory is ready to score.",
        "- The vector now explicitly covers `gamma`, `beta`, `alpha1`, `alpha2`, `alpha3`, `zeta1`, `zeta2`, `zeta3`, `zeta4`, and `xi`.",
        "- Main result: the block is not the shape algebra alone; it is parent-line/source-normalization ownership plus finite residual inputs.",
        "- Scoring is blocked until `MPL3395` is parent-adopted or finite source-normalization rows exist for `delta_kappa`, `delta_ellJ`, `epsilon_Gref_match`, `delta_KC`, `Delta_Newton_v_coupled`, and `kappa_v`.",
        "- This prevents the bad shortcut: claiming local GR from a gamma-like first-order shape while beta, preferred-frame, conservation and preferred-location sectors remain open.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Parent Line Handoff Status",
        md_table(rows_by_name["handoff_status"]),
        "## Full PPN Vector Contract",
        md_table(rows_by_name["ppn_vector_contract"]),
        "## PPN Dependency Matrix",
        md_table(rows_by_name["dependency_matrix"]),
        "## PPN Input Schema",
        md_table(rows_by_name["input_schema"]),
        "## PPN Readiness Gate",
        md_table(rows_by_name["readiness_gate"]),
        "## PPN Scoring Firewall",
        md_table(rows_by_name["scoring_firewall"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "handoff_status": handoff_status_rows(),
        "ppn_vector_contract": ppn_vector_contract_rows(),
        "dependency_matrix": dependency_matrix_rows(),
        "input_schema": input_schema_rows(),
        "readiness_gate": readiness_gate_rows(),
        "scoring_firewall": scoring_firewall_rows(),
    }
    rows_by_name["runner"] = runner_rows(rows_by_name)
    rows_by_name["gates"] = gate_rows()
    rows_by_name["decision"] = decision_rows()
    rows_by_name["next"] = next_rows()
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
