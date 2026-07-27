from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2012-Y5-R2FR-Aframe-current-nohair-source-neutrality-theorem-or-finite-QA-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "branch_id": BRANCH_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp(),
    }


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


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
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_rows_parse(path: Path) -> bool:
    try:
        read_csv(path)
    except csv.Error:
        return False
    return True


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2012_00_2011_handoff",
            "2011-Y5-R2FR-covariant-MTS-current-source-law-for-Aframe-or-first-coefficient-dry-run.md",
            ["NEXT2011_0_2012", "CSA2011_1_ordinary_conserved_current", "VAL2011_OVERALL"],
            "2011 selected A-current nohair/source-neutrality theorem or finite Q_A row.",
        ),
        (
            "SRC2012_01_source_neutrality",
            "06-reciprocal-charge-source-neutrality.md",
            ["reciprocal_charge_neutrality_conditional_not_parent_derived", "Pi_R = 0 -> Q_R = 0", "Q_R neutrality is the missing source theorem"],
            "source-neutrality analogy: boundary momentum zero kills reciprocal charge, but is not parent-derived.",
        ),
        (
            "SRC2012_02_current_obstruction",
            "11-cell-current-origin-attempt.md",
            ["cell_current_origin_no_charge_obstruction", "Q_R = constant.", "ordinary cell-current conservation does not close"],
            "current-conservation obstruction: conserved current leaves charge hair unless zero-charge theorem exists.",
        ),
        (
            "SRC2012_03_1266_source_hunt",
            "1266-Y5-R10-RAB-primitive-auxiliary-grammar-source-hunt-or-finite-ZR-intake-review.md",
            ["HUNT1266_7_cell_current", "DEC1266_1_best_derivation_route", "GATE1266_1_current_nohair"],
            "later source hunt confirms ordinary current/noether wording does not kill hair without a constraint.",
        ),
        (
            "SRC2012_04_2009_kernel",
            "2009-Y5-R2FR-Aframe-no-extra-mode-theorem-or-first-residual-response-kernel.md",
            ["KER2009_1_Newton_acceleration", "KER2009_5_R10_yukawa_projection", "KER2009_7_total_response_vector"],
            "A-frame residual kernel to receive finite Q_A/C_A/lambda_A rows.",
        ),
        (
            "SRC2012_05_2010_coeff_pack",
            "2010-Y5-R2FR-Aframe-parent-source-map-rank-certificate-or-residual-coefficient-source-pack.md",
            ["COEF2010_0_A_profile_amplitude", "COEF2010_5_R10_alpha", "VAL2010_OVERALL"],
            "coefficient pack slots for A amplitude and R10 alpha.",
        ),
        (
            "SRC2012_06_790_local_suppression",
            "790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md",
            ["LSG790_0_Ward_compatible_split", "LSG790_3_anisotropic_PPN_suppression", "LSG790_7_Newton_limit_gate"],
            "local suppression gates that finite A hair must pass.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, relative_path, needles, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "2012 A-frame current nohair/source-neutrality theorem or finite Q_A row",
                "needles": ";".join(needles),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "note": note,
            }
        )
        rows.append(row)
    return rows


