from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2079-Y5-R2FR-kfloor-topological-Hessian-owner-or-finite-noncoercive-Robin-demotion.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2079_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2079-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2079*",
        "*Y5_R2FR_kfloor_topological_Hessian_owner_or_finite_noncoercive_Robin_demotion_2079*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2079_00_2078_doc",
            ROOT / "2078-Y5-R2FR-Jmin-Hmax-lambda-min-mu-min-first-source-rows-or-impossibility-ledger.md",
            ["NEXT2078_0_2079", "STRICT_CURRENT_ROUTE_BLOCKED_SELECT_FLOOR_OR_FINITE_BRANCH", "VAL2078_OVERALL"],
            "2078 handoff: strict current-density route is blocked; test k_floor or demote to finite branch.",
        ),
        (
            "SRC2079_01_2078_validation",
            OUT / "P8_Y5_BRR545_2078_VALIDATION.csv",
            ["VAL2078_OVERALL", "2079 k_floor", "claim_allowed"],
            "2078 validation proves the route-selection handoff and no-claim state.",
        ),
        (
            "SRC2079_02_2077_lower_bound",
            OUT / "P8_Y5_PARENT_QLOC_2077_KC_MIN_LOWER_BOUND_THEOREM.csv",
            ["LBT2077_2_strict_bound", "STRICT_COERCIVITY_NOT_AUTOMATIC", "SYMBOLIC_JOIN_ONLY"],
            "2077 lower-bound theorem and finite energy-bound join.",
        ),
        (
            "SRC2079_03_2076_energy_inputs",
            ROOT / "2076-Y5-R2FR-positive-current-density-cap-functional-or-first-numeric-energy-bound-inputs.md",
            ["q_R_hat_policy_ceiling = 4.6e-05", "RUNNER_BLOCKED_MISSING_INPUTS", "FEI2076_11_KqR"],
            "2076 energy input ledger and nonclaim q_R policy ceiling.",
        ),
        (
            "SRC2079_04_1056_topology",
            ROOT / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
            ["TL1056_1_BF_or_CS_level", "TOPOLOGICAL_ROUTE_NOT_CLOSED", "independent F_Q^2"],
            "topological/level route audit: topology alone does not own a kinetic coefficient.",
        ),
        (
            "SRC2079_05_1101_level",
            ROOT / "1101-Y5-R10-gauge-fibre-level-index-monopole-Ward-owner-or-alpha-product-route.md",
            ["GNO1101_1_topological_level", "NO_EM_LEVEL_SOURCE", "CURRENT_OWNER_SUPPORT_NOT_KINETIC_OWNER"],
            "level/Ward audit: level-like structures can own labels/currents but not a continuous stiffness without a norm owner.",
        ),
        (
            "SRC2079_06_1025_hessian",
            ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            ["SV1025_2_Hessian_signs", "MISSING_PARENT_HESSIAN_SIGN", "FAIL_CURRENT_CLAIM"],
            "parent Hessian route: exact second-variation contract exists but signs/units are not parent-owned.",
        ),
        (
            "SRC2079_07_1551_qnorm",
            ROOT / "1551-Y5-parent-qnorm-source-or-local-closure-demotion.md",
            ["HUNT1551_1_parent_hessian", "MISSING_PARENT_HESSIAN", "closure-only"],
            "q-norm hunt already demotes unsourced Hessian/local closure routes.",
        ),
        (
            "SRC2079_08_1552_template",
            ROOT / "1552-Y5-parent-q-sector-action-norm-extraction-template.md",
            ["ACT1552_1_quadratic_form", "TEMPLATE_REQUIRED_NOT_SUPPLIED", "BLOCKED_PENDING_POSITIVITY"],
            "positive parent quadratic form template: useful contract, no supplied positive/coercive input.",
        ),
        (
            "SRC2079_09_1904_constructor",
            ROOT / "1904-Y5-R2FR-parent-action-constructor-exhaustion-or-action-scale-owner.md",
            ["CE1904_0_target", "PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED", "topological level"],
            "constructor exhaustion/action-scale owner remains conditional; cannot create a hidden floor by fiat.",
        ),
        (
            "SRC2079_10_2062_boundary",
            ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            ["BGA2062_4_orientation", "MISSING_ORIENTATION_CONVENTION", "CONDITIONAL_PROOF_ONLY"],
            "cap/worldtube orientation and boundary/corner grammar are not signed enough for finite stiffness scoring.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                exists=path.exists(),
                needle_count=len(needles),
                missing_needles=";".join(missing),
                status="EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                note=note,
            )
        )
    return rows


