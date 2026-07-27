from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_MTS_TO_DD_CHARGE_MAP_OR_WEP_SOURCE_LEG_OWNER_2441"
CHECKPOINT_ID = "2441"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2441-Y5-R2FR-MTS-to-DD-charge-map-or-WEP-source-leg-owner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2441_SOURCE_REGISTER.csv",
    "dd_map": OUT / "P8_Y5_PARENT_QLOC_2441_MTS_TO_DD_CHARGE_MAP.csv",
    "mass_gap": OUT / "P8_Y5_PARENT_QLOC_2441_MASS_SECTOR_GAP_LEDGER.csv",
    "wep_reduced_formula": OUT / "P8_Y5_PARENT_QLOC_2441_WEP_REDUCED_FORMULA_NONCLAIM.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2441_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2441_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2441_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2441_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2441_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_dd_map": QUEUE / "JR2441_MTS_TO_DD_CHARGE_MAP_NONCLAIM.csv",
    "queue_mass_gap": QUEUE / "JR2441_MASS_SECTOR_GAP_LEDGER_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "MTS_to_DD_charge_map_nonclaim_2441.csv",
    "beta_docs": BETA_DOCS / "MTS_TO_DD_CHARGE_MAP_2441_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2441_00_2440_handoff",
        "source_path": ROOT / "2440-Y5-R2FR-WEP-K-vector-material-source-charge-sensitivity-or-deltaw-bound-row.md",
        "needles": ["NEXT2440_0_selected", "WKP2440_0_DD_material_formula", "WB2440_0_MTS_to_DD_map", "VAL2440_OVERALL"],
        "role": "fresh handoff selecting MTS-to-DD charge map/source leg",
    },
    {
        "source_id": "SRC2441_01_2440_projection_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv",
        "needles": ["WKP2440_1_MTS_expanded_formula", "D_mhat_source", "D_e_source"],
        "role": "current WEP projection formulas",
    },
    {
        "source_id": "SRC2441_02_2439_basis",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2439_COUPLING_COMPONENT_BASIS.csv",
        "needles": ["delta_w_block", "b_alpha", "b_g", "c_projector"],
        "role": "current MTS coupling component basis",
    },
    {
        "source_id": "SRC2441_03_2440_material",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
        "needles": ["WMS2440_2_Pt_minus_Ti", "3.330000e-03", "2.040000e-03"],
        "role": "source-backed Ti/Pt DD material contrast",
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


def dd_map_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "map_id": "DDMAP2441_0_b_alpha_to_De",
            "mts_component": "b_alpha",
            "dd_target": "D_e_source",
            "map_formula": "D_e_source = S_E^q * b_alpha, if q is the DD-like scalar/vertical drive and alpha_EM(q)=alpha_0 exp(b_alpha q)",
            "required_owner": "q normalization; Earth/source scalar leg S_E^q; EM coefficient target owner; no readout reentry",
            "map_status": "CONDITIONAL_FORMULA_SOURCE_LEG_MISSING",
            "partial_success": True,
        },
        {
            "map_id": "DDMAP2441_1_missing_b_mhat",
            "mts_component": "b_mhat_or_b_nuclear",
            "dd_target": "D_mhat_source",
            "map_formula": "D_mhat_source = S_E^q * b_mhat, where b_mhat = partial ln(mhat/Lambda_QCD or nuclear binding scale)/partial q",
            "required_owner": "mass/quark/nuclear-binding coefficient in the parent matter action",
            "map_status": "MTS_COMPONENT_NOT_IN_CURRENT_BASIS",
            "partial_success": False,
        },
        {
            "map_id": "DDMAP2441_2_delta_w_block_direct",
            "mts_component": "delta_w_block",
            "dd_target": "direct_active_source_weight",
            "map_formula": "delta_w_block contributes directly to eta only if Ti/Pt occupy distinct ordinary exchange/source blocks or if source-weight labels survive the parent source functor",
            "required_owner": "ordinary exchange graph; label-forgetting/source functor; block basis for test masses and Earth source",
            "map_status": "NOT_DD_CHARGE_DIRECT_COUNTERMODEL_CHANNEL",
            "partial_success": False,
        },
        {
            "map_id": "DDMAP2441_3_delta_w_shadow_direct",
            "mts_component": "delta_w_shadow",
            "dd_target": "source_shadow_weight",
            "map_formula": "delta_w_shadow contributes through J_shadow, not through the ordinary DD material charges, unless the shadow current is reduced to an effective material charge basis",
            "required_owner": "source-shadow basis; projection of J_shadow onto Ti/Pt/Earth material charges",
            "map_status": "NOT_DD_CHARGE_SHADOW_CHANNEL_RETAINED",
            "partial_success": False,
        },
        {
            "map_id": "DDMAP2441_4_b_g",
            "mts_component": "b_g",
            "dd_target": "frame_or_metric_response",
            "map_formula": "b_g is primarily a frame/PPN/clock response; it is WEP-active only through material-standard or hidden-visible reentry not yet parent-owned",
            "required_owner": "basic coframe theorem or material-standard response coefficient",
            "map_status": "NO_DIRECT_DD_WEP_MAP",
            "partial_success": False,
        },
        {
            "map_id": "DDMAP2441_5_verdict",
            "mts_component": "current_MTS_basis",
            "dd_target": "DD_two_charge_WEP_map",
            "map_formula": "Only the b_alpha -> D_e channel has a clean conditional map; the dominant nuclear/mass D_mhat channel requires a new/owned b_mhat-like coefficient or a theorem that it is zero.",
            "required_owner": "b_mhat zero theorem or b_mhat coefficient row; source leg S_E^q",
            "map_status": "PARTIAL_MAP_EXPOSES_MASS_SECTOR_GAP",
            "partial_success": False,
        },
    ]
    return [base_row(**row, score_ready=False) for row in rows]


