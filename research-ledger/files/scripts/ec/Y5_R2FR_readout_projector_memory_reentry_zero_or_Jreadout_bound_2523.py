from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_READOUT_PROJECTOR_REENTRY_2523"
CHECKPOINT_ID = "2523"
DOC = ROOT / "2523-Y5-R2FR-readout-projector-memory-reentry-zero-or-Jreadout-bound.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2523_SOURCE_REGISTER.csv",
    "readout_reentry_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2523_READOUT_REENTRY_AUDIT.csv",
    "commutator_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2523_COMMUTATOR_GATE.csv",
    "jreadout_bound_rows": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2523_JREADOUT_BOUND_ROWS.csv",
    "observable_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2523_OBSERVABLE_GATE.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2523_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2523_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2523_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2523_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2523_VALIDATION.csv",
}

BRANCH_COPIES = {
    "readout_reentry_audit": ROOT
    / "source-intake"
    / "local_bounds"
    / "Readout_reentry_audit_2523_NONCLAIM.csv",
    "jreadout_bound_rows": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Jreadout_bound_rows_2523_NONCLAIM.csv",
    "commutator_gate": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2523_COMMUTATOR_GATE_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2523_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2523_0_2522_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2522_NEXT_TARGET.csv",
        "needles": ["NEXT2522_0_selected", "J_readout"],
        "role": "authoritative 2522 handoff to readout/projector memory re-entry",
    },
    {
        "source_id": "SRC2523_1_2522_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2522_VALIDATION.csv",
        "needles": ["VAL2522_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
    {
        "source_id": "SRC2523_2_2521_jmem_rows",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2521_JMEM_DRIVE_BOUND_ROWS.csv",
        "needles": ["JDRV2521_4_readout_projector", "MISSING_READOUT_COMMUTATOR_ZERO_OR_BOUND"],
        "role": "J_mem already exposes J_readout as an unsolved drive component",
    },
    {
        "source_id": "SRC2523_3_2520_qmem_rows",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2520_QMEM_COMPONENT_ROWS.csv",
        "needles": ["QMC2520_5_Nsrc", "QMC2520_11_Qmem_total"],
        "role": "Q_mem receives source-current drives through N_src/A_ref",
    },
    {
        "source_id": "SRC2523_4_2522_jdirect_rows",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2522_JDIRECT_BOUND_ROWS.csv",
        "needles": ["JDIR2522_6_effective_m", "MISSING_EFFECTIVE_REENTRY_ZERO_OR_BOUND"],
        "role": "direct matter-memory checkpoint separates effective/readout re-entry from direct coupling",
    },
    {
        "source_id": "SRC2523_5_2522_argument_gate",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2522_MATTER_ARGUMENT_LIST_GATE.csv",
        "needles": ["ARG2522_5_variation_order", "GUARD_ACTIVE_REENTRY_NOT_ZEROED"],
        "role": "variation-order guard remains active and must be handled here",
    },
    {
        "source_id": "SRC2523_6_1898_commutator",
        "path": "source-intake/microscope/branch_locked_wep/residuals/P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
        "needles": [
            "RVC1898_1_pure_postprocessing_zero",
            "RVC1898_2_projection_commutator_survives",
            "RVC1898_5_verdict",
        ],
        "role": "sharpest prior theorem/countermodel pair for readout variation",
    },
    {
        "source_id": "SRC2523_7_2508_countermodels",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2508_SOURCE_ONLY_COUNTERMODELS.csv",
        "needles": ["CM2508_4_readout_projector", "delta(Pi J)=Pi delta J"],
        "role": "source-only-slot countermodel showing projector re-entry survives",
    },
    {
        "source_id": "SRC2523_8_2508_theorem_gates",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2508_NO_SOURCE_SLOT_THEOREM_GATES.csv",
        "needles": ["GATE2508_4_variation_order", "FAIL_GENERAL_READOUT_ORDER_UNSIGNED"],
        "role": "variation-before-readout remains unsigned in object-language gate",
    },
    {
        "source_id": "SRC2523_9_2487_coframe",
        "path": "2487-Y5-R2FR-observed-coframe-functor-and-vertical-generator-certificate-or-DObs-leak-row.md",
        "needles": ["DOK2487_3_current_verdict", "DOBS_E_KERNEL_ZERO_NOT_SIGNED"],
        "role": "observed coframe/readout functor still has a finite leak route",
    },
    {
        "source_id": "SRC2523_10_2486_quotient",
        "path": "2486-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md",
        "needles": ["RO2486_0_variation_before_readout", "GATE2486_3_matter_descent"],
        "role": "quotient theorem is conditional and requires q-basic readout before use",
    },
    {
        "source_id": "SRC2523_11_2503_worldtube",
        "path": "2503-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R-eq-fill.md",
        "needles": ["RES2503_5_I_commutator", "ZERO_BOUNDARY_FLUX_NOT_DERIVED_CURRENT_CORPUS"],
        "role": "Pi_M/worldtube/boundary selector carries the central local-source commutator debt",
    },
]


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
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells: list[str] = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["path"]
        text = read_text(path)
        found_needles = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found_needles),
                role=spec["role"],
                source_pass=path.exists() and len(found_needles) == len(spec["needles"]),
            )
        )
    return rows


