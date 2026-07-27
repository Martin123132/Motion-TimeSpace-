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

CHECKPOINT = "3248"
DOC = ROOT / "3248-Y5-R2FR-qbasic-local-collar-source-or-first-Poynting-arena-row-fill-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3248_SOURCE_REGISTER.csv",
    "collar": OUT / "P8_Y5_R2FR_3248_QBASIC_COLLAR_CONSTRUCTION_ATTEMPT.csv",
    "theorem": OUT / "P8_Y5_R2FR_3248_COLLAR_QBASIC_CHAIN_RULE_THEOREM.csv",
    "arena": OUT / "P8_Y5_R2FR_3248_FIRST_POYNTING_ARENA_ROW_PARTIAL_FILL.csv",
    "missing": OUT / "P8_Y5_R2FR_3248_COLLAR_MISSING_SIGNATURES.csv",
    "score_update": OUT / "P8_Y5_R2FR_3248_SCORE_ROW_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3248_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3248_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3248_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3248_VALIDATION.csv",
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
            "SRC3248_3247",
            ROOT / "3247-Y5-R2FR-parent-owned-boundary-frame-certificate-or-Poynting-arena-source-row-under-AX1090.md",
            "immediate q-basic collar handoff",
            ["s_B", "chi_B", "ARENA3247_0", "NEXT3247"],
        ),
        (
            "SRC3248_1016_selector",
            ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            "parent worldtube support selector contract",
            ["W_source", "closure(supp J_H", "support_selector", "claim"],
        ),
        (
            "SRC3248_1015_same_object",
            ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
            "same compact Hilbert source worldtube lemma",
            ["W_source", "worldtube", "source measure", "claim"],
        ),
        (
            "SRC3248_1150_glue",
            ROOT / "1150-Y5-R10-Hilbert-worldtube-glue-or-PiM-equality-commutator-first-row.md",
            "Hilbert-worldtube glue status",
            ["W_source", "Hilbert", "worldtube", "not derived"],
        ),
        (
            "SRC3248_worldtube_clauses",
            OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            "worldtube/exterior annulus clauses",
            ["W504_0_worldtube_setup", "exterior", "S1", "S2"],
        ),
        (
            "SRC3248_worldtube_measure",
            OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
            "worldtube source measure theorem",
            ["T510_1_worldtube_source_measure", "M_source", "H_tau", "MTS_transfer"],
        ),
        (
            "SRC3248_hwg_certificate",
            OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
            "Hilbert worldtube certificate gaps",
            ["HWG535_0_worldtube_fixed_before_readout", "missing_certificate"],
        ),
        (
            "SRC3248_hsm_contract",
            OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            "Hamiltonian source measure contract",
            ["HSM541_2_observed_worldtube_source", "W_source=supp", "not_derived"],
        ),
        (
            "SRC3248_3136_coframe",
            ROOT / "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md",
            "observed coframe/clock selector",
            ["e_obs", "Dq(v)=0", "clock", "parent ownership"],
        ),
        (
            "SRC3248_3234_poynting",
            ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
            "Poynting flux formula needing B,u,n",
            ["T_EM(u,n)", "C_flux", "C_coll", "valid_for_claim"],
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


def collar_rows() -> list[dict[str, Any]]:
    return [
        {
            "collar_id": "COL3248_0_worldtube_selector",
            "object": "source worldtube",
            "candidate_formula": "W_source := closure(supp J_H[tau])",
            "qbasic_condition": "J_H, tau, e_obs and support topology are parent-owned q-basic objects",
            "current_status": "CONDITIONAL_SELECTOR_FROM_1016_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "collar_id": "COL3248_1_distance_function",
            "object": "public metric distance to W_source",
            "candidate_formula": "rho_pub(x) := dist_{g_pub(q)}(x,W_source)",
            "qbasic_condition": "g_pub and W_source descend through q; use a normal tubular neighbourhood avoiding cut locus/caustics",
            "current_status": "CONDITIONAL_GEOMETRIC_CONSTRUCTION",
            "valid_for_claim": "false",
        },
        {
            "collar_id": "COL3248_2_boundary_levels",
            "object": "boundary level functions",
            "candidate_formula": "s_i(x) := rho_pub(x)^2-r_i^2, S_i := {s_i=0}, A_ext[r1,r2] := {r1<=rho_pub<=r2}",
            "qbasic_condition": "r1,r2 fixed before readout; grad s_i non-null/spacelike as required; orientation fixed",
            "current_status": "FORMULA_FILLED_INPUTS_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "collar_id": "COL3248_3_smooth_collar",
            "object": "collar cutoff",
            "candidate_formula": "chi_B(x) := eta((rho_pub(x)-r1)/(r2-r1)) with eta fixed once",
            "qbasic_condition": "eta,r1,r2 fixed constants and rho_pub q-basic",
            "current_status": "FORMULA_FILLED_INPUTS_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "collar_id": "COL3248_4_frame_normal",
            "object": "observed frame and normal",
            "candidate_formula": "u := clock leg of e_obs(q); n_i := grad_i s_i / sqrt(|g_pub^{ab} grad_a s_i grad_b s_i|)",
            "qbasic_condition": "e_obs=Obs_e(q), g_pub=q-owned, non-null boundary, common orientation",
            "current_status": "FORMULA_FILLED_INPUTS_UNSIGNED",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM3248_0_chain_rule",
            "statement": "If W_source, g_pub, r_i and eta are q-basic, then s_i, chi_B, u and n are fixed by any vertical response direction e_A.",
            "proof": "D_A rho_pub = D rho_pub[Dq(e_A)] plus source-support variation; both vanish when g_pub and W_source descend through q. Then D_A s_i=D_A chi_B=D_A u=D_A n=0, away from nonregular boundary points.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": "false",
        },
        {
            "theorem_id": "THM3248_1_regular_tube",
            "statement": "The geodesic collar is legal only inside a regular tubular neighbourhood of W_source.",
            "proof": "Distance to a submanifold/support can fail at cut loci, caustics, null boundaries or nonsmooth support; those defects must be excluded or bounded.",
            "current_status": "DOMAIN_GUARD_REQUIRED",
            "claim_allowed": "false",
        },
        {
            "theorem_id": "THM3248_2_not_numeric",
            "statement": "The formula partially fills the score row but does not make it numeric or claim-grade.",
            "proof": "The corpus still lacks parent-signed W_source, J_H/tau, r1/r2, non-null guard, flux regime, C_flux/C_coll, flux norms, and e_A trace norm.",
            "current_status": "PARTIAL_FILL_ONLY",
            "claim_allowed": "false",
        },
    ]


def arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_row_id": "ARENA3248_0_qbasic_geodesic_collar_partial_fill",
            "boundary_id": "qbasic_geodesic_collar_Wsource_r1_r2_CONDITIONAL",
            "surface_class": "A_ext[r1,r2]={x:r1<=dist_gpub(x,W_source)<=r2}; S_i={dist_gpub^2-r_i^2=0}",
            "s_B": "s_i(x)=dist_gpub(x,W_source)^2-r_i^2",
            "chi_B": "chi_B(x)=eta((dist_gpub(x,W_source)-r1)/(r2-r1))",
            "frame_u": "u=e_obs_clock_leg(q)",
            "normal_n": "n=normalize_gpub(grad s_i)",
            "filled_fields": "boundary_id;surface_class;s_B;chi_B;frame_u;normal_n",
            "still_missing": "parent-signed W_source;J_H;tau;e_obs selector;r1;r2;eta;non-null regularity;orientation;flux regime;C_flux;C_coll;flux norms;eA trace norm;units",
            "computed_J_Poynting_bound": "NOT_COMPUTED",
            "status": "PARTIAL_FORMULA_FILL_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "arena_row_id": "ARENA3248_1_source_worldtube_finite_bound",
            "boundary_id": "source_worldtube_Wsource_CONDITIONAL",
            "surface_class": "material/Hilbert source support worldtube boundary",
            "s_B": "support boundary of J_H[tau] if regular",
            "chi_B": "source-support mask chi_source from parent Hilbert support",
            "frame_u": "MISSING_same_frame_source_u",
            "normal_n": "MISSING_worldtube_normal",
            "filled_fields": "surface_class;s_B_template;chi_B_template",
            "still_missing": "same-frame source support;worldtube regularity;normal;flux norm;source measure glue",
            "computed_J_Poynting_bound": "NOT_COMPUTED",
            "status": "FINITE_BOUND_FALLBACK_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def missing_rows() -> list[dict[str, Any]]:
    return [
        {
            "missing_id": "MISS3248_0_Wsource",
            "field": "W_source",
            "needed_signature": "parent-owned compact Hilbert source worldtube W_source=closure(supp J_H[tau])",
            "current_evidence": "1016 writes exact selector contract but current MTS claim fails",
            "blocks": "boundary_id claim; source-worldtube finite-bound claim",
            "valid_for_claim": "false",
        },
        {
            "missing_id": "MISS3248_1_JH_tau_eobs",
            "field": "J_H;tau;e_obs",
            "needed_signature": "same observed coframe/time generator/source current before readout",
            "current_evidence": "3136 and 2600 provide conditional coframe/clock/tau routes; not parent-signed",
            "blocks": "frame_u claim and source support",
            "valid_for_claim": "false",
        },
        {
            "missing_id": "MISS3248_2_radii_regular",
            "field": "r1;r2;regularity",
            "needed_signature": "fixed radii, regular tubular neighbourhood, non-null boundaries, orientation",
            "current_evidence": "no source-backed local collar radii/regularity row found in inspected sources",
            "blocks": "normal_n and C_flux trace norm",
            "valid_for_claim": "false",
        },
        {
            "missing_id": "MISS3248_3_flux_inputs",
            "field": "flux constants and norms",
            "needed_signature": "C_flux,C_coll,||T_EM(u,n)||,||e_A|| trace norm, units",
            "current_evidence": "3234 supplies formulas but marks inputs missing",
            "blocks": "computed_J_Poynting_bound",
            "valid_for_claim": "false",
        },
    ]


def score_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "score_update_id": "SCU3248_0_PJS3246",
            "score_id": "PJS3246_0_first_component",
            "previous_status": "MISSING_PARENT_BOUNDARY_ID and MISSING_BOUNDARY_COLLAR_WORLDTUBE_CLASS",
            "new_partial_fields": "boundary_id=qbasic_geodesic_collar_Wsource_r1_r2_CONDITIONAL; surface_class=A_ext[r1,r2]; frame_u=e_obs_clock_leg(q); normal_n=normalize(grad s_i)",
            "not_filled": "source-backed W_source,r1,r2,regularity,flux constants,norms,units",
            "claim_effect": "schema improves from blank boundary to conditional collar formula; valid_for_claim remains false",
            "valid_for_claim": "false",
        }
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3248_0_collar_formula",
            "claim": "q-basic collar formula exists",
            "condition_passed": "true",
            "status": "geodesic/source-support formula written",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3248_1_current_boundary",
            "claim": "current MTS owns q-basic collar boundary",
            "condition_passed": "false",
            "status": "W_source/J_H/tau/e_obs/radii/regularity not parent-signed",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3248_2_score_numeric",
            "claim": "Poynting Jtot row is numeric/source-backed",
            "condition_passed": "false",
            "status": "flux constants/norms/eA units still missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3248_3_local_GR",
            "claim": "local GR/Newton/PPN reduction",
            "condition_passed": "false",
            "status": "no numeric qloc/amplitude residual",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3248_0_partial_fill",
            "decision": "Use the Hilbert-source geodesic collar as the best q-basic collar candidate.",
            "because": "It is derived from public metric distance and parent source support, so it is the least post-hoc boundary choice if its premises close.",
            "next_action": "Attack W_source/J_H/tau/e_obs ownership rather than inventing a radius.",
        },
        {
            "decision_id": "DEC3248_1_no_claim",
            "decision": "Do not promote the collar or Poynting score row.",
            "because": "The source support and regularity inputs are still unsigned and flux inputs are absent.",
            "next_action": "Keep the row as partial formula fill, nonclaim.",
        },
        {
            "decision_id": "DEC3248_2_fallback",
            "decision": "Keep source-worldtube finite-bound row as the fallback.",
            "because": "If the q-basic exterior collar cannot be signed, physical source-worldtube flux must be bounded rather than erased.",
            "next_action": "Build a source-worldtube selector/fill row next.",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3248_0_3249",
            "priority": "selected_primary",
            "next_doc": "3249-Y5-R2FR-Wsource-JH-tau-eobs-selector-or-source-worldtube-Poynting-bound-row-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3249_Wsource_JH_tau_eobs_selector_or_source_worldtube_Poynting_bound_row.py",
            "objective": "Try to parent-sign or source W_source=closure(supp J_H[tau]), the same observed coframe/time generator, and the source support regularity needed for the q-basic collar; if not, fill the source-worldtube finite-bound row explicitly as nonclaim.",
            "exclude": "do not choose radii after seeing flux; do not claim measured-GM/source glue; do not edit formalization-workbench",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources_exist = all(row["exists"] == "true" for row in source_rows)
    sources_hit = all(row["evidence_hits"] not in {"MISSING_SOURCE", "NO_MATCH"} for row in source_rows)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    outputs_under_post = all(ROOT in path.parents for path in generated_csvs) and ROOT in DOC.parents
    formalization_3248 = list(FW.rglob("*3248*")) if FW.exists() else []
    formalization_clean = len(formalization_3248) == 0
    formula_filled = any(row["arena_row_id"] == "ARENA3248_0_qbasic_geodesic_collar_partial_fill" for row in arena_rows())
    missing_retained = all(row["valid_for_claim"] == "false" for row in missing_rows())
    claims_blocked = all(row["claim_allowed"] == "false" for row in gate_rows())
    partial_nonclaim = all(row["valid_for_claim"] == "false" for row in arena_rows())
    next_written = bool(next_rows())
    checks = [
        ("VAL3248_0_sources_exist", sources_exist, "all cited source paths exist", str(sources_exist)),
        ("VAL3248_1_source_hits", sources_hit, "source evidence hits are present", str(sources_hit)),
        ("VAL3248_2_csvs_parse", csvs_parse, "all generated CSV files parse", str(csvs_parse)),
        ("VAL3248_3_outputs_under_post_checkpoint", outputs_under_post, "all outputs are under post-checkpoint-work", str(outputs_under_post)),
        ("VAL3248_4_formalization_clean", formalization_clean, "no 3248 outputs in formalization-workbench", f"formalization_3248_count={len(formalization_3248)}"),
        ("VAL3248_5_formula_filled", formula_filled, "q-basic collar formula row was written", str(formula_filled)),
        ("VAL3248_6_missing_retained", missing_retained, "missing signatures remain explicit and nonclaim", str(missing_retained)),
        ("VAL3248_7_claims_blocked", claims_blocked, "all claim gates remain blocked", str(claims_blocked)),
        ("VAL3248_8_partial_nonclaim", partial_nonclaim, "arena partial-fill rows remain nonclaim", str(partial_nonclaim)),
        ("VAL3248_9_next_written", next_written, "3249 next target written", str(next_written)),
        ("VAL3248_10_doc_written", DOC.exists(), "3248 markdown checkpoint exists", str(DOC.exists())),
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
            "validation_id": "VAL3248_OVERALL",
            "passed": bool_str(all(row["passed"] == "true" for row in rows)),
            "requirement": "3248 validation overall",
            "evidence": "all required validation rows passed",
        }
    )
    return rows


