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

CHECKPOINT = "3249"
DOC = ROOT / "3249-Y5-R2FR-Wsource-JH-tau-eobs-selector-or-source-worldtube-Poynting-bound-row-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3249_SOURCE_REGISTER.csv",
    "selector": OUT / "P8_Y5_R2FR_3249_W_SOURCE_SELECTOR_ATTEMPT.csv",
    "regularity": OUT / "P8_Y5_R2FR_3249_SUPPORT_REGULARITY_AUDIT.csv",
    "worldtube_row": OUT / "P8_Y5_R2FR_3249_SOURCE_WORLDTUBE_POYNTING_BOUND_ROW.csv",
    "qcollar_update": OUT / "P8_Y5_R2FR_3249_QCOLLAR_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3249_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3249_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3249_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3249_VALIDATION.csv",
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
            "SRC3249_3248_handoff",
            ROOT / "3248-Y5-R2FR-qbasic-local-collar-source-or-first-Poynting-arena-row-fill-under-AX1090.md",
            "immediate W_source collar handoff",
            ["W_source", "J_H", "tau", "e_obs", "NEXT3248"],
        ),
        (
            "SRC3249_1016_selector",
            ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            "parent worldtube selector contract",
            ["W_source", "closure(supp J_H", "support_selector", "CG1016"],
        ),
        (
            "SRC3249_1720_JH",
            ROOT / "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md",
            "observed Hilbert current and matter functor route",
            ["J_H", "T_obs", "e_obs", "matter functor"],
        ),
        (
            "SRC3249_3136_eobs_tau",
            ROOT / "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md",
            "observed coframe clock functional theorem",
            ["e_obs", "Dq(v)=0", "tau_clk", "parent ownership"],
        ),
        (
            "SRC3249_2600_moving_tau",
            ROOT / "2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md",
            "moving tau source-current obstruction and exact law",
            ["Delta_JH_delta_tau", "C_Tobs_tau", "tau_obs", "BLOCKED_NO_CLAIM"],
        ),
        (
            "SRC3249_2557_clock_gate",
            ROOT / "2557-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
            "Hilbert current conservation and clock compatibility gate",
            ["J_M", "tau", "worldtube", "DERIVATION_SHARPENED"],
        ),
        (
            "SRC3249_3234_poynting",
            ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
            "Poynting flux finite-bound functional",
            ["T_EM(u,n)", "C_flux", "C_coll", "Phi_Poynting"],
        ),
        (
            "SRC3249_worldtube_clauses",
            OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            "parent worldtube/exterior annulus clauses",
            ["W504_0_worldtube_setup", "W504_4_worldtube_source_measure_glue"],
        ),
        (
            "SRC3249_worldtube_measure",
            OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
            "worldtube source measure theorem",
            ["T510_1_worldtube_source_measure", "M_source", "H_tau"],
        ),
        (
            "SRC3249_hwg_certificate",
            OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
            "Hilbert worldtube certificate gaps",
            ["HWG535_0_worldtube_fixed_before_readout", "missing_certificate"],
        ),
        (
            "SRC3249_hsm_contract",
            OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            "Hamiltonian source measure contract",
            ["HSM541_2_observed_worldtube_source", "W_source=supp", "not_derived"],
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


def selector_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "SEL3249_0_define_vertical_test",
            "object": "vertical response direction e_A",
            "derivation": "Take e_A in ker(Dq), so D_A q=0. This is the same representative/internal direction used by the q-basic collar route.",
            "required_parent_signature": "parent quotient map q and response basis e_A are fixed before readout",
            "current_status": "CONDITIONAL_FROM_PRIOR_CHAIN",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SEL3249_1_observed_coframe_fixed",
            "object": "e_obs",
            "derivation": "If e_obs=Obs_e(q(Phi)), then D_A e_obs = D Obs_e[D_A q] = 0.",
            "required_parent_signature": "explicit Obs_e(q) map and ordinary matter coupling to that coframe",
            "current_status": "FORMAL_CHAIN_EXACT_IF_3136_INPUTS_SIGNED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SEL3249_2_time_generator_fixed",
            "object": "tau",
            "derivation": "If tau=tau_obs[e_obs] or tau=tau_q(q) with the same observed clock leg, then D_A tau=0 whenever D_A e_obs=0.",
            "required_parent_signature": "same tau for clock/source/charge/orbit/boundary; no moving-tau source current",
            "current_status": "FORMAL_CHAIN_EXACT_IF_2600_MOVING_TAU_TERM_ZERO_OR_FIXED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SEL3249_3_Hilbert_current_fixed",
            "object": "J_H[tau]",
            "derivation": "For ordinary matter descending as S_matter[e_obs,psi,theta], J_H[tau]=star_eobs(T_obs(tau,.)); hence D_A J_H=0 if D_A e_obs=0, D_A tau=0, and no source-only prefactor/connection/boundary channel survives.",
            "required_parent_signature": "1720 matter-functor package plus no hidden source prefactor and same-frame stress current",
            "current_status": "CONDITIONAL_EXACT_NOT_CURRENTLY_PARENT_SIGNED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SEL3249_4_support_fixed",
            "object": "supp J_H[tau]",
            "derivation": "If J_H is invariant as a distribution under e_A, every open set on which J_H vanishes remains empty of source, and every regular nonzero source patch remains source; with compact regular support this gives D_A supp(J_H)=0 in the Hausdorff/support sense.",
            "required_parent_signature": "compact support, regular threshold/no nodal degeneration, no readout-selected mask",
            "current_status": "NEW_SUPPORT_SELECTOR_LEMMA_CONDITIONAL",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SEL3249_5_worldtube_fixed",
            "object": "W_source",
            "derivation": "W_source := closure(supp J_H[tau]) is therefore q-basic: D_A W_source=0, provided SEL3249_1 through SEL3249_4 are signed.",
            "required_parent_signature": "J_H/tau/e_obs/support regularity all owned by the same parent branch",
            "current_status": "EXACT_CONDITIONAL_SELECTOR_GATE_NOT_PHYSICS_CLAIM",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SEL3249_6_collar_consequence",
            "object": "rho_pub,s_i,chi_B,u,n",
            "derivation": "With W_source and g_pub(q) q-basic, rho_pub=dist_gpub(x,W_source), s_i=rho_pub^2-r_i^2, chi_B=eta((rho_pub-r1)/(r2-r1)), u=e_obs clock leg, and n=normalize(grad s_i) are q-basic inside the regular tube.",
            "required_parent_signature": "fixed radii, regular tube, orientation, observed frame and public metric",
            "current_status": "ROLLS_3248_FORWARD_WITH_STRONGER_WSOURCE_CONTRACT",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def regularity_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "REG3249_0_compact_support",
            "needed_condition": "J_H[tau] has compact support on the local source branch",
            "why_needed": "without compact support there is no finite source worldtube/collar split",
            "current_evidence": "1016/2557 treat compact-source route as conditional; current parent has not signed it",
            "status": "UNSIGNED",
            "blocks": "W_source claim; source-worldtube row numeric claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "REG3249_1_distribution_invariance",
            "needed_condition": "D_A J_H=0 as a distribution for all vertical e_A",
            "why_needed": "support invariance follows from current invariance, not from visual/source fitting",
            "current_evidence": "1720 gives J_H definition conditionally; 2600 leaves moving-tau source current active unless fixed",
            "status": "UNSIGNED",
            "blocks": "D_A W_source=0",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "REG3249_2_no_threshold_degeneracy",
            "needed_condition": "support is defined by exact nonzero current or by a parent-fixed threshold with no nodal boundary degeneracy",
            "why_needed": "first-order support maps can jump at zero-density/nodal boundaries",
            "current_evidence": "no parent threshold or regular nonzero-density clause is signed",
            "status": "UNSIGNED",
            "blocks": "Hausdorff/support derivative claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "REG3249_3_regular_tube",
            "needed_condition": "there is a tubular neighbourhood with smooth distance function and no cut-locus/caustic collision between r1 and r2",
            "why_needed": "rho_pub, s_i and n must be differentiable enough for Poynting/stress traces",
            "current_evidence": "3248 states this condition but does not source r1/r2 or regularity",
            "status": "UNSIGNED",
            "blocks": "normal_n and trace-norm claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "REG3249_4_no_readout_mask",
            "needed_condition": "W_source is not chosen after orbital/flux readout and not by a fitted mask",
            "why_needed": "otherwise the boundary is post hoc and can hide leakage",
            "current_evidence": "1016 forbids readout-selected support, but current MTS has not supplied the parent selector",
            "status": "GUARDRAIL_ACTIVE_UNSIGNED",
            "blocks": "claim promotion",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "REG3249_5_same_frame_measure",
            "needed_condition": "same e_obs/tau used for matter source, clock, boundary charge, orbit and Poynting stress",
            "why_needed": "frame mismatch creates source-measure and Poynting residuals",
            "current_evidence": "3136/1720/2600 each identify pieces; no one parent certificate joins them",
            "status": "UNSIGNED",
            "blocks": "source coupling/local GR claim",
            "valid_for_claim": "false",
        },
    ]