def mass_gap_rows() -> list[dict[str, Any]]:
    rows = [
        ("MSG2441_0_b_mhat", "b_mhat", "partial ln(mhat/Lambda_QCD or average light-quark mass ratio)/partial q", "needed for D_mhat_source and Ti/Pt nuclear binding sensitivity", "MISSING_COMPONENT"),
        ("MSG2441_1_b_bind", "b_bind", "partial ln nuclear binding energy coefficients with respect to q", "needed if MTS modifies nuclear binding rather than quark masses directly", "MISSING_COMPONENT"),
        ("MSG2441_2_b_me", "b_me", "partial ln electron mass/material standard with respect to q", "subdominant DD charge but relevant to clocks/material standards", "NOT_IN_CURRENT_BASIS"),
        ("MSG2441_3_source_leg", "S_E^q", "Earth/source scalar or vertical drive leg multiplying coefficient slopes", "needed before b_alpha or b_mhat becomes a WEP source parameter", "MISSING_SOURCE_OWNER"),
        ("MSG2441_4_zero_route", "mass-sector zero theorem", "prove all mass/nuclear coefficients are fixed representation/superselection data q-blind", "alternative to adding b_mhat rows", "UNSIGNED"),
    ]
    return [
        base_row(
            gap_id=gap_id,
            missing_symbol=symbol,
            definition=definition,
            why_needed=why,
            current_status=status,
        )
        for gap_id, symbol, definition, why, status in rows
    ]


