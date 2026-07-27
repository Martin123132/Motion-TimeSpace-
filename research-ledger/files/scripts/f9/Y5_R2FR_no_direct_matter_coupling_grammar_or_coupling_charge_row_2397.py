from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_NO_DIRECT_MATTER_COUPLING_GRAMMAR_OR_COUPLING_CHARGE_ROW_2397"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2397-Y5-R2FR-no-direct-matter-coupling-grammar-or-coupling-charge-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


SOURCES = [
    {
        "source_id": "SRC2397_2396_doc",
        "path": str(POST_ROOT / "2396-Y5-R2FR-matter-source-lift-and-no-direct-slot-proof-or-source-charge-row.md"),
        "needed_for": "current chain selects no-direct matter coupling grammar",
        "needles": "NEXT2396_0_selected|A(X)J_H|epsilon_nonminimal_coupling_slot|VAL2396_OVERALL",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2397_1761_doc",
        "path": str(POST_ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md"),
        "needed_for": "older no-direct vertex and source-prefactor countermodel",
        "needles": "NDV1761_1_allowed_syntax|HOM1761_0_target|DV1761_1_wA|VAL1761_OVERALL",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2397_1761_prefactors",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1761_SOURCE_PREFACTOR_CLASSIFICATION.csv"),
        "needed_for": "source-prefactor classes and live countermodels",
        "needles": "SP1761_1_common_mode|SP1761_2_relative_species|SP1761_4_hidden_frame|SP1761_5_alpha_mass_vertex",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2397_1762_doc",
        "path": str(POST_ROOT / "1762-Y5-R2FR-parent-object-language-Hom-exclusion-from-minimality-or-deltaw-bound.md"),
        "needed_for": "no-source-only Hom theorem attempt and delta_w bound interface",
        "needles": "HOM1762_1_conditional_meta_theorem|HOM1762_3_invariant_algebra_import|DW1762_1_delta_w_A|VAL1762_OVERALL",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2397_1762_hom_csv",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1762_HOM_EXCLUSION_THEOREM_ATTEMPT.csv"),
        "needed_for": "machine-readable Hom exclusion status",
        "needles": "HOM1762_0_target|HOM1762_1_conditional_meta_theorem|HOM1762_5_current_verdict|DELTA_W_RETAINED",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2397_1762_deltaw_csv",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv"),
        "needed_for": "delta_w and A_direct bound rows",
        "needles": "DW1762_1_delta_w_A|DW1762_3_delta_w_hidden|DW1762_6_A_direct_response",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2397_1756_counterexamples",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_COUNTEREXAMPLE_LEDGER.csv"),
        "needed_for": "matter/worldtube hidden source counterexample",
        "needles": "HSC1756_2_matter_worldtube_vertex|J_matter=delta_X V_m|HSC1756_9_verdict",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2397_1771_sector_csv",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1771_SECTOR_ACTION_VARIATION_LEDGER.csv"),
        "needed_for": "nonminimal coupling sector warning",
        "needles": "SAV1771_3_nonminimal|S_nonmin = int sqrt(-g)|A(X)J_m|MUST_CLASSIFY_NOT_FORBIDDEN",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2397_2389_certificate",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_CURRENT_OWNER_CERTIFICATE.csv"),
        "needed_for": "current matter/source no-direct-slot certificate",
        "needles": "OCC2389_2_Lm_density|OCC2389_4_matter_lift|OCC2389_5_no_direct_slots|OCC2389_7_MHref",
        "valid_for_claim": no_claim(),
    },
]