def nohair_attempt_rows() -> list[dict[str, object]]:
    specs = [
        (
            "NHA2012_0_target",
            "Q_A^a := integral_{partial Sigma} Pi_A^{n a} or integral_{partial Sigma} *J_A^a",
            "To close the A-current route, the parent theory must prove Q_A=0 or an allowed bound in the local GR exterior.",
            "TARGET_EXACT",
            "requires parent boundary variation, source neutrality, or gauge/topological zero theorem",
            "false",
        ),
        (
            "NHA2012_1_current_conservation",
            "D_mu J_A^{a mu}=0",
            "Conservation gives Q_A=constant, not Q_A=0.",
            "REJECTED_AS_ZERO_PROOF",
            "same obstruction as Q_R: a constant exterior charge is still hair",
            "false",
        ),
        (
            "NHA2012_2_free_boundary_neumann",
            "Pi_A^{n a}=0 at source/exterior boundary",
            "A free source-boundary variation would kill the conjugate A charge.",
            "CONDITIONAL_ROUTE_NOT_SIGNED",
            "source action and boundary terms are not parent-derived; fixed/source-coupled boundary can give nonzero Pi_A",
            "false",
        ),
        (
            "NHA2012_3_source_neutrality",
            "Pi_A^{n a}=0 by source neutrality",
            "Direct analogue of reciprocal source neutrality: no source momentum in A direction means no exterior A hair.",
            "BEST_NOHAIR_ROUTE_UNSIGNED",
            "needs parent proof that compact matter/source sectors carry no A-frame charge",
            "false",
        ),
        (
            "NHA2012_4_gauge_charge",
            "Q_A is generator of pure split-gauge/local Lorentz redundancy",
            "If Q_A generates an unobservable gauge transformation and all readouts commute with it, finite Q_A can be quotient-trivial.",
            "CONDITIONAL_GAUGE_ROUTE",
            "requires first-class constraint and invariant matter/readout proof, not current wording",
            "false",
        ),
        (
            "NHA2012_5_topological_zero",
            "Q_A = integral rho_A = 0 by signed source representation/topological class",
            "Topological/source representation could kill the total charge without fitting.",
            "POSSIBLE_NOT_DERIVED",
            "no parent topological class or source representation for A is identified",
            "false",
        ),
        (
            "NHA2012_6_asymptotic_flatness",
            "A -> 0 at infinity",
            "Asymptotic falloff alone does not kill charge; it can still allow Yukawa or 1/r hair.",
            "REJECTED_AS_ZERO_PROOF",
            "needs source/boundary zero, not just exterior falloff",
            "false",
        ),
        (
            "NHA2012_7_verdict",
            "A-current nohair theorem",
            "No inspected source proves Q_A=0. The theorem route remains source-neutrality/gauge/topology, but finite Q_A must be retained.",
            "NOHAIR_NOT_DERIVED",
            "create finite Q_A residual rows and target source-neutrality proof next only if a parent boundary action appears",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for nohair_id, object_text, attempt, status, missing_before_claim, parent_signed in specs:
        row = base_row()
        row.update(
            {
                "nohair_id": nohair_id,
                "object": object_text,
                "attempt": attempt,
                "status": status,
                "missing_before_claim": missing_before_claim,
                "parent_signed": parent_signed,
            }
        )
        rows.append(row)
    return rows


def finite_qa_rows() -> list[dict[str, object]]:
    specs = [
        (
            "FQA2012_0_QA",
            "Q_A",
            "A-current exterior charge/hair",
            "Q_A = integral_{partial Sigma} Pi_A^n or integral *J_A",
            "MISSING_PARENT_BOUNDARY_VARIATION",
            "A-charge units",
            "feeds C_A and all A-frame residuals",
        ),
        (
            "FQA2012_1_PiA",
            "Pi_A^n",
            "boundary/source conjugate momentum to A",
            "delta S_boundary = Pi_A^n delta A|_surface + ...",
            "MISSING_SOURCE_BOUNDARY_ACTION",
            "action variation units",
            "zero if source-neutrality theorem is signed",
        ),
        (
            "FQA2012_2_CA",
            "C_A",
            "observable A residual amplitude",
            "C_A = N_A kappa_A Q_A, with N_A fixed by the A Green function and source normalization",
            "MISSING_KAPPA_A_QA_NORMALIZATION",
            "dimensionless or model-normalized",
            "feeds Newton/PPN/clock/R10 residual kernels",
        ),
        (
            "FQA2012_3_lambdaA",
            "lambda_A",
            "range/correlation length of finite A hair",
            "lambda_A from Green kernel pole, screening length, or compact support scale",
            "MISSING_GREEN_KERNEL_OR_SCREENING_MAP",
            "m",
            "feeds R10/orbital/clock profile tests",
        ),
        (
            "FQA2012_4_profile",
            "f_A(r)",
            "finite A hair radial/profile shape",
            "h_A00(r)=2 C_A f_A(r) after weak-field gauge choice",
            "MISSING_PROFILE_SOLUTION",
            "dimensionless profile",
            "feeds acceleration, clock, orbital, PPN projections",
        ),
        (
            "FQA2012_5_alpha",
            "alpha_A(lambda_A)",
            "Yukawa-equivalent short-range strength",
            "alpha_A derived by matching h_A00 to Yukawa potential at range lambda_A",
            "MISSING_FULL_R10_BOUND_AND_A_MATCHING",
            "dimensionless",
            "must compare to real alpha(lambda) bound before any R10 claim",
        ),
        (
            "FQA2012_6_PPN",
            "delta_PPN_A",
            "PPN residual vector from finite A hair",
            "delta_PPN_A = J_PPN[A] dot (C_A,lambda_A,profile)",
            "MISSING_PPN_RESPONSE_MATRIX",
            "dimensionless",
            "gamma,beta,alpha_i scoring blocked",
        ),
        (
            "FQA2012_7_total",
            "R_QA",
            "finite A-charge local response vector",
            "R_QA=(Q_A,C_A,lambda_A,alpha_A,delta_PPN_A,delta_clock_A,delta_orbit_A)",
            "MISSING_ALL_NUMERIC_INPUTS",
            "mixed",
            "schema only; nonclaim until sourced",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, symbol, meaning, relation, status, units, note in specs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "meaning": meaning,
                "relation": relation,
                "status": status,
                "numeric_value": "MISSING",
                "units": units,
                "source_path": "MISSING_PARENT_OR_BOUND_SOURCE",
                "note": note,
            }
        )
        rows.append(row)
    return rows


def arena_routing_rows() -> list[dict[str, object]]:
    specs = [
        ("ARENA2012_0_Newton", "C_A, f_A(r)", "a_A^i=(c^2/2) partial^i h_A00", "MISSING_PROFILE_AND_BOUND"),
        ("ARENA2012_1_PPN", "C_A, lambda_A, J_PPN[A]", "delta gamma,beta,alpha_i from weak-field decomposition", "MISSING_RESPONSE_MATRIX"),
        ("ARENA2012_2_clock", "C_A, f_A(site)", "delta nu/nu = 0.5 Delta h_A00", "MISSING_CLOCK_PROFILE_AND_BOUND"),
        ("ARENA2012_3_orbital", "h_A_mu_nu along orbit/ray", "integrated perturbation of light-time/perihelion/ephemeris", "MISSING_ORBITAL_KERNEL_AND_BOUND"),
        ("ARENA2012_4_R10", "alpha_A(lambda_A)", "abs(alpha_A)<=alpha_bound(lambda_A)", "MISSING_FULL_CURVE_AND_ALPHA_MATCH"),
        ("ARENA2012_5_WEP", "matter no-spurion plus Q_A source neutrality", "composition dependence must be zero or bounded", "MISSING_NO_SPURION_AND_SOURCE_COMPOSITION"),
        ("ARENA2012_6_q_loc", "q_loc carrier coupling to A hair", "separate from matter Ward zero; include in total stress response", "MISSING_GAMMA_KHAT_EQUATIONS"),
    ]
    rows: list[dict[str, object]] = []
    for arena_id, inputs, observable_rule, status in specs:
        row = base_row()
        row.update(
            {
                "arena_id": arena_id,
                "inputs": inputs,
                "observable_rule": observable_rule,
                "status": status,
                "score_ready": "false",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("CG2012_0_nohair_attempt", "A-current nohair theorem attempted", "PASS_NONCLAIM", "zero routes audited"),
        ("CG2012_1_current_conservation", "ordinary current conservation kills Q_A", "FAIL_REJECTED", "conservation leaves constant charge/hair"),
        ("CG2012_2_source_neutrality", "Pi_A^n=0 or Q_A=0 parent-derived", "FAIL_BLOCKED", "source/boundary action and no-spurion source neutrality missing"),
        ("CG2012_3_gauge_topology", "Q_A gauge/topological zero", "FAIL_BLOCKED", "no first-class generator or topological source representation found"),
        ("CG2012_4_finite_QA_rows", "finite Q_A residual rows staged", "PASS_NONCLAIM", "rows exist but all numeric/source inputs are missing"),
        ("CG2012_5_arena_score_ready", "Newton/PPN/clock/orbital/R10 arenas score-ready", "FAIL_BLOCKED", "coefficients, profiles, response matrices, and bounds missing"),
        ("CG2012_6_local_GR_Newton", "local GR/Newton derived", "FAIL_BLOCKED", "finite Q_A, q_loc, R11, matter silence, and A ownership remain open"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, gate, status, reason in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "status": status,
                "reason": reason,
                "passed_for_claim": "false",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2012_0_result",
            "A_CURRENT_NOHAIR_NOT_DERIVED",
            "The only honest zero routes are source-neutrality, true gauge charge, or topological zero; none are parent-signed.",
            "retain finite Q_A residual rows and stop treating conservation/falloff as a pass",
        ),
        (
            "DEC2012_1_best_derivation_route",
            "SOURCE_NEUTRALITY_BOUNDARY_VARIATION_IS_THE_BEST_ZERO_ROUTE",
            "The cleanest proof would show Pi_A^n=0 from the parent source/boundary action and matter no-spurion silence.",
            "target parent boundary/source action only if enough source text exists; otherwise move to finite-bound acquisition",
        ),
        (
            "DEC2012_2_testing_route",
            "FINITE_QA_BRANCH_NOW_HAS_EXPLICIT_ROWS",
            "If Q_A is not zero, it becomes C_A/lambda_A/profile/alpha_A and must face Newton/PPN/clock/orbital/R10 bounds.",
            "next work should acquire or derive the first real coefficient/bound input",
        ),
    ]
    rows: list[dict[str, object]] = []
    for decision_id, verdict, rationale, next_action in specs:
        row = base_row()
        row.update(
            {
                "decision_id": decision_id,
                "verdict": verdict,
                "rationale": rationale,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2012_0_2013",
            "selected": "true",
            "next_doc": "2013-Y5-R2FR-Aframe-finite-QA-bound-source-acquisition-or-boundary-neutrality-proof.md",
            "next_script": "scripts/Y5_R2FR_Aframe_finite_QA_bound_source_acquisition_or_boundary_neutrality_proof_2013.py",
            "objective": "try one focused parent boundary/source-neutrality proof for Pi_A^n=0; if not signed, acquire/source real finite Q_A/C_A/lambda_A bound inputs for the A-frame residual comparator",
            "include": "Pi_A boundary variation; source neutrality clauses; matter no-spurion; finite Q_A coefficient schema; R10 full curve requirement; PPN/clock/orbital bound source ledger",
            "exclude": "ordinary current conservation as zero proof; asymptotic falloff as nohair; scalar exact-gradient retry; local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2012_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    nohair: list[dict[str, object]],
    finite_qa: list[dict[str, object]],
    arenas: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks = [
        ("VAL2012_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"),
        ("VAL2012_01_nohair_not_promoted", any(row["status"] == "NOHAIR_NOT_DERIVED" for row in nohair) and all(row["parent_signed"] == "false" for row in nohair), "A-current nohair theorem not falsely promoted"),
        ("VAL2012_02_conservation_rejected", any(row["status"] == "REJECTED_AS_ZERO_PROOF" for row in nohair), "ordinary conservation/falloff rejected as nohair proof"),
        ("VAL2012_03_finite_rows_nonclaim", all(row["numeric_value"] == "MISSING" and row["valid_for_claim"] == "false" for row in finite_qa), "finite Q_A rows remain missing/nonclaim"),
        ("VAL2012_04_finite_rows_core_slots", {"FQA2012_0_QA", "FQA2012_2_CA", "FQA2012_3_lambdaA", "FQA2012_5_alpha", "FQA2012_6_PPN"}.issubset({row["row_id"] for row in finite_qa}), "finite Q_A rows cover Q_A/C_A/lambda_A/alpha/PPN"),
        ("VAL2012_05_arenas_blocked", all(row["score_ready"] == "false" for row in arenas), "all arena routes remain blocked until inputs exist"),
        ("VAL2012_06_claim_gates_blocked", all(row["passed_for_claim"] == "false" for row in claim_gates), "all claim gates remain blocked"),
        ("VAL2012_07_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2012_08_branch_copies", all(path.exists() for path in branch_paths), "branch-copy CSVs exist"),
        ("VAL2012_09_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"),
        ("VAL2012_10_output_scope", all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]), "all outputs are under post-checkpoint-work"),
    ]
    rows: list[dict[str, object]] = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = all(row["status"] == "PASS" for row in rows)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2012_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2012 A-frame current nohair/source-neutrality theorem or finite Q_A row",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    nohair: list[dict[str, object]],
    finite_qa: list[dict[str, object]],
    arenas: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2012 Y5 R2FR: A-Frame Current Nohair Source-Neutrality Theorem Or Finite Q_A Row

Private checkpoint. This tests whether the A-current charge `Q_A` can be killed properly, or whether it must become a finite residual.

## Current Verdict

The A-current nohair theorem is **not derived yet**. Ordinary current conservation gives at best `Q_A=constant`; it does not give `Q_A=0`. Asymptotic falloff is also not enough, because a finite exterior charge can still appear as `1/r`, Yukawa, screened, or compact-profile hair.

The clean zero routes are now sharply named: source neutrality (`Pi_A^n=0`), a true gauge charge whose readout is quotient-trivial, or a topological/source-representation zero. None is parent-signed in the inspected corpus.

Therefore finite `Q_A` is retained as an explicit residual branch. It now has rows for `Q_A`, `Pi_A^n`, `C_A`, `lambda_A`, `f_A(r)`, `alpha_A(lambda_A)`, PPN, and the total local response vector. These are not evidence yet; they are the refusal-to-cheat plumbing for the next empirical/theory gate.

No local-GR/Newton/WEP/R10 claim is promoted.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## A-Current Nohair Attempt
{md_table(nohair, ["nohair_id", "object", "status", "missing_before_claim", "parent_signed"])}

## Finite Q_A Residual Rows
{md_table(finite_qa, ["row_id", "symbol", "meaning", "relation", "status", "numeric_value", "units", "note"])}

## Arena Routing
{md_table(arenas, ["arena_id", "inputs", "observable_rule", "status", "score_ready"])}

## Claim Gates
{md_table(claim_gates, ["gate_id", "gate", "status", "reason", "passed_for_claim"])}

## Decision Ledger
{md_table(decisions, ["decision_id", "verdict", "rationale", "next_action"])}

## Branch Copies
{md_table(branch_copies, ["copy_id", "copy_path", "exists", "note"])}

## Next Target
{md_table(next_target, ["target_id", "next_doc", "objective", "include", "exclude"])}

## Validation
{md_table(validation, ["check_id", "status", "detail"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    nohair = nohair_attempt_rows()
    finite_qa = finite_qa_rows()
    arenas = arena_routing_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2012_SOURCE_REGISTER.csv",
        "nohair": OUT / "P8_Y5_PARENT_QLOC_2012_A_CURRENT_NOHAIR_ATTEMPT.csv",
        "finite_qa": OUT / "P8_Y5_PARENT_QLOC_2012_FINITE_QA_RESIDUAL_ROWS.csv",
        "arenas": OUT / "P8_Y5_PARENT_QLOC_2012_ARENA_ROUTING.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2012_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2012_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2012_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["nohair"], nohair)
    write_csv(output_map["finite_qa"], finite_qa)
    write_csv(output_map["arenas"], arenas)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_QA_NOHAIR_2012_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2012_FINITE_QA_STATUS_NONCLAIM.csv",
        QUEUE / "JR2012_AFRAME_FINITE_QA_BOUND_SOURCE_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["nohair"], branch_paths[0])
    shutil.copyfile(output_map["finite_qa"], branch_paths[1])
    shutil.copyfile(output_map["arenas"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-current nohair attempt nonclaim copy",
            "finite Q_A residual status nonclaim copy",
            "finite Q_A arena/bound-source queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2012_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, nohair, finite_qa, arenas, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2012_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, nohair, finite_qa, arenas, claim_gates, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2012_OVERALL"][0]["status"]
    print(f"VAL2012_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
