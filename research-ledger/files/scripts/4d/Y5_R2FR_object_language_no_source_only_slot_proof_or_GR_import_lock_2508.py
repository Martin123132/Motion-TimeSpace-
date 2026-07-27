from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_OBJECT_LANGUAGE_NO_SOURCE_ONLY_SLOT_2508"
CHECKPOINT_ID = "2508"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"

DOC = ROOT / "2508-Y5-R2FR-object-language-no-source-only-slot-proof-or-GR-import-lock.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2508_SOURCE_REGISTER.csv",
    "proof_attempt": OUT / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv",
    "theorem_gates": OUT / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_SLOT_THEOREM_GATES.csv",
    "countermodels": OUT / "P8_Y5_NO_SHADOW_2508_SOURCE_ONLY_COUNTERMODELS.csv",
    "residual_rows": OUT / "P8_Y5_NO_SHADOW_2508_SOURCE_WEIGHT_RESIDUAL_ROWS.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2508_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2508_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2508_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2508_VALIDATION.csv",
}

BRANCH_COPIES = {
    "proof_attempt": LOCAL_BOUNDS / "No_source_only_slot_proof_attempt_2508_NONCLAIM.csv",
    "theorem_gates": LOCAL_BOUNDS / "No_source_slot_theorem_gates_2508_NONCLAIM.csv",
    "residual_rows": QUEUE / "JR2508_SOURCE_WEIGHT_RESIDUAL_ROWS_NONCLAIM.csv",
    "next_target": QUEUE / "JR2508_CONSTRUCTOR_EXHAUSTION_NEXT.csv",
    "decision_ledger": BETA_DOCS / "No_source_only_slot_decision_2508_NONCLAIM.csv",
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
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def source_register_rows() -> list[dict[str, Any]]:
    residuals = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
    specs = [
        (
            "SRC2508_00_2507_handoff",
            ROOT / "2507-Y5-R2FR-parent-signature-synthesis-quotient-source-glue-or-GR-import-lock.md",
            ["NEXT2507_0_selected", "OBJECT_LANGUAGE_NO_SOURCE_ONLY_SLOT_NEXT", "VAL2507_OVERALL"],
            "2507 selects the no-source-only object-language proof as the next route.",
        ),
        (
            "SRC2508_01_2507_validation",
            OUT / "P8_Y5_BRR545_2507_VALIDATION.csv",
            ["VAL2507_OVERALL", "PASS"],
            "2507 validation passed before 2508 continues the chain.",
        ),
        (
            "SRC2508_02_1695_no_slot",
            ROOT / "1695-Y5-R2FR-no-source-only-slot-theorem-or-tau-WEP-projection-current-branch.md",
            ["NO_SOURCE_ONLY_SLOT_NOT_DERIVED_TAU_ROUTE_RETAINED", "S_matter=sum_A w_A S_A", "VAL1695_OVERALL"],
            "1695 gives the clean no-source-only-slot theorem and says it is exact only if parent grammar is signed.",
        ),
        (
            "SRC2508_03_owner_grammar",
            residuals / "R2FR_parent_source_owner_grammar_1699.csv",
            ["G1699_4_forbidden_target", "G1699_8_verdict", "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED"],
            "1699 compresses the desired source-owner grammar into explicit allowed/forbidden objects.",
        ),
        (
            "SRC2508_04_owner_derivation_test",
            residuals / "R2FR_owner_axiom_derivation_test_1698.csv",
            ["DER1698_0_domain_exhaustion", "DER1698_6_result", "blocked_no_claim"],
            "1698 tests whether owner axioms have been derived and keeps them blocked.",
        ),
        (
            "SRC2508_05_action_measure_gate",
            residuals / "R2FR_action_measure_owner_proof_gate_1694.csv",
            ["OWG1694_0_countermodel", "COUNTERMODEL_SURVIVES", "OWG1694_7_verdict"],
            "1694 shows pre-variation source/action weights survive covariance and classical EOM shortcuts.",
        ),
        (
            "SRC2508_06_parent_label_quotient",
            residuals / "R2FR_parent_label_quotient_clause_audit_1686.csv",
            ["PLQ1686_0_exact_clause", "PROOF_NOT_CLOSED", "w_A S_A"],
            "1686 has the exact label-quotient clause but not a parent proof.",
        ),
        (
            "SRC2508_07_typing_audit",
            residuals / "P8_Y5_PARENT_QLOC_1887_OBJECT_LANGUAGE_TYPING_PROOF_AUDIT.csv",
            ["OLT1887_1_exact_conditional_certificate", "OBJECT_LANGUAGE_TYPING_NOT_PARENT_DERIVED", "OLT1887_3_direct_sum_counterexample"],
            "1887 gives the typed object-language proof and says it is not parent-derived.",
        ),
        (
            "SRC2508_08_nohom_attempt",
            residuals / "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv",
            ["NH1896_1_conditional_typed_proof", "PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED", "NH1896_3_counterexamples"],
            "1896 isolates the no-Hom theorem and keeps counterexamples retained.",
        ),
        (
            "SRC2508_09_parent_grammar",
            residuals / "P8_Y5_PARENT_QLOC_1903_NO_SOURCE_ONLY_SLOT_PARENT_GRAMMAR_ATTEMPT.csv",
            ["NSG1903_1_inside_typed_grammar", "NO_SOURCE_ONLY_SLOT_PARENT_GRAMMAR_NOT_DERIVED", "NSG1903_4_countermodel"],
            "1903 repeats the parent grammar route and leaves constructor exhaustion unsigned.",
        ),
        (
            "SRC2508_10_action_scale_readout",
            residuals / "P8_Y5_PARENT_QLOC_1897_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv",
            ["ASR1897_1_exact_conditional_theorem", "ACTION_SCALE_READOUT_STABILITY_NOT_PARENT_DERIVED"],
            "1897 shows tree-level no-slot would still need action-scale/readout stability.",
        ),
        (
            "SRC2508_11_readout_commutator",
            residuals / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
            ["RVC1898_1_pure_postprocessing_zero", "PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED"],
            "1898 separates safe pure postprocessing from projector/EFT/source-worldtube reentry.",
        ),
        (
            "SRC2508_12_object_packet",
            residuals / "R2FR_object_language_packet_nonclaim_1666.csv",
            ["OLP1666_4_matter_descent", "MATTER_DESCENT_NOT_SIGNED", "OBJECT_LANGUAGE_PACKET_CONTRACT_ONLY"],
            "1666 says the object-language packet is a contract, not a parent signature.",
        ),
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
                source_pass=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def proof_attempt_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NSP2508_0_target",
            "NoSourceOnlySpeciesSlot target",
            "Allowed[S_matter] has no independent w_A S_A, kappa_A T_A, hidden label marker, or source-only material multiplier before variation.",
            "TARGET_SHARP",
            "If signed, relative source weights vanish after common calibration.",
            "not_signed",
        ),
        (
            "NSP2508_1_inside_typed_grammar",
            "typed grammar theorem",
            "If parent sorts are derived/disjoint and Arg(Coeff_active_source) excludes SpeciesLabel, then w_A/kappa_A cannot be formed as parent terms.",
            "EXACT_CONDITIONAL_THEOREM",
            "This is syntax/category proof, not dynamics or small coupling.",
            "conditional_only",
        ),
        (
            "NSP2508_2_nohom",
            "no-Hom source coefficient theorem",
            "Hom_parent(SpeciesLabel,Coeff_active_source)=empty and Hom_parent(HiddenMarker,Coeff_active_source)=empty before readout.",
            "EXACT_IF_PARENT_SORTS_SIGNED",
            "Would make source-only coefficients untypeable rather than tuned to zero.",
            "not_parent_signed",
        ),
        (
            "NSP2508_3_constructor_exhaustion",
            "parent constructor exhaustion",
            "Every source-relevant coefficient must be in Image(ParentGenerate[q(Phi),theta_rep,universal_constants]).",
            "CONSTRUCTOR_EXHAUSTION_NOT_DERIVED",
            "The chain-rule/no-Hom proof works only after membership in this image is derived.",
            "core_gap",
        ),
        (
            "NSP2508_4_action_scale",
            "single action-scale/measure owner",
            "One parent action measure/hbar/current normalization covers ordinary matter; species-indexed action multipliers are not independent.",
            "ACTION_SCALE_MEASURE_OWNER_UNSIGNED",
            "Classical field equations can hide w_A while Hilbert source and path weight still change.",
            "core_gap",
        ),
        (
            "NSP2508_5_readout_reentry",
            "readout/effective no-reentry",
            "Post-variation readout, source-worldtube, EFT, clock/orbit and projector maps preserve the same coefficient domain.",
            "GENERAL_READOUT_COMMUTATOR_NOT_DERIVED",
            "Pure postprocessing is safe, but projector/source-worldtube/effective-action maps can still reintroduce source coefficients.",
            "core_gap",
        ),
        (
            "NSP2508_6_counterexample",
            "surviving legal countermodel",
            "S_matter=sum_A w_A S_A is covariant/additive and can preserve isolated classical equations while changing T_source=sum_A w_A T_A.",
            "COUNTERMODEL_SURVIVES",
            "This is the seam a real parent grammar must forbid, not a small parameter to ignore.",
            "live_obstruction",
        ),
        (
            "NSP2508_7_verdict",
            "2508 no-source-slot verdict",
            "Current MTS evidence does not derive the no-source-only slot theorem from primitives without a closure grammar.",
            "NO_SOURCE_ONLY_SLOT_PROOF_NOT_PARENT_DERIVED",
            "Do not keep repeating this theorem unless a deeper constructor-exhaustion premise is supplied.",
            "claim_blocked",
        ),
    ]
    return [
        base_row(
            proof_id=proof_id,
            claim_piece=claim_piece,
            formal_statement=formal_statement,
            result=result,
            implication=implication,
            live_status=live_status,
        )
        for proof_id, claim_piece, formal_statement, result, implication, live_status in specs
    ]


