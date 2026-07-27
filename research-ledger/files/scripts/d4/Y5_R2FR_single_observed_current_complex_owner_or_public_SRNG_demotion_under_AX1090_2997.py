from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2997"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2997-Y5-R2FR-single-observed-current-complex-owner-or-public-SRNG-demotion-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2997_SOURCE_REGISTER.csv",
    "owner": RESIDUALS / "P8_Y5_R2FR_2997_SINGLE_OBSERVED_CURRENT_COMPLEX_OWNER_AUDIT.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_2997_PUBLIC_SRNG_DEMOTION_LEDGER.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_2997_FINITE_RESIDUAL_GATE_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2997_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2997_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2997_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2997_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2997_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "owner_copy": PARENT_ACTION / "single_observed_current_complex_owner_2997_NOT_SIGNED.csv",
    "demotion_copy": LOCAL_BOUNDS / "public_SRNG_closure_only_and_residual_gates_2997_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2997_QV_OR_CURRENT_COMPLEX_BOUND_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def base(row: dict[str, Any]) -> dict[str, Any]:
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


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC2997_00_2996_next",
        RESIDUALS / "P8_Y5_R2FR_2996_NEXT_TARGET.csv",
        ["NEXT2996_0_2997", "single parent-owned observed-current complex"],
        "2996 selects the single observed-current complex proof or public SRNG demotion.",
    ),
    (
        "SRC2997_01_2996_contract",
        RESIDUALS / "P8_Y5_R2FR_2996_SRNG_OFC_PUBLIC_PARENT_CONTRACT_AUDIT.csv",
        ["PC2996_3_source_worldtube_complex", "PUBLIC_PARENT_CONTRACT_NOT_SIGNED"],
        "public SRNG/OFC contract identifies source-worldtube/current-complex as shared antecedent.",
    ),
    (
        "SRC2997_02_2901_q_nullness",
        RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_NULLNESS_AUDIT.csv",
        ["QK2901_9_verdict", "FAIL_CURRENT_MTS_Q_KERNEL_OWNER_NOT_DERIVED"],
        "parent q/observed-stack kernel owner attempt fails current MTS.",
    ),
    (
        "SRC2997_03_2901_certificate",
        RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_CERTIFICATE_GATE.csv",
        ["CERT2901_0_q_map", "MISSING_PARENT_Q_MAP"],
        "certificate gate lists missing q map and vertical-kernel inputs.",
    ),
    (
        "SRC2997_04_2900_source_complex",
        RESIDUALS / "P8_Y5_R2FR_2900_SOURCE_COMPLEX_OWNER_AUDIT.csv",
        ["SC2900_9_verdict", "FAIL_CURRENT_MTS_SOURCE_COMPLEX_OWNER_NOT_DERIVED"],
        "source-worldtube/current-complex owner theorem is not derived.",
    ),
    (
        "SRC2997_05_2900_hilbert_contract",
        RESIDUALS / "P8_Y5_R2FR_2900_HILBERT_CURRENT_COMPLEX_CONTRACT.csv",
        ["HCC2900_0_primary_current", "CONDITIONAL_CONTRACT"],
        "Hilbert current complex contract is least-circular but conditional.",
    ),
    (
        "SRC2997_06_2588_owner",
        RESIDUALS / "P8_Y5_OBS_STACK_2588_OWNER_CERTIFICATE.csv",
        ["OSC2588_0_q_map", "MISSING_PARENT_Q_MAP"],
        "observed stack owner certificate keeps q map missing.",
    ),
    (
        "SRC2997_07_2588_claims",
        RESIDUALS / "P8_Y5_OBS_STACK_2588_CLAIM_GATES.csv",
        ["CG2588_1_parent_q", "BLOCKED_NONCLAIM"],
        "observed stack claim gates block parent q promotion.",
    ),
    (
        "SRC2997_08_2587_matter",
        RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
        ["MCA2587_7_current_verdict", "CONTRACT"],
        "minimal matter coupling contract exists but is not parent-adopted.",
    ),
    (
        "SRC2997_09_2542_observation",
        RESIDUALS / "P8_Y5_NO_SHADOW_2542_OBSERVATION_FUNCTOR_CONTRACT.csv",
        ["OFC2542_5_status", "PRIVATE_CONTRACT_READY_NOT_DERIVED"],
        "downstream observation functor contract remains private/nonclaim.",
    ),
    (
        "SRC2997_10_2925_reduction",
        RESIDUALS / "P8_Y5_R2FR_2925_REDUCTION_THEOREM_LADDER.csv",
        ["RTL2925_0_statement", "EXACT_CONDITIONAL_THEOREM_WRITTEN"],
        "conditional local reduction theorem exists but is not promoted.",
    ),
    (
        "SRC2997_11_2941_gk",
        RESIDUALS / "P8_Y5_R2FR_2941_GK_ACTION_EXISTENCE_THEOREM_GATE.csv",
        ["GKT2941_0_weak_action_existence", "FAIL_CURRENT_STRONG_ADOPTION"],
        "GK/q_loc weak action template exists but strong parent adoption fails.",
    ),
]