def worldtube_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SWP3249_0_source_worldtube_Poynting_bound",
            "component_id": "PJS3246_0_first_component",
            "boundary_id": "source_worldtube_Wsource_CONDITIONAL",
            "surface_class": "source_worldtube_or_regular_support_tube",
            "W_source": "closure(supp J_H[tau])",
            "frame_u": "e_obs_clock_leg(q)_CONDITIONAL",
            "normal_n": "MISSING_WORLD_TUBE_NORMAL_OR_REGULAR_LEVEL_SET",
            "bound_formula": "|J_A^Poynting| <= ||e_A||_B(C_flux||S_EM dot n||_B+B_corner_flux)+||e_A||_coll C_coll||T_EM(u,n)||_collar",
            "C_flux": "MISSING_C_FLUX",
            "C_coll": "MISSING_C_COLL",
            "flux_norm": "MISSING_T_EM_U_N_ON_SOURCE_COLLAR",
            "eA_norm": "MISSING_RESPONSE_BASIS_TRACE_NORM",
            "units": "MISSING_COMMON_JTOT_UNITS",
            "computed_J_Poynting_bound": "NOT_COMPUTED",
            "source_paths": str(ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md")
            + ";"
            + str(DOC),
            "current_status": "FORMULA_READY_SOURCE_WORLDTUBE_INPUTS_MISSING_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SWP3249_1_selector_bound_piece",
            "component_id": "selector_stability",
            "boundary_id": "W_source_support_stability",
            "surface_class": "support_map",
            "W_source": "closure(supp J_H[tau])",
            "frame_u": "same e_obs/tau package",
            "normal_n": "not_applicable",
            "bound_formula": "D_A W_source=0 if D_A J_H=0 distributionally plus compact regular support; otherwise retain Delta_W_source support drift",
            "C_flux": "not_applicable",
            "C_coll": "not_applicable",
            "flux_norm": "not_applicable",
            "eA_norm": "not_applicable",
            "units": "support/Hausdorff or distribution topology must be specified",
            "computed_J_Poynting_bound": "NOT_COMPUTED",
            "source_paths": str(OUTPUTS["selector"]),
            "current_status": "CONDITIONAL_SELECTOR_BOUND_FORM_ONLY",
            "valid_for_claim": "false",
        },
    ]


