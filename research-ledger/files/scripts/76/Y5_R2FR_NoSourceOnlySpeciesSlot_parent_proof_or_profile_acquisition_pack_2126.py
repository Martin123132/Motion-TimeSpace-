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


DOC = ROOT / "2126-Y5-R2FR-NoSourceOnlySpeciesSlot-parent-proof-or-profile-acquisition-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2125_NEXT = OUT / "P8_Y5_PARENT_QLOC_2125_NEXT_TARGET.csv"
CSV_2125_VAL = OUT / "P8_Y5_BRR545_2125_VALIDATION.csv"
CSV_2125_DESCENT = OUT / "P8_Y5_PARENT_QLOC_2125_COMMON_MODE_DESCENT_AUDIT.csv"
CSV_2125_PROFILE = OUT / "P8_Y5_PARENT_QLOC_2125_EARTH_PROFILE_BOUND_ROW.csv"
CSV_2125_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_2125_GM_ABSORPTION_REFUSAL.csv"
CSV_2125_GATES = OUT / "P8_Y5_PARENT_QLOC_2125_SOURCE_VECTOR_PROMOTION_GATES.csv"
CSV_1337_CONTRACT = OUT / "P8_Y5_R10_1337_MINIMAL_PARENT_ACTION_CONTRACT.csv"
CSV_1337_REDUCTION = OUT / "P8_Y5_R10_1337_COMMON_MODE_PREMISE_REDUCTION.csv"
CSV_1337_COUNTER = OUT / "P8_Y5_R10_1337_ADMISSIBLE_COUNTERMODEL_LEDGER.csv"
CSV_1963_ACTION = OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv"
CSV_1963_NO_GAMMA = OUT / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv"
CSV_1425_PROOF = OUT / "P8_Y5_R10_1425_COMMON_MODE_WEP_ZERO_PROOF_ATTEMPT.csv"
CSV_1424_CONTRACT = OUT / "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv"
CSV_1419_VECTOR = OUT / "P8_Y5_R10_1419_SOURCE_RESIDUAL_COEFFICIENT_VECTOR.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2126_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2126-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2126*",
        "*Y5_R2FR_NoSourceOnlySpeciesSlot_parent_proof_or_profile_acquisition_pack_2126*",
        "*AFRAME_NOSOURCE_SLOT_2126*",
        "*JR2126_NOSOURCE*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2126_00_2125_next", CSV_2125_NEXT, ["NEXT2125_0_2126", "NoSourceOnlySpeciesSlot-parent-proof"], "2125 handoff selects NoSourceOnlySpeciesSlot proof or profile acquisition."),
        ("SRC2126_01_2125_validation", CSV_2125_VAL, ["VAL2125_OVERALL", "PASS"], "2125 validation passed."),
        ("SRC2126_02_2125_descent", CSV_2125_DESCENT, ["CMD2125_1_minimal_missing_clause", "THEOREM_TARGET_SHARPENED_NOT_CLOSED"], "source-side route sharpened to NoSourceOnlySpeciesSlot."),
        ("SRC2126_03_2125_profile", CSV_2125_PROFILE, ["EPB2125_1_profile_weighted_target", "MISSING_PROFILE_WEIGHTING_FOR_CLAIM"], "profile/worldtube source vector remains missing."),
        ("SRC2126_04_2125_refusals", CSV_2125_REFUSAL, ["REF2125_1_measured_G_hiding", "REF2125_3_countermodel_ignored"], "shortcuts refused."),
        ("SRC2126_05_2125_gates", CSV_2125_GATES, ["GATE2125_1_no_source_slot_parent_signed", "False"], "NoSourceOnlySpeciesSlot not parent signed."),
        ("SRC2126_06_1337_contract", CSV_1337_CONTRACT, ["PACT1337_2_no_source_only_species_slot", "SHARPEST_REQUIRED_PARENT_PREMISE"], "minimal parent action contract clause."),
        ("SRC2126_07_1337_reduction", CSV_1337_REDUCTION, ["RED1337_3_no_source_only_species_slot", "SHARPEST_MISSING_PREMISE"], "premise reduction."),
        ("SRC2126_08_1337_counter", CSV_1337_COUNTER, ["CM1337_0_relative_source_weight", "LIVE_UNLESS_NO_SOURCE_SLOT_PARENT_SIGNED"], "countermodel ledger."),
        ("SRC2126_09_1963_action", CSV_1963_ACTION, ["ACT1963_4_matter_functor", "MATTER_FUNCTOR_SELECTED_NONCANONICAL"], "candidate owned-coframe matter functor."),
        ("SRC2126_10_1963_no_gamma", CSV_1963_NO_GAMMA, ["NGT1963_2_q_vertical_silence", "CONDITIONAL_CHAIN_RULE_ZERO"], "vertical silence chain rule."),
        ("SRC2126_11_1425_proof", CSV_1425_PROOF, ["CMZ1425_3_no_relative_prefactor", "NOT_DERIVED_CURRENT_CORPUS"], "common-mode WEP proof gap."),
        ("SRC2126_12_1424_contract", CSV_1424_CONTRACT, ["SRCMAP1424_0_R_source", "MISSING_SOURCE_VECTOR"], "finite source-vector contract."),
        ("SRC2126_13_1419_vector", CSV_1419_VECTOR, ["SRCV1419_5_verdict", "VECTOR_DECLARED_VALUES_MISSING"], "source residual vector missing."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, expected_needles="; ".join(needles), needles_found=exists and all(needle in text for needle in needles), role=role))
    return rows