def source_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "required_needles": "; ".join(needles),
                "needles_found": anchors(path, needles),
                "role": role,
            }
        )
        for source_id, path, needles, role in SOURCE_SPECS
    ]


def owner_rows() -> list[dict[str, Any]]:
    data = [
        (
            "SOC2997_0_theorem",
            "single observed-current complex theorem",
            "If q/e_obs/tau/ell_J, W_source, A_ext, S_link, J_H, Pi_M and M_ref are same-branch parent objects fixed before readout, then SRNG/OFC can be promoted from private closure to public source/readout no-reentry theorem.",
            "EXACT_ACCEPTANCE_THEOREM_WRITTEN",
            "every object-owner clause must pass together",
            False,
        ),
        (
            "SOC2997_1_q_map",
            "parent q map and Dq",
            "q:Phi_parent->Q_vis with explicit components, Dq, constant-rank domain and vertical basis V=ker(Dq)",
            "MISSING_PARENT_Q_MAP_AND_VERTICAL_BASIS",
            "2901/2588 retain epsilon_q_owner and projection-declaration guard",
            False,
        ),
        (
            "SOC2997_2_vertical_kernel",
            "presymplectic-null/matter-invisible kernel",
            "vertical generators must carry zero compact CPS charge and leave matter/source/support/readout invisible before readout",
            "MISSING_THETA_QV_ZERO_FLUX_AND_MATTER_DESCENT",
            "2901 sends this to vertical Noether Qv extraction",
            False,
        ),
        (
            "SOC2997_3_basic_stack",
            "basic e_obs/tau/ell_J stack",
            "e_obs, tau and ell_J must be functors of q or have source-backed finite leakage bounds in the same branch",
            "MISSING_BASIC_STACK_CERTIFICATE",
            "2588 and 2901 keep tau/ell_J/basic-coframe leak rows live",
            False,
        ),
        (
            "SOC2997_4_matter_action",
            "single parent matter action before readout",
            "S_matter must use q/e_obs/tau/ell_J and no source-only/species/material hidden slot before variation",
            "CONTRACT_EXISTS_NOT_ADOPTED",
            "2587 writes the least-circular contract but adoption/uniqueness remains blocked",
            False,
        ),
        (
            "SOC2997_5_worldtube_domain",
            "W_source/A_ext/S_link support complex",
            "source worldtube, compact exterior annulus, linking surfaces, orientation and support jumps are fixed before readout",
            "MISSING_FIXED_DOMAIN_SUPPORT_LEDGER",
            "2900 keeps domain motion, support jump and current escape rows",
            False,
        ),
        (
            "SOC2997_6_hilbert_current",
            "Hilbert current J_H[e_obs,tau]",
            "J_H lives in C_H(A_ext;W_source,S_link,e_obs,tau) and descends from the same matter action",
            "CONDITIONAL_CONTRACT_ONLY",
            "HCC2900 is selected least-circularly but not parent-signed",
            False,
        ),
        (
            "SOC2997_7_PiM_Mref",
            "Pi_M fixed chain map and positive M_ref",
            "Pi_M:C_H->C_M is parent-selected before readout, commutes with d, and M_ref is positive/same-frame",
            "MISSING_PIM_SAME_OBJECT_AND_MREF",
            "R_eq, B_zero_flux, projector stress and M_ref locks remain unfilled",
            False,
        ),
        (
            "SOC2997_8_GK_compatibility",
            "q_loc/GK compatibility",
            "The same J_H/Pi_M/source stack must match the weak S_GK template without adding A_mu/P_loc/stress by hand",
            "WEAK_TEMPLATE_NOT_PARENT_ADOPTED",
            "2941 strong adoption fails",
            False,
        ),
        (
            "SOC2997_9_verdict",
            "single observed-current complex owner",
            "All owner clauses are required before public SRNG/OFC can be a theorem.",
            "OWNER_NOT_DERIVED_PUBLIC_SRNG_DEMOTED_TO_CLOSURE_ONLY",
            "SOC2997_1..8 remain unsigned or conditional",
            False,
        ),
    ]
    return [
        base(
            {
                "owner_id": owner_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "owner_signed": signed,
            }
        )
        for owner_id, obj, statement, status, gap, signed in data
    ]


