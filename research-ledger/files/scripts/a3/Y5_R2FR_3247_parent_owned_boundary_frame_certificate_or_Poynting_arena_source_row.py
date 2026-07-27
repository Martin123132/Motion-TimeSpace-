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

CHECKPOINT = "3247"
DOC = ROOT / "3247-Y5-R2FR-parent-owned-boundary-frame-certificate-or-Poynting-arena-source-row-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3247_SOURCE_REGISTER.csv",
    "certificate": OUT / "P8_Y5_R2FR_3247_BOUNDARY_FRAME_CERTIFICATE_ATTEMPT.csv",
    "clauses": OUT / "P8_Y5_R2FR_3247_BOUNDARY_FRAME_CLAUSE_AUDIT.csv",
    "arena": OUT / "P8_Y5_R2FR_3247_POYNTING_ARENA_SOURCE_ROW_NONCLAIM.csv",
    "score_update": OUT / "P8_Y5_R2FR_3247_SCORE_ROW_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3247_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3247_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3247_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3247_VALIDATION.csv",
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
            "SRC3247_3246",
            ROOT / "3246-Y5-R2FR-first-Poynting-Jtot-score-row-or-boundary-frame-source-acquisition-under-AX1090.md",
            "immediate boundary/frame handoff",
            ["boundary_id", "frame_u", "normal_n", "NEXT3246"],
        ),
        (
            "SRC3247_1003_frame",
            ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
            "covariant frame/coframe zero theorem attempt",
            ["quotient_coframe_descent", "e_obs", "partial_frame", "claim"],
        ),
        (
            "SRC3247_1031_terminal_metric",
            ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
            "terminal public metric/coframe proof audit",
            ["terminal public metric", "coframe", "matter_interface", "claim"],
        ),
        (
            "SRC3247_3136_clock",
            ROOT / "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md",
            "observed coframe clock theorem",
            ["observed coframe", "Dq(v)=0", "clock", "parent ownership"],
        ),
        (
            "SRC3247_2600_boundary_clock",
            ROOT / "2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md",
            "boundary clock/tau action audit",
            ["boundary-clock", "tau", "fixed boundary", "claim"],
        ),
        (
            "SRC3247_2991_boundary",
            ROOT / "2991-Y5-R2FR-fixed-boundary-reference-theta-zero-proof-or-epsilon-Bv-source-bound-under-AX1090.md",
            "fixed boundary/reference theta audit",
            ["fixed_surface", "boundary", "B_ref", "epsilon_Bv"],
        ),
        (
            "SRC3247_1039_compact",
            ROOT / "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md",
            "proper compact collar boundary lemma",
            ["proper compact", "source worldtubes", "boundary", "claim"],
        ),
        (
            "SRC3247_10_observer",
            ROOT / "10-observer-map-symplectic-contract.md",
            "observer map/coframe contract",
            ["observer coframe", "PPN", "all matter sectors", "Verdict"],
        ),
        (
            "SRC3247_3234_poynting",
            ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
            "Poynting flux through B,u,n",
            ["T_EM(u,n)", "boundary", "C_flux", "valid_for_claim"],
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


def certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "cert_id": "BFC3247_0_boundary_definition",
            "object": "q-basic local boundary/collar",
            "statement": "Let B be the level set s_B(q(Phi))=0 or support collar chi_B(q(Phi)) chosen before source/readout.",
            "derivation": "For a response vertical e_A with Dq[e_A]=0, D_A s_B(q)=ds_B(Dq[e_A])=0, so the boundary embedding and collar support are fixed to first order.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": "false",
        },
        {
            "cert_id": "BFC3247_1_frame_definition",
            "object": "observed frame u",
            "statement": "Let e_obs=Obs_e(q(Phi)) and u be the unit future timelike leg selected by the observed clock/coframe convention.",
            "derivation": "D_A e_obs=D Obs_e(Dq[e_A])=0, so D_A u=0 if the clock leg is a q-owned functional of e_obs.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": "false",
        },
        {
            "cert_id": "BFC3247_2_normal_definition",
            "object": "boundary normal n",
            "statement": "Let n_mu = grad_mu s_B / sqrt(|g_pub^{ab} grad_a s_B grad_b s_B|) on a non-null q-basic boundary.",
            "derivation": "If g_pub and s_B descend through q, then D_A n=0 except at caustic/null/domain-change points, which must be excluded or bounded.",
            "current_status": "EXACT_CONDITIONAL_WITH_DOMAIN_GUARD",
            "claim_allowed": "false",
        },
        {
            "cert_id": "BFC3247_3_poynting_insertion",
            "object": "Poynting score row",
            "statement": "With B,u,n owned, the first missing score-row fields boundary_id, surface_class, frame_u, normal_n become sourceable.",
            "derivation": "Phi_Poynting[v_A]=int_B w_A T_EM(u,n)dSigma is then evaluated on a predeclared arena, not a post-hoc surface.",
            "current_status": "CONDITIONAL_SCORE_ROW_INTERFACE",
            "claim_allowed": "false",
        },
        {
            "cert_id": "BFC3247_4_current_mts_verdict",
            "object": "current MTS boundary/frame",
            "statement": "The theorem is clean, but current MTS has not parent-signed the actual q-basic boundary function, support collar, observed frame selector, or no-shadow-frame matter functor.",
            "derivation": "1003/1031/2600/2991 retain the necessary frame, terminal metric, tau, and fixed-surface clauses as nonclaim.",
            "current_status": "NOT_PARENT_SIGNED_RETAIN_ARENA_ROW",
            "claim_allowed": "false",
        },
    ]


def clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "CLA3247_0_q_boundary",
            "required_clause": "boundary/collar/worldtube is q-basic and chosen before source/readout",
            "status": "MISSING_PARENT_BOUNDARY_FUNCTION",
            "if_missing": "boundary_id and surface_class remain missing",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CLA3247_1_coframe",
            "required_clause": "observed coframe descends from q and all ordinary matter/readout uses it",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_missing": "frame_u remains a frame-profile residual",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CLA3247_2_normal",
            "required_clause": "boundary is non-null, oriented and has a q-owned normal n",
            "status": "DOMAIN_GUARD_NOT_SOURCED",
            "if_missing": "normal_n and C_flux cannot be computed",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CLA3247_3_tau_support",
            "required_clause": "same tau/coframe/support is used for clock, source, charge, orbit and boundary",
            "status": "2600_UNSIGNED",
            "if_missing": "tau/support mismatch enters epsilon_frame_leak and epsilon_Bv",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CLA3247_4_source_worldtube",
            "required_clause": "source worldtube, if used, is declared by the parent arena rather than chosen after flux",
            "status": "SOURCE_WORLDTUBE_NOT_OWNED",
            "if_missing": "finite Poynting row remains arena-only nonclaim",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CLA3247_5_compact_proper",
            "required_clause": "proper compact collar sublemma applies only to representative/gauge transformations",
            "status": "NARROW_ZERO_ONLY",
            "if_missing": "cannot use compact-proper result to erase physical source boundary flux",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CLA3247_6_stress_descent",
            "required_clause": "T_EM is standard/parent-derived in the same observed frame",
            "status": "CONDITIONAL_EM_STRESS_NOT_PARENT_DERIVED",
            "if_missing": "Poynting row is a target stress channel, not an MTS Maxwell claim",
            "valid_for_claim": "false",
        },
    ]


def arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_row_id": "ARENA3247_0_qbasic_local_collar",
            "boundary_id": "MISSING_qbasic_sB_or_chiB",
            "surface_class": "candidate_qbasic_compact_local_collar",
            "frame_u": "u=e_obs_clock_leg(q)",
            "normal_n": "n=normalize(grad s_B(q))",
            "zero_or_bound_route": "conditional zero if no-flux support; otherwise finite Poynting bound",
            "missing_inputs": "s_B_or_chi_B_source_path;non_null_guard;orientation;coframe_parent_signature;stress_descent;flux_regime",
            "status": "BEST_DERIVATION_ROUTE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "arena_row_id": "ARENA3247_1_source_worldtube",
            "boundary_id": "MISSING_source_worldtube_id",
            "surface_class": "source_worldtube_or_material_support_boundary",
            "frame_u": "MISSING_source_frame_or_observed_frame_lock",
            "normal_n": "MISSING_worldtube_normal",
            "zero_or_bound_route": "finite bound required unless physical no-flux certificate is sourced",
            "missing_inputs": "worldtube_support;material_source_map;u_n;T_EM_flux_norm;corner_terms",
            "status": "LIVE_FINITE_ROUTE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "arena_row_id": "ARENA3247_2_proper_compact_sublemma",
            "boundary_id": "proper_compact_representative_support_only",
            "surface_class": "open_collar_where_generator_jets_vanish",
            "frame_u": "not_a_physical_source_frame",
            "normal_n": "not_a_physical_source_normal",
            "zero_or_bound_route": "boundary charge terms vanish for compact representative transformations",
            "missing_inputs": "does_not_apply_to_source_worldtube_or_physical_flux",
            "status": "NARROW_ZERO_NOT_SCORE_ROW",
            "valid_for_claim": "false",
        },
    ]