def readout_reentry_audit_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "audit_id": "JRZ2523_0_definition",
            "claim_piece": "readout/projector memory-source re-entry",
            "formal_statement": "J_readout := ||Pi_CoeffSource([delta_m,R_A]J_source)|| plus pre-variation, calibration, projector, and support-map commutator pieces assigned outside J_direct_matter",
            "result": "DEFINITION_LOCKED",
            "blocking_gap": "definition by itself does not prove zero or provide a numeric bound",
            "effect": "separates readout/projector debt from direct matter-memory coupling",
        },
        {
            "audit_id": "JRZ2523_1_pure_postprocessing_zero",
            "claim_piece": "pure data-only postprocessing zero",
            "formal_statement": "If R_post is absent from S_parent, absent from S_eff before variation, has no codomain in Coeff_active_source, and all source coefficients are already fixed by variation, then [delta_m,R_post] contributes no source coefficient.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "blocking_gap": "actual local readouts include projectors, source worldtubes, material kernels, fitted-source maps, boundary selectors, or effective maps not signed as pure data-only",
            "effect": "keeps the clean theorem, but only for genuinely post-solution reporting maps",
        },
        {
            "audit_id": "JRZ2523_2_fixed_projector_clause",
            "claim_piece": "fixed projector/selector zero",
            "formal_statement": "If delta_m Pi_A=0, delta_m W_source=0, delta_m P_loc=0, delta_m e_obs=0, and R_A is post-variation only, then delta_m(Pi_A J)=Pi_A delta_m J and no new readout coefficient is generated.",
            "result": "EXACT_CONDITIONAL_LEMMA",
            "blocking_gap": "fixedness of Pi_M, P_loc, material projector, worldtube/support and observed coframe is not parent-signed",
            "effect": "turns the next proof route into a concrete fixed-map checklist",
        },
        {
            "audit_id": "JRZ2523_3_projector_commutator",
            "claim_piece": "projector/source-worldtube commutator",
            "formal_statement": "delta_m(Pi_A J)=Pi_A delta_m J + (delta_m Pi_A)J, so J_readout contains ||(delta_m Pi_A)J|| whenever Pi_A depends on source support, material response, domain, boundary, or the hidden branch.",
            "result": "COUNTERMODEL_ACTIVE",
            "blocking_gap": "no signed theorem kills (delta_m Pi_A)J for Pi_M/P_loc/readout/material/orbit maps",
            "effect": "general J_readout=0 is not derived",
        },
        {
            "audit_id": "JRZ2523_4_effective_prevariation",
            "claim_piece": "effective readout before variation",
            "formal_statement": "If S_eff[R_A] or a calibrated readout weight enters before variation, its derivative is a source coefficient, not a harmless observation.",
            "result": "COUNTERMODEL_ACTIVE",
            "blocking_gap": "EFT/readout/source-worldtube no-reentry theorem and fitted-GM guard are unsigned",
            "effect": "calibration and effective-map pieces must be bounded or forbidden explicitly",
        },
        {
            "audit_id": "JRZ2523_5_worldtube_boundary",
            "claim_piece": "Pi_M/worldtube/boundary selector",
            "formal_statement": "Pi_M, W_source, boundary flux, and annulus commutator terms must be fixed before variation or proven exact-zero in the scored source class.",
            "result": "BLOCKED_BY_2503_SELECTOR_DEBT",
            "blocking_gap": "Hamiltonian Pi_M identity, same Hilbert source object, source worldtube, and zero boundary flux remain unsigned",
            "effect": "Pi_M is the highest-leverage subgate to attack next",
        },
        {
            "audit_id": "JRZ2523_6_observed_coframe",
            "claim_piece": "observed coframe/readout leak",
            "formal_statement": "If e_obs=E(q_parent(Phi)) is q-basic and DObs_e[v_m]=0, readout cannot reintroduce memory through the public carrier.",
            "result": "BLOCKED_BY_DOBS_KERNEL",
            "blocking_gap": "DObs_e kernel zero, common-frame ownership and boundary endpoint clauses are not signed",
            "effect": "clock/orbit/PPN readout channels remain nonclaim residual routes",
        },
        {
            "audit_id": "JRZ2523_7_verdict",
            "claim_piece": "J_readout=0 theorem",
            "formal_statement": "J_readout=0 requires pure-postprocessing status plus fixed projector/worldtube/coframe/calibration/boundary maps or theorem-zero commutators for each local arena.",
            "result": "JREADOUT_ZERO_THEOREM_NOT_DERIVED_STAGE_COMMUTATOR_ROWS",
            "blocking_gap": "projector/worldtube/material/coframe/calibration commutator clauses are not parent-signed",
            "effect": "retain finite nonclaim J_readout rows and move to Pi_M projector commutator",
        },
    ]
    return [base_row(**entry) for entry in entries]