def build_doc(
    source_rows: list[dict[str, Any]],
    collar: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    missing: list[dict[str, Any]],
    score_update: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3248 - q-Basic Local Collar Source or First Poynting Arena Row Fill under AX1090",
            f"Generated: `{RUN_UTC}`",
            "Status: `Y5_R2FR_3248_qbasic_geodesic_collar_formula_partially_fills_Poynting_arena_row_Wsource_unsigned_nonclaim`",
            "Claim ceiling: `collar_formula_only_no_parent_Wsource_no_numeric_Poynting_score_no_amplitude_score_no_local_GR_claim`",
            "## Summary",
            "- `3248` makes the constructive move: define the local collar from the Hilbert source support, `W_source=closure(supp J_H[tau])`, and the public metric distance `rho_pub=dist_gpub(x,W_source)`.",
            "- This gives explicit candidate boundary functions: `s_i=rho_pub^2-r_i^2`, `S_i={s_i=0}`, `A_ext[r1,r2]={r1<=rho_pub<=r2}`, and `chi_B=eta((rho_pub-r1)/(r2-r1))`.",
            "- If `W_source`, `g_pub`, `e_obs`, `tau`, radii and regularity all descend through `q`, the collar, frame `u`, and normal `n` are fixed under vertical response directions by chain rule.",
            "- Current MTS still cannot claim the row because `W_source/J_H/tau/e_obs/r1/r2/regularity` are not parent-signed, and the Poynting flux constants/norms remain missing.",
            "- The first Poynting arena row is partially filled with formulas rather than blanks, while `valid_for_claim=false` stays locked.",
            "## q-Basic Collar Construction Attempt",
            md_table(collar, ["collar_id", "object", "candidate_formula", "qbasic_condition", "current_status", "valid_for_claim"]),
            "## Collar q-Basic Chain-Rule Theorem",
            md_table(theorem, ["theorem_id", "statement", "proof", "current_status", "claim_allowed"]),
            "## First Poynting Arena Row Partial Fill",
            md_table(arena, ["arena_row_id", "boundary_id", "surface_class", "s_B", "chi_B", "frame_u", "normal_n", "filled_fields", "still_missing", "computed_J_Poynting_bound", "status", "valid_for_claim"]),
            "## Collar Missing Signatures",
            md_table(missing, ["missing_id", "field", "needed_signature", "current_evidence", "blocks", "valid_for_claim"]),
            "## Score Row Update",
            md_table(score_update, ["score_update_id", "score_id", "previous_status", "new_partial_fields", "not_filled", "claim_effect", "valid_for_claim"]),
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
    collar = collar_rows()
    theorem = theorem_rows()
    arena = arena_rows()
    missing = missing_rows()
    score_update = score_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["collar"], collar)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["missing"], missing)
    write_csv(OUTPUTS["score_update"], score_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    generated_csvs = [
        OUTPUTS["sources"],
        OUTPUTS["collar"],
        OUTPUTS["theorem"],
        OUTPUTS["arena"],
        OUTPUTS["missing"],
        OUTPUTS["score_update"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, collar, theorem, arena, missing, score_update, gates, decisions, next_target, validation),
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, collar, theorem, arena, missing, score_update, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    failed = [row for row in validation if row["passed"] != "true"]
    if failed:
        raise SystemExit(f"3248 validation failed: {failed}")


if __name__ == "__main__":
    main()
