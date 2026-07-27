from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "721-Y5-R10-parent-ZM-source-hunt-or-canonical-mode-template-fill.md"
NEXT_TARGET = "722-Y5-R10-affine-no-pole-map-to-ZM-template-or-retained-single-X-mode.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "720_doc": {
        "path": POST_CHECKPOINT / "720-Y5-R10-canonical-mode-kinetic-null-or-retained-ZM-source-pack.md",
        "note": "immediate handoff: missing Z/M/projector/canonical-mode gate",
        "needles": ["rank(P_phys)=0", "Z_IJ", "M2_IJ", "721-Y5-R10-parent-ZM-source-hunt-or-canonical-mode-template-fill.md"],
    },
    "720_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_720_VALIDATION.csv",
        "note": "prior validation",
        "needles": ["V720_3_Z_M_E_missing_confirmed", "pass", "V720_13_formalization_workbench_untouched"],
    },
    "720_retained_zm_pack": {
        "path": RESIDUALS / "P8_Y5_R10_720_RETAINED_ZM_SOURCE_PACK.csv",
        "note": "retained Z/M source pack to be filled or blocked",
        "needles": ["Z_IJ(u0)", "M2_IJ", "E_a^I", "MISSING_CANONICAL_DIAGONALIZATION"],
    },
    "511_fixed_point_ansatz": {
        "path": POST_CHECKPOINT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "note": "multi-field local-GR fixed-point action contract",
        "needles": ["S_extra", "G_AB(Phi)", "Hessian(V)>0", "candidate action contract"],
    },
    "564_hessian_extraction": {
        "path": POST_CHECKPOINT / "564-Y5-R10-parent-Hessian-source-zero-attempt.md",
        "note": "single-X parent Hessian extraction formulas",
        "needles": ["Z_X", "M_X^2", "second-variation residues", "no explicit parent Lagrangian"],
    },
    "564_hessian_csv": {
        "path": RESIDUALS / "P8_Y5_R10_564_HESSIAN_EXTRACTION_FORMULA.csv",
        "note": "machine-readable Hessian extraction rows",
        "needles": ["H564_1_ZX_extraction", "H564_2_MX_extraction", "conditional_extraction_formula_derived"],
    },
    "579_parent_fill": {
        "path": POST_CHECKPOINT / "579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md",
        "note": "explicit parent X-block contract and countermodel blocker",
        "needles": ["S_X^(2)", "Z_X", "M_X^2", "countermodel_blocks"],
    },
    "579_contract_csv": {
        "path": RESIDUALS / "P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv",
        "note": "machine-readable explicit parent X-block contract",
        "needles": ["PXC579_1_positive_kinetic_residue", "PXC579_2_positive_mass_gap", "formula_only"],
    },
    "581_no_pole": {
        "path": POST_CHECKPOINT / "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md",
        "note": "conditional quotient-vertical no-pole theorem",
        "needles": ["H(v_X,.)", "no Z_X", "constraint algebra", "conditional"],
    },
    "582_momentum_map": {
        "path": POST_CHECKPOINT / "582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md",
        "note": "momentum-map and boundary-cocycle no-pole gate",
        "needles": ["momentum map", "boundary cocycle", "rank-zero", "no R10/local-GR claim"],
    },
    "586_affine_vdef": {
        "path": POST_CHECKPOINT / "586-Y5-R10-Vdef-owner-action-sketch-or-edge-runner-numeric-priors.md",
        "note": "affine Vdef zero-Hessian/no-pole contract",
        "needles": ["affine", "zero_Hessian", "partial^2 V_def", "not_parent_sourced"],
    },
    "607_factorization": {
        "path": POST_CHECKPOINT / "607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md",
        "note": "conditional compact-shell Green-function factorization",
        "needles": ["lambda_X=sqrt(Z_X/M_X^2)", "C_X", "factorization_derived", "blocked"],
    },
    "626_matter_descent": {
        "path": POST_CHECKPOINT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "note": "matter descent/coupling blocker",
        "needles": ["S_matter descends", "not_signed", "c_g", "local_GR=false"],
    },
    "708_contract": {
        "path": RESIDUALS / "P8_Y5_R10_708_SCALAR_CLASS_SOURCE_ROW_CONTRACT.csv",
        "note": "older scalar/class source row contract",
        "needles": ["MISSING_KINETIC_METRIC", "MISSING_MASS_MATRIX", "MISSING_CANONICAL_DIAGONALIZATION"],
    },
    "715_pack": {
        "path": RESIDUALS / "P8_Y5_R10_715_MINIMUM_EXECUTABLE_COEFFICIENT_PACK.csv",
        "note": "minimum local coefficient pack confirming Z/M/E blockers",
        "needles": ["MISSING_KINETIC_METRIC", "MISSING_MASS_MATRIX", "MISSING_CANONICAL_DIAGONALIZATION"],
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


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def csv_contains(path: Path, *needles: str) -> bool:
    return text_contains(path, list(needles))


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
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["note"],
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
        for key, info in SOURCES.items()
    ]

    source_hunt_candidate_ledger = [
        {
            "candidate_id": "SH721_0_720_handoff",
            "source_key": "720_doc",
            "candidate_object": "full local scalar/class ZM gate",
            "found_evidence": "720 proves the needed objects are exactly Z_IJ, M2_IJ, rank/signature, P_phys, E_a^I, lambda_a, A_a, B_Aa",
            "claim_use": "handoff_only",
            "claim_grade_ZM_source": "false",
            "reason": "720 explicitly says the current corpus cannot claim them",
            "next_action": "fill template rows or prove no-pole/zero-charge branch",
            "valid_for_claim": "false",
            "source_paths": source_path_string("720_doc", "720_retained_zm_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "candidate_id": "SH721_1_minimal_parent_ansatz",
            "source_key": "511_fixed_point_ansatz",
            "candidate_object": "multi-field action skeleton with G_AB, V, C(Phi)R",
            "found_evidence": "S_extra has a recognizable scalar-field kinetic metric G_AB(Phi), potential V(Phi), and fixed-point/mass-gap conditions",
            "claim_use": "template_source",
            "claim_grade_ZM_source": "false",
            "reason": "511 states it is a candidate contract, not proof current MTS satisfies it",
            "next_action": "map actual MTS variables into G_AB/V/C or leave as skeleton",
            "valid_for_claim": "false",
            "source_paths": source_path_string("511_fixed_point_ansatz"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "candidate_id": "SH721_2_single_X_hessian_contract",
            "source_key": "564_hessian_extraction",
            "candidate_object": "single-X Hessian residues Z_X and M_X^2",
            "found_evidence": "Z_X and M_X^2 are defined as second-variation residues of one parent action and give lambda_X=sqrt(Z_X/M_X^2)",
            "claim_use": "conditional_formula_source",
            "claim_grade_ZM_source": "false",
            "reason": "564 does not evaluate or sign the explicit parent Lagrangian coefficients",
            "next_action": "embed as the X-X block of the full Z_IJ/M2_IJ template",
            "valid_for_claim": "false",
            "source_paths": source_path_string("564_hessian_extraction", "564_hessian_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "candidate_id": "SH721_3_parent_X_block_contract",
            "source_key": "579_parent_fill",
            "candidate_object": "explicit parent X-block fill contract",
            "found_evidence": "579 restates S_X^(2), identifies Z_X, M_X^2, source charges, and proves covariance/universal coupling alone cannot fill them",
            "claim_use": "blocker_and_template_source",
            "claim_grade_ZM_source": "false",
            "reason": "579 leaves Z_X, M_X^2/Z_X, Qbar_XH, qbar_XT, and projector leak missing",
            "next_action": "use its countermodel guard before any numeric local bound score",
            "valid_for_claim": "false",
            "source_paths": source_path_string("579_parent_fill", "579_contract_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "candidate_id": "SH721_4_quotient_vertical_no_pole",
            "source_key": "581_no_pole",
            "candidate_object": "conditional no-pole theorem for vertical X",
            "found_evidence": "if X is quotient-vertical before variation and constraints/boundary/matter descend, H(v_X,.)=0 and no X Green function appears",
            "claim_use": "zero_branch_template_source",
            "claim_grade_ZM_source": "false",
            "reason": "projection, constraint algebra, and boundary clauses are unfilled",
            "next_action": "route to affine/no-pole mapping if no numeric ZM source appears",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_no_pole", "582_momentum_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "candidate_id": "SH721_5_affine_Vdef",
            "source_key": "586_affine_vdef",
            "candidate_object": "affine/topological V_def zero-Hessian mechanism",
            "found_evidence": "generic nonlinear V_def creates a physical Hessian/pole; affine V_def makes the Z Hessian exactly zero and X acts as multiplier/gauge if parent-owned",
            "claim_use": "preferred_less_scrutiny_no_pole_skeleton",
            "claim_grade_ZM_source": "false",
            "reason": "P, J_eff, A, quotient matter map, and boundary counterterm are not parent sourced",
            "next_action": "attempt 722 affine/no-pole map to the ZM template",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_affine_vdef"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "candidate_id": "SH721_6_compact_shell_factorization",
            "source_key": "607_factorization",
            "candidate_object": "conditional alpha(lambda) factorization",
            "found_evidence": "607 derives alpha_X(lambda_X)=epsilon_shell^p C_X(lambda_X) once Z_X/M_X^2/source charges exist",
            "claim_use": "fallback_score_template",
            "claim_grade_ZM_source": "false",
            "reason": "lambda_X, C_X, exponent p, sign, and source/test projections are blocked",
            "next_action": "only use after ZM or no-pole choice is made",
            "valid_for_claim": "false",
            "source_paths": source_path_string("607_factorization"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "candidate_id": "SH721_7_matter_descent_coupling",
            "source_key": "626_matter_descent",
            "candidate_object": "ordinary matter coupling descent",
            "found_evidence": "626 writes the descent criterion that would kill representative c_g and related source charges",
            "claim_use": "coupling_blocker_source",
            "claim_grade_ZM_source": "false",
            "reason": "matter action descent is not signed and does not supply Z_IJ or M2_IJ",
            "next_action": "retain as coupling-side blocker for Q_Aa after ZM template",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_matter_descent"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    parent_zm_template = [
        {
            "row_id": "PZT721_0_parent_action",
            "symbol": "S_parent",
            "definition": "local parent action containing metric/coframe, retained scalar/class fields u^I, constraints/topological terms, and matter descent map",
            "template_formula": "S=∫√-g[A_EH(u)R/(2κ*) - 1/2 Z_IJ(u)∇u^I∇u^J - V_eff(u) + L_constraint + L_top] + S_matter[ψ,hat_g(q(u),g),θ(q(u))]",
            "required_fill": "explicit parent action block with field list, units, sign convention, and matter map",
            "current_status": "TEMPLATE_ONLY_PARENT_ACTION_NOT_FILLED",
            "claim_gate": "blocks_all_ZM_claims",
            "valid_for_claim": "false",
            "source_paths": source_path_string("511_fixed_point_ansatz", "720_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "PZT721_1_field_list",
            "symbol": "u^I",
            "definition": "ordered local scalar/class/memory/domain/motion variables retained after quotient and constraints",
            "template_formula": "u^I=(X,C_perp,C_g,memory/domain scalars,...) only after parent variables are fixed",
            "required_fill": "source-backed field list and background u0",
            "current_status": "MISSING_FIELD_LIST_AND_BACKGROUND",
            "claim_gate": "blocks_index_convention",
            "valid_for_claim": "false",
            "source_paths": source_path_string("720_retained_zm_pack", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "PZT721_2_kinetic_tensor",
            "symbol": "Z_IJ^{mu nu}",
            "definition": "second variation of the parent action with respect to gradients of retained fields",
            "template_formula": "Z_IJ^{mu nu}:= -1/sqrt(-g) δ²S_parent/δ(∇_mu u^I)δ(∇_nu u^J)|_0",
            "required_fill": "explicit matrix/tensor residues with units and sign convention",
            "current_status": "MISSING_KINETIC_TENSOR",
            "claim_gate": "blocks_ghost_rank_projector_tests",
            "valid_for_claim": "false",
            "source_paths": source_path_string("564_hessian_extraction", "720_retained_zm_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "PZT721_3_isotropic_Z",
            "symbol": "Z_IJ",
            "definition": "locally isotropic static kinetic matrix on the physical branch",
            "template_formula": "Z_IJ=(1/3)h_munu Z_IJ^{mu nu} in the same convention as S_2",
            "required_fill": "matrix values/signs or parent theorem proving rank zero/gauge",
            "current_status": "MISSING_KINETIC_METRIC",
            "claim_gate": "blocks_rank_Pphys_and_lambda",
            "valid_for_claim": "false",
            "source_paths": source_path_string("564_hessian_csv", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "PZT721_4_mass_matrix",
            "symbol": "M2_IJ",
            "definition": "second variation/Hessian of the local effective potential/operator on retained fields",
            "template_formula": "M2_IJ:= +1/sqrt(-g) δ²S_parent/δu^Iδu^J|_0 after moving S_2 to -1/2 M2_IJ δu^Iδu^J convention",
            "required_fill": "mass matrix, sign, units, and field normalization",
            "current_status": "MISSING_MASS_MATRIX",
            "claim_gate": "blocks_mode_ranges",
            "valid_for_claim": "false",
            "source_paths": source_path_string("564_hessian_extraction", "579_contract_csv", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "PZT721_5_constraint_split",
            "symbol": "G_alpha^I,N_r^I,P_phys",
            "definition": "gauge, null, auxiliary, topological, and physical projector split",
            "template_formula": "δu^I=G_alpha^I ξ^alpha + N_r^I c^r + P_phys^I{}_a s^a",
            "required_fill": "constraint algebra, rank, boundary charge, and degree count",
            "current_status": "MISSING_PHYSICAL_PROJECTOR",
            "claim_gate": "blocks_no_mode_theorem",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_no_pole", "582_momentum_map", "720_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "PZT721_6_canonical_modes",
            "symbol": "E_a^I,m_a^2,lambda_a",
            "definition": "canonical eigenmodes and ranges on the physical subspace",
            "template_formula": "(P^T M2 P)E_a=m_a^2(P^T Z P)E_a; E_a^T Z E_b=δ_ab; lambda_a=1/m_a or hbar/(m_a c)",
            "required_fill": "generalized eigenbasis and range convention",
            "current_status": "MISSING_CANONICAL_DIAGONALIZATION",
            "claim_gate": "blocks_R10_PPN_WEP_clock_orbital_scores",
            "valid_for_claim": "false",
            "source_paths": source_path_string("720_doc", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "PZT721_7_source_projection",
            "symbol": "A_a,B_Aa,Q_Aa",
            "definition": "projected AEH and matter charges in D=4 observed branch",
            "template_formula": "A_a=E_a^I a_I; B_Aa=E_a^I b_A,I; Q_Aa=N_frame(B_Aa-A_a/2)",
            "required_fill": "a_I, b_A,I, E_a^I, N_frame and matter descent/coupling source",
            "current_status": "MISSING_PROJECTED_SOURCE_CHARGES",
            "claim_gate": "blocks_local_observable_residual_vector",
            "valid_for_claim": "false",
            "source_paths": source_path_string("720_doc", "626_matter_descent"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "PZT721_8_single_X_embedding",
            "symbol": "Z_XX,M2_XX",
            "definition": "single-X specialization of the full template using 564/579 Hessian residues",
            "template_formula": "Z_XX≡Z_X; M2_XX≡M_X^2; lambda_X=sqrt(Z_X/M_X^2) if X is a physical positive mode",
            "required_fill": "explicit parent X block or affine/no-pole certificate",
            "current_status": "FORMULA_SOURCE_EXISTS_VALUES_MISSING",
            "claim_gate": "blocks_numeric_alpha_and_no_pole_choice",
            "valid_for_claim": "false",
            "source_paths": source_path_string("564_hessian_extraction", "579_parent_fill", "586_affine_vdef"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    candidate_to_template_map = [
        {
            "map_id": "CTM721_0_511_to_full_template",
            "candidate": "G_AB(Phi), V(Phi), C(Phi)R",
            "template_destination": "Z_IJ, M2_IJ, A_EH",
            "translation": "identify Phi^A with u^I; G_AB maps to Z_IJ; Hessian(V) maps to M2_IJ; dC maps to a_I",
            "usable_now": "template_only",
            "claim_gap": "no actual MTS field list or coefficient map",
            "valid_for_claim": "false",
            "source_paths": source_path_string("511_fixed_point_ansatz"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "CTM721_1_564_to_X_block",
            "candidate": "Z_X=(1/3)h_munu H_grad^{munu}; M_X^2=H_0",
            "template_destination": "Z_XX, M2_XX",
            "translation": "embed single-X Hessian residues as the diagonal X-X block of Z_IJ and M2_IJ",
            "usable_now": "formula_only",
            "claim_gap": "explicit parent second variation and normalization missing",
            "valid_for_claim": "false",
            "source_paths": source_path_string("564_hessian_extraction", "564_hessian_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "CTM721_2_586_to_zero_block",
            "candidate": "affine/topological V_def gives exact zero Hessian in vertical X",
            "template_destination": "P_phys excludes X or K_X=0 no-pole branch",
            "translation": "if parent owns affine Vdef plus momentum-map/boundary/matter descent, X is not a physical Z/M eigenmode",
            "usable_now": "conditional_no_pole_skeleton",
            "claim_gap": "P,J_eff,A,boundary and quotient matter map are not parent sourced",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_affine_vdef", "581_no_pole", "582_momentum_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "CTM721_3_607_to_finite_score",
            "candidate": "alpha_X=lambda branch factorization",
            "template_destination": "R10/PPN/WEP finite residual score",
            "translation": "after Z_XX/M2_XX/Q projections exist, use alpha_X=lambda factorization for empirical scoring",
            "usable_now": "fallback_only",
            "claim_gap": "lambda_X, C_X, p, sign, source/test charges, and bound curve are missing/nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("607_factorization"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    claim_blocker_ledger = [
        {
            "blocker_id": "CB721_0_no_multifield_parent_action",
            "missing_object": "explicit current MTS parent action",
            "why_it_matters": "without S_parent there is no source-backed second variation for Z_IJ or M2_IJ",
            "strongest_current_evidence": "511 gives an ansatz/contract only",
            "repair": "write or extract exact local parent action block and field list",
            "claim_blocked": "local_GR_Newton_PPN_R10_WEP_clock_orbital",
            "valid_for_claim": "false",
            "source_paths": source_path_string("511_fixed_point_ansatz", "720_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "CB721_1_single_X_formula_not_values",
            "missing_object": "numeric/signed Z_X and M_X^2",
            "why_it_matters": "formula-only Hessian residues cannot determine range, stability, ghost status, or alpha normalization",
            "strongest_current_evidence": "564/579 define residues and countermodel; values remain missing",
            "repair": "derive explicit X block or choose affine/no-pole route with proof certificate",
            "claim_blocked": "R10_alpha_lambda_and_local_scalar_residual",
            "valid_for_claim": "false",
            "source_paths": source_path_string("564_hessian_extraction", "579_parent_fill"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "CB721_2_no_constraint_degree_count",
            "missing_object": "first-class constraint/momentum-map closure and zero boundary cocycle",
            "why_it_matters": "zero Hessian can mean gauge/constraint or under-specified dynamics; it is not automatically no-pole",
            "strongest_current_evidence": "581/582 define the exact no-pole certificate",
            "repair": "prove the affine/vertical block is parent-owned and boundary differentiable",
            "claim_blocked": "K_X_zero_no_pole",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_no_pole", "582_momentum_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "CB721_3_matter_coupling_descent_unsigned",
            "missing_object": "quotient-invariant ordinary matter action",
            "why_it_matters": "even with a mode basis, Q_Aa may be nonzero unless matter descends or couplings are sourced",
            "strongest_current_evidence": "626 descent criterion not signed",
            "repair": "prove matter descent or fill c_g/source-charge bound rows",
            "claim_blocked": "Q_Aa_zero_WEP_PPN_clock_R10",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_matter_descent"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "CB721_4_no_full_bound_ready_mode",
            "missing_object": "claim-grade lambda_a, alpha(lambda), and source/test charge coefficients",
            "why_it_matters": "finite residual scoring cannot start with symbolic or template coefficients",
            "strongest_current_evidence": "607 factorizes but leaves C_X, p, lambda_X and charges blocked",
            "repair": "after ZM/no-pole decision, fill a nonclaim runner first and only promote with real sourced values",
            "claim_blocked": "empirical_local_bound_pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("607_factorization"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    decision_matrix = [
        {
            "decision_id": "D721_0_claim_grade_ZM_found",
            "question": "Did the source hunt find a claim-grade full Z_IJ/M2_IJ/E_a^I source?",
            "answer": "no",
            "reason": "sources contain contracts, single-X formulas, and no-pole skeletons, but no explicit multi-field parent second variation",
            "decision": "do_not_promote_any_local_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("720_doc", "511_fixed_point_ansatz", "564_hessian_extraction"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D721_1_best_route",
            "question": "Which route is least exposed to local fifth-force scrutiny?",
            "answer": "affine/topological no-pole first, retained finite X second",
            "reason": "a physical positive scalar mode needs bounds; affine/no-pole could remove K_X if parent-owned",
            "decision": "attempt_722_affine_no_pole_map",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_affine_vdef", "581_no_pole", "582_momentum_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D721_2_template_fill_status",
            "question": "Can 721 fill the canonical template without overclaim?",
            "answer": "yes_template_only",
            "reason": "definitions and source slots are precise; values and theorem certificates remain absent",
            "decision": "write_template_rows_valid_for_claim_false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("720_retained_zm_pack", "579_contract_csv"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    bound_or_derive_queue = [
        {
            "queue_id": "BDQ721_0_affine_no_pole_map",
            "target": "map affine Vdef/no-pole skeleton to the ZM template",
            "preferred_route": "prove X is affine/topological/quotient before variation, matter descends, and boundary cocycle vanishes",
            "fallback_route": "retain X as a physical finite branch with symbolic Z_XX/M2_XX",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_affine_vdef", "581_no_pole", "582_momentum_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ721_1_single_X_block",
            "target": "instantiate the single-X row of the canonical template",
            "preferred_route": "derive explicit X block and signs/units for Z_X and M_X^2",
            "fallback_route": "keep Z_X/M_X^2 formula-only and block local scoring",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("564_hessian_extraction", "579_parent_fill"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ721_2_full_multifield_later",
            "target": "generalize from X to full u^I field-space after single-X route is sorted",
            "preferred_route": "extract actual field multiplet and parent action second variation",
            "fallback_route": "keep multi-field table as source-ready schema only",
            "priority": "P1",
            "next_artifact": "after_722_full_uI_parent_action_second_variation_or_source_pack",
            "valid_for_claim": "false",
            "source_paths": source_path_string("511_fixed_point_ansatz", "720_retained_zm_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ721_3_coupling_after_mode",
            "target": "project matter coupling after mode/no-pole choice",
            "preferred_route": "derive quotient-invariant matter descent so Q_Aa or c_g vanishes",
            "fallback_route": "fill finite coupling rows and score them",
            "priority": "P1",
            "next_artifact": "after_722_source_current_orthogonality_or_cg_QAa_score_pack",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_matter_descent"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_parent_ZM_source_hunt_found_formula_contracts_not_claim_grade_ZM_template_filled_nonclaim",
            "claim_ceiling": "canonical_ZM_template_and_source_hunt_only_no_local_GR_Newton_PPN_R10_WEP_clock_or_orbital_claim",
            "main_result": "no claim-grade full Z_IJ/M2_IJ/E_a^I source found; single-X Hessian formulas and affine/no-pole skeleton are usable as conditional templates",
            "best_next_route": "attempt affine/topological no-pole map to the ZM template before finite residual scoring",
            "remaining_blocker": "explicit parent action, field list, signed Z/M or no-pole certificate, matter descent/coupling projection, boundary silence",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("720_doc", "564_hessian_extraction", "579_parent_fill", "586_affine_vdef"),
            "generated_utc": GENERATED_UTC,
        }
    ]

    outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_721_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
        ),
        "source_hunt_candidate_ledger": (
            RESIDUALS / "P8_Y5_R10_721_SOURCE_HUNT_CANDIDATE_LEDGER.csv",
            source_hunt_candidate_ledger,
            [
                "candidate_id",
                "source_key",
                "candidate_object",
                "found_evidence",
                "claim_use",
                "claim_grade_ZM_source",
                "reason",
                "next_action",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "parent_zm_template": (
            RESIDUALS / "P8_Y5_R10_721_PARENT_ZM_TEMPLATE.csv",
            parent_zm_template,
            [
                "row_id",
                "symbol",
                "definition",
                "template_formula",
                "required_fill",
                "current_status",
                "claim_gate",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "candidate_to_template_map": (
            RESIDUALS / "P8_Y5_R10_721_CANDIDATE_TO_TEMPLATE_MAP.csv",
            candidate_to_template_map,
            ["map_id", "candidate", "template_destination", "translation", "usable_now", "claim_gap", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "claim_blocker_ledger": (
            RESIDUALS / "P8_Y5_R10_721_CLAIM_BLOCKER_LEDGER.csv",
            claim_blocker_ledger,
            [
                "blocker_id",
                "missing_object",
                "why_it_matters",
                "strongest_current_evidence",
                "repair",
                "claim_blocked",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "decision_matrix": (
            RESIDUALS / "P8_Y5_R10_721_DECISION_MATRIX.csv",
            decision_matrix,
            ["decision_id", "question", "answer", "reason", "decision", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "bound_or_derive_queue": (
            RESIDUALS / "P8_Y5_R10_721_BOUND_OR_DERIVE_QUEUE.csv",
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
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_721_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            [
                "status",
                "claim_ceiling",
                "main_result",
                "best_next_route",
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
    claim_grade_found = any(row["claim_grade_ZM_source"] == "true" for row in source_hunt_candidate_ledger)
    validations = [
        {
            "check_id": "V721_0_source_paths_exist",
            "result": "pass" if all(info["path"].exists() for info in SOURCES.values()) else "fail",
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "V721_1_source_needles_present",
            "result": "pass" if all(text_contains(info["path"], info["needles"]) for info in SOURCES.values()) else "fail",
            "detail": "all source files contain the expected evidence needles",
        },
        {
            "check_id": "V721_2_prior_720_clean",
            "result": "pass" if prior_validation_clean(SOURCES["720_validation"]["path"]) else "fail",
            "detail": "720 validation has no failures",
        },
        {
            "check_id": "V721_3_720_selected_721",
            "result": "pass" if csv_contains(SOURCES["720_doc"]["path"], "721-Y5-R10-parent-ZM-source-hunt-or-canonical-mode-template-fill.md") else "fail",
            "detail": "720 next target matches this checkpoint",
        },
        {
            "check_id": "V721_4_ZM_missing_confirmed",
            "result": "pass"
            if csv_contains(
                SOURCES["720_retained_zm_pack"]["path"],
                "MISSING_KINETIC_METRIC",
                "MISSING_MASS_MATRIX",
                "MISSING_CANONICAL_DIAGONALIZATION",
            )
            else "fail",
            "detail": "720 retained ZM pack confirms missing Z/M/E",
        },
        {
            "check_id": "V721_5_single_X_hessian_contract_found",
            "result": "pass"
            if csv_contains(SOURCES["564_hessian_csv"]["path"], "H564_1_ZX_extraction", "H564_2_MX_extraction")
            else "fail",
            "detail": "single-X Hessian formulas available as conditional templates",
        },
        {
            "check_id": "V721_6_no_claim_grade_ZM_promoted",
            "result": "pass" if not claim_grade_found else "fail",
            "detail": f"claim_grade_ZM_sources={sum(row['claim_grade_ZM_source'] == 'true' for row in source_hunt_candidate_ledger)}",
        },
        {
            "check_id": "V721_7_parent_template_core_rows_present",
            "result": "pass"
            if {"S_parent", "u^I", "Z_IJ", "M2_IJ", "E_a^I,m_a^2,lambda_a", "Z_XX,M2_XX"}.issubset(
                {row["symbol"] for row in parent_zm_template}
            )
            else "fail",
            "detail": f"template_rows={len(parent_zm_template)}",
        },
        {
            "check_id": "V721_8_affine_no_pole_route_selected",
            "result": "pass" if decision_matrix[1]["decision"] == "attempt_722_affine_no_pole_map" else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V721_9_blockers_preserved",
            "result": "pass"
            if {"explicit current MTS parent action", "numeric/signed Z_X and M_X^2", "quotient-invariant ordinary matter action"}.issubset(
                {row["missing_object"] for row in claim_blocker_ledger}
            )
            else "fail",
            "detail": f"blocker_rows={len(claim_blocker_ledger)}",
        },
        {
            "check_id": "V721_10_next_target_selected",
            "result": "pass" if all(row["next_target"] == NEXT_TARGET for row in decision_matrix) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V721_11_no_claim_rows_promoted",
            "result": "pass" if all_valid_false(generated_paths) else "fail",
            "detail": "all generated rows with valid_for_claim remain false",
        },
        {
            "check_id": "V721_12_outputs_scoped",
            "result": "pass" if under_post_checkpoint([OUTPUT_DOC, *generated_paths]) else "fail",
            "detail": "all outputs under post-checkpoint-work",
        },
        {
            "check_id": "V721_13_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V721_14_nonclaim_status",
            "result": "pass" if "nonclaim" in nonclaim_summary[0]["status"] else "fail",
            "detail": "claim ceiling blocks local-GR/Newton/PPN/R10/WEP/clock/orbital claims",
        },
        {
            "check_id": "V721_15_source_register_written",
            "result": "pass" if len(source_register) >= 12 else "fail",
            "detail": f"source_rows={len(source_register)}",
        },
        {
            "check_id": "V721_16_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]

    validation_path = RESIDUALS / "P8_Y5_BRR545_721_VALIDATION.csv"
    write_csv(validation_path, validations, ["check_id", "result", "detail"])

    doc = f"""# 721 - Y5 R10 Parent ZM Source Hunt Or Canonical Mode Template Fill

## Summary

This checkpoint does the source hunt requested by 720. It asks whether the existing private corpus already contains a claim-grade parent source for the local `Z_IJ/M2_IJ/E_a^I` mode data.

Verdict: **no claim-grade full `Z/M` source was found**.

What was found is still useful:

- 511 gives a multi-field local-GR fixed-point action contract.
- 564 and 579 give a conditional single-`X` Hessian-residue contract: `Z_X`, `M_X^2`, and `lambda_X=sqrt(Z_X/M_X^2)`.
- 581, 582, and 586 give the cleaner no-pole route: affine/topological/quotient `X` can avoid a physical Green function only if the parent momentum-map, boundary, and matter-descent clauses close.
- 607 gives the finite-residual scoring shape if the no-pole route fails.

So 721 fills the canonical `Z/M` template, but every row remains `valid_for_claim=false`.

| Field | Value |
| --- | --- |
| Generated UTC | `{GENERATED_UTC}` |
| Claim status | nonclaim/private checkpoint |
| Next target | `{NEXT_TARGET}` |

## Source Hunt Candidate Ledger

{markdown_table(source_hunt_candidate_ledger, ["candidate_id", "candidate_object", "claim_use", "claim_grade_ZM_source", "reason", "next_action", "valid_for_claim"])}

## Parent ZM Template

{markdown_table(parent_zm_template, ["row_id", "symbol", "template_formula", "current_status", "claim_gate", "valid_for_claim"])}

## Candidate To Template Map

{markdown_table(candidate_to_template_map, ["map_id", "candidate", "template_destination", "usable_now", "claim_gap", "valid_for_claim"])}

## Claim Blocker Ledger

{markdown_table(claim_blocker_ledger, ["blocker_id", "missing_object", "why_it_matters", "repair", "claim_blocked", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_matrix, ["decision_id", "question", "answer", "decision", "next_target", "valid_for_claim"])}

## Bound Or Derive Queue

{markdown_table(bound_or_derive_queue, ["queue_id", "target", "preferred_route", "fallback_route", "priority", "next_artifact", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "best_next_route", "remaining_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Verdict

The useful move is not to pretend the full `Z_IJ/M2_IJ` matrix has been found. It has not. The honest improvement is that the single-`X` branch now has a source-backed template route: either map the affine/topological no-pole mechanism into the `Z/M` template and close the momentum-map/boundary/matter certificates, or retain a physical `X` mode with symbolic `Z_XX`, `M2_XX`, `Q` rows and score it later. The next checkpoint should try the no-pole map first because it is the less exposed route.
"""

    OUTPUT_DOC.write_text(doc, encoding="utf-8")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {validation_path}")
    print(f"validation_passes={sum(row['result'] == 'pass' for row in validations)}/{len(validations)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