def floor_theorem_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="KFT2079_0_minimal_floor_form",
            claim_piece="strict Robin floor candidate",
            formal_statement="k_C := k_floor + lambda_C*mu_C*||J_tau^cap||_h^2/H_*^2",
            sufficient_condition="k_floor >= k_floor_min > 0 from the same parent action/domain as the Robin boundary term",
            consequence="k_C >= k_floor_min even when J_tau^cap=0",
            status="CONDITIONAL_THEOREM_EXACT",
            parent_signed=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="KFT2079_1_boundary_Hessian_condition",
            claim_piece="Hessian floor",
            formal_statement="delta^2 S_parent|_cap >= k_floor_min ||delta R_cap||^2_boundary after quotienting gauge/null modes",
            sufficient_condition="self-adjoint cap/domain operator, positive boundary Hessian spectrum, fixed units, and no negative mixed block",
            consequence="strict cap coercivity is derived without forcing nonzero current",
            status="BEST_DERIVATION_SHAPE_NOT_SOURCED",
            parent_signed=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="KFT2079_2_topological_limit",
            claim_piece="topological level as floor",
            formal_statement="integer/topological level k can quantize a coefficient only if the parent action includes an inheritance theorem from k to the metric-dependent Robin quadratic form",
            sufficient_condition="cap-specific level, fixed normalization, no independent counterterm, and positive boundary quadratic response",
            consequence="topology alone does not supply k_floor_min",
            status="TOPOLOGY_ALONE_REJECTED_AS_STIFFNESS_PROOF",
            parent_signed=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="KFT2079_3_protected_modulus_condition",
            claim_piece="protected cap modulus floor",
            formal_statement="U_cap''(R_*) >= m_cap^2 > 0 plus fixed cap measure/orientation gives a positive local stiffness floor",
            sufficient_condition="parent-owned cap modulus, positive Hessian/gap, fixed measure/orientation, and boundary/corner silence",
            consequence="would repair strict Robin if sourced",
            status="CONDITIONAL_ROUTE_MISSING_MODULUS_AND_GEOMETRY",
            parent_signed=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="KFT2079_4_verdict",
            claim_piece="promote strict Robin activation",
            formal_statement="Current corpus supplies a parent-owned k_floor_min>0",
            sufficient_condition="KFT2079_1 or KFT2079_3 parent-signed with units and source path",
            consequence="strict Robin local-GR route could reopen",
            status="FAIL_CURRENT_CORPUS_DEMOTE_STRICT_ROBIN",
            parent_signed=False,
            claim_allowed=False,
        ),
    ]


