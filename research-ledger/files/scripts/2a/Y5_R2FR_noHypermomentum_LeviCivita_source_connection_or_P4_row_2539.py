from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2539"
BRANCH_ID = "MTS_R2FR_NOHYPERMOMENTUM_LEVICIVITA_OR_P4_ROW_2539"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2539-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2539_SOURCE_REGISTER.csv",
    "proof": RESIDUALS / "P8_Y5_NO_SHADOW_2539_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv",
    "p4": RESIDUALS / "P8_Y5_NO_SHADOW_2539_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv",
    "no_gamma": RESIDUALS / "P8_Y5_NO_SHADOW_2539_NO_GAMMA_SLOT_AUDIT_SEED.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2539_CONNECTION_GATE_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2539_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2539_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2539_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2539_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2539_VALIDATION.csv",
}

BRANCH_COPIES = {
    "proof": POST_ROOT / "source-intake" / "beta-source" / "docs" / "NoHypermomentum_LeviCivita_proof_audit_2539_NONCLAIM.csv",
    "p4": POST_ROOT / "source-intake" / "local_bounds" / "P4_hypermomentum_residual_row_2539_NONCLAIM.csv",
    "no_gamma": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "NoGamma_slot_audit_seed_2539_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "NOGAMMA2539_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    ("SRC2539_0_2538_doc", "2538-Y5-R2FR-Noether-source-charge-identity-or-nonHilbert-residual-row.md", "NEXT2538_0_selected", "2538 selected no-hypermomentum/Levi-Civita gate"),
    ("SRC2539_1_2538_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2538_VALIDATION.csv", "VAL2538_OVERALL,PASS", "2538 validation anchor"),
    ("SRC2539_2_2538_trident", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2538_NONHILBERT_TRIDENT_UPDATE.csv", "TRI2538_1_spin_torsion", "current spin/torsion head selected as primary gate"),
    ("SRC2539_3_2538_residual", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2538_NONHILBERT_RESIDUAL_ROW.csv", "NHR2538_1_spin_torsion", "current E_spin residual input"),
    ("SRC2539_4_2374_doc", "2374-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md", "NHL2374_6_verdict", "older no-hypermomentum precedent"),
    ("SRC2539_5_2374_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2374_VALIDATION.csv", "VAL2374_OVERALL", "2374 validation anchor"),
    ("SRC2539_6_2374_proof", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2374_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv", "NHL2374_6_verdict", "Levi-Civita/no-hypermomentum proof audit precedent"),
    ("SRC2539_7_2374_p4", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2374_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv", "P4R2374_0_hypermomentum_total", "P4 hypermomentum residual row precedent"),
    ("SRC2539_8_2374_no_gamma", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2374_NO_GAMMA_SLOT_AUDIT_SEED.csv", "NGS2374_6_verdict", "no-Gamma slot audit seed precedent"),
    ("SRC2539_9_2374_decision", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2374_CONNECTION_GATE_DECISION_LEDGER.csv", "CGD2374_1_best_next", "connection gate decision precedent"),
    ("SRC2539_10_2374_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2374_NEXT_TARGET.csv", "NEXT2374_0_selected", "no-Gamma slot next target precedent"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in SOURCE_SPECS:
        path = POST_ROOT / source_path
        rows.append(
            stamp(
                {
                    "source_id": source_id,
                    "source_path": source_path,
                    "needle": needle,
                    "role": role,
                    "path_exists": str(path.exists()).lower(),
                    "needle_found": str(contains(path, needle)).lower(),
                    "status": "SOURCE_OK" if path.exists() and contains(path, needle) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def proof_audit() -> list[dict[str, object]]:
    rows = [
        (
            "NHL2539_0_target",
            "no-hypermomentum / Levi-Civita source connection",
            "Gamma_obs=Gamma_LC[g_obs] and Delta_lambda^{mu nu}=delta S_ord/delta Gamma^lambda_{mu nu}=0 for matter, source, clock, light, orbit and readout sectors.",
            "TARGET_SHARPENED",
            "must be signed by parent variable selection or Palatini/no-hypermomentum theorem",
            "E_spin=0 and a major source-side GR coupling gate closes",
        ),
        (
            "NHL2539_1_metric_only_parent",
            "metric-only observed ordinary sector",
            "ordinary/source/readout configuration contains e_obs/g_obs and omega_LC[e_obs], but no independent Gamma argument",
            "EXACT_IF_PARENT_VARIABLE_LIST_SIGNED",
            "not signed for every matter/source/readout sector",
            "Delta_lambda^{mu nu}=0 by absence of variable",
        ),
        (
            "NHL2539_2_chain_rule_spin_connection",
            "coframe-owned spin connection",
            "spin connection is omega[e_obs], so spinor variation is counted through e_obs rather than an independent torsionful Gamma",
            "EXACT_CONDITIONAL_CLAUSE",
            "spinor and transport sectors need explicit coframe-owned connection clause",
            "ordinary spin does not create independent torsion source",
        ),
        (
            "NHL2539_3_palatini_route",
            "Palatini EH + no hypermomentum",
            "if independent Gamma enters only EH and Delta_lambda^{mu nu}=0, the Gamma equation gives Levi-Civita up to projective gauge",
            "CONDITIONAL_ROUTE_NOT_ACTIVE",
            "EH-only operator, no-Gamma matter/source/readout, and projective silence remain unsigned",
            "dynamic Levi-Civita compatibility rather than metric-only kinematics",
        ),
        (
            "NHL2539_4_source_readout_guard",
            "source/readout Gamma-slot exclusion",
            "delta S_source/delta Gamma = delta S_clock/delta Gamma = delta S_light/delta Gamma = delta S_orbit/delta Gamma = delta S_readout/delta Gamma = 0",
            "REQUIRED_GUARD_UNSIGNED",
            "source/worldtube/clock/light/orbit/readout Gamma-slot audit is not parent-signed",
            "connection cannot re-enter through measurement protocols",
        ),
        (
            "NHL2539_5_projective_caveat",
            "projective trace silence",
            "projective mode is gauge/fixed/unobservable in source charge, clocks, lightcones, spin transport and orbital readout",
            "UNSIGNED_OR_OPTIONAL_SOURCE_MISSING",
            "projective certificate/policy is not claim-grade in this branch",
            "Palatini route can avoid trace leakage",
        ),
        (
            "NHL2539_6_verdict",
            "promote Levi-Civita/no-hypermomentum",
            "current MTS corpus proves no independent connection source and no hypermomentum for all ordinary local tests",
            "NOT_DERIVED_RETAIN_P4_ROW",
            "metric-only parent, Palatini/EH, spin connection, source/readout Gamma-slot and projective clauses are unsigned",
            "use P4 hypermomentum residual row",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "route": route,
            "formal_statement": statement,
            "status": status,
            "obstruction": obstruction,
            "effect_if_closed": effect,
        }
        for row_id, route, statement, status, obstruction, effect in rows
    ]


def p4_residual_row() -> list[dict[str, object]]:
    rows = [
        (
            "P4R2539_0_hypermomentum_total",
            "independent_connection_hypermomentum",
            "Delta_abs",
            "Delta_abs := ||Delta_matter|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary||",
            "WEP;clock;source_charge;orbital;PPN;local_GR",
            "hypermomentum units or normalized dimensionless envelope",
            "MISSING_DELTA_COMPONENT_VALUES",
            "Delta components; K_hyper; norm definition; weak-field projection; arena bounds; source path",
        ),
        (
            "P4R2539_1_no_gamma_switch",
            "zero-switch",
            "Delta_lambda^{mu nu}",
            "Delta_lambda^{mu nu}=0 only if no independent Gamma slot exists in ordinary/source/readout branch",
            "all local source-current arenas",
            "boolean/theorem",
            "REQUIRES_PARENT_VARIABLE_ABSENCE",
            "parent variable list; matter/source/readout no-Gamma audit",
        ),
        (
            "P4R2539_2_axial_torsion_guard",
            "axial_torsion_spin_coupling",
            "S_axial_abs",
            "S_axial_abs := ||c_A S_mu J5^mu|| or normalized spin-torsion response envelope",
            "spin_transport;clock;WEP;source_charge",
            "spin-current units or normalized dimensionless envelope",
            "MISSING_SPIN_TORSION_COEFFICIENT",
            "spinor action branch; torsion coefficient; fermion source density; clock_or_spin_bound; source path",
        ),
        (
            "P4R2539_3_mapping_contract",
            "P4 weak-field/arena map",
            "K_P4",
            "epsilon_P4 <= K_hyper * Delta_abs plus absolute envelopes for torsion/nonmetricity components",
            "R10;PPN;clock;WEP;orbital;lightcone",
            "arena-specific after projection",
            "MISSING_WEAK_FIELD_MAP_AND_UNIT_NORMALIZATION",
            "component basis; unit normalization; lab frame; observable kernel; no-cancellation policy",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "channel": channel,
            "residual_symbol": symbol,
            "residual_formula": formula,
            "affected_tests": tests,
            "units": units,
            "current_status": status,
            "required_inputs": inputs,
        }
        for row_id, channel, symbol, formula, tests, units, status, inputs in rows
    ]


def no_gamma_slot_audit_seed() -> list[dict[str, object]]:
    rows = [
        ("NGS2539_0_matter", "ordinary matter action", "no independent Gamma argument in L_A beyond omega_LC[e_obs]", "MISSING_SECTOR_AUDIT"),
        ("NGS2539_1_source", "source support/worldtube", "source profile and support use observed metric/coframe data, not independent connection response", "MISSING_SECTOR_AUDIT"),
        ("NGS2539_2_clock", "clock/readout standards", "clock protocols do not vary Gamma independently or create hypermomentum source", "MISSING_SECTOR_AUDIT"),
        ("NGS2539_3_light", "lightcone/EM optics", "light propagation branch uses metric/coframe observable structure or retains connection residual", "MISSING_SECTOR_AUDIT"),
        ("NGS2539_4_orbit", "orbit/Kepler readout", "orbital calibration uses observed connection determined by metric/coframe or finite residual", "MISSING_SECTOR_AUDIT"),
        ("NGS2539_5_readout", "PPN/local readout maps", "readout maps are downstream and no-source-codomain, not Gamma-source couplings", "MISSING_SECTOR_AUDIT"),
        ("NGS2539_6_verdict", "all local sectors", "Delta_lambda^{mu nu}=0 across matter/source/readout branch", "NOT_DERIVED_AUDIT_REQUIRED"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "sector": sector,
            "no_gamma_condition": condition,
            "status": status,
        }
        for row_id, sector, condition, status in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        (
            "CGD2539_0_route",
            "no-hypermomentum theorem not promoted",
            "all clean routes require parent-signed variable/action/readout clauses that are not currently active",
            "retain P4 hypermomentum row as mandatory fallback",
            "P4_ROW_REQUIRED_NONCLAIM",
        ),
        (
            "CGD2539_1_best_next",
            "attack no-Gamma slot audit next",
            "absence of independent Gamma is stronger and cleaner than bounding arbitrary connection residues",
            "if it fails, P4 row declares required inputs",
            "SELECT_NO_GAMMA_AUDIT_NEXT",
        ),
        (
            "CGD2539_2_public_policy",
            "do not publish as GR reduction",
            "Levi-Civita/no-hypermomentum is conditional and P4 rows are not score-ready",
            "private derivation/fallback checkpoint only",
            "NO_GITHUB_EVIDENCE_UPDATE",
        ),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "decision": decision,
                "reason": reason,
                "consequence": consequence,
                "status": status,
            }
        )
        for row_id, decision, reason, consequence, status in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2539_0_sources", "source paths and needles valid", "PASS", "audit reproducible"),
        ("CG2539_1_metric_only_route", "metric-only observed connection parent-signed", "FAIL", "Levi-Civita not kinematically derived"),
        ("CG2539_2_palatini_route", "Palatini EH plus no hypermomentum closes", "FAIL", "dynamic LC route not active"),
        ("CG2539_3_no_gamma_source_readout", "source/readout Gamma-slot exclusion signed", "FAIL", "connection may re-enter via protocols"),
        ("CG2539_4_P4_score", "P4 hypermomentum residual score-ready", "FAIL", "values/maps/units missing"),
        ("CG2539_5_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "connection gate still open"),
        ("CG2539_6_github_public_update", "safe to push as public evidence", "FAIL", "private connection-gate checkpoint only"),
    ]
    return [
        stamp({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect})
        for row_id, gate, status, effect in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2539_0_import_GR_connection", "use Levi-Civita because GR uses it", "false", "LC must be parent-signed or residualized"),
        ("REF2539_1_spinor_shortcut", "ordinary spinors imply no independent torsion source automatically", "false", "coframe-owned spin connection must be explicit"),
        ("REF2539_2_projective_ignore", "projective trace is harmless without proof", "false", "projective mode must be gauge/fixed/unobservable in every local arena"),
        ("REF2539_3_P4_claim", "P4 fallback row is an empirical pass", "false", "P4 row is schema only; component values, units and weak-field maps are missing"),
    ]
    return [stamp({"row_id": row_id, "claim": claim, "allowed": allowed, "reason": reason}) for row_id, claim, allowed, reason in rows]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2539_0_selected",
            "selected",
            "2540-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md",
            "scripts/Y5_R2FR_noGamma_slot_matter_source_readout_audit_2540.py",
            "prove ordinary matter, source support, clocks, light, orbit and readout have no independent Gamma argument",
            "if any sector has a Gamma slot, route it to P4 hypermomentum component map and units",
        ),
        (
            "NEXT2539_1_fallback",
            "fallback",
            "2540b-Y5-R2FR-first-P4-hypermomentum-component-map-and-units.md",
            "scripts/Y5_R2FR_first_P4_hypermomentum_component_map_and_units_2540b.py",
            "fill Delta components, K_hyper, unit normalization, weak-field projection and arena bounds",
            "keep all values nonclaim until source-backed and same-frame",
        ),
        (
            "NEXT2539_2_parallel",
            "parallel",
            "2540c-Y5-R2FR-projective-trace-certificate-or-residual-policy.md",
            "scripts/Y5_R2FR_projective_trace_certificate_or_residual_policy_2540c.py",
            "prove projective trace is gauge/fixed/unobservable across source, clocks, lightcones, spin transport and orbit readout",
            "otherwise retain projective residual policy",
        ),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "priority": priority,
                "next_file": next_file,
                "next_script": next_script,
                "success_condition": success,
                "fallback_condition": fallback,
            }
        )
        for row_id, priority, next_file, next_script, success, fallback in rows
    ]


def branch_copy_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for copy_id, destination in BRANCH_COPIES.items():
        source = OUTPUTS[copy_id]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": copy_id,
                    "source_path": rel(source),
                    "destination_path": rel(destination),
                    "destination_exists": str(destination.exists()).lower(),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        if not changed:
            return True, "git modified-file count for formalization-workbench is 0"
        return False, f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("source_id") or row.get("copy_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() in {"true", "pass", "passed", "ready", "yes", "1"}:
                    offenders.append(f"{rel(path)}:{row_name}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append(stamp({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail}))

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2539_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2539_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2539_02_outputs_exist", all(path.exists() for path in generated), "all 2539 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2539_03_csv_parse", parse_ok, parse_detail)

    proof = {row["row_id"]: row["status"] for row in read_csv(outputs["proof"])}
    add("VAL2539_04_nohyper_not_promoted", proof.get("NHL2539_6_verdict") == "NOT_DERIVED_RETAIN_P4_ROW", "no-hypermomentum/LC not promoted")
    add("VAL2539_05_metric_route_conditional", proof.get("NHL2539_1_metric_only_parent") == "EXACT_IF_PARENT_VARIABLE_LIST_SIGNED", "metric-only route is exact only if parent variable list is signed")

    p4 = {row["row_id"]: row["current_status"] for row in read_csv(outputs["p4"])}
    add("VAL2539_06_p4_row_exists", p4.get("P4R2539_0_hypermomentum_total") == "MISSING_DELTA_COMPONENT_VALUES", "P4 hypermomentum total row exists")

    seed = {row["row_id"]: row["status"] for row in read_csv(outputs["no_gamma"])}
    add("VAL2539_07_no_gamma_audit_seeded", seed.get("NGS2539_6_verdict") == "NOT_DERIVED_AUDIT_REQUIRED", "no-Gamma slot audit seeded")

    decision = {row["row_id"]: row["status"] for row in read_csv(outputs["decision"])}
    add("VAL2539_08_no_gamma_selected", decision.get("CGD2539_1_best_next") == "SELECT_NO_GAMMA_AUDIT_NEXT", "no-Gamma audit selected as best next route")

    claims = {row["row_id"]: row["gate_status"] for row in read_csv(outputs["claims"])}
    add("VAL2539_09_claim_gates_block", claims.get("CG2539_5_local_GR_Newton") == "FAIL", "local GR/Newton claim gate remains false")
    add("VAL2539_10_github_blocked", claims.get("CG2539_6_github_public_update") == "FAIL", "public GitHub evidence update remains blocked")

    next_rows = read_csv(outputs["next"])
    add("VAL2539_11_next_selected", any(row.get("row_id") == "NEXT2539_0_selected" and "noGamma_slot" in row.get("next_script", "") for row in next_rows), "2540 no-Gamma slot audit selected")

    copy_rows = read_csv(outputs["copies"])
    add("VAL2539_12_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2539_13_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2539_14_formalization_untouched", formal_ok, formal_detail)
    add("VAL2539_15_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2539_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2539 valid: no-hypermomentum/LC not promoted, P4 residual row retained, no-Gamma slot audit selected" if overall else "one or more validation gates failed",
            }
        )
    )
    return rows


def table(headers: list[str], rows: list[dict[str, str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(header, "").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    proof = read_csv(outputs["proof"])
    p4 = read_csv(outputs["p4"])
    seed = read_csv(outputs["no_gamma"])
    decision = read_csv(outputs["decision"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2539 - noHypermomentum LeviCivita Source Connection Or P4 Row

## Result

The Levi-Civita/no-hypermomentum route remains the cleanest way to collapse the spin/torsion head, but it is not yet derived.

The desired theorem is:

`Gamma_obs = Gamma_LC[g_obs]` and `Delta_lambda^{{mu nu}} = delta S_ord / delta Gamma^lambda_{{mu nu}} = 0`.

This cannot be imported from GR. It must follow from either a parent variable list with no independent `Gamma` argument in matter/source/readout sectors, or a Palatini/EH route plus no-hypermomentum and projective silence.

Because those clauses are still unsigned, the P4 fallback remains live:

`Delta_abs := ||Delta_matter|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary||`.

Next target: audit each local sector for an independent `Gamma` slot. If every sector is no-Gamma, `Delta_lambda^{{mu nu}}=0` by absence of variable. If any sector has a Gamma slot, it must be routed into P4 residuals.

## noHypermomentum / Levi-Civita Proof Audit

{table(["row_id", "route", "status", "obstruction"], proof)}

## P4 Hypermomentum Residual Row

{table(["row_id", "channel", "residual_symbol", "current_status", "required_inputs"], p4)}

## no-Gamma Slot Audit Seed

{table(["row_id", "sector", "status", "no_gamma_condition"], seed)}

## Connection Gate Decision Ledger

{table(["row_id", "decision", "status", "consequence"], decision)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], gates)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["proof"])}`
- `{rel(outputs["p4"])}`
- `{rel(outputs["no_gamma"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is another useful narrowing. The connection problem is no longer just "does it reduce to GR"; it is now a sector-by-sector variable ownership audit. Either Gamma is absent from ordinary/source/readout sectors, or P4 becomes a real residual branch. This is still not local GR, but it is a cleaner path toward a derived GR limit than assuming the connection away.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    write_csv(OUTPUTS["proof"], proof_audit())
    write_csv(OUTPUTS["p4"], p4_residual_row())
    write_csv(OUTPUTS["no_gamma"], no_gamma_slot_audit_seed())
    write_csv(OUTPUTS["decision"], decision_ledger())
    write_csv(OUTPUTS["claims"], claim_gates())
    write_csv(OUTPUTS["refusal"], refusal_runner())
    write_csv(OUTPUTS["next"], next_target())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
