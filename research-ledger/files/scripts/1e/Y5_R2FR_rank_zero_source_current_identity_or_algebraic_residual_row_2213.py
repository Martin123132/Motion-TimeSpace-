from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2213"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2213-Y5-R2FR-rank-zero-source-current-identity-or-algebraic-residual-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2213_SOURCE_REGISTER.csv",
    "theorem_attempt": OUT / "P8_Y5_PARENT_QLOC_2213_RANK_ZERO_SOURCE_CURRENT_THEOREM_ATTEMPT.csv",
    "clause_audit": OUT / "P8_Y5_PARENT_QLOC_2213_JA_BA_DQZ_CLAUSE_AUDIT.csv",
    "algebraic_residual": OUT / "P8_Y5_PARENT_QLOC_2213_ALGEBRAIC_RESIDUAL_ROW.csv",
    "arena_blocker": OUT / "P8_Y5_PARENT_QLOC_2213_ARENA_PROJECTION_BLOCKER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2213_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2213_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2213_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2213_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2213_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2213_ALGEBRAIC_RESIDUAL_COEFFICIENTS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2213_RANK_ZERO_SOURCE_CURRENT_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_RANK_ZERO_SOURCE_CURRENT_2213_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2213_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2213-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2213*",
        "*P8_Y5_BRR545_2213*",
        "*Y5_R2FR_rank_zero_source_current_identity_or_algebraic_residual_row_2213*",
        "*JR2213*",
        "*PARENT_QLOC_RANK_ZERO_SOURCE_CURRENT_2213*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2212_rank_zero_handoff",
            ROOT / "2212-Y5-R2FR-principal-symbol-ZAB-owner-or-rank-zero-constraint-proof.md",
            ["NEXT2212_0_2213", "RZC2212_1_source_current_zero", "VAL2212_OVERALL"],
            "2212 selects the strict rank-zero source-current identity as the next derivation target.",
        ),
        (
            "2212_rank_zero_contract",
            OUT / "P8_Y5_PARENT_QLOC_2212_RANK_ZERO_CONSTRAINT_CONTRACT.csv",
            ["RZC2212_0_algebraic_euler", "RZC2212_5_verdict", "PROMISING_ROUTE_NOT_CLAIMED"],
            "machine-readable rank-zero contract: algebraic Euler plus J_A/B_A/Dq_Z blockers.",
        ),
        (
            "1011_source_current",
            ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
            ["RDT1011_3_source_current_zero", "RDT1011_4_boundary_zero", "V1011_SUMMARY"],
            "source-current and boundary zero remain conditional, not parent-signed.",
        ),
        (
            "1675_descent_doc",
            ROOT / "1675-Y5-R2FR-constraint-first-Z-elimination-and-coframe-source-descent.md",
            ["CFD1675_4_source_readout", "LEAK1675_5_residual_lock", "VAL1675_OVERALL"],
            "Dq_Z descent route failed current proof and emitted surviving leak vector.",
        ),
        (
            "1675_leak_vector",
            OUT / "P8_Y5_PARENT_QLOC_1675_SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv",
            ["LEAK1675_0_coframe", "LEAK1675_4_boundary", "LEAK1675_5_residual_lock"],
            "surviving Dq_Z leak components to be carried into the algebraic residual row.",
        ),
        (
            "1620_chain_rule",
            OUT / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv",
            ["CR1620_1_zero_lemma", "CR1620_3_pre_action_countermodel", "CHAIN_RULE_THEOREM_CLOSED_APPLICATION_BLOCKED"],
            "exact chain-rule zero lemma exists, but its MTS application is blocked.",
        ),
        (
            "1620_bridge",
            OUT / "P8_Y5_PARENT_QLOC_1620_PARENT_SIGNATURE_BRIDGE_CONTRACT.csv",
            ["BRC1620_2_matter_descent", "BRC1620_4_boundary_silence", "PARENT_SIGNATURE_BRIDGE_NOT_CLOSED"],
            "parent signature bridge lists verticality, matter descent, no-marker, boundary and PPN lock gaps.",
        ),
        (
            "1666_blockers",
            OUT / "P8_Y5_PARENT_QLOC_1666_BLOCKER_MATRIX.csv",
            ["BLK1666_3_matter_descent", "BLK1666_6_boundary_projector", "BLK1666_8_verdict"],
            "blocker matrix confirms matter descent, boundary/projector, and no-mode theorem are still open.",
        ),
        (
            "761_matter_vertical_action",
            OUT / "P8_Y5_R10_761_PARENT_MATTER_VERTICAL_ACTION_CONTRACT.csv",
            ["MVA761_1_fixed_Psi_vertical_action", "MVA761_4_boundary_of_matter_domain", "MVA761_5_evaluability_verdict"],
            "matter vertical action is admissible as a contract, not yet parent-constructed.",
        ),
        (
            "1045_matter_functor",
            OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            ["MFS1045_1_observed_coframe_functor", "MFS1045_4_no_shadow_frame", "MFS1045_6_verdict"],
            "sufficient matter functor signature exists but is not parent-signed.",
        ),
        (
            "1229_source_coupling",
            OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
            ["THM1229_1_iff", "THM1229_2_countermodel", "THM1229_3_residual_vector"],
            "universal source coupling iff condition and residual vector are symbolic only.",
        ),
        (
            "1023_coupling_descent",
            OUT / "P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv",
            ["CDA1023_0_metric_chain_rule", "CDA1023_3_projector_boundary", "CDA1023_4_verdict"],
            "metric chain-rule can pass conditionally, but constants, hidden frames and boundary/projector remain live.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            theorem_id="RZS2213_0_strict_euler_identity",
            theorem_piece="strict rank-zero Euler identity",
            mathematical_statement="On the strict fixed-L0 branch with no Z_AB principal symbol, the eliminated local coordinate obeys M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector.",
            derivation_status="EXACT_CONDITIONAL_NORMAL_FORM",
            proof_effect="replaces the false Yukawa-range language with an algebraic source-balance equation.",
            missing_for_current_MTS="parent-owned M_AB signature, source split, boundary split, CDB split, and readout/source projection units.",
            verdict="usable as private theorem skeleton only",
        ),
        base_row(
            theorem_id="RZS2213_1_chain_rule_zero_condition",
            theorem_piece="source-current zero condition",
            mathematical_statement="If Dq[v_Z]=0, Lie_v theta=0, direct source vertices vanish, and boundary/projector terms are zero or proper, then J_A=delta_Z S_matter=0.",
            derivation_status="IMPORTABLE_CONDITIONAL_LEMMA",
            proof_effect="1011/1620 give the correct route: source-current zero follows by descent and chain rule, not by assuming a plateau.",
            missing_for_current_MTS="verticality, matter descent, no-marker/current-owner theorem, and boundary projector silence are unsigned together.",
            verdict="mathematically good but not fired",
        ),
        base_row(
            theorem_id="RZS2213_2_rank_zero_silence_theorem",
            theorem_piece="local invisibility theorem",
            mathematical_statement="If M_AB is invertible on physical quotient directions and J_A=B_A=C_A^CDB=R_A^src/readout/projector=0 with Dq_Z=0, then Z^A=0 and all observed local residuals vanish.",
            derivation_status="CONDITIONAL_THEOREM_WRITTEN",
            proof_effect="this is the clean GR/Newton route for the strict branch: algebraic elimination plus observed descent.",
            missing_for_current_MTS="M_AB lock, J_A=0, B_A=0, Dq_Z=0, CDB silence and arena projections are all not parent-signed.",
            verdict="not claimable",
        ),
        base_row(
            theorem_id="RZS2213_3_current_application_failure",
            theorem_piece="current MTS application",
            mathematical_statement="Current corpus cannot set the right-hand side of M_AB Z^B to zero because source, boundary, CDB and readout terms remain live.",
            derivation_status="APPLICATION_BLOCKED",
            proof_effect="prevents smuggling a local-GR pass through the strict branch.",
            missing_for_current_MTS="the exact blockers are carried in the 2213 clause audit and algebraic residual row.",
            verdict="write residual row instead of claiming zero",
        ),
        base_row(
            theorem_id="RZS2213_4_verdict",
            theorem_piece="2213 theorem verdict",
            mathematical_statement="The local-vacuum plateau can be replaced by an algebraic rank-zero theorem, but only conditionally. Current MTS must carry R_alg until the source/boundary/descent clauses close.",
            derivation_status="DERIVED_CONDITIONAL_ROUTE_RESIDUAL_RETAINED",
            proof_effect="one real leap forward: the missing object is no longer vague; it is a finite algebraic residual/source coefficient pack.",
            missing_for_current_MTS="parent coefficients and arena projection maps.",
            verdict="promote algebraic residual coefficient map next",
        ),
    ]