def score_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "SCU3247_0_first_score_row_update",
            "score_id": "PJS3246_0_first_component",
            "field_updates_available": "conditional formulas for boundary_id,surface_class,frame_u,normal_n",
            "fields_still_missing": "actual s_B/chi_B source path;non-null normal guard;orientation;flux regime;C_flux/C_coll;flux norms;e_A norms;units",
            "computed_J_Poynting_bound": "NOT_COMPUTED",
            "reason": "boundary/frame ownership theorem is conditional, not parent-signed with concrete arena data",
            "valid_for_claim": "false",
        }
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3247_0_conditional_certificate",
            "claim": "q-basic boundary/frame certificate theorem exists",
            "condition_passed": "true",
            "status": "exact conditional chain-rule theorem written",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3247_1_current_boundary",
            "claim": "current MTS has parent-owned boundary_id/surface_class",
            "condition_passed": "false",
            "status": "q-basic s_B/chi_B or source worldtube not parent-signed",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3247_2_current_frame",
            "claim": "current MTS has parent-owned frame_u/normal_n for the score row",
            "condition_passed": "false",
            "status": "observed coframe route remains conditional and normal/domain guard missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3247_3_poynting_score",
            "claim": "Poynting Jtot score row is numeric/source-backed",
            "condition_passed": "false",
            "status": "arena row staged but no concrete flux constants/norms",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3247_4_local_GR",
            "claim": "local GR/Newton/PPN reduction",
            "condition_passed": "false",
            "status": "no numeric qloc/amplitude residual",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3247_0_theorem",
            "decision": "Keep the q-basic boundary/frame theorem as the clean derivation route.",
            "because": "It fixes B,u,n by chain rule instead of choosing a surface after seeing the flux.",
            "next_action": "Source or derive the actual q-basic local collar function s_B/chi_B.",
        },
        {
            "decision_id": "DEC3247_1_no_promotion",
            "decision": "Do not promote the first Poynting score row yet.",
            "because": "The actual boundary/support object and observed frame selector are still unsigned.",
            "next_action": "Use the arena source rows as the fill targets.",
        },
        {
            "decision_id": "DEC3247_2_compact_guard",
            "decision": "Do not use the compact-proper boundary lemma as a physical flux eraser.",
            "because": "1039 only silences representative/gauge boundary charges, not source worldtube Poynting flux.",
            "next_action": "Treat physical source boundaries as finite-bound arenas unless no-flux is sourced.",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3247_0_3248",
            "priority": "selected_primary",
            "next_doc": "3248-Y5-R2FR-qbasic-local-collar-source-or-first-Poynting-arena-row-fill-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3248_qbasic_local_collar_source_or_first_Poynting_arena_row_fill.py",
            "objective": "Try to source or derive the concrete q-basic local collar function s_B/chi_B, orientation/non-null normal guard, and observed coframe selector for ARENA3247_0; if not available, choose the source-worldtube finite-bound row explicitly as nonclaim.",
            "exclude": "do not choose boundary after seeing flux; do not use compact-proper gauge lemma for physical source flux; do not edit formalization-workbench",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources_exist = all(row["exists"] == "true" for row in source_rows)
    sources_hit = all(row["evidence_hits"] not in {"MISSING_SOURCE", "NO_MATCH"} for row in source_rows)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    outputs_under_post = all(ROOT in path.parents for path in generated_csvs) and ROOT in DOC.parents
    formalization_3247 = list(FW.rglob("*3247*")) if FW.exists() else []
    formalization_clean = len(formalization_3247) == 0
    conditional_not_claim = any(
        row["claim_gate_id"] == "CG3247_0_conditional_certificate"
        and row["condition_passed"] == "true"
        and row["claim_allowed"] == "false"
        for row in gate_rows()
    )
    physics_blocked = all(
        row["claim_allowed"] == "false"
        for row in gate_rows()
        if row["claim_gate_id"] != "CG3247_0_conditional_certificate"
    )
    arena_nonclaim = all(row["valid_for_claim"] == "false" for row in arena_rows())
    missing_boundary_retained = any("MISSING" in row["missing_inputs"] or row["boundary_id"].startswith("MISSING") for row in arena_rows())
    next_written = bool(next_rows())
    checks = [
        ("VAL3247_0_sources_exist", sources_exist, "all cited source paths exist", str(sources_exist)),
        ("VAL3247_1_source_hits", sources_hit, "source evidence hits are present", str(sources_hit)),
        ("VAL3247_2_csvs_parse", csvs_parse, "all generated CSV files parse", str(csvs_parse)),
        ("VAL3247_3_outputs_under_post_checkpoint", outputs_under_post, "all outputs are under post-checkpoint-work", str(outputs_under_post)),
        ("VAL3247_4_formalization_clean", formalization_clean, "no 3247 outputs in formalization-workbench", f"formalization_3247_count={len(formalization_3247)}"),
        ("VAL3247_5_conditional_not_claim", conditional_not_claim, "boundary/frame theorem not promoted to current physics claim", str(conditional_not_claim)),
        ("VAL3247_6_physics_claims_blocked", physics_blocked, "boundary/frame/score/local-GR claims remain blocked", str(physics_blocked)),
        ("VAL3247_7_arena_nonclaim", arena_nonclaim, "arena source rows remain nonclaim", str(arena_nonclaim)),
        ("VAL3247_8_missing_boundary_retained", missing_boundary_retained, "missing concrete boundary/source fields remain visible", str(missing_boundary_retained)),
        ("VAL3247_9_next_written", next_written, "3248 next target written", str(next_written)),
        ("VAL3247_10_doc_written", DOC.exists(), "3247 markdown checkpoint exists", str(DOC.exists())),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": bool_str(passed),
            "requirement": requirement,
            "evidence": evidence_text,
        }
        for validation_id, passed, requirement, evidence_text in checks
    ]
    rows.append(
        {
            "validation_id": "VAL3247_OVERALL",
            "passed": bool_str(all(row["passed"] == "true" for row in rows)),
            "requirement": "3247 validation overall",
            "evidence": "all required validation rows passed",
        }
    )
    return rows


