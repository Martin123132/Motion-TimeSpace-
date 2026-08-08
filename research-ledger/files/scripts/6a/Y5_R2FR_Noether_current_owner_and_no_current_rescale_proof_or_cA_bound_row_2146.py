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


DOC = ROOT / "2146-Y5-R2FR-Noether-current-owner-and-no-current-rescale-proof-or-cA-bound-row.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2145": ROOT / "2145-Y5-R2FR-Delta-Hsrc-integrability-reference-lock-or-first-source-row.md",
    "1815": ROOT / "1815-Y5-R2FR-Noether-current-owner-and-no-current-rescale-proof-or-cA-bound-row.md",
    "1816": ROOT / "1816-Y5-R2FR-variation-before-readout-source-selector-order-or-post-current-cA-row.md",
    "1817": ROOT / "1817-Y5-R2FR-source-worldtube-transfer-kernel-or-post-current-cA-bound-row.md",
    "1818": ROOT / "1818-Y5-R2FR-Hilbert-worldtube-charge-identity-or-R-Hsrc-bound-row.md",
    "1819": ROOT / "1819-Y5-R2FR-local-EH-symplectic-charge-inheritance-or-Cterm-residual-vector.md",
    "1820": ROOT / "1820-Y5-R2FR-EH-operator-selection-minimality-or-R11-C-EH-first-row.md",
    "1821": ROOT / "1821-Y5-R2FR-no-higher-derivative-parent-minimality-or-R2FR-bound-row.md",
    "1822": ROOT / "1822-Y5-R2FR-linear-holonomy-parent-axiom-or-R2FR-coefficient-owner-row.md",
    "1823": ROOT / "1823-Y5-R2FR-primitive-deficit-action-law-or-visible-c2-owner-row.md",
    "2139": ROOT / "2139-Y5-R2FR-deep-parent-action-owner-hunt-or-coefficient-owner-checklist.md",
    "2140": ROOT / "2140-Y5-R2FR-GammaG-metric-variation-local-silence-or-residual-row.md",
    "2141": ROOT / "2141-Y5-R2FR-GammaG-functional-contract-or-local-kernel-zero-proof.md",
    "2142": ROOT / "2142-Y5-R2FR-saturation-action-vs-constitutive-branch-and-PPN-bound-runner.md",
    "2143": ROOT / "2143-Y5-R2FR-local-curvature-operator-norm-and-source-bridge-bound.md",
    "2144": ROOT / "2144-Y5-R2FR-MHref-Qtau-Gref-source-readout-bridge-or-closure.md",
}


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2146_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2146-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2146*",
        "*Y5_R2FR_Noether_current_owner_and_no_current_rescale_proof_or_cA_bound_row_2146*",
        "*AFRAME_LOCAL_GR_TWO_GATE_2146*",
        "*JR2146*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2146_00_2145", DOCS["2145"], [["VAL2145_OVERALL"], ["Noether current owner/no-rescale"]], "current handoff: 2145 selects Noether current owner/no-current-rescale"),
        ("SRC2146_01_1815", DOCS["1815"], [["VAL1815_OVERALL"], ["NO_CURRENT_RESCALE_CONTRACT_NOT_CURRENT_PROOF"], ["pre_variation_weight", "pre-variation"]], "post-current rescale conditionally killed; pre-action weight survives"),
        ("SRC2146_02_1816", DOCS["1816"], [["VAL1816_OVERALL"], ["variation-before-readout"], ["preaction", "pre-action"]], "variation-before-readout theorem target"),
        ("SRC2146_03_1817", DOCS["1817"], [["VAL1817_OVERALL"], ["K_arena"], ["HILBERT_WORLDTUBE_CHARGE_IDENTITY_NEXT"]], "worldtube/arena transfer kernel survives"),
        ("SRC2146_04_1818", DOCS["1818"], [["VAL1818_OVERALL"], ["G_ref^-1 Q_tau"], ["LOCAL_EH_SYMPLECTIC_CHARGE_INHERITANCE_NEXT"]], "Hilbert/worldtube charge identity contract"),
        ("SRC2146_05_1819", DOCS["1819"], [["VAL1819_OVERALL"], ["C_EH"], ["EH_OPERATOR_SELECTION_MINIMALITY_NEXT"]], "local EH charge inheritance and C-term residual vector"),
        ("SRC2146_06_1820", DOCS["1820"], [["VAL1820_OVERALL"], ["R2/fR"], ["NO_HIGHER_DERIVATIVE_PARENT_MINIMALITY_NEXT"]], "EH selector/R2FR scalar branch gate"),
        ("SRC2146_07_1821", DOCS["1821"], [["VAL1821_OVERALL"], ["LINEAR_HOLONOMY_PARENT_AXIOM_NEXT"]], "linear holonomy/additivity parent route"),
        ("SRC2146_08_1822", DOCS["1822"], [["VAL1822_OVERALL"], ["PRIMITIVE_DEFICIT_ACTION_LAW_NEXT"]], "same-cell linearity fails; primitive deficit action law selected"),
        ("SRC2146_09_1823", DOCS["1823"], [["VAL1823_OVERALL"], ["PHI_SECOND_DERIVATIVE_ZERO_OR_VISIBLE_C2_SOURCE_NEXT"], ["c2_visible"]], "primitive deficit law not derived; visible c2 owner exposed"),
        ("SRC2146_10_2139", DOCS["2139"], [["VAL2139_OVERALL"], ["EH_ACTION_SOURCE_FOUND"], ["GAMMAG_IS_PRIMARY_ACTION_OWNER_CANDIDATE"]], "raw parent action source scan found EH/Gamma_G source route"),
        ("SRC2146_11_2140", DOCS["2140"], [["VAL2140_OVERALL"], ["D_Gamma"], ["Gamma_G -> 0"]], "Gamma_G zeroth-order silence not enough for first variation"),
        ("SRC2146_12_2141", DOCS["2141"], [["VAL2141_OVERALL"], ["PROMOTE_S_AS_PRIMARY_GAMMAG_PARENT_SKELETON"], ["flat-kernel double-zero"]], "S/Gamma_G functional skeleton and flat double-zero only"),
        ("SRC2146_13_2142", DOCS["2142"], [["VAL2142_OVERALL"], ["NUMERIC_SMALLNESS_IS_REAL"], ["S_K=1.000000E-122"]], "smallness runner exists but remains nonclaim"),
        ("SRC2146_14_2143", DOCS["2143"], [["VAL2143_OVERALL"], ["DELTAK_REDUCED_TO_SOURCE_FRACTIONS"], ["2.000000E-122"]], "local curvature operator bound reduced to source/readout fractions"),
        ("SRC2146_15_2144", DOCS["2144"], [["VAL2144_OVERALL"], ["BRIDGE_NOT_CLOSED"], ["Delta_Hsrc"]], "measured-source bridge remains primary source blocker"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=needles_found,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
                role=role,
            )
        )
    return rows


