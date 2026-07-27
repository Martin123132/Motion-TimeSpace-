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
DOC = ROOT / "2016-Y5-R2FR-Aframe-no-physical-pole-gauge-constraint-theorem-or-finite-prior-runner.md"
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


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


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
        {
            "source_id": "SRC2016_00_2015_handoff",
            "path": ROOT / "2015-Y5-R2FR-Aframe-parent-quadratic-action-ZA-lambdaA-source-charge-or-finite-prior-envelope.md",
            "needles": ["NEXT2015_0_2016", "PQA2015_9_verdict", "VAL2015_OVERALL"],
            "note": "2015 handoff to no-physical-A-pole theorem or finite-prior runner.",
        },
        {
            "source_id": "SRC2016_01_2009_closure",
            "path": ROOT / "2009-Y5-R2FR-Aframe-no-extra-mode-theorem-or-first-residual-response-kernel.md",
            "needles": ["NEM2009_1_variation_chain_rule", "NEM2009_3_kinetic_A_branch", "DEC2009_0_result"],
            "note": "conditional e-only closure theorem and independent-A warning.",
        },
        {
            "source_id": "SRC2016_02_2010_no_spurion",
            "path": ROOT / "2010-Y5-R2FR-Aframe-parent-source-map-rank-certificate-or-residual-coefficient-source-pack.md",
            "needles": ["NSP2010_0_matter_functor", "NSP2010_6_verdict", "VAL2010_OVERALL"],
            "note": "A-frame no-spurion/matter-readout silence requirements.",
        },
        {
            "source_id": "SRC2016_03_2012_QA_nohair",
            "path": ROOT / "2012-Y5-R2FR-Aframe-current-nohair-source-neutrality-theorem-or-finite-QA-row.md",
            "needles": ["NHA2012_4_gauge_charge", "FQA2012_0_QA", "VAL2012_OVERALL"],
            "note": "finite Q_A/nohair obstruction to a naked alpha_A=0 claim.",
        },
        {
            "source_id": "SRC2016_04_2014_green_kernel",
            "path": ROOT / "2014-Y5-R2FR-Aframe-Green-kernel-normalization-or-QA-comparator-refusal-runner.md",
            "needles": ["AGK2014_7_pure_gauge_branch", "FAC2014_2_ZA", "VAL2014_OVERALL"],
            "note": "A Green-kernel factorization and pure-gauge branch warning.",
        },
        {
            "source_id": "SRC2016_05_581_no_pole_template",
            "path": OUT / "P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv",
            "needles": ["NPC581_0_configuration_space", "NPC581_4_boundary_silence", "NPC581_6_claim_gate"],
            "note": "generic no-pole certificate template.",
        },
        {
            "source_id": "SRC2016_06_582_momentum",
            "path": OUT / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
            "needles": ["MMT582_0_constraint_generator", "MMT582_4_no_pole_result", "MMT582_5_failure_result"],
            "note": "first-class momentum-map closure theorem template.",
        },
        {
            "source_id": "SRC2016_07_590_vertical_map",
            "path": OUT / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
            "needles": ["metric_or_coframe", "matter_readout", "boundary_edge"],
            "note": "field-by-field vertical generator map template.",
        },
        {
            "source_id": "SRC2016_08_670_no_pole_chain",
            "path": OUT / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
            "needles": ["NQ670_0_null_distribution", "NQ670_5_matter_descent", "NQ670_7_boundary_and_degree_count"],
            "note": "later no-pole quotient proof chain.",
        },
    ]
    rows: list[dict[str, object]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = spec["needles"]
        needles_ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": spec["source_id"],
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if needles_ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": spec["note"],
            }
        )
        rows.append(row)
    return rows


