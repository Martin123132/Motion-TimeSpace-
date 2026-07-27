from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
SOURCE_WEIGHT_DOCS = SOURCE_WEIGHT / "docs"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
HAMILTONIAN_SOURCE = ROOT / "source-intake" / "hamiltonian-source"
WEP_SOURCES = ROOT / "source-intake" / "wep-sources"
MICRO_QUAR = ROOT / "source-intake" / "microscope" / "quarantine"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2979"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2979-Y5-R2FR-no-marker-source-covector-theorem-or-JZ-component-coefficient-acquisition-under-AX1090.md"

SRC_2978_DOC = ROOT / "2978-Y5-R2FR-no-linear-source-JZ-BZ-theorem-or-source-bound-rows-under-AX1090.md"
SRC_2978_NEXT = RESIDUALS / "P8_Y5_R2FR_2978_NEXT_TARGET.csv"
SRC_2978_THEOREM = RESIDUALS / "P8_Y5_R2FR_2978_NO_LINEAR_SOURCE_THEOREM_ATTEMPT.csv"
SRC_2978_CLAUSES = RESIDUALS / "P8_Y5_R2FR_2978_JZ_BZ_CLAUSE_AUDIT.csv"
SRC_2978_BOUNDS = RESIDUALS / "P8_Y5_R2FR_2978_JZ_BZ_SOURCE_BOUND_ROWS_NONCLAIM.csv"
SRC_2978_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2978_VALIDATION.csv"

SRC_2852_SYM = LOCAL_BOUNDS / "RAB_SOURCE_DOUBLET_SYMMETRY_CANDIDATES_2852_NONCLAIM.csv"
SRC_2835_NORMAL = SOURCE_WEIGHT / "RAB_source_slot_normal_form_attempt_2835_NONCLAIM.csv"
SRC_2328_NOSOURCE = BETA_DOCS / "NO_SOURCE_ONLY_SPECIES_SLOT_DERIVATION_ATTEMPT_2328_NONCLAIM.csv"
SRC_2508_DECISION = BETA_DOCS / "No_source_only_slot_decision_2508_NONCLAIM.csv"
SRC_2343_AUDIT = BETA_DOCS / "NOSOURCEONLYSPECIES_AUDIT_2343_NONCLAIM.csv"
SRC_2329_SIGNATURE = BETA_DOCS / "SOURCE_BLIND_FUNCTOR_SIGNATURE_2329_NONCLAIM.csv"
SRC_2344_OBLIGATION = BETA_DOCS / "PARENT_SOURCE_BLIND_FUNCTOR_PROOF_OBLIGATION_2344_NONCLAIM.csv"
SRC_2677_GRAMMAR = WEP_SOURCES / "no_species_action_weight_object_language_wip_2677.csv"
SRC_1479_TYPING = MICRO_QUAR / "1479" / "NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT_NONCLAIM.csv"
SRC_1479_BOUNDS = MICRO_QUAR / "1479" / "COMPONENT_DELTA_W_BOUND_PACK_NONCLAIM.csv"
SRC_1478_ACTIONLINE = MICRO_QUAR / "1478" / "SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT_NONCLAIM.csv"
SRC_1476_FORGETTING = MICRO_QUAR / "1476" / "SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv"
SRC_2345_CURRENT = BETA_DOCS / "CURRENT_OWNER_NORMAL_FORM_AUDIT_2345_NONCLAIM.csv"
SRC_2330_DEEPER = BETA_DOCS / "DEEPER_QUOTIENT_DERIVATION_AUDIT_2330_NONCLAIM.csv"
SRC_2774_ACTION_SCALE = BETA_DOCS / "ACTION_SCALE_OWNER_2774_NONCLAIM.csv"
SRC_2437_SHADOW = BETA_DOCS / "COUPLING_SHADOW_BOUND_PACK_2437_NONCLAIM.csv"
SRC_2828_VMQ = SOURCE_WEIGHT / "vmq_zero_proof_audit_2828_NONCLAIM.csv"
SRC_2956_DESCENT = PARENT_ACTION / "matter_pullback_descent_audit_2956_NOT_DERIVED.csv"
SRC_2164_LOCK = SOURCE_WEIGHT_DOCS / "AFRAME_JZ_BZ_COUPLING_LOCK_2164_NONCLAIM.csv"
SRC_2521_JMEM = BETA_DOCS / "Jmem_drive_bound_rows_2521_NONCLAIM.csv"
SRC_2522_JDIRECT = BETA_DOCS / "Jdirect_matter_bound_rows_2522_NONCLAIM.csv"
SRC_2523_JREADOUT = BETA_DOCS / "Jreadout_bound_rows_2523_NONCLAIM.csv"
SRC_2524_JPIM = BETA_DOCS / "JPiM_bound_rows_2524_NONCLAIM.csv"
SRC_2446_CURRENT_PACK = HAMILTONIAN_SOURCE / "MTS_residual_current_pack_for_S_Eq_2446_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2979_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2979_NO_MARKER_SOURCE_COVECTOR_THEOREM_ATTEMPT.csv",
    "constructor": RESIDUALS / "P8_Y5_R2FR_2979_PARENT_CONSTRUCTOR_EXHAUSTION_GATE.csv",
    "coefficients": RESIDUALS / "P8_Y5_R2FR_2979_JZ_COMPONENT_COEFFICIENT_LEDGER_NONCLAIM.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2979_JZ_COEFFICIENT_PROMOTION_RULES.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2979_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2979_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2979_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2979_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2979_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "no_marker_source_covector_theorem_attempt_2979_NOT_DERIVED.csv",
    "coefficient_copy": LOCAL_BOUNDS / "JZ_component_coefficient_ledger_2979_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2979_parent_constructor_exhaustion_or_first_JZ_coefficient_next_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except Exception:
        return False
    return True


