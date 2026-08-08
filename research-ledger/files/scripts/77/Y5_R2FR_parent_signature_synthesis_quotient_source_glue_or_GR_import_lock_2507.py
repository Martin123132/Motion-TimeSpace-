from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_SIGNATURE_SYNTHESIS_2507"
CHECKPOINT_ID = "2507"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"

DOC = ROOT / "2507-Y5-R2FR-parent-signature-synthesis-quotient-source-glue-or-GR-import-lock.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2507_SOURCE_REGISTER.csv",
    "signature_synthesis": OUT / "P8_Y5_NO_SHADOW_2507_PARENT_SIGNATURE_SYNTHESIS.csv",
    "countermodel_ledger": OUT / "P8_Y5_NO_SHADOW_2507_COUNTERMODEL_LEDGER.csv",
    "gr_import_lock": OUT / "P8_Y5_NO_SHADOW_2507_GR_IMPORT_LOCK.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2507_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2507_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2507_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2507_VALIDATION.csv",
}

BRANCH_COPIES = {
    "signature_synthesis": LOCAL_BOUNDS / "Parent_signature_synthesis_2507_NONCLAIM.csv",
    "countermodel_ledger": LOCAL_BOUNDS / "Parent_signature_countermodels_2507_NONCLAIM.csv",
    "gr_import_lock": BETA_DOCS / "GR_import_lock_2507_NONCLAIM.csv",
    "next_target": QUEUE / "JR2507_OBJECT_LANGUAGE_NO_SOURCE_SLOT_NEXT.csv",
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
    coeff = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
    residuals = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
    runs = ROOT / "runs"
    specs = [
        (
            "SRC2507_00_2506_handoff",
            ROOT / "2506-Y5-R2FR-parent-EH-descent-source-glue-proof-or-explicit-GR-import-demotion.md",
            ["NEXT2506_0_selected", "PARENT_SIGNATURE_SYNTHESIS_NEXT", "VAL2506_OVERALL"],
            "2506 selects parent signature synthesis and GR-import lock as next target.",
        ),
        (
            "SRC2507_01_2506_validation",
            OUT / "P8_Y5_BRR545_2506_VALIDATION.csv",
            ["VAL2506_OVERALL", "PASS"],
            "2506 validation passed before 2507 continues the chain.",
        ),
        (
            "SRC2507_02_source_label_proof",
            coeff / "source_label_forgetting_proof_attempt_nonclaim_1476.csv",
            ["SLF1476_0_target", "COUNTERMODEL_SURVIVES", "NOT_PARENT_DERIVED"],
            "Source-label forgetting has exact conditional lemmas but an active relative-weight countermodel.",
        ),
        (
            "SRC2507_03_source_label_decision",
            coeff / "source_label_forgetting_signing_decision_1476.csv",
            ["SIGN1476_0_source_label_forgetting", "REFUSE_SOURCE_LABEL_FORGETTING_PROMOTION_KEEP_DELTA_W_INPUT_NONCLAIM"],
            "Prior signing decision refuses to promote source-label forgetting.",
        ),
        (
            "SRC2507_04_double_zero",
            coeff / "parent_coupling_double_zero_theorem_attempt_nonclaim_1473.csv",
            ["DZ1473_0_taylor_lemma", "NO_GO_GUARD", "NOT_PARENT_DERIVED"],
            "Double-zero Taylor lemma is exact but requires a parent-signed complete coupling list.",
        ),
        (
            "SRC2507_05_double_zero_decision",
            coeff / "parent_coupling_double_zero_signing_decision_1473.csv",
            ["SIGN1473_0_double_zero", "REFUSE_DOUBLE_ZERO_PROMOTION_EMIT_EXECUTABLE_RESIDUAL_VECTOR"],
            "Prior signing decision refuses to promote double-zero theorem.",
        ),
        (
            "SRC2507_06_quotient_descent",
            coeff / "neighbourhood_quotient_descent_attempt_nonclaim_1486.csv",
            ["NQD1486_1_chain_rule", "EXACT_CONDITIONAL_POINTWISE", "NOT_CLOSED_SOURCE_MAP_BUILT"],
            "Quotient descent has a pointwise chain-rule lemma but no parent functor over an open neighbourhood.",
        ),
        (
            "SRC2507_07_parent_label_quotient",
            residuals / "R2FR_parent_label_quotient_clause_audit_1686.csv",
            ["PLQ1686_0_exact_clause", "PROOF_NOT_CLOSED", "legal kappa_A T_A and w_A S_A countermodels"],
            "Parent label quotient is exactly specified but not parent-derived.",
        ),
        (
            "SRC2507_08_owner_grammar",
            residuals / "R2FR_parent_source_owner_grammar_1699.csv",
            ["G1699_4_forbidden_target", "G1699_5_action_constructor", "conditional_constructor"],
            "Owner grammar states the desired object language but is not parent-signed.",
        ),
        (
            "SRC2507_09_owner_derivation_test",
            residuals / "R2FR_owner_axiom_derivation_test_1698.csv",
            ["DER1698_0_domain_exhaustion", "DER1698_6_result", "blocked_no_claim"],
            "Derivation test lists six unsigned clauses and surviving countermodels.",
        ),
        (
            "SRC2507_10_kappa_contract",
            OUT / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
            ["CU1_global_coupling_status", "CU3_species_source_blindness", "not_parent_derived"],
            "Constant universal kappa/G is contract-written but not parent-derived.",
        ),
        (
            "SRC2507_11_PiM_decision",
            runs / "20260605-044500-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion" / "results" / "P8_Y5_PIM_HAMILTONIAN_DECISION.csv",
            ["D539_0_Hamiltonian_PiM_candidate", "candidate_only", "local_GR_false"],
            "PiM-as-Hamiltonian charge is a candidate repair, not a signed source-glue proof.",
        ),
        (
            "SRC2507_12_boundary_decision",
            runs / "20260605-064500-Y5-boundary-reference-residual-theorem-or-fill-first-row" / "results" / "P8_Y5_BOUNDARY_REFERENCE_DECISION.csv",
            ["D543_0_zero_theorem_failed_current_claim", "boundary_reference_zero_not_derived", "Newton_PPN_local_GR_false"],
            "Boundary/reference zero theorem failed for current claim.",
        ),
        (
            "SRC2507_13_EH_source_owner",
            residuals / "R2FR_EH_source_owner_gate_1692.csv",
            ["OWNG1692_5_verdict", "FAIL_CURRENT_CLAIM_PARENT_OWNER_NOT_DERIVED"],
            "EH source-owner branch remains a target theorem, not evidence.",
        ),
        (
            "SRC2507_14_action_measure_gate",
            residuals / "R2FR_action_measure_owner_proof_gate_1694.csv",
            ["OWG1694_0_countermodel", "COUNTERMODEL_SURVIVES", "UNSIGNED_PARENT_GRAMMAR"],
            "Action-measure owner gate keeps the pre-variation relative-weight countermodel alive.",
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


def signature_synthesis_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SYN2507_0_quotient_vertical_blindness",
            "quotient naturality of observed geometry",
            "If e_obs=Obs_e(q(Phi)) and Dq[V]=0, then Lie_V e_obs=0.",
            "EXACT_CONDITIONAL_POINTWISE_LEMMA",
            "This signs only a chain-rule fact, not the live parent matter functor or no-reentry package.",
            "not_parent_signed",
            "needs parent-signed q, S_ord descent on an open neighbourhood, matter lift and no hidden reentry",
        ),
        (
            "SYN2507_1_source_label_forgetting",
            "universal matter/source-label forgetting",
            "If the parent ordinary-matter source functor has no labelled active-source coefficient target, relative source weights cannot be formed.",
            "EXACT_CONDITIONAL_THEOREM_COUNTERMODEL_SURVIVES",
            "The theorem is clean but w_A S_A remains a legal countermodel without parent object-language exhaustion.",
            "not_parent_signed",
            "needs no-source-only-slot grammar, connected ordinary matter category, common measure/current owner, variation-before-readout",
        ),
        (
            "SYN2507_2_double_zero",
            "extra-sector double-zero leakage kill",
            "If every non-EH coupling C_i obeys C_i(Phi0)=0 and partial_A C_i(Phi0)=0, first-order local leakage vanishes.",
            "EXACT_CONDITIONAL_TAYLOR_LEMMA",
            "The Taylor lemma is mathematically solid but the complete C_i list and double-zero origin are unsigned.",
            "not_parent_signed",
            "needs parent action to enumerate all source/readout/finite-range/PiM/boundary couplings and force double zeros",
        ),
        (
            "SYN2507_3_constant_kappa",
            "topological/global kappa constancy",
            "If kappa_eff is a global/superselected coupling with no source, marker, range or domain dependence, local G drift terms vanish.",
            "CONTRACT_WRITTEN_NOT_DERIVED",
            "No current parent theorem proves d kappa_eff=0 and species/source/range blindness together.",
            "not_parent_signed",
            "needs global-coupling parent action or superselection theorem plus no invariant-dependence proof",
        ),
        (
            "SYN2507_4_PiM_source_glue",
            "PiM/Hilbert/Hamiltonian source equality",
            "Pi_M must be the covariant phase-space Hamiltonian mass charge and equal the Hilbert source measure on the same worldtube.",
            "CANDIDATE_REPAIR_NOT_CLOSED",
            "Defining PiM as Hamiltonian charge is not enough until integrability, source frame and worldtube glue pass.",
            "not_parent_signed",
            "needs fixed reference, same source frame, old PiM equivalence, commutator zero and Gauss/PPN readout",
        ),
        (
            "SYN2507_5_boundary_silence",
            "boundary/reference/topological silence",
            "Boundary/reference/exact terms must have zero local linked-surface source flux.",
            "ZERO_THEOREM_FAILED_CURRENT_CLAIM",
            "Existing boundary theorem attempt explicitly says B_zero_flux and Delta_symp are not derived.",
            "not_parent_signed",
            "needs fixed reference subtraction, exact boundary zero, boundary no-hair and projector-variation silence",
        ),
        (
            "SYN2507_6_live_verdict",
            "live parent signature synthesis",
            "No currently unsigned 2506 clause becomes parent-signed in 2507 without adding a closure axiom.",
            "NO_PARENT_SIGNATURE_SIGNED_GR_IMPORT_LOCK_RETENTIVE",
            "2507 prevents circular promotion and preserves a clean next derivation target.",
            "claim_blocked",
            "attack object-language/no-source-only-slot first; it blocks the largest family of coupling countermodels",
        ),
    ]
    return [
        base_row(
            synthesis_id=synthesis_id,
            signature=signature,
            formal_statement=statement,
            result=result,
            implication=implication,
            live_status=live_status,
            missing_for_claim=missing,
        )
        for synthesis_id, signature, statement, result, implication, live_status, missing in specs
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CM2507_0_relative_source_weight",
            "S_matter=sum_A w_A S_A[Psi_A,e_obs]",
            "Preserves covariance/additivity and can preserve isolated classical EOM form while changing Hilbert source weights.",
            "blocks source-label forgetting and universal matter coupling",
            "object-language theorem excluding source-only coefficients plus common action measure owner",
        ),
        (
            "CM2507_1_labelled_source_multiplier",
            "F_grav(q_src((T_A,A))) = kappa_A T_A",
            "Keeps observed stress tensors but inserts an active source multiplier after label projection.",
            "blocks parent label quotient and WEP/source-normalization zero",
            "parent quotient must erase labels before coupling and forbid Hom(label,Coeff_active_source)",
        ),
        (
            "CM2507_2_nonzero_Ci_slope",
            "C_i(Phi)=c0+c1(Phi-Phi0)+...",
            "A stationary field equation E_A(Phi0)=0 does not force unrelated coupling functions to have c0=c1=0.",
            "blocks double-zero proof from fixed-point existence alone",
            "selection symmetry, quotient grammar, or parent variation tying couplings to fixed-point annihilator",
        ),
        (
            "CM2507_3_boundary_monopole",
            "exact/reference/topological boundary term carries finite linked-surface monopole",
            "An exact or reference term can still shift the mass charge unless the reference class and flux vanish theorem are fixed.",
            "blocks boundary silence and measured GM identity",
            "boundary no-hair plus fixed-reference Hamiltonian subtraction theorem",
        ),
        (
            "CM2507_4_kappa_marker_dependence",
            "kappa_eff=kappa0[1+epsilon f(memory,source,range,domain)]",
            "A scalar/source marker dependence creates G drift, fifth-force or WEP residuals even if a constant part is calibrated.",
            "blocks constant universal G/kappa",
            "global-coupling superselection and no marker/source/range/domain dependence theorem",
        ),
        (
            "CM2507_5_Hamiltonian_wrong_source",
            "conserved Hamiltonian charge exists but is not the Hilbert matter source mass",
            "A conserved charge can be the wrong object for Newton/orbits if source frame and worldtube glue are missing.",
            "blocks PiM/source glue",
            "same worldtube, same time generator, same observed coframe and PiM-Hilbert-Hamiltonian identity",
        ),
    ]
    return [
        base_row(
            countermodel_id=countermodel_id,
            countermodel=countermodel,
            why_legal_without_signature=why,
            blocks=blocks,
            required_kill_clause=kill_clause,
        )
        for countermodel_id, countermodel, why, blocks, kill_clause in specs
    ]


