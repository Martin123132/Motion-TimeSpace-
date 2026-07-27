from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFF = BRANCH_ROOT / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1447-Y5-R10-RAB-C-parent-functional-derivative-source-or-AX1090-parent-object-proof.md"

PREV_NEXT = OUT / "P8_Y5_R10_1446_NEXT_TARGET.csv"
PREV_CANDIDATES = OUT / "P8_Y5_R10_1446_PARENT_ACTION_COUPLING_CANDIDATE_LEDGER.csv"
PREV_CLAUSE_AUDIT = OUT / "P8_Y5_R10_1446_CONTRACT_CLAUSE_REDUCTION_AUDIT.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1446_VALIDATION.csv"
CONTRACT = COEFF / "C_parent_WEP_coupling_theorem_contract.csv"
IMPORT_SCHEMA = COEFF / "C_parent_import_schema.csv"
AX1090_STATUS = COEFF / "AX1090_reduction_status.csv"
MOMS_CLAUSE = OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv"
MOMS_THEOREM = OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv"
AX1090_AXIOMS = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
CPARENT_MAP = OUT / "P8_Y5_R10_1217_CPARENT_MAP_ATTEMPT.csv"

LIVE_C_PARENT_IMPORT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1447_SOURCE_REGISTER.csv"
FD_ATTEMPT = OUT / "P8_Y5_R10_1447_FUNCTIONAL_DERIVATIVE_DEFINITION_ATTEMPT.csv"
VWEP_REQUIREMENTS = OUT / "P8_Y5_R10_1447_VWEP_DOMAIN_REQUIREMENTS.csv"
AX_PROOF = OUT / "P8_Y5_R10_1447_AX1090_PARENT_OBJECT_PROOF_ATTEMPT.csv"
OBSTRUCTION_MATRIX = OUT / "P8_Y5_R10_1447_OBSTRUCTION_MATRIX.csv"
IMPORT_REFUSAL = OUT / "P8_Y5_R10_1447_IMPORT_TEMPLATE_REFUSAL.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1447_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1447_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1447_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1447_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1447_VALIDATION.csv"

