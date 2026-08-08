from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2537"
BRANCH_ID = "MTS_R2FR_PARENT_ACTION_SOURCE_BLIND_FUNCTOR_SIGNATURE_OR_SOURCE_PROFILE_VECTOR_2537"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2537-Y5-R2FR-parent-action-source-blind-functor-signature-or-source-profile-vector.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2537_SOURCE_REGISTER.csv",
    "signature": RESIDUALS / "P8_Y5_NO_SHADOW_2537_MINIMAL_UNIVERSAL_MATTER_COUPLING_SIGNATURE.csv",
    "derivation": RESIDUALS / "P8_Y5_NO_SHADOW_2537_DERIVATION_AUDIT.csv",
    "adoption": RESIDUALS / "P8_Y5_NO_SHADOW_2537_ADOPTION_DECISION_MATRIX.csv",
    "impact": RESIDUALS / "P8_Y5_NO_SHADOW_2537_DOWNSTREAM_GATE_IMPACT.csv",
    "noether": RESIDUALS / "P8_Y5_NO_SHADOW_2537_NOETHER_SOURCE_CHARGE_TARGET.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2537_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2537_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2537_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2537_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2537_VALIDATION.csv",
}

BRANCH_COPIES = {
    "signature": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Minimal_universal_matter_coupling_2537_PRIVATE_NONCLAIM.csv",
    "noether": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "Noether_source_charge_target_2537_NONCLAIM.csv",
    "impact": POST_ROOT / "source-intake" / "local_bounds" / "Source_blind_downstream_impact_2537_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "NOETHER2537_NEXT_TARGET_NONCLAIM.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


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


SOURCE_SPECS = [
    ("SRC2537_0_2536_doc", "2536-Y5-R2FR-source-feedback-epsilon-sigma-or-PPN-gauge-bound-row.md", "NEXT2536_0_selected", "2536 selected source-blind functor route"),
    ("SRC2537_1_2536_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2536_VALIDATION.csv", "VAL2536_OVERALL,PASS", "2536 validation anchor"),
    ("SRC2537_2_2536_nosource", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2536_NOSOURCEONLY_PARALLEL_ROUTE.csv", "NSOS2536_2_source_blind_functor", "current source-blind route input"),
    ("SRC2537_3_2372_doc", "2372-Y5-R2FR-parent-action-source-blind-functor-signature-or-source-profile-vector.md", "MUC2372_6_verdict", "source-blind private branch precedent"),
    ("SRC2537_4_2372_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2372_VALIDATION.csv", "VAL2372_OVERALL,PASS", "2372 validation anchor"),
    ("SRC2537_5_2372_signature", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2372_MINIMAL_UNIVERSAL_MATTER_COUPLING_SIGNATURE.csv", "MUC2372_6_verdict", "Minimal Universal Matter Coupling signature precedent"),
    ("SRC2537_6_2372_derivation", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2372_DERIVATION_AUDIT.csv", "DA2372_5_verdict", "derivation audit precedent"),
    ("SRC2537_7_2372_noether", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2372_NOETHER_SOURCE_CHARGE_TARGET.csv", "NSC2372_0_identity_target", "Noether/source-charge target precedent"),
    ("SRC2537_8_2372_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2372_NEXT_TARGET.csv", "NEXT2372_0_selected", "Noether/source-charge selected next in precedent"),
    ("SRC2537_9_2373_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2373_VALIDATION.csv", "VAL2373_OVERALL,PASS", "Noether/source-charge downstream validation anchor"),
]


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in SOURCE_SPECS:
        path = POST_ROOT / source_path
        rows.append(
            stamp(
                {
                    "source_id": source_id,
                    "source_path": source_path,
                    "needle": needle,
                    "role": role,
                    "path_exists": str(path.exists()).lower(),
                    "needle_found": str(contains(path, needle)).lower(),
                    "status": "SOURCE_OK" if path.exists() and contains(path, needle) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def minimal_coupling_signature() -> list[dict[str, object]]:
    rows = [
        ("MUC2537_0_parent_data", "observed quotient before matter coupling", "Phi -> q(Phi)=Q_obs; O(q)=(M,g_obs,e_obs,omega_obs,theta)", "ordinary matter sees only observed quotient data plus ordinary material constants", "PROVISIONAL_PRIVATE_PARENT_RESTRICTION"),
        ("MUC2537_1_source_blind_functor", "source-blind ordinary matter functor", "Matter: Q_obs x SpeciesRep -> ActionDensity, with no Coeff_active_source(A) argument", "species labels specify representations/fields, not independent gravitational source strength", "CORE_RESTRICTION_DRAFT_READY"),
        ("MUC2537_2_single_measure_scale", "one observed measure and one common source scale", "S_m = integral mu_obs sum_A L_A(j^k Psi_A,e_obs,omega_obs,theta_A)", "Hilbert variation is label-additive and one common scale can be absorbed into kappa/G_N/GM", "PROVISIONAL_PRIVATE_PARENT_RESTRICTION"),
        ("MUC2537_3_theta_separation", "theta_A cannot hide a source-only multiplier", "theta_A is admissible only if it changes ordinary matter dynamics/standards or is retained as finite residual", "prevents w_A being renamed as a harmless material constant", "ADMISSIBILITY_RULE_REQUIRED"),
        ("MUC2537_4_hilbert_before_readout", "source current before arena/readout", "T_H := delta S_m/delta e_obs; K_arena, masks, Pi_gamma and GM calibration act downstream", "kills post-variation source-current rescaling tricks", "EXACT_GIVEN_RESTRICTED_READOUT_ORDER"),
        ("MUC2537_5_nonhilbert_policy", "non-Hilbert source currents retained unless proved silent", "J_source = T_H + J_NH + J_boundary + J_readout", "prevents the private restriction from sweeping hidden source tails away", "OPEN_PARALLEL_GATE_RETAINED"),
        ("MUC2537_6_verdict", "Minimal Universal Matter Coupling branch", "MUC2537_0 through MUC2537_5", "usable as private bookkeeping restriction, not a public derivation", "PRIVATE_BRANCH_READY_NOT_DERIVED"),
    ]
    return [
        {
            **no_claim(),
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
        ("DA2537_0_target", "derive Minimal Universal Matter Coupling", "Can q/flow structure force Matter: Q_obs x SpeciesRep -> ActionDensity with no active-source coefficient slot?", "TARGET_SHARPENED", "need to show ordinary species labels cannot define independent gravitational charge"),
        ("DA2537_1_quotient_descent", "quotient descent", "S_matter factors through q(Phi) and observed coframe data", "PARTIAL_WIN_NOT_ENOUGH", "descent removes representative-only fields, but species-indexed constants can still live in theta_A"),
        ("DA2537_2_naturality", "naturality over observed matter data", "natural functoriality forbids non-natural source coefficients only if Coeff_active_source is already absent", "CONDITIONAL_WIN_RESTATES_SIGNATURE", "must derive the allowed functor domain rather than assume it"),
        ("DA2537_3_double_accounting", "no duplicate inertial/source normalization", "a source-only w_A changes gravitational source without changing ordinary matter normalization", "STRONG_PHYSICAL_PRINCIPLE_NOT_FORMAL_DERIVATION", "needs parent admissibility principle or deeper Noether/source-charge identity"),
        ("DA2537_4_no_independent_grav_charge", "no independent gravitational source charge", "ordinary matter has one Hilbert/Noether stress source, not a second species charge for gravity", "BEST_DEEPER_DERIVATION_TARGET", "prove source charge equals Hilbert/Noether energy for all ordinary matter from parent symmetries"),
        ("DA2537_5_verdict", "derive source-blind signature now", "assemble quotient descent, naturality, no-double-counting and source-charge identity", "NOT_DERIVED_PROVISIONAL_RESTRICTION_RETAINED", "use the branch privately while attacking Noether/source-charge identity next"),
    ]
    return [
        {
            **no_claim(),
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
        ("ADM2537_0_private_restriction", "use Minimal Universal Matter Coupling privately", "ALLOW_AS_PRIVATE_WORKING_BRANCH", "lets the source-side GR route be developed without pretending source-only couplings are legal", "must be labelled provisional; not public evidence"),
        ("ADM2537_1_deeper_derivation", "derive restriction from Noether/source-charge identity", "SELECT_AS_NEXT_THEOREM_TARGET", "would make the local GR reduction derived rather than stipulated", "not closed here"),
        ("ADM2537_2_finite_fallback", "source-profile vector and L_source_GM bound", "RETAIN_IF_DERIVATION_FAILS", "keeps branch testable and honest", "less elegant; turns zero theorem into bounded residual"),
        ("ADM2537_3_decision", "2537 live branch decision", "DUAL_TRACK_PRIVATE_BRANCH_PLUS_DERIVATION", "use restriction for internal bookkeeping while immediately pursuing derivation", "do not claim local GR/Newton pass"),
    ]
    return [
        {
            **no_claim(),
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
        ("DGI2537_0_source_only_slot", "NoSourceOnlySpeciesSlot", "closed only inside the provisional restricted parent-action branch", "deeper derivation or public justification", "conditional_private_branch_only"),
        ("DGI2537_1_source_GM_zero", "epsilon_sigma_source_GM=0", "species-weight leak removed inside restricted branch", "source profile/GM same-frame calibration and hidden-current gates", "not_zero_yet"),
        ("DGI2537_2_source_side_GR", "ordinary matter source -> calibrated Hilbert current", "source-side common-mode theorem becomes cleaner", "non-Hilbert residual closure and left-hand EH/Newton operator", "conditional_source_side_only"),
        ("DGI2537_3_local_GR_Newton", "full local GR/Newton recovery", "not enough by itself", "EH/Newton left-hand limit, PPN/readout residuals, projector/domain terms", "blocked"),
        ("DGI2537_4_finite_fallback", "source-profile vector branch", "parked but not deleted", "needed if derivation/adoption or hidden-current gates fail", "retained_nonclaim"),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "gate": gate,
                "impact_if_private_restriction_used": impact,
                "still_missing": missing,
                "claim_status": status,
            }
        )
        for row_id, gate, impact, missing, status in rows
    ]


def noether_source_charge_target() -> list[dict[str, object]]:
    rows = [
        ("NSC2537_0_identity_target", "No independent gravitational source charge", "For ordinary matter, the generator that couples to local gravitational/coframe variation is the same Hilbert/Noether stress source obtained from S_matter; there is no separate SpeciesLabel -> gravitational charge map.", "NEXT_THEOREM_TO_PROVE", "would derive the source-blind functor restriction instead of adopting it"),
        ("NSC2537_1_required_symmetry", "observed-frame diffeomorphism/local-frame invariance", "Noether identity must bind source response to variation of e_obs/g_obs and ordinary matter fields.", "SOURCE_SYMMETRY_INPUT_REQUIRED", "need exact parent symmetry and variation order"),
        ("NSC2537_2_allowed_theta", "ordinary material constants", "theta_A may affect masses, charges, clock standards, interactions or representations, but then it enters ordinary matter tensors rather than a hidden source-only slot.", "ADMISSIBILITY_CLASSIFICATION_REQUIRED", "need a crisp test for source-only theta_A"),
        ("NSC2537_3_nonhilbert_guard", "non-Hilbert/boundary/readout current guard", "Any J_NH, J_boundary or J_readout term must be exact/projected-silent or finite-bounded.", "PARALLEL_GATE_OPEN", "source charge identity alone does not silence hidden currents"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "target_piece": piece,
            "statement": statement,
            "status": status,
            "effect_or_missing": effect,
        }
        for row_id, piece, statement, status, effect in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2537_0_sources", "source paths and needles valid", "PASS", "audit reproducible"),
        ("CG2537_1_signature_ready", "Minimal Universal Matter Coupling precisely written", "PASS", "private branch ready only"),
        ("CG2537_2_deeper_derivation", "source-blind signature derived from q/flow/Noether primitives now", "FAIL", "not derived"),
        ("CG2537_3_source_GM_zero", "epsilon_sigma_source_GM zero active", "FAIL", "source profile/GM/same-frame and hidden-current gates remain"),
        ("CG2537_4_local_GR_Newton", "full local GR/Newton recovery", "FAIL", "not enough; left-hand and readout residual gates remain"),
        ("CG2537_5_github_public_update", "safe to push as public evidence", "FAIL", "private fork-control checkpoint only"),
    ]
    return [
        stamp({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect})
        for row_id, gate, status, effect in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2537_0_no_public_derivation", "Refuse to call Minimal Universal Matter Coupling derived.", "Noether/source-charge identity remains open"),
        ("REF2537_1_no_local_gr", "Refuse to claim local GR/Newton pass from the private restriction.", "source_GM, non-Hilbert, EH/Newton and readout gates remain"),
        ("REF2537_2_no_species_handwave", "Refuse to dismiss species source weights by covariance alone.", "species-indexed constants can still be written unless parent object language excludes them"),
        ("REF2537_3_no_github", "Refuse GitHub/public claim framing.", "checkpoint is private branch control"),
    ]
    return [stamp({"row_id": row_id, "refusal": refusal, "reason": reason}) for row_id, refusal, reason in rows]


def next_target() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "NEXT2537_0_selected",
            "priority": "selected",
            "next_file": "2538-Y5-R2FR-Noether-source-charge-identity-or-nonHilbert-residual-row.md",
            "next_script": "scripts/Y5_R2FR_Noether_source_charge_identity_or_nonHilbert_residual_row_2538.py",
            "success_condition": "prove ordinary matter has no independent gravitational source charge beyond its Hilbert/Noether stress source; if not, retain explicit non-Hilbert/source-charge residual row",
            "fallback_condition": "do not use Minimal Universal Matter Coupling as a public derivation unless this identity closes",
        },
        {
            "row_id": "NEXT2537_1_branch_ledger",
            "priority": "parallel",
            "next_file": "2538b-Y5-R2FR-private-minimal-universal-matter-coupling-branch-ledger.md",
            "next_script": "scripts/Y5_R2FR_private_minimal_universal_matter_coupling_branch_ledger_2538b.py",
            "success_condition": "track all results that depend on the provisional parent-action restriction separately",
            "fallback_condition": "prevent provisional branch claims from contaminating public/local-GR gate status",
        },
        {
            "row_id": "NEXT2537_2_fallback",
            "priority": "fallback",
            "next_file": "2538c-Y5-R2FR-source-profile-vector-acquisition-if-source-charge-identity-fails.md",
            "next_script": "scripts/Y5_R2FR_source_profile_vector_acquisition_if_source_charge_identity_fails_2538c.py",
            "success_condition": "stage source-profile/source-weight vector rows with basis, units, frame and GM calibration",
            "fallback_condition": "keep every finite value nonclaim until same-frame projections and bounds are source-backed",
        },
    ]
    return [stamp(row) for row in rows]


def branch_copy_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, destination in BRANCH_COPIES.items():
        source = OUTPUTS[key]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": key,
                    "source_path": rel(source),
                    "destination_path": rel(destination),
                    "destination_exists": str(destination.exists()).lower(),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        return len(changed) == 0, "git modified-file count for formalization-workbench is 0" if not changed else f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("source_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() in {"true", "pass", "passed", "ready", "yes", "1"}:
                    offenders.append(f"{rel(path)}:{row_name}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append(stamp({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail}))

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2537_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2537_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2537_02_outputs_exist", all(path.exists() for path in generated), "all 2537 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2537_03_csv_parse", parse_ok, parse_detail)

    signature = {row["row_id"]: row["status"] for row in read_csv(outputs["signature"])}
    add("VAL2537_04_signature_written", signature.get("MUC2537_6_verdict") == "PRIVATE_BRANCH_READY_NOT_DERIVED", "Minimal Universal Matter Coupling branch recorded as private-not-derived")

    derivation = {row["row_id"]: row["result"] for row in read_csv(outputs["derivation"])}
    add("VAL2537_05_derivation_not_overclaimed", derivation.get("DA2537_5_verdict") == "NOT_DERIVED_PROVISIONAL_RESTRICTION_RETAINED", "deeper derivation remains unclaimed")

    adoption = {row["row_id"]: row["decision"] for row in read_csv(outputs["adoption"])}
    add("VAL2537_06_dual_track_decision", adoption.get("ADM2537_3_decision") == "DUAL_TRACK_PRIVATE_BRANCH_PLUS_DERIVATION", "dual-track private restriction plus derivation audit recorded")

    impact = {row["row_id"]: row["claim_status"] for row in read_csv(outputs["impact"])}
    add("VAL2537_07_local_gr_still_blocked", impact.get("DGI2537_3_local_GR_Newton") == "blocked", "full local GR/Newton gate remains blocked")

    noether = {row["row_id"]: row["status"] for row in read_csv(outputs["noether"])}
    add("VAL2537_08_noether_selected", noether.get("NSC2537_0_identity_target") == "NEXT_THEOREM_TO_PROVE", "Noether/source-charge identity selected as theorem target")

    claims = {row["row_id"]: row["gate_status"] for row in read_csv(outputs["claims"])}
    add("VAL2537_09_github_blocked", claims.get("CG2537_5_github_public_update") == "FAIL", "public GitHub evidence update remains blocked")

    next_rows = read_csv(outputs["next"])
    add("VAL2537_10_next_selected", any(row.get("row_id") == "NEXT2537_0_selected" and "2538" in row.get("next_file", "") for row in next_rows), "2538 Noether/source-charge target selected")

    copy_rows = read_csv(outputs["copies"])
    add("VAL2537_11_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2537_12_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2537_13_formalization_untouched", formal_ok, formal_detail)
    add("VAL2537_14_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2537_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2537 valid: Minimal Universal Matter Coupling is private-not-derived, deeper derivation remains open, Noether/source-charge identity selected next" if overall else "one or more validation gates failed",
            }
        )
    )
    return rows


def table(headers: list[str], rows: list[dict[str, str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(header, "").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    signature = read_csv(outputs["signature"])
    derivation = read_csv(outputs["derivation"])
    adoption = read_csv(outputs["adoption"])
    impact = read_csv(outputs["impact"])
    noether = read_csv(outputs["noether"])
    claims = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2537 - Parent Action Source-Blind Functor Signature Or Source-Profile Vector

**Current verdict:** the coupling throat is now controlled by a precise private branch, not by a vague hope.

The private branch is **Minimal Universal Matter Coupling**:

`Matter: Q_obs x SpeciesRep -> ActionDensity`

with one observed measure/source scale, one Hilbert source before readout, ordinary matter constants inside `theta_A`, and no independent `SpeciesLabel -> Coeff_active_source` object.

**Why this is not a public derivation:** this closes the source-only species coupling leak only inside the restricted branch. It is not yet derived from deeper MTS primitives. Quotient descent and naturality are partial wins, but they do not by themselves forbid species-indexed constants.

**Next purist target:** ordinary matter has no independent gravitational source charge beyond its Hilbert/Noether stress source.

## Minimal Universal Matter Coupling Signature

{table(["row_id", "signature_clause", "status", "function"], signature)}

## Derivation Audit

{table(["row_id", "derivation_target", "result", "obstruction_or_next"], derivation)}

## Adoption Decision Matrix

{table(["row_id", "option", "decision", "cost_or_guard"], adoption)}

## Downstream Gate Impact

{table(["row_id", "gate", "impact_if_private_restriction_used", "still_missing", "claim_status"], impact)}

## Noether / Source-Charge Target

{table(["row_id", "target_piece", "status", "effect_or_missing"], noether)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], claims)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["signature"])}`
- `{rel(outputs["derivation"])}`
- `{rel(outputs["adoption"])}`
- `{rel(outputs["impact"])}`
- `{rel(outputs["noether"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is progress, but not a victory lap. The source-side coupling problem is now sharply framed: either derive the Noether/source-charge identity and make the minimal coupling branch feel inevitable, or admit the finite source-profile/non-Hilbert residuals explicitly. That is much better than hand-waving the coupling away.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    write_csv(OUTPUTS["signature"], minimal_coupling_signature())
    write_csv(OUTPUTS["derivation"], derivation_audit())
    write_csv(OUTPUTS["adoption"], adoption_decision_matrix())
    write_csv(OUTPUTS["impact"], downstream_gate_impact())
    write_csv(OUTPUTS["noether"], noether_source_charge_target())
    write_csv(OUTPUTS["claims"], claim_gates())
    write_csv(OUTPUTS["refusal"], refusal_runner())
    write_csv(OUTPUTS["next"], next_target())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