def wep_reduced_formula_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "formula_id": "WRF2441_0_reduced_DD_MTS",
            "formula": "eta_TiPt ~= DeltaQ_mhat*S_E^q*b_mhat + DeltaQ_e*S_E^q*b_alpha + direct_delta_w_block + direct_delta_w_shadow + projector_tail_abs",
            "known_inputs": "DeltaQ_mhat=3.33e-3; DeltaQ_e=2.04e-3; eta_bound=2.745906e-15",
            "unknown_inputs": "S_E^q;b_mhat;b_alpha parent owner;direct_delta_w_block;direct_delta_w_shadow;projector_tail_abs",
            "use_status": "REDUCED_FORMULA_READY_NONCLAIM",
        },
        {
            "formula_id": "WRF2441_1_if_bmhat_zero",
            "formula": "If b_mhat=0, delta_w_block=0, delta_w_shadow=0, projector_tail=0 and S_E^q is known, MICROSCOPE gives |S_E^q*b_alpha| <= eta_bound/DeltaQ_e.",
            "known_inputs": "one-component smoke scale from 2440: 1.346032e-12",
            "unknown_inputs": "all zero premises plus S_E^q",
            "use_status": "ALPHA_ONLY_ROUTE_CONDITIONAL_TOO_STRONG_FOR_CURRENT_CORPUS",
        },
        {
            "formula_id": "WRF2441_2_if_alpha_zero",
            "formula": "If b_alpha=0 and all direct source/shadow/projector tails vanish, MICROSCOPE gives |S_E^q*b_mhat| <= eta_bound/DeltaQ_mhat.",
            "known_inputs": "one-component smoke scale from 2440: 8.245964e-13",
            "unknown_inputs": "b_mhat owner and source leg",
            "use_status": "MASS_CHANNEL_BOUND_ROUTE_IF_COMPONENT_EXISTS",
        },
        {
            "formula_id": "WRF2441_3_no_cancellation",
            "formula": "|DeltaQ_mhat*S_E^q*b_mhat| + |DeltaQ_e*S_E^q*b_alpha| + |direct_delta_w_block| + |direct_delta_w_shadow| + |projector_tail_abs| <= eta_bound",
            "known_inputs": "material contrasts and eta bound",
            "unknown_inputs": "all component magnitudes",
            "use_status": "NO_CANCELLATION_ENVELOPE_ONLY",
        },
    ]
    return [base_row(**row, score_ready=False) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2441_0_balpha_map", "b_alpha has conditional DD electromagnetic map", "PASS_NONCLAIM", "D_e_source=S_E^q*b_alpha if q/alpha/source-leg premises hold"),
        ("CG2441_1_Dmhat_map", "D_mhat_source is owned", "BLOCKED", "b_mhat/b_nuclear coefficient is missing from current MTS component basis"),
        ("CG2441_2_source_leg", "Earth/source leg S_E^q is owned", "BLOCKED", "source leg not derived"),
        ("CG2441_3_WEP_score", "MICROSCOPE WEP score can constrain MTS coefficients", "BLOCKED", "mass/source/direct-shadow channels remain open"),
        ("CG2441_4_local_GR", "WEP/local GR pass", "BLOCKED", "WEP branch remains a nonclaim partial map"),
    ]
    return [base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=status == "PASS_NONCLAIM") for claim_id, claim, status, reason in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2441_0_partial_map", "BALPHA_TO_DE_CONDITIONAL_MAP_ACCEPTED", "the EM/fine-structure channel has a clean DD analogue if q and source leg are owned", "keep b_alpha in WEP map but nonclaim"),
        ("DEC2441_1_mass_gap", "MASS_NUCLEAR_CHANNEL_IS_MISSING", "Ti/Pt WEP sensitivity is not alpha-only; the DD mass/nuclear charge contrast is larger than the EM contrast", "add/derive/prove-zero b_mhat or b_nuclear"),
        ("DEC2441_2_deltaw", "DELTAW_SHADOW_NOT_DD_CHARGE", "delta_w_block and delta_w_shadow are direct source-weight/shadow channels, not ordinary DD material charges", "do not fold them into D_mhat without theorem"),
        ("DEC2441_3_next", "TARGET_MASS_SECTOR_OWNER", "the highest-leverage next step is to derive b_mhat/b_nuclear or prove mass-sector q-blindness", "select 2442"),
        ("DEC2441_4_public", "NO_GITHUB_ACTION", "private WEP source-leg checkpoint only", "continue private framework work"),
    ]
    return [base_row(decision_id=row_id, decision=decision, rationale=rationale, consequence=consequence) for row_id, decision, rationale, consequence in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2441_0_selected",
            selection_status="selected",
            target_file="2442-Y5-R2FR-mass-sector-bmhat-owner-or-WEP-nuclear-binding-gap.md",
            target_script="scripts/Y5_R2FR_mass_sector_bmhat_owner_or_WEP_nuclear_binding_gap_2442.py",
            task="derive or prove zero the mass/quark/nuclear-binding coefficient b_mhat/b_nuclear that feeds D_mhat_source, while keeping b_alpha and direct delta_w/shadow channels separate",
            acceptance_target="mass-sector q-blind theorem closes, or b_mhat/b_nuclear becomes an explicit nonclaim coefficient row with units/source-leg/projection blockers",
            guardrails="do not pretend alpha-only closes WEP, do not fold source-shadow into DD charges by naming, do not invent source leg S_E^q, do not claim WEP/local GR, do not edit formalization-workbench, and do not push GitHub",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_dd_map", OUTPUTS["dd_map"], COPY_TARGETS["queue_dd_map"], "MTS-to-DD charge map nonclaim queue"),
        ("queue_mass_gap", OUTPUTS["mass_gap"], COPY_TARGETS["queue_mass_gap"], "mass-sector gap nonclaim queue"),
        ("branch_wep", OUTPUTS["wep_reduced_formula"], COPY_TARGETS["branch_wep"], "WEP reduced formula branch"),
        ("beta_docs", OUTPUTS["dd_map"], COPY_TARGETS["beta_docs"], "MTS-to-DD charge map for beta docs"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target, note in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=source,
                target_path=target,
                source_exists=source.exists(),
                target_exists=target.exists(),
                notes=note,
            )
        )
    return rows