def parent_language_audit_rows() -> list[dict[str, object]]:
    return [
        row(
            audit_id="OLA2126_0_observed_frame",
            clause="ordinary matter sees q-descended observed coframe",
            current_evidence="ACT1963_1_variable_list; ACT1963_4_matter_functor; NGT1963_2_q_vertical_silence",
            proof_effect="blocks representative-only vertical leakage into ordinary matter arguments",
            proof_status="CONDITIONAL_SUPPORTS_COMMON_MODE",
            missing_or_escape="q/e_obs ownership remains candidate-level, not canonical corpus-wide",
        ),
        row(
            audit_id="OLA2126_1_single_matter_functional",
            clause="ordinary matter is varied from one observed matter functor",
            current_evidence="PACT1337_1_single_matter_functional; ACT1963_4_matter_functor",
            proof_effect="gives one Hilbert/coframe derivative per chosen matter action",
            proof_status="SUPPORTS_BUT_DOES_NOT_FORBID_WA",
            missing_or_escape="sum_A w_A S_A is still a matter functional unless w_A is type-forbidden",
        ),
        row(
            audit_id="OLA2126_2_theta_A_slot",
            clause="species constants theta_A are allowed",
            current_evidence="ACT1963_4_matter_functor uses theta_A; PACT1337_2 permits internal representation constants but not active-source multipliers",
            proof_effect="masses, charges, spin reps and internal constants can differ without becoming source-only weights",
            proof_status="TYPE_SPLIT_REQUIRED_NOT_DERIVED",
            missing_or_escape="current corpus does not prove theta_A excludes an active-source multiplier",
        ),
        row(
            audit_id="OLA2126_3_no_source_slot",
            clause="Hom(SpeciesLabel,Coeff_active_source)=empty",
            current_evidence="PACT1337_2_no_source_only_species_slot; RED1337_3_no_source_only_species_slot",
            proof_effect="would kill relative source weights w_A and collapse source side to common mode",
            proof_status="EXPLICIT_CONTRACT_NOT_PARENT_DERIVED",
            missing_or_escape="needs parent object-language derivation or accepted closure",
        ),
        row(
            audit_id="OLA2126_4_countermodel",
            clause="relative active-source coefficient",
            current_evidence="CM1337_0_relative_source_weight; CMZ1425_3_no_relative_prefactor",
            proof_effect="shows covariance/additivity/quotient descent alone do not forbid w_A",
            proof_status="LIVE_COUNTERMODEL",
            missing_or_escape="only NoSourceOnlySpeciesSlot or finite source-vector bound controls it",
        ),
    ]


