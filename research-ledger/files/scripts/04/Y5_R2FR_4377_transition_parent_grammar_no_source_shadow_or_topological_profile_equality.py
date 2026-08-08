from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4377"
CLAIM_ID = "L-218"
MARKER = "PPC4161_TRANSITION_PARENT_GRAMMAR_NO_SOURCE_SHADOW_OR_TOPOLOGICAL_PROFILE_EQUALITY_4377"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_PARENT_GRAMMAR_NO_SOURCE_SHADOW_OR_TOPOLOGICAL_PROFILE_EQUALITY_4377"
DECISION = "PARENT_GRAMMAR_NO_SOURCE_SHADOW_PRIVATE_PACKET_CONDITIONAL_TOPOLOGICAL_PROFILE_EQUALITY_REDUCED_TO_MOMENT_GATE_NONCLAIM"
NEXT_TARGET = "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"

FORMAL_PATH = FORMAL / "393-PPC4161-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md"
DOC_PATH = POST / "4377-Y5-R2FR-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4377_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4377_00_4376_formal": (
        FORMAL / "392-PPC4161-transition-source-shadow-ban-or-Eprofile-first-source-density-row.md",
        "parent grammar/no-source-shadow or distributional Hilbert/topological profile equality",
        "4376 selects the parent grammar or distributional profile equality fork.",
    ),
    "SRC4377_01_4376_grammar": (
        SOURCE_DIR / "P8_Y5_R2FR_4376_GRAMMAR_CLAUSES.csv",
        "GR4376_2_no_source_only_functional",
        "4376 identifies the no source-only functional clause.",
    ),
    "SRC4377_02_4376_noether": (
        SOURCE_DIR / "P8_Y5_R2FR_4376_NOETHER_EXCHANGE_TEST.csv",
        "NET4376_1_source_shadow_bypass",
        "Noether exchange cannot kill a source-shadow bypass by itself.",
    ),
    "SRC4377_03_hsrc_grammar": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "S_src != sum_A w_A S_A",
        "185 contains the private packet Hilbert source-measure grammar with no independent source weights.",
    ),
    "SRC4377_04_hsrc_Hilbert": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "T_H^munu = -2/sqrt(-g_obs) delta S_src/delta g_obs_munu.",
        "185 defines the Hilbert source stress from the same local source action.",
    ),
    "SRC4377_05_visible_contract": (
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "T_H = -2/sqrt(-g_obs) delta S_vis/delta g_obs.",
        "4210 imports standard visible matter through Hilbert stress.",
    ),
    "SRC4377_06_domain_theorem": (
        SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
        "ODT2659_1_exact_typed_theorem",
        "operator-domain theorem gives the typed route to no hidden/source-label slots.",
    ),
    "SRC4377_07_domain_matrix": (
        SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_PROOF_REDUCTION_MATRIX.csv",
        "RED2659_1_functor_domain",
        "ordinary matter functor domain must exclude hidden current slots.",
    ),
    "SRC4377_08_owner_no_wA": (
        FORMAL / "377-PPC4161-transition-owner-no-wA-theorem-or-explicit-source-coupling-closure.md",
        "single parent action-density line",
        "4361 assembles the single-action/no-wA grammar route.",
    ),
    "SRC4377_09_hamiltonian_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "It is the Hamiltonian/Hilbert charge map of the same source current and same worldtube.",
        "186 ties Pi_M to the Hamiltonian/Hilbert charge map of the same source current.",
    ),
    "SRC4377_10_same_object": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "Same-Object Glue",
        "186 distinguishes same-charge glue from a post-readout topological mask.",
    ),
    "SRC4377_11_newton_density": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "int_W rho_H dV = M_H^dress[W_H;tau].",
        "187 gives the integrated Hilbert source mass used by Poisson/Gauss readout.",
    ),
    "SRC4377_12_selector_topology": (
        SOURCE_DIR / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv",
        "WSC2577_4_R_eq_zero_lemma",
        "2577 names the same Hilbert/topological source class route and its unsigned premises.",
    ),
    "SRC4377_13_charge_current": (
        SOURCE_DIR / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "CC3_projected_mass_current",
        "charge-current equality requires projected Hilbert mass current before readout.",
    ),
    "SRC4377_14_charge_status": (
        SOURCE_DIR / "P8_charge_current_equality_STATUS.csv",
        "charge-current equality parent-derived,fail",
        "existing charge-current equality is not parent-derived.",
    ),
    "SRC4377_15_boundary_topological": (
        FORMAL / "143-boundary-topological-backup-gate.md",
        "bulk metric-nullity passes formally, but is insufficient.",
        "earlier boundary/topological backup warns that metric-nullity alone is not local profile safety.",
    ),
    "SRC4377_16_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "visible EM/Poynting energy is Hilbert stress or boundary flux, not a new source density.",
    ),
    "SRC4377_17_transition_monopole": (
        FORMAL / "305-PPC4161-transition-monopole-absorption-or-residual-profile-gate.md",
        "Only `q_tr^Hilbert-monopole` is absorbable.",
        "transition/profile work already separated absorbable monopole from residual multipoles.",
    ),
}


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


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


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
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


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


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
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