def noether_current_gate_rows() -> list[dict[str, object]]:
    return [
        row(
            gate_id="NC2146_0_parent_connection",
            object="A_Q^vis",
            exact_clause="visible EM/test connection must be a parent-owned connection slot, not a post-fit label",
            result="CONTRACT_ONLY_FROM_1813_1814",
            implication="needed before any current-rescale theorem can bite",
            current_status="UNSIGNED_PARENT_OWNER",
        ),
        row(
            gate_id="NC2146_1_parent_current",
            object="J_Q",
            exact_clause="J_Q = delta S_matter / delta A_Q^vis before readout, arena projection, or source fitting",
            result="EXACT_CONDITIONAL_CLAUSE",
            implication="source/test current has one parent owner if antecedents are signed",
            current_status="CONDITIONAL_NOT_FULL_PROOF",
        ),
        row(
            gate_id="NC2146_2_post_current_rescale",
            object="c_A_post",
            exact_clause="after variation, replacing J_Q by c_A J_Q is not a new parent source; it is either a unit/common-normalizer convention or an illegal post-Euler rescale",
            result="CONDITIONALLY_KILLED",
            implication="post-current c_A is not the main gremlin if current ownership and variation-before-readout hold",
            current_status="DEMOTED_TO_GUARD_ROW_NOT_CLAIM",
        ),
        row(
            gate_id="NC2146_3_pre_action_weight",
            object="w_A",
            exact_clause="a coefficient multiplying a visible-sector matter/action term before variation changes the source current honestly",
            result="COUNTERMODEL_SURVIVES",
            implication="pre-action weights remain a real coupling debt",
            current_status="LIVE_RESIDUAL",
        ),
        row(
            gate_id="NC2146_4_selector_kernel",
            object="K_arena_or_FTA",
            exact_clause="arena/readout selectors downstream of the parent current can alter measured response without being post-current c_A",
            result="TRANSFER_KERNEL_SURVIVES",
            implication="WEP/R10/clock transfer cannot be borrowed from one arena to another",
            current_status="LIVE_RESIDUAL",
        ),
        row(
            gate_id="NC2146_5_source_hamiltonian_bridge",
            object="Delta_Hsrc_or_R_Hsrc",
            exact_clause="source charge used in local Newton/PPN must equal the parent Hilbert/Hamiltonian/worldtube charge under fixed reference and boundary conditions",
            result="NOT_CLOSED",
            implication="measured GM is still not derived merely from Poisson/EH shape",
            current_status="PRIMARY_SOURCE_SIDE_BLOCKER",
        ),
        row(
            gate_id="NC2146_6_operator_side",
            object="C_EH_R2FR_GammaG",
            exact_clause="local operator must reduce to EH plus silent/bounded Gamma_G and no live R2/fR scalar coefficient",
            result="NOT_CLOSED",
            implication="operator-side GR reduction remains separate from current-rescale cleanup",
            current_status="PRIMARY_OPERATOR_SIDE_BLOCKER",
        ),
        row(
            gate_id="NC2146_7_verdict",
            object="Noether current/no-current-rescale",
            exact_clause="current ownership can demote post-current rescaling only after parent connection/current and variation order are signed",
            result="CONDITIONAL_THEOREM_SHARPENED_NOT_PROMOTED",
            implication="do not keep circling c_A; carry it as a guard while attacking source/operator gates",
            current_status="NO_LOCAL_GR_CLAIM",
        ),
    ]