def grammar_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NDMC2397_0_allowed_minimal_syntax",
            "grammar_piece": "minimal ordinary matter syntax",
            "statement": "Allowed ordinary matter is S_ord=sum_A S_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A] plus a single common calibration constant w_star.",
            "status": "EXACT_CONDITIONAL_SCHEMA",
            "effect_if_signed": "ordinary matter/source sees only the observed GR-like geometry and one universal normalization",
            "gap": "current parent action has not signed this as the only grammar",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NDMC2397_1_forbidden_direct_slots",
            "grammar_piece": "forbidden direct residual matter/source slots",
            "statement": "Forbid V_m[X,rho_A,W_source,C_top], A_A(X)L_A, A(X)J_H, A(X)J_m, species-frame factors, source-only prefactors, material markers, and post-readout masks outside q/Obs_e.",
            "status": "TARGET_EXACT_NOT_PARENT_SIGNED",
            "effect_if_signed": "G_direct[v]=0 and epsilon_hidden_source_slot/epsilon_nonminimal_coupling_slot close",
            "gap": "absence of a slot is an object-language theorem, not a covariance consequence",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NDMC2397_2_common_calibration",
            "grammar_piece": "common universal calibration mode",
            "statement": "A universal w_star multiplying all ordinary matter can be absorbed into measured kappa/G and does not by itself create a relative source or WEP residual.",
            "status": "CALIBRATION_MODE_ALLOWED",
            "effect_if_signed": "separates harmless common normalization from dangerous relative couplings",
            "gap": "does not remove relative species, hidden-marker, frame, alpha/mass, or readout weights",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NDMC2397_3_relative_countermodel",
            "grammar_piece": "relative source prefactor countermodel",
            "statement": "S_ord=sum_A w_A S_A with w_A=w_star(1+delta_w_A) can preserve ordinary-looking equations while changing active source charge and composition response.",
            "status": "LIVE_COUNTERMODEL",
            "effect_if_signed": "none; this is the failure mode that must be forbidden or bounded",
            "gap": "relative w_A is not killed by covariance, additivity, Ward identities, or a common measured-G calibration",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NDMC2397_4_no_source_Hom_route",
            "grammar_piece": "no-source-only Hom route",
            "statement": "If Hom_parent(SpeciesLabel or I_hid or ReadoutSelector, R_+ active-source-prefactor)=CommonConst only, then relative delta_w_A and direct source-prefactor slots are undefined.",
            "status": "EXACT_CONDITIONAL_META_THEOREM",
            "effect_if_signed": "kills the source-prefactor branch without fitting",
            "gap": "minimality, invariant-algebra triviality, source-label forgetting, and no-hidden-return are unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NDMC2397_5_verdict",
            "grammar_piece": "current no-direct coupling verdict",
            "statement": "2397 sharpens the coupling gate but cannot promote it: current MTS has an exact conditional grammar, live countermodels, and retained delta_w/coupling charge rows.",
            "status": "CONDITIONAL_ROUTE_EXACT_NOT_PROMOTED",
            "effect_if_signed": "would close the direct matter/source coupling door",
            "gap": "parent object-language and invariant-generator elimination are not signed",
            "valid_for_claim": no_claim(),
        },
    ]


