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
DOC = ROOT / "2011-Y5-R2FR-covariant-MTS-current-source-law-for-Aframe-or-first-coefficient-dry-run.md"
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
            "SRC2011_00_2010_handoff",
            "2010-Y5-R2FR-Aframe-parent-source-map-rank-certificate-or-residual-coefficient-source-pack.md",
            ["NEXT2010_0_2011", "DEC2010_1_best_derivation_route", "VAL2010_OVERALL"],
            "2010 selected covariant MTS current/source law or first coefficient dry-run.",
        ),
        (
            "SRC2011_01_2009_kernel",
            "2009-Y5-R2FR-Aframe-no-extra-mode-theorem-or-first-residual-response-kernel.md",
            ["KER2009_5_R10_yukawa_projection", "KER2009_7_total_response_vector", "VAL2009_OVERALL"],
            "symbolic A-frame residual kernel to feed if source-law derivation fails.",
        ),
        (
            "SRC2011_02_cell_current_warning",
            "11-cell-current-origin-attempt.md",
            ["cell_current_origin_no_charge_obstruction", "Q_R = constant.", "ordinary cell-current conservation does not close"],
            "ordinary conserved current leaves hair unless a no-charge theorem is supplied.",
        ),
        (
            "SRC2011_03_parent_current_chain",
            "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            ["PCS1009_4_Gamma_Khat_extra", "DEC1009_1_root_hard_block", "V1009_SUMMARY"],
            "parent current-chain action contract and Gamma/Khat/q_loc action-existence blocker.",
        ),
        (
            "SRC2011_04_source_hunt_warning",
            "1266-Y5-R10-RAB-primitive-auxiliary-grammar-source-hunt-or-finite-ZR-intake-review.md",
            ["HUNT1266_7_cell_current", "DEC1266_1_best_derivation_route", "VAL1266_3_source_hunt_nonclaim"],
            "source-hunt warning that ordinary current conservation gives hair unless a constraint already exists.",
        ),
        (
            "SRC2011_05_local_residuals",
            "790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md",
            ["LSG790_0_Ward_compatible_split", "LSG790_3_anisotropic_PPN_suppression", "D790_1_Q_first"],
            "Bianchi-compatible residual split and PPN suppression gates.",
        ),
        (
            "SRC2011_06_q_loc_split",
            "791-Y5-R10-Ward-compatible-exchange-current-q-loc-zero-or-bound.md",
            ["ECT791_1_q_loc_geometric", "WZG791_3_geometric_q_loc_zero", "D791_1_q_loc_still_open"],
            "ordinary matter Ward zero does not automatically kill geometric q_loc.",
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
                "needed_for": "2011 covariant MTS current source law for A-frame or first coefficient dry-run",
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


def current_source_attempt_rows() -> list[dict[str, object]]:
    specs = [
        (
            "CSA2011_0_target",
            "J_MTS^a_mu -> A^a_MTS",
            "Find a Lorentz-vector one-form current/moment source such that a covariant A-equation generates nonholonomic tetrad deformation without matter spurions.",
            "TARGET_EXACT",
            "needs parent action, covariance, split-gauge compatibility, rank/domain certificate, and no-hair/no-spurion clauses",
            "false",
        ),
        (
            "CSA2011_1_ordinary_conserved_current",
            "D_mu J_MTS^{a mu}=0",
            "Conservation alone gives a constant exterior charge/hair, by analogy with the reciprocal-cell current obstruction.",
            "REJECTED_AS_ZERO_THEOREM",
            "it can make A source conserved, but does not prove the A charge/amplitude is zero or small",
            "false",
        ),
        (
            "CSA2011_2_Ward_Noether_current",
            "J_MTS from diffeo/local-Lorentz Noether identity",
            "A Noether identity can enforce compatibility of the total equations, but it does not by itself define a nonzero source law or kill boundary charge.",
            "WARD_COMPATIBLE_NOT_SOURCE_MAP",
            "requires a parent action and boundary charge theorem before it becomes ownership",
            "false",
        ),
        (
            "CSA2011_3_moment_current_candidate",
            "J_MTS^a_mu = P^a_rho D_nu M_MTS^{rho nu}{}_mu or covariant projection of coarse-grained motion moments",
            "This is the least-circular route: source A from covariant MTS moments rather than a single scalar or exact labels.",
            "PROMISING_FORMAL_CANDIDATE",
            "the moment tensor, projector, evolution equation, and projection to Lorentz-vector one-form are not parent-derived",
            "false",
        ),
        (
            "CSA2011_4_action_equation_candidate",
            "E_A^a_mu := delta S_A/delta A^a_mu = kappa_A J_MTS^a_mu",
            "A variational equation would make A ownership inspectable and connect coefficients to first variation.",
            "FORMAL_EQUATION_ONLY",
            "no S_A, Helmholtz-compatible E_A, theta_A, or Q_tau contribution is sourced",
            "false",
        ),
        (
            "CSA2011_5_green_function_candidate",
            "A^a_mu(x)=kappa_A integral G_A(x,y) J_MTS^a_mu(y) dV_y",
            "This is executable for tests and gives C_A, lambda_A, and profile slots.",
            "TESTABLE_RESIDUAL_ROUTE",
            "it is a finite residual/source model unless kappa_A, G_A, and J_MTS are parent-derived",
            "false",
        ),
        (
            "CSA2011_6_rank_domain",
            "rank(delta A/delta J_MTS * delta J_MTS/delta Phi_MTS)",
            "Even with a current, the map must cover tetrad/metric variations and preserve determinant/signature.",
            "MISSING_RANK_DOMAIN_CERTIFICATE",
            "no current map is available to certify rank or local Lorentzian domain",
            "false",
        ),
        (
            "CSA2011_7_verdict",
            "covariant MTS current source law",
            "A credible current/source-law scaffold exists, but it is not derived from the parent corpus; ordinary current conservation is specifically not enough.",
            "CURRENT_SOURCE_LAW_NOT_DERIVED",
            "move to A-current no-hair/source-neutrality theorem or keep coefficient dry-run as fallback",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for current_id, object_text, attempt, status, missing_before_claim, parent_signed in specs:
        row = base_row()
        row.update(
            {
                "current_id": current_id,
                "object": object_text,
                "attempt": attempt,
                "status": status,
                "missing_before_claim": missing_before_claim,
                "parent_signed": parent_signed,
            }
        )
        rows.append(row)
    return rows


def covariance_guard_rows() -> list[dict[str, object]]:
    specs = [
        (
            "COV2011_0_diffeomorphism",
            "J_MTS^a_mu is a covariant one-form density or one-form with measure fixed by e",
            "required so A equation has tensor meaning and total Ward identity can close",
            "UNSIGNED",
        ),
        (
            "COV2011_1_local_Lorentz",
            "J_MTS^a_mu transforms as an internal Lorentz vector and has no preferred-frame spurion",
            "required so the completed tetrad does not carry hidden species/readout frame labels",
            "UNSIGNED",
        ),
        (
            "COV2011_2_split_gauge",
            "source law depends on e=dX+A or split-gauge invariant combinations, not X and A separately in observable sectors",
            "protects the no-extra-mode closure theorem from 2009",
            "UNSIGNED",
        ),
        (
            "COV2011_3_Bianchi",
            "D_mu E_A^{a mu}=D_mu(kappa_A J_MTS^{a mu}) is compatible with total stress conservation",
            "prevents an A source from becoming an unbalanced q_loc or non-geodesic force",
            "UNSIGNED",
        ),
        (
            "COV2011_4_boundary_nohair",
            "surface charge Q_A=integral_boundary *J_A or conjugate Pi_A^n vanishes or is bounded",
            "ordinary current conservation alone leaves charge hair",
            "MISSING_NOHAIR_THEOREM",
        ),
        (
            "COV2011_5_matter_blindness",
            "ordinary matter couples to e, omega[e], and owned gauge fields only",
            "needed for Ward matter-zero and WEP/clock safety",
            "UNSIGNED",
        ),
        (
            "COV2011_6_guard_verdict",
            "all covariance guards",
            "the source-current route is meaningful but cannot be promoted without these guards",
            "GUARDS_NOT_PARENT_SIGNED",
        ),
    ]
    rows: list[dict[str, object]] = []
    for guard_id, clause, why_needed, status in specs:
        row = base_row()
        row.update(
            {
                "guard_id": guard_id,
                "clause": clause,
                "why_needed": why_needed,
                "status": status,
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )
        rows.append(row)
    return rows


def coefficient_dry_run_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DRY2011_0_C_A",
            "C_A",
            "overall A-source coupling/amplitude",
            "A response amplitude from A=kappa_A G_A*J_MTS",
            "MISSING_PARENT_COEFFICIENT",
            "REFUSED_PLACEHOLDER",
            "required before Newton/PPN/clock/R10 scoring",
        ),
        (
            "DRY2011_1_lambda_A",
            "lambda_A",
            "range/correlation length or inverse mass of A residual",
            "lambda_A from Green kernel pole or screening profile",
            "MISSING_RANGE_OR_SCREENING_MAP",
            "REFUSED_PLACEHOLDER",
            "required before R10/orbital profile scoring",
        ),
        (
            "DRY2011_2_f_A",
            "f_A(r)",
            "normalized local source profile",
            "h_A00(r)=2 C_A f_A(r) in weak-field normalization after gauge fixing",
            "MISSING_PROFILE",
            "REFUSED_PLACEHOLDER",
            "required before acceleration/clock/orbital integrals",
        ),
        (
            "DRY2011_3_alpha_A",
            "alpha_A(lambda_A)",
            "Yukawa-equivalent R10 amplitude",
            "if h_A00=2 G M alpha_A exp(-r/lambda_A)/(c^2 r), compare |alpha_A| to bound(lambda_A)",
            "MISSING_C_A_LAMBDA_PROFILE_AND_FULL_BOUND_CURVE",
            "REFUSED_PLACEHOLDER",
            "anchor-only rows remain smoke-only",
        ),
        (
            "DRY2011_4_PPN_vector",
            "delta_PPN_A",
            "PPN residual vector",
            "J_PPN[A] dot (C_A,lambda_A,profile parameters)",
            "MISSING_PPN_RESPONSE_MATRIX",
            "REFUSED_PLACEHOLDER",
            "do not score gamma/beta/alpha_i without weak-field projection",
        ),
        (
            "DRY2011_5_clock_orbit",
            "delta_clock_A, delta_orbit_A",
            "clock and orbital residuals",
            "integrate h_A along clock sites or orbital/light-time kernels",
            "MISSING_SOURCE_PROFILE_AND_BOUNDS",
            "REFUSED_PLACEHOLDER",
            "do not claim local pass from symbolic kernel",
        ),
        (
            "DRY2011_6_q_loc_handoff",
            "h_Q_mu_nu",
            "metric response to geometric q_loc carrier",
            "solve div T_Q=-q_loc and apply linearized response",
            "MISSING_GAMMA_EFF_KHAT_EQUATIONS",
            "REFUSED_PLACEHOLDER",
            "keeps q_loc separate from ordinary matter Ward zero",
        ),
        (
            "DRY2011_7_dry_run_verdict",
            "first coefficient dry-run",
            "dry-run schema is executable but every numeric coefficient is missing",
            "claim false until all inputs are sourced or theorem-zero",
            "ALL_NUMERIC_INPUTS_MISSING",
            "DRY_RUN_PASS_REFUSAL",
            "this is good plumbing, not evidence",
        ),
    ]
    rows: list[dict[str, object]] = []
    for dry_id, symbol, meaning, formula_or_rule, missing_input, dry_run_status, note in specs:
        row = base_row()
        row.update(
            {
                "dry_id": dry_id,
                "symbol": symbol,
                "meaning": meaning,
                "formula_or_rule": formula_or_rule,
                "missing_input": missing_input,
                "numeric_value": "MISSING",
                "units": "MISSING",
                "source_path": "MISSING_PARENT_OR_BOUND_SOURCE",
                "dry_run_status": dry_run_status,
                "note": note,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("CG2011_0_current_scaffold", "covariant current source scaffold written", "PASS_NONCLAIM", "formal source-law rows exist"),
        ("CG2011_1_current_derivation", "J_MTS -> A parent-derived", "FAIL_BLOCKED", "no parent S_A/E_A/J_MTS derivation or variation certificate"),
        ("CG2011_2_ordinary_current_zero", "ordinary current conservation proves A charge zero", "FAIL_REJECTED", "conservation leaves exterior charge/hair unless no-hair theorem is added"),
        ("CG2011_3_covariance_guards", "diffeo/Lorentz/split-gauge/Bianchi guards signed", "FAIL_BLOCKED", "guards are requirements, not parent-signed results"),
        ("CG2011_4_coeff_dry_run", "first coefficient dry-run refuses placeholders", "PASS_NONCLAIM", "C_A, lambda_A, alpha_A slots are explicit but missing"),
        ("CG2011_5_R10_PPN_clock_orbit", "local arenas score-ready", "FAIL_BLOCKED", "no coefficients, full bound curves, or response matrices"),
        ("CG2011_6_local_GR_Newton", "local GR/Newton derived", "FAIL_BLOCKED", "A ownership, nohair, q_loc, R11, and matter silence remain open"),
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
            "DEC2011_0_result",
            "COVARIANT_CURRENT_SOURCE_LAW_NOT_DERIVED",
            "A credible J_MTS -> A scaffold can be written, but the parent action, source current, and boundary no-hair theorem are missing.",
            "do not claim A ownership; attack the A-current no-hair/source-neutrality theorem next",
        ),
        (
            "DEC2011_1_current_warning",
            "ORDINARY_CURRENT_CONSERVATION_IS_NOT_ENOUGH",
            "The project has seen this trap before: a conserved current can leave Q_A/Q_R hair, which is exactly a finite local residual.",
            "require Q_A=0 from gauge/topology/boundary silence or keep finite coefficient rows",
        ),
        (
            "DEC2011_2_testing_plumbing",
            "FIRST_C_A_LAMBDA_ALPHA_DRY_RUN_READY_BUT_EMPTY",
            "The R10/PPN/clock/orbital plumbing now refuses placeholders while preserving the exact coefficient slots we need.",
            "fill coefficients only from parent derivation or source-backed bounds/profiles",
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
            "target_id": "NEXT2011_0_2012",
            "selected": "true",
            "next_doc": "2012-Y5-R2FR-Aframe-current-nohair-source-neutrality-theorem-or-finite-QA-row.md",
            "next_script": "scripts/Y5_R2FR_Aframe_current_nohair_source_neutrality_theorem_or_finite_QA_row_2012.py",
            "objective": "try to prove the A-current charge Q_A vanishes by gauge/topology/source-neutrality/boundary silence; if not, create finite Q_A/C_A/lambda_A residual rows for the A-frame kernel",
            "include": "Q_A definition; boundary momentum Pi_A^n; nohair theorem clauses; split-gauge and matter silence; finite residual coefficient rows; R10/PPN/clock/orbital routing",
            "exclude": "ordinary current conservation as zero proof; scalar exact-gradient retry; unlabelled tetrad insertion; local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2011_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    current_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks = [
        ("VAL2011_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"),
        ("VAL2011_01_current_not_promoted", any(row["status"] == "CURRENT_SOURCE_LAW_NOT_DERIVED" for row in current_rows) and all(row["parent_signed"] == "false" for row in current_rows), "current source law not falsely promoted"),
        ("VAL2011_02_ordinary_current_rejected", any(row["status"] == "REJECTED_AS_ZERO_THEOREM" for row in current_rows), "ordinary current conservation rejected as zero theorem"),
        ("VAL2011_03_covariance_guards_unsigned", any(row["status"] == "GUARDS_NOT_PARENT_SIGNED" for row in guard_rows), "covariance/no-spurion guards remain unsigned"),
        ("VAL2011_04_dry_run_refuses_placeholders", all(row["numeric_value"] == "MISSING" and row["valid_for_claim"] == "false" for row in dry_rows), "coefficient dry-run rows remain missing/nonclaim"),
        ("VAL2011_05_dry_run_covers_core_slots", {"DRY2011_0_C_A", "DRY2011_1_lambda_A", "DRY2011_3_alpha_A", "DRY2011_4_PPN_vector", "DRY2011_6_q_loc_handoff"}.issubset({row["dry_id"] for row in dry_rows}), "dry-run covers C_A/lambda_A/alpha_A/PPN/q_loc"),
        ("VAL2011_06_claim_gates_blocked", all(row["passed_for_claim"] == "false" for row in claim_gates), "all claim gates remain blocked"),
        ("VAL2011_07_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2011_08_branch_copies", all(path.exists() for path in branch_paths), "branch-copy CSVs exist"),
        ("VAL2011_09_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"),
        ("VAL2011_10_output_scope", all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]), "all outputs are under post-checkpoint-work"),
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
            "check_id": "VAL2011_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2011 covariant MTS current source law for A-frame or first coefficient dry-run",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    current_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2011 Y5 R2FR: Covariant MTS Current Source Law For A-Frame Or First Coefficient Dry-Run

Private checkpoint. This attacks the least-circular route left by 2010: derive a covariant MTS moment/current that sources `A^a_MTS`, or turn the A-frame residual into coefficient rows that refuse placeholders.

## Current Verdict

The covariant source-law route is **not derived yet**. A plausible scaffold can be written:

`E_A^a_mu = delta S_A/delta A^a_mu = kappa_A J_MTS^a_mu`, with `A^a_mu(x)=kappa_A integral G_A(x,y)J_MTS^a_mu(y)dV_y`.

But this is not yet a parent theorem. The parent action `S_A`, the current `J_MTS`, the Green kernel, the rank/domain certificate, and the boundary no-hair theorem are all missing. Most importantly, ordinary current conservation is explicitly not enough: it can leave an exterior A-charge/hair, just like the earlier reciprocal-cell current obstruction.

The practical win is that the first coefficient dry-run now exists and refuses fake numbers. `C_A`, `lambda_A`, `f_A(r)`, `alpha_A(lambda_A)`, PPN, clock/orbital, and `q_loc` handoff slots are named, but all remain nonclaim until sourced or theorem-zeroed.

No local-GR/Newton/WEP/R10 claim is promoted.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## Covariant Current Source-Law Attempt
{md_table(current_rows, ["current_id", "object", "status", "missing_before_claim", "parent_signed"])}

## Covariance And No-Spurion Guards
{md_table(guard_rows, ["guard_id", "clause", "why_needed", "status"])}

## First Coefficient Dry-Run
{md_table(dry_rows, ["dry_id", "symbol", "meaning", "formula_or_rule", "missing_input", "dry_run_status", "note"])}

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
    current_rows = current_source_attempt_rows()
    guard_rows = covariance_guard_rows()
    dry_rows = coefficient_dry_run_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2011_SOURCE_REGISTER.csv",
        "current_attempt": OUT / "P8_Y5_PARENT_QLOC_2011_COVARIANT_CURRENT_SOURCE_ATTEMPT.csv",
        "guards": OUT / "P8_Y5_PARENT_QLOC_2011_COVARIANCE_GUARD_AUDIT.csv",
        "dry_run": OUT / "P8_Y5_PARENT_QLOC_2011_FIRST_COEFFICIENT_DRY_RUN.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2011_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2011_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2011_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["current_attempt"], current_rows)
    write_csv(output_map["guards"], guard_rows)
    write_csv(output_map["dry_run"], dry_rows)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "COVARIANT_MTS_CURRENT_AFRAME_2011_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2011_CURRENT_SOURCE_STATUS_NONCLAIM.csv",
        QUEUE / "JR2011_AFRAME_COEFFICIENT_DRY_RUN_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["current_attempt"], branch_paths[0])
    shutil.copyfile(output_map["guards"], branch_paths[1])
    shutil.copyfile(output_map["dry_run"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "covariant MTS current A-frame attempt nonclaim copy",
            "A-frame current covariance/no-spurion guard status nonclaim copy",
            "A-frame coefficient dry-run queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2011_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, current_rows, guard_rows, dry_rows, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2011_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, current_rows, guard_rows, dry_rows, claim_gates, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2011_OVERALL"][0]["status"]
    print(f"VAL2011_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
