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

DOC_PATH = ROOT / "1964-Y5-R2FR-owned-coframe-legitimacy-and-EH-second-order-gate.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1964_VALIDATION.csv"

SOURCES = {
    "1963_doc": {
        "path": ROOT / "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md",
        "needles": ["ACT1963_1_variable_list", "NGT1963_0_theorem", "NEXT1963_0_primary"],
    },
    "1963_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1963_VALIDATION.csv",
        "needles": ["VAL1963_OVERALL", "PASS"],
    },
    "observer_contract_10": {
        "path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["The local observer coframe must be defined before any PPN claim", "all matter sectors couple to the same observer coframe"],
    },
    "radial_cell_09": {
        "path": ROOT / "09-hamiltonian-radial-cell-derivation.md",
        "needles": ["defined clock-load coframe", "defined radial routing coframe"],
    },
    "1339_eh_gate": {
        "path": ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
        "needles": ["EHGate1339_2_second_order", "LOV1339_0_conditional_EH_selection", "R11V1339_0_R2_fR_scalar"],
    },
    "958_premise_csv": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_958_EH_PREMISE_AUDIT.csv",
        "needles": ["EHP958_P5_local_4D_metric_action", "EHP958_P6_second_order", "EHP958_P3_no_extra_fields"],
    },
    "958_r11_csv": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_958_R11_OPERATOR_FAMILY_PRIORITY.csv",
        "needles": ["R11PRI958_1", "R2_fR_scalar_mode"],
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
    for source_id, source_spec in SOURCES.items():
        path = source_spec["path"]
        needles = source_spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1964 owned-coframe legitimacy and EH second-order gate",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def coframe_legitimacy_rows() -> list[dict[str, object]]:
    entries = [
        (
            "LEG1964_0_risk",
            "An owned coframe can be a legitimate MTS readout variable or a disguised import of GR geometry.",
            "GR_INSERTION_RISK_EXPLICIT",
            "This is the right scrutiny point after 1963.",
            "prove e_obs comes from motion/time/space readout, or demote ACT1963 to a closure branch",
        ),
        (
            "LEG1964_1_operational_support",
            "Earlier work already requires a local observer coframe, clock-load coframe, radial-routing coframe, and same coframe for matter.",
            "SOURCE_SUPPORT_FOR_COFRAME_LANGUAGE",
            "The coframe concept is not newly invented in 1963.",
            "still must turn those contracts into a parent action object",
        ),
        (
            "LEG1964_2_not_four_scalar_gradients",
            "Do not derive a general coframe as merely dX^a from four scalar coordinates.",
            "SCALAR_GRADIENT_ROUTE_TOO_RESTRICTIVE",
            "Exact gradients would kill anholonomy and cannot represent generic local curved/tidal frame structure.",
            "need coframe one-forms or a frame-deformation field, not only four coordinate scalars",
        ),
        (
            "LEG1964_3_MTS_readout_contract",
            "Legitimate MTS coframe means e_obs is the local conversion map from parent motion-time-space flow data to clock, ruler, photon, and matter readouts.",
            "CONTRACT_WRITTEN_NOT_PROVED",
            "This makes e_obs operational rather than an arbitrary metric insertion.",
            "write parent map e_obs=E[q(Phi_MTS)] with nondegenerate determinant and Lorentz gauge equivalence",
        ),
        (
            "LEG1964_4_universality_condition",
            "The same e_obs must be used by clocks, rods, photons, massive matter, source charge, and orbital/PPN readout.",
            "UNIVERSAL_READOUT_REQUIRED",
            "Without this, WEP and measured-GM transfer fragment.",
            "audit species and source/readout maps for shadow frames",
        ),
        (
            "LEG1964_5_legitimacy_verdict",
            "The owned-coframe branch is plausible and source-supported but not yet fully derived from MTS parent variables.",
            "PARTIAL_LEGITIMACY_NOT_CANONICAL",
            "Good enough to continue as the best derivation route, not enough for public local-GR claim.",
            "next must either derive E[q(Phi_MTS)] or keep ACT1963 as conditional closure only",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def eh_second_order_rows() -> list[dict[str, object]]:
    entries = [
        (
            "EH2_1964_0_Lovelock_conditional",
            "If the surviving compact local exterior is 4D, diffeo-invariant, metric/coframe-only, Levi-Civita, second-order, and boundary-harmless, the left-hand operator reduces to EH plus Lambda up to normalization.",
            "MATHEMATICAL_CONDITIONAL_RETAINED",
            "This is the GR bridge theorem, but only after premises are parent-signed.",
            "do not invoke EH until all premises are explicit",
        ),
        (
            "EH2_1964_1_what_1963_helped",
            "ACT1963 conditionally supplies the Levi-Civita/no-independent-connection premise.",
            "LC_PREMISE_CONDITIONALLY_HELPED",
            "Connection is no longer the primary obstacle if ACT1963 is adopted.",
            "canonicalize or reject ACT1963",
        ),
        (
            "EH2_1964_2_central_blocker",
            "The general local action S_local_geom[e,Xi] still permits R2, fR, Ricci-square, Weyl-square, nonlocal memory, and extra-sector stress.",
            "SECOND_ORDER_NOT_DERIVED",
            "This is now the main route-blocker for deriving GR rather than a modified-gravity family.",
            "prove a second-order/no-extra-sector selection rule or build executable R11 residuals",
        ),
        (
            "EH2_1964_3_no_extra_sector",
            "Xi_MTS fields must be absent, gauge, topological/no-flux, no-haired, integrated out harmlessly, or retained as explicit residuals in the local exterior.",
            "EXTRA_SECTOR_SILENCE_NOT_DERIVED",
            "Motion/time/domain/memory cannot be allowed to carry hidden exterior stress if claiming GR.",
            "write no-hair/silence theorem or residual vector",
        ),
        (
            "EH2_1964_4_decision",
            "The next best attack is not more coframe wording; it is the R11 second-order/no-extra-sector fork.",
            "MOVE_TO_R11_OR_SECOND_ORDER_PROOF",
            "This is the path that decides whether MTS becomes GR in local vacuum or a constrained modified-gravity branch.",
            "1965 should try an R2/fR zero proof first, then stage executable bound rows if it fails",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def r11_interface_rows() -> list[dict[str, object]]:
    entries = [
        (
            "R11X1964_0_R2_fR_scalar",
            "R2 or fR scalar mode",
            "highest",
            "c_R2 or f_RR; scalar mass m0; coupling alpha0; range lambda0; PPN gamma/beta map; R10 alpha(lambda) map",
            "MISSING_ZERO_CERTIFICATE_OR_EXECUTABLE_BOUND",
            "first because 958 marks it as the central second-order blocker",
        ),
        (
            "R11X1964_1_Ricci_Weyl_square",
            "Ricci-square or Weyl-square spin-2 correction",
            "high",
            "c_Ricci2; c_Weyl2; ghost/mass scale; weak-field potential signs; light-bending and PPN map",
            "MISSING_COEFFICIENT_AND_STABILITY_MAP",
            "needed if second-order theorem fails",
        ),
        (
            "R11X1964_2_nonlocal_memory_kernel",
            "nonlocal or memory kernel in local exterior",
            "high",
            "kernel norm; support scale; time-scale; local-vacuum silence certificate; Gdot/PPN/R10 projection",
            "MISSING_KERNEL_ZERO_OR_BOUND",
            "keeps MTS memory from being hidden dark-sector stress",
        ),
        (
            "R11X1964_3_Xi_extra_stress",
            "extra MTS sector exterior stress",
            "high",
            "Xi stress tensor; no-hair or compact-support condition; boundary flux; source coupling; PPN projection",
            "MISSING_NO_EXTRA_SECTOR_THEOREM",
            "directly decides whether local exterior is metric-only",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, family, priority, required_inputs, status, reason in entries:
        row = base(row_id)
        row.update(
            {
                "family": family,
                "priority": priority,
                "required_inputs": required_inputs,
                "status": status,
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1964_0_coframe_language", "Coframe language has prior MTS readout support.", "PASS_NONCLAIM", "support is not derivation"),
        ("CG1964_1_coframe_legitimacy", "Owned coframe is fully derived from MTS parent variables.", "FAIL_BLOCKED", "E[q(Phi_MTS)] not written"),
        ("CG1964_2_LC_branch", "LC/no-hypermomentum branch is canonical.", "FAIL_BLOCKED", "ACT1963 not adopted into parent action"),
        ("CG1964_3_EH_second_order", "Second-order EH operator selected.", "FAIL_BLOCKED", "R2/fR and extra-sector families remain legal"),
        ("CG1964_4_Newton", "Newtonian mechanics derived with measured GM.", "FAIL_BLOCKED", "EH and GM-transfer gates remain"),
        ("CG1964_5_R11_executable", "R11 residual vector is executable.", "FAIL_BLOCKED", "schemas only, no coefficients/projections"),
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
            "DEC1964_0_verdict",
            "COFRAME_BRANCH_REMAINS_BEST_ROUTE_BUT_NOT_FULLY_LEGITIMIZED",
            "There is prior coframe/readout support, but a parent map e_obs=E[q(Phi_MTS)] is still missing.",
            "keep ACT1963 alive as the leading branch, not as a final claim",
        ),
        (
            "DEC1964_1_next",
            "ATTACK_SECOND_ORDER_R11_FORK",
            "Once LC is conditionally solved, the central obstruction is higher-curvature/nonlocal/extra-sector operator freedom.",
            "try R2/fR zero proof first; if it fails, make executable bound rows",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1964_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1965-Y5-R2FR-R2-fR-zero-proof-or-executable-R11-bound-row.md",
            "target_script": "scripts/Y5_R2FR_R2_fR_zero_proof_or_executable_R11_bound_row_1965.py",
            "objective": "try to derive why R2/fR scalar higher-curvature terms vanish in the local exterior; if not, stage executable R11 bound rows",
            "acceptance_output": "second-order zero certificate for R2/fR or source-ready c_R2/f_RR alpha(lambda)/PPN schema",
            "nonclaim_rule": "no EH/Newton claim while R11 zero/bound rows remain missing",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1964_0_project_position")
    row.update(
        {
            "strongest_result": "The owned coframe branch is not arbitrary: older observer-map work already demanded a common coframe, but MTS still needs a parent map E[q(Phi_MTS)].",
            "what_improved": "We separated the GR-insertion risk from the real EH blocker; the next hard problem is now the second-order/R11 operator fork.",
            "still_missing": "E[q(Phi_MTS)] derivation, canonical ACT1963 adoption, R2/fR zero or bound, extra-sector silence, GM transfer, PPN closure",
            "claim_status": "conditional branch plus explicit next obstruction; no local-GR/Newton claim",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1964_SOURCE_REGISTER.csv",
    "coframe_legitimacy": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1964_COFRAME_LEGITIMACY_GATE.csv",
    "eh_second_order": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1964_EH_SECOND_ORDER_GATE.csv",
    "r11_interface": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1964_R11_EXECUTABLE_INTERFACE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1964_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1964_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1964_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1964_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "OWNED_COFRAME_LEGITIMACY_1964_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1964_R2_FR_SECOND_ORDER_R11_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1964_0_nonclaim_weight"),
            "artifact": "1964 owned-coframe legitimacy and EH second-order gate",
            "weight": "BRANCH_LEGITIMACY_PARTIAL_NEXT_BLOCKER_R11",
            "reason": "coframe language has prior support but parent derivation and R11 zero/bounds remain missing",
        }
    ]
    queue = [
        {
            **base("AQ1964_0_R2_fR"),
            "target": "R2/fR scalar mode zero or bound",
            "needed_inputs": "coefficient;mass/range;coupling;weak-field alpha(lambda);PPN map;source path",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1964_1_E_map"),
            "target": "e_obs=E[q(Phi_MTS)] parent map",
            "needed_inputs": "motion-time-space readout fields; nondegeneracy; Lorentz gauge; universal matter/readout use",
            "priority": "PARALLEL_HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "coframe_legitimacy": coframe_legitimacy_rows(),
        "eh_second_order": eh_second_order_rows(),
        "r11_interface": r11_interface_rows(),
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
    patterns = ("1964-", "*_1964_*", "*Y5*1964*", "*VAL1964*", "*P8*1964*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1964_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    support_ok = any(row["row_id"] == "LEG1964_1_operational_support" and row["status"] == "SOURCE_SUPPORT_FOR_COFRAME_LANGUAGE" for row in tables["coframe_legitimacy"])
    risk_ok = any(row["row_id"] == "LEG1964_0_risk" and row["status"] == "GR_INSERTION_RISK_EXPLICIT" for row in tables["coframe_legitimacy"])
    rows.append(validation_row("VAL1964_01_coframe_support_and_risk", "PASS" if support_ok and risk_ok else "FAIL", "coframe support and GR-insertion risk both retained"))

    scalar_ok = any(row["row_id"] == "LEG1964_2_not_four_scalar_gradients" and row["status"] == "SCALAR_GRADIENT_ROUTE_TOO_RESTRICTIVE" for row in tables["coframe_legitimacy"])
    rows.append(validation_row("VAL1964_02_scalar_gradient_guard", "PASS" if scalar_ok else "FAIL", "four-scalar-gradient shortcut rejected"))

    eh_block_ok = any(row["row_id"] == "EH2_1964_2_central_blocker" and row["status"] == "SECOND_ORDER_NOT_DERIVED" for row in tables["eh_second_order"])
    rows.append(validation_row("VAL1964_03_second_order_blocker", "PASS" if eh_block_ok else "FAIL", "second-order blocker retained"))

    r11_ok = any(row["row_id"] == "R11X1964_0_R2_fR_scalar" and row["status"] == "MISSING_ZERO_CERTIFICATE_OR_EXECUTABLE_BOUND" for row in tables["r11_interface"])
    rows.append(validation_row("VAL1964_04_r11_interface", "PASS" if r11_ok else "FAIL", "R2/fR R11 interface staged"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1964_3_EH_second_order" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1964_05_claim_gates", "PASS" if gate_ok else "FAIL", "no local-GR claim promoted"))

    decision_ok = any(row["decision"] == "ATTACK_SECOND_ORDER_R11_FORK" for row in tables["decision"])
    rows.append(validation_row("VAL1964_06_decision", "PASS" if decision_ok else "FAIL", "R11 second-order fork selected"))

    next_ok = tables["next"][0]["target_doc"] == "1965-Y5-R2FR-R2-fR-zero-proof-or-executable-R11-bound-row.md"
    rows.append(validation_row("VAL1964_07_next_target", "PASS" if next_ok else "FAIL", "1965 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1964_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1964_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1964_10_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1964_11_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1964_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1964_OVERALL", overall, "1964 owned-coframe legitimacy and EH second-order gate"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Coframe Legitimacy Gate", tables["coframe_legitimacy"]),
        ("EH Second-Order Gate", tables["eh_second_order"]),
        ("R11 Executable Interface", tables["r11_interface"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1964 Y5 R2FR: Owned-Coframe Legitimacy And EH Second-Order Gate",
        "",
        "Private checkpoint. This asks the dangerous question directly: is the owned coframe a legitimate MTS readout object, or did the branch merely import GR geometry?",
        "",
        "Verdict: the coframe branch has real prior support in the corpus because observer/readout work already required a local coframe and universal matter coframe. It is still not fully derived because the parent map `e_obs=E[q(Phi_MTS)]` is missing.",
        "",
        "The next hard obstruction is no longer the independent connection. It is the EH second-order/no-extra-sector fork: either prove higher-curvature and extra-sector terms vanish locally, or make R11 residual rows executable.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1964_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
