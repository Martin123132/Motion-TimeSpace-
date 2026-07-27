from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2679"
BRANCH_ID = "Y5_R2FR_PARENT_ACTION_DENSITY_LINE_OWNER_OR_EDGE_RESIDUAL_BOUND_2679"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "2679-Y5-R2FR-parent-action-density-line-owner-or-edge-residual-bound.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2679_SOURCE_REGISTER.csv",
    "line_owner_audit": RESIDUALS / "P8_Y5_R2FR_2679_ACTION_DENSITY_LINE_OWNER_AUDIT.csv",
    "line_owner_contract": RESIDUALS / "P8_Y5_R2FR_2679_LINE_OWNER_THEOREM_CONTRACT_NONCLAIM.csv",
    "edge_residual_rows": RESIDUALS / "P8_Y5_R2FR_2679_EDGE_ACTION_LINE_RESIDUAL_ROWS_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2679_LINE_OWNER_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2679_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2679_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2679_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2679_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2679_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "microscope_audit": WEP_COEFF / "action_density_line_owner_audit_nonclaim_2679.csv",
    "microscope_contract": WEP_COEFF / "line_owner_theorem_contract_nonclaim_2679.csv",
    "microscope_residuals": WEP_COEFF / "edge_action_line_residual_rows_nonclaim_2679.csv",
    "source_weight": SOURCE_INTAKE / "source-weight" / "ACTION_LINE_EDGE_RESIDUALS_2679_NONCLAIM.csv",
    "local_bounds": SOURCE_INTAKE / "local_bounds" / "edge_action_line_residual_rows_2679_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2679_2678_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2678_NEXT_TARGET.csv",
        "required_needles": ["NEXT2678_0_selected", "single parent L_action", "formalization-workbench edits"],
        "purpose": "confirms the selected 2679 line-owner target",
    },
    {
        "source_id": "SRC2679_2678_MORPHISMS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2678_PARENT_MORPHISM_CERTIFICATE_TEMPLATE_NONCLAIM.csv",
        "required_needles": ["MOR2678_4_action_density_functor", "FAIL_LINE_OWNER_UNSIGNED", "single parent L_matter=sum_A L_A"],
        "purpose": "imports the missing action-density functor row from 2678",
    },
    {
        "source_id": "SRC2679_SINGLE_LINE_ATTEMPT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/single_action_density_line_proof_attempt_nonclaim_1478.csv",
        "required_needles": ["SAL1478_0_target", "SAL1478_1_conditional_theorem", "SAL1478_4_verdict", "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED"],
        "purpose": "primary previous action-density line theorem attempt",
    },
    {
        "source_id": "SRC2679_SINGLE_LINE_GATES",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/single_action_density_line_reduction_gates_1478.csv",
        "required_needles": ["GATE1478_0_conditional_theorem", "GATE1478_2_no_go_retained", "GATE1478_5_claim_refusal"],
        "purpose": "confirms line theorem is conditional and claims are refused",
    },
    {
        "source_id": "SRC2679_NO_SOURCE_PREF_THEOREM",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv",
        "required_needles": ["NST1479_0_target", "NST1479_1_conditional_typing", "NST1479_3_same_action_limit", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
        "purpose": "imports the Hom/no-source-only prefactor theorem route",
    },
    {
        "source_id": "SRC2679_NO_SOURCE_PREF_GATES",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_reduction_gates_1479.csv",
        "required_needles": ["GATE1479_0_conditional_theorem", "GATE1479_1_theorem_refused", "GATE1479_6_firewalls"],
        "purpose": "confirms no-source-prefactor route remains nonclaim",
    },
    {
        "source_id": "SRC2679_PARENT_GRAMMAR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2677_PARENT_GRAMMAR_CONTRACT_NONCLAIM.csv",
        "required_needles": ["GRM2677_0_single_action_density_line", "GRM2677_4_source_label_forgetting", "GRM2677_6_verdict", "GRAMMAR_NOT_PARENT_SIGNED"],
        "purpose": "imports object-language clauses that would forbid w_A",
    },
    {
        "source_id": "SRC2679_PARENT_OWNER_AUDIT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2676_ACTION_SCALE_MEASURE_OWNER_PROOF_AUDIT.csv",
        "required_needles": ["OWN2676_0_parent_owner_target", "TARGET_SHARPENED_NOT_PARENT_SIGNED", "OWN2676_4_verdict"],
        "purpose": "imports common action-scale/measure owner status",
    },
    {
        "source_id": "SRC2679_EXACT_LEMMAS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2676_EXACT_CONDITIONAL_LEMMA_LEDGER.csv",
        "required_needles": ["LEM2676_0_variation_before_readout", "LEM2676_1_classical_eom_not_enough", "LEM2676_2_minimal_parent_clause"],
        "purpose": "keeps exact lemmas and no-go guardrails visible",
    },
    {
        "source_id": "SRC2679_COMMON_MEASURE",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv",
        "required_needles": ["CMT1452_0_target", "CMT1452_1_classical_EOM_limit", "CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
        "purpose": "imports hbar/measure/current owner obstruction",
    },
    {
        "source_id": "SRC2679_CURRENT_OWNER",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv",
        "required_needles": ["CSO1453_1_hilbert_variation", "CSO1453_5_pre_variation_weight", "CSO1453_7_verdict", "PARTIAL_THEOREM_NOT_CLOSED"],
        "purpose": "imports Hilbert-current subtheorem and its limit",
    },
    {
        "source_id": "SRC2679_AX1090_REDUCTION",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv",
        "required_needles": ["AXRED1441_0_parent_object", "NOT_REDUCED", "AXRED1441_2_common_measure", "AXRED1441_4_variation_order"],
        "purpose": "confirms parent object and common-measure reductions remain unsigned",
    },
    {
        "source_id": "SRC2679_PARENT_ACTION_AUDIT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/parent_action_object_current_chain_audit_nonclaim_1487.csv",
        "required_needles": ["PAO1487_0_parent_object", "PAO1487_4_ordinary_matter_route", "BEST_NARROW_ROUTE_NOT_PARENT_SIGNED", "PAO1487_5_verdict"],
        "purpose": "identifies ordinary matter subaction owner as the narrow route",
    },
    {
        "source_id": "SRC2679_ORDINARY_SUBACTION",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv",
        "required_needles": ["OMSCC1488_0_target", "OMSCC1488_2_vertical_blindness", "OMSCC1488_3_prefactor_countermodel", "NOT_CLOSED_WA_RESIDUAL_LOCKED"],
        "purpose": "imports ordinary subaction/current-chain target and prefactor countermodel",
    },
    {
        "source_id": "SRC2679_SOURCE_FACTORING",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv",
        "required_needles": ["SIGN1461_0_source_factorization", "source_label_forgetting_signed", "REFUSE_DELTA_Q_ZERO_IMPORT_WRITE_CMSM_SCAFFOLD"],
        "purpose": "keeps source-label forgetting as an unsigned dependency",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def line_owner_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ADO2679_0_target",
            "claim_piece": "single parent ordinary-matter action-density line",
            "candidate_statement": "All ordinary matter subactions are sections over one parent density/action line before source variation, readout, material projection or calibration.",
            "proof_move": "promote the 1478 target from a clean conditional theorem into a parent-owned line-bundle/action-functor statement",
            "current_evidence": "1478 states the exact target, but says L_action, hbar_parent, Dmu_parent and ordinary object language are not constructed as one syntax",
            "current_status": "TARGET_SHARPENED_NOT_PARENT_DERIVED",
            "blocking_clauses": "parent action object; single density line; common measure/hbar; no source-only scalar slot; variation order",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/single_action_density_line_proof_attempt_nonclaim_1478.csv")),
            "exact_conditional": "false",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "state the line-bundle contract and test each parent signature",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ADO2679_1_line_bundle_conditional",
            "claim_piece": "line-owner theorem",
            "candidate_statement": "If ordinary matter is A-linear over a single parent density line and only universal scalar endomorphisms of that line are admissible, relative w_A is not an object of the theory.",
            "proof_move": "treat w_A as an attempted scalar endomorphism of the action line; connected morphisms force it to one common constant and source-label forgetting removes relative readout",
            "current_evidence": "1478 and 1479 contain the exact conditional theorem pieces",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "blocking_clauses": "the line bundle/object language itself is not parent-signed",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/single_action_density_line_proof_attempt_nonclaim_1478.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
                ]
            ),
            "exact_conditional": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "derive the parent line bundle from MTS quotient/category primitives or keep residual rows",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ADO2679_2_parent_object_owner",
            "claim_piece": "one parent action object before readout",
            "candidate_statement": "S_parent owns geometry, matter, source/readout, boundary/reference and extra-sector contributions before any projection or fitting choice.",
            "proof_move": "use AX1090 and 1487 to see whether the line can be owned by an existing parent action",
            "current_evidence": "AXRED1441_0 and PAO1487_0 both keep one parent action object not reduced/not current-chain closed",
            "current_status": "PARENT_OBJECT_NOT_REDUCED",
            "blocking_clauses": "explicit L_parent and first-variation current chain are missing",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/AX1090_reduction_status.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/parent_action_object_current_chain_audit_nonclaim_1487.csv")),
                ]
            ),
            "exact_conditional": "false",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "do not treat separated sector contracts as one parent owner",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ADO2679_3_common_measure_current",
            "claim_piece": "common hbar/measure/current owner",
            "candidate_statement": "The same hbar_parent, Dmu_parent and Hilbert/Noether source extraction apply before ordinary source normalization.",
            "proof_move": "combine common-measure theorem with current-owner theorem",
            "current_evidence": "Hilbert and Ward pieces are useful conditionals, but pre-action weights and non-Hilbert bypasses survive",
            "current_status": "COMMON_MEASURE_CURRENT_UNSIGNED",
            "blocking_clauses": "hbar/measure owner; variation-before-readout; pre-action weights; zeta_NH bypass",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv")),
                ]
            ),
            "exact_conditional": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "retain measure/current residuals until parent owner exists",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ADO2679_4_no_source_prefactor_hom",
            "claim_piece": "no Hom into source-only scalar prefactors",
            "candidate_statement": "Hom_parent(species label or hidden marker, active source-prefactor scalars) is empty or common-constant only.",
            "proof_move": "convert w_A from a possible field coefficient into an ill-typed object-language term",
            "current_evidence": "1479 proves the theorem only conditionally; hidden/source marker coefficient maps remain live",
            "current_status": "HOM_EXCLUSION_NOT_PARENT_DERIVED",
            "blocking_clauses": "primitive parent object language; no hidden-visible Hom; no spurion return",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
            "exact_conditional": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "make Hom exclusion a quotient/category theorem, not an axiom",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ADO2679_5_connected_morphisms",
            "claim_piece": "A-linear parent-owned ordinary matter morphisms",
            "candidate_statement": "Ordinary matter sectors are connected by nonzero parent morphisms that preserve the same density/source-normalization line.",
            "proof_move": "reuse 2678 naturality but strengthen its edge owner to A-linear action-density maps",
            "current_evidence": "physical graph template exists, but parent-owned action-line morphisms are unsigned",
            "current_status": "MORPHISM_EDGES_UNSIGNED",
            "blocking_clauses": "MOR2678_4 action-density functor; all vertices/edges/path signatures",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2678_PARENT_MORPHISM_CERTIFICATE_TEMPLATE_NONCLAIM.csv")),
            "exact_conditional": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "stage edge residuals rather than import Delta_w_AB=0",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ADO2679_6_source_label_readout",
            "claim_piece": "source labels cannot re-enter after line collapse",
            "candidate_statement": "Source/readout forgets species labels before source normalization and cannot reintroduce material labels as spurions.",
            "proof_move": "test whether common line plus source-factorization gives observed source universality",
            "current_evidence": "source_label_forgetting_signed=false and no-spurion clauses remain unsigned",
            "current_status": "SOURCE_LABEL_REENTRY_OPEN",
            "blocking_clauses": "source-label forgetting; no source-only slot; readout and boundary silence",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
            "exact_conditional": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "keep sigma_label residual live",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ADO2679_7_nonhilbert_boundary_bypass",
            "claim_piece": "no non-Hilbert/boundary/domain bypass",
            "candidate_statement": "No retained non-Hilbert current, boundary source charge or domain projector can mimic source-weight differences after the action-line theorem.",
            "proof_move": "keep bypass channels as explicit residuals under a no-cancellation envelope",
            "current_evidence": "common-measure/current files keep zeta_A and boundary/domain composition charges live",
            "current_status": "BYPASS_CHANNELS_RETAINED",
            "blocking_clauses": "zeta_NH; q_boundary; q_domain; projector stress; no-cancellation",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
                    str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2676_ACTION_SCALE_MEASURE_OWNER_PROOF_AUDIT.csv")),
                ]
            ),
            "exact_conditional": "false",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "retain bypass terms in the residual vector",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ADO2679_8_verdict",
            "claim_piece": "parent action-density line owner closes w_A",
            "candidate_statement": "single density line + Hom exclusion + connected A-linear morphisms + source-label forgetting + no bypass implies relative action/source weights vanish",
            "proof_move": "try to turn the exact conditional theorem into a signed parent proof",
            "current_evidence": "the conditional theorem is clean, but every parent-owner signature needed for a claim remains unsigned",
            "current_status": "LINE_OWNER_NOT_PARENT_DERIVED",
            "blocking_clauses": "parent action object; line bundle; Hom exclusion; graph morphisms; source/readout silence; bypass silence",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/single_action_density_line_proof_attempt_nonclaim_1478.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv")),
                ]
            ),
            "exact_conditional": "true",
            "parent_signed": "false",
            "theorem_zero_promoted": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "attack Hom/line-bundle derivation from the quotient category or keep finite edge residuals",
            "timestamp_utc": stamp(),
        },
    ]