def no_pole_theorem_rows() -> list[dict[str, object]]:
    data = [
        {
            "theorem_id": "ANP2016_0_e_only_closure",
            "clause": "strict tetrad/public-frame closure",
            "formula": "e^a_mu=dX^a_mu + A^a_mu and S_parent=S_red[e,omega[e],Psi,theta]",
            "status": "PROVED_ONLY_INSIDE_CLOSURE_BRANCH",
            "what_is_proved": "delta S/delta A equals the tetrad equation, so A has no independent local Green pole.",
            "missing_before_claim": "parent action must exclude independent A kinetic/source/boundary terms.",
            "closure_proved": True,
        },
        {
            "theorem_id": "ANP2016_1_parent_quotient_map",
            "clause": "A is vertical for a parent quotient map",
            "formula": "D q_A[v_A]=0 with q_A(Phi) fixed before variation",
            "status": "MISSING_A_SPECIFIC_QUOTIENT_MAP",
            "what_is_proved": "generic quotient-zero template exists.",
            "missing_before_claim": "the actual q_A map and v_A action on all MTS parent fields are not sourced.",
            "closure_proved": False,
        },
        {
            "theorem_id": "ANP2016_2_action_descent",
            "clause": "bulk action descends through q_A",
            "formula": "S_bulk[Phi]=S_red[q_A(Phi)] and L_{v_A} S_bulk=0",
            "status": "CONDITIONAL_DESCENT_NOT_PARENT_SIGNED",
            "what_is_proved": "if descent holds, the A-Hessian vertical block is gauge/null, not a physical pole.",
            "missing_before_claim": "no parent action row proves descent or forbids independent A/torsion terms.",
            "closure_proved": False,
        },
        {
            "theorem_id": "ANP2016_3_first_class_generator",
            "clause": "split-gauge/vertical A direction is first-class",
            "formula": "i_{v_A} Omega_parent = delta G_A[epsilon], G_A=int epsilon C_A + Q_A",
            "status": "MISSING_PARENT_OMEGA_DCA_VERTICAL_GENERATOR",
            "what_is_proved": "581/582/590/670 give the exact momentum-map certificate shape.",
            "missing_before_claim": "Omega_parent, D C_A, bracket closure, and all-field v_A are missing for A.",
            "closure_proved": False,
        },
        {
            "theorem_id": "ANP2016_4_no_hidden_pole",
            "clause": "Hessian null direction is not a hidden second-class or edge mode",
            "formula": "rank reduction removes the A canonical pair and reduced Omega has no A stabilizer",
            "status": "MISSING_DEGREE_COUNT_AND_REDUCED_NONDEGENERACY",
            "what_is_proved": "a test exists for distinguishing gauge null directions from hidden dynamics.",
            "missing_before_claim": "no A-specific constraint/rank/degree count has been evaluated.",
            "closure_proved": False,
        },
        {
            "theorem_id": "ANP2016_5_boundary_charge_silence",
            "clause": "local A vertical transformations carry no source or edge charge",
            "formula": "Q_A[epsilon]=0/exact/proper and K_boundary^A=0 on compact local branch",
            "status": "MISSING_BOUNDARY_CHARGE_ZERO",
            "what_is_proved": "2012/2013 already show ordinary conservation/falloff does not kill Q_A.",
            "missing_before_claim": "parent boundary/source variation must prove Pi_A^n=0 or pure-gauge charge.",
            "closure_proved": False,
        },
        {
            "theorem_id": "ANP2016_6_matter_readout_descent",
            "clause": "ordinary matter/readout is blind to the A representative",
            "formula": "S_matter=Sbar[Psi,e_pub(q_A),omega[e_pub],theta(q_A)] and L_{v_A} theta=0",
            "status": "MISSING_NO_SPURION_MATTER_SIGNATURE",
            "what_is_proved": "2010 gives the no-spurion clause list; it is mandatory for WEP/clock safety.",
            "missing_before_claim": "matter, clocks, source masses, constants, and boundary source measures are not parent-signed.",
            "closure_proved": False,
        },
        {
            "theorem_id": "ANP2016_7_projection_silence",
            "clause": "no A representative leaks into metric/PPN/readout projection",
            "formula": "P_00^A v_A=0 and J_PPN[A_pure_gauge]=0 after gauge fixing",
            "status": "MISSING_A_PROJECTION_SILENCE",
            "what_is_proved": "pure-gauge A should be unobservable if the public tetrad projection is the only readout.",
            "missing_before_claim": "P_00^A, clock/orbital projection, and gauge-fixing convention remain missing.",
            "closure_proved": False,
        },
        {
            "theorem_id": "ANP2016_8_verdict",
            "clause": "no physical local A pole in the GR/Newton branch",
            "formula": "ANP2016_0 through ANP2016_7 close from one parent action",
            "status": "FAIL_CURRENT_CLAIM_A_NO_POLE_NOT_PARENT_SIGNED",
            "what_is_proved": "the exact theorem is now written; the closure branch is mathematically clean.",
            "missing_before_claim": "A-specific quotient/action descent, first-class generator, boundary silence, degree count, matter/readout descent, and projection silence.",
            "closure_proved": False,
        },
    ]
    rows = []
    for item in data:
        row = base_row()
        row.update(
            {
                **item,
                "parent_signed": False,
                "claim_policy": "NONCLAIM_UNTIL_ALL_CLAUSES_PARENT_SIGNED",
            }
        )
        rows.append(row)
    return rows


