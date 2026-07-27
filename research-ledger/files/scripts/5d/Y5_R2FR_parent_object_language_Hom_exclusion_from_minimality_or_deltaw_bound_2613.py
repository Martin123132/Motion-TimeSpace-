from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_HOM_EXCLUSION_GATE_2613"
CHECKPOINT_ID = "2613"

DOC = ROOT / "2613-Y5-R2FR-parent-object-language-Hom-exclusion-from-minimality-or-deltaw-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_LINEAGE_LEDGER.csv",
    "hom_theorem": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_HOM_EXCLUSION_THEOREM_ATTEMPT.csv",
    "minimality_import": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_MINIMALITY_IMPORT_AUDIT.csv",
    "invariant_hom": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_INVARIANT_ALGEBRA_HOM_AUDIT.csv",
    "source_functor": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv",
    "deltaw_bound": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_DELTAW_BOUND_INTERFACE.csv",
    "source_zero": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_SOURCE_ZERO_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2613_VALIDATION.csv",
}

COPY_TARGETS = {
    "hom_theorem": LOCAL_BOUNDS / "Hom_exclusion_theorem_attempt_2613_NONCLAIM.csv",
    "deltaw_bound": LOCAL_BOUNDS / "Deltaw_bound_interface_2613_NONCLAIM.csv",
    "source_zero": LOCAL_BOUNDS / "Hom_source_zero_status_2613_NONCLAIM.csv",
    "next_target": QUEUE / "JR2613_INVARIANT_GENERATOR_ELIMINATION_NEXT.csv",
}