def anchors_present(path: Path, anchors: list[str]) -> bool:
    text = read_text(path)
    return path.exists() and all(anchor in text for anchor in anchors)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2979_0_2978_doc", SRC_2978_DOC, ["Status:", "Best next attack"], "2978 markdown handoff"),
        ("SRC2979_1_2978_next", SRC_2978_NEXT, ["NEXT2978_0_2979", "source-doublet covector"], "selected 2979 target"),
        ("SRC2979_2_2978_theorem", SRC_2978_THEOREM, ["THM2978_4_no_source_covector", "THM2978_7_verdict"], "source-covector blocker"),
        ("SRC2979_3_2978_clauses", SRC_2978_CLAUSES, ["CL2978_3_constants_markers", "CL2978_4_no_shadow_frame", "CL2978_8_Y5"], "open no-marker/Y5 clauses"),
        ("SRC2979_4_2978_bounds", SRC_2978_BOUNDS, ["JZ2978_0_total", "JZ2978_5_shadow_marker", "JZ2978_6_Y5", "JZ2978_7_Y6"], "J_Z bound rows"),
        ("SRC2979_5_2978_validation", SRC_2978_VALIDATION, ["VAL2978_OVERALL"], "2978 validation"),
        ("SRC2979_6_2852_symmetry", SRC_2852_SYM, ["SYM2852_3_no_marker_object_language", "OBSTRUCTED_BY_980_AND_1078"], "source-doublet symmetry candidates"),
        ("SRC2979_7_2835_normal_form", SRC_2835_NORMAL, ["NF2835_0_target", "NF2835_3_object_language", "NF2835_5_verdict"], "source-slot normal form"),
        ("SRC2979_8_2328_no_source", SRC_2328_NOSOURCE, ["NSOS2328_0_target", "NSOS2328_4_source_blind_functor", "NSOS2328_6_verdict"], "no source-only species derivation attempt"),
        ("SRC2979_9_2508_decision", SRC_2508_DECISION, ["DEC2508_0_exact_theorem", "DEC2508_2_loop_guard", "DEC2508_3_next"], "loop guard and pivot decision"),
        ("SRC2979_10_2343_audit", SRC_2343_AUDIT, ["NSS2343_0_target", "NSS2343_3_source_blind_functor", "NSS2343_5_verdict"], "NoSourceOnlySpecies audit"),
        ("SRC2979_11_2329_signature", SRC_2329_SIGNATURE, ["SBF2329_1_source_blind_functor", "SBF2329_5_nonhilbert_residual_policy", "SBF2329_6_verdict"], "source-blind signature"),
        ("SRC2979_12_2344_obligation", SRC_2344_OBLIGATION, ["PSBF2344_1_absent_target", "PSBF2344_5_relative_counterexample", "PSBF2344_6_verdict"], "source-blind proof obligation"),
        ("SRC2979_13_2677_grammar", SRC_2677_GRAMMAR, ["GRM2677_0_single_action_density_line", "GRM2677_6_verdict"], "no species action-weight grammar"),
        ("SRC2979_14_1479_typing", SRC_1479_TYPING, ["NST1479_0_target", "NST1479_3_same_action_limit", "NST1479_4_verdict"], "no source-only prefactor typing theorem"),
        ("SRC2979_15_1479_bounds", SRC_1479_BOUNDS, ["CBP1479_1_delta_w_e", "CBP1479_7_delta_c_A", "CBP1479_8_zeta_A"], "component delta-w proxy pack"),
        ("SRC2979_16_1478_actionline", SRC_1478_ACTIONLINE, ["SAL1478_0_target", "SAL1478_3_direct_sum_countermodel", "SAL1478_4_verdict"], "single action-density line attempt"),
        ("SRC2979_17_1476_forgetting", SRC_1476_FORGETTING, ["SLF1476_0_target", "SLF1476_3_countermodel", "SLF1476_4_verdict"], "source-label forgetting attempt"),
        ("SRC2979_18_2345_current", SRC_2345_CURRENT, ["CNF2345_1_hilbert_owner", "CNF2345_3_pre_action_wall", "CNF2345_6_verdict"], "current owner normal form"),
        ("SRC2979_19_2330_deeper", SRC_2330_DEEPER, ["DQD2330_0_target", "DQD2330_3_double_accounting", "DQD2330_5_verdict"], "deeper quotient derivation"),
        ("SRC2979_20_2774_action_scale", SRC_2774_ACTION_SCALE, ["ASO2774_1_classical_EOM_vs_source", "ASO2774_5_verdict"], "action scale owner"),
        ("SRC2979_21_2437_shadow", SRC_2437_SHADOW, ["SCB2437_0_delta_w_block", "SCB2437_7_total_abs"], "coupling shadow bound pack"),
        ("SRC2979_22_2828_vmq", SRC_2828_VMQ, ["ZPA2828_2_no_source_prefactor", "ZPA2828_6_verdict"], "vmq no-prefactor proof audit"),
        ("SRC2979_23_2956_descent", SRC_2956_DESCENT, ["DESC2956_4_constants", "DESC2956_5_hidden_frame", "DESC2956_7_verdict"], "matter pullback descent audit"),
        ("SRC2979_24_2164_lock", SRC_2164_LOCK, ["SFE2164_4_readout_species", "SFE2164_5_Y5_Y6", "SFE2164_6_verdict"], "coupling lock"),
        ("SRC2979_25_2521_jmem", SRC_2521_JMEM, ["JDRV2521_7_shadow_weight", "JDRV2521_9_Qmem_insertion"], "Jmem component rows"),
        ("SRC2979_26_2522_jdirect", SRC_2522_JDIRECT, ["JDIR2522_5_marker_m", "JDIR2522_7_Qmem_insertion"], "direct matter component rows"),
        ("SRC2979_27_2523_jreadout", SRC_2523_JREADOUT, ["JRO2523_4_material_comm", "JRO2523_10_Qmem_insertion"], "readout component rows"),
        ("SRC2979_28_2524_jpim", SRC_2524_JPIM, ["JPIM2524_8_extra_current", "JPIM2524_12_Qmem_insertion"], "Pi_M component rows"),
        ("SRC2979_29_2446_current_pack", SRC_2446_CURRENT_PACK, ["RCS2446_3_matter_source_glue", "RCS2446_6_EM_clock_mass_coupling_guard", "RCS2446_7_verdict"], "residual current pack"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "role": role,
                    "required_anchors": ";".join(anchors),
                    "exists": path.exists(),
                    "anchors_found": anchors_present(path, anchors),
                }
            )
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "NMC2979_0_target",
            "object": "independent source-doublet covector",
            "statement": "A linear source term a_A Z^A is absent if Coeff_source-only is not an object/target in the parent constructor image.",
            "status": "TARGET_SHARP",
            "proof_or_blocker": "the desired theorem is now exactly a parent-constructor exhaustion/no-Hom theorem, not a covariance slogan",
            "theorem_zero": False,
        },
        {
            "theorem_id": "NMC2979_1_conditional_typing",
            "object": "typed object-language theorem",
            "statement": "If S_parent arguments are only Q_obs, Psi, gauge/current data, theta_rep and universal constants, inert source-only a_A is ill-typed.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_blocker": "NST1479 and SBF2329 give this theorem shape, but the parent constructor has not been exhausted from MTS primitives",
            "theorem_zero": False,
        },
        {
            "theorem_id": "NMC2979_2_hilbert_owner",
            "object": "same-action Hilbert source",
            "statement": "Once ordinary matter action is fixed, its source is the Hilbert/coframe variation before readout.",
            "status": "EXACT_SUBTHEOREM_NOT_ENOUGH",
            "proof_or_blocker": "CNF2345/NSCI rows support this, but S_m=sum_A w_A S_A is still a legal covariant countermodel unless w_A is forbidden",
            "theorem_zero": False,
        },
        {
            "theorem_id": "NMC2979_3_countermodel",
            "object": "relative source-weight countermodel",
            "statement": "S_matter=sum_A w_A S_A is diffeomorphism-covariant/additive and changes Hilbert source to sum_A w_A T_A.",
            "status": "COUNTERMODEL_LIVE",
            "proof_or_blocker": "covariance, additivity and classical EOM rescaling do not by themselves kill the source covector",
            "theorem_zero": False,
        },
        {
            "theorem_id": "NMC2979_4_single_action_line",
            "object": "single ordinary-matter action-density line",
            "statement": "One parent action-density line plus one parent measure/hbar would collapse relative w_A to a common calibration mode.",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "proof_or_blocker": "SAL1478/GRM2677 define the needed object, but direct-sum component weights and measure ownership remain open",
            "theorem_zero": False,
        },
        {
            "theorem_id": "NMC2979_5_source_label_forgetting",
            "object": "source-label forgetting",
            "statement": "If the source functor domain is Stress_total rather than labelled pairs {(T_A,A)}, relative source weights are unformable.",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "proof_or_blocker": "SLF1476 gives the clean route, but connected matter graph/source functor ownership is unsigned",
            "theorem_zero": False,
        },
        {
            "theorem_id": "NMC2979_6_hidden_marker",
            "object": "hidden marker/shadow frame",
            "statement": "No hidden Weyl/disformal/source-only marker can feed an active source coefficient.",
            "status": "NOT_DERIVED_RETAIN_SHADOW_ROWS",
            "proof_or_blocker": "DESC2956/SCB2437 keep hidden frame and shadow-current coefficient rows live",
            "theorem_zero": False,
        },
        {
            "theorem_id": "NMC2979_7_Y5_Y6",
            "object": "Y5/Y6 source-normalization and extra-stress",
            "statement": "Y5/Y6 must be generated as even/topological/common-mode or kept as finite source coefficients.",
            "status": "OPEN_HARD_BLOCK",
            "proof_or_blocker": "SFE2164/RCS2446 identify these as hard source-current channels",
            "theorem_zero": False,
        },
        {
            "theorem_id": "NMC2979_8_verdict",
            "object": "no-marker source-covector theorem",
            "statement": "Current corpus does not derive Hom_parent(source labels/hidden markers, Coeff_source-only)=empty.",
            "status": "NOT_DERIVED_CONSTRUCTOR_EXHAUSTION_OR_FINITE_JZ_COEFFICIENTS_REQUIRED",
            "proof_or_blocker": "conditional theorem is clean, but parent constructor exhaustion is missing and countermodels remain legal",
            "theorem_zero": False,
        },
    ]
    return [add_common(row) for row in rows]


