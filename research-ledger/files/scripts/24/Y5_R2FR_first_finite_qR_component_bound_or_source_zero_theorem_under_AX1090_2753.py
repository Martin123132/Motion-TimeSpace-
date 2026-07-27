from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2753-Y5-R2FR-first-finite-qR-component-bound-or-source-zero-theorem-under-AX1090.md"
BRANCH_ID = "MTS_R2FR_AX1090_FIRST_FINITE_QR_COMPONENT_2753"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2753_SOURCE_REGISTER.csv",
    "source_zero": RESIDUALS / "P8_Y5_R2FR_2753_JEFF_SOURCE_ZERO_THEOREM_ATTEMPT.csv",
    "decomposition": RESIDUALS / "P8_Y5_R2FR_2753_JEFF_COMPONENT_DECOMPOSITION.csv",
    "first_component": RESIDUALS / "P8_Y5_R2FR_2753_FIRST_FINITE_QR_COMPONENT_ROW.csv",
    "ppn_bound": RESIDUALS / "P8_Y5_R2FR_2753_QR_PPN_CONTROL_BOUND_LINK.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2753_REFUSAL_RUNNER_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2753_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2753_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2753_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2753_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2753_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "first_component_local": LOCAL_BOUNDS / "first_finite_qR_component_BqWeyl_2753_NONCLAIM.csv",
    "source_zero_weight": SOURCE_WEIGHT / "Jeff_source_zero_attempt_2753_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2753_BQWEYL_OR_DQWEYL2_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
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


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["numeric_value_present"] = False
    row["source_backed"] = False
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2753_0_2752_doc",
            "description": "2752 finite q_R/R_AB vector handoff.",
            "source_path": "2752-Y5-R2FR-current-parent-protection-contract-saturation-or-finite-qR-residual-vector-under-AX1090.md",
            "required_needles": "NEXT2752_0_2753;QRV2752_5_Jeff;VAL2752_OVERALL",
        },
        {
            "source_id": "SRC2753_1_2752_validation",
            "description": "2752 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2752_VALIDATION.csv",
            "required_needles": "VAL2752_OVERALL;True",
        },
        {
            "source_id": "SRC2753_2_2752_vector",
            "description": "current finite q_R residual vector.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2752_FINITE_QR_RESIDUAL_VECTOR.csv",
            "required_needles": "QRV2752_0_qR;QRV2752_5_Jeff;MISSING_SOURCE_ZERO_OR_COMPONENT_BOUND",
        },
        {
            "source_id": "SRC2753_3_2747_ppn",
            "description": "q_R/delta_beta PPN control bounds.",
            "source_path": "2747-Y5-R2FR-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt-under-AX1090.md",
            "required_needles": "gamma-1 = q_R;BOX2747_0_qR;VAL2747_OVERALL",
        },
        {
            "source_id": "SRC2753_4_2297_zero",
            "description": "prior q-sector J_q source-zero theorem attempt.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2297_JQ_ZERO_THEOREM_ATTEMPT.csv",
            "required_needles": "JZT2297_4_verdict;JQ_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED",
        },
        {
            "source_id": "SRC2753_5_2297_decomp",
            "description": "prior q-sector component decomposition.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2297_JQ_COMPONENT_DECOMPOSITION.csv",
            "required_needles": "JQD2297_9_total_abs_guard;ABS_ENVELOPE_SCHEMA_READY_VALUES_MISSING",
        },
        {
            "source_id": "SRC2753_6_2297_body",
            "description": "body/source-worldtube charge law.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2297_BODY_CHARGE_SOURCE_LAW.csv",
            "required_needles": "BCL2297_1_body_charge;BODY_CHARGE_TEMPLATE_NONCLAIM",
        },
        {
            "source_id": "SRC2753_7_2299_acq",
            "description": "q source-slot acquisition ledger.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2299_BQR_CQT_QQ_ACQUISITION_LEDGER.csv",
            "required_needles": "ACQ2299_0_BqR;ACQ2299_6_total_abs",
        },
        {
            "source_id": "SRC2753_8_2301_doc",
            "description": "Ricci/Weyl split and first-class removal prior.",
            "source_path": "2301-Y5-R2FR-q-firstclass-removal-or-Ricci-Weyl-source-vector-split.md",
            "required_needles": "QRWS2301_2_Weyl_not_silent;B_qWeyl is the dangerous local-GR residual;VAL2301_OVERALL",
        },
        {
            "source_id": "SRC2753_9_2305_doc",
            "description": "linear B_qWeyl demotion and quadratic Weyl residual prior.",
            "source_path": "2305-Y5-R2FR-BqWeyl-linear-zero-typed-grammar-signature-or-quadratic-Weyl-residual-row.md",
            "required_needles": "LINEAR_BQWEYL_ROUTE_DEMOTED_TO_CLOSURE_ONLY;D_qWeyl2;VAL2305_OVERALL",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def source_zero_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "JZ2753_0_definition",
            "J_eff total source",
            "J_eff := J_matter + J_Ricci + J_Weyl + J_body + J_boundary + J_readout + J_history + J_projector + J_constants",
            "DECOMPOSITION_WRITTEN_NOT_ZERO",
            "MISSING_COMPONENT_ZERO_OR_ABS_BOUNDS",
        ),
        (
            "JZ2753_1_matter_chain_rule",
            "ordinary matter bulk source",
            "J_matter=0 if matter functor descends through quotient observables with no q marker/source weight and variation-before-readout",
            "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "MISSING_PARENT_MATTER_DESCENT_FOR_QR",
        ),
        (
            "JZ2753_2_exterior_vacuum",
            "exterior local vacuum",
            "T_H=0 and Ricci=0 outside matter do not remove Weyl/tidal terms or body/worldtube boundary data",
            "EXTERIOR_VACUUM_INSUFFICIENT",
            "MISSING_BQWEYL_ZERO_OR_BOUND_AND_QBODY_ZERO",
        ),
        (
            "JZ2753_3_body_boundary",
            "body/worldtube and boundary charge",
            "Q_q[body] or Pi_q can set exterior q/R_AB profile even when bulk exterior source vanishes",
            "BODY_CHARGE_OPEN",
            "MISSING_BODY_NEUTRALITY_OR_BOUND",
        ),
        (
            "JZ2753_4_tail_channels",
            "readout/history/projector/constants",
            "post-variation source normalization, history kernels, projector commutators, and material labels must vanish or be bounded separately",
            "TAIL_CHANNELS_OPEN",
            "MISSING_TAIL_ZERO_OR_BOUNDS",
        ),
        (
            "JZ2753_5_verdict",
            "J_eff=0 source-zero theorem",
            "J_eff=0 is not proved under current evidence; the first dangerous finite component is exterior Weyl/tidal driving",
            "JEFF_ZERO_NOT_PROVED_COMPONENT_BOUND_REQUIRED",
            "MISSING_PARENT_SIGNATURE_OR_BQWEYL_DQWEYL2_BOUND",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "attempt_id": aid,
                "target": target,
                "statement": statement,
                "current_status": status,
                "missing_input": missing,
                "theorem_zero": False,
            }
        )
        for aid, target, statement, status, missing in specs
    ]


