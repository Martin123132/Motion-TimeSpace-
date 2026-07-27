from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4359"
CLAIM_ID = "L-200"
BRANCH = "MTS_R2FR_Y5_TRANSITION_TAU_MIN_LOWER_BOUND_OR_ACTION_MEASURE_ZERO_PROOF_4359"
DECISION = "TAU_MIN_REQUIRES_NONNULL_ALIGNMENT_ACTION_MEASURE_OWNER_AXIOM_IMPORTED_UNSIGNED_OFFICIAL_READOUT_TARGET_SELECTED_NONCLAIM"
MARKER = "PPC4161_TRANSITION_TAU_MIN_LOWER_BOUND_OR_ACTION_MEASURE_ZERO_PROOF_4359"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_TAU_MIN_LOWER_BOUND_OR_ACTION_MEASURE_ZERO_PROOF_4359"
NEXT_TARGET = "4360-Y5-R2FR-transition-official-MICROSCOPE-readout-or-parent-nondegeneracy.md"

FORMAL_PATH = FORMAL / "375-PPC4161-transition-tau-min-lower-bound-or-action-measure-zero-proof.md"
DOC_PATH = POST / "4359-Y5-R2FR-transition-tau-min-lower-bound-or-action-measure-zero-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4359_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4359_00_4358_next": (
        FORMAL / "374-PPC4161-transition-action-measure-owner-or-tau-WEP-source-projection-bridge.md",
        "4359-Y5-R2FR-transition-tau-min-lower-bound-or-action-measure-zero-proof.md",
        "4358 handoff to tau-min lower bound or action-measure zero proof.",
    ),
    "SRC4359_01_4358_amplitude": (
        FORMAL / "374-PPC4161-transition-action-measure-owner-or-tau-WEP-source-projection-bridge.md",
        "then abs(Delta_w_TiPt) <= 2.8e-15/tau_min.",
        "4358 product-to-amplitude bridge.",
    ),
    "SRC4359_02_1597_condition": (
        POST / "1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md",
        "1597 derives the precise `tau_min` condition",
        "Existing tau-min condition proof.",
    ),
    "SRC4359_03_1597_nonzero_not_enough": (
        POST / "1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md",
        "Nonzero factors alone do not prove `tau_WEP != 0`",
        "Nonzero factor shortcut rejection.",
    ),
    "SRC4359_04_1597_sufficient": (
        POST / "1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md",
        "if ||K_CMSM||>=k_min, ||S_Earth||>=s_min, ||M_TiPt||>=m_min, |cos(theta)|>=c_min>0 and N_eta<=N_max",
        "Sufficient lower-bound inequality.",
    ),
    "SRC4359_05_1597_kernel": (
        POST / "1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md",
        "`tau_WEP=0` while every component is nonzero",
        "Null-space countermodel in prose.",
    ),
    "SRC4359_06_1597_next": (
        POST / "1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md",
        "NEXT_1598_OFFICIAL_READOUT_OR_PARENT_NONDEGENERACY",
        "Existing next target: official readout or parent nondegeneracy.",
    ),
    "SRC4359_07_1597_tau_audit": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1597_TAU_LOWER_BOUND_THEOREM_AUDIT.csv",
        "TLB1597_1_sufficient_lower_bound",
        "Tau lower-bound theorem audit row.",
    ),
    "SRC4359_08_1597_null": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1597_NULL_SPACE_COUNTERMODEL.csv",
        "NSC1597_0_linear_space_model",
        "Readout-kernel null-space countermodel row.",
    ),
    "SRC4359_09_1597_inputs": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1597_REQUIRED_NONDEGENERACY_INPUTS.csv",
        "NDI1597_3_alignment",
        "Alignment/non-null input requirement.",
    ),
    "SRC4359_10_1597_coupling_zero": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1597_COUPLING_ZERO_PROOF_AUDIT.csv",
        "CZP1597_0_delta_w_zero_route",
        "Coupling zero/action-measure route remains blocked.",
    ),
    "SRC4359_11_1597_product": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1597_WEP_PRODUCT_BRANCH_STATUS.csv",
        "WPS1597_0_product_bound",
        "WEP product-bound-only branch status.",
    ),
    "SRC4359_12_1696_owner": (
        POST / "1696-Y5-R2FR-parent-object-language-owner-or-tau-min-current-branch.md",
        "PARENT_OBJECT_LANGUAGE_OWNER_NOT_DERIVED_TAU_MIN_ROUTE_RETAINED",
        "Owner stack is coherent but not parent-derived.",
    ),
    "SRC4359_13_1697_axiom": (
        POST / "1697-Y5-R2FR-owner-axiom-candidate-and-WEP-readout-source-pack.md",
        "AX1697_1_no_source_prefactor",
        "Owner axiom candidate forbids source-only prefactors if derived.",
    ),
    "SRC4359_14_1697_tau_pack": (
        POST / "1697-Y5-R2FR-owner-axiom-candidate-and-WEP-readout-source-pack.md",
        "ACQ1697_4_tau_min",
        "WEP tau-min acquisition pack target.",
    ),
    "SRC4359_15_1084_readout": (
        SOURCE_DIR / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
        "OFFICIAL_ARRAYS_NOT_IMPORTED",
        "Official MICROSCOPE readout arrays remain missing.",
    ),
}

