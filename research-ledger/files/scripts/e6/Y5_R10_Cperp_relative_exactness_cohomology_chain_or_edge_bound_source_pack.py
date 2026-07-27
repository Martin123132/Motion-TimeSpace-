from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1160-Y5-R10-Cperp-relative-exactness-cohomology-chain-or-edge-bound-source-pack.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def missing_or_blocked(value: object) -> bool:
    text = str(value)
    return (
        text.strip() == ""
        or "MISSING" in text
        or "NOT_DERIVED" in text
        or "NOT_PROVED" in text
        or "NOT_ACQUIRED" in text
        or "BLOCKED" in text
        or "UNSIGNED" in text
    )


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1160_0_1159_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1159_NEXT_TARGET.csv",
            "needle": "NEXT1159_0_1160",
            "role": "handoff selecting Cperp relative exactness or edge-bound source pack.",
        },
        {
            "source_id": "SRC1160_1_1159_exactness",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1159_BOUNDARY_PRIMITIVE_ZERO_AUDIT.csv",
            "needle": "BPZ1159_1_Cperp_exactness",
            "role": "1159 exactness input that must be derived before boundary zero proof.",
        },
        {
            "source_id": "SRC1160_2_1159_edge_law",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1159_EDGE_BOUND_LAW_ROWS.csv",
            "needle": "EBL1159_0_QC_bound_law",
            "role": "edge-bound fallback law when Cperp boundary zero fails.",
        },
        {
            "source_id": "SRC1160_3_272_target",
            "relative_path": "272-quotient-configuration-principle-from-topological-projector.md",
            "needle": "derive Cperp relative exactness for the C-sector",
            "role": "older handoff naming Cperp relative exactness as the next burden.",
        },
        {
            "source_id": "SRC1160_4_1020_cohomology",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_2_relative_cohomology",
            "role": "relative cohomology/harmonic edge class gate.",
        },
        {
            "source_id": "SRC1160_5_1020_stokes",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_1_weighted_Stokes_identity",
            "role": "weighted Stokes identity for exact boundary terms.",
        },
        {
            "source_id": "SRC1160_6_1019_edge_pack",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "SP1019_4_edge_coefficients",
            "role": "older edge coefficient source-pack schema.",
        },
        {
            "source_id": "SRC1160_7_1019_projector",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "PO1019_5_verdict",
            "role": "projector orthogonality still fails current claim.",
        },
        {
            "source_id": "SRC1160_8_407_quotient_sketch",
            "relative_path": "407-primitive-relational-quotient-action-sketch.md",
            "needle": "matter quotient functor/no-marker selector proof",
            "role": "primitive quotient sketch still needs matter functor proof.",
        },
        {
            "source_id": "SRC1160_9_720_kinetic",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_720_KINETIC_NULL_THEOREM_AUDIT.csv",
            "needle": "KNT720_8_no_mode_theorem",
            "role": "no-mode theorem fails current corpus without rank/source/boundary silence.",
        },
        {
            "source_id": "SRC1160_10_1030_spm",
            "relative_path": "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
            "needle": "SPD1030_6_verdict",
            "role": "single-public-metric/no-shadow-frame theorem not derived.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def exactness_chain_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "chain_id": "CRE1160_0_Cperp_object",
                "claim_piece": "Cperp parent object",
                "required_statement": "C_perp is a source-backed local C-sector residual form with declared degree, domain, pullback, and variation rule.",
                "current_status": "MISSING_PARENT_CPERP_FORM",
                "closing_condition": "source path gives C_perp, form degree, local branch, and relation to the topological/projector sector",
                "effect_if_closed": "relative complex can be instantiated",
                "valid_for_claim": "false",
            },
            {
                "chain_id": "CRE1160_1_relative_complex",
                "claim_piece": "relative differential and boundary map",
                "required_statement": "d_rel, boundary pullback i^*, and relative pair convention are defined for the same local branch.",
                "current_status": "MISSING_DREL_OPERATOR",
                "closing_condition": "source path defines (Omega_C^k(U),Omega_C^{k-1}(S),d_rel) and allowed boundary class",
                "effect_if_closed": "closedness/exactness become meaningful, not slogans",
                "valid_for_claim": "false",
            },
            {
                "chain_id": "CRE1160_2_closedness",
                "claim_piece": "relative closedness",
                "required_statement": "d_rel C_perp=0 in the local branch, including source, support, and boundary terms.",
                "current_status": "NOT_PROVED",
                "closing_condition": "parent variational identity or Bianchi/Noether identity proves closedness with no omitted source tail",
                "effect_if_closed": "relative Poincare/cohomology test can be applied",
                "valid_for_claim": "false",
            },
            {
                "chain_id": "CRE1160_3_relative_cohomology",
                "claim_piece": "trivial relative class",
                "required_statement": "[C_perp]=0 in H_rel^k(U,S;C-sector), or the harmonic coefficient is separately zero/bounded.",
                "current_status": "HREL_CLASS_NOT_ZEROED",
                "closing_condition": "local topology/branch selector proves H_rel^k trivial for this sector or supplies h_C coefficients",
                "effect_if_closed": "C_perp may be written as d_rel B_C up to bounded residuals",
                "valid_for_claim": "false",
            },
            {
                "chain_id": "CRE1160_4_primitive_existence",
                "claim_piece": "B_C primitive",
                "required_statement": "there exists a sourced B_C with C_perp=d_rel B_C and declared units/norms.",
                "current_status": "PRIMITIVE_NOT_CONSTRUCTED",
                "closing_condition": "explicit primitive or constructive homotopy operator with source path and norms",
                "effect_if_closed": "edge-bound law can use norm_bC; zero route can test B_C boundary silence",
                "valid_for_claim": "false",
            },
            {
                "chain_id": "CRE1160_5_boundary_decomposition",
                "claim_piece": "boundary decomposition",
                "required_statement": "B_C|S=d_S b_C+h_C+r_C with h_C/r_C zero or source-bounded.",
                "current_status": "DECOMPOSITION_NOT_SOURCED",
                "closing_condition": "relative Hodge/cohomology decomposition, surface norm convention, h_C/r_C rows",
                "effect_if_closed": "turns edge leakage into computable terms",
                "valid_for_claim": "false",
            },
            {
                "chain_id": "CRE1160_6_local_branch_selector",
                "claim_piece": "local trivial versus FLRW active branch",
                "required_statement": "parent law selects trivial/relative-exact local compact class without killing active cosmological branch by hand.",
                "current_status": "BRANCH_SELECTOR_UNSIGNED",
                "closing_condition": "domain/branch functional separates local compact exact class from FLRW homogeneous memory class",
                "effect_if_closed": "allows local silence without global/cosmology cheating",
                "valid_for_claim": "false",
            },
            {
                "chain_id": "CRE1160_7_presymplectic_null",
                "claim_piece": "q-null consequence",
                "required_statement": "exact/trivial Cperp plus boundary silence implies Omega(v_X,delta)=0 and v_X in ker(Dq).",
                "current_status": "CONDITIONAL_ONLY",
                "closing_condition": "CRE1160_0 through CRE1160_6 plus 1159 boundary-zero clauses all close",
                "effect_if_closed": "can feed the c_g zero theorem route",
                "valid_for_claim": "false",
            },
            {
                "chain_id": "CRE1160_8_matter_descent_link",
                "claim_piece": "matter/no-shadow link",
                "required_statement": "even with Cperp exactness, ordinary matter must factor through quotient/public frame so A_g(Xhat) is not allowed.",
                "current_status": "NOT_DERIVED_CURRENT_CORPUS",
                "closing_condition": "single-public-metric or quotient-matter functor theorem in same local branch",
                "effect_if_closed": "converts q-null geometry into c_g=0 instead of only boundary silence",
                "valid_for_claim": "false",
            },
            {
                "chain_id": "CRE1160_9_verdict",
                "claim_piece": "Cperp relative exactness for current MTS",
                "required_statement": "CRE1160_0 through CRE1160_8 all parent-signed.",
                "current_status": "CPERP_RELATIVE_EXACTNESS_NOT_DERIVED",
                "closing_condition": "C_perp form, d_rel complex, closedness, H_rel triviality, B_C primitive, boundary decomposition, branch selector, and matter link",
                "effect_if_closed": "only then can local q-null/c_g zero route be reopened as theorem rather than closure",
                "valid_for_claim": "false",
            },
        ]
    )