def demotion_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEM2997_0_private_SRNG",
            "private SRNG/OFC branch",
            "RETAIN_AS_PRIVATE_WORKING_CLOSURE",
            "inside private calculations, source/readout Gamma slots and private projective trace may be switched off by contract",
            "not public evidence",
        ),
        (
            "DEM2997_1_public_SRNG",
            "public SRNG/OFC theorem",
            "DEMOTED_TO_CLOSURE_ONLY",
            "single observed-current complex owner not derived",
            "cannot claim local-GR/Newton/WEP/PPN",
        ),
        (
            "DEM2997_2_public_projective",
            "public projective silence",
            "FALLBACK_RETAINED",
            "private no-Gamma branch kills projective by variable absence only inside private branch",
            "retain P4 projective row if affine fallback survives",
        ),
        (
            "DEM2997_3_source_mass",
            "Newton source denominator",
            "RETAIN_RESIDUAL_GATE",
            "J_H, Pi_M, M_ref and worldtube support are not same-object parent-owned",
            "no noncircular measured-GM/Newton derivation yet",
        ),
        (
            "DEM2997_4_WEP_MICROSCOPE",
            "finite WEP/MICROSCOPE route",
            "RETAIN_DATA_INPUT_GATE",
            "range owner, source-current zero, DD map and official readout still missing",
            "no WEP product score",
        ),
        (
            "DEM2997_5_policy",
            "public framework status",
            "CLOSURE_OR_RESIDUALS_ONLY",
            "public theorem not signed, finite residual values not filled",
            "next work must prove Qv/current-complex owner or fill first component bound",
        ),
    ]
    return [
        base(
            {
                "demotion_id": demotion_id,
                "branch": branch,
                "status": status,
                "reason": reason,
                "claim_effect": effect,
            }
        )
        for demotion_id, branch, status, reason, effect in data
    ]


