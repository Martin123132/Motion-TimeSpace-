from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3346-Y5-R2FR-parent-action-normal-form-inventory-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3346_0_3345_doc",
        "path": ROOT / "3345-Y5-R2FR-ordinary-coefficient-domain-parent-signature-under-AX1090.md",
        "role": "3345 parent-domain theorem handoff",
    },
    {
        "source_id": "SRC3346_1_3345_signature",
        "path": OUT / "P8_Y5_R2FR_3345_ORDINARY_COEFFICIENT_DOMAIN_SIGNATURE.csv",
        "role": "3345 ordinary coefficient-domain signature",
    },
    {
        "source_id": "SRC3346_2_3345_evidence",
        "path": OUT / "P8_Y5_R2FR_3345_PARENT_SIGNATURE_EVIDENCE_SCORE.csv",
        "role": "3345 parent signature evidence score",
    },
    {
        "source_id": "SRC3346_3_3345_countermodels",
        "path": OUT / "P8_Y5_R2FR_3345_SURVIVING_COUNTERMODEL_MATRIX.csv",
        "role": "surviving countermodels if parent domain unsigned",
    },
    {
        "source_id": "SRC3346_4_3345_residuals",
        "path": OUT / "P8_Y5_R2FR_3345_RESIDUAL_INTERFACE_IF_UNSIGNED.csv",
        "role": "residual interface if parent signature remains unsigned",
    },
    {
        "source_id": "SRC3346_5_3340_clause",
        "path": OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv",
        "role": "candidate parent Hilbert source clause",
    },
    {
        "source_id": "SRC3346_6_3340_evidence",
        "path": OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv",
        "role": "current parent Hilbert clause evidence",
    },
    {
        "source_id": "SRC3346_7_3339_requirements",
        "path": OUT / "P8_Y5_R2FR_3339_PARENT_SIGNATURE_REQUIREMENTS.csv",
        "role": "source-coupling parent signature requirements",
    },
    {
        "source_id": "SRC3346_8_2624_domain",
        "path": OUT / "P8_Y5_READOUT_SCHEMA_GATE_2624_PARENT_DOMAIN_SIGNATURE_AUDIT.csv",
        "role": "parent domain/readout signature audit",
    },
    {
        "source_id": "SRC3346_9_2624_readout",
        "path": OUT / "P8_Y5_READOUT_SCHEMA_GATE_2624_READOUT_SCHEMA_THEOREM_ATTEMPT.csv",
        "role": "variation-before-readout theorem",
    },
    {
        "source_id": "SRC3346_10_2643_descent",
        "path": OUT / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv",
        "role": "common matter descent parent signature gate",
    },
    {
        "source_id": "SRC3346_11_2659_domain",
        "path": OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
        "role": "ordinary coefficient domain theorem",
    },
    {
        "source_id": "SRC3346_12_2617_single_source",
        "path": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv",
        "role": "single source-map identity theorem",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3346_SOURCE_REGISTER.csv",
    "normal_form": OUT / "P8_Y5_R2FR_3346_PARENT_ACTION_NORMAL_FORM.csv",
    "allowed_args": OUT / "P8_Y5_R2FR_3346_ALLOWED_ARGUMENT_INVENTORY.csv",
    "forbidden_args": OUT / "P8_Y5_R2FR_3346_FORBIDDEN_ARGUMENT_INVENTORY.csv",
    "scorecard": OUT / "P8_Y5_R2FR_3346_ARGUMENT_SCORECARD.csv",
    "closure_attempt": OUT / "P8_Y5_R2FR_3346_CLOSURE_CERTIFICATE_ATTEMPT.csv",
    "surviving_residuals": OUT / "P8_Y5_R2FR_3346_SURVIVING_RESIDUALS_IF_UNSIGNED.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3346_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3346_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3346_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3346_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "form_id": "NF3346_0_candidate_parent_action",
            "action_piece": "candidate local parent normal form",
            "mathematical_form": "S_parent = S_geom[Phi;q] + S_matter[Psi_A,e_obs(q(Phi)),A_Q(q(Phi)),theta_A] + S_EM[e_obs(q(Phi)),A_Q,lambda_0] + S_boundary[B;Phi,Psi,A_Q]",
            "allowed_arguments": "Phi via q; e_obs/g_obs/omega; Psi_A; A_Q/J_Q; fixed theta_A; fixed lambda_0; boundary data B if classified",
            "forbidden_arguments": "I_hid hidden coefficient maps; w_A source weights; F_shadow/P_material; P_read/R_read; hidden frames g_A; varied S_red",
            "status": "NORMAL_FORM_CANDIDATE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "form_id": "NF3346_1_variation_order",
            "action_piece": "variation before readout",
            "mathematical_form": "Conf_parent --delta S_parent=0--> Sol(S_parent) --R_read--> Obs",
            "allowed_arguments": "readout map after solving",
            "forbidden_arguments": "P_read/R_read as Euler-Lagrange arguments of S_parent",
            "status": "EXACT_SCHEMA_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "form_id": "NF3346_2_source_owner",
            "action_piece": "ordinary active source owner",
            "mathematical_form": "T_active := T_H := (-2/sqrt(-g_obs)) delta(S_matter+S_EM)/delta g_obs",
            "allowed_arguments": "total Hilbert stress/current from one varied action",
            "forbidden_arguments": "post-variation T_source=sum_A kappa_A T_A or P_material(T_H)",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def allowed_argument_rows() -> list[dict[str, Any]]:
    return [
        {
            "arg_id": "ARG3346_A0_parent_fields",
            "argument": "Phi_parent",
            "where_allowed": "S_geom and q(Phi)",
            "typing_rule": "parent fields may affect ordinary matter only through q-visible objects unless explicitly classified as geometry/residual sectors",
            "closes_if_signed": "defines ker(Dq) and hidden vertical directions",
            "source_path": str(OUT / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv"),
            "status": "SKETCH_EXISTS_NOT_CLOSED",
            "valid_for_claim": "false",
        },
        {
            "arg_id": "ARG3346_A1_q_visible_geometry",
            "argument": "e_obs(q(Phi)), g_obs(q(Phi)), omega[e_obs]",
            "where_allowed": "S_matter, S_EM, Hilbert variation",
            "typing_rule": "ordinary matter and EM see one observed metric/coframe",
            "closes_if_signed": "hidden frame/c_g/b_dis ordinary matter slots",
            "source_path": str(OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv"),
            "status": "CONTRACT_PRESENT_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "arg_id": "ARG3346_A2_matter_fields",
            "argument": "Psi_A",
            "where_allowed": "S_matter only",
            "typing_rule": "matter fields enter dynamics and stress through the same functional",
            "closes_if_signed": "source-shadow functional not separate from ordinary matter dynamics",
            "source_path": str(OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv"),
            "status": "CONTRACT_WRITTEN_NOT_PARENT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "arg_id": "ARG3346_A3_gauge_current_owner",
            "argument": "A_Q and J_Q from fixed representation/Noether current",
            "where_allowed": "S_matter interaction and S_EM",
            "typing_rule": "current and charge lattice are action-owned, not source/test knobs",
            "closes_if_signed": "delta_J and source/test charge normalization drift",
            "source_path": str(OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv"),
            "status": "CONDITIONAL_CURRENT_OWNER_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "arg_id": "ARG3346_A4_fixed_constants",
            "argument": "theta_A, representation labels, masses, charges, lambda_0, calibration constants",
            "where_allowed": "A_fixed only",
            "typing_rule": "fixed data have L_v theta=0 and are not hidden coefficient functions",
            "closes_if_signed": "b_alpha constant drift, hidden material markers, species source weights",
            "source_path": str(OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"),
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "arg_id": "ARG3346_A5_boundary_terms",
            "argument": "S_boundary and improvement data B",
            "where_allowed": "boundary/improvement sector only",
            "typing_rule": "boundary terms are allowed only if exact, zero-flux, or carried as finite residuals",
            "closes_if_signed": "epsilon_boundary/contact readout leakage",
            "source_path": str(OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv"),
            "status": "ROUTE_DEFINED_NOT_PARENT_OR_NUMERIC_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def forbidden_argument_rows() -> list[dict[str, Any]]:
    return [
        {
            "arg_id": "ARG3346_F0_hidden_coefficient",
            "forbidden_argument": "f_X(I_hid)F_Q^2 or hidden-visible coefficient maps",
            "why_forbidden": "would make ordinary coefficients depend on hidden vertical variables outside q^*A_Q + A_fixed",
            "residual_if_present": "epsilon_coeff_domain; b_alpha; epsilon_EM",
            "source_path": str(OUT / "P8_Y5_R2FR_3345_SURVIVING_COUNTERMODEL_MATRIX.csv"),
            "status": "FORBID_IF_PARENT_DOMAIN_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "arg_id": "ARG3346_F1_source_weight",
            "forbidden_argument": "w_A(X), kappa_A(I_hid), species/source-only prefactors",
            "why_forbidden": "post-variation or source-only weights create WEP/source-composition residuals without changing ordinary dynamics",
            "residual_if_present": "epsilon_source_shadow; eta_species",
            "source_path": str(OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_PARENT_SIGNATURE_REQUIREMENTS.csv"),
            "status": "FORBID_IF_SINGLE_SOURCE_OWNER_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "arg_id": "ARG3346_F2_source_projector",
            "forbidden_argument": "F_shadow(T_H,labels) or P_material(T_H)",
            "why_forbidden": "an independent source-map argument reintroduces labels after variation",
            "residual_if_present": "epsilon_source_shadow",
            "source_path": str(OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv"),
            "status": "FORBID_OR_CLASSIFY_AS_ACTION_BOUNDARY_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "arg_id": "ARG3346_F3_hidden_frame",
            "forbidden_argument": "g_A=A_A(X)^2 g_obs or disformal labelled matter frame",
            "why_forbidden": "ordinary matter would not be minimally coupled to one public metric/coframe",
            "residual_if_present": "c_g; b_dis; PPN/WEP/clock residuals",
            "source_path": str(OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"),
            "status": "FORBID_IF_OBSERVED_GEOMETRY_DESCENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "arg_id": "ARG3346_F4_readout_argument",
            "forbidden_argument": "P_read, R_read, fitted masks, active readout blocks inside S_parent",
            "why_forbidden": "readout happens after solving; if varied it is a reduced EFT branch, not theorem-zero",
            "residual_if_present": "epsilon_readout_backreaction",
            "source_path": str(OUT / "P8_Y5_READOUT_SCHEMA_GATE_2624_READOUT_SCHEMA_THEOREM_ATTEMPT.csv"),
            "status": "FORBID_OR_DEMOTE_S_RED",
            "valid_for_claim": "false",
        },
        {
            "arg_id": "ARG3346_F5_uninventoried_decoupled_block",
            "forbidden_argument": "unlisted conserved nonordinary source block T_D in a local ordinary source arena",
            "why_forbidden": "would alter measured G/PPN/WEP without being part of ordinary Hilbert source inventory",
            "residual_if_present": "epsilon_decoupled_block",
            "source_path": str(OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv"),
            "status": "FORBID_UNLESS_ARENA_INVENTORIED_AND_BOUNDED",
            "valid_for_claim": "false",
        },
    ]


def scorecard_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in allowed_argument_rows():
        rows.append(
            {
                "score_id": f"SCORE_{row['arg_id']}",
                "argument_type": "allowed",
                "argument": row["argument"],
                "source_path": row["source_path"],
                "source_exists": bool_str(Path(row["source_path"]).exists()),
                "evidence_status": row["status"],
                "parent_signed": "false",
                "blocks_if_unsigned": row["closes_if_signed"],
                "valid_for_claim": "false",
            }
        )
    for row in forbidden_argument_rows():
        rows.append(
            {
                "score_id": f"SCORE_{row['arg_id']}",
                "argument_type": "forbidden",
                "argument": row["forbidden_argument"],
                "source_path": row["source_path"],
                "source_exists": bool_str(Path(row["source_path"]).exists()),
                "evidence_status": row["status"],
                "parent_signed": "false",
                "blocks_if_unsigned": row["residual_if_present"],
                "valid_for_claim": "false",
            }
        )
    return rows


def closure_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_id": "CLOSE3346_0_domain",
            "attempted_closure": "Args(S_parent) subset equals q-visible fields plus fixed constants plus classified boundary/improvement terms",
            "result": "NOT_CLOSED",
            "reason": "corpus has candidate normal form and exact typed theorem but not closed field-by-field parent argument certificate",
            "promotion_requirement": "source-backed inventory proving every hidden/source/readout slot is absent or classified",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "CLOSE3346_1_source",
            "attempted_closure": "ordinary active source equals total Hilbert stress before source labels are exposed",
            "result": "NOT_CLOSED",
            "reason": "identity source-map theorem is conditional; source-shadow/projector countermodel survives",
            "promotion_requirement": "parent action normal form with no F_shadow/P_material argument or finite epsilon_source_shadow bound",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "CLOSE3346_2_readout",
            "attempted_closure": "readout/projector excluded from parent variation",
            "result": "NOT_CLOSED",
            "reason": "readout schema theorem is clean, but Args(S_parent) exclusion is not a closed parent certificate",
            "promotion_requirement": "closed parent domain list excluding P_read/R_read and demoting all S_red variations",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "CLOSE3346_3_boundary_inventory",
            "attempted_closure": "boundary/improvement and decoupled blocks are silent or inventoried",
            "result": "NOT_CLOSED",
            "reason": "boundary/contact/decoupled sectors require explicit arena inventory or finite bounds",
            "promotion_requirement": "zero-flux/improvement theorem or source-backed residual rows",
            "valid_for_claim": "false",
        },
    ]


def surviving_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "SURV3346_0_epsilon_source_shadow",
            "symbol": "epsilon_source_shadow",
            "definition": "post-variation source-map/projector leakage",
            "why_next": "highest-pressure countermodel for eta_species and measured-G calibration",
            "next_route": "prove identity source map or build finite source-shadow/projector bound",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SURV3346_1_epsilon_coeff_domain",
            "symbol": "epsilon_coeff_domain",
            "definition": "hidden coefficient maps outside q-visible/fixed constants",
            "why_next": "controls b_alpha, mass/clock/material markers, and hidden frames",
            "next_route": "field-by-field no-hidden-visible Hom certificate or coefficient derivative bounds",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SURV3346_2_epsilon_readout_backreaction",
            "symbol": "epsilon_readout_backreaction",
            "definition": "varied reduced/readout projector functional",
            "why_next": "prevents readout closure from being smuggled as theorem-zero",
            "next_route": "closed readout exclusion or explicit S_red residual vector",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "SURV3346_3_epsilon_decoupled_block",
            "symbol": "epsilon_decoupled_block",
            "definition": "uninventoried conserved nonordinary source sector",
            "why_next": "would alter source normalization if present in local ordinary arenas",
            "next_route": "arena inventory exclusion or density/coupling bound",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3346_0_normal_form_written",
            "claim": "candidate parent action normal form is explicit",
            "passed": "true",
            "reason": "normal form lists S_geom, S_matter, S_EM, boundary, source owner, and readout order",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3346_1_allowed_inventory",
            "claim": "allowed argument inventory covers q-visible fields, matter, EM/current, constants, and boundary terms",
            "passed": "true",
            "reason": "allowed inventory has six typed rows",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3346_2_forbidden_inventory",
            "claim": "forbidden argument inventory covers hidden coefficients, source weights, source projectors, hidden frames, readout arguments, and decoupled blocks",
            "passed": "true",
            "reason": "forbidden inventory has six typed rows",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3346_3_parent_signed",
            "claim": "Args(S_parent) certificate is closed for current MTS",
            "passed": "false",
            "reason": "every high-pressure item remains contract/conditional/open rather than source-backed parent-signed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3346_4_local_GR_claim",
            "claim": "local-GR source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "normal form is now explicit but not parent-signed; surviving residual rows remain",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3346_0",
            "question": "Did 3346 close the parent action domain?",
            "answer": "no",
            "reason": "it made the normal-form inventory explicit, but the corpus still lacks field-by-field parent ownership proof",
            "next_action": "attack epsilon_source_shadow first, because it is the strongest source-coupling bypass",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3346_1",
            "question": "Did 3346 move the work forward?",
            "answer": "yes",
            "reason": "allowed and forbidden arguments are now machine-readable, scoreable, and tied to residual interfaces",
            "next_action": "use the inventory as the checklist for future parent action derivation or finite bounds",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3347-Y5-R2FR-source-shadow-projector-bound-or-zero-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3347_source_shadow_projector_bound_or_zero.py",
            "objective": "prove the identity source-map/no-projector theorem from the 3346 Args(S_parent) inventory, or stage a finite epsilon_source_shadow projector/source-composition bound row",
            "why_next": "source-shadow/projector leakage is the highest-pressure countermodel for eta_species and measured-G calibration after the normal-form inventory failed to close",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3347b-Y5-R2FR-coefficient-domain-field-by-field-certificate.md",
            "target_script": "scripts/Y5_R2FR_3347b_coefficient_domain_field_by_field_certificate.py",
            "objective": "turn epsilon_coeff_domain into a field-by-field certificate for Z_Q, masses, charges, clocks, material labels, and hidden frames",
            "why_next": "needed to convert the exact A_ord theorem into parent-owned no-hidden-visible coefficient silence",
            "valid_for_claim": "false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]], limit: int = 20) -> str:
    if not rows:
        return "_No rows._"
    fieldnames: list[str] = []
    for row in rows[:limit]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows[:limit]:
        values = [compact(row.get(key, ""), 260).replace("|", "\\|") for key in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    if len(rows) > limit:
        lines.append(f"\n_Truncated in markdown: showing {limit} of {len(rows)} rows._")
    return "\n".join(lines)


def render_doc() -> str:
    return "\n\n".join(
        [
            "# 3346 — Parent Action Normal-Form Inventory Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- This checkpoint writes the explicit `Args(S_parent)` normal-form inventory demanded by 3345.\n"
            "- The candidate action keeps ordinary matter/EM on q-visible geometry plus fixed constants, and forbids hidden coefficients, source projectors, hidden frames, and readout arguments.\n"
            "- The inventory is now machine-readable and scoreable, but not parent-signed: the current corpus still has contracts and conditional theorems, not a closed field-by-field parent certificate.\n"
            "- The highest-pressure survivor is `epsilon_source_shadow`, because it can reintroduce `eta_species` and source-normalization drift after variation.",
            "## Candidate Parent Normal Form\n" + markdown_table(normal_form_rows()),
            "## Allowed Argument Inventory\n" + markdown_table(allowed_argument_rows()),
            "## Forbidden Argument Inventory\n" + markdown_table(forbidden_argument_rows()),
            "## Argument Scorecard\n" + markdown_table(scorecard_rows()),
            "## Closure Certificate Attempt\n" + markdown_table(closure_attempt_rows()),
            "## Surviving Residuals If Unsigned\n" + markdown_table(surviving_residual_rows()),
            "## Promotion Gates\n" + markdown_table(promotion_gate_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_rows()
    allowed = allowed_argument_rows()
    forbidden = forbidden_argument_rows()
    scorecard = scorecard_rows()
    closure = closure_attempt_rows()
    residuals = surviving_residual_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3346_0_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3346_1_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3346_2_outputs_parse",
            "check": "all 3346 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3346_3_allowed_inventory",
            "check": "allowed inventory covers parent fields, q-visible geometry, matter, gauge/current, fixed constants, and boundary",
            "passed": {row["arg_id"] for row in allowed}
            == {"ARG3346_A0_parent_fields", "ARG3346_A1_q_visible_geometry", "ARG3346_A2_matter_fields", "ARG3346_A3_gauge_current_owner", "ARG3346_A4_fixed_constants", "ARG3346_A5_boundary_terms"},
            "detail": "",
        },
        {
            "check_id": "VAL3346_4_forbidden_inventory",
            "check": "forbidden inventory covers hidden coefficients, source weights, source projectors, hidden frames, readout, and decoupled blocks",
            "passed": {row["arg_id"] for row in forbidden}
            == {"ARG3346_F0_hidden_coefficient", "ARG3346_F1_source_weight", "ARG3346_F2_source_projector", "ARG3346_F3_hidden_frame", "ARG3346_F4_readout_argument", "ARG3346_F5_uninventoried_decoupled_block"},
            "detail": "",
        },
        {
            "check_id": "VAL3346_5_scorecard_paths",
            "check": "every scorecard source path exists",
            "passed": all(row["source_exists"] == "true" for row in scorecard),
            "detail": "",
        },
        {
            "check_id": "VAL3346_6_closure_not_overclaimed",
            "check": "closure attempt explicitly remains not closed",
            "passed": all(row["result"] == "NOT_CLOSED" for row in closure),
            "detail": "",
        },
        {
            "check_id": "VAL3346_7_residuals_survive",
            "check": "surviving residuals include source shadow, coefficient domain, readout, and decoupled block",
            "passed": {row["symbol"] for row in residuals}
            == {"epsilon_source_shadow", "epsilon_coeff_domain", "epsilon_readout_backreaction", "epsilon_decoupled_block"},
            "detail": "",
        },
        {
            "check_id": "VAL3346_8_no_claim",
            "check": "parent-signed and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3346_3_parent_signed", "GATE3346_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3346_9_next_target",
            "check": "next target attacks epsilon_source_shadow and coefficient-domain certificate",
            "passed": any("epsilon_source_shadow" in row["objective"] for row in next_target_rows())
            and any("epsilon_coeff_domain" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3346_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3346_11_overall",
            "check": "3346 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_rows())
    write_csv(OUTPUTS["normal_form"], normal_form_rows())
    write_csv(OUTPUTS["allowed_args"], allowed_argument_rows())
    write_csv(OUTPUTS["forbidden_args"], forbidden_argument_rows())
    write_csv(OUTPUTS["scorecard"], scorecard_rows())
    write_csv(OUTPUTS["closure_attempt"], closure_attempt_rows())
    write_csv(OUTPUTS["surviving_residuals"], surviving_residual_rows())
    write_csv(OUTPUTS["promotion_gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