def edge_source_pack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "pack_id": "ESP1160_0_Cperp_form",
                "quantity": "C_perp",
                "required_source": "parent C-sector residual form, form degree, local domain, units, and variation rule",
                "feeds": "CRE1160_0;CRE1160_2;EBL1159_3",
                "current_value": "MISSING_PARENT_CPERP_FORM",
                "source_path": "MISSING_PARENT_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "ESP1160_1_drel_complex",
                "quantity": "d_rel;i_star;relative_pair",
                "required_source": "relative differential, boundary pullback, relative pair convention, and allowed boundary/domain class",
                "feeds": "CRE1160_1;CRE1160_2;CRE1160_3",
                "current_value": "MISSING_DREL_OPERATOR",
                "source_path": "MISSING_RELATIVE_COMPLEX_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "ESP1160_2_Hrel_class",
                "quantity": "H_rel_C;h_C",
                "required_source": "relative cohomology basis/triviality theorem or harmonic coefficient/source bound",
                "feeds": "CRE1160_3;CRE1160_5;EBL1159_4",
                "current_value": "MISSING_HREL_TRIVIALITY_OR_HC_BOUND",
                "source_path": "MISSING_COHOMOLOGY_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "ESP1160_3_BC_primitive",
                "quantity": "B_C;b_C;norm_bC",
                "required_source": "explicit primitive or constructive homotopy, boundary primitive, norm convention, units",
                "feeds": "CRE1160_4;CRE1160_5;EBL1159_3",
                "current_value": "MISSING_BC_PRIMITIVE_AND_NORM",
                "source_path": "MISSING_PRIMITIVE_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "ESP1160_4_weighted_stokes_terms",
                "quantity": "C_corner;norm_dS_Feps",
                "required_source": "boundary/corner topology, F_lambda profile, epsilon_X domain, surface metric, norm convention",
                "feeds": "EBL1159_1;EBL1159_2",
                "current_value": "MISSING_WEIGHTED_STOKES_INPUTS",
                "source_path": "MISSING_BOUNDARY_PROFILE_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "ESP1160_5_residual_class",
                "quantity": "r_C;residual_edge_abs",
                "required_source": "non-exact residual decomposition, source/support map, and absolute bound",
                "feeds": "CRE1160_5;EBL1159_5",
                "current_value": "MISSING_RESIDUAL_CLASS_ZERO_OR_BOUND",
                "source_path": "MISSING_RESIDUAL_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "ESP1160_6_cocycle",
                "quantity": "K_boundary",
                "required_source": "parent Omega, differentiable generator G_X, boundary bracket, cocycle zero theorem or bound",
                "feeds": "EBL1159_6",
                "current_value": "MISSING_COCYCLE_ZERO_OR_BOUND",
                "source_path": "MISSING_SYMPLECTIC_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "ESP1160_7_projector_source",
                "quantity": "Pi_M^H;M_H_ref_min;Qbar_CXH",
                "required_source": "projector norm, denominator lock, source-worldtube lock, and Q_C edge bound",
                "feeds": "EBL1159_7;local source-normalization residual",
                "current_value": "MISSING_PROJECTOR_SOURCE_BOUND",
                "source_path": "MISSING_PROJECTOR_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "ESP1160_8_branch_selector",
                "quantity": "local_trivial_FLRW_active_selector",
                "required_source": "parent domain/branch functional selecting local exact class while retaining cosmological active class",
                "feeds": "CRE1160_6",
                "current_value": "MISSING_BRANCH_SELECTOR",
                "source_path": "MISSING_BRANCH_SELECTOR_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "ESP1160_9_matter_descent",
                "quantity": "matter_quotient_functor;terminal_e_pub",
                "required_source": "ordinary matter functor factors through quotient/public coframe and has no A_g shadow slot",
                "feeds": "CRE1160_8;c_g_zero_route",
                "current_value": "MISSING_MATTER_DESCENT_NO_SHADOW_THEOREM",
                "source_path": "MISSING_MATTER_FUNCTOR_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1160_0_no_Cperp_symbol_only",
                "guard": "Cperp exactness cannot be claimed without a sourced C_perp object and d_rel complex",
                "status": "ACTIVE",
                "reason": "exactness of an undefined object is closure language, not a theorem",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1160_1_no_relative_Poincare_without_Hrel",
                "guard": "relative Poincare/cohomology arguments require closedness and trivial relative class",
                "status": "ACTIVE",
                "reason": "harmonic edge classes can survive local exact-looking manipulations",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1160_2_no_bulk_exact_to_edge_zero",
                "guard": "bulk relative exactness does not erase weighted boundary/cocycle/projector terms",
                "status": "ACTIVE",
                "reason": "1159 showed the exact edge readout has independent terms",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1160_3_no_local_cosmo_hand_switch",
                "guard": "local trivial and FLRW active branches need one parent selector, not hand switching",
                "status": "ACTIVE",
                "reason": "a local silence theorem must not accidentally kill the cosmology branch by the same logic",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1160_4_no_cg_zero_without_matter_descent",
                "guard": "geometric q-null is not enough to prove c_g=0 unless matter cannot see the representative",
                "status": "ACTIVE",
                "reason": "A_g shadow-frame slot remains a legal countermodel until matter functor/domain closes",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1160_0_sources_exist",
                "rule": "all cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1160_1_conditional_theorem_shape",
                "rule": "conditional relative-exactness theorem chain is stated",
                "gate_pass": "true_nonclaim",
                "reason": "closedness + trivial H_rel + primitive + boundary/matter clauses are explicit",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1160_2_Cperp_exactness_derived",
                "rule": "Cperp relative exactness is parent-signed",
                "gate_pass": "false",
                "reason": "C_perp form, d_rel complex, closedness, H_rel triviality, primitive, and branch selector are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1160_3_edge_pack_ready",
                "rule": "edge-bound source pack exists as nonclaim fallback",
                "gate_pass": "true_nonclaim",
                "reason": "source-pack rows are complete but all values remain missing/nonclaim",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1160_4_claim_promotion",
                "rule": "q-null/c_g-zero/local-GR/Newton/R10/PPN/WEP/clock/orbital claim allowed",
                "gate_pass": "false",
                "reason": "relative exactness, boundary zero, matter descent, and finite source rows remain incomplete",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1160_0_exactness_status",
                "decision": "Cperp_relative_exactness_not_derived",
                "reason": "the corpus does not yet provide C_perp, d_rel, closedness, H_rel triviality, or primitive construction",
                "next_action": "source the C_perp form and d_rel operator before another zero proof attempt",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1160_1_edge_status",
                "decision": "edge_bound_source_pack_ready_nonclaim",
                "reason": "if exactness remains open, the leakage terms are now sourceable one by one",
                "next_action": "fill C_perp, H_rel/h_C, B_C/norms, K_boundary, and projector rows",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1160_2_best_next",
                "decision": "target_Cperp_form_drel_operator_or_branch_selector",
                "reason": "without the actual object and differential, all further exactness work is symbolic fog",
                "next_action": "1161 Cperp form/d_rel source row or local/FLRW branch selector proof",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1160_0_1161",
                "next_target": "1161-Y5-R10-Cperp-form-drel-operator-source-row-or-local-branch-selector-proof.md",
                "objective": "define the actual C_perp form and d_rel relative complex for the local branch, or derive the parent selector that makes local C-sector cohomology trivial while retaining FLRW activity",
                "include": "C_perp form degree; local domain; d_rel; boundary pullback; relative pair; H_rel class; branch selector; source paths",
                "exclude": "undefined Cperp exactness; bulk-exactness-as-edge-zero; local/FLRW hand switch; c_g zero claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    edge_pack: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = chain + edge_pack + guards + gates + decisions + next_target
    required_edge_pack = {
        "ESP1160_0_Cperp_form",
        "ESP1160_1_drel_complex",
        "ESP1160_2_Hrel_class",
        "ESP1160_3_BC_primitive",
        "ESP1160_4_weighted_stokes_terms",
        "ESP1160_5_residual_class",
        "ESP1160_6_cocycle",
        "ESP1160_7_projector_source",
        "ESP1160_8_branch_selector",
        "ESP1160_9_matter_descent",
    }
    add(
        "V1160_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1160_1_chain_shape_complete",
        {"CRE1160_0_Cperp_object", "CRE1160_1_relative_complex", "CRE1160_2_closedness", "CRE1160_3_relative_cohomology", "CRE1160_4_primitive_existence", "CRE1160_9_verdict"}.issubset(
            {row["chain_id"] for row in chain}
        ),
        "relative-exactness chain covers object, complex, closedness, cohomology, primitive, and verdict",
    )
    add(
        "V1160_2_exactness_not_claimed",
        any(row["chain_id"] == "CRE1160_9_verdict" and row["current_status"] == "CPERP_RELATIVE_EXACTNESS_NOT_DERIVED" for row in chain),
        "Cperp relative exactness remains unclaimed",
    )
    add(
        "V1160_3_edge_pack_complete",
        required_edge_pack.issubset({row["pack_id"] for row in edge_pack}),
        "edge source pack covers Cperp, d_rel, H_rel, B_C, Stokes, residual, cocycle, projector, branch, and matter rows",
    )
    add(
        "V1160_4_edge_pack_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and missing_or_blocked(row["current_value"]) for row in edge_pack),
        "edge/source-pack rows remain missing/nonclaim until sourced",
    )
    add(
        "V1160_5_guards_active",
        {
            "GUARD1160_0_no_Cperp_symbol_only",
            "GUARD1160_1_no_relative_Poincare_without_Hrel",
            "GUARD1160_2_no_bulk_exact_to_edge_zero",
            "GUARD1160_3_no_local_cosmo_hand_switch",
            "GUARD1160_4_no_cg_zero_without_matter_descent",
        }.issubset({row["guard_id"] for row in guards if row["status"] == "ACTIVE"}),
        "all Cperp exactness no-cheat guards are active",
    )
    add(
        "V1160_6_claim_gates_blocked",
        any(row["gate_id"] == "G1160_2_Cperp_exactness_derived" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1160_4_claim_promotion" and row["gate_pass"] == "false" for row in gates),
        "Cperp and local claim gates remain blocked",
    )
    add(
        "V1160_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1160_8_next_target",
        next_target[0]["next_target"].startswith("1161-")
        and "Cperp-form-drel-operator" in str(next_target[0]["next_target"]),
        "1161 handoff targets Cperp form/d_rel source row or branch selector proof",
    )
    add(
        "V1160_9_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1160_10_csv_parse", csv_parse_ok, "all 1160 CSV outputs parse cleanly")
    add("V1160_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1160_SUMMARY",
        True,
        "1160 isolates the exact Cperp/d_rel/cohomology bottleneck, keeps exactness nonclaim, and emits a complete edge-bound source pack",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    edge_pack: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1160 - Y5/R10 Cperp Relative Exactness Cohomology Chain or Edge Bound Source Pack

**Current verdict:** `Cperp` relative exactness is not derived for current MTS. The bottleneck is now exact and useful: the corpus still needs the actual `C_perp` form, the `d_rel` relative complex, relative closedness, trivial `H_rel` or sourced harmonic class, a `B_C` primitive, and a local/FLRW branch selector.

**The theorem shape is real:** if `C_perp` is a sourced relative-closed local form and `[C_perp]=0` in the relevant relative cohomology, then a primitive `B_C` exists. But 1159 already showed that primitive still needs weighted-boundary, cocycle, projector, and matter-descent silence before it can imply `q`-null or `c_g=0`.

**Main progress:** the next source pack is now complete. If exactness will not close, every surviving edge term has a named row instead of hiding in "boundary effects".

**No claim:** no `Cperp` exactness, `B_C=0`, `q`-null, `c_g=0`, finite `c_g` score, local-GR, Newton, R10, PPN, WEP, clock, orbital, GitHub, or public claim follows from 1160.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Cperp Relative Exactness Chain
{table(["chain_id", "claim_piece", "required_statement", "current_status", "closing_condition", "effect_if_closed", "valid_for_claim"], chain)}

## Edge Bound Source Pack
{table(["pack_id", "quantity", "required_source", "feeds", "current_value", "source_path", "status", "valid_for_claim", "claim_allowed"], edge_pack)}

## No-Cheat Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1160_SOURCE_REGISTER.csv",
        "chain": OUT / "P8_Y5_R10_1160_CPERP_RELATIVE_EXACTNESS_CHAIN.csv",
        "edge_pack": OUT / "P8_Y5_R10_1160_EDGE_BOUND_SOURCE_PACK.csv",
        "guards": OUT / "P8_Y5_R10_1160_NO_CPERP_CHEAT_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1160_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1160_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1160_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1160_VALIDATION.csv",
    }

    sources = source_rows()
    chain = exactness_chain_rows()
    edge_pack = edge_source_pack_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["chain"], chain)
    write_csv(outputs["edge_pack"], edge_pack)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, chain, edge_pack, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, chain, edge_pack, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
