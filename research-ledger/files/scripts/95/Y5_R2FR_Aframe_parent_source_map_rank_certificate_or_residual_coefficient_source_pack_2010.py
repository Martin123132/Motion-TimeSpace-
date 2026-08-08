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
DOC = ROOT / "2010-Y5-R2FR-Aframe-parent-source-map-rank-certificate-or-residual-coefficient-source-pack.md"
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
            "SRC2010_00_2009_handoff",
            "2009-Y5-R2FR-Aframe-no-extra-mode-theorem-or-first-residual-response-kernel.md",
            ["NEXT2009_0_2010", "NEM2009_7_verdict", "VAL2009_OVERALL"],
            "2009 selected A-frame parent source-map/rank certificate or coefficient source pack.",
        ),
        (
            "SRC2010_01_2008_source_map_gap",
            "2008-Y5-R2FR-parent-nonholonomic-frame-deformation-action-or-tetrad-residual-runner.md",
            ["GRK2008_2_parent_map_rank", "AFF2008_7_verdict", "RUN2008_8_total_envelope"],
            "parent A-map/rank gap and residual runner schema.",
        ),
        (
            "SRC2010_02_787_rank_gate",
            "787-Y5-R10-multifield-pregeometry-rank-gate-or-independent-metric-branch-decision.md",
            ["MPR787_2_surjectivity_condition", "MPR787_5_rank_gate_verdict", "CIG787_2_moment_closure"],
            "rank/surjectivity and moment-closure route constraints.",
        ),
        (
            "SRC2010_03_788_nonholonomic",
            "788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md",
            ["PAC788_1_distortion_owned_contract", "MCG788_3_Bianchi_conservation", "NHC788_4_ownership_warning"],
            "distortion-owned contract and Bianchi warning.",
        ),
        (
            "SRC2010_04_789_matter",
            "789-Y5-R10-palatini-tetrad-GR-limit-with-MTS-exchange-contract.md",
            ["MIR789_4_matter_universality", "PTG789_1_action_form", "D789_1_no_local_GR_claim"],
            "matter universality and local-GR residual warning.",
        ),
        (
            "SRC2010_05_790_suppression",
            "790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md",
            ["LSG790_3_anisotropic_PPN_suppression", "LSG790_6_matter_frame_universality", "D790_1_Q_first"],
            "local residual suppression gates and Q-first decision.",
        ),
        (
            "SRC2010_06_791_q_loc",
            "791-Y5-R10-Ward-compatible-exchange-current-q-loc-zero-or-bound.md",
            ["ECT791_1_q_loc_geometric", "WZG791_3_geometric_q_loc_zero", "QBI791_3_R10"],
            "geometric q_loc and R10/PPN bound interface.",
        ),
        (
            "SRC2010_07_1965_R11",
            "1965-Y5-R2FR-R2-fR-zero-proof-or-executable-R11-bound-row.md",
            ["ZP1965_6_verdict", "EXR1965_1_mts_prediction", "EXR1965_4_decision_logic"],
            "R11/EH minimality coefficient gate.",
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
                "needed_for": "2010 A-frame parent source-map rank certificate or residual coefficient source pack",
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


def source_map_attempt_rows() -> list[dict[str, object]]:
    specs = [
        (
            "ASM2010_0_target",
            "A^a_mu = A^a_mu[Phi_MTS]",
            "Need a parent-owned nonholonomic deformation one-form whose image has full tetrad rank in the local GR domain.",
            "TARGET_EXACT",
            "requires source map, rank certificate, determinant/signature domain, and no-spurion matter silence",
            "false",
        ),
        (
            "ASM2010_1_scalar_or_single_flow",
            "A^a_mu = F^a_mu(psi,partial psi,...)",
            "A single scalar/flow variable cannot generically span tetrad or metric variations at a point.",
            "REJECTED_RANK_INSUFFICIENT",
            "rank collapses to a scalar-jet submanifold and tends back toward exact-gradient traps",
            "false",
        ),
        (
            "ASM2010_2_four_exact_labels",
            "A^a_mu = partial_mu X^a - delta^a_mu",
            "Four exact labels give an integrable coframe; this was already rejected for generic curvature/anholonomy.",
            "REJECTED_EXACT_GRADIENT",
            "cannot supply generic nonholonomic local GR geometry",
            "false",
        ),
        (
            "ASM2010_3_multifield_jet_map",
            "A^a_mu = F^a_mu(Phi^I,partial Phi^I,...), I>=4",
            "A sufficiently rich multifield jet could pass algebraic rank if its Jacobian covers sixteen tetrad components or ten metric components after quotient.",
            "CONDITIONAL_ALGEBRAIC_ROUTE",
            "the corpus does not identify the Phi^I, invariant F, or source equation that fixes them",
            "false",
        ),
        (
            "ASM2010_4_moment_closure",
            "A or g from coarse-grained motion moments M_mu_nu=<partial Phi partial Phi>",
            "Closest to the motion/time/space intuition and can escape scalar rank if M has independent covariant dynamics.",
            "PROMISING_BUT_UNSIGNED",
            "moment evolution, closure, signature rule, and EH dynamics are not derived",
            "false",
        ),
        (
            "ASM2010_5_constraint_owned_A",
            "S_constraint = integral lambda_a^mu(A^a_mu-F^a_mu[Phi_MTS])",
            "This would own A if F and lambda arise from the parent action and the constraint algebra is first-class/consistent.",
            "FORMAL_CONSTRAINT_ONLY",
            "currently an imposed closure, not a derived parent theorem",
            "false",
        ),
        (
            "ASM2010_6_response_current_map",
            "A^a_mu(x)=integral G_A(x,y) J^a_mu[MTS](y) dy",
            "A source-current/Green-function map is executable for tests and can carry nonholonomy.",
            "TESTABLE_RESIDUAL_ROUTE",
            "needs kernel, coupling coefficient, source profile, range, screening/regime map, and bounds",
            "false",
        ),
        (
            "ASM2010_7_verdict",
            "parent source map",
            "No inspected source derives a parent A^a_MTS source map with full rank and domain control.",
            "PARENT_SOURCE_MAP_NOT_DERIVED",
            "use coefficient/source pack while keeping derivation target explicit",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for map_id, candidate, test, status, missing_before_claim, parent_signed in specs:
        row = base_row()
        row.update(
            {
                "map_id": map_id,
                "candidate": candidate,
                "test": test,
                "status": status,
                "missing_before_claim": missing_before_claim,
                "parent_signed": parent_signed,
            }
        )
        rows.append(row)
    return rows


def rank_domain_rows() -> list[dict[str, object]]:
    specs = [
        (
            "RDC2010_0_raw_tetrad_rank",
            "rank(delta A^a_mu / delta Phi_parent_jet)",
            "rank >= 16 before quotient, or a proven equivalent covering all local tetrad variations modulo constraints",
            "MISSING_PARENT_JACOBIAN",
            "no source map exists to differentiate",
        ),
        (
            "RDC2010_1_metric_quotient_rank",
            "rank(delta g_mu_nu / delta Phi_parent_jet)",
            "rank >= 10 for symmetric metric variations, modulo diffeomorphism/gauge directions in the local domain",
            "MISSING_QUOTIENT_CERTIFICATE",
            "multifield rank is only conditional in current corpus",
        ),
        (
            "RDC2010_2_nonholonomy",
            "dA^a != 0 allowed",
            "source map must produce non-integrable coframes rather than exact scalar pullbacks only",
            "MISSING_NONHOLONOMIC_SOURCE_LAW",
            "no parent equation supplies de^a=dA^a with generic curvature support",
        ),
        (
            "RDC2010_3_determinant_lower_bound",
            "sigma_min(e)>0 or |det(e)|>=epsilon_det",
            "ensures the tetrad is invertible over the local GR patch",
            "MISSING_DOMAIN_BOUND",
            "no lower bound from parent action or solution family",
        ),
        (
            "RDC2010_4_signature_stability",
            "signature(g)=(-,+,+,+)",
            "Lorentzian signature must be preserved under allowed A variations",
            "MISSING_SIGNATURE_RULE",
            "internal Lorentzian structure or stability theorem remains unsigned",
        ),
        (
            "RDC2010_5_orientation_time_orientation",
            "det(e) sign and time leg orientation",
            "prevents branch flips across unphysical frames",
            "MISSING_ORIENTATION_CONDITION",
            "no parent selection rule recorded",
        ),
        (
            "RDC2010_6_rank_domain_verdict",
            "rank/domain certificate",
            "rank and domain requirements are now explicit, but none are parent-signed.",
            "CERTIFICATE_NOT_DERIVED",
            "move to coefficient/source pack or derive source map next",
        ),
    ]
    rows: list[dict[str, object]] = []
    for rank_id, object_text, requirement, status, blocker in specs:
        row = base_row()
        row.update(
            {
                "rank_id": rank_id,
                "object": object_text,
                "requirement": requirement,
                "status": status,
                "blocker": blocker,
                "parent_signed": "false",
            }
        )
        rows.append(row)
    return rows


def no_spurion_rows() -> list[dict[str, object]]:
    specs = [
        (
            "NSP2010_0_matter_functor",
            "S_matter[e,omega[e],Psi,owned gauge,theta]",
            "ordinary matter sees only the public tetrad/connection and owned gauge fields",
            "CONDITIONAL_REQUIRED",
            "parent-signed matter functor not found",
        ),
        (
            "NSP2010_1_no_X",
            "no direct X^a in matter/readout/source terms",
            "protects translation split gauge and prevents label forces",
            "UNSIGNED",
            "source/boundary/readout audit missing",
        ),
        (
            "NSP2010_2_no_A_representative",
            "no direct A^a_mu outside e=dX+A",
            "prevents matter from seeing the frame-deformation representative rather than the tetrad",
            "UNSIGNED",
            "kinetic/source A terms not excluded by parent theorem",
        ),
        (
            "NSP2010_3_no_Phi_species_marker",
            "no direct Phi_MTS/species/mass marker in ordinary matter",
            "equivalence principle and clock/WEP safety",
            "UNSIGNED",
            "no-spurion certificate missing",
        ),
        (
            "NSP2010_4_no_qloc_readout",
            "no direct q_loc/Gamma_eff/K_hat readout by matter",
            "keeps geometric q_loc as stress/geometry residual, not a direct matter force",
            "UNSIGNED",
            "q_loc carrier still lacks zero/bound proof",
        ),
        (
            "NSP2010_5_boundary_source_measure",
            "boundary/source-measure terms respect the same public frame",
            "prevents hidden source renormalization or frame leakage",
            "UNSIGNED",
            "boundary variation and source-measure coefficient missing",
        ),
        (
            "NSP2010_6_verdict",
            "no-spurion silence",
            "requirements are explicit but not parent-signed; matter Ward zero remains conditional.",
            "NO_SPURION_NOT_DERIVED",
            "must be proven or bounded through WEP/clock/PPN/source rows",
        ),
    ]
    rows: list[dict[str, object]] = []
    for silence_id, clause, purpose, status, missing_before_claim in specs:
        row = base_row()
        row.update(
            {
                "silence_id": silence_id,
                "clause": clause,
                "purpose": purpose,
                "status": status,
                "missing_before_claim": missing_before_claim,
                "parent_signed": "false",
            }
        )
        rows.append(row)
    return rows


def coefficient_source_pack_rows() -> list[dict[str, object]]:
    specs = [
        (
            "COEF2010_0_A_profile_amplitude",
            "C_A",
            "overall amplitude/coupling for deltaA profile",
            "KER2009_0_metric_response;KER2009_1_Newton_acceleration",
            "MISSING_PARENT_COEFFICIENT",
            "MISSING",
            "source path for parent S_A or A source map",
        ),
        (
            "COEF2010_1_A_range",
            "lambda_A",
            "range or correlation length for A-frame residual",
            "KER2009_5_R10_yukawa_projection;KER2009_4_light_or_orbital_integral",
            "MISSING_RANGE_OR_SCREENING_MAP",
            "m",
            "parent mass/range or empirical profile source",
        ),
        (
            "COEF2010_2_A_radial_shape",
            "f_A(r)",
            "radial/profile shape of h_A_00 or deltaA near compact/local source",
            "KER2009_1_Newton_acceleration;KER2009_3_clock_shift",
            "MISSING_PROFILE",
            "dimensionless or normalized profile",
            "source solution or ansatz label",
        ),
        (
            "COEF2010_3_PPN_response",
            "J_PPN[A]",
            "Jacobian mapping A-profile coefficients to gamma,beta,alpha_i shifts",
            "KER2009_2_PPN_gamma_beta",
            "MISSING_PPN_PROJECTION",
            "dimensionless response matrix",
            "local weak-field expansion source",
        ),
        (
            "COEF2010_4_clock_response",
            "J_clock[A]",
            "clock/redshift response to h_A_00 between sites",
            "KER2009_3_clock_shift",
            "MISSING_CLOCK_PROJECTION",
            "dimensionless",
            "clock observable model and site/source profile",
        ),
        (
            "COEF2010_5_R10_alpha",
            "alpha_A(lambda_A)",
            "short-range Yukawa-equivalent amplitude for A residual",
            "KER2009_5_R10_yukawa_projection",
            "MISSING_ALPHA_AND_FULL_BOUND_CURVE",
            "dimensionless",
            "parent C_A, lambda_A, full R10 alpha(lambda) curve",
        ),
        (
            "COEF2010_6_q_loc_response",
            "G_Q or T_Q carrier coefficients",
            "Green function/stress carrier converting q_loc into metric residual",
            "KER2009_6_q_loc_carrier",
            "MISSING_QLOC_EQUATIONS_AND_BOUNDARY_CONDITIONS",
            "stress/metric response units",
            "Gamma_eff/K_hat equations and local Green function",
        ),
        (
            "COEF2010_7_R11_scalar",
            "c_R2_or_fRR",
            "higher-curvature/scalaron residual coefficient if A/Xi integration generates R11 terms",
            "KER2009_7_total_response_vector",
            "MISSING_R11_PARENT_COEFFICIENT",
            "model-dependent",
            "EH minimality or scalar residual source",
        ),
        (
            "COEF2010_8_bound_vector",
            "B_local",
            "arena bounds for acceleration, PPN, clock, orbital, R10",
            "all KER2009 rows",
            "MISSING_CONSOLIDATED_BOUND_SOURCES",
            "mixed",
            "PPN limits, clock bounds, orbital residuals, R10 full curve",
        ),
    ]
    rows: list[dict[str, object]] = []
    for coeff_id, symbol, meaning, feeds_kernel, status, units, required_source in specs:
        row = base_row()
        row.update(
            {
                "coeff_id": coeff_id,
                "symbol": symbol,
                "meaning": meaning,
                "feeds_kernel": feeds_kernel,
                "status": status,
                "numeric_value": "MISSING",
                "units": units,
                "required_source": required_source,
                "source_path": "MISSING_PARENT_OR_BOUND_SOURCE",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("CG2010_0_source_map_attempt", "parent A source-map attempted", "PASS_NONCLAIM", "all candidate routes audited"),
        ("CG2010_1_parent_source_map", "A^a_MTS=A^a[Phi_MTS] derived", "FAIL_BLOCKED", "no parent source map, invariant F, or source equation found"),
        ("CG2010_2_rank_certificate", "full tetrad/metric quotient rank certified", "FAIL_BLOCKED", "no parent Jacobian exists to certify"),
        ("CG2010_3_domain_certificate", "determinant/signature/orientation protected", "FAIL_BLOCKED", "no determinant lower bound or signature theorem"),
        ("CG2010_4_no_spurion", "matter/boundary sees only public tetrad", "FAIL_BLOCKED", "no parent-signed no-spurion matter/source audit"),
        ("CG2010_5_coefficient_pack", "residual coefficient source pack staged", "PASS_NONCLAIM", "required coefficient rows are explicit but empty"),
        ("CG2010_6_local_GR_Newton", "local GR/Newton derived", "FAIL_BLOCKED", "source map, q_loc, R11, matter silence, and residual coefficients remain open"),
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
            "DEC2010_0_result",
            "PARENT_A_SOURCE_MAP_NOT_DERIVED",
            "The exact ownership target is now written, but the corpus does not yet supply A^a_MTS=A^a[Phi_MTS] with full rank, determinant/signature stability, and no-spurion matter silence.",
            "do not claim derived tetrad; either derive a moment/source-current law or populate coefficient rows",
        ),
        (
            "DEC2010_1_best_derivation_route",
            "MOMENT_OR_SOURCE_CURRENT_ROUTE_IS_BEST_NEXT_SHOT",
            "Scalar/exact-label routes are dead; the least-circular derivation route is a covariant MTS moment/current that sources A with a constraint/rank theorem.",
            "try to derive J_MTS -> A source equation before doing broad empirical scoring",
        ),
        (
            "DEC2010_2_testing_route",
            "COEFFICIENT_SOURCE_PACK_READY_BUT_EMPTY",
            "The local residual kernel now has named coefficient slots for A amplitude, range, PPN, clock, R10, q_loc, and R11.",
            "first executable test needs real values or theorem-zero for these rows",
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
            "target_id": "NEXT2010_0_2011",
            "selected": "true",
            "next_doc": "2011-Y5-R2FR-covariant-MTS-current-source-law-for-Aframe-or-first-coefficient-dry-run.md",
            "next_script": "scripts/Y5_R2FR_covariant_MTS_current_source_law_for_Aframe_or_first_coefficient_dry_run_2011.py",
            "objective": "try to derive a covariant MTS moment/current source law J_MTS -> A^a_MTS with no-spurion and rank/domain control; if it fails, instantiate the first coefficient dry-run for C_A, lambda_A, and alpha_A(lambda)",
            "include": "J_MTS definition; A Green function/source equation; split-gauge covariance; Bianchi compatibility; C_A/lambda_A/alpha_A placeholders; R10/PPN/clock routing",
            "exclude": "scalar exact-gradient retry; unlabelled tetrad insertion; local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2010_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    source_map: list[dict[str, object]],
    rank_domain: list[dict[str, object]],
    no_spurion: list[dict[str, object]],
    coeff_pack: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks = [
        ("VAL2010_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"),
        ("VAL2010_01_source_map_failed_cleanly", any(row["status"] == "PARENT_SOURCE_MAP_NOT_DERIVED" for row in source_map), "parent A source-map not falsely promoted"),
        ("VAL2010_02_rank_domain_explicit", any(row["rank_id"] == "RDC2010_0_raw_tetrad_rank" for row in rank_domain) and all(row["parent_signed"] == "false" for row in rank_domain), "rank/domain certificate requirements explicit and unsigned"),
        ("VAL2010_03_no_spurion_unsigned", any(row["status"] == "NO_SPURION_NOT_DERIVED" for row in no_spurion) and all(row["parent_signed"] == "false" for row in no_spurion), "no-spurion silence remains conditional/nonclaim"),
        ("VAL2010_04_coeff_pack_empty_nonclaim", all(row["numeric_value"] == "MISSING" and row["valid_for_claim"] == "false" for row in coeff_pack), "coefficient source pack remains empty/nonclaim"),
        ("VAL2010_05_coeff_pack_covers_kernel", {"COEF2010_0_A_profile_amplitude", "COEF2010_1_A_range", "COEF2010_3_PPN_response", "COEF2010_5_R10_alpha", "COEF2010_6_q_loc_response"}.issubset({row["coeff_id"] for row in coeff_pack}), "coefficient pack covers A amplitude/range/PPN/R10/q_loc"),
        ("VAL2010_06_claim_gates_blocked", all(row["passed_for_claim"] == "false" for row in claim_gates), "all claim gates remain blocked"),
        ("VAL2010_07_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2010_08_branch_copies", all(path.exists() for path in branch_paths), "branch-copy CSVs exist"),
        ("VAL2010_09_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"),
        ("VAL2010_10_output_scope", all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]), "all outputs are under post-checkpoint-work"),
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
            "check_id": "VAL2010_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2010 A-frame parent source-map rank certificate or residual coefficient source pack",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    source_map: list[dict[str, object]],
    rank_domain: list[dict[str, object]],
    no_spurion: list[dict[str, object]],
    coeff_pack: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2010 Y5 R2FR: A-Frame Parent Source-Map Rank Certificate Or Residual Coefficient Source Pack

Private checkpoint. This tries to make the nonholonomic A-frame actually owned by MTS rather than merely protected as a tetrad closure.

## Current Verdict

The parent source map is **not derived yet**. The exact target is now sharp: derive `A^a_MTS=A^a[Phi_MTS]` with enough rank to cover local tetrad/metric variations, preserve `det(e)!=0` and Lorentzian signature, respect the `X/A` split gauge, and keep ordinary matter blind to `X`, `A`, `Phi_MTS`, `q_loc`, and source markers except through the public tetrad.

The scalar and exact-label routes are rejected. A multifield jet, moment-closure, or covariant source-current route could still work, but the inspected corpus does not yet provide the parent invariant, source equation, rank certificate, or domain theorem.

That means the honest path is now two-pronged: keep trying the least-circular derivation route, namely a covariant MTS current/moment source law for `A^a_MTS`; and in parallel keep the coefficient/source pack ready so the first local residual can be tested as soon as a coefficient or theorem-zero exists.

No local-GR/Newton/WEP/R10 claim is promoted.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## Parent Source-Map Attempt
{md_table(source_map, ["map_id", "candidate", "status", "missing_before_claim", "parent_signed"])}

## Rank And Domain Certificate
{md_table(rank_domain, ["rank_id", "object", "requirement", "status", "blocker"])}

## No-Spurion Silence Audit
{md_table(no_spurion, ["silence_id", "clause", "purpose", "status", "missing_before_claim"])}

## Residual Coefficient Source Pack
{md_table(coeff_pack, ["coeff_id", "symbol", "meaning", "feeds_kernel", "status", "numeric_value", "units", "required_source"])}

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
    source_map = source_map_attempt_rows()
    rank_domain = rank_domain_rows()
    no_spurion = no_spurion_rows()
    coeff_pack = coefficient_source_pack_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2010_SOURCE_REGISTER.csv",
        "source_map": OUT / "P8_Y5_PARENT_QLOC_2010_AFRAME_SOURCE_MAP_ATTEMPT.csv",
        "rank_domain": OUT / "P8_Y5_PARENT_QLOC_2010_RANK_DOMAIN_CERTIFICATE.csv",
        "no_spurion": OUT / "P8_Y5_PARENT_QLOC_2010_NO_SPURION_SILENCE_AUDIT.csv",
        "coeff_pack": OUT / "P8_Y5_PARENT_QLOC_2010_RESIDUAL_COEFFICIENT_SOURCE_PACK.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2010_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2010_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2010_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["source_map"], source_map)
    write_csv(output_map["rank_domain"], rank_domain)
    write_csv(output_map["no_spurion"], no_spurion)
    write_csv(output_map["coeff_pack"], coeff_pack)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_SOURCE_MAP_RANK_2010_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2010_RANK_DOMAIN_STATUS_NONCLAIM.csv",
        QUEUE / "JR2010_AFRAME_RESIDUAL_COEFFICIENT_SOURCE_PACK_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["source_map"], branch_paths[0])
    shutil.copyfile(output_map["rank_domain"], branch_paths[1])
    shutil.copyfile(output_map["coeff_pack"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame source-map/rank attempt nonclaim copy",
            "A-frame rank/domain status nonclaim copy",
            "A-frame residual coefficient source-pack queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2010_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, source_map, rank_domain, no_spurion, coeff_pack, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2010_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, source_map, rank_domain, no_spurion, coeff_pack, claim_gates, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2010_OVERALL"][0]["status"]
    print(f"VAL2010_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
