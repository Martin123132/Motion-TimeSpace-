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


DOC = ROOT / "2116-Y5-R2FR-spin-connection-parent-action-signature-or-axial-CMTS-component-source-values.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2115_NEXT = OUT / "P8_Y5_PARENT_QLOC_2115_NEXT_TARGET.csv"
CSV_2115_SPIN = OUT / "P8_Y5_PARENT_QLOC_2115_SPIN_GUARD_GATE.csv"
CSV_2115_AXIAL = OUT / "P8_Y5_PARENT_QLOC_2115_AXIAL_CMTS_KRT_MAP.csv"
CSV_2115_KRT = OUT / "P8_Y5_PARENT_QLOC_2115_KRT_BOUND_ANCHOR_STATUS.csv"
CSV_2115_VAL = OUT / "P8_Y5_BRR545_2115_VALIDATION.csv"

DOC_1963 = ROOT / "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md"
CSV_1963_ACTION = OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv"
CSV_1963_NOGAMMA = OUT / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv"
DOC_1962 = ROOT / "1962-Y5-R2FR-parent-q-metric-matter-ownership-or-P4-fallback.md"
CSV_1962_OWN = OUT / "P8_Y5_PARENT_QLOC_1962_OWNERSHIP_THEOREM_ATTEMPT.csv"

CSV_1309_MATTER = OUT / "P8_Y5_R10_1309_MATTER_CONSTANT_PREMISE_GATE.csv"
CSV_943_COFRAME = OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"
CSV_944_DESCENT = OUT / "P8_Y5_R10_944_DESCENT_PROOF_GATE.csv"
CSV_2114_SECTOR = OUT / "P8_Y5_PARENT_QLOC_2114_SECTOR_GAMMA_SLOT_AUDIT.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2116_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2116-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2116*",
        "*Y5_R2FR_spin_connection_parent_action_signature_or_axial_CMTS_component_source_values_2116*",
        "*AFRAME_SPIN_PARENT_SIGNATURE_2116*",
        "*JR2116_CANONICAL*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2116_00_2115_next",
            CSV_2115_NEXT,
            ["NEXT2115_0_2116", "omega_LC[e_obs]", "C_basis"],
            "2115 selects parent spin signature or axial component sourcing.",
        ),
        (
            "SRC2116_01_2115_spin",
            CSV_2115_SPIN,
            ["SOG2115_0_spin_connection_owner", "SOG2115_6_verdict", "SPIN_ZERO_NOT_PARENT_SIGNED"],
            "2115 records the missing parent spin-connection signature.",
        ),
        (
            "SRC2116_02_2115_axial",
            CSV_2115_AXIAL,
            ["AKM2115_4_KRT_basis_projection", "AKM2115_5_spin_coupling_kernel", "AKM2115_8_verdict"],
            "2115 records the fallback axial C_MTS/KRT map and missing coupling inputs.",
        ),
        (
            "SRC2116_03_2115_krt",
            CSV_2115_KRT,
            ["KRT2115_0_KRT2008_anchor", "1e-31", "ready_for_scoring"],
            "2115 keeps KRT as a source-backed anchor but not a score.",
        ),
        (
            "SRC2116_04_2115_validation",
            CSV_2115_VAL,
            ["VAL2115_OVERALL", "PASS", "coupling signature"],
            "2115 validation passed and points at the coupling signature.",
        ),
        (
            "SRC2116_05_1963_doc",
            DOC_1963,
            ["S_parent = S_MTS_core[Xi,e,q]", "omega_LC[e_obs]", "NGT1963_1_spinor_guard"],
            "1963 writes the owned-coframe candidate parent action and spinor guard.",
        ),
        (
            "SRC2116_06_1963_action",
            CSV_1963_ACTION,
            ["ACT1963_0_target", "ACT1963_1_variable_list", "ACT1963_5_no_independent_Gamma_clause"],
            "1963 gives the candidate variable signature excluding independent observed connection.",
        ),
        (
            "SRC2116_07_1963_nogamma",
            CSV_1963_NOGAMMA,
            ["NGT1963_0_theorem", "NGT1963_1_spinor_guard", "NGT1963_3_not_EH"],
            "1963 proves no independent connection current inside the candidate branch and states the scope limit.",
        ),
        (
            "SRC2116_08_1962_doc",
            DOC_1962,
            ["OWN1962_3_connection_lock", "OWN1962_5_no_Gamma_variation", "ZERO_PROOF_NOT_CLAIMED"],
            "1962 supplies the parent ownership theorem attempt and warns it is not yet a claim.",
        ),
        (
            "SRC2116_09_1962_own",
            CSV_1962_OWN,
            ["OWN1962_3_connection_lock", "OWN1962_4_matter_functor", "OWN1962_7_verdict"],
            "1962 states the owned-coframe branch and its unsigned status.",
        ),
        (
            "SRC2116_10_1309_matter",
            CSV_1309_MATTER,
            ["MCG1309_0_observed_coframe", "CONDITIONAL_NOT_PARENT_DERIVED"],
            "1309 confirms the universal matter coframe/spin-connection clause is conditional.",
        ),
        (
            "SRC2116_11_943_coframe",
            CSV_943_COFRAME,
            ["CFC943_4_connection_lock", "CFC943_7_contract_verdict", "contract_exact_but_unsigned"],
            "943 keeps the coframe coupling contract exact but unsigned.",
        ),
        (
            "SRC2116_12_944_descent",
            CSV_944_DESCENT,
            ["QDG944_4_geometry_stack_descent", "QDG944_7_total", "not_proved_current_corpus"],
            "944 keeps geometry-stack descent conditional.",
        ),
        (
            "SRC2116_13_2114_sector",
            CSV_2114_SECTOR,
            ["SGS2114_2_spin", "SGS2114_9_verdict", "FAIL_CURRENT_CLAIM"],
            "2114 shows spin is only one sector and LC activation remains globally blocked.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                expected_needles="; ".join(needles),
                needles_found=exists and all(needle in text for needle in needles),
                role=role,
            )
        )
    return rows