def commutator_gate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "gate_id": "JRG2523_0_parent_absence",
            "required_clause": "readout absent from parent action",
            "formal_condition": "R_A not in S_parent and no readout weight appears before Hilbert/Noether variation",
            "current_status": "CONDITIONAL_ONLY_NOT_PARENT_SIGNED_FOR_LOCAL_READOUTS",
            "if_fail": "readout coefficient is an ordinary source coefficient",
        },
        {
            "gate_id": "JRG2523_1_effective_absence",
            "required_clause": "readout absent from effective pre-variation action",
            "formal_condition": "S_eff contains no R_A, calibrated source map, material readout, or source-worldtube branch before delta_m",
            "current_status": "FAIL_EFFECTIVE_REENTRY_UNSIGNED",
            "if_fail": "integrated-out sectors generate J_effective/J_readout",
        },
        {
            "gate_id": "JRG2523_2_codomain_separation",
            "required_clause": "data codomain separate from active source coefficients",
            "formal_condition": "Codomain(R_post) cap Coeff_active_source is empty after quotient/readout",
            "current_status": "FAIL_NO_SHADOW_CODOMAIN_UNSIGNED",
            "if_fail": "data map can be repackaged as source-normalization coefficient",
        },
        {
            "gate_id": "JRG2523_3_fixed_PiM",
            "required_clause": "Hamiltonian Pi_M fixed under memory variation",
            "formal_condition": "delta_m Pi_M=0 or ||(delta_m Pi_M)J_H|| has a sourced bound",
            "current_status": "FAIL_PIM_HAMILTONIAN_IDENTITY_AND_COMMUTATOR_UNSIGNED",
            "if_fail": "Newton/source mass normalization and R10/PPN channels remain live",
        },
        {
            "gate_id": "JRG2523_4_fixed_Ploc",
            "required_clause": "local projector P_loc fixed under memory variation",
            "formal_condition": "delta_m P_loc=0 or ||(delta_m P_loc)source|| has a sourced bound",
            "current_status": "FAIL_LOCAL_DOMAIN_PROJECTOR_UNSIGNED",
            "if_fail": "local residual vector can re-enter through domain/support choice",
        },
        {
            "gate_id": "JRG2523_5_fixed_worldtube",
            "required_clause": "source worldtube/support fixed under memory variation",
            "formal_condition": "delta_m W_source=0, no jump/support drift, and zero boundary flux in the scored source class",
            "current_status": "FAIL_WORLDTUBE_AND_BOUNDARY_FLUX_UNSIGNED",
            "if_fail": "side flux and annulus commutator become finite source residuals",
        },
        {
            "gate_id": "JRG2523_6_qbasic_coframe",
            "required_clause": "observed coframe and material readout q-basic",
            "formal_condition": "DObs_e[v_m]=0 and material/clock/orbit kernels are functions of public q-data only",
            "current_status": "FAIL_DOBS_AND_MATERIAL_KERNEL_UNSIGNED",
            "if_fail": "clock/WEP/orbit readouts retain common-frame and material leak rows",
        },
        {
            "gate_id": "JRG2523_7_no_calibration_feedback",
            "required_clause": "no fitted-source feedback",
            "formal_condition": "GM, eta, clock, BAO/SN nuisance, and orbit readout parameters are not fed back into the parent source coefficient",
            "current_status": "FAIL_CALIBRATION_FEEDBACK_GUARD_UNSIGNED",
            "if_fail": "fitted GM/readout can hide the residual rather than derive Newton",
        },
        {
            "gate_id": "JRG2523_8_theorem",
            "required_clause": "general J_readout zero theorem",
            "formal_condition": "JRG2523_0 through JRG2523_7 all pass with source paths",
            "current_status": "CLAIM_BLOCKED_STAGE_JREADOUT_ROWS",
            "if_fail": "retain nonclaim finite commutator rows",
        },
    ]
    return [base_row(**entry, gate_pass=False) for entry in entries]