def hom_certificate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HGC2397_0_parent_object_inventory",
            "certificate": "minimal parent object inventory",
            "required_test": "Obj_parent contains only q-owned geometry, matter fields, gauge data, fixed representation labels, and CommonConst for ordinary matter coupling",
            "status": "MISSING_PARENT_OBJECT_LANGUAGE_INVENTORY",
            "residual_if_missing": "delta_w_A",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HGC2397_1_no_marker_extension",
            "certificate": "no co-moving material/source marker extension",
            "required_test": "Conf_parent=Q_MTS, not Q_tilde=(Q_MTS,m)/G_rel with a marker/source coefficient target",
            "status": "MISSING_NO_MARKER_EXTENSION_THEOREM",
            "residual_if_missing": "delta_w_marker",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HGC2397_2_invariant_algebra_triviality",
            "certificate": "local invariant algebra has no source-prefactor generators",
            "required_test": "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor Const with no fibre/domain/chi/memory/species/readout generator",
            "status": "MISSING_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY",
            "residual_if_missing": "delta_w_hidden",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HGC2397_3_label_forgetting_source_functor",
            "certificate": "source functor forgets labels before coupling",
            "required_test": "q_src({(T_A,A)})=T_total before source coupling, so F_src cannot see relative species labels",
            "status": "MISSING_LABEL_FORGETTING_SOURCE_FUNCTOR",
            "residual_if_missing": "delta_w_species",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HGC2397_4_no_hidden_return",
            "certificate": "no hidden return through frames/constants/readout",
            "required_test": "forbid hidden conformal/disformal frames, alpha/mass/charge vertices, source masks, worldtube readout weights, and post-variation projector labels",
            "status": "MISSING_NO_HIDDEN_RETURN_THEOREM",
            "residual_if_missing": "epsilon_nonminimal_coupling_slot",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HGC2397_5_no_Hom_ready",
            "certificate": "no-source-only Hom closure",
            "required_test": "HGC2397_0 through HGC2397_4 pass together",
            "status": "CONDITIONAL_NO_HOM_READY_BUT_UNSIGNED",
            "residual_if_missing": "delta_w_A_retained",
            "valid_for_claim": no_claim(),
        },
    ]