FALSE_FLAGS = {
    "score_ready": False,
    "valid_prediction_row": False,
    "valid_for_claim": False,
    "claim_allowed": False,
    "accepted_for_scoring": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def false_flags() -> dict[str, bool]:
    return dict(FALSE_FLAGS)


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2613_00_2612_handoff_doc",
            "source_key": "2612_handoff_to_Hom_gate",
            "source_path": ROOT / "2612-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
            "needles": ["NEXT2612_0_selected", "HOM2612_4_verdict", "VAL2612_OVERALL"],
            "role": "current 26xx handoff selecting parent object-language Hom exclusion",
        },
        {
            "source_id": "SRC2613_01_2612_coefficients",
            "source_key": "2612_deltaw_A_direct_pack",
            "source_path": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_AMATTER_COEFFICIENT_PACK.csv",
            "needles": ["CP2612_1_delta_w_A", "CP2612_6_A_direct_matter", "CP2612_7_R_source_direct"],
            "role": "current live residual symbols that Hom theorem would kill or bound",
        },
        {
            "source_id": "SRC2613_02_2612_hom_audit",
            "source_key": "2612_no_source_only_Hom_audit",
            "source_path": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_SOURCE_ONLY_HOM_AUDIT.csv",
            "needles": ["HOM2612_0_target", "HOM2612_4_verdict", "FAIL_CURRENT_CLAIM_HOM_NOT_DERIVED"],
            "role": "immediate grammar target and current block",
        },
        {
            "source_id": "SRC2613_03_1762_doc",
            "source_key": "1762_prior_Hom_checkpoint_doc",
            "source_path": ROOT / "1762-Y5-R2FR-parent-object-language-Hom-exclusion-from-minimality-or-deltaw-bound.md",
            "needles": ["HOM1762_0_target", "DEC1762_3_best_next", "VAL1762_OVERALL"],
            "role": "prior Hom theorem attempt used as source logic, not a claim",
        },
        {
            "source_id": "SRC2613_04_1762_hom",
            "source_key": "1762_Hom_theorem_attempt",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1762_HOM_EXCLUSION_THEOREM_ATTEMPT.csv",
            "needles": ["HOM1762_0_target", "HOM1762_1_conditional_meta_theorem", "HOM1762_5_current_verdict"],
            "role": "conditional no-source-only Hom theorem and parent unsigned verdict",
        },
        {
            "source_id": "SRC2613_05_1762_minimality",
            "source_key": "1762_minimality_import",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1762_MINIMALITY_IMPORT_AUDIT.csv",
            "needles": ["MIN1762_0_fixed_spurions", "MIN1762_1_no_marker_extension", "MIN1762_3_verdict"],
            "role": "primitive minimality import and marker-extension blocker",
        },
        {
            "source_id": "SRC2613_06_1762_invariant",
            "source_key": "1762_invariant_algebra_Hom_audit",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1762_INVARIANT_ALGEBRA_HOM_AUDIT.csv",
            "needles": ["IH1762_0_target", "IH1762_6_readout", "IH1762_7_verdict"],
            "role": "invariant-generator debts that prevent Hom exclusion from closing",
        },
        {
            "source_id": "SRC2613_07_1762_source_functor",
            "source_key": "1762_label_forgetting_source_functor",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1762_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv",
            "needles": ["SF1762_0_label_forgetting", "SF1762_3_no_hidden_return", "SF1762_4_verdict"],
            "role": "source functor label-forgetting theorem contract and unsigned parent status",
        },
        {
            "source_id": "SRC2613_08_1762_deltaw",
            "source_key": "1762_deltaw_bound_interface",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
            "needles": ["DW1762_0_zero_condition", "DW1762_1_delta_w_A", "DW1762_6_A_direct_response"],
            "role": "fallback finite delta_w interface inherited from prior branch",
        },
        {
            "source_id": "SRC2613_09_1763_priority",
            "source_key": "1763_invariant_generator_priority",
            "source_path": ROOT / "1763-Y5-R2FR-invariant-generator-elimination-priority-or-deltaw-source-acquisition.md",
            "needles": ["DEC1763_3_best_next", "NEXT1763_0_primary", "VAL1763_OVERALL"],
            "role": "downstream target already identified: species-label forgetting first",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_key": spec["source_key"],
                    "source_path": spec["source_path"],
                    "source_exists": spec["source_path"].exists(),
                    "needles": spec["needles"],
                    "needles_present": not missing,
                    "missing_needles": missing,
                    "role": spec["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "lineage_id": "LIN2613_0_current_parent",
            "input_checkpoint": "2612",
            "input_artifact": "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_*",
            "imported_result": "direct matter/source branch reduced to no-source-only Hom or finite delta_w/A_direct rows",
            "2613_use": "translate into parent object-language Hom exclusion gate",
        },
        {
            "lineage_id": "LIN2613_1_prior_Hom_branch",
            "input_checkpoint": "1762",
            "input_artifact": "P8_Y5_PARENT_QLOC_1762_*",
            "imported_result": "exact conditional Hom theorem exists but current parent signature is unsigned",
            "2613_use": "reuse theorem contract in current 26xx chain without promoting it",
        },
        {
            "lineage_id": "LIN2613_2_generator_priority",
            "input_checkpoint": "1763",
            "input_artifact": "1763-Y5-R2FR-invariant-generator-elimination-priority-or-deltaw-source-acquisition.md",
            "imported_result": "species-label generator is least-scrutiny next zero route",
            "2613_use": "set next step after Hom exclusion remains blocked",
        },
        {
            "lineage_id": "LIN2613_3_residual_interface",
            "input_checkpoint": "2612+1762",
            "input_artifact": "delta_w and A_direct nonclaim rows",
            "imported_result": "source-prefactor residual vector is explicit and dimensionless, but unsourced",
            "2613_use": "retain residual vector rather than hiding it in matter prose",
        },
        {
            "lineage_id": "LIN2613_4_claim_policy",
            "input_checkpoint": "all",
            "input_artifact": "claim gates and validation ledgers",
            "imported_result": "no local-GR/Newton/PPN/WEP/R10/clock/orbital claim without source-side closure",
            "2613_use": "keep this checkpoint private and nonclaim",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def hom_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "hom_id": "HOM2613_0_target",
            "claim_piece": "no source-only Hom theorem",
            "mathematical_form": "Hom_parent(SpeciesLabel or I_hid or ReadoutSelector or MarkerClass, R_+ active-source-prefactor)=CommonConst only",
            "attempt_status": "TARGET_EXACT",
            "would_imply": "relative delta_w_A is undefined; only common w_star/kappa calibration remains",
            "blocker": "requires parent object inventory, primitive minimality, invariant-algebra triviality, label-forgetting source functor and no hidden return",
        },
        {
            "hom_id": "HOM2613_1_conditional_meta_theorem",
            "claim_piece": "minimal typed grammar implies no source-only prefactor",
            "mathematical_form": "If Obj_parent contains only q-owned geometry, ordinary matter fields, gauge data, fixed representation labels and CommonConst, no object can feed w_A except CommonConst",
            "attempt_status": "EXACT_CONDITIONAL_META_THEOREM",
            "would_imply": "w_A=w_star for every source-relevant matter component",
            "blocker": "current MTS has not parent-signed that object inventory",
        },
        {
            "hom_id": "HOM2613_2_minimality_import",
            "claim_piece": "primitive minimality supplies object inventory",
            "mathematical_form": "Conf_parent=Q_MTS and no quotient extension Q_tilde=(Q_MTS,m)/G_rel with material/source markers",
            "attempt_status": "BLOCKED_CURRENT_CLAIM",
            "would_imply": "no Hom(material marker, R_+ source prefactor)",
            "blocker": "co-moving material/source markers remain legal until a no-extension theorem is derived",
        },
        {
            "hom_id": "HOM2613_3_invariant_algebra_import",
            "claim_piece": "local invariant algebra has no source-prefactor generators",
            "mathematical_form": "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor Const, with no fibre/domain/chi/memory/species/readout generators",
            "attempt_status": "BLOCKED_CURRENT_CLAIM",
            "would_imply": "hidden, marker, readout and species source weights cannot be generated",
            "blocker": "finite fibre spectrum, domain class, chi_D, memory scalar, species constants and readout projector are not eliminated",
        },
        {
            "hom_id": "HOM2613_4_source_functor_import",
            "claim_piece": "label-forgetting source functor removes species weights",
            "mathematical_form": "q_src({(T_A,A)})=T_total before F_src; covariant additive F_src gives kappa_univ T_total",
            "attempt_status": "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "would_imply": "delta_w_species=0 and common source normalization only",
            "blocker": "label forgetting is a parent source-category contract, not a derived parent theorem",
        },
        {
            "hom_id": "HOM2613_5_current_verdict",
            "claim_piece": "current MTS signs no-source-only Hom",
            "mathematical_form": "HOM2613_1 through HOM2613_4 close in one parent branch",
            "attempt_status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "would_imply": "DELTA_W_RETAINED unless parent signs all clauses",
            "blocker": "minimality and invariant algebra fail current claim; constant/source universality and label forgetting remain unsigned",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def minimality_import_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "minimality_id": "MIN2613_0_fixed_spurions",
            "clause": "fixed external labels are excluded",
            "test_form": "m_fixed is not a function on Q=Phi/G_rep",
            "status": "CONDITIONAL_PASS_IF_STRICT_QUOTIENT",
            "impact": "removes non-orbit covectors as parent-action source weights",
            "blocker": "does not exclude co-moving material markers or quotient-invariant class scalars",
        },
        {
            "minimality_id": "MIN2613_1_no_marker_extension",
            "clause": "no co-moving material/source marker quotient extension",
            "test_form": "Conf_parent=Q_MTS, not Q_tilde=(Q_MTS,m)/G_rel",
            "status": "NOT_DERIVED",
            "impact": "would forbid Hom(m, R_+ source prefactor)",
            "blocker": "current corpus does not prove marker extensions impossible",
        },
        {
            "minimality_id": "MIN2613_2_no_marker_functor",
            "clause": "no nonconstant natural marker functor on local branch",
            "test_form": "Nat(Q_MTS, Marker)_loc = constants",
            "status": "REDUCED_TO_INVARIANT_ALGEBRA_TRIVIALITY",
            "impact": "would reduce hidden-marker Hom to common constants",
            "blocker": "local invariant algebra still has source-like generators",
        },
        {
            "minimality_id": "MIN2613_3_verdict",
            "clause": "primitive minimality derives no-source-only Hom",
            "test_form": "MIN2613_0 through MIN2613_2 close with source-label forgetting",
            "status": "FAIL_CURRENT_CLAIM_MINIMALITY_NOT_PROVED",
            "impact": "would remove delta_w_marker and direct marker source weights",
            "blocker": "retain delta_w_marker/A_marker/A_direct rows",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def invariant_hom_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "invariant_id": "IH2613_0_target",
            "generator": "target local invariant algebra",
            "legal_source_route": "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor Const would leave only common source calibration",
            "status": "TARGET_EXACT",
            "delta_w_channel": "none if proved",
            "required_closure": "MISSING_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY",
        },
        {
            "invariant_id": "IH2613_1_fibre",
            "generator": "finite_cell_fibre_spectrum",
            "legal_source_route": "can act as material/source marker or effective charge label",
            "status": "NOT_TRIVIALIZED",
            "delta_w_channel": "delta_w_hidden or delta_w_species",
            "required_closure": "MISSING_FIBRE_SPECTRUM_UNIVERSAL_OR_GAUGE_PROOF",
        },
        {
            "invariant_id": "IH2613_2_domain",
            "generator": "relative_boundary_domain_class",
            "legal_source_route": "can carry local source class, boundary/domain charge, or worldtube mask",
            "status": "NOT_DERIVED",
            "delta_w_channel": "delta_w_marker or delta_w_readout",
            "required_closure": "MISSING_LOCAL_TRIVIAL_CLASS_OR_CLASS_NOHAIR",
        },
        {
            "invariant_id": "IH2613_3_selector",
            "generator": "chi_D/domain_selector",
            "legal_source_route": "can become preferred-frame/source-normalization/R10/R11 marker",
            "status": "NOT_DERIVED",
            "delta_w_channel": "delta_w_hidden or source-normalization coefficient",
            "required_closure": "MISSING_SELECTOR_GAUGE_OR_LOCAL_TRIVIAL_BRANCH",
        },
        {
            "invariant_id": "IH2613_4_memory",
            "generator": "memory_or_class_scalar",
            "legal_source_route": "can enter clock/source/fifth-force channels",
            "status": "NOT_SILENCED_AS_THEOREM",
            "delta_w_channel": "delta_w_hidden or A_mu_even",
            "required_closure": "MISSING_LOCAL_VALUE_GRADIENT_ZERO_OR_BOUND",
        },
        {
            "invariant_id": "IH2613_5_species_constants",
            "generator": "species_charge_constants",
            "legal_source_route": "can generate theta_A(X), kappa_A, source weights or relative matter normalization",
            "status": "NOT_UNIVERSALIZED",
            "delta_w_channel": "delta_w_species, b_theta or b_kappa",
            "required_closure": "MISSING_CONSTANT_SOURCE_UNIVERSALITY",
        },
        {
            "invariant_id": "IH2613_6_readout",
            "generator": "post_readout_projector",
            "legal_source_route": "can re-enter as reduced-action source after apparent closure",
            "status": "NO_CHEAT_RULE_ONLY",
            "delta_w_channel": "delta_w_readout",
            "required_closure": "MISSING_FULL_PARENT_DOMAIN_READOUT_AUDIT",
        },
        {
            "invariant_id": "IH2613_7_verdict",
            "generator": "source-prefactor generator debts",
            "legal_source_route": "at least one legal Hom source target remains unless all generators are eliminated or bounded",
            "status": "FAIL_CURRENT_CLAIM_GENERATOR_DEBTS_RETAINED",
            "delta_w_channel": "delta_w coefficient pack remains mandatory",
            "required_closure": "derive each generator zero or source each coefficient",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_functor_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "functor_id": "SF2613_0_label_forgetting",
            "clause": "source functor sees total Hilbert current, not labelled family",
            "math_form": "q_src({(T_A,A)})=T_total=sum_A T_A",
            "status": "EXACT_MATH_CONTRACT_PARENT_UNSIGNED",
            "impact": "species labels cannot feed relative source weight",
            "blocker": "delta_w_species remains until q_src is parent-derived",
        },
        {
            "functor_id": "SF2613_1_covariant_additive_map",
            "clause": "source map is natural, covariant, additive and local after labels are forgotten",
            "math_form": "F_src(T+U)=F_src(T)+F_src(U), F_src(phi_*T)=phi_*F_src(T)",
            "status": "CONDITIONAL_THEOREM_CLEAN",
            "impact": "one scalar kappa_univ remains",
            "blocker": "cannot infer unique source coupling before labels are forgotten",
        },
        {
            "functor_id": "SF2613_2_common_calibration",
            "clause": "common scalar is calibrated by measured G and not treated as composition field",
            "math_form": "kappa_univ <-> 8 pi G_ref/c^4",
            "status": "COMMON_MODE_ONLY",
            "impact": "w_star/kappa common mode separated from residual vector",
            "blocker": "common normalization nuisance remains but is not a relative WEP/local-force proof",
        },
        {
            "functor_id": "SF2613_3_no_hidden_return",
            "clause": "no hidden constants, masks, markers, boundary classes or post-readout maps reintroduce species dependence",
            "math_form": "partial_A kappa=partial_m kappa=partial_boundary kappa=partial_D kappa=0",
            "status": "NAMED_BY_CONTRACTS_NOT_PARENT_SIGNED",
            "impact": "delta_w_hidden/marker/readout close if proved",
            "blocker": "source weights can return under another name",
        },
        {
            "functor_id": "SF2613_4_verdict",
            "clause": "source functor derives no-source-only Hom",
            "math_form": "SF2613_0 through SF2613_3 all signed",
            "status": "FAIL_CURRENT_CLAIM_SOURCE_FUNCTOR_PARENT_UNSIGNED",
            "impact": "relative delta_w_A=0",
            "blocker": "retain delta_w component vector",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def deltaw_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "deltaw_id": "DW2613_0_zero_condition",
            "quantity": "Z_delta_w",
            "definition": "True only if minimality, invariant algebra, label-forgetting source functor, no hidden return and constant/source universality are all parent-signed",
            "status": "FALSE_PARENT_UNSIGNED",
            "units": "dimensionless",
            "equation_or_bound": "delta_w_A=0 theorem condition",
        },
        {
            "deltaw_id": "DW2613_1_delta_w_A",
            "quantity": "delta_w_A",
            "definition": "component vector over source-relevant ordinary matter sectors with declared basis and norm",
            "status": "MISSING_COMPONENT_BASIS_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "equation_or_bound": "w_A=w_star(1+delta_w_A)",
        },
        {
            "deltaw_id": "DW2613_2_delta_w_species",
            "quantity": "delta_w_species",
            "definition": "species-label source prefactor bound or Hom(species,R_+) zero theorem",
            "status": "MISSING_HOM_SPECIES_EXCLUSION_OR_NUMERIC_BOUND",
            "units": "dimensionless",
            "equation_or_bound": "relative species source-weight amplitude",
        },
        {
            "deltaw_id": "DW2613_3_delta_w_hidden",
            "quantity": "delta_w_hidden",
            "definition": "hidden invariant source coefficient bound or invariant-algebra zero theorem",
            "status": "MISSING_HIDDEN_INVARIANT_ZERO_OR_BOUND",
            "units": "dimensionless",
            "equation_or_bound": "source-prefactor dependence on hidden invariant",
        },
        {
            "deltaw_id": "DW2613_4_delta_w_marker",
            "quantity": "delta_w_marker",
            "definition": "material/domain/boundary marker coefficient bound or no-marker theorem",
            "status": "MISSING_NO_MARKER_THEOREM_OR_BOUND",
            "units": "dimensionless",
            "equation_or_bound": "source-prefactor dependence on co-moving marker/domain class",
        },
        {
            "deltaw_id": "DW2613_5_delta_w_readout",
            "quantity": "delta_w_readout",
            "definition": "readout/worldtube transfer coefficient bound or before-readout owner theorem",
            "status": "MISSING_READOUT_TRANSFER_ZERO_OR_BOUND",
            "units": "dimensionless",
            "equation_or_bound": "post-variation source-mask/source-support transfer",
        },
        {
            "deltaw_id": "DW2613_6_A_direct_response",
            "quantity": "A_direct_matter",
            "definition": "direct matter/source response to source-prefactor vector",
            "status": "MISSING_K_W_OPERATOR_NORM_DELTAW_NORM_OR_THEOREM_ZERO",
            "units": "E*_dual_or_declared_arena_units",
            "equation_or_bound": "||delta_v V_m||_{E*} <= K_w ||delta_w||",
        },
        {
            "deltaw_id": "DW2613_7_R_source_direct",
            "quantity": "R_source_direct",
            "definition": "direct matter/source contribution to residual source side",
            "status": "MISSING_ADIRECT_AND_ESTAR_UNITS",
            "units": "E*_dual_or_declared_arena_units",
            "equation_or_bound": "||R_source,direct||_{E*} <= U_B A_direct_matter",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "status_id": "SZ2613_0_Hom",
            "target": "no-source-only Hom",
            "status": "NOT_DERIVED",
            "reason": "conditional meta-theorem is written, but minimality/invariant/source-functor clauses are parent-unsigned",
            "next_required": "primitive minimality, local invariant algebra triviality, label forgetting and no hidden return",
        },
        {
            "status_id": "SZ2613_1_delta_w",
            "target": "delta_w_A",
            "status": "RETAINED_NONCLAIM",
            "reason": "relative prefactor countermodel survives unless Hom exclusion is parent-signed",
            "next_required": "component basis, numeric/source-backed bounds or theorem-zero",
        },
        {
            "status_id": "SZ2613_2_A_direct",
            "target": "A_direct_matter",
            "status": "NOT_ZEROED",
            "reason": "A_direct can be killed by no-Hom/no-marker/no-hidden-frame package, but package fails current claim",
            "next_required": "K_w, E* norm, delta_w bounds, or zero theorem",
        },
        {
            "status_id": "SZ2613_3_source_silence",
            "target": "S_cg(D_L=0,Y)",
            "status": "NOT_DERIVED",
            "reason": "source-prefactor branch remains open and can feed hidden/source residuals",
            "next_required": "Hom theorem or finite source residual bound",
        },
        {
            "status_id": "SZ2613_4_local_GR",
            "target": "GR/Newton source side",
            "status": "NOT_CLAIMABLE",
            "reason": "source-side matter grammar is still nonclaim; other hidden-source channels remain open",
            "next_required": "A_hidden_total plus source-to-Poisson/orbital calibration gates",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2613_0_no_Hom",
            "claim": "no-source-only Hom is parent-derived",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_OBJECT_LANGUAGE_UNSIGNED",
        },
        {
            "gate_id": "GATE2613_1_delta_w_zero",
            "claim": "delta_w_A=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_MINIMALITY_INVARIANT_SOURCE_FUNCTOR_UNSIGNED",
        },
        {
            "gate_id": "GATE2613_2_A_direct_zero",
            "claim": "A_direct_matter=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTAW_AND_DIRECT_VERTEX_ROWS_UNSOURCED",
        },
        {
            "gate_id": "GATE2613_3_source_silence",
            "claim": "S_cg(D_L=0,Y)=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_PREFACOR_AND_HIDDEN_SOURCE_CHANNELS",
        },
        {
            "gate_id": "GATE2613_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10/WEP/clock/orbital branch can claim",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTAW_AND_SOURCE_SIDE_GATES_NOT_CLOSED",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2613_0_conditional_theorem",
            "decision": "NO_HOM_THEOREM_IS_EXACT_CONDITIONAL",
            "why": "minimal typed object language plus label forgetting leaves only a common calibration constant",
            "action": "keep the theorem as parent-action contract",
        },
        {
            "decision_id": "DEC2613_1_current_result",
            "decision": "NO_HOM_NOT_PARENT_DERIVED",
            "why": "primitive minimality and invariant algebra triviality are not proved; source functor label forgetting remains unsigned",
            "action": "do not set delta_w_A or A_direct_matter to zero",
        },
        {
            "decision_id": "DEC2613_2_bound",
            "decision": "DELTAW_BOUND_INTERFACE_WRITTEN_NONCLAIM",
            "why": "if the theorem stalls, delta_w must become a finite residual vector with declared basis, units and source paths",
            "action": "use bound rows only as nonclaim plumbing until sourced",
        },
        {
            "decision_id": "DEC2613_3_best_next",
            "decision": "SPECIES_LABEL_FORGETTING_IS_NEXT_BEST_DERIVATION_ROUTE",
            "why": "1763 already ranked species labels as the cleanest generator to kill first and this checkpoint confirms Hom still depends on it",
            "action": "build 2614 species-label forgetting source-functor parent proof or delta_w_species bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2613_0_primary",
            "status": "selected",
            "doc": "2614-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md",
            "script": "scripts/Y5_R2FR_species_label_forgetting_source_functor_parent_proof_or_deltaw_species_bound_2614.py",
            "task": "try to prove q_src forgets species labels before source coupling selection; if not, stage source-ready delta_w_species bound rows",
            "success_condition": "delta_w_species is theorem-zero or becomes explicit finite nonclaim input with units and provenance",
            "fallback": "2614b-Y5-R2FR-deltaw-species-bound-source-pack.md",
            "guardrail": "no local-GR, WEP, PPN, R10, clock, orbital or source-zero claim from this checkpoint",
        },
        {
            "next_id": "NEXT2613_1_fallback",
            "status": "held_fallback",
            "doc": "2614b-Y5-R2FR-deltaw-species-bound-source-pack.md",
            "script": "scripts/Y5_R2FR_deltaw_species_bound_source_pack_2614b.py",
            "task": "build nonclaim source-acquisition rows for delta_w_species with component basis, units, target bounds and provenance",
            "success_condition": "species source prefactor residual can be tested as a finite envelope, not assumed zero",
            "fallback": "return to fibre/domain/chi/memory/readout generators",
            "guardrail": "no placeholder numeric row can be valid_for_claim",
        },
        {
            "next_id": "NEXT2613_2_generator_queue",
            "status": "queued_after_species",
            "doc": "2614c-Y5-R2FR-hidden-marker-readout-generator-zero-queue.md",
            "script": "scripts/Y5_R2FR_hidden_marker_readout_generator_zero_queue_2614c.py",
            "task": "order the remaining hidden, marker, domain, memory and readout generators after species-label attempt",
            "success_condition": "each generator has zero theorem target or finite source-bound interface",
            "fallback": "deltaw component-bound pack",
            "guardrail": "do not merge generator debts into one fog-bank residual",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "hom": hom_theorem_rows(),
        "minimality": minimality_import_rows(),
        "invariant": invariant_hom_rows(),
        "source_functor": source_functor_rows(),
        "deltaw": deltaw_bound_rows(),
        "source_zero": source_zero_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }


def copy_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, target in COPY_TARGETS.items():
        source = OUTPUTS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        ok, count, error = csv_parses(target)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2613_{key}",
                    "source_key": key,
                    "source_path": source,
                    "copy_path": target,
                    "copy_exists": target.exists(),
                    "csv_parse": ok,
                    "row_count": count,
                    "error": error,
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = set(FALSE_FLAGS)
    for key, rows in rows_map.items():
        if key == "sources":
            continue
        for row in rows:
            for field in flag_fields:
                if str(row.get(field, "false")).lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(row_value(value) for value in row.values())
            if "MISSING_" not in text:
                continue
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return False
            status = str(row.get("status", row.get("attempt_status", ""))).upper()
            if status in {"READY", "PASS", "VALID_FOR_CLAIM"}:
                return False
    return True


def sources_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(row["source_exists"] and row["needles_present"] for row in rows_map["sources"])


def lineage_complete(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    text = " ".join(row_value(value) for row in rows_map["lineage"] for value in row.values())
    return all(token in text for token in ["2612", "1762", "1763"])


def conditional_theorem_present(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("hom_id") == "HOM2613_1_conditional_meta_theorem"
        and row.get("attempt_status") == "EXACT_CONDITIONAL_META_THEOREM"
        for row in rows_map["hom"]
    )


def hom_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("hom_id") == "HOM2613_5_current_verdict"
        and row.get("attempt_status") == "THEOREM_CONTRACT_READY_PARENT_UNSIGNED"
        and "DELTA_W_RETAINED" in row.get("would_imply", "")
        for row in rows_map["hom"]
    )


def generator_debts_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("invariant_id") == "IH2613_7_verdict"
        and row.get("status") == "FAIL_CURRENT_CLAIM_GENERATOR_DEBTS_RETAINED"
        for row in rows_map["invariant"]
    )