ARENAS = [
    ("WEP_species", "Delta_w_TiPt amplitude", "requires tau_min>0 or Delta_w=0 theorem"),
    ("Newton_source", "source normalization/common matter", "blocked while w_A countermodel survives"),
    ("local_GR", "source/coupling side of local GR", "blocked until WEP source-weight branch is zero or bounded"),
    ("PPN_gamma_beta", "source-weight metric transfer", "needs arena projection, not WEP product anchor alone"),
    ("clock_Gdot", "time-dependent source weight", "requires derivative/source-label silence or finite projection"),
    ("orbital_GM", "source mass normalization", "requires same source-worldtube owner"),
    ("R10_range", "finite-range source coupling", "parallel alpha(lambda) branch remains separate"),
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def tau_lower_rows() -> List[Dict[str, str]]:
    return [
        {
            "tau_id": "TLB4359_0_pairing_definition",
            "statement": "tau_WEP = N_eta^-1 <K_CMSM, V_ST>",
            "definitions": "V_ST := S_Earth x M_TiPt after source-worldtube, material-response and orbit/readout conventions are fixed",
            "result": "formal pairing only",
            "status": "DEFINITION_SHARPENED_NOT_EVALUATED",
            "valid_for_claim": "False",
        },
        {
            "tau_id": "TLB4359_1_sufficient_lower_bound",
            "statement": "if ||K_CMSM|| >= k_min, ||S_Earth|| >= s_min, ||M_TiPt|| >= m_min, |cos(theta)| >= c_min > 0, and N_eta <= N_max, then |tau_WEP| >= k_min*s_min*m_min*c_min/N_max",
            "definitions": "cos(theta) is the branch-locked alignment between the readout functional and the source-material vector",
            "result": "tau_min := k_min*s_min*m_min*c_min/N_max",
            "status": "CONDITIONAL_THEOREM_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "tau_id": "TLB4359_2_nonzero_not_enough",
            "statement": "nonzero readout, source and material norms alone do not imply tau_WEP != 0",
            "definitions": "V_ST can lie in ker(K_CMSM) or cancel under signed orbit/readout averaging",
            "result": "alignment/non-null proof is mandatory",
            "status": "NO_SHORTCUT_LEMMA",
            "valid_for_claim": "False",
        },
        {
            "tau_id": "TLB4359_3_current_verdict",
            "statement": "current corpus lacks official K_CMSM, source worldtube, material tensor, normalization and c_min proof",
            "definitions": "all must be fixed before WEP scoring",
            "result": "NO_NUMERIC_TAU_MIN",
            "status": "TAU_MIN_NOT_DERIVED",
            "valid_for_claim": "False",
        },
    ]


def null_counterexample_rows() -> List[Dict[str, str]]:
    return [
        {
            "counterexample_id": "NS4359_0_linear_kernel",
            "model": "Let K_CMSM be a nonzero readout functional and V_ST be a nonzero source-material vector in ker(K_CMSM).",
            "result": "<K_CMSM,V_ST>=0 while ||K_CMSM||>0 and ||V_ST||>0",
            "blocks": "generic tau_min theorem from nonzero factors alone",
            "required_to_defeat": "official data or parent theorem proving V_ST not in ker(K_CMSM)",
            "valid_for_claim": "False",
        },
        {
            "counterexample_id": "NS4359_1_signed_orbit_cancellation",
            "model": "Orbit/readout contributions with opposite signs cancel in the reported eta channel.",
            "result": "positive bulk source intuition does not imply positive tau_WEP after projection",
            "blocks": "positivity-only tau_min proof",
            "required_to_defeat": "signed kernel plus no-cancellation theorem or absolute-response construction",
            "valid_for_claim": "False",
        },
        {
            "counterexample_id": "NS4359_2_material_null",
            "model": "Ti/Pt finite source-weight response difference is zero or projected silent in the chosen parent basis.",
            "result": "material pair label alone does not guarantee m_min>0",
            "blocks": "material-label-only lower bound",
            "required_to_defeat": "full material response tensor in same source-weight convention",
            "valid_for_claim": "False",
        },
    ]


def nondegeneracy_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "ND4359_0_K_norm",
            "needed_input": "k_min lower bound for official K_CMSM readout functional",
            "why_needed": "readout must be nonzero in the branch-locked eta channel",
            "source_or_derivation": "official MICROSCOPE readout/design matrix",
            "current_status": "MISSING_OFFICIAL_READOUT",
            "priority": "highest",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ND4359_1_source_norm",
            "needed_input": "s_min lower bound for Earth source-weight vector",
            "why_needed": "source object must be nonzero in the same observed-frame convention",
            "source_or_derivation": "source worldtube/profile import or parent source theorem",
            "current_status": "MISSING_SOURCE_WORLDTUBE",
            "priority": "highest",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ND4359_2_material_norm",
            "needed_input": "m_min lower bound for Ti/Pt material response",
            "why_needed": "test-pair vector must be nonzero in the finite source-weight channel",
            "source_or_derivation": "material response tensor or parent matter-action map",
            "current_status": "MISSING_MATERIAL_TENSOR",
            "priority": "high",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ND4359_3_alignment",
            "needed_input": "c_min lower bound for |cos(theta)| between readout functional and source-material vector",
            "why_needed": "excludes the readout-kernel null countermodel",
            "source_or_derivation": "official data computation or parent nondegeneracy theorem",
            "current_status": "MISSING_CRITICAL_ALIGNMENT",
            "priority": "highest",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ND4359_4_normalization",
            "needed_input": "N_max upper bound and sign/absolute eta convention",
            "why_needed": "turns pairing lower bound into dimensionless tau_min",
            "source_or_derivation": "MICROSCOPE product convention/readout normalization",
            "current_status": "MISSING_NORMALIZATION",
            "priority": "high",
            "valid_for_claim": "False",
        },
    ]