def fast_forward_rows() -> list[dict[str, object]]:
    chain = [
        ("FF2146_00", "2145", "current handoff", "Delta_Hsrc/source bridge branch syncs to Noether current owner target", "Noether-current target selected"),
        ("FF2146_01", "1815", "post-current c_A", "current-rescale theorem shape written; pre-variation weight survives", "c_A_post conditional, w_A live"),
        ("FF2146_02", "1816", "variation before readout", "post-readout source selectors cannot rewrite parent source unless smuggled into action", "pre-action route untouched"),
        ("FF2146_03", "1817", "arena/worldtube kernel", "fixed downstream K_arena cannot change parent source but arena maps remain open", "K_arena/R_Hsrc retained"),
        ("FF2146_04", "1818", "Hilbert charge identity", "G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc identified", "identity contract only"),
        ("FF2146_05", "1819", "local EH charge inheritance", "compact annulus EH charge inheritance reduces problem to C-term vector", "C_EH/C_extra/projector/boundary/ref open"),
        ("FF2146_06", "1820", "EH operator selection", "metric-only second-order/no-extra-scalar would kill simple R2/fR branch", "minimality unsigned"),
        ("FF2146_07", "1821", "linear holonomy", "single additive curvature-flux response would force linear curvature", "same-cell premise unsigned"),
        ("FF2146_08", "1822", "primitive deficit law", "linear area*deficit action is sharper than vague additivity", "deficit linearity unsigned"),
        ("FF2146_09", "1823", "visible c2 owner", "generic Phi(delta) exposes c2_visible=Phi''(0)/2", "Phi''(0) zero or c2 source is next"),
    ]
    rows: list[dict[str, object]] = []
    for chain_id, checkpoint, object_name, progress, current_status in chain:
        source_path = DOCS[checkpoint]
        line_number, snippet = find_line(source_path, ["Current verdict", "Current Verdict", "**Current verdict:**"])
        rows.append(
            row(
                chain_id=chain_id,
                checkpoint=checkpoint,
                source_path=str(source_path),
                verdict_line=line_number,
                object=object_name,
                progress=progress,
                current_status=current_status,
            )
        )
    return rows