def source_functor_unsigned(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("functor_id") == "SF2613_4_verdict"
        and row.get("status") == "FAIL_CURRENT_CLAIM_SOURCE_FUNCTOR_PARENT_UNSIGNED"
        for row in rows_map["source_functor"]
    )


def deltaw_interface_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["deltaw"]
    has_delta = any(row.get("deltaw_id") == "DW2613_1_delta_w_A" for row in rows)
    return has_delta and all(str(row.get("valid_for_claim", "false")).lower() == "false" for row in rows)


def ub_power_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("deltaw_id") == "DW2613_7_R_source_direct" and "U_B" in row.get("equation_or_bound", "")
        for row in rows_map["deltaw"]
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("status_id") == "SZ2613_4_local_GR" and row.get("status") == "NOT_CLAIMABLE"
        for row in rows_map["source_zero"]
    )


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(str(row.get("gate_pass", "false")).lower() == "false" for row in rows_map["claim_gates"])


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("decision_id") == "DEC2613_3_best_next"
        and "SPECIES_LABEL_FORGETTING" in row.get("decision", "")
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("next_id") == "NEXT2613_0_primary"
        and row.get("status") == "selected"
        and "species-label" in row.get("doc", "")
        for row in rows_map["next"]
    )


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2613*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL2613_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present"),
        ("VAL2613_01_lineage_complete", lineage_complete(rows_map), "lineage covers 2612 current gate plus 1762/1763 prior Hom branches"),
        ("VAL2613_02_conditional_theorem", conditional_theorem_present(rows_map), "no-Hom conditional theorem recorded"),
        ("VAL2613_03_hom_not_promoted", hom_not_promoted(rows_map), "no-Hom theorem remains unpromoted"),
        ("VAL2613_04_generator_debts_retained", generator_debts_retained(rows_map), "invariant-generator debts retained"),
        ("VAL2613_05_source_functor_unsigned", source_functor_unsigned(rows_map), "label-forgetting source functor remains parent-unsigned"),
        ("VAL2613_06_deltaw_nonclaim", deltaw_interface_nonclaim(rows_map), "delta_w interface remains nonclaim"),
        ("VAL2613_07_U_B_power_retained", ub_power_retained(rows_map), "explicit U_B source-residual factor retained"),
        ("VAL2613_08_source_zero_blocked", source_zero_blocked(rows_map), "source/local-GR status remains blocked"),
        ("VAL2613_09_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked"),
        ("VAL2613_10_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false"),
        ("VAL2613_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        ("VAL2613_12_formalization_untouched", no_formalization_artifacts(), "no 2613 outputs found under formalization-workbench"),
        ("VAL2613_13_decision_next", decision_next(rows_map), "decision selects species-label forgetting route"),
        ("VAL2613_14_next_selected", next_selected(rows_map), "next target selected"),
        (
            "VAL2613_15_branch_copies",
            all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"]),
            "nonclaim branch copies exist and parse",
        ),
        ("VAL2613_16_pycache_absent", pycache_absent(), "scripts __pycache__ absent"),
    ]
    rows: list[dict[str, Any]] = []
    for check_id, passed, detail in checks:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": detail,
                    "detail": "",
                    "valid_for_claim": False,
                }
            )
        )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, error = csv_parses(path)
        rows.append(
            with_stamp(
                {
                    "check_id": f"VAL2613_CSV_{path.stem}",
                    "status": "PASS" if ok else "FAIL",
                    "notes": f"CSV parses with {count} rows" if ok else "CSV parse failed",
                    "detail": error,
                    "valid_for_claim": False,
                }
            )
        )

    for key, path in COPY_TARGETS.items():
        ok, count, error = csv_parses(path)
        rows.append(
            with_stamp(
                {
                    "check_id": f"VAL2613_COPY_CSV_{key}",
                    "status": "PASS" if ok else "FAIL",
                    "notes": f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed",
                    "detail": error,
                    "valid_for_claim": False,
                }
            )
        )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        with_stamp(
            {
                "check_id": "VAL2613_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "notes": "2613 parent object-language Hom exclusion remains conditional and selects species-label forgetting next",
                "detail": "",
                "valid_for_claim": False,
            }
        )
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row_value(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validations: list[dict[str, Any]]) -> str:
    return "\n\n".join(
        [
            "# 2613 Y5 R2FR Parent Object-Language Hom Exclusion From Minimality Or Delta-W Bound",
            "## Summary\n"
            "- This checkpoint ports the no-source-only Hom theorem attempt into the current 26xx chain.\n"
            "- The clean theorem is exact but conditional: a strict parent object language plus source-label forgetting leaves only a common calibration constant.\n"
            "- Current MTS does not yet parent-sign primitive minimality, local invariant-algebra triviality, source label forgetting, or no-hidden-return clauses.\n"
            "- Therefore `delta_w_A`, `A_direct_matter`, and `R_source_direct` remain explicit nonclaim residuals; no local-GR/Newton/PPN/WEP/R10/clock/orbital claim is made.\n"
            "- The next least-scrutiny target is species-label forgetting before source coupling selection.",
            "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "source_key", "source_path", "source_exists", "needles_present"]),
            "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "imported_result", "2613_use"]),
            "## Hom Exclusion Theorem Attempt\n" + markdown_table(rows_map["hom"], ["hom_id", "claim_piece", "mathematical_form", "attempt_status", "would_imply", "blocker"]),
            "## Minimality Import Audit\n" + markdown_table(rows_map["minimality"], ["minimality_id", "clause", "test_form", "status", "impact", "blocker"]),
            "## Invariant Algebra Hom Audit\n" + markdown_table(rows_map["invariant"], ["invariant_id", "generator", "legal_source_route", "status", "delta_w_channel", "required_closure"]),
            "## Label-Forgetting Source Functor Audit\n" + markdown_table(rows_map["source_functor"], ["functor_id", "clause", "math_form", "status", "impact", "blocker"]),
            "## Delta-W Bound Interface\n" + markdown_table(rows_map["deltaw"], ["deltaw_id", "quantity", "definition", "status", "units", "equation_or_bound"]),
            "## Source Zero Status\n" + markdown_table(rows_map["source_zero"], ["status_id", "target", "status", "reason", "next_required"]),
            "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
            "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "why", "action"]),
            "## Next Target\n" + markdown_table(rows_map["next"], ["next_id", "status", "doc", "script", "task", "success_condition", "guardrail"]),
            "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
            "## Validation\n" + markdown_table(validations, ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        ]
    ) + "\n"


def main() -> None:
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["hom_theorem"], rows_map["hom"])
    write_csv(OUTPUTS["minimality_import"], rows_map["minimality"])
    write_csv(OUTPUTS["invariant_hom"], rows_map["invariant"])
    write_csv(OUTPUTS["source_functor"], rows_map["source_functor"])
    write_csv(OUTPUTS["deltaw_bound"], rows_map["deltaw"])
    write_csv(OUTPUTS["source_zero"], rows_map["source_zero"])
    write_csv(OUTPUTS["claim_gates"], rows_map["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], rows_map["decisions"])
    write_csv(OUTPUTS["next_target"], rows_map["next"])
    rows_map["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_map["branch_copies"])
    validations = validation_rows(rows_map)
    write_csv(OUTPUTS["validation"], validations)
    DOC.write_text(build_markdown(rows_map, validations), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation={OUTPUTS['validation']}")
    print(f"2613 validation {validations[-1]['status']}")


if __name__ == "__main__":
    main()
