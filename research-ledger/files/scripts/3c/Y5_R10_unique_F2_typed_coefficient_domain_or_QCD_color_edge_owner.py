from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1235"
TITLE = "1235-Y5-R10-unique-F2-typed-coefficient-domain-or-QCD-color-edge-owner"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
UNIQUE_F2_PROOF_PATH = OUT_DIR / f"{PACK_ID}_UNIQUE_F2_TYPED_COEFFICIENT_DOMAIN_PROOF_ATTEMPT.csv"
TYPED_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_TYPED_DOMAIN_REQUIREMENTS.csv"
UNIQUE_F2_BLOCKERS_PATH = OUT_DIR / f"{PACK_ID}_UNIQUE_F2_BLOCKER_LEDGER.csv"
QCD_COLOR_EDGE_PATH = OUT_DIR / f"{PACK_ID}_QCD_COLOR_EDGE_OWNER_PROOF_ATTEMPT.csv"
FINITE_RESIDUAL_PATH = OUT_DIR / f"{PACK_ID}_FINITE_EM_QCD_RESIDUAL_BACKSTOP.csv"
EDGE_STATUS_PATH = OUT_DIR / f"{PACK_ID}_GRAPH_EDGE_STATUS_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1235_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1235_0_1234_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1234_NEXT_TARGET.csv",
            "needle": "NEXT1234_0_1235",
            "purpose": "1234 handoff to unique-F2 typed domain or QCD color edge owner",
        },
        {
            "source_id": "SRC1235_1_1234_unique_F2",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1234_EM_OWNER_UNIQUENESS_PROOF_ATTEMPT.csv",
            "needle": "EMU1234_2_unique_F2",
            "purpose": "unique Maxwell kinetic term blocker",
        },
        {
            "source_id": "SRC1235_2_1234_blocker",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1234_EM_OWNER_BLOCKER_LEDGER.csv",
            "needle": "EMB1234_0_unique_F2_counterexample",
            "purpose": "active hidden scalar or independent Maxwell counterexample",
        },
        {
            "source_id": "SRC1235_3_1234_QCD_fallback",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1234_QUARK_GLUON_EDGE_OWNER_FALLBACK.csv",
            "needle": "QGE1234_1_promising_route",
            "purpose": "staged quark-gluon edge route",
        },
        {
            "source_id": "SRC1235_4_1219_typed_domain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
            "needle": "TVC1219_1_typed_domain_theorem",
            "purpose": "typed coefficient domain conditional theorem",
        },
        {
            "source_id": "SRC1235_5_1219_hidden_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv",
            "needle": "HSC1219_1_alpha",
            "purpose": "hidden scalar gauge-kinetic counterexample",
        },
        {
            "source_id": "SRC1235_6_1220_parent_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "needle": "PTOL1220_1_visible_coefficient_domain",
            "purpose": "parent typed object-language signature gap",
        },
        {
            "source_id": "SRC1235_7_1049_operator_rule",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
            "needle": "OCR1049_1_quotient_descent_selection",
            "purpose": "operator classification and quotient descent conditional rule",
        },
        {
            "source_id": "SRC1235_8_1049_symmetry_fail",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv",
            "needle": "SBT1049_4_product_functor",
            "purpose": "symmetry alone fails; product functor would work if signed",
        },
        {
            "source_id": "SRC1235_9_1051_no_mixed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
            "needle": "NMM1051_2_scalar_counterexample",
            "purpose": "no-mixed morphism scalar counterexample",
        },
        {
            "source_id": "SRC1235_10_1051_scalar_obstruction",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv",
            "needle": "ISO1051_0_hidden_scalar_I",
            "purpose": "invariant scalar obstruction audit",
        },
        {
            "source_id": "SRC1235_11_1114_no_hidden_visible",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "NHV1114_6_verdict",
            "purpose": "no-hidden-visible coefficient theorem still not derived",
        },
        {
            "source_id": "SRC1235_12_1115_local_invariant",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
            "needle": "LIA1115_6_verdict",
            "purpose": "local invariant algebra triviality not derived",
        },
        {
            "source_id": "SRC1235_13_1092_hidden_triviality",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv",
            "needle": "HIT1092_5_verdict",
            "purpose": "hidden invariant triviality still blocked",
        },
        {
            "source_id": "SRC1235_14_1232_edges",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv",
            "needle": "EDGE1232_2_quark_gluon",
            "purpose": "quark-gluon graph edge target",
        },
        {
            "source_id": "SRC1235_15_1232_fractions",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv",
            "needle": "FSP1232_4_QCD_gluon_fraction",
            "purpose": "QCD component fraction source gap",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    unique_f2_proof = [
        {
            "proof_id": "UF21235_0_target",
            "claim_piece": "unique F_Q^2 typed coefficient domain",
            "formal_statement": "Show that visible Maxwell kinetic coefficients have no hidden/local scalar argument slot, so f(I_hid) F_Q^2 and lambda_A F_Q^2 are absent rather than merely tuned.",
            "attempt_result": "TARGET_SHARP",
            "blocker": "must be parent-signed at object-language/action-domain level",
            "effect_if_signed": "kills the sharp EM alpha gauge-kinetic counterexample",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1234_EM_OWNER_UNIQUENESS_PROOF_ATTEMPT.csv", "EMU1234_2_unique_F2"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "UF21235_1_typed_domain_route",
            "claim_piece": "hidden scalar cannot enter Coeff(F_Q^2)",
            "formal_statement": "If Arg(Coeff(F_Q^2)) = Q_vis x Rep_Q x Top_Q and contains no C_hid object, then c(I_hid) F_Q^2 is ill-typed and cannot be written.",
            "attempt_result": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "blocker": "PTOL1220_1 and NHV1114 remain conditional; current corpus has no parent certificate for the coefficient domain",
            "effect_if_signed": "unique-F2 blocker would close for hidden scalar gauge-kinetic terms",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv", "TVC1219_1_typed_domain_theorem"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "UF21235_2_unique_curvature_norm_route",
            "claim_piece": "single parent curvature norm",
            "formal_statement": "If the EM subblock descends from one parent curvature norm with fixed projection and no independent visible counterterm slot, then lambda_A F_Q^2 is absent.",
            "attempt_result": "EXACT_CONDITIONAL_ROUTE_NOT_DERIVED",
            "blocker": "single curvature norm and counterterm exclusion have not been derived from MTS primitives",
            "effect_if_signed": "would close the independent Maxwell normalization branch",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1234_EM_OWNER_BLOCKER_LEDGER.csv", "EMB1234_0_unique_F2_counterexample"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "UF21235_3_product_sequester_route",
            "claim_piece": "product category visible projection",
            "formal_statement": "If C_parent = C_vis x C_hid and Coeff(F_Q^2) factors through pi_vis, then D_hid Coeff(F_Q^2)=0 by chain rule.",
            "attempt_result": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "blocker": "product functor/sequestration is exactly the missing parent route and cannot be inserted after the fact",
            "effect_if_signed": "would force hidden-direction alpha response to vanish",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv", "SBT1049_4_product_functor"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "UF21235_4_invariant_triviality_route",
            "claim_piece": "no hidden scalar invariant",
            "formal_statement": "If O(C_hid)^inv = R on the physical local branch, then any invariant coefficient c:C_hid->R is constant and cannot generate alpha drift.",
            "attempt_result": "EXACT_CONDITIONAL_THEOREM_NOT_DERIVED",
            "blocker": "local/hidden invariant algebra triviality remains unproved; scalar generators are still live obstructions",
            "effect_if_signed": "would remove the scalar argument that powers f(I_hid)F_Q^2",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv", "LIA1115_1_sufficiency"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "UF21235_5_covariance_gauge_fail",
            "claim_piece": "ordinary covariance/gauge invariance ban",
            "formal_statement": "Diffeomorphism covariance and U(1) gauge invariance do not ban f(I_hid)F_Q^2 when I_hid is a scalar and F_Q^2 is gauge invariant.",
            "attempt_result": "INSUFFICIENT_PROVED",
            "blocker": "symmetry permits the counterexample unless a stronger parent-typing rule exists",
            "effect_if_signed": "not applicable; this route is rejected",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv", "TVC1219_4_covariance_gauge_insufficient"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "UF21235_6_scalar_counterexample_status",
            "claim_piece": "surviving scalar counterexample",
            "formal_statement": "If an invariant scalar I_hid survives, c=c0+epsilon I_hid gives a legal covariant coefficient unless typing/triviality forbids the argument.",
            "attempt_result": "COUNTEREXAMPLE_REMAINS_ACTIVE",
            "blocker": "HSC1219_1/NMM1051_2/ISO1051_0 remain active",
            "effect_if_signed": "not signed; finite coefficient residual is mandatory",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv", "NMM1051_2_scalar_counterexample"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "UF21235_7_verdict",
            "claim_piece": "unique F_Q^2 closure",
            "formal_statement": "1235 cannot prove unique F_Q^2 from the current corpus; the theorem is exact only as a parent typed-domain certificate.",
            "attempt_result": "UNIQUE_F2_NOT_CLOSED_DEMOTE_TO_FINITE_RESIDUAL",
            "blocker": "no parent object-language certificate, no unique curvature norm, and no invariant algebra triviality proof",
            "effect_if_signed": "future 1236 certificate could reopen closure; present branch remains nonclaim",
            "source": "UF21235_1 through UF21235_6",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    typed_requirements = [
        {
            "requirement_id": "TREQ1235_0_parent_object_language",
            "required_certificate": "declared parent object-language/action domain before readout or fitting",
            "why_needed": "prevents adding hidden-visible coefficient functions as post-hoc closure terms",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv", "PTOL1220_0_parent_domain"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "TREQ1235_1_visible_coeff_domain",
            "required_certificate": "Arg(Coeff(F_Q^2)) excludes C_hid and hidden invariant scalar arguments",
            "why_needed": "directly forbids f(I_hid)F_Q^2 as ill-typed",
            "current_status": "POWERFUL_RULE_NOT_DERIVED",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv", "PTOL1220_1_visible_coefficient_domain"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "TREQ1235_2_no_extension_marker",
            "required_certificate": "no hidden marker, domain selector, or extension label can be smuggled into a visible coefficient slot",
            "why_needed": "blocks a renamed scalar obstruction from re-entering as a constant-like label",
            "current_status": "NO_EXTENSION_MARKER_PROOF_MISSING",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv", "ISO1051_1_Xhat_value"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "TREQ1235_3_unique_curvature_norm",
            "required_certificate": "one parent curvature norm fixes the EM kinetic normalization and excludes independent lambda_A",
            "why_needed": "hidden scalar exclusion alone does not remove an independent visible Maxwell counterterm",
            "current_status": "UNIQUE_CURVATURE_NORM_NOT_DERIVED",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1234_EM_OWNER_BLOCKER_LEDGER.csv", "EMB1234_0_unique_F2_counterexample"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "TREQ1235_4_readout_radiative_closure",
            "required_certificate": "radiative/readout maps cannot reintroduce hidden dependence into measured alpha",
            "why_needed": "even a tree-level F2 certificate is not enough if clocks/spectroscopy leak hidden dependence",
            "current_status": "READOUT_RADIATIVE_CLOSURE_UNSIGNED",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv", "NHV1114_6_verdict"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "TREQ1235_5_invariant_algebra_triviality",
            "required_certificate": "O(C_hid)^inv = R or an equivalent no-scalar theorem on the physical local branch",
            "why_needed": "removes the scalar data that would feed continuous visible coefficients",
            "current_status": "TRIVIALITY_NOT_DERIVED",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv", "HIT1092_5_verdict"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    unique_f2_blockers = [
        {
            "blocker_id": "UBLOCK1235_0_unique_F2",
            "counterexample_or_gap": "lambda_A F_Q^2 or f(I_hid) F_Q^2",
            "why_it_survives": "ordinary covariance and U(1) gauge invariance allow scalar gauge-kinetic functions",
            "required_to_close": "parent typed coefficient domain and/or unique parent curvature norm",
            "status": "ACTIVE_DEMOTED_TO_FINITE_RESIDUAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "UBLOCK1235_1_parent_typed_domain",
            "counterexample_or_gap": "no certified Arg(Coeff(F_Q^2)) grammar",
            "why_it_survives": "typed-domain theorem exists only conditionally",
            "required_to_close": "signed parent object-language certificate",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "UBLOCK1235_2_scalar_invariant",
            "counterexample_or_gap": "surviving hidden invariant scalar I_hid",
            "why_it_survives": "local invariant algebra triviality has not been proved",
            "required_to_close": "O(C_hid)^inv=R or explicit kill list covering all scalar generators",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "UBLOCK1235_3_visible_counterterm",
            "counterexample_or_gap": "independent visible Maxwell normalization lambda_A",
            "why_it_survives": "unique parent curvature norm is not derived",
            "required_to_close": "no-independent-F2 action theorem",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "UBLOCK1235_4_readout_loop",
            "counterexample_or_gap": "hidden dependence reappears in clocks, spectroscopy, Hodge/coframe, or loop matching",
            "why_it_survives": "radiative/readout closure remains unsigned",
            "required_to_close": "quotient-fixed readout plus radiative closure theorem",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    qcd_color_edge = [
        {
            "edge_id": "QCD1235_0_target",
            "edge": "EDGE1232_2_quark_gluon",
            "claim_piece": "quark-gluon parent graph edge owner",
            "formal_statement": "Prove that light-quark mass and QCD/gluon binding components are connected by a parent-owned color gauge interaction and bound-state map.",
            "proof_result": "TARGET_SHARP",
            "required_parent_owner": "ordinary matter strong-sector action owner",
            "gap": "color sector has not been parent-signed in the MTS action corpus",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "QCD1235_1_color_edge_conditional",
            "edge": "EDGE1232_2_quark_gluon",
            "claim_piece": "nonzero color interaction morphism",
            "formal_statement": "If the parent matter action contains a color connection A_c, quarks in nontrivial SU(3)-like representations, and D_mu q = partial_mu q + i g_s A_mu^a T_a q, then variation gives a nonzero color current and the quark-gluon edge is owned.",
            "proof_result": "EXACT_CONDITIONAL_THEOREM",
            "required_parent_owner": "A_c, representation labels, g_s/current normalization, and gauge kinetic norm all owned by the same parent action",
            "gap": "current corpus supplies the graph template but not the strong-sector parent owner",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "QCD1235_2_hadronization_map",
            "edge": "EDGE1232_2_quark_gluon",
            "claim_piece": "material component transfer",
            "formal_statement": "A color interaction edge only becomes a source-weight edge after a bound-state/hadronization map connects quark/gluon energy fractions to material response variables.",
            "proof_result": "CONDITIONAL_UNSIGNED",
            "required_parent_owner": "parent-owned bound-state map and mass-decomposition basis",
            "gap": "FSP1232_3/FSP1232_4 component fractions are not source-backed claim rows",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "QCD1235_3_finite_component_backstop",
            "edge": "EDGE1232_2_quark_gluon",
            "claim_piece": "finite QCD source residual",
            "formal_statement": "If the color edge cannot be parent-signed, retain F_B,q, F_B,g, delta w_q, and delta w_g as finite nonclaim inputs rather than theorem-zeroes.",
            "proof_result": "BACKSTOP_ACTIVE",
            "required_parent_owner": "source-backed QCD component fractions or a parent zero theorem",
            "gap": "no claim-grade component-fraction table exists yet",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "QCD1235_4_verdict",
            "edge": "EDGE1232_2_quark_gluon",
            "claim_piece": "QCD edge status",
            "formal_statement": "The QCD color edge has a clean conditional proof shape but is not counted until the parent strong-sector action owner and component transfer map are sourced.",
            "proof_result": "QCD_COLOR_EDGE_STAGED_NOT_SIGNED",
            "required_parent_owner": "strong-sector parent action and component-fraction transfer",
            "gap": "owner and source-weight transfer are both missing",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_residuals = [
        {
            "residual_id": "FEMQCD1235_0_EM_alpha",
            "quantity": "b_alpha or c_alpha_DD",
            "source_of_residual": "unclosed unique-F2 / hidden scalar gauge-kinetic counterexample",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "source-backed coefficient prior or parent EM-lock theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEMQCD1235_1_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "source_of_residual": "unowned EM current/source normalization",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "parent current owner or numeric beta prior with source path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEMQCD1235_2_readout_alpha",
            "quantity": "tau_clock/tau_WEP/readout alpha transfer",
            "source_of_residual": "unclosed quotient-fixed readout/radiative descent",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "official readout kernels or parent readout theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEMQCD1235_3_QCD_quark_fraction",
            "quantity": "F_B,q",
            "source_of_residual": "QCD color edge and material decomposition are not parent/source-signed",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "claim-grade quark energy fraction source or parent transfer theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEMQCD1235_4_QCD_gluon_fraction",
            "quantity": "F_B,g",
            "source_of_residual": "gluon/binding component decomposition is not source-backed",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "claim-grade gluon/binding energy fraction source or parent transfer theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEMQCD1235_5_delta_w_qg",
            "quantity": "delta w_q and delta w_g",
            "source_of_residual": "unclosed QCD component coupling response",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "parent zero theorem or finite coupling priors with sourced units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    edge_status = [
        {
            "edge_id": "EDGE1232_0_electron_photon",
            "prior_status": "EM_OWNER_UNIQUENESS_NOT_CLOSED",
            "new_status": "BLOCKED_BY_UNIQUE_F2",
            "reason": "1235 did not close hidden scalar or independent Maxwell F2 counterexamples",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_1_quark_photon",
            "prior_status": "PENDING",
            "new_status": "PENDING",
            "reason": "not attempted in 1235",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_2_quark_gluon",
            "prior_status": "EXACT_CONDITIONAL_ROUTE_STAGED_NOT_SIGNED",
            "new_status": "QCD_COLOR_EDGE_STAGED_NOT_SIGNED",
            "reason": "conditional color-current proof exists but strong-sector owner and component transfer are missing",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1235_0_no_unique_F2_claim",
            "decision": "do not claim unique F_Q^2",
            "because": "typed-domain, unique-curvature, and invariant-triviality routes are exact but unsigned",
            "next_action": "try a parent typed object-language certificate, not another symmetry-only ban",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1235_1_keep_EM_residual",
            "decision": "retain finite EM residual branch",
            "because": "hidden scalar gauge-kinetic and readout/radiative leakage remain live",
            "next_action": "track b_alpha/c_alpha_DD, beta_source_alpha, and readout transfer as nonclaim inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1235_2_QCD_route_promising_but_unsigned",
            "decision": "stage QCD color edge as a cleaner graph route",
            "because": "the interaction-current theorem is crisp if the parent strong sector exists",
            "next_action": "either sign the strong-sector owner or source QCD component fractions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1235_3_local_GR_remains_blocked",
            "decision": "keep local GR/source-side reduction blocked",
            "because": "no ordinary matter graph edge counts and finite residual rows remain active",
            "next_action": "attack the parent certificate before scoring WEP/PPN/local-GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1235_0_unique_F2",
            "claim": "unique F_Q^2 theorem",
            "status": "BLOCKED",
            "reason": "UF21235_7 verdict=UNIQUE_F2_NOT_CLOSED_DEMOTE_TO_FINITE_RESIDUAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1235_1_EM_owner",
            "claim": "EM owner uniqueness and electron-photon edge",
            "status": "BLOCKED",
            "reason": "unique-F2, current, and readout clauses remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1235_2_QCD_color_edge",
            "claim": "quark-gluon edge parent-signed",
            "status": "BLOCKED",
            "reason": "QCD1235_4 verdict=QCD_COLOR_EDGE_STAGED_NOT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1235_3_graph_connectedness",
            "claim": "ordinary matter component graph connected with signed edges",
            "status": "BLOCKED",
            "reason": "no updated edge counts for connected graph",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1235_4_Delta_w_zero",
            "claim": "Delta_w=0 for ordinary matter source components",
            "status": "BLOCKED",
            "reason": "finite EM/QCD residual rows remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1235_5_WEP_R10_PPN_clock",
            "claim": "R10/WEP/PPN/clock local tests pass",
            "status": "BLOCKED",
            "reason": "source-coupling graph and coefficient transfers are not closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1235_6_local_GR",
            "claim": "local GR/Newton source-side reduction",
            "status": "BLOCKED",
            "reason": "local matter coupling closure remains missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1235_0_1236",
            "target_file": "1236-Y5-R10-parent-typed-object-language-certificate-or-QCD-color-owner-deepening.md",
            "target_script": "scripts/Y5_R10_parent_typed_object_language_certificate_or_QCD_color_owner_deepening.py",
            "task": "either write the exact parent typed object-language certificate that makes hidden scalars ill-typed for visible coefficients, or deepen the QCD color-sector owner proof with finite component-source requirements",
            "success_condition": "unique-F2 closes only if the certificate is parent-signed; otherwise QCD edge remains conditional and finite EM/QCD residuals stay explicit",
            "do_not_do": "do not claim EM lock, QCD edge, graph connectedness, Delta_w=0, WEP, PPN, clock, R10, local GR, or public victory from finite residual rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        UNIQUE_F2_PROOF_PATH,
        TYPED_REQUIREMENTS_PATH,
        UNIQUE_F2_BLOCKERS_PATH,
        QCD_COLOR_EDGE_PATH,
        FINITE_RESIDUAL_PATH,
        EDGE_STATUS_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(UNIQUE_F2_PROOF_PATH, unique_f2_proof)
    write_csv(TYPED_REQUIREMENTS_PATH, typed_requirements)
    write_csv(UNIQUE_F2_BLOCKERS_PATH, unique_f2_blockers)
    write_csv(QCD_COLOR_EDGE_PATH, qcd_color_edge)
    write_csv(FINITE_RESIDUAL_PATH, finite_residuals)
    write_csv(EDGE_STATUS_PATH, edge_status)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            unique_f2_proof,
            typed_requirements,
            unique_f2_blockers,
            qcd_color_edge,
            finite_residuals,
            edge_status,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    unique_f2_not_closed = any(
        row["proof_id"] == "UF21235_7_verdict"
        and row["attempt_result"] == "UNIQUE_F2_NOT_CLOSED_DEMOTE_TO_FINITE_RESIDUAL"
        for row in unique_f2_proof
    )
    typed_route_conditional = any(
        row["proof_id"] == "UF21235_1_typed_domain_route"
        and row["attempt_result"] == "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED"
        for row in unique_f2_proof
    )
    covariance_rejected = any(
        row["proof_id"] == "UF21235_5_covariance_gauge_fail"
        and row["attempt_result"] == "INSUFFICIENT_PROVED"
        for row in unique_f2_proof
    )
    hidden_scalar_active = any(
        row["blocker_id"] == "UBLOCK1235_2_scalar_invariant" and row["status"] == "ACTIVE"
        for row in unique_f2_blockers
    )
    qcd_staged = any(
        row["edge_id"] == "QCD1235_4_verdict"
        and row["proof_result"] == "QCD_COLOR_EDGE_STAGED_NOT_SIGNED"
        for row in qcd_color_edge
    )
    qcd_conditional = any(
        row["edge_id"] == "QCD1235_1_color_edge_conditional"
        and row["proof_result"] == "EXACT_CONDITIONAL_THEOREM"
        for row in qcd_color_edge
    )
    finite_backstop_active = len(finite_residuals) == 6 and all(
        row["status"] == "FINITE_RESIDUAL_ACTIVE_NONCLAIM" for row in finite_residuals
    )
    no_edges_signed = all(parse_bool(row["counts_for_connected_graph"]) is False for row in edge_status)
    gates_blocked = all(row["status"] == "BLOCKED" and is_false(row, "claim_allowed") for row in claim_gates)
    next_is_1236 = next_target[0]["target_file"].startswith("1236-Y5-R10-parent-typed-object-language")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1235_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1235_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1235_2_unique_F2_not_closed",
            "unique-F2 is not promoted",
            unique_f2_not_closed,
            "UF21235_7 verdict=UNIQUE_F2_NOT_CLOSED_DEMOTE_TO_FINITE_RESIDUAL",
        ),
        validation_row(
            "VAL1235_3_typed_route_conditional",
            "typed coefficient route remains conditional",
            typed_route_conditional,
            "UF21235_1 exact conditional theorem not parent-signed",
        ),
        validation_row(
            "VAL1235_4_covariance_gauge_rejected",
            "covariance/gauge-only ban is rejected",
            covariance_rejected,
            "UF21235_5 records f(I_hid)F_Q^2 remains symmetry-allowed",
        ),
        validation_row(
            "VAL1235_5_hidden_scalar_active",
            "hidden scalar obstruction remains active",
            hidden_scalar_active,
            "UBLOCK1235_2 status=ACTIVE",
        ),
        validation_row(
            "VAL1235_6_QCD_conditional",
            "QCD color edge conditional proof is recorded",
            qcd_conditional,
            "QCD1235_1 exact conditional theorem",
        ),
        validation_row(
            "VAL1235_7_QCD_not_signed",
            "QCD color edge is not counted",
            qcd_staged,
            "QCD1235_4 verdict=QCD_COLOR_EDGE_STAGED_NOT_SIGNED",
        ),
        validation_row(
            "VAL1235_8_finite_backstop",
            "finite EM/QCD residual backstop remains active",
            finite_backstop_active,
            f"finite_residual_rows={len(finite_residuals)}",
        ),
        validation_row(
            "VAL1235_9_no_edges_signed",
            "no graph edge is counted as parent-signed",
            no_edges_signed,
            "counts_for_connected_graph=false for all updated edges",
        ),
        validation_row(
            "VAL1235_10_claim_gates_blocked",
            "all claim gates remain blocked",
            gates_blocked,
            f"blocked_gates={sum(row['status'] == 'BLOCKED' for row in claim_gates)}/{len(claim_gates)}",
        ),
        validation_row(
            "VAL1235_11_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1235_12_next_target_1236",
            "next target is parent typed certificate or QCD owner deepening",
            next_is_1236,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1235_13_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1235_14_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1235_15_overall",
            "overall 1235 validation",
            all(row["status"] == "PASS" for row in validation),
            "1235 demotes unique-F2 to finite EM residual, records typed-domain certificate requirements, and stages QCD color edge without claiming it",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1235 does **not** close `unique F_Q^2`. The clean typed-domain proof exists only conditionally: hidden scalar coefficient maps are ill-typed only after a parent object-language/action-domain certificate is actually signed.",
        "",
        "**Main progress:** the blocker is now precise. Ordinary covariance and U(1) gauge symmetry are not enough; the required missing object is a parent typed coefficient-domain certificate or unique parent curvature norm. The QCD color edge has a crisp conditional owner route, but it is not counted.",
        "",
        "**No-claim guard:** no EM lock, QCD edge, graph connectedness, `Delta_w=0`, R10, WEP, PPN, clock, orbital, local-GR, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Unique F2 Typed Coefficient Domain Proof Attempt",
        markdown_table(unique_f2_proof, list(unique_f2_proof[0].keys())),
        "",
        "## Typed Domain Requirements",
        markdown_table(typed_requirements, list(typed_requirements[0].keys())),
        "",
        "## Unique F2 Blocker Ledger",
        markdown_table(unique_f2_blockers, list(unique_f2_blockers[0].keys())),
        "",
        "## QCD Color Edge Owner Proof Attempt",
        markdown_table(qcd_color_edge, list(qcd_color_edge[0].keys())),
        "",
        "## Finite EM/QCD Residual Backstop",
        markdown_table(finite_residuals, list(finite_residuals[0].keys())),
        "",
        "## Graph Edge Status Update",
        markdown_table(edge_status, list(edge_status[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
