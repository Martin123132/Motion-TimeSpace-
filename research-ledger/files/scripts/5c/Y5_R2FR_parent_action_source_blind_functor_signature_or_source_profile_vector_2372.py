from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_PARENT_ACTION_SOURCE_BLIND_FUNCTOR_SIGNATURE_OR_SOURCE_PROFILE_VECTOR_2372"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2372-Y5-R2FR-parent-action-source-blind-functor-signature-or-source-profile-vector.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2372_2371_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2371_NEXT_TARGET.csv", "NEXT2371_0_selected", "2371 selected source-blind functor route"),
        ("SRC2372_2371_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2371_VALIDATION.csv", "VAL2371_OVERALL", "2371 validation"),
        ("SRC2372_2329_signature", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2329_SOURCE_BLIND_FUNCTOR_SIGNATURE.csv", "SBF2329_6_verdict", "source-blind matter functor signature"),
        ("SRC2372_2329_theorem", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2329_NOSOURCE_SLOT_THEOREM_PROOF.csv", "NST2329_6_verdict", "NoSourceOnlySpeciesSlot conditional theorem"),
        ("SRC2372_2329_activation", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2329_PARENT_SIGNATURE_ACTIVATION_MATRIX.csv", "ACT2329_2_adopt_as_parent_action_definition", "activation/adoption matrix"),
        ("SRC2372_2330_deeper", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2330_DEEPER_QUOTIENT_DERIVATION_AUDIT.csv", "DQD2330_5_verdict", "deeper quotient derivation audit"),
        ("SRC2372_2330_adoption", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2330_ADOPTION_DECISION_MATRIX.csv", "ADM2330_3_decision", "dual-track adoption decision"),
        ("SRC2372_2330_restriction", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2330_PARENT_ACTION_RESTRICTION_DRAFT.csv", "PAR2330_0_name", "Minimal Universal Matter Coupling draft"),
        ("SRC2372_2330_impact", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2330_DOWNSTREAM_GATE_IMPACT.csv", "DGI2330_3_local_GR_Newton", "downstream local-GR impact"),
        ("SRC2372_2330_claims", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2330_CLAIM_GATES.csv", "CG2330_6_github_public_update", "claim gates"),
        ("SRC2372_2330_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2330_NEXT_TARGET.csv", "NEXT2330_0", "Noether/source-charge next target"),
        ("SRC2372_2330_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2330_VALIDATION.csv", "VAL2330_OVERALL", "2330 validation"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def minimal_coupling_signature() -> list[dict[str, object]]:
    rows = [
        (
            "MUC2372_0_parent_data",
            "observed quotient before matter coupling",
            "Phi -> q(Phi)=Q_obs; O(q)=(M,g_obs,e_obs,omega_obs,theta)",
            "ordinary matter sees only observed quotient data plus ordinary material constants",
            "PROVISIONAL_PRIVATE_PARENT_RESTRICTION",
        ),
        (
            "MUC2372_1_source_blind_functor",
            "source-blind ordinary matter functor",
            "Matter: Q_obs x SpeciesRep -> ActionDensity, with no Coeff_active_source(A) argument",
            "species labels specify representations/fields, not independent gravitational source strength",
            "CORE_RESTRICTION_DRAFT_READY",
        ),
        (
            "MUC2372_2_single_measure_scale",
            "one observed measure and one common source scale",
            "S_m = integral mu_obs sum_A L_A(j^k Psi_A,e_obs,omega_obs,theta_A)",
            "Hilbert variation is label-additive and one common scale can be absorbed into kappa/G_N/GM",
            "PROVISIONAL_PRIVATE_PARENT_RESTRICTION",
        ),
        (
            "MUC2372_3_theta_separation",
            "theta_A cannot hide a source-only multiplier",
            "theta_A is admissible only if it changes ordinary matter dynamics/standards or is retained as finite residual",
            "prevents w_A being renamed as a harmless material constant",
            "ADMISSIBILITY_RULE_REQUIRED",
        ),
        (
            "MUC2372_4_hilbert_before_readout",
            "source current before arena/readout",
            "T_H := delta S_m/delta e_obs; K_arena, masks, Pi_gamma and GM calibration act downstream",
            "kills post-variation source-current rescaling tricks",
            "EXACT_GIVEN_RESTRICTED_READOUT_ORDER",
        ),
        (
            "MUC2372_5_nonhilbert_policy",
            "non-Hilbert source currents retained unless proved silent",
            "J_source = T_H + J_NH + J_boundary + J_readout",
            "prevents the private restriction from sweeping hidden source tails away",
            "OPEN_PARALLEL_GATE_RETAINED",
        ),
        (
            "MUC2372_6_verdict",
            "Minimal Universal Matter Coupling branch",
            "MUC2372_0 through MUC2372_5",
            "usable as private bookkeeping restriction, not a public derivation",
            "PRIVATE_BRANCH_READY_NOT_DERIVED",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "signature_clause": clause,
            "mathematical_form": form,
            "function": function,
            "status": status,
        }
        for row_id, clause, form, function, status in rows
    ]


def derivation_audit() -> list[dict[str, object]]:
    rows = [
        (
            "DA2372_0_target",
            "derive Minimal Universal Matter Coupling",
            "Can q/flow structure force Matter: Q_obs x SpeciesRep -> ActionDensity with no active-source coefficient slot?",
            "TARGET_SHARPENED",
            "need to show ordinary species labels cannot define independent gravitational charge",
        ),
        (
            "DA2372_1_quotient_descent",
            "quotient descent",
            "S_matter factors through q(Phi) and observed coframe data",
            "PARTIAL_WIN_NOT_ENOUGH",
            "descent removes representative-only fields, but species-indexed constants can still live in theta_A",
        ),
        (
            "DA2372_2_naturality",
            "naturality over observed matter data",
            "natural functoriality forbids non-natural source coefficients only if Coeff_active_source is already absent",
            "CONDITIONAL_WIN_RESTATES_SIGNATURE",
            "must derive the allowed functor domain rather than assume it",
        ),
        (
            "DA2372_3_double_accounting",
            "no duplicate inertial/source normalization",
            "a source-only w_A changes gravitational source without changing ordinary matter normalization",
            "STRONG_PHYSICAL_PRINCIPLE_NOT_FORMAL_DERIVATION",
            "needs parent admissibility principle or deeper Noether/source-charge identity",
        ),
        (
            "DA2372_4_no_independent_grav_charge",
            "no independent gravitational source charge",
            "ordinary matter has one Hilbert/Noether stress source, not a second species charge for gravity",
            "BEST_DEEPER_DERIVATION_TARGET",
            "prove source charge equals Hilbert/Noether energy for all ordinary matter from parent symmetries",
        ),
        (
            "DA2372_5_verdict",
            "derive source-blind signature now",
            "assemble quotient descent, naturality, no-double-counting and source-charge identity",
            "NOT_DERIVED_PROVISIONAL_RESTRICTION_RETAINED",
            "use the branch privately while attacking Noether/source-charge identity next",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "derivation_target": target,
            "test": test,
            "result": result,
            "obstruction_or_next": obstruction,
        }
        for row_id, target, test, result, obstruction in rows
    ]


def adoption_decision_matrix() -> list[dict[str, object]]:
    rows = [
        (
            "ADM2372_0_private_restriction",
            "use Minimal Universal Matter Coupling privately",
            "ALLOW_AS_PRIVATE_WORKING_BRANCH",
            "lets the source-side GR route be developed without pretending source-only couplings are legal",
            "must be labelled provisional; not public evidence",
        ),
        (
            "ADM2372_1_deeper_derivation",
            "derive restriction from Noether/source-charge identity",
            "SELECT_AS_NEXT_THEOREM_TARGET",
            "would make the local GR reduction derived rather than stipulated",
            "not closed here",
        ),
        (
            "ADM2372_2_finite_fallback",
            "source-profile vector and L_source_GM bound",
            "RETAIN_IF_DERIVATION_FAILS",
            "keeps branch testable and honest",
            "less elegant; turns zero theorem into bounded residual",
        ),
        (
            "ADM2372_3_decision",
            "2372 live branch decision",
            "DUAL_TRACK_PRIVATE_BRANCH_PLUS_DERIVATION",
            "use restriction for internal bookkeeping while immediately pursuing derivation",
            "do not claim local GR/Newton pass",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "option": option,
            "decision": decision,
            "benefit": benefit,
            "cost_or_guard": cost,
        }
        for row_id, option, decision, benefit, cost in rows
    ]


def downstream_gate_impact() -> list[dict[str, object]]:
    rows = [
        (
            "DGI2372_0_source_only_slot",
            "NoSourceOnlySpeciesSlot",
            "closed only inside the provisional restricted parent-action branch",
            "deeper derivation or public justification",
            "conditional_private_branch_only",
        ),
        (
            "DGI2372_1_source_GM_zero",
            "epsilon_sigma_source_GM=0",
            "species-weight leak removed inside restricted branch",
            "source profile/GM same-frame calibration and hidden-current gates",
            "not_zero_yet",
        ),
        (
            "DGI2372_2_source_side_GR",
            "ordinary matter source -> calibrated Hilbert current",
            "source-side common-mode theorem becomes cleaner",
            "non-Hilbert residual closure and left-hand EH/Newton operator",
            "conditional_source_side_only",
        ),
        (
            "DGI2372_3_local_GR_Newton",
            "full local GR/Newton recovery",
            "not enough by itself",
            "EH/Newton left-hand limit, PPN/readout residuals, projector/domain terms",
            "blocked",
        ),
        (
            "DGI2372_4_finite_fallback",
            "source-profile vector branch",
            "parked but not deleted",
            "needed if derivation/adoption or hidden-current gates fail",
            "retained_nonclaim",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "impact_if_private_restriction_used": impact,
            "still_missing": missing,
            "claim_status": status,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, impact, missing, status in rows
    ]


def noether_source_charge_target() -> list[dict[str, object]]:
    rows = [
        (
            "NSC2372_0_identity_target",
            "No independent gravitational source charge",
            "For ordinary matter, the generator that couples to local gravitational/coframe variation is the same Hilbert/Noether stress source obtained from S_matter; there is no separate SpeciesLabel -> gravitational charge map.",
            "NEXT_THEOREM_TO_PROVE",
            "would derive the source-blind functor restriction instead of adopting it",
        ),
        (
            "NSC2372_1_required_symmetry",
            "observed-frame diffeomorphism/local-frame invariance",
            "Noether identity must bind source response to variation of e_obs/g_obs and ordinary matter fields.",
            "SOURCE_SYMMETRY_INPUT_REQUIRED",
            "need exact parent symmetry and variation order",
        ),
        (
            "NSC2372_2_allowed_theta",
            "ordinary material constants",
            "theta_A may affect masses, charges, clock standards, interactions or representations, but then it enters ordinary matter tensors rather than a hidden source-only slot.",
            "ADMISSIBILITY_CLASSIFICATION_REQUIRED",
            "need a crisp test for source-only theta_A",
        ),
        (
            "NSC2372_3_nonhilbert_guard",
            "non-Hilbert/boundary/readout current guard",
            "Any J_NH, J_boundary or J_readout term must be exact/projected-silent or finite-bounded.",
            "PARALLEL_GATE_OPEN",
            "source charge identity alone does not silence hidden currents",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "target_piece": piece,
            "formal_statement": statement,
            "status": status,
            "effect_or_missing": effect,
        }
        for row_id, piece, statement, status, effect in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2372_0_sources", "source paths and needles valid", "PASS", "audit reproducible"),
        ("CG2372_1_signature_ready", "Minimal Universal Matter Coupling precisely written", "PASS", "private branch ready only"),
        ("CG2372_2_deeper_derivation", "source-blind signature derived from q/flow/Noether primitives now", "FAIL", "not derived"),
        ("CG2372_3_source_GM_zero", "epsilon_sigma_source_GM zero active", "FAIL", "source profile/GM/same-frame and hidden-current gates remain"),
        ("CG2372_4_local_GR_Newton", "full local GR/Newton recovery", "FAIL", "not enough; left-hand and readout residual gates remain"),
        ("CG2372_5_github_public_update", "safe to push as public evidence", "FAIL", "private fork-control checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "gate_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, status, effect in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        (
            "REF2372_0_adoption_as_derivation",
            "Private Minimal Universal Matter Coupling branch is a derivation from older primitives.",
            "false",
            "the derivation audit still says q descent/naturality do not forbid species-indexed source constants by themselves",
        ),
        (
            "REF2372_1_adoption_as_public_claim",
            "Minimal Universal Matter Coupling proves local GR/Newton publicly.",
            "false",
            "source_GM, non-Hilbert, same-frame, readout and left-hand EH/Newton gates remain open",
        ),
        (
            "REF2372_2_delete_fallback",
            "Finite source-profile vector route can be deleted.",
            "false",
            "fallback remains if deeper derivation or hidden-current gates fail",
        ),
        (
            "REF2372_3_skip_noether",
            "Noether/source-charge derivation is optional busywork.",
            "false",
            "the objective is derivability; the private restriction is bookkeeping, not final victory",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, allowed, reason in rows
    ]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2372_0_selected",
            "2373-Y5-R2FR-Noether-source-charge-identity-or-nonHilbert-residual-row.md",
            "scripts/Y5_R2FR_Noether_source_charge_identity_or_nonHilbert_residual_row_2373.py",
            "prove ordinary matter has no independent gravitational source charge beyond its Hilbert/Noether stress source; if not, retain explicit non-Hilbert/source-charge residual row",
            "do not use Minimal Universal Matter Coupling as a public derivation unless this identity closes",
        ),
        (
            "NEXT2372_1_branch_ledger",
            "2373b-Y5-R2FR-private-minimal-universal-matter-coupling-branch-ledger.md",
            "scripts/Y5_R2FR_private_minimal_universal_matter_coupling_branch_ledger_2373b.py",
            "track all results that depend on the provisional parent-action restriction separately",
            "prevent provisional branch claims from contaminating public/local-GR gate status",
        ),
        (
            "NEXT2372_2_fallback",
            "2373c-Y5-R2FR-source-profile-vector-acquisition-if-source-charge-identity-fails.md",
            "scripts/Y5_R2FR_source_profile_vector_acquisition_if_source_charge_identity_fails_2373c.py",
            "stage source-profile/source-weight vector rows with basis, units, frame and GM calibration",
            "keep every finite value nonclaim until same-frame projections and bounds are source-backed",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "next_file": file_name,
            "next_script": script_name,
            "success_condition": success,
            "fallback_condition": fallback,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, file_name, script_name, success, fallback in rows
    ]


def all_output_files() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_2372_SOURCE_REGISTER.csv",
        "minimal_coupling_signature": RESIDUALS / "P8_Y5_PARENT_QLOC_2372_MINIMAL_UNIVERSAL_MATTER_COUPLING_SIGNATURE.csv",
        "derivation_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2372_DERIVATION_AUDIT.csv",
        "adoption_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2372_ADOPTION_DECISION_MATRIX.csv",
        "downstream_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_2372_DOWNSTREAM_GATE_IMPACT.csv",
        "noether_target": RESIDUALS / "P8_Y5_PARENT_QLOC_2372_NOETHER_SOURCE_CHARGE_TARGET.csv",
        "claim_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2372_CLAIM_GATES.csv",
        "refusal_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_2372_REFUSAL_RUNNER.csv",
        "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_2372_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2372_VALIDATION.csv",
    }


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    sensitive = {
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
        "local_gr_claim",
        "epsilon_zero_active",
        "vector_complete",
    }
    positive_values = {"true", "pass", "passed", "ready", "yes", "1"}
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in sensitive and str(value).strip().lower() in positive_values:
                    return False
    return True


def validation_rows(outputs: dict[str, Path]) -> list[dict[str, object]]:
    source_rows = read_csv(outputs["source_register"])
    generated_paths = [path for key, path in outputs.items() if key != "validation"]
    parsed_ok = True
    for path in generated_paths:
        try:
            parsed_ok = parsed_ok and bool(read_csv(path))
        except Exception:
            parsed_ok = False

    signature_rows = read_csv(outputs["minimal_coupling_signature"])
    derivation_rows = read_csv(outputs["derivation_audit"])
    adoption_rows = read_csv(outputs["adoption_decision"])
    impact_rows = read_csv(outputs["downstream_impact"])
    noether_rows = read_csv(outputs["noether_target"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])

    checks = [
        (
            "VAL2372_00_required_sources_exist",
            all(row["path_exists"] == "true" for row in source_rows),
            "all required source paths exist",
        ),
        (
            "VAL2372_01_required_needles_found",
            all(row["needle_found"] == "true" for row in source_rows),
            "all source needles found",
        ),
        (
            "VAL2372_02_outputs_exist",
            all(path.exists() for path in generated_paths),
            "all 2372 output files written",
        ),
        (
            "VAL2372_03_csv_parse",
            parsed_ok,
            "all generated CSV files parse and contain rows",
        ),
        (
            "VAL2372_04_signature_written",
            any(row["row_id"] == "MUC2372_6_verdict" and row["status"] == "PRIVATE_BRANCH_READY_NOT_DERIVED" for row in signature_rows),
            "Minimal Universal Matter Coupling branch recorded as private-not-derived",
        ),
        (
            "VAL2372_05_derivation_not_overclaimed",
            any(row["row_id"] == "DA2372_5_verdict" and row["result"].startswith("NOT_DERIVED") for row in derivation_rows),
            "deeper derivation remains unclaimed",
        ),
        (
            "VAL2372_06_dual_track_decision",
            any(row["row_id"] == "ADM2372_3_decision" and row["decision"] == "DUAL_TRACK_PRIVATE_BRANCH_PLUS_DERIVATION" for row in adoption_rows),
            "dual-track private restriction plus derivation audit recorded",
        ),
        (
            "VAL2372_07_local_gr_still_blocked",
            any(row["row_id"] == "DGI2372_3_local_GR_Newton" and row["claim_status"] == "blocked" for row in impact_rows),
            "full local GR/Newton gate remains blocked",
        ),
        (
            "VAL2372_08_noether_selected",
            any(row["row_id"] == "NSC2372_0_identity_target" and row["status"] == "NEXT_THEOREM_TO_PROVE" for row in noether_rows),
            "Noether/source-charge identity selected as theorem target",
        ),
        (
            "VAL2372_09_github_blocked",
            any(row["row_id"] == "CG2372_5_github_public_update" and row["gate_status"] == "FAIL" for row in gates),
            "public GitHub evidence update remains blocked",
        ),
        (
            "VAL2372_10_no_positive_claim_flags",
            check_no_positive_claim_flags(generated_paths),
            "all generated claim/readiness flags remain negative",
        ),
        (
            "VAL2372_11_formalization_untouched",
            not any(FORMALIZATION_WORKBENCH in path.parents for path in generated_paths),
            "generator writes only under post-checkpoint-work",
        ),
        (
            "VAL2372_12_next_selected",
            any(row["row_id"] == "NEXT2372_0_selected" and "Noether_source_charge_identity" in row["next_script"] for row in next_rows),
            "2373 Noether/source-charge target selected",
        ),
    ]
    rows = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in checks
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2372_OVERALL",
            "status": "PASS" if overall_ok else "FAIL",
            "detail": "2372 valid: Minimal Universal Matter Coupling is private-not-derived, deeper derivation remains open, Noether/source-charge identity selected next"
            if overall_ok
            else "2372 validation failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    signature = read_csv(outputs["minimal_coupling_signature"])
    derivation = read_csv(outputs["derivation_audit"])
    adoption = read_csv(outputs["adoption_decision"])
    impact = read_csv(outputs["downstream_impact"])
    noether = read_csv(outputs["noether_target"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])
    generated = [rel(path) for path in outputs.values()]

    text = f"""# 2372 - Parent Action Source-Blind Functor Signature Or Source-Profile Vector

## Result

The coupling throat is now controlled by a precise private branch, not by a vague hope.

The private branch is **Minimal Universal Matter Coupling**:

`Matter: Q_obs x SpeciesRep -> ActionDensity`

with one observed measure/source scale, one Hilbert source before readout, ordinary matter constants inside `theta_A`, and no independent `SpeciesLabel -> Coeff_active_source` object.

That would close the source-only species coupling leak **inside the restricted branch**, but it is not yet derived from deeper MTS primitives.  Quotient descent and naturality are partial wins; they do not by themselves forbid species-indexed constants.  The next purist target is therefore sharper:

`ordinary matter has no independent gravitational source charge beyond its Hilbert/Noether stress source`.

No local-GR/Newton claim is made here.  This checkpoint keeps the private restriction useful for bookkeeping while selecting the Noether/source-charge identity as the next derivation attempt.

## Minimal Universal Matter Coupling Signature

{md_table(signature, ["row_id", "signature_clause", "status", "function"])}

## Derivation Audit

{md_table(derivation, ["row_id", "derivation_target", "result", "obstruction_or_next"])}

## Adoption Decision Matrix

{md_table(adoption, ["row_id", "option", "decision", "cost_or_guard"])}

## Downstream Gate Impact

{md_table(impact, ["row_id", "gate", "impact_if_private_restriction_used", "still_missing", "claim_status"])}

## Noether / Source-Charge Target

{md_table(noether, ["row_id", "target_piece", "status", "effect_or_missing"])}

## Claim Gates

{md_table(gates, ["row_id", "gate", "gate_status", "claim_effect"])}

## Next Target

{md_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition"])}

## Generated Files

"""
    text += "\n".join(f"- `{path}`" for path in generated)
    text += """

## Practical Status

This is progress, but not a victory lap.  The source-side coupling problem is now sharply framed: either derive the Noether/source-charge identity and make the minimal coupling branch feel inevitable, or admit the finite source-profile/non-Hilbert residuals explicitly.  That is much better than hand-waving the coupling away.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    outputs = all_output_files()
    write_csv(outputs["source_register"], source_register())
    write_csv(outputs["minimal_coupling_signature"], minimal_coupling_signature())
    write_csv(outputs["derivation_audit"], derivation_audit())
    write_csv(outputs["adoption_decision"], adoption_decision_matrix())
    write_csv(outputs["downstream_impact"], downstream_gate_impact())
    write_csv(outputs["noether_target"], noether_source_charge_target())
    write_csv(outputs["claim_gates"], claim_gates())
    write_csv(outputs["refusal_runner"], refusal_runner())
    write_csv(outputs["next_target"], next_target())
    write_csv(outputs["validation"], validation_rows(outputs))
    write_doc(outputs)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {outputs['validation']}")


if __name__ == "__main__":
    main()
