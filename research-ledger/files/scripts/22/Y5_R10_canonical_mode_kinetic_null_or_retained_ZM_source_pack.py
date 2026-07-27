from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "720-Y5-R10-canonical-mode-kinetic-null-or-retained-ZM-source-pack.md"
NEXT_TARGET = "721-Y5-R10-parent-ZM-source-hunt-or-canonical-mode-template-fill.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "719_doc": {
        "path": POST_CHECKPOINT / "719-Y5-R10-AEH-gradient-canonical-projection-zero-or-mode-source-pack.md",
        "note": "projection-zero target and retained charge formula",
    },
    "719_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_719_VALIDATION.csv",
        "note": "prior checkpoint validation",
    },
    "719_mode_source_pack": {
        "path": RESIDUALS / "P8_Y5_R10_719_MODE_SOURCE_PACK.csv",
        "note": "missing Z/M/E mode source pack from 719",
    },
    "719_canonical_mode_derivation": {
        "path": RESIDUALS / "P8_Y5_R10_719_CANONICAL_MODE_DERIVATION.csv",
        "note": "canonical mode formulas from 719",
    },
    "719_decision": {
        "path": RESIDUALS / "P8_Y5_R10_719_ZERO_OR_MODE_SOURCE_DECISION.csv",
        "note": "719 decision selecting the kinetic/null-mode gate",
    },
    "715_pack": {
        "path": RESIDUALS / "P8_Y5_R10_715_MINIMUM_EXECUTABLE_COEFFICIENT_PACK.csv",
        "note": "minimum local scalar coefficient pack",
    },
    "714_queue": {
        "path": RESIDUALS / "P8_Y5_R10_714_RETAINED_BRANCH_SOURCE_QUEUE.csv",
        "note": "retained branch source queue",
    },
    "714_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_714_VALIDATION.csv",
        "note": "714 validation",
    },
    "708_contract": {
        "path": RESIDUALS / "P8_Y5_R10_708_SCALAR_CLASS_SOURCE_ROW_CONTRACT.csv",
        "note": "scalar/class source row contract",
    },
    "708_expansion": {
        "path": RESIDUALS / "P8_Y5_R10_708_LOCAL_EXPANSION_MAP.csv",
        "note": "symbolic local expansion and mode map",
    },
    "708_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_708_VALIDATION.csv",
        "note": "708 validation",
    },
    "716_doc": {
        "path": POST_CHECKPOINT / "716-Y5-R10-matter-coupling-source-charge-derivation-or-free-coefficient-lock.md",
        "note": "source charge and b_A,I definition",
    },
    "717_conformal": {
        "path": RESIDUALS / "P8_Y5_R10_717_CONFORMAL_DERIVATION.csv",
        "note": "observed/Einstein-frame charge transfer",
    },
    "718_variation": {
        "path": RESIDUALS / "P8_Y5_R10_718_AEH_VARIATION_DERIVATION.csv",
        "note": "AEH prefactor gradient and A_a source",
    },
}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def csv_contains(path: Path, *needles: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def all_valid_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows:
            continue
        if "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def under_post_checkpoint(paths: list[Path]) -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
    return True


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "role": info["note"],
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
        for key, info in SOURCES.items()
    ]

    kinetic_null_theorem_audit = [
        {
            "audit_id": "KNT720_0_field_space",
            "clause": "retained scalar/class field space",
            "required_statement": "the parent action supplies an ordered local field multiplet u^I and background u0",
            "current_status": "missing_field_list_and_background",
            "derivation_effect": "Z_IJ, M2_IJ, a_I, and b_A,I have no claim-ready index convention",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_mode_source_pack", "715_pack", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "KNT720_1_kinetic_metric",
            "clause": "kinetic metric",
            "required_statement": "Z_IJ(u0) is sourced as a matrix or a parent-signed theorem says it vanishes as gauge/topology/constraint",
            "current_status": "missing_Z_IJ",
            "derivation_effect": "cannot separate propagating modes from gauge, null, constrained, or pathological directions",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "714_queue"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "KNT720_2_rank_signature",
            "clause": "rank and signature classification",
            "required_statement": "rank(Z_phys), positive subspace, null/gauge basis, auxiliary constraints, and ghost directions are classified",
            "current_status": "missing_rank_signature_gauge_null_classification",
            "derivation_effect": "rank(P_phys)=0 cannot be asserted",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "719_mode_source_pack", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "KNT720_3_Z_zero_guard",
            "clause": "zero kinetic metric guard",
            "required_statement": "Z_IJ=0 is harmless only if the algebraic/constraint equation removes the field without finite non-GR contact or boundary residual",
            "current_status": "Z_IJ_zero_not_automatically_harmless",
            "derivation_effect": "prevents smuggling a missing kinetic term into a local-GR proof",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_contract", "714_queue"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "KNT720_4_mass_matrix",
            "clause": "mass/range matrix",
            "required_statement": "M2_IJ is sourced in the same field-space convention as Z_IJ and projected to the physical subspace",
            "current_status": "missing_M2_IJ",
            "derivation_effect": "cannot distinguish exact no-mode from finite-range retained scalar physics",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "KNT720_5_canonical_basis",
            "clause": "canonical eigenmodes",
            "required_statement": "E_a^I solves the generalized Z/M eigenproblem and is normalized on the physical subspace",
            "current_status": "missing_E_a_I",
            "derivation_effect": "A_a, B_Aa, Q_Aa, alpha(lambda), and PPN residuals cannot be evaluated",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_canonical_mode_derivation", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "KNT720_6_source_orthogonality",
            "clause": "source-current silence",
            "required_statement": "J_I, a_I, and b_A,I annihilate every null/constrained direction or the integrated-out branch leaves only calibrated constants",
            "current_status": "not_parent_signed",
            "derivation_effect": "a null or auxiliary direction can still generate a local residual if its source equation is not solved",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal", "718_variation"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "KNT720_7_boundary_silence",
            "clause": "boundary/topological silence",
            "required_statement": "boundary terms, topological sectors, and local projection terms carry no source stress or fifth-force residual",
            "current_status": "not_parent_signed",
            "derivation_effect": "topological/no-bulk-mode language is insufficient unless boundary currents are silent",
            "valid_for_claim": "false",
            "source_paths": source_path_string("714_queue", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "KNT720_8_no_mode_theorem",
            "clause": "exact no local scalar mode theorem",
            "required_statement": "rank(P_phys)=0 after quotienting gauge/topology/constraints, with no residual contact/current term",
            "current_status": "fail_current_corpus",
            "derivation_effect": "local-GR scalar silence is not claimable from current files",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "715_pack", "714_queue"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "KNT720_9_heavy_mass_guard",
            "clause": "heavy mass is not exact GR",
            "required_statement": "large m_a or small lambda_a is a bound/scoring route, not a proof that GR is exactly recovered",
            "current_status": "guard_active",
            "derivation_effect": "keeps empirical suppression distinct from derivational closure",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "KNT720_10_ghost_guard",
            "clause": "ghost/negative kinetic rejection",
            "required_statement": "negative kinetic directions are removed by constraints or the branch is pathological, not evidence for local GR",
            "current_status": "guard_active",
            "derivation_effect": "prevents a bad kinetic signature being counted as a pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    zm_canonicalization_derivation = [
        {
            "step_id": "ZMD720_0_perturbation",
            "object": "field perturbations",
            "equation": "u^I(x)=u0^I+delta u^I(x)",
            "result": "local scalar/class fluctuations must be indexed before any mode statement is meaningful",
            "status": "definition_contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "ZMD720_1_quadratic_action",
            "object": "local quadratic scalar branch",
            "equation": "S_2=int sqrt(-g)[-1/2 Z_IJ nabla delta u^I nabla delta u^J - 1/2 M2_IJ delta u^I delta u^J + J_I delta u^I]",
            "result": "Z_IJ decides whether fields propagate; M2_IJ decides range after canonicalization",
            "status": "derived_shape_from_contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_canonical_mode_derivation", "708_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "ZMD720_2_constraint_split",
            "object": "gauge/null/auxiliary split",
            "equation": "delta u^I = G_alpha^I xi^alpha + N_r^I c^r + P_phys^I{}_a s^a",
            "result": "only the quotient physical component s^a may mediate finite-range local forces",
            "status": "conditional_formula",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "ZMD720_3_physical_projector",
            "object": "physical projector",
            "equation": "P_phys = projector onto non-gauge, non-null, non-topological, positive-kinetic scalar directions",
            "result": "the local-GR theorem target is rank(P_phys)=0, not merely missing or small coefficients",
            "status": "theorem_target",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "719_mode_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "ZMD720_4_generalized_eigenproblem",
            "object": "canonical modes",
            "equation": "(P^T M2 P) E_a = m_a^2 (P^T Z P) E_a, with E_a^T Z E_b = delta_ab",
            "result": "canonical eigenvectors E_a^I and masses m_a are executable only after Z/M are sourced",
            "status": "conditional_formula",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_canonical_mode_derivation", "708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "ZMD720_5_mode_charges",
            "object": "projected effective charges",
            "equation": "A_a=E_a^I a_I; B_Aa=E_a^I b_A,I; Q_Aa=N_frame(B_Aa-A_a/2) in D=4",
            "result": "local tests see canonical projected charges, not raw field-space coefficients",
            "status": "derived_from_716_717_718_719",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal", "718_variation", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "ZMD720_6_exact_silence_condition",
            "object": "local scalar silence",
            "equation": "rank(P_phys)=0 OR Q_Aa=0 for every relevant body A and every physical finite-range mode a",
            "result": "this is the exact local branch target before claiming GR/Newton/PPN recovery",
            "status": "theorem_target_not_met",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "ZMD720_7_auxiliary_contact_guard",
            "object": "integrating out non-propagating directions",
            "equation": "delta S/delta c^r=0 must imply c^r=c^r_calibrated with Delta S_eff containing no non-GR local observable",
            "result": "auxiliary is not automatically safe; the source equation must be solved or bounded",
            "status": "guard",
            "valid_for_claim": "false",
            "source_paths": source_path_string("714_queue", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    retained_zm_source_pack = [
        {
            "pack_id": "ZMS720_0_field_list",
            "symbol": "u^I",
            "definition": "ordered retained scalar/class field coordinates at the local branch",
            "required_input": "field names, background u0, units, field-space convention",
            "current_value_or_status": "MISSING_FIELD_LIST",
            "priority": "P0",
            "unlocks": "index convention for Z_IJ, M2_IJ, a_I, b_A,I",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_mode_source_pack", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "ZMS720_1_kinetic_metric",
            "symbol": "Z_IJ(u0)",
            "definition": "field-space kinetic metric/Hessian multiplying nabla delta u^I nabla delta u^J",
            "required_input": "numeric/symbolic matrix plus source path and units",
            "current_value_or_status": "MISSING_KINETIC_METRIC",
            "priority": "P0",
            "unlocks": "rank/signature and physical projector",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "714_queue"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "ZMS720_2_rank_signature",
            "symbol": "rank(Z), sig(Z)",
            "definition": "rank and positive/null/negative classification after gauge quotient",
            "required_input": "rank, null vectors, ghost rejection/projection statement",
            "current_value_or_status": "MISSING_RANK_SIGNATURE_CLASSIFICATION",
            "priority": "P0",
            "unlocks": "no-mode theorem or retained physical scalar branch",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_mode_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "ZMS720_3_gauge_null_basis",
            "symbol": "G_alpha^I, N_r^I",
            "definition": "gauge/topological/null/constrained directions in field space",
            "required_input": "basis vectors and proof they are non-observable or constrained",
            "current_value_or_status": "MISSING_GAUGE_NULL_BASIS",
            "priority": "P0",
            "unlocks": "quotient projector and source orthogonality checks",
            "valid_for_claim": "false",
            "source_paths": source_path_string("714_queue", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "ZMS720_4_physical_projector",
            "symbol": "P_phys",
            "definition": "projector onto physical scalar mode subspace after quotient/constraints",
            "required_input": "projector or parent-signed theorem rank(P_phys)=0",
            "current_value_or_status": "MISSING_PHYSICAL_PROJECTOR",
            "priority": "P0",
            "unlocks": "A_a projection zero and no-mode theorem",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "719_mode_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "ZMS720_5_mass_matrix",
            "symbol": "M2_IJ",
            "definition": "local mass/range matrix in the same field-space convention as Z_IJ",
            "required_input": "second variation of V_eff or full local operator Hessian",
            "current_value_or_status": "MISSING_MASS_MATRIX",
            "priority": "P1",
            "unlocks": "mode masses, ranges, and R10 lambda axis",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "ZMS720_6_canonical_modes",
            "symbol": "E_a^I",
            "definition": "canonical eigenmode basis normalized by Z on the physical subspace",
            "required_input": "generalized eigenvectors, normalization, source path",
            "current_value_or_status": "MISSING_CANONICAL_DIAGONALIZATION",
            "priority": "P0",
            "unlocks": "A_a, B_Aa, Q_Aa, PPN, WEP, R10",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_canonical_mode_derivation", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "ZMS720_7_mode_masses",
            "symbol": "m_a^2, lambda_a",
            "definition": "canonical mode masses and ranges",
            "required_input": "m_a^2 from Z/M eigenproblem and lambda_a convention",
            "current_value_or_status": "MISSING_MODE_MASS_AND_RANGE",
            "priority": "P1",
            "unlocks": "R10 alpha(lambda) and range suppression tests",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion", "719_canonical_mode_derivation"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "ZMS720_8_AEH_projection",
            "symbol": "A_a",
            "definition": "E_a^I a_I",
            "required_input": "a_I and canonical mode basis",
            "current_value_or_status": "MISSING_AEH_CANONICAL_PROJECTION",
            "priority": "P0",
            "unlocks": "AEH/frame part of scalar source charge",
            "valid_for_claim": "false",
            "source_paths": source_path_string("718_variation", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "ZMS720_9_matter_projection",
            "symbol": "B_Aa",
            "definition": "E_a^I b_A,I",
            "required_input": "source/test body charge gradients and canonical modes",
            "current_value_or_status": "MISSING_MATTER_CHARGE_PROJECTION",
            "priority": "P1",
            "unlocks": "composition dependence and WEP residuals",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "ZMS720_10_effective_charge",
            "symbol": "Q_Aa",
            "definition": "N_frame(B_Aa-A_a/2) in D=4 observed-frame branch",
            "required_input": "N_frame, A_a, B_Aa, frame convention",
            "current_value_or_status": "MISSING_EFFECTIVE_CANONICAL_CHARGE",
            "priority": "P1",
            "unlocks": "R10, PPN, WEP, clocks, orbital residuals",
            "valid_for_claim": "false",
            "source_paths": source_path_string("717_conformal", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    mode_branch_matrix = [
        {
            "branch_id": "MBM720_0_no_physical_mode",
            "branch": "no local scalar mode",
            "condition": "rank(P_phys)=0 after quotienting gauge/topology/constraints and no contact/current residual remains",
            "local_effect": "A_a, B_Aa, and Q_Aa are absent",
            "status": "not_parent_signed",
            "claim_effect": "would be the clean GR-reduction route if proved",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "MBM720_1_null_gauge_projected",
            "branch": "null/gauge projected scalar",
            "condition": "mode lies entirely in ker(Dq) or a sourced gauge/topological null space and all sources annihilate it",
            "local_effect": "no finite-range scalar force from that direction",
            "status": "conditional_not_signed",
            "claim_effect": "partial closure only for the signed directions",
            "valid_for_claim": "false",
            "source_paths": source_path_string("714_queue", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "MBM720_2_auxiliary_contact",
            "branch": "auxiliary/algebraic scalar",
            "condition": "Z direction is constrained but sourced by J_I, a_I, or b_A,I",
            "local_effect": "no propagating Yukawa mode, but possible contact or renormalized local residual",
            "status": "unresolved_contact_term",
            "claim_effect": "cannot be counted as exact local GR until the constraint equation is solved",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "MBM720_3_positive_retained",
            "branch": "positive physical retained mode",
            "condition": "rank(P_phys)>0 with positive kinetic signature",
            "local_effect": "finite-range scalar mode must be scored with Q_Aa and lambda_a",
            "status": "selected_fallback_if_zero_proof_fails",
            "claim_effect": "no GR/local pass; empirical scoring required",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_mode_source_pack", "708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "MBM720_4_heavy_retained",
            "branch": "heavy short-range retained mode",
            "condition": "rank(P_phys)>0 and lambda_a is very small",
            "local_effect": "suppressed at long range, still a bound/scoring route",
            "status": "guarded_not_exact_zero",
            "claim_effect": "may pass an empirical bound, but does not prove exact GR reduction",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "MBM720_5_ghost",
            "branch": "negative kinetic/ghost direction",
            "condition": "negative eigenvalue remains in the physical quotient",
            "local_effect": "pathology unless removed by a signed constraint/gauge theorem",
            "status": "rejected_as_evidence",
            "claim_effect": "not a local-GR pass and not a healthy retained branch",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "MBM720_6_charge_orthogonality",
            "branch": "physical mode but zero charge",
            "condition": "Q_Aa=0 for all relevant sources/tests and every physical mode",
            "local_effect": "physical scalar exists but is locally silent at tested order",
            "status": "not_derived",
            "claim_effect": "would still need derivative/loop/higher-order residual checks",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "716_doc", "717_conformal"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    observable_unlock_map = [
        {
            "arena_id": "OUM720_0_Newton",
            "arena": "Newtonian/local-GR limit",
            "needed_ZM_input": "rank(P_phys), Q_Aa, lambda_a, measured-G normalization",
            "current_status": "blocked_until_no_mode_or_ZM_charge_source",
            "claim_effect": "no Newton/local-GR pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "OUM720_1_R10",
            "arena": "short-range fifth force",
            "needed_ZM_input": "alpha_AB,a(lambda_a)=Q_Aa Q_Ba with real bound curve and sourced Q/lambda",
            "current_status": "blocked_until_ZM_Q_lambda_and_real_bounds",
            "claim_effect": "no R10 pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "OUM720_2_PPN",
            "arena": "PPN gamma/beta",
            "needed_ZM_input": "universal/canonical coupling strength and derivative of projected charge",
            "current_status": "blocked_until_QAa_and_derivatives_sourced",
            "claim_effect": "no PPN pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("717_conformal", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "OUM720_3_WEP",
            "arena": "composition dependence",
            "needed_ZM_input": "B_Aa differences across materials plus A_a common shift",
            "current_status": "blocked_until_material_charge_projection_sourced",
            "claim_effect": "no WEP pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "OUM720_4_clocks",
            "arena": "clock/fine-structure drift",
            "needed_ZM_input": "projected charge dependence of clock transition constants and local/time gradients",
            "current_status": "blocked_until_mode_projection_and_source_current_sourced",
            "claim_effect": "no clock pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "718_variation"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "OUM720_5_orbital",
            "arena": "orbital/solar-system residuals",
            "needed_ZM_input": "range-dependent scalar correction and source/test charges for macroscopic bodies",
            "current_status": "blocked_until_retained_mode_amplitude_and_range_sourced",
            "claim_effect": "no orbital pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    zero_or_retain_decision = [
        {
            "decision_id": "D720_0_kinetic_no_mode",
            "target": "rank(P_phys)=0 with no contact/current residual",
            "result": "not_available_current_corpus",
            "reason": "Z_IJ, rank/signature, gauge/null basis, and constraint-source equations are missing",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D720_1_charge_silence",
            "target": "Q_Aa=0 for all relevant bodies and modes",
            "result": "not_available_current_corpus",
            "reason": "E_a^I, A_a, B_Aa, and N_frame are not executable",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal", "719_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D720_2_retained_ZM",
            "target": "retained Z/M canonical mode pack",
            "result": "selected_current_route",
            "reason": "zero proof cannot honestly close without parent-sourced Z/M/projector data",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("714_queue", "715_pack", "719_mode_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    bound_or_derive_queue = [
        {
            "queue_id": "BDQ720_0_parent_action",
            "target": "parent scalar/class action in local branch",
            "preferred_route": "derive exact Z_IJ and M2_IJ by second variation of the parent action",
            "fallback_route": "write a canonical template with symbolic Z/M entries and keep all local tests nonclaim",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_contract", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ720_1_rank_null",
            "target": "rank/null/gauge classification",
            "preferred_route": "prove all scalar/class directions are gauge/topological/constrained and source-silent",
            "fallback_route": "construct P_phys and retain every positive physical mode",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "714_queue"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ720_2_mass_modes",
            "target": "M2_IJ and canonical eigenmodes",
            "preferred_route": "derive mass matrix from V_eff/local operator Hessian and diagonalize with Z",
            "fallback_route": "record MISSING_MASS_MATRIX and block R10/PPN until sourced",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("708_expansion", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ720_3_source_current",
            "target": "source-current orthogonality/contact cleanup",
            "preferred_route": "show J_I, a_I, b_A,I vanish on constrained/null directions or integrate out into calibrated constants",
            "fallback_route": "retain explicit Q_Aa rows and score them against local bounds",
            "priority": "P1",
            "next_artifact": "after_721_source_current_orthogonality_or_retained_QAa_score_pack",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal", "718_variation"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    claim_gate_evaluation = [
        {
            "gate_id": "CG720_0_prior_719",
            "gate": "prior projection checkpoint",
            "observed_state": "719 validation clean and selected 720",
            "result": "pass_structure",
            "claim_effect": "safe to build Z/M gate without promoting claims",
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_validation", "719_decision"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG720_1_kinetic_no_mode",
            "gate": "rank(P_phys)=0 no-mode theorem",
            "observed_state": "Z_IJ, rank/signature, and constraints missing",
            "result": "fail_blocked",
            "claim_effect": "no local scalar silence claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "719_mode_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG720_2_canonical_modes",
            "gate": "E_a^I and m_a executable",
            "observed_state": "M2_IJ and canonical diagonalization missing",
            "result": "fail_blocked",
            "claim_effect": "no alpha(lambda), PPN, WEP, clock, or orbital score",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "708_expansion"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG720_3_Z_zero_guard",
            "gate": "missing/zero kinetic not counted as no-mode",
            "observed_state": "explicit guard row active",
            "result": "pass_guard",
            "claim_effect": "prevents fake local-GR closure",
            "valid_for_claim": "false",
            "source_paths": source_path_string("714_queue"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG720_4_ghost_guard",
            "gate": "ghost branch rejected",
            "observed_state": "negative kinetic cannot be evidence unless projected out",
            "result": "pass_guard",
            "claim_effect": "bad signatures remain pathology, not success",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG720_5_next_target",
            "gate": "next practical target",
            "observed_state": NEXT_TARGET,
            "result": "pass_structure",
            "claim_effect": "source/derive parent Z/M before further scoring",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "719_mode_source_pack"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_kinetic_null_no_mode_proof_failed_retained_ZM_source_pack_written_nonclaim",
            "claim_ceiling": "canonical_mode_contract_only_no_local_GR_Newton_PPN_R10_WEP_clock_or_orbital_claim",
            "main_result": "the exact zero route is rank(P_phys)=0 with no contact/current residual, or Q_Aa=0 on every physical mode",
            "derived_contract": "S_2 fixes Z/M/projector/canonical-mode requirements; missing Z is not a theorem",
            "retained_formula": "A_a=E_a^I a_I; B_Aa=E_a^I b_A,I; Q_Aa=N_frame(B_Aa-A_a/2)",
            "remaining_blocker": "parent-sourced Z_IJ, rank/signature, gauge/null basis, M2_IJ, E_a^I, lambda_a, A_a, B_Aa",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("719_doc", "715_pack", "714_queue"),
            "generated_utc": GENERATED_UTC,
        }
    ]

    outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_720_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "role", "valid_for_claim", "generated_utc"],
        ),
        "kinetic_null_theorem_audit": (
            RESIDUALS / "P8_Y5_R10_720_KINETIC_NULL_THEOREM_AUDIT.csv",
            kinetic_null_theorem_audit,
            [
                "audit_id",
                "clause",
                "required_statement",
                "current_status",
                "derivation_effect",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "zm_canonicalization_derivation": (
            RESIDUALS / "P8_Y5_R10_720_ZM_CANONICALIZATION_DERIVATION.csv",
            zm_canonicalization_derivation,
            ["step_id", "object", "equation", "result", "status", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "retained_zm_source_pack": (
            RESIDUALS / "P8_Y5_R10_720_RETAINED_ZM_SOURCE_PACK.csv",
            retained_zm_source_pack,
            [
                "pack_id",
                "symbol",
                "definition",
                "required_input",
                "current_value_or_status",
                "priority",
                "unlocks",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "mode_branch_matrix": (
            RESIDUALS / "P8_Y5_R10_720_MODE_BRANCH_MATRIX.csv",
            mode_branch_matrix,
            [
                "branch_id",
                "branch",
                "condition",
                "local_effect",
                "status",
                "claim_effect",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "observable_unlock_map": (
            RESIDUALS / "P8_Y5_R10_720_OBSERVABLE_UNLOCK_MAP.csv",
            observable_unlock_map,
            [
                "arena_id",
                "arena",
                "needed_ZM_input",
                "current_status",
                "claim_effect",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "zero_or_retain_decision": (
            RESIDUALS / "P8_Y5_R10_720_ZERO_OR_RETAIN_DECISION.csv",
            zero_or_retain_decision,
            ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "bound_or_derive_queue": (
            RESIDUALS / "P8_Y5_R10_720_BOUND_OR_DERIVE_QUEUE.csv",
            bound_or_derive_queue,
            [
                "queue_id",
                "target",
                "preferred_route",
                "fallback_route",
                "priority",
                "next_artifact",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "claim_gate_evaluation": (
            RESIDUALS / "P8_Y5_R10_720_CLAIM_GATE_EVALUATION.csv",
            claim_gate_evaluation,
            ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_720_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            [
                "status",
                "claim_ceiling",
                "main_result",
                "derived_contract",
                "retained_formula",
                "remaining_blocker",
                "next_target",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
    }

    for path, rows, fields in outputs.values():
        write_csv(path, rows, fields)

    generated_paths = [path for path, _, _ in outputs.values()]
    formalization_count = formalization_changed_after_cutoff()
    validations = [
        {
            "check_id": "V720_0_source_paths_exist",
            "result": "pass" if all(info["path"].exists() for info in SOURCES.values()) else "fail",
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "V720_1_prior_719_clean",
            "result": "pass" if prior_validation_clean(SOURCES["719_validation"]["path"]) else "fail",
            "detail": "719 validation has no failures",
        },
        {
            "check_id": "V720_2_719_selected_720",
            "result": "pass" if csv_contains(SOURCES["719_decision"]["path"], "720-Y5-R10-canonical-mode-kinetic-null-or-retained-ZM-source-pack.md") else "fail",
            "detail": "719 decision selected the kinetic/null-mode gate",
        },
        {
            "check_id": "V720_3_Z_M_E_missing_confirmed",
            "result": "pass"
            if (
                csv_contains(
                    SOURCES["715_pack"]["path"],
                    "MISSING_KINETIC_METRIC",
                    "MISSING_MASS_MATRIX",
                    "MISSING_CANONICAL_DIAGONALIZATION",
                )
                and csv_contains(
                    SOURCES["719_mode_source_pack"]["path"],
                    "MISSING_KINETIC_METRIC",
                    "MISSING_MASS_MATRIX",
                    "MISSING_CANONICAL_DIAGONALIZATION",
                )
            )
            else "fail",
            "detail": "715/719 confirm Z/M/E remain missing",
        },
        {
            "check_id": "V720_4_no_mode_not_promoted",
            "result": "pass" if any(row["current_status"] == "fail_current_corpus" for row in kinetic_null_theorem_audit) else "fail",
            "detail": "no-mode theorem remains blocked",
        },
        {
            "check_id": "V720_5_missing_Z_guard",
            "result": "pass" if any(row["current_status"] == "missing_Z_IJ" for row in kinetic_null_theorem_audit) else "fail",
            "detail": "missing Z is recorded explicitly",
        },
        {
            "check_id": "V720_6_Z_zero_not_harmless_guard",
            "result": "pass" if any(row["current_status"] == "Z_IJ_zero_not_automatically_harmless" for row in kinetic_null_theorem_audit) else "fail",
            "detail": "zero kinetic is not promoted to exact no-mode",
        },
        {
            "check_id": "V720_7_ghost_rejected",
            "result": "pass" if any(row["status"] == "rejected_as_evidence" for row in mode_branch_matrix) else "fail",
            "detail": "ghost/negative kinetic branch is not evidence",
        },
        {
            "check_id": "V720_8_retained_ZM_pack_complete",
            "result": "pass"
            if {"Z_IJ(u0)", "M2_IJ", "P_phys", "E_a^I", "Q_Aa"}.issubset({row["symbol"] for row in retained_zm_source_pack})
            else "fail",
            "detail": f"retained_pack_rows={len(retained_zm_source_pack)}",
        },
        {
            "check_id": "V720_9_local_arenas_blocked",
            "result": "pass" if all(row["current_status"].startswith("blocked_") for row in observable_unlock_map) else "fail",
            "detail": "all local observable arenas remain blocked",
        },
        {
            "check_id": "V720_10_next_target_selected",
            "result": "pass" if all(row["next_action"] == NEXT_TARGET for row in zero_or_retain_decision) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V720_11_no_claim_rows_promoted",
            "result": "pass" if all_valid_false(generated_paths) else "fail",
            "detail": "all generated rows with valid_for_claim remain false",
        },
        {
            "check_id": "V720_12_outputs_scoped",
            "result": "pass" if under_post_checkpoint([OUTPUT_DOC, *generated_paths]) else "fail",
            "detail": "all outputs under post-checkpoint-work",
        },
        {
            "check_id": "V720_13_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V720_14_nonclaim_status",
            "result": "pass" if "nonclaim" in nonclaim_summary[0]["status"] else "fail",
            "detail": "claim ceiling blocks local-GR/Newton/PPN/R10/WEP/clock/orbital claims",
        },
        {
            "check_id": "V720_15_source_register_written",
            "result": "pass" if len(source_register) >= 10 else "fail",
            "detail": f"source_rows={len(source_register)}",
        },
        {
            "check_id": "V720_16_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]

    validation_path = RESIDUALS / "P8_Y5_BRR545_720_VALIDATION.csv"
    write_csv(validation_path, validations, ["check_id", "result", "detail"])

    doc = f"""# 720 - Y5 R10 Canonical Mode Kinetic Null Or Retained ZM Source Pack

## Summary

This checkpoint attacks the best derivation route left after 719: prove there is no physical local scalar mode, or retain the canonical `Z/M` mode pack honestly.

The exact local-zero target is now:

`rank(P_phys)=0` after quotienting gauge/topology/constraints **and** after proving no source-current/contact/boundary residual remains.

Equivalently, if a physical mode exists, local silence requires:

`Q_Aa=0` for every relevant source/test body `A` and every physical finite-range mode `a`.

The current corpus cannot claim either theorem. `Z_IJ`, rank/signature, gauge/null basis, `M2_IJ`, `E_a^I`, `lambda_a`, `A_a`, and `B_Aa` remain missing. The retained D=4 charge stays:

`A_a=E_a^I a_I`, `B_Aa=E_a^I b_A,I`, `Q_Aa=N_frame(B_Aa-A_a/2)`.

| Field | Value |
| --- | --- |
| Generated UTC | `{GENERATED_UTC}` |
| Claim status | nonclaim/private checkpoint |
| Next target | `{NEXT_TARGET}` |

## Kinetic Null Theorem Audit

{markdown_table(kinetic_null_theorem_audit, ["audit_id", "clause", "current_status", "derivation_effect", "valid_for_claim"])}

## ZM Canonicalization Derivation

{markdown_table(zm_canonicalization_derivation, ["step_id", "object", "equation", "result", "status", "valid_for_claim"])}

## Retained ZM Source Pack

{markdown_table(retained_zm_source_pack, ["pack_id", "symbol", "current_value_or_status", "priority", "unlocks", "valid_for_claim"])}

## Mode Branch Matrix

{markdown_table(mode_branch_matrix, ["branch_id", "branch", "condition", "status", "claim_effect", "valid_for_claim"])}

## Observable Unlock Map

{markdown_table(observable_unlock_map, ["arena_id", "arena", "needed_ZM_input", "current_status", "claim_effect", "valid_for_claim"])}

## Zero Or Retain Decision

{markdown_table(zero_or_retain_decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Bound Or Derive Queue

{markdown_table(bound_or_derive_queue, ["queue_id", "target", "preferred_route", "fallback_route", "priority", "next_artifact", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(claim_gate_evaluation, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "remaining_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Verdict

This route is useful because it sharpens what has to be proved. A missing kinetic metric is not the same as no physics. A zero kinetic direction is not automatically harmless. A heavy mode is not exact GR. A ghost is not a win. The only clean local-GR scalar exit is a parent-signed quotient/constraint theorem with no residual current, or a sourced canonical-mode calculation showing all physical `Q_Aa` vanish. Current files do not yet supply that, so the next move is a targeted parent `Z/M` source hunt or canonical template fill.
"""

    OUTPUT_DOC.write_text(doc, encoding="utf-8")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {validation_path}")
    print(f"validation_passes={sum(row['result'] == 'pass' for row in validations)}/{len(validations)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
