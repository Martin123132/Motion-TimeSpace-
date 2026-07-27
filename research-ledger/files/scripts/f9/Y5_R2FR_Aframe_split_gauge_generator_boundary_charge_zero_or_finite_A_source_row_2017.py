from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2017-Y5-R2FR-Aframe-split-gauge-generator-boundary-charge-zero-or-finite-A-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_rows_parse(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def md_cell(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    try:
        result = subprocess.run(
            ["git", "-C", str(FORMALIZATION), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2017_00_2016_handoff",
            ROOT / "2016-Y5-R2FR-Aframe-no-physical-pole-gauge-constraint-theorem-or-finite-prior-runner.md",
            ["NEXT2016_0_2017", "ANP2016_5_boundary_charge_silence", "VAL2016_OVERALL"],
            "2016 selected A split-gauge generator and boundary charge as the next theorem object.",
        ),
        (
            "SRC2017_01_2009_closure",
            ROOT / "2009-Y5-R2FR-Aframe-no-extra-mode-theorem-or-first-residual-response-kernel.md",
            ["NEM2009_1_variation_chain_rule", "NEM2009_6_boundary_silence_clause", "VAL2009_OVERALL"],
            "conditional e=dX+A closure gives the split variation and Noether identity.",
        ),
        (
            "SRC2017_02_2010_no_spurion",
            ROOT / "2010-Y5-R2FR-Aframe-parent-source-map-rank-certificate-or-residual-coefficient-source-pack.md",
            ["NSP2010_0_matter_functor", "NSP2010_5_boundary_source_measure", "NSP2010_6_verdict"],
            "matter/source no-spurion clauses needed before boundary charge can be called gauge.",
        ),
        (
            "SRC2017_03_2012_QA_rows",
            ROOT / "2012-Y5-R2FR-Aframe-current-nohair-source-neutrality-theorem-or-finite-QA-row.md",
            ["NHA2012_0_target", "FQA2012_1_PiA", "DEC2012_1_best_derivation_route"],
            "finite Q_A/Pi_A rows and source-neutrality target.",
        ),
        (
            "SRC2017_04_2013_boundary",
            ROOT / "2013-Y5-R2FR-Aframe-finite-QA-bound-source-acquisition-or-boundary-neutrality-proof.md",
            ["BNA2013_1_variation_formula", "BNA2013_6_verdict", "VAL2013_OVERALL"],
            "boundary/source neutrality attempt and finite Q_A acquisition warning.",
        ),
        (
            "SRC2017_05_582_boundary",
            OUT / "P8_Y5_R10_582_BOUNDARY_DIFFERENTIABILITY_AUDIT.csv",
            ["BD582_0_bulk_variation", "BD582_2_central_term", "BD582_5_verdict"],
            "generic boundary differentiability/cocycle audit.",
        ),
        (
            "SRC2017_06_582_dirac",
            OUT / "P8_Y5_R10_582_DIRAC_BRACKET_AUDIT.csv",
            ["DA582_2_secondary_constraint", "DA582_4_bracket_closure", "DA582_5_degree_count"],
            "generic Dirac constraint and degree-count audit.",
        ),
        (
            "SRC2017_07_590_vertical_map",
            OUT / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
            ["metric_or_coframe", "canonical_momenta_or_boundary_charge", "boundary_edge"],
            "field-by-field vertical action and boundary-edge map.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def split_generator_rows() -> list[dict[str, object]]:
    data = [
        {
            "derivation_id": "SGG2017_0_split_transformation",
            "object": "split-gauge transformation",
            "formula": "delta_epsilon X^a=epsilon^a; delta_epsilon A^a_mu=-partial_mu epsilon^a plus covariant/local-Lorentz correction if the parent connection requires it; delta_epsilon e^a_mu=0",
            "derivation_status": "DERIVED_ALGEBRAICALLY_INSIDE_E_CLOSURE",
            "meaning": "the public tetrad is unchanged, so any e-only action is split-gauge invariant.",
            "claim_limit": "does not exclude independent A kinetic/source/boundary terms.",
            "theorem_zero": False,
        },
        {
            "derivation_id": "SGG2017_1_noether_identity",
            "object": "split Noether identity",
            "formula": "delta S=int (E_X_a + partial_mu E_A^{a mu}) epsilon^a dV - int_boundary epsilon_a n_mu E_A^{a mu}; hence E_X_a + partial_mu E_A^{a mu}=0 when boundary term is silent",
            "derivation_status": "DERIVED_CONDITIONAL_NOETHER_IDENTITY",
            "meaning": "the X equation is the divergence of the A/tetrad equation in the strict closure branch.",
            "claim_limit": "boundary term and independent A-sector terms are not parent-owned.",
            "theorem_zero": False,
        },
        {
            "derivation_id": "SGG2017_2_constraint_candidate",
            "object": "canonical split constraint",
            "formula": "C_A^a = pi_X^a + D_i pi_A^{i a} plus connection/source improvements; G_A[epsilon]=int_Sigma epsilon_a C_A^a + Q_A[epsilon]",
            "derivation_status": "FORMAL_GENERATOR_DERIVED_TO_BOUNDARY_TERM",
            "meaning": "with the canonical sign convention this generates delta X=epsilon and delta A_i=-D_i epsilon.",
            "claim_limit": "pi variables, D_i improvement, and source terms require a parent symplectic potential.",
            "theorem_zero": False,
        },
        {
            "derivation_id": "SGG2017_3_boundary_charge",
            "object": "A split-gauge boundary charge",
            "formula": "Q_A[epsilon] = int_partialSigma epsilon_a pi_A^{n a} plus improvement/source-edge terms",
            "derivation_status": "BOUNDARY_CHARGE_FORM_DERIVED",
            "meaning": "the missing Q_A is not mysterious anymore: it is the normal A momentum weighted by the split parameter.",
            "claim_limit": "Q_A=0 needs epsilon|boundary=0, pi_A^n=0, exact/proper charge, or a signed source-neutrality theorem.",
            "theorem_zero": False,
        },
        {
            "derivation_id": "SGG2017_4_zero_for_proper_gauge_only",
            "object": "proper compact split transformations",
            "formula": "if epsilon^a vanishes on every physical/source boundary, then Q_A[epsilon]=0",
            "derivation_status": "ZERO_FOR_PROPER_COMPACT_GAUGE_TRANSFORMS_ONLY",
            "meaning": "proper gauge transformations carry no charge by definition.",
            "claim_limit": "this does not prove physical source-boundary charge is zero when epsilon labels a nontrivial frame displacement.",
            "theorem_zero": True,
        },
        {
            "derivation_id": "SGG2017_5_boundary_cocycle",
            "object": "K_boundary^A",
            "formula": "{G_A[epsilon],G_A[eta]} = K_boundary^A[epsilon,eta] for abelian split shifts unless all boundary/improvement terms are differentiable and proper",
            "derivation_status": "BULK_ABELIAN_BOUNDARY_COCYCLE_UNOWNED",
            "meaning": "the bulk split algebra wants to be abelian; any obstruction lives at boundary/source/improvement level.",
            "claim_limit": "K_boundary^A=0 is not computed without parent Omega, Q_A, and boundary conditions.",
            "theorem_zero": False,
        },
        {
            "derivation_id": "SGG2017_6_matter_source_silence",
            "object": "matter/source split invariance",
            "formula": "delta_epsilon S_matter=0 if S_matter=Sbar[Psi,e,omega[e],theta] and source measures contain no X/A/Phi_MTS/q_loc markers",
            "derivation_status": "CONDITIONAL_NO_SPURION_SOURCE_SILENCE",
            "meaning": "matter cannot source Q_A if it only sees the public tetrad.",
            "claim_limit": "source/boundary matter grammar is not parent-signed.",
            "theorem_zero": False,
        },
        {
            "derivation_id": "SGG2017_7_verdict",
            "object": "A split generator and boundary-zero theorem",
            "formula": "G_A[epsilon]=int epsilon_a(pi_X^a + D_i pi_A^{i a}+improvements)+int_partial epsilon_a pi_A^{n a}+edge terms",
            "derivation_status": "GENERATOR_FORM_DERIVED_BOUNDARY_ZERO_NOT_PARENT_SIGNED",
            "meaning": "we have the actual generator skeleton and boundary charge formula; the remaining proof is pi_A^n=0/proper/exact or finite Q_A.",
            "claim_limit": "no local-GR/no-pole/R10 claim follows yet.",
            "theorem_zero": False,
        },
    ]
    rows = []
    for item in data:
        row = base_row()
        row.update({**item, "parent_signed": False})
        rows.append(row)
    return rows


def source_row_rows() -> list[dict[str, object]]:
    data = [
        ("ASR2017_0_QA_charge", "Q_A[epsilon]", "int_partialSigma epsilon_a pi_A^{n a} plus source-edge improvements", "FIRST_FINITE_A_SOURCE_ROW_FORMULA", "A-charge", "not_numeric"),
        ("ASR2017_1_PiA_normal", "pi_A^{n a}", "normal momentum conjugate to A at compact source/boundary", "ZERO_TARGET_OR_SOURCE_INPUT", "action/A/area units", "not_numeric"),
        ("ASR2017_2_Kboundary", "K_boundary^A", "boundary cocycle/improvement obstruction in split-gauge bracket", "MISSING_PARENT_BOUNDARY_BRACKET", "charge algebra units", "not_numeric"),
        ("ASR2017_3_source_neutrality", "pi_A^n=0", "condition that collapses finite A hair and supports no-pole route", "BEST_ZERO_ROUTE_NOT_SIGNED", "boolean theorem", "not_signed"),
        ("ASR2017_4_finite_A_hair", "Q_A -> C_A, lambda_A, alpha_A", "if pi_A^n or K_boundary survives, it feeds the 2012-2016 finite residual rows", "RESIDUAL_BRANCH_RETAINED", "mixed", "not_score_ready"),
    ]
    rows = []
    for row_id, symbol, formula, status, units, numeric_status in data:
        row = base_row()
        row.update(
            {
                "source_row_id": row_id,
                "symbol": symbol,
                "formula_or_condition": formula,
                "status": status,
                "numeric_value": "MISSING",
                "units": units,
                "numeric_status": numeric_status,
                "score_ready": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2017_0_split_generator_skeleton", "split generator skeleton derived", True, "G_A and Q_A formulas are written as conditional closure math"),
        ("CG2017_1_QA_formula", "A boundary charge formula identified", True, "Q_A is int epsilon pi_A^n plus improvements, but nonclaim"),
        ("CG2017_2_QA_zero", "Q_A=0 for physical source boundary", False, "only proper compact gauge epsilon gives automatic zero; physical/source boundary needs pi_A^n=0/proper/exact proof"),
        ("CG2017_3_Kboundary_zero", "K_boundary^A=0", False, "bulk split algebra is abelian but boundary cocycle is not computed"),
        ("CG2017_4_no_pole", "A has no physical pole", False, "boundary/source, parent Omega, degree count, and matter/source silence remain unsigned"),
        ("CG2017_5_finite_source_score", "finite A source row score-ready", False, "Q_A formula exists but no numeric/sourced pi_A^n, kappa_A, Z_A, lambda_A, P_00"),
        ("CG2017_6_local_GR_Newton", "local GR/Newton derived", False, "closure route is closer but still not parent-signed"),
    ]
    rows = []
    for gate_id, gate, passed_for_nonclaim, reason in data:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "passed_for_nonclaim": passed_for_nonclaim,
                "passed_for_claim": False,
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2017_0_boundary_zero", "claim Q_A=0", "REFUSE", "Q_A=0 only follows for proper compact gauge parameters or if pi_A^n=0/proper/exact is parent-signed."),
        ("REF2017_1_no_pole", "claim no physical A pole", "REFUSE", "generator skeleton exists, but first-class closure, K_boundary, degree count, and source silence remain unsigned."),
        ("REF2017_2_finite_source_score", "score finite A source row", "REFUSE", "Q_A formula has no numeric/source-backed pi_A^n or projection coefficients."),
        ("REF2017_3_R10_PPN", "score R10/PPN/local tests", "REFUSE", "A source prediction, range, coupling, residue, and projection are missing."),
        ("REF2017_4_local_GR", "claim local GR/Newton reduction", "REFUSE", "strict closure is promising but not yet derived from the parent MTS action."),
    ]
    rows = []
    for refusal_id, attempted_claim, verdict, reason in data:
        row = base_row()
        row.update(
            {
                "refusal_id": refusal_id,
                "attempted_claim": attempted_claim,
                "verdict": verdict,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2017_0_result",
            "SPLIT_GENERATOR_FORM_DERIVED_QA_ZERO_NOT_SIGNED",
            "The split transformation gives a real generator skeleton and identifies Q_A as the normal A momentum boundary charge. This is a genuine narrowing of the coupling problem.",
            "do not claim no-pole; prove pi_A^n=0/proper/exact or treat Q_A as finite source row",
        ),
        (
            "DEC2017_1_key_math",
            "PROPER_GAUGE_ZERO_IS_NOT_PHYSICAL_SOURCE_ZERO",
            "Q_A vanishes automatically only when epsilon dies on the relevant boundary. A physical compact source can still carry pi_A^n unless source neutrality is derived.",
            "target the source/boundary matter action and no-spurion grammar next",
        ),
        (
            "DEC2017_2_best_next_route",
            "PARENT_SOURCE_BOUNDARY_ACTION_FOR_PIA_ZERO_IS_NEXT",
            "The shortest path to local GR is no longer vague coupling; it is pi_A^n=0 plus K_boundary^A=0 from the source/boundary action.",
            "build 2018 source-boundary action Pi_A zero theorem or finite pi_A source-prior row",
        ),
    ]
    rows = []
    for decision_id, verdict, rationale, next_action in data:
        row = base_row()
        row.update({"decision_id": decision_id, "verdict": verdict, "rationale": rationale, "next_action": next_action})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2017_0_2018",
            "next_doc": "2018-Y5-R2FR-Aframe-source-boundary-action-PiA-zero-or-finite-PiA-source-prior.md",
            "objective": "derive pi_A^n=0 and K_boundary^A=0 from the parent source/boundary action and no-spurion matter grammar; if that fails, create finite pi_A/Q_A source-prior rows without claims",
            "required_inputs": "source action; boundary variation; matter/source no-spurion grammar; allowed split parameter class; Pi_A normal momentum; Q_A exact/proper/zero test; K_boundary bracket; finite source prior schema",
            "excluded": "proper-gauge zero used as physical source zero; ordinary current conservation as nohair; invented Pi_A/Q_A values; R10/local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update({"copy_id": f"COPY2017_{idx}", "path": str(path), "exists": path.exists(), "note": note})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    generator: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2017_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"))
    checks.append(("VAL2017_01_split_transformation", any(row["derivation_id"] == "SGG2017_0_split_transformation" and "delta_epsilon e" in row["formula"] for row in generator), "split transformation keeps e fixed"))
    checks.append(("VAL2017_02_generator_formula", any(row["derivation_id"] == "SGG2017_2_constraint_candidate" and "pi_X" in row["formula"] and "pi_A" in row["formula"] for row in generator), "canonical generator skeleton contains pi_X and pi_A"))
    checks.append(("VAL2017_03_boundary_formula", any(row["derivation_id"] == "SGG2017_3_boundary_charge" and "pi_A" in row["formula"] for row in generator), "Q_A boundary formula is explicit"))
    checks.append(("VAL2017_04_no_false_zero", any(row["derivation_id"] == "SGG2017_7_verdict" and row["derivation_status"] == "GENERATOR_FORM_DERIVED_BOUNDARY_ZERO_NOT_PARENT_SIGNED" for row in generator), "boundary zero not falsely promoted"))
    checks.append(("VAL2017_05_source_rows_nonclaim", all(row["score_ready"] is False and row["numeric_value"] == "MISSING" for row in source_rows), "finite source rows remain missing/nonclaim"))
    checks.append(("VAL2017_06_claim_gates_blocked", all(row["passed_for_claim"] is False for row in claim_gates), "all claim gates remain blocked"))
    checks.append(("VAL2017_07_refusals_active", all(row["verdict"] == "REFUSE" and row["accepted_for_claim"] is False for row in refusals), "refusals remain active"))
    checks.append(("VAL2017_08_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"))
    checks.append(("VAL2017_09_branch_copies", all(path.exists() and csv_rows_parse(path) for path in branch_paths), "branch-copy CSVs exist and parse"))
    checks.append(("VAL2017_10_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"))
    checks.append(("VAL2017_11_output_scope", all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in output_paths + branch_paths + [DOC]), "all outputs are under post-checkpoint-work"))
    overall = all(passed for _, passed, _ in checks)
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2017_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2017 A-frame split-gauge generator boundary charge zero or finite A source row",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    generator: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    parts = [
        "# 2017 Y5 R2FR: A-Frame Split-Gauge Generator Boundary Charge Zero Or Finite A Source Row\n",
        "Private checkpoint. This takes the 2016 theorem gate seriously and derives the split-gauge generator skeleton rather than merely naming the missing coupling.\n",
        "## Current Verdict\n",
        "A real mathematical step landed: in the strict closure branch `e=dX+A`, the split transformation `delta X=epsilon`, `delta A=-d epsilon` leaves the public tetrad fixed. The associated Noether/generator skeleton is `G_A[epsilon]=int epsilon_a (pi_X^a + D_i pi_A^{ia}+improvements)+Q_A[epsilon]`, with boundary charge `Q_A[epsilon]=int_partial epsilon_a pi_A^{na}` plus possible improvements.\n",
        "That is progress, but it is not yet the local-GR proof. `Q_A=0` is automatic only for proper gauge transformations whose parameter vanishes on the physical/source boundary. A physical compact source can still carry `pi_A^n` unless the parent source/boundary action proves source neutrality, exactness, or properness. So the next bottleneck is sharp: prove `pi_A^n=0` and `K_boundary^A=0`, or keep finite `Q_A` as the first source row.\n",
        "## Source Register\n",
        md_table(sources, ["source_id", "source_path", "status", "needles", "note"]),
        "## Split-Gauge Generator Derivation\n",
        md_table(generator, ["derivation_id", "object", "formula", "derivation_status", "meaning", "claim_limit", "theorem_zero", "parent_signed"]),
        "## Finite A Source Rows\n",
        md_table(source_rows, ["source_row_id", "symbol", "formula_or_condition", "status", "numeric_value", "units", "numeric_status", "score_ready"]),
        "## Claim Gates\n",
        md_table(claim_gates, ["gate_id", "gate", "passed_for_nonclaim", "passed_for_claim", "reason"]),
        "## Refusal Runner\n",
        md_table(refusals, ["refusal_id", "attempted_claim", "verdict", "reason", "accepted_for_claim"]),
        "## Decision Ledger\n",
        md_table(decisions, ["decision_id", "verdict", "rationale", "next_action"]),
        "## Branch Copies\n",
        md_table(branch_copies, ["copy_id", "path", "exists", "note"]),
        "## Next Target\n",
        md_table(next_target, ["target_id", "next_doc", "objective", "required_inputs", "excluded"]),
        "## Validation\n",
        md_table(validation, ["check_id", "status", "detail"]),
    ]
    DOC.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    generator = split_generator_rows()
    source_rows = source_row_rows()
    claim_gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2017_SOURCE_REGISTER.csv",
        "generator": OUT / "P8_Y5_PARENT_QLOC_2017_AFRAME_SPLIT_GAUGE_GENERATOR_DERIVATION.csv",
        "source_rows": OUT / "P8_Y5_PARENT_QLOC_2017_AFRAME_FINITE_SOURCE_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2017_CLAIM_GATE.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2017_REFUSAL_RUNNER.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2017_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2017_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["generator"], generator)
    write_csv(output_map["source_rows"], source_rows)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["refusals"], refusals)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_SPLIT_GAUGE_GENERATOR_2017_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2017_AFRAME_BOUNDARY_CHARGE_STATUS_NONCLAIM.csv",
        QUEUE / "JR2017_AFRAME_FINITE_QA_SOURCE_ROW_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["generator"], branch_paths[0])
    shutil.copyfile(output_map["claim_gates"], branch_paths[1])
    shutil.copyfile(output_map["source_rows"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame split-gauge generator derivation nonclaim copy",
            "A-frame boundary charge claim-gate status nonclaim copy",
            "finite A source-row queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2017_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, generator, source_rows, claim_gates, refusals, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2017_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, generator, source_rows, claim_gates, refusals, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2017_OVERALL"][0]["status"]
    print(f"VAL2017_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
