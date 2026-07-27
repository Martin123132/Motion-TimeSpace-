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


DOC = ROOT / "2127-Y5-R2FR-inertial-active-source-identity-or-explicit-EP-closure.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2126_NEXT = OUT / "P8_Y5_PARENT_QLOC_2126_NEXT_TARGET.csv"
CSV_2126_VAL = OUT / "P8_Y5_BRR545_2126_VALIDATION.csv"
CSV_2126_PROOF = OUT / "P8_Y5_PARENT_QLOC_2126_NOSOURCE_SLOT_PROOF_ATTEMPT.csv"
CSV_2126_CLOSURE = OUT / "P8_Y5_PARENT_QLOC_2126_EXPLICIT_CLOSURE_CLAUSE.csv"
CSV_2126_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2126_PARENT_OBJECT_LANGUAGE_AUDIT.csv"
CSV_1676_OWNER = OUT / "P8_Y5_PARENT_QLOC_1676_ACTION_SCALE_CURRENT_OWNER_GATE.csv"
CSV_1687_OWNER = OUT / "P8_Y5_PARENT_QLOC_1687_COMMON_ACTION_MEASURE_CURRENT_OWNER_PROOF_ATTEMPT.csv"
CSV_1899_OWNER = OUT / "P8_Y5_PARENT_QLOC_1899_ACTION_CURRENT_OWNER_LEMMA_ATTEMPT.csv"
CSV_1418_LOCK = OUT / "P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv"
CSV_953_FUNCTOR = OUT / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv"
CSV_955_PREF = OUT / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv"
CSV_956_SPINE = OUT / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv"
CSV_966_ELIM = OUT / "P8_Y5_R10_966_GENERATOR_ELIMINATION_LEDGER.csv"
CSV_1479_TYPING = OUT / "P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv"
CSV_1479_HOM = OUT / "P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv"
CSV_1479_COUNTER = OUT / "P8_Y5_R10_1479_SOURCE_ONLY_PREFACTOR_COUNTERMODEL_LEDGER.csv"
CSV_1895_OBJECT = OUT / "P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv"
CSV_1895_GATE = OUT / "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2127_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2127-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2127*",
        "*Y5_R2FR_inertial_active_source_identity_or_explicit_EP_closure_2127*",
        "*AFRAME_EP_CLOSURE_2127*",
        "*JR2127_EP*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2127_00_2126_next", CSV_2126_NEXT, ["NEXT2126_0_2127", "inertial-active-source-identity"], "2126 handoff selects inertial-active source identity or explicit EP closure."),
        ("SRC2127_01_2126_validation", CSV_2126_VAL, ["VAL2126_OVERALL", "PASS"], "2126 validation passed."),
        ("SRC2127_02_2126_proof", CSV_2126_PROOF, ["NSP2126_4_verdict", "NOT_PARENT_DERIVED"], "NoSourceOnlySpeciesSlot proof failed as parent derivation."),
        ("SRC2127_03_2126_closure", CSV_2126_CLOSURE, ["CLS2126_0_minimal_clause", "EXPLICIT_CLOSURE_REQUIRED_IF_NOT_DERIVED"], "minimal no-source closure clause."),
        ("SRC2127_04_2126_audit", CSV_2126_AUDIT, ["OLA2126_4_countermodel", "LIVE_COUNTERMODEL"], "source-weight countermodel retained."),
        ("SRC2127_05_1676_owner_gate", CSV_1676_OWNER, ["ACO1676_0_single_action_scale", "SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED"], "action/current owner gate."),
        ("SRC2127_06_1687_owner_proof", CSV_1687_OWNER, ["COM1687_3_action_scale", "OBSTRUCTION_EXPLICIT", "COM1687_6_verdict"], "common action measure/current owner attempt."),
        ("SRC2127_07_1899_owner_lemma", CSV_1899_OWNER, ["ACO1899_3_classical_rescale_obstruction", "ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED"], "action/current owner lemma."),
        ("SRC2127_08_1418_lock", CSV_1418_LOCK, ["ACL1418_1_classical_not_enough", "LOCK_NOT_PROVED_CURRENT_CORPUS"], "action-scale/current-owner lock."),
        ("SRC2127_09_953_functor", CSV_953_FUNCTOR, ["NSF953_2_conditional_uniqueness", "NSF953_4_calibration_limit"], "source functor theorem attempt."),
        ("SRC2127_10_955_prefactor", CSV_955_PREF, ["SPC955_2_relative_species_weight", "live_countermodel"], "source prefactor classification."),
        ("SRC2127_11_956_spine", CSV_956_SPINE, ["SSG956_5_source_side_verdict", "conditional_spine_sharp_not_claimable"], "source-side GR/Newton spine."),
        ("SRC2127_12_966_elim", CSV_966_ELIM, ["GE966_1_species_constants", "conditional_uniqueness_not_parent_signed"], "generator elimination ledger."),
        ("SRC2127_13_1479_typing", CSV_1479_TYPING, ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"], "typing theorem attempt."),
        ("SRC2127_14_1479_hom", CSV_1479_HOM, ["HOM1479_1_species_to_prefactor", "FORBIDDEN_BY_CONTRACT_NOT_PARENT_DERIVED"], "Hom species to prefactor audit."),
        ("SRC2127_15_1479_counter", CSV_1479_COUNTER, ["CM1479_0_wA_action", "True"], "source-only prefactor countermodel ledger."),
        ("SRC2127_16_1895_object", CSV_1895_OBJECT, ["NSP1895_5_verdict", "NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED"], "object-language proof attempt."),
        ("SRC2127_17_1895_gate", CSV_1895_GATE, ["TYP1895_5_verdict", "NO_SOURCE_PREFACTOR_TYPING_CLAIM_BLOCKED"], "typing gate."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, expected_needles="; ".join(needles), needles_found=exists and all(needle in text for needle in needles), role=role))
    return rows