def countermodel_rows() -> list[dict[str, object]]:
    data = [
        {
            "countermodel_id": "PCM2016_0_independent_A_kinetic",
            "countermodel": "the parent action contains Z_A (dA)^2 or torsion-like A kinetic terms",
            "why_it_matters": "then A has a real propagator/pole and no-pole closure is false.",
            "blocked_by": "explicit parent action descent or Z_A=0 constraint theorem",
        },
        {
            "countermodel_id": "PCM2016_1_second_class_A_constraint",
            "countermodel": "A looks constrained but the bracket is second-class or rank-incomplete",
            "why_it_matters": "a hidden local mode can remain even with a degenerate Hessian.",
            "blocked_by": "Omega/D C_A/bracket closure/degree-count certificate",
        },
        {
            "countermodel_id": "PCM2016_2_edge_or_source_charge",
            "countermodel": "bulk A is gauge but Q_A or K_boundary^A survives at compact source boundary",
            "why_it_matters": "R10/PPN can see edge hair even when the bulk pole is absent.",
            "blocked_by": "Q_A=0/exact/proper and K_boundary^A=0 proof",
        },
        {
            "countermodel_id": "PCM2016_3_shadow_matter_A_frame",
            "countermodel": "ordinary matter uses an A-dependent Weyl/disformal/source frame",
            "why_it_matters": "WEP can appear common-mode while R10/clock/PPN see beta_source beta_test leakage.",
            "blocked_by": "parent no-spurion matter/readout/source-measure theorem",
        },
        {
            "countermodel_id": "PCM2016_4_projection_leak",
            "countermodel": "A representative enters h_00, clocks, or orbital readout before quotienting",
            "why_it_matters": "pure-gauge language would not protect measured observables.",
            "blocked_by": "P_00^A v_A=0 and public tetrad/readout projection proof",
        },
        {
            "countermodel_id": "PCM2016_5_topological_residual",
            "countermodel": "compact source topology or representation class carries nonzero A charge",
            "why_it_matters": "Q_A can be finite without violating local conservation.",
            "blocked_by": "topological/source-representation zero theorem or finite prior bounds",
        },
    ]
    rows = []
    for item in data:
        row = base_row()
        row.update({**item, "claim_blocks": True})
        rows.append(row)
    return rows


def finite_prior_runner_rows() -> list[dict[str, object]]:
    data = [
        ("FPR2016_0_QA", "Q_A", "finite A charge or edge/source hair", "MISSING_PARENT_BOUNDARY_VARIATION", "A-charge units"),
        ("FPR2016_1_ZA", "Z_A", "A-mode quadratic residue if a physical pole survives", "MISSING_PARENT_RESIDUE", "model-normalized"),
        ("FPR2016_2_lambdaA", "lambda_A", "range/screening length/compact support scale", "MISSING_RANGE_RULE", "m"),
        ("FPR2016_3_kappaA", "kappa_A", "source coupling in E_A=kappa_A J_A", "MISSING_PARENT_COUPLING", "model-normalized"),
        ("FPR2016_4_P00A", "P_00^A", "weak-field metric projection from A to h_00", "MISSING_METRIC_PROJECTION", "dimensionless"),
        ("FPR2016_5_beta_source_A", "beta_source_A", "source leg if A couples through matter/source mass", "MISSING_SOURCE_LEG", "dimensionless"),
        ("FPR2016_6_beta_test_A", "beta_test_A", "test/readout leg if A couples to probe/clock", "MISSING_TEST_LEG", "dimensionless"),
        ("FPR2016_7_profile_A", "f_A(r;lambda_A)", "normalized radial/support profile", "MISSING_PROFILE", "dimensionless"),
        ("FPR2016_8_alphaA", "alpha_A(lambda_A)", "R10 Yukawa-equivalent prediction", "MISSING_ALL_JOIN_INPUTS", "dimensionless"),
        ("FPR2016_9_local_vector", "R_A", "PPN/clock/orbital/R10/q_loc residual vector", "MISSING_ARENA_PROJECTIONS", "mixed"),
    ]
    rows = []
    for row_id, symbol, meaning, status, units in data:
        row = base_row()
        row.update(
            {
                "prior_id": row_id,
                "symbol": symbol,
                "meaning": meaning,
                "if_no_pole_signed": "NOT_APPLICABLE_OR_ZERO",
                "if_no_pole_fails": "REQUIRED_BEFORE_SCORING",
                "status": status,
                "prior_min": "MISSING",
                "prior_max": "MISSING",
                "units": units,
                "score_ready": False,
            }
        )
        rows.append(row)
    return rows


