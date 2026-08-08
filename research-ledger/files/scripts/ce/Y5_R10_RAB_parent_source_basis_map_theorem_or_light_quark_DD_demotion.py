from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1331"
TITLE = "1331-Y5-R10-RAB-parent-source-basis-map-theorem-or-light-quark-DD-demotion"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
THEOREM_PATH = OUT_DIR / f"{PACK_ID}_PARENT_SOURCE_BASIS_MAP_THEOREM.csv"
CLAUSE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_MAP_CLAUSE_AUDIT.csv"
COMPONENT_DEMOTION_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_DD_DEMOTION_LEDGER.csv"
PROMOTION_LADDER_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_PROMOTION_LADDER.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_DELTA_W_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1331_VALIDATION.csv"


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
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not is_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not is_false(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1331*") if path.is_file()]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1331_0_1330_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1330_NEXT_TARGET.csv",
            "needle": "NEXT1330_0_1331",
            "role": "selected 1331 target",
        },
        {
            "source_id": "SRC1331_1_1330_DD_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1330_PARENT_DD_MAP_GATE.csv",
            "needle": "DDG1330_0_map_target",
            "role": "latest parent DD map blockers",
        },
        {
            "source_id": "SRC1331_2_1330_electron",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1330_AUDITED_ELECTRON_FRACTION_ROWS.csv",
            "needle": "CFI1330_TA6V_electron",
            "role": "audited electron component row",
        },
        {
            "source_id": "SRC1331_3_1076_parent_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1076_PARENT_MAP_DERIVATION_ATTEMPT.csv",
            "needle": "DER1076_5_verdict",
            "role": "first parent material/source map attempt",
        },
        {
            "source_id": "SRC1331_4_1081_parent_basis",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1081_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv",
            "needle": "PB1081_4_verdict",
            "role": "parent WEP basis attempt",
        },
        {
            "source_id": "SRC1331_5_1082_parent_DD",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv",
            "needle": "PTD1082_4_verdict",
            "role": "parent to DD coefficient map attempt",
        },
        {
            "source_id": "SRC1331_6_1086_first_row",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1086_DD_PARENT_MAP_FIRST_ROW_ATTEMPT.csv",
            "needle": "PDM1086_4_verdict",
            "role": "first parent-to-DD coefficient row attempt",
        },
        {
            "source_id": "SRC1331_7_1217_Cparent",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1217_CPARENT_MAP_ATTEMPT.csv",
            "needle": "CMAP1217_5_verdict",
            "role": "C_parent map attempt",
        },
        {
            "source_id": "SRC1331_8_1231_component_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1231_DELTA_W_COMPONENT_MAP.csv",
            "needle": "DWM1231_1_TiPt_difference",
            "role": "Delta_w component formula",
        },
        {
            "source_id": "SRC1331_9_1231_basis",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1231_DISCONNECTED_COMPONENT_RESIDUAL_BASIS.csv",
            "needle": "DCW1231_2_light_quark_mass",
            "role": "disconnected component residual slots",
        },
        {
            "source_id": "SRC1331_10_984_imported_basis",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_984_IMPORTED_PHENOMENOLOGICAL_BASIS.csv",
            "needle": "IMP984_1_nuclear_surface_light_quark",
            "role": "imported DD phenomenological basis policy",
        },
        {
            "source_id": "SRC1331_11_726_parent_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_726_PARENT_OWNER_MAP.csv",
            "needle": "POM726_9_matter_quotient",
            "role": "parent owner map and matter quotient blocker",
        },
        {
            "source_id": "SRC1331_12_1330_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1330_VALIDATION.csv",
            "needle": "VAL1330_13_overall",
            "role": "1330 pass gate",
        },
    ]
    source_register: list[dict[str, object]] = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    theorem = [
        {
            "theorem_id": "THM1331_0_conditional_parent_basis_map",
            "statement": "If the parent matter action supplies a differentiable ordinary-matter mass functional m_B[Y,X] and a parent-owned vertical generator X such that partial_X ln m_B decomposes in a declared component basis Q_I(B) with one normalization N_X, then C_I=N_X partial_X ln p_I defines a parent source-basis map into that component basis.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "The vertical derivative of ln m_B is a linear functional on material response space. Choosing a parent-owned finite basis Q_I(B) gives coordinate coefficients C_I. If the same N_X and source/readout convention are used for source and test bodies, the finite Delta_w product is well-defined.",
            "claim_result": "CONDITIONAL_ONLY_NOT_CURRENTLY_PROMOTED",
            "missing_for_unconditional": "parent mass functional; parent component basis; same-branch normalization; no-double-counting; source/readout projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1331_1_no_import_theorem",
            "statement": "An external DD/material charge basis cannot become an MTS parent basis merely because it spans useful phenomenological WEP contrasts.",
            "proof_status": "EXACT_GUARD_THEOREM",
            "proof_sketch": "A basis of observed material contrasts fixes coordinates after a response functional exists; it does not define the parent vertical derivative, coefficient units, source profile, or readout kernel.",
            "claim_result": "DD_REMAINS_EXTERNAL_COMPARATOR",
            "missing_for_unconditional": "explicit parent functor from MTS source weights to DD charge vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1331_2_universal_metric_escape",
            "statement": "If the quotient matter action is universally metric/coframe-coupled and contains no independent component source labels, then all ordinary component weights collapse to a common mode removable by G_N calibration.",
            "proof_status": "CONDITIONAL_LOCAL_GR_ROUTE",
            "proof_sketch": "Universal coupling makes the variation proportional to the total stress-energy, not separate electron/quark/QCD/EM labels. The common source scale is absorbed into measured G_N; relative Delta_w components vanish.",
            "claim_result": "ATTRACTIVE_BUT_UNSIGNED",
            "missing_for_unconditional": "quotient matter action signature; no hidden marker coupling; readout/source-worldtube descent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    clause_audit = [
        {
            "clause_id": "CLAUSE1331_0_parent_mass_functional",
            "needed_clause": "m_B[Y,X] or S_matter[q(Y),psi] whose vertical derivative defines material response",
            "source_evidence": "DER1076_0;PDM1086_0;CMAP1217_0",
            "current_status": "CONTRACT_ONLY_NOT_DERIVED",
            "blocks": "cannot define partial_X ln m_B as MTS object",
            "promotion_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLAUSE1331_1_parent_vertical_generator",
            "needed_clause": "same parent vertical generator X on matter constants, source profile, and readout branch",
            "source_evidence": "POM726_1;POM726_6;CMAP1217_3",
            "current_status": "NOT_CONSTRUCTED",
            "blocks": "DD coefficients could mix different branches or normalizations",
            "promotion_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLAUSE1331_2_EM_alpha_owner",
            "needed_clause": "signed EM/fine-structure operator owner giving c_alpha=N_X partial_X ln alpha_EM",
            "source_evidence": "PTD1082_1;PDM1086_1;CMAP1217_1",
            "current_status": "NOT_SIGNED",
            "blocks": "EM/Coulomb DD row cannot be called parent MTS",
            "promotion_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLAUSE1331_3_nuclear_binding_owner",
            "needed_clause": "signed nuclear/surface/binding response operator and coefficient normalization",
            "source_evidence": "PTD1082_2;PDM1086_2;CMAP1217_2",
            "current_status": "NOT_SIGNED",
            "blocks": "light-quark/surface/binding rows remain phenomenological",
            "promotion_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLAUSE1331_4_QCD_residual_rule",
            "needed_clause": "no-double-counting rule for QCD/gluon residual after electron/quark/EM/nuclear terms",
            "source_evidence": "DDG1330_2_QCD_residual;DCW1231_3_QCD_gluon_binding",
            "current_status": "MISSING_NO_DOUBLE_COUNT_RULE",
            "blocks": "QCD residual would absorb convention choices",
            "promotion_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLAUSE1331_5_source_readout_projection",
            "needed_clause": "same-basis Earth/source vector and MICROSCOPE readout kernel",
            "source_evidence": "PDD1081_2;PDD1081_3;CMAP1217_3;POM726_8",
            "current_status": "MISSING_SOURCE_READOUT_BRANCH",
            "blocks": "finite product cannot be compared to tau_WEP",
            "promotion_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLAUSE1331_6_matter_quotient_universality",
            "needed_clause": "S_matter descends through a quotient metric/coframe with no species marker coupling",
            "source_evidence": "POM726_9_matter_quotient;THM1331_2_universal_metric_escape",
            "current_status": "NOT_SIGNED",
            "blocks": "universal common-mode closure cannot be promoted",
            "promotion_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    component_demotion = [
        {
            "component_id": "electron",
            "current_numeric_status": "AUDIT_EXTRACTED_NONCLAIM",
            "parent_status": "NORMALIZATION_NOT_PARENT_SIGNED",
            "demotion": "component row can remain as source plumbing, not WEP evidence",
            "what_would_promote": "CLAUSE1331_0 plus CLAUSE1331_1 plus electron normalization convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "light_quark",
            "current_numeric_status": "EXTERNAL_DD_ONLY",
            "parent_status": "NUCLEAR_BINDING_OWNER_NOT_SIGNED",
            "demotion": "DD light-quark/surface direction is comparator only",
            "what_would_promote": "parent derivative of quark-mass/nuclear-binding term in m_B[Y,X]",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "QCD_gluon",
            "current_numeric_status": "RESIDUAL_ONLY",
            "parent_status": "NO_DOUBLE_COUNT_RULE_MISSING",
            "demotion": "cannot be a residual sink for all missing mass-budget choices",
            "what_would_promote": "parent-owned residual convention after all other components are declared",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "EM_Coulomb",
            "current_numeric_status": "EXTERNAL_DD_ALPHA_COMPARATOR",
            "parent_status": "EM_ALPHA_OWNER_NOT_SIGNED",
            "demotion": "alpha/Coulomb row is useful pressure but not parent MTS",
            "what_would_promote": "signed parent EM/fine-structure operator pullback to DD Q_alpha_Coulomb",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "nuclear_surface",
            "current_numeric_status": "EXTERNAL_DD_SURFACE_COMPARATOR",
            "parent_status": "NUCLEAR_SURFACE_OWNER_NOT_SIGNED",
            "demotion": "surface/binding row remains phenomenological",
            "what_would_promote": "signed nuclear/surface/binding response operator and isotope/alloy averaging convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "measure_readout",
            "current_numeric_status": "DATA_SOURCE_PENDING",
            "parent_status": "SOURCE_READOUT_PROJECTION_NOT_SIGNED",
            "demotion": "readout residual remains a gate, not a fitted escape hatch",
            "what_would_promote": "source-worldtube and MICROSCOPE readout projection in same branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    promotion_ladder = [
        {
            "rank": 1,
            "route": "universal_metric_escape",
            "target": "prove all ordinary component weights are common-mode",
            "why_first": "most derivable route to GR-like local behavior if quotient matter action closes",
            "required_input": "matter quotient universality and no marker coupling",
            "expected_effect": "Delta_w components vanish after G_N calibration",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rank": 2,
            "route": "electron_normalization",
            "target": "prove or demote electron rest-mass source normalization",
            "why_first": "electron row is now audited numeric, so the theory question is isolated",
            "required_input": "parent mass functional and same X normalization",
            "expected_effect": "electron component becomes parent-owned or stays plumbing-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rank": 3,
            "route": "EM_alpha_owner",
            "target": "derive c_alpha=N_X partial_X ln alpha_EM",
            "why_first": "EM/Coulomb DD row is an important cross-sector bridge",
            "required_input": "parent EM/fine-structure action dependence and field normalization",
            "expected_effect": "promote or permanently demote EM_Coulomb row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rank": 4,
            "route": "nuclear_QCD_owner",
            "target": "derive nuclear binding/QCD residual owner",
            "why_first": "hardest and highest scrutiny; should not be first unless simpler clauses fail",
            "required_input": "binding operator, no-double-counting rule, isotope/alloy averaging",
            "expected_effect": "decide light_quark/QCD/nuclear_surface rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1331_0_parent_map_theorem",
            "target": "parent source-basis map to DD/component charges",
            "input_status": "CONDITIONAL_THEOREM_ONLY",
            "runner_status": "REFUSED_NO_PROMOTED_COMPONENT",
            "reason": "the theorem is exact conditional, but no current parent clause signs the basis map",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1331_1_component_demotion",
            "target": "light-quark/DD/QCD/EM/nuclear/readout rows",
            "input_status": "DEMOTED_TO_EXTERNAL_OR_BLOCKED_STATUS",
            "runner_status": "REFUSED_NOT_SCOREABLE",
            "reason": "external DD rows remain comparator-only and cannot enter full Delta_w claim",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1331_2_universal_metric_escape",
            "target": "derive local GR-like common-mode source coupling",
            "input_status": "BEST_NEXT_THEOREM_ROUTE_UNSIGNED",
            "runner_status": "STAGED_NOT_CLAIMED",
            "reason": "if quotient matter universality closes, the finite component branch collapses into common-mode calibration",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1331_0_no_DD_import",
            "shortcut": "use DD charges as parent MTS basis without a functor",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1331_1_no_component_fit",
            "shortcut": "fit component residuals to make Ti/Pt pass",
            "enforcement": "REFUSED; no one-pair cancellation",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1331_2_no_theorem_premise_claim",
            "shortcut": "claim the conditional theorem as if premises are signed",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1331_3_no_local_GR_claim",
            "shortcut": "treat parent-map theorem gate as local-GR derivation",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1331_0_derivation_result",
            "decision": "parent source-basis map is not derivable from the current corpus",
            "because": "the exact conditional theorem needs parent mass functional, vertical generator, basis ownership, and source/readout projection that remain unsigned",
            "effect": "DD/light-quark/QCD/EM/nuclear components stay external or blocked; electron remains audited plumbing only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1331_1_best_next_route",
            "decision": "attack universal metric escape/electron normalization before nuclear/QCD residuals",
            "because": "this route is closest to deriving GR-like local behavior rather than building a phenomenological component fit",
            "effect": "next checkpoint should try to prove common-mode ordinary matter coupling or explicitly keep finite component residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1331_0_1332",
            "target_file": "1332-Y5-R10-RAB-universal-metric-source-coupling-or-electron-normalization-closure.md",
            "target_script": "scripts/Y5_R10_RAB_universal_metric_source_coupling_or_electron_normalization_closure.py",
            "task": "try to prove the quotient matter action forces ordinary electron/component source weights into a common metric mode; if not, write the finite electron residual branch explicitly",
            "success_condition": "either common-mode source coupling closes conditionally with exact premises, or electron residual remains as a bounded nonclaim finite component with its parent-normalization blocker",
            "do_not": "do not use DD import, do not tune Ti/Pt, do not score WEP, and do not claim local GR unless the quotient matter premises are actually signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        theorem,
        clause_audit,
        component_demotion,
        promotion_ladder,
        runner,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    theorem_conditional = any(row["theorem_id"] == "THM1331_0_conditional_parent_basis_map" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem)
    no_promoted_clauses = all(row["promotion_allowed"] is False for row in clause_audit)
    all_components_demoted = len(component_demotion) == 6 and all(is_false(row["valid_for_claim"]) for row in component_demotion)
    no_score = all(row["score_ready"] is False for row in runner)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1332 = next_target[0]["target_file"].startswith("1332-")

    validations = [
        validation_row(
            "VAL1331_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1331_1_conditional_theorem",
            "parent source-basis map theorem is recorded as exact conditional only",
            theorem_conditional,
            "THM1331_0_conditional_parent_basis_map=EXACT_CONDITIONAL_THEOREM",
        ),
        validation_row(
            "VAL1331_2_no_promoted_clauses",
            "no parent-map clause is promoted without signed parent evidence",
            no_promoted_clauses,
            ";".join(f"{row['clause_id']}={row['current_status']}" for row in clause_audit),
        ),
        validation_row(
            "VAL1331_3_components_demoted",
            "all non-common components remain nonclaim/demoted or blocked",
            all_components_demoted,
            ";".join(f"{row['component_id']}={row['parent_status']}" for row in component_demotion),
        ),
        validation_row(
            "VAL1331_4_runners_not_scoreable",
            "runners refuse WEP/full Delta_w scoring",
            no_score,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner),
        ),
        validation_row(
            "VAL1331_5_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1331_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1331_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1331_8_next_target_1332",
            "next target routes to universal metric source coupling/electron normalization closure",
            next_is_1332,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1331_9_overall",
            "overall 1331 validation",
            all(row["status"] == "PASS" for row in validations),
            "1331 proves only a conditional parent-map theorem and demotes DD/component imports until parent premises close",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(THEOREM_PATH, theorem)
    write_csv(CLAUSE_AUDIT_PATH, clause_audit)
    write_csv(COMPONENT_DEMOTION_PATH, component_demotion)
    write_csv(PROMOTION_LADDER_PATH, promotion_ladder)
    write_csv(RUNNER_PATH, runner)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1331 derives the parent source-basis map only as an exact conditional theorem. The current corpus still does not sign the parent mass functional, vertical generator, component basis, no-double-counting rule, or source/readout projection needed to promote DD/light-quark/QCD/EM/nuclear rows as MTS source weights.

**Main progress:** the failure is now useful: DD is not just vaguely "not derived"; it is blocked by a named parent-map contract. This keeps the field-theory route honest and prevents a phenomenological DD import from replacing the missing parent action.

**Decision:** the best next route is not a component fit. It is the universal metric/common-mode escape: prove ordinary matter only couples through the quotient metric/coframe, or keep the finite electron residual branch explicitly nonclaim.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Parent Source-Basis Map Theorem
{markdown_table(theorem, ["theorem_id", "statement", "proof_status", "proof_sketch", "claim_result", "missing_for_unconditional", "valid_for_claim", "claim_allowed"])}

## Parent Map Clause Audit
{markdown_table(clause_audit, ["clause_id", "needed_clause", "source_evidence", "current_status", "blocks", "promotion_allowed", "valid_for_claim", "claim_allowed"])}

## Component DD Demotion Ledger
{markdown_table(component_demotion, ["component_id", "current_numeric_status", "parent_status", "demotion", "what_would_promote", "valid_for_claim", "claim_allowed"])}

## Component Promotion Ladder
{markdown_table(promotion_ladder, ["rank", "route", "target", "why_first", "required_input", "expected_effect", "valid_for_claim", "claim_allowed"])}

## Delta-w Runner Update
{markdown_table(runner, ["runner_id", "target", "input_status", "runner_status", "reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