def identity_attempt_rows() -> list[dict[str, object]]:
    return [
        row(
            identity_id="IAS2127_0_target",
            claim="active source normalization equals inertial/matter normalization after one common measured-G quotient",
            proof_move="Use one parent action scale, one hbar/measure owner, one Hilbert source current, and variation-before-readout to make w_A source-only coefficients ill-typed.",
            current_result="TARGET_EXACT",
            obstruction="all owner clauses must be parent signed together",
            parent_signed=False,
        ),
        row(
            identity_id="IAS2127_1_hilbert_identity",
            claim="source current is the Hilbert/coframe derivative of the same matter action that defines inertial dynamics",
            proof_move="T_total := delta S_matter / delta e_obs before readout",
            current_result="EXACT_SUBTHEOREM_CONDITIONAL",
            obstruction="requires common S_matter and variation-before-readout as parent premises",
            parent_signed=False,
        ),
        row(
            identity_id="IAS2127_2_classical_rescale_obstruction",
            claim="classical equations alone remove species action scales",
            proof_move="Try to divide delta(w_A S_A)/delta Psi_A by w_A",
            current_result="FALSE_FOR_SOURCE",
            obstruction="delta(w_A S_A)/delta e_obs = w_A T_A, so Hilbert source still sees w_A",
            parent_signed=False,
        ),
        row(
            identity_id="IAS2127_3_measure_hbar_gap",
            claim="one parent quantum/statistical measure removes action-weight replicas",
            proof_move="Require exp(i sum_A S_A/hbar_parent) with species-blind measure/Jacobian",
            current_result="OWNER_NOT_DERIVED",
            obstruction="species-dependent hbar_A or measure factors can mimic source weights unless parent measure owner is signed",
            parent_signed=False,
        ),
        row(
            identity_id="IAS2127_4_current_readout_gap",
            claim="same owner fixes source current through readout/effective reductions",
            proof_move="Variation before readout plus no re-entry prevents J_A -> c_A J_A and non-Hilbert readout source drift",
            current_result="TRANSFER_UNSIGNED",
            obstruction="readout/radiative/current owner clauses remain open",
            parent_signed=False,
        ),
        row(
            identity_id="IAS2127_5_verdict",
            claim="inertial-active source identity is derived from current corpus",
            proof_move="Assemble 1676/1687/1899/1418/1479/1895 owner and typing rows",
            current_result="IDENTITY_NOT_PARENT_DERIVED_EXPLICIT_EP_CLOSURE_REQUIRED",
            obstruction="action-scale owner, measure/hbar owner, source-current owner, no-Hom source coefficient exclusion, and readout transfer are not jointly signed",
            parent_signed=False,
        ),
    ]