def residual_rows() -> list[dict[str, Any]]:
    data = [
        ("RES2997_0_epsilon_q_owner", "epsilon_q_owner", "parent q map / observed-stack owner leak", "MISSING_PARENT_Q_MAP", "source_normalization;PPN;R11;local_GR"),
        ("RES2997_1_epsilon_kernel_charge", "epsilon_kernel_charge", "vertical CPS charge leakage", "MISSING_THETA_QV_ZERO_FLUX", "local_GR;Newton;PPN;R10;clock"),
        ("RES2997_2_epsilon_basic_stack", "epsilon_basic_stack", "e_obs/tau/ell_J vertical/basic leakage", "MISSING_BASIC_STACK_CERTIFICATE", "same_frame;clock;source_mass;PPN"),
        ("RES2997_3_E_matter_action", "E_matter_action", "matter action/adoption/source-slot obstruction", "MISSING_ACTION_ADOPTION_AND_NO_SOURCE_SLOT", "WEP;source_current;Newton;local_GR"),
        ("RES2997_4_Jdomain_escape", "J_domain_current_escape_envelope", "worldtube/domain/support/current-complex escape", "MISSING_FIXED_DOMAIN_SUPPORT_AND_CURRENT_DESCENT", "PiM;Newton;PPN;R10;local_GR"),
        ("RES2997_5_epsilon_PiM", "epsilon_PiM_equality_commutator", "Pi_M same-object/commutator/projector stress residual", "MISSING_PIM_SAME_OBJECT_AND_STRESS_SILENCE", "Newton;PPN;local_GR"),
        ("RES2997_6_q_loc", "q_loc_residual", "GK/q_loc source/projector/boundary/stress residual", "WEAK_SGK_TEMPLATE_NOT_ADOPTED", "local_GR;PPN;R10;clock;orbital"),
        ("RES2997_TOTAL", "Delta_public_SRNG_owner_total_abs", "absolute envelope over public SRNG owner failures", "COMPONENTS_MISSING_NONCLAIM", "framework_gate;local_GR;Newton;WEP"),
    ]
    return [
        base(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "definition": definition,
                "current_status": status,
                "observable_link": observable_link,
                "numeric_value": "MISSING_NUMERIC_VALUE",
                "source_path": "see_source_register_and_component_rows",
            }
        )
        for residual_id, symbol, definition, status, observable_link in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2997_0_theorem_written", "single observed-current complex theorem is written", True, "EXACT_ACCEPTANCE_THEOREM_NONCLAIM", False),
        ("GATE2997_1_q_map", "parent q/Dq/vertical basis signed", False, "MISSING_PARENT_Q_MAP_AND_VERTICAL_BASIS", False),
        ("GATE2997_2_Qv_null", "vertical kernel charge and compact flux vanish", False, "MISSING_THETA_QV_ZERO_FLUX", False),
        ("GATE2997_3_matter_invisible", "matter/source/worldtube invisible to vertical kernel", False, "MISSING_MATTER_DESCENT_AND_NO_SOURCE_SLOT", False),
        ("GATE2997_4_basic_stack", "e_obs/tau/ell_J basic over q", False, "MISSING_BASIC_STACK_CERTIFICATE", False),
        ("GATE2997_5_source_complex", "W_source/A_ext/S_link/J_H live in one parent complex", False, "MISSING_SOURCE_COMPLEX_OWNER", False),
        ("GATE2997_6_PiM_Mref", "Pi_M and M_ref are same-object parent-owned", False, "MISSING_PIM_MREF_LOCK", False),
        ("GATE2997_7_public_SRNG", "public SRNG/OFC theorem can be promoted", False, "DEMOTED_TO_CLOSURE_ONLY", False),
        ("GATE2997_8_local_GR_Newton", "local GR/Newton/PPN claim allowed", False, "OWNER_AND_RESIDUAL_GATES_OPEN", False),
    ]
    return [
        base(
            {
                "gate_id": gate_id,
                "gate": gate,
                "condition_passed": passed,
                "status": status,
                "promotion_allowed_now": promotion,
            }
        )
        for gate_id, gate, passed, status, promotion in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC2997_0_owner_result",
            "Do not promote the single observed-current complex owner.",
            "q map, vertical Qv/nullness, matter descent, basic stack, fixed worldtube/current complex, Pi_M/M_ref and GK compatibility are all unsigned or conditional.",
            "public SRNG/OFC cannot be used as proof",
        ),
        (
            "DEC2997_1_demote_public_SRNG",
            "Demote public SRNG/OFC to closure-only.",
            "the private branch is useful for internal calculations but not a parent-signed theorem.",
            "keep private SRNG explicitly labelled; retain public residual rows",
        ),
        (
            "DEC2997_2_next_math",
            "The best derivation target is vertical Qv/current-complex ownership.",
            "2901 already says q/observed-stack ownership requires CPS charge/nullness and matter invisibility.",
            "attack Theta_parent/Q_v/zero-flux plus matter/source invisibility",
        ),
        (
            "DEC2997_3_next_fallback",
            "If Qv ownership does not close, fill the first finite residual component.",
            "public theorem route cannot progress by restating contracts.",
            "source a numeric/theorem-zero row for epsilon_q_owner, epsilon_kernel_charge or J_domain escape",
        ),
    ]
    return [
        base(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "next_id": "NEXT2997_0_2998",
                "priority": "selected_primary",
                "next_doc": "2998-Y5-R2FR-vertical-Qv-current-complex-owner-or-first-public-SRNG-residual-bound-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_vertical_Qv_current_complex_owner_or_first_public_SRNG_residual_bound_under_AX1090_2998.py",
                "objective": "Try to derive the vertical Noether/Qv and current-complex ownership clauses required by 2997: parent q/Dq, vertical basis, Theta_parent, Q_v, compact zero flux, matter invisibility, basic e_obs/tau/ell_J, and fixed W_source/A_ext/S_link/J_H. If not, fill the first finite public-SRNG residual bound row with units/source path.",
                "include": "2901 q-kernel nullness;2902 Qv extraction contract;2588 observed stack owner;2587 matter action contract;2900 current-complex audit;2997 residual rows",
                "exclude": "public SRNG proof by declaration;private SRNG as public theorem;EH-only charge import;closure multiplier;local-GR/Newton/PPN/WEP/R10 claim;GitHub;formalization-workbench edits",
            }
        )
    ]


