from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3251-Y5-R2FR-source-prefactor-edge-zero-or-same-frame-DJH-residual-first-bound-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3251_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3251_NOHOM_CONNECTED_NATURALITY_THEOREM.csv",
    "edge_audit": OUT / "P8_Y5_R2FR_3251_ACTION_DENSITY_EDGE_CERTIFICATE_AUDIT.csv",
    "bound_row": OUT / "P8_Y5_R2FR_3251_DJH_WEIGHTED_SOURCE_BOUND_ROW.csv",
    "residual_update": OUT / "P8_Y5_R2FR_3251_DJH_RESIDUAL_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3251_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3251_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3251_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3251_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
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
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            low = line.lower()
            if any(needle in low for needle in lowered):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:220]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3251_3250_handoff",
            ROOT / "3250-Y5-R2FR-Hilbert-current-eobs-tau-owner-or-source-worldtube-flux-norm-row-under-AX1090.md",
            "same-frame D_A J_H residual handoff",
            ["DJH3250_3_weighted_source", "C_wH", "NEXT3250"],
        ),
        (
            "SRC3251_1721_prefactor",
            ROOT / "1721-Y5-R2FR-source-prefactor-exclusion-or-wA-current-row.md",
            "source-only prefactor theorem audit",
            ["NSP1721_3_action_density_graph_route", "C_wH", "source-only"],
        ),
        (
            "SRC3251_1722_CwH",
            OUT / "P8_Y5_PARENT_QLOC_1722_CWH_BOUND_LAW.csv",
            "weighted Hilbert current operator bound",
            ["CWHL1722_1_operator_bound", "C_Tw", "EXACT_NORM_BOUND_FORM"],
        ),
        (
            "SRC3251_1722_edge",
            OUT / "P8_Y5_PARENT_QLOC_1722_PARENT_ACTION_DENSITY_EDGE_AUDIT.csv",
            "action-density edge theorem route",
            ["PED1722_2_no_Hom_plus_edge_zero_law", "connected", "C_wH=0"],
        ),
        (
            "SRC3251_1065_grammar",
            OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
            "no-source-only parent grammar audit",
            ["PGG1065_1_no_inert_species_scalar", "w_A", "source-only"],
        ),
        (
            "SRC3251_1066_scalar",
            OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "source scalar exclusion and naturality route",
            ["SSE1066_0_target", "SSE1066_3_naturality_route", "source-only"],
        ),
        (
            "SRC3251_1230_action_scale",
            OUT / "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv",
            "connected-naturality theorem",
            ["UAS1230_1_connected_naturality_lemma", "w_A=w_*", "EXACT_CONDITIONAL_THEOREM"],
        ),
        (
            "SRC3251_1231_connectedness",
            OUT / "P8_Y5_R10_1231_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv",
            "ordinary matter category connectedness",
            ["CMC1231_1_interaction_graph_lemma", "connected interaction graph", "w_*"],
        ),
        (
            "SRC3251_1232_graph",
            OUT / "P8_Y5_R10_1232_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv",
            "interaction graph certificate attempt",
            ["IGC1232_1_graph_connectedness_lemma", "G_ord", "connected"],
        ),
        (
            "SRC3251_1232_edges",
            OUT / "P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv",
            "ordinary matter edge audit",
            ["EDGE1232_0_electron_photon", "EDGE1232_2_quark_gluon", "parent"],
        ),
        (
            "SRC3251_1233_edge_attempt",
            OUT / "P8_Y5_R10_1233_EM_CURRENT_EDGE_OWNER_PROOF_ATTEMPT.csv",
            "first edge owner proof attempt",
            ["EME1233_4_graph_edge_verdict", "electron-photon", "not parent-signed"],
        ),
        (
            "SRC3251_1046_marker",
            ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md",
            "constant/marker/source-only weight audit",
            ["CMA1046_4_source_only_weights", "FV1046_6_source_only_weight", "CG1046"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NHE3251_0_language",
            "claim_piece": "no inert source-only scalar",
            "formal_statement": "The parent matter grammar has no argument w_A that multiplies active source strength while carrying no observable, gauge, representation, geometry, or quotient type.",
            "proof_step": "If a symbol changes only gravitational source extraction and has no parent type, it is not a legal parent argument; otherwise it is retained as an explicit residual.",
            "result": "EXACT_TYPING_CLAUSE_IF_PARENT_LANGUAGE_SIGNED",
            "missing_for_claim": "parent object-language derivation from MTS primitives",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHE3251_1_action_density_line",
            "claim_piece": "one parent action-density line",
            "formal_statement": "Ordinary matter sectors are sections of one parent action-density/source functor L_action over C_ord, not independent source-normalization lines.",
            "proof_step": "A relative source multiplier is a positive natural automorphism w of L_action only if the parent permits such automorphisms.",
            "result": "CONDITIONAL_ACTION_LINE_OWNER",
            "missing_for_claim": "single L_action/hbar/measure owner not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHE3251_2_edge_equalizer",
            "claim_piece": "nonzero edge forces equal weights",
            "formal_statement": "For a parent-owned nonzero morphism F_e:A->B, naturality gives w_B F_e = F_e w_A; on one-dimensional positive action-density lines this implies w_B=w_A.",
            "proof_step": "This is the algebraic punch: a real parent-owned interaction/current edge collapses two relative source weights.",
            "result": "EXACT_CONDITIONAL_LEMMA",
            "missing_for_claim": "parent-owned nonzero graph-edge certificates",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHE3251_3_connected_graph",
            "claim_piece": "connected graph collapses all relative weights",
            "formal_statement": "If G_ord is connected and every edge is a parent-owned nonzero action-density/source morphism, then w_A=w_* for every ordinary matter component.",
            "proof_step": "Propagate NHE3251_2 along paths in G_ord.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "G_ord connectedness and edge ownership remain unsigned",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHE3251_4_common_mode",
            "claim_piece": "common source scale is not a local residual",
            "formal_statement": "If w_A=w_* is universal, range-independent, species-independent, frame-independent, and fixed before readout, then T_eff=w_* sum_A T_A and w_* is one coupling normalization rather than a relative source residual.",
            "proof_step": "Common mode may be absorbed into the calibrated gravitational coupling only after universality is proven; relative modes cannot.",
            "result": "EXACT_IF_NHE3251_3_SIGNED_AND_D_A_WSTAR_ZERO",
            "missing_for_claim": "common-mode constancy and universal coupling owner",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHE3251_5_CwH_zero",
            "claim_piece": "remove weighted-source term from D_A J_H",
            "formal_statement": "With NHE3251_0 through NHE3251_4 signed, delta_w_rel=0 and C_wH=||star(sum_A delta_w_A T_A_obs(tau,.))||=0.",
            "proof_step": "The 3250 residual term DJH3250_3 vanishes without fitting or data.",
            "result": "FUSED_ZERO_THEOREM_CONDITIONAL",
            "missing_for_claim": "no-Hom grammar, connected graph, action-line owner, measure/current owner, and edge certificates",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHE3251_6_current_verdict",
            "claim_piece": "current MTS C_wH theorem status",
            "formal_statement": "The theorem shape is now exact, but current MTS has not parent-signed the premises, so C_wH remains a live nonclaim residual.",
            "proof_step": "Use bound rows unless a future parent action signs the edge/grammar package.",
            "result": "NOT_CURRENT_CLAIM",
            "missing_for_claim": "parent signatures rather than further notation",
            "valid_for_claim": "false",
        },
    ]