def source_attempt_rows() -> list[dict[str, object]]:
    return [
        row(
            attempt_id="KFS2079_0_topological_level",
            candidate_owner="topological/level floor",
            searched_sources="1056;1101;1904",
            positive_evidence="level-like routes are known theorem targets and can fix discrete labels or response coefficients conditionally",
            obstruction="no cap-specific inheritance theorem maps a discrete level to the metric-dependent positive Robin stiffness k_floor",
            status="MISSING_CAP_LEVEL_TO_ROBIN_STIFFNESS_MAP",
            next_action="do not use topology as stiffness unless a cap-level Hessian/Robin inheritance row is written",
            source_ready=False,
            claim_allowed=False,
        ),
        row(
            attempt_id="KFS2079_1_parent_Hessian_gap",
            candidate_owner="parent Hessian or mass-gap floor",
            searched_sources="1025;1551;1552",
            positive_evidence="exact second-variation contracts exist for positive operators and q-norm extraction",
            obstruction="Z/Hessian signs, units, cross-Hessian positivity, and source-free boundary domain are not parent-signed",
            status="MISSING_PARENT_HESSIAN_GAP_FOR_CAP",
            next_action="requires explicit cap-sector second variation and quotient/null-mode removal",
            source_ready=False,
            claim_allowed=False,
        ),
        row(
            attempt_id="KFS2079_2_protected_cap_modulus",
            candidate_owner="protected cap modulus",
            searched_sources="2062;2076;2077;2078",
            positive_evidence="mu_min compact-geometry route is conditionally plausible once cap geometry/orientation is fixed",
            obstruction="no cap modulus potential U_cap and no parent-signed boundary/corner orientation grammar",
            status="MISSING_CAP_MODULUS_AND_ORIENTATION",
            next_action="source cap geometry/orientation only after a modulus/Hessian owner exists",
            source_ready=False,
            claim_allowed=False,
        ),
        row(
            attempt_id="KFS2079_3_constructor_exhaustion",
            candidate_owner="absence of extra local floor counterterms",
            searched_sources="1904",
            positive_evidence="constructor-exhaustion normal form would be powerful if parent-signed",
            obstruction="constructor membership and no-marker/no-extension closure are not derived",
            status="CANNOT_DECLARE_ONLY_ALLOWED_FLOOR",
            next_action="keep k_floor as missing, not chosen",
            source_ready=False,
            claim_allowed=False,
        ),
    ]


def demotion_rows() -> list[dict[str, object]]:
    return [
        row(
            demotion_id="DEM2079_0_strict_Robin",
            object="strict Robin activation via k_C_min>0",
            previous_state="candidate repair after J_min route failed",
            new_state="DEMOTED_TO_CLOSURE_ONLY_UNTIL_KFLOOR_SOURCE_EXISTS",
            reason="J_min can vanish and no parent-owned k_floor_min was found",
            retained_use="may be used as a conditional theorem target, not as evidence for local GR",
            claim_allowed=False,
        ),
        row(
            demotion_id="DEM2079_1_current_density_floor",
            object="positive current-density cap functional",
            previous_state="sign-safe nonnegative stiffness",
            new_state="NONNEGATIVE_ONLY",
            reason="k_C>=0 does not control constant/zero-current modes",
            retained_use="valid sign mechanism inside finite energy identities",
            claim_allowed=False,
        ),
        row(
            demotion_id="DEM2079_2_kfloor",
            object="additive k_floor",
            previous_state="best repair candidate",
            new_state="MISSING_PARENT_INPUT",
            reason="topological, Hessian, and protected-modulus routes are conditional but unsigned",
            retained_use="exact acquisition row and future theorem target",
            claim_allowed=False,
        ),
        row(
            demotion_id="DEM2079_3_local_claim",
            object="local GR/Newton/PPN/R10 from strict Robin zero theorem",
            previous_state="blocked",
            new_state="STILL_BLOCKED",
            reason="no strict coercive cap activation and no finite q_R_hat prediction",
            retained_use="finite residual testing only after source inputs are acquired",
            claim_allowed=False,
        ),
    ]


def finite_branch_rows() -> list[dict[str, object]]:
    return [
        row(
            row_id="FIN2079_0_branch_law",
            quantity="finite noncoercive Robin energy branch",
            formula="a := C_Poincare*rho_R_norm + C_trace*b_C_norm; X_E <= 0.5*(a + sqrt(a^2 + 4*F_outer_abs)); q_R_hat <= K_qR*X_E",
            status="RETAINED_AS_NONCLAIM_FALLBACK",
            required_inputs="C_Poincare;C_trace;rho_R_norm;b_C_norm;F_outer_abs;K_qR;domain_id;norm_id;source_paths",
            value="SYMBOLIC_ONLY",
            score_ready=False,
            claim_allowed=False,
        ),
        row(
            row_id="FIN2079_1_kCmin_policy",
            quantity="k_C_min",
            formula="k_C_min=0 for the demoted noncoercive fallback branch",
            status="DELIBERATE_NONZERO_THEOREM_REFUSAL",
            required_inputs="none for demotion; finite branch still needs source norms and constants before scoring",
            value="0",
            score_ready=False,
            claim_allowed=False,
        ),
        row(
            row_id="FIN2079_2_qR_ceiling",
            quantity="q_R_hat_policy_ceiling",
            formula="external comparator from QRHAT1255/2076/2077",
            status="SOURCE_BACKED_NONCLAIM_COMPARATOR_ONLY",
            required_inputs="q_R_hat_predicted from MTS finite branch before any comparison",
            value="4.6e-05",
            score_ready=False,
            claim_allowed=False,
        ),
        row(
            row_id="FIN2079_3_next_inputs",
            quantity="finite branch acquisition inputs",
            formula="source rows before scoring",
            status="MISSING_THEORY_SIDE_INPUTS",
            required_inputs="C_Poincare;C_trace;rho_R_norm;b_C_norm;F_outer_abs;K_qR;orientation/domain/norm metadata",
            value="MISSING",
            score_ready=False,
            claim_allowed=False,
        ),
    ]