def line_owner_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "LOT2679_0_parent_density_line",
            "clause": "one density/action line",
            "formal_requirement": "There exists a parent line object A_ord such that L_ord,A are A_ord-valued densities before source/readout.",
            "proof_effect": "relative pre-variation scalar weights are no longer independent line choices",
            "current_status": "NOT_PARENT_CONSTRUCTED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/single_action_density_line_proof_attempt_nonclaim_1478.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "construct A_ord from parent quotient/category primitives",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LOT2679_1_A_linear_morphisms",
            "clause": "A-linear ordinary matter graph",
            "formal_requirement": "Every source-relevant ordinary-matter morphism preserves A_ord and is nonzero on the action-density/source-normalization functor.",
            "proof_effect": "naturality w_B F(f)=F(f) w_A collapses weights along every connected edge",
            "current_status": "PHYSICAL_TEMPLATE_NOT_PARENT_SIGNED",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2678_PARENT_MORPHISM_CERTIFICATE_TEMPLATE_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "replace physical template edges with parent-owned morphism signatures",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LOT2679_2_scalar_endomorphism_collapse",
            "clause": "no relative source scalar endomorphism",
            "formal_requirement": "End_parent(A_ord) admits only universal constants/common calibration on the connected ordinary component.",
            "proof_effect": "Delta_w_AB=0 modulo a global calibration constant",
            "current_status": "EXACT_IF_HOM_EXCLUSION_PARENT_SIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "prove Hom(species/hidden/readout, active-source-prefactor)=empty_or_common",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LOT2679_3_source_label_forgetting",
            "clause": "source/readout line descent",
            "formal_requirement": "The source/readout map is computed after parent variation and forgets ordinary species labels except representation constants already inside L_ord.",
            "proof_effect": "line collapse is not undone by material readout labels",
            "current_status": "UNSIGNED_DEPENDENCY",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "retain sigma_label_AB until readout/source factorization closes",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LOT2679_4_variation_before_readout",
            "clause": "Hilbert/current extraction before readout",
            "formal_requirement": "delta S_ord / delta e_obs or delta S_ord / delta g_obs is taken before material selector, calibration, source-worldtube or post-processing maps.",
            "proof_effect": "post-variation current rescaling is calibration/readout bookkeeping, not parent source ownership",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "derive readout order from parent detector/source model",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LOT2679_5_no_bypass",
            "clause": "no non-Hilbert or boundary/domain bypass",
            "formal_requirement": "No zeta_NH, boundary, domain, projector or hidden-current term has an independent material/source label after quotient descent.",
            "proof_effect": "action-line theorem would control the whole source residual vector, not just w_A",
            "current_status": "BYPASS_SILENCE_NOT_SIGNED",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2676_ACTION_SCALE_MEASURE_OWNER_PROOF_AUDIT.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "keep bypass residual rows under a no-cancellation envelope",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "LOT2679_6_verdict",
            "clause": "line-owner proof verdict",
            "formal_requirement": "All clauses LOT2679_0..5 parent-signed",
            "proof_effect": "Delta_w_AB and action-line edge residuals become theorem-zero/common-calibration, enabling WEP/local-GR source branch cleanup",
            "current_status": "CONTRACT_READY_PROOF_NOT_CLOSED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "select Hom/line-bundle derivation as next target",
            "timestamp_utc": stamp(),
        },
    ]


