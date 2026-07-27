from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4356"
CLAIM_ID = "L-197"
BRANCH = "MTS_R2FR_Y5_TRANSITION_STATIC_MONOPOLE_UNIVERSAL_RANGEFREE_HAIR_ZERO_OR_BOUND_4356"
DECISION = "TRANSITION_STATIC_MONOPOLE_COMMON_MODE_HAIR_LAW_DERIVED_FINITE_HAIR_ROWS_RETAINED_NONCLAIM"
MARKER = "PPC4161_TRANSITION_STATIC_MONOPOLE_UNIVERSAL_RANGEFREE_HAIR_ZERO_OR_BOUND_4356"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_STATIC_MONOPOLE_UNIVERSAL_RANGEFREE_HAIR_ZERO_OR_BOUND_4356"
NEXT_TARGET = "4357-Y5-R2FR-transition-common-mode-parent-grammar-or-first-finite-hair-inputs.md"

FORMAL_PATH = FORMAL / "372-PPC4161-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md"
DOC_PATH = POST / "4356-Y5-R2FR-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4356_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4356_00_4355_next": (
        FORMAL / "371-PPC4161-transition-shell-same-worldtube-nonHilbert-residue-or-bounded-source-hair.md",
        "4356-Y5-R2FR-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md",
        "4355 handoff to the remaining static/monopole/universal/rangefree hair problem.",
    ),
    "SRC4356_01_310_kernel_definition": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "P_kernel := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube,",
        "Original transition source-kernel projector definition.",
    ),
    "SRC4356_02_310_static": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "static l=0 exterior,",
        "Static monopole condition in the conditional zero theorem.",
    ),
    "SRC4356_03_310_universal": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "universal/species-blind coupling,",
        "Universal species-blind coupling condition.",
    ),
    "SRC4356_04_305_split": (
        FORMAL / "305-PPC4161-transition-monopole-absorption-or-residual-profile-gate.md",
        "q_tr = q_tr^Hilbert-monopole + q_tr^residual.",
        "Transition split into absorbable Hilbert monopole plus residual hair.",
    ),
    "SRC4356_05_305_absorbable": (
        FORMAL / "305-PPC4161-transition-monopole-absorption-or-residual-profile-gate.md",
        "Only `q_tr^Hilbert-monopole` is absorbable.",
        "Only the common Hilbert monopole can be hidden in source charge.",
    ),
    "SRC4356_06_311_unsigned": (
        FORMAL / "311-PPC4161-parent-action-source-kernel-signature-search-and-leak-projector-reduction.md",
        "raw transition shell q_tr source-kernel membership = not parent-signed.",
        "Current raw transition shell is not yet in the kernel.",
    ),
    "SRC4356_07_311_time_multipole": (
        FORMAL / "311-PPC4161-parent-action-source-kernel-signature-search-and-leak-projector-reduction.md",
        "P_time_multipole q_tr",
        "Named time/multipole leak component.",
    ),
    "SRC4356_08_191_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "So the Poynting vector is not a separate background field.",
        "EM/Poynting is counted once as Hilbert stress, not as hidden transition hair.",
    ),
    "SRC4356_09_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "J_tr^nu = 0 through <=2PN.",
        "No-flux boundary theorem for local transition current.",
    ),
    "SRC4356_10_193_matter_descent": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "S_matter = Sbar_m[psi, g_obs(q), A(q), theta(q)].",
        "Matter/source readouts descend through the quotient before variation.",
    ),
    "SRC4356_11_193_no_source_norm": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "D_v theta_A = D_v m_A = D_v alpha_EM = D_v source_normalization = 0.",
        "Vertical/source normalization silence needed for label-forgetting.",
    ),
    "SRC4356_12_221_same_coframe": (
        FORMAL / "221-PPC4161-EH-coframe-parent-signature-or-Kperp-score.md",
        "same observed coframe for matter, EM, clocks and rods;",
        "Same observed coframe/EH readout gate.",
    ),
    "SRC4356_13_1064_common_G": (
        POST / "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md",
        "a common source normalization can be absorbed into measured `G` only if it is universal",
        "Measured-G common-mode guard.",
    ),
    "SRC4356_14_1064_derivative_guard": (
        POST / "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md",
        "D_A=0;D_t=0;D_r=0;D_lambda=0;Delta_frame=0",
        "Derivative guard for common-mode source normalization.",
    ),
    "SRC4356_15_1065_common_only": (
        POST / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
        "measured `G` absorbs only a common universal range/time/species/frame independent normalization",
        "Relative source weights cannot be hidden in measured G.",
    ),
}