def decomposition_rows() -> list[dict[str, Any]]:
    specs = [
        ("JCOMP2753_0_matter", "J_matter", "ordinary matter q/R_AB source", "conditional chain-rule zero only", "MISSING_PARENT_MATTER_DESCENT_FOR_QR", "WEP;PPN;R10"),
        ("JCOMP2753_1_Ricci", "B_qRic R_Ricci", "Ricci/Einstein-sector geometric mixing", "can be vacuum-silent only after GR LHS and diagonalization are signed", "MISSING_RICCI_DIAGONALIZATION", "local_GR;PPN"),
        ("JCOMP2753_2_Weyl_linear", "B_qWeyl C_Weyl", "linear Weyl/tidal exterior-vacuum source", "FIRST_DANGEROUS_COMPONENT_LINEAR_CLOSURE_ONLY", "MISSING_NO_SPURION_PARENT_SIGNATURE_OR_BOUND", "PPN;orbital;local_GR"),
        ("JCOMP2753_3_Weyl_quadratic", "D_qWeyl2 C^2", "quadratic Weyl/tidal scalar source not killed by linear index theorem", "FIRST_SURVIVING_COMPONENT_AFTER_LINEAR_DEMOTION", "MISSING_NO_TOWER_THEOREM_OR_BOUND", "PPN;orbital;R10;clock"),
        ("JCOMP2753_4_body", "Q_q[body]", "body/source-worldtube q charge", "EXTERIOR_ZERO_INSUFFICIENT", "MISSING_BODY_NEUTRALITY_OR_BOUND", "R10;PPN;orbital"),
        ("JCOMP2753_5_boundary", "Pi_q/B_q", "boundary/reference/support momentum", "BOUNDARY_SOURCE_OPEN", "MISSING_BOUNDARY_ZERO_OR_BOUND", "boundary;R10;orbital"),
        ("JCOMP2753_6_tail", "tail_q", "readout/history/projector/counterterm/constants source tail", "TAIL_OPEN", "MISSING_TAIL_ZERO_OR_BOUND", "clock;PPN;orbital"),
        ("JCOMP2753_7_total_abs", "J_eff_abs", "absolute no-cancellation total source vector", "SCHEMA_READY_VALUES_MISSING", "MISSING_COMMON_NORMALIZATION_AND_COMPONENT_VALUES", "all_local_arenas"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "component_id": cid,
                "symbol": symbol,
                "meaning": meaning,
                "current_status": status,
                "missing_input": missing,
                "observable_link": observable,
                "no_cancellation_policy": "sum absolute component magnitudes; no sign-cancellation credit",
            }
        )
        for cid, symbol, meaning, status, missing, observable in specs
    ]