def refusal_rows() -> list[dict[str, object]]:
    data = [
        (
            "REF2016_0_no_pole_claim",
            "claim no physical A pole",
            "REFUSE",
            "A-specific q map, action descent, first-class generator, boundary silence, degree count, matter/readout descent, and projection silence are not parent-signed.",
        ),
        (
            "REF2016_1_alpha_zero",
            "set alpha_A(lambda)=0",
            "REFUSE",
            "alpha_A=0 follows only inside the strict closure/no-pole branch, not from the current parent corpus.",
        ),
        (
            "REF2016_2_finite_prior_score",
            "score finite prior envelope",
            "REFUSE",
            "Q_A, Z_A, lambda_A, kappa_A, P_00^A, source/test legs, and profile are missing.",
        ),
        (
            "REF2016_3_R10",
            "R10 short-range pass",
            "REFUSE",
            "no promoted A-side alpha prediction; external bounds cannot replace theory-side rows.",
        ),
        (
            "REF2016_4_PPN_clock_WEP_orbit",
            "PPN/clock/WEP/orbital local pass",
            "REFUSE",
            "A-to-observable projection and no-spurion matter/source map are missing.",
        ),
        (
            "REF2016_5_local_GR",
            "local GR/Newton derived from A branch",
            "REFUSE",
            "closure branch is promising but not parent-signed; finite residual branch remains live.",
        ),
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


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2016_0_conditional_closure_written", "strict e-only/public-tetrad closure theorem is written", True, "mathematical closure branch exists but is not a parent derivation"),
        ("CG2016_1_parent_no_pole", "A has no physical local pole in the parent corpus", False, "missing quotient/action descent, first-class generator, boundary, degree count, matter/readout, projection"),
        ("CG2016_2_alpha_zero", "alpha_A(lambda_A)=0 can be used in local tests", False, "zero is only conditional until no-pole certificate is signed"),
        ("CG2016_3_finite_prior_runner", "finite A prior runner is score-ready", False, "all numeric/source-backed A-side rows remain missing"),
        ("CG2016_4_R10_score", "R10 can score A branch", False, "alpha_A and promoted A projection absent"),
        ("CG2016_5_PPN_clock_WEP_orbit", "local comparator suite can score A branch", False, "arena projections/source legs absent"),
        ("CG2016_6_local_GR_Newton", "local GR/Newton reduction is derived", False, "A closure is unsigned and q_loc/R11/matter silence remain outside this gate"),
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


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2016_0_result",
            "CONDITIONAL_A_NO_POLE_THEOREM_WRITTEN_PARENT_CLAIM_FAILS",
            "Inside strict e-only/public-tetrad closure, A is a redundant representative and has no independent Green pole. The current parent corpus does not prove that closure.",
            "do not score alpha_A=0; keep finite A residual branch live",
        ),
        (
            "DEC2016_1_not_circling",
            "THIS_IS_NOW_A_SPECIFIC_THEOREM_GATE_NOT_A_VAGUE_COUPLING_GAP",
            "The missing objects are named: q_A, S descent, Omega/D C_A, v_A, Q_A/K_boundary, degree count, matter descent, and P_00 silence.",
            "attack the first object that can kill both no-pole and finite-hair routes: split-gauge generator plus boundary charge",
        ),
        (
            "DEC2016_2_best_next_route",
            "A_SPLIT_GAUGE_GENERATOR_AND_BOUNDARY_CHARGE_ZERO_IS_NEXT",
            "If Q_A and K_boundary vanish for the allowed local split transformation, the finite hair branch collapses cleanly; if not, it becomes the first source row.",
            "build 2017 split-gauge generator/boundary charge zero or finite A-source row",
        ),
        (
            "DEC2016_3_empirical_route",
            "FINITE_PRIOR_RUNNER_EXISTS_ONLY_AS_A_REFUSAL_SCHEMA",
            "No A-side prior/range/coupling/profile row is numeric or source-backed yet, so testing remains blocked but organized.",
            "only run comparator scoring after theory-side rows are real or theorem-zeroed",
        ),
    ]
    rows = []
    for decision_id, verdict, rationale, next_action in data:
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
            "target_id": "NEXT2016_0_2017",
            "next_doc": "2017-Y5-R2FR-Aframe-split-gauge-generator-boundary-charge-zero-or-finite-A-source-row.md",
            "objective": "derive the A split-gauge/vertical generator and prove Q_A=0 and K_boundary^A=0 for the compact local branch; if this fails, promote Q_A/K_boundary to the first finite A source row without claims",
            "required_inputs": "split transformation; parent Omega/theta piece; D C_A or A constraint; boundary variation; Q_A exact/proper/zero test; K_boundary cocycle; matter/readout no-spurion check; finite source-row schema",
            "excluded": "asserted gauge status; ordinary current conservation as zero proof; invented Q_A/kappa_A/lambda_A values; R10/local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2016_{idx}",
                "path": str(path),
                "exists": path.exists(),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    countermodels: list[dict[str, object]],
    priors: list[dict[str, object]],
    refusals: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "VAL2016_00_sources",
            all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources),
            "all cited source paths exist and needles are found",
        )
    )
    checks.append(
        (
            "VAL2016_01_closure_branch_written",
            any(row["theorem_id"] == "ANP2016_0_e_only_closure" and row["closure_proved"] is True for row in theorem),
            "conditional e-only/no-extra-mode closure theorem is retained",
        )
    )
    checks.append(
        (
            "VAL2016_02_no_pole_not_promoted",
            any(row["theorem_id"] == "ANP2016_8_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_A_NO_POLE_NOT_PARENT_SIGNED" for row in theorem)
            and all(row["parent_signed"] is False for row in theorem),
            "parent no-physical-A-pole claim is not falsely promoted",
        )
    )
    required_statuses = {
        "MISSING_A_SPECIFIC_QUOTIENT_MAP",
        "MISSING_PARENT_OMEGA_DCA_VERTICAL_GENERATOR",
        "MISSING_BOUNDARY_CHARGE_ZERO",
        "MISSING_NO_SPURION_MATTER_SIGNATURE",
        "MISSING_A_PROJECTION_SILENCE",
    }
    checks.append(
        (
            "VAL2016_03_required_missing_objects_explicit",
            required_statuses.issubset({str(row["status"]) for row in theorem}),
            "q_A/Omega-DCA/boundary/matter/projection gaps are explicit",
        )
    )
    checks.append(
        (
            "VAL2016_04_countermodels_block_shortcuts",
            len(countermodels) >= 5 and all(row["claim_blocks"] is True for row in countermodels),
            "countermodels block weak no-pole shortcuts",
        )
    )
    checks.append(
        (
            "VAL2016_05_prior_runner_nonclaim",
            all(row["score_ready"] is False and row["prior_min"] == "MISSING" and row["prior_max"] == "MISSING" for row in priors),
            "finite prior runner rows remain missing/nonclaim",
        )
    )
    checks.append(
        (
            "VAL2016_06_refusals_active",
            all(row["verdict"] == "REFUSE" and row["accepted_for_claim"] is False for row in refusals),
            "all claim/refusal rows remain active",
        )
    )
    checks.append(
        (
            "VAL2016_07_claim_gates_blocked",
            all(row["passed_for_claim"] is False for row in claim_gates),
            "all claim gates remain blocked",
        )
    )
    checks.append(
        (
            "VAL2016_08_csv_parse",
            all(path.exists() and csv_rows_parse(path) for path in output_paths),
            "all generated CSV outputs parse cleanly",
        )
    )
    checks.append(
        (
            "VAL2016_09_branch_copies",
            all(path.exists() and csv_rows_parse(path) for path in branch_paths),
            "branch-copy CSVs exist and parse",
        )
    )
    checks.append(
        (
            "VAL2016_10_no_formalization_edits",
            count_formalization_modified_since_start() == 0,
            "formalization-workbench modified-file count remains 0 for this run",
        )
    )
    checks.append(
        (
            "VAL2016_11_output_scope",
            all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in output_paths + branch_paths + [DOC]),
            "all outputs are under post-checkpoint-work",
        )
    )
    overall_pass = all(passed for _, passed, _ in checks)
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2016_OVERALL",
            "status": "PASS" if overall_pass else "FAIL",
            "detail": "2016 A-frame no-physical-pole gauge/constraint theorem or finite-prior runner",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    countermodels: list[dict[str, object]],
    priors: list[dict[str, object]],
    refusals: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    parts = [
        "# 2016 Y5 R2FR: A-Frame No-Physical-Pole Gauge Constraint Theorem Or Finite Prior Runner\n",
        "Private checkpoint. This attempts the clean local-GR route first: make `A` a redundant/gauge/constraint representative with no physical local pole. If that does not close, retain the finite-A prior runner without scoring claims.\n",
        "## Current Verdict\n",
        "The best route is real but still conditional: inside strict public-tetrad closure, where the parent action sees only `e=dX+A` and ordinary matter/readout sees only the public tetrad/connection, `A` has no independent Green pole. That is the clean GR-reduction move.\n",
        "The current parent corpus does **not** yet sign that closure. The missing pieces are now exact: the A-specific quotient map, action descent, `Omega/D C_A` first-class generator, boundary charge/cocycle silence, degree count, matter/readout no-spurion descent, and projection silence. Therefore `alpha_A=0`, local-GR pass, R10 pass, and finite-A scoring remain refused.\n",
        "This is not another vague coupling gap. The coupling problem has been split into a sharp theorem gate: either the split-gauge generator has zero local boundary charge, or that boundary/source charge becomes the first finite A source row.\n",
        "## Source Register\n",
        md_table(sources, ["source_id", "source_path", "status", "needles", "note"]),
        "## A-Frame No-Physical-Pole Theorem Audit\n",
        md_table(
            theorem,
            [
                "theorem_id",
                "clause",
                "formula",
                "status",
                "what_is_proved",
                "missing_before_claim",
                "closure_proved",
                "parent_signed",
            ],
        ),
        "## Countermodel Stress Tests\n",
        md_table(countermodels, ["countermodel_id", "countermodel", "why_it_matters", "blocked_by", "claim_blocks"]),
        "## Finite A Prior Runner Schema\n",
        md_table(
            priors,
            [
                "prior_id",
                "symbol",
                "meaning",
                "if_no_pole_signed",
                "if_no_pole_fails",
                "status",
                "prior_min",
                "prior_max",
                "units",
                "score_ready",
            ],
        ),
        "## Refusal Runner\n",
        md_table(refusals, ["refusal_id", "attempted_claim", "verdict", "reason", "accepted_for_claim"]),
        "## Claim Gates\n",
        md_table(claim_gates, ["gate_id", "gate", "passed_for_nonclaim", "passed_for_claim", "reason"]),
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
    theorem = no_pole_theorem_rows()
    countermodels = countermodel_rows()
    priors = finite_prior_runner_rows()
    refusals = refusal_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2016_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2016_AFRAME_NO_PHYSICAL_POLE_THEOREM_AUDIT.csv",
        "countermodels": OUT / "P8_Y5_PARENT_QLOC_2016_AFRAME_COUNTERMODEL_STRESS_TESTS.csv",
        "priors": OUT / "P8_Y5_PARENT_QLOC_2016_AFRAME_FINITE_PRIOR_RUNNER.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2016_AFRAME_REFUSAL_RUNNER.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2016_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2016_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2016_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["theorem"], theorem)
    write_csv(output_map["countermodels"], countermodels)
    write_csv(output_map["priors"], priors)
    write_csv(output_map["refusals"], refusals)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_NO_PHYSICAL_POLE_2016_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2016_AFRAME_NOPOLE_STATUS_NONCLAIM.csv",
        QUEUE / "JR2016_AFRAME_FINITE_PRIOR_RUNNER_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["theorem"], branch_paths[0])
    shutil.copyfile(output_map["claim_gates"], branch_paths[1])
    shutil.copyfile(output_map["priors"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame no-physical-pole theorem audit nonclaim copy",
            "A-frame no-pole/claim-gate status nonclaim copy",
            "A-frame finite prior runner queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2016_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, theorem, countermodels, priors, refusals, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2016_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, theorem, countermodels, priors, refusals, claim_gates, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2016_OVERALL"][0]["status"]
    print(f"VAL2016_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