def proof_attempt_rows() -> list[dict[str, object]]:
    return [
        row(
            proof_id="NSP2126_0_target",
            statement="Prove the parent object language has no source-only species coefficient slot.",
            derivation_attempt="Use 1963 owned-coframe matter functor plus 1337 single-measure/source-scale contract to remove any independent active-source multiplier.",
            result="TARGET_SHARP",
            blocker_or_scope="proof must distinguish allowed theta_A constants from forbidden active-source multipliers",
            parent_signed=False,
        ),
        row(
            proof_id="NSP2126_1_success_condition",
            statement="If theta_A is typed as nongravitational/inertial/internal data only, and the source current is the Hilbert derivative after quotienting one universal normalization, then no w_A can be formed.",
            derivation_attempt="Object-language typing: SpeciesLabel -> theta_A is allowed; SpeciesLabel -> Coeff_active_source is absent.",
            result="EXACT_CONDITIONAL_THEOREM",
            blocker_or_scope="conditional on a type rule not yet derived from deeper MTS primitives",
            parent_signed=False,
        ),
        row(
            proof_id="NSP2126_2_failure_mode",
            statement="If theta_A may contain a source-only scalar w_A, then S_m=sum_A w_A S_A remains covariant and additive.",
            derivation_attempt="Countermodel from 1337 survives 1963 matter functor because w_A can be hidden as a constant unless the active-source slot is type-forbidden.",
            result="PROOF_FAILS_WITHOUT_TYPE_RULE",
            blocker_or_scope="NoSourceOnlySpeciesSlot cannot be inferred from covariance/additivity/descent alone",
            parent_signed=False,
        ),
        row(
            proof_id="NSP2126_3_no_field_redefinition_rescue",
            statement="A field/unit redefinition cannot be used as a proof unless it also preserves measured inertial normalization and removes the source coefficient from all source/readout products.",
            derivation_attempt="Relative source weights are exactly the residual left after one common normalization is calibrated into G_N/GM.",
            result="REDEFINITION_NOT_A_PROOF",
            blocker_or_scope="measured-G guard forbids hiding relative coefficients",
            parent_signed=False,
        ),
        row(
            proof_id="NSP2126_4_verdict",
            statement="NoSourceOnlySpeciesSlot is not derived from current parent rows; it is the minimal explicit closure needed for source-side GR, unless a deeper MTS object-language theorem is supplied.",
            derivation_attempt="Assemble 1963, 1337, 1425, 2125 evidence.",
            result="NOT_PARENT_DERIVED_DEMOTE_TO_EXPLICIT_CLOSURE_OR_NEXT_THEOREM",
            blocker_or_scope="parent object-language source slot still unsigned",
            parent_signed=False,
        ),
    ]


def explicit_closure_rows() -> list[dict[str, object]]:
    return [
        row(
            closure_id="CLS2126_0_minimal_clause",
            closure_clause="NoSourceOnlySpeciesSlot",
            formal_clause="Hom(SpeciesLabel,Coeff_active_source)=empty while Hom(SpeciesLabel,Theta_internal) may be nonempty",
            what_it_allows="masses, charges, spins, field representations, internal constants and ordinary material composition inside theta_A",
            what_it_forbids="a species/material label selecting an active gravitational source multiplier w_A independent of inertial/nongravitational normalization",
            status="EXPLICIT_CLOSURE_REQUIRED_IF_NOT_DERIVED",
            claim_allowed=False,
        ),
        row(
            closure_id="CLS2126_1_effect_if_adopted",
            closure_clause="source-side common mode",
            formal_clause="S_matter -> one Hilbert source current up to one universal measured-G normalization",
            what_it_allows="ordinary composition dependence in inertial/material response",
            what_it_forbids="relative active-source weights in WEP/R10/PPN source legs",
            status="WOULD_CLOSE_SOURCE_SIDE_ONLY_NOT_EH_OR_READOUT",
            claim_allowed=False,
        ),
        row(
            closure_id="CLS2126_2_not_enough",
            closure_clause="scope guard",
            formal_clause="NoSourceOnlySpeciesSlot does not prove EH, second-order PPN, readout silence, profile weighting, or CMSM data import",
            what_it_allows="continued local-GR derivation work",
            what_it_forbids="promoting this closure to full GR/Newton claim",
            status="SCOPE_LIMIT_EXPLICIT",
            claim_allowed=False,
        ),
    ]