ARENAS = [
    ("WEP_species", "species/source-label transition hair", "Delta_w_AB or eta_source_AB must be theorem-zero or sourced"),
    ("R10_range", "finite-range transition hair", "alpha_tr(lambda) must vanish or use source-backed lambda rows"),
    ("PPN_gamma_beta", "non-EH or anisotropic source hair", "gamma/beta/preferred-frame response needs projection constants"),
    ("clock_Gdot", "time-dependent common mode", "D_tau q_tr and D_t ln G_cal must vanish or be bounded"),
    ("orbital_GM", "absorbed monopole versus independent range/source term", "only constant common Hilbert monopole belongs in GM"),
    ("EM_Poynting", "visible EM momentum flux", "Poynting stress is not a second background field"),
    ("local_Newton_GR", "ordinary source-kernel bridge", "static l=0 common-mode source dressing is safe only after all guards close"),
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


def zero_clause_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "ZC4356_0_stationary_time",
            "hair": "Y_tau",
            "zero_premise": "q_tr is generated on the same stationary Hamiltonian collar and Lie_tau q_tr = 0 before local readout",
            "derived_zero": "partial_tau q_tr = 0",
            "bound_if_open": "Y_tau := ||Lie_tau q_tr||/M_H_ref",
            "status": "CONDITIONAL_ZERO_NOT_RAW_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZC4356_1_l0_monopole",
            "hair": "Y_l>=1",
            "zero_premise": "the exterior transition response is the unique static Hilbert source solution with only the linking-surface monopole charge",
            "derived_zero": "Q_l>=1_tr = 0",
            "bound_if_open": "Y_l>=1 := sum_l>=1 |Q_l,tr|/M_H_ref",
            "status": "CONDITIONAL_ZERO_NEEDS_BOUNDARY_AND_SOURCE_SYMMETRY_SIGNATURE",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZC4356_2_species_frame_source",
            "hair": "Y_species_frame_source",
            "zero_premise": "matter/source action descends through q and the parent grammar has no source-only species, frame, or material normalization slot",
            "derived_zero": "D_species q_tr = D_frame q_tr = D_source_weight q_tr = 0",
            "bound_if_open": "Y_species_frame_source := |D_species q_tr| + |D_frame q_tr| + |Delta_source_weight_tr|",
            "status": "CONDITIONAL_ZERO_COMMON_MODE_GUARD_IMPORTED",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZC4356_3_rangefree",
            "hair": "Y_lambda",
            "zero_premise": "the transition source has no independent finite-range pole or lambda-dependent kernel beyond the massless EH/Hilbert source channel",
            "derived_zero": "D_lambda q_tr = 0 and q_range_tail = 0",
            "bound_if_open": "Y_lambda := |D_lambda q_tr| + |q_range_tail|",
            "status": "CONDITIONAL_ZERO_NEEDS_OPERATOR_SPECTRUM_SIGNATURE",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZC4356_4_same_metric_EH",
            "hair": "Y_nonEH",
            "zero_premise": "same observed coframe and EH principal metric block are used by matter, EM, clocks, rods, PPN and orbital readouts",
            "derived_zero": "Sigma_nonEH[q_tr] = 0",
            "bound_if_open": "Y_nonEH := ||Pi_arena Sigma_nonEH[q_tr]||",
            "status": "CONDITIONAL_ZERO_IMPORTED_FROM_EH_COFRAME_GATE",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZC4356_5_boundary_no_flux",
            "hair": "Y_boundary",
            "zero_premise": "boundary/nonlocal transition flux is fixed, exact, projection-null, or routed as Hamiltonian boundary charge before bulk local scoring",
            "derived_zero": "B_tr_nonlocal contributes no hidden compact-local bulk source",
            "bound_if_open": "Y_boundary := |B_tr_nonlocal|/M_H_ref",
            "status": "CONDITIONAL_ZERO_IMPORTED_FROM_NO_FLUX_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZC4356_6_EM_Poynting_no_double_count",
            "hair": "Y_EM_extra",
            "zero_premise": "Maxwell-Hodge stress is included once in T_total and the Poynting vector is treated as Hilbert momentum flux, not as a background source field",
            "derived_zero": "epsilon_EM_extra_inner = 0 on the compact local selector branch",
            "bound_if_open": "radiative EM flux is routed to boundary/Hamiltonian rows, not hidden transition bulk hair",
            "status": "CONDITIONAL_ZERO_IMPORTED_FROM_MAXWELL_HODGE_OWNER",
            "valid_for_claim": "False",
        },
    ]