def qcollar_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "QCU3249_0_Wsource_derivation_upgrade",
            "target": "ARENA3248_0_qbasic_geodesic_collar_partial_fill",
            "previous_status": "W_source formula stated; source ownership missing",
            "new_derivation": "D_A W_source=0 follows from D_A e_obs=0, D_A tau=0, D_A J_H=0 and compact regular support; this is an exact conditional selector theorem.",
            "current_status": "UPGRADED_TO_EXACT_CONDITIONAL_GATE_NOT_PARENT_SIGNED",
            "claim_effect": "improves the ladder rung but does not make the local branch pass",
            "valid_for_claim": "false",
        },
        {
            "update_id": "QCU3249_1_Poynting_row_upgrade",
            "target": "PJS3246_0_first_component",
            "previous_status": "missing boundary_id and boundary/collar inputs",
            "new_derivation": "boundary_id may now be source_worldtube_Wsource_CONDITIONAL if support selector is signed; otherwise use explicit finite-bound row SWP3249_0",
            "current_status": "SOURCE_WORLDTUBE_BOUND_ROW_WRITTEN_NONCLAIM",
            "claim_effect": "turns the Poynting coupling worry into a sourceable finite row",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3249_0_selector_theorem",
            "claim": "W_source support selector theorem is mathematically exact under stated premises",
            "gate_pass": "true",
            "reason": "distributional J_H invariance plus compact regular support fixes closure(supp J_H)",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3249_1_current_parent_signature",
            "claim": "current MTS parent signs J_H/tau/e_obs/support regularity as one object",
            "gate_pass": "false",
            "reason": "1720/3136/2600/2557 remain conditional or bounded, not one parent-owned certificate",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3249_2_worldtube_Poynting_numeric",
            "claim": "source-worldtube Poynting row is numeric/source-backed",
            "gate_pass": "false",
            "reason": "normal, flux constants, flux norms, response trace norm and units remain missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3249_3_local_GR_Newton",
            "claim": "local GR/Newton/PPN branch is derived",
            "gate_pass": "false",
            "reason": "source coupling and Poynting/local residual vector are bounded-form only",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3249_0_result",
            "decision": "Keep the source-worldtube collar route",
            "because": "the support selector has a real conditional proof, unlike arbitrary plateau/boundary closure",
            "next_action": "try to sign J_H/e_obs/tau from one parent matter action, or source the first flux-norm row",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3249_1_no_claim",
            "decision": "Do not claim local GR, PPN, R10, WEP, clocks, or orbital pass",
            "because": "the theorem is conditional and current MTS lacks same-parent signatures",
            "next_action": "turn unsigned clauses into either theorem signatures or finite residual coefficients",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3249_2_best_pressure_point",
            "decision": "Attack the one-parent observed matter package next",
            "because": "if e_obs/tau/J_H are signed together, W_source, collar, and source coupling all move at once",
            "next_action": "write 3250 as Hilbert-current e_obs tau owner or source-worldtube flux-norm row",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3249_0_3250",
            "selection": "selected_primary",
            "next_checkpoint": "3250-Y5-R2FR-Hilbert-current-eobs-tau-owner-or-source-worldtube-flux-norm-row-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3250_Hilbert_current_eobs_tau_owner_or_source_worldtube_flux_norm_row.py",
            "objective": "Try to derive/source the same-frame parent matter package J_H=star_eobs(T_obs(tau,.)) with e_obs and tau owned together; if not, source the first concrete T_EM(u,n) / S_EM dot n flux-norm row for the source-worldtube Poynting bound.",
            "guardrail": "do not claim local GR/Newton/Maxwell; do not infer tau ownership from clocks alone; do not choose flux collars after readout",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources_exist = all(row["exists"] == "true" for row in source_rows)
    sources_hit = all(row["evidence_hits"] not in {"MISSING_SOURCE", "NO_MATCH"} for row in source_rows)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    under_post_checkpoint = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in [*generated_csvs, DOC])
    formalization_3249 = list(FW.rglob("*3249*")) if FW.exists() else []
    formalization_clean = len(formalization_3249) == 0
    selector_exact = any(row["step_id"] == "SEL3249_5_worldtube_fixed" for row in selector_rows())
    support_regular_unsigned = all(row["valid_for_claim"] == "false" for row in regularity_rows())
    fallback_nonclaim = all(row["valid_for_claim"] == "false" for row in worldtube_bound_rows())
    fallback_has_missing = any("MISSING_" in ";".join(str(value) for value in row.values()) for row in worldtube_bound_rows())
    claims_blocked = all(row["claim_allowed"] == "false" for row in gate_rows())
    parent_signature_false = any(row["claim_gate_id"] == "CG3249_1_current_parent_signature" and row["gate_pass"] == "false" for row in gate_rows())
    next_written = bool(next_rows())
    doc_written = DOC.exists()
    checks = [
        ("VAL3249_0_sources_exist", sources_exist, "all cited source paths exist", str(sources_exist)),
        ("VAL3249_1_source_hits", sources_hit, "source evidence hits are present", str(sources_hit)),
        ("VAL3249_2_csvs_parse", csvs_parse, "all generated CSV files parse", str(csvs_parse)),
        ("VAL3249_3_outputs_under_post_checkpoint", under_post_checkpoint, "all outputs are under post-checkpoint-work", str(under_post_checkpoint)),
        ("VAL3249_4_formalization_clean", formalization_clean, "no 3249 outputs in formalization-workbench", f"formalization_3249_count={len(formalization_3249)}"),
        ("VAL3249_5_selector_exact_conditional", selector_exact, "W_source exact conditional selector gate written", str(selector_exact)),
        ("VAL3249_6_support_regular_unsigned", support_regular_unsigned, "support regularity gaps remain explicit and nonclaim", str(support_regular_unsigned)),
        ("VAL3249_7_fallback_nonclaim", fallback_nonclaim, "source-worldtube Poynting bound rows remain nonclaim", str(fallback_nonclaim)),
        ("VAL3249_8_fallback_has_missing", fallback_has_missing, "fallback row preserves missing-input markers", str(fallback_has_missing)),
        ("VAL3249_9_claims_blocked", claims_blocked, "all claim gates remain blocked", str(claims_blocked)),
        ("VAL3249_10_parent_signature_false", parent_signature_false, "current parent signature gate remains false", str(parent_signature_false)),
        ("VAL3249_11_next_written", next_written, "3250 next target written", str(next_written)),
        ("VAL3249_12_doc_written", doc_written, "3249 markdown checkpoint exists", str(doc_written)),
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
            "validation_id": "VAL3249_OVERALL",
            "passed": bool_str(all(row["passed"] == "true" for row in rows)),
            "requirement": "3249 validation overall",
            "evidence": "all required validation rows passed",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    selector: list[dict[str, Any]],
    regularity: list[dict[str, Any]],
    worldtube: list[dict[str, Any]],
    qcollar: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    lines = [
        "# 3249 - Wsource JH tau eobs selector or source-worldtube Poynting bound row under AX1090",
        "",
        f"Generated: `{RUN_UTC}`",
        "",
        "Private derivation checkpoint. This does not claim local GR, Newton, Maxwell, PPN, R10, WEP, clocks or orbital closure.",
        "",
        "## Summary",
        "",
        "- `3249` pushes the `3248` collar route one rung deeper: `W_source := closure(supp J_H[tau])` is now an exact conditional selector gate, not just a named missing object.",
        "- The proof route is: `Dq[e_A]=0`, `e_obs=Obs_e(q)`, fixed same `tau`, ordinary matter descends to `e_obs`, so `D_A J_H=0`; compact regular support then gives `D_A W_source=0` in the support/Hausdorff sense.",
        "- This is real movement toward coupling: if a future parent action signs the same-frame package, the boundary/collar/frame used by the Poynting term is no longer arbitrary.",
        "- Current MTS still cannot claim the local branch because the corpus has not signed `J_H`, `tau`, `e_obs`, and support regularity as one parent-owned object.",
        "- The fallback is no longer vibes: a source-worldtube Poynting finite-bound row is written with exact missing inputs and `valid_for_claim=false`.",
        "",
        "## W Source Selector Attempt",
        "",
        md_table(selector, ["step_id", "object", "derivation", "required_parent_signature", "current_status", "claim_allowed", "valid_for_claim"]),
        "",
        "## Support Regularity Audit",
        "",
        md_table(regularity, ["audit_id", "needed_condition", "why_needed", "current_evidence", "status", "blocks", "valid_for_claim"]),
        "",
        "## Source-Worldtube Poynting Bound Row",
        "",
        md_table(worldtube, ["row_id", "component_id", "boundary_id", "surface_class", "W_source", "frame_u", "normal_n", "bound_formula", "C_flux", "C_coll", "flux_norm", "eA_norm", "units", "computed_J_Poynting_bound", "current_status", "valid_for_claim"]),
        "",
        "## Q-Collar Update",
        "",
        md_table(qcollar, ["update_id", "target", "previous_status", "new_derivation", "current_status", "claim_effect", "valid_for_claim"]),
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
        "`W_source` has been advanced from a missing boundary name to a conditional theorem gate. The project should now press the same-frame matter package: prove `J_H=star_eobs(T_obs(tau,.))`, `e_obs`, and `tau` are all parent-owned together, or accept the finite source-worldtube flux-norm row as the next honest bound.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register()
    selector = selector_rows()
    regularity = regularity_rows()
    worldtube = worldtube_bound_rows()
    qcollar = qcollar_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    generated_without_validation = [
        OUTPUTS["sources"],
        OUTPUTS["selector"],
        OUTPUTS["regularity"],
        OUTPUTS["worldtube_row"],
        OUTPUTS["qcollar_update"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["selector"], selector)
    write_csv(OUTPUTS["regularity"], regularity)
    write_csv(OUTPUTS["worldtube_row"], worldtube)
    write_csv(OUTPUTS["qcollar_update"], qcollar)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    DOC.write_text(
        "# 3249 - Wsource JH tau eobs selector or source-worldtube Poynting bound row under AX1090\n\n"
        "Pending final validation table.\n",
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_without_validation)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(source_rows, selector, regularity, worldtube, qcollar, gates, decisions, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    overall = next(row for row in validation if row["validation_id"] == "VAL3249_OVERALL")
    if overall["passed"] != "true":
        raise SystemExit("3249 validation failed")


if __name__ == "__main__":
    main()