def gr_import_lock_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "LOCK2507_0_label",
            "current local branch label",
            "GR/EH import plus explicit MTS residual interface",
            "required",
            "No parent signature closes in 2507; the 2505 EH coefficients remain inherited from EH, not owned by MTS.",
        ),
        (
            "LOCK2507_1_allowed",
            "allowed private use",
            "Use EH-to-v coefficients as a target/benchmark and conditional inheritance branch.",
            "allowed_nonclaim",
            "This keeps the route alive without pretending the parent proof is done.",
        ),
        (
            "LOCK2507_2_forbidden",
            "forbidden promotion",
            "Do not claim local GR/Newton/PPN pass from beta/gamma or conditional descent alone.",
            "blocked",
            "Requires source glue, double zeros, boundary silence, constant kappa and readout ownership.",
        ),
        (
            "LOCK2507_3_unlock_condition",
            "unlock condition",
            "At least one parent signature must be derived from MTS primitives without fitting G or adding a closure axiom.",
            "next_gate",
            "Best first target is no-source-only object-language exhaustion because it kills the w_A/kappa_A countermodels.",
        ),
    ]
    return [
        base_row(lock_id=lock_id, gate=gate, rule=rule, status=status, reason=reason)
        for lock_id, gate, rule, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2507_0_no_signature_signed",
            "NO_PARENT_SIGNATURE_SIGNED",
            "All candidate routes are exact conditional lemmas or contracts, but every route retains parent-ownership gaps and at least one legal countermodel.",
            "selected",
        ),
        (
            "DEC2507_1_not_a_failure",
            "COUNTERMODELS_ARE_NOW_EXPLICIT",
            "The result is not random circling: it identifies the exact countermodels that a real MTS parent action must make syntactically or dynamically impossible.",
            "selected",
        ),
        (
            "DEC2507_2_lock",
            "GR_IMPORT_LOCK_RETAINED",
            "Until a parent signature is derived, the local branch remains GR/EH import plus residual interface.",
            "selected",
        ),
        (
            "DEC2507_3_next",
            "OBJECT_LANGUAGE_NO_SOURCE_ONLY_SLOT_NEXT",
            "The best next attack is to prove that the parent object language excludes source-only coefficients w_A/kappa_A before source coupling; this is the least hand-wavy route.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2507_0_selected",
            selection_status="selected",
            target_file="2508-Y5-R2FR-object-language-no-source-only-slot-proof-or-GR-import-lock.md",
            target_script="scripts/Y5_R2FR_object_language_no_source_only_slot_proof_or_GR_import_lock_2508.py",
            objective="try to prove from MTS primitives that source-only coefficients w_A, kappa_A, hidden label markers and post-variation source rescalers are not legal parent-action arguments; if not, keep explicit residual rows",
            success_condition="parent grammar exhaustion proves allowed ordinary-matter arguments are observed geometry, matter fields, gauge/representation data and universal constants only, with no active source multiplier target",
            do_not_do="do not assume universal coupling, do not absorb relative weights into measured G, do not call a conditional category lemma a parent proof, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2507_1_parallel_numeric",
            selection_status="held_parallel",
            target_file="2508b-Y5-R2FR-GR-import-residual-bound-pack.md",
            target_script="scripts/Y5_R2FR_GR_import_residual_bound_pack_2508b.py",
            objective="if object-language derivation fails, source the residual interface for PPN, WEP, R10, clocks and orbital comparisons",
            success_condition="each retained residual has units, source path, arena projection and valid_for_claim=false until sourced numeric rows exist",
            do_not_do="do not score placeholders or promote bound survival to derivation",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("signature_synthesis", OUTPUTS["signature_synthesis"], BRANCH_COPIES["signature_synthesis"]),
        ("countermodel_ledger", OUTPUTS["countermodel_ledger"], BRANCH_COPIES["countermodel_ledger"]),
        ("gr_import_lock", OUTPUTS["gr_import_lock"], BRANCH_COPIES["gr_import_lock"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=f"COPY2507_{copy_id}", source_path=str(source), target_path=str(target), copied=target.exists()))
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

    add("VAL2507_00_sources_exist", all(row["path_exists"] for row in rows_by_name["source_register"]), "all cited source paths exist")
    add("VAL2507_01_source_needles", all(row["source_pass"] for row in rows_by_name["source_register"]), "all required source needles are present")

    synthesis_results = {row["result"] for row in rows_by_name["signature_synthesis"]}
    add(
        "VAL2507_02_synthesis_verdict",
        "NO_PARENT_SIGNATURE_SIGNED_GR_IMPORT_LOCK_RETENTIVE" in synthesis_results,
        "signature synthesis refuses unsupported promotion",
    )
    add(
        "VAL2507_03_countermodels",
        len(rows_by_name["countermodel_ledger"]) >= 5 and any("w_A" in row["countermodel"] for row in rows_by_name["countermodel_ledger"]),
        "countermodel ledger includes relative source-weight obstruction",
    )
    lock_rules = {row["status"] for row in rows_by_name["gr_import_lock"]}
    add(
        "VAL2507_04_gr_import_lock",
        {"required", "blocked", "next_gate"}.issubset(lock_rules),
        "GR-import lock is explicit",
    )
    decision_text = " ".join(row["decision"] for row in rows_by_name["decision_ledger"])
    add("VAL2507_05_decision", "OBJECT_LANGUAGE_NO_SOURCE_ONLY_SLOT_NEXT" in decision_text, "decision chooses object-language no-source-only-slot next")
    add("VAL2507_06_next_target", any(row["route_id"] == "NEXT2507_0_selected" for row in rows_by_name["next_target"]), "2508 object-language target selected")
    add("VAL2507_07_no_claim_flags", no_claim_flags(rows_by_name), "all generated rows keep valid_for_claim=false and claim_allowed=false")
    add("VAL2507_08_branch_copies", all(row["copied"] for row in rows_by_name["branch_copies"]), "branch copies were written")

    formalization_artifacts: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*2507*", "*P8_Y5_NO_SHADOW_2507*", "*JR2507*"):
            formalization_artifacts.extend(path for path in FORMALIZATION.rglob(pattern) if path.is_file())
    add("VAL2507_09_no_formalization_artifacts", not formalization_artifacts, "no 2507 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for path in OUTPUTS.values():
        if path == OUTPUTS["validation"]:
            continue
        parsed, count, detail = csv_rows_parse(path)
        add(f"VAL2507_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", detail)

    for key, path in BRANCH_COPIES.items():
        parsed, count, detail = csv_rows_parse(path)
        add(f"VAL2507_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", detail)

    remove_pycache()
    add("VAL2507_10_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts pycache removed")

    overall = all(row["status"] == "PASS" for row in validations)
    add(
        "VAL2507_OVERALL",
        overall,
        "2507 audits parent-signature synthesis, signs no unsupported clause, locks GR-import label, and selects object-language no-source-slot proof next",
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2507 Y5 R2FR Parent Signature Synthesis Quotient Source Glue Or GR Import Lock

## Current Verdict

2507 tries the leap and refuses to fake it.

The search found exact conditional lemmas:

- quotient vertical blindness by chain rule;
- source-label forgetting if the parent source functor has no label coefficient target;
- double-zero leakage suppression if every non-EH coupling has value and first variation zero;
- constant-kappa/source-blindness if kappa is truly global/superselected;
- PiM/Hilbert/Hamiltonian equality if the Hamiltonian source frame and worldtube glue are signed.

But none of these are live parent signatures yet. Each route still has a legal countermodel: `w_A S_A`, `kappa_A T_A`, nonzero `C_i` slope, boundary monopole, kappa marker-dependence, or conserved-but-wrong Hamiltonian charge.

So the local branch stays honestly labelled:

**GR/EH import plus explicit MTS residual interface.**

The next best attack is not more beta algebra. It is the parent object-language theorem: prove that source-only coefficients like `w_A` and `kappa_A` are not legal parent-action arguments in the first place.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "source_pass", "role", "valid_for_claim"])}

## Parent Signature Synthesis

{md_table(rows_by_name["signature_synthesis"], ["synthesis_id", "signature", "formal_statement", "result", "implication", "live_status", "missing_for_claim", "valid_for_claim"])}

## Countermodel Ledger

{md_table(rows_by_name["countermodel_ledger"], ["countermodel_id", "countermodel", "why_legal_without_signature", "blocks", "required_kill_clause", "valid_for_claim"])}

## GR Import Lock

{md_table(rows_by_name["gr_import_lock"], ["lock_id", "gate", "rule", "status", "reason", "valid_for_claim"])}

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
        "signature_synthesis": signature_synthesis_rows(),
        "countermodel_ledger": countermodel_rows(),
        "gr_import_lock": gr_import_lock_rows(),
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