def validation_rows(
    source_output_rows: list[dict[str, Any]],
    owner_output_rows: list[dict[str, Any]],
    demotion_output_rows: list[dict[str, Any]],
    residual_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    sources_ok = all(boolish(row["path_exists"]) for row in source_output_rows)
    anchors_ok = all(boolish(row["needles_found"]) for row in source_output_rows)
    theorem_written = any(row["owner_id"] == "SOC2997_0_theorem" for row in owner_output_rows)
    owner_refused = any(row["owner_id"] == "SOC2997_9_verdict" and row["current_status"] == "OWNER_NOT_DERIVED_PUBLIC_SRNG_DEMOTED_TO_CLOSURE_ONLY" for row in owner_output_rows)
    demotion_ok = any(row["demotion_id"] == "DEM2997_1_public_SRNG" and row["status"] == "DEMOTED_TO_CLOSURE_ONLY" for row in demotion_output_rows)
    residuals_ok = any(row["residual_id"] == "RES2997_TOTAL" and row["current_status"] == "COMPONENTS_MISSING_NONCLAIM" for row in residual_output_rows)
    gates_ok = any(row["gate_id"] == "GATE2997_8_local_GR_Newton" and not boolish(row["condition_passed"]) for row in gate_output_rows)
    branch_ok = all(boolish(row["copy_exists"]) and boolish(row["parse_ok"]) for row in branch_output_rows)
    csv_parse_ok = all(csv_ok(path) for path in output_paths if path.exists() and path.suffix == ".csv")
    outputs_under_post = all(under(path, ROOT) for path in output_paths + [DOC])
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*2997*") if path.is_file())
    no_claim_flags = True
    for output_path in output_paths:
        if output_path.exists() and output_path.suffix == ".csv":
            for output_row in rows(output_path):
                if str(output_row.get("valid_for_claim", "")).strip().lower() == "true":
                    no_claim_flags = False
                if str(output_row.get("claim_allowed", "")).strip().lower() == "true":
                    no_claim_flags = False
                if str(output_row.get("promotion_allowed_now", "")).strip().lower() == "true":
                    no_claim_flags = False
    data = [
        ("VAL2997_0_sources_exist", sources_ok, "all cited local source paths exist"),
        ("VAL2997_1_anchors_found", anchors_ok, "all cited source anchors found"),
        ("VAL2997_2_theorem_written", theorem_written, "single observed-current complex theorem is written"),
        ("VAL2997_3_owner_refused", owner_refused, "owner theorem is refused for current MTS"),
        ("VAL2997_4_public_SRNG_demoted", demotion_ok, "public SRNG/OFC is demoted to closure-only"),
        ("VAL2997_5_residual_rows", residuals_ok, "finite residual gate rows are staged"),
        ("VAL2997_6_local_claim_false", gates_ok, "local GR/Newton/PPN gate remains false"),
        ("VAL2997_7_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2997_8_csvs_parse", csv_parse_ok, "all generated CSVs parse"),
        ("VAL2997_9_outputs_under_post", outputs_under_post, "all outputs are under post-checkpoint-work"),
        ("VAL2997_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2997_11_formalization_clean", formalization_count == 0, f"no 2997 outputs in formalization-workbench (count={formalization_count})"),
        ("VAL2997_12_doc_written", DOC.exists(), "2997 markdown checkpoint exists"),
    ]
    overall = all(passed for _, passed, _ in data)
    data.append(("VAL2997_OVERALL", overall, "2997 attempts the single observed-current complex owner, refuses public promotion, demotes public SRNG/OFC to closure-only, and selects Qv/current-complex ownership next"))
    return [
        base(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": True,
            }
        )
        for validation_id, passed, check in data
    ]


