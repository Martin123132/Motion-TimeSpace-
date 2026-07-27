from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1219"
TITLE = "1219-Y5-R10-typed-visible-coefficient-functor-or-hidden-scalar-counterexample-lock"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
FUNCTOR_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv"
CONDITIONAL_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_NO_HIDDEN_ARGUMENT_CONDITIONAL_THEOREM.csv"
COUNTEREXAMPLE_LOCK_PATH = OUT_DIR / f"{PACK_ID}_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv"
CROSS_CHANNEL_PATH = OUT_DIR / f"{PACK_ID}_CROSS_CHANNEL_COUPLING_IMPACT_LEDGER.csv"
FINITE_ROWS_PATH = OUT_DIR / f"{PACK_ID}_FINITE_COUPLING_CLOSURE_DEBT_ROWS.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_FEED_UPDATE.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_PRODUCT_RUNNER_STUB.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1219_VALIDATION.csv"


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


def is_false(row: dict[str, object], key: str) -> bool:
    value = row.get(key, False)
    if isinstance(value, bool):
        return value is False
    return str(value).strip().lower() == "false"


def has_missing(row: dict[str, object]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values()).upper()


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise ValueError(f"missing row {key}={value}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1219_0_1218_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1218_NEXT_TARGET.csv",
            "needle": "1219-Y5-R10-typed-visible-coefficient-functor-or-hidden-scalar-counterexample-lock.md",
            "purpose": "1218 handoff to typed visible coefficient functor target",
        },
        {
            "source_id": "SRC1219_1_1218_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1218_ALPHA_SURFACE_OPERATOR_OWNER_AUDIT.csv",
            "needle": "OWNER1218_6_verdict",
            "purpose": "parent alpha/surface operator owner not derived",
        },
        {
            "source_id": "SRC1219_2_1218_counterexamples",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1218_COUNTEREXAMPLE_RETENTION_LEDGER.csv",
            "needle": "CX1218_1_hidden_F2",
            "purpose": "hidden scalar counterexamples retained",
        },
        {
            "source_id": "SRC1219_3_1049_classification",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
            "needle": "OCR1049_5_verdict",
            "purpose": "operator classification rule attempt",
        },
        {
            "source_id": "SRC1219_4_1049_symmetry",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv",
            "needle": "SBT1049_4_product_functor",
            "purpose": "symmetry ban and product functor gate",
        },
        {
            "source_id": "SRC1219_5_1051_no_mixed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
            "needle": "NMM1051_5_verdict",
            "purpose": "no mixed morphism lemma attempt",
        },
        {
            "source_id": "SRC1219_6_1051_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv",
            "needle": "ISO1051_0_hidden_scalar_I",
            "purpose": "hidden scalar obstruction audit",
        },
        {
            "source_id": "SRC1219_7_1114_no_hom",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "NHV1114_6_verdict",
            "purpose": "typed/product-category no-hidden-visible theorem attempt",
        },
        {
            "source_id": "SRC1219_8_1114_obstructions",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv",
            "needle": "OBS1114_0_grammar",
            "purpose": "coupling obstruction ledger",
        },
        {
            "source_id": "SRC1219_9_1115_invariant",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
            "needle": "LIA1115_6_verdict",
            "purpose": "local invariant algebra triviality attempt",
        },
        {
            "source_id": "SRC1219_10_1092_hidden",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv",
            "needle": "HIT1092_5_verdict",
            "purpose": "hidden invariant triviality attempt",
        },
        {
            "source_id": "SRC1219_11_1092_generators",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv",
            "needle": "GEN1092_3_memory_scalar",
            "purpose": "surviving hidden/invariant generators",
        },
        {
            "source_id": "SRC1219_12_980_functor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "NMF980_7_verdict",
            "purpose": "no-marker functor theorem and scalar obstruction",
        },
        {
            "source_id": "SRC1219_13_980_counterexamples",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv",
            "needle": "CEX980_0_theta_IQ",
            "purpose": "active marker/coupling counterexamples",
        },
        {
            "source_id": "SRC1219_14_1045_functor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            "needle": "MFS1045_6_verdict",
            "purpose": "matter functor signature not parent-signed",
        },
        {
            "source_id": "SRC1219_15_1055_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_6_single_parent_action",
            "purpose": "single parent action contract candidate",
        },
        {
            "source_id": "SRC1219_16_1066_typing",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
            "needle": "OLT1066_6_verdict",
            "purpose": "object-language typing not parent-derived",
        },
        {
            "source_id": "SRC1219_17_1066_domain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
            "needle": "ODR1066_4_verdict",
            "purpose": "operator-domain source-scalar exclusion not derived",
        },
        {
            "source_id": "SRC1219_18_1088_MOMS",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
            "needle": "MOMS1088_7_verdict",
            "purpose": "ordinary matter signature remains unsigned",
        },
        {
            "source_id": "SRC1219_19_1088_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
            "needle": "THM1088_6_current_corpus_verdict",
            "purpose": "conditional zero theorem not promoted",
        },
        {
            "source_id": "SRC1219_20_1218_thresholds",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1218_THRESHOLD_CARRY_FORWARD_NONCLAIM.csv",
            "needle": "TCF1218_0_alpha",
            "purpose": "finite coefficient threshold rows remain nonclaim",
        },
    ]

    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    threshold_1218 = read_csv(OUT_DIR / "P8_Y5_R10_1218_THRESHOLD_CARRY_FORWARD_NONCLAIM.csv")
    alpha_threshold = find_row(threshold_1218, "threshold_id", "TCF1218_0_alpha")
    surface_threshold = find_row(threshold_1218, "threshold_id", "TCF1218_1_surface")
    common_threshold = find_row(threshold_1218, "threshold_id", "TCF1218_2_common_abs")

    functor_rows = [
        {
            "attempt_id": "TVC1219_0_target",
            "claim_piece": "typed visible coefficient functor",
            "formal_statement": "Coeff_vis(O_vis) has domain only Q_obs x Rep_vis x Top_vis x fixed constants; hidden/local representatives I_hid are not well-typed arguments.",
            "result": "TARGET_SHARP",
            "proof_or_blocker": "would remove hidden scalar arguments from alpha, mass, surface/binding, clock, WEP, and source-weight coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TVC1219_1_typed_domain_theorem",
            "claim_piece": "no hidden argument by grammar",
            "formal_statement": "If parent syntax supplies no morphism C_hid -> Arg(Coeff_vis), then c_vis(I_hid) cannot be formed.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_blocker": "type checking kills the expression before dynamics; this is the cleanest non-tuning route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TVC1219_2_product_projection_theorem",
            "claim_piece": "visible coefficient factors through visible projection",
            "formal_statement": "If C_parent=C_vis x C_hid and coeff_vis=coeff_bar o pi_vis, then D_hid coeff_vis=0.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_blocker": "chain rule through pi_vis kills hidden tangent vectors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TVC1219_3_current_corpus_signature",
            "claim_piece": "current corpus signs the typed/product grammar",
            "formal_statement": "MTS parent action already proves all visible coefficients are typed/factored away from hidden scalar arguments.",
            "result": "NOT_DERIVED",
            "proof_or_blocker": "OCR1049, NHV1114, OLT1066, and MFS1045 keep the grammar/action signature conditional rather than parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TVC1219_4_covariance_gauge_insufficient",
            "claim_piece": "diffeomorphism/U(1) covariance bans hidden coefficient maps",
            "formal_statement": "f(I_hid)F_Q^2, m_A(I_hid), binding(I_hid), clock(I_hid), and w_A(I_hid) are forbidden by ordinary covariance/gauge invariance.",
            "result": "FALSE",
            "proof_or_blocker": "1049/1099/1114 show these are scalar-density or visible-gauge-invariant terms unless typed/sequestered out",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TVC1219_5_invariant_triviality_alternative",
            "claim_piece": "no hidden scalar inputs exist",
            "formal_statement": "O(C_hid)^inv=R, so every hidden coefficient map into R is constant.",
            "result": "EXACT_CONDITIONAL_BUT_NOT_DERIVED",
            "proof_or_blocker": "HIT1092_5 and LIA1115_6 keep surviving generator debts; scalar counterexample remains active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TVC1219_6_verdict",
            "claim_piece": "derive typed visible coefficient functor now",
            "formal_statement": "visible coefficient functors are parent-typed to exclude hidden/local scalar arguments",
            "result": "TYPED_VISIBLE_COEFFICIENT_FUNCTOR_NOT_DERIVED",
            "proof_or_blocker": "conditional theorem is exact, but parent grammar, product sequester, no-extension, invariant triviality, and radiative/readout closure are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_rows = [
        {
            "theorem_id": "NHA1219_0_type_rule",
            "assumption": "Visible coefficient functors have typed domain Arg_vis = Q_obs x Rep_vis x fixed Top_vis; C_hid is not in Arg_vis.",
            "derivation": "A term c(I_hid) O_vis is syntactically ill-typed; therefore no vertical derivative of c can source O_vis.",
            "would_kill": "f(I_hid)F_Q^2; a_surface(I_hid); m_A(I_hid); clock(I_hid); source_weight(I_hid)",
            "promotion_status": "CONDITIONAL_ONLY",
            "missing_for_claim": "parent typed object language and action-domain signature",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "NHA1219_1_product_rule",
            "assumption": "C_parent=C_vis x C_hid and every visible coefficient factors as c_vis=c_bar(pi_vis(-)).",
            "derivation": "For v_hid in ker(D pi_vis), Lie_v c_vis = D c_bar[D pi_vis(v_hid)] = 0.",
            "would_kill": "all smooth hidden-to-visible coefficient morphisms",
            "promotion_status": "CONDITIONAL_ONLY",
            "missing_for_claim": "parent product-category/sequester theorem and radiative/readout preservation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "NHA1219_2_trivial_invariant_rule",
            "assumption": "O(C_hid)^inv=R on the physical local branch.",
            "derivation": "Any invariant coefficient c:C_hid -> R factors through constants, so Lie_v c=0.",
            "would_kill": "continuous scalar coefficient maps if all hidden invariants are removed",
            "promotion_status": "CONDITIONAL_ONLY",
            "missing_for_claim": "surviving generator debts in 1092/1115",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "NHA1219_3_combined_zero_rule",
            "assumption": "NHA1219_0 or NHA1219_1 holds, and EFT/readout maps preserve the same type rule.",
            "derivation": "bare and effective visible coefficients have no hidden arguments; local vertical residuals from coefficient drift vanish.",
            "would_kill": "alpha/surface/clock/WEP/source-weight coefficient branch as a structural theorem",
            "promotion_status": "NOT_PROMOTED",
            "missing_for_claim": "radiative/readout closure and parent grammar signature",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    counterexample_rows = [
        {
            "counterexample_id": "HSC1219_0_generic_scalar",
            "hidden_input": "I_hid in O(C_hid)^inv with dI_hid != 0",
            "visible_coefficient_map": "c_vis = c0 + epsilon I_hid",
            "visible_operator": "generic O_vis scalar density",
            "why_allowed_now": "current corpus has not typed out hidden arguments or proved invariant algebra triviality",
            "blocks": "global no-hidden-visible coefficient theorem",
            "status": "LOCKED_AS_ACTIVE_COUNTEREXAMPLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "HSC1219_1_alpha",
            "hidden_input": "I_hid or Xhat",
            "visible_coefficient_map": "f(I_hid) F_Q^2",
            "visible_operator": "EM kinetic / alpha",
            "why_allowed_now": "diffeomorphism and visible U(1) gauge invariance allow scalar gauge kinetic functions",
            "blocks": "c_alpha_DD=b_alpha theorem-zero",
            "status": "LOCKED_AS_ACTIVE_COUNTEREXAMPLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "HSC1219_2_surface_binding",
            "hidden_input": "I_hid, marker, or domain scalar",
            "visible_coefficient_map": "a_surface(I_hid), B_A(I_hid), Lambda_QCD(I_hid)",
            "visible_operator": "binding/surface material response",
            "why_allowed_now": "ordinary-matter constant superselection and visible coefficient typing are unsigned",
            "blocks": "c_surface_DD theorem-zero",
            "status": "LOCKED_AS_ACTIVE_COUNTEREXAMPLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "HSC1219_3_clock",
            "hidden_input": "I_hid after readout/EFT reduction",
            "visible_coefficient_map": "nu_i(I_hid) or alpha_eff(I_hid)",
            "visible_operator": "clock/spectroscopy readout",
            "why_allowed_now": "radiative/readout closure remains unsigned",
            "blocks": "clock-product transfer and alpha readout silence",
            "status": "LOCKED_AS_ACTIVE_COUNTEREXAMPLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "HSC1219_4_source_weight",
            "hidden_input": "marker/domain/source scalar",
            "visible_coefficient_map": "w_A(I_hid) S_A or kappa_A(I_hid) T_A",
            "visible_operator": "WEP/source weight/gravitational source coupling",
            "why_allowed_now": "object-language typing and action-scale/current owner are not parent-derived",
            "blocks": "source-weight and local-GR source-side theorem-zero",
            "status": "LOCKED_AS_ACTIVE_COUNTEREXAMPLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    cross_channel_rows = [
        {
            "impact_id": "IMPACT1219_0_alpha",
            "sector": "EM/alpha",
            "row_hit": "OWNER1218_0_alpha_EM_F2_image; CPRIor alpha chain",
            "if_type_rule_signed": "c_alpha_DD/b_alpha can move to theorem-zero after EM-F2/readout closure",
            "if_not_signed": "retain alpha finite coefficient/prior source rows",
            "current_status": "FINITE_COUPLING_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "impact_id": "IMPACT1219_1_surface",
            "sector": "surface/binding",
            "row_hit": "OWNER1218_3_surface_binding_superselection",
            "if_type_rule_signed": "c_surface_DD can be zero if binding constants are fixed representation/superselection data",
            "if_not_signed": "retain surface finite coefficient/prior source rows",
            "current_status": "FINITE_COUPLING_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "impact_id": "IMPACT1219_2_clock",
            "sector": "clock/readout",
            "row_hit": "AOR1051_3_verdict; HSC1219_3_clock",
            "if_type_rule_signed": "clock coefficient drift can be killed only if readout/EFT preserves the same typing",
            "if_not_signed": "retain b_alpha*tau_clock and clock-readout finite products",
            "current_status": "READOUT_CLOSURE_STILL_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "impact_id": "IMPACT1219_3_WEP_source",
            "sector": "WEP/source weights",
            "row_hit": "SSE1066_5_verdict; HSC1219_4_source_weight",
            "if_type_rule_signed": "source-only species scalars are forbidden if common action-scale/current owner also signs",
            "if_not_signed": "retain finite Delta_w/source-weight prior rows",
            "current_status": "SOURCE_COUPLING_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "impact_id": "IMPACT1219_4_local_GR",
            "sector": "local GR/Newton source branch",
            "row_hit": "MFS1045_6_verdict; CG1066_4_local_GR_source_branch",
            "if_type_rule_signed": "removes one class of source-side leaks but still needs EH/source Hamiltonian/PPN gates",
            "if_not_signed": "local-GR branch remains claim-blocked",
            "current_status": "NOT_SUFFICIENT_FOR_LOCAL_GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_rows = [
        {
            "debt_id": "FC1219_0_alpha",
            "coefficient_or_debt": "c_alpha_DD / b_alpha",
            "retained_counterexample": "HSC1219_1_alpha",
            "threshold_or_source": alpha_threshold["threshold_abs"],
            "required_to_promote": "typed no-hidden coefficient theorem plus EM-F2/readout closure, or external source-backed coefficient prior",
            "current_status": "FINITE_NONCLAIM_CLOSURE_DEBT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "debt_id": "FC1219_1_surface",
            "coefficient_or_debt": "c_surface_DD",
            "retained_counterexample": "HSC1219_2_surface_binding",
            "threshold_or_source": surface_threshold["threshold_abs"],
            "required_to_promote": "typed matter coefficient functor plus constant-superselection/readout closure, or external source-backed prior",
            "current_status": "FINITE_NONCLAIM_CLOSURE_DEBT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "debt_id": "FC1219_2_common_norm",
            "coefficient_or_debt": "C_parent vector norm",
            "retained_counterexample": "HSC1219_0_generic_scalar",
            "threshold_or_source": common_threshold["threshold_abs"],
            "required_to_promote": "same-branch vector norm fixed before material choice",
            "current_status": "FINITE_NONCLAIM_CLOSURE_DEBT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "debt_id": "FC1219_3_tail",
            "coefficient_or_debt": "q_tail(A)",
            "retained_counterexample": "HSC1219_2_surface_binding;HSC1219_4_source_weight",
            "threshold_or_source": "MISSING_TAIL_ENVELOPE",
            "required_to_promote": "basis completeness theorem or empirical all-material tail envelope",
            "current_status": "FINITE_NONCLAIM_CLOSURE_DEBT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "debt_id": "FC1219_4_readout",
            "coefficient_or_debt": "effective/readout coefficient drift",
            "retained_counterexample": "HSC1219_3_clock",
            "threshold_or_source": "MISSING_RADIOUT_CLOSURE",
            "required_to_promote": "renormalized/readout functor preserves the same typed coefficient rule",
            "current_status": "FINITE_NONCLAIM_CLOSURE_DEBT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed_rows = [
        {
            "feed_id": "FEED1219_0_to_OWNER1218_2",
            "target_row": "OWNER1218_2_alpha_counterterm_obstruction",
            "update": "no-hidden-visible type rule remains conditional; alpha hidden-F2 counterexample locked active",
            "source_rows": "TVC1219_6_verdict;HSC1219_1_alpha",
            "current_status": "HIDDEN_F2_COUNTEREXAMPLE_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1219_1_to_OWNER1218_4",
            "target_row": "OWNER1218_4_surface_hidden_coefficient_obstruction",
            "update": "surface/binding hidden coefficient map remains legal unless typed matter coefficient functor is parent-signed",
            "source_rows": "TVC1219_3_current_corpus_signature;HSC1219_2_surface_binding",
            "current_status": "SURFACE_HIDDEN_COEFFICIENT_COUNTEREXAMPLE_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1219_2_to_PSRC1218",
            "target_row": "PSRC1218_0_alpha_parent;PSRC1218_2_surface_parent;PSRC1218_5_tail_envelope",
            "update": "no theorem-zero or coefficient prior acquired; finite closure-debt rows now carry explicit hidden-scalar counterexamples",
            "source_rows": "FC1219_0_alpha;FC1219_1_surface;FC1219_3_tail",
            "current_status": "FINITE_COUPLING_DEBT_EXPLICIT_COUNTEREXAMPLE_LOCK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_rows = [
        {
            "runner_id": "APR1219_0_typed_functor_stub",
            "typed_functor_claim_valid": False,
            "hidden_counterexamples_locked": 5,
            "finite_closure_debt_rows": 5,
            "valid_prediction_rows": 0,
            "claim_allowed": False,
            "expected_result": "reject typed-functor theorem promotion and retain finite coupling debts",
            "reason": "parent grammar/product sequester/invariant triviality/radiative closure are unsigned",
            "valid_for_claim": False,
        }
    ]

    decisions = [
        {
            "decision_id": "DEC1219_0_no_promotion",
            "decision": "do not promote the typed visible coefficient functor",
            "because": "the theorem is exact conditionally, but the parent grammar/action-domain signature is not derived",
            "next_action": "target the parent typed object-language signature directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1219_1_counterexample_lock",
            "decision": "lock the hidden-scalar counterexample into every finite coupling row",
            "because": "one surviving invariant scalar can feed continuous visible coefficients",
            "next_action": "no finite coupling row may be retired without killing HSC1219 rows or sourcing a prior",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1219_2_next_route",
            "decision": "derive the parent typed object-language signature next",
            "because": "that is the most leverage per derivation: it attacks coupling, WEP, clocks, alpha, and source weights together",
            "next_action": "build or reject a parent grammar/signature certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1219_0_sources",
            "gate": "source path and needle audit",
            "status": "PASS",
            "reason": "all local sources used by 1219 are traceable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1219_1_typed_functor",
            "gate": "typed visible coefficient functor derived",
            "status": "BLOCKED",
            "reason": "TVC1219_6_verdict=TYPED_VISIBLE_COEFFICIENT_FUNCTOR_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1219_2_hidden_scalar",
            "gate": "hidden-scalar counterexample removed",
            "status": "BLOCKED",
            "reason": "HSC1219 rows remain active counterexamples",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1219_3_finite_debts",
            "gate": "finite coupling debts retired",
            "status": "BLOCKED",
            "reason": "FC1219 rows remain finite nonclaim closure debts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1219_4_local_GR",
            "gate": "local GR/Newton source branch closes from typed rule",
            "status": "BLOCKED",
            "reason": "typed rule would help but does not replace EH/source Hamiltonian/PPN gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1219_5_product",
            "gate": "claim-valid WEP/local product",
            "status": "BLOCKED",
            "reason": "valid_prediction_rows=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1219_0_1220",
            "target_file": "1220-Y5-R10-parent-typed-object-language-signature-or-finite-coupling-closure.md",
            "target_script": "scripts/Y5_R10_parent_typed_object_language_signature_or_finite_coupling_closure.py",
            "task": "try to build a parent typed object-language/action-domain signature that forbids hidden arguments in visible coefficient functors; if it cannot be built, demote the no-hidden-visible route to explicit finite-coupling closure",
            "success_condition": "a signed parent grammar certificate exists for visible coefficients, or all affected alpha/surface/clock/WEP/source-weight rows are explicitly finite closure debts",
            "do_not_do": "do not claim covariance/gauge invariance is enough; do not retire finite rows from absence in a draft action; do not claim WEP/local-GR/R10; do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    functor_fields = ["attempt_id", "claim_piece", "formal_statement", "result", "proof_or_blocker", "valid_for_claim", "claim_allowed"]
    theorem_fields = ["theorem_id", "assumption", "derivation", "would_kill", "promotion_status", "missing_for_claim", "valid_for_claim", "claim_allowed"]
    counterexample_fields = ["counterexample_id", "hidden_input", "visible_coefficient_map", "visible_operator", "why_allowed_now", "blocks", "status", "valid_for_claim", "claim_allowed"]
    impact_fields = ["impact_id", "sector", "row_hit", "if_type_rule_signed", "if_not_signed", "current_status", "valid_for_claim", "claim_allowed"]
    finite_fields = ["debt_id", "coefficient_or_debt", "retained_counterexample", "threshold_or_source", "required_to_promote", "current_status", "valid_for_claim", "claim_allowed"]
    feed_fields = ["feed_id", "target_row", "update", "source_rows", "current_status", "valid_for_claim", "claim_allowed"]
    runner_fields = ["runner_id", "typed_functor_claim_valid", "hidden_counterexamples_locked", "finite_closure_debt_rows", "valid_prediction_rows", "claim_allowed", "expected_result", "reason", "valid_for_claim"]
    decision_fields = ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(FUNCTOR_ATTEMPT_PATH, functor_rows, functor_fields)
    write_csv(CONDITIONAL_THEOREM_PATH, theorem_rows, theorem_fields)
    write_csv(COUNTEREXAMPLE_LOCK_PATH, counterexample_rows, counterexample_fields)
    write_csv(CROSS_CHANNEL_PATH, cross_channel_rows, impact_fields)
    write_csv(FINITE_ROWS_PATH, finite_rows, finite_fields)
    write_csv(FEED_PATH, feed_rows, feed_fields)
    write_csv(RUNNER_PATH, runner_rows, runner_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        FUNCTOR_ATTEMPT_PATH,
        CONDITIONAL_THEOREM_PATH,
        COUNTEREXAMPLE_LOCK_PATH,
        CROSS_CHANNEL_PATH,
        FINITE_ROWS_PATH,
        FEED_PATH,
        RUNNER_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = read_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    target_sharp = any(row["attempt_id"] == "TVC1219_0_target" and row["result"] == "TARGET_SHARP" for row in functor_rows)
    conditional_theorems_present = all(
        any(row["theorem_id"] == theorem_id and row["promotion_status"] in {"CONDITIONAL_ONLY", "NOT_PROMOTED"} for row in theorem_rows)
        for theorem_id in ["NHA1219_0_type_rule", "NHA1219_1_product_rule", "NHA1219_2_trivial_invariant_rule", "NHA1219_3_combined_zero_rule"]
    )
    functor_not_overclaimed = any(row["attempt_id"] == "TVC1219_6_verdict" and row["result"] == "TYPED_VISIBLE_COEFFICIENT_FUNCTOR_NOT_DERIVED" for row in functor_rows)
    covariance_rejected = any(row["attempt_id"] == "TVC1219_4_covariance_gauge_insufficient" and row["result"] == "FALSE" for row in functor_rows)
    counterexamples_locked = all(row["status"] == "LOCKED_AS_ACTIVE_COUNTEREXAMPLE" for row in counterexample_rows)
    finite_debts_retained = all(row["current_status"] == "FINITE_NONCLAIM_CLOSURE_DEBT" for row in finite_rows)
    threshold_rows_positive = all(float(row["threshold_or_source"]) > 0 for row in finite_rows[:3])
    missing_rows_nonclaim = all(not (has_missing(row) and not is_false(row, "valid_for_claim")) for row in finite_rows + feed_rows)
    runner_refuses = runner_rows[0]["valid_prediction_rows"] == 0 and not runner_rows[0]["claim_allowed"]
    claim_locks_blocked = all(
        any(row["gate_id"] == gate_id and row["status"] == "BLOCKED" for row in claim_gates)
        for gate_id in ["GATE1219_1_typed_functor", "GATE1219_2_hidden_scalar", "GATE1219_3_finite_debts", "GATE1219_4_local_GR", "GATE1219_5_product"]
    )
    no_claim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for row in functor_rows + theorem_rows + counterexample_rows + cross_channel_rows + finite_rows + feed_rows + runner_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1220 = next_rows[0]["target_file"].startswith("1220-")

    validation_rows = [
        validation_row("VAL1219_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1219_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1219_2_target_sharp", "typed functor target is sharp", target_sharp, "TVC1219_0_target=TARGET_SHARP"),
        validation_row("VAL1219_3_conditionals_present", "conditional theorems are recorded", conditional_theorems_present, "type/product/triviality/readout conditional rules present"),
        validation_row("VAL1219_4_functor_not_overclaimed", "typed functor not overclaimed", functor_not_overclaimed, "TVC1219_6_verdict=TYPED_VISIBLE_COEFFICIENT_FUNCTOR_NOT_DERIVED"),
        validation_row("VAL1219_5_covariance_rejected", "covariance/gauge shortcut rejected", covariance_rejected, "TVC1219_4 result=FALSE"),
        validation_row("VAL1219_6_counterexamples_locked", "hidden scalar counterexamples locked", counterexamples_locked, "; ".join(row["counterexample_id"] for row in counterexample_rows)),
        validation_row("VAL1219_7_finite_debts_retained", "finite coupling debts retained", finite_debts_retained, "; ".join(row["debt_id"] for row in finite_rows)),
        validation_row("VAL1219_8_thresholds_positive", "carried numeric thresholds are positive", threshold_rows_positive, "; ".join(f"{row['debt_id']}={row['threshold_or_source']}" for row in finite_rows[:3])),
        validation_row("VAL1219_9_missing_rows_nonclaim", "no MISSING row is valid for claim", missing_rows_nonclaim, "tail/readout missing rows remain nonclaim"),
        validation_row("VAL1219_10_runner_refuses", "runner stub refuses missing product", runner_refuses, "valid_prediction_rows=0 and claim_allowed=false"),
        validation_row("VAL1219_11_claim_locks_blocked", "claim locks remain blocked", claim_locks_blocked, "typed functor, hidden scalar, finite debt, local-GR, and product gates blocked"),
        validation_row("VAL1219_12_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1219_13_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1219_14_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1219_15_next_target", "next target is staged", next_1220, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1219_16_overall",
            "overall 1219 validation",
            validation_pass,
            "1219 typed visible coefficient functor pack is reproducible, nonclaim, and counterexample-locked" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1219 Y5/R10 Typed Visible Coefficient Functor Or Hidden Scalar Counterexample Lock

**Current verdict:** 1219 does **not** derive the typed visible coefficient functor. It does lock the hidden/local scalar counterexample into the finite-coupling branch, so alpha, surface/binding, clock, WEP, and source-weight rows cannot be retired by silence or aesthetic minimality.

**Main progress:** we now have an exact conditional theorem: if visible coefficient functors are parent-typed to exclude hidden/local scalar arguments, hidden coefficient drift vanishes by syntax/chain rule. But the current corpus has not signed that parent grammar, product sequester, invariant-algebra triviality, or radiative/readout closure.

**Practical consequence:** the coupling problem has a clean win condition. Either derive a parent typed object-language/action-domain certificate, or carry finite coupling closure debts explicitly with the hidden-scalar counterexample attached.

## Source Register

{markdown_table(source_rows, source_fields)}

## Typed Visible Coefficient Functor Attempt

{markdown_table(functor_rows, functor_fields)}

## No-Hidden-Argument Conditional Theorem

{markdown_table(theorem_rows, theorem_fields)}

## Hidden Scalar Counterexample Lock

{markdown_table(counterexample_rows, counterexample_fields)}

## Cross-Channel Coupling Impact Ledger

{markdown_table(cross_channel_rows, impact_fields)}

## Finite Coupling Closure Debt Rows

{markdown_table(finite_rows, finite_fields)}

## Feed Update

{markdown_table(feed_rows, feed_fields)}

## Product Runner Stub

{markdown_table(runner_rows, runner_fields)}

## Decision Ledger

{markdown_table(decisions, decision_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print("typed_visible_coefficient_functor_derived=false")
    print("hidden_scalar_counterexamples_locked=true")
    print("valid_prediction_rows=0")


if __name__ == "__main__":
    main()
