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


DOC = ROOT / "2128-Y5-R2FR-source-side-EP-closure-ledger-and-remaining-local-GR-gates.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2127_NEXT = OUT / "P8_Y5_PARENT_QLOC_2127_NEXT_TARGET.csv"
CSV_2127_VAL = OUT / "P8_Y5_BRR545_2127_VALIDATION.csv"
CSV_2127_ID = OUT / "P8_Y5_PARENT_QLOC_2127_INERTIAL_ACTIVE_SOURCE_IDENTITY_ATTEMPT.csv"
CSV_2127_EP = OUT / "P8_Y5_PARENT_QLOC_2127_EXPLICIT_EP_CLOSURE.csv"
CSV_2127_ROUTES = OUT / "P8_Y5_PARENT_QLOC_2127_RESIDUAL_ROUTE_LEDGER.csv"
CSV_2127_GATES = OUT / "P8_Y5_PARENT_QLOC_2127_CLAIM_GATES.csv"
CSV_1963_ACTION = OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv"
CSV_1963_NO_GAMMA = OUT / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv"
CSV_2117_EXCEPTIONS = OUT / "P8_Y5_PARENT_QLOC_2117_SECTOR_EXCEPTION_LEDGER.csv"
CSV_2118_KERNELS = OUT / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv"
CSV_2123_ARENA = OUT / "P8_Y5_PARENT_QLOC_2123_ARENA_VERDICT.csv"
CSV_655_EH = OUT / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv"
CSV_1669_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1669_ARENA_PROJECTION_MATRIX.csv"
CSV_1670_UPDATE = OUT / "P8_Y5_PARENT_QLOC_1670_ARENA_PROJECTION_UPDATE.csv"
CSV_1670_PRODUCT = OUT / "P8_Y5_PARENT_QLOC_1670_PRODUCT_BOUND_CONTRACT.csv"
CSV_2099_DG = OUT / "P8_Y5_PARENT_QLOC_2099_DELTAGAMMA_COMPONENT_MAP.csv"
CSV_LOCAL_TEMPLATE = OUT / "MTS_local_residual_predictions_TEMPLATE.csv"
CSV_1209_DOMAIN = OUT / "P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv"
CSV_2120_STATUS = OUT / "P8_Y5_PARENT_QLOC_2120_ACQUISITION_STATUS.csv"
CSV_2121_IMPORT = OUT / "P8_Y5_PARENT_QLOC_2121_IMPORT_STATUS.csv"
CSV_2122_LIVE = OUT / "P8_Y5_PARENT_QLOC_2122_LIVE_DROP_PREFLIGHT.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2128_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2128-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2128*",
        "*Y5_R2FR_source_side_EP_closure_ledger_and_remaining_local_GR_gates_2128*",
        "*AFRAME_LOCAL_GR_GATES_2128*",
        "*JR2128_LOCAL_GR*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2128_00_2127_next", CSV_2127_NEXT, ["NEXT2127_0_2128", "remaining-local-GR-gates"], "2127 handoff selects source-side closure ledger and remaining local-GR gates."),
        ("SRC2128_01_2127_validation", CSV_2127_VAL, ["VAL2127_OVERALL", "PASS"], "2127 validation passed."),
        ("SRC2128_02_2127_identity", CSV_2127_ID, ["IAS2127_5_verdict", "IDENTITY_NOT_PARENT_DERIVED"], "inertial-active identity closure status."),
        ("SRC2128_03_2127_ep", CSV_2127_EP, ["EPC2127_0_identity_clause", "EXPLICIT_EP_CLOSURE_IF_NOT_DERIVED"], "explicit EP closure clause."),
        ("SRC2128_04_2127_routes", CSV_2127_ROUTES, ["RES2127_0_if_closure_adopted", "RES2127_3_remaining_gr"], "closure/no-closure residual routes."),
        ("SRC2128_05_2127_gates", CSV_2127_GATES, ["GATE2127_5_local_GR_Newton_PPN_claim", "False"], "local GR claim remains false."),
        ("SRC2128_06_1963_action", CSV_1963_ACTION, ["ACT1963_3_geometry_term", "GENERAL_LOCAL_OPERATOR_RETAINED"], "owned-coframe local action still not EH-selected."),
        ("SRC2128_07_1963_no_gamma", CSV_1963_NO_GAMMA, ["NGT1963_3_not_EH", "SCOPE_LIMIT_EXPLICIT"], "no-Gamma theorem does not prove EH/Newton."),
        ("SRC2128_08_2117_exceptions", CSV_2117_EXCEPTIONS, ["SEC2117_0_gravity_geometry", "SEC2117_9_verdict"], "sector exceptions block promotion."),
        ("SRC2128_09_2118_kernels", CSV_2118_KERNELS, ["KSR2118_2_clock_redshift_kernel", "KSR2118_7_total_no_cancellation"], "explicit residual kernels retained."),
        ("SRC2128_10_2123_arena", CSV_2123_ARENA, ["ARENA2123_4_local_gr", "NOT_CLAIMABLE"], "arena verdict blocks local GR."),
        ("SRC2128_11_655_eh", CSV_655_EH, ["EHP655_P6_second_order", "EHP655_P9_PPN_completion"], "EH-only premise audit."),
        ("SRC2128_12_1669_matrix", CSV_1669_MATRIX, ["R3_gamma", "R4_beta", "R11_EH_operator_ledger"], "arena projection matrix."),
        ("SRC2128_13_1670_update", CSV_1670_UPDATE, ["MISSING_WEAK_FIELD_METRIC_RESPONSE", "MISSING_POST_NEWTONIAN_SECOND_ORDER_RESPONSE"], "PPN projection update."),
        ("SRC2128_14_1670_product", CSV_1670_PRODUCT, ["PB1670_1_Cobs", "MISSING_OBSERVED_COFRAME_FUNCTOR_AND_NORM"], "C_obs product bound contract."),
        ("SRC2128_15_2099_dg", CSV_2099_DG, ["DGM2099_3_clock_rods", "DGM2099_5_orbital_readout"], "DeltaGamma component map."),
        ("SRC2128_16_local_template", CSV_LOCAL_TEMPLATE, ["R3_gamma", "R11_EH_operator_ledger"], "local residual prediction template."),
        ("SRC2128_17_1209_domain", CSV_1209_DOMAIN, ["DMP1209_4_total_epsilon_status", "LOWERED_NOT_NUMERIC"], "domain/projector stress audit."),
        ("SRC2128_18_2120_status", CSV_2120_STATUS, ["STAT2120_3_tau", "TAU_WEP_BLOCKED"], "MICROSCOPE numeric tau still blocked."),
        ("SRC2128_19_2121_import", CSV_2121_IMPORT, ["IMP2121_2_tau", "TAU_WEP_NOT_RUNNABLE"], "manual CMSM import status."),
        ("SRC2128_20_2122_live", CSV_2122_LIVE, ["LIVE2122_0_readout", "MISSING_LIVE_ARTIFACT"], "live drop preflight."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, expected_needles="; ".join(needles), needles_found=exists and all(needle in text for needle in needles), role=role))
    return rows