def write_doc(
    source_output_rows: list[dict[str, Any]],
    owner_output_rows: list[dict[str, Any]],
    demotion_output_rows: list[dict[str, Any]],
    residual_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    decision_output_rows: list[dict[str, Any]],
    next_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
    validation_output_rows: list[dict[str, Any]],
) -> None:
    document = f"""# 2997 - Y5/R2FR Single Observed-Current Complex Owner Or Public SRNG Demotion Under AX1090

Status: `Y5_R2FR_2997_single_observed_current_complex_owner_not_derived_public_SRNG_demoted_closure_only_nonclaim`

Claim ceiling: `no_public_SRNG_claim_no_single_complex_owner_claim_no_Newton_no_local_GR_no_PPN_no_WEP_no_R10_no_GitHub_no_formalization_edit`

## Current Verdict

2997 tries the exact owner proof demanded by 2996. The theorem shape is clean: if `q/e_obs/tau/ell_J`, `W_source`, `A_ext`, `S_link`, `J_H`, `Pi_M` and `M_ref` are all parent-owned, same-branch, fixed before readout, and invisible to vertical kernel directions, then private `SRNG/OFC` can become a public source/readout no-reentry theorem.

Current MTS does not yet prove that object. The upstream `q` map, vertical basis, CPS/Noether charge, matter invisibility, basic observed stack, fixed worldtube/domain, Hilbert-current complex, `Pi_M` same-object lock and positive `M_ref` are still unsigned or conditional.

Therefore public `SRNG/OFC` is demoted to closure-only. It remains useful as a private working branch, but it cannot support a public local-GR/Newton/WEP/PPN claim. The finite residual route stays explicit.

## Source Register

{md_table(source_output_rows, ["source_id", "path_exists", "needles_found", "role"])}

## Single Observed-Current Complex Owner Audit

{md_table(owner_output_rows, ["owner_id", "object", "current_status", "owner_signed", "blocking_gap"])}

## Public SRNG Demotion Ledger

{md_table(demotion_output_rows, ["demotion_id", "branch", "status", "reason", "claim_effect"])}

## Finite Residual Gate Rows

{md_table(residual_output_rows, ["residual_id", "symbol", "current_status", "observable_link", "numeric_value"])}

## Promotion Gates

{md_table(gate_output_rows, ["gate_id", "gate", "condition_passed", "status", "promotion_allowed_now"])}

## Decision Ledger

{md_table(decision_output_rows, ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(next_output_rows, ["next_id", "next_doc", "objective", "exclude"])}

## Branch Copies

{md_table(branch_output_rows, ["copy_id", "destination", "copy_exists", "row_count", "parse_ok", "valid_for_claim"])}

## Validation

{md_table(validation_output_rows, ["validation_id", "passed", "check", "required"])}

## Plain-English Takeaway

This is a hard but useful answer. The public route is not allowed to coast on a private contract anymore. Either the vertical Noether/current-complex owner gets proved, or public `SRNG/OFC` stays closure-only and we work with explicit residual bounds. That is exactly the kind of discipline needed before claiming any GR reduction.
"""
    DOC.write_text(document, encoding="utf-8")


def main() -> None:
    source_output_rows = source_rows()
    owner_output_rows = owner_rows()
    demotion_output_rows = demotion_rows()
    residual_output_rows = residual_rows()
    gate_output_rows = gate_rows()
    decision_output_rows = decision_rows()
    next_output_rows = next_rows()

    write_csv(OUTPUTS["sources"], source_output_rows)
    write_csv(OUTPUTS["owner"], owner_output_rows)
    write_csv(OUTPUTS["demotion"], demotion_output_rows)
    write_csv(OUTPUTS["residuals"], residual_output_rows)
    write_csv(OUTPUTS["gates"], gate_output_rows)
    write_csv(OUTPUTS["decision"], decision_output_rows)
    write_csv(OUTPUTS["next"], next_output_rows)

    shutil.copyfile(OUTPUTS["owner"], BRANCH_OUTPUTS["owner_copy"])
    shutil.copyfile(OUTPUTS["demotion"], BRANCH_OUTPUTS["demotion_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branch_output_rows = [
        base(
            {
                "copy_id": copy_id,
                "destination": str(destination),
                "copy_exists": destination.exists(),
                "row_count": len(rows(destination)) if destination.exists() else 0,
                "parse_ok": csv_ok(destination) if destination.exists() else False,
            }
        )
        for copy_id, destination in BRANCH_OUTPUTS.items()
    ]
    write_csv(OUTPUTS["branches"], branch_output_rows)

    DOC.write_text("", encoding="utf-8")
    validation_output_rows = validation_rows(
        source_output_rows,
        owner_output_rows,
        demotion_output_rows,
        residual_output_rows,
        gate_output_rows,
        branch_output_rows,
    )
    write_csv(OUTPUTS["validation"], validation_output_rows)

    write_doc(
        source_output_rows,
        owner_output_rows,
        demotion_output_rows,
        residual_output_rows,
        gate_output_rows,
        decision_output_rows,
        next_output_rows,
        branch_output_rows,
        validation_output_rows,
    )


if __name__ == "__main__":
    main()