def decomposition_rows() -> List[Dict[str, str]]:
    return [
        {
            "decomposition_id": "DECMP4356_0_total",
            "object": "q_tr",
            "decomposition": "q_tr = q_0^H + delta q_tr^hair",
            "meaning": "q_0^H is the common static Hilbert monopole; delta q_tr^hair is everything a local precision test can see as extra structure",
            "safe_if": "delta q_tr^hair=0 and q_0^H is inside M_H^dress before readout",
            "valid_for_claim": "False",
        },
        {
            "decomposition_id": "DECMP4356_1_common_monopole",
            "object": "q_0^H",
            "decomposition": "q_0^H := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube q_tr",
            "meaning": "the only absorbable transition piece",
            "safe_if": "D_tau=D_lambda=D_species=D_frame=D_source_weight=0 and same EH/coframe/boundary ownership holds",
            "valid_for_claim": "False",
        },
        {
            "decomposition_id": "DECMP4356_2_hair",
            "object": "delta q_tr^hair",
            "decomposition": "(I-P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube) q_tr",
            "meaning": "the finite transition hair vector to be projected into WEP/R10/PPN/clock/orbital tests",
            "safe_if": "each named hair component is theorem-zero or source-backed below arena bounds",
            "valid_for_claim": "False",
        },
    ]


def common_mode_rows() -> List[Dict[str, str]]:
    return [
        {
            "common_id": "CM4356_0_absorbable_G_mode",
            "candidate": "common transition monopole",
            "guards": "D_tau=0; D_lambda=0; D_species=0; D_frame=0; D_source_weight=0; same_metric=True; boundary_owned=True",
            "result": "may be absorbed into M_H^dress / calibrated source charge",
            "not_allowed": "using measured G to hide relative, time-varying, finite-range, frame, or non-EH transition hair",
            "status": "CONDITIONAL_COMMON_MODE_ONLY",
            "valid_for_claim": "False",
        },
        {
            "common_id": "CM4356_1_relative_source_weight",
            "candidate": "w_A/w_B or source label dependence",
            "guards": "parent grammar excludes source-only species scalars before variation",
            "result": "D_species q_tr=0 only if the grammar/source descent is signed",
            "not_allowed": "folding relative weights into G_cal after the fact",
            "status": "OPEN_PARENT_GRAMMAR_TARGET",
            "valid_for_claim": "False",
        },
        {
            "common_id": "CM4356_2_range_tail",
            "candidate": "lambda-dependent transition source",
            "guards": "no independent massive/Yukawa pole in the transition source operator",
            "result": "D_lambda q_tr=0 only if the source operator has no range label",
            "not_allowed": "calling a finite-range alpha(lambda) row a Newtonian mass renormalization",
            "status": "OPEN_OPERATOR_SPECTRUM_TARGET",
            "valid_for_claim": "False",
        },
    ]