def jreadout_bound_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "row_id": "JRO2523_0_total",
            "quantity": "J_readout",
            "row_role": "total post-variation readout/projector memory-source re-entry",
            "formula_or_bound": "J_readout <= J_PiM_comm + J_Ploc_comm + J_worldtube_comm + J_material_comm + J_coframe_DObs + J_EFT_pre + J_calibration + J_boundary_endpoint",
            "units": "memory_source_units",
            "required_inputs": "component zero certificates or finite values; units; source paths; no-cancellation allocation; arena projection maps",
            "current_status": "MISSING_GENERAL_READOUT_ZERO_OR_COMPONENT_VALUES",
            "observable_links": "J_mem;Q_mem;Newton;PPN;WEP;clock;orbit;R10",
        },
        {
            "row_id": "JRO2523_1_PiM_comm",
            "quantity": "J_PiM_comm",
            "row_role": "Hamiltonian mass projector commutator",
            "formula_or_bound": "J_PiM_comm := ||(delta_m Pi_M) J_H|| or ||[delta_m,Pi_M]J_H||",
            "units": "memory_source_units_or_GM_flux_after_normalization",
            "required_inputs": "Pi_M definition; Hamiltonian identity; J_H source path; memory variation; local/source normalization",
            "current_status": "MISSING_PIM_COMMUTATOR_ZERO_OR_BOUND",
            "observable_links": "Newton;PPN;R10;source_normalization",
        },
        {
            "row_id": "JRO2523_2_Ploc_comm",
            "quantity": "J_Ploc_comm",
            "row_role": "local projector/domain commutator",
            "formula_or_bound": "J_Ploc_comm := ||(delta_m P_loc) Source|| on the local domain",
            "units": "memory_source_units",
            "required_inputs": "P_loc parent definition; local domain; variation support; norm convention",
            "current_status": "MISSING_PLOC_FIXEDNESS_OR_BOUND",
            "observable_links": "local_GR;PPN;clock;orbit",
        },
        {
            "row_id": "JRO2523_3_worldtube_comm",
            "quantity": "J_worldtube_comm",
            "row_role": "source-worldtube/support drift",
            "formula_or_bound": "J_worldtube_comm <= ||delta_m W_source|| ||J_H|| + jump/support side-flux terms",
            "units": "memory_source_units",
            "required_inputs": "source worldtube; support/jump condition; side-flux bound; boundary surface",
            "current_status": "MISSING_WORLDTUBE_FIXEDNESS_AND_SIDE_FLUX_BOUND",
            "observable_links": "Newton;orbit;WEP;R10",
        },
        {
            "row_id": "JRO2523_4_material_comm",
            "quantity": "J_material_comm",
            "row_role": "material/WEP/source composition readout",
            "formula_or_bound": "J_material_comm <= ||delta_m Pi_material|| ||J_source|| + material-sensitivity kernels",
            "units": "memory_source_units",
            "required_inputs": "Ti/Pt or material tensor; source composition map; readout kernel; units",
            "current_status": "MISSING_MATERIAL_READOUT_KERNELS",
            "observable_links": "WEP;clock;R10",
        },
        {
            "row_id": "JRO2523_5_coframe_DObs",
            "quantity": "J_coframe_DObs",
            "row_role": "observed coframe/common-frame readout leak",
            "formula_or_bound": "J_coframe_DObs <= K_DObs ||DObs_e[v_m]|| plus endpoint/common-frame rows",
            "units": "memory_source_units_after_frame_kernel",
            "required_inputs": "DObs_e kernel theorem or finite DObs row; common-frame kernel; endpoint/boundary owner",
            "current_status": "MISSING_DOBS_KERNEL_ZERO_OR_FRAME_BOUND",
            "observable_links": "PPN;clock;orbit;local_GR",
        },
        {
            "row_id": "JRO2523_6_EFT_pre",
            "quantity": "J_EFT_pre",
            "row_role": "effective pre-variation readout/source reduction",
            "formula_or_bound": "J_EFT_pre := ||partial_m S_eff[R_A,W_source,hidden]|| before local scoring",
            "units": "memory_source_units",
            "required_inputs": "effective action construction; hidden/domain integration rule; no-reentry theorem or finite coefficient",
            "current_status": "MISSING_EFFECTIVE_READOUT_REENTRY_ZERO_OR_BOUND",
            "observable_links": "J_mem;Q_mem;clock;orbit",
        },
        {
            "row_id": "JRO2523_7_calibration",
            "quantity": "J_calibration",
            "row_role": "fitted-source/readout feedback",
            "formula_or_bound": "J_calibration <= ||partial_m C_fit|| ||partial Source/partial C_fit|| for fitted GM/eta/clock/orbit nuisance maps",
            "units": "memory_source_units",
            "required_inputs": "calibration protocol; fixed-prior/fitted-parameter split; no-feedback theorem or finite sensitivity",
            "current_status": "MISSING_CALIBRATION_FEEDBACK_GUARD",
            "observable_links": "Newton;orbit;cosmology;clock",
        },
        {
            "row_id": "JRO2523_8_boundary_endpoint",
            "quantity": "J_boundary_endpoint",
            "row_role": "boundary/reference endpoint readout leak",
            "formula_or_bound": "J_boundary_endpoint <= ||delta_m B_ref|| + ||delta_m endpoint|| contributions in source-current norm",
            "units": "boundary_flux_or_memory_source_units",
            "required_inputs": "boundary primitive; endpoint owner; zero-flux theorem or finite surface integral",
            "current_status": "MISSING_BOUNDARY_ENDPOINT_ZERO_OR_BOUND",
            "observable_links": "PPN;R10;clock;orbit",
        },
        {
            "row_id": "JRO2523_9_Jmem_insertion",
            "quantity": "J_readout contribution to J_mem",
            "row_role": "readout component in total memory drive",
            "formula_or_bound": "|J_mem| <= J_direct_matter + J_Hilbert_exchange + J_bath + J_readout + J_history + J_domain + J_worldtube + J_shadow",
            "units": "memory_source_units",
            "required_inputs": "J_readout value/theorem-zero plus remaining J_mem components and no double counting",
            "current_status": "FILL_CONTRACT_READY_VALUES_MISSING",
            "observable_links": "J_mem;Q_mem;local_GR",
        },
        {
            "row_id": "JRO2523_10_Qmem_insertion",
            "quantity": "N_src J_readout",
            "row_role": "readout source-drive insertion into Q_mem",
            "formula_or_bound": "Q_mem_readout <= A_ref^-1 N_src J_readout",
            "units": "dimensionless_after_Aref",
            "required_inputs": "A_ref;N_src;J_readout value/theorem-zero; source path",
            "current_status": "FILL_CONTRACT_READY_VALUES_MISSING",
            "observable_links": "Q_norm;PPN_gamma;local_GR",
        },
    ]
    return [
        base_row(
            **entry,
            score_ready=False,
            valid_prediction_row=False,
            accepted_for_scoring=False,
            claim_pass=False,
        )
        for entry in entries
    ]