def parent_grammar_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "PG4377_0_typed_source_object",
            "claim_piece": "ordinary-source grammar object",
            "formal_statement": "OrdSrc(P,W_H) has source density functor rho_H(P)=Hilb_00(S_src[g_obs,fields,theta_fixed])/c^2 on W_H.",
            "derivation_result": "DEFINITION_CONSTRUCTED",
            "effect_if_signed": "the source density is selected by action variation, not by an independent source-profile rule",
            "current_blocker": "the grammar must be parent-adopted for the whole local branch, not only written as a private packet selector",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PG4377_1_no_source_shadow_type_error",
            "claim_piece": "no source-only functional/current slot",
            "formal_statement": "If AllowedBulkSource(P,W_H)=im Hilb_00(S_src) and no SourceOnly->Dens(W_H) morphism exists, then rho_shadow is not a well-typed parent source object.",
            "derivation_result": "EXACT_CONDITIONAL_THEOREM",
            "effect_if_signed": "rho_eff=rho_H and the source-shadow part of E_profile is zero",
            "current_blocker": "no-source-shadow grammar is conditional; non-Hilbert currents and topological representatives still need profile-silence clauses",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PG4377_2_private_Hsrc_signature",
            "claim_piece": "private packet support",
            "formal_statement": "PPC4161-TK-H writes S_src with one Hilbert source measure and explicitly excludes independent weights: S_src != sum_A w_A S_A.",
            "derivation_result": "PRIVATE_PACKET_SIGNATURE_PRESENT",
            "effect_if_signed": "inside that selector, D_A w_B=0 because no w_B object exists",
            "current_blocker": "private packet adoption does not prove global MTS parent adoption or every rest/topological profile clause",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PG4377_3_rest_top_zero_clause",
            "claim_piece": "topological/rest sector profile silence",
            "formal_statement": "S_rest^top/zero is harmless for E_profile only if delta_g S_rest=0 as a bulk distribution and any boundary flux has zero local profile projection.",
            "derivation_result": "NECESSARY_CLAUSE_DERIVED",
            "effect_if_signed": "rest/topological terms cannot re-enter as rho_top_profile",
            "current_blocker": "metric-nullity or closed charge alone is insufficient; distributional profile equality is still required",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PG4377_4_no_readout_reentry",
            "claim_piece": "variation before readout",
            "formal_statement": "The grammar survives observables only if support, worldtube, Pi_M and source profile are fixed before exterior/orbital readout.",
            "derivation_result": "READOUT_FIREWALL_FORMALIZED",
            "effect_if_signed": "post-readout profile selectors cannot manufacture sigma_shadow",
            "current_blocker": "Pi_M/Hamiltonian and readout-frame ownership are still conditional in the broader corpus",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PG4377_5_current_verdict",
            "claim_piece": "parent grammar no-source-shadow theorem",
            "formal_statement": "Parent-adopted OrdSrc(P,W_H)=Hilb_00(S_src)/c^2 plus no non-Hilbert/topological/readout profile slot implies rho_shadow=0.",
            "derivation_result": "CONDITIONAL_THEOREM_PRIVATE_PACKET_READY_NOT_GLOBAL",
            "effect_if_signed": "source-shadow branch of E_profile closes",
            "current_blocker": "topological/profile equality and broader parent adoption remain unsigned; no local-GR claim fires",
            "valid_for_claim": "False",
        },
    ]


