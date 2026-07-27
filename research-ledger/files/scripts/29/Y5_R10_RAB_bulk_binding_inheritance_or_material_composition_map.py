from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1394-Y5-R10-RAB-bulk-binding-inheritance-or-material-composition-map.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1394_SOURCE_REGISTER.csv"
INHERITANCE_PROOF_PATH = SRC_DIR / "P8_Y5_R10_1394_BINDING_INHERITANCE_PROOF_ATTEMPT.csv"
COMPOSITION_MAP_PATH = SRC_DIR / "P8_Y5_R10_1394_BULK_MATERIAL_COMPOSITION_MAP.csv"
BINDING_BETA_PATH = SRC_DIR / "P8_Y5_R10_1394_BINDING_BETA_COEFFICIENT_ROWS.csv"
INTERFACE_PATH = SRC_DIR / "P8_Y5_R10_1394_BINDING_TO_BETA_INTERFACE_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1394_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1394_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1394_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1394_VALIDATION.csv"

STATUS = (
    "bulk_binding_inheritance_conditional_theorem_written_"
    "material_composition_map_nonclaim_beta_bind_blocked"
)
CLAIM_CEILING = (
    "binding_inheritance_attempt_and_material_composition_map_only_no_binding_zero_no_beta_values_"
    "no_R10_no_WEP_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1394_0_1393_doc",
        "source_path": "1393-Y5-R10-RAB-beta-bulk-source-test-convention-or-theorem-zero.md",
        "required_anchor": "NEXT1393_0_1394",
        "purpose": "handoff to binding inheritance or material composition map",
    },
    {
        "source_id": "SRC1394_1_1393_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1393_NEXT_TARGET.csv",
        "required_anchor": "NEXT1393_0_1394",
        "purpose": "machine-readable 1394 target",
    },
    {
        "source_id": "SRC1394_2_1393_proof",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1393_BETA_BULK_CONVENTION_PROOF_ATTEMPT.csv",
        "required_anchor": "BBC1393_3_zero_route",
        "purpose": "beta zero requires binding inheritance",
    },
    {
        "source_id": "SRC1394_3_1393_beta_rows",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1393_BETA_BULK_SOURCE_TEST_COEFFICIENT_ROWS.csv",
        "required_anchor": "BBS1393_3_beta_bind_source",
        "purpose": "binding beta source/test rows to refine",
    },
    {
        "source_id": "SRC1394_4_1393_interface",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1393_BETA_RUNNER_INTERFACE_GATE.csv",
        "required_anchor": "BRI1393_4_verdict",
        "purpose": "beta-to-runner gate remains blocked",
    },
    {
        "source_id": "SRC1394_5_1389_material_map",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_MATERIAL_SOURCE_CLASS_MAP.csv",
        "required_anchor": "MSC1389_2_nuclear_binding",
        "purpose": "electronic/nuclear/EM binding material classes",
    },
    {
        "source_id": "SRC1394_6_1389_convention",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1389_COUPLING_EXPANSION_CONVENTION.csv",
        "required_anchor": "CEC1389_4_observed_mass_charge",
        "purpose": "observed mass/binding charge decomposition convention",
    },
    {
        "source_id": "SRC1394_7_1392_template",
        "source_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM.csv",
        "required_anchor": "beta_bulk_S",
        "purpose": "alpha template still depends on beta source/test legs",
    },
    {
        "source_id": "SRC1394_8_1392_runner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1392_R10_RUNNER_SMOKE_SUMMARY.csv",
        "required_anchor": "RUN1392_0_anchor_smoke",
        "purpose": "runner must remain blocked",
    },
    {
        "source_id": "SRC1394_9_this_script",
        "source_path": "scripts/Y5_R10_RAB_bulk_binding_inheritance_or_material_composition_map.py",
        "required_anchor": "STATUS",
        "purpose": "1394 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        rows.append(
            {
                **source,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, source["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def inheritance_rows() -> list[dict[str, str]]:
    return [
        {
            "inheritance_id": "BIH1394_0_target",
            "target": "beta_bind,S and beta_bind,T vanish or inherit common owner",
            "attempted_derivation": "treat electronic, nuclear, and EM binding energy as internal parts of the same ordinary-matter action owner",
            "result": "TARGET_DEFINED",
            "gap": "none for target definition",
            "composition_consequence": "binding terms must be either theorem-zero or explicit composition rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "inheritance_id": "BIH1394_1_common_owner_inheritance",
            "target": "all binding sectors inherit one matter owner",
            "attempted_derivation": "if electronic, nuclear, and EM binding sub-actions are not independent parent arguments, their beta rows inherit the common matter beta",
            "result": "CONDITIONAL_INHERITANCE_ROUTE",
            "gap": "parent object-language/action-measure owner is still unsigned for binding sub-sectors",
            "composition_consequence": "cannot set beta_e, beta_nuc, beta_EM to zero yet",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "inheritance_id": "BIH1394_2_observed_mass_decomposition",
            "target": "bulk observed mass decomposes into rest, electronic, nuclear, and EM binding pieces",
            "attempted_derivation": "M_bulk^obs = M_rest + E_e/c^2 + E_nuc/c^2 + E_EM/c^2 + ...",
            "result": "FORMAL_DECOMPOSITION_READY",
            "gap": "source/test fractions f_e, f_nuc, f_EM are not supplied",
            "composition_consequence": "material composition map must carry f_i,S and f_i,T rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "inheritance_id": "BIH1394_3_binding_charge_formula",
            "target": "binding beta enters as composition-weighted inherited sector charges",
            "attempted_derivation": "beta_bind,A = f_e,A beta_e + f_nuc,A beta_nuc + f_EM,A beta_EM + f_other,A beta_other",
            "result": "EXACT_FORMULA_SCHEMA",
            "gap": "sector beta_i and composition fractions are missing",
            "composition_consequence": "write beta_bind source/test rows as formula-only nonclaim inputs",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "inheritance_id": "BIH1394_4_zero_condition",
            "target": "beta_bind,S=beta_bind,T=0",
            "attempted_derivation": "if all inherited sector beta_i=0, or all composition-weighted sums cancel by theorem rather than fit, binding beta vanishes",
            "result": "EXACT_CONDITIONAL_BINDING_ZERO",
            "gap": "sector beta zero and composition cancellation are not parent-signed",
            "composition_consequence": "zero certificate shape exists but cannot be used as evidence",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "inheritance_id": "BIH1394_5_current_verdict",
            "target": "binding inheritance claim status",
            "attempted_derivation": "compare 1393 beta rows, 1389 material map, and coupling convention",
            "result": "BINDING_INHERITANCE_NOT_SIGNED_COMPOSITION_MAP_REQUIRED",
            "gap": "binding sector ownership, composition fractions, and inherited beta_i rows are missing",
            "composition_consequence": "create nonclaim material composition and binding beta rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def composition_rows() -> list[dict[str, str]]:
    return [
        {
            "composition_id": "MCM1394_0_source_electronic",
            "body_leg": "source",
            "sector": "electronic_atomic",
            "fraction_symbol": "f_e,S",
            "sector_beta_symbol": "beta_e",
            "formula_contribution": "f_e,S*beta_e",
            "required_provenance": "source material composition and electronic/atomic beta row or theorem-zero",
            "current_value": "MISSING",
            "current_status": "MISSING_SOURCE_ELECTRONIC_FRACTION_OR_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "composition_id": "MCM1394_1_source_nuclear",
            "body_leg": "source",
            "sector": "nuclear_binding",
            "fraction_symbol": "f_nuc,S",
            "sector_beta_symbol": "beta_nuc",
            "formula_contribution": "f_nuc,S*beta_nuc",
            "required_provenance": "source nuclear binding fraction and nuclear beta row or theorem-zero",
            "current_value": "MISSING",
            "current_status": "MISSING_SOURCE_NUCLEAR_FRACTION_OR_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "composition_id": "MCM1394_2_source_EM",
            "body_leg": "source",
            "sector": "EM_binding",
            "fraction_symbol": "f_EM,S",
            "sector_beta_symbol": "beta_EM",
            "formula_contribution": "f_EM,S*beta_EM",
            "required_provenance": "source EM binding/charge fraction and EM beta row or theorem-zero",
            "current_value": "MISSING",
            "current_status": "MISSING_SOURCE_EM_FRACTION_OR_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "composition_id": "MCM1394_3_test_electronic",
            "body_leg": "test",
            "sector": "electronic_atomic",
            "fraction_symbol": "f_e,T",
            "sector_beta_symbol": "beta_e",
            "formula_contribution": "f_e,T*beta_e",
            "required_provenance": "test material composition and electronic/atomic beta row or theorem-zero",
            "current_value": "MISSING",
            "current_status": "MISSING_TEST_ELECTRONIC_FRACTION_OR_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "composition_id": "MCM1394_4_test_nuclear",
            "body_leg": "test",
            "sector": "nuclear_binding",
            "fraction_symbol": "f_nuc,T",
            "sector_beta_symbol": "beta_nuc",
            "formula_contribution": "f_nuc,T*beta_nuc",
            "required_provenance": "test nuclear binding fraction and nuclear beta row or theorem-zero",
            "current_value": "MISSING",
            "current_status": "MISSING_TEST_NUCLEAR_FRACTION_OR_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "composition_id": "MCM1394_5_test_EM",
            "body_leg": "test",
            "sector": "EM_binding",
            "fraction_symbol": "f_EM,T",
            "sector_beta_symbol": "beta_EM",
            "formula_contribution": "f_EM,T*beta_EM",
            "required_provenance": "test EM binding/charge fraction and EM beta row or theorem-zero",
            "current_value": "MISSING",
            "current_status": "MISSING_TEST_EM_FRACTION_OR_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "composition_id": "MCM1394_6_composition_verdict",
            "body_leg": "source_and_test",
            "sector": "composition_map",
            "fraction_symbol": "f_i,S;f_i,T",
            "sector_beta_symbol": "beta_i",
            "formula_contribution": "beta_bind,A=sum_i f_i,A beta_i",
            "required_provenance": "every listed fraction and sector beta must be source-backed or theorem-zero",
            "current_value": "MISSING",
            "current_status": "MATERIAL_COMPOSITION_MAP_READY_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def binding_beta_rows() -> list[dict[str, str]]:
    return [
        {
            "binding_id": "BBR1394_0_beta_e",
            "coefficient": "beta_e",
            "role": "electronic/atomic inherited sector beta",
            "definition": "canonical phi_c derivative of electronic/atomic contribution to observed bulk mass",
            "formula": "appears in beta_bind,A as f_e,A beta_e",
            "required_for_claim": "electronic sector owner theorem or sourced bound",
            "current_value": "MISSING",
            "current_status": "MISSING_ELECTRONIC_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "binding_id": "BBR1394_1_beta_nuc",
            "coefficient": "beta_nuc",
            "role": "nuclear binding inherited sector beta",
            "definition": "canonical phi_c derivative of nuclear binding/composite rest-mass contribution",
            "formula": "appears in beta_bind,A as f_nuc,A beta_nuc",
            "required_for_claim": "nuclear binding owner theorem or sourced bound",
            "current_value": "MISSING",
            "current_status": "MISSING_NUCLEAR_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "binding_id": "BBR1394_2_beta_EM",
            "coefficient": "beta_EM",
            "role": "electromagnetic binding/charge inherited sector beta",
            "definition": "canonical phi_c derivative of EM binding/charge contribution",
            "formula": "appears in beta_bind,A as f_EM,A beta_EM",
            "required_for_claim": "EM action descent/theorem-zero or sourced clock/WEP/alpha_EM bound",
            "current_value": "MISSING",
            "current_status": "MISSING_EM_BETA",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "binding_id": "BBR1394_3_beta_bind_source",
            "coefficient": "beta_bind,S",
            "role": "source binding contribution to beta_bulk,S",
            "definition": "sum_i f_i,S beta_i",
            "formula": "f_e,S beta_e + f_nuc,S beta_nuc + f_EM,S beta_EM + ...",
            "required_for_claim": "all source fractions and inherited beta_i values/zeros",
            "current_value": "MISSING",
            "current_status": "MISSING_SOURCE_BINDING_SUM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "binding_id": "BBR1394_4_beta_bind_test",
            "coefficient": "beta_bind,T",
            "role": "test binding contribution to beta_bulk,T",
            "definition": "sum_i f_i,T beta_i",
            "formula": "f_e,T beta_e + f_nuc,T beta_nuc + f_EM,T beta_EM + ...",
            "required_for_claim": "all test fractions and inherited beta_i values/zeros",
            "current_value": "MISSING",
            "current_status": "MISSING_TEST_BINDING_SUM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "binding_id": "BBR1394_5_binding_verdict",
            "coefficient": "binding beta pack",
            "role": "feeds beta_bulk,S and beta_bulk,T",
            "definition": "binding beta terms are explicit nonclaim rows until inherited sector betas and composition fractions are real",
            "formula": "beta_bulk,A = beta_* + beta_w,bulk,A + beta_bind,A",
            "required_for_claim": "BBR1394_0 through BBR1394_4 and MCM1394 rows complete without MISSING markers",
            "current_value": "MISSING",
            "current_status": "BINDING_BETA_ROWS_READY_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def interface_rows() -> list[dict[str, str]]:
    return [
        {
            "interface_id": "BTB1394_0_beta_bulk_source",
            "target_row": "BBS1393_5_beta_bulk_source",
            "dependency": "beta_bind,S from BBR1394_3",
            "gate": "cannot fill beta_bulk,S until source binding sum is real or zero-certified",
            "current_status": "BLOCKED_BINDING_SOURCE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BTB1394_1_beta_bulk_test",
            "target_row": "BBS1393_6_beta_bulk_test",
            "dependency": "beta_bind,T from BBR1394_4",
            "gate": "cannot fill beta_bulk,T until test binding sum is real or zero-certified",
            "current_status": "BLOCKED_BINDING_TEST_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BTB1394_2_WEP_warning",
            "target_row": "WEP/source-charge gate",
            "dependency": "composition differences f_i,S vs f_i,T and sector beta_i",
            "gate": "composition-dependent binding betas open WEP/clock gates, not only R10",
            "current_status": "WEP_CLOCK_GATES_RETAINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BTB1394_3_runner_warning",
            "target_row": "1392 bulk alpha template",
            "dependency": "beta_bulk,S and beta_bulk,T",
            "gate": "runner template remains symbolic until binding and nonbinding beta pieces are real",
            "current_status": "RUNNER_PROMOTION_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BTB1394_4_verdict",
            "target_row": "beta_bind to beta_bulk interface",
            "dependency": "all composition and binding beta rows",
            "gate": "binding rows must close before beta_bulk rows can promote R10/local scoring",
            "current_status": "BINDING_TO_BETA_INTERFACE_READY_SCORING_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1394_0_sources",
            "gate": "all cited local sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1394_1_binding_inheritance",
            "gate": "binding sectors inherit common owner or vanish",
            "status": "BLOCKED_PARENT_UNSIGNED",
            "reason": "binding sector ownership and inherited beta zero are not parent-signed",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1394_2_composition_map",
            "gate": "material composition rows exist",
            "status": "PASS_NONCLAIM_MAP",
            "reason": "source/test electronic, nuclear, and EM composition factors are explicit but missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1394_3_binding_beta",
            "gate": "binding beta rows can fill beta_bulk,S/T",
            "status": "BLOCKED_VALUES_MISSING",
            "reason": "sector betas and composition fractions are missing or not theorem-zero",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1394_4_R10_WEP_score",
            "gate": "R10/WEP/clock scores may be reported",
            "status": "BLOCKED_NO_BINDING_INPUTS",
            "reason": "composition-dependent binding terms remain unresolved",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1394_5_local_claim",
            "gate": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1394 is a binding/composition checkpoint, not a derived local GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1394_0_inheritance_status",
            "decision": "binding inheritance remains conditional",
            "because": "electronic, nuclear, and EM binding sector ownership is not parent-signed",
            "next_action": "keep binding beta rows explicit and nonclaim",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1394_1_composition_status",
            "decision": "material composition must be source/test specific",
            "because": "R10 and WEP depend on source/test material legs, not one generic bulk value",
            "next_action": "derive sector beta zero or build sector-specific source rows",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1394_2_next",
            "decision": "go after sector beta ownership next",
            "because": "composition fractions alone are useless unless beta_e, beta_nuc, and beta_EM are zero or bounded",
            "next_action": "try electronic/nuclear/EM sector beta zero theorem or nonclaim sector-beta source pack",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1394_0_1395",
            "next_doc": "1395-Y5-R10-RAB-sector-beta-zero-theorem-or-binding-sector-source-pack.md",
            "next_script": "scripts/Y5_R10_RAB_sector_beta_zero_theorem_or_binding_sector_source_pack.py",
            "task": "derive theorem-zero for beta_e, beta_nuc, and beta_EM from sector ownership/descent, or create nonclaim sector-beta source rows",
            "success_condition": "electronic, nuclear, and EM binding beta rows are either theorem-zero under signed premises or explicit nonclaim rows with provenance and local/WEP/R10 gates",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;WEP pass;q_loc=0;numeric alpha(lambda);GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows(
    sources: list[dict[str, str]],
    inheritance: list[dict[str, str]],
    composition: list[dict[str, str]],
    binding: list[dict[str, str]],
    interface: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_pass = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    conditional_zero = any(
        row["inheritance_id"] == "BIH1394_4_zero_condition"
        and row["result"] == "EXACT_CONDITIONAL_BINDING_ZERO"
        and row["valid_for_claim"] == "False"
        for row in inheritance
    )
    inheritance_blocked = any(
        row["inheritance_id"] == "BIH1394_5_current_verdict"
        and row["result"] == "BINDING_INHERITANCE_NOT_SIGNED_COMPOSITION_MAP_REQUIRED"
        and row["claim_allowed"] == "False"
        for row in inheritance
    )
    composition_ready = any(
        row["composition_id"] == "MCM1394_6_composition_verdict"
        and row["current_status"] == "MATERIAL_COMPOSITION_MAP_READY_NONCLAIM"
        and row["claim_allowed"] == "False"
        for row in composition
    )
    binding_ready = any(
        row["binding_id"] == "BBR1394_5_binding_verdict"
        and row["current_status"] == "BINDING_BETA_ROWS_READY_NONCLAIM"
        and row["claim_allowed"] == "False"
        for row in binding
    )
    no_values = all(row["current_value"] == "MISSING" for row in composition + binding)
    all_nonclaim = all(
        row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in composition + binding
    )
    interface_blocked = any(
        row["interface_id"] == "BTB1394_4_verdict"
        and row["current_status"] == "BINDING_TO_BETA_INTERFACE_READY_SCORING_BLOCKED"
        and row["claim_allowed"] == "False"
        for row in interface
    )
    local_claim_blocked = any(
        row["gate_id"] == "GATE1394_5_local_claim"
        and row["status"] == "BLOCKED_NO_CLAIM"
        and row["claim_allowed"] == "False"
        for row in gates
    )
    prior_1393 = csv_rows(SRC_DIR / "P8_Y5_R10_1393_CLAIM_GATE.csv")
    prior_local_blocked = any(
        row["gate_id"] == "GATE1393_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM"
        for row in prior_1393
    )
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        INHERITANCE_PROOF_PATH,
        COMPOSITION_MAP_PATH,
        BINDING_BETA_PATH,
        INTERFACE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_bulk_binding_inheritance_or_material_composition_map.py"),
    ]
    formalization_touched = any("formalization-workbench" in str((ROOT / output).resolve()) for output in outputs)
    scope_ok = all((ROOT / output).resolve().is_relative_to(ROOT.resolve()) for output in outputs) and not formalization_touched
    overall = (
        source_pass
        and conditional_zero
        and inheritance_blocked
        and composition_ready
        and binding_ready
        and no_values
        and all_nonclaim
        and interface_blocked
        and local_claim_blocked
        and prior_local_blocked
        and scope_ok
    )
    return [
        {
            "validation_id": "VAL1394_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if source_pass else "FAIL",
            "details": "; ".join(
                f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources
            ),
        },
        {
            "validation_id": "VAL1394_1_inheritance",
            "check": "binding inheritance zero is exact conditional but unsigned",
            "status": "PASS" if conditional_zero and inheritance_blocked else "FAIL",
            "details": "BIH1394_4 records conditional binding zero; BIH1394_5 keeps inheritance unsigned.",
        },
        {
            "validation_id": "VAL1394_2_composition_map",
            "check": "source/test material composition map is explicit and nonclaim",
            "status": "PASS" if composition_ready and no_values and all_nonclaim else "FAIL",
            "details": f"composition_rows={len(composition)}; binding_rows={len(binding)}; all_values_missing={no_values}",
        },
        {
            "validation_id": "VAL1394_3_interface",
            "check": "binding rows cannot promote beta_bulk yet",
            "status": "PASS" if binding_ready and interface_blocked else "FAIL",
            "details": "BTB1394_4 blocks beta_bulk/R10 promotion until binding rows are real or zero-certified.",
        },
        {
            "validation_id": "VAL1394_4_claim_refusal",
            "check": "R10/WEP/local claims remain blocked",
            "status": "PASS" if local_claim_blocked and prior_local_blocked else "FAIL",
            "details": "GATE1394_5 and prior GATE1393_5 both block local GR/Newton promotion.",
        },
        {
            "validation_id": "VAL1394_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if scope_ok else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched={formalization_touched}",
        },
        {
            "validation_id": "VAL1394_6_overall",
            "check": "overall 1394 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1394 writes binding inheritance conditions and nonclaim material composition rows without enabling beta/R10/local scoring.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    inheritance: list[dict[str, str]],
    composition: list[dict[str, str]],
    binding: list[dict[str, str]],
    interface: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1394 - Y5 R10 RAB Bulk Binding Inheritance Or Material Composition Map

**Generated:** {generated}

**Current verdict:** binding inheritance has a clean conditional theorem, but it is not signed. `beta_bind,A=0` follows only if electronic, nuclear, and EM binding sectors inherit the common matter owner or have theorem-zero beta rows.

**Discipline move:** split `beta_bind,S/T` into explicit source/test composition sums: electronic, nuclear, and EM fractions times inherited sector betas. Composition dependence now visibly feeds R10, WEP, clocks, and local-GR gates; no binding row is allowed to score yet.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Binding Inheritance Proof Attempt

{md_table(inheritance)}

## Bulk Material Composition Map

{md_table(composition)}

## Binding Beta Coefficient Rows

{md_table(binding)}

## Binding-to-Beta Interface Gate

{md_table(interface)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    inheritance = inheritance_rows()
    composition = composition_rows()
    binding = binding_beta_rows()
    interface = interface_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, inheritance, composition, binding, interface, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(INHERITANCE_PROOF_PATH, inheritance)
    write_csv(COMPOSITION_MAP_PATH, composition)
    write_csv(BINDING_BETA_PATH, binding)
    write_csv(INTERFACE_PATH, interface)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, inheritance, composition, binding, interface, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1394 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