def branch_split_rows() -> list[dict[str, object]]:
    return [
        row(
            branch_case_id="BR2128_0_EP_closure_assumed",
            branch="source-side EP closure assumed",
            source_side_status="R1/source-only species weights closure-assumed zero after one measured-G quotient",
            what_this_buys="removes the source-only active prefactor obstruction as private closure debt",
            what_it_does_not_buy="EH operator selection, PPN gamma/beta, clock/light/readout transfer, source profile data, empirical validation",
            local_gr_claim_allowed=False,
        ),
        row(
            branch_case_id="BR2128_1_no_closure",
            branch="no source-side closure",
            source_side_status="finite source-vector acquisition required",
            what_this_buys="keeps all countermodels explicit and testable",
            what_it_does_not_buy="cannot score without source profile, parent basis, material tensor, C_parent, readout kernel",
            local_gr_claim_allowed=False,
        ),
        row(
            branch_case_id="BR2128_2_empirical_parallel",
            branch="empirical WEP/CMSM route",
            source_side_status="data route separate from theorem route",
            what_this_buys="can bound/test finite products if official arrays arrive",
            what_it_does_not_buy="does not prove parent source/current owner or EH operator selection",
            local_gr_claim_allowed=False,
        ),
    ]


def remaining_local_gr_gate_rows() -> list[dict[str, object]]:
    return [
        row(
            gate_id="LGR2128_0_owned_coframe_LC",
            gate="owned coframe and Levi-Civita branch",
            closure_branch_status="CONDITIONAL_SUPPORT",
            no_closure_branch_status="CONDITIONAL_SUPPORT",
            source_anchor="ACT1963_1; ACT1963_5; NGT1963_0",
            blocker="candidate branch not globally canonical; spin/affine fallback retained if rejected",
            next_action="carry as candidate support, not full local-GR proof",
            gate_pass=False,
        ),
        row(
            gate_id="LGR2128_1_EH_operator_selection",
            gate="Einstein-Hilbert/operator selection",
            closure_branch_status="OPEN",
            no_closure_branch_status="OPEN",
            source_anchor="ACT1963_3_geometry_term; NGT1963_3_not_EH; EHP655_P5/P6",
            blocker="local geometry term is general; second-order/EH-only premise not parent-derived; R11 vector required",
            next_action="attack EH/operator selection or write non-EH residual operator vector",
            gate_pass=False,
        ),
        row(
            gate_id="LGR2128_2_Newton_GM_source_normalization",
            gate="Newton/GM source normalization",
            closure_branch_status="PARTLY_CLOSURE_ASSUMED_SOURCE_SIDE_BUT_GM_TRANSFER_OPEN",
            no_closure_branch_status="OPEN_SOURCE_VECTOR",
            source_anchor="EHP655_P8_source_normalization; KSR2118_4_orbital_GM_kernel; DGM2099_5_orbital_readout",
            blocker="GM transfer convention, source profile, range law and no fitted-G absorption proof remain non-executable",
            next_action="separate source-side EP closure from orbital/GM readout kernel",
            gate_pass=False,
        ),
        row(
            gate_id="LGR2128_3_PPN_gamma",
            gate="PPN gamma/light spatial metric response",
            closure_branch_status="OPEN",
            no_closure_branch_status="OPEN",
            source_anchor="R3_gamma in 1669/1670; KSR2118_3_lightcone_kernel; DGM2099_4_photon_lightcone",
            blocker="weak-field metric/lightcone response operator missing",
            next_action="derive observed coframe weak-field response or retain gamma residual row",
            gate_pass=False,
        ),
        row(
            gate_id="LGR2128_4_PPN_beta",
            gate="PPN beta/second-order temporal response",
            closure_branch_status="OPEN",
            no_closure_branch_status="OPEN",
            source_anchor="R4_beta in 1669/1670; EHP655_P6/P9",
            blocker="post-Newtonian second-order response missing; Poisson limit alone insufficient",
            next_action="derive beta response only after EH/operator and GM normalization gates",
            gate_pass=False,
        ),
        row(
            gate_id="LGR2128_5_clock_light_readout",
            gate="clock/light/readout response",
            closure_branch_status="OPEN",
            no_closure_branch_status="OPEN",
            source_anchor="SEC2117_5; KSR2118_2; KSR2118_3; DGM2099_3/DGM2099_4",
            blocker="clock/rod/light response functionals and nonmetricity response operators not parent-signed",
            next_action="derive metric-only readout or fill response-operator bounds",
            gate_pass=False,
        ),
        row(
            gate_id="LGR2128_6_boundary_domain_projective",
            gate="boundary/domain/projective residuals",
            closure_branch_status="OPEN",
            no_closure_branch_status="OPEN",
            source_anchor="SEC2117_7/8; KSR2118_5/6; DMP1209_4_total_epsilon_status",
            blocker="domain motion, projector stress, boundary transport and all-sector projective invariance not parent-signed/numeric",
            next_action="retain absolute residual envelope unless theorem-zero or finite bounds are supplied",
            gate_pass=False,
        ),
        row(
            gate_id="LGR2128_7_empirical_validation",
            gate="empirical local/WEP validation",
            closure_branch_status="NOT_RUNNABLE",
            no_closure_branch_status="NOT_RUNNABLE",
            source_anchor="STAT2120_3_tau; IMP2121_2_tau; LIVE2122_0_readout",
            blocker="official CMSM/readout/source-worldtube live artifacts absent; tau_WEP not runnable",
            next_action="do not score until live data validate; keep derivation route separate",
            gate_pass=False,
        ),
        row(
            gate_id="LGR2128_8_total_verdict",
            gate="local GR/Newton/PPN promotion",
            closure_branch_status="BLOCKED_PRIVATE_CLOSURE_PLUS_OPEN_LEFT_HAND_GATES",
            no_closure_branch_status="BLOCKED_SOURCE_VECTOR_PLUS_OPEN_LEFT_HAND_GATES",
            source_anchor="2127 plus 1963/655/2117/2118/2123",
            blocker="multiple necessary gates remain open; closure cannot replace derivation or empirical validation",
            next_action="next target should attack EH/operator selection, the largest remaining left-hand gate",
            gate_pass=False,
        ),
    ]