def topological_profile_equality_rows() -> List[Dict[str, str]]:
    return [
        {
            "topology_id": "TPE4377_0_define_profile_defect",
            "object": "topological/Hamiltonian profile defect",
            "formal_statement": "delta rho_top := rho_top - rho_H on the same W_H, with int_W delta rho_top dV_H=0 if the total charge matches.",
            "status": "SETUP_EXACT",
            "what_is_new": "separates monopole charge equality from local density-profile equality",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "topology_id": "TPE4377_1_monopole_not_enough",
            "object": "charge equality",
            "formal_statement": "int_W delta rho_top dV_H=0 is only the f=1 test function; it does not imply delta rho_top=0.",
            "status": "COUNTERMODEL_RETAINED",
            "what_is_new": "formalizes why same M_Hdress or same linking charge cannot prove E_profile=0",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "topology_id": "TPE4377_2_distributional_equality",
            "object": "profile equality as distribution",
            "formal_statement": "rho_top=rho_H as distributions iff for every f in C_c^infty(W_H), int_W f(y) delta rho_top(y) dV_H=0.",
            "status": "EXACT_TEST_FUNCTION_GATE",
            "what_is_new": "turns the vague topological equality requirement into a precise infinite test-function gate",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "topology_id": "TPE4377_3_moment_hierarchy",
            "object": "compact-source moment gate",
            "formal_statement": "For compact ordinary profiles, the zero-monopole exterior defect is controlled by all l>=1 moments M_lm^top-H := int_W delta rho_top r^l Y_lm dV_H.",
            "status": "MOMENT_GATE_DERIVED",
            "what_is_new": "the topological wrong-distribution branch becomes a multipole/profile row rather than a slogan",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "topology_id": "TPE4377_4_exterior_transfer",
            "object": "topological profile Green transfer",
            "formal_statement": "deltaPhi_top(x)=-G_cal int_W delta rho_top(y)/|x-y| dV_y; with zero monopole, the leading exterior terms are l>=1 moments.",
            "status": "GREEN_TRANSFER_IMPORTED_AND_REFINED",
            "what_is_new": "connects distributional profile failure directly to Newton/local residual scoring",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "topology_id": "TPE4377_5_current_verdict",
            "object": "topological profile equality",
            "formal_statement": "Current corpus supports same-charge/same-worldtube glue but not all-test-function or all-moment equality of rho_top and rho_H.",
            "status": "NOT_PROVED_MOMENT_GATE_REQUIRED",
            "what_is_new": "next work is a concrete moment-zero proof or first multipole bound, not another total-charge check",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def test_function_moment_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "MOM4377_0_test_function_all",
            "quantity": "distributional profile defect",
            "definition": "Delta_f := int_W f(y)(rho_top-rho_H)(y)dV_H for all compact test functions f",
            "zero_condition": "Delta_f=0 for every f",
            "current_status": "FORMULA_READY_NOT_PROVED",
            "fallback_bound": "choose finite basis/moment rows and bound the remaining profile norm",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "MOM4377_1_monopole",
            "quantity": "M_00^top-H",
            "definition": "M_00^top-H := int_W delta rho_top dV_H",
            "zero_condition": "same integrated Hamiltonian/topological/Hilbert charge",
            "current_status": "CONDITIONAL_MONOPOLE_ONLY",
            "fallback_bound": "not enough for E_profile; proceed to l>=1",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "MOM4377_2_dipole",
            "quantity": "M_1m^top-H",
            "definition": "M_1m^top-H := int_W delta rho_top r Y_1m dV_H",
            "zero_condition": "same center/profile owner or symmetry plus no readout shift",
            "current_status": "MISSING_ZERO_OR_SOURCE_BOUND",
            "fallback_bound": "include dipole acceleration residual in deltaPhi_top",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "MOM4377_3_quadrupole_and_higher",
            "quantity": "M_lm^top-H for l>=2",
            "definition": "M_lm^top-H := int_W delta rho_top r^l Y_lm dV_H",
            "zero_condition": "distributional equality or complete profile/moment hierarchy",
            "current_status": "MISSING_ZERO_OR_SOURCE_BOUND",
            "fallback_bound": "multipole sum or coarse K_N E_top_profile bound",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "MOM4377_4_coarse_norm",
            "quantity": "E_top_profile",
            "definition": "E_top_profile := ||(rho_top-rho_H)_perp/rho_H||_inf",
            "zero_condition": "rho_top=rho_H as distributions on W_H",
            "current_status": "BOUND_SCHEMA_READY_VALUE_MISSING",
            "fallback_bound": "|deltaa_top|/|a_N| <= K_N(s) E_top_profile",
            "valid_for_claim": "False",
        },
    ]