def first_component_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FC2753_0_BqWeyl_linear",
            "B_qWeyl",
            "linear q-Weyl/tidal coupling",
            "q source term proportional to B_qWeyl C_abcd",
            "first exterior-vacuum component because C_abcd is nonzero around a source even when Ricci/T vanish",
            "LINEAR_ZERO_CONDITIONAL_DEMOTED_TO_CLOSURE",
            "MISSING_NO_SPURION_PARENT_SIGNATURE_OR_NUMERIC_BOUND",
            "PPN;orbital;local_GR",
            "2.3e-05 q_R control bound from 2747 is only a future projection target",
        ),
        (
            "FC2753_1_DqWeyl2",
            "D_qWeyl2",
            "quadratic q-Weyl scalar coupling",
            "q C_abcd C^abcd or q C_abcd *C^abcd",
            "survives the one-Weyl index theorem and is therefore the next live finite source row if linear BqWeyl stays closure-only",
            "LIVE_NEXT_RESIDUAL_NONCLAIM",
            "MISSING_NO_HIGHER_CURVATURE_TOWER_THEOREM_OR_NUMERIC_BOUND",
            "PPN;orbital;R10_if_projected;clock",
            "requires Schwarzschild/exterior scaling, q Green function, source cutoff, and arena projection",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "component_row_id": cid,
                "symbol": symbol,
                "definition": definition,
                "formula_or_operator": formula,
                "why_first": why,
                "current_status": status,
                "required_source": required,
                "observable_link": observable,
                "ppn_control_link": ppn,
                "units_status": "MISSING_COMMON_Q_OPERATOR_NORMALIZATION",
            }
        )
        for cid, symbol, definition, formula, why, status, required, observable, ppn in specs
    ]


def ppn_bound_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PBOUND2753_0_qR",
            "q_R",
            "gamma-1=q_R",
            "2.3e-05",
            "Cassini/gamma control bound from 2747",
            "projection target only; no MTS q_R value exists",
        ),
        (
            "PBOUND2753_1_BqWeyl_to_qR",
            "B_qWeyl -> q_R",
            "q_R ~ tau_PPN G_q[B_qWeyl C_Weyl + D_qWeyl2 C^2 + body/boundary/tails]",
            "MISSING_NUMERIC_BOUND",
            "future source-to-PPN map",
            "needs Z_R/M_R^2/domain/source profile/tau_PPN before scoring",
        ),
        (
            "PBOUND2753_2_no_claim",
            "first finite component score",
            "abs(q_R_predicted) <= 2.3e-05 only after all internal factors are numeric/source-backed or theorem-zero",
            "BLOCKED",
            "acceptance guard",
            "placeholder B_qWeyl/D_qWeyl2 rows cannot be scored",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "bound_id": bid,
                "quantity": quantity,
                "mapping": mapping,
                "control_bound": bound,
                "source": source,
                "status": status,
            }
        )
        for bid, quantity, mapping, bound, source, status in specs
    ]