def observable_gate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "gate_id": "JOG2523_0_Jmem",
            "arena": "J_mem total drive",
            "map_formula": "J_mem contains J_readout as the post-variation readout/projector component",
            "required_bundle": "J_readout zero certificate or finite component bounds plus J_direct/J_bath/J_worldtube allocation",
            "status": "BLOCKED_MISSING_JREADOUT_VALUE_OR_THEOREM",
        },
        {
            "gate_id": "JOG2523_1_Qmem",
            "arena": "Q_mem residual",
            "map_formula": "Q_mem_readout <= A_ref^-1 N_src J_readout",
            "required_bundle": "A_ref;N_src;J_readout units/value/source path",
            "status": "BLOCKED_MISSING_QMEM_READOUT_INSERTION_VALUES",
        },
        {
            "gate_id": "JOG2523_2_Newton_local_GR",
            "arena": "Newton/local GR source normalization",
            "map_formula": "Pi_M and W_source must be the same fixed Hilbert source object before local scoring",
            "required_bundle": "Pi_M Hamiltonian identity; worldtube selector; zero boundary flux; no fitted GM feedback",
            "status": "BLOCKED_MISSING_PIM_WORLDTUBE_ZERO",
        },
        {
            "gate_id": "JOG2523_3_PPN",
            "arena": "PPN/local residual vector",
            "map_formula": "J_Ploc_comm,J_coframe_DObs,J_boundary_endpoint -> gamma/beta/preferred-frame residuals",
            "required_bundle": "P_loc kernel; DObs kernel; boundary endpoint bound; PPN projection matrix",
            "status": "BLOCKED_MISSING_PPN_READOUT_KERNELS",
        },
        {
            "gate_id": "JOG2523_4_WEP_R10",
            "arena": "WEP/R10 source and composition tests",
            "map_formula": "J_material_comm,J_PiM_comm,J_worldtube_comm -> eta or alpha(lambda) projection",
            "required_bundle": "material tensor; source/test charge map; bound curve; range/source normalization",
            "status": "BLOCKED_MISSING_WEP_R10_PROJECTION_INPUTS",
        },
        {
            "gate_id": "JOG2523_5_clock_orbit",
            "arena": "clock/orbital readout",
            "map_formula": "J_coframe_DObs,J_calibration,J_boundary_endpoint -> clock/orbit residuals",
            "required_bundle": "clock kernels; orbit/attitude arrays; fixed calibration protocol; no hidden fitted GM",
            "status": "BLOCKED_MISSING_CLOCK_ORBIT_READOUT_BUNDLE",
        },
    ]
    return [base_row(**entry, claim_pass=False) for entry in entries]


