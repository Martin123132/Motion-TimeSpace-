from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PSI_DETERMINANT_QUOTIENT_MAP_OR_FINITE_QR_COEFFICIENTS_2421"
CHECKPOINT_ID = "2421"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2421-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2421_SOURCE_REGISTER.csv",
    "frontier_synthesis": OUT / "P8_Y5_PARENT_QLOC_2421_FRONTIER_SYNTHESIS_LEDGER.csv",
    "proof_status": OUT / "P8_Y5_PARENT_QLOC_2421_PROOF_STATUS_MATRIX.csv",
    "finite_branch": OUT / "P8_Y5_PARENT_QLOC_2421_FINITE_QR_BRANCH_HANDOFF.csv",
    "route_priority": OUT / "P8_Y5_PARENT_QLOC_2421_DERIVATION_ROUTE_PRIORITY.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2421_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2421_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2421_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2421_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2421_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2421_PSI_QUOTIENT_FRONTIER_SYNTHESIS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2421_LOCAL_GR_REFUSAL_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_PSI_QUOTIENT_FRONTIER_DECISION_2421_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2421_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2421-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2421*",
        "*P8_Y5_BRR545_2421*",
        "*Y5_R2FR_psi_determinant_quotient_map_or_finite_qR_coefficients_2421*",
        "*JR2421*",
        "*PARENT_QLOC_PSI_QUOTIENT_FRONTIER_DECISION_2421*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("2420_coupling_gate", ROOT / "2420-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md", ["QNP2420_4_psi_quotient", "NEXT2420_0_selected", "VAL2420_OVERALL"], "current handoff: psi determinant/quotient selected after coupling gate."),
        ("2270_psi_to_phiq", ROOT / "2270-Y5-R2FR-psi-to-Phiq-quotient-map-or-qR-stiffness-source.md", ["PCM2270_1_component_projection", "PQT2270_4_verdict", "VAL2270_OVERALL"], "q identified as temporal/radial covariance mismatch."),
        ("2271_pullback", ROOT / "2271-Y5-R2FR-parent-psi-action-Phiq-pullback-contract-or-qR-numeric-backstop.md", ["PBF2271_1_q_tangent", "PBC2271_8_verdict", "VAL2271_OVERALL"], "exact Phi/q covariance inverse map and q tangent locked."),
        ("2272_algebraic_lift", ROOT / "2272-Y5-R2FR-minimal-psi-covariance-lift-or-qR-profile-template.md", ["ACL2272_1_right_inverse", "FIL2272_0_exactness", "VAL2272_OVERALL"], "conditional algebraic covariance lift exists, field lift unsigned."),
        ("2273_curl_gate", ROOT / "2273-Y5-R2FR-exact-psi-gradient-lift-curl-smoothing-gate.md", ["COD2273_0_general", "DEC2273_1_obstruction", "VAL2273_OVERALL"], "generic curl obstruction for promoting algebraic lift to psi gradients."),
        ("2274_curl_mechanism", ROOT / "2274-Y5-R2FR-curl-zero-mechanism-or-Hodge-residual-bound.md", ["CZM2274_3_hodge_projection", "DEC2274_3_next", "VAL2274_OVERALL"], "exact curl-zero candidates and Hodge/scale residual bound staged."),
        ("2275_carrier_inventory", ROOT / "2275-Y5-R2FR-minimal-carrier-inventory-or-scale-separated-qR-bound.md", ["MCI2275_0_covariance_ensemble", "DEC2275_3_next", "VAL2275_OVERALL"], "minimal temporal/radial carrier inventory represents q tangent algebraically."),
        ("2363_finite_qr", ROOT / "2363-Y5-R2FR-finite-qR-coefficient-source-pack-or-selector-reentry.md", ["FNF2363_0_algebraic", "NEXT2363_0_selected"], "finite q_R normal form and coefficient pack."),
        ("2364_source_vector", ROOT / "2364-Y5-R2FR-q-source-vector-normal-form-or-first-finite-bound-row.md", ["SLOT2364_0_q_euler", "FBQ2364_0_BqWeyl"], "q Euler/source-vector normal form and first bound-row queue."),
        ("2365_weyl_spurion", ROOT / "2365-Y5-R2FR-q-representation-no-Weyl-spurion-or-BqWeyl-bound-row.md", ["LBZ2365_0_metric_trace", "QWR2365_0_DqWeyl2"], "linear Weyl spurion lemma conditional; quadratic Weyl remains live."),
        ("2366_q_operator", ROOT / "2366-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md", ["QON2366_2_conditional_mass", "FRF2366_5_verdict"], "conditional q operator denominator imported; numerator/source leg selected."),
        ("2367_jq_source_leg", ROOT / "2367-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md", ["JQZ2367_1_matter_descent", "DEC2367_3_no_hidden_visible"], "j_q zero theorem conditional; coefficient functor/no-hidden-visible route selected."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def frontier_synthesis_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="FS2421_0_q_channel", object="q covariance channel", established_result="q=ln[(1-C_tt)(1+C_rr)] and weak q=C_rr-C_tt+O(C^2)", status="EXACT_CHANNEL_TARGET", implication="the local-GR branch must derive the temporal/radial channel relation, not assume AB=1"),
        base_row(row_id="FS2421_1_q_zero_surface", object="determinant/reciprocity surface", established_result="q=0 iff (1-C_tt)(1+C_rr)=1, equivalently C_rr=C_tt/(1-C_tt)", status="EXACT_CONDITIONAL_RELATION", implication="this is the reduced-GR target surface"),
        base_row(row_id="FS2421_2_pullback_tangent", object="Phi/q covariance tangent", established_result="A=exp(2Phi+q/2), B=exp(-2Phi+q/2), partial_q C_tt=-A/2, partial_q C_rr=B/2", status="EXACT_TANGENT", implication="M_q^2 and j_q have a definite tangent direction if the parent action can be pulled back"),
        base_row(row_id="FS2421_3_algebraic_lift", object="covariance-level lift", established_result="deltaU=(1/2) deltaC C^{-1} U is a right inverse for invertible active covariance block", status="CONDITIONAL_LINEAR_ALGEBRA_GAIN", implication="q direction can be represented at covariance level, but not yet as parent psi field"),
        base_row(row_id="FS2421_4_curl_obstruction", object="field-level psi-gradient lift", established_result="Omega_A=d(delta u_A) is generically nonzero for algebraic delta u_A=M u_A over finite cells", status="ACTIVE_FIELD_LIFT_BLOCKER", implication="pointwise/covariance lift cannot be promoted to local-GR proof"),
        base_row(row_id="FS2421_5_curl_zero_candidates", object="curl-zero mechanisms", established_result="constant/affine cells, carrier-aligned scalings, Lie-drag lifts, and Hodge exact projection are exact under their own clauses", status="CANDIDATES_NOT_PARENT_SIGNED", implication="the next proof needs parent carrier inventory or Hodge residual bound"),
        base_row(row_id="FS2421_6_carrier_inventory", object="temporal/radial carrier weights", established_result="deltaW_T=deltaC_tt/(s_T Omega_T^2), deltaW_R=deltaC_rr/(s_R K_R^2) can represent q tangent without curling fixed exact phases", status="MOST_CONSTRUCTIVE_DERIVATION_LEVER", implication="requires parent multimode/phase/weight permission and smoothing theorem"),
        base_row(row_id="FS2421_7_finite_qR", object="finite q residual", established_result="L_q=-1/2 M_q^2 q^2+J_q q, J_q=j_q L+O(L^2), q_R=j_q/M_q^2", status="TESTABLE_SHAPE_NOT_PREDICTION", implication="finite branch needs M_q^2, Z_q, j_q, boundary, projection, and source normalization"),
        base_row(row_id="FS2421_8_source_vector", object="q Euler/source vector", established_result="source-looking terms must be classified as forbidden, operator-owned, boundary-owned, first-class removed, or finite residual", status="NORMAL_FORM_READY_NONCLAIM", implication="no hidden cancellation policy; every surviving channel must get a coefficient or theorem-zero"),
        base_row(row_id="FS2421_9_weyl", object="Weyl source branch", established_result="linear one-Weyl scalar source vanishes under typed no-spurion grammar, but quadratic Weyl/tower survives", status="CONDITIONAL_LEMMA_PLUS_LIVE_RESIDUAL", implication="parent object-language/no-tower theorem still needed"),
        base_row(row_id="FS2421_10_jq", object="matter/source numerator", established_result="j_q=0 follows conditionally if matter/source/current coefficients descend through the same parent observed coframe", status="EXACT_CONDITIONAL_THEOREM_NOT_SIGNED", implication="coefficient functor/no-hidden-visible Hom is the source-side bottleneck"),
        base_row(row_id="FS2421_11_frontier", object="current frontier", established_result="the quotient proof is not closed; the true frontier is parent multimode permission plus coefficient-functor/source silence", status="FRONTIER_SYNTHESIZED_NONCLAIM", implication="do not loop back to generic psi quotient; attack the two live parent-structure gates"),
    ]


