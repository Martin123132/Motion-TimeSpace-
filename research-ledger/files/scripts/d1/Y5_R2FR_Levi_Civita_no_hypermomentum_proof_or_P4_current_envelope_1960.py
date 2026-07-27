from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1960-Y5-R2FR-Levi-Civita-no-hypermomentum-proof-or-P4-current-envelope.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1960_VALIDATION.csv"

SOURCES = {
    "1959_doc": {
        "path": ROOT / "1959-Y5-R2FR-torsion-boundary-readout-current-silence-or-envelope.md",
        "needles": ["SIL1959_1_torsion_Levi_Civita_route", "NEXT1959_0_primary", "VAL1959_OVERALL"],
    },
    "1959_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1959_VALIDATION.csv",
        "needles": ["VAL1959_OVERALL", "PASS"],
    },
    "443_connection": {
        "path": ROOT / "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md",
        "needles": ["P4_R0_metric_formalism_if_parent_selects_only_g", "P4_R1_Palatini_EH_no_hypermomentum", "Levi_Civita_parent_derived"],
    },
    "785_stack": {
        "path": ROOT / "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md",
        "needles": ["PMC785_4_connection_from_coframe", "CDS785_2_torsion_nonmetricity", "BGL785_2_connection_trigger"],
    },
    "960_torsion": {
        "path": ROOT / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md",
        "needles": ["LC960_1_metric_formalism_route", "LC960_2_Palatini_route", "P4REV960_0"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        needles = spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1960 Levi-Civita no-hypermomentum proof or P4 current envelope",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def lc_rows() -> list[dict[str, object]]:
    entries = [
        (
            "LC1960_0_target",
            "prove observed connection is Levi-Civita with no independent hypermomentum source, or demote connection residues into P4 envelopes",
            "Gamma_obs=Gamma_LC[g_obs] and Delta_lambda^{mu nu}=0, else retain C(T,Q,Delta)",
            "TARGET_EXACT",
            "This is a real local-GR bridge clause: no LC, no clean Hilbert-current/source-side GR.",
            "one route must be signed or bounded",
        ),
        (
            "LC1960_1_metric_only_parent_route",
            "connection is not an independent parent variable and matter uses omega[e_obs]",
            "fields include g/e but no independent Gamma; omega=omega[e_obs] by definition",
            "CONDITIONAL_ROUTE_NOT_PARENT_SIGNED",
            "Cleanest win if parent configuration really excludes independent connection.",
            "need parent variable-selection theorem and matter blindness to underlying fields",
        ),
        (
            "LC1960_2_Palatini_no_hypermomentum_route",
            "EH/Palatini variation plus matter/source/readout independence from Gamma forces LC up to harmless projective freedom",
            "delta_Gamma S_EH=0 and Delta_lambda^{mu nu}=0 -> nabla g=0, T=0 modulo projective gauge",
            "CONDITIONAL_ROUTE_NOT_PARENT_SIGNED",
            "This route is standard but unavailable until EH operator and no-hypermomentum premises are signed.",
            "need EH-only operator plus no Gamma matter/light/spin/source/readout coupling",
        ),
        (
            "LC1960_3_first_order_spin_route",
            "first-order coframe/spin-connection action imposes zero torsion only if spin/hypermomentum source is excluded or mapped",
            "delta_omega S -> T^a = kappa spin^a; zero only if spin source silent or constrained",
            "OPEN_SPIN_TORSION_ESCAPE",
            "Spinor matter blocks a silent torsion-zero claim unless the parent route says how spin is handled.",
            "need no independent spin-connection source or spin-torsion envelope",
        ),
        (
            "LC1960_4_metric_affine_zero_route",
            "metric-affine parent equations could algebraically force torsion and nonmetricity to zero",
            "E_Gamma(T,Q,Delta)=0 -> T=0,Q=0 only if source matrix invertible and Delta=0",
            "NOT_SUPPLIED",
            "No current action-level equation supplies this theorem.",
            "need explicit connection Euler equation",
        ),
        (
            "LC1960_5_projective_caveat",
            "projective freedom is harmless only if all matter/source/readout sectors are projectively invariant or the mode is fixed",
            "Gamma -> Gamma + delta^lambda_mu A_nu; safe iff observable couplings invariant",
            "PARTIAL_NOT_FULL_P4",
            "Projective gauge cannot hide axial torsion, shear nonmetricity, or hypermomentum.",
            "need projective invariance proof or residual row",
        ),
        (
            "LC1960_6_verdict",
            "Levi-Civita/no-hypermomentum proof is not closed at 1960",
            "blocked by unsigned parent variable selection, EH/Palatini premise, spin/hypermomentum, and matter/readout Gamma-independence",
            "ZERO_PROOF_FAILED_CLEANLY",
            "The fork is exact: sign LC/no-hypermomentum or fill P4 connection envelopes.",
            "next target should fill or prove the P4 connection subchannels",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, math_form, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "math_form": math_form,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def p4_rows() -> list[dict[str, object]]:
    entries = [
        (
            "P4C1960_0_combined",
            "torsion_nonmetricity_combined",
            "c_T_or_c_Q",
            "combined torsion/nonmetricity current residual",
            "MISSING_COEFFICIENT_VALUE_UNITS_MAP",
            "source-current or normalized dimensionless",
            "fill coefficient, normalization, weak-field/source map, and bound path",
        ),
        (
            "P4C1960_1_axial_torsion",
            "axial_torsion_spin_coupling",
            "c_A_or_S_mu",
            "spin/axial torsion current residual",
            "MISSING_SPIN_TORSION_MAP",
            "spin-current units",
            "spinor matter prevents silent zero unless excluded, mapped, or bounded",
        ),
        (
            "P4C1960_2_projective_trace",
            "torsion_trace_projective_mode",
            "c_Ttrace_or_T_mu",
            "projective/trace torsion source residual",
            "MISSING_PROJECTIVE_INVARIANCE_OR_BOUND",
            "inverse length or normalized",
            "prove universal projective invariance or retain source/WEP row",
        ),
        (
            "P4C1960_3_weyl_nonmetricity",
            "nonmetricity_weyl_trace",
            "c_Qtrace_or_Q_mu",
            "clock/rod/source normalization residual",
            "MISSING_CLOCK_ROD_SOURCE_MAP",
            "inverse length or normalized",
            "fill clock/redshift/rod/source residual map",
        ),
        (
            "P4C1960_4_shear_nonmetricity",
            "nonmetricity_shear_lightcone",
            "c_Qshear_or_Q_tilde",
            "lightcone/clock/WEP residual",
            "MISSING_LIGHTCONE_CLOCK_MAP",
            "inverse length or normalized",
            "metric lightcone cannot be assumed if shear nonmetricity survives",
        ),
        (
            "P4C1960_5_hypermomentum",
            "independent_connection_hypermomentum",
            "c_Delta_or_Delta_lambda_munu",
            "matter/source/readout independent-connection current",
            "MISSING_NO_GAMMA_MATTER_PROOF_OR_BOUND",
            "hypermomentum units or normalized",
            "derive no-Gamma matter/source/readout theorem or bound hypermomentum",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, channel, coefficient, definition, status, units, next_action in entries:
        row = base(row_id)
        row.update(
            {
                "channel": channel,
                "coefficient": coefficient,
                "definition": definition,
                "status": status,
                "units": units,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RUN1960_0_LC_zero",
            "metric-only parent or Palatini no-hypermomentum -> Gamma=Gamma_LC",
            "P_2[J_TQ]=0",
            "MISSING_PARENT_VARIABLE_SELECTION;MISSING_EH_PALATINI_PREMISE;MISSING_NO_HYPERMOMENTUM",
            "BLOCKED_ZERO_THEOREM_NOT_CLOSED",
            "no torsion/nonmetricity source-side claim",
        ),
        (
            "RUN1960_1_metric_only_conditional",
            "if parent has no independent connection, LC follows kinematically",
            "conditional theorem branch",
            "MISSING_PARENT_ACTION_VARIABLE_SIGNATURE",
            "PASS_NONCLAIM_CONDITIONAL_ROUTE",
            "best clean route, but unsigned",
        ),
        (
            "RUN1960_2_P4_envelope",
            "retained connection residues map to P4 current envelopes",
            "source-side residual bound after P4 coefficients and maps",
            "MISSING_P4_COEFFICIENTS_UNITS_MAPS",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "fallback empirical route not scoreable",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, prediction, acceptance_rule, missing_inputs, runner_status, consequence in entries:
        row = base(row_id)
        row.update(
            {
                "prediction": prediction,
                "acceptance_rule": acceptance_rule,
                "missing_inputs": missing_inputs,
                "runner_status": runner_status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1960_0_target", "LC/no-hypermomentum fork is explicit.", "PASS_NONCLAIM", "contract only"),
        ("CG1960_1_metric_only_route", "Metric-only route would make LC kinematic.", "PASS_NONCLAIM", "parent variable signature missing"),
        ("CG1960_2_LC_signed", "Observed connection is parent-signed Levi-Civita.", "FAIL_BLOCKED", "LC proof not parent-derived"),
        ("CG1960_3_no_hypermomentum", "Matter/source/readout have no independent Gamma charge.", "FAIL_BLOCKED", "no-Gamma matter/readout theorem missing"),
        ("CG1960_4_P4_envelopes", "P4 connection current envelopes are numeric/source-backed.", "FAIL_BLOCKED", "P4 rows remain placeholders"),
        ("CG1960_5_source_side_pass", "Torsion/nonmetricity source-side residual is zero/bounded.", "FAIL_BLOCKED", "LC proof and P4 bound both missing"),
        ("CG1960_6_local_GR", "MTS derives local GR/Newton.", "FAIL_BLOCKED", "connection, EH/R11, source mass, and PPN gates remain open"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1960_0_verdict",
            "LC_PROOF_NOT_CLOSED_P4_FORK_EXACT",
            "existing corpus already knew the route; 1960 makes the fork operational for the source-side current residual",
            "either sign parent metric-only/no-Gamma matter route or fill P4 channels",
        ),
        (
            "DEC1960_1_best_next",
            "PARENT_METRIC_ONLY_VARIABLE_SIGNATURE",
            "this is cleaner than chasing six P4 bounds because it kills the whole connection bypass at once",
            "attempt parent variable-selection/no-independent-connection signature before P4 numeric acquisition",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1960_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1961-Y5-R2FR-parent-metric-only-variable-signature-or-P4-fill.md",
            "target_script": "scripts/Y5_R2FR_parent_metric_only_variable_signature_or_P4_fill_1961.py",
            "objective": "prove the parent action has no independent observed-branch connection variable, or fill first P4 connection residual rows",
            "acceptance_output": "metric-only parent signature/no-Gamma matter theorem, or P4 coefficient/envelope rows",
            "nonclaim_rule": "no local-GR/source-side claim unless LC/no-hypermomentum or P4 residual bounds are live",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1960_0_project_position")
    row.update(
        {
            "strongest_result": "The Levi-Civita connection gate is an exact fork: parent metric-only/no-hypermomentum theorem or explicit P4 residual envelopes.",
            "what_improved": "source-side non-Hilbert current now has the upstream geometric condition it needs",
            "still_missing": "parent variable-selection theorem, EH/Palatini no-hypermomentum premises, no-Gamma matter/readout theorem, or P4 coefficients/maps",
            "claim_status": "not a source-side/Cassini/local-GR pass; a sharper connection fork",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1960_SOURCE_REGISTER.csv",
    "lc": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1960_LC_NO_HYPERMOMENTUM_ATTEMPT.csv",
    "p4": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1960_RUNNER_UPDATE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1960_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1960_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1960_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1960_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "LC_NO_HYPERMOMENTUM_1960_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1960_PARENT_METRIC_ONLY_OR_P4_FILL_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1960_0_nonclaim_weight"),
            "artifact": "1960 LC/no-hypermomentum proof or P4 envelope fork",
            "weight": "FORK_AUDIT_NOT_EVIDENCE",
            "reason": "connection route is exact but not signed or numeric",
        }
    ]
    queue = [
        {
            **base("AQ1960_0_metric_only_signature"),
            "target": "parent metric-only observed-branch signature",
            "needed_inputs": "parent variable list; q(Phi)->g/e; proof no independent Gamma/omega enters observed matter/source/readout",
            "priority": "HIGH",
        },
        {
            **base("AQ1960_1_P4_fill"),
            "target": "first P4 connection residual fill",
            "needed_inputs": "connection coefficients, units, weak-field maps, spin/source/readout assumptions",
            "priority": "FALLBACK_HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "lc": lc_rows(),
        "p4": p4_rows(),
        "runner": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1960-", "*_1960_*", "*Y5*1960*", "*VAL1960*", "*P8*1960*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1960_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    target_ok = any(row["row_id"] == "LC1960_0_target" and row["status"] == "TARGET_EXACT" for row in tables["lc"])
    rows.append(validation_row("VAL1960_01_target", "PASS" if target_ok else "FAIL", "LC/no-hypermomentum target recorded"))

    metric_ok = any(row["row_id"] == "LC1960_1_metric_only_parent_route" and row["status"] == "CONDITIONAL_ROUTE_NOT_PARENT_SIGNED" for row in tables["lc"])
    rows.append(validation_row("VAL1960_02_metric_route", "PASS" if metric_ok else "FAIL", "metric-only route retained as conditional"))

    p4_channels = {"torsion_nonmetricity_combined", "axial_torsion_spin_coupling", "independent_connection_hypermomentum"}
    p4_ok = p4_channels.issubset({row["channel"] for row in tables["p4"]})
    rows.append(validation_row("VAL1960_03_p4_channels", "PASS" if p4_ok else "FAIL", "P4 connection channels retained"))

    verdict_ok = any(row["row_id"] == "LC1960_6_verdict" and row["status"] == "ZERO_PROOF_FAILED_CLEANLY" for row in tables["lc"])
    rows.append(validation_row("VAL1960_04_verdict", "PASS" if verdict_ok else "FAIL", "LC proof failure recorded cleanly"))

    runner_statuses = {row["runner_status"] for row in tables["runner"]}
    runner_ok = {"BLOCKED_ZERO_THEOREM_NOT_CLOSED", "PASS_NONCLAIM_CONDITIONAL_ROUTE", "BLOCKED_MISSING_BOUND_FACTORS"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1960_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks claim branches"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1960_0_target" and row["status"] == "PASS_NONCLAIM" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1960_06_claim_gates", "PASS" if gate_ok else "FAIL", "only nonclaim gates pass"))

    decision_ok = any(row["decision"] == "PARENT_METRIC_ONLY_VARIABLE_SIGNATURE" for row in tables["decision"])
    rows.append(validation_row("VAL1960_07_decision", "PASS" if decision_ok else "FAIL", "parent metric-only signature selected"))

    next_ok = tables["next"][0]["target_doc"] == "1961-Y5-R2FR-parent-metric-only-variable-signature-or-P4-fill.md"
    rows.append(validation_row("VAL1960_08_next_target", "PASS" if next_ok else "FAIL", "1961 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1960_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1960_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1960_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1960_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1960_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1960_OVERALL", overall, "1960 Levi-Civita no-hypermomentum proof or P4 current envelope"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("LC No-Hypermomentum Attempt", tables["lc"]),
        ("P4 Connection Envelope Ledger", tables["p4"]),
        ("Runner Update", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1960 Y5 R2FR: Levi-Civita No-Hypermomentum Proof Or P4 Current Envelope",
        "",
        "Private checkpoint. This attacks the upstream geometric condition needed to silence torsion/nonmetricity non-Hilbert source currents.",
        "",
        "Verdict: the clean connection route is exact but unsigned. Either the parent action has no independent observed-branch connection / no hypermomentum, or the connection sector must be demoted into explicit P4 residual envelopes.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for name, path in OUTPUTS.items():
        write_csv(path, tables[name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1960_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