def dryrun_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "case_id": "DRY2523_0_pure_postprocessing_for_projector",
            "case_description": "claim J_readout=0 by calling every local projector pure postprocessing",
            "missing_requirements": "fixed Pi_M/P_loc/worldtube/material/coframe; no prevariation map; no boundary leak",
            "result_status": "REJECT",
            "blocking_markers": "PROJECTOR_COMMUTATOR_SURVIVES",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2523_1_drop_delta_projector_term",
            "case_description": "use delta(Pi J)=Pi delta J without the (delta Pi)J term",
            "missing_requirements": "delta_m Pi=0 theorem or finite commutator row",
            "result_status": "REJECT",
            "blocking_markers": "COMMUTATOR_TERM_DROPPED",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2523_2_Hilbert_source_as_readout_silence",
            "case_description": "treat measured Hilbert source mass as proof that readout/projector has no memory dependence",
            "missing_requirements": "Pi_M same-object proof; fixed worldtube; zero boundary flux; no source feedback",
            "result_status": "REJECT",
            "blocking_markers": "SOURCE_MASS_NOT_READOUT_COMMUTATOR_ZERO",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2523_3_fitted_GM_absorption",
            "case_description": "absorb readout/source residual into fitted GM or calibration nuisance",
            "missing_requirements": "fixed calibration protocol; no-feedback theorem; external source normalization",
            "result_status": "REJECT",
            "blocking_markers": "FITTED_SOURCE_FEEDBACK",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2523_4_WEP_arrays_without_sources",
            "case_description": "score WEP/material readout without source worldtube, Ti/Pt tensor, orbit/readout arrays and eta convention",
            "missing_requirements": "material tensor; source path; orbit kernel; units; tau_WEP",
            "result_status": "REJECT",
            "blocking_markers": "MISSING_WEP_READOUT_BUNDLE",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2523_5_numeric_Jreadout_without_units",
            "case_description": "provide a numeric J_readout without component allocation, units, A_ref/N_src and source paths",
            "missing_requirements": "units;component rows;source paths;A_ref;N_src;no-cancellation ledger",
            "result_status": "REJECT",
            "blocking_markers": "MISSING_JREADOUT_RUNNER_BUNDLE",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2523_6_future_complete_Jreadout",
            "case_description": "future J_readout row with source-backed fixed-map theorem or finite commutator values",
            "missing_requirements": "none in schema; evidence remains future",
            "result_status": "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST",
            "blocking_markers": "FUTURE_EVIDENCE_ONLY",
            "pass_fail": "TEMPLATE_NONCLAIM",
        },
    ]
    return [base_row(**entry, claim_pass=False) for entry in entries]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "decision_id": "DEC2523_0_status",
            "decision": "do not claim J_readout=0",
            "rationale": "pure postprocessing is safe, but local projectors/worldtubes/material/coframe/calibration maps are not signed as pure data-only",
            "next_action": "retain nonclaim J_readout commutator rows",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2523_1_main_gain",
            "decision": "split readout debt into named subcomponents",
            "rationale": "this prevents the theory from hiding a source residual inside fitted readout or calling every local map an observation",
            "next_action": "attack the largest shared component first: Pi_M projector commutator",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2523_2_next_route",
            "decision": "select Pi_M projector commutator before fibre B_h",
            "rationale": "Pi_M/worldtube controls Newton source normalization and feeds PPN/R10/WEP more directly than the fibre queue",
            "next_action": "construct 2524 Pi_M zero proof or JPiM bound rows",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2523_3_claim_guard",
            "decision": "keep all local-GR/Newton/WEP/R10/PPN claims blocked",
            "rationale": "J_readout remains finite/unsigned and must pass through J_mem/Q_mem before local claims",
            "next_action": "only promote after theorem-zero or source-backed finite rows with arena kernels",
            "status": "ACTIVE",
        },
    ]
    return [base_row(**entry) for entry in entries]