def edge_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ELR2679_0_action_line_weight",
            "symbol": "Delta_w_AB",
            "residual_channel": "relative action/source weight on ordinary matter",
            "formula_or_bound_contract": "Delta_w_AB=0 only if the parent line-owner theorem is signed; otherwise abs(Delta_w_AB) must be sourced or bounded independently",
            "arena_links": "WEP;R10;Newton-source;PPN;local-GR",
            "bound_or_scale": "2.8e-15 WEP envelope only, not a theory value",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/single_action_density_line_proof_attempt_nonclaim_1478.csv")),
            "status": "NONCLAIM_PARENT_ZERO_MISSING",
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive line-owner theorem or fill a source-backed finite Delta_w_AB row",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "ELR2679_1_line_owner_leak",
            "symbol": "epsilon_L",
            "residual_channel": "failure of ordinary sectors to share one density line",
            "formula_or_bound_contract": "epsilon_L measures non-common A_ord line ownership before variation",
            "arena_links": "WEP;R10;source-normalization;local-GR",
            "bound_or_scale": "requires parent line-bundle certificate or numeric residual",
            "units": "dimensionless or declared line-norm",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/parent_action_object_current_chain_audit_nonclaim_1487.csv")),
            "status": "MISSING_PARENT_LINE_OWNER",
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "construct A_ord and its norm/convention",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "ELR2679_2_edge_morphism_leak",
            "symbol": "epsilon_edge_AB",
            "residual_channel": "physical graph edge not promoted to A-linear parent morphism",
            "formula_or_bound_contract": "epsilon_edge_AB=0 if every relevant matter edge is a nonzero parent-owned A_ord-linear morphism",
            "arena_links": "WEP material graph;ordinary matter source graph",
            "bound_or_scale": "schema",
            "units": "edge certificate / dimensionless residual if normed",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2678_PARENT_MORPHISM_CERTIFICATE_TEMPLATE_NONCLAIM.csv")),
            "status": "EDGE_CERTIFICATE_TEMPLATE_NONCLAIM",
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "parent-sign electron/photon/quark/gluon/bound-state/material morphisms",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "ELR2679_3_measure_current_leak",
            "symbol": "epsilon_mu_AB",
            "residual_channel": "hbar/measure/current source-normalization mismatch",
            "formula_or_bound_contract": "epsilon_mu_AB includes relative hbar_A, J_A, c_A and pre-variation current weights",
            "arena_links": "WEP;clock;R10;PPN",
            "bound_or_scale": "2.8e-15 WEP envelope only, not score-ready",
            "units": "dimensionless after source normalization",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
            "status": "COMMON_MEASURE_CURRENT_UNSIGNED",
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive common measure/current owner or source finite components",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "ELR2679_4_source_label_reentry",
            "symbol": "sigma_label_AB",
            "residual_channel": "source/readout label re-entry after line collapse",
            "formula_or_bound_contract": "sigma_label_AB=0 only if source_label_forgetting and no-spurion-return are parent-signed",
            "arena_links": "WEP;source-worldtube;clock/readout;local-GR",
            "bound_or_scale": "requires theorem-zero or numeric source model",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
            "status": "SOURCE_LABEL_FORGETTING_UNSIGNED",
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive source/readout descent or keep material-label residual",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "ELR2679_5_nonhilbert_boundary_bypass",
            "symbol": "zeta_NH_AB+q_boundary_AB+q_domain_AB",
            "residual_channel": "non-Hilbert, boundary or domain source bypass",
            "formula_or_bound_contract": "bypass residuals must vanish individually or enter the no-cancellation envelope",
            "arena_links": "PPN;orbital;R10;local-GR;boundary/domain source tests",
            "bound_or_scale": "requires arena projection rows",
            "units": "dimensionless after projection",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2676_ACTION_SCALE_MEASURE_OWNER_PROOF_AUDIT.csv")),
            "status": "BYPASS_CHANNELS_RETAINED",
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive bypass silence or keep as separate residual vector entries",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "ELR2679_6_no_cancellation_envelope",
            "symbol": "epsilon_action_line_total",
            "residual_channel": "absolute no-cancellation envelope",
            "formula_or_bound_contract": "abs(epsilon_total)>=abs(Delta_w_AB)+abs(epsilon_L)+abs(epsilon_edge_AB)+abs(epsilon_mu_AB)+abs(sigma_label_AB)+abs(zeta_NH_AB+q_boundary_AB+q_domain_AB)",
            "arena_links": "all local source arenas",
            "bound_or_scale": "not computable until component rows are theorem-zero or numeric",
            "units": "dimensionless/envelope",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2677_WA_JA_BOUND_ROWS_NONCLAIM.csv")),
            "status": "NO_CANCELLATION_ENVELOPE_NOT_COMPUTED",
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "score only after every component is zero or source-backed",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "ELR2679_7_acquisition_template",
            "symbol": "K_edge * tau_arena * epsilon_action_line_total",
            "residual_channel": "future finite residual projection",
            "formula_or_bound_contract": "arena residual <= bound only after K_edge, tau_arena, source path, units and no-cancellation statement are filled",
            "arena_links": "WEP;R10;PPN;clock;orbital",
            "bound_or_scale": "template only",
            "units": "declared per arena",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_reduction_gates_1479.csv")),
            "status": "ACQUISITION_TEMPLATE_NONCLAIM",
            "score_ready": "false",
            "has_numeric_value": "false",
            "parent_zero_available": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "fill only after parent theorem fails and arena projection inputs are sourced",
            "timestamp_utc": stamp(),
        },
    ]


