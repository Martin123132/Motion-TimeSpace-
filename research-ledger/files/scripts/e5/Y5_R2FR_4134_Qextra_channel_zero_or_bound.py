from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4134-Y5-R2FR-Qextra-channel-zero-or-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_QEXTRA_CHANNEL_ZERO_OR_BOUND_4134"
CHECKPOINT_ID = "4134"
DECISION = "QEXTRA_REDUCED_TO_SURVIVOR_OPERATOR_BOUNDARY_FLUX_REMAINDER"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4134_00_4133_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4133_NEXT_TARGET.csv",
        "4134-Y5-R2FR-Qextra-channel-zero-or-bound.md",
        "4133 selected channelwise Q_extra zero-or-bound.",
    ),
    "SRC4134_01_4133_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4133_STATUS.csv",
        "PARENT_JH_ORIGIN_UNSIGNED_QEXTRA_VECTOR_FILLED",
        "4133 parent-origin and Qextra status.",
    ),
    "SRC4134_02_4133_qextra": (
        SOURCE_DIR / "P8_Y5_R2FR_4133_QEXTRA_CHANNEL_VECTOR.csv",
        "Q_radiative_Poynting",
        "Current finite Qextra channel vector.",
    ),
    "SRC4134_03_4133_origin": (
        SOURCE_DIR / "P8_Y5_R2FR_4133_PARENT_JH_ORIGIN_GATE.csv",
        "NO_NONHILBERT_BYPASS",
        "Parent Hilbert-current origin clauses.",
    ),
    "SRC4134_04_3576_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_3576_CANDIDATE_PARENT_BRANCH_ADOPTION_PACKET.csv",
        "ADOPT3576_3_PiM_identity",
        "Candidate branch PiM identity and constant-kappa packet.",
    ),
    "SRC4134_05_3579_no_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_3579_NO_FLUX_CONDITIONS.csv",
        "NFC3579_6_local_exterior_clause",
        "Stationary local EM/Poynting no-flux conditions.",
    ),
    "SRC4134_06_3776_source": (
        SOURCE_DIR / "P8_Y5_R2FR_3776_TOTAL_HILBERT_SOURCE_INCLUSION_THEOREM.csv",
        "THI3776_4_interior_monopole_reclassification",
        "Total Hilbert source inclusion and EM/Poynting reclassification.",
    ),
    "SRC4134_07_3999_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_3999_FLUX_CLOSURE_THEOREM.csv",
        "FCT3999_3_flux_closure_theorem",
        "Hilbert mass flux closure theorem.",
    ),
    "SRC4134_08_4100_nonhilbert": (
        SOURCE_DIR / "P8_Y5_R2FR_4100_NONHILBERT_BYPASS_THEOREM.csv",
        "NHB4100_1_exact_dmu_improvement_zero",
        "Non-Hilbert bypass and exact improvement zero clauses.",
    ),
    "SRC4134_09_4021_witness": (
        SOURCE_DIR / "P8_Y5_R2FR_4021_PARENT_LOCAL_ACTION_WITNESS.csv",
        "WIT4021_2_no_extra_operators",
        "Sufficient local parent-action witness.",
    ),
    "SRC4134_10_4021_lemmas": (
        SOURCE_DIR / "P8_Y5_R2FR_4021_DERIVED_ZERO_LEMMAS.csv",
        "LEM4021_6_PPN_zero_vector_under_witness",
        "Derived local zero lemmas under the witness.",
    ),
    "SRC4134_11_4022_ops": (
        SOURCE_DIR / "P8_Y5_R2FR_4022_OPERATOR_CLASS_STRESS_TEST.csv",
        "OP4022_11_EM_Hodge_Poynting",
        "Operator-class stress test against the witness.",
    ),
    "SRC4134_12_4022_survivors": (
        SOURCE_DIR / "P8_Y5_R2FR_4022_SURVIVOR_PPN_ROUTE.csv",
        "SURV4022_10_Gamma_Khat_q_loc",
        "Survivor operators requiring score or excision.",
    ),
    "SRC4134_13_3970_channels": (
        SOURCE_DIR / "P8_Y5_R2FR_3970_EXTRA_MONOPOLE_CHANNEL_VECTOR.csv",
        "CH3970_2_bulk_memory_range",
        "Older extra-monopole channel ledger.",
    ),
    "SRC4134_14_3987_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_BOUND_ROWS.csv",
        "CEM3987_13_epsilon_nonEH_source",
        "Extra-monopole absolute bound rows.",
    ),
    "SRC4134_15_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4134_Qextra_channel_zero_or_bound.py",
        "Reproducible generator for this 4134 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def qextra_zero_theorem_rows() -> List[dict]:
    data = [
        (
            "QZT4134_0_split",
            "finite additive split",
            "Q_extra/Q_ref = sum_i epsilon_i",
            "4133/3970 turn extra source charge into channel projections; no cancellation credit is allowed.",
            "EXACT_SPLIT_IMPORTED",
        ),
        (
            "QZT4134_1_candidate_zero_theorem",
            "candidate branch zero theorem",
            "WIT4021 + ADOPT3576 + NFC3579 + boundary-silent exact terms + no survivor operators => Q_extra=0",
            "Under one observed Hilbert/coframe source action, constant K_G, Pi_M=Pi_M^H, total-system domain, and compact stationary no-flux exterior, each listed channel either reclassifies into M_H or has zero projection.",
            "DERIVED_CANDIDATE_THEOREM_NOT_CORPUS_ADOPTED",
        ),
        (
            "QZT4134_2_reduced_remainder",
            "post-zero-attempt remainder",
            "Q_extra/Q_ref -> R_survivor_ops + R_boundary_harmonic + R_undescended_support + R_unstationary_flux + R_parent_adoption",
            "The useful reduction is that PiM-stress, kappa drift, same-frame readout, exact symplectic improvement, and static Poynting pieces have explicit zero routes; the hard live terms are survivor operators and boundary/domain/flux clauses.",
            "REDUCED_REMAINDER_VECTOR",
        ),
        (
            "QZT4134_3_no_public_claim",
            "claim ceiling",
            "Q_extra=0 is not claimed until the parent action adopts the witness or all remainder rows are source-backed and below tolerance",
            "This avoids smuggling local GR by naming the exact branch where the theorem would be true.",
            "NO_LOCAL_GR_CLAIM",
        ),
    ]
    rows: List[dict] = []
    for theorem_id, claim_piece, formula, derivation, status in data:
        row = row_base()
        row.update(
            {
                "theorem_id": theorem_id,
                "claim_piece": claim_piece,
                "formula": formula,
                "derivation": derivation,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def channel_zero_matrix_rows() -> List[dict]:
    data = [
        (
            "CZM4134_0_symp",
            "Q_symp",
            "delta(i_tau mu)-i_tau(delta mu)=0 under fixed bundle, tau, surface, no-corner, and no-readout-dependence clauses",
            "exact improvements do not feed the Hamiltonian surface one-form",
            "CANDIDATE_ZERO_EXACT_IMPROVEMENT_BRANCH",
            "R_boundary_harmonic if corner/harmonic/reference dependence remains",
            "boundary; beta/gamma; xi",
        ),
        (
            "CZM4134_1_PiM",
            "Q_PiM_stress",
            "Pi_M:=Pi_M^H on the Hilbert mass-current complex => Pi_M J_H=J_H, [d,Pi_M]J_H=0, delta_g Pi_M has no independent stress",
            "3576 gives an internal candidate identity branch; 3999 then removes the projector-commutator contribution",
            "CANDIDATE_ZERO_PIM_IDENTITY_BRANCH",
            "R_projector_domain if Pi_M is not adopted as source-blind Hilbert identity",
            "PPN alpha_i/xi; beta/gamma; radial source hair",
        ),
        (
            "CZM4134_2_kappa",
            "Q_delta_kappa",
            "Q_parent^loc=Q_dyn^loc x K_G and local variations have no K_G component => D_X ln kappa_*=0 and delta_kappa_source=0",
            "4021 derives local G/kappa derivative silence; absolute G remains calibrated, not numerically predicted",
            "CANDIDATE_ZERO_KG_FACTOR_BRANCH",
            "R_product_lock if K_G factorization is rejected",
            "Gdot; WEP; PPN; common-G",
        ),
        (
            "CZM4134_3_frame",
            "Q_frame",
            "single observed tau/coframe/source frame fixed before clocks, orbit and PPN readout",
            "same generator and observed Hodge keep source charge, Poynting stress and readout in one frame",
            "CANDIDATE_ZERO_SAME_OBSERVED_BRANCH",
            "R_frame_species if hidden species/readout selector survives",
            "WEP; clock; preferred-frame PPN",
        ),
        (
            "CZM4134_4_radiative",
            "Q_radiative_Poynting",
            "stationary compact source-free exterior plus no net Poynting/radiation/current crossing gives int_A J_rad/Poynting=0",
            "static EM/Poynting stress is included inside T_H; only crossing flux is an extra source",
            "STATIONARY_COMPACT_BRANCH_ZERO_IF_NO_FLUX",
            "R_unstationary_flux if radiative/background leakage crosses the linking surface",
            "clock/orbit flux; Gdot; source hair",
        ),
        (
            "CZM4134_5_domain",
            "Q_domain",
            "total-system domain includes material body, EM field support, binding, apparatus and interaction support",
            "3776 reclassifies included EM/Poynting/binding/apparatus monopoles into M_H,total instead of Q_extra",
            "CONDITIONAL_RECLASSIFICATION_TO_MH_TOTAL",
            "R_undescended_support for any sector not descended through q_obs or not included in the domain",
            "WEP; Newton GM; R10; beta",
        ),
        (
            "CZM4134_6_boundary",
            "Q_boundary_leak",
            "exact boundary/reference difference has zero compact flux if fixed before readout and no harmonic/corner remainder exists",
            "3576 signs the exact wrong-object piece only; harmonic/corner/worldtube reference still needs proof or bound",
            "PARTIAL_ZERO_EXACT_BOUNDARY_ONLY",
            "R_boundary_harmonic",
            "alpha3; xi; beta; Gdot",
        ),
        (
            "CZM4134_7_nonEH",
            "Q_nonEH",
            "non-EH <=2PN operators must be exact, topological, vertical-only, auxiliary double-zero, or explicitly scored",
            "4022 leaves R2/fR, Ricci/Weyl, scalar-tensor, vector, torsion/nonmetricity, bulk_X, nonlocal memory and GK/q_loc as survivor classes",
            "NOT_ZERO_UNTIL_SURVIVOR_OPERATORS_EXCISED_OR_BOUNDED",
            "R_survivor_ops",
            "PPN; R10 alpha(lambda); WEP; clocks",
        ),
        (
            "CZM4134_8_memory",
            "Q_memory",
            "local compact branch must make memory kernel vertical/source-silent/double-zero or give a norm bound",
            "nonlocal memory remains a 4022 survivor and cannot be killed by stationary language alone",
            "LIVE_SURVIVOR_MEMORY_KERNEL",
            "R_memory_kernel",
            "alpha3; Gdot; R10",
        ),
        (
            "CZM4134_9_range",
            "Q_range",
            "finite-range/direct-force tails must be excluded by EH-only local branch or bounded by alpha(lambda)/PPN maps",
            "bulk_X and GK/q_loc routes remain finite-range/source-exchange survivors",
            "LIVE_SURVIVOR_RANGE_TAIL",
            "R_range_tail",
            "R10; beta/gamma; radial source hair",
        ),
    ]
    rows: List[dict] = []
    for channel_id, symbol, candidate_zero_formula, proof_route, verdict, live_remainder, arena in data:
        row = row_base()
        row.update(
            {
                "channel_id": channel_id,
                "symbol": symbol,
                "candidate_zero_formula": candidate_zero_formula,
                "proof_route": proof_route,
                "verdict": verdict,
                "live_remainder_if_unsigned": live_remainder,
                "arena_projection": arena,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def candidate_zero_ledger_rows() -> List[dict]:
    data = [
        (
            "CZL4134_0_closed_candidate",
            "candidate-zero set",
            "Q_symp + Q_PiM_stress + Q_delta_kappa + Q_frame",
            "0 inside WIT4021/ADOPT3576 local branch",
            "PRIVATE_CANDIDATE_ZERO_NOT_PUBLIC_CLAIM",
        ),
        (
            "CZL4134_1_reclassified",
            "reclassified into Hilbert mass",
            "EM/Poynting static stress + binding + apparatus + interaction support",
            "included in M_H,total when one descended total source action and total-system domain are adopted",
            "RECLASSIFIED_NOT_DELETED",
        ),
        (
            "CZL4134_2_flux_zero",
            "stationary crossing flux",
            "int_A J_rad/Poynting + J_source_crossing",
            "0 for compact stationary local exterior with no current/radiation crossing",
            "CONDITIONAL_STATIC_ZERO",
        ),
        (
            "CZL4134_3_exact_boundary",
            "exact boundary improvement",
            "int_boundary dB_exact",
            "0 for fixed reference/exact term with no harmonic/corner/readout dependence",
            "PARTIAL_ZERO_REMAINDER_RETAINED",
        ),
    ]
    rows: List[dict] = []
    for ledger_id, group, terms, zero_value, status in data:
        row = row_base()
        row.update(
            {
                "ledger_id": ledger_id,
                "group": group,
                "terms": terms,
                "candidate_zero_or_reclassification": zero_value,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def live_bound_rows() -> List[dict]:
    data = [
        (
            "LBR4134_0_master",
            "epsilon_Qextra_4134",
            "R_survivor_ops + R_boundary_harmonic + R_undescended_support + R_unstationary_flux + R_parent_adoption",
            "dimensionless",
            "local GR/Newton source denominator",
            "Q_extra_over_Q_ref after candidate zeros/reclassifications",
            "NONCLAIM_REDUCED_MASTER_BOUND",
        ),
        (
            "LBR4134_1_survivor_ops",
            "R_survivor_ops",
            "sum_abs(R2/fR, Ricci/Weyl, scalar-tensor, vector, torsion/nonmetricity, bulk_X, nonlocal_memory, GK/q_loc)",
            "dimensionless or mapped coefficient norms",
            "PPN + R10 + clocks + WEP",
            "operator-family coefficient, weak-field projection, mass/range, source charge and source path",
            "LIVE_PRIMARY_BOUND_TARGET",
        ),
        (
            "LBR4134_2_memory",
            "R_memory_kernel",
            "||K_mem^loc|| * ||source_support|| / |Q_ref|",
            "dimensionless",
            "alpha3 + Gdot + R10",
            "local memory kernel norm, support radius, projection to monopole",
            "LIVE_SURVIVOR_COMPONENT",
        ),
        (
            "LBR4134_3_range",
            "R_range_tail",
            "sum_X |alpha_X(lambda_X)| + |q_X/Q_ref| over finite-range/direct-force survivors",
            "dimensionless alpha(lambda) plus source-charge norm",
            "R10 + PPN + radial source hair",
            "lambda_X, alpha_X, source charge, arena tolerance",
            "LIVE_SURVIVOR_COMPONENT",
        ),
        (
            "LBR4134_4_boundary",
            "R_boundary_harmonic",
            "abs(Q_boundary_harmonic + Q_corner + Q_worldtube_reference)/abs(Q_ref)",
            "dimensionless",
            "alpha3 + xi + beta + Gdot",
            "harmonic/corner/reference coefficient and compact-boundary proof or numeric bound",
            "LIVE_BOUNDARY_COMPONENT",
        ),
        (
            "LBR4134_5_domain",
            "R_undescended_support",
            "abs(Q_sector_not_in_Ssrc_or_domain)/abs(Q_ref)",
            "dimensionless",
            "WEP + Newton GM + R10 + beta",
            "sector action, q_obs descent flag, domain-support integral",
            "LIVE_DOMAIN_COMPONENT",
        ),
        (
            "LBR4134_6_flux",
            "R_unstationary_flux",
            "abs(int_A (J_rad/Poynting + J_source_crossing))/abs(Q_ref)",
            "dimensionless flux ratio",
            "clock/orbit flux + Gdot + source hair",
            "stationarity flag, Poynting/radiation flux integral, current-crossing integral",
            "LIVE_FLUX_COMPONENT",
        ),
        (
            "LBR4134_7_parent",
            "R_parent_adoption",
            "1 - Z_WIT4021_ADOPTED",
            "boolean guard",
            "claim governance",
            "actual MTS parent corpus adoption or every rejected clause numerically scored",
            "NON_NUMERIC_CLAIM_GUARD",
        ),
    ]
    rows: List[dict] = []
    for bound_id, symbol, formula, units, arena, inputs, status in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "arena_projection": arena,
                "required_inputs": inputs,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DG4134_0_real_progress",
            "CANDIDATE_ZERO_ROUTES_FOUND",
            "PiM-stress, kappa drift, same-frame readout, exact symplectic improvement, static Poynting crossing and total-domain EM/binding pieces now have explicit zero/reclassification routes.",
            "do not keep treating every Qextra term as equally unknown",
        ),
        (
            "DG4134_1_not_closed",
            "QEXTRA_ZERO_NOT_CLAIMED",
            "The proof is conditional on WIT4021/ADOPT3576 and stationary no-flux clauses; the actual parent corpus has not adopted all of them.",
            "keep local GR source-denominator claim blocked",
        ),
        (
            "DG4134_2_hard_remainder",
            "SURVIVOR_OPERATOR_BOUNDARY_FLUX_REMAINDER",
            "The live technical work is now survivor operators, boundary harmonic/corner/reference terms, undescended domain support, and unstationary flux.",
            "target survivor-operator excision or score rows next",
        ),
        (
            "DG4134_3_G_policy",
            "G_DECIMAL_NOT_REQUIRED_BUT_DRIFT_MUST_ZERO",
            "Like GR, the measured value of G may be calibrated; what must be derived for MTS is no source/range/time/species/frame drift of the local coupling product.",
            "use K_G factorization route; retain Gdot/WEP/PPN bounds if rejected",
        ),
        (
            "DG4134_4_next",
            "NEXT_SURVIVOR_OPERATOR_EXCISION_SELECTED",
            "The least hand-wavy next route is to excise or score the survivor operator classes that feed Q_nonEH/Q_memory/Q_range.",
            "4135-Y5-R2FR-survivor-operator-excision-or-bound-map.md",
        ),
    ]
    rows: List[dict] = []
    for gate_id, decision, rationale, next_action in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "decision": decision,
                "rationale": rationale,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4134_0",
            "result": DECISION,
            "summary": (
                "4134 performs the requested channelwise Q_extra zero attempt. It finds real conditional zeros: "
                "PiM-stress, kappa drift, same-frame readout, exact symplectic improvement, static Poynting flux, "
                "and total-domain EM/binding terms can vanish or reclassify inside the WIT4021/ADOPT3576 stationary "
                "local branch. It still does not claim Q_extra=0 because survivor non-EH/memory/range operators, "
                "boundary harmonic/corner/reference terms, undescended support, and parent-adoption guard remain."
            ),
            "candidate_zero_routes_found": "True",
            "Q_extra_zero_signed": "False",
            "reduced_remainder_vector_filled": "True",
            "bound_rows_filled": "True",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass",
            "next_target": "4135 survivor operator excision or bound map",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4134_0",
            "target_doc": "4135-Y5-R2FR-survivor-operator-excision-or-bound-map.md",
            "target_script": "scripts/Y5_R2FR_4135_survivor_operator_excision_or_bound_map.py",
            "objective": (
                "take the reduced Qextra remainder and try to excise survivor operator classes from the local "
                "2PN branch: R2/fR, Ricci/Weyl, scalar-tensor, vector preferred-frame, torsion/nonmetricity, "
                "bulk_X, nonlocal memory, and Gamma/Khat/q_loc; if not excisable, produce source-backed PPN/R10/WEP/clock bound rows"
            ),
            "success_gate": "each survivor operator is either forbidden by the parent local action witness/double-zero/topological route, or has explicit coefficient, units, source path, weak-field projection and arena tolerance",
            "reason": "4134 made the Qextra zero attempt productive: the remaining nontrivial obstruction is the survivor-operator remainder plus boundary/domain/flux edge terms.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4134_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4134_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4134_QEXTRA_ZERO_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4134_QEXTRA_ZERO_THEOREM.csv",
        "P8_Y5_R2FR_4134_CHANNEL_ZERO_MATRIX": SOURCE_DIR / "P8_Y5_R2FR_4134_CHANNEL_ZERO_MATRIX.csv",
        "P8_Y5_R2FR_4134_CANDIDATE_ZERO_LEDGER": SOURCE_DIR / "P8_Y5_R2FR_4134_CANDIDATE_ZERO_LEDGER.csv",
        "P8_Y5_R2FR_4134_LIVE_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4134_LIVE_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4134_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4134_DECISION_GATES.csv",
        "P8_Y5_R2FR_4134_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4134_STATUS.csv",
        "P8_Y5_R2FR_4134_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4134_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4134 - Qextra Channel Zero or Bound",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- This is a real zero-proof attempt: several `Q_extra` channels now have explicit candidate zero or reclassification routes.",
        "- The full `Q_extra=0` proof is not signed because survivor operators and boundary/domain/flux edge terms remain.",
        "- No Newton/local-GR/PPN/R10 pass is claimed.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Zero Theorem", "", "| claim piece | status | formula |", "|---|---|---|"])
    for row in qextra_zero_theorem_rows():
        sections.append(f"| {row['claim_piece']} | {row['status']} | {row['formula']} |")
    sections.extend(["", "## Channel Matrix", "", "| symbol | verdict | live remainder |", "|---|---|---|"])
    for row in channel_zero_matrix_rows():
        sections.append(f"| {row['symbol']} | {row['verdict']} | {row['live_remainder_if_unsigned']} |")
    sections.extend(["", "## Reduced Bound Rows", "", "| symbol | status | arena |", "|---|---|---|"])
    for row in live_bound_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['arena_projection']} |")
    sections.extend(
        [
            "",
            "## Current Meaning",
            "",
            "- `G` policy: the decimal value of `G` does not need deriving for local GR recovery; the no-drift/no-source-dependence of the coupling product does.",
            "- `Poynting` policy: static EM/Poynting stress is Hilbert source, not an extra force; only crossing flux is a live extra channel.",
            "- `Q_extra` policy: the remaining fight is survivor operators plus boundary/domain/flux edge terms.",
            "",
            "## Claim Ceiling",
            "",
            f"- {status['claim_state']}.",
            "- This checkpoint narrows the proof route; it does not close local GR.",
            "",
            "## Next Target",
            "",
            "- `4135-Y5-R2FR-survivor-operator-excision-or-bound-map.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4134_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4134_QEXTRA_ZERO_THEOREM": qextra_zero_theorem_rows,
        "P8_Y5_R2FR_4134_CHANNEL_ZERO_MATRIX": channel_zero_matrix_rows,
        "P8_Y5_R2FR_4134_CANDIDATE_ZERO_LEDGER": candidate_zero_ledger_rows,
        "P8_Y5_R2FR_4134_LIVE_BOUND_ROWS": live_bound_rows,
        "P8_Y5_R2FR_4134_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4134_STATUS": status_rows,
        "P8_Y5_R2FR_4134_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4134_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4134_1_doc",
        "checkpoint markdown exists and names decision",
        DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"),
        str(DOC_PATH),
    )

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4134_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    theorem_text = flatten_rows([outputs["P8_Y5_R2FR_4134_QEXTRA_ZERO_THEOREM"]])
    theorem_ok = all(
        token in theorem_text
        for token in ["WIT4021 + ADOPT3576 + NFC3579", "Q_extra=0", "R_survivor_ops", "NO_LOCAL_GR_CLAIM"]
    )
    add("VAL4134_3_zero_theorem", "zero theorem states candidate premises, reduction and no-claim ceiling", theorem_ok, "zero theorem tokens checked")

    matrix_text = flatten_rows([outputs["P8_Y5_R2FR_4134_CHANNEL_ZERO_MATRIX"]])
    matrix_ok = all(
        token in matrix_text
        for token in [
            "Q_symp",
            "Q_PiM_stress",
            "Q_delta_kappa",
            "Q_frame",
            "Q_radiative_Poynting",
            "Q_domain",
            "Q_boundary_leak",
            "Q_nonEH",
            "Q_memory",
            "Q_range",
        ]
    )
    add("VAL4134_4_channel_matrix", "channel matrix covers every 4133 Qextra channel", matrix_ok, "channel tokens checked")

    matrix_verdict_ok = all(
        token in matrix_text
        for token in [
            "CANDIDATE_ZERO_PIM_IDENTITY_BRANCH",
            "CANDIDATE_ZERO_KG_FACTOR_BRANCH",
            "CONDITIONAL_RECLASSIFICATION_TO_MH_TOTAL",
            "NOT_ZERO_UNTIL_SURVIVOR_OPERATORS_EXCISED_OR_BOUNDED",
            "LIVE_SURVIVOR_MEMORY_KERNEL",
            "LIVE_SURVIVOR_RANGE_TAIL",
        ]
    )
    add("VAL4134_5_verdicts", "matrix distinguishes candidate zeros, reclassifications and live survivors", matrix_verdict_ok, "verdict tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4134_LIVE_BOUND_ROWS"]])
    bound_ok = all(
        token in bound_text
        for token in [
            "epsilon_Qextra_4134",
            "R_survivor_ops",
            "R_boundary_harmonic",
            "R_undescended_support",
            "R_unstationary_flux",
            "R_parent_adoption",
        ]
    )
    add("VAL4134_6_bounds", "live bound rows contain reduced Qextra remainder components", bound_ok, "bound tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4134_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "CANDIDATE_ZERO_ROUTES_FOUND",
            "QEXTRA_ZERO_NOT_CLAIMED",
            "SURVIVOR_OPERATOR_BOUNDARY_FLUX_REMAINDER",
            "G_DECIMAL_NOT_REQUIRED_BUT_DRIFT_MUST_ZERO",
            "NEXT_SURVIVOR_OPERATOR_EXCISION_SELECTED",
        ]
    )
    add("VAL4134_7_decisions", "decision gates capture progress, no-claim, G policy and next target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4134_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("candidate_zero_routes_found") == "True"
        and status[0].get("Q_extra_zero_signed") == "False"
        and status[0].get("reduced_remainder_vector_filled") == "True"
    )
    add("VAL4134_8_status", "status records candidate progress and unsigned full Qextra zero", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4134_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4135-Y5-R2FR-survivor-operator-excision-or-bound-map.md"
    add("VAL4134_9_next_target", "next target is survivor operator excision or bound map", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4134_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4134*")) or any(FORMALIZATION.rglob("4134-Y5-R2FR*"))
    add(
        "VAL4134_11_scope",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        in_scope and not formalization_output and not formalization_touched,
        f"doc={DOC_PATH}; csv_count={len(outputs)}",
    )

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4134_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4134_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