def acquisition_rows() -> list[dict[str, object]]:
    specs = [
        ("ACQ2079_0_kfloor_min", "k_floor_min", "positive additive Robin floor", "MISSING_PARENT_FLOOR", "source cap Hessian/topological inheritance/protected modulus", "W_R/length units"),
        ("ACQ2079_1_cap_Hessian", "H_cap_min", "positive quotient cap-boundary Hessian eigenvalue", "MISSING_PARENT_HESSIAN_GAP", "derive second variation in same branch/domain", "action per boundary field squared"),
        ("ACQ2079_2_cap_level", "k_top_cap", "cap-specific topological/level coefficient tied to Robin stiffness", "MISSING_LEVEL_TO_STIFFNESS_MAP", "write inheritance theorem or reject", "dimensionless or level-normalized units"),
        ("ACQ2079_3_cap_modulus", "m_cap^2", "protected cap modulus curvature", "MISSING_CAP_MODULUS", "source U_cap'' and field normalization", "mass/stiffness units"),
        ("ACQ2079_4_cap_geometry", "mu_C_orientation_domain", "fixed cap measure/orientation/domain metadata", "MISSING_ORIENTATION_CONVENTION", "source normal, corner, boundary and domain rows", "cap measure units"),
        ("ACQ2079_5_C_Poincare", "C_Poincare", "annulus/domain Poincare constant for finite branch", "MISSING_DOMAIN_GEOMETRY_CONSTANT", "source domain/norm constant", "geometry units"),
        ("ACQ2079_6_C_trace", "C_trace", "boundary trace constant for finite branch", "MISSING_DOMAIN_TRACE_CONSTANT", "source boundary Sobolev/trace constant", "geometry units"),
        ("ACQ2079_7_rho", "rho_R_norm", "bulk reciprocal source dual norm", "MISSING_BULK_SOURCE_NORM", "derive/source local source profile norm", "dual source units"),
        ("ACQ2079_8_bC", "b_C_norm", "cap boundary/source-reference residue norm", "MISSING_BOUNDARY_RESIDUE_NORM", "derive/source cap residue norm", "dual boundary units"),
        ("ACQ2079_9_Fouter", "F_outer_abs", "absolute outer/asymptotic flux", "MISSING_OUTER_FLUX_BOUND", "derive/source outer flux envelope", "energy-like units"),
        ("ACQ2079_10_KqR", "K_qR", "map reciprocal energy norm to q_R_hat", "MISSING_QRHAT_MAP", "derive normalization chain to q_R_hat", "dimensionless per norm"),
        ("ACQ2079_11_qRceiling", "q_R_hat_policy_ceiling", "external nonclaim comparison ceiling", "SOURCE_BACKED_NONCLAIM_COMPARATOR_ONLY", "compare only after q_R_hat_predicted exists", "dimensionless"),
    ]
    rows = []
    for row_id, quantity, definition, status, next_action, units in specs:
        rows.append(
            row(
                row_id=row_id,
                quantity=quantity,
                definition=definition,
                current_value="4.6e-05" if row_id == "ACQ2079_11_qRceiling" else "MISSING",
                units=units,
                status=status,
                next_action=next_action,
                score_ready=False,
                claim_allowed=False,
            )
        )
    return rows


def dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2079_0_kfloor_source_hunt",
            target="k_floor_min parent source",
            verdict="FAIL_MISSING_PARENT_OWNER",
            reason="topological/level, Hessian/gap, and protected-modulus routes are conditional but unsigned",
            score_ready=False,
            claim_allowed=False,
        ),
        row(
            run_id="RUN2079_1_strict_robin",
            target="strict Robin zero theorem",
            verdict="DEMOTE_TO_CLOSURE_ONLY",
            reason="no k_C_min>0 route survives without missing parent inputs",
            score_ready=False,
            claim_allowed=False,
        ),
        row(
            run_id="RUN2079_2_finite_branch",
            target="finite noncoercive energy branch",
            verdict="PASS_SCHEMA_ONLY",
            reason="symbolic bound law retained with k_C_min=0, but source norms/constants are missing",
            score_ready=False,
            claim_allowed=False,
        ),
        row(
            run_id="RUN2079_VERDICT",
            target="route decision",
            verdict="STRICT_ROBIN_DEMOTED_FINITE_BRANCH_NEXT",
            reason="2079 makes the no-smuggling decision: no nonzero floor without source; next attack is finite theory-side input acquisition",
            score_ready=False,
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(
            gate_id="GATE2079_0_kfloor",
            condition="parent-owned k_floor_min>0 exists",
            status="FAIL_BLOCKED",
            reason="no cap-level, Hessian/gap, or protected-modulus source is parent-signed",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2079_1_topology",
            condition="topological level alone supplies stiffness",
            status="FAIL_REJECTED",
            reason="topology/level can quantize labels or response but not a metric-dependent positive Robin quadratic without inheritance theorem",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2079_2_Hessian",
            condition="positive cap Hessian/gap is parent signed",
            status="FAIL_BLOCKED",
            reason="prior Hessian/q-norm source rows remain missing/conditional",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2079_3_strict_Robin",
            condition="strict Robin activation is usable as derived local closure",
            status="FAIL_DEMOTED",
            reason="k_C_min>0 is not sourced",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2079_4_finite_score",
            condition="finite branch can compute q_R_hat_predicted",
            status="FAIL_MISSING_INPUTS",
            reason="C_Poincare, C_trace, rho_R_norm, b_C_norm, F_outer_abs, and K_qR are missing",
            claim_allowed=False,
        ),
        row(
            gate_id="GATE2079_5_local_claim",
            condition="derived local GR/Newton/PPN/R10 claim",
            status="FAIL_BLOCKED",
            reason="neither zero theorem nor finite prediction exists",
            claim_allowed=False,
        ),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2079_0_exact_floor_contract",
            decision="k_floor has a clean exact contract",
            because="an additive positive boundary/cap Hessian floor would repair the zero-current problem without forcing J_min>0",
            next_action="keep as theorem target and acquisition row",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2079_1_no_topology_shortcut",
            decision="topology/level is not a stiffness proof by itself",
            because="a metric-independent level or label owner does not give a positive Robin quadratic unless inheritance to k_floor is parent-signed",
            next_action="reject topology-only k_floor claims",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2079_2_demote_strict_Robin",
            decision="strict Robin activation is demoted",
            because="neither J_min nor k_floor_min is source-backed",
            next_action="use finite noncoercive energy branch as the next executable route",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2079_3_next",
            decision="finite energy-bound source acquisition is now the best route",
            because="it is less likely to be accused of closure smuggling and keeps all residuals visible",
            next_action="2080 should source C_Poincare, C_trace, rho_R_norm, b_C_norm, F_outer_abs, and K_qR",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2079_0_2080",
            target_doc="2080-Y5-R2FR-finite-noncoercive-energy-bound-input-source-runner.md",
            objective="source or bound the finite noncoercive Robin energy-branch inputs after strict k_C_min activation is demoted: C_Poincare, C_trace, rho_R_norm, b_C_norm, F_outer_abs, K_qR, domain/norm metadata, and q_R_hat_predicted dry-run",
            must_include="finite bound law; k_C_min=0 demotion guard; domain/norm constants; source norms; boundary residue; outer flux; K_qR normalization; QRHAT1255 comparator guard; no-cancellation envelope",
            exclusions="k_floor by assertion; topology-only stiffness; J_min from norm positivity; q_R_hat=0 closure; using policy ceiling as prediction; local-GR/PPN/R10 claim; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    floor_rows: list[dict[str, object]],
    demotion: list[dict[str, object]],
    finite: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2079_0_source_weight_kfloor",
            SOURCE_WEIGHT_DOCS / "AFRAME_KFLOOR_TOPOLOGICAL_HESSIAN_2079_NONCLAIM.csv",
            floor_rows,
        ),
        (
            "COPY2079_1_wep_demotion",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2079_STRICT_ROBIN_DEMOTION_NONCLAIM.csv",
            demotion + finite,
        ),
        (
            "COPY2079_2_queue_finite_inputs",
            QUEUE / "JR2079_FINITE_NONCOERCIVE_ENERGY_INPUTS_QUEUE.csv",
            acquisition + next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data_rows in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=copy_id,
                path=str(path),
                rows_written=len(data_rows),
                status="WRITTEN_NONCLAIM_COPY",
                claim_allowed=False,
            )
        )
    return rows


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass_claim", "claim_allowed"}


