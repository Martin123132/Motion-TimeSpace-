from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2689"
BRANCH_ID = "Y5_R2FR_TOTAL_PARENT_ACTION_SOURCE_LABEL_FORGETTING_OR_DELTA_W_COMPONENT_VALUES_2689"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"

DOC_PATH = ROOT / "2689-Y5-R2FR-total-parent-action-source-label-forgetting-or-delta-w-component-values.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2689_SOURCE_REGISTER.csv",
    "parent_action_audit": RESIDUALS / "P8_Y5_R2FR_2689_TOTAL_PARENT_ACTION_SOURCE_FUNCTOR_AUDIT.csv",
    "label_forgetting_attempt": RESIDUALS / "P8_Y5_R2FR_2689_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "owner_gate": RESIDUALS / "P8_Y5_R2FR_2689_PARENT_ACTION_OWNER_GATE.csv",
    "deltaw_values": RESIDUALS / "P8_Y5_R2FR_2689_DELTAW_COMPONENT_VALUE_ROWS_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2689_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2689_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2689_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2689_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2689_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2689_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2689_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_parent_action_audit": LOCAL_BOUNDS / "total_parent_action_source_functor_audit_2689_NONCLAIM.csv",
    "local_deltaw_values": LOCAL_BOUNDS / "deltaw_component_value_rows_2689_NONCLAIM.csv",
    "wep_parent_action_audit": WEP_RESIDUALS / "total_parent_action_source_functor_audit_2689_NONCLAIM.csv",
    "wep_deltaw_values": WEP_RESIDUALS / "deltaw_component_value_rows_2689_NONCLAIM.csv",
    "source_weight_deltaw_values": SOURCE_WEIGHT / "DELTAW_COMPONENT_VALUE_ROWS_2689_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2689_2688_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2688_NEXT_TARGET.csv",
        "required_needles": ["NEXT2688_0_selected", "total parent action plus source-label forgetting", "formalization-workbench edits"],
        "purpose": "confirms selected 2689 action/source-label-forgetting target",
    },
    {
        "source_id": "SRC2689_2688_DECISIONS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2688_DECISION_LEDGER.csv",
        "required_needles": ["ATTACK_TOTAL_PARENT_ACTION_SOURCE_LABEL_FORGETTING_NEXT", "source functor owner", "DELTAW_VALUES_STAGED_NONCLAIM"],
        "purpose": "imports 2688 verdict that source-functor owner is the missing hinge",
    },
    {
        "source_id": "SRC2689_2688_DELTW",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2688_DELTAW_COMPONENT_VALUE_REQUIREMENTS_NONCLAIM.csv",
        "required_needles": ["DWBV2688_10_acceptance", "FINITE_DELTAW_VALUES_STAGED_NONCLAIM", "DWBV2688_9_no_cancellation"],
        "purpose": "imports 2688 Delta_w component-value requirements",
    },
    {
        "source_id": "SRC2689_1055_PARENT_ACTION",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
        "required_needles": ["PAC1055_4_source_label_forgetting", "PAC1055_6_single_parent_action", "CONDITIONAL_LEMMA_NOT_PARENT_DERIVED"],
        "purpose": "imports parent action/source-label contract candidate",
    },
    {
        "source_id": "SRC2689_1055_GATES",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
        "required_needles": ["ADG1055_3_source_label_forgetting", "CONDITIONAL_LEMMA_NOT_PARENT_SIGNED", "ADG1055_4_radiative_closure"],
        "purpose": "imports contract adoption blockers",
    },
    {
        "source_id": "SRC2689_2485_NORMAL_FORM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_NORMAL_FORM_2485_NORMAL_FORM_CONTRACT.csv",
        "required_needles": ["NF2485_0_parent_action_skeleton", "SKELETON_WRITTEN_NOT_PARENT_DERIVED", "NF2485_2_public_field_equation"],
        "purpose": "imports local parent-action normal-form skeleton",
    },
    {
        "source_id": "SRC2689_2648_ATTEMPT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_SOURCE_FUNCTOR_LABEL_FORGETTING_2648_LABEL_FORGETTING_ATTEMPT.csv",
        "required_needles": ["SFL2648_3_conditional_uniqueness", "PRE_ACTION_WEIGHT_COUNTERMODEL_SURVIVES", "SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_PARENT_DERIVED"],
        "purpose": "imports source-functor label-forgetting attempt",
    },
    {
        "source_id": "SRC2689_2648_CLAUSES",
        "relative_path": "source-intake/mts_residuals/P8_Y5_SOURCE_FUNCTOR_LABEL_FORGETTING_2648_CLAUSE_AUDIT.csv",
        "required_needles": ["LFA2648_0_domain_quotient", "NO_SOURCE_PREFACTOR_NOT_DERIVED", "LFA2648_5_verdict"],
        "purpose": "imports clause audit for q_src/no-prefactor/no-spurion package",
    },
    {
        "source_id": "SRC2689_2616_SHADOW",
        "relative_path": "source-intake/mts_residuals/P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_SHADOW_BAN_ATTEMPT.csv",
        "required_needles": ["SSB2616_1_variational_owner_filter", "SSB2616_4_no_nonHilbert_label_current", "CONTRACT_READY_PARENT_UNSIGNED"],
        "purpose": "imports source-shadow and non-Hilbert current bypasses",
    },
    {
        "source_id": "SRC2689_1905_CONNECTED",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1905_CONNECTED_MATTER_CATEGORY_ATTEMPT.csv",
        "required_needles": ["CMC1905_1_naturality", "CONNECTED_MATTER_CATEGORY_NOT_PARENT_DERIVED", "CMC1905_5_verdict"],
        "purpose": "imports connected matter category conditional theorem",
    },
    {
        "source_id": "SRC2689_1905_LINE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1905_ACTION_DENSITY_LINE_OWNER_GATE.csv",
        "required_needles": ["ADL1905_0_line_owner", "ACTION_DENSITY_LINE_OWNER_NOT_DERIVED", "ADL1905_5_verdict"],
        "purpose": "imports action-density line owner gap",
    },
    {
        "source_id": "SRC2689_2643_QVIS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv",
        "required_needles": ["QVIS2643_4_no_source_only_slot", "SOURCE_WEIGHT_SEAM_OPEN", "QVIS2643_6_verdict"],
        "purpose": "imports common-matter descent/no-source-only seam",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def parent_action_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TPA2689_0_target",
            "total parent action/source functor owner",
            "One parent variational object owns geometry, ordinary matter, source extraction, coupling selection, readout and residual slots before fitting.",
            "TARGET_SHARP",
            "This is the object that would make source-label forgetting a derivation rather than a typed closure.",
            "2688:DEC2688_3_next;1055:PAC1055_6_single_parent_action",
        ),
        (
            "TPA2689_1_single_parent_action_shape",
            "single action skeleton",
            "S_parent = S_geom + S_hidden + S_EM[q(Phi)] + sum_A S_A[Psi_A,q(Phi),theta_A] + S_boundary + S_res.",
            "SCHEMA_EXISTS_NOT_DERIVED",
            "The skeleton is useful, but existing sources call it contract/skeleton rather than a parent-derived MTS Lagrangian with variations.",
            "1055:PAC1055_6_single_parent_action;2485:NF2485_0_parent_action_skeleton",
        ),
        (
            "TPA2689_2_total_hilbert_source",
            "total Hilbert source extraction",
            "T_total := 2/sqrt(-g_obs) delta S_matter/delta g_obs = sum_A T_A, computed before source/readout selection.",
            "EXACT_CONDITIONAL_SUBTHEOREM",
            "Works once one common matter action and variation-before-readout are signed; it does not forbid pre-action weights by itself.",
            "2648:SFL2648_1_hilbert_owner_if_common_action;1838:SLG1838_0_total_Hilbert_source",
        ),
        (
            "TPA2689_3_source_domain_quotient",
            "q_src labelled-family quotient",
            "q_src({(T_A,A)}) = T_total before coupling selection, and F_src accepts only T_total.",
            "SOURCE_DOMAIN_QUOTIENT_NOT_CONSTRUCTED",
            "No current parent construction proves the source functor has no access to species/source labels.",
            "2648:LFA2648_0_domain_quotient;1893:SFL1893_0_target",
        ),
        (
            "TPA2689_4_no_prefactor_package",
            "no pre-action source prefactor",
            "w_A S_A, kappa_A T_A and source-only material multipliers are not legal parent objects before variation.",
            "NO_SOURCE_PREFACTOR_NOT_DERIVED",
            "The countermodel survives: if w_A is legal before variation, Hilbert variation returns a weighted source.",
            "2648:SFL2648_4_preaction_prefactor_obstruction;2648:LFA2648_1_no_prefactors",
        ),
        (
            "TPA2689_5_source_shadow_nonhilbert",
            "no shadow/non-Hilbert labelled current",
            "T_active = delta S_matter/delta e_obs and J_NH,label=0, or any bypass is an explicit residual.",
            "SOURCE_SHADOW_BAN_UNSIGNED",
            "Bianchi filters inconsistency, but a real conserved shadow block or projector can still carry labels unless excluded or bounded.",
            "2616:SSB2616_1_variational_owner_filter;2616:SSB2616_4_no_nonHilbert_label_current",
        ),
        (
            "TPA2689_6_connected_action_line",
            "connected matter category/action-density line",
            "Connected ordinary matter plus one action-density line collapses relative weights to a common calibration mode.",
            "EXACT_CONDITIONAL_PARENT_EDGES_UNSIGNED",
            "Naturality is clean, but parent-owned graph edges and the line/measure/current owner are not signed.",
            "1905:CMC1905_1_naturality;1905:ADL1905_0_line_owner",
        ),
        (
            "TPA2689_7_readout_radiative_stability",
            "readout/radiative/projector no-reentry",
            "Post-variation maps cannot regenerate source labels or alter the active-source coefficient codomain.",
            "READOUT_RADIATIVE_STABILITY_UNSIGNED",
            "Even a tree source theorem does not survive to WEP/R10/PPN/clocks/orbits until this is parent-signed or residualized.",
            "1055:ADG1055_4_radiative_closure;2648:LFA2648_2_variation_before_readout",
        ),
        (
            "TPA2689_8_common_coupling_owner",
            "single universal source coupling/common mode",
            "F_src(T_total)=kappa_univ T_total, with G/kappa/GM common-mode calibration only after no label/time/range/frame dependence.",
            "COMMON_COUPLING_OWNER_UNSIGNED",
            "A common factor can be calibrated, but relative source labels can hide in the calibration if the previous gates are open.",
            "2648:LFA2648_4_projected_mass_calibration;1055:ADG1055_3_source_label_forgetting",
        ),
        (
            "TPA2689_9_verdict",
            "promote total parent action/source-label forgetting",
            "The current corpus parent-derives one action/source functor that forgets species labels before source coupling.",
            "TOTAL_PARENT_ACTION_SOURCE_LABEL_FORGETTING_NOT_DERIVED",
            "The clean theorem is now localized to q_src + no-prefactor + no-shadow + action-line/readout/coupling owner; current evidence does not sign the package.",
            "TPA2689_0_target through TPA2689_8_common_coupling_owner",
        ),
    ]
    return [
        {
            "audit_id": row[0],
            "claim_piece": row[1],
            "formal_statement": row[2],
            "current_status": row[3],
            "derivation_or_obstruction": row[4],
            "source_anchor": row[5],
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def label_forgetting_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SLF2689_0_target",
            "source-label forgetting theorem",
            "q_src({(T_A,A)})=T_total and F_src(q_src)=kappa_univ T_total with no access to A, w_A, kappa_A, material masks, preparation labels or readout selectors.",
            "TARGET_SHARP",
            "This is the narrow theorem that kills Delta_w_species and source-only relative weights.",
            "2648:SFL2648_0_target;2688:PSC2688_4_source_label_forgetting",
        ),
        (
            "SLF2689_1_exact_conditional",
            "conditional uniqueness after labels are forgotten",
            "If F_src sees only T_total and is local/covariant/additive/natural on one observed coframe with one calibrated scale, then F_src(T_total)=kappa_univ T_total.",
            "EXACT_CONDITIONAL_THEOREM",
            "Once labels are absent, relative weights cannot be formed; the issue is deriving absence of labels.",
            "2648:SFL2648_3_conditional_uniqueness;1893:SFL1893_3_conditional_uniqueness",
        ),
        (
            "SLF2689_2_ward_bianchi_filter",
            "Ward/Bianchi bridge",
            "Diffeomorphism invariance conserves the source selected by the action and Bianchi rejects nonconserved shadow sources.",
            "VALID_FILTER_NOT_LABEL_FORGETTING",
            "Ward/Bianchi can police consistency but cannot choose between T_total and sum_A kappa_A T_A when the latter is conserved.",
            "2648:SFL2648_2_ward_not_enough;2616:SSB2616_2_conservation_filter",
        ),
        (
            "SLF2689_3_preaction_countermodel",
            "pre-action source weights",
            "S_matter=sum_A w_A S_A Hilbert-varies to sum_A w_A T_A if w_A is a legal parent coefficient.",
            "COUNTERMODEL_SURVIVES",
            "This is the cleanest reason source-label forgetting cannot be claimed from total variation alone.",
            "2648:SFL2648_4_preaction_prefactor_obstruction;1055:CE1055_3_relative_source_weight",
        ),
        (
            "SLF2689_4_shadow_countermodel",
            "source-shadow/readout/non-Hilbert bypass",
            "A post-variation source map, material projector, readout selector or non-Hilbert labelled current can recreate source labels after Hilbert extraction.",
            "BYPASS_RETAINED_AS_RESIDUAL",
            "The bypass is isolated but not eliminated; it must be theorem-zero or carried as finite Delta_w/J_NH/projector rows.",
            "2616:SSB2616_5_current_verdict;2643:QVIS2643_4_no_source_only_slot",
        ),
        (
            "SLF2689_5_connected_category_support",
            "ordinary connected matter support",
            "Connected parent-owned matter graph plus one action-density line would collapse ordinary-sector relative weights to common mode.",
            "EXACT_CONDITIONAL_SUPPORT",
            "Good route, but parent-owned graph edges and line owner remain unsigned.",
            "1905:CMC1905_5_verdict;1905:ADL1905_5_verdict",
        ),
        (
            "SLF2689_6_local_GR_implication",
            "impact on local GR/Newton",
            "A signed theorem would remove a major source-universality obstruction for Newton/PPN/WEP/R10 source channels.",
            "PARTIAL_DOWNSTREAM_ONLY",
            "It would not by itself prove EH origin, kappa owner, residual silence or PPN field equations.",
            "1055:TC1055_4_local_GR;2688:STATUS2688_4_local_gr",
        ),
        (
            "SLF2689_7_verdict",
            "promote source-label forgetting",
            "The present MTS corpus derives source-label forgetting from the total parent action rather than imposing it.",
            "SOURCE_LABEL_FORGETTING_NOT_PARENT_DERIVED",
            "Conditional theorem stands; parent q_src/no-prefactor/no-shadow/action-line/readout package is unsigned.",
            "SLF2689_0_target through SLF2689_6_local_GR_implication",
        ),
    ]
    return [
        {
            "attempt_id": row[0],
            "claim_piece": row[1],
            "formal_statement": row[2],
            "status": row[3],
            "proof_or_obstruction": row[4],
            "source_anchor": row[5],
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("POG2689_0_explicit_parent_lagrangian", "fully varied MTS parent Lagrangian with field list, boundary term and symplectic/current owner", "FAIL_SCHEMA_ONLY", "turns contract into derivation", "action remains an adoption template", "1055:PAC1055_6_single_parent_action", "false"),
        ("POG2689_1_q_src", "source-domain quotient q_src maps labelled family to total Hilbert source before coupling", "FAIL_QSRC_NOT_CONSTRUCTED", "species labels cannot feed coupling", "Delta_w_species remains legal", "2648:LFA2648_0_domain_quotient", "false"),
        ("POG2689_2_no_prefactor", "no w_A S_A, kappa_A T_A or source-only material multiplier in parent object language", "FAIL_NO_PREFACTOR_NOT_DERIVED", "weighted Hilbert source countermodel killed", "pre-action weight countermodel survives", "2648:LFA2648_1_no_prefactors", "false"),
        ("POG2689_3_shadow_current", "no source-shadow/projector/non-Hilbert labelled source current", "FAIL_SOURCE_SHADOW_UNSIGNED", "post-Hilbert label reentry killed", "shadow/projector/J_NH rows remain live", "2616:SSB2616_5_current_verdict", "false"),
        ("POG2689_4_action_line", "connected ordinary matter graph plus one action-density/measure/current owner", "FAIL_ACTION_LINE_UNSIGNED", "ordinary relative weights collapse to common mode", "ordinary Delta_w components remain explicit", "1905:ADL1905_5_verdict", "false"),
        ("POG2689_5_readout_stability", "readout/radiative/projector maps preserve label-forgotten source domain", "FAIL_READOUT_STABILITY_UNSIGNED", "tree theorem transfers to arenas", "arena kernels and transfer coefficients remain finite", "1055:ADG1055_4_radiative_closure", "false"),
        ("POG2689_6_ward_guard", "Ward/Bianchi consistency is used only as a filter, not a source-domain proof", "PASS_GUARD_ONLY", "prevents Ward-only promotion", "none; guard only", "2648:SFL2648_2_ward_not_enough", "true"),
        ("POG2689_7_no_cancellation_guard", "finite Delta_w scores cannot pass through fitted cancellations", "PASS_GUARD_ONLY", "keeps empirical branch honest", "none; guard only", "2688:DWBV2688_9_no_cancellation", "true"),
        ("POG2689_8_verdict", "total parent action/source-label forgetting package can be claimed", "CLAIM_BLOCKED", "source-label theorem promotable", "package remains a derivation target", "POG2689_0 through POG2689_7", "false"),
    ]
    return [
        {
            "gate_id": row[0],
            "required_clause": row[1],
            "current_status": row[2],
            "if_signed": row[3],
            "if_unsigned": row[4],
            "source_anchor": row[5],
            "gate_pass": row[6],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def deltaw_value_rows() -> list[dict[str, Any]]:
    rows = [
        ("DWV2689_0_delta_w_species", "Delta_w_species", "relative pre-variation source/action weight after common-mode subtraction", "epsilon_A vector or theorem-zero no-prefactor/q_src certificate", "dimensionless", "MISSING_PARENT_VALUE_OR_ZERO_THEOREM", "WEP;R10;PPN;clock;orbital"),
        ("DWV2689_1_current_rescale", "c_A_current_rescale", "post-variation labelled source-current rescale", "source-current owner/no-rescale theorem or coefficient row", "dimensionless", "MISSING_CURRENT_OWNER_VALUE", "WEP;R10;PPN;clock;orbital"),
        ("DWV2689_2_source_shadow", "Delta_w_shadow", "source-shadow/projector/readout material selector bypass", "source-shadow ban theorem or finite shadow coefficient bounds", "dimensionless/source-normalized", "MISSING_SHADOW_BAN_OR_VALUE", "WEP;PPN;orbital"),
        ("DWV2689_3_action_measure", "Delta_w_measure", "relative action-density/measure/Jacobian multiplier", "one action-density/measure owner or numeric Z_A^measure bounds", "dimensionless log response", "MISSING_ACTION_LINE_VALUE", "WEP;R10;clock"),
        ("DWV2689_4_nonhilbert_current", "J_NH_label", "label-carrying non-Hilbert/source exchange/improvement current", "J_NH,label=0 theorem or finite C_i J_NH_i coefficient row", "declared current units", "MISSING_NONHILBERT_CURRENT_VALUE", "WEP;PPN;orbital"),
        ("DWV2689_5_readout_transfer", "K_readout_label", "readout/projector/radiative map that reintroduces source labels", "readout no-reentry theorem or transfer kernel bound", "arena-specific", "MISSING_READOUT_TRANSFER_KERNEL", "WEP;R10;clock;orbital"),
        ("DWV2689_6_common_projector", "P_perp", "common-mode projector removing universal calibration", "composition weights p_A and common-mode convention", "dimensionless projector", "MISSING_COMMON_PROJECTOR_INPUT", "all"),
        ("DWV2689_7_arena_kernels", "K_arena/tau_arena", "projection from parent Delta_w vector to observable residual", "WEP/R10/PPN/clock/orbital source-test kernels, units and readout conventions", "arena declared", "MISSING_ARENA_PROJECTION_KERNELS", "all"),
        ("DWV2689_8_no_cancellation", "no_cancellation_envelope", "sum_i |K_i Delta_w_i| unless parent identity proves signed cancellation", "policy already written; covariance envelope must be sourced if used", "policy", "POLICY_WRITTEN_GUARD_ONLY", "all"),
        ("DWV2689_9_acceptance", "finite_Delta_w_value_acceptance", "all components have theorem-zero or numeric parent values plus arena projections before scoring", "values/bounds, source paths, units, kernels, uncertainties and no-cancellation rule", "mixed", "FINITE_DELTAW_VALUE_ROWS_NONCLAIM", "all"),
    ]
    return [
        {
            "row_id": row[0],
            "component": row[1],
            "definition": row[2],
            "required_input": row[3],
            "units": row[4],
            "current_status": row[5],
            "arena_links": row[6],
            "numeric_value_present": "false",
            "source_path_present": "false",
            "projection_ready": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    cases = [
        ("DRY2689_0_all_parent_signed", "true", "true", "true", "true", "true", "true", "false", "false", "THEOREM_READY_IF_PARENT_SIGNED"),
        ("DRY2689_1_action_schema_only", "true", "false", "false", "false", "false", "false", "false", "false", "REJECT_ACTION_SCHEMA_ONLY"),
        ("DRY2689_2_ward_only", "false", "false", "false", "false", "false", "false", "false", "true", "REJECT_WARD_ONLY"),
        ("DRY2689_3_qsrc_no_prefactor", "true", "true", "false", "true", "true", "true", "false", "false", "REJECT_PREACTION_PREFACTOR_COUNTERMODEL"),
        ("DRY2689_4_shadow_open", "true", "true", "true", "false", "true", "true", "false", "false", "REJECT_SOURCE_SHADOW_OPEN"),
        ("DRY2689_5_values_missing", "false", "false", "false", "false", "false", "false", "false", "false", "REJECT_DELTW_VALUES_MISSING"),
        ("DRY2689_6_values_without_kernels", "false", "false", "false", "false", "false", "true", "false", "false", "REJECT_VALUES_WITHOUT_PROJECTIONS"),
        ("DRY2689_7_cancellation_only", "false", "false", "false", "false", "false", "true", "true", "false", "REJECT_CANCELLATION_ONLY_PASS"),
    ]
    return [
        {
            "case_id": row[0],
            "single_action": row[1],
            "q_src_signed": row[2],
            "no_prefactor_signed": row[3],
            "no_shadow_signed": row[4],
            "readout_stable": row[5],
            "parent_values_present": row[6],
            "cancellation_only": row[7],
            "ward_only": row[8],
            "expected_status": row[9],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in cases
    ]


def evaluate_dryrun(case: dict[str, Any]) -> str:
    if case["cancellation_only"] == "true":
        return "REJECT_CANCELLATION_ONLY_PASS"
    if case["ward_only"] == "true":
        return "REJECT_WARD_ONLY"
    theorem_ready = (
        case["single_action"] == "true"
        and case["q_src_signed"] == "true"
        and case["no_prefactor_signed"] == "true"
        and case["no_shadow_signed"] == "true"
        and case["readout_stable"] == "true"
    )
    if theorem_ready:
        return "THEOREM_READY_IF_PARENT_SIGNED"
    if case["single_action"] == "true" and case["q_src_signed"] == "false":
        return "REJECT_ACTION_SCHEMA_ONLY"
    if case["q_src_signed"] == "true" and case["no_prefactor_signed"] == "false":
        return "REJECT_PREACTION_PREFACTOR_COUNTERMODEL"
    if case["no_shadow_signed"] == "false" and case["q_src_signed"] == "true":
        return "REJECT_SOURCE_SHADOW_OPEN"
    if case["parent_values_present"] == "true":
        return "REJECT_VALUES_WITHOUT_PROJECTIONS"
    return "REJECT_DELTW_VALUES_MISSING"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        computed = evaluate_dryrun(case)
        rows.append(
            {
                "case_id": case["case_id"],
                "computed_status": computed,
                "expected_status": case["expected_status"],
                "status_match": as_bool(computed == case["expected_status"]),
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2689_0_parent_action", "total parent action is explicit and parent-derived", "FAIL_SCHEMA_ONLY_NOT_DERIVED", "TPA2689_1_single_parent_action_shape", "false"),
        ("CG2689_1_qsrc", "source-domain quotient q_src is constructed", "FAIL_QSRC_NOT_CONSTRUCTED", "TPA2689_3_source_domain_quotient", "false"),
        ("CG2689_2_no_prefactor", "pre-action source prefactors are impossible", "FAIL_NO_SOURCE_PREFACTOR_NOT_DERIVED", "TPA2689_4_no_prefactor_package", "false"),
        ("CG2689_3_shadow", "source-shadow/non-Hilbert/readout label reentry is forbidden or bounded", "FAIL_SOURCE_SHADOW_BAN_UNSIGNED", "TPA2689_5_source_shadow_nonhilbert", "false"),
        ("CG2689_4_action_line", "connected matter action-density line owner is signed", "FAIL_ACTION_LINE_OWNER_UNSIGNED", "TPA2689_6_connected_action_line", "false"),
        ("CG2689_5_readout", "readout/radiative stability is signed", "FAIL_READOUT_STABILITY_UNSIGNED", "TPA2689_7_readout_radiative_stability", "false"),
        ("CG2689_6_deltaw_values", "finite Delta_w component values/kernels are sourced if theorem route fails", "FAIL_DELTW_VALUES_AND_KERNELS_MISSING", "DWV2689_9_acceptance", "false"),
        ("CG2689_7_guards", "Ward-only and cancellation-only shortcuts are refused", "PASS_GUARD_ONLY", "POG2689_6_ward_guard;POG2689_7_no_cancellation_guard", "true"),
        ("CG2689_8_verdict", "source coupling/local-GR branch can claim pass", "CLAIM_BLOCKED", "CG2689_0_parent_action through CG2689_7_guards", "false"),
    ]
    return [
        {
            "gate_id": row[0],
            "condition": row[1],
            "current_status": row[2],
            "source_anchor": row[3],
            "gate_pass": row[4],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2689_0_parent_action",
            "decision": "DO_NOT_PROMOTE_TOTAL_PARENT_ACTION_SOURCE_LABEL_FORGETTING",
            "reason": "The action/source theorem is exact conditionally, but current evidence supplies contracts and schemas rather than a parent-derived MTS action with q_src and no-prefactor/no-shadow clauses.",
            "status": "SOURCE_LABEL_FORGETTING_NOT_PARENT_DERIVED",
            "next_dependency": "construct q_src and no-prefactor/no-shadow package, or fill finite Delta_w values",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2689_1_progress",
            "decision": "KEEP_THE_THEOREM_AS_THE_RIGHT_ROUTE",
            "reason": "This is still the best derivation route because a signed source functor would erase a whole class of WEP/R10/PPN source-side residuals without tuning.",
            "status": "ROUTE_SHARPENED_NOT_CLOSED",
            "next_dependency": "source-domain quotient constructor",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2689_2_fallback",
            "decision": "STAGE_DELTAW_VALUE_ROWS_WITHOUT_SCORING",
            "reason": "If q_src/no-prefactor/no-shadow cannot be derived, the honest fallback is component values and arena kernels, not a verbal pass.",
            "status": "DELTAW_VALUE_ROWS_NONCLAIM",
            "next_dependency": "first source-ready Delta_w component value row plus kernels",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2689_3_next",
            "decision": "ATTACK_QSRC_NO_PREFACTOR_NO_SHADOW_PACKAGE_NEXT",
            "reason": "The next non-circular leap is to construct the source-domain quotient and close the two bypasses that make q_src non-theorem-grade.",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "2690 source-domain quotient plus no-prefactor/no-shadow package or Delta_w first value row",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2689_0_selected",
            "kind": "selected",
            "target_doc": "2690-Y5-R2FR-source-domain-quotient-no-prefactor-no-shadow-package-or-delta-w-first-value-row.md",
            "target_script": "scripts/Y5_R2FR_source_domain_quotient_no_prefactor_no_shadow_package_or_delta_w_first_value_row_2690.py",
            "purpose": "try to construct q_src and prove no pre-action source prefactor or source-shadow label reentry; if it fails, create the first source-ready Delta_w component value row as nonclaim",
            "acceptance_gate": "q_src maps labelled ordinary Hilbert source family to T_total before coupling, no w_A/kappa_A/source-shadow bypass remains, or finite Delta_w value row has explicit value/source/unit/projection blockers",
            "forbidden_shortcuts": "Ward-only proof; action schema as derivation; source labels forgotten by preference; tau=1 shortcut; bound-as-prediction; cancellation-only pass; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2689_0_theorem", "source-label forgetting", "EXACT_CONDITIONAL_NOT_PARENT_DERIVED", "the theorem form is now crisp but the parent owner package is unsigned"),
        ("STATUS2689_1_parent_action", "total parent action", "SCHEMA_EXISTS_NOT_DERIVED", "one-action shape exists as a contract but not as a fully varied MTS parent Lagrangian"),
        ("STATUS2689_2_coupling", "source coupling", "COUPLING_HINGE_LOCALIZED", "missing hinge is q_src/no-prefactor/no-shadow/readout package, not generic coupling fog"),
        ("STATUS2689_3_empirical", "Delta_w fallback", "VALUE_ROWS_NONCLAIM", "component values and kernels are explicit blockers before any scoring"),
        ("STATUS2689_4_local_gr", "local GR/Newton", "SOURCE_SIDE_NARROWED_BUT_NOT_DERIVED", "source universality is narrowed but EH/coupling/PPN/residual gates remain open"),
    ]
    return [
        {
            "status_id": row[0],
            "sector": row[1],
            "status": row[2],
            "meaning": row[3],
            "claim_allowed": "false",
            "next_action": "run 2690 q_src/no-prefactor/no-shadow package target",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2689_{name}",
            "absolute_path": str(path),
            "relative_path": rel_path(path),
            "exists": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for name, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    parent_action: list[dict[str, Any]],
    label_attempt: list[dict[str, Any]],
    owner_gates: list[dict[str, Any]],
    deltaw: list[dict[str, Any]],
    dryrun_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    parent_verdict_blocked = any(row["audit_id"] == "TPA2689_9_verdict" and row["current_status"] == "TOTAL_PARENT_ACTION_SOURCE_LABEL_FORGETTING_NOT_DERIVED" for row in parent_action)
    conditional_theorem = any(row["attempt_id"] == "SLF2689_1_exact_conditional" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in label_attempt)
    label_verdict_blocked = any(row["attempt_id"] == "SLF2689_7_verdict" and row["status"] == "SOURCE_LABEL_FORGETTING_NOT_PARENT_DERIVED" for row in label_attempt)
    owner_blocked = any(row["gate_id"] == "POG2689_8_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in owner_gates)
    guard_rows_ok = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in owner_gates)
    deltaw_nonclaim = all(
        row["valid_for_claim"] == "false"
        and row["claim_allowed"] == "false"
        and row["score_ready"] == "false"
        and row["numeric_value_present"] == "false"
        for row in deltaw
    )
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in claim_gates)
    overall_claim_blocked = any(row["gate_id"] == "CG2689_8_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2690" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2689_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2689_parent_action_not_promoted", parent_verdict_blocked, "total parent action/source-label forgetting is not promoted"),
        ("VAL2689_conditional_theorem_written", conditional_theorem, "exact conditional source-label theorem is written"),
        ("VAL2689_label_forgetting_not_promoted", label_verdict_blocked, "source-label forgetting remains unsigned"),
        ("VAL2689_owner_gates_block", owner_blocked and guard_rows_ok, "owner gates block claims while retaining guards"),
        ("VAL2689_deltaw_rows_nonclaim", deltaw_nonclaim, "Delta_w value rows remain nonclaim/not score-ready"),
        ("VAL2689_dryrun_refusals", dryrun_ok, "dry-run refuses action-schema-only, Ward-only, prefactor, shadow, missing-value and cancellation shortcuts"),
        ("VAL2689_claim_gates_block_claims", claim_blocked and overall_claim_blocked, "all claim gates block promotion"),
        ("VAL2689_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2689_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2689_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2689_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2689_next_target_selected", next_target_ok, "2690 q_src/no-prefactor/no-shadow target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2689_OVERALL",
            "passed": as_bool(overall),
            "detail": "2689 localizes the coupling hinge to q_src/no-prefactor/no-shadow/readout owner package, refuses source-label promotion, and stages Delta_w value rows",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(
    source_rows: list[dict[str, Any]],
    parent_action: list[dict[str, Any]],
    label_attempt: list[dict[str, Any]],
    owner_gates: list[dict[str, Any]],
    deltaw: list[dict[str, Any]],
    dry_cases: list[dict[str, Any]],
    dry_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2689 - Y5/R2FR Total Parent Action Source-Label Forgetting or Delta-w Component Values",
                "",
                "## Private Verdict",
                "",
                "The coupling hinge is now properly named: source-label forgetting is exact once a parent source-domain quotient `q_src`, no-prefactor theorem, no-shadow-current theorem, action-line owner and readout stability are all signed. Current evidence does not sign that package.",
                "",
                "So this is not a claim-grade GR/Newton step yet. But it is progress: the missing thing is no longer vague coupling mysticism; it is a finite owner package that can be attacked clause by clause.",
                "",
                "No source-label theorem, Delta_w=0 theorem, local-GR, WEP, R10, PPN, clock, orbital, Newton-source, GitHub, or public claim is allowed from this checkpoint.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Total Parent Action Source-Functor Audit",
                "",
                markdown_table(parent_action),
                "",
                "## Source-Label Forgetting Theorem Attempt",
                "",
                markdown_table(label_attempt),
                "",
                "## Parent Action Owner Gate",
                "",
                markdown_table(owner_gates),
                "",
                "## Delta-w Component Value Rows",
                "",
                markdown_table(deltaw),
                "",
                "## Dry-Run Cases",
                "",
                markdown_table(dry_cases),
                "",
                "## Dry-Run Results",
                "",
                markdown_table(dry_results),
                "",
                "## Claim Gates",
                "",
                markdown_table(claim_gates),
                "",
                "## Decisions",
                "",
                markdown_table(decisions),
                "",
                "## Next Target",
                "",
                markdown_table(next_target),
                "",
                "## Project Status Snapshot",
                "",
                markdown_table(status),
                "",
                "## Validation",
                "",
                markdown_table(validation),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    parent_action = parent_action_audit_rows()
    label_attempt = label_forgetting_attempt_rows()
    owner_gates = owner_gate_rows()
    deltaw = deltaw_value_rows()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["parent_action_audit"], parent_action)
    write_csv(OUTPUTS["label_forgetting_attempt"], label_attempt)
    write_csv(OUTPUTS["owner_gate"], owner_gates)
    write_csv(OUTPUTS["deltaw_values"], deltaw)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_parent_action_audit"], parent_action)
    write_csv(BRANCH_OUTPUTS["local_deltaw_values"], deltaw)
    write_csv(BRANCH_OUTPUTS["wep_parent_action_audit"], parent_action)
    write_csv(BRANCH_OUTPUTS["wep_deltaw_values"], deltaw)
    write_csv(BRANCH_OUTPUTS["source_weight_deltaw_values"], deltaw)

    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validation = validation_rows(source_rows, parent_action, label_attempt, owner_gates, deltaw, dry_results, claim_gates)
    write_csv(OUTPUTS["validation"], validation)
    write_document(source_rows, parent_action, label_attempt, owner_gates, deltaw, dry_cases, dry_results, claim_gates, decisions, next_target, status, validation)

    print(f"wrote {DOC_PATH}")
    for key, path in OUTPUTS.items():
        print(f"{key}: {path}")
    for key, path in BRANCH_OUTPUTS.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
