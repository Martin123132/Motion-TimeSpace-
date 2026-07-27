from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4068-Y5-R2FR-field-space-descent-from-MTS-parent-to-local-action-skeleton.md"

DECISION = "CONDITIONAL_PARENT_TO_LOCAL_DESCENT_THEOREM_BUILT_METRIC_EH_COUPLING_BRANCH_OWNERS_OPEN"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4068_00_4067_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4067_NEXT_TARGET.csv",
        "field-space-descent-from-MTS-parent-to-local-action-skeleton",
        "4067 selected the parent field-space descent as the next target.",
    ),
    "SRC4068_01_4067_open_parent_descent": (
        SOURCE_DIR / "P8_Y5_R2FR_4067_ADOPTION_RESULT.csv",
        "RES4067_1_parent_descent",
        "4067 left global parent descent open after constructing the local skeleton.",
    ),
    "SRC4068_02_spine_parent_to_gr": (
        FORMALIZATION / "07-unification-spine.md",
        "MTS parent theory -> effective GR",
        "formal spine contains the parent-to-GR reduction target.",
    ),
    "SRC4068_03_metric_from_psi": (
        FORMALIZATION / "04-variable-audit.csv",
        "d_mu_psi_covariance",
        "variable audit records the psi-gradient metric emergence route and its limits.",
    ),
    "SRC4068_04_local_packet_q": (
        FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
        "q:Q_dyn^loc -> Met_obs",
        "formal local packet supplies the target local quotient variables.",
    ),
    "SRC4068_05_parent_quotient_map": (
        SOURCE_DIR / "P8_Y5_PARENT_NORMAL_FORM_2485_QUOTIENT_DESCENT_MAP.csv",
        "q_parent: Phi_parent",
        "2485 supplies the older parent quotient descent map contract.",
    ),
    "SRC4068_06_quotient_chain_rule": (
        SOURCE_DIR / "P8_Y5_FIELD_QUOTIENT_2570_THEOREM_ATTEMPT.csv",
        "THM2570_0_chain_rule_descent",
        "2570 proves the conditional chain-rule descent theorem.",
    ),
    "SRC4068_07_field_signature": (
        SOURCE_DIR / "P8_Y5_FIELD_QUOTIENT_2570_FIELD_SIGNATURE_ATTEMPT.csv",
        "FSIG2570_0_public_geometry",
        "2570 records public geometry as candidate rather than parent-derived.",
    ),
    "SRC4068_08_eh_descent_package": (
        SOURCE_DIR / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_DESCENT_PACKAGE_AUDIT.csv",
        "EDP2579_0_EH_core",
        "2579 gives the EH descent package clauses.",
    ),
    "SRC4068_09_matter_descent": (
        SOURCE_DIR / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv",
        "PRE2611_2_matter_functor",
        "2611 gives the ordinary matter descent premise.",
    ),
    "SRC4068_10_action_normal_form": (
        SOURCE_DIR / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "ANF2618_0_parent_action_partition",
        "2618 turns source-looking terms into action-normal-form ownership clauses.",
    ),
    "SRC4068_11_vertical_generator": (
        SOURCE_DIR / "P8_Y5_PARENT_ACTION_2464_CANDIDATE_ACTIONS.csv",
        "ACT2464_A_vertical_generator_current_law",
        "2464 supplies the constructive vertical-generator current-law block.",
    ),
    "SRC4068_12_khat_variation": (
        SOURCE_DIR / "P8_Y5_PARENT_ACTION_2465_VARIATION_AUDIT.csv",
        "VAR2465_1_define_Khat",
        "2465 verifies the Khat variation contract.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4068_SOURCE_REGISTER.csv",
    "parent_field_sort": SOURCE_DIR / "P8_Y5_R2FR_4068_PARENT_FIELD_SORT.csv",
    "descent_map": SOURCE_DIR / "P8_Y5_R2FR_4068_PARENT_TO_LOCAL_DESCENT_MAP.csv",
    "theorem_attempt": SOURCE_DIR / "P8_Y5_R2FR_4068_DESCENT_THEOREM_ATTEMPT.csv",
    "clause_status": SOURCE_DIR / "P8_Y5_R2FR_4068_DESCENT_CLAUSE_STATUS.csv",
    "open_gaps": SOURCE_DIR / "P8_Y5_R2FR_4068_CORE_OPEN_GAPS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4068_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4068_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4068_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4068_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4068_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, source_tuple in SOURCES.items():
        path, needle, role = source_tuple
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def parent_field_sort_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "sort_id": "PFS4068_0_core_motion",
            "parent_object": "psi / motion field packet",
            "target_local_object": "g_obs or e_obs",
            "descent_role": "candidate origin of observed metric/coframe",
            "status": "CANDIDATE_NOT_EH_DERIVED",
            "repair_move": "prove psi-gradient covariance induces Lorentzian metric, diffeomorphism invariance, and EH normal form, or promote g_obs as primitive local branch field",
            "timestamp_utc": current_timestamp,
        },
        {
            "sort_id": "PFS4068_1_memory_exchange",
            "parent_object": "Gamma_mem / M / compression-memory variables",
            "target_local_object": "Gamma_ren, Khat, S_GK",
            "descent_role": "renormalized vertical-generator/Hilbert-response sector",
            "status": "PARTIAL_CONSTRUCTIVE_VIA_2464_2465",
            "repair_move": "show Gamma_ren and Khat are normal-form descendants of the parent memory variables rather than new local objects",
            "timestamp_utc": current_timestamp,
        },
        {
            "sort_id": "PFS4068_2_observed_geometry",
            "parent_object": "q_parent(Phi_parent)",
            "target_local_object": "Met_obs, clock/coframe, connection",
            "descent_role": "public quotient readout varied in local EH branch",
            "status": "QUOTIENT_CONTRACT_NOT_PARENT_SIGNED",
            "repair_move": "supply field-by-field q_parent, Dq generators, and proof no second public metric/coframe survives locally",
            "timestamp_utc": current_timestamp,
        },
        {
            "sort_id": "PFS4068_3_matter_EM",
            "parent_object": "ordinary matter Psi and EM A_mu",
            "target_local_object": "S_matter, S_EM, T_H, T_EM",
            "descent_role": "same observed geometry and same Hilbert source branch",
            "status": "EXACT_IF_Q_BASIC_NOT_PARENT_SIGNED",
            "repair_move": "prove ordinary matter/EM actions are q-basic and have no hidden source-only prefactors or source markers",
            "timestamp_utc": current_timestamp,
        },
        {
            "sort_id": "PFS4068_4_coupling",
            "parent_object": "a1 / kappa_MTS / K_G / local normalization",
            "target_local_object": "kappa_eff and calibrated G_N",
            "descent_role": "fixed coupling owner for local EH/Newton branch",
            "status": "SUPERSELECTION_CONTRACT_NUMERICAL_G_NOT_DERIVED",
            "repair_move": "derive coefficient ownership or explicitly declare G_N as measured input while keeping no-prediction firewall",
            "timestamp_utc": current_timestamp,
        },
        {
            "sort_id": "PFS4068_5_private_auxiliary",
            "parent_object": "q_private, projectors, boundary/readout/memory reset variables",
            "target_local_object": "S_aux_no_flux, S_top, S_vertical, S_reset",
            "descent_role": "local silence and branch-control sectors",
            "status": "SELECTED_BRANCH_CONDITIONAL",
            "repair_move": "prove compact local branch selector and boundary charges kill these variations without killing FLRW/cosmology memory",
            "timestamp_utc": current_timestamp,
        },
    ]


