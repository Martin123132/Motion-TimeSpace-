from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "979-Y5-R10-parent-action-spine-superselection-clause-or-first-qbar-prior-source.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
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
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    text = str(value).replace("\n", "<br>")
    return text.replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "978_doc",
            "path": "978-Y5-R10-superselection-parent-sector-or-qbar-source-prior-runner.md",
            "role": "direct 978 handoff and next target",
            "needle": "DEC978_4_best_next",
        },
        {
            "source_id": "978_parent_sector",
            "path": "source-intake/mts_residuals/P8_Y5_R10_978_PARENT_SECTOR_ATTEMPT.csv",
            "role": "superselection/topological mechanism attempt",
            "needle": "PSA978_6_verdict",
        },
        {
            "source_id": "978_topological_kappa",
            "path": "source-intake/mts_residuals/P8_Y5_R10_978_TOPOLOGICAL_KAPPA_AUDIT.csv",
            "role": "topological kappa limitations",
            "needle": "TKA978_5_verdict",
        },
        {
            "source_id": "978_qbar_priors",
            "path": "source-intake/mts_residuals/P8_Y5_R10_978_QBAR_SOURCE_PRIOR_RUNNER_ROWS.csv",
            "role": "nonclaim finite qbar/source prior placeholders",
            "needle": "QSP978_4_species_source_weight",
        },
        {
            "source_id": "453_doc",
            "path": "453-global-coupling-superselection-parent-action-contract.md",
            "role": "older parent topological coupling route",
            "needle": "P1_topological_zero_form",
        },
        {
            "source_id": "452_doc",
            "path": "452-constant-universal-Geff-kappa-identity-attempt.md",
            "role": "Bianchi does not fix local/running kappa alone",
            "needle": "Bianchi_limit",
        },
        {
            "source_id": "448_doc",
            "path": "448-constant-sector-universality-theorem-attempt.md",
            "role": "constant-sector conditional theorem and theta(I_Q) warning",
            "needle": "quotient_invariance_not_overclaimed",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "local alpha3/Gdot boundary sensitivity anchors",
            "needle": "alpha3_flux",
        },
        {
            "source_id": "constant_sector_contract",
            "path": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
            "role": "constant-sector identities C0-C7",
            "needle": "C1_superselection_independence",
        },
        {
            "source_id": "kappa_contract",
            "path": "source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv",
            "role": "constant universal kappa requirements",
            "needle": "CU1_global_coupling_status",
        },
        {
            "source_id": "576_qbar_trigger",
            "path": "source-intake/mts_residuals/P8_Y5_R10_576_QBAR_ENVELOPE_TRIGGER.csv",
            "role": "finite qbar retained when theorem-zero not parent-derived",
            "needle": "QE576_0_qbar_retained",
        },
        {
            "source_id": "576_premise_ledger",
            "path": "source-intake/mts_residuals/P8_Y5_R10_576_UNIVERSALITY_PREMISE_LEDGER.csv",
            "role": "premises needed before qbar theorem-zero",
            "needle": "P576_3_constant_trivial_action",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_action_spine_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PASC979_0_parent_bundle",
            "clause": "parent configuration space is fibred over global constant sectors",
            "mathematical_form": "pi_const: C_parent -> Sigma_const = Theta_rep x K_grav x B_boundary; C_parent = disjoint_union_s C_dyn(s)",
            "derived_result_if_owned": "local MTS dynamics occurs inside a fixed fibre C_dyn(s)",
            "status": "SPINE_CLAUSE_REQUIRED",
            "missing_for_derivation": "parent action has not yet derived pi_const from deeper MTS primitives",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PASC979_1_local_vertical_distribution",
            "clause": "local MTS generators are vertical for the constant-sector projection",
            "mathematical_form": "V_MTS subset ker(D pi_const)",
            "derived_result_if_owned": "for X in V_MTS, X theta_A = 0 and X kappa = 0",
            "status": "RELATIVE_DERIVATION_STEP",
            "missing_for_derivation": "need parent proof that every admissible local variation is tangent to fixed-sector fibres",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PASC979_2_parent_action_functional",
            "clause": "one action owns geometry, topological coupling, matter, and boundary terms",
            "mathematical_form": "S_parent = S_geom[Phi;kappa] + S_top^kappa[kappa,A3] + sum_A S_m[Psi_A,e_obs(Phi);theta_A] + S_boundary",
            "derived_result_if_owned": "all source/coupling bookkeeping lives in one parent variational object",
            "status": "CONTRACT_FORM_READY",
            "missing_for_derivation": "S_geom/e_obs/Phi need final normalization and boundary variational policy",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PASC979_3_theta_representation_data",
            "clause": "matter constants theta_A are representation/superselection data, not local MTS functions",
            "mathematical_form": "theta_A in Rep_A; no admissible map I_loc(Q_MTS,m_A) -> theta_A",
            "derived_result_if_owned": "b_theta and local alpha/mass-ratio drift vanish in the local branch",
            "status": "CLOSURE_UNLESS_PARENT_CATEGORY_PROVEN",
            "missing_for_derivation": "no-marker/no-functor theorem not proven",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PASC979_4_single_gravitational_kappa",
            "clause": "there is one shared gravitational coupling sector, not species-weighted kappa_A",
            "mathematical_form": "K_grav contains kappa only; E_munu = kappa T_munu; not sum_A kappa_A T_A_munu",
            "derived_result_if_owned": "species-source splitting b_kappa is killed",
            "status": "CLOSURE_UNLESS_SUPERSELECTION_PROVEN",
            "missing_for_derivation": "topological d kappa=0 does not by itself forbid many constant kappa_A",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PASC979_5_topological_kappa_zero_form",
            "clause": "topological zero-form term kills local kappa gradients",
            "mathematical_form": "S_top^kappa = int_M A3 wedge d kappa; delta_A3 S_top = 0 gives d kappa = 0",
            "derived_result_if_owned": "range/radius/time running of kappa vanishes on connected local domains",
            "status": "DERIVED_WITHIN_EXTENDED_PARENT_ACTION",
            "missing_for_derivation": "does not fix one-kappa universality, measured-GM calibration, or boundary flux",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PASC979_6_no_marker_functor",
            "clause": "local quotient/material markers cannot select global sectors",
            "mathematical_form": "Hom_alg(A_loc^MTS, Sigma_const) = constants only",
            "derived_result_if_owned": "theta_A(I_Q), kappa(I_Q), and kappa_A(matter-marker) counterexamples are illegal",
            "status": "KEY_UNPROVED_CLAUSE",
            "missing_for_derivation": "need algebra/category theorem or explicit parent-domain axiom",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PASC979_7_boundary_policy",
            "clause": "topological and geometric boundary variations produce no alpha3/local preferred-frame leakage",
            "mathematical_form": "boundary pullback/flux projection P_alpha3(delta S_boundary + delta S_top) = 0",
            "derived_result_if_owned": "K_boundary_alpha3 is zero rather than an empirical prior",
            "status": "NOT_CLOSED",
            "missing_for_derivation": "boundary exchange no-hair/Ward-owned cancellation remains missing",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PASC979_8_relative_theorem",
            "clause": "relative local coupling theorem",
            "mathematical_form": "If PASC979_0...PASC979_7 are parent-owned, then b_theta=0, b_kappa=0, and qbar source rows tied only to these components may be retired",
            "derived_result_if_owned": "constant/coupling part of the local-GR branch becomes theorem-zero",
            "status": "RELATIVE_THEOREM_ONLY",
            "missing_for_derivation": "because PASC979_3, PASC979_4, PASC979_6, and PASC979_7 are not parent-derived, finite priors remain live",
            "valid_for_claim": "false",
        },
    ]