def parent_spin_signature_rows() -> list[dict[str, object]]:
    return [
        row(
            audit_id="PSS2116_0_candidate_action",
            requirement="write a parent action branch where ordinary spin sees only owned coframe geometry",
            evidence="ACT1963_0_target writes S_parent = S_MTS_core + S_local_geom + sum_A S_A[Psi_A,e,omega_LC[e],A_owned,theta_A]",
            status="CANDIDATE_BRANCH_EXISTS_NONCANONICAL",
            consequence="the spin-zero route is not fantasy; it has a concrete candidate branch",
            missing_for_global_claim="promote candidate branch into canonical parent framework",
            branch_zero=True,
        ),
        row(
            audit_id="PSS2116_1_variable_list",
            requirement="exclude independent observed connection from local variables",
            evidence="ACT1963_1_variable_list gives Vars_local = {e_obs, Xi_MTS, Psi_A, A_owned}; omega_obs is defined as omega_LC[e_obs]",
            status="VARIABLE_SIGNATURE_EXPLICIT_IN_CANDIDATE",
            consequence="delta/delta Gamma_ind is vacuous inside the candidate branch",
            missing_for_global_claim="show this variable list covers every local ordinary sector and readout",
            branch_zero=True,
        ),
        row(
            audit_id="PSS2116_2_no_independent_Gamma",
            requirement="forbid Palatini, torsion, nonmetricity and connection-readout slots",
            evidence="ACT1963_5_no_independent_Gamma_clause excludes observed Palatini/torsion/nonmetricity/connection-readout slots",
            status="SIGNED_INSIDE_CANDIDATE_BRANCH",
            consequence="no independent contorsion K_abc or C_MTS spin argument exists in this branch",
            missing_for_global_claim="audit sector exceptions from 2114 and promote exclusion language to canonical action",
            branch_zero=True,
        ),
        row(
            audit_id="PSS2116_3_spinor_guard",
            requirement="spinor dependence on omega_LC[e_obs] must not source independent torsion",
            evidence="NGT1963_1_spinor_guard: spin current is Belinfante/Hilbert absorbed unless an Einstein-Cartan connection is separately introduced",
            status="SPIN_ESCAPE_GUARDED_IN_CANDIDATE",
            consequence="within the candidate owned-coframe branch, spin torsion current is not an independent P4 residual",
            missing_for_global_claim="explicitly split or forbid Einstein-Cartan/metric-affine alternatives",
            branch_zero=True,
        ),
        row(
            audit_id="PSS2116_4_vertical_silence",
            requirement="q-vertical representative changes cannot alter spin geometry",
            evidence="NGT1963_2_q_vertical_silence: Dq(v)=0 implies delta_v e_obs=0, delta_v omega_LC[e_obs]=0, delta_v S_matter=0",
            status="CONDITIONAL_CHAIN_RULE_ZERO_IN_CANDIDATE",
            consequence="q_loc spin-sector leakage vanishes if the owned quotient map is parent-signed",
            missing_for_global_claim="derive q and e_obs from deeper MTS variables rather than install them as branch skeleton",
            branch_zero=True,
        ),
        row(
            audit_id="PSS2116_5_scope_limit",
            requirement="do not overclaim EH/Newton from this spin closure",
            evidence="NGT1963_3_not_EH and 2114 sector audit state LC/no-hypermomentum is necessary but not sufficient",
            status="SCOPE_LIMIT_ENFORCED",
            consequence="spin branch progress does not claim local GR, Newtonian GM, PPN, WEP or KRT pass",
            missing_for_global_claim="EH/second-order/source/readout/PPN gates remain live",
            branch_zero=False,
        ),
        row(
            audit_id="PSS2116_6_verdict",
            requirement="decide whether the parent spin signature is found",
            evidence="1963 supplies a candidate action branch, while 1309/943/944/2114 say the full corpus remains conditional/unsigned",
            status="SIGNED_INSIDE_1963_CANDIDATE_NOT_GLOBAL_CORPUS",
            consequence="set spin/axial coupling to zero only inside the candidate owned-coframe branch; keep fallback rows globally",
            missing_for_global_claim="canonical owned-coframe promotion plus sector-exception audit",
            branch_zero=True,
        ),
    ]