def hair_bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "HB4356_0_tau",
            "hair_component": "Y_tau",
            "formula": "Y_tau := ||Lie_tau q_tr||/M_H_ref",
            "zero_if": "same stationary Hamiltonian collar gives Lie_tau q_tr=0",
            "feeds": "clock_Gdot; PPN preferred-frame; orbital secular drift",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4356_1_multipole",
            "hair_component": "Y_l>=1",
            "formula": "Y_l>=1 := sum_l>=1 |Q_l,tr|/M_H_ref",
            "zero_if": "static exterior transition response has only the source-kernel l=0 Hilbert monopole",
            "feeds": "PPN anisotropy; orbital precession; local Newton residual",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4356_2_species_frame_source",
            "hair_component": "Y_species_frame_source",
            "formula": "Y_species_frame_source := |D_species q_tr| + |D_frame q_tr| + |Delta_source_weight_tr|",
            "zero_if": "source-label forgetting and same-frame descent are parent-signed",
            "feeds": "WEP; preferred-frame PPN; source normalization",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4356_3_range",
            "hair_component": "Y_lambda",
            "formula": "Y_lambda := |D_lambda q_tr| + |q_range_tail|",
            "zero_if": "transition source operator is range-free/common massless Hilbert monopole only",
            "feeds": "R10 alpha(lambda); orbital range tests",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4356_4_nonEH",
            "hair_component": "Y_nonEH",
            "formula": "Y_nonEH := ||Pi_arena Sigma_nonEH[q_tr]||",
            "zero_if": "same EH coframe/metric readout owns all local matter, EM, clock, rod and orbital response",
            "feeds": "PPN gamma/beta; clock; local GR bridge",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4356_5_boundary",
            "hair_component": "Y_boundary",
            "formula": "Y_boundary := |B_tr_nonlocal|/M_H_ref",
            "zero_if": "boundary/nonlocal term is exact, fixed, projection-null or Hamiltonian-routed",
            "feeds": "PPN; clock; orbital; transition closure",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4356_6_total_remaining",
            "hair_component": "epsilon_tr_hair_remaining",
            "formula": "epsilon_tr_hair_remaining <= Y_tau + Y_l>=1 + Y_species_frame_source + Y_lambda + Y_nonEH + Y_boundary",
            "zero_if": "all ZC4356 zero clauses close on one selector branch",
            "feeds": "epsilon_tr_hair; epsilon_Gsrc; all local arenas",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4356_7_total_with_4355",
            "hair_component": "epsilon_tr_hair",
            "formula": "epsilon_tr_hair <= Y_nonHilbert + Delta_Wtr + epsilon_tr_hair_remaining",
            "zero_if": "4355 owner/worldtube legs plus all 4356 common-mode hair legs close",
            "feeds": "epsilon_Gsrc <- epsilon_Gsrc + epsilon_tr_hair if open",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4356_0_static_monopole_common_mode",
            "statement": "If q_tr descends through the same Hilbert source functor, is stationary, has only l=0 exterior charge, is species/frame/source-label blind, range-free, same-metric/EH and boundary-owned, then delta q_tr^hair=0.",
            "derivation": "The quotient/action descent kills source-only labels; stationary Hamiltonian flow kills Lie_tau q_tr; exterior uniqueness with only the linking-surface monopole kills Q_l>=1_tr; absence of extra poles kills D_lambda q_tr; same EH/coframe and no-flux routing kill nonEH and boundary bulk terms.",
            "consequence": "transition contribution is common source dressing inside M_H^dress, not a separate local residual",
            "status": "CONDITIONAL_THEOREM_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4356_1_common_mode_guard",
            "statement": "Measured G/calibrated coupling can absorb only a constant universal range/time/species/frame independent source normalization.",
            "derivation": "1064/1065 derivative guards forbid hiding relative, finite-range, frame, species, or time-dependent transition weights in G_cal.",
            "consequence": "all non-common transition hair remains a physical local-test row",
            "status": "IMPORTED_GUARD_APPLIED_TO_TRANSITION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4356_2_Poynting_not_background_hair",
            "statement": "A Poynting vector inside compact local matter is already the spatial flux component of Maxwell-Hodge Hilbert stress.",
            "derivation": "T_EM is included once in T_total; radiative flux crossing the collar is routed as boundary/Hamiltonian charge.",
            "consequence": "do not invent a second Poynting background field as transition source hair",
            "status": "EM_SIDE_CHANNEL_CLOSED_CONDITIONALLY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4356_3_raw_shell_still_open",
            "statement": "The raw transition shell is not promoted to local-GR safety unless the 4356 zero clauses are parent-signed or finite rows are sourced and pass.",
            "derivation": "311 and 4355 both retain raw transition source-kernel membership as unsigned.",
            "consequence": "no R10, WEP, PPN, clock, orbital or public local-GR claim fires from 4356",
            "status": "FIREWALL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for arena, observable, requirement in ARENAS:
        rows.append(
            {
                "arena_id": f"AR4356_{arena}",
                "arena": arena,
                "observable": observable,
                "zero_branch": "epsilon_tr_hair_remaining=0 and common monopole enters only M_H^dress",
                "finite_branch_requirement": requirement,
                "current_status": "NO_PASS_FROM_4356_ALONE",
                "valid_for_claim": "False",
            }
        )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4356_0_clean",
            "input": "4355 owner/worldtube legs closed plus all ZC4356 zero clauses",
            "action": "ROUTE_TRANSITION_TO_COMMON_STATIC_HILBERT_MONOPOLE",
            "result": "delta q_tr^hair=0; epsilon_tr_hair_remaining=0; q_tr contributes only to M_H^dress",
            "claim_policy": "private conditional theorem only",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4356_1_common_mode_guard",
            "input": "constant common transition monopole but derivative/source/range guards not all closed",
            "action": "REFUSE_G_ABSORPTION_FOR_NONCOMMON_BITS",
            "result": "relative/time/range/frame/nonEH terms stay in finite hair rows",
            "claim_policy": "no measured-G hiding shortcut",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4356_2_finite",
            "input": "any 4356 zero clause open",
            "action": "KEEP_EPSILON_TR_HAIR_REMAINING_BOUND",
            "result": "epsilon_tr_hair <= Y_nonHilbert + Delta_Wtr + epsilon_tr_hair_remaining",
            "claim_policy": "requires numeric/source-backed rows before empirical scoring",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4356_3_next",
            "input": "source-label/range/time common-mode clauses still unsigned for raw q_tr",
            "action": "ATTACK_PARENT_COMMON_MODE_GRAMMAR_OR_FILL_FIRST_HAIR_INPUTS",
            "result": NEXT_TARGET,
            "claim_policy": "derive before fitting; otherwise source finite rows",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4356_0",
            "rule": "Do not absorb a transition term into G_cal or M_H^dress unless it is constant, universal, range-free, species/frame/source-label blind and same-metric.",
            "reason": "only the common Hilbert monopole is a source-charge dressing.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4356_1",
            "rule": "Do not treat raw q_tr as static l=0 just because the ordinary source kernel has an l=0 sector.",
            "reason": "raw transition-shell source-kernel membership remains unsigned.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4356_2",
            "rule": "Do not use Poynting-vector language as a new hidden background field.",
            "reason": "Poynting flux is Maxwell-Hodge Hilbert stress or boundary/Hamiltonian flux.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4356_3",
            "rule": "Do not cancel time, multipole, species, range, nonEH or boundary hair against each other.",
            "reason": "epsilon_tr_hair_remaining is an absolute no-cancellation envelope.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4356_4",
            "rule": "Do not claim R10, WEP, PPN, clock, orbital or public local-GR pass from 4356.",
            "reason": "4356 is a conditional derivation plus finite-row schema, not a sourced empirical pass.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4356_0",
            "decision": DECISION,
            "reason": "4356 derives the sharper common-mode hair law. The safe transition contribution is only q_0^H: a stationary l=0 Hilbert monopole that is universal, range-free, species/frame/source-label blind, same-metric/EH and boundary-owned. Under those clauses delta q_tr^hair=0 and the transition contribution enters M_H^dress only. The current raw transition shell still lacks parent signatures for those clauses, so 4356 retains explicit finite no-cancellation rows for time, multipole, species/frame/source, range, nonEH and boundary hair.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4356_0",
            "item": "static monopole route",
            "status": "DERIVED_AS_CONDITIONAL_COMMON_MODE_THEOREM",
            "note": "If the parent signs stationarity and exterior l=0 uniqueness, time/multipole hair vanish.",
        },
        {
            "status_id": "STAT4356_1",
            "item": "coupling/source-label route",
            "status": "SHARPENED_TO_PARENT_GRAMMAR_COMMON_MODE_GATE",
            "note": "Measured G absorbs only constant universal range/time/species/frame independent normalization.",
        },
        {
            "status_id": "STAT4356_2",
            "item": "Poynting/vector route",
            "status": "NOT_A_SEPARATE_BACKGROUND_SOURCE_ON_COMPACT_SELECTOR",
            "note": "Poynting is Maxwell-Hodge Hilbert stress or boundary flux.",
        },
        {
            "status_id": "STAT4356_3",
            "item": "raw transition shell",
            "status": "NOT_PARENT_SIGNED_INTO_COMMON_MODE",
            "note": "No local-GR/R10/PPN/WEP/clock/orbital claim fires.",
        },
        {
            "status_id": "STAT4356_4",
            "item": "next target",
            "status": "COMMON_MODE_PARENT_GRAMMAR_OR_FIRST_FINITE_INPUTS",
            "note": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4356_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the parent action grammar force transition q_tr to be a common-mode source dressing with no source-label, frame, time, range or nonEH slots?",
            "preferred_route": "prove the no-source-only-slot/range-free/operator-spectrum rule for q_tr from quotient descent and Hamiltonian source ownership",
            "fallback_route": "fill the first finite source-backed hair inputs for Y_species_frame_source and Y_lambda, then project to WEP and R10 without claiming a pass",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "clauses": zero_clause_rows(),
        "decomposition": decomposition_rows(),
        "common": common_mode_rows(),
        "hair": hair_bound_rows(),
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
        "sources": "P8_Y5_R2FR_4356_SOURCE_REGISTER.csv",
        "clauses": "P8_Y5_R2FR_4356_ZERO_CLAUSE_ROWS.csv",
        "decomposition": "P8_Y5_R2FR_4356_DECOMPOSITION_ROWS.csv",
        "common": "P8_Y5_R2FR_4356_COMMON_MODE_ROWS.csv",
        "hair": "P8_Y5_R2FR_4356_HAIR_BOUND_ROWS.csv",
        "theorems": "P8_Y5_R2FR_4356_THEOREM_ROWS.csv",
        "arenas": "P8_Y5_R2FR_4356_ARENA_ROWS.csv",
        "runner": "P8_Y5_R2FR_4356_RUNNER.csv",
        "firewall": "P8_Y5_R2FR_4356_CLAIM_FIREWALL.csv",
        "decision": "P8_Y5_R2FR_4356_DECISION.csv",
        "status": "P8_Y5_R2FR_4356_STATUS.csv",
        "next": "P8_Y5_R2FR_4356_NEXT_TARGET.csv",
    }
    for key, filename in mapping.items():
        write_csv(SOURCE_DIR / filename, tables[key])


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 372 PPC4161 transition static monopole universal rangefree hair zero or bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4356 does not prove public local GR, Newton, R10, PPN, WEP, clock, orbital, EM, or transition-shell safety.