def derivation_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "DGT979_0_define_sector_projection",
            "statement": "Define sector projection pi_const from parent configurations to global constant labels.",
            "proof_status": "conditional_pass",
            "reason": "a fibre-bundle/superselection parent domain can make this mathematically exact",
            "blocks_claim": "true",
        },
        {
            "gate_id": "DGT979_1_kernel_lemma",
            "statement": "If X is an admissible local MTS generator and X in ker(D pi_const), then X theta_A = X kappa = 0.",
            "proof_status": "proved_relative_to_domain",
            "reason": "chain rule: D(theta_A,kappa)(X)=D pi_const(X)=0",
            "blocks_claim": "true",
        },
        {
            "gate_id": "DGT979_2_topological_gradient_lemma",
            "statement": "If S_top^kappa=int A3 wedge d kappa is in the parent action, variation of A3 imposes d kappa=0.",
            "proof_status": "proved_relative_to_extended_action",
            "reason": "delta_A3 S_top gives the local Euler-Lagrange equation d kappa=0",
            "blocks_claim": "true",
        },
        {
            "gate_id": "DGT979_3_one_kappa_universality",
            "statement": "The parent sector contains one shared kappa, not kappa_A or source-class couplings.",
            "proof_status": "not_proven",
            "reason": "a topological zero-form can make each kappa_A constant, but does not force equality",
            "blocks_claim": "true",
        },
        {
            "gate_id": "DGT979_4_no_marker_functor",
            "statement": "No local quotient, memory, class, material, or readout marker can select the sector labels.",
            "proof_status": "not_proven",
            "reason": "theta_A(I_Q) and kappa(I_Q,m) remain legal until the local algebra has no nonconstant maps to Sigma_const",
            "blocks_claim": "true",
        },
        {
            "gate_id": "DGT979_5_measured_GM_calibration",
            "statement": "The constant kappa sector calibrates to the measured Newtonian GM without hidden source normalization drift.",
            "proof_status": "not_proven",
            "reason": "constant kappa is not yet the same as a fully normalized, observed-source Newtonian limit",
            "blocks_claim": "true",
        },
        {
            "gate_id": "DGT979_6_boundary_silence",
            "statement": "Boundary/topological terms do not reintroduce alpha3 or other local preferred-frame leakage.",
            "proof_status": "not_proven",
            "reason": "417 alpha3_flux remains the visible bound if no no-hair/Ward cancellation is derived",
            "blocks_claim": "true",
        },
        {
            "gate_id": "DGT979_7_verdict",
            "statement": "979 parent-action route status.",
            "proof_status": "PARENT_ACTION_SPINE_READY_AS_CLOSURE_NOT_DERIVED_LOCAL_GR",
            "reason": "the clean coupling mechanism is now precise, but core ownership clauses remain closures",
            "blocks_claim": "true",
        },
    ]