def owner_axiom_rows() -> List[Dict[str, str]]:
    return [
        {
            "axiom_id": "AX4359_0_object_language",
            "candidate": "OrdinaryMatterObjectLanguage",
            "would_forbid": "source-only coefficient targets are absent from the parent domain",
            "effect_if_derived": "w_A is ill-typed except common calibration",
            "current_status": "CANDIDATE_NOT_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "axiom_id": "AX4359_1_no_source_prefactor",
            "candidate": "NoSourceOnlyPrefactor",
            "would_forbid": "independent w_A, kappa_A, c_A, zeta_A active-source multipliers",
            "effect_if_derived": "Delta_w_TiPt=0 route can replace tau_min finite route",
            "current_status": "CANDIDATE_NOT_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "axiom_id": "AX4359_2_single_action_line",
            "candidate": "SingleActionDensityLine",
            "would_forbid": "species action weights not tied to measured matter parameters",
            "effect_if_derived": "collapses action weights to common calibration or observable matter constants",
            "current_status": "CANDIDATE_NOT_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "axiom_id": "AX4359_3_no_reentry",
            "candidate": "NoHiddenReadoutReentry",
            "would_forbid": "w_A returning through hidden/source marker channels after variation",
            "effect_if_derived": "protects source-label forgetting from readout/EFT loopholes",
            "current_status": "CANDIDATE_NOT_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "axiom_id": "AX4359_4_verdict",
            "candidate": "owner axiom package",
            "would_forbid": "pre-variation and hidden source-weight routes",
            "effect_if_derived": "Delta_w theorem-zero; WEP tau numeric becomes optional for this branch",
            "current_status": "READY_TARGET_NOT_CLAIM",
            "valid_for_claim": "False",
        },
    ]