def profile_acquisition_pack_rows() -> list[dict[str, object]]:
    return [
        row(
            pack_id="PACQ2126_0_source_profile",
            required_artifact="profile/worldtube-weighted Earth source vector",
            minimum_content="density/composition/profile weighting in observed/source frame with altitude/support convention",
            accepted_resolution="source-backed profile vector or theorem reducing source to common-mode point source with error bound",
            current_status="MISSING_PROFILE_WEIGHTING_FOR_CLAIM",
            valid_for_claim=False,
        ),
        row(
            pack_id="PACQ2126_1_parent_basis",
            required_artifact="MTS parent residual vector to source/material basis map",
            minimum_content="operator map from MTS parent coefficient/residual basis to DD/source/material response basis with units",
            accepted_resolution="parent-derived basis map or source-backed finite-prior operator ledger",
            current_status="MISSING_PARENT_OPERATOR_BASIS_MAP",
            valid_for_claim=False,
        ),
        row(
            pack_id="PACQ2126_2_material_tensor",
            required_artifact="full material response tensor",
            minimum_content="TA6V minus PtRh10 response in same source basis, sign convention, uncertainties",
            accepted_resolution="source-backed material tensor or parent theorem that material leg is common-mode",
            current_status="MISSING_FULL_TENSOR",
            valid_for_claim=False,
        ),
        row(
            pack_id="PACQ2126_3_readout_kernel",
            required_artifact="readout/orbit/mask kernel",
            minimum_content="official or validated CMSM gx/gz/Sxx/Sxz/masks/timing/attitude arrays and eta convention",
            accepted_resolution="complete live-drop validation from 2121/2122 workflow",
            current_status="OFFICIAL_ARRAYS_MISSING",
            valid_for_claim=False,
        ),
        row(
            pack_id="PACQ2126_4_no_shortcuts",
            required_artifact="anti-shortcut manifest",
            minimum_content="refuse bulk-as-profile, fitted-G relative absorption, tau=1, cancellation, surrogate templates",
            accepted_resolution="manifest plus validator dry-run refusal rows",
            current_status="RULES_WRITTEN_NONCLAIM",
            valid_for_claim=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2126_0_conditional_theorem", gate="conditional NoSourceOnlySpeciesSlot theorem stated", gate_pass=True, rationale="if active-source slot is absent by type, relative source weights cannot be formed"),
        row(gate_id="GATE2126_1_parent_derivation", gate="NoSourceOnlySpeciesSlot derived from existing parent action", gate_pass=False, rationale="current 1963/1337 rows require the type rule; they do not derive it"),
        row(gate_id="GATE2126_2_countermodel_retained", gate="relative source-weight countermodel retained", gate_pass=True, rationale="S_m=sum_A(1+epsilon_A)S_A survives unless source-only slot is forbidden"),
        row(gate_id="GATE2126_3_closure_ready", gate="explicit closure clause ready if user chooses closure route", gate_pass=True, rationale="minimal clause and scope guard are written"),
        row(gate_id="GATE2126_4_profile_pack_ready", gate="fallback profile acquisition pack ready", gate_pass=True, rationale="required source/profile/basis/material/readout artifacts are listed"),
        row(gate_id="GATE2126_5_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="source-side closure/proof remains unsigned and readout/EH gates remain separate"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2126_0", decision="PROOF_ATTEMPT_FAILED_AS_PARENT_DERIVATION", because="covariance/additivity/descent do not forbid a source-only constant unless the parent language types it out", next_action="try a deeper inertial-active-source identity or adopt explicit closure"),
        row(decision_id="DEC2126_1", decision="CLOSURE_IS_MINIMAL_IF_USED", because="NoSourceOnlySpeciesSlot forbids only active source multipliers, not ordinary masses/charges/spins", next_action="keep as explicit private closure, not public claim"),
        row(decision_id="DEC2126_2", decision="PROFILE_PACK_STAGED", because="fallback data route needs profile/worldtube and basis/readout artifacts, not bulk Earth context alone", next_action="use only if theorem route stalls"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2126_0_2127",
            next_target="2127-Y5-R2FR-inertial-active-source-identity-or-explicit-EP-closure.md",
            script="scripts/Y5_R2FR_inertial_active_source_identity_or_explicit_EP_closure_2127.py",
            objective="Try one deeper derivation: prove active gravitational source normalization is identical to inertial/matter normalization after one common measured-G quotient, so a source-only species slot cannot be formed. If that fails, retain NoSourceOnlySpeciesSlot as an explicit equivalence-principle closure and keep profile acquisition as fallback.",
            forbidden_shortcuts="assuming equivalence principle as proof; hiding relative weights in fitted G; treating closure as derivation; bulk Earth as profile vector; cancellation; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    proof: list[dict[str, object]],
    closure: list[dict[str, object]],
    pack: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2126_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_NOSOURCE_SLOT_2126_NONCLAIM.csv", proof + closure + pack),
        ("COPY2126_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2126_NOSOURCE_SLOT_STATUS_NONCLAIM.csv", proof + closure + pack),
        ("COPY2126_2_acquisition_queue", QUEUE / "JR2126_NOSOURCE_SLOT_OR_PROFILE_ACQUISITION_QUEUE.csv", next_rows + pack),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    proof: list[dict[str, object]],
    closure: list[dict[str, object]],
    pack: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    audit_ok = any(item["audit_id"] == "OLA2126_3_no_source_slot" and item["proof_status"] == "EXPLICIT_CONTRACT_NOT_PARENT_DERIVED" for item in audit) and any(item["audit_id"] == "OLA2126_4_countermodel" and item["proof_status"] == "LIVE_COUNTERMODEL" for item in audit)
    proof_ok = any(item["proof_id"] == "NSP2126_4_verdict" and item["result"] == "NOT_PARENT_DERIVED_DEMOTE_TO_EXPLICIT_CLOSURE_OR_NEXT_THEOREM" for item in proof)
    closure_ok = any(item["closure_id"] == "CLS2126_0_minimal_clause" and item["status"] == "EXPLICIT_CLOSURE_REQUIRED_IF_NOT_DERIVED" for item in closure)
    pack_ok = len(pack) >= 5 and all(not truthy(item.get("valid_for_claim", False)) for item in pack)
    gates_ok = any(item["gate_id"] == "GATE2126_0_conditional_theorem" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2126_5_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2126_0" and item["decision"] == "PROOF_ATTEMPT_FAILED_AS_PARENT_DERIVATION" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2126_0_2127" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, audit, proof, closure, pack, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2126_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, audit_ok, proof_ok, closure_ok, pack_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2126_00_sources", sources_ok, "all cited NoSource/profile rows exist and contain expected needles"),
        ("VAL2126_01_audit", audit_ok, "object-language audit keeps NoSourceOnlySpeciesSlot unsigned and countermodel live"),
        ("VAL2126_02_proof", proof_ok, "proof attempt fails as parent derivation but records exact conditional theorem"),
        ("VAL2126_03_closure", closure_ok, "minimal explicit closure clause is written with scope guard"),
        ("VAL2126_04_pack", pack_ok, "profile acquisition pack is complete and nonclaim"),
        ("VAL2126_05_gates", gates_ok, "conditional theorem gate passes while local-GR/Newton/PPN claim fails"),
        ("VAL2126_06_decisions", decisions_ok, "decision ledger records failed derivation and next theorem route"),
        ("VAL2126_07_next", next_ok, "next target selects inertial-active-source identity or explicit EP closure"),
        ("VAL2126_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2126_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2126_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2126_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2126"),
        ("VAL2126_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2126_OVERALL", all_ok, "2126 attempts NoSourceOnlySpeciesSlot, finds it not parent-derived yet, writes the minimal closure and fallback profile acquisition pack."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    proof: list[dict[str, object]],
    closure: list[dict[str, object]],
    pack: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2126 - Y5/R2FR NoSourceOnlySpeciesSlot Parent Proof Or Profile Acquisition Pack",
            "## Current Verdict",
            "2126 tries the clean theorem route and keeps the result honest. The conditional theorem is exact: if the parent object language has no active-source species slot, then relative source weights cannot be formed and the ordinary matter source collapses to one calibrated common mode. But the current corpus does not derive that type rule from deeper MTS primitives.",
            "The countermodel survives: `S_m=sum_A(1+epsilon_A)S_A` is still covariant/additive unless the source-only coefficient is explicitly forbidden. So `NoSourceOnlySpeciesSlot` is not yet a derived theorem; it is the minimal closure clause or the next theorem target. The fallback data route is also staged, but remains nonclaim because profile/worldtube source weighting, parent basis map, material tensor and official readout kernel are missing.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Parent Object-Language Audit",
            md_table(audit, ["audit_id", "clause", "proof_status", "proof_effect", "missing_or_escape", "valid_for_claim"]),
            "## Proof Attempt",
            md_table(proof, ["proof_id", "statement", "derivation_attempt", "result", "blocker_or_scope", "parent_signed", "valid_for_claim"]),
            "## Explicit Closure Clause",
            md_table(closure, ["closure_id", "closure_clause", "formal_clause", "what_it_allows", "what_it_forbids", "status", "claim_allowed"]),
            "## Profile Acquisition Pack",
            md_table(pack, ["pack_id", "required_artifact", "minimum_content", "accepted_resolution", "current_status", "valid_for_claim"]),
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
    audit = parent_language_audit_rows()
    proof = proof_attempt_rows()
    closure = explicit_closure_rows()
    pack = profile_acquisition_pack_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2126_SOURCE_REGISTER.csv",
        "audit": OUT / "P8_Y5_PARENT_QLOC_2126_PARENT_OBJECT_LANGUAGE_AUDIT.csv",
        "proof": OUT / "P8_Y5_PARENT_QLOC_2126_NOSOURCE_SLOT_PROOF_ATTEMPT.csv",
        "closure": OUT / "P8_Y5_PARENT_QLOC_2126_EXPLICIT_CLOSURE_CLAUSE.csv",
        "pack": OUT / "P8_Y5_PARENT_QLOC_2126_PROFILE_ACQUISITION_PACK.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2126_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2126_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2126_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2126_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2126_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["audit"], audit)
    write_csv(paths["proof"], proof)
    write_csv(paths["closure"], closure)
    write_csv(paths["pack"], pack)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(proof, closure, pack, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, audit, proof, closure, pack, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, audit, proof, closure, pack, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