def validation_rows(
    sources: list[dict[str, object]],
    floor: list[dict[str, object]],
    attempts: list[dict[str, object]],
    demotion: list[dict[str, object]],
    finite: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    floor_conditional = any(r["theorem_id"] == "KFT2079_0_minimal_floor_form" and r["status"] == "CONDITIONAL_THEOREM_EXACT" for r in floor)
    topology_rejected = any(r["status"] == "TOPOLOGY_ALONE_REJECTED_AS_STIFFNESS_PROOF" for r in floor)
    hessian_missing = any(r["status"] == "MISSING_PARENT_HESSIAN_GAP_FOR_CAP" for r in attempts)
    strict_demoted = any(r["new_state"] == "DEMOTED_TO_CLOSURE_ONLY_UNTIL_KFLOOR_SOURCE_EXISTS" for r in demotion)
    finite_retained = any(r["row_id"] == "FIN2079_0_branch_law" and r["status"] == "RETAINED_AS_NONCLAIM_FALLBACK" for r in finite)
    dry_verdict = any(r["verdict"] == "STRICT_ROBIN_DEMOTED_FINITE_BRANCH_NEXT" for r in dry)
    gates_blocked = all(not truthy(r.get("claim_allowed")) and str(r["status"]).startswith("FAIL") for r in gates)
    acquisition_nonclaim = all(not truthy(r.get("score_ready")) and not truthy(r.get("claim_allowed")) for r in acquisition)
    next_ok = next_rows_[0]["target_id"] == "NEXT2079_0_2080"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [floor, attempts, demotion, finite, acquisition, dry, gates, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2079_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2079_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2079_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2079_02_floor_contract", floor_conditional, "exact k_floor conditional contract is written"),
        ("VAL2079_03_topology_rejected", topology_rejected, "topology-only stiffness shortcut is rejected"),
        ("VAL2079_04_hessian_missing", hessian_missing, "parent Hessian/gap owner remains missing"),
        ("VAL2079_05_strict_robin_demoted", strict_demoted, "strict Robin activation is demoted to closure-only"),
        ("VAL2079_06_finite_branch_retained", finite_retained, "finite noncoercive branch is retained as nonclaim fallback"),
        ("VAL2079_07_dry_verdict", dry_verdict, "dry run selects finite branch next"),
        ("VAL2079_08_claim_gates_blocked", gates_blocked, "all claim gates remain blocked"),
        ("VAL2079_09_acquisition_nonclaim", acquisition_nonclaim, "acquisition rows remain nonclaim/non-score"),
        ("VAL2079_10_next_selected", next_ok, "2080 finite input source-runner target selected"),
        ("VAL2079_11_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2079_12_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2079_13_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2079_14_no_formalization_artifacts", no_formalization_artifacts, "no 2079 artifacts were written under formalization-workbench"),
        ("VAL2079_15_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(("VAL2079_OVERALL", overall, "2079 demotes strict Robin activation and selects finite noncoercive source acquisition"))
    return [
        row(
            check_id=check_id,
            status="PASS" if status else "FAIL",
            detail=detail,
            claim_allowed=False,
        )
        for check_id, status, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    floor: list[dict[str, object]],
    attempts: list[dict[str, object]],
    demotion: list[dict[str, object]],
    finite: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2079 Y5 R2FR kfloor topological Hessian owner or finite noncoercive Robin demotion",
        "",
        "## Current Verdict",
        "",
        "2079 tests the only honest repair left for strict Robin activation after `J_min>0` failed: an additive positive floor stiffness.",
        "",
        "The clean conditional theorem is real: if the same parent branch supplies `k_floor>=k_floor_min>0`, then",
        "`k_C := k_floor + lambda_C mu_C ||J_tau^cap||_h^2/H_*^2` gives strict coercivity even when the cap current vanishes.",
        "",
        "But the current corpus does not source that floor. Topological/level rows are analogues only, not a cap Robin stiffness inheritance theorem; Hessian/gap rows remain unsigned; protected cap-modulus rows are missing orientation, boundary/corner, and potential-curvature ownership.",
        "",
        "Therefore the strict Robin activation branch is demoted to closure-only. The live route is now the finite noncoercive energy-bound branch with `k_C_min=0`, source-ready inputs, and no local-GR/PPN/R10 claim until a theory-side `q_R_hat_predicted` is computed.",
        "",
        "No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "note", "valid_for_claim"]),
        "## k_floor Conditional Theorem",
        md_table(floor, ["theorem_id", "claim_piece", "formal_statement", "sufficient_condition", "consequence", "status", "parent_signed", "claim_allowed", "valid_for_claim"]),
        "## Source Attempts",
        md_table(attempts, ["attempt_id", "candidate_owner", "searched_sources", "positive_evidence", "obstruction", "status", "next_action", "source_ready", "claim_allowed", "valid_for_claim"]),
        "## Demotion Ledger",
        md_table(demotion, ["demotion_id", "object", "previous_state", "new_state", "reason", "retained_use", "claim_allowed", "valid_for_claim"]),
        "## Finite Noncoercive Branch",
        md_table(finite, ["row_id", "quantity", "formula", "status", "required_inputs", "value", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Acquisition Rows",
        md_table(acquisition, ["row_id", "quantity", "definition", "current_value", "units", "status", "next_action", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Dry Run",
        md_table(dry, ["run_id", "target", "verdict", "reason", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "condition", "status", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "exclusions", "claim_allowed", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows_written", "status", "claim_allowed", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    floor = floor_theorem_rows()
    attempts = source_attempt_rows()
    demotion = demotion_rows()
    finite = finite_branch_rows()
    acquisition = acquisition_rows()
    dry = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2079_SOURCE_REGISTER.csv",
        "floor": OUT / "P8_Y5_PARENT_QLOC_2079_KFLOOR_CONDITIONAL_THEOREM.csv",
        "attempts": OUT / "P8_Y5_PARENT_QLOC_2079_KFLOOR_SOURCE_ATTEMPTS.csv",
        "demotion": OUT / "P8_Y5_PARENT_QLOC_2079_STRICT_ROBIN_DEMOTION_LEDGER.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2079_FINITE_NONCOERCIVE_BRANCH.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2079_FINITE_BRANCH_ACQUISITION_ROWS.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2079_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2079_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2079_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2079_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2079_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2079_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["floor"], floor)
    write_csv(paths["attempts"], attempts)
    write_csv(paths["demotion"], demotion)
    write_csv(paths["finite"], finite)
    write_csv(paths["acquisition"], acquisition)
    write_csv(paths["dry"], dry)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(floor, demotion, finite, acquisition, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, floor, attempts, demotion, finite, acquisition, dry, gates, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, floor, attempts, demotion, finite, acquisition, dry, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