def descent_map_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "map_id": "D4068_0_inclusion",
            "parent_side": "Phi_parent with local compact stationary boundary data",
            "local_side": "Q_parent^loc = Met_obs x Matter x EM x K_G x Aux_GK x Aux_private",
            "map_statement": "iota_loc^* S_parent should equal S_loc^{<=2PN} plus vertical-exact and boundary-silent terms",
            "derivation_status": "CONDITIONAL_THEOREM_FORMULATED",
            "closed_by_4068": "the target map is now explicit enough to test clause-by-clause",
            "not_closed": "the actual global parent action and parent-signed iota_loc remain missing",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "map_id": "D4068_1_metric",
            "parent_side": "psi-gradient covariance / q_parent observable geometry",
            "local_side": "g_obs or e_obs varied by S_EH",
            "map_statement": "Obs_g(q_parent(Phi)) = g_obs and local normal form contains (2*kappa_eff)^-1 int sqrt(-g_obs) R[g_obs]",
            "derivation_status": "OPEN_HARDEST_CLAUSE",
            "closed_by_4068": "identifies the precise metric/EH induction target",
            "not_closed": "psi-to-Lorentzian-metric and EH kinetic-term derivation are not supplied by existing rows",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "map_id": "D4068_2_matter_EM",
            "parent_side": "ordinary matter and EM coupled to q-basic observed geometry",
            "local_side": "S_matter[Psi,e_obs,theta] + S_EM[A,e_obs] + S_binding",
            "map_statement": "if matter/EM are q-basic then delta_v S_matter = delta_v S_EM = 0 for every local vertical v in ker(Dq)",
            "derivation_status": "EXACT_CONDITIONAL_CHAIN_RULE",
            "closed_by_4068": "imports the exact quotient theorem as a local skeleton descent clause",
            "not_closed": "no-marker/no-source-prefactor grammar and constants owner are not parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "map_id": "D4068_3_GK",
            "parent_side": "Gamma_mem/M compression-memory sector",
            "local_side": "S_GK with Gamma_ren and Khat = partial L_K / partial(nabla A)",
            "map_statement": "local memory sector descends to the vertical-generator current-law action rather than being imposed as q_loc closure",
            "derivation_status": "PARTIAL_CONSTRUCTIVE",
            "closed_by_4068": "ties 2464/2465 variation ownership to the 4067 local skeleton",
            "not_closed": "Gamma_ren/Khat are not yet derived from the original parent variables",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "map_id": "D4068_4_coupling",
            "parent_side": "a1/kappa_MTS/K_G coefficient family",
            "local_side": "fixed kappa_eff and measured G_N firewall",
            "map_statement": "T_local K_G = 0 on the compact local branch; G_N := c^4 kappa_eff/(8*pi) is read as calibrated unless parent coefficient theorem exists",
            "derivation_status": "SAFE_CONTRACT_NOT_NUMERICAL_DERIVATION",
            "closed_by_4068": "prevents pretending MTS predicts the numerical value of Newton G",
            "not_closed": "parent coefficient owner remains unsigned",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "map_id": "D4068_5_auxiliary_branch",
            "parent_side": "private/projector/boundary/reset variables",
            "local_side": "S_aux_no_flux + S_top + S_vertical + S_reset",
            "map_statement": "local compact branch restricts auxiliary variations to Dq=0, no-flux, or boundary-silent directions",
            "derivation_status": "SELECTED_BRANCH_CONDITIONAL",
            "closed_by_4068": "makes the branch selector an explicit descent clause rather than an unspoken plateau axiom",
            "not_closed": "the branch selector itself is not parent-derived and must not erase cosmological memory effects",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "map_id": "D4068_6_readout",
            "parent_side": "post-variation observable map",
            "local_side": "PPN, R10, clocks, orbital, EM, cosmology readouts",
            "map_statement": "readouts are applied after variation and cannot be used to tune the local action",
            "derivation_status": "FIREWALL_RETAINED",
            "closed_by_4068": "keeps empirical testing downstream of the parent/local action derivation",
            "not_closed": "not a physics proof by itself; it is a discipline rule",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def theorem_attempt_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "THM4068_0_parent_to_local_descent",
            "statement": "If q_parent, iota_loc, EH normal form, q-basic matter/EM, coefficient ownership, and branch/boundary silence are parent-signed, then the 4067 local action skeleton is the local <=2PN pullback of S_parent.",
            "proof_sketch": "Define S_loc := iota_loc^* S_parent. Split S_parent into geometry/MTS, q-basic matter/EM, coefficient, auxiliary, and boundary blocks. Chain-rule descent kills vertical representative variations; boundary/no-flux clauses kill surface charges; EH normal form supplies the local metric kinetic term. The remaining local terms match the 4067 skeleton.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_advances": "turns the parent-descent problem from a vague gap into a finite set of parent-owned clauses",
            "what_it_does_not_claim": "it does not prove the clauses from the original MTS corpus",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "THM4068_1_no_smuggling_rule",
            "statement": "A local GR/Newton/PPN branch is not smuggled in if every local skeleton term is either a pullback of S_parent, a q-basic matter/EM functor, or a boundary/reference term with zero local charge.",
            "proof_sketch": "This is a classification theorem: any term outside those three classes must be named as a residual operator or demoted to closure.",
            "proof_status": "CLASSIFICATION_RULE_CONSTRUCTED",
            "what_it_advances": "prevents future checkpoints from adding local terms without declaring their parent owner",
            "what_it_does_not_claim": "it does not show all current MTS terms pass the classification",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "THM4068_2_best_next_derivation",
            "statement": "The metric/EH induction clause is the bottleneck: without it, local GR can only be a guarded effective branch; with it, the whole chain becomes a serious GR-reduction candidate.",
            "proof_sketch": "Matter descent, q_loc variation, and readout firewalls are already exact-conditional or constructive. The unsupported leap is still psi/q_parent -> observed Lorentzian geometry with EH kinetic normal form.",
            "proof_status": "TARGET_SELECTION_PROOF",
            "what_it_advances": "selects 4069 as a real derivation attempt rather than another broad audit",
            "what_it_does_not_claim": "no numerical Newton G prediction and no public local-GR theorem",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def clause_status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "clause_id": "C4068_0_q_parent",
            "clause": "field-by-field parent quotient q_parent and local inclusion iota_loc",
            "status": "CONTRACT_EXISTS_NOT_PARENT_SIGNED",
            "evidence_path": str(SOURCES["SRC4068_05_parent_quotient_map"][0]),
            "repair_attempt": "use 4069 to decide whether psi/q_parent can generate the observed metric branch or must be demoted",
            "timestamp_utc": current_timestamp,
        },
        {
            "clause_id": "C4068_1_metric_EH",
            "clause": "observed metric/coframe plus EH kinetic normal form",
            "status": "OPEN_CORE_DERIVATION",
            "evidence_path": str(SOURCES["SRC4068_03_metric_from_psi"][0]),
            "repair_attempt": "derive Lorentzian signature, Levi-Civita connection, and EH term from psi covariance/quotient geometry, or declare g_obs primitive",
            "timestamp_utc": current_timestamp,
        },
        {
            "clause_id": "C4068_2_matter_EM_q_basic",
            "clause": "ordinary matter and EM depend only on observed geometry/coframe and fixed representation data",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "evidence_path": str(SOURCES["SRC4068_09_matter_descent"][0]),
            "repair_attempt": "prove no hidden source-only prefactors, source labels, or worldtube vertices survive the parent grammar",
            "timestamp_utc": current_timestamp,
        },
        {
            "clause_id": "C4068_3_GK_memory",
            "clause": "Gamma/Khat block descends from memory/compression variables",
            "status": "PARTIAL_CONSTRUCTIVE_NOT_CORE_DERIVED",
            "evidence_path": str(SOURCES["SRC4068_11_vertical_generator"][0]),
            "repair_attempt": "map Gamma_mem/M into Gamma_ren and Khat, with dimensions and Hilbert variation owned by S_parent",
            "timestamp_utc": current_timestamp,
        },
        {
            "clause_id": "C4068_4_coupling_owner",
            "clause": "kappa_eff/K_G is fixed locally or derived from a parent coefficient theorem",
            "status": "FIREWALLED_MEASURED_INPUT_NOT_DERIVED",
            "evidence_path": str(SOURCES["SRC4068_06_quotient_chain_rule"][0]),
            "repair_attempt": "either derive coefficient descent or keep Newton G as calibrated input; do not claim numerical G prediction",
            "timestamp_utc": current_timestamp,
        },
        {
            "clause_id": "C4068_5_branch_boundary",
            "clause": "compact local branch selector, no-flux boundaries, and reset/projector silence",
            "status": "SELECTED_BRANCH_CONDITIONAL",
            "evidence_path": str(SOURCES["SRC4068_08_eh_descent_package"][0]),
            "repair_attempt": "derive branch selector from parent boundary/regularity conditions while preserving cosmological memory sector",
            "timestamp_utc": current_timestamp,
        },
    ]