def local_gr_status_rows() -> list[dict[str, object]]:
    return [
        row(
            status_id="LGR2146_0_raw_EH_source",
            sector="operator/source action",
            current_gain="raw corpus contains an EH-looking action with kappa and Gamma_G route",
            blocker="raw notation is not terminal proof of measured Newton coupling or first-variation silence",
            best_next="keep as source evidence, not claim",
        ),
        row(
            status_id="LGR2146_1_GammaG_silence",
            sector="Gamma_G/local saturation",
            current_gain="flat-kernel double-zero and K_solar smallness runner exist",
            blocker="real local systems need D_Gamma/operator norm, boundary kernel, Bianchi exchange current, and source bridge",
            best_next="join Gamma_G residual to source-normalized PPN/Newton bound",
        ),
        row(
            status_id="LGR2146_2_source_bridge",
            sector="measured Newton/source charge",
            current_gain="epsilon_mu has been decomposed through Delta_Hsrc/readout/source components",
            blocker="M_H_ref, Q_tau, G_ref, Pi_M^H and measured GM equality are not parent-signed",
            best_next="attack Delta_Hsrc/charge identity without orbital-fitting shortcuts",
        ),
        row(
            status_id="LGR2146_3_current_coupling",
            sector="visible current/coupling",
            current_gain="post-current c_A is conditionally demoted by Noether current ownership",
            blocker="pre-action weights, selector kernels and arena projections survive",
            best_next="stop treating post c_A as the main frontier; retain guard rows",
        ),
        row(
            status_id="LGR2146_4_R2FR_operator",
            sector="EH/no-extra-operator",
            current_gain="R2/fR blocker is sharpened to Phi''(0)=0 or c2_visible owner",
            blocker="primitive deficit law is promising but not derived",
            best_next="derive Phi''(0)=0 or carry c2_visible into finite bound rows",
        ),
        row(
            status_id="LGR2146_5_project_status",
            sector="whole local-GR route",
            current_gain="the project now has a two-gate spine: operator-side EH/Gamma_G/R2FR plus source-side Hamiltonian/measured-G bridge",
            blocker="neither gate is fully closed, so no local GR/Newton/PPN claim is allowed",
            best_next="build 2147 as the explicit two-gate theorem and choose the least circular closure attempt",
        ),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2146_0_post_cA",
            decision="POST_CURRENT_C_A_DEMOTED_CONDITIONALLY",
            because="Noether current ownership plus variation-before-readout makes a later J_A -> c_A J_A rescale ill-typed or conventional",
            next_action="keep c_A_post as guard row, not frontier",
        ),
        row(
            decision_id="DEC2146_1_pre_weights",
            decision="PRE_ACTION_WEIGHTS_AND_SELECTORS_SURVIVE",
            because="a coefficient in the parent action or an arena transfer kernel is not killed by post-current ownership",
            next_action="retain w_A/K_arena/R_Hsrc residuals",
        ),
        row(
            decision_id="DEC2146_2_fast_forward",
            decision="NOETHER_BRANCH_ALREADY_REACHES_C2_VISIBLE_HINGE",
            because="1815-1823 chase the current/coupling route through worldtube charge, EH charge inheritance, R2FR, linear holonomy and primitive deficit law",
            next_action="do not repeat broad coupling audits",
        ),
        row(
            decision_id="DEC2146_3_current_project_status",
            decision="LOCAL_GR_REDUCTION_IS_TWO_GATE_SPINE",
            because="latest 2139-2145 work adds raw EH/Gamma_G action source, Gamma_G residual smallness, and Delta_Hsrc/source bridge rows",
            next_action="join source-side and operator-side gates explicitly in 2147",
        ),
        row(
            decision_id="DEC2146_4_claim_policy",
            decision="NO_LOCAL_GR_NEWTON_PPN_R10_CLAIM",
            because="post c_A is only conditional and the remaining source/operator gates are open",
            next_action="private derivation-first work continues; no GitHub/public claim",
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2146_0_2147",
            next_target="2147-Y5-R2FR-local-GR-two-gate-spine-source-operator-join.md",
            script="scripts/Y5_R2FR_local_GR_two_gate_spine_source_operator_join_2147.py",
            objective="Write the exact local-GR/Newton reduction theorem with two gates: operator-side EH/Gamma_G/R2FR silence and source-side Hamiltonian/measured-G bridge. Then pick one closure attempt: Delta_Hsrc source equality or Phi''(0)=0/c2_visible, with all failed clauses kept as nonclaim rows.",
            forbidden_shortcuts="do not claim GR from EH-looking notation; do not claim Newton from Poisson shape; do not zero Gamma_G from Gamma_G=0 alone; do not zero R2/fR from locality/additivity alone; do not use post-current c_A cleanup to erase pre-action weights; no formalization-workbench edits; no GitHub action",
        )
    ]