def theorem_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2508_0_parent_sorts", "parent sorts derived/disjoint", "Q_obs, SpeciesLabel, Coeff_active_source, Readout and HiddenMarker sorts have parent-derived non-overlapping constructors.", "FAIL_SCHEMA_WRITTEN_NOT_DERIVED", "syntax-by-decree is closure"),
        ("GATE2508_1_nohom", "no Hom into active source coefficient", "Hom(SpeciesLabel,Coeff_active_source)=empty except one universal constant calibration mode.", "FAIL_NOHOM_NOT_PARENT_DERIVED", "w_A/kappa_A still legal if Hom exists"),
        ("GATE2508_2_constructor_exhaustion", "parent generated coefficient image exhaustive", "Coeff_active_source subset Image(ParentGenerate[q(Phi),theta_rep,universal_constants,retained_residuals]).", "FAIL_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED", "hidden/source-only coefficients can be appended"),
        ("GATE2508_3_action_scale", "single action-scale and measure owner", "No species-indexed hbar, measure, current or action-density line exists.", "FAIL_ACTION_SCALE_OWNER_UNSIGNED", "relative action weights can hide before variation"),
        ("GATE2508_4_variation_order", "variation before readout/projection", "Hilbert/Noether source is produced before material/readout/orbit/projector maps.", "FAIL_GENERAL_READOUT_ORDER_UNSIGNED", "post-variation source labels can re-enter"),
        ("GATE2508_5_no_marker_reentry", "no hidden marker/domain/boundary reentry", "Hidden scalar, domain, boundary, material and frame markers cannot target source coefficient slots.", "FAIL_NO_MARKER_REENTRY_NOT_PROVED", "source-only coefficient returns under another name"),
        ("GATE2508_6_theorem", "NoSourceOnlySpeciesSlot live claim", "GATE2508_0 through GATE2508_5 all pass.", "CLAIM_BLOCKED", "keep source-weight residual rows and GR-import lock"),
    ]
    return [
        base_row(
            gate_id=gate_id,
            required_clause=clause,
            formal_condition=formal_condition,
            current_status=status,
            if_fail=if_fail,
            gate_pass=False,
        )
        for gate_id, clause, formal_condition, status, if_fail in specs
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    specs = [
        ("CM2508_0_wA_action", "S_matter=sum_A w_A S_A", "changes Hilbert source and path weight while covariance/additivity/classical-looking equations can survive", "single action measure plus no source-only slot"),
        ("CM2508_1_kappaA_source", "F_grav((T_A,A))=kappa_A T_A", "keeps source labels alive after quotient unless label forgetting is parent-signed before coupling", "parent label quotient before source coupling"),
        ("CM2508_2_direct_sum", "direct-sum ordinary sectors carry independent constants c_A", "connectedness/naturality is not enough if the parent category has disconnected source-normalization components", "connected source category or forbidden component characters"),
        ("CM2508_3_hidden_marker", "hidden scalar/domain/boundary marker feeds Coeff_active_source", "a surviving invariant can target source coefficients unless no-hidden-visible Hom is signed", "no-marker/no-Hom theorem plus readout stability"),
        ("CM2508_4_readout_projector", "delta(Pi J)=Pi delta J +(delta Pi)J", "source-worldtube/material/projector maps can create finite source residuals after variation", "readout-variation commutator zero or residual rows"),
        ("CM2508_5_action_scale", "species-indexed hbar/measure/current normalization", "relative action weights can hide in the path measure rather than in classical equations", "one action-scale/hbar/measure owner"),
    ]
    return [
        base_row(countermodel_id=countermodel_id, countermodel=countermodel, why_survives=why, required_kill_clause=kill_clause)
        for countermodel_id, countermodel, why, kill_clause in specs
    ]


def residual_rows() -> list[dict[str, Any]]:
    specs = [
        ("RSW2508_0", "epsilon_wA_source_weight", "relative source/action weights w_A before variation", "MISSING_NO_SOURCE_ONLY_SLOT_THEOREM", "WEP;Newton;PPN;R10;clock", "core_blocker"),
        ("RSW2508_1", "epsilon_kappaA_source", "labelled source-coupling coefficients kappa_A", "MISSING_PARENT_LABEL_QUOTIENT", "WEP;Newton;PPN", "core_blocker"),
        ("RSW2508_2", "epsilon_noHom", "failure of Hom(SpeciesLabel,Coeff_active_source)=empty", "MISSING_PARENT_SORT_DISJOINTNESS_NOHOM", "WEP;R10;clock", "core_blocker"),
        ("RSW2508_3", "epsilon_action_scale", "species-indexed action measure/hbar/current normalization", "MISSING_SINGLE_ACTION_SCALE_OWNER", "WEP;clock;particle", "core_blocker"),
        ("RSW2508_4", "epsilon_readout_reentry", "source coefficient reentry through readout/projector/EFT maps", "MISSING_READOUT_VARIATION_COMMUTATOR_ZERO", "WEP;PPN;orbital;clock", "finite_residual_until_mapped"),
        ("RSW2508_5", "epsilon_hidden_marker", "hidden/domain/boundary/material marker targets active source coefficients", "MISSING_NO_MARKER_REENTRY_THEOREM", "R10;WEP;PPN", "core_blocker"),
        ("RSW2508_6", "local_branch_label", "local EH coefficients used before source-only weights are forbidden", "GR_IMPORT_PLUS_SOURCE_WEIGHT_RESIDUAL_INTERFACE", "all_local_tests", "honest_current_label"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            current_value=value,
            observable_link=observable,
            blocker_class=blocker,
            score_ready=False,
            source_path=str(DOC),
        )
        for row_id, symbol, definition, value, observable, blocker in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2508_0_exact_theorem", "CONDITIONAL_NO_SOURCE_SLOT_THEOREM_IS_CLEAN", "Inside a parent-derived typed grammar with no Hom into active source coefficients, w_A/kappa_A are unformable.", "selected"),
        ("DEC2508_1_live_status", "NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED", "Current evidence still supplies contracts and conditional lemmas, not a derivation from MTS primitives.", "selected"),
        ("DEC2508_2_loop_guard", "STOP_REPEATING_NO_SLOT_UNLESS_CONSTRUCTOR_EXHAUSTION_NEW", "1695, 1886, 1887, 1895 and 1903 already tested this route; repeating it without a deeper constructor principle is wheel-spinning.", "selected"),
        ("DEC2508_3_next", "PARENT_CONSTRUCTOR_EXHAUSTION_OR_RESIDUAL_PIVOT_NEXT", "The only derivation-first move left is to derive the parent constructor image from MTS primitives; otherwise pivot to finite source-weight residual bounds.", "selected"),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2508_0_selected",
            selection_status="selected",
            target_file="2509-Y5-R2FR-parent-constructor-exhaustion-from-MTS-primitives-or-source-weight-residual-pivot.md",
            target_script="scripts/Y5_R2FR_parent_constructor_exhaustion_from_MTS_primitives_or_source_weight_residual_pivot_2509.py",
            objective="derive the allowed parent coefficient constructors directly from MTS primitives so Coeff_active_source has no species/source-only target; if this cannot be done, stop the no-source-slot proof loop and build the finite source-weight residual bound interface",
            success_condition="a non-closure constructor theorem derives Image(ParentGenerate) and excludes w_A/kappa_A/hidden source markers before variation, including action-scale and readout stability",
            do_not_do="do not repeat 1695/1886/1895/1903 as a new proof, do not assume universal coupling, do not absorb relative weights into measured G, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2508_1_parallel_bounds",
            selection_status="held_parallel",
            target_file="2509b-Y5-R2FR-source-weight-residual-bound-pack-WEP-R10-PPN-clock.md",
            target_script="scripts/Y5_R2FR_source_weight_residual_bound_pack_WEP_R10_PPN_clock_2509b.py",
            objective="turn surviving w_A/kappa_A/no-Hom/action-scale/readout residuals into bound-ready rows for WEP, R10, PPN, clocks and orbital systems",
            success_condition="each residual has units, projection, source path and valid_for_claim=false until numeric source-backed rows exist",
            do_not_do="do not score placeholders or call empirical survival a derivation",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("proof_attempt", OUTPUTS["proof_attempt"], BRANCH_COPIES["proof_attempt"]),
        ("theorem_gates", OUTPUTS["theorem_gates"], BRANCH_COPIES["theorem_gates"]),
        ("residual_rows", OUTPUTS["residual_rows"], BRANCH_COPIES["residual_rows"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
        ("decision_ledger", OUTPUTS["decision_ledger"], BRANCH_COPIES["decision_ledger"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=f"COPY2508_{copy_id}", source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        validations.append(base_row(check_id=check_id, status="PASS" if status else "FAIL", notes=notes, detail=detail))

    add("VAL2508_00_sources_exist", all(row["path_exists"] for row in rows_by_name["source_register"]), "all cited source paths exist")
    add("VAL2508_01_source_needles", all(row["source_pass"] for row in rows_by_name["source_register"]), "all required source needles are present")

    proof_results = {row["result"] for row in rows_by_name["proof_attempt"]}
    add(
        "VAL2508_02_proof_verdict",
        "NO_SOURCE_ONLY_SLOT_PROOF_NOT_PARENT_DERIVED" in proof_results and "EXACT_CONDITIONAL_THEOREM" in proof_results,
        "conditional theorem and live failure both represented",
    )

    gate_statuses = {row["current_status"] for row in rows_by_name["theorem_gates"]}
    add(
        "VAL2508_03_theorem_gates",
        "CLAIM_BLOCKED" in gate_statuses and "FAIL_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED" in gate_statuses,
        "theorem gates block no-source-slot promotion",
    )

    add(
        "VAL2508_04_countermodels",
        len(rows_by_name["countermodels"]) >= 5 and any("w_A" in row["countermodel"] for row in rows_by_name["countermodels"]),
        "countermodel ledger keeps source-action weight seam visible",
    )

    residual_values = {row["current_value"] for row in rows_by_name["residual_rows"]}
    add(
        "VAL2508_05_residual_rows",
        "MISSING_NO_SOURCE_ONLY_SLOT_THEOREM" in residual_values and "GR_IMPORT_PLUS_SOURCE_WEIGHT_RESIDUAL_INTERFACE" in residual_values,
        "residual interface keeps local branch nonclaim",
    )

    decision_text = " ".join(row["decision"] for row in rows_by_name["decision_ledger"])
    add("VAL2508_06_loop_guard", "STOP_REPEATING_NO_SLOT_UNLESS_CONSTRUCTOR_EXHAUSTION_NEW" in decision_text, "loop guard prevents repeated same-theorem checkpoints")
    add("VAL2508_07_next_target", any(row["route_id"] == "NEXT2508_0_selected" for row in rows_by_name["next_target"]), "2509 constructor-exhaustion target selected")
    add("VAL2508_08_no_claim_flags", no_claim_flags(rows_by_name), "all generated rows keep valid_for_claim=false and claim_allowed=false")
    add("VAL2508_09_branch_copies", all(row["copied"] for row in rows_by_name["branch_copies"]), "branch copies were written")

    formalization_artifacts: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*2508*", "*P8_Y5_NO_SHADOW_2508*", "*JR2508*"):
            formalization_artifacts.extend(path for path in FORMALIZATION.rglob(pattern) if path.is_file())
    add("VAL2508_10_no_formalization_artifacts", not formalization_artifacts, "no 2508 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for path in OUTPUTS.values():
        if path == OUTPUTS["validation"]:
            continue
        parsed, count, detail = csv_rows_parse(path)
        add(f"VAL2508_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", detail)

    for key, path in BRANCH_COPIES.items():
        parsed, count, detail = csv_rows_parse(path)
        add(f"VAL2508_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", detail)

    remove_pycache()
    add("VAL2508_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts pycache removed")

    overall = all(row["status"] == "PASS" for row in validations)
    add(
        "VAL2508_OVERALL",
        overall,
        "2508 proves no-source-slot only conditionally, keeps source-weight residuals live, and selects constructor exhaustion or residual pivot next",
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2508 Y5 R2FR Object Language No Source Only Slot Proof Or GR Import Lock

## Current Verdict

2508 tried the coupling loophole directly.

The theorem is clean inside a typed parent grammar:

`Hom_parent(SpeciesLabel, Coeff_active_source)=empty`

and

`Arg(Coeff_active_source) subset Q_obs x theta_rep x UniversalCalibration x RetainedResidual`.

If that grammar is parent-derived, `w_A S_A`, `kappa_A T_A`, hidden source markers and source-only material multipliers cannot even be written before variation. That would be a serious route to MTS-owned source universality.

But the live corpus still does not derive the grammar from MTS primitives. The old countermodel survives:

`S_matter = sum_A w_A S_A`.

It is covariant/additive and can preserve isolated classical-looking equations while changing:

`T_source = sum_A w_A T_A`.

So the no-source-only-slot theorem remains exact but conditional. Local GR remains **GR/EH import plus source-weight residual interface** until a deeper constructor-exhaustion theorem is proved.

2508 therefore adds a loop guard: do not repeat the same no-source-slot theorem again unless the next checkpoint derives the parent constructor image from MTS primitives. Otherwise pivot to finite residual bounds.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "source_pass", "role", "valid_for_claim"])}

## No Source Only Slot Proof Attempt

{md_table(rows_by_name["proof_attempt"], ["proof_id", "claim_piece", "formal_statement", "result", "implication", "live_status", "valid_for_claim"])}

## Theorem Gates

{md_table(rows_by_name["theorem_gates"], ["gate_id", "required_clause", "formal_condition", "current_status", "if_fail", "gate_pass", "valid_for_claim"])}

## Surviving Countermodels

{md_table(rows_by_name["countermodels"], ["countermodel_id", "countermodel", "why_survives", "required_kill_clause", "valid_for_claim"])}

## Source Weight Residual Rows

{md_table(rows_by_name["residual_rows"], ["row_id", "symbol", "definition", "current_value", "observable_link", "blocker_class", "score_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["check_id", "status", "notes", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "proof_attempt": proof_attempt_rows(),
        "theorem_gates": theorem_gate_rows(),
        "countermodels": countermodel_rows(),
        "residual_rows": residual_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