def closure_debt_rows() -> list[dict[str, object]]:
    return [
        row(debt_id="DEBT2128_0_EP_source_closure", debt="source-side EP closure", status="PRIVATE_CLOSURE_NOT_DERIVATION", carried_in_branch="BR2128_0_EP_closure_assumed", must_not_claim="derived source-side GR"),
        row(debt_id="DEBT2128_1_EH_operator", debt="EH/operator selection", status="OPEN_IN_BOTH_BRANCHES", carried_in_branch="all", must_not_claim="Einstein equations/Newtonian limit"),
        row(debt_id="DEBT2128_2_PPN_response", debt="PPN gamma/beta response", status="OPEN_IN_BOTH_BRANCHES", carried_in_branch="all", must_not_claim="solar-system GR/PPN pass"),
        row(debt_id="DEBT2128_3_readout", debt="clock/light/orbit/readout transfer", status="OPEN_IN_BOTH_BRANCHES", carried_in_branch="all", must_not_claim="observable equivalence to GR"),
        row(debt_id="DEBT2128_4_empirical", debt="CMSM/profile/local data validation", status="NOT_RUNNABLE", carried_in_branch="all", must_not_claim="WEP/local empirical pass"),
    ]


def residual_template_update_rows() -> list[dict[str, object]]:
    return [
        row(row_id="R0_identity_coframe_direct", recommended_status="conditional_support", branch="both", reason="owned coframe/no-Gamma candidate exists but is not full EH/local-GR"),
        row(row_id="R1_WEP_source_charge", recommended_status="closure_assumed in EP branch; finite_bound_required in no-closure branch", branch="split", reason="source-side EP closure is explicit private debt"),
        row(row_id="R2_clock_redshift", recommended_status="open_response_operator", branch="both", reason="clock/rod functional missing"),
        row(row_id="R3_gamma", recommended_status="open_weak_field_response", branch="both", reason="gamma metric/lightcone response missing"),
        row(row_id="R4_beta", recommended_status="open_second_order_response", branch="both", reason="beta/post-Newtonian response missing"),
        row(row_id="R10_fifth_force", recommended_status="open_curve_and_coefficients", branch="both", reason="R10 field map/bound curve/coefficient chain missing"),
        row(row_id="R11_EH_operator_ledger", recommended_status="open_operator_vector", branch="both", reason="EH/operator selection not derived"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2128_0_branch_split", gate="closure/no-closure branches separated", gate_pass=True, rationale="source-side EP closure and finite source-vector acquisition are distinct branches"),
        row(gate_id="GATE2128_1_EP_closure_marked_private", gate="EP closure marked as private closure debt", gate_pass=True, rationale="closure is not treated as derivation or public claim"),
        row(gate_id="GATE2128_2_EH_gate_open", gate="EH/operator gate closed", gate_pass=False, rationale="ACT1963 retains general local operator; EHP655 P6 open"),
        row(gate_id="GATE2128_3_PPN_gate_open", gate="PPN gamma/beta gates closed", gate_pass=False, rationale="weak-field and second-order response rows remain missing"),
        row(gate_id="GATE2128_4_readout_empirical_open", gate="readout and empirical gates closed", gate_pass=False, rationale="response operators and live CMSM arrays remain absent"),
        row(gate_id="GATE2128_5_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="closure branch still has open EH/PPN/readout/empirical gates; no-closure branch also has source-vector gate"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2128_0", decision="BRANCH_SPLIT_ADOPTED_FOR_LEDGER_ONLY", because="source-side EP closure is useful bookkeeping but not derivation", next_action="carry closure flag explicitly in future local residual rows"),
        row(decision_id="DEC2128_1", decision="EH_OPERATOR_IS_NEXT_BEST_TARGET", because="even with source-side closure, GR/Newton still needs EH/operator selection before PPN beta/gamma are meaningful", next_action="attack EH/operator selection or write non-EH operator vector"),
        row(decision_id="DEC2128_2", decision="EMPIRICAL_ROUTE_STAYS_SEPARATE", because="CMSM/live source profile data can test finite products but cannot prove parent closure", next_action="do not run WEP score until live artifacts validate"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2128_0_2129",
            next_target="2129-Y5-R2FR-EH-operator-selection-or-nonEH-residual-vector.md",
            script="scripts/Y5_R2FR_EH_operator_selection_or_nonEH_residual_vector_2129.py",
            objective="On the EP-closure bookkeeping branch, attack the largest remaining left-hand gate: prove the owned-coframe local geometry term reduces to EH plus Lambda through local 4D metric second-order/diffeomorphism premises, or retain a non-EH residual operator vector for R3/R4/R10/R11.",
            forbidden_shortcuts="treating EP closure as EH proof; using Poisson limit as PPN beta/gamma; dropping higher-curvature/nonlocal/operator terms; claiming local GR/Newton/PPN; cancellation; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    branch_split: list[dict[str, object]],
    gates: list[dict[str, object]],
    debts: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2128_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_LOCAL_GR_GATE_MAP_2128_NONCLAIM.csv", branch_split + gates + debts),
        ("COPY2128_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2128_LOCAL_GR_GATE_MAP_NONCLAIM.csv", branch_split + gates + debts),
        ("COPY2128_2_acquisition_queue", QUEUE / "JR2128_EH_OPERATOR_OR_LOCAL_GR_GATE_QUEUE.csv", next_rows + gates),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    branch_split: list[dict[str, object]],
    local_gr_gates: list[dict[str, object]],
    debts: list[dict[str, object]],
    residual_template: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    split_ok = any(item["branch_case_id"] == "BR2128_0_EP_closure_assumed" for item in branch_split) and any(item["branch_case_id"] == "BR2128_1_no_closure" for item in branch_split)
    local_gates_ok = any(item["gate_id"] == "LGR2128_1_EH_operator_selection" and not truthy(item["gate_pass"]) for item in local_gr_gates) and any(item["gate_id"] == "LGR2128_8_total_verdict" and not truthy(item["gate_pass"]) for item in local_gr_gates)
    debts_ok = any(item["debt_id"] == "DEBT2128_0_EP_source_closure" and item["status"] == "PRIVATE_CLOSURE_NOT_DERIVATION" for item in debts) and any(item["debt_id"] == "DEBT2128_1_EH_operator" for item in debts)
    residual_template_ok = any(item["row_id"] == "R1_WEP_source_charge" and "closure_assumed" in item["recommended_status"] for item in residual_template) and any(item["row_id"] == "R11_EH_operator_ledger" and item["recommended_status"] == "open_operator_vector" for item in residual_template)
    gates_ok = any(item["gate_id"] == "GATE2128_0_branch_split" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2128_5_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2128_1" and item["decision"] == "EH_OPERATOR_IS_NEXT_BEST_TARGET" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2128_0_2129" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, branch_split, local_gr_gates, debts, residual_template, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2128_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, split_ok, local_gates_ok, debts_ok, residual_template_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2128_00_sources", sources_ok, "all cited source/local-GR gate rows exist and contain expected needles"),
        ("VAL2128_01_split", split_ok, "EP-closure and no-closure branches are separated"),
        ("VAL2128_02_local_gates", local_gates_ok, "EH/operator and total local-GR gates remain blocked"),
        ("VAL2128_03_debts", debts_ok, "closure debt and EH/operator debt are explicit"),
        ("VAL2128_04_residual_template", residual_template_ok, "local residual template statuses are staged without claim flags"),
        ("VAL2128_05_gates", gates_ok, "branch split gate passes while local-GR/Newton/PPN claim fails"),
        ("VAL2128_06_decisions", decisions_ok, "decision ledger selects EH/operator selection as next best target"),
        ("VAL2128_07_next", next_ok, "next target is EH operator selection or non-EH residual vector"),
        ("VAL2128_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2128_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2128_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2128_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2128"),
        ("VAL2128_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2128_OVERALL", all_ok, "2128 separates source-side EP closure from no-closure finite-source acquisition and maps the remaining local-GR/Newton gates."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    branch_split: list[dict[str, object]],
    local_gr_gates: list[dict[str, object]],
    debts: list[dict[str, object]],
    residual_template: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2128 - Y5/R2FR Source-Side EP Closure Ledger And Remaining Local-GR Gates",
            "## Current Verdict",
            "2128 separates the local branch into two honest paths. Path A assumes the source-side EP closure privately: source-only active prefactors are closure-zero after one measured-G quotient. Path B rejects that closure and keeps a finite source-vector acquisition branch. Neither path earns a local GR/Newton/PPN claim.",
            "The reason is now clean: even if Path A removes the source-side coupling obstruction, the left-hand GR side is still open. The owned-coframe/no-independent-Gamma branch helps, but it does not select Einstein-Hilbert, does not prove second-order PPN beta/gamma, does not close clock/light/orbit readout transfer, and does not validate local data. Next best target is therefore EH/operator selection.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Branch Split",
            md_table(branch_split, ["branch_case_id", "branch", "source_side_status", "what_this_buys", "what_it_does_not_buy", "local_gr_claim_allowed"]),
            "## Remaining Local-GR Gates",
            md_table(local_gr_gates, ["gate_id", "gate", "closure_branch_status", "no_closure_branch_status", "blocker", "next_action", "gate_pass"]),
            "## Closure Debt Ledger",
            md_table(debts, ["debt_id", "debt", "status", "carried_in_branch", "must_not_claim", "valid_for_claim"]),
            "## Residual Template Update",
            md_table(residual_template, ["row_id", "recommended_status", "branch", "reason", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "valid_for_claim", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    branch_split = branch_split_rows()
    local_gr_gates = remaining_local_gr_gate_rows()
    debts = closure_debt_rows()
    residual_template = residual_template_update_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2128_SOURCE_REGISTER.csv",
        "branch_split": OUT / "P8_Y5_PARENT_QLOC_2128_SOURCE_SIDE_BRANCH_SPLIT.csv",
        "local_gr_gates": OUT / "P8_Y5_PARENT_QLOC_2128_REMAINING_LOCAL_GR_GATE_MAP.csv",
        "debts": OUT / "P8_Y5_PARENT_QLOC_2128_CLOSURE_DEBT_LEDGER.csv",
        "residual_template": OUT / "P8_Y5_PARENT_QLOC_2128_RESIDUAL_TEMPLATE_UPDATE.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2128_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2128_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2128_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2128_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2128_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["branch_split"], branch_split)
    write_csv(paths["local_gr_gates"], local_gr_gates)
    write_csv(paths["debts"], debts)
    write_csv(paths["residual_template"], residual_template)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(branch_split, local_gr_gates, debts, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, branch_split, local_gr_gates, debts, residual_template, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, branch_split, local_gr_gates, debts, residual_template, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