def proof_status_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="PSM2421_0_absent_q", proof_route="q absent from psi image", evidence="psi covariance ansatz has independent temporal/radial channels", status="FAIL_CURRENT_CLAIM", blocker="no parent image theorem forces (1-C_tt)(1+C_rr)=1"),
        base_row(route_id="PSM2421_1_vertical_q", proof_route="q quotient-vertical", evidence="q/v open-branch remains unsigned and Dq envelope retained", status="NOT_DERIVED", blocker="no equivalence relation/Dq kernel/matter descent signed"),
        base_row(route_id="PSM2421_2_stationary_q", proof_route="q stationary/minimized", evidence="finite normal form exists but M_q^2/j_q/source terms missing", status="NOT_DERIVED", blocker="no parent free-energy/action selector chooses q=0"),
        base_row(route_id="PSM2421_3_algebraic_lift", proof_route="covariance algebra realizes q tangent", evidence="deltaU=(1/2)deltaC C^{-1}U", status="CONDITIONAL_MATH_GAIN", blocker="only covariance-level; not field-level"),
        base_row(route_id="PSM2421_4_exact_gradient_lift", proof_route="psi-gradient lift realizes q tangent", evidence="curl obstruction Omega_A=d(delta u_A)", status="BLOCKED_GENERALLY", blocker="exactness/smoothing/cell boundary mechanism unsigned"),
        base_row(route_id="PSM2421_5_carrier_weight_lift", proof_route="multimode carrier weights realize q tangent without curl", evidence="two-channel carrier weight transfer formulas", status="PROMISING_NOT_PARENT_SIGNED", blocker="parent multimode permission, W_I dynamics, kernel and cone margins missing"),
        base_row(route_id="PSM2421_6_hodge_bound", proof_route="Hodge residual small by scale separation", evidence="epsilon_total <= K2 ell_cg/L_cg + K_amp epsilon_amp", status="BOUND_TEMPLATE_ONLY", blocker="ell_cg/L_cg, K constants, carrier amplitudes, q readout map and arena tolerances missing"),
        base_row(route_id="PSM2421_7_source_zero", proof_route="j_q source numerator zero", evidence="conditional matter/source descent theorem", status="EXACT_CONDITIONAL_NOT_SIGNED", blocker="coefficient functor/no-hidden-visible Hom and readout closure missing"),
        base_row(route_id="PSM2421_8_public_local_GR", proof_route="local GR/Newton derived", evidence="all upstream gates would need to close", status="BLOCKED", blocker="q protection or finite q_R bound not claim-grade"),
    ]