def next_target_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "route_id": "NEXT2523_0_selected",
            "selection_status": "selected",
            "target_file": "2524-Y5-R2FR-PiM-projector-commutator-zero-or-JPiM-bound.md",
            "target_script": "scripts/Y5_R2FR_PiM_projector_commutator_zero_or_JPiM_bound_2524.py",
            "objective": "prove delta_m Pi_M=0 as a parent-owned Hamiltonian mass projector fixed before readout, or stage finite J_PiM_comm rows with units and source paths",
            "success_condition": "J_PiM_comm is theorem-zero from parent Pi_M/Hilbert source same-object fixedness or retained as a finite nonclaim component of J_readout",
            "do_not_do": "do not absorb into fitted GM; do not treat conserved Hilbert mass as projector commutator silence; do not claim Newton/local GR",
        },
        {
            "route_id": "NEXT2523_1_fibre_queue",
            "selection_status": "queued_after_PiM",
            "target_file": "2525-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md",
            "target_script": "scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2525.py",
            "objective": "classify fibre B_h with hidden-visible grammar reentry or finite fibre coefficient rows after the readout/source projector lane is narrowed",
            "success_condition": "B_h has theorem-zero evidence or finite nonclaim Z_h/M2_h/B_h/C_h/source-charge rows",
            "do_not_do": "do not let memory/readout closure erase independent fibre residuals",
        },
    ]
    return [base_row(**entry) for entry in entries]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_map = {
        "readout_reentry_audit": OUTPUTS["readout_reentry_audit"],
        "jreadout_bound_rows": OUTPUTS["jreadout_bound_rows"],
        "commutator_gate": OUTPUTS["commutator_gate"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, destination in BRANCH_COPIES.items():
        source = source_map[key]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        parse_ok, row_count, parse_message = csv_rows_parse(destination)
        rows.append(
            base_row(
                copy_id=f"COPY2523_{key}",
                source_path=str(source.relative_to(ROOT)),
                destination_path=str(destination.relative_to(ROOT)),
                copied=destination.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_message=parse_message,
                status="NONCLAIM_BRANCH_COPY",
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for key in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "valid_prediction_row",
                "accepted_for_scoring",
                "claim_pass",
                "gate_pass",
            ):
                if key in row and not falsey(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    audit_rows = rows_by_name["readout_reentry_audit"]
    commutator_rows = rows_by_name["commutator_gate"]
    bound_rows = rows_by_name["jreadout_bound_rows"]

    add("VAL2523_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2523_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2523_02_pure_postprocessing_theorem_written",
        any(
            row["audit_id"] == "JRZ2523_1_pure_postprocessing_zero"
            and row["result"] == "EXACT_CONDITIONAL_THEOREM"
            for row in audit_rows
        ),
        "data-only postprocessing zero is preserved as a real theorem",
    )
    add(
        "VAL2523_03_general_zero_not_promoted",
        any(
            row["audit_id"] == "JRZ2523_7_verdict"
            and row["result"] == "JREADOUT_ZERO_THEOREM_NOT_DERIVED_STAGE_COMMUTATOR_ROWS"
            for row in audit_rows
        ),
        "general J_readout zero remains unclaimed",
    )
    add(
        "VAL2523_04_commutator_gates_blocked",
        len(commutator_rows) == 9 and all(str(row["gate_pass"]) == "False" for row in commutator_rows),
        "projector/worldtube/coframe/calibration gates all block promotion",
    )
    add(
        "VAL2523_05_bound_rows_complete",
        all(
            any(row["row_id"] == required for row in bound_rows)
            for required in [
                "JRO2523_0_total",
                "JRO2523_1_PiM_comm",
                "JRO2523_2_Ploc_comm",
                "JRO2523_3_worldtube_comm",
                "JRO2523_5_coframe_DObs",
                "JRO2523_9_Jmem_insertion",
                "JRO2523_10_Qmem_insertion",
            ]
        ),
        "J_readout rows include total, Pi_M, P_loc, worldtube, coframe, Jmem and Qmem insertion",
    )
    add(
        "VAL2523_06_bound_rows_nonclaim",
        all(
            str(row["accepted_for_scoring"]) == "False"
            and str(row["claim_pass"]) == "False"
            and str(row["score_ready"]) == "False"
            for row in bound_rows
        ),
        "all J_readout bound rows are blocked for scoring",
    )
    add(
        "VAL2523_07_observable_gates_blocked",
        all(
            str(row["claim_pass"]) == "False" and str(row["status"]).startswith("BLOCKED")
            for row in rows_by_name["observable_gate"]
        ),
        "Jmem/Qmem/Newton/PPN/WEP/R10/clock/orbit gates remain blocked",
    )
    add(
        "VAL2523_08_dryruns_block_bad_rows",
        all(str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"])
        and all(
            str(row["result_status"]) in {"REJECT", "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST"}
            for row in rows_by_name["dryrun_results"]
        ),
        "pure-postprocessing shortcut, dropped commutator, Hilbert-as-silence, fitted GM and incomplete numeric rows do not score",
    )
    add(
        "VAL2523_09_next_target_PiM",
        any(
            row["route_id"] == "NEXT2523_0_selected"
            and "PiM-projector-commutator" in row["target_file"]
            for row in rows_by_name["next_target"]
        ),
        "Pi_M projector commutator selected next",
    )
    add("VAL2523_10_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2523_11_branch_copies",
        all(
            str(row["copied"]) == "True" and str(row["parse_ok"]) == "True"
            for row in rows_by_name["branch_copies"]
        ),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = [
        path
        for path in formalization.rglob("*2523*")
        if ".venv" not in path.parts and "site-packages" not in path.parts
    ] if formalization.exists() else []
    add(
        "VAL2523_12_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2523_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        parse_ok, row_count, parse_message = csv_rows_parse(path)
        add(f"VAL2523_CSV_{path.stem}", parse_ok, f"{parse_message}; rows={row_count}")
    for key, path in BRANCH_COPIES.items():
        parse_ok, row_count, parse_message = csv_rows_parse(path)
        add(f"VAL2523_COPY_CSV_{key}", parse_ok, f"{parse_message}; rows={row_count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2523_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2523 preserves the pure postprocessing zero theorem, refuses to promote general readout/projector silence, stages J_readout commutator rows, and selects Pi_M projector commutator next.",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2523 - Readout/Projector Memory Re-entry Zero or Jreadout Bound",
                "",
                "**Current verdict:** pure data-only postprocessing is theorem-silent, but the general local readout/projector route is not. `J_readout=0` requires fixed/projector-worldtube-coframe-calibration clauses that the current corpus has not parent-signed.",
                "",
                "**Main gain:** the readout debt is now split into named commutator rows: `Pi_M`, `P_loc`, source worldtube, material readout, observed coframe, effective pre-variation maps, calibration feedback, and boundary/endpoint leakage.",
                "",
                "**Claim discipline:** no Newton, local-GR, PPN, WEP, R10, clock, orbit, `J_mem`, `Q_mem`, or GitHub/public claim is made. The clean theorem is retained only for genuine post-solution reporting maps.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Readout Re-entry Audit",
                md_table(rows_by_name["readout_reentry_audit"], ["audit_id", "claim_piece", "formal_statement", "result", "blocking_gap", "effect"]),
                "",
                "## Commutator Gate",
                md_table(rows_by_name["commutator_gate"], ["gate_id", "required_clause", "formal_condition", "current_status", "if_fail", "gate_pass"]),
                "",
                "## Jreadout Bound Rows",
                md_table(rows_by_name["jreadout_bound_rows"], ["row_id", "quantity", "row_role", "formula_or_bound", "required_inputs", "current_status", "observable_links"]),
                "",
                "## Observable Gate",
                md_table(rows_by_name["observable_gate"], ["gate_id", "arena", "map_formula", "required_bundle", "status", "claim_pass"]),
                "",
                "## Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "missing_requirements", "result_status", "blocking_markers", "pass_fail"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "next_action", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "readout_reentry_audit": readout_reentry_audit_rows(),
        "commutator_gate": commutator_gate_rows(),
        "jreadout_bound_rows": jreadout_bound_rows(),
        "observable_gate": observable_gate_rows(),
        "dryrun_results": dryrun_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