def acquisition_pack_rows() -> List[Dict[str, str]]:
    return [
        {
            "pack_id": "ACQ4359_0_readout_matrix",
            "artifact": "P_WEP_K_CMSM_readout.csv",
            "content": "official CMSM/export arrays or validated exact equivalent",
            "current_status": "missing",
            "next_route": "CNES/ONERA/CMSM or validated exact reconstruction",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "ACQ4359_1_source_worldtube",
            "artifact": "P_WEP_R_source_Earth_worldtube.csv",
            "content": "Earth source profile weighted in observed frame",
            "current_status": "missing",
            "next_route": "geophysical Earth model plus MTS source-weight convention",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "ACQ4359_2_material_tensor",
            "artifact": "P_WEP_TiPt_material_response_tensor.csv",
            "content": "TA6V/PtRh10 material response tensor",
            "current_status": "missing",
            "next_route": "official material/composition model or parent matter calculation",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "ACQ4359_3_product_convention",
            "artifact": "P_WEP_eta_product_convention.csv",
            "content": "eta product normalization, signs and absolute-response convention",
            "current_status": "missing",
            "next_route": "MICROSCOPE convention/import gate",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "ACQ4359_4_tau_min",
            "artifact": "P_WEP_tau_min_lower_bound.csv",
            "content": "strictly positive lower bound or parent nondegeneracy theorem",
            "current_status": "missing",
            "next_route": "compute c_min from sourced arrays or derive non-null theorem",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "ACQ4359_5_parser_manifest",
            "artifact": "P_WEP_tau_min_parser_manifest.csv",
            "content": "branch id, units, columns, masks, provenance and refusal gates",
            "current_status": "missing",
            "next_route": "dry-run manifest before scoring",
            "valid_for_claim": "False",
        },
    ]