## Result

4356 attacks the remaining 4355 hair directly. The safe object is not an arbitrary transition shell. The safe object is only the common-mode Hilbert monopole:

```text
q_tr = q_0^H + delta q_tr^hair,

q_0^H :=
  P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube q_tr.
```

The clean theorem is:

```text
Lie_tau q_tr = 0,
Q_l>=1_tr = 0,
D_species q_tr = 0,
D_frame q_tr = 0,
D_source_weight q_tr = 0,
D_lambda q_tr = 0,
Sigma_nonEH[q_tr] = 0,
B_tr_nonlocal = fixed/exact/routed/projection-null
```

imply

```text
delta q_tr^hair = 0,
epsilon_tr_hair_remaining = 0.
```

Then the transition term is just source dressing:

```text
M_H^dress -> M_H^dress + M_tr^H.
```

This is the GR/Newton-compatible route: the same calibrated source charge changes, not a second local force law.

## Common-Mode Guard

The important coupling rule is:

```text
measured G absorbs only a constant universal range/time/species/frame independent source normalization.
```

So any time dependence, finite range, source-label dependence, frame dependence, species dependence, non-EH metric response, or non-owned boundary flux is not a Newtonian mass renormalization. It is hair.

The finite branch is therefore:

```text
epsilon_tr_hair_remaining <=
  Y_tau
  + Y_l>=1
  + Y_species_frame_source
  + Y_lambda
  + Y_nonEH
  + Y_boundary,

epsilon_tr_hair <=
  Y_nonHilbert
  + Delta_Wtr
  + epsilon_tr_hair_remaining.
```