def formalization_hits() -> list[Path]:
    patterns = [
        "*2441-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2441*",
        "*P8_Y5_BRR545_2441*",
        "*JR2441*",
        "*MTS_TO_DD_CHARGE_MAP_2441*",
    ]
    hits: list[Path] = []
    if not FORMALIZATION.exists():
        return hits
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return hits


def validation_rows(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = outputs["source_register"]
    rows.append(base_row(check_id="VAL2441_00_sources_exist", status="PASS" if all(row["path_exists"] == True for row in sources) else "FAIL", notes="all cited source paths exist"))
    rows.append(base_row(check_id="VAL2441_01_source_needles", status="PASS" if all(row["needles_found"] == True for row in sources) else "FAIL", notes="all cited source needles are present"))

    dd = outputs["dd_map"]
    rows.append(base_row(check_id="VAL2441_02_balpha_conditional_map", status="PASS" if any(row["map_id"] == "DDMAP2441_0_b_alpha_to_De" and row["partial_success"] == True for row in dd) else "FAIL", notes="b_alpha to D_e conditional map is present"))
    rows.append(base_row(check_id="VAL2441_03_mass_gap_detected", status="PASS" if any(row["map_id"] == "DDMAP2441_1_missing_b_mhat" and row["partial_success"] == False for row in dd) else "FAIL", notes="missing b_mhat mass-sector map is detected"))

    gaps = outputs["mass_gap"]
    rows.append(base_row(check_id="VAL2441_04_gap_rows_present", status="PASS" if any(row["missing_symbol"] == "b_mhat" for row in gaps) and any(row["missing_symbol"] == "S_E^q" for row in gaps) else "FAIL", notes="mass coefficient and source leg gaps are explicit"))

    formulas = outputs["wep_reduced_formula"]
    rows.append(base_row(check_id="VAL2441_05_no_cancellation_formula", status="PASS" if any(row["formula_id"] == "WRF2441_3_no_cancellation" for row in formulas) else "FAIL", notes="WEP no-cancellation reduced formula is present"))
    rows.append(base_row(check_id="VAL2441_06_formulas_nonclaim", status="PASS" if all(row["score_ready"] == False and row["valid_for_claim"] == False for row in formulas) else "FAIL", notes="reduced formulas are not score-ready"))

    claims = outputs["claim_gates"]
    rows.append(base_row(check_id="VAL2441_07_claims_blocked_except_balpha_map", status="PASS" if all((row["gate_status"] == "PASS_NONCLAIM") == (row["claim_id"] == "CG2441_0_balpha_map") for row in claims) else "FAIL", notes="only b_alpha conditional map passes as nonclaim"))
    rows.append(base_row(check_id="VAL2441_08_next_target_written", status="PASS" if outputs["next_target"][0]["target_file"].startswith("2442-") else "FAIL", notes="2442 mass-sector target selected"))

    hits = formalization_hits()
    rows.append(base_row(check_id="VAL2441_09_no_formalization_artifacts", status="PASS" if not hits else "FAIL", notes="no 2441 artifacts were written to formalization-workbench" if not hits else "formalization-workbench contains 2441 artifacts", detail="; ".join(str(hit) for hit in hits)))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        rows.append(base_row(check_id=f"VAL2441_CSV_{path.stem}", status="PASS" if ok and count > 0 else "FAIL", notes=f"CSV parses with {count} rows" if ok else "CSV parse failed", detail=detail))

    overall_pass = all(row["status"] == "PASS" for row in rows)
    rows.append(base_row(check_id="VAL2441_OVERALL", status="PASS" if overall_pass else "FAIL", notes="2441 maps b_alpha conditionally to the DD electromagnetic charge, exposes the missing mass/nuclear coefficient and source leg, and selects mass-sector owner next"))
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2441 - Y5/R2FR MTS To DD Charge Map Or WEP Source Leg Owner",
        "",
        "## Result",
        "- 2441 maps the MTS coupling basis into the Damour-Donoghue WEP charge language.",
        "- `b_alpha` has a clean conditional route into the electromagnetic charge channel: `D_e_source = S_E^q b_alpha`.",
        "- The nuclear/mass channel `D_mhat_source` is not owned by the current MTS coefficient basis.  This is now an explicit gap: `b_mhat` or `b_nuclear` must be derived or proved zero.",
        "- Direct `delta_w_block` and `delta_w_shadow` are not silently folded into DD charges; they remain separate source-weight/shadow channels.",
        "- Next target is 2442: mass-sector owner or WEP nuclear-binding gap.",
        "",
        "## Source Register",
        table(["source_id", "source_path", "path_exists", "needles_found", "role"], outputs["source_register"]),
        "",
        "## MTS To DD Charge Map",
        table(["map_id", "mts_component", "dd_target", "map_formula", "required_owner", "map_status", "partial_success", "score_ready", "valid_for_claim"], outputs["dd_map"]),
        "",
        "## Mass Sector Gap Ledger",
        table(["gap_id", "missing_symbol", "definition", "why_needed", "current_status", "valid_for_claim"], outputs["mass_gap"]),
        "",
        "## WEP Reduced Formula",
        table(["formula_id", "formula", "known_inputs", "unknown_inputs", "use_status", "score_ready", "valid_for_claim"], outputs["wep_reduced_formula"]),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"], outputs["claim_gates"]),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], outputs["decisions"]),
        "",
        "## Next Target",
        table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], outputs["next_target"]),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], outputs["branch_copies"]),
        "",
        "## Validation",
        table(["check_id", "status", "notes", "detail"], outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "dd_map": dd_map_rows(),
        "mass_gap": mass_gap_rows(),
        "wep_reduced_formula": wep_reduced_formula_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in outputs.items():
        write_csv(OUTPUTS[key], rows)

    outputs["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], outputs["branch_copies"])

    outputs["validation"] = validation_rows(outputs)
    write_csv(OUTPUTS["validation"], outputs["validation"])
    write_doc(outputs)

    print(DOC)
    print(OUTPUTS["validation"])
    overall = next(row for row in outputs["validation"] if row["check_id"] == "VAL2441_OVERALL")
    print(f"VAL2441_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
