from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_VERTICAL_NOETHER_CHARGE_QV_AND_TYPED_TARGET_EXCLUSION_OR_BALPHA_BG_SOURCE_ROW_2435"
CHECKPOINT_ID = "2435"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2435-Y5-R2FR-vertical-Noether-charge-Qv-and-typed-target-exclusion-or-balpha-bg-source-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2435_SOURCE_REGISTER.csv",
    "qv_extraction": OUT / "P8_Y5_PARENT_QLOC_2435_VERTICAL_QV_EXTRACTION_TEST.csv",
    "target_exclusion": OUT / "P8_Y5_PARENT_QLOC_2435_TYPED_TARGET_EXCLUSION_TEST.csv",
    "joint_owner": OUT / "P8_Y5_PARENT_QLOC_2435_JOINT_OWNER_DECISION.csv",
    "source_row": OUT / "P8_Y5_PARENT_QLOC_2435_BALPHA_BG_SOURCE_ROW_NONCLAIM.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2435_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2435_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2435_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2435_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2435_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_qv": QUEUE / "JR2435_QV_EXTRACTION_TEST_NONCLAIM.csv",
    "queue_source_row": QUEUE / "JR2435_BALPHA_BG_SOURCE_ROW_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "qv_target_exclusion_source_row_nonclaim_2435.csv",
    "beta_docs": BETA_DOCS / "BALPHA_BG_SOURCE_ROW_2435_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2435_00_2434_handoff",
        "source_path": ROOT / "2434-Y5-R2FR-parent-typed-object-language-and-vertical-basis-certificate-or-balpha-bg-bound-row.md",
        "needles": ["NEXT2434_0_selected", "OWN2434_4_verdict", "VAL2434_OVERALL"],
        "role": "fresh handoff selecting vertical Q_v plus typed target exclusion or b_alpha/b_g source row",
    },
    {
        "source_id": "SRC2435_01_2434_validation",
        "source_path": OUT / "P8_Y5_BRR545_2434_VALIDATION.csv",
        "needles": ["VAL2434_OVERALL", "PASS"],
        "role": "confirms 2434 passed before 2435",
    },
    {
        "source_id": "SRC2435_02_2434_bound_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2434_BALPHA_BG_BOUND_ROW_CONTRACT.csv",
        "needles": ["BND2434_0_b_alpha", "BND2434_1_b_g"],
        "role": "b_alpha/b_g source-row contract input",
    },
    {
        "source_id": "SRC2435_03_2393_qv",
        "source_path": ROOT / "2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md",
        "needles": ["VNC2393_5_verdict", "VQC2393_4_Qv", "VQL2393_0_kernel_charge"],
        "role": "vertical Noether charge extraction precedent",
    },
    {
        "source_id": "SRC2435_04_1220_typed",
        "source_path": ROOT / "1220-Y5-R10-parent-typed-object-language-signature-or-finite-coupling-closure.md",
        "needles": ["PTOL1220_7_verdict", "FCCR1220_0_alpha", "VAL1220_16_overall"],
        "role": "typed object-language and finite alpha closure debt precedent",
    },
    {
        "source_id": "SRC2435_05_1219_counter",
        "source_path": ROOT / "1219-Y5-R10-typed-visible-coefficient-functor-or-hidden-scalar-counterexample-lock.md",
        "needles": ["HSC1219_1_alpha", "HSC1219_4_source_weight", "VAL1219_16_overall"],
        "role": "hidden alpha/source-weight counterexample lock",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def qv_extraction_rows() -> list[dict[str, Any]]:
    rows = [
        ("QV2435_0_parent_variation", "parent variation identity", "delta L_parent = E_A delta Phi^A + dTheta_parent(Phi;delta Phi)", "MISSING_TOTAL_PARENT_ACTION_AND_THETA", "without Theta_parent no Q_v is owned"),
        ("QV2435_1_vertical_generator", "vertical generator action", "v_epsilon must act on metric/coframe, q-sector, matter, projector, boundary/reference and readout fields", "MISSING_ALL_FIELD_VERTICAL_GENERATOR", "cannot test kernel charge or DObs_coeff"),
        ("QV2435_2_noether_current", "vertical Noether current", "J_v := Theta_parent(v_epsilon)-mu_v with delta_v L_parent=dmu_v+E_A v^A", "MISSING_MU_V_AND_CURRENT", "current is formal only"),
        ("QV2435_3_charge_form", "vertical charge form", "J_v=dQ_v+C_v and Q_v splits into EH/reference, matter/source, extra/residual, projector and boundary pieces", "MISSING_QV_SECTOR_SPLIT", "piece leakage cannot be audited"),
        ("QV2435_4_zero_compact_flux", "kernel Hamiltonian zero", "integral_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece)=0 on allowed compact local surfaces", "MISSING_ZERO_FLUX_CERTIFICATE", "kernel can carry physical charge"),
        ("QV2435_5_verdict", "vertical Q_v extraction status", "Q_v zero is not extracted for current MTS; only the formal charge contract is available", "QV_ZERO_NOT_PROVED", "epsilon_kernel_charge remains live"),
    ]
    return [
        base_row(test_id=test_id, object=obj, required_formula=formula, current_status=status, consequence=consequence, gate_pass=False)
        for test_id, obj, formula, status, consequence in rows
    ]


def target_exclusion_rows() -> list[dict[str, Any]]:
    rows = [
        ("TEX2435_0_hidden_scalar", "hidden scalar to visible coefficient", "Hom(I_hid, c_alpha/c_matter/c_clock)=empty by parent type, or I_hid is quotient-constant", "HIDDEN_SCALAR_TARGET_NOT_EXCLUDED", "b_alpha and material/clock drifts remain live"),
        ("TEX2435_1_source_prefactor", "source-only active weight", "Hom(source/species label, R_+^active prefactor)=empty except common calibration", "SOURCE_PREFACTOR_TARGET_NOT_EXCLUDED", "Delta_w/source_norm remains live"),
        ("TEX2435_2_shadow_frame", "shadow Weyl/disformal frame", "frame target excludes q representative labels or proves b_g=0/basic coframe", "SHADOW_FRAME_TARGET_NOT_EXCLUDED", "b_g remains live"),
        ("TEX2435_3_readout_reentry", "readout/effective coefficient target", "S_eff, clocks, detectors and source-worldtube readouts preserve the same q-blind target category", "READOUT_TARGET_NOT_EXCLUDED", "readout tails remain live"),
        ("TEX2435_4_verdict", "typed target exclusion status", "target exclusion is exact as a type rule but not parent-signed; counterexamples remain legal", "TYPED_TARGET_EXCLUSION_NOT_PROVED", "finite coefficient rows remain mandatory"),
    ]
    return [
        base_row(test_id=test_id, target=target, exclusion_rule=rule, current_status=status, consequence=consequence, gate_pass=False)
        for test_id, target, rule, status, consequence in rows
    ]


def joint_owner_rows() -> list[dict[str, Any]]:
    return [
        base_row(owner_id="JOINT2435_0_if_both_close", condition="Q_v compact charge zero and typed target exclusion both close", implication="q vertical kernel is gauge/null for coefficient channels; b_alpha/b_g/source-prefactor slopes vanish by chain rule", current_status="CONDITIONAL_ROUTE_READY", claim_allowed_now=False),
        base_row(owner_id="JOINT2435_1_Qv_fails", condition="Q_v zero not extracted", implication="kernel may carry physical Hamiltonian/boundary charge; do not call it gauge", current_status="CURRENT_BRANCH", claim_allowed_now=False),
        base_row(owner_id="JOINT2435_2_target_fails", condition="typed target exclusion not parent-signed", implication="hidden scalar/source-prefactor/shadow-frame coefficient maps remain legal", current_status="CURRENT_BRANCH", claim_allowed_now=False),
        base_row(owner_id="JOINT2435_3_fallback", condition="either owner lock fails", implication="stage b_alpha/b_g finite coefficient row as nonclaim and source-backed only when real inputs exist", current_status="NONCLAIM_SOURCE_ROW_STAGED", claim_allowed_now=False),
        base_row(owner_id="JOINT2435_4_verdict", condition="current MTS", implication="both hard locks remain open; no J_q=0/local-GR promotion", current_status="FAIL_CURRENT_CLAIM_OWNER_LOCKS_OPEN", claim_allowed_now=False),
    ]


def source_row_rows() -> list[dict[str, Any]]:
    rows = [
        ("SRCROW2435_0_b_alpha_candidate", "b_alpha", "vertical derivative of EM/gauge kinetic or fine-structure coefficient", "dimensionless_or_per_q_unit", "clocks;WEP;R10;EM", "hidden-visible alpha counterexample locked; 1220 carries finite closure debt threshold candidate but not a source-backed claim", "threshold_candidate_from_1220_nonclaim", "MISSING_REAL_SOURCE_OR_THEOREM_ZERO"),
        ("SRCROW2435_1_b_g_candidate", "b_g", "universal Weyl/shadow-frame slope in e_obs=exp(b_g q)e_basic", "dimensionless_or_per_q_unit", "R10;PPN;WEP;clock", "tests shadow-frame leakage; exchange accounting must be quadratic/product-law when universal", "no_numeric_bound_available", "MISSING_REAL_SOURCE_OR_THEOREM_ZERO"),
        ("SRCROW2435_2_required_provenance", "source_row_required_fields", "symbol, definition, q normalization, units, source URL/path, extraction method, uncertainty, projection matrix, arena support, no-cancellation group", "schema", "all_local_arenas", "row cannot score with MISSING markers or without source-backed value/theorem-zero", "not_applicable", "SCHEMA_READY_NONCLAIM"),
        ("SRCROW2435_3_verdict", "first b_alpha/b_g source row", "source-row skeleton only; no real coefficient value is filled at 2435", "n/a", "all_local_arenas", "next step should either source real b_alpha/b_g constraints or continue Q_v/typed owner derivation", "not_applicable", "NONCLAIM_NO_VALUE_FILLED"),
    ]
    return [
        base_row(row_id=row_id, symbol=symbol, definition=definition, units=units, observable_links=links, rationale=rationale, source_status=source_status, current_status=status, theorem_zero=False, source_backed=False, score_ready=False)
        for row_id, symbol, definition, units, links, rationale, source_status, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(claim_id="CGATE2435_0_Qv_zero", claim="vertical Q_v charge vanishes", gate_pass=False, reason="Theta_parent, all-field v, mu_v, Q_v, sector split and zero compact flux are missing"),
        base_row(claim_id="CGATE2435_1_target_exclusion", claim="typed target exclusion forbids hidden/source coefficient maps", gate_pass=False, reason="hidden scalar, source prefactor, shadow frame and readout reentry targets remain legal countermodels"),
        base_row(claim_id="CGATE2435_2_Jq_zero", claim="J_q coefficient channels vanish", gate_pass=False, reason="requires both Q_v/vertical kernel and target exclusion locks"),
        base_row(claim_id="CGATE2435_3_balpha_bg_score", claim="b_alpha/b_g source row can score", gate_pass=False, reason="rows are nonclaim skeletons; no real source-backed coefficient value or theorem-zero proof"),
        base_row(claim_id="CGATE2435_4_local_GR", claim="local GR/Newton reduction follows", gate_pass=False, reason="q no-hair, J_q, boundary/source and PPN gates remain open"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2435_0_Qv", decision="QV_EXTRACTION_NOT_CLOSED", rationale="formal Noether charge contract exists but no parent Theta/Q_v/zero-flux extraction", consequence="kernel cannot be called gauge by name"),
        base_row(decision_id="DEC2435_1_target", decision="TYPED_TARGET_EXCLUSION_NOT_CLOSED", rationale="hidden scalar/source-prefactor/shadow/readout maps remain legal without parent grammar signature", consequence="coefficient drift rows remain live"),
        base_row(decision_id="DEC2435_2_fallback", decision="STAGE_BALPHA_BG_SOURCE_ROW_NONCLAIM", rationale="these are highest-leverage finite coefficients for EM/clocks/WEP/R10/frame leakage", consequence="requires real source acquisition before scoring"),
        base_row(decision_id="DEC2435_3_next", decision="MOVE_TO_REAL_SOURCE_OR_QV_PIECE_LEDGER", rationale="another abstract restatement has diminishing return; next progress is piece ledger or actual coefficient source", consequence="select 2436"),
        base_row(decision_id="DEC2435_4_public", decision="NO_GITHUB_ACTION", rationale="private owner/source gate only", consequence="continue private framework work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2435_0_selected",
            selection_status="selected",
            target_file="2436-Y5-R2FR-Qv-sector-piece-ledger-or-real-balpha-bg-source-acquisition.md",
            target_script="scripts/Y5_R2FR_Qv_sector_piece_ledger_or_real_balpha_bg_source_acquisition_2436.py",
            task="either build a sector-by-sector Q_v piece ledger from available parent action terms, or acquire real source-backed b_alpha/b_g bound inputs for a nonclaim finite coefficient row",
            acceptance_target="Q_v piece ledger identifies exact missing parent sectors, or b_alpha/b_g row gets source path/units/projection/provenance with valid_for_claim=false",
            guardrails="do not invent Q_v pieces or coefficient values, use projection-by-declaration, cancel components, claim local GR/R10/PPN/WEP/clock/orbital pass, edit formalization-workbench, or push GitHub",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_qv", OUTPUTS["qv_extraction"], COPY_TARGETS["queue_qv"], "vertical Q_v extraction nonclaim queue"),
        ("queue_source_row", OUTPUTS["source_row"], COPY_TARGETS["queue_source_row"], "b_alpha/b_g source row nonclaim queue"),
        ("branch_wep", OUTPUTS["joint_owner"], COPY_TARGETS["branch_wep"], "Q_v and target exclusion owner status for WEP/local branch"),
        ("beta_docs", OUTPUTS["source_row"], COPY_TARGETS["beta_docs"], "b_alpha/b_g source row for beta docs"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target, note in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=source, target_path=target, source_exists=source.exists(), target_exists=target.exists(), notes=note))
    return rows


def validation_rows(all_outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_rows = all_outputs["source_register"]
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_hits: list[Path] = []
    for pattern in ["*2435-Y5-R2FR*", "*P8_Y5_PARENT_QLOC_2435*", "*P8_Y5_BRR545_2435*", "*JR2435*", "*BALPHA_BG_SOURCE_ROW_2435*"]:
        formalization_hits.extend(FORMALIZATION.rglob(pattern) if FORMALIZATION.exists() else [])

    checks = [
        ("VAL2435_00_sources_exist", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2435_01_source_needles", all(row["needles_found"] for row in source_rows), "all cited source needles are present"),
        ("VAL2435_02_Qv_not_proved", any(row["test_id"] == "QV2435_5_verdict" and row["current_status"] == "QV_ZERO_NOT_PROVED" for row in all_outputs["qv_extraction"]), "Q_v zero is not overclaimed"),
        ("VAL2435_03_target_not_proved", any(row["test_id"] == "TEX2435_4_verdict" and row["current_status"] == "TYPED_TARGET_EXCLUSION_NOT_PROVED" for row in all_outputs["target_exclusion"]), "typed target exclusion is not overclaimed"),
        ("VAL2435_04_joint_owner_blocked", any(row["owner_id"] == "JOINT2435_4_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_OWNER_LOCKS_OPEN" for row in all_outputs["joint_owner"]), "joint owner locks remain open"),
        ("VAL2435_05_source_rows_nonclaim", all(not row["theorem_zero"] and not row["source_backed"] and not row["score_ready"] for row in all_outputs["source_row"]), "b_alpha/b_g source rows remain nonclaim skeletons"),
        ("VAL2435_06_claims_blocked", all(not row["gate_pass"] for row in all_outputs["claim_gates"]), "all claim gates remain false"),
        ("VAL2435_07_next_target_written", any(row["route_id"] == "NEXT2435_0_selected" for row in all_outputs["next_target"]), "next target selected"),
        ("VAL2435_08_branch_copies", all(row["target_exists"] for row in all_outputs["branch_copies"]), "branch copies were written"),
        ("VAL2435_09_no_formalization_artifacts", len(formalization_hits) == 0, "no 2435 artifacts were written to formalization-workbench"),
    ]
    for check_id, passed, notes in checks:
        rows.append(base_row(check_id=check_id, status="PASS" if passed else "FAIL", notes=notes, detail="" if passed else "required checkpoint condition failed"))
    for path in output_csvs:
        parses, row_count, message = csv_parses(path)
        rows.append(base_row(check_id=f"VAL2435_CSV_{path.stem}", status="PASS" if parses and row_count > 0 else "FAIL", notes=f"CSV parses with {row_count} rows", detail=message))
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            check_id="VAL2435_OVERALL",
            status="PASS" if overall else "FAIL",
            notes="2435 tests vertical Q_v extraction and typed target exclusion directly, refuses both owner claims, stages nonclaim b_alpha/b_g source-row skeletons, and selects Q_v sector piece ledger or real coefficient source acquisition next",
            detail="",
        )
    )
    return rows


def write_markdown(all_outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2435 - Y5/R2FR Vertical Noether Charge Qv And Typed Target Exclusion Or b_alpha/b_g Source Row",
        "",
        "## Result",
        "- 2435 attacks the two hard locks directly: vertical Noether charge `Q_v` and typed target exclusion.",
        "- `Q_v` is not extracted: the parent action, `Theta_parent`, all-field vertical generator, `mu_v`, sector split, and zero compact flux certificate are still missing.",
        "- Typed target exclusion is not proved: hidden scalar, source-prefactor, shadow-frame and readout-reentry targets remain legal countermodels.",
        "- Therefore `J_q=0`, local-GR/Newton, R10, PPN, WEP, clock and orbital claims stay blocked.",
        "- The fallback is now concrete: source a real `b_alpha` or `b_g` row, but 2435 only stages nonclaim source-row skeletons.",
        "",
        "## Practical Status",
        "This is the point where theory and data start to meet again: either extract actual `Q_v` pieces from the parent action, or stop abstracting and source a real coefficient bound.",
        "",
        "## Source Register",
        table(["source_id", "source_path", "path_exists", "needles_found", "role"], all_outputs["source_register"]),
        "",
        "## Vertical Q_v Extraction Test",
        table(["test_id", "object", "required_formula", "current_status", "consequence", "gate_pass", "valid_for_claim"], all_outputs["qv_extraction"]),
        "",
        "## Typed Target Exclusion Test",
        table(["test_id", "target", "exclusion_rule", "current_status", "consequence", "gate_pass", "valid_for_claim"], all_outputs["target_exclusion"]),
        "",
        "## Joint Owner Decision",
        table(["owner_id", "condition", "implication", "current_status", "claim_allowed_now", "valid_for_claim"], all_outputs["joint_owner"]),
        "",
        "## b_alpha / b_g Source Row Skeleton",
        table(["row_id", "symbol", "definition", "units", "observable_links", "rationale", "source_status", "current_status", "source_backed", "score_ready", "valid_for_claim"], all_outputs["source_row"]),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], all_outputs["claim_gates"]),
        "",
        "## Decisions",
        table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], all_outputs["decisions"]),
        "",
        "## Next Target",
        table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], all_outputs["next_target"]),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], all_outputs["branch_copies"]),
        "",
        "## Validation",
        table(["check_id", "status", "notes", "detail"], all_outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        path.mkdir(parents=True, exist_ok=True)

    all_outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "qv_extraction": qv_extraction_rows(),
        "target_exclusion": target_exclusion_rows(),
        "joint_owner": joint_owner_rows(),
        "source_row": source_row_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in all_outputs.items():
        write_csv(OUTPUTS[key], rows)

    all_outputs["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], all_outputs["branch_copies"])
    all_outputs["validation"] = validation_rows(all_outputs)
    write_csv(OUTPUTS["validation"], all_outputs["validation"])
    write_markdown(all_outputs)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    print(DOC)
    print(OUTPUTS["validation"])
    print(f"VAL2435_OVERALL={all_outputs['validation'][-1]['status']}")


if __name__ == "__main__":
    main()