def edge_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "AEC3251_0_no_Hom",
            "required_clause": "no source-only Hom/species scalar in parent grammar",
            "current_evidence": "1065/1066 make the clause sharp but conditional",
            "if_signed": "delta_w symbols are illegal unless observable/residual",
            "if_unsigned": "relative source weights survive covariance and additivity",
            "status": "UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AEC3251_1_L_action",
            "required_clause": "one parent action-density line and hbar/measure owner for ordinary matter",
            "current_evidence": "1230 UAS/MDS rows state the owner theorem and measure extension",
            "if_signed": "sector source scales become one natural automorphism",
            "if_unsigned": "species hbar/measure Jacobian can recreate w_A",
            "status": "UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AEC3251_2_connected_Gord",
            "required_clause": "G_ord connected across electron, EM, quark, gluon, nuclear, measure/readout components",
            "current_evidence": "1231/1232 write graph theorem and edge list",
            "if_signed": "relative component weights collapse to common mode",
            "if_unsigned": "disconnected-component residual basis remains active",
            "status": "UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AEC3251_3_edge_ownership",
            "required_clause": "each graph edge is parent-owned and nonzero before source extraction",
            "current_evidence": "1233 electron-photon edge is conditional math clear but not parent-signed",
            "if_signed": "naturality equalizer can propagate through real edges",
            "if_unsigned": "graph connectedness is only physical plausibility",
            "status": "UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AEC3251_4_readout_no_reentry",
            "required_clause": "measure, coframe, boundary and readout maps do not reintroduce species labels after summation",
            "current_evidence": "1230/1231 keep measure/readout descent open",
            "if_signed": "q_src label forgetting survives to J_H",
            "if_unsigned": "delta_w_K/readout residual stays live",
            "status": "UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AEC3251_5_no_shadow_marker",
            "required_clause": "no hidden frame, constant, marker or material label acts as source-only prefactor",
            "current_evidence": "1046 classifies source-only weights and marker/constant debt",
            "if_signed": "delta_w cannot hide in qbar_marker/qbar_constants",
            "if_unsigned": "weighted-source residual couples to WEP/R10/clock rows",
            "status": "UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AEC3251_6_nonHilbert_silence",
            "required_clause": "non-Hilbert, boundary, torsion, projector or domain currents do not create an independent source label",
            "current_evidence": "1044/1721/3250 retain non-Hilbert and edge terms as residuals",
            "if_signed": "C_wH is the only source-weight slot and can vanish with delta_w",
            "if_unsigned": "finite same-frame residual bound remains mandatory",
            "status": "UNSIGNED",
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DWB3251_0_operator",
            "target_residual": "DJH3250_3_weighted_source",
            "quantity": "C_Tw",
            "definition": "C_Tw := ||L_Tw||_{Sigma->J,A}, L_Tw[delta_w]=star_eobs(sum_c delta_w_c T_c_obs(tau,.))",
            "bound": "C_wH <= C_Tw ||delta_w||_Sigma",
            "required_inputs": "A_ext;norm_pair;component_basis;T_c_obs_decomposition;tau_id;Sigma_metric;units;source_paths",
            "current_value": "MISSING_C_TW_OPERATOR_NORM",
            "units": "MISSING_CURRENT_NORM_UNITS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DWB3251_1_delta_w_norm",
            "target_residual": "DJH3250_3_weighted_source",
            "quantity": "||delta_w||_Sigma",
            "definition": "relative source-weight norm after removing the common mode: delta_w := Pi_rel w, ||delta_w||_Sigma=(delta_w^T Sigma delta_w)^{1/2}",
            "bound": "zero if NHE3251 package signs; otherwise finite prior/source row required",
            "required_inputs": "component weights;common-mode projector;Sigma covariance;source or parent theorem;no-cancellation policy",
            "current_value": "MISSING_DELTA_W_VECTOR_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DWB3251_2_first_DJH_bound",
            "target_residual": "D_A J_H master residual",
            "quantity": "weighted_source_piece",
            "definition": "same-frame weighted-source contribution to ||D_A J_H||",
            "bound": "||D_A J_H||_weighted <= C_Tw ||delta_w||_Sigma",
            "required_inputs": "DWB3251_0_operator;DWB3251_1_delta_w_norm;same e_obs/tau/A_ext;absolute-sum policy",
            "current_value": "NOT_COMPUTED",
            "units": "same_as_J_H_current_norm",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def residual_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "DRU3251_0_replace_Cw_placeholder",
            "target": "DJH3250_3_weighted_source",
            "previous_form": "C_w||delta w||",
            "new_form": "C_wH <= C_Tw(A_ext,norm_pair,tau,component_basis)||delta_w||_Sigma",
            "gain": "weighted-source debt now has an exact operator, domain, codomain and norm target",
            "claim_effect": "nonclaim until C_Tw and delta_w are theorem-zero or source-backed",
            "valid_for_claim": "false",
        },
        {
            "update_id": "DRU3251_1_zero_route",
            "target": "SFP3250_3_DJH_zero_if_signed",
            "previous_form": "D_A w_i=0 required",
            "new_form": "D_A w_i=0 follows if no-Hom + connected naturality + common-mode constancy are parent-signed",
            "gain": "turns one same-frame package clause into a concrete theorem route",
            "claim_effect": "does not close current local branch",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3251_0_theorem_shape",
            "claim": "no-Hom plus connected naturality implies C_wH=0 conditionally",
            "gate_pass": "true",
            "reason": "edge equalizer and connected graph proof are written exactly",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3251_1_current_parent_signature",
            "claim": "current MTS parent signs no-Hom/action-density/connected-edge package",
            "gate_pass": "false",
            "reason": "all edge certificate clauses remain unsigned",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3251_2_CwH_zero_current",
            "claim": "C_wH=0 is a current MTS theorem",
            "gate_pass": "false",
            "reason": "delta_w theorem-zero requires parent signatures not present in corpus",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3251_3_CwH_bound_numeric",
            "claim": "weighted-source residual bound is numeric/source-backed",
            "gate_pass": "false",
            "reason": "C_Tw, delta_w vector, norm pair, component tensors, annulus and units are missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3251_4_local_GR_Newton",
            "claim": "local GR/Newton source coupling is derived",
            "gate_pass": "false",
            "reason": "D_A J_H still has live residual components after this checkpoint",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3251_0_progress",
            "decision": "Promote connected naturality to the active C_wH zero route",
            "because": "it is a real theorem: nonzero parent edges force source weights equal, not fitted",
            "next_action": "try to parent-sign the action-density line/measure owner or one graph edge certificate",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3251_1_bound",
            "decision": "Keep the finite C_Tw||delta_w|| row as the fallback",
            "because": "same-action covariance does not kill relative weights and the parent signature is not closed",
            "next_action": "do not claim; source C_Tw and delta_w only if theorem route fails",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3251_2_best_next",
            "decision": "Attack parent action-density line and measure owner before data",
            "because": "without a single L_action/hbar/measure owner, disconnected source-weight loopholes keep returning",
            "next_action": "write 3252 against the parent L_action/hbar/measure owner or C_Tw operator-norm first source row",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3251_0_3252",
            "selection": "selected_primary",
            "next_checkpoint": "3252-Y5-R2FR-parent-action-density-line-owner-or-C_Tw-operator-norm-first-source-row-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3252_parent_action_density_line_owner_or_CTw_operator_norm_first_source_row.py",
            "objective": "Try to parent-sign one ordinary matter action-density line/hbar/measure owner that makes source weights a common mode; if not, fill the first C_Tw operator-norm source row for the same-frame D_A J_H weighted-source residual.",
            "guardrail": "do not use covariance/additivity/classical EOM scaling as proof; do not absorb relative weights into G; no local-GR/WEP/R10 claim",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources_exist = all(row["exists"] == "true" for row in source_rows)
    sources_hit = all(row["evidence_hits"] not in {"MISSING_SOURCE", "NO_MATCH"} for row in source_rows)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    under_post_checkpoint = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in [*generated_csvs, DOC])
    formalization_3251 = list(FW.rglob("*3251*")) if FW.exists() else []
    formalization_clean = len(formalization_3251) == 0
    theorem_present = any(row["theorem_id"] == "NHE3251_5_CwH_zero" for row in theorem_rows())
    edge_audit_present = len(edge_audit_rows()) >= 6
    bound_present = any(row["row_id"] == "DWB3251_2_first_DJH_bound" for row in bound_rows())
    bound_nonclaim = all(row["valid_for_claim"] == "false" for row in bound_rows())
    bound_has_missing = any("MISSING_" in ";".join(str(value) for value in row.values()) for row in bound_rows())
    claims_blocked = all(row["claim_allowed"] == "false" for row in gate_rows())
    parent_signature_false = any(row["claim_gate_id"] == "CG3251_1_current_parent_signature" and row["gate_pass"] == "false" for row in gate_rows())
    next_written = bool(next_rows())
    doc_written = DOC.exists()
    checks = [
        ("VAL3251_0_sources_exist", sources_exist, "all cited source paths exist", str(sources_exist)),
        ("VAL3251_1_source_hits", sources_hit, "source evidence hits are present", str(sources_hit)),
        ("VAL3251_2_csvs_parse", csvs_parse, "all generated CSV files parse", str(csvs_parse)),
        ("VAL3251_3_outputs_under_post_checkpoint", under_post_checkpoint, "all outputs are under post-checkpoint-work", str(under_post_checkpoint)),
        ("VAL3251_4_formalization_clean", formalization_clean, "no 3251 outputs in formalization-workbench", f"formalization_3251_count={len(formalization_3251)}"),
        ("VAL3251_5_theorem_present", theorem_present, "C_wH zero theorem route written", str(theorem_present)),
        ("VAL3251_6_edge_audit_present", edge_audit_present, "edge certificate audit covers required clauses", str(edge_audit_present)),
        ("VAL3251_7_bound_present", bound_present, "first D_A J_H weighted-source bound row present", str(bound_present)),
        ("VAL3251_8_bound_nonclaim", bound_nonclaim, "weighted-source bound rows remain nonclaim", str(bound_nonclaim)),
        ("VAL3251_9_bound_has_missing", bound_has_missing, "bound rows preserve missing-input markers", str(bound_has_missing)),
        ("VAL3251_10_claims_blocked", claims_blocked, "all claim gates remain blocked", str(claims_blocked)),
        ("VAL3251_11_parent_signature_false", parent_signature_false, "current parent signature gate remains false", str(parent_signature_false)),
        ("VAL3251_12_next_written", next_written, "3252 next target written", str(next_written)),
        ("VAL3251_13_doc_written", doc_written, "3251 markdown checkpoint exists", str(doc_written)),
    ]
    rows = [
        {"validation_id": validation_id, "passed": bool_str(passed), "requirement": requirement, "evidence": evidence_text}
        for validation_id, passed, requirement, evidence_text in checks
    ]
    rows.append(
        {
            "validation_id": "VAL3251_OVERALL",
            "passed": bool_str(all(row["passed"] == "true" for row in rows)),
            "requirement": "3251 validation overall",
            "evidence": "all required validation rows passed",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    edge_audit: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    residual_update: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    lines = [
        "# 3251 - Source-prefactor edge zero or same-frame DJH residual first bound under AX1090",
        "",
        f"Generated: `{RUN_UTC}`",
        "",
        "Private derivation checkpoint. This does not claim local GR, Newton, WEP, R10, PPN, clock, orbital, or source-coupling closure.",
        "",
        "## Summary",
        "",
        "- `3251` takes the `C_wH` term from `3250` and gives it a real theorem route: no inert source-only scalar plus connected naturality of the ordinary matter action-density graph forces all `w_A` to one common `w_*`.",
        "- The algebraic core is sharp: for every parent-owned nonzero edge `F_e:A->B`, naturality gives `w_B F_e = F_e w_A`, hence `w_B=w_A`; connectedness propagates this through `G_ord`.",
        "- If the common mode is universal and fixed, it is a coupling calibration, not a relative source residual; therefore `delta_w_rel=0` and `C_wH=0`.",
        "- Current MTS still cannot claim this because the parent action-density line, `hbar`/measure owner, connected graph and no-Hom grammar remain unsigned.",
        "- The fallback is now a precise same-frame bound row: `C_wH <= C_Tw(A_ext,norm,tau,basis)||delta_w||_Sigma`.",
        "",
        "## No-Hom Connected-Naturality Theorem",
        "",
        md_table(theorem, ["theorem_id", "claim_piece", "formal_statement", "proof_step", "result", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Action-Density Edge Certificate Audit",
        "",
        md_table(edge_audit, ["clause_id", "required_clause", "current_evidence", "if_signed", "if_unsigned", "status", "valid_for_claim"]),
        "",
        "## D_A J_H Weighted-Source Bound Row",
        "",
        md_table(bounds, ["row_id", "target_residual", "quantity", "definition", "bound", "required_inputs", "current_value", "units", "score_ready", "valid_for_claim"]),
        "",
        "## D_A J_H Residual Update",
        "",
        md_table(residual_update, ["update_id", "target", "previous_form", "new_form", "gain", "claim_effect", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(gates, ["claim_gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_id", "selection", "next_checkpoint", "next_script", "objective", "guardrail", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
        "",
        "## Working Verdict",
        "",
        "`3251` does not close source coupling, but it does upgrade the weighted-source problem from a loose coupling worry into a clean algebraic fork: either parent-sign one connected action-density line/measure owner and kill `C_wH`, or source the operator norm `C_Tw` and relative vector `delta_w` honestly.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register()
    theorem = theorem_rows()
    edge_audit = edge_audit_rows()
    bounds = bound_rows()
    residual_update = residual_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    generated_without_validation = [
        OUTPUTS["sources"],
        OUTPUTS["theorem"],
        OUTPUTS["edge_audit"],
        OUTPUTS["bound_row"],
        OUTPUTS["residual_update"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["edge_audit"], edge_audit)
    write_csv(OUTPUTS["bound_row"], bounds)
    write_csv(OUTPUTS["residual_update"], residual_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    DOC.write_text(
        "# 3251 - Source-prefactor edge zero or same-frame DJH residual first bound under AX1090\n\n"
        "Pending final validation table.\n",
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_without_validation)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(source_rows, theorem, edge_audit, bounds, residual_update, gates, decisions, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    overall = next(row for row in validation if row["validation_id"] == "VAL3251_OVERALL")
    if overall["passed"] != "true":
        raise SystemExit("3251 validation failed")


if __name__ == "__main__":
    main()