def write_branch_copies(
    fast_forward: list[dict[str, object]],
    noether_gates: list[dict[str, object]],
    local_gr: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2146_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_LOCAL_GR_TWO_GATE_2146_NONCLAIM.csv", local_gr + noether_gates),
        ("COPY2146_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2146_CURRENT_COUPLING_GUARD_NONCLAIM.csv", noether_gates + fast_forward),
        ("COPY2146_2_acquisition_queue", QUEUE / "JR2146_LOCAL_GR_TWO_GATE_QUEUE.csv", next_rows + local_gr),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    noether_gates: list[dict[str, object]],
    fast_forward: list[dict[str, object]],
    local_gr: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    noether_ok = (
        any(item["gate_id"] == "NC2146_2_post_current_rescale" and item["result"] == "CONDITIONALLY_KILLED" for item in noether_gates)
        and any(item["gate_id"] == "NC2146_3_pre_action_weight" and item["result"] == "COUNTERMODEL_SURVIVES" for item in noether_gates)
        and any(item["gate_id"] == "NC2146_7_verdict" and item["current_status"] == "NO_LOCAL_GR_CLAIM" for item in noether_gates)
    )
    fast_forward_ok = (
        len(fast_forward) == 10
        and fast_forward[0]["checkpoint"] == "2145"
        and fast_forward[-1]["checkpoint"] == "1823"
        and any(item["object"] == "visible c2 owner" for item in fast_forward)
    )
    local_gr_ok = (
        any(item["status_id"] == "LGR2146_2_source_bridge" and "Delta_Hsrc" in str(item["current_gain"]) for item in local_gr)
        and any(item["status_id"] == "LGR2146_4_R2FR_operator" and "Phi''(0)" in str(item["current_gain"]) for item in local_gr)
        and any(item["status_id"] == "LGR2146_5_project_status" and "two-gate spine" in str(item["current_gain"]) for item in local_gr)
    )
    decisions_ok = (
        any(item["decision"] == "POST_CURRENT_C_A_DEMOTED_CONDITIONALLY" for item in decisions)
        and any(item["decision"] == "LOCAL_GR_REDUCTION_IS_TWO_GATE_SPINE" for item in decisions)
    )
    next_ok = any(item["route_id"] == "NEXT2146_0_2147" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, noether_gates, fast_forward, local_gr, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2146_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, noether_ok, fast_forward_ok, local_gr_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2146_00_sources", sources_ok, "2145, 1815-1823 and 2139-2144 source checkpoints validate"),
        ("VAL2146_01_noether_gate", noether_ok, "post-current c_A is conditionally demoted while pre-action weights survive"),
        ("VAL2146_02_fast_forward", fast_forward_ok, "current/no-rescale branch is fast-forwarded to the c2_visible hinge"),
        ("VAL2146_03_local_gr_status", local_gr_ok, "local-GR status contains source bridge, R2FR/Phi'' and two-gate spine rows"),
        ("VAL2146_04_decisions", decisions_ok, "decisions reject circling and select the two-gate spine"),
        ("VAL2146_05_next", next_ok, "next target is 2147 local-GR two-gate source/operator join"),
        ("VAL2146_06_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2146_07_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2146_08_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2146_09_formalization_clean", formalization_clean, "formalization-workbench untouched by 2146"),
        ("VAL2146_10_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2146_OVERALL", all_ok, "2146 conditionally demotes post-current c_A, preserves live pre-action/source/operator gates, and selects the local-GR two-gate spine next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    noether_gates: list[dict[str, object]],
    fast_forward: list[dict[str, object]],
    local_gr: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2146 - Y5/R2FR Noether Current Owner And No Current Rescale Proof Or cA Bound Row",
            "## Current Verdict",
            "2146 does **not** prove local GR, Newton, PPN, WEP, R10, or a public coupling claim. It does something cleaner: it demotes the narrow post-current rescale gremlin. If `A_Q^vis` and `J_Q = delta S_matter/delta A_Q^vis` are parent-owned and matter is varied before readout, then a later `J_A -> c_A J_A` is not a new physical source coupling; it is either a common normalization/unit convention or an illegal post-Euler rescale.",
            "That is a useful conditional theorem, but not a total victory. Pre-action weights `w_A`, arena transfer kernels `K_arena`, source Hamiltonian mismatch `Delta_Hsrc/R_Hsrc`, and operator-side residuals `Gamma_G/C_EH/R2FR` survive. So the project should not keep circling broad 'coupling' language. The real local-GR reduction problem is now a **two-gate spine**: operator-side EH/Gamma_G/R2FR silence plus source-side Hamiltonian/measured-G bridge.",
            "The fast-forward result is important: the older current/no-rescale branch already reaches the primitive deficit / visible `c2` hinge. The next honest leap is not another c_A audit; it is to join the source and operator gates into one exact local-GR/Newton theorem and then try to close one gate without shortcuts.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Noether Current Gate",
            md_table(noether_gates, ["gate_id", "object", "exact_clause", "result", "implication", "current_status", "valid_for_claim"]),
            "## Fast-Forward Chain",
            md_table(fast_forward, ["chain_id", "checkpoint", "verdict_line", "object", "progress", "current_status", "valid_for_claim"]),
            "## Local GR Status",
            md_table(local_gr, ["status_id", "sector", "current_gain", "blocker", "best_next", "valid_for_claim"]),
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
    noether_gates = noether_current_gate_rows()
    fast_forward = fast_forward_rows()
    local_gr = local_gr_status_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2146_SOURCE_REGISTER.csv",
        "noether_gates": OUT / "P8_Y5_PARENT_QLOC_2146_NOETHER_CURRENT_GATE.csv",
        "fast_forward": OUT / "P8_Y5_PARENT_QLOC_2146_FAST_FORWARD_CHAIN.csv",
        "local_gr": OUT / "P8_Y5_PARENT_QLOC_2146_LOCAL_GR_STATUS.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2146_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2146_NEXT_TARGET.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2146_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2146_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["noether_gates"], noether_gates)
    write_csv(paths["fast_forward"], fast_forward)
    write_csv(paths["local_gr"], local_gr)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(fast_forward, noether_gates, local_gr, next_rows)
    write_csv(paths["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, noether_gates, fast_forward, local_gr, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, noether_gates, fast_forward, local_gr, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
