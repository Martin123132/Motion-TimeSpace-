from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "944_doc",
            "path": "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
            "role": "handoff selecting parent q-map and Obs_e construction",
            "needle": "construct `q:Phi->Q_obs` and `Obs_e(q)` explicitly",
        },
        {
            "source_id": "944_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_944_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V944_12_validation_rows_ready",
        },
        {
            "source_id": "944_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_944_NEXT_TARGET.csv",
            "role": "945 target contract",
            "needle": "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
        },
        {
            "source_id": "272_quotient_principle",
            "path": "272-quotient-configuration-principle-from-topological-projector.md",
            "role": "presymplectic/topological route to quotient configuration space",
            "needle": "quotient_principle_conditionally_derived_from_presymplectic",
        },
        {
            "source_id": "341_cell_quotient",
            "path": "341-indistinguishable-cell-quotient-parent-action-gate.md",
            "role": "finite-cell quotient/orbit route and marker hazard",
            "needle": "the quotient route is mathematically clean",
        },
        {
            "source_id": "407_relational_action",
            "path": "407-primitive-relational-quotient-action-sketch.md",
            "role": "primitive relational quotient parent-action sketch",
            "needle": "primitive_relational_quotient_action_sketch_written",
        },
        {
            "source_id": "414_invariant_algebra",
            "path": "414-local-quotient-invariant-algebra-triviality-gate.md",
            "role": "local invariant algebra burden",
            "needle": "I_loc(Q) = I_geom",
        },
        {
            "source_id": "415_trivial_class",
            "path": "415-local-trivial-class-selector-theorem-attempt.md",
            "role": "local trivial class selector attempt",
            "needle": "local_trivial_class_selector_theorem_attempt_written",
        },
        {
            "source_id": "623_coframe_functor",
            "path": "623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md",
            "role": "coframe factorization lemma",
            "needle": "OCF623_0_factorization_lemma",
        },
        {
            "source_id": "624_parent_signature",
            "path": "624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md",
            "role": "observed coframe parent signature audit",
            "needle": "SIG624_0_parent_quotient",
        },
        {
            "source_id": "710_descent_clause",
            "path": "710-Y5-R10-scalar-class-zero-premise-parent-action-clause-or-frame-transfer-guard.md",
            "role": "descent clause and frame-transfer guard",
            "needle": "DPC710_9_verdict",
        },
        {
            "source_id": "QDA711_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv",
            "role": "quotient descent audit of parent q-map burdens",
            "needle": "QDA711_9_verdict",
        },
        {
            "source_id": "MDS898_signature",
            "path": "source-intake/mts_residuals/P8_Y5_R10_898_MATTER_DESCENT_SIGNATURE.csv",
            "role": "latest matter descent signature",
            "needle": "MDS898_5_verdict",
        },
        {
            "source_id": "FLB944_bound_pack",
            "path": "source-intake/mts_residuals/P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
            "role": "frame-leak bound pack schema from 944",
            "needle": "FLB944_0_cg_weyl",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def q_map_candidate_construction() -> list[dict[str, str]]:
    specs = [
        (
            "QMAP945_0_parent_field_inventory",
            "Phi_parent",
            "candidate parent field inventory",
            "Phi_parent contains observed/local geometry variables, topological/relative class data, finite-cell fibre data, domain/boundary data, memory/scalar/class labels, matter fields, constants, and readout conventions",
            "inventory_synthesized_not_parent_action_complete",
            "field list is not a variational parent action",
        ),
        (
            "QMAP945_1_candidate_projection",
            "q_candidate",
            "candidate quotient projection",
            "q_candidate(Phi)=(e_obs, [C]_PD, Orbit_27(h), [J_rel]_local, theta_univ, boundary_class_if_owned)",
            "candidate_written_not_claim_ready",
            "putting e_obs into q makes Obs_e projection easy but does not prove the kernel is gauge",
        ),
        (
            "QMAP945_2_observed_functor",
            "Obs_e(q_candidate)",
            "observed coframe functor as projection",
            "Obs_e(q_candidate)=e_obs",
            "formal_functor_written",
            "projection-by-declaration trap unless e_obs is parent-owned and kernel directions are null",
        ),
        (
            "QMAP945_3_kernel_definition",
            "ker(Dq_candidate)",
            "formal vertical directions",
            "v in ker(Dq_candidate) iff delta_v e_obs=0, delta_v[C]_PD=0, delta_v Orbit_27(h)=0, delta_v[J_rel]_local=0, delta_v theta_univ=0",
            "formal_kernel_written",
            "must prove each such v is presymplectic/gauge and matter-invisible",
        ),
        (
            "QMAP945_4_presymplectic_ownership",
            "Omega(v,.)=0",
            "kernel ownership certificate",
            "i_v Omega_parent=0 and i_v Theta_parent=dB_v with zero compact local flux",
            "not_proved",
            "272 leaves Cperp exactness and boundary primitive open; 414/415 leave marker/class generators open",
        ),
        (
            "QMAP945_5_matter_invisibility",
            "Lie_v S_matter=0",
            "matter descent certificate",
            "S_matter=Sbar[q_candidate(Phi),Psi,theta] with Lie_v theta=0 and zero boundary/source tail",
            "not_parent_signed",
            "410/626/898 keep matter functor, constants, geometry stack, and boundary tails unsigned",
        ),
        (
            "QMAP945_6_verdict",
            "q_candidate_status",
            "construction verdict",
            "candidate q and Obs_e can be written, but the kernel/null/matter certificates are not proved",
            "candidate_construction_only_no_descent_claim",
            "no frame-leak zero or local-GR promotion",
        ),
    ]
    return [
        {
            "construction_id": construction_id,
            "object": object_name,
            "role": role,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "failure_if_used_as_proof": failure_if_used_as_proof,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for construction_id, object_name, role, mathematical_form, current_status, failure_if_used_as_proof in specs
    ]


def obs_e_functor_audit() -> list[dict[str, str]]:
    specs = [
        (
            "OBS945_0_projection_functor",
            "Obs_e(q)=e_obs projection",
            "valid as a candidate definition if e_obs is an included quotient datum",
            "projection_written",
            "does not prove e_obs is the only matter-visible geometry",
        ),
        (
            "OBS945_1_Q_only_multiple_frames",
            "E_A(q) species/readout frames",
            "vertical-blind if every E_A factors through q",
            "allowed_but_interpretation_debt",
            "single public observed frame still needs species/readout equivalence",
        ),
        (
            "OBS945_2_local_lorentz_gauge",
            "e_obs -> Lambda(x)e_obs",
            "safe if Lambda is ordinary local Lorentz gauge and S_matter is gauge invariant",
            "conditional_gauge_safe",
            "needs matter gauge-invariance source/certificate",
        ),
        (
            "OBS945_3_representative_weyl",
            "e_m=A_g(X)e_obs",
            "not a q-functor if X is vertical representative data",
            "counterexample_retained",
            "requires c_g/b_g bound or no-representative-frame theorem",
        ),
        (
            "OBS945_4_representative_disformal",
            "g_m=A_g(X)^2g_obs+B_g(X)U_muU_nu",
            "not killed by coframe projection unless B_g and U are quotient-owned/gauge",
            "counterexample_retained",
            "requires disformal bound or absence theorem",
        ),
        (
            "OBS945_5_material_marker",
            "theta_A(X), m_A(X), alpha_EM(X)",
            "quotient can be extended by material markers unless no-marker theorem forbids them",
            "counterexample_retained",
            "requires constants/mass descent or b_A/b_alpha bounds",
        ),
        (
            "OBS945_6_verdict",
            "Obs_e functor status",
            "Obs_e can be formally projected from q_candidate, but parent uniqueness/descent is not signed",
            "formal_only",
            "no same-frame/source selector claim",
        ),
    ]
    return [
        {
            "audit_id": audit_id,
            "case": case,
            "mathematical_status": mathematical_status,
            "current_status": current_status,
            "remaining_gap": remaining_gap,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for audit_id, case, mathematical_status, current_status, remaining_gap in specs
    ]


def kernel_test_rows() -> list[dict[str, str]]:
    specs = [
        (
            "KT945_0_Cperp_shift",
            "Cperp relative-exact shift",
            "candidate_null_if eta_perp=d_rel alpha and boundary primitive zero",
            "conditional_from_272",
            "Cperp exactness and boundary primitive remain open",
        ),
        (
            "KT945_1_S27_relabel",
            "finite-cell relabel/orbit direction",
            "null if cells are unlabelled parent fibre coordinates rather than species/material channels",
            "conditional_from_341",
            "parent variable origin and marker extension remain open",
        ),
        (
            "KT945_2_relative_class_shift",
            "local relative/domain class variation",
            "null only if local class is trivial, no-defect, and boundary exchange vanishes",
            "not_proved_from_415",
            "local selector/topology/no-boundary-hair not derived",
        ),
        (
            "KT945_3_scalar_class_label",
            "scalar/class label variation",
            "null only if topological/readout-only and no EH prefactor or matter frame transfer exists",
            "not_proved_from_710",
            "F(sigma)R and B_A(sigma) counterexamples remain legal",
        ),
        (
            "KT945_4_representative_weyl",
            "Weyl frame variation",
            "not in safe kernel unless no-representative-frame theorem or c_g=0 source exists",
            "fails_currently",
            "retained as FLB944_0/BND945_0",
        ),
        (
            "KT945_5_species_marker",
            "species/mass/clock marker variation",
            "not in safe kernel unless constants are quotient-owned or universal",
            "fails_currently",
            "retained as b_A/b_alpha bound rows",
        ),
        (
            "KT945_6_total_kernel",
            "ker(Dq_candidate) as physical gauge kernel",
            "all candidate kernel directions are presymplectic-null, matter-invisible, and boundary-silent",
            "not_proved",
            "cannot sign q_candidate as parent quotient map",
        ),
    ]
    return [
        {
            "kernel_test_id": kernel_test_id,
            "direction": direction,
            "test": test,
            "current_status": current_status,
            "failure_gap": failure_gap,
            "passes_kernel_gate": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for kernel_test_id, direction, test, current_status, failure_gap in specs
    ]


def first_frame_leak_bound_rows() -> list[dict[str, str]]:
    specs = [
        (
            "BND945_0_cg_value",
            "c_g",
            "d ln A_g/dXhat for a representative Weyl/common matter frame",
            "dimensionless",
            "MISSING_PARENT_ZERO_OR_NUMERIC_CG",
            "source parent no-representative-frame theorem or numeric c_g prior",
            "R10;PPN;WEP;clock",
        ),
        (
            "BND945_1_tau_R10",
            "tau_R10",
            "R10 material/source-test projection of c_g or b_g",
            "dimensionless",
            "MISSING_ARENA_PROJECTION",
            "source material trace/projection convention for short-range tests",
            "R10",
        ),
        (
            "BND945_2_tau_PPN",
            "tau_PPN",
            "PPN projection of common-frame/disformal response",
            "dimensionless",
            "MISSING_ARENA_PROJECTION",
            "source gauge-fixed weak-field projection",
            "PPN",
        ),
        (
            "BND945_3_bA_species",
            "b_A",
            "d ln m_A^obs/dXhat or constants/clock derivative for material species A",
            "dimensionless",
            "MISSING_CONSTANT_DESCENT_OR_NUMERIC_BA",
            "source constants/mass descent theorem or material sensitivity bound",
            "WEP;clock;composition",
        ),
        (
            "BND945_4_disformal_value",
            "b_dis",
            "representative disformal derivative dB_g/dXhat with profile convention",
            "model_dependent",
            "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND",
            "source disformal absence theorem or PPN/preferred-frame projection",
            "PPN;preferred_frame;clock",
        ),
        (
            "BND945_5_nonHilbert_projection",
            "q_nonH",
            "ordinary source projection of non-Hilbert current or boundary tail",
            "source_current_units",
            "MISSING_NONHILBERT_ZERO_FLUX_OR_NUMERIC_SOURCE",
            "source boundary/no-tail theorem or finite flux row",
            "R10;PPN;source_normalization",
        ),
        (
            "BND945_6_support_frame_shift",
            "Delta_W_support",
            "source support shift under allowed observed-frame choices",
            "dimensionless",
            "MISSING_SUPPORT_EQUIVALENCE_OR_NUMERIC_BOUND",
            "source support-frame equivalence theorem or system-level bound",
            "orbital;local_GR",
        ),
        (
            "BND945_7_score_gate",
            "score_gate",
            "no retained frame-leak row is scoreable until parent value, arena projection, units, and source path are real",
            "policy",
            "SCHEMA_ONLY_NONCLAIM",
            "all BND945 rows valid_for_claim=false until no MISSING markers remain",
            "all_local_arenas",
        ),
    ]
    return [
        {
            "bound_row_id": bound_row_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "current_status": current_status,
            "next_source_action": next_source_action,
            "observable_link": observable_link,
            "source_path": "MISSING_PARENT_SOURCE",
            "numeric_value": "MISSING_PARENT_INPUT",
            "arena_projection": "MISSING_ARENA_PROJECTION",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for bound_row_id, symbol, definition, units, current_status, next_source_action, observable_link in specs
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC945_0_candidate_q",
            "decision": "q_candidate_and_Obs_e_functor_written_but_not_parent_signed",
            "reason": "q_candidate can include e_obs and quotient/orbit/class data, but its kernel is not proved presymplectic-null, marker-free, matter-invisible, and boundary-silent",
            "consequence": "quotient descent remains a conditional theorem; no frame-leak zero or local-GR promotion",
            "next_action": "attack kernel ownership certificate before calling q_candidate physical",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC945_1_best_next",
            "decision": "q_kernel_presymplectic_null_selected_next",
            "reason": "the obstruction moved from writing q notation to proving that ker(Dq_candidate) is a gauge/null kernel of the parent action",
            "consequence": "946 should try to prove Omega(v,.)=0 and Lie_v S_matter=0 for the candidate kernel, or fall back to first c_g/b_A source rows",
            "next_action": "946-Y5-R10-q-kernel-presymplectic-null-and-no-marker-certificate-or-cg-ba-bound-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC945_2_bound_rows",
            "decision": "first_frame_leak_bound_rows_promoted_to_schema_nonclaim",
            "reason": "if kernel ownership fails, c_g, tau_R10, tau_PPN, b_A, b_dis, q_nonH, and Delta_W_support are the first empirical interfaces",
            "consequence": "data-facing local testing has a clean shopping list, but all rows remain blocked by MISSING inputs",
            "next_action": "source these rows only if derivation route stalls",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE945_0_q_candidate",
            "claim": "q_candidate is the physical parent quotient map",
            "blocker": "kernel ownership/presymplectic null certificate missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE945_1_Obs_e",
            "claim": "Obs_e(q) signs observed coframe descent",
            "blocker": "Obs_e projection is formal unless q_candidate is parent-owned and matter sees no extra frames",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE945_2_kernel",
            "claim": "ker(Dq_candidate) is gauge/null and matter-invisible",
            "blocker": "Cperp exactness, marker exclusion, local trivial class, scalar prefactor, and boundary no-tail remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE945_3_bound_rows",
            "claim": "frame-leak bound rows are scoreable",
            "blocker": "BND945 rows contain MISSING_PARENT_INPUT and MISSING_ARENA_PROJECTION",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE945_4_local_GR",
            "claim": "local GR/Newton/PPN reduction is derived",
            "blocker": "q-kernel ownership, matter descent, same-worldtube glue, measured-GM calibration, and PPN stability remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "946-Y5-R10-q-kernel-presymplectic-null-and-no-marker-certificate-or-cg-ba-bound-row.md",
            "objective": "try to prove the candidate q-kernel is presymplectic-null, marker-free, matter-invisible, and boundary-silent; if not, fill the first real c_g/b_A bound rows from BND945",
            "include": "Omega(v,.)=0, i_vTheta=dB_v zero flux, Cperp exactness, S27 unlabelled-fibre proof, no material marker theorem, local trivial class, matter descent, c_g/b_A first-bound fallback",
            "exclude": "projection-by-declaration q proof, assuming e_obs insertion solves descent, hiding marker/Weyl/disformal leaks, local-GR claim, beta pass claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    construction_rows: list[dict[str, str]],
    obs_rows: list[dict[str, str]],
    kernel_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_944_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    candidate_written = any(row["construction_id"] == "QMAP945_1_candidate_projection" and row["current_status"] == "candidate_written_not_claim_ready" for row in construction_rows)
    construction_nonclaim = any(row["construction_id"] == "QMAP945_6_verdict" and row["current_status"] == "candidate_construction_only_no_descent_claim" for row in construction_rows)
    obs_formal = any(row["audit_id"] == "OBS945_6_verdict" and row["current_status"] == "formal_only" for row in obs_rows)
    kernel_not_passed = any(row["kernel_test_id"] == "KT945_6_total_kernel" and row["current_status"] == "not_proved" for row in kernel_rows) and all(row["passes_kernel_gate"] == "false" for row in kernel_rows)
    bounds_blocked = bound_rows and all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in bound_rows)
    next_selected = any(row["next_target"].startswith("946-Y5-R10-q-kernel") for row in target_rows)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claims_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + construction_rows + obs_rows + kernel_rows + bound_rows + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V945_0_sources_exist_and_needles", sources_ok, "all 945 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V945_1_prior_944_clean", prior_clean, "P8_Y5_BRR545_944_VALIDATION.csv clean")
    add("V945_2_q_candidate_written", candidate_written, "candidate q projection written")
    add("V945_3_construction_nonclaim", construction_nonclaim, "candidate construction not promoted to descent proof")
    add("V945_4_Obs_e_formal_only", obs_formal, "Obs_e functor remains formal only")
    add("V945_5_kernel_gate_not_passed", kernel_not_passed, "q-kernel ownership not proved")
    add("V945_6_bound_rows_blocked", bounds_blocked, "first frame-leak bound rows remain blocked schemas")
    add("V945_7_next_target_selected", next_selected, "946 q-kernel/null certificate target selected")
    add("V945_8_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V945_9_claim_gates_false", claims_false, "all claim gates remain false")
    add("V945_10_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V945_11_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V945_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    construction_rows: list[dict[str, str]],
    obs_rows: list[dict[str, str]],
    kernel_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 945 - Y5/R10 Parent q-Map Obs_e Functor Construction Or First Frame-Leak Bound Pack

Generated: `{stamp()}`

Status: `Y5_R10_945_q_candidate_Obs_e_written_kernel_ownership_missing_first_frame_leak_bound_rows_ready_nonclaim`

Claim ceiling: `q_candidate_gate_only_no_parent_quotient_claim_no_frame_leak_zero_no_local_GR_pass`

## Result

945 writes the most honest candidate map currently available:

```text
q_candidate(Phi) = (e_obs, [C]_PD, Orbit_27(h), [J_rel]_local, theta_univ, boundary_class_if_owned),
Obs_e(q_candidate) = e_obs.
```

This is useful, but it is **not** enough. If `e_obs` is simply inserted into `q_candidate`, the chain rule becomes a projection-by-declaration trick unless the parent also proves:

```text
ker(Dq_candidate) is presymplectic-null,
i_v Theta_parent = dB_v with zero compact local flux,
Lie_v S_matter = 0,
no marker/Weyl/disformal/mass channel survives in the kernel.
```

So 945 does not sign quotient descent. It narrows the next obstruction: the problem is no longer how to write `q`; the problem is whether `ker(Dq_candidate)` is really gauge/null/matter-invisible in the parent action.

If that certificate fails, the first retained empirical rows are now explicit:

```text
c_g, tau_R10, tau_PPN, b_A, b_dis, q_nonH, Delta_W_support.
```

All remain nonclaim until their parent zero theorem or numeric source/projection exists.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## q-Map Candidate Construction

{md_table(construction_rows, ["construction_id", "object", "role", "mathematical_form", "current_status", "failure_if_used_as_proof"])}

## Obs_e Functor Audit

{md_table(obs_rows, ["audit_id", "case", "mathematical_status", "current_status", "remaining_gap"])}

## Kernel Test

{md_table(kernel_rows, ["kernel_test_id", "direction", "test", "current_status", "failure_gap", "passes_kernel_gate"])}

## First Frame-Leak Bound Rows

{md_table(bound_rows, ["bound_row_id", "symbol", "definition", "current_status", "next_source_action", "observable_link", "score_ready"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def ensure_csv_roundtrip(paths: list[Path]) -> None:
    for path in paths:
        rows = read_csv(path)
        if rows and any(None in row for row in rows):
            raise SystemExit(f"malformed CSV row in {path}")


def main() -> None:
    sources = source_register()
    construction_rows = q_map_candidate_construction()
    obs_rows = obs_e_functor_audit()
    kernel_rows = kernel_test_rows()
    bound_rows = first_frame_leak_bound_rows()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, construction_rows, obs_rows, kernel_rows, bound_rows, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_945_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_945_Q_MAP_CANDIDATE_CONSTRUCTION.csv",
            construction_rows,
            ["construction_id", "object", "role", "mathematical_form", "current_status", "failure_if_used_as_proof", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_945_OBS_E_FUNCTOR_AUDIT.csv",
            obs_rows,
            ["audit_id", "case", "mathematical_status", "current_status", "remaining_gap", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_945_KERNEL_TEST.csv",
            kernel_rows,
            ["kernel_test_id", "direction", "test", "current_status", "failure_gap", "passes_kernel_gate", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
            bound_rows,
            ["bound_row_id", "symbol", "definition", "units", "current_status", "next_source_action", "observable_link", "source_path", "numeric_value", "arena_projection", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_945_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_945_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_945_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_945_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, construction_rows, obs_rows, kernel_rows, bound_rows, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_945_q_candidate_Obs_e_written_kernel_ownership_missing_first_frame_leak_bound_rows_ready_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 946-Y5-R10-q-kernel-presymplectic-null-and-no-marker-certificate-or-cg-ba-bound-row.md")


if __name__ == "__main__":
    main()