def constructor_rows() -> list[dict[str, Any]]:
    rows = [
        ("PCX2979_0_parent_constructor", "ParentGenerate image is derived from MTS primitives", "ParentGenerate[Q_obs,Psi,theta_rep,universal constants,boundary proper terms]", "MISSING_CONSTRUCTOR_EXHAUSTION", "DEC2508 explicitly says repeating no-slot without constructor exhaustion is wheel-spinning"),
        ("PCX2979_1_no_coeff_target", "Coeff_source-only target absent from parent object language", "Coeff_active_source notin Obj(Language_parent)", "CONDITIONAL_ONLY", "PSBF2344/NST1479 give the target but not derivation"),
        ("PCX2979_2_no_hom", "no Hom from species/hidden markers into source coefficient", "Hom_parent(SpeciesLabel or HiddenMarker,Coeff_source-only)=empty or common constant", "NOT_PARENT_SIGNED", "NSS2343/GRM2677 contracts remain unsigned"),
        ("PCX2979_3_single_action_density", "one parent ordinary-matter action-density line", "S_ord=int dmu_parent L_ord / hbar_parent with no w_A S_A slots", "CONDITIONAL_NOT_PARENT_SIGNED", "SAL1478 direct-sum countermodel remains live"),
        ("PCX2979_4_species_blind_measure", "species-blind measure/Jacobian/action scale", "D_A log mu_parent = D_A log J_measure = 0", "MEASURE_OWNER_REQUIRED", "ASO2774 says field rescaling cannot close it"),
        ("PCX2979_5_label_forgetting", "source labels forgotten before coupling", "q_src({(T_A,A)})=T_total before kappa/gravity coupling", "UNSIGNED_DEPENDENCY", "SLF1476 route exists but connected graph/source functor not owned"),
        ("PCX2979_6_no_readout_reentry", "readout/projector/material labels cannot re-enter source current", "variation precedes readout; readout maps on solutions only", "CONDITIONAL_ONLY", "Jreadout/PiM rows remain finite nonclaim"),
        ("PCX2979_7_no_boundary_domain_reentry", "boundary/domain/worldtube cannot carry composition/source labels", "B/domain/support terms exact, proper, source-blind or bounded", "DEFERRED_BOUNDARY_DOMAIN", "B_Z branch kept separate by 2978"),
        ("PCX2979_8_same_branch", "all clauses close in one branch", "PCX2979_0 through PCX2979_7 parent-signed together", "NOT_CLOSED", "separate conditional wins are not enough for theorem-zero"),
    ]
    return [
        add_common(
            {
                "constructor_id": constructor_id,
                "required_gate": required_gate,
                "formal_requirement": formal_requirement,
                "status": status,
                "blocking_gap": blocking_gap,
                "gate_closed": False,
            }
        )
        for constructor_id, required_gate, formal_requirement, status, blocking_gap in rows
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    rows = [
        ("JZC2979_0_total", "eps_JZ", "eps_JZ <= eps_direct + eps_mem + eps_readout + eps_PiM + eps_shadow + eps_Y5 + eps_Y6 + eps_common_drift", "source norm", "MISSING_COMPONENT_VALUES", "all component rows theorem-zero or source-backed numeric", "MISSING", "none"),
        ("JZC2979_1_delta_w_common", "delta_w_common", "common source/action calibration mode", "dimensionless", "COMMON_MODE_NOT_HARMLESS_UNTIL_DRIFT_SILENT", "time/frame/source calibration silence", "MISSING_OR_PROXY_NONCLAIM", "CBP1479_0_delta_w_common"),
        ("JZC2979_2_delta_w_e_proxy", "delta_w_e", "electron/lepton source-weight component proxy", "dimensionless", "PROXY_NOT_PARENT_BASIS", "MTS parent component map and tau/source/readout/product convention", "8.948213306283e-11", "CBP1479_1_delta_w_e"),
        ("JZC2979_3_delta_w_EM", "delta_w_EM", "EM/Coulomb component", "dimensionless", "MISSING_PARENT_EM_COMPONENT_MAP", "MTS parent EM/Coulomb component map", "MISSING_OR_PROXY_NONCLAIM", "CBP1479_2_delta_w_EM"),
        ("JZC2979_4_delta_w_qg", "delta_w_qg", "light-quark/QCD/gluon/bulk binding components", "dimensionless", "MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS", "sourced mass-decomposition basis and parent split", "MISSING_OR_PROXY_NONCLAIM", "CBP1479_3_delta_w_q;CBP1479_4_delta_w_g"),
        ("JZC2979_5_delta_J_A", "delta_J_A", "species-only measure/Jacobian residual", "dimensionless", "MISSING_MEASURE_OWNER_OR_BOUND", "measure theorem or numeric projection", "MISSING_OR_PROXY_NONCLAIM", "CBP1479_6_delta_J_A"),
        ("JZC2979_6_delta_c_A", "delta_c_A", "current/source normalization residual", "dimensionless", "MISSING_CURRENT_OWNER_OR_COEFFICIENT", "current-owner theorem or finite c_A row", "MISSING_OR_PROXY_NONCLAIM", "CBP1479_7_delta_c_A"),
        ("JZC2979_7_zeta_A", "zeta_A", "non-Hilbert/readout source-current residual", "dimensionless", "MISSING_NONHILBERT_CURRENT_OWNER", "J_NH definition and projection/silence proof", "MISSING_OR_PROXY_NONCLAIM", "CBP1479_8_zeta_A"),
        ("JZC2979_8_Jdirect_marker", "J_direct_marker", "direct matter marker/source coupling", "source norm", "MISSING_MARKER_COEFFICIENT", "JDIR marker and effective direct coupling coefficients", "MISSING", "JDIR2522_5_marker_m;JDIR2522_6_effective_m"),
        ("JZC2979_9_Jmem_shadow", "J_shadow", "source-only weight/hidden marker/source-normalization shadow", "memory source units", "MISSING_NO_SOURCE_ONLY_SLOT_THEOREM", "source-weight vector, no-source-slot theorem, arena kernel", "MISSING", "JDRV2521_7_shadow_weight"),
        ("JZC2979_10_Jreadout_material", "J_material_comm", "material/WEP/source composition readout", "source norm", "MISSING_READOUT_PROJECTION", "material projector and composition sensitivity coefficients", "MISSING", "JRO2523_4_material_comm"),
        ("JZC2979_11_JPiM_extra", "E_extra_current", "extra source-current/anomaly leakage in projected mass closure", "dimensionless/source norm", "MISSING_EXTRA_CURRENT_OWNER", "extra-current/anomaly coefficient and projection", "MISSING", "JPIM2524_8_extra_current"),
        ("JZC2979_12_Y5", "eps_JZ_Y5", "source-normalization channel", "source norm", "MISSING_Y5_ZERO_OR_BOUND", "Y5 even/topological proof or finite coefficient", "MISSING", "RCS2446_4_coupling_constant;SFE2164_5_Y5_Y6"),
        ("JZC2979_13_Y6", "eps_JZ_Y6", "extra-stress/visible-coefficient channel", "source norm", "MISSING_Y6_ZERO_OR_BOUND", "Y6 even/topological proof or finite coefficient", "MISSING", "RCS2446_6_EM_clock_mass_coupling_guard;SFE2164_5_Y5_Y6"),
    ]
    return [
        add_common(
            {
                "coefficient_id": coefficient_id,
                "symbol": symbol,
                "meaning": meaning,
                "units": units,
                "status": status,
                "required_for_promotion": required_for_promotion,
                "current_value": current_value,
                "source_anchor": source_anchor,
                "accepted_for_scoring": False,
            }
        )
        for coefficient_id, symbol, meaning, units, status, required_for_promotion, current_value, source_anchor in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN2979_0_no_missing", "No `MISSING`, blank source paths, or proxy-only component values", "every J_Z component value has a source-backed number or theorem_zero=true", False),
        ("RUN2979_1_same_branch", "All zero theorems/numeric coefficients belong to the same parent branch", "no mixing source-blind theorem from one branch with coefficient map from another", False),
        ("RUN2979_2_units", "Units/norms are compatible with the q_loc envelope", "source norm and dimensionless weights have declared conversion into eps_JZ", False),
        ("RUN2979_3_no_cancellation", "No sign cancellation is used unless a parent identity proves it", "sum absolute component norms", True),
        ("RUN2979_4_proxy_policy", "Proxy rows remain nonclaim", "delta_w_e proxy cannot score until parent EM/matter map and projection conventions exist", True),
        ("RUN2979_5_claim_gate", "J_Z can be promoted only when theorem-zero or all finite components pass", "current checkpoint fails promotion", False),
    ]
    return [
        add_common(
            {
                "rule_id": rule_id,
                "rule": rule,
                "requirement": requirement,
                "passed_now": passed_now,
            }
        )
        for rule_id, rule, requirement, passed_now in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2979_0_typing_template", "conditional no-source-covector typing theorem", True, "template valid but not parent-derived", False),
        ("CG2979_1_constructor_exhaustion", "parent constructor forbids source-only covectors", False, "ParentGenerate image not exhausted", False),
        ("CG2979_2_JZ_zero", "J_Z=0 theorem-zero", False, "no-marker theorem not parent-signed", False),
        ("CG2979_3_JZ_finite", "finite J_Z coefficient row usable for scoring", False, "component values remain missing/proxy/nonparent", False),
        ("CG2979_4_local_GR", "local GR/Newton reduction", False, "q_loc source-current suppression still open", False),
        ("CG2979_5_empirical_claims", "R10/PPN/clock/orbital/WEP claims", False, "no promoted J_Z theorem or finite bound", False),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": allowed,
            }
        )
        for gate_id, claim, passed, status, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2979_0_conditional_win",
            "decision": "Retain the no-source-covector theorem as a clean conditional grammar theorem.",
            "because": "inside a parent-derived typed grammar with no source coefficient target, a_A Z^A is ill-typed.",
            "next_action": "do not promote without constructor exhaustion",
        },
        {
            "decision_id": "DEC2979_1_countermodel",
            "decision": "Do not claim covariance/Hilbert/current-owner alone kills source weights.",
            "because": "S_m=sum_A w_A S_A remains a live covariant countermodel.",
            "next_action": "require parent action-line/measure/no-Hom proof or finite coefficients",
        },
        {
            "decision_id": "DEC2979_2_pivot",
            "decision": "Stop looping the no-slot theorem unless new constructor-exhaustion evidence appears.",
            "because": "2508 already warned that repeating no-slot without ParentGenerate exhaustion is wheel-spinning.",
            "next_action": "attack ParentGenerate exhaustion directly or acquire first real J_Z coefficient",
        },
        {
            "decision_id": "DEC2979_3_proxy",
            "decision": "Keep the electron delta_w proxy visible but nonclaim.",
            "because": "a proxy value exists, but not on the MTS parent basis or projection convention.",
            "next_action": "use it only as a schema smoke row until parent component map exists",
        },
    ]
    return [add_common(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2979_0_2980",
            "priority": "selected_primary",
            "next_doc": "2980-Y5-R2FR-parent-constructor-exhaustion-or-first-real-JZ-coefficient-row-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_parent_constructor_exhaustion_or_first_real_JZ_coefficient_row_under_AX1090_2980.py",
            "objective": "Either derive the ParentGenerate image/no-Hom exclusion that forbids source-only covectors, or promote one real source-backed J_Z component coefficient row without proxy or MISSING markers.",
            "include": "ParentGenerate;no Hom;source coefficient target;single action density;species-blind measure;source-label forgetting;delta_w_e proxy audit;J_direct;J_shadow;Y5;Y6",
            "exclude": "B_Z full boundary proof;full K_metric certificate;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
        }
    ]
    return [add_common(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        add_common({"copy_id": key, "path": str(path), "exists": path.exists()})
        for key, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    formalization_2979_count = 0
    if FORMALIZATION.exists():
        formalization_2979_count = sum(1 for path in FORMALIZATION.rglob("*2979*") if path.is_file())
    checks = [
        ("VAL2979_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2979_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2979_2_conditional_theorem", any(row["theorem_id"] == "NMC2979_1_conditional_typing" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in all_rows["theorem"]), "conditional no-source-covector theorem recorded", True),
        ("VAL2979_3_countermodel_live", any(row["theorem_id"] == "NMC2979_3_countermodel" and row["status"] == "COUNTERMODEL_LIVE" for row in all_rows["theorem"]), "source-weight countermodel retained", True),
        ("VAL2979_4_verdict_not_derived", any(row["theorem_id"] == "NMC2979_8_verdict" and row["status"].startswith("NOT_DERIVED") for row in all_rows["theorem"]), "no-marker theorem remains unclaimed", True),
        ("VAL2979_5_constructor_open", all(not row["gate_closed"] for row in all_rows["constructor"]), "constructor-exhaustion gates remain open", True),
        ("VAL2979_6_coefficients_nonclaim", all((not row["accepted_for_scoring"]) and row["valid_for_claim"] is False for row in all_rows["coefficients"]), "J_Z coefficient rows remain nonclaim", True),
        ("VAL2979_7_proxy_nonclaim", any(row["coefficient_id"] == "JZC2979_2_delta_w_e_proxy" and row["status"] == "PROXY_NOT_PARENT_BASIS" and row["accepted_for_scoring"] is False for row in all_rows["coefficients"]), "delta_w_e proxy is visible but nonclaim", True),
        ("VAL2979_8_claims_blocked_except_template", all((row["claim_gate_id"] == "CG2979_0_typing_template") or (row["claim_allowed"] is False) for row in all_rows["claims"]), "physics claim gates remain blocked", True),
        ("VAL2979_9_next_target_written", any(row["next_id"] == "NEXT2979_0_2980" for row in all_rows["next"]), "2980 constructor/first-JZ-coefficient target selected", True),
        ("VAL2979_10_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2979_11_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2979_12_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2979_13_formalization_clean", formalization_2979_count == 0, f"no 2979 outputs were written to formalization-workbench (count={formalization_2979_count})", True),
        ("VAL2979_14_doc_written", DOC.exists(), "2979 markdown checkpoint exists", True),
    ]
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": bool(passed),
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(add_common({"validation_id": "VAL2979_OVERALL", "passed": overall, "check": "2979 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    output_rows = [
        {"output": key, "path": str(path), "exists": path.exists()}
        for key, path in OUTPUTS.items()
        if key != "validation"
    ]
    branch_rows = [
        {"copy": key, "path": str(path), "exists": path.exists()}
        for key, path in BRANCH_OUTPUTS.items()
    ]
    text = f"""# 2979 - No-Marker Source-Covector Theorem or J_Z Component Coefficient Acquisition

Status: `Y5_R2FR_2979_no_source_covector_conditional_theorem_clean_not_parent_derived_countermodel_live_JZ_coefficients_staged_nonclaim`

Claim ceiling: `no_no_marker_theorem_zero_no_JZ_zero_no_q_loc_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

## Summary

- The no-marker route is mathematically clean as a conditional grammar theorem: if the parent constructor has no source-coefficient target, a linear source covector `a_A Z^A` is ill-typed.
- It is not parent-derived yet: covariance, additivity, current ownership, and classical field rescaling do not forbid `S_matter=sum_A w_A S_A`.
- This is a useful sharpening: the missing proof is now `ParentGenerate` exhaustion/no-Hom, not a vague appeal to naturalness.
- Finite `J_Z` coefficient rows are staged, including the existing electron `delta_w_e` proxy, but every row remains nonclaim until parent basis/projection/source backing is real.
- Best next move: either derive the parent constructor image or promote one real non-proxy `J_Z` coefficient row.

## Generated Outputs

{md_table(output_rows, ["output", "path", "exists"])}

## Branch Copies

{md_table(branch_rows, ["copy", "path", "exists"])}

## No-Marker Theorem Attempt

{md_table(all_rows["theorem"], ["theorem_id", "object", "statement", "status", "proof_or_blocker", "theorem_zero"])}

## Parent Constructor Exhaustion Gate

{md_table(all_rows["constructor"], ["constructor_id", "required_gate", "formal_requirement", "status", "blocking_gap", "gate_closed"])}

## J_Z Component Coefficient Ledger

{md_table(all_rows["coefficients"], ["coefficient_id", "symbol", "meaning", "units", "status", "required_for_promotion", "current_value", "accepted_for_scoring"])}

## Promotion Rules

{md_table(all_rows["runner"], ["rule_id", "rule", "requirement", "passed_now"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "theorem": theorem_rows(),
        "constructor": constructor_rows(),
        "coefficients": coefficient_rows(),
        "runner": runner_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    shutil.copyfile(OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"])
    shutil.copyfile(OUTPUTS["coefficients"], BRANCH_OUTPUTS["coefficient_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_copy_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2979 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