BRANCH_FD_ATTEMPT = COEFF / "C_parent_WEP_functional_derivative_definition_attempt.csv"
BRANCH_VWEP_REQUIREMENTS = COEFF / "V_WEP_domain_requirements.csv"
BRANCH_AX_PROOF = COEFF / "AX1090_parent_object_proof_attempt.csv"
BRANCH_IMPORT_REFUSAL = COEFF / "C_parent_WEP_slot_import_REFUSED_1447.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_table(handle: Any, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"\n## {title}\n")
    if not rows:
        handle.write("\nNo rows.\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        handle.write("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |\n")


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    entries = [
        ("SRC1447_0_prev_next", PREV_NEXT, "1447 handoff"),
        ("SRC1447_1_prev_candidates", PREV_CANDIDATES, "1446 candidate routes"),
        ("SRC1447_2_prev_clause_audit", PREV_CLAUSE_AUDIT, "1446 contract clause audit"),
        ("SRC1447_3_prev_validation", PREV_VALIDATION, "1446 validation"),
        ("SRC1447_4_contract", CONTRACT, "C_parent coupling theorem contract"),
        ("SRC1447_5_import_schema", IMPORT_SCHEMA, "C_parent import schema"),
        ("SRC1447_6_AX1090_status", AX1090_STATUS, "AX1090 reduction status"),
        ("SRC1447_7_MOMS_clause", MOMS_CLAUSE, "MOMS minimal ordinary-matter signature"),
        ("SRC1447_8_MOMS_theorem", MOMS_THEOREM, "MOMS conditional zero theorem"),
        ("SRC1447_9_AX1090_axioms", AX1090_AXIOMS, "missing AX1090 axiom ledger"),
        ("SRC1447_10_Cparent_map", CPARENT_MAP, "Cparent coefficient map attempt"),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": path.exists(),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, role in entries
    ]


def fd_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "definition_id": "FD1447_0_candidate_definition",
            "candidate_definition": "C_parent_WEP[V_WEP] := N_WEP^{-1} (d/dε S_parent[Phi + ε V_WEP, Psi_ε, theta_ε])|_{ε=0}",
            "intended_meaning": "parent-owned WEP/source coefficient obtained before material/readout projection",
            "required_inputs": "S_parent; V_WEP; Psi_ε lift; theta_ε constant/representation rule; N_WEP units/sign/basis; source/readout projection",
            "current_status": "FORMAL_DEFINITION_WRITTEN_NOT_SOURCE_SIGNED",
            "blocking_evidence": "AX1090_0 parent object not reduced; V_WEP domain not signed; normalization/readout absent",
            "importable_as_C_parent": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "definition_id": "FD1447_1_zero_branch",
            "candidate_definition": "If V_WEP is quotient-vertical and MOMS1088_0..6 are parent-derived, then δ_{V_WEP} S_matter = 0 up to gauge/boundary terms",
            "intended_meaning": "DERIVED_ZERO route for ordinary-matter WEP composition response",
            "required_inputs": "MOMS parent action signature; fixed/gauge matter lift; no source weights; no shadow/domain terms; variation-before-readout",
            "current_status": "CONDITIONAL_ZERO_ONLY",
            "blocking_evidence": "THM1088_6 and AX1090 status keep MOMS unsigned",
            "importable_as_C_parent": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "definition_id": "FD1447_2_finite_branch",
            "candidate_definition": "If δ_{V_WEP} S_parent is nonzero, project it into same-branch coefficient vector (c_alpha, c_surface, q_tail, ...) with N_WEP and K_CMSM",
            "intended_meaning": "finite source-backed coefficient route",
            "required_inputs": "parent mass/EM/binding derivatives; same-branch normalization; source profile; readout matrix; material tensor",
            "current_status": "FINITE_ROUTE_SCHEMA_ONLY",
            "blocking_evidence": "CMAP1217_5 C_PARENT map not derived; live K_CMSM readout absent",
            "importable_as_C_parent": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def vwep_requirement_rows() -> list[dict[str, Any]]:
    requirements = [
        ("VREQ1447_0_field_space", "parent configuration space Φ and tangent bundle", "MISSING_SINGLE_PARENT_OBJECT", "AX1090_0 not reduced"),
        ("VREQ1447_1_verticality", "V_WEP ∈ ker(Dq) or declared finite visible residual", "CONDITIONAL_QUOTIENT_ONLY", "MOMS1088 quotient clauses are not parent-derived"),
        ("VREQ1447_2_matter_lift", "Ψ_A(ε) lift under V_WEP fixed as zero/gauge/boundary or finite residual", "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR", "MOMS1088_2 unsigned"),
        ("VREQ1447_3_constant_lift", "θ_A masses/charges/clocks/representation data have Lie_V θ_A=0 or explicit residual", "CONSTANT_SUPERSELECTION_UNSIGNED", "AX1090_3 partial only"),
        ("VREQ1447_4_no_weights", "no pre-action species/source weights w_A(X)", "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED", "AX1090_2 common measure not reduced"),
        ("VREQ1447_5_no_shadow_domain", "no shadow matter frame/domain/source-only metric", "NO_SHADOW_DOMAIN_UNSIGNED", "AX1090_1 not reduced"),
        ("VREQ1447_6_variation_order", "variation before material/readout/source projection", "CONDITIONAL_RULE_NOT_PARENT_SIGNED", "AX1090_4 partial only"),
        ("VREQ1447_7_normalization", "N_WEP units/sign/basis and same-branch readout normalization", "MISSING_NORMALIZATION_AND_READOUT", "Cparent map/readout gates still open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": req_id,
            "required_object": obj,
            "current_status": status,
            "obstruction": obstruction,
            "required_for_import": True,
            "satisfied_now": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for req_id, obj, status, obstruction in requirements
    ]


def ax_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_step_id": "AXP1447_0_candidate_object",
            "claim": "S_parent may be assembled from 1009 sectors into one variational object",
            "test": "one owner must fix fields, first variation, symplectic potential, matter/source/readout coupling, and variation domain before readout",
            "result": "FAILS_CURRENTLY",
            "evidence": "1009 sector contract exists but sector runner refuses total parent current-chain contract",
            "can_sign_AX1090_0": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_step_id": "AXP1447_1_MOMS_object",
            "claim": "MOMS1088 ordinary-matter signature supplies the needed parent object",
            "test": "MOMS1088_0..6 must be parent-derived in one action, not adopted as a clean axiom",
            "result": "FAILS_CURRENTLY",
            "evidence": "MOMS1088_7 not derived; THM1088_6 blocks promotion",
            "can_sign_AX1090_0": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_step_id": "AXP1447_2_axiom_reduction",
            "claim": "AX1090_0 follows from MTS primitives without adding a new axiom",
            "test": "current primitive files must prove one parent action owner before projection/fitting",
            "result": "FAILS_CURRENTLY",
            "evidence": "AXRED1441_0_parent_object remains NOT_REDUCED",
            "can_sign_AX1090_0": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_step_id": "AXP1447_3_verdict",
            "claim": "AX1090_0 parent object is proven enough to define C_parent_WEP",
            "test": "all previous proof steps close and no countermodel remains",
            "result": "PARENT_OBJECT_NOT_PROVEN",
            "evidence": "sector, MOMS, and AX1090 reductions remain conditional/unsigned",
            "can_sign_AX1090_0": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": "OBS1447_0_S_parent",
            "blocks_definition_id": "FD1447_0_candidate_definition",
            "obstruction": "no source-signed total S_parent",
            "current_best_source": str(PREV_CANDIDATES),
            "severity": "HARD_BLOCK",
            "remedy": "derive AX1090_0 or supply one parent action source",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": "OBS1447_1_V_WEP",
            "blocks_definition_id": "FD1447_0_candidate_definition",
            "obstruction": "V_WEP generator lacks signed domain, matter lift, and hidden-visible exclusion",
            "current_best_source": str(VWEP_REQUIREMENTS),
            "severity": "HARD_BLOCK",
            "remedy": "derive V_WEP domain from MOMS/quotient functor or keep finite residuals explicit",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": "OBS1447_2_N_WEP",
            "blocks_definition_id": "FD1447_2_finite_branch",
            "obstruction": "normalization/readout/source basis absent",
            "current_best_source": str(CPARENT_MAP),
            "severity": "HARD_BLOCK",
            "remedy": "fill same-branch K_CMSM, source worldtube, material tensor, units, and signs",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": "OBS1447_3_zero_certificate",
            "blocks_definition_id": "FD1447_1_zero_branch",
            "obstruction": "MOMS zero theorem is conditional only",
            "current_best_source": str(MOMS_THEOREM),
            "severity": "HARD_BLOCK",
            "remedy": "source-sign MOMS1088_0..6 or demote zero to closure-only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def import_refusal_rows() -> list[dict[str, Any]]:
    schema_fields = [row["field"] for row in read_csv(IMPORT_SCHEMA) if row.get("field")]
    missing_fields = "value;uncertainty;units;sign_convention;basis;source_path;parent_status;zero_certificate_status"
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "IR1447_0_no_import_row",
            "would_be_target": str(LIVE_C_PARENT_IMPORT),
            "target_exists": LIVE_C_PARENT_IMPORT.exists(),
            "schema_fields_checked": ";".join(schema_fields),
            "missing_or_invalid_fields": missing_fields,
            "refusal_status": "REFUSED_NO_SOURCE_SIGNED_FUNCTIONAL_DERIVATIVE",
            "safe_branch_file": str(BRANCH_IMPORT_REFUSAL),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def parser_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1447_0_fd_attempt",
            "target_path": str(BRANCH_FD_ATTEMPT),
            "target_exists": BRANCH_FD_ATTEMPT.exists(),
            "parser_status": "PASS_DEFINITION_ATTEMPT_NONCLAIM",
            "refusal_reason": "formal definition is not source-signed and not importable",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1447_1_V_WEP_requirements",
            "target_path": str(BRANCH_VWEP_REQUIREMENTS),
            "target_exists": BRANCH_VWEP_REQUIREMENTS.exists(),
            "parser_status": "PASS_REQUIREMENTS_ONLY_NONCLAIM",
            "refusal_reason": "all V_WEP requirements are unsatisfied",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1447_2_live_import",
            "target_path": str(LIVE_C_PARENT_IMPORT),
            "target_exists": LIVE_C_PARENT_IMPORT.exists(),
            "parser_status": "REFUSED_LIVE_C_PARENT_IMPORT_ABSENT",
            "refusal_reason": "no DERIVED_ZERO or finite coefficient row exists",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1447_0_definition_not_source_signed", "functional derivative definition is formal only"),
        ("CG1447_1_AX1090_0_not_proven", "parent object remains not reduced"),
        ("CG1447_2_V_WEP_not_defined", "WEP generator domain is unsatisfied"),
        ("CG1447_3_zero_not_certified", "MOMS zero theorem remains conditional"),
        ("CG1447_4_finite_not_sourced", "finite coefficient branch lacks normalization/readout/source rows"),
        ("CG1447_5_import_absent", "live C_parent import remains absent"),
        ("CG1447_6_no_score", "no WEP/local-GR/Newton score or claim is allowed from 1447"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_CLAIM_FALSE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1447_0_formal_definition_kept",
            "decision": "keep the functional derivative formula as a nonclaim target definition",
            "why": "it is the right mathematical shape for derivability, but source inputs are missing",
            "consequence": "future proof work can attack named missing objects instead of vague coupling language",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1447_1_no_import",
            "decision": "do not create C_parent_WEP_slot_import.csv",
            "why": "no value, units, sign, basis, source path, parent_status, or zero certificate exists",
            "consequence": "all local/WEP claims remain blocked",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1447_2_next_V_WEP_domain",
            "decision": "try to derive the V_WEP domain from MOMS/quotient clauses next",
            "why": "without a generator domain, the derivative formula cannot even be evaluated",
            "consequence": "1448 should target V_WEP generator/domain proof before any coefficient value",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1447_0_1448",
            "next_target": "1448-Y5-R10-RAB-V-WEP-generator-domain-or-MOMS-signature-source-pack.md",
            "script": "scripts/Y5_R10_RAB_V_WEP_generator_domain_or_MOMS_signature_source_pack.py",
            "objective": "attempt to derive the V_WEP generator domain, matter lift, constant lift, no-weight rule, no-shadow rule, and variation-before-readout rule from MOMS/quotient clauses; otherwise keep C_parent functional derivative non-evaluable.",
            "include": "V_WEP tangent-domain proof; MOMS clause source pack; obstruction audit; no-claim parser dry-run",
            "exclude": "numeric WEP score; local-GR claim; invented coefficient; closure-only zero; bound-inverted coefficient; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_live_scaffolds(fd: list[dict[str, Any]], vreq: list[dict[str, Any]], axp: list[dict[str, Any]], refusal: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_FD_ATTEMPT, fd)
    write_csv(BRANCH_VWEP_REQUIREMENTS, vreq)
    write_csv(BRANCH_AX_PROOF, axp)
    write_csv(BRANCH_IMPORT_REFUSAL, refusal)


def validation_rows(
    sources: list[dict[str, Any]],
    fd: list[dict[str, Any]],
    vreq: list[dict[str, Any]],
    axp: list[dict[str, Any]],
    obs: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = [
        SOURCE_REGISTER,
        FD_ATTEMPT,
        VWEP_REQUIREMENTS,
        AX_PROOF,
        OBSTRUCTION_MATRIX,
        IMPORT_REFUSAL,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_FD_ATTEMPT,
        BRANCH_VWEP_REQUIREMENTS,
        BRANCH_AX_PROOF,
        BRANCH_IMPORT_REFUSAL,
    ]
    all_sources = all(str(row["exists"]) == "True" for row in sources)
    fd_written_not_importable = any(row["definition_id"] == "FD1447_0_candidate_definition" and str(row["importable_as_C_parent"]) == "False" for row in fd)
    all_vreq_unsatisfied = all(str(row["satisfied_now"]) == "False" for row in vreq)
    ax_not_proven = all(str(row["can_sign_AX1090_0"]) == "False" for row in axp)
    hard_blocks = all(row["severity"] == "HARD_BLOCK" for row in obs)
    import_refused = refusal[0]["refusal_status"] == "REFUSED_NO_SOURCE_SIGNED_FUNCTIONAL_DERIVATIVE" and not LIVE_C_PARENT_IMPORT.exists()
    parser_false = all(str(row["claim_allowed"]) == "False" for row in parser)
    gates_false = all(str(row["claim_allowed"]) == "False" for row in gates)
    csvs_parse = all(csv_parses(path) for path in generated)
    formalization_recent = 0
    if FORMALIZATION.exists():
        formalization_recent = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)
    checks = [
        ("VAL1447_0_sources", all_sources, "all cited source paths exist"),
        ("VAL1447_1_fd_written_not_importable", fd_written_not_importable, "functional derivative target definition written but nonimportable"),
        ("VAL1447_2_VWEP_unsatisfied", all_vreq_unsatisfied, "all V_WEP domain requirements remain unsatisfied"),
        ("VAL1447_3_AX1090_not_proven", ax_not_proven, "AX1090_0 parent object proof attempt fails currently"),
        ("VAL1447_4_obstructions_hard", hard_blocks, "all obstruction rows are hard blocks"),
        ("VAL1447_5_import_refused", import_refused, "C_parent import remains absent and refused"),
        ("VAL1447_6_parser_false", parser_false, "parser dry-run refuses claim/import paths"),
        ("VAL1447_7_claim_gates", gates_false, "all claim gates remain false"),
        ("VAL1447_8_csv_parse", csvs_parse, "all generated 1447 CSVs parse cleanly"),
        ("VAL1447_9_formalization_untouched", formalization_recent == 0, f"formalization modified-file count since start={formalization_recent}"),
        ("VAL1447_10_next_target", True, "1448 handoff written"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail, "generated_utc": now()}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1447_11_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1447 writes the right functional-derivative target but proves it cannot import yet",
            "generated_utc": now(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    fd: list[dict[str, Any]],
    vreq: list[dict[str, Any]],
    axp: list[dict[str, Any]],
    obs: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    nxt: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1447 - C_parent functional derivative source or AX1090 parent-object proof\n\n")
        handle.write(
            "**Current verdict:** the right mathematical target is now explicit: `C_parent_WEP` should be a "
            "normalized parent variation against a WEP generator. But `S_parent`, `V_WEP`, `N_WEP`, and the "
            "MOMS/AX1090 signatures are not source-signed, so no import or local-GR/WEP claim opens.\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Functional derivative definition attempt", fd)
        write_table(handle, "V_WEP domain requirements", vreq)
        write_table(handle, "AX1090 parent-object proof attempt", axp)
        write_table(handle, "Obstruction matrix", obs)
        write_table(handle, "Import template refusal", refusal)
        write_table(handle, "Parser dry-run", parser)
        write_table(handle, "Claim gates", gates)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", nxt)


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def main() -> None:
    sources = source_register_rows()
    fd = fd_attempt_rows()
    vreq = vwep_requirement_rows()
    axp = ax_proof_rows()
    obs = obstruction_rows()
    refusal = import_refusal_rows()
    parser = parser_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    nxt = next_rows()

    write_live_scaffolds(fd, vreq, axp, refusal)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(FD_ATTEMPT, fd)
    write_csv(VWEP_REQUIREMENTS, vreq)
    write_csv(AX_PROOF, axp)
    write_csv(OBSTRUCTION_MATRIX, obs)
    write_csv(IMPORT_REFUSAL, refusal)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, nxt)

    validation = validation_rows(sources, fd, vreq, axp, obs, refusal, parser, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, fd, vreq, axp, obs, refusal, parser, gates, decisions, validation, nxt)
    remove_pycache()
    print("Y5_R10_1447_Cparent_functional_derivative_target_nonimportable")


if __name__ == "__main__":
    main()