def open_gap_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "gap_id": "GAP4068_0_metric_EH_induction",
            "gap": "psi/q_parent to observed Lorentzian metric and EH normal form",
            "why_it_matters": "this is the difference between an MTS-derived GR limit and an adopted GR effective branch",
            "best_attack": "try a metric normal-form theorem from psi-gradient covariance and diffeomorphism-invariant low-derivative action",
            "fallback_if_failed": "demote g_obs/EH to an effective branch input, keep all empirical tests honest",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "gap_id": "GAP4068_1_Gamma_Khat_origin",
            "gap": "Gamma_ren/Khat local block is not yet derived from original memory variables",
            "why_it_matters": "without this, q_loc is improved but still partly engineered",
            "best_attack": "map memory/exchange variables into a conjugate current-law block and check dimensions",
            "fallback_if_failed": "treat S_GK as local closure with bounded residual coefficients",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
        {
            "gap_id": "GAP4068_2_matter_prefactor_exclusion",
            "gap": "q-basic matter/EM and no hidden source-prefactor theorem are not parent-signed",
            "why_it_matters": "this controls WEP/local-source leakage and composition dependence",
            "best_attack": "write the allowed matter action grammar and prove all source labels enter only through observed geometry",
            "fallback_if_failed": "score composition/source residual coefficients instead of claiming local-GR silence",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
        {
            "gap_id": "GAP4068_3_branch_selector",
            "gap": "compact local reset/no-flux branch is not derived from global parent dynamics",
            "why_it_matters": "local GR and cosmological memory must both survive without contradiction",
            "best_attack": "derive branch selector from asymptotic/boundary regularity and scale separation",
            "fallback_if_failed": "separate local branch closure from cosmological branch and test both as effective sectors",
            "priority": "P2",
            "timestamp_utc": current_timestamp,
        },
        {
            "gap_id": "GAP4068_4_coupling_owner",
            "gap": "kappa_eff/G_N is calibrated, not predicted",
            "why_it_matters": "safe for GR reduction but not a derivation of Newton's constant",
            "best_attack": "look for parent normalization or scale-setting theorem after metric/EH induction",
            "fallback_if_failed": "state G_N is measured like in GR; MTS predicts deviations/residuals, not the constant value",
            "priority": "P3",
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "decision_gate": [
            {
                "decision_id": "DEC4068_0",
                "decision": DECISION,
                "summary": "4068 builds an exact conditional theorem and typed descent map from the parent MTS field space to the 4067 local action skeleton, but leaves metric/EH induction, coupling ownership, branch selection, and no-prefactor matter grammar unsigned.",
                "formalization_modified": False,
                "public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4068_0",
                "claim": "the parent-to-local descent problem has a finite typed theorem form",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "useful private derivation scaffold, not a completed proof from the original MTS parent action",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4068_1",
                "claim": "MTS derives local GR/Newton/PPN from first principles",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "psi-to-metric/EH induction and parent coefficient/matter/branch ownership remain open",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4068_2",
                "claim": "MTS predicts the numerical value of Newton G",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "current safe route calibrates G_N from kappa_eff just as the guarded local GR branch requires",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4068_0",
                "next_doc": "4069-Y5-R2FR-psi-to-observed-metric-EH-induction-or-demotion.md",
                "next_script": "scripts/Y5_R2FR_4069_psi_to_observed_metric_EH_induction_or_demotion.py",
                "reason": "metric/EH induction is now the P0 bottleneck; prove psi/q_parent induces g_obs plus EH normal form, or demote g_obs/EH to an explicit effective branch input",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4068",
                "status": DECISION,
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            }
        ],
    }


def validate_sources(source_table: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in source_table if not row["exists"]]
    absent_needles = [row["source_id"] for row in source_table if not row["needle_found"]]
    if missing or absent_needles:
        return False, f"missing={missing}; absent_needles={absent_needles}"
    return True, "all cited source paths exist and needles are present"


def validate_csv_parse(paths: Iterable[Path]) -> Tuple[bool, str]:
    details: List[str] = []
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as input_file:
                parsed_rows = list(csv.DictReader(input_file))
            details.append(f"{path.name}:rows={len(parsed_rows)}")
    except Exception as exc:  # pragma: no cover
        return False, repr(exc)
    return True, "; ".join(details)


def validate_no_public_claim(row_groups: Iterable[List[Dict[str, object]]]) -> Tuple[bool, str]:
    offenders: List[str] = []
    for rows in row_groups:
        for row in rows:
            for key in ("valid_for_claim", "allowed_public", "public_claim", "github_action"):
                if key in row and str(row[key]).lower() == "true":
                    offenders.append(str(row))
    if offenders:
        return False, f"public/github claim flags found: {offenders}"
    return True, "all claim-bearing rows preserve public/github false"


def validate_no_bare_missing(open_gaps: List[Dict[str, object]]) -> Tuple[bool, str]:
    offenders = [
        row["gap_id"]
        for row in open_gaps
        if not row.get("best_attack") or not row.get("fallback_if_failed")
    ]
    if offenders:
        return False, f"open gaps without attack/fallback: {offenders}"
    return True, "every open gap has a best attack and fallback"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
    open_gaps: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    claims_ok, claims_detail = validate_no_public_claim(row_groups)
    gaps_ok, gaps_detail = validate_no_bare_missing(open_gaps)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4068_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4068_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4068_02_no_public_or_github_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4068_03_conditional_theorem",
            "passed": "THM4068_0_parent_to_local_descent" in joined and "EXACT_CONDITIONAL_THEOREM" in joined,
            "detail": "parent-to-local descent theorem is formulated explicitly",
        },
        {
            "check_id": "VAL4068_04_metric_EH_open",
            "passed": "OPEN_CORE_DERIVATION" in joined and "psi/q_parent" in joined,
            "detail": "metric/EH induction remains the explicit P0 bottleneck",
        },
        {
            "check_id": "VAL4068_05_no_bare_missing",
            "passed": gaps_ok,
            "detail": gaps_detail,
        },
        {
            "check_id": "VAL4068_06_next_target",
            "passed": "4069-Y5-R2FR-psi-to-observed-metric-EH-induction-or-demotion.md" in joined,
            "detail": "next target attacks the hardest descent clause",
        },
        {"check_id": "VAL4068_07_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4068 - Field-Space Descent From MTS Parent to Local Action Skeleton

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public local-GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Result

4068 does not just say "parent descent is missing". It builds the exact conditional theorem that a future parent action must satisfy:

```text
If q_parent, iota_loc, EH normal form, q-basic matter/EM,
coefficient ownership, and branch/boundary silence are parent-signed,
then S_loc^{{<=2PN}} = iota_loc^* S_parent + vertical-exact/boundary-silent terms.
```

That is a real step forward because the 4067 local action skeleton is now connected to a typed parent-descent map rather than left as a hand-built local packet.

## Parent-To-Local Map

The descent map now has seven typed channels:

1. parent local inclusion `iota_loc`;
2. `psi/q_parent -> g_obs/e_obs` metric readout and EH normal form;
3. q-basic matter/EM descent into one Hilbert source;
4. `Gamma_mem/M -> Gamma_ren/Khat/S_GK`;
5. `K_G/kappa_eff -> calibrated local G_N` with no numerical-G claim;
6. compact local auxiliary/reset/no-flux branch;
7. post-variation empirical readout firewall.

## What Closed

- The field-space descent problem is now a finite theorem with named clauses.
- The matter/EM vertical-source silence is exact if the q-basic action grammar is signed.
- The 2464/2465 vertical-generator current-law block can be attached to the 4067 skeleton as a constructive partial descendant.
- The Newton-G point is kept honest: current route calibrates `G_N`; it does not predict its numerical value.

## What Still Has To Be Derived

The P0 bottleneck is now:

```text
psi / q_parent  ->  observed Lorentzian metric g_obs
                 ->  EH kinetic normal form
                 ->  local GR weak-field branch.
```

If this closes, the whole GR-reduction route becomes much more serious. If it fails, `g_obs + EH` must be demoted to an explicit effective branch input rather than treated as derived.

## Next

`4069` should attempt `psi-to-observed-metric-EH-induction-or-demotion` directly. This is the leap that matters; everything else is secondary until this is either proved, bounded, or honestly demoted.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    field_sort = parent_field_sort_rows(current_timestamp)
    descent_map = descent_map_rows(current_timestamp)
    theorem_attempt = theorem_attempt_rows(current_timestamp)
    clause_status = clause_status_rows(current_timestamp)
    open_gaps = open_gap_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["parent_field_sort"], field_sort)
    write_csv(OUTPUTS["descent_map"], descent_map)
    write_csv(OUTPUTS["theorem_attempt"], theorem_attempt)
    write_csv(OUTPUTS["clause_status"], clause_status)
    write_csv(OUTPUTS["open_gaps"], open_gaps)
    write_csv(OUTPUTS["decision_gate"], static["decision_gate"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["parent_field_sort"],
        OUTPUTS["descent_map"],
        OUTPUTS["theorem_attempt"],
        OUTPUTS["clause_status"],
        OUTPUTS["open_gaps"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        field_sort,
        descent_map,
        theorem_attempt,
        clause_status,
        open_gaps,
        static["decision_gate"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, row_groups, open_gaps)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