def clause_audit_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            clause_id="JBD2213_0_M_lock",
            required_clause="M_AB invertible or projector-owned on physical quotient directions",
            current_evidence="2211/2212 identify M_AB as algebraic Hessian candidate only.",
            status="MISSING_PARENT_SIGNATURE",
            if_closed="Z=(M^-1)source is well-defined, or null directions are removed as gauge/constraints.",
            if_open="null/wrong-sign algebraic branches can survive as local residuals.",
            next_action="derive M_AB from parent quadratic action with rank/sign/units/eigenbasis.",
        ),
        base_row(
            clause_id="JBD2213_1_J_zero",
            required_clause="J_A=0 for ordinary matter/source normalization/readouts along eliminated Z directions",
            current_evidence="1011 and 1620 provide a conditional chain-rule lemma but mark current application blocked.",
            status="BLOCKED_NONCLAIM",
            if_closed="matter cannot source the eliminated local coordinate.",
            if_open="Z=(M^-1)J creates a local PPN/source-normalization residual.",
            next_action="derive parent matter descent plus no source-only weights/no marker theorem.",
        ),
        base_row(
            clause_id="JBD2213_2_B_zero",
            required_clause="B_A=0 for boundary, source-worldtube, corner, reference and local projector terms",
            current_evidence="1675/1023/1666 keep boundary/projector source-measure terms open.",
            status="BOUNDARY_PROJECTOR_OPEN",
            if_closed="bulk algebraic elimination cannot be re-sourced by edges.",
            if_open="compact local tests can see an edge/projector charge even with Z_AB=0.",
            next_action="split proper-collar boundary zero from source-worldtube/corner/reference residuals.",
        ),
        base_row(
            clause_id="JBD2213_3_DqZ_zero",
            required_clause="Dq_Z=0 after constraint elimination for coframe, metric, measure, source and readouts",
            current_evidence="1675 failed to sign coframe/source/readout/boundary descent and emitted LEAK1675 rows.",
            status="DESCENT_THEOREM_NOT_CLOSED",
            if_closed="observed arenas cannot see the eliminated Z even if parent variables move.",
            if_open="R_alg feeds PPN/R10/WEP/clock/orbit through Dq_Z leak vector.",
            next_action="attempt Dq_Z source/readout descent or fill finite projection coefficients.",
        ),
        base_row(
            clause_id="JBD2213_4_CDB_silence",
            required_clause="C_A^CDB=0 or bounded for K_conn, K_domain, K_boundary and K_comm",
            current_evidence="2212 holds CDB as the only remaining possible hidden derivative/source owner.",
            status="LIVE_PARALLEL_BLOCKER",
            if_closed="strict rank-zero branch remains algebraic with no hidden principal symbol.",
            if_open="finite-range or derivative residual branch can reopen outside strict algebraic closure.",
            next_action="run CDB principal-symbol/source split after algebraic residual map is staged.",
        ),
        base_row(
            clause_id="JBD2213_5_source_readout_descent",
            required_clause="ordinary matter, constants, clock/EM standards, source weights and readout maps descend through Q_vis",
            current_evidence="761/1045/1229 show clean contracts but no parent-signed ordinary-matter functor/action-scale theorem.",
            status="MATTER_SOURCE_READOUT_DESCENT_UNSIGNED",
            if_closed="J_A and observed projection pieces collapse together.",
            if_open="species weights, markers or hidden frames can mimic a residual force.",
            next_action="derive parent object-language/current-owner theorem or retain each coefficient.",
        ),
        base_row(
            clause_id="JBD2213_6_verdict",
            required_clause="all rank-zero silence clauses close in one parent branch",
            current_evidence="no current source closes M_AB lock, J_A, B_A, Dq_Z, CDB and arena projection together.",
            status="ZERO_THEOREM_NOT_CLOSED",
            if_closed="strict local GR/Newton route becomes serious.",
            if_open="use algebraic residual coefficient map, no local-GR/Newton claim.",
            next_action="2214 algebraic residual coefficient map or Dq_Z source descent proof.",
        ),
    ]