def runner_results_rows(audit_rows: list[dict[str, Any]], contract_rows: list[dict[str, Any]], residual_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in audit_rows:
        rows.append(
            {
                "runner_id": f"RUN2679_{row['audit_id']}",
                "target_id": row["audit_id"],
                "stage": "line_owner_audit",
                "has_parent_zero": row["theorem_zero_promoted"],
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(all(Path(path).exists() for path in row["source_paths"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_LINE_OWNER_UNSIGNED",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in contract_rows:
        rows.append(
            {
                "runner_id": f"RUN2679_{row['contract_id']}",
                "target_id": row["contract_id"],
                "stage": "line_owner_contract",
                "has_parent_zero": "false",
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_CONTRACT_NOT_PARENT_SIGNED",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in residual_rows:
        rows.append(
            {
                "runner_id": f"RUN2679_{row['row_id']}",
                "target_id": row["row_id"],
                "stage": "edge_residual_bound",
                "has_parent_zero": row["parent_zero_available"],
                "has_numeric_bound": row["has_numeric_value"],
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_RESIDUAL_NONCLAIM",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2679_0_conditional_theorem",
            "claim": "line-owner theorem is mathematically useful",
            "status": "PASS_EXACT_CONDITIONAL_ONLY",
            "blocking_rows": "ADO2679_1_line_bundle_conditional;LOT2679_6_verdict",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2679_1_parent_object",
            "claim": "one parent action object owns ordinary matter before readout",
            "status": "FAIL_PARENT_OBJECT_NOT_REDUCED",
            "blocking_rows": "ADO2679_2_parent_object_owner;LOT2679_0_parent_density_line",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2679_2_Hom_exclusion",
            "claim": "species/hidden/readout labels cannot map into active source prefactors",
            "status": "FAIL_HOM_EXCLUSION_UNSIGNED",
            "blocking_rows": "ADO2679_4_no_source_prefactor_hom;LOT2679_2_scalar_endomorphism_collapse",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2679_3_graph_edges",
            "claim": "ordinary matter graph edges are A-linear parent morphisms",
            "status": "FAIL_EDGE_CERTIFICATE_UNSIGNED",
            "blocking_rows": "ADO2679_5_connected_morphisms;ELR2679_2_edge_morphism_leak",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2679_4_residual_bound",
            "claim": "edge/action-line residual vector can be scored",
            "status": "FAIL_COMPONENTS_MISSING_NUMERIC_OR_THEOREM_ZERO",
            "blocking_rows": "ELR2679_0_action_line_weight;ELR2679_1_line_owner_leak;ELR2679_6_no_cancellation_envelope",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2679_5_local_GR",
            "claim": "local GR/PPN can use action-line owner to silence source coupling",
            "status": "CLAIM_BLOCKED",
            "blocking_rows": "ADO2679_8_verdict;CG2679_1_parent_object;CG2679_2_Hom_exclusion;CG2679_4_residual_bound",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2679_0_theorem_attempt",
            "question": "Can 2679 prove the parent action-density line owner?",
            "result": "not_yet",
            "reason": "the theorem is exact conditional, but parent action object, line bundle, Hom exclusion, source/readout and bypass clauses are not parent-signed",
            "action": "do not import Delta_w_AB=0 or any local-GR source coupling pass",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2679_1_actual_progress",
            "question": "What is new rather than circular?",
            "result": "root coupling contract isolated",
            "reason": "w_A is now pinned to a precise line-bundle/Hom-exclusion problem rather than vague WEP failure",
            "action": "attack parent line-bundle object language next",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2679_2_fallback",
            "question": "If line-owner proof fails, what remains?",
            "result": "explicit finite residual vector",
            "reason": "epsilon_L, epsilon_edge, epsilon_mu, sigma_label and bypass terms are separated under a no-cancellation envelope",
            "action": "source numeric bounds only if theorem route fails and arena projections are real",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2679_3_next_route",
            "question": "Best next derivation target?",
            "result": "parent_line_bundle_Hom_exclusion_or_ordinary_subaction_descent",
            "reason": "the least smuggly route is to derive the admissible coefficient/Hom algebra from the quotient/category, not assume WEP/EEP",
            "action": "select 2680",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2679_0_selected",
            "kind": "selected",
            "target_doc": "2680-Y5-R2FR-parent-line-bundle-Hom-exclusion-or-ordinary-subaction-descent.md",
            "target_script": "scripts/Y5_R2FR_parent_line_bundle_Hom_exclusion_or_ordinary_subaction_descent_2680.py",
            "purpose": "try to derive the no-source-prefactor Hom exclusion from the parent quotient/line-bundle object language, or demote the action-line route to explicit residual bounds",
            "acceptance_gate": "construct A_ord line object, admissible coefficient algebra, Hom(species/hidden/readout, source-prefactor)=empty_or_common, ordinary subaction descent and variation-before-readout",
            "forbidden_shortcuts": "assuming EEP/WEP; using classical EOM scaling; treating physical graph as parent proof; importing Delta_w=0; bound inversion; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PS2679_0_scope",
            "field": "workspace_scope",
            "value": str(ROOT),
            "status": "private_post_checkpoint_only",
            "note": "no GitHub action and no formalization-workbench writes",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2679_1_progress",
            "field": "coupling_problem",
            "value": "w_A source coupling reduced to action-density line/Hom-exclusion contract",
            "status": "sharpened_not_claimed",
            "note": "this is a real narrowing of the root coupling debt, not a pass",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2679_2_next",
            "field": "next_derivation",
            "value": "parent_line_bundle_Hom_exclusion_or_ordinary_subaction_descent",
            "status": "selected",
            "note": "derive from quotient/object-language primitives before numeric testing",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2679_0_audit",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["line_owner_audit"]),
            "destination": str(BRANCH_OUTPUTS["microscope_audit"]),
            "contents": "action-density line owner audit retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2679_1_contract",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["line_owner_contract"]),
            "destination": str(BRANCH_OUTPUTS["microscope_contract"]),
            "contents": "line-owner theorem contract retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2679_2_residuals",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["edge_residual_rows"]),
            "destination": str(BRANCH_OUTPUTS["microscope_residuals"]),
            "contents": "edge/action-line residual rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2679_3_source_weight",
            "branch": "source-weight",
            "source_table": rel_path(OUTPUTS["edge_residual_rows"]),
            "destination": str(BRANCH_OUTPUTS["source_weight"]),
            "contents": "source-weight action-line residuals retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2679_4_local_bounds",
            "branch": "local_bounds",
            "source_table": rel_path(OUTPUTS["edge_residual_rows"]),
            "destination": str(BRANCH_OUTPUTS["local_bounds"]),
            "contents": "local bound action-line residuals retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "true" and row["missing_needles"] == "" for row in rows["source_register"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_sources_exist_and_needles_found", "passed": as_bool(source_ok), "details": "all cited source paths exist and required needles are present"})

    all_nonclaim = all(row.get("valid_for_claim") == "false" for table in rows.values() for row in table)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_nonclaim_guard", "passed": as_bool(all_nonclaim), "details": "all generated rows carry valid_for_claim=false"})

    verdict_blocks = any(row["audit_id"] == "ADO2679_8_verdict" and row["current_status"] == "LINE_OWNER_NOT_PARENT_DERIVED" for row in rows["line_owner_audit"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_line_owner_verdict_blocks_claim", "passed": as_bool(verdict_blocks), "details": "line-owner theorem is not promoted"})

    conditional_kept = any(row["audit_id"] == "ADO2679_1_line_bundle_conditional" and row["exact_conditional"] == "true" and row["theorem_zero_promoted"] == "false" for row in rows["line_owner_audit"])
    contract_ready = any(row["contract_id"] == "LOT2679_6_verdict" and row["current_status"] == "CONTRACT_READY_PROOF_NOT_CLOSED" for row in rows["line_owner_contract"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_contract_conditional_not_claim", "passed": as_bool(conditional_kept and contract_ready), "details": "exact conditional contract exists but is not parent-signed"})

    no_go_guard = any(row["audit_id"] == "ADO2679_3_common_measure_current" and "pre-action weights" in row["blocking_clauses"] for row in rows["line_owner_audit"]) and any(row["contract_id"] == "LOT2679_4_variation_before_readout" for row in rows["line_owner_contract"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_no_go_guards_retained", "passed": as_bool(no_go_guard), "details": "classical EOM/pre-variation-weight loophole is retained"})

    residual_ids = {row["row_id"] for row in rows["edge_residual_rows"]}
    residuals_complete = {"ELR2679_0_action_line_weight", "ELR2679_1_line_owner_leak", "ELR2679_2_edge_morphism_leak", "ELR2679_4_source_label_reentry", "ELR2679_5_nonhilbert_boundary_bypass", "ELR2679_6_no_cancellation_envelope"}.issubset(residual_ids)
    residuals_nonclaim = all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in rows["edge_residual_rows"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_residual_rows_complete_nonclaim", "passed": as_bool(residuals_complete and residuals_nonclaim), "details": "action-line, edge, label, bypass and no-cancellation residuals exist and remain nonclaim"})

    gates_ok = any(row["gate_id"] == "CG2679_5_local_GR" and row["status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and any(row["gate_id"] == "CG2679_0_conditional_theorem" and row["status"] == "PASS_EXACT_CONDITIONAL_ONLY" for row in rows["claim_gates"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_claim_gates_correct", "passed": as_bool(gates_ok), "details": "conditional theorem acknowledged while local-GR remains blocked"})

    runner_refuses = all(row["scored"] == "false" and row["claim_pass"] == "false" for row in rows["runner_results"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_runner_refuses_unsigned_rows", "passed": as_bool(runner_refuses), "details": "runner refuses scoring without parent zero or numeric residuals"})

    next_selected = any(row["target_id"] == "NEXT2679_0_selected" and "2680-Y5-R2FR-parent-line-bundle-Hom-exclusion-or-ordinary-subaction-descent.md" in row["target_doc"] for row in rows["next_target"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_next_target_selected", "passed": as_bool(next_selected), "details": "next target selects parent line-bundle/Hom exclusion"})

    parse_results = [parse_csv(path) for path in csv_paths]
    csv_ok = all(result[0] and result[1] > 0 for result in parse_results)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_csv_parse", "passed": as_bool(csv_ok), "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(csv_paths, parse_results))})

    branch_paths = [Path(row["destination"]) for row in rows["branch_copies"]]
    branch_parse = [parse_csv(path) for path in branch_paths]
    branch_ok = all(result[0] and result[1] > 0 for result in branch_parse)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_branch_copies_parse", "passed": as_bool(branch_ok), "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(branch_paths, branch_parse))})

    generated_paths = [*csv_paths, *branch_paths, DOC_PATH]
    formalization_guard = all("formalization-workbench" not in str(path) for path in generated_paths)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_formalization_write_guard", "passed": as_bool(formalization_guard), "details": "generated path allowlist excludes formalization-workbench"})

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_pycache_absent_at_validation_time", "passed": as_bool(pycache_absent), "details": "scripts/__pycache__ absent when validation rows were produced"})

    overall = all(row["passed"] == "true" for row in out if row["validation_id"] != "VAL2679_pycache_absent_at_validation_time")
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2679_OVERALL", "passed": as_bool(overall), "details": "2679 isolates the root coupling debt as a parent action-density line/Hom-exclusion theorem, keeps it nonclaim, and stages finite edge residual rows"})
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        f"# {CHECKPOINT} - Parent Action-Density Line Owner Or Edge Residual Bound",
        "",
        "## Private Verdict",
        "",
        "2679 is a real narrowing, not a victory lap. The coupling problem is now pinned to a precise statement: ordinary matter must live on one parent action-density line, with no species/hidden/readout Hom into active source prefactors. If that line-bundle/Hom contract is parent-signed, relative `w_A` collapses to a common calibration mode and cannot source WEP/local-GR residuals.",
        "",
        "But the current corpus does not yet parent-sign the line object, scalar endomorphism algebra, A-linear graph morphisms, source-label forgetting, variation-before-readout, or bypass silence. So no `Delta_w_AB=0`, no local-GR pass, and no WEP/R10/PPN/clock/orbital claim is made here.",
        "",
        "The useful output is the exact contract plus a finite residual vector. The next non-circular attack is to derive the parent line-bundle/Hom exclusion from quotient/category primitives instead of assuming EEP/WEP.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["source_register"]),
        "",
        "## Action-Density Line Owner Audit",
        "",
        markdown_table(rows["line_owner_audit"]),
        "",
        "## Line Owner Theorem Contract",
        "",
        markdown_table(rows["line_owner_contract"]),
        "",
        "## Edge/Action-Line Residual Rows",
        "",
        markdown_table(rows["edge_residual_rows"]),
        "",
        "## Runner Results",
        "",
        markdown_table(rows["runner_results"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(rows["claim_gates"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision_ledger"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next_target"]),
        "",
        "## Project Status",
        "",
        markdown_table(rows["project_status"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branch_copies"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)

    rows: dict[str, list[dict[str, Any]]] = {}
    rows["source_register"] = source_register_rows()
    rows["line_owner_audit"] = line_owner_audit_rows()
    rows["line_owner_contract"] = line_owner_contract_rows()
    rows["edge_residual_rows"] = edge_residual_rows()
    rows["runner_results"] = runner_results_rows(rows["line_owner_audit"], rows["line_owner_contract"], rows["edge_residual_rows"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision_ledger"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    rows["branch_copies"] = branch_copy_rows()

    for name in [
        "source_register",
        "line_owner_audit",
        "line_owner_contract",
        "edge_residual_rows",
        "runner_results",
        "claim_gates",
        "decision_ledger",
        "next_target",
        "project_status",
        "branch_copies",
    ]:
        write_csv(OUTPUTS[name], rows[name])

    write_csv(BRANCH_OUTPUTS["microscope_audit"], rows["line_owner_audit"])
    write_csv(BRANCH_OUTPUTS["microscope_contract"], rows["line_owner_contract"])
    write_csv(BRANCH_OUTPUTS["microscope_residuals"], rows["edge_residual_rows"])
    write_csv(BRANCH_OUTPUTS["source_weight"], rows["edge_residual_rows"])
    write_csv(BRANCH_OUTPUTS["local_bounds"], rows["edge_residual_rows"])

    csv_paths = [OUTPUTS[name] for name in OUTPUTS if name != "validation"]
    rows["validation"] = validation_rows(rows, csv_paths)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