def transition_update_rows() -> List[Dict[str, str]]:
    return [
        {
            "update_id": "TU4359_0_tau_min",
            "4358_state": "tau_min positive lower bound needed",
            "4359_update": "nonzero-factor shortcut rejected; alignment/non-null c_min is mandatory",
            "effect": "next route is official readout/source data or parent nondegeneracy theorem",
            "valid_for_claim": "False",
        },
        {
            "update_id": "TU4359_1_action_measure",
            "4358_state": "action-measure/no-w_A theorem unsigned",
            "4359_update": "AX1697 owner axiom candidate imported as exact target but not as proof",
            "effect": "zero route remains available but claim-blocked",
            "valid_for_claim": "False",
        },
        {
            "update_id": "TU4359_2_product_branch",
            "4358_state": "MICROSCOPE product anchor available",
            "4359_update": "product branch remains the only source-backed WEP statement",
            "effect": "Delta_w and local-GR remain unclaimed until tau_min or zero theorem closes",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4359_0_tau_min_sufficient",
            "statement": "A positive tau-WEP lower bound follows from positive readout/source/material norms plus a positive alignment lower bound and finite normalization upper bound.",
            "derivation": "|tau_WEP|=|<K,V_ST>|/N_eta >= ||K|| ||V_ST|| |cos(theta)| / N_eta, with ||V_ST|| bounded below by source and material norms.",
            "consequence": "tau_min = k_min*s_min*m_min*c_min/N_max is the exact finite-route target.",
            "status": "CONDITIONAL_THEOREM_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4359_1_nonzero_not_enough",
            "statement": "Nonzero K_CMSM, source vector and material vector do not imply tau_WEP is nonzero.",
            "derivation": "A nonzero vector can lie in the kernel of a nonzero linear functional, or signed orbit/readout terms can cancel.",
            "consequence": "alignment/non-null evidence is mandatory.",
            "status": "NO_SHORTCUT_THEOREM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4359_2_owner_axiom_status",
            "statement": "The owner axiom package would kill w_A if derived, but it is currently a candidate target, not a parent theorem.",
            "derivation": "1696/1697 assemble typed language, no source prefactor, single action line, connected naturality and no reentry, but mark the stack not parent-derived.",
            "consequence": "Delta_w_TiPt=0 cannot be claimed from the owner package yet.",
            "status": "ZERO_ROUTE_TARGET_IMPORTED_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4359_3_transition_source_gate",
            "statement": "The transition source-label hair gate is now reduced to either c_min>0/nondegenerate WEP projection or a parent no-w_A theorem.",
            "derivation": "4357 finite WEP anchor, 4358 product-to-amplitude bridge and 1597 null-space obstruction combine into one fork.",
            "consequence": "the next target is official MICROSCOPE readout/source import or parent nondegeneracy.",
            "status": "REAL_NARROWING_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for arena, observable, requirement in ARENAS:
        rows.append(
            {
                "arena_id": f"AR4359_{arena}",
                "arena": arena,
                "observable": observable,
                "4359_requirement": requirement,
                "zero_route": "derive AX4359 owner/no-w_A package",
                "finite_route": "source k_min,s_min,m_min,c_min,N_max and compute tau_min",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4359_0_tau_min",
            "input": "k_min,s_min,m_min,c_min,N_max all source-backed",
            "action": "COMPUTE_TAU_MIN",
            "result": "tau_min=k_min*s_min*m_min*c_min/N_max and Delta_w bound follows",
            "current_result": "WAITING_FOR_INPUTS",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4359_1_nonzero_factors",
            "input": "nonzero K/source/material without alignment",
            "action": "TEST_SHORTCUT",
            "result": "reject tau_min claim by null-space countermodel",
            "current_result": "REJECT_SHORTCUT",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4359_2_owner_axiom",
            "input": "AX4359 candidate package",
            "action": "TEST_ZERO_ROUTE",
            "result": "candidate exact but unsigned; no Delta_w zero claim",
            "current_result": "REJECT_ZERO_CLAIM_NOW",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4359_3_product_branch",
            "input": "MICROSCOPE product anchor only",
            "action": "KEEP_PRODUCT_BOUND",
            "result": "abs(Delta_w_TiPt*tau_WEP)<=2.8e-15 remains the only source-backed statement",
            "current_result": "NONCLAIM_BOUND_ONLY",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4359_4_next",
            "input": "no tau_min, no owner theorem",
            "action": "SELECT_OFFICIAL_READOUT_OR_PARENT_NONDEGENERACY",
            "result": NEXT_TARGET,
            "current_result": "NEXT_TARGET_SELECTED",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4359_0",
            "rule": "Do not infer tau_min from nonzero readout, source and material factors alone.",
            "reason": "nonzero source-material vector may lie in the readout kernel.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4359_1",
            "rule": "Do not use positivity intuition before the signed readout/orbit/material convention is fixed.",
            "reason": "signed orbit/readout contributions can cancel.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4359_2",
            "rule": "Do not treat AX1697 owner axioms as derived MTS theorem.",
            "reason": "they are a candidate target, not a parent-signed proof.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4359_3",
            "rule": "Do not score WEP/local GR from the product anchor without tau_min or Delta_w=0 theorem.",
            "reason": "Delta_w can remain unconstrained if tau_WEP is null or arbitrarily small.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4359_4",
            "rule": "Do not substitute surrogate-only readout matrices for official MICROSCOPE arrays in a claim.",
            "reason": "official readout/source convention is part of the tau_min object.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4359_0",
            "decision": DECISION,
            "reason": "4359 tries the tau_min proof and derives the exact sufficient condition: k_min, s_min, m_min, c_min>0 and N_max give tau_min=k_min*s_min*m_min*c_min/N_max. It also proves why nonzero factors are not enough: the branch source-material vector can sit in the readout kernel, or signed orbit/readout contributions can cancel. Therefore the positive alignment/non-null input c_min is the critical missing object. The action-measure zero route is imported as the AX1697 owner-axiom candidate, but remains unsigned. The project is narrowed to official MICROSCOPE readout/source/material import or a parent nondegeneracy theorem excluding the null-space countermodel.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4359_0",
            "item": "tau_min theorem",
            "status": "CONDITIONAL_SUFFICIENT_BOUND_DERIVED",
            "note": "tau_min=k_min*s_min*m_min*c_min/N_max if all terms are sourced and c_min>0.",
        },
        {
            "status_id": "STAT4359_1",
            "item": "null-space obstruction",
            "status": "COUNTERMODEL_ACTIVE",
            "note": "nonzero factors can still give tau_WEP=0.",
        },
        {
            "status_id": "STAT4359_2",
            "item": "owner axiom package",
            "status": "CANDIDATE_IMPORTED_UNSIGNED",
            "note": "would kill w_A if derived, but cannot be used as a claim.",
        },
        {
            "status_id": "STAT4359_3",
            "item": "WEP product branch",
            "status": "BOUND_ONLY",
            "note": "abs(Delta_w_TiPt*tau_WEP)<=2.8e-15 remains retained.",
        },
        {
            "status_id": "STAT4359_4",
            "item": "next target",
            "status": "OFFICIAL_READOUT_OR_PARENT_NONDEGENERACY",
            "note": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4359_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can we import/source the official MICROSCOPE readout/source/material objects or prove parent nondegeneracy so c_min>0?",
            "preferred_route": "official readout/source/material acquisition with a dry-run parser and nonzero alignment computation",
            "fallback_route": "derive parent nondegeneracy theorem excluding V_ST in ker(K_CMSM), or derive AX4359 owner theorem to set Delta_w=0",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "tau_lower": tau_lower_rows(),
        "null_counterexamples": null_counterexample_rows(),
        "nondegeneracy": nondegeneracy_rows(),
        "owner_axiom": owner_axiom_rows(),
        "acquisition_pack": acquisition_pack_rows(),
        "transition_updates": transition_update_rows(),
        "theorems": theorem_rows(),
        "arenas": arena_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_tables(tables: Dict[str, List[Dict[str, str]]]) -> None:
    mapping = {
        "sources": "P8_Y5_R2FR_4359_SOURCE_REGISTER.csv",
        "tau_lower": "P8_Y5_R2FR_4359_TAU_LOWER_BOUND_ROWS.csv",
        "null_counterexamples": "P8_Y5_R2FR_4359_NULL_COUNTEREXAMPLE_ROWS.csv",
        "nondegeneracy": "P8_Y5_R2FR_4359_NONDEGENERACY_INPUT_ROWS.csv",
        "owner_axiom": "P8_Y5_R2FR_4359_OWNER_AXIOM_ROWS.csv",
        "acquisition_pack": "P8_Y5_R2FR_4359_WEP_ACQUISITION_PACK.csv",
        "transition_updates": "P8_Y5_R2FR_4359_TRANSITION_UPDATE_ROWS.csv",
        "theorems": "P8_Y5_R2FR_4359_THEOREM_ROWS.csv",
        "arenas": "P8_Y5_R2FR_4359_ARENA_ROWS.csv",
        "runner": "P8_Y5_R2FR_4359_RUNNER.csv",
        "firewall": "P8_Y5_R2FR_4359_CLAIM_FIREWALL.csv",
        "decision": "P8_Y5_R2FR_4359_DECISION.csv",
        "status": "P8_Y5_R2FR_4359_STATUS.csv",
        "next": "P8_Y5_R2FR_4359_NEXT_TARGET.csv",
    }
    for key, filename in mapping.items():
        write_csv(SOURCE_DIR / filename, tables[key])


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 375 PPC4161 transition tau-min lower bound or action-measure zero proof

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4359 does not prove public local GR, Newton, WEP, R10, PPN, clock, orbital, EM, or transition-shell safety.

## Result

4359 tries to turn the 4358 `tau_min` target into a theorem.

The useful lower-bound route is:

```text
tau_WEP = N_eta^-1 <K_CMSM, V_ST>,
V_ST := S_Earth x M_TiPt.
```

If:

```text
||K_CMSM|| >= k_min,
||S_Earth|| >= s_min,
||M_TiPt|| >= m_min,
|cos(theta)| >= c_min > 0,
N_eta <= N_max,
```

then:

```text
|tau_WEP| >= tau_min,
tau_min := k_min*s_min*m_min*c_min/N_max.
```

So the WEP product anchor would become:

```text
abs(Delta_w_TiPt) <= 2.8e-15/tau_min.
```

The important obstruction is now explicit:

```text
nonzero K_CMSM and nonzero V_ST do not imply <K_CMSM,V_ST> != 0.
```

`V_ST` can lie in `ker(K_CMSM)`, or signed orbit/readout pieces can cancel. Therefore a tau-min proof needs an alignment/non-null lower bound `c_min>0`, not merely nonzero source/readout/material rows.

The clean zero route is also imported:

```text
AX4359 owner/no-w_A package
=> Delta_w_TiPt = 0.
```

But AX4359 is a candidate target, not a derived parent theorem. No claim fires.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Tau Lower Bound Rows

{md_table(tables["tau_lower"], ["tau_id", "statement", "definitions", "result", "status", "valid_for_claim"])}

## Null Counterexample Rows

{md_table(tables["null_counterexamples"], ["counterexample_id", "model", "result", "blocks", "required_to_defeat", "valid_for_claim"])}

## Nondegeneracy Input Rows

{md_table(tables["nondegeneracy"], ["input_id", "needed_input", "why_needed", "source_or_derivation", "current_status", "priority", "valid_for_claim"])}

## Owner Axiom Rows

{md_table(tables["owner_axiom"], ["axiom_id", "candidate", "would_forbid", "effect_if_derived", "current_status", "valid_for_claim"])}

## WEP Acquisition Pack

{md_table(tables["acquisition_pack"], ["pack_id", "artifact", "content", "current_status", "next_route", "valid_for_claim"])}

## Transition Update Rows

{md_table(tables["transition_updates"], ["update_id", "4358_state", "4359_update", "effect", "valid_for_claim"])}

## Theorem Rows

{md_table(tables["theorems"], ["theorem_id", "statement", "derivation", "consequence", "status", "claim_allowed", "valid_for_claim"])}

## Arena Rows

{md_table(tables["arenas"], ["arena_id", "arena", "observable", "4359_requirement", "zero_route", "finite_route", "claim_allowed", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "input", "action", "result", "current_result", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "rule", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    post = f"""# 4359 Y5-R2FR transition tau-min lower bound or action-measure zero proof

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4359 derives the precise finite-route target:

```text
tau_min = k_min*s_min*m_min*c_min/N_max.
```

The killer detail is `c_min`: nonzero readout/source/material factors are not enough, because the source-material vector can sit in the readout kernel.

So the route is now:

```text
official readout/source/material data -> c_min>0 -> tau_min>0 -> Delta_w bound
```

or:

```text
parent owner/no-w_A theorem -> Delta_w=0.
```

No claim yet.

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        csv.writer(handle).writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4359 derives the tau-min lower-bound fork for transition source-label hair. If the branch-locked MICROSCOPE readout functional, Earth source vector and Ti/Pt material vector have lower norm bounds k_min, s_min and m_min, if their readout alignment satisfies |cos(theta)|>=c_min>0, and if N_eta<=N_max, then |tau_WEP|>=tau_min=k_min*s_min*m_min*c_min/N_max. Combined with the MICROSCOPE product bound this gives abs(Delta_w_TiPt)<=2.8e-15/tau_min. The checkpoint also proves the null-space obstruction: nonzero factors alone do not prove tau_WEP!=0 because the source-material vector can lie in ker(K_CMSM) or signed orbit/readout terms can cancel. The action-measure/no-w_A owner axiom package is imported as a clean zero target, but remains candidate/unsigned. No WEP, local-GR, Newton, PPN, R10, clock, orbital or public claim fires."
                ),
                (
                    "4359 source register, tau lower-bound rows, null-counterexample rows, nondegeneracy input rows, owner-axiom rows, WEP acquisition pack, transition update rows, theorem rows, arena rows, runner, firewall, decision, status, next-target and validation CSV."
                ),
                "tau_min_alignment_condition_derived_null_countermodel_blocks_claim_owner_axiom_unsigned_nonclaim",
                (
                    "Import/source official MICROSCOPE readout/source/material objects or prove parent nondegeneracy c_min>0; alternatively derive the owner/no-w_A theorem."
                ),
                (
                    "Inferring tau_min from nonzero factors alone; using positivity before signed readout convention; treating owner axioms as derived; scoring WEP/local GR from product bound only; using surrogate-only readout matrices for a claim."
                ),
            ]
        )


def append_spine_and_packet() -> None:
    spine_block = f"""

## PPC4161 4359 transition tau-min non-null alignment gate

Marker: `{MARKER}`

4359 derives the exact tau-min sufficient condition:

```text
tau_min = k_min*s_min*m_min*c_min/N_max.
```

The new nontrivial object is `c_min>0`, an alignment/non-null lower bound excluding `V_ST in ker(K_CMSM)`. Nonzero readout/source/material norms alone do not prove `tau_WEP != 0`.

The clean zero route is the owner/no-`w_A` axiom package, imported as a target but not a claim. Next target: official MICROSCOPE readout/source/material import or parent nondegeneracy.
"""
    packet_block = f"""

## PPC4161 packet update 4359 tau-min alignment gate

Marker: `{PACKET_MARKER}`

Packet update: the finite WEP route now needs a sourced non-null alignment bound `c_min>0`, not just nonzero factors. The zero route remains the unsigned owner/no-`w_A` theorem.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    checks: List[Tuple[str, bool, str]] = []
    formal_text = read_text(FORMAL_PATH)
    checks.append(("formal_doc_written", FORMAL_PATH.exists(), str(FORMAL_PATH)))
    checks.append(("post_doc_written", DOC_PATH.exists(), str(DOC_PATH)))
    checks.append(("marker_in_formal", MARKER in formal_text, MARKER))
    checks.append(("decision_in_formal", DECISION in formal_text, DECISION))
    checks.append(("tau_min_formula_present", "tau_min := k_min*s_min*m_min*c_min/N_max" in formal_text, "tau_min formula"))
    checks.append(("nonzero_not_enough_present", "nonzero K_CMSM and nonzero V_ST do not imply" in formal_text, "nonzero shortcut rejection"))
    checks.append(("kernel_countermodel_present", "ker(K_CMSM)" in formal_text, "kernel countermodel"))
    checks.append(("owner_axiom_present", "AX4359 owner/no-w_A package" in formal_text, "owner axiom"))
    checks.append(("next_target_present", NEXT_TARGET in formal_text, NEXT_TARGET))
    checks.append(("all_sources_exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source paths"))
    checks.append(("all_needles_found", all(row["needle_found"] == "True" for row in tables["sources"]), "source needles"))
    checks.append(("tau_rows_present", len(tables["tau_lower"]) >= 4, str(len(tables["tau_lower"]))))
    checks.append(("null_rows_present", len(tables["null_counterexamples"]) >= 3, str(len(tables["null_counterexamples"]))))
    checks.append(("nondegeneracy_rows_present", len(tables["nondegeneracy"]) >= 5, str(len(tables["nondegeneracy"]))))
    checks.append(("owner_axiom_rows_present", len(tables["owner_axiom"]) >= 5, str(len(tables["owner_axiom"]))))
    checks.append(("acquisition_pack_present", len(tables["acquisition_pack"]) >= 6, str(len(tables["acquisition_pack"]))))
    checks.append(("theorem_rows_present", len(tables["theorems"]) >= 4, str(len(tables["theorems"]))))
    checks.append(("arena_rows_present", len(tables["arenas"]) == len(ARENAS), str(len(tables["arenas"]))))
    checks.append(("no_valid_claim_rows", all(row.get("valid_for_claim") == "False" for rows in tables.values() for row in rows if "valid_for_claim" in row), "all generated claim flags false"))
    checks.append(("claim_row_recorded", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID))
    checks.append(("spine_marker_recorded", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER))
    checks.append(("packet_marker_recorded", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER))
    for filename in [
        "P8_Y5_R2FR_4359_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4359_TAU_LOWER_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4359_NULL_COUNTEREXAMPLE_ROWS.csv",
        "P8_Y5_R2FR_4359_NONDEGENERACY_INPUT_ROWS.csv",
        "P8_Y5_R2FR_4359_OWNER_AXIOM_ROWS.csv",
        "P8_Y5_R2FR_4359_WEP_ACQUISITION_PACK.csv",
        "P8_Y5_R2FR_4359_TRANSITION_UPDATE_ROWS.csv",
        "P8_Y5_R2FR_4359_THEOREM_ROWS.csv",
        "P8_Y5_R2FR_4359_ARENA_ROWS.csv",
        "P8_Y5_R2FR_4359_RUNNER.csv",
        "P8_Y5_R2FR_4359_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4359_DECISION.csv",
        "P8_Y5_R2FR_4359_STATUS.csv",
        "P8_Y5_R2FR_4359_NEXT_TARGET.csv",
    ]:
        path = SOURCE_DIR / filename
        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8"))) if path.exists() else []
        checks.append((f"csv_{filename}_parse_rows", bool(rows), f"{len(rows)} rows"))
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": str(bool(passed)),
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    tables = build_tables()
    write_tables(tables)
    write_docs(tables)
    append_claim_once()
    append_spine_and_packet()
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    failures = [row for row in validation_rows if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 14 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation_rows)} failed={len(failures)}")
    if failures:
        for row in failures:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