def algebraic_residual_rows() -> list[dict[str, Any]]:
    source_paths = "; ".join(
        [
            str(OUTPUTS["clause_audit"]),
            str(OUT / "P8_Y5_PARENT_QLOC_1675_SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv"),
            str(OUT / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv"),
            str(OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv"),
        ]
    )
    return [
        base_row(
            residual_id="RALG2213_0_eliminated_coordinate",
            residual_object="strict rank-zero eliminated coordinate Z^A",
            symbolic_formula="Z^A = (M^-1)^{AB}(J_B + B_B + C_B^CDB + R_B^src/readout/projector) when M is invertible on quotient directions",
            singular_case_formula="Z^A = (M^+)^{AB}S_B + Z_null^A with P_null S=0 required; otherwise null branch is physical residual",
            units="Z_units_from_parent_basis",
            source_paths=source_paths,
            status="SYMBOLIC_NONCLAIM_RESIDUAL",
            required_numeric_inputs="M_AB rank/sign/units; J_A; B_A; C_A^CDB; source/readout projection coefficients",
            arena_links="PPN;Newton_limit;WEP;R10;clock;EM;orbital;R11",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="RALG2213_1_observed_residual_vector",
            residual_object="observable local residual R_obs^I",
            symbolic_formula="R_obs^I = L^I_A (M^-1)^{AB}(J_B + B_B + C_B^CDB + R_B^src/readout/projector) + E^I_DqZ",
            singular_case_formula="replace M^-1 by M^+ and add L^I_A Z_null^A unless parent projector removes null directions",
            units="arena_dependent_units",
            source_paths=source_paths,
            status="SYMBOLIC_NONCLAIM_PROJECTION",
            required_numeric_inputs="L^I_A arena projection; E^I_DqZ leak map; arena bounds and units",
            arena_links="gamma;beta;alpha_i;xi;Gdot;source_GM;R10_alpha;clock_drift;orbit_precession",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="RALG2213_2_source_current_piece",
            residual_object="J_A source-current piece",
            symbolic_formula="J_A = delta_Z S_matter = D Sbar.Dq_Z + J_theta Lie_Z theta + J_direct[Z] + delta_Z B_matter",
            singular_case_formula="J_A=0 only if all chain-rule premises close; otherwise keep finite J_A coefficient rows",
            units="action_variation_per_Z",
            source_paths=source_paths,
            status="SOURCE_CURRENT_ZERO_BLOCKED",
            required_numeric_inputs="matter descent; theta/no-marker silence; direct vertex list; boundary matter term",
            arena_links="Newton_limit;WEP;R10;clocks;EM",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="RALG2213_3_boundary_projector_piece",
            residual_object="B_A boundary/projector piece",
            symbolic_formula="B_A = B_A^proper + B_A^worldtube + B_A^corner + B_A^reference + [P_loc,D]A",
            singular_case_formula="proper compact-collar zero may remove B_A^proper only; source/projector pieces require proof or bounds",
            units="action_variation_boundary_per_Z",
            source_paths=source_paths,
            status="BOUNDARY_PROJECTOR_OPEN",
            required_numeric_inputs="boundary primitive; compact support rule; source-worldtube/corner/reference coefficients; projector commutator",
            arena_links="R10;WEP;orbital;source_measure",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="RALG2213_4_DqZ_leak_piece",
            residual_object="E^I_DqZ observed descent leak",
            symbolic_formula="E^I_DqZ = Pi_coframe^I Dq_Z[e,g,mu,D] + Pi_source^I Dq_Z[J_H] + Pi_readout^I Dq_Z[O_i] + Pi_boundary^I Dq_Z[B_edge,P_loc,Q_X]",
            singular_case_formula="if Dq_Z=0 theorem closes, this row collapses; otherwise every arena needs finite projection coefficients",
            units="arena_dependent_units",
            source_paths=source_paths,
            status="DESCENT_LEAK_RETAINED",
            required_numeric_inputs="LEAK1675 coefficient map, source/readout/coframe projections, arena units",
            arena_links="PPN;R10;WEP;clock;EM;orbital;R11",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="RALG2213_5_verdict",
            residual_object="strict-branch algebraic residual pack",
            symbolic_formula="R_alg is the correct nonclaim object until J_A=B_A=CDB_A=R_A=0 and Dq_Z=0 are parent-signed.",
            singular_case_formula="null/projector cases must be handled before any local-GR claim",
            units="mixed_symbolic",
            source_paths=source_paths,
            status="STAGED_FOR_2214_COEFFICIENT_MAP",
            required_numeric_inputs="coefficient source paths and arena projection maps",
            arena_links="all local tests",
            score_ready=False,
            valid_prediction_row=False,
        ),
    ]


def arena_blocker_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            arena_id="APB2213_0_Newton",
            arena="Newton/source-normalized GM",
            required_projection="Delta(GM)_obs or q_source^nu from R_alg",
            current_blocker="source weights/action scale and measured Hamiltonian mass descent unsigned",
            symbolic_map="Delta_GM ~ Pi_source M^-1 (J+B+CDB+R)",
            next_input_needed="single action scale/current-owner theorem or finite source coefficient rows",
            score_ready=False,
        ),
        base_row(
            arena_id="APB2213_1_PPN",
            arena="PPN gamma,beta,alpha_i,xi,Gdot",
            required_projection="weak-field metric solution sourced by R_alg",
            current_blocker="L^I_A and Dq_Z readout projection not derived",
            symbolic_map="Delta_PPN^I = L^I_A M^-1 S_A + E^I_DqZ",
            next_input_needed="linearized field equations and residual-to-PPN map",
            score_ready=False,
        ),
        base_row(
            arena_id="APB2213_2_R10",
            arena="short-range/R10",
            required_projection="finite force or alpha(lambda) only if live CDB supplies a range; strict branch needs contact/algebraic projection",
            current_blocker="strict branch has no lambda; algebraic contact/source coefficient not mapped",
            symbolic_map="alpha_R10 not legal for strict branch unless CDB reopens Z_AB",
            next_input_needed="CDB principal-symbol extraction or algebraic/contact residual bound",
            score_ready=False,
        ),
        base_row(
            arena_id="APB2213_3_WEP",
            arena="WEP/composition dependence",
            required_projection="species-dependent component of R_alg",
            current_blocker="no-marker/species-weight theorem not parent-signed",
            symbolic_map="eta_AB ~ Pi_WEP M^-1 (Delta J_species + Delta marker)",
            next_input_needed="ordinary matter functor plus source-weight silence or composition coefficient rows",
            score_ready=False,
        ),
        base_row(
            arena_id="APB2213_4_clocks_EM",
            arena="clocks/EM/fine-structure",
            required_projection="Lie_Z theta_A and readout-standard drift",
            current_blocker="constants/superselection and hidden frame silence unsigned",
            symbolic_map="Delta clock/alpha_EM ~ Pi_theta Lie_Z(theta) + Pi_readout M^-1 S",
            next_input_needed="constant/no-marker theorem or clock/EM coefficient bounds",
            score_ready=False,
        ),
        base_row(
            arena_id="APB2213_5_orbital",
            arena="orbital/local dynamics",
            required_projection="perihelion, ephemeris, binary timing or compact source residual from R_alg",
            current_blocker="boundary/worldtube/source-measure terms and weak-field residual map open",
            symbolic_map="Delta_orbit ~ Pi_orb M^-1 (J+B+CDB+R)",
            next_input_needed="local weak-field solution plus source-worldtube coefficient rows",
            score_ready=False,
        ),
        base_row(
            arena_id="APB2213_6_R11",
            arena="non-EH/R11 operator family",
            required_projection="operator vector generated by algebraic elimination",
            current_blocker="operator basis and units not connected to R_alg",
            symbolic_map="c_GK^I ~ Pi_R11^I M^-1 S",
            next_input_needed="operator basis map and EFT dimensions",
            score_ready=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2213_0_theorem_skeleton",
            gate="rank-zero algebraic silence theorem written",
            status="PASS_NONCLAIM",
            reason="conditional theorem is explicit and does not rely on a plateau axiom.",
        ),
        base_row(
            gate_id="CG2213_1_current_application",
            gate="current MTS fires J_A=B_A=CDB=R=0 and Dq_Z=0",
            status="BLOCKED_NONCLAIM",
            reason="all source-facing clauses are not parent-signed together.",
        ),
        base_row(
            gate_id="CG2213_2_algebraic_residual",
            gate="algebraic residual row staged",
            status="PASS_NONCLAIM",
            reason="R_alg row is written with source paths, arenas, and required numeric inputs.",
        ),
        base_row(
            gate_id="CG2213_3_R10",
            gate="strict branch R10 alpha(lambda) claim",
            status="REJECTED_FOR_STRICT_BRANCH",
            reason="strict branch has no principal symbol and therefore no lambda; R10 remains only for live CDB or contact residual bounds.",
        ),
        base_row(
            gate_id="CG2213_4_local_GR_Newton",
            gate="local GR/Newton reduction claim",
            status="BLOCKED_NONCLAIM",
            reason="source-current, boundary, observed descent and arena projection are still open.",
        ),
        base_row(
            gate_id="CG2213_5_public",
            gate="GitHub/public update",
            status="BLOCKED_NONCLAIM",
            reason="private derivation checkpoint only.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2213_0_gain",
            decision="PLATEAU_AXIOM_REPLACED_BY_RANK_ZERO_CONDITIONAL_THEOREM",
            rationale="the strict branch can be stated as M_AB Z^B=S_A, with silence following only when S_A and Dq_Z vanish.",
            next_action="use the theorem skeleton, but do not claim it fires.",
        ),
        base_row(
            decision_id="DEC2213_1_failure",
            decision="ZERO_PROOF_DOES_NOT_CLOSE_CURRENT_CORPUS",
            rationale="J_A, B_A, Dq_Z, CDB, source/readout and M_AB lock remain unsigned in one parent branch.",
            next_action="carry an explicit algebraic residual row.",
        ),
        base_row(
            decision_id="DEC2213_2_best_next",
            decision="ALGEBRAIC_RESIDUAL_COEFFICIENT_MAP_NEXT",
            rationale="the missing object is now concrete: M^-1 times source/boundary/CDB/readout pieces, projected into arenas.",
            next_action="try to derive Dq_Z/source descent again; if it fails, fill finite coefficient acquisition rows.",
        ),
        base_row(
            decision_id="DEC2213_3_scope",
            decision="NO_GITHUB_NO_LOCAL_CLAIM",
            rationale="this is a private derivation discipline checkpoint, not a public result.",
            next_action="keep all rows valid_for_claim=false.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2213_0_2214",
            selection_status="selected",
            target_file="2214-Y5-R2FR-algebraic-residual-coefficient-map-or-DqZ-source-descent-proof.md",
            target_script="scripts/Y5_R2FR_algebraic_residual_coefficient_map_or_DqZ_source_descent_proof_2214.py",
            objective="derive or source the coefficient map R_obs^I=L^I_A M^-1(J+B+CDB+R)+E_DqZ for Newton/PPN/R10/WEP/clock/orbital arenas; if Dq_Z/source descent closes, collapse rows to theorem-zero.",
            success_condition="either one source/readout descent clause becomes parent-signed or every surviving algebraic residual component gets a finite nonclaim coefficient acquisition row.",
            do_not_do="do not claim local GR/Newton, do not run alpha(lambda) for the strict branch, do not push GitHub.",
        ),
        base_row(
            route_id="NEXT2213_1_CDB_parallel",
            selection_status="held_parallel",
            target_file="2213b-Y5-R2FR-CDB-principal-symbol-extraction.md",
            target_script="scripts/Y5_R2FR_CDB_principal_symbol_extraction_2213b.py",
            objective="separate K_conn/K_domain/K_boundary/K_comm into kinetic principal-symbol pieces versus algebraic/source/boundary leakage.",
            success_condition="CDB table tells whether finite-range route reopens or only adds terms to R_alg.",
            do_not_do="do not delete CDB by strict branch algebra alone.",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["algebraic_residual"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["clause_audit"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["theorem_attempt"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        copied = False
        parse_ok = False
        count = 0
        if source.exists():
            shutil.copyfile(source, target)
            copied = True
            parse_ok, count, _ = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=copied,
                parse_ok=parse_ok,
                row_count=count,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    clause_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    add("VAL2213_00_sources_exist", all(truthy(row.get("path_exists")) for row in source_rows), f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2213_01_needles_found", all(truthy(row.get("needles_found")) for row in source_rows), f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    theorem_ok = any(row.get("theorem_id") == "RZS2213_2_rank_zero_silence_theorem" and row.get("derivation_status") == "CONDITIONAL_THEOREM_WRITTEN" for row in theorem_rows)
    theorem_ok = theorem_ok and any(row.get("theorem_id") == "RZS2213_3_current_application_failure" and row.get("derivation_status") == "APPLICATION_BLOCKED" for row in theorem_rows)
    add("VAL2213_02_theorem_attempt", theorem_ok, "rank-zero theorem skeleton written and current application blocked")

    clause_ids = {row.get("clause_id") for row in clause_rows}
    required_clause_ids = {"JBD2213_0_M_lock", "JBD2213_1_J_zero", "JBD2213_2_B_zero", "JBD2213_3_DqZ_zero", "JBD2213_4_CDB_silence", "JBD2213_5_source_readout_descent", "JBD2213_6_verdict"}
    add("VAL2213_03_clause_audit", required_clause_ids <= clause_ids, "J_A/B_A/Dq_Z/CDB/source-readout/M lock clauses audited")

    residual_ok = any(row.get("residual_id") == "RALG2213_0_eliminated_coordinate" and "M^-1" in str(row.get("symbolic_formula")) for row in residual_rows)
    residual_ok = residual_ok and any(row.get("residual_id") == "RALG2213_1_observed_residual_vector" and "R_obs" in str(row.get("residual_object")) for row in residual_rows)
    residual_ok = residual_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in residual_rows)
    add("VAL2213_04_algebraic_residual", residual_ok, "symbolic nonclaim algebraic residual row staged with no scoring flags")

    arena_ok = len(arena_rows) == 7 and all(not truthy(row.get("score_ready")) for row in arena_rows)
    add("VAL2213_05_arena_blockers", arena_ok, "Newton/PPN/R10/WEP/clock/orbital/R11 projections remain blocked and named")

    claim_ok = any(row.get("gate_id") == "CG2213_3_R10" and row.get("status") == "REJECTED_FOR_STRICT_BRANCH" for row in claim_rows)
    claim_ok = claim_ok and any(row.get("gate_id") == "CG2213_4_local_GR_Newton" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2213_06_claim_gate", claim_ok, "R10 strict branch rejected and local-GR/Newton remains blocked")

    decision_ok = any(row.get("decision") == "ALGEBRAIC_RESIDUAL_COEFFICIENT_MAP_NEXT" for row in decision_rows_)
    add("VAL2213_07_decision", decision_ok, "decision ledger selects algebraic residual coefficient map next")

    next_ok = any(
        row.get("route_id") == "NEXT2213_0_2214"
        and (
            "algebraic" in str(row.get("objective")).lower()
            or "algebraic" in str(row.get("target_file")).lower()
        )
        for row in next_rows
    )
    add("VAL2213_08_next_target", next_ok, "2214 algebraic residual coefficient map selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2213_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in copy_rows)
    add("VAL2213_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in copy_rows))

    generated_groups = [source_rows, theorem_rows, clause_rows, residual_rows, arena_rows, claim_rows, decision_rows_, next_rows, copy_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2213_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    no_missing_promoted = all(
        not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row"))
        for row in residual_rows
    ) and all(not truthy(row.get("score_ready")) for row in arena_rows)
    add("VAL2213_12_missing_not_promoted", no_missing_promoted, "symbolic/missing residual rows are not promoted to score-ready")

    formalization_clean = not formalization_has_2213_artifacts()
    add("VAL2213_13_formalization_clean", formalization_clean, "formalization-workbench has no 2213 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2213_14_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2213_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2213 writes the exact conditional rank-zero silence theorem, rejects current zero proof, stages the algebraic residual row, and selects coefficient-map/Dq_Z-source descent next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    clause_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2213 - Y5/R2FR Rank-Zero Source-Current Identity Or Algebraic Residual Row",
        "",
        "## Current Verdict",
        "",
        "2213 takes the derivation path first. The good news is that the local-vacuum plateau axiom is no longer the right object. The strict fixed-`L0` branch admits a clean conditional algebraic theorem:",
        "",
        "`M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector`.",
        "",
        "If `M_AB` is locked on physical quotient directions and the entire right-hand side vanishes, then the eliminated coordinate has `Z=0`. If observed descent also gives `Dq_Z=0`, the strict branch can be locally invisible without needing a Yukawa range.",
        "",
        "But current MTS does not yet prove those zeros. `J_A`, `B_A`, `Dq_Z`, CDB terms, source/readout descent, and the `M_AB` signature are not parent-signed together. So 2213 does not claim local GR/Newton. It stages the surviving algebraic residual row instead.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Rank-Zero Source-Current Theorem Attempt",
        "",
        md_table(theorem_rows, ["theorem_id", "theorem_piece", "mathematical_statement", "derivation_status", "proof_effect", "missing_for_current_MTS", "verdict", "valid_for_claim"]),
        "",
        "## J_A / B_A / Dq_Z Clause Audit",
        "",
        md_table(clause_rows, ["clause_id", "required_clause", "current_evidence", "status", "if_closed", "if_open", "next_action", "valid_for_claim"]),
        "",
        "## Algebraic Residual Row",
        "",
        md_table(residual_rows, ["residual_id", "residual_object", "symbolic_formula", "singular_case_formula", "units", "status", "required_numeric_inputs", "arena_links", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "",
        "## Arena Projection Blockers",
        "",
        md_table(arena_rows, ["arena_id", "arena", "required_projection", "current_blocker", "symbolic_map", "next_input_needed", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "This is not grim. It is narrower and cleaner. We have not proved local GR, but we have converted the vague missing step into a named algebraic residual. That is progress because the next fight is no longer philosophical: either derive the source/descent zeros, or fill the finite coefficient map and test it.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    theorem_rows = theorem_attempt_rows()
    clause_rows = clause_audit_rows()
    residual_rows = algebraic_residual_rows()
    arena_rows = arena_blocker_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["theorem_attempt"], theorem_rows),
        (OUTPUTS["clause_audit"], clause_rows),
        (OUTPUTS["algebraic_residual"], residual_rows),
        (OUTPUTS["arena_blocker"], arena_rows),
        (OUTPUTS["claim_gate"], claim_rows),
        (OUTPUTS["decision"], decision_rows_),
        (OUTPUTS["next_target"], next_rows),
    ]:
        write_csv(path, rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_ = validation_rows(
        source_rows,
        theorem_rows,
        clause_rows,
        residual_rows,
        arena_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        theorem_rows,
        clause_rows,
        residual_rows,
        arena_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
        validation_rows_,
    )

    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