def finite_branch_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="FBR2421_0_Mq2", quantity="M_q^2", formula="M_q^2=n_q^A H_AB n_q^B if parent Hessian/covariance branch is signed", current_status="CONDITIONAL_DENOMINATOR_NOT_CLAIM_GRADE", needed_for="q_R denominator and local range"),
        base_row(row_id="FBR2421_1_Zq", quantity="Z_q", formula="Z_q=xi_q^2 n_q^A H_AB n_q^B; lambda_q=sqrt(Z_q/M_q^2)=xi_q conditionally", current_status="CONDITIONAL_RANGE_NOT_SOURCED", needed_for="R10/PPN/clock/orbital projection range"),
        base_row(row_id="FBR2421_2_jq", quantity="j_q", formula="delta_q S_matter=int sqrt(g) j_q L q + O(L^2 q,q^2)", current_status="SOURCE_NUMERATOR_NOT_ZERO_NOT_SOURCED", needed_for="q_R amplitude and WEP/source sensitivity"),
        base_row(row_id="FBR2421_3_weyl_linear", quantity="B_qWeyl_linear", formula="zero under scalar/quotient q and no-Weyl-spurion object grammar", current_status="CONDITIONAL_ZERO_NOT_PARENT_SIGNED", needed_for="exterior Weyl local branch"),
        base_row(row_id="FBR2421_4_weyl_quadratic", quantity="D_qWeyl2", formula="q C_abcd C^abcd or q C_abcd *C^abcd survives one-Weyl lemma", current_status="LIVE_UNSOURCED_RESIDUAL", needed_for="quadratic Weyl tower and exterior source kernel"),
        base_row(row_id="FBR2421_5_curl_residual", quantity="epsilon_curl / epsilon_total", formula="Hodge coexact residual plus WKB amplitude leakage", current_status="TEMPLATE_ONLY_INPUTS_MISSING", needed_for="finite q_R residual bound if exact carrier proof fails"),
        base_row(row_id="FBR2421_6_projection", quantity="P_obs/tau_arena", formula="maps finite q residual to PPN/R10/clock/orbital observables", current_status="MISSING_ARENA_PROJECTION", needed_for="empirical scoring"),
        base_row(row_id="FBR2421_7_acceptance", quantity="finite branch claim state", formula="only allowed after source-backed coefficients, units, projections, and no-cancellation guards", current_status="NOT_SCORE_READY", needed_for="no local empirical claim"),
    ]