def refusal_rows() -> list[dict[str, Any]]:
    specs = [
        ("REF2753_0_Jeff_zero", "claim J_eff=0", "BLOCKED", "source-zero theorem attempt ends JEFF_ZERO_NOT_PROVED_COMPONENT_BOUND_REQUIRED"),
        ("REF2753_1_qR_zero", "claim q_R=0", "BLOCKED", "q_R has PPN translation but no parent zero theorem or finite profile bound"),
        ("REF2753_2_BqWeyl_zero", "claim linear B_qWeyl=0", "BLOCKED", "typed no-spurion grammar is closure-only under 2305"),
        ("REF2753_3_DqWeyl2_zero", "claim quadratic Weyl source absent", "BLOCKED", "no higher-curvature/no-tower theorem or coefficient bound"),
        ("REF2753_4_score", "score finite q_R component against PPN", "BLOCKED", "normalization, Green domain, source profile, and tau_PPN missing"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": rid,
                "attempted_claim": claim,
                "status": status,
                "reason": reason,
                "runner_allows_claim": False,
            }
        )
        for rid, claim, status, reason in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2753_0_Jeff_zero", "J_eff=0 source theorem", "BLOCKED_NO_CLAIM", "component zeros are unsigned"),
        ("GATE2753_1_body_charge", "Q_q[body]/boundary neutrality", "BLOCKED_NO_CLAIM", "exterior vacuum is insufficient"),
        ("GATE2753_2_BqWeyl_linear", "linear B_qWeyl theorem-zero or source-backed bound", "BLOCKED_NO_CLAIM", "linear zero is closure-only; no numeric bound"),
        ("GATE2753_3_DqWeyl2", "quadratic Weyl residual theorem-zero or source-backed bound", "BLOCKED_NO_CLAIM", "no no-tower theorem or coefficient"),
        ("GATE2753_4_qR_PPN", "finite q_R score against PPN", "BLOCKED_NO_CLAIM", "no internal q_R prediction"),
        ("GATE2753_5_local_GR", "derived local GR/Newton", "BLOCKED_NO_CLAIM", "J_eff/q_R source-zero not derived"),
    ]
    return [nonclaim({"claim_gate_id": gid, "claim_gate": gate, "status": status, "reason": reason}) for gid, gate, status, reason in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2753_0_source_zero",
            "J_eff source-zero theorem",
            "FAILED_CURRENT_CLAIM",
            "ordinary-matter chain rule is exact conditional, but Weyl/body/boundary/readout components remain open",
        ),
        (
            "DEC2753_1_first_component",
            "first dangerous finite q_R component",
            "B_QWEYL_LINEAR_IDENTIFIED_NONCLAIM",
            "Weyl/tidal curvature survives in local vacuum; this is the first component that can source q_R outside matter",
        ),
        (
            "DEC2753_2_linear_status",
            "linear B_qWeyl zero route",
            "CLOSURE_ONLY_UNTIL_PARENT_SIGNATURE",
            "2305 already demoted the typed no-spurion grammar because it is not parent-derived",
        ),
        (
            "DEC2753_3_next",
            "next target",
            "NEXT_2754_BQWEYL_LINEAR_REVIVAL_OR_DQWEYL2_NO_TOWER",
            "either revive linear B_qWeyl with a new parent signature, or move to the quadratic Weyl/no-higher-curvature residual row",
        ),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "reason": reason}) for did, decision, result, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2753_0_2754",
                "status": "selected_primary",
                "target_doc": "2754-Y5-R2FR-BqWeyl-linear-revival-or-DqWeyl2-no-tower-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_BqWeyl_linear_revival_or_DqWeyl2_no_tower_bound_under_AX1090_2754.py",
                "mission": "do not rerun generic source-zero: either find a new parent-signed no-Weyl-spurion/q-representation certificate for linear B_qWeyl, or accept linear closure-only and attack D_qWeyl2/no-higher-curvature tower as the next finite local residual",
                "acceptance": "linear B_qWeyl theorem-zero only with parent signature; otherwise a D_qWeyl2 residual row with required coefficient, units, source path, exterior scaling, and PPN/orbital projection blockers",
                "forbidden": "do not claim local GR; do not use exterior vacuum to erase Weyl; do not score placeholders; do not edit formalization-workbench; no GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2753_0_first_component_local", "source_table": rel(OUTPUTS["first_component"]), "copy_path": rel(BRANCH_OUTPUTS["first_component_local"]), "purpose": "local-bound first finite qR component row", "exists": BRANCH_OUTPUTS["first_component_local"].exists()}),
        nonclaim({"copy_id": "BR2753_1_source_zero_weight", "source_table": rel(OUTPUTS["source_zero"]), "copy_path": rel(BRANCH_OUTPUTS["source_zero_weight"]), "purpose": "source-weight J_eff source-zero failure", "exists": BRANCH_OUTPUTS["source_zero_weight"].exists()}),
        nonclaim({"copy_id": "BR2753_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB queue for BqWeyl/DqWeyl2 next", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    source_zero: list[dict[str, Any]],
    decomposition: list[dict[str, Any]],
    first_component: list[dict[str, Any]],
    ppn_bound: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    zero_ok = any(row["attempt_id"] == "JZ2753_5_verdict" and row["current_status"] == "JEFF_ZERO_NOT_PROVED_COMPONENT_BOUND_REQUIRED" for row in source_zero)
    decomp_ok = any(row["component_id"] == "JCOMP2753_2_Weyl_linear" and row["current_status"] == "FIRST_DANGEROUS_COMPONENT_LINEAR_CLOSURE_ONLY" for row in decomposition) and any(row["component_id"] == "JCOMP2753_7_total_abs" for row in decomposition)
    first_ok = any(row["component_row_id"] == "FC2753_0_BqWeyl_linear" and row["current_status"] == "LINEAR_ZERO_CONDITIONAL_DEMOTED_TO_CLOSURE" for row in first_component) and any(row["component_row_id"] == "FC2753_1_DqWeyl2" for row in first_component)
    ppn_ok = any(row["bound_id"] == "PBOUND2753_0_qR" and row["control_bound"] == "2.3e-05" for row in ppn_bound) and any(row["bound_id"] == "PBOUND2753_2_no_claim" and row["control_bound"] == "BLOCKED" for row in ppn_bound)
    refusal_ok = all(row["runner_allows_claim"] is False for row in refusal)
    gate_ok = all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in gates) and any(row["claim_gate_id"] == "GATE2753_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    decision_ok = any(row["decision_id"] == "DEC2753_3_next" and row["result"] == "NEXT_2754_BQWEYL_LINEAR_REVIVAL_OR_DQWEYL2_NO_TOWER" for row in decisions)
    next_ok = next_target[0]["selected"] is True and "2754" in next_target[0]["target_doc"]
    no_claim_flags_ok = all(
        row.get("valid_for_claim") is False and row.get("claim_allowed") is False
        for block in [source_zero, decomposition, first_component, ppn_bound, refusal, gates, decisions, next_target]
        for row in block
    )
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    rows = [
        {"validation_id": "VAL2753_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2753_1_source_zero_refused", "passed": zero_ok, "detail": "J_eff source-zero theorem remains unproved", "timestamp_utc": ts()},
        {"validation_id": "VAL2753_2_decomposition", "passed": decomp_ok, "detail": "Weyl component and total absolute guard are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2753_3_first_component", "passed": first_ok, "detail": "B_qWeyl linear and D_qWeyl2 first-component rows staged nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2753_4_ppn_bound_link", "passed": ppn_ok, "detail": "q_R control bound link recorded but blocked from scoring", "timestamp_utc": ts()},
        {"validation_id": "VAL2753_5_refusal_runner", "passed": refusal_ok, "detail": "refusal runner blocks all attempted claims", "timestamp_utc": ts()},
        {"validation_id": "VAL2753_6_claim_gates", "passed": gate_ok and no_claim_flags_ok, "detail": "claim gates remain closed and flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2753_7_decision_next", "passed": decision_ok and next_ok, "detail": "2754 BqWeyl revival or DqWeyl2 no-tower selected", "timestamp_utc": ts()},
        {"validation_id": "VAL2753_8_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2753_9_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2753_10_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2753_11_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2753_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2753 refuses J_eff/q_R source-zero, stages BqWeyl/DqWeyl2 as first finite local components, and selects BqWeyl revival or DqWeyl2 no-tower next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2753 - Y5 R2/f(R): First Finite q_R Component Bound Or Source-Zero Theorem Under AX1090

Status: `Y5_R2FR_2753_Jeff_zero_refused_BqWeyl_DqWeyl2_first_components_nonclaim`

## Private Verdict

2753 attacks the first finite `q_R/R_AB` source component selected by 2752.

The source-zero theorem does not close. Ordinary matter can be made silent by an exact conditional chain-rule theorem, but that is not enough: exterior vacuum does not erase Weyl/tidal curvature, body/worldtube matching, boundary momentum, or readout/history/projector tails.

So the first dangerous finite component is now named:

`B_qWeyl C_abcd`

This is the exterior-vacuum problem because `C_abcd` is generally nonzero around a source even where Ricci and `T_H` vanish. The linear `B_qWeyl` zero route is precise but currently closure-only: it needs a parent-signed q-representation/no-Weyl-spurion grammar. Since prior 2305 already demoted that route under the current corpus, 2753 also stages the next survivor:

`D_qWeyl2 C_abcd C^abcd`

No local-GR, Newton, PPN, R10, clock, orbital, or public claim follows. The PPN `q_R` bound is only a future control target until the internal coefficient, profile, Green domain, and projection kernel exist.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## J_eff Source-Zero Theorem Attempt

{markdown_table(data["source_zero"], ["attempt_id", "target", "statement", "current_status", "missing_input", "theorem_zero", "valid_for_claim"])}

## J_eff Component Decomposition

{markdown_table(data["decomposition"], ["component_id", "symbol", "meaning", "current_status", "missing_input", "observable_link", "no_cancellation_policy", "valid_for_claim"])}

## First Finite q_R Component Row

{markdown_table(data["first_component"], ["component_row_id", "symbol", "definition", "formula_or_operator", "why_first", "current_status", "required_source", "observable_link", "ppn_control_link", "units_status", "valid_for_claim"])}

## q_R PPN Control Bound Link

{markdown_table(data["ppn_bound"], ["bound_id", "quantity", "mapping", "control_bound", "source", "status", "valid_for_claim"])}

## Refusal Runner

{markdown_table(data["refusal"], ["refusal_id", "attempted_claim", "status", "reason", "runner_allows_claim", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is a useful narrowing. We are no longer saying “the coupling is missing” in a vague way. The first local-vacuum danger is Weyl/tidal driving. If the parent theory proves q has no Weyl-spurion route, linear `B_qWeyl` can die cleanly. If not, the next real residual is `D_qWeyl2`, and that has to be theorem-zero or bounded. That is the next lock.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    source_zero = source_zero_rows()
    decomposition = decomposition_rows()
    first_component = first_component_rows()
    ppn_bound = ppn_bound_rows()
    refusal = refusal_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["source_zero"], source_zero)
    write_csv(OUTPUTS["decomposition"], decomposition)
    write_csv(OUTPUTS["first_component"], first_component)
    write_csv(OUTPUTS["ppn_bound"], ppn_bound)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["first_component_local"], first_component)
    write_csv(BRANCH_OUTPUTS["source_zero_weight"], source_zero)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, source_zero, decomposition, first_component, ppn_bound, refusal, gates, decisions, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "source_zero": source_zero,
        "decomposition": decomposition,
        "first_component": first_component,
        "ppn_bound": ppn_bound,
        "refusal": refusal,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2753 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