def obstruction_rows() -> list[dict[str, object]]:
    return [
        row(obstruction_id="OBS2127_0_wA_action", countermodel="S_matter=sum_A w_A S_A", why_survives="covariant/additive and may preserve isolated classical EOM while changing Hilbert source", source_anchor="COM1687_3_action_scale; CM1479_0_wA_action", retained=True),
        row(obstruction_id="OBS2127_1_kappaA_source", countermodel="F((T_A,A))=kappa_A T_A", why_survives="source functor can remain labelled unless label forgetting/no-Hom source target is signed", source_anchor="NSF953_3_additivity_limit; CM1479_1_kappaA_source", retained=True),
        row(obstruction_id="OBS2127_2_measure_hbar", countermodel="species-dependent hbar_A or measure Jacobian", why_survives="path-integral/statistical measure owner remains unsigned", source_anchor="COM1687_4_measure_hbar; ACL1418_2_hbar_measure_owner", retained=True),
        row(obstruction_id="OBS2127_3_current_rescaling", countermodel="J_A -> c_A J_A", why_survives="current/source normalization owner is missing", source_anchor="ACO1899_2_current_owner_clause; CM1479_3_current_rescaling", retained=True),
        row(obstruction_id="OBS2127_4_readout_nonHilbert", countermodel="J_src=T_Hilbert+sum_A zeta_A J_NH,A", why_survives="non-Hilbert/readout transfer closure remains unsigned", source_anchor="CM1479_4_nonHilbert_readout; ACL1418_5_readout_transfer", retained=True),
    ]


def ep_closure_rows() -> list[dict[str, object]]:
    return [
        row(
            closure_id="EPC2127_0_identity_clause",
            closure_clause="InertialActiveSourceIdentity",
            formal_clause="Coeff_active_source(A) = Coeff_inertial_matter(A) after one universal measured-G quotient; no independent source-only coefficient target exists.",
            status="EXPLICIT_EP_CLOSURE_IF_NOT_DERIVED",
            effect_if_adopted="forbids w_A source-only residuals and supports NoSourceOnlySpeciesSlot",
            scope_limit="does not prove EH operator selection, PPN second order, clock/light/readout transfer, or source-profile data",
        ),
        row(
            closure_id="EPC2127_1_common_quotient",
            closure_clause="MeasuredGCommonQuotient",
            formal_clause="one universal common factor may be absorbed into measured G_N/GM; all relative source weights remain forbidden or residual",
            status="GUARD_ALREADY_SUPPORTED",
            effect_if_adopted="prevents fitted-G hiding while allowing unit calibration",
            scope_limit="does not set finite non-Hilbert/readout residuals to zero",
        ),
        row(
            closure_id="EPC2127_2_private_status",
            closure_clause="closure is private/internal only",
            formal_clause="mark source-side GR bridge as closure_assumed unless a later parent theorem signs the identity",
            status="NO_PUBLIC_CLAIM",
            effect_if_adopted="lets future local branch bookkeeping separate closure debt from empirical residuals",
            scope_limit="no local-GR/Newton/PPN claim from this checkpoint",
        ),
    ]