def qbar_prior_priority_rows() -> list[dict[str, str]]:
    return [
        {
            "priority_id": "QPRI979_0_b_kappa_species_split",
            "component": "b_kappa",
            "observable_channel": "WEP/source-composition/source-normalization",
            "current_source": "452/448/977 counterexamples",
            "candidate_bound_or_anchor": "MISSING_EXTERNAL_NUMERIC_BOUND",
            "why_priority": "one-kappa universality is the main coupling gap; if not derived, it must be bounded first",
            "status": "source_needed",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "QPRI979_1_kappa_running_Gdot",
            "component": "b_kappa",
            "observable_channel": "orbital/clocks/Gdot",
            "current_source": "417-boundary-exchange-nohair-theorem-attempt.md",
            "candidate_bound_or_anchor": "local anchor row Gdot_drift = 9.600e-15 yr^-1",
            "why_priority": "topological d kappa=0 should kill this; if not parent-owned, this is a direct residual test",
            "status": "local_anchor_exists_needs_source_hardening",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "QPRI979_2_K_boundary_alpha3",
            "component": "boundary_alpha3_flux",
            "observable_channel": "PPN alpha3/preferred-frame",
            "current_source": "417-boundary-exchange-nohair-theorem-attempt.md",
            "candidate_bound_or_anchor": "local anchor row alpha3_flux = 4.000e-20",
            "why_priority": "topological/superselection mechanism does not silence boundary flux by itself",
            "status": "local_anchor_exists_needs_source_hardening",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "QPRI979_3_b_theta_alpha_mass",
            "component": "b_theta",
            "observable_channel": "clock/fine-structure/mass-ratio spectra",
            "current_source": "448 theta_A(I_Q) warning and 978 qbar placeholders",
            "candidate_bound_or_anchor": "MISSING_EXTERNAL_NUMERIC_BOUND",
            "why_priority": "theta_A as representation data is clean, but no-marker functor is still unproved",
            "status": "source_needed",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "QPRI979_4_qbarXT_R10",
            "component": "qbarXT_vec",
            "observable_channel": "R10 short-range / fifth-force alpha(lambda)",
            "current_source": "576 qbar envelope trigger and 978 qbar rows",
            "candidate_bound_or_anchor": "MISSING_PARENT_INPUT and real alpha(lambda) curve still required for claims",
            "why_priority": "finite branch must remain runnable if theorem-zero route fails",
            "status": "source_needed",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE979_0_parent_superselection_derived",
            "claim": "parent superselection sector is derived from MTS primitives",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "979 writes the exact clause, but does not derive the parent category/domain from deeper primitives",
        },
        {
            "gate_id": "CGATE979_1_btheta_bkappa_zero",
            "claim": "b_theta and b_kappa are theorem-zero",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "kernel lemma is relative; no-marker functor and one-kappa universality remain unsigned",
        },
        {
            "gate_id": "CGATE979_2_boundary_alpha3_zero",
            "claim": "K_boundary_alpha3 is zero",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "topological kappa does not automatically silence boundary flux",
        },
        {
            "gate_id": "CGATE979_3_local_GR_or_R10_pass",
            "claim": "local-GR/R10/PPN branch passes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "constant/coupling spine is not enough; finite qbar and boundary priors remain live",
        },
        {
            "gate_id": "CGATE979_4_qbar_rows_retired",
            "claim": "finite qbar/source prior rows may be removed",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "576 finite branch rule remains active unless all theorem-zero premises are parent-derived",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC979_0_parent_spine",
            "topic": "coupling mechanism",
            "result": "exact_parent_action_clause_written",
            "reason": "theta_A and one kappa can be made constant by a sector projection plus local verticality",
            "next_action": "attack no-marker sector functor theorem or demote the clause to explicit closure",
        },
        {
            "decision_id": "DEC979_1_topological_kappa",
            "topic": "kappa gradients",
            "result": "d_kappa_zero_relative_to_extended_action",
            "reason": "A3 zero-form term gives d kappa=0, but does not prove one species-blind kappa",
            "next_action": "separate gradient-zero from universality-zero in the parent spine",
        },
        {
            "decision_id": "DEC979_2_theta_constants",
            "topic": "matter constants",
            "result": "representation_data_route_clean_but_unowned",
            "reason": "placing theta_A in Rep_A is mathematically clean, but local marker functors remain possible",
            "next_action": "try a no-marker functor theorem for local observable algebra",
        },
        {
            "decision_id": "DEC979_3_finite_priors",
            "topic": "empirical fallback",
            "result": "finite_qbar_source_priority_written",
            "reason": "if the no-marker/one-kappa route fails, b_kappa, Gdot, alpha3, b_theta, and qbarXT need sourced finite priors",
            "next_action": "first acquire/source b_kappa_species_split or Gdot/alpha3 anchors",
        },
        {
            "decision_id": "DEC979_4_best_next",
            "topic": "next checkpoint",
            "result": "no_marker_sector_functor_theorem_or_first_qbar_source",
            "reason": "this is now the shortest route to either theorem-zero or honest empirical fallback",
            "next_action": "write 980 no-marker sector functor theorem attempt, else begin first numeric qbar/source prior acquisition",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "980-Y5-R10-no-marker-sector-functor-theorem-or-first-qbar-source-acquisition.md",
            "objective": "prove that local MTS/quotient/material observables admit no nonconstant functor to global sector labels; if this fails, source the first finite b_kappa/qbar prior",
            "include": "local observable algebra, sector-label target Sigma_const, Hom_alg(A_loc,Sigma_const)=Const gate, kappa_A/theta(I_Q) counterexamples, finite-prior fallback",
            "exclude": "local-GR claim, qbar theorem-zero, invented numeric bounds, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_ts = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_ts:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    spine_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    priority_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_paths_ok = all(row["exists"] == "true" for row in sources)
    source_needles_ok = all(row["needle_found"] == "true" for row in sources)
    relative_theorem_ok = any(
        row["clause_id"] == "PASC979_8_relative_theorem"
        and row["status"] == "RELATIVE_THEOREM_ONLY"
        for row in spine_rows
    )
    derivation_verdict_ok = any(
        row["gate_id"] == "DGT979_7_verdict"
        and row["proof_status"] == "PARENT_ACTION_SPINE_READY_AS_CLOSURE_NOT_DERIVED_LOCAL_GR"
        and row["blocks_claim"] == "true"
        for row in derivation_rows
    )
    priority_nonclaim_ok = all(row["valid_for_claim"] == "false" for row in priority_rows)
    claims_blocked_ok = all(
        row["gate_pass"] == "false" and row["claim_allowed"] == "false"
        for row in claim_rows
    )
    decisions_ok = any(
        row["decision_id"] == "DEC979_4_best_next"
        and row["result"] == "no_marker_sector_functor_theorem_or_first_qbar_source"
        for row in decision_rows_
    )
    target_ok = bool(target_rows) and target_rows[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {
            "check_id": "V979_0_source_paths_exist",
            "result": "pass" if source_paths_ok else "fail",
            "detail": "all cited local source paths exist" if source_paths_ok else "one or more cited local source paths are missing",
        },
        {
            "check_id": "V979_1_source_needles_found",
            "result": "pass" if source_needles_ok else "fail",
            "detail": "all source needles found" if source_needles_ok else "one or more source needles are missing",
        },
        {
            "check_id": "V979_2_relative_theorem_only",
            "result": "pass" if relative_theorem_ok else "fail",
            "detail": "relative parent-action theorem is explicitly nonclaim",
        },
        {
            "check_id": "V979_3_derivation_verdict_blocks_claim",
            "result": "pass" if derivation_verdict_ok else "fail",
            "detail": "derivation gate records closure-not-local-GR status",
        },
        {
            "check_id": "V979_4_qbar_prior_priority_nonclaim",
            "result": "pass" if priority_nonclaim_ok else "fail",
            "detail": "all finite-prior priority rows remain valid_for_claim=false",
        },
        {
            "check_id": "V979_5_claim_gates_false",
            "result": "pass" if claims_blocked_ok else "fail",
            "detail": "all parent-superselection/local-GR/qbar-retirement claims remain blocked",
        },
        {
            "check_id": "V979_6_decision_next_target",
            "result": "pass" if decisions_ok else "fail",
            "detail": "980 no-marker sector functor or first qbar source selected",
        },
        {
            "check_id": "V979_7_next_target_written",
            "result": "pass" if target_ok else "fail",
            "detail": "next target row is present and nonclaim",
        },
        {
            "check_id": "V979_8_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
        },
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V979_READY",
            "result": "pass" if ready else "fail",
            "detail": "979 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    spine_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    priority_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> None:
    lines = [
        "# 979 Y5 R10: Parent Action Spine Superselection Clause Or First Qbar Prior Source",
        "",
        "Status: `Y5_R10_979_parent_action_spine_clause_written_as_relative_theorem_not_derived_local_GR_finite_priors_retained`",
        "",
        "Claim ceiling: this checkpoint does not claim parent superselection is derived, does not retire finite `qbar` rows, does not prove `b_theta=b_kappa=0`, and does not claim R10/PPN/local-GR pass.",
        "",
        "## Readout",
        "",
        "This checkpoint turns the coupling intuition into a sharp parent-action clause. The clean mathematical move is:",
        "",
        "`pi_const: C_parent -> Sigma_const = Theta_rep x K_grav x B_boundary`",
        "",
        "with admissible local MTS generators restricted by:",
        "",
        "`V_MTS subset ker(D pi_const)`.",
        "",
        "Then the kernel lemma is immediate: for every local generator `X`, `X theta_A = 0` and `X kappa = 0`. This is the good news. The catch is also now exact: unless the parent action derives the projection and proves the no-marker functor, the result is a closure clause, not a completed derivation.",
        "",
        "For `kappa`, a topological zero-form term gives the cleanest gradient-killing mechanism:",
        "",
        "`S_top^kappa = int_M A3 wedge d kappa`.",
        "",
        "Varying `A3` gives `d kappa = 0` on connected local domains. But this does not by itself prove there is only one species-blind `kappa`, does not forbid `kappa_A`, does not calibrate measured `GM`, and does not close boundary `alpha3` flux.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Parent Action Spine Clauses",
        "",
        md_table(spine_rows, ["clause_id", "clause", "status", "derived_result_if_owned", "missing_for_derivation", "valid_for_claim"]),
        "",
        "## Derivation Gate",
        "",
        md_table(derivation_rows, ["gate_id", "statement", "proof_status", "reason", "blocks_claim"]),
        "",
        "## Qbar / Coupling Prior Priority",
        "",
        md_table(priority_rows, ["priority_id", "component", "observable_channel", "candidate_bound_or_anchor", "why_priority", "status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claim_rows, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "topic", "result", "reason", "next_action"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    spine = parent_action_spine_rows()
    derivation = derivation_gate_rows()
    priorities = qbar_prior_priority_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    targets = next_target_rows()
    validation = validation_rows(sources, spine, derivation, priorities, claims, decisions, targets)

    write_csv(OUT / "P8_Y5_R10_979_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_979_PARENT_ACTION_SPINE_CLAUSE.csv", spine)
    write_csv(OUT / "P8_Y5_R10_979_DERIVATION_GATE.csv", derivation)
    write_csv(OUT / "P8_Y5_R10_979_QBAR_PRIOR_SOURCE_PRIORITY.csv", priorities)
    write_csv(OUT / "P8_Y5_R10_979_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_979_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_979_NEXT_TARGET.csv", targets)
    write_csv(OUT / "P8_Y5_BRR545_979_VALIDATION.csv", validation)
    write_doc(sources, spine, derivation, priorities, claims, decisions, validation, targets)


if __name__ == "__main__":
    main()