def route_priority_rows() -> list[dict[str, Any]]:
    return [
        base_row(priority_id="RPR2421_0_primary", route="parent multimode permission or scalar-only no-go", rank=1, why="it decides whether the promising carrier-weight q lift is a lawful MTS parent structure or merely a useful ansatz", target="2422-Y5-R2FR-parent-multimode-permission-or-scalar-only-no-go.md"),
        base_row(priority_id="RPR2421_1_parallel", route="parent coefficient functor / no-hidden-visible Hom", rank=1, why="it attacks j_q, constants, EM, shadow/readout leakage, and source-current descent from the source side", target="2422b-Y5-R2FR-parent-coefficient-functor-or-finite-coupling-prior-runner.md"),
        base_row(priority_id="RPR2421_2_backstop", route="scale-separated q_R residual bound", rank=2, why="if multimode permission is WKB-only, this converts curl leakage into a finite local-test input", target="held_after_RPR2421_0"),
        base_row(priority_id="RPR2421_3_tower", route="quadratic Weyl/no-tower object language", rank=3, why="needed for exterior vacuum, but it is downstream of whether q is a lawful carrier/source variable", target="held_after_source_functor"),
        base_row(priority_id="RPR2421_4_empirical", route="R10/PPN/clock/orbital scoring", rank=5, why="testing before at least one parent-owned q prediction row would only test placeholders", target="defer"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2421_0_quotient_proof", gate="psi determinant/quotient proof closes", passed=False, reason="q-zero surface identified but not parent-selected"),
        base_row(gate_id="CG2421_1_algebraic_lift", gate="covariance algebraic lift can be treated as parent psi variation", passed=False, reason="curl/exactness and smoothing gates block promotion"),
        base_row(gate_id="CG2421_2_carrier_inventory", gate="carrier-weight lift is parent-signed", passed=False, reason="multimode permission and W_I dynamics missing"),
        base_row(gate_id="CG2421_3_hodge_bound", gate="curl/Hodge residual bound is score-ready", passed=False, reason="scale/readout/tolerance inputs missing"),
        base_row(gate_id="CG2421_4_finite_qR", gate="finite q_R row is score-ready", passed=False, reason="M_q^2/Z_q/j_q/projection not source-backed"),
        base_row(gate_id="CG2421_5_jq_zero", gate="j_q=0 source theorem is promoted", passed=False, reason="coefficient functor/no-hidden-visible Hom missing"),
        base_row(gate_id="CG2421_6_local_GR_Newton", gate="local GR/Newton reduction derived", passed=False, reason="q protection or finite residual bound missing"),
        base_row(gate_id="CG2421_7_GitHub", gate="public/GitHub update", passed=False, reason="private nonclaim checkpoint only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2421_0_result", decision="PSI_QUOTIENT_PROOF_NOT_CLOSED", rationale="existing evidence identifies the exact q channel and q=0 surface but does not parent-select it", consequence="no local-GR/Newton claim"),
        base_row(decision_id="DEC2421_1_real_gain", decision="COUPLING_GAP_IS_NOW_STRUCTURAL", rationale="the obstruction is not vague: algebraic covariance lift exists conditionally, but field exactness/curl/smoothing and parent carrier permission are unsigned", consequence="attack parent multimode permission instead of looping on q definitions"),
        base_row(decision_id="DEC2421_2_carrier_route", decision="CARRIER_WEIGHT_Q_LIFT_IS_PRIMARY_DERIVATION_ROUTE", rationale="it can represent temporal/radial q exchange without curling fixed exact phase gradients", consequence="2422 should decide multimode permission or scalar-only no-go"),
        base_row(decision_id="DEC2421_3_source_route", decision="COEFFICIENT_FUNCTOR_IS_PARALLEL_SOURCE_ROUTE", rationale="j_q source silence would make the finite branch harmless if descent/no-hidden-visible Hom closes", consequence="hold 2422b as parallel target"),
        base_row(decision_id="DEC2421_4_finite_policy", decision="FINITE_BRANCH_STAYS_NONCLAIM", rationale="q_R shape is testable but coefficients/projections are not sourced", consequence="do not run empirical local tests yet"),
        base_row(decision_id="DEC2421_5_public_policy", decision="NO_GITHUB_NO_PUBLIC_CLAIM", rationale="the work is frontier narrowing, not a finished GR reduction", consequence="continue private derivation work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="NEXT2421_0_selected", selection_status="selected", target_file="2422-Y5-R2FR-parent-multimode-permission-or-scalar-only-no-go.md", target_script="scripts/Y5_R2FR_parent_multimode_permission_or_scalar_only_no_go_2422.py", objective="decide whether the parent psi action permits the temporal/radial carrier-weight ensemble needed for the curl-free q lift, or prove the scalar-only route insufficient and keep q_R residual-bound only", success_condition="parent-signed multimode/phase/weight permission with smoothing and cone guards, or scalar-only no-go plus explicit nonclaim residual-bound route", do_not_do="do not smuggle in carrier weights as definitions, treat WKB intuition as a theorem, or claim local GR from algebraic covariance alone"),
        base_row(route_id="NEXT2421_1_parallel", selection_status="held_parallel", target_file="2422b-Y5-R2FR-parent-coefficient-functor-or-finite-coupling-prior-runner.md", target_script="scripts/Y5_R2FR_parent_coefficient_functor_or_finite_coupling_prior_runner_2422b.py", objective="derive the coefficient target category/functor so visible coefficients descend and vertical derivatives vanish, or stage finite coupling prior rows with units/projections", success_condition="j_q source numerator and hidden-visible coefficient leakage are zero by parent functor, or finite coupling priors remain nonclaim", do_not_do="do not claim j_q=0 from ordinary matter descent alone without constants/readout/boundary/source weights"),
    ]


def copy_branch_rows(frontier: list[dict[str, Any]], gates: list[dict[str, Any]], decision: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["frontier_synthesis"], BRANCH_COPIES["queue"], frontier),
        ("branch_wep", OUTPUTS["claim_gates"], BRANCH_COPIES["branch_wep"], gates),
        ("beta_docs", OUTPUTS["decision"], BRANCH_COPIES["beta_docs"], decision),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, source_rows in copy_specs:
        write_csv(target_path, source_rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        rows.append(base_row(copy_id=copy_id, source_path=str(source_path), target_path=str(target_path), copied=target_path.exists(), parse_ok=parse_ok, row_count=row_count, parse_detail=parse_detail))
    return rows


def all_generated_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, value in data.items():
        if key != "validation":
            rows.extend(value)
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    sources = data["source_register"]
    rows.append(base_row(validation_id="VAL2421_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2421_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    frontier_text = " ".join(str(row) for row in data["frontier_synthesis"])
    rows.append(base_row(validation_id="VAL2421_02_exact_q_channel", status="PASS" if "q=ln[(1-C_tt)(1+C_rr)]" in frontier_text and "partial_q C_tt=-A/2" in frontier_text else "FAIL", detail="exact q channel and pullback tangent retained"))
    rows.append(base_row(validation_id="VAL2421_03_lift_obstruction", status="PASS" if "deltaU=(1/2) deltaC C^{-1} U" in frontier_text and "Omega_A=d(delta u_A)" in frontier_text else "FAIL", detail="conditional algebraic lift and curl obstruction both recorded"))
    rows.append(base_row(validation_id="VAL2421_04_frontier_not_loop", status="PASS" if "FRONTIER_SYNTHESIZED_NONCLAIM" in frontier_text and "parent multimode permission" in frontier_text else "FAIL", detail="frontier advanced beyond generic psi quotient loop"))

    proof_text = " ".join(str(row) for row in data["proof_status"])
    rows.append(base_row(validation_id="VAL2421_05_proof_routes_blocked", status="PASS" if "FAIL_CURRENT_CLAIM" in proof_text and "PROMISING_NOT_PARENT_SIGNED" in proof_text and "EXACT_CONDITIONAL_NOT_SIGNED" in proof_text else "FAIL", detail="absent/vertical/stationary/carrier/source routes separated without promotion"))

    finite_text = " ".join(str(row) for row in data["finite_branch"])
    required_finite = ["M_q^2", "Z_q", "j_q", "D_qWeyl2", "epsilon_curl", "P_obs"]
    rows.append(base_row(validation_id="VAL2421_06_finite_branch_coverage", status="PASS" if all(term in finite_text for term in required_finite) else "FAIL", detail="finite q_R branch retains denominator, numerator, Weyl, curl and projection rows"))
    rows.append(base_row(validation_id="VAL2421_07_route_priority", status="PASS" if any(row["route"] == "parent multimode permission or scalar-only no-go" and int(row["rank"]) == 1 for row in data["route_priority"]) else "FAIL", detail="primary derivation route selected"))
    rows.append(base_row(validation_id="VAL2421_08_claim_gates_blocked", status="PASS" if all(not bool(row["passed"]) for row in data["claim_gates"]) else "FAIL", detail="local-GR/Newton/public/GitHub claims blocked"))
    rows.append(base_row(validation_id="VAL2421_09_next_target", status="PASS" if any(row["route_id"] == "NEXT2421_0_selected" and "multimode" in row["target_file"] for row in data["next_target"]) else "FAIL", detail="2422 multimode/scalar-no-go target selected"))

    parse_details: list[str] = []
    parse_ok_all = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, detail = csv_rows_parse(path)
        parse_ok_all = parse_ok_all and parse_ok
        parse_details.append(f"{path.name}:{row_count}:{detail}")
    rows.append(base_row(validation_id="VAL2421_10_csv_parse", status="PASS" if parse_ok_all else "FAIL", detail="; ".join(parse_details)))

    branch_ok = all(row["copied"] and row["parse_ok"] for row in data["branch_copies"])
    rows.append(base_row(validation_id="VAL2421_11_branch_copies", status="PASS" if branch_ok else "FAIL", detail=";".join(str(row["target_path"]) for row in data["branch_copies"])))

    generated = all_generated_rows(data)
    no_claim_flags = all(str(row.get("valid_for_claim")).lower() == "false" and str(row.get("claim_allowed")).lower() == "false" for row in generated)
    rows.append(base_row(validation_id="VAL2421_12_no_claim_flags", status="PASS" if no_claim_flags else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    formalization_dirty = formalization_has_2421_artifacts()
    rows.append(base_row(validation_id="VAL2421_13_formalization_untouched_by_outputs", status="PASS" if not formalization_dirty else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(base_row(validation_id="VAL2421_OVERALL", status="PASS" if overall else "FAIL", detail="2421 synthesizes the psi quotient/frontier evidence, refuses quotient/local-GR promotion, keeps finite q_R nonclaim, and selects parent multimode permission or scalar-only no-go next"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2421 — Psi Determinant Quotient Map Or Finite `q_R` Coefficients

## Result

This checkpoint prevents a loop.

The `psi` determinant/quotient route has already produced real structure: `q=ln[(1-C_tt)(1+C_rr)]`, so weakly `q=C_rr-C_tt+O(C^2)`, and the reduced local-GR target is the determinant surface `(1-C_tt)(1+C_rr)=1`.  The exact pullback tangent is also known: `partial_q C_tt=-A/2`, `partial_q C_rr=B/2`.

The best mathematical gain is the conditional covariance lift `deltaU=(1/2) deltaC C^(-1) U`.  But that is only covariance linear algebra.  A parent `psi` field needs exact gradient variations, and the field-level obstruction is `Omega_A=d(delta u_A)`, which is generically nonzero for the algebraic q-lift over finite cells.

The strongest current derivation lever is therefore the carrier-weight route: represent q as a temporal/radial carrier-weight exchange while keeping fixed exact phase gradients.  That is promising, but not yet parent-signed.  The finite `q_R` branch also remains live, but it is not score-ready because `M_q^2`, `Z_q`, `j_q`, Weyl/tower coefficients, and arena projections are not sourced.

Bottom line: no local-GR/Newton claim, no GitHub/public claim.  Next best attack is not another generic psi quotient pass; it is whether the parent MTS `psi` action permits the required multimode carrier/phase/weight inventory, or whether scalar-only MTS cannot derive this route.

## Source Register

{md_table(data["source_register"], ["source_id", "path_exists", "needles_found", "role", "source_path"])}

## Frontier Synthesis Ledger

{md_table(data["frontier_synthesis"], ["row_id", "object", "established_result", "status", "implication"])}

## Proof Status Matrix

{md_table(data["proof_status"], ["route_id", "proof_route", "evidence", "status", "blocker"])}

## Finite `q_R` Branch Handoff

{md_table(data["finite_branch"], ["row_id", "quantity", "formula", "current_status", "needed_for"])}

## Derivation Route Priority

{md_table(data["route_priority"], ["priority_id", "route", "rank", "why", "target"])}

## Claim Gates

{md_table(data["claim_gates"], ["gate_id", "gate", "passed", "reason"])}

## Decision Ledger

{md_table(data["decision"], ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(data["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"])}

## Generated Files

{md_table([base_row(output_id=key, path=str(path), exists=path.exists()) for key, path in OUTPUTS.items()], ["output_id", "path", "exists"])}

## Branch Copies

{md_table(data["branch_copies"], ["copy_id", "copied", "parse_ok", "row_count", "target_path"])}

## Validation

{md_table(data["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Practical Status

- The project is not stuck at “missing coupling” anymore; the coupling/lift gap has been localized to parent carrier permission, exactness/smoothing, and source coefficient descent.
- The cleanest derivation route is now the multimode carrier inventory, because it can represent the q tangent without treating a curled one-form deformation as a scalar field variation.
- The cleanest finite route is `j_q/M_q^2`, but only after `j_q`, `M_q^2`, `Z_q`, Weyl/tower terms, and projections are source-backed.
- Empirical local tests remain deferred until at least one parent-owned q prediction row exists.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    remove_pycache()
    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "frontier_synthesis": frontier_synthesis_rows(),
        "proof_status": proof_status_rows(),
        "finite_branch": finite_branch_rows(),
        "route_priority": route_priority_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in data.items():
        write_csv(OUTPUTS[key], rows)

    data["branch_copies"] = copy_branch_rows(data["frontier_synthesis"], data["claim_gates"], data["decision"])
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2421_OVERALL")
    print(f"{overall['validation_id']},{overall['status']},{overall['detail']}")
    print(str(DOC))


if __name__ == "__main__":
    main()