def build_doc(
    source_rows: list[dict[str, Any]],
    certificate: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    score_update: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3247 - Parent-Owned Boundary/Frame Certificate or Poynting Arena Source Row under AX1090",
            f"Generated: `{RUN_UTC}`",
            "Status: `Y5_R2FR_3247_qbasic_boundary_frame_chain_rule_certificate_written_actual_arena_unsigned_Poynting_rows_nonclaim`",
            "Claim ceiling: `conditional_boundary_frame_theorem_only_no_current_boundary_id_no_frame_un_claim_no_numeric_Poynting_score_no_local_GR_claim`",
            "## Summary",
            "- `3247` derives the clean boundary/frame theorem: if the local boundary/collar is q-basic, `B={s_B(q)=0}` or `chi_B(q)`, and `e_obs=Obs_e(q)`, then every vertical response direction with `Dq[e_A]=0` fixes `B`, `u`, and `n` by the chain rule.",
            "- This is the right way to stop post-hoc surface choice: `u` and `n` must come from the public observed coframe and q-basic boundary before any Poynting flux is read.",
            "- Current MTS still does not get a numeric Poynting row because the actual `s_B/chi_B`, non-null normal guard, orientation/collar support, and observed-frame selector are not parent-signed.",
            "- The proper-compact boundary lemma remains useful but narrow: it kills representative/gauge edge terms, not physical source-worldtube Poynting flux.",
            "- The first arena source rows are now explicit: q-basic local collar as the best derivation route, source worldtube as the live finite-bound route, and compact-proper as a non-score zero hygiene lemma.",
            "## Boundary/Frame Certificate Attempt",
            md_table(certificate, ["cert_id", "object", "statement", "derivation", "current_status", "claim_allowed"]),
            "## Boundary/Frame Clause Audit",
            md_table(clauses, ["clause_id", "required_clause", "status", "if_missing", "valid_for_claim"]),
            "## Poynting Arena Source Rows",
            md_table(arena, ["arena_row_id", "boundary_id", "surface_class", "frame_u", "normal_n", "zero_or_bound_route", "missing_inputs", "status", "valid_for_claim"]),
            "## Score Row Update",
            md_table(score_update, ["update_id", "score_id", "field_updates_available", "fields_still_missing", "computed_J_Poynting_bound", "reason", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Next Target",
            md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude", "valid_for_claim"]),
            "## Source Register",
            md_table(source_rows, ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
            "## Generated Evidence",
            "\n".join(f"- `{path}`" for path in OUTPUTS.values()),
        ]
    )


def main() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    DOC.parent.mkdir(parents=True, exist_ok=True)

    source_rows = source_register()
    certificate = certificate_rows()
    clauses = clause_rows()
    arena = arena_rows()
    score_update = score_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["certificate"], certificate)
    write_csv(OUTPUTS["clauses"], clauses)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["score_update"], score_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    generated_csvs = [
        OUTPUTS["sources"],
        OUTPUTS["certificate"],
        OUTPUTS["clauses"],
        OUTPUTS["arena"],
        OUTPUTS["score_update"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, certificate, clauses, arena, score_update, gates, decisions, next_target, validation),
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, certificate, clauses, arena, score_update, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    failed = [row for row in validation if row["passed"] != "true"]
    if failed:
        raise SystemExit(f"3247 validation failed: {failed}")


if __name__ == "__main__":
    main()