def coupling_charge_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "delta_w_A",
            "definition": "relative active-source/action prefactor vector for ordinary matter sectors",
            "units": "dimensionless",
            "formula_or_bound": "w_A=w_star(1+delta_w_A)",
            "current_value_status": "MISSING_NO_HOM_THEOREM_OR_COMPONENT_BOUND",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_A_Lm",
            "definition": "direct residual coupling through A_A(X)L_A",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "||delta_X sum_A A_A(X)L_A||/M_H_ref",
            "current_value_status": "MISSING_A_LM_FORBIDDEN_OR_BOUND",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_A_JH",
            "definition": "direct residual coupling through A(X)J_H or A(X)J_m",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "||delta_X(A(X)J_H)||/M_H_ref",
            "current_value_status": "MISSING_A_JH_FORBIDDEN_OR_BOUND",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_species_frame",
            "definition": "universal or species conformal/disformal hidden matter frame",
            "units": "dimensionless or arena-specific PPN/clock/R10 projection",
            "formula_or_bound": "||delta_X g_A(X)|| projected into source/clock/PPN/R10 arenas",
            "current_value_status": "MISSING_HIDDEN_FRAME_FORBIDDEN_OR_BOUND",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_alpha_mass_charge",
            "definition": "direct alpha, mass, charge, or constant vertex",
            "units": "arena-specific clock/WEP/fine-structure/fifth-force projection",
            "formula_or_bound": "||delta_X alpha_EM, delta_X m_A, delta_X q_A|| in declared observable arena",
            "current_value_status": "MISSING_NO_CONSTANT_VERTEX_THEOREM_OR_BOUND",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_readout_worldtube_mask",
            "definition": "post-readout source/worldtube/projector mask that changes active source after variation",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "||delta_v W_source, delta_v Pi_M, delta_w_readout||/M_H_ref",
            "current_value_status": "MISSING_BEFORE_READOUT_SOURCE_OWNER_OR_BOUND",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_nonminimal_coupling_slot",
            "definition": "total nonminimal matter/source coupling slot left by no-Hom failure",
            "units": "dimensionless after M_H_ref normalization",
            "formula_or_bound": "delta_w_A + epsilon_A_Lm + epsilon_A_JH + epsilon_species_frame + epsilon_alpha_mass_charge + epsilon_readout_worldtube_mask",
            "current_value_status": "COMPONENTS_MISSING",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2397_0_accept_conditional_no_direct_grammar",
            "decision": "accept the no-direct coupling grammar as an exact conditional route",
            "reason": "minimal observed-frame matter plus no-source-only Hom would remove direct source-prefactor couplings without fitting",
            "consequence": "coupling closure becomes a parent object-language theorem, not a phenomenological smallness assumption",
            "status": "CONDITIONAL_GRAMMAR_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2397_1_common_mode_only_harmless",
            "decision": "allow only a common calibration mode as harmless",
            "reason": "relative or hidden source weights survive common G/kappa calibration and can alter source/composition response",
            "consequence": "all noncommon coupling slots remain explicit residuals",
            "status": "RELATIVE_COUPLINGS_RETAINED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2397_2_no_current_promotion",
            "decision": "do not claim no-direct coupling closure for current MTS",
            "reason": "minimality, invariant algebra, label forgetting, and no-hidden-return are unsigned",
            "consequence": "delta_w_A and epsilon_nonminimal_coupling_slot remain nonclaim",
            "status": "NO_DIRECT_COUPLING_NOT_PROMOTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2397_3_next",
            "decision": "attack invariant-generator elimination next",
            "reason": "the no-Hom theorem now fails only because fibre/domain/chi/memory/species/readout generators may still feed source-prefactor targets",
            "consequence": "2398 should rank and eliminate or bound those generators",
            "status": "SELECT_2398_INVARIANT_GENERATOR_ELIMINATION",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2397_0_no_direct_coupling",
            "gate": "no direct residual matter/source coupling",
            "gate_status": "CONDITIONAL_BLOCKED",
            "claim_effect": "the grammar route is exact, but no-Hom/minimality/invariant clauses are unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2397_1_delta_w_zero",
            "gate": "relative source prefactor delta_w_A zero",
            "gate_status": "BLOCKED",
            "claim_effect": "delta_w_A remains live without no-Hom theorem or source-backed bound",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2397_2_matter_Qv_zero",
            "gate": "matter/source vertical Qv zero",
            "gate_status": "BLOCKED",
            "claim_effect": "matter theorem cannot promote while coupling slot is live",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2397_3_GR_Newton",
            "gate": "local GR/Newton reduction",
            "gate_status": "BLOCKED",
            "claim_effect": "no local GR/Newton claim from 2397",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2397_0_claim_no_direct_coupling",
            "claim": "current MTS forbids all direct matter/source coupling slots",
            "allowed": "false",
            "reason": "the no-source-only Hom theorem is conditional and unsigned",
            "blocking_rows": "HGC2397_0_parent_object_inventory;HGC2397_2_invariant_algebra_triviality;HGC2397_3_label_forgetting_source_functor;HGC2397_4_no_hidden_return",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2397_1_claim_delta_w_zero",
            "claim": "delta_w_A=0",
            "allowed": "false",
            "reason": "relative source prefactors remain a live countermodel unless no-Hom closes",
            "blocking_rows": "NDMC2397_3_relative_countermodel;delta_w_A",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2397_2_claim_local_GR",
            "claim": "local GR/Newton is derived from no-direct coupling grammar",
            "allowed": "false",
            "reason": "2397 is a coupling grammar gate only; total Qv, projector, boundary, PPN, and Newtonian-limit gates remain",
            "blocking_rows": "CG2397_2_matter_Qv_zero;CG2397_3_GR_Newton",
            "valid_for_claim": no_claim(),
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2397_0_selected",
            "next_file": "2398-Y5-R2FR-invariant-generator-elimination-priority-or-deltaw-source-pack.md",
            "success_condition": "rank fibre/domain/chi/memory/species/readout generators and eliminate the least-scrutiny source-prefactor generators first",
            "fallback_condition": "create source-ready delta_w_species, delta_w_hidden, delta_w_marker, delta_w_readout, and K_w bound rows",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2397_1_parallel",
            "next_file": "2398b-Y5-R2FR-deltaw-component-basis-and-arena-bound-interface.md",
            "success_condition": "define a component basis/norm for delta_w_A and arena projections to WEP, clocks, R10, PPN, and source normalization",
            "fallback_condition": "keep all coupling rows non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2397_SOURCE_REGISTER.csv": lambda: SOURCES,
    "P8_Y5_PARENT_QLOC_2397_NO_DIRECT_COUPLING_GRAMMAR.csv": grammar_rows,
    "P8_Y5_PARENT_QLOC_2397_NO_HOM_CERTIFICATE.csv": hom_certificate_rows,
    "P8_Y5_PARENT_QLOC_2397_COUPLING_CHARGE_ROWS.csv": coupling_charge_rows,
    "P8_Y5_PARENT_QLOC_2397_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2397_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2397_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2397_NEXT_TARGET.csv": next_rows,
}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    missing_sources = [src["path"] for src in SOURCES if not Path(src["path"]).exists()]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_00_sources_exist",
            "status": "PASS" if not missing_sources else "FAIL",
            "detail": "all required source paths exist" if not missing_sources else ";".join(missing_sources),
            "valid_for_claim": no_claim(),
        }
    )

    missing_needles: list[str] = []
    for src in SOURCES:
        path = Path(src["path"])
        for needle in src["needles"].split("|"):
            if not contains(path, needle):
                missing_needles.append(f"{src['source_id']}::{needle}")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_01_needles_found",
            "status": "PASS" if not missing_needles else "FAIL",
            "detail": "all source needles found" if not missing_needles else ";".join(missing_needles),
            "valid_for_claim": no_claim(),
        }
    )

    grammar = grammar_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_02_forbidden_slots_present",
            "status": "PASS" if any("A_A(X)L_A" in row["statement"] and "A(X)J_H" in row["statement"] and "V_m[X" in row["statement"] for row in grammar) else "FAIL",
            "detail": "direct matter/source coupling forbidden-slot list is present",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_03_common_mode_guard_present",
            "status": "PASS" if any(row["row_id"] == "NDMC2397_2_common_calibration" for row in grammar) else "FAIL",
            "detail": "common calibration is separated from relative coupling",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_04_relative_countermodel_present",
            "status": "PASS" if any("w_A=w_star(1+delta_w_A)" in row["statement"] for row in grammar) else "FAIL",
            "detail": "relative source-prefactor countermodel is retained",
            "valid_for_claim": no_claim(),
        }
    )

    certificates = hom_certificate_rows()
    required_statuses = {
        "MISSING_PARENT_OBJECT_LANGUAGE_INVENTORY",
        "MISSING_NO_MARKER_EXTENSION_THEOREM",
        "MISSING_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY",
        "MISSING_LABEL_FORGETTING_SOURCE_FUNCTOR",
        "MISSING_NO_HIDDEN_RETURN_THEOREM",
    }
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_05_no_Hom_gaps_explicit",
            "status": "PASS" if required_statuses <= {row["status"] for row in certificates} else "FAIL",
            "detail": "object inventory, marker, invariant algebra, label-forgetting, and hidden-return gaps explicit",
            "valid_for_claim": no_claim(),
        }
    )

    charge_rows = coupling_charge_rows()
    required_quantities = {
        "delta_w_A",
        "epsilon_A_Lm",
        "epsilon_A_JH",
        "epsilon_species_frame",
        "epsilon_alpha_mass_charge",
        "epsilon_readout_worldtube_mask",
        "epsilon_nonminimal_coupling_slot",
    }
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_06_coupling_rows_present_nonclaim",
            "status": "PASS" if required_quantities <= {row["quantity_id"] for row in charge_rows} and all(row["valid_for_claim"] == "false" for row in charge_rows) else "FAIL",
            "detail": "coupling charge rows are present and nonclaim",
            "valid_for_claim": no_claim(),
        }
    )

    gates = claim_gate_rows()
    gate_ok = all(row["gate_status"] in {"BLOCKED", "CONDITIONAL_BLOCKED"} for row in gates)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_07_global_claims_blocked",
            "status": "PASS" if gate_ok else "FAIL",
            "detail": "no-direct coupling, delta_w, matter Qv, and GR/Newton gates not promoted",
            "valid_for_claim": no_claim(),
        }
    )

    csv_failures: list[str] = []
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            csv_failures.append(f"{name}:missing")
            continue
        try:
            parsed = csv_rows(path)
        except Exception as exc:
            csv_failures.append(f"{name}:{exc}")
            continue
        if not parsed:
            csv_failures.append(f"{name}:empty")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_08_csv_parse",
            "status": "PASS" if not csv_failures else "FAIL",
            "detail": "generated CSVs parse and have rows" if not csv_failures else ";".join(csv_failures),
            "valid_for_claim": no_claim(),
        }
    )

    true_claims: list[str] = []
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            continue
        for row in csv_rows(path):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                true_claims.append(f"{name}:{row}")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_09_no_claim_flags",
            "status": "PASS" if not true_claims else "FAIL",
            "detail": "no generated row has valid_for_claim=true" if not true_claims else ";".join(true_claims),
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_10_formalization_untouched_by_script",
            "status": "PASS",
            "detail": "script writes only post-checkpoint-work outputs",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_11_next_selected",
            "status": "PASS" if any(row["row_id"] == "NEXT2397_0_selected" for row in next_rows()) else "FAIL",
            "detail": "invariant-generator elimination selected next",
            "valid_for_claim": no_claim(),
        }
    )

    overall_status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2397_OVERALL",
            "status": overall_status,
            "detail": "2397 states the no-direct matter coupling grammar, separates common calibration from live relative couplings, refuses no-Hom promotion, and selects invariant-generator elimination next",
            "valid_for_claim": no_claim(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]], headers: list[str]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    grammar = grammar_rows()
    certificates = hom_certificate_rows()
    charge_rows = coupling_charge_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    next_targets = next_rows()
    validation = validation_rows()

    body = f"""# 2397 — No Direct Matter Coupling Grammar Or Coupling Charge Row

## Result

2397 is the cleanest statement so far of the coupling problem.

The only low-scrutiny ordinary-matter grammar is:

`S_ord = sum_A S_A[Psi_A, e_obs(q(Phi)), omega[e_obs], theta_A]`

plus at most one common universal calibration `w_star`, absorbable into measured `kappa/G`.

Everything else must be absent by parent object-language theorem or retained as a coupling charge row:

`V_m[X,rho_A,W_source,C_top]`, `A_A(X)L_A`, `A(X)J_H`, `A(X)J_m`, source-only prefactors, species-frame factors,
material markers, alpha/mass/charge vertices, and post-readout source masks.

The hard theorem is:

`Hom_parent(SpeciesLabel or I_hid or ReadoutSelector, R_+ active-source-prefactor) = CommonConst only`.

If that Hom exclusion is parent-signed, relative `delta_w_A` is not a definable object and the direct matter/source
coupling slot closes.  If it is not signed, the coupling leak is real enough to keep as a finite source vector.

Current MTS does not yet sign the Hom theorem.  Minimality, invariant-algebra triviality, label-forgetting source
functor, and no-hidden-return are still unsigned.  So this is not a coupling pass.  It is a precise proof contract and
an explicit set of coupling residual rows.

## Source Register

{markdown_table(SOURCES, ["source_id", "path", "needed_for", "needles", "valid_for_claim"])}

## No Direct Coupling Grammar

{markdown_table(grammar, ["row_id", "grammar_piece", "statement", "status", "effect_if_signed", "gap", "valid_for_claim"])}

## No-Hom Certificate

{markdown_table(certificates, ["row_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"])}

## Coupling Charge Rows

{markdown_table(charge_rows, ["quantity_id", "definition", "units", "formula_or_bound", "current_value_status", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_targets, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is not grim; it is the lock picking itself out.  The coupling problem is no longer "maybe something in matter".
It is a typed-Hom/invariant-generator problem.  We either prove there is no parent object that can feed a relative
active-source prefactor, or we carry `delta_w_A` and the coupling charge rows into bounds.  The next best derivation
move is to rank the surviving invariant generators and attack the least defensible ones first.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2397_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2397_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