4356 also fixes the Poynting fork: on the compact local selector branch, the Poynting vector is Maxwell-Hodge Hilbert stress already counted in `T_total`, not a separate background field. Radiative flux is routed to the boundary/Hamiltonian charge.

The raw transition shell is still not parent-signed into this common-mode kernel. That is the point of the next target.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Zero Clause Rows

{md_table(tables["clauses"], ["clause_id", "hair", "zero_premise", "derived_zero", "bound_if_open", "status", "valid_for_claim"])}

## Decomposition Rows

{md_table(tables["decomposition"], ["decomposition_id", "object", "decomposition", "meaning", "safe_if", "valid_for_claim"])}

## Common Mode Rows

{md_table(tables["common"], ["common_id", "candidate", "guards", "result", "not_allowed", "status", "valid_for_claim"])}

## Hair Bound Rows

{md_table(tables["hair"], ["bound_id", "hair_component", "formula", "zero_if", "feeds", "valid_for_claim"])}

## Theorem Rows

{md_table(tables["theorems"], ["theorem_id", "statement", "derivation", "consequence", "status", "claim_allowed", "valid_for_claim"])}

## Arena Rows

{md_table(tables["arenas"], ["arena_id", "arena", "observable", "zero_branch", "finite_branch_requirement", "current_status", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "input", "action", "result", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "rule", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    post = f"""# 4356 Y5-R2FR transition static monopole universal rangefree hair zero or bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4356 turns the remaining transition hair into a sharper common-mode law:

```text
q_tr = q_0^H + delta q_tr^hair
```

Only `q_0^H` is absorbable into `M_H^dress`. Everything else is hair:

```text
epsilon_tr_hair_remaining <=
  Y_tau + Y_l>=1 + Y_species_frame_source + Y_lambda + Y_nonEH + Y_boundary.
```

Clean branch: stationary, l=0, universal/species-frame/source blind, range-free, same-metric/EH and boundary-owned transition contribution.

Finite branch: no cancellation; source the hair rows before WEP/R10/PPN/clock/orbital scoring.

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
                    "4356 derives the transition static-monopole/common-mode hair law. The absorbable transition contribution is only q_0^H: a stationary l=0 Hilbert monopole that is universal, range-free, species/frame/source-label blind, same-metric/EH and boundary-owned before readout. Under those clauses delta q_tr^hair=0 and epsilon_tr_hair_remaining=0, so the transition term enters M_Hdress as ordinary source dressing. Measured G/calibrated coupling can absorb only constant universal range/time/species/frame independent normalization; time, multipole, source-label, finite-range, nonEH or boundary hair remains physical. Raw transition shells are still not parent-signed into this common-mode kernel, so 4356 keeps finite no-cancellation hair rows and no public local-GR/R10/WEP/PPN/clock/orbital claim fires."
                ),
                (
                    "4356 source register, zero-clause rows, decomposition rows, common-mode rows, hair-bound rows, theorem rows, arena rows, runner, firewall, decision, status, next-target and validation CSV."
                ),
                "conditional_transition_common_mode_hair_zero_or_finite_rows_nonclaim",
                (
                    "Prove the parent common-mode grammar/range-free operator rule for raw transition q_tr, or fill first finite source-backed Y_species_frame_source and Y_lambda rows."
                ),
                (
                    "Absorbing relative/time/range/frame/species transition hair into measured G; treating raw q_tr as static l=0 without parent signature; double-counting Poynting flux as a hidden background field; cancelling hair components; claiming local GR from the conditional theorem."
                ),
            ]
        )


def append_spine_and_packet() -> None:
    spine_block = f"""

## PPC4161 4356 transition static-monopole common-mode hair law

Marker: `{MARKER}`

4356 sharpens the transition route:

```text
q_tr = q_0^H + delta q_tr^hair
```

Only the stationary `l=0`, universal, range-free, species/frame/source-label blind, same-metric/EH and boundary-owned Hilbert monopole `q_0^H` may enter `M_H^dress`. The remaining vector obeys:

```text
epsilon_tr_hair_remaining <=
  Y_tau + Y_l>=1 + Y_species_frame_source + Y_lambda + Y_nonEH + Y_boundary.
```

Poynting flux is not a second background source on the compact selector branch: it is Maxwell-Hodge Hilbert stress or boundary/Hamiltonian flux. Raw transition shells remain unsigned, so the next target is the parent common-mode grammar/range-free operator proof or finite source-backed hair rows.
"""
    packet_block = f"""

## PPC4161 packet update 4356 transition common-mode hair

Marker: `{PACKET_MARKER}`

Packet update: the transition shell can be safe only as a common static Hilbert monopole source dressing. Any time, multipole, species/frame/source, range, nonEH or boundary residue remains explicit hair. The Poynting-vector fork is routed to Maxwell-Hodge Hilbert stress or boundary flux, not a new hidden background field.
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
    checks.append(("decomposition_present", "q_tr = q_0^H + delta q_tr^hair" in formal_text, "transition decomposition"))
    checks.append(("stationary_condition_present", "Lie_tau q_tr = 0" in formal_text, "stationarity"))
    checks.append(("multipole_zero_present", "Q_l>=1_tr = 0" in formal_text, "multipole zero"))
    checks.append(("lambda_zero_present", "D_lambda q_tr = 0" in formal_text, "rangefree zero"))
    checks.append(("hair_bound_present", "epsilon_tr_hair_remaining <=" in formal_text, "remaining hair bound"))
    checks.append(("total_bound_present", "epsilon_tr_hair <=" in formal_text, "total hair bound"))
    checks.append(("common_G_guard_present", "measured G absorbs only" in formal_text, "common-mode guard"))
    checks.append(("poynting_guard_present", "Poynting vector is Maxwell-Hodge Hilbert stress" in formal_text, "Poynting guard"))
    checks.append(("all_sources_exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source paths"))
    checks.append(("all_needles_found", all(row["needle_found"] == "True" for row in tables["sources"]), "source needles"))
    checks.append(("zero_clause_rows_present", len(tables["clauses"]) >= 7, str(len(tables["clauses"]))))
    checks.append(("decomposition_rows_present", len(tables["decomposition"]) >= 3, str(len(tables["decomposition"]))))
    checks.append(("common_rows_present", len(tables["common"]) >= 3, str(len(tables["common"]))))
    checks.append(("hair_rows_present", len(tables["hair"]) >= 8, str(len(tables["hair"]))))
    checks.append(("theorem_rows_present", len(tables["theorems"]) >= 4, str(len(tables["theorems"]))))
    checks.append(("arena_rows_present", len(tables["arenas"]) == len(ARENAS), str(len(tables["arenas"]))))
    checks.append(("no_valid_claim_rows", all(row.get("valid_for_claim") == "False" for rows in tables.values() for row in rows if "valid_for_claim" in row), "all generated claim flags false"))
    checks.append(("claim_row_recorded", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID))
    checks.append(("spine_marker_recorded", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER))
    checks.append(("packet_marker_recorded", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER))
    for filename in [
        "P8_Y5_R2FR_4356_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4356_ZERO_CLAUSE_ROWS.csv",
        "P8_Y5_R2FR_4356_DECOMPOSITION_ROWS.csv",
        "P8_Y5_R2FR_4356_COMMON_MODE_ROWS.csv",
        "P8_Y5_R2FR_4356_HAIR_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4356_THEOREM_ROWS.csv",
        "P8_Y5_R2FR_4356_ARENA_ROWS.csv",
        "P8_Y5_R2FR_4356_RUNNER.csv",
        "P8_Y5_R2FR_4356_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4356_DECISION.csv",
        "P8_Y5_R2FR_4356_STATUS.csv",
        "P8_Y5_R2FR_4356_NEXT_TARGET.csv",
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
    print(f"{CHECKPOINT}: wrote 12 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation_rows)} failed={len(failures)}")
    if failures:
        for row in failures:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
