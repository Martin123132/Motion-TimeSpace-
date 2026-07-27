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
DOC = ROOT / "2009-Y5-R2FR-Aframe-no-extra-mode-theorem-or-first-residual-response-kernel.md"
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
            "SRC2009_00_2008_handoff",
            "2008-Y5-R2FR-parent-nonholonomic-frame-deformation-action-or-tetrad-residual-runner.md",
            ["NEXT2008_0_2009", "AFF2008_7_verdict", "VAL2008_OVERALL"],
            "2008 selected no-extra-mode theorem or first residual response kernel.",
        ),
        (
            "SRC2009_01_787_rank",
            "787-Y5-R10-multifield-pregeometry-rank-gate-or-independent-metric-branch-decision.md",
            ["MPR787_2_surjectivity_condition", "MPR787_3_internal_signature", "CIG787_1_nonholonomic_coframe"],
            "rank/surjectivity, internal signature, and nonholonomic route constraints.",
        ),
        (
            "SRC2009_02_788_nonholonomic",
            "788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md",
            ["NHC788_1_nonholonomic_ansatz", "PAC788_0_palatini_tetrad_contract", "PAC788_1_distortion_owned_contract"],
            "Palatini/tetrad route and distortion-owned coframe contract.",
        ),
        (
            "SRC2009_03_789_local_GR_bridge",
            "789-Y5-R10-palatini-tetrad-GR-limit-with-MTS-exchange-contract.md",
            ["PTG789_1_action_form", "MIR789_4_matter_universality", "D789_1_no_local_GR_claim"],
            "local GR bridge, matter universality, and residual warning.",
        ),
        (
            "SRC2009_04_790_residual_decomp",
            "790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md",
            ["LSG790_0_Ward_compatible_split", "LSG790_3_anisotropic_PPN_suppression", "LSG790_6_matter_frame_universality"],
            "residual decomposition and PPN/matter-frame suppression gates.",
        ),
        (
            "SRC2009_05_791_q_loc",
            "791-Y5-R10-Ward-compatible-exchange-current-q-loc-zero-or-bound.md",
            ["ECT791_1_q_loc_geometric", "WZG791_3_geometric_q_loc_zero", "QBI791_2_PPN"],
            "geometric q_loc remains separate from ordinary matter Ward zero.",
        ),
        (
            "SRC2009_06_1965_R11",
            "1965-Y5-R2FR-R2-fR-zero-proof-or-executable-R11-bound-row.md",
            ["ZP1965_3_minimality_route", "ZP1965_6_verdict", "EXR1965_1_mts_prediction"],
            "EH/R11 minimality and scalar residual warning.",
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
                "needed_for": "2009 A-frame no-extra-mode theorem or first residual response kernel",
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


def no_extra_mode_theorem_rows() -> list[dict[str, object]]:
    specs = [
        (
            "NEM2009_0_theorem_statement",
            "If e^a=dX^a+A^a_MTS and the full local action depends on X^a and A^a_MTS only through e^a, then the X/A split adds no physical local mode beyond the tetrad.",
            "split gauge X^a->X^a+xi^a, A^a->A^a-dxi^a; no separate X or A in matter, boundary, S_MTS, or sources",
            "CONDITIONAL_THEOREM_AVAILABLE",
            "This proves no extra split mode only under closure assumptions; it does not derive e or A from MTS parent variables.",
            "false",
        ),
        (
            "NEM2009_1_variation_chain_rule",
            "delta S/delta A^a_mu = delta S/delta e^a_mu and delta S/delta X^a = -partial_mu(delta S/delta e^a_mu) up to covariant/boundary terms.",
            "S=S[e,omega,Phi,Psi] with e=dX+A; boundary terms also e-only",
            "PROVED_CONDITIONAL",
            "The X equation is a Noether consequence of the e/A equation, not a new parent source law.",
            "false",
        ),
        (
            "NEM2009_2_pure_closure_branch",
            "A^a_MTS is harmless if it is only a parametrization of the tetrad.",
            "no F_A^2, no torsion-square A kinetic term, no source-measure A dependence, no matter representative dependence",
            "NO_EXTRA_MODE_AS_TETRAD_REWRITE",
            "This is safe but it is tetrad closure, not a motion/time/space derivation.",
            "false",
        ),
        (
            "NEM2009_3_kinetic_A_branch",
            "An independent kinetic or torsion-like A sector generally creates extra local response unless constrained or topological.",
            "S_A contains dA, T[A,omega], F_A, mass, nonlocal memory kernel, or non-EH counterterms",
            "NO_EXTRA_MODE_NOT_PROVED",
            "Need first-class constraint algebra, mass gap/screening, topological redundancy, or measured residual bounds.",
            "false",
        ),
        (
            "NEM2009_4_constraint_owned_branch",
            "A^a_MTS could be parent-owned if a variational constraint forces A^a=A^a[Phi_MTS] with full rank and no extra solutions.",
            "parent Lagrange/constraint sector, rank(delta A/delta Phi), determinant domain, stable signature, closed constraint algebra",
            "PROMISING_BUT_UNSIGNED",
            "No inspected source supplies the parent constraint or rank certificate.",
            "false",
        ),
        (
            "NEM2009_5_matter_no_spurion_clause",
            "Ordinary matter must see e and omega[e] only, not X, A, Phi_MTS, q_loc, species labels, or source markers directly.",
            "universal matter functor plus no-spurion audit",
            "REQUIRED_FOR_WARD_ZERO",
            "This condition is exactly what makes Q_matter vanish conditionally, but it is not parent-signed.",
            "false",
        ),
        (
            "NEM2009_6_boundary_silence_clause",
            "Boundary/source-measure terms must also respect the split gauge and matter-frame universality.",
            "S_boundary/source depends on e or invariant total stress only",
            "MISSING_BOUNDARY_PROOF",
            "Separate X/A dependence reintroduces frame leakage and source renormalization.",
            "false",
        ),
        (
            "NEM2009_7_verdict",
            "The no-extra-mode theorem is real only as a conditional field-redefinition/closure theorem.",
            "all e-only and no-spurion clauses signed",
            "CLOSURE_ONLY_NOT_PARENT_DERIVATION",
            "Next leap is parent source-map/rank certificate; otherwise use residual response kernel.",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for theorem_id, claim, assumptions, status, blocker, parent_signed in specs:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "claim": claim,
                "assumptions": assumptions,
                "status": status,
                "blocker": blocker,
                "parent_signed": parent_signed,
            }
        )
        rows.append(row)
    return rows


def mode_count_rows() -> list[dict[str, object]]:
    specs = [
        (
            "MCT2009_0_XA_split",
            "X^a plus A^a_mu",
            "20 raw components with four split-gauge functions; physical combination is e^a_mu",
            "NO_EXTRA_SPLIT_DOF_IF_E_ONLY",
            "does not reduce or derive the tetrad itself",
        ),
        (
            "MCT2009_1_tetrad_GR",
            "e^a_mu, omega^ab_mu Palatini/EH",
            "standard local Lorentz, diffeomorphism, and Hamiltonian constraints reduce to GR propagating content under EH action",
            "CONDITIONAL_GR_MODE_CONTENT",
            "requires EH/minimality and torsionless connection equation",
        ),
        (
            "MCT2009_2_independent_A_kinetic",
            "A^a_mu with F_A/dA/torsion kinetic terms",
            "adds local vector/torsion-like response unless constraints remove it",
            "EXTRA_MODE_RISK",
            "must be theorem-zero, massive/screened, or empirically bounded",
        ),
        (
            "MCT2009_3_parent_constraint",
            "A^a=A^a[Phi_MTS]",
            "could make A owned by MTS rather than independent if rank and constraints close",
            "OWNERSHIP_ROUTE_OPEN",
            "no parent source map or rank certificate yet",
        ),
        (
            "MCT2009_4_R11_backreaction",
            "integrated-out A/Xi sector",
            "can regenerate R^2/f(R)/nonlocal operators even after tetrad exists",
            "EH_MINIMALITY_STILL_OPEN",
            "R11/scalar residual branch remains live",
        ),
    ]
    rows: list[dict[str, object]] = []
    for mode_id, object_text, count_logic, status, blocker in specs:
        row = base_row()
        row.update(
            {
                "mode_id": mode_id,
                "object": object_text,
                "count_logic": count_logic,
                "status": status,
                "blocker": blocker,
                "parent_signed": "false",
            }
        )
        rows.append(row)
    return rows


def first_residual_kernel_rows() -> list[dict[str, object]]:
    specs = [
        (
            "KER2009_0_metric_response",
            "h_A_mu_nu",
            "h_A_mu_nu = eta_ab(bar_e^a_mu deltaA^b_nu + bar_e^a_nu deltaA^b_mu)",
            "maps A-frame displacement into metric perturbation around a local GR background",
            "background tetrad bar_e; deltaA profile; gauge choice; units for A",
            "dimensionless h",
        ),
        (
            "KER2009_1_Newton_acceleration",
            "a_A^i",
            "stationary weak-field: a_A^i = (c^2/2) partial^i h_A_00",
            "extra acceleration vector for orbital/lab tests",
            "spatial h_A_00 profile and source normalization",
            "m s^-2",
        ),
        (
            "KER2009_2_PPN_gamma_beta",
            "delta_PPN_A",
            "decompose h_A_00,h_A_rr,h_A_0i into gamma,beta,alpha_i shifts relative to GR weak-field form",
            "PPN residual vector",
            "spherical/source solution or response Jacobian J_PPN[A]",
            "dimensionless",
        ),
        (
            "KER2009_3_clock_shift",
            "delta_nu_over_nu_A",
            "leading static clock residual between sites: Delta(delta nu/nu)_A = 0.5 Delta h_A_00",
            "clock/redshift test residual",
            "site-dependent h_A_00; environmental/source profile",
            "dimensionless",
        ),
        (
            "KER2009_4_light_or_orbital_integral",
            "Delta_obs_A",
            "integrate metric residual along ray/orbit using standard weak-field perturbation kernels",
            "light bending, Shapiro, perihelion, ephemeris, lunar/binary timing",
            "h_A_mu_nu along trajectory and benchmark covariance/bounds",
            "observable-specific",
        ),
        (
            "KER2009_5_R10_yukawa_projection",
            "alpha_A(lambda_A)",
            "if h_A_00(r) can be written as -2 Phi_A/c^2 with Phi_A=-Gm alpha_A exp(-r/lambda_A)/r, compare abs(alpha_A) to bound(lambda_A)",
            "short-range fifth-force/R10 comparator",
            "lambda_A; alpha_A from parent coefficients; full bound curve",
            "dimensionless alpha, metre lambda",
        ),
        (
            "KER2009_6_q_loc_carrier",
            "h_Q_mu_nu",
            "if q_loc is nonzero, solve nabla_mu T_Q^mu_nu=-q_loc_nu and apply linearized Einstein response to T_Q",
            "geometric exchange-current residual",
            "Gamma_eff, K_hat, boundary conditions, Green function or response matrix",
            "metric/stress units",
        ),
        (
            "KER2009_7_total_response_vector",
            "R_A",
            "R_A = (a_A, delta_gamma_A, delta_beta_A, delta_alpha_i_A, delta_clock_A, alpha_A(lambda), h_Q, Xi_R11)",
            "first executable local response vector once parent coefficients exist",
            "all component coefficients, units, source paths, arena bounds",
            "mixed vector",
        ),
    ]
    rows: list[dict[str, object]] = []
    for kernel_id, symbol, formula, observable_channel, required_inputs, units in specs:
        row = base_row()
        row.update(
            {
                "kernel_id": kernel_id,
                "symbol": symbol,
                "formula": formula,
                "observable_channel": observable_channel,
                "required_inputs": required_inputs,
                "units": units,
                "numeric_status": "MISSING_PARENT_COEFFICIENTS_OR_PROFILES",
                "status": "SYMBOLIC_KERNEL_READY_NONCLAIM",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("CG2009_0_conditional_no_extra_mode", "field-redefinition no-extra-mode theorem", "PASS_CONDITIONAL_NONCLAIM", "valid only if every e-only/no-spurion/boundary clause is signed"),
        ("CG2009_1_parent_ownership", "A^a_MTS derived from parent variables", "FAIL_BLOCKED", "source map A[Phi_MTS], rank certificate, and constraint origin missing"),
        ("CG2009_2_independent_A_modes", "kinetic/constraint A sector adds no extra modes", "FAIL_BLOCKED", "no topological/no-mode/mass-gap/screening proof"),
        ("CG2009_3_matter_Ward", "matter exchange current zero", "FAIL_BLOCKED", "conditional theorem exists, but matter universality is not parent-signed"),
        ("CG2009_4_q_loc", "geometric q_loc zero or bounded", "FAIL_BLOCKED", "q_loc remains separate from ordinary matter Ward zero"),
        ("CG2009_5_first_kernel", "first local residual response kernel", "PASS_NONCLAIM", "symbolic kernel exists, but parent coefficients/profiles and bounds are missing"),
        ("CG2009_6_local_GR_Newton", "local GR/Newton derived", "FAIL_BLOCKED", "closure theorem alone does not derive parent tetrad ownership or residual silence"),
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
            "DEC2009_0_result",
            "NO_EXTRA_MODE_THEOREM_PROVED_ONLY_AS_CLOSURE",
            "If the action sees only e=dX+A, then X/A is a redundant parametrization and adds no local modes. That is useful, but it is not a derivation of e or A from MTS.",
            "next target must derive the parent source map/rank certificate or populate residual coefficients",
        ),
        (
            "DEC2009_1_leap_status",
            "WE_DID_TAKE_THE_LEAP_AND_IT_LANDED_ON_A_SHARP_FORK",
            "The fork is clean: pure e-only branch equals safe tetrad closure; independent A branch needs no-extra-mode or measurable residuals.",
            "stop retrying exact-gradient/coframe wording; work the source-map or residual-coefficient fork",
        ),
        (
            "DEC2009_2_testing_path",
            "FIRST_LOCAL_RESPONSE_KERNEL_IS_NOW_WRITTEN",
            "The kernel maps deltaA into h_A, acceleration, PPN, clocks, R10, orbital, and q_loc carrier channels, but all coefficients remain missing.",
            "use it once parent A profile/coefficient rows exist",
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
            "target_id": "NEXT2009_0_2010",
            "selected": "true",
            "next_doc": "2010-Y5-R2FR-Aframe-parent-source-map-rank-certificate-or-residual-coefficient-source-pack.md",
            "next_script": "scripts/Y5_R2FR_Aframe_parent_source_map_rank_certificate_or_residual_coefficient_source_pack_2010.py",
            "objective": "try to derive A^a_MTS=A^a[Phi_MTS] with full tetrad rank, determinant/signature domain, and no-spurion matter silence; if not, create coefficient/source rows for the 2009 residual kernel",
            "include": "parent source map; rank(delta A/delta Phi_MTS); determinant lower bound; local Lorentz/split-gauge quotient; A-profile coefficients; PPN/R10/clock/orbital source pack",
            "exclude": "another exact-gradient route; unlabelled tetrad insertion; local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2009_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    mode_rows: list[dict[str, object]],
    kernel_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks = [
        ("VAL2009_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"),
        ("VAL2009_01_conditional_theorem_written", any(row["status"] == "CONDITIONAL_THEOREM_AVAILABLE" for row in theorem_rows), "no-extra-mode theorem written as conditional theorem"),
        ("VAL2009_02_closure_not_parent_claim", any(row["status"] == "CLOSURE_ONLY_NOT_PARENT_DERIVATION" for row in theorem_rows) and all(row["parent_signed"] == "false" for row in theorem_rows), "closure theorem not promoted as parent derivation"),
        ("VAL2009_03_extra_mode_risk_retained", any(row["status"] == "EXTRA_MODE_RISK" for row in mode_rows), "independent A kinetic branch remains blocked"),
        ("VAL2009_04_kernel_symbolic_ready", all(row["status"] == "SYMBOLIC_KERNEL_READY_NONCLAIM" and row["valid_for_claim"] == "false" for row in kernel_rows), "first residual kernel rows are symbolic nonclaim rows"),
        ("VAL2009_05_kernel_has_local_arenas", {"KER2009_1_Newton_acceleration", "KER2009_2_PPN_gamma_beta", "KER2009_3_clock_shift", "KER2009_5_R10_yukawa_projection", "KER2009_6_q_loc_carrier"}.issubset({row["kernel_id"] for row in kernel_rows}), "kernel covers Newton/PPN/clocks/R10/q_loc arenas"),
        ("VAL2009_06_claim_gates_blocked", all(row["passed_for_claim"] == "false" for row in claim_gates), "all claim gates remain blocked"),
        ("VAL2009_07_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2009_08_branch_copies", all(path.exists() for path in branch_paths), "branch-copy CSVs exist"),
        ("VAL2009_09_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"),
        ("VAL2009_10_output_scope", all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]), "all outputs are under post-checkpoint-work"),
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
            "check_id": "VAL2009_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2009 A-frame no-extra-mode theorem or first residual response kernel",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    mode_rows: list[dict[str, object]],
    kernel_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2009 Y5 R2FR: A-Frame No-Extra-Mode Theorem Or First Residual Response Kernel

Private checkpoint. This takes the 2008 fork seriously: either prove `A^a_MTS` is harmless in the local GR branch, or stop pretending and write the first local response kernel it must pass.

## Current Verdict

The no-extra-mode theorem **does exist**, but only as a conditional closure theorem. If the action depends on `X^a` and `A^a_MTS` only through the completed tetrad `e^a=dX^a+A^a_MTS`, then the `X/A` split is a redundant parametrization. The variation with respect to `A` is just the tetrad variation, and the variation with respect to `X` is the corresponding Noether identity. That adds no extra local mode beyond the tetrad branch.

That is useful, but it is not the full MTS derivation. It proves safety only if we accept the tetrad closure. It does not prove that `A^a_MTS` is generated by motion/time/space parent variables. If `A^a_MTS` has its own kinetic, constraint, source-measure, or boundary terms, the no-extra-mode result no longer follows and the branch must be bounded.

So the project has moved forward: the local-GR route is now a sharp fork, not a fog. Either derive `A^a_MTS=A^a[Phi_MTS]` with a full rank/domain/no-spurion certificate, or use the response kernel below to test the residuals.

No local-GR/Newton/WEP/R10 claim is promoted.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## No-Extra-Mode Theorem Gate
{md_table(theorem_rows, ["theorem_id", "claim", "status", "blocker", "parent_signed"])}

## Mode Count Ledger
{md_table(mode_rows, ["mode_id", "object", "count_logic", "status", "blocker"])}

## First Residual Response Kernel
{md_table(kernel_rows, ["kernel_id", "symbol", "formula", "observable_channel", "required_inputs", "units", "status"])}

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
    theorem_rows = no_extra_mode_theorem_rows()
    mode_rows = mode_count_rows()
    kernel_rows = first_residual_kernel_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2009_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2009_NO_EXTRA_MODE_THEOREM.csv",
        "mode_count": OUT / "P8_Y5_PARENT_QLOC_2009_MODE_COUNT_LEDGER.csv",
        "kernel": OUT / "P8_Y5_PARENT_QLOC_2009_FIRST_RESIDUAL_RESPONSE_KERNEL.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2009_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2009_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2009_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["theorem"], theorem_rows)
    write_csv(output_map["mode_count"], mode_rows)
    write_csv(output_map["kernel"], kernel_rows)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_NO_EXTRA_MODE_2009_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2009_NO_EXTRA_MODE_STATUS_NONCLAIM.csv",
        QUEUE / "JR2009_AFRAME_FIRST_RESIDUAL_KERNEL_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["theorem"], branch_paths[0])
    shutil.copyfile(output_map["mode_count"], branch_paths[1])
    shutil.copyfile(output_map["kernel"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame no-extra-mode theorem nonclaim copy",
            "A-frame mode-count status nonclaim copy",
            "first A-frame residual kernel queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2009_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, theorem_rows, mode_rows, kernel_rows, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2009_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, theorem_rows, mode_rows, kernel_rows, claim_gates, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2009_OVERALL"][0]["status"]
    print(f"VAL2009_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