def residual_route_rows() -> list[dict[str, object]]:
    return [
        row(route_id="RES2127_0_if_closure_adopted", route="source-side closure branch", required_next="carry closure flag into local residual ledger and continue EH/operator/readout gates", current_status="AVAILABLE_PRIVATE_CLOSURE_NOT_DERIVATION", score_ready=False),
        row(route_id="RES2127_1_if_closure_rejected", route="finite source-vector branch", required_next="source profile/worldtube vector, parent basis map, material tensor, readout kernel and residual coefficients", current_status="PROFILE_ACQUISITION_PACK_REQUIRED", score_ready=False),
        row(route_id="RES2127_2_parallel_empirical", route="MICROSCOPE/WEP empirical branch", required_next="official CMSM arrays and validated live-drop manifest", current_status="DATA_ROUTE_SEPARATE_NOT_THEOREM", score_ready=False),
        row(route_id="RES2127_3_remaining_gr", route="left-hand GR/Newton branch", required_next="EH/second-order PPN/operator-selection and readout response gates", current_status="STILL_SEPARATE_FROM_SOURCE_SIDE", score_ready=False),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2127_0_hilbert_identity_conditional", gate="Hilbert/inertial source identity conditional theorem", gate_pass=True, rationale="same matter action gives same source by functional derivative if common owner premises hold"),
        row(gate_id="GATE2127_1_parent_identity_derived", gate="identity parent-derived in current corpus", gate_pass=False, rationale="action-scale, hbar/measure, current owner and readout transfer remain unsigned"),
        row(gate_id="GATE2127_2_classical_rescale_rejected", gate="classical EOM rescale accepted as proof", gate_pass=False, rationale="Hilbert source still scales by w_A"),
        row(gate_id="GATE2127_3_EP_closure_ready", gate="explicit EP closure ready", gate_pass=True, rationale="minimal closure identity and measured-G quotient are written with scope guard"),
        row(gate_id="GATE2127_4_countermodels_retained", gate="all source-prefactor countermodels retained unless closure adopted", gate_pass=True, rationale="w_A, kappa_A, measure/hbar, current and non-Hilbert readout routes remain listed"),
        row(gate_id="GATE2127_5_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="identity is closure, not derivation, and left-hand/readout gates remain open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2127_0", decision="DEEPER_DERIVATION_NOT_CLOSED", because="the identity works only if common action/measure/current/readout ownership is already parent-signed", next_action="do not claim source-side GR as derived"),
        row(decision_id="DEC2127_1", decision="EP_CLOSURE_IS_MINIMAL_PRIVATE_OPTION", because="it forbids only source-only active coefficients while preserving ordinary matter constants", next_action="carry closure flag explicitly if used"),
        row(decision_id="DEC2127_2", decision="NEXT_LEDGER_SHOULD_SEPARATE_DEBTS", because="source-side closure debt is now distinct from EH/operator/readout/profile data debts", next_action="build remaining local-GR gate map with closure and no-closure branches"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2127_0_2128",
            next_target="2128-Y5-R2FR-source-side-EP-closure-ledger-and-remaining-local-GR-gates.md",
            script="scripts/Y5_R2FR_source_side_EP_closure_ledger_and_remaining_local_GR_gates_2128.py",
            objective="Separate the project state into two honest branches: source-side EP closure assumed vs no-closure finite source-vector acquisition. For the closure branch, map the remaining local-GR/Newton gates: EH/operator selection, PPN beta/gamma, clock/light/readout transfer, source profile, and empirical validation.",
            forbidden_shortcuts="treating EP closure as derivation; dropping countermodels; claiming local GR/Newton/PPN; ignoring EH/operator/readout gates; fitted-G hiding; bulk Earth as profile vector; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    identity: list[dict[str, object]],
    closure: list[dict[str, object]],
    residuals: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2127_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_EP_CLOSURE_2127_NONCLAIM.csv", identity + closure + residuals),
        ("COPY2127_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2127_EP_CLOSURE_STATUS_NONCLAIM.csv", identity + closure + residuals),
        ("COPY2127_2_acquisition_queue", QUEUE / "JR2127_EP_CLOSURE_OR_SOURCE_VECTOR_QUEUE.csv", next_rows + residuals),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    identity: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    closure: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    identity_ok = any(item["identity_id"] == "IAS2127_5_verdict" and item["current_result"] == "IDENTITY_NOT_PARENT_DERIVED_EXPLICIT_EP_CLOSURE_REQUIRED" for item in identity)
    obstructions_ok = len(obstructions) >= 5 and all(truthy(item["retained"]) for item in obstructions)
    closure_ok = any(item["closure_id"] == "EPC2127_0_identity_clause" and item["status"] == "EXPLICIT_EP_CLOSURE_IF_NOT_DERIVED" for item in closure)
    residuals_ok = any(item["route_id"] == "RES2127_0_if_closure_adopted" for item in residuals) and any(item["route_id"] == "RES2127_1_if_closure_rejected" for item in residuals)
    gates_ok = any(item["gate_id"] == "GATE2127_0_hilbert_identity_conditional" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2127_5_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2127_2" and item["decision"] == "NEXT_LEDGER_SHOULD_SEPARATE_DEBTS" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2127_0_2128" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, identity, obstructions, closure, residuals, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2127_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, identity_ok, obstructions_ok, closure_ok, residuals_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2127_00_sources", sources_ok, "all cited inertial/source owner rows exist and contain expected needles"),
        ("VAL2127_01_identity", identity_ok, "inertial-active source identity is exact conditional but not parent-derived"),
        ("VAL2127_02_obstructions", obstructions_ok, "source-prefactor countermodels remain retained"),
        ("VAL2127_03_closure", closure_ok, "explicit EP closure clause is ready with scope guard"),
        ("VAL2127_04_residual_routes", residuals_ok, "closure and no-closure residual routes are both staged"),
        ("VAL2127_05_gates", gates_ok, "Hilbert identity conditional gate passes while local claim gate fails"),
        ("VAL2127_06_decisions", decisions_ok, "decision ledger separates closure debt from remaining GR gates"),
        ("VAL2127_07_next", next_ok, "next target maps source-side closure and remaining local-GR gates"),
        ("VAL2127_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2127_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2127_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2127_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2127"),
        ("VAL2127_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2127_OVERALL", all_ok, "2127 tests the inertial-active-source identity, keeps it as explicit EP closure rather than derived theorem, and stages the remaining local-GR gate ledger."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    identity: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    closure: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2127 - Y5/R2FR Inertial-Active-Source Identity Or Explicit EP Closure",
            "## Current Verdict",
            "2127 tries the deepest source-side derivation available in the current corpus. The identity is exact as a conditional theorem: if inertial/matter normalization and active gravitational source normalization are the same parent-owned object after one measured-G quotient, then a source-only species slot cannot be formed.",
            "But the current corpus does not derive that identity. Classical action rescaling is the killer obstruction: `delta(w_A S_A)/delta Psi_A` can leave the matter equations looking unchanged, while `delta(w_A S_A)/delta e_obs = w_A T_A` still changes the Hilbert source. So the identity must either be parent-derived later from action-scale/measure/current/readout ownership, or carried as an explicit private equivalence-principle closure.",
            "No local-GR/Newton/PPN claim is made. This checkpoint separates the debts: source-side EP closure debt, finite source-vector acquisition if closure is rejected, and the still-separate EH/operator/readout gates.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Inertial-Active Source Identity Attempt",
            md_table(identity, ["identity_id", "claim", "proof_move", "current_result", "obstruction", "parent_signed", "valid_for_claim"]),
            "## Retained Obstructions",
            md_table(obstructions, ["obstruction_id", "countermodel", "why_survives", "source_anchor", "retained", "valid_for_claim"]),
            "## Explicit EP Closure",
            md_table(closure, ["closure_id", "closure_clause", "formal_clause", "status", "effect_if_adopted", "scope_limit", "valid_for_claim"]),
            "## Residual Routes",
            md_table(residuals, ["route_id", "route", "required_next", "current_status", "score_ready", "valid_for_claim"]),
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
    identity = identity_attempt_rows()
    obstructions = obstruction_rows()
    closure = ep_closure_rows()
    residuals = residual_route_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2127_SOURCE_REGISTER.csv",
        "identity": OUT / "P8_Y5_PARENT_QLOC_2127_INERTIAL_ACTIVE_SOURCE_IDENTITY_ATTEMPT.csv",
        "obstructions": OUT / "P8_Y5_PARENT_QLOC_2127_RETAINED_SOURCE_PREFACTOR_OBSTRUCTIONS.csv",
        "closure": OUT / "P8_Y5_PARENT_QLOC_2127_EXPLICIT_EP_CLOSURE.csv",
        "residuals": OUT / "P8_Y5_PARENT_QLOC_2127_RESIDUAL_ROUTE_LEDGER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2127_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2127_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2127_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2127_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2127_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["identity"], identity)
    write_csv(paths["obstructions"], obstructions)
    write_csv(paths["closure"], closure)
    write_csv(paths["residuals"], residuals)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(identity, closure, residuals, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, identity, obstructions, closure, residuals, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, identity, obstructions, closure, residuals, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