def axial_component_source_value_rows() -> list[dict[str, object]]:
    return [
        row(
            value_id="ACV2116_0_xi_A_candidate_branch",
            input_name="xi_A",
            candidate_owned_coframe_value="0",
            fallback_affine_value="MISSING_XI_A_AND_MIXING_MATRIX",
            status="DERIVED_ZERO_ONLY_INSIDE_CANDIDATE_BRANCH",
            rationale="xi_A multiplies an independent axial torsion spin coupling; that coupling is not an argument of the 1963 owned-coframe candidate action.",
            source_anchor="ACT1963_5_no_independent_Gamma_clause; NGT1963_1_spinor_guard; AKM2115_5_spin_coupling_kernel",
            score_ready=False,
        ),
        row(
            value_id="ACV2116_1_A_MTS_candidate_branch",
            input_name="A_MTS^mu",
            candidate_owned_coframe_value="0",
            fallback_affine_value="MISSING_C_MTS_COMPONENTS_OR_ZERO_THEOREM",
            status="DERIVED_ZERO_ONLY_IF_Gamma_MTS_EQUALS_LC_IN_CANDIDATE",
            rationale="candidate branch defines omega_obs as omega_LC[e_obs] and excludes independent connection; torsion/axial projection are absent rather than fitted small.",
            source_anchor="PSS2116_1_variable_list; SOG2115_4_LC_spin_axial_zero; AKM2115_2_axial_projection",
            score_ready=False,
        ),
        row(
            value_id="ACV2116_2_C_basis_candidate_branch",
            input_name="C_basis",
            candidate_owned_coframe_value="not_required_when_A_MTS_zero",
            fallback_affine_value="MISSING_BASIS_MAP",
            status="NOT_REQUIRED_FOR_ZERO_BRANCH_REQUIRED_FOR_AFFINE_FALLBACK",
            rationale="if A_MTS is theorem-zero, no KRT basis projection is needed; otherwise C_basis remains mandatory.",
            source_anchor="AKM2115_4_KRT_basis_projection",
            score_ready=False,
        ),
        row(
            value_id="ACV2116_3_frame_candidate_branch",
            input_name="R_KRT<-MTS",
            candidate_owned_coframe_value="not_required_when_A_MTS_zero",
            fallback_affine_value="MISSING_FRAME_CONVENTION",
            status="NOT_REQUIRED_FOR_ZERO_BRANCH_REQUIRED_FOR_AFFINE_FALLBACK",
            rationale="frame/component labels matter only if a nonzero axial component is being compared to KRT.",
            source_anchor="AKM2115_6_frame_component",
            score_ready=False,
        ),
        row(
            value_id="ACV2116_4_KRT_bound_candidate_branch",
            input_name="KRT component bound",
            candidate_owned_coframe_value="not_used_as_pass",
            fallback_affine_value="SOURCE_BACKED_ORDER_ANCHOR_NOT_COMPONENT_TABLE",
            status="ANCHOR_RETAINED_NOT_SCORE",
            rationale="the KRT 1e-31 GeV row is useful only for the affine fallback after component/basis/frame/coupling inputs are filled.",
            source_anchor="KRT2115_0_KRT2008_anchor",
            score_ready=False,
        ),
        row(
            value_id="ACV2116_5_affine_fallback_total",
            input_name="C_MTS -> KRT score row",
            candidate_owned_coframe_value="zero_by_variable_absence_if_branch_promoted",
            fallback_affine_value="MISSING_C_MTS_XI_A_C_BASIS_FRAME_COMPONENT_BOUND",
            status="FALLBACK_STILL_BLOCKED_GLOBALLY",
            rationale="outside the candidate zero branch, all 2115 coupling inputs remain missing and no cancellation is allowed.",
            source_anchor="AKM2115_8_verdict; GATE2115_4_KRT_score_ready",
            score_ready=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(
            gate_id="GATE2116_0_candidate_parent_spin_signature",
            gate="1963 candidate branch signs spin connection owner",
            gate_pass=True,
            rationale="inside the candidate branch, variables exclude independent connection and spinors use omega_LC[e_obs]",
        ),
        row(
            gate_id="GATE2116_1_candidate_xiA_zero",
            gate="xi_A is zero by variable absence inside candidate branch",
            gate_pass=True,
            rationale="no independent A_MTS_mu J5^mu or contorsion argument exists in the candidate action",
        ),
        row(
            gate_id="GATE2116_2_global_parent_signature",
            gate="full corpus has canonical parent spin signature",
            gate_pass=False,
            rationale="1963 is candidate/noncanonical, while 1309/943/944/2114 still mark the universal matter/descent/sector gates unsigned",
        ),
        row(
            gate_id="GATE2116_3_affine_KRT_score",
            gate="affine fallback can be scored against KRT",
            gate_pass=False,
            rationale="C_MTS values, xi_A fallback, C_basis, frame and component-specific KRT table are still missing",
        ),
        row(
            gate_id="GATE2116_4_LC_activation",
            gate="LC/local-GR activation for whole project",
            gate_pass=False,
            rationale="spin is improved, but other Gamma slots plus EH/source/readout/PPN gates remain open",
        ),
        row(
            gate_id="GATE2116_5_no_claim",
            gate="no local-GR/KRT/WEP/PPN claim allowed",
            gate_pass=True,
            rationale="2116 records a branch-signature advance and fallback ledger only",
        ),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2116_0",
            decision="SPIN_CLOSES_INSIDE_OWNED_COFRAME_CANDIDATE",
            because="1963 gives a candidate action with omega_LC[e_obs] and no independent observed connection variable.",
            next_action="Use this as the least-scrutiny spin route rather than trying to numerically fit away torsion.",
        ),
        row(
            decision_id="DEC2116_1",
            decision="GLOBAL_CLAIM_STILL_BLOCKED",
            because="The candidate branch is noncanonical and every-sector matter/source/readout exceptions are not yet audited shut.",
            next_action="Promote the owned-coframe branch to a canonical parent action or list exact exceptions.",
        ),
        row(
            decision_id="DEC2116_2",
            decision="AFFINE_KRT_FALLBACK_KEPT",
            because="If the candidate branch fails, the theory still needs real C_MTS, xi_A, C_basis, frame and component-specific bound inputs.",
            next_action="Do not use KRT as a pass unless those inputs are filled.",
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2116_0_2117",
            next_target="2117-Y5-R2FR-canonical-owned-coframe-action-promotion-or-sector-exceptions-ledger.md",
            script="scripts/Y5_R2FR_canonical_owned_coframe_action_promotion_or_sector_exceptions_ledger_2117.py",
            objective=(
                "Try to promote the 1963 owned-coframe candidate into a canonical local parent branch by auditing every ordinary sector "
                "for direct Gamma, contorsion, representative, source/readout, species-marker, boundary or projective exceptions. If any survive, "
                "write explicit exception residual rows rather than claiming LC/local GR."
            ),
            forbidden_shortcuts=(
                "treating the 1963 candidate as already global; ignoring 2114 sector exceptions; using KRT as a pass; "
                "local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action"
            ),
        )
    ]