def eprofile_update_rows() -> List[Dict[str, str]]:
    return [
        {
            "update_id": "EPU4377_0_source_shadow",
            "component": "E_shadow",
            "new_status": "ZERO_INSIDE_PARENT_ADOPTED_HILBERT_GRAMMAR_ONLY",
            "formula": "no SourceOnly->Dens(W_H) slot => rho_shadow=0",
            "claim_effect": "not claim-grade globally",
            "valid_for_claim": "False",
        },
        {
            "update_id": "EPU4377_1_topological_profile",
            "component": "E_top_profile",
            "new_status": "MOMENT_GATE_REQUIRED",
            "formula": "rho_top=rho_H iff int f(rho_top-rho_H)dV=0 for all f; equivalently all profile moments vanish under compact regularity assumptions",
            "claim_effect": "topological charge equality remains insufficient",
            "valid_for_claim": "False",
        },
        {
            "update_id": "EPU4377_2_nonHilbert_rest",
            "component": "E_nonHilbert_profile",
            "new_status": "RETAINED_AS_PROFILE_SILENCE_CLAUSE",
            "formula": "delta_g S_rest^top/zero=0 as a bulk distribution and boundary projection silent",
            "claim_effect": "must be proved before top/rest sectors are harmless",
            "valid_for_claim": "False",
        },
        {
            "update_id": "EPU4377_3_profile_envelope",
            "component": "E_profile",
            "new_status": "REFINED_NO_CANCELLATION_ENVELOPE",
            "formula": "E_profile <= E_shadow + E_top_profile + E_nonHilbert_profile + E_readout_profile",
            "claim_effect": "source-shadow grammar can zero only the first component; topological/profile components remain",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4377_0_parent_grammar_shadow_zero",
            "claim_tested": "E_shadow=0",
            "required_inputs": "parent-adopted ordinary-source grammar with Hilb_00 as the only bulk source-density functor and no source-only/non-Hilbert/readout slot",
            "status": "PRIVATE_PACKET_CONDITIONAL_NOT_GLOBAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4377_1_topological_distributional_equality",
            "claim_tested": "E_top_profile=0",
            "required_inputs": "all-test-function equality int f(rho_top-rho_H)dV=0 or complete moment/profile equality on W_H",
            "status": "BLOCKED_MOMENT_GATE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4377_2_Eprofile_zero",
            "claim_tested": "E_profile=0",
            "required_inputs": "E_shadow, E_top_profile, E_nonHilbert_profile and E_readout_profile all zero on the same branch",
            "status": "BLOCKED_TOPOLOGICAL_AND_REST_PROFILE_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4377_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "full E_profile plus remaining E_mass/E_measure/E_transition/E_Xi/E_T and local projection gates closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4377_0",
            "decision": DECISION,
            "summary": (
                "4377 constructs the parent grammar theorem in its cleanest form: if the parent-adopted ordinary-source object has only the Hilbert T00 density functor and no source-only, non-Hilbert, hidden-Hom, or readout source slot, then a source-shadow density is ill-typed and E_shadow=0. "
                "The private H_src packet already has this shape, but that is not a global MTS/local-GR claim because topological/rest sectors and readout equality still need profile silence. "
                "The topological branch is reduced to an exact distributional gate: same total charge is only the monopole test, while local profile equality requires all compact test functions or all moments to vanish. "
                "The next target is therefore a moment-zero proof or first topological multipole/profile bound."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "it attacks the remaining topological wrong-distribution component directly rather than circling through total charge or Noether arguments.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4377_0_parent_grammar",
            "object": "no source-shadow parent grammar",
            "status": "EXACT_CONDITIONAL_THEOREM_PRIVATE_PACKET_READY",
            "note": "source-shadow is ill-typed if Hilbert T00 is the only allowed bulk source-density functor.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4377_1_Hsrc",
            "object": "private H_src packet",
            "status": "SUPPORTS_GRAMMAR_ROUTE",
            "note": "185 explicitly excludes independent source weights inside the private packet.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4377_2_topological",
            "object": "topological profile equality",
            "status": "REDUCED_TO_TEST_FUNCTION_MOMENT_GATE",
            "note": "same charge/monopole is insufficient; all zero-monopole profile moments or distributional equality are required.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4377_3_Eprofile",
            "object": "E_profile envelope",
            "status": "REFINED",
            "note": "E_profile splits into E_shadow, E_top_profile, E_nonHilbert_profile and E_readout_profile.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4377_4_next",
            "object": "next derivation",
            "status": "TOPOLOGICAL_MOMENT_ZERO_OR_FIRST_BOUND_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4377_0",
            "target": NEXT_TARGET,
            "question": "Can the topological/Hamiltonian representative be proved profile-equal to Hilbert T00 by killing every zero-monopole moment, or must the first M_lm/E_top bound row be filled?",
            "preferred_route": "derive that S_rest^top/zero and Pi_M/H_tau differ from Hilbert T00 only by an exact boundary term with zero bulk profile and zero local projection, so all l>=1 moments vanish.",
            "fallback_route": "instantiate the first nonclaim topological multipole/profile row, starting with dipole/quadrupole or coarse E_top_profile, and score it through Green/K_N.",
            "avoid": "claiming profile equality from integrated mass, same topological class, closed current, or metric-null topological action alone.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    grammar: List[Dict[str, str]],
    topology: List[Dict[str, str]],
    moments: List[Dict[str, str]],
    updates: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: parent grammar no-source-shadow or topological profile equality

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4377 takes the leap that 4376 set up.

The source-shadow ban has a clean theorem form:

```text
AllowedBulkSource(P,W_H) = im Hilb_00(S_src[g_obs,fields,theta_fixed])
and no SourceOnly -> Dens(W_H) morphism exists
=> rho_shadow is not a well-typed parent source object
=> E_shadow=0.
```

The private `H_src` packet already has the right shape:

```text
S_src != sum_A w_A S_A,
D_A w_B = 0 only because no w_B exists.
```

That is real progress, but not a public local-GR claim. The remaining danger is not ordinary source-shadow notation anymore; it is topological/rest/profile reentry.

The topological branch is now forced through a distributional gate:

```text
delta rho_top := rho_top-rho_H,
int_W delta rho_top dV_H = 0       # only monopole / same total charge

rho_top=rho_H as profiles
iff
int_W f(y) delta rho_top(y) dV_H = 0 for every compact test function f.
```

Equivalently, for compact regular profiles, all zero-monopole moments must vanish:

```text
M_lm^top-H := int_W delta rho_top r^l Y_lm dV_H = 0 for all l>=1,m.
```

If not, the retained profile defect is physical:

```text
deltaPhi_top(x)=-G_cal int_W delta rho_top(y)/|x-y| dV_y,
|deltaa_top|/|a_N| <= K_N(s) E_top_profile.
```

So 4377 does not end the local route. It converts the last vague "topological wrong-distribution" escape into a concrete moment/profile proof or bound.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Parent Grammar Theorem

{md_table(grammar, ["theorem_id", "claim_piece", "formal_statement", "derivation_result", "effect_if_signed", "current_blocker"])}

## Topological Profile Equality

{md_table(topology, ["topology_id", "object", "formal_statement", "status", "what_is_new"])}

## Test-Function / Moment Gate

{md_table(moments, ["gate_id", "quantity", "definition", "zero_condition", "current_status", "fallback_bound"])}

## E_profile Update Rows

{md_table(updates, ["update_id", "component", "new_status", "formula", "claim_effect"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4377: parent grammar no-source-shadow or topological profile equality

Marker: `{MARKER}`

## What changed

- Built the exact typed parent-grammar theorem: no source-density object exists except Hilbert `T_H(n,n)/c^2`.
- Imported `H_src` as private packet support, while keeping global/local-GR claim gates false.
- Reduced topological wrong-distribution equality to test functions and multipole/profile moments.
- Refined `E_profile` into `E_shadow + E_top_profile + E_nonHilbert_profile + E_readout_profile`.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4377 Transition parent grammar or topological profile equality

Marker: `{MARKER}`

4377 constructs the typed no-source-shadow theorem:

```text
AllowedBulkSource(P,W_H)=im Hilb_00(S_src)
+ no SourceOnly -> Dens(W_H)
=> rho_shadow is ill-typed
=> E_shadow=0.
```

The private `H_src` packet supports this route, but local GR is still not claimed because topological/rest/profile reentry remains. Same total charge is only the monopole condition:

```text
int_W (rho_top-rho_H)dV_H=0.
```

Profile equality requires the distributional gate:

```text
int_W f(rho_top-rho_H)dV_H=0 for every compact test function f,
```

or equivalently all non-monopole compact profile moments vanish. The next target is the moment-zero proof or first topological multipole/profile bound.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4377 packet update: source-shadow grammar sharpened, topology becomes moment gate

Marker: `{PACKET_MARKER}`

Packet update: ordinary source-shadow is now an exact typed-grammar problem. In a parent-adopted Hilbert source grammar, a separate `rho_shadow` is not a legal bulk source object. The private `H_src` selector has this form, but the packet still carries the topological/rest profile defect because same charge is only a monopole statement. The remaining profile equality gate is distributional: all compact test functions, or all non-monopole moments, must vanish before `E_profile=0` can be claimed.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4377 constructs the exact typed parent-grammar theorem for the source-shadow leg: if the parent-adopted ordinary source object has only the Hilbert T00 density functor and no source-only, non-Hilbert, hidden-Hom or readout source slot, then rho_shadow is ill-typed and E_shadow=0. "
                "The private H_src packet supports this route but does not make a global local-GR claim. The topological wrong-distribution branch is reduced to a distributional/moment gate: same total charge is only the monopole test, while profile equality requires int f(rho_top-rho_H)dV=0 for every compact test function or all l>=1 profile moments to vanish. "
                "No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4377 source register, parent grammar theorem rows, topological profile equality rows, test-function/moment gate, E_profile update rows, claim gates, decision, status, next target and validation CSV.",
            "parent_grammar_no_source_shadow_private_packet_conditional_topological_profile_moment_gate_nonclaim",
            "Prove topological/Hilbert distributional profile equality by killing all non-monopole moments, or fill the first topological multipole/profile bound row.",
            "Claiming profile equality from integrated mass, same topological class, closed current, metric-null topological action, or Noether exchange alone.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4377_SOURCE_REGISTER.csv")
    grammar = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4377_PARENT_GRAMMAR_THEOREM.csv")
    topology = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4377_TOPOLOGICAL_PROFILE_EQUALITY.csv")
    moments = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4377_TEST_FUNCTION_MOMENT_GATE.csv")
    updates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4377_EPROFILE_UPDATE_ROWS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4377_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4377_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4377_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4377_2_parent_grammar_theorem",
        any(row["theorem_id"] == "PG4377_1_no_source_shadow_type_error" and "not a well-typed parent source object" in row["formal_statement"] for row in grammar),
        "typed no-source-shadow theorem row exists",
    )
    add(
        "VAL4377_3_private_Hsrc_support",
        any(row["theorem_id"] == "PG4377_2_private_Hsrc_signature" and row["derivation_result"] == "PRIVATE_PACKET_SIGNATURE_PRESENT" for row in grammar),
        "private H_src support is recorded without promotion",
    )
    add(
        "VAL4377_4_distributional_gate",
        any(row["topology_id"] == "TPE4377_2_distributional_equality" and "every f" in row["formal_statement"] for row in topology),
        "distributional all-test-function gate exists",
    )
    add(
        "VAL4377_5_moment_gate",
        any(row["gate_id"] == "MOM4377_2_dipole" for row in moments)
        and any(row["gate_id"] == "MOM4377_3_quadrupole_and_higher" for row in moments),
        "non-monopole moment rows exist",
    )
    add(
        "VAL4377_6_Eprofile_refined",
        any(row["component"] == "E_profile" and "E_shadow" in row["formula"] and "E_top_profile" in row["formula"] for row in updates),
        "E_profile refined no-cancellation envelope exists",
    )
    add("VAL4377_7_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4377_8_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4377_9_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4377_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4377_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4377_12_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4377_13_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4377_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    return validations


def main() -> None:
    sources = source_register_rows()
    grammar = parent_grammar_theorem_rows()
    topology = topological_profile_equality_rows()
    moments = test_function_moment_gate_rows()
    updates = eprofile_update_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4377_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4377_PARENT_GRAMMAR_THEOREM.csv": grammar,
        "P8_Y5_R2FR_4377_TOPOLOGICAL_PROFILE_EQUALITY.csv": topology,
        "P8_Y5_R2FR_4377_TEST_FUNCTION_MOMENT_GATE.csv": moments,
        "P8_Y5_R2FR_4377_EPROFILE_UPDATE_ROWS.csv": updates,
        "P8_Y5_R2FR_4377_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4377_DECISION.csv": decisions,
        "P8_Y5_R2FR_4377_STATUS.csv": statuses,
        "P8_Y5_R2FR_4377_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, grammar, topology, moments, updates, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