def write_branch_copies(
    signature_rows: list[dict[str, object]],
    axial_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2116_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_SPIN_PARENT_SIGNATURE_2116_NONCLAIM.csv",
            signature_rows + axial_rows + gates,
        ),
        (
            "COPY2116_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2116_SPIN_PARENT_STATUS_NONCLAIM.csv",
            signature_rows + axial_rows,
        ),
        (
            "COPY2116_2_acquisition_queue",
            QUEUE / "JR2116_CANONICAL_OWNED_COFRAME_OR_AXIAL_INPUT_QUEUE.csv",
            next_rows + axial_rows,
        ),
    ]
    result: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        result.append(
            row(
                copy_id=copy_id,
                destination=str(destination),
                path_exists=destination.exists(),
                row_count=len(rows_to_write),
                parse_ok=csv_rows_parse(destination),
            )
        )
    return result


def validation_rows(
    sources: list[dict[str, object]],
    signature_rows: list[dict[str, object]],
    axial_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    candidate_ok = any(
        item["audit_id"] == "PSS2116_6_verdict"
        and item["status"] == "SIGNED_INSIDE_1963_CANDIDATE_NOT_GLOBAL_CORPUS"
        for item in signature_rows
    )
    xi_zero_ok = any(
        item["value_id"] == "ACV2116_0_xi_A_candidate_branch"
        and item["candidate_owned_coframe_value"] == "0"
        and item["status"] == "DERIVED_ZERO_ONLY_INSIDE_CANDIDATE_BRANCH"
        for item in axial_rows
    )
    fallback_blocked_ok = any(
        item["value_id"] == "ACV2116_5_affine_fallback_total"
        and item["status"] == "FALLBACK_STILL_BLOCKED_GLOBALLY"
        for item in axial_rows
    )
    gates_ok = (
        any(item["gate_id"] == "GATE2116_0_candidate_parent_spin_signature" and truthy(item["gate_pass"]) for item in gates)
        and any(item["gate_id"] == "GATE2116_2_global_parent_signature" and not truthy(item["gate_pass"]) for item in gates)
        and any(item["gate_id"] == "GATE2116_3_affine_KRT_score" and not truthy(item["gate_pass"]) for item in gates)
    )
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, signature_rows, axial_rows, gates, decisions, next_rows, copies)
        for item in group
    )
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2116_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    next_ok = any(item["route_id"] == "NEXT2116_0_2117" for item in next_rows)
    all_ok = all(
        [
            sources_ok,
            candidate_ok,
            xi_zero_ok,
            fallback_blocked_ok,
            gates_ok,
            no_claim_flags,
            branch_ok,
            csv_ok,
            formalization_clean,
            pycache_clean,
            next_ok,
        ]
    )
    checks = [
        ("VAL2116_00_sources", sources_ok, "all cited 2115/1963/1962 coupling sources exist and contain expected needles"),
        ("VAL2116_01_candidate_signature", candidate_ok, "spin parent signature is found inside the 1963 candidate branch but not globally"),
        ("VAL2116_02_xiA_zero_branch", xi_zero_ok, "xi_A is derived zero only inside the owned-coframe candidate branch"),
        ("VAL2116_03_affine_fallback", fallback_blocked_ok, "affine KRT fallback remains blocked globally"),
        ("VAL2116_04_claim_gates", gates_ok, "candidate gate passes but global/KRT/local-GR gates remain false"),
        ("VAL2116_05_no_claim_flags", no_claim_flags, "no generated row allows a claim or score"),
        ("VAL2116_06_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2116_07_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2116_08_formalization_clean", formalization_clean, "formalization-workbench untouched by 2116"),
        ("VAL2116_09_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2116_10_next", next_ok, "next target selects canonical owned-coframe promotion or sector exceptions"),
        (
            "VAL2116_OVERALL",
            all_ok,
            "2116 finds a candidate parent spin signature, derives zero axial coupling inside that branch, keeps global claims blocked, and selects canonicalization next.",
        ),
    ]
    return [
        row(
            check_id=check_id,
            status="PASS" if passed else "FAIL",
            detail=detail,
        )
        for check_id, passed, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    signature_rows: list[dict[str, object]],
    axial_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2116 - Y5/R2FR Spin Connection Parent Action Signature Or Axial CMTS Component Source Values",
            "## Current Verdict",
            (
                "2116 finds the first useful leap through the coupling problem. The 1963 owned-coframe candidate branch already has the "
                "right spin signature: ordinary spinors use `omega_LC[e_obs]`, the observed variable list excludes an independent "
                "connection, and the spinor guard says spin current is Belinfante/Hilbert absorbed unless an Einstein-Cartan branch is separately introduced."
            ),
            (
                "So inside that candidate branch the axial spin coupling can be set to zero by variable absence: `xi_A=0`, `A_MTS=0`, "
                "and the KRT map is not needed. That is stronger than a fitted small number."
            ),
            (
                "But this is not yet a public/global MTS claim. The branch is still labelled candidate/noncanonical, and the 2114 sector audit plus "
                "1309/943/944 still leave ordinary-sector exceptions and geometry descent unsigned. Therefore the honest status is: "
                "spin closes inside the owned-coframe candidate branch; full local-GR/LC activation remains blocked until the branch is canonicalized "
                "and sector exceptions are audited."
            ),
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Parent Spin Signature Audit",
            md_table(
                signature_rows,
                [
                    "audit_id",
                    "requirement",
                    "status",
                    "evidence",
                    "consequence",
                    "missing_for_global_claim",
                    "branch_zero",
                    "valid_for_claim",
                ],
            ),
            "## Axial Component Source Values",
            md_table(
                axial_rows,
                [
                    "value_id",
                    "input_name",
                    "candidate_owned_coframe_value",
                    "fallback_affine_value",
                    "status",
                    "rationale",
                    "score_ready",
                    "valid_for_claim",
                ],
            ),
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
    signature_rows = parent_spin_signature_rows()
    axial_rows = axial_component_source_value_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2116_SOURCE_REGISTER.csv",
        "signature": OUT / "P8_Y5_PARENT_QLOC_2116_PARENT_SPIN_SIGNATURE_AUDIT.csv",
        "axial": OUT / "P8_Y5_PARENT_QLOC_2116_AXIAL_COMPONENT_SOURCE_VALUES.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2116_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2116_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2116_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2116_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2116_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["signature"], signature_rows)
    write_csv(paths["axial"], axial_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(signature_rows, axial_rows, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, signature_rows, axial_rows, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, signature_rows, axial_rows, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
