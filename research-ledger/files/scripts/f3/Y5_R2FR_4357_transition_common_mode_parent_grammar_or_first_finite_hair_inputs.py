from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds"

CHECKPOINT = "4357"
CLAIM_ID = "L-198"
BRANCH = "MTS_R2FR_Y5_TRANSITION_COMMON_MODE_PARENT_GRAMMAR_OR_FIRST_FINITE_HAIR_INPUTS_4357"
DECISION = "COMMON_MODE_GRAMMAR_GATE_SHARPENED_WA_COUNTEREXAMPLE_RETAINED_FIRST_WEP_R10_INPUTS_IMPORTED_NONCLAIM"
MARKER = "PPC4161_TRANSITION_COMMON_MODE_PARENT_GRAMMAR_OR_FIRST_FINITE_HAIR_INPUTS_4357"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_COMMON_MODE_PARENT_GRAMMAR_OR_FIRST_FINITE_HAIR_INPUTS_4357"
NEXT_TARGET = "4358-Y5-R2FR-transition-action-measure-owner-or-tau-WEP-source-projection-bridge.md"

FORMAL_PATH = FORMAL / "373-PPC4161-transition-common-mode-parent-grammar-or-first-finite-hair-inputs.md"
DOC_PATH = POST / "4357-Y5-R2FR-transition-common-mode-parent-grammar-or-first-finite-hair-inputs.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4357_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4357_00_4356_next": (
        FORMAL / "372-PPC4161-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md",
        "4357-Y5-R2FR-transition-common-mode-parent-grammar-or-first-finite-hair-inputs.md",
        "4356 handoff to common-mode parent grammar or finite hair inputs.",
    ),
    "SRC4357_01_4356_common": (
        FORMAL / "372-PPC4161-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md",
        "measured G absorbs only a constant universal range/time/species/frame independent source normalization.",
        "Common-mode guard to be parent-signed or bounded.",
    ),
    "SRC4357_02_193_source_norm": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "D_v theta_A = D_v m_A = D_v alpha_EM = D_v source_normalization = 0.",
        "Quotient descent source-normalization silence clause.",
    ),
    "SRC4357_03_393_common_G": (
        POST / "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "Only a constant, universal, range-independent `mu_obs` can be absorbed into measured `GM`.",
        "Source-normalized Newtonian common-mode rule.",
    ),
    "SRC4357_04_1594_counterexample": (
        POST / "1594-Y5-R2FR-action-weight-exclusion-or-beta-source-acquisition-validator.md",
        "Classical matter equations do not remove `w_A`:",
        "Pre-variation action-weight counterexample survives classical equations.",
    ),
    "SRC4357_05_1594_target": (
        POST / "1594-Y5-R2FR-action-weight-exclusion-or-beta-source-acquisition-validator.md",
        "Allowed[S_matter] = sum_A S_A[Psi_A,e_obs(q),A_Q,theta_A] with no independent w_A S_A source/action multiplier.",
        "Exact grammar target needed to kill source-only weights.",
    ),
    "SRC4357_06_1594_metric_variation": (
        POST / "1594-Y5-R2FR-action-weight-exclusion-or-beta-source-acquisition-validator.md",
        "source variation still sees w_A",
        "Why current-owner/classical EOM alone cannot kill pre-variation weights.",
    ),
    "SRC4357_07_1595_bound": (
        POST / "1595-Y5-R2FR-first-source-backed-beta-or-action-measure-owner-reopen.md",
        "abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15",
        "First validator-readable source-backed WEP bound anchor.",
    ),
    "SRC4357_08_local_bound_claims": (
        LOCAL_BOUNDS / "local_bound_claims.csv",
        "R1_WEP_source_charge",
        "Local bound source row for the WEP source-charge proxy.",
    ),
    "SRC4357_09_563_r10_anchor": (
        POST / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "Real Eot-Wash source-backed anchor points are now staged",
        "R10 source-backed anchor acquisition checkpoint.",
    ),
    "SRC4357_10_r10_anchor_file": (
        LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
        "R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
        "Modern Eot-Wash alpha=1/lambda anchor row.",
    ),
    "SRC4357_11_r10_symbolic_smoke": (
        SOURCE_DIR / "R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM.csv",
        "symbolic_prefactor_nonclaim_smoke_parent_coefficients_absent",
        "MTS R10 alpha row is symbolic and invalid for claim scoring.",
    ),
    "SRC4357_12_563_blocker": (
        SOURCE_DIR / "P8_Y5_R10_563_BLOCKER_LEDGER.csv",
        "Only alpha=1 threshold anchors were staged",
        "R10 finite-range data remains anchor-only and nonclaim.",
    ),
    "SRC4357_13_563_runner": (
        SOURCE_DIR / "P8_Y5_R10_563_RUNNER_SUMMARY.csv",
        "R10_RUNNER_563_ANCHOR_SMOKE_RECHECK",
        "Existing R10 comparator blocks claim rows.",
    ),
    "SRC4357_14_310_universal": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "universal/species-blind coupling,",
        "Original source-kernel universal/species-blind clause.",
    ),
}

ARENAS = [
    ("Newton_source", "source normalization in GM/G_cal", "common constant factor only; relative w_A remains physical"),
    ("WEP_species", "Delta_w_AB and source/test charge contrast", "first bound anchor exists but tau_WEP/source projection missing"),
    ("R10_range", "finite-range alpha(lambda) hair", "Eot-Wash anchors exist but parent alpha numeric/full curve missing"),
    ("PPN_gamma_beta", "source-weight and finite-range metric transfer", "no identity projection or measured-G absorption shortcut"),
    ("clock_Gdot", "time-dependent source/action weight", "derivative-silent common factor only"),
    ("orbital_GM", "range-dependent force versus absorbed mass", "finite range cannot be folded into orbital GM calibration"),
    ("local_GR", "all source/coupling gates together", "local GR remains blocked while w_A or lambda hair survives"),
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


def grammar_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GG4357_0_allowed_matter_functor",
            "required_statement": "Allowed[S_matter] = sum_A S_A[Psi_A,e_obs(q),A_Q,theta_A] with no independent w_A S_A source/action multiplier",
            "would_derive": "D_species q_tr = D_source_weight q_tr = 0 for transition common-mode source dressing",
            "evidence_now": "exact target written in 1594 but not parent-signed",
            "status": "CONDITIONAL_GRAMMAR_GATE",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GG4357_1_action_measure_owner",
            "required_statement": "one universal parent action scale/measure makes independent exp(i w_A S_A/hbar_parent) inadmissible",
            "would_derive": "relative pre-variation action weights are absent or common",
            "evidence_now": "1595 reopens the route and still finds no parent-signed owner",
            "status": "CLEANEST_ZERO_ROUTE_NOT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GG4357_2_current_owner_limit",
            "required_statement": "Hilbert current is varied before readout after one common action is fixed",
            "would_derive": "post-variation rescalings cannot create independent source weights",
            "evidence_now": "partial theorem only; T_H inherits w_A if w_A is already inside S_matter before variation",
            "status": "POST_VARIATION_ONLY",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GG4357_3_quotient_source_silence",
            "required_statement": "D_v theta_A = D_v m_A = D_v alpha_EM = D_v source_normalization = 0",
            "would_derive": "vertical/source-label drift is silent inside the compact quotient branch",
            "evidence_now": "private selector theorem exists but raw transition q_tr still needs branch membership",
            "status": "PRIVATE_BRANCH_SUPPORT_NOT_RAW_TRANSITION_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GG4357_4_no_extra_range_operator",
            "required_statement": "transition common-mode source operator has no independent massive/Yukawa pole or lambda label",
            "would_derive": "D_lambda q_tr = 0 and q_range_tail=0",
            "evidence_now": "R10 rows show the finite-range scoring interface exists, but parent coefficients and full curve are missing",
            "status": "OPERATOR_SPECTRUM_GATE_OPEN",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GG4357_5_same_branch_total",
            "required_statement": "GG4357_0 through GG4357_4 close on the same transition branch before empirical scoring",
            "would_derive": "Y_species_frame_source=0 and Y_lambda=0 inside epsilon_tr_hair_remaining",
            "evidence_now": "package does not close; finite input route activated",
            "status": "COMMON_MODE_THEOREM_NOT_CLAIM_GRADE",
            "valid_for_claim": "False",
        },
    ]


def counterexample_rows() -> List[Dict[str, str]]:
    return [
        {
            "counterexample_id": "CE4357_0_prevariation_wA",
            "counterexample": "S_matter -> sum_A w_A S_A before variation",
            "why_it_survives": "delta(w_A S_A)/delta Psi_A=0 can preserve isolated classical matter equations while delta(w_A S_A)/delta g = w_A T_A",
            "kills_fake_proof": "classical EOM/free-fall route",
            "residual_if_survives": "Delta_w_A and beta_w_A source-weight rows",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "counterexample_id": "CE4357_1_current_owner_not_enough",
            "counterexample": "post-variation current owner cannot remove a weight inserted before the action variation",
            "why_it_survives": "T_H is unique only after one common action is fixed",
            "kills_fake_proof": "current-owner-only route",
            "residual_if_survives": "Y_species_frame_source",
            "status": "ACTIVE_UNLESS_ACTION_MEASURE_OWNER_CLOSES",
            "valid_for_claim": "False",
        },
        {
            "counterexample_id": "CE4357_2_anchor_not_prediction",
            "counterexample": "using MICROSCOPE eta bound as MTS Delta_w prediction",
            "why_it_survives": "tau_WEP, source worldtube, material map and readout kernel are not supplied",
            "kills_fake_proof": "bound-anchor-as-score shortcut",
            "residual_if_survives": "P_WEP_relative_source_weight bound-only input",
            "status": "BLOCKED_SCORE",
            "valid_for_claim": "False",
        },
        {
            "counterexample_id": "CE4357_3_R10_anchor_not_curve",
            "counterexample": "using alpha=1 threshold anchors as a full alpha(lambda) exclusion curve",
            "why_it_survives": "full digitized curve and numeric MTS alpha coefficients are missing",
            "kills_fake_proof": "R10 anchor-as-pass shortcut",
            "residual_if_survives": "Y_lambda source-acquisition row",
            "status": "BLOCKED_SCORE",
            "valid_for_claim": "False",
        },
    ]


def finite_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "FI4357_0_WEP_Delta_w_tau_anchor",
            "hair_component": "Y_species_frame_source",
            "quantity": "P_WEP_relative_source_weight = abs(Delta_w_TiPt*tau_WEP)",
            "value": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(LOCAL_BOUNDS / "local_bound_claims.csv"),
            "source_anchor": "R1_WEP_source_charge",
            "extraction_method": "MICROSCOPE Ti/Pt WEP source-charge proxy imported as bound-only anchor",
            "what_this_gives": "first source-backed finite input for the w_A/source-label gremlin",
            "what_is_missing": "tau_WEP; source worldtube; material response map; readout kernel; MTS Delta_w prediction",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "input_id": "FI4357_1_R10_EotWash_2020_anchor",
            "hair_component": "Y_lambda",
            "quantity": "alpha_bound(lambda=3.86e-5 m)",
            "value": "1.0",
            "units": "dimensionless alpha at metres",
            "source_path": str(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"),
            "source_anchor": "R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
            "extraction_method": "source-backed threshold anchor only, not full curve digitization",
            "what_this_gives": "finite-range evidence plumbing and unit anchor for lambda hair",
            "what_is_missing": "full alpha(lambda) curve; numeric MTS Z_X, M_X^2, K_X, Qbar_XH and qbar_XT",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "input_id": "FI4357_2_R10_EotWash_2007_anchor",
            "hair_component": "Y_lambda",
            "quantity": "alpha_bound(lambda=5.6e-5 m)",
            "value": "1.0",
            "units": "dimensionless alpha at metres",
            "source_path": str(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"),
            "source_anchor": "R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM",
            "extraction_method": "source-backed continuity anchor only",
            "what_this_gives": "older continuity threshold for range-hair acquisition",
            "what_is_missing": "full curve and numeric MTS parent alpha coefficients",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def updated_hair_rows() -> List[Dict[str, str]]:
    return [
        {
            "hair_id": "UH4357_0_species_frame_source",
            "4356_component": "Y_species_frame_source",
            "old_status": "formula ready, source-label grammar unsigned",
            "4357_update": "w_A counterexample remains active, but WEP source-charge bound anchor is now imported as first finite input",
            "current_law": "Y_species_frame_source >= |D_species q_tr| + |D_frame q_tr| + |Delta_source_weight_tr|",
            "finite_input": "abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15 bound-only anchor",
            "claim_status": "nonclaim_bound_input_only",
            "valid_for_claim": "False",
        },
        {
            "hair_id": "UH4357_1_range",
            "4356_component": "Y_lambda",
            "old_status": "range-free operator gate unsigned",
            "4357_update": "Eot-Wash anchor rows imported as nonclaim source-backed finite-range anchors; MTS alpha remains symbolic",
            "current_law": "Y_lambda >= |D_lambda q_tr| + |q_range_tail|",
            "finite_input": "alpha_bound=1 at lambda=38.6 um and 56 um anchor-only rows",
            "claim_status": "nonclaim_anchor_only",
            "valid_for_claim": "False",
        },
        {
            "hair_id": "UH4357_2_total_remaining",
            "4356_component": "epsilon_tr_hair_remaining",
            "old_status": "finite no-cancellation envelope",
            "4357_update": "two first finite data anchors exist, but neither gives a theorem-zero or score-ready prediction",
            "current_law": "epsilon_tr_hair_remaining <= Y_tau + Y_l>=1 + Y_species_frame_source + Y_lambda + Y_nonEH + Y_boundary",
            "finite_input": "WEP bound anchor + R10 threshold anchors",
            "claim_status": "local_GR_still_blocked",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4357_0_common_mode_grammar",
            "statement": "If the parent matter/source grammar has no source-only pre-variation action weight, one action-measure owner, quotient source-normalization silence, Hilbert current ownership before readout, and no independent range pole, then transition q_tr has no source-label or range hair.",
            "derived_result": "D_species q_tr=D_frame q_tr=D_source_weight q_tr=D_lambda q_tr=0, hence Y_species_frame_source=Y_lambda=0",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4357_1_wA_counterexample",
            "statement": "Classical matter equations and current-owner arguments do not by themselves remove w_A inserted before metric variation.",
            "derived_result": "pre-variation source/action weight remains the highest-pressure source-coupling gremlin",
            "current_status": "COUNTEREXAMPLE_ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4357_2_first_finite_inputs",
            "statement": "When the grammar theorem is unsigned, the honest fallback is finite source-backed inputs, not another assumption.",
            "derived_result": "WEP Delta_w*tau anchor and R10 alpha(lambda) threshold anchors are imported into the transition hair ledger as nonclaim inputs",
            "current_status": "FINITE_INPUTS_IMPORTED_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4357_3_no_local_GR_reentry",
            "statement": "Local GR/Newton cannot be claimed while w_A/source-label or range hair is open, even if some bound anchors exist.",
            "derived_result": "4357 moves from blank missing rows to bounded-input plumbing, but not to a pass",
            "current_status": "FIREWALL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for arena, observable, requirement in ARENAS:
        rows.append(
            {
                "arena_id": f"AR4357_{arena}",
                "arena": arena,
                "observable": observable,
                "4357_status": requirement,
                "zero_route": "parent common-mode grammar/action-measure/range-free theorem",
                "finite_route": "source-backed rows with tau/profile/readout/kernels before scoring",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4357_0_theorem_zero",
            "input": "all grammar/action-measure/current-owner/source-silence/range-free gates signed on the same transition branch",
            "action": "SET_COMMON_MODE_HAIR_ZERO",
            "result": "Y_species_frame_source=0 and Y_lambda=0",
            "current_result": "REJECT_ZERO_CLAIM_NOW",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4357_1_wA_counterexample",
            "input": "classical EOM or current owner only",
            "action": "TEST_IF_WA_KILLED",
            "result": "w_A survives if inserted before variation",
            "current_result": "KEEP_DELTA_W_ROWS",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4357_2_WEP_anchor",
            "input": "R1_WEP_source_charge bound anchor",
            "action": "IMPORT_AS_FINITE_INPUT_ONLY",
            "result": "abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15; tau/source/readout missing",
            "current_result": "BOUND_INPUT_NOT_SCORE",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4357_3_R10_anchor",
            "input": "Eot-Wash anchor smoke rows",
            "action": "IMPORT_AS_RANGE_INPUT_ONLY",
            "result": "alpha_bound anchors exist; full curve and numeric parent alpha missing",
            "current_result": "ANCHOR_INPUT_NOT_SCORE",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4357_4_next",
            "input": "grammar theorem unsigned but first finite anchors available",
            "action": "BRIDGE_TO_ACTION_MEASURE_OR_TAU_WEP",
            "result": NEXT_TARGET,
            "current_result": "NEXT_TARGET_SELECTED",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4357_0",
            "rule": "Do not declare source-label forgetting from classical equations alone.",
            "reason": "pre-variation w_A preserves isolated matter equations while changing Hilbert source variation.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4357_1",
            "rule": "Do not absorb relative w_A, beta_w, finite-range or time-varying transition hair into measured G.",
            "reason": "only common constant derivative-silent source normalization is calibration.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4357_2",
            "rule": "Do not score WEP from the MICROSCOPE bound anchor without tau_WEP/source-worldtube/readout projection.",
            "reason": "the imported row is a bound-only input, not an MTS prediction.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4357_3",
            "rule": "Do not score R10 from alpha=1 anchors without a full curve and numeric MTS alpha coefficients.",
            "reason": "anchor rows are provenance plumbing, not claim-grade exclusions.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4357_4",
            "rule": "Do not claim local GR/Newton while source/action weight or range hair remains open.",
            "reason": "4357 narrows and imports inputs, but it does not close the common-mode package.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4357_0",
            "decision": DECISION,
            "reason": "4357 attacks the common-mode source/coupling gate directly. The exact theorem route is now written as a parent grammar/action-measure/operator package: no pre-variation source-only action weight w_A, one action-measure owner, quotient source-normalization silence, Hilbert current before readout, and no independent range pole. If that package closed, Y_species_frame_source and Y_lambda would vanish. It does not close from current evidence: w_A remains an active counterexample to classical-EOM/current-owner shortcuts. The concrete forward move is finite-input import: MICROSCOPE supplies a source-backed bound-only WEP anchor for abs(Delta_w_TiPt*tau_WEP)<=2.8e-15, and Eot-Wash supplies source-backed R10 alpha=1 threshold anchors. Both are nonclaim inputs, not scores.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4357_0",
            "item": "common-mode grammar",
            "status": "EXACT_CONDITIONAL_GATE_WRITTEN",
            "note": "Would kill source-label and range hair if parent-signed on the transition branch.",
        },
        {
            "status_id": "STAT4357_1",
            "item": "w_A",
            "status": "ACTIVE_COUNTEREXAMPLE",
            "note": "Classical equations/current owner do not remove pre-variation action weights.",
        },
        {
            "status_id": "STAT4357_2",
            "item": "WEP finite input",
            "status": "SOURCE_BACKED_BOUND_ANCHOR_IMPORTED",
            "note": "abs(Delta_w_TiPt*tau_WEP)<=2.8e-15 is bound-only and nonclaim.",
        },
        {
            "status_id": "STAT4357_3",
            "item": "R10 finite input",
            "status": "SOURCE_BACKED_THRESHOLD_ANCHORS_IMPORTED",
            "note": "alpha=1 at 38.6um/56um is anchor-only; full curve and MTS alpha coefficients missing.",
        },
        {
            "status_id": "STAT4357_4",
            "item": "next target",
            "status": "ACTION_MEASURE_OR_TAU_WEP_BRIDGE",
            "note": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4357_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the parent action-measure owner be derived strongly enough to kill w_A, or can tau_WEP/source projection turn the WEP anchor into a real Delta_w constraint?",
            "preferred_route": "derive one universal parent action measure/hbar owner from MTS primitives; this is the cleanest way to kill pre-variation w_A",
            "fallback_route": "derive/source tau_WEP, source worldtube and readout kernel so the 2.8e-15 product anchor becomes a usable finite Delta_w row",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "grammar": grammar_gate_rows(),
        "counterexamples": counterexample_rows(),
        "finite_inputs": finite_input_rows(),
        "updated_hair": updated_hair_rows(),
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
        "sources": "P8_Y5_R2FR_4357_SOURCE_REGISTER.csv",
        "grammar": "P8_Y5_R2FR_4357_GRAMMAR_GATE_ROWS.csv",
        "counterexamples": "P8_Y5_R2FR_4357_COUNTEREXAMPLE_ROWS.csv",
        "finite_inputs": "P8_Y5_R2FR_4357_FINITE_INPUT_ROWS.csv",
        "updated_hair": "P8_Y5_R2FR_4357_UPDATED_HAIR_ROWS.csv",
        "theorems": "P8_Y5_R2FR_4357_THEOREM_ROWS.csv",
        "arenas": "P8_Y5_R2FR_4357_ARENA_ROWS.csv",
        "runner": "P8_Y5_R2FR_4357_RUNNER.csv",
        "firewall": "P8_Y5_R2FR_4357_CLAIM_FIREWALL.csv",
        "decision": "P8_Y5_R2FR_4357_DECISION.csv",
        "status": "P8_Y5_R2FR_4357_STATUS.csv",
        "next": "P8_Y5_R2FR_4357_NEXT_TARGET.csv",
    }
    for key, filename in mapping.items():
        write_csv(SOURCE_DIR / filename, tables[key])


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 373 PPC4161 transition common-mode parent grammar or first finite hair inputs

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4357 does not prove public local GR, Newton, R10, PPN, WEP, clock, orbital, EM, or transition-shell safety.

## Result

4357 goes after the coupling/source gremlin directly.

The clean common-mode theorem would be:

```text
Allowed[S_matter] =
  sum_A S_A[Psi_A, e_obs(q), A_Q, theta_A]
```

with no independent pre-variation source/action multiplier:

```text
w_A S_A.
```

Together with one parent action-measure owner, quotient source-normalization silence, Hilbert current ownership before readout, and no independent range pole, this would imply:

```text
D_species q_tr = 0,
D_frame q_tr = 0,
D_source_weight q_tr = 0,
D_lambda q_tr = 0,
Y_species_frame_source = 0,
Y_lambda = 0.
```

That is the exact low-scrutiny route for making the transition contribution a common source dressing rather than a hidden fifth force.

But the proof does **not** close yet. The live counterexample is:

```text
S_matter -> sum_A w_A S_A
```

inserted before variation. Classical matter equations can look unchanged while the Hilbert metric variation inherits `w_A T_A`. Current-owner arguments kill post-variation rescalings only after a common action is fixed; they do not kill pre-variation weights.

## Forward Move

This checkpoint therefore imports first finite inputs instead of circling empty rows:

```text
abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15
```

as a source-backed MICROSCOPE bound-only anchor for `Y_species_frame_source`.

And:

```text
alpha_bound(lambda=3.86e-5 m) = 1,
alpha_bound(lambda=5.6e-5 m) = 1
```

as source-backed Eot-Wash threshold anchors for `Y_lambda`.

These are not MTS predictions and not claim-grade scores. They are real input plumbing: the next bridge is either derive the action-measure owner that kills `w_A`, or derive/source `tau_WEP`, the source worldtube and readout kernel so the WEP anchor becomes a usable finite `Delta_w` constraint.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Grammar Gate Rows

{md_table(tables["grammar"], ["gate_id", "required_statement", "would_derive", "evidence_now", "status", "valid_for_claim"])}

## Counterexample Rows

{md_table(tables["counterexamples"], ["counterexample_id", "counterexample", "why_it_survives", "kills_fake_proof", "residual_if_survives", "status", "valid_for_claim"])}

## Finite Input Rows

{md_table(tables["finite_inputs"], ["input_id", "hair_component", "quantity", "value", "units", "source_path", "source_anchor", "extraction_method", "what_this_gives", "what_is_missing", "score_ready", "valid_for_claim"])}

## Updated Hair Rows

{md_table(tables["updated_hair"], ["hair_id", "4356_component", "old_status", "4357_update", "current_law", "finite_input", "claim_status", "valid_for_claim"])}

## Theorem Rows

{md_table(tables["theorems"], ["theorem_id", "statement", "derived_result", "current_status", "claim_allowed", "valid_for_claim"])}

## Arena Rows

{md_table(tables["arenas"], ["arena_id", "arena", "observable", "4357_status", "zero_route", "finite_route", "claim_allowed", "valid_for_claim"])}

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
    post = f"""# 4357 Y5-R2FR transition common-mode parent grammar or first finite hair inputs

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4357 tried the proof path first. The exact zero route is:

```text
no pre-variation w_A
+ one action-measure owner
+ quotient source-normalization silence
+ Hilbert current before readout
+ no range pole
=> Y_species_frame_source=0 and Y_lambda=0.
```

But `w_A` still survives as the live counterexample, so no theorem-zero claim fires.

Concrete progress: first finite inputs are now imported:

```text
abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15
alpha_bound(38.6um)=1
alpha_bound(56um)=1
```

All are nonclaim anchors. Next: action-measure owner proof, or `tau_WEP`/source/readout projection.

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
                    "4357 attacks the transition common-mode source/coupling gate. The exact zero route is a parent grammar/action-measure/operator package: no pre-variation source-only action weight w_A, one action-measure owner, quotient source-normalization silence, Hilbert current ownership before readout, and no independent finite-range pole. If this package closed on the same transition branch, D_species q_tr, D_frame q_tr, D_source_weight q_tr and D_lambda q_tr would vanish, killing Y_species_frame_source and Y_lambda. Current evidence does not close the package: w_A remains an active counterexample because classical matter equations and post-variation current-owner arguments do not remove weights inserted before metric variation. The checkpoint imports first finite inputs instead: a MICROSCOPE source-backed bound-only anchor abs(Delta_w_TiPt*tau_WEP)<=2.8e-15 and Eot-Wash alpha=1 threshold anchors at 38.6um and 56um. These are nonclaim anchors, not MTS predictions or local-test passes."
                ),
                (
                    "4357 source register, grammar gate rows, counterexample rows, finite input rows, updated hair rows, theorem rows, arena rows, runner, firewall, decision, status, next-target and validation CSV."
                ),
                "common_mode_grammar_gate_unsigned_first_finite_WEP_R10_inputs_nonclaim",
                (
                    "Derive the parent action-measure owner that kills w_A, or derive/source tau_WEP, source worldtube and readout kernel so the WEP anchor can become a usable Delta_w constraint."
                ),
                (
                    "Declaring source-label forgetting from classical equations alone; absorbing relative or range hair into measured G; using MICROSCOPE/R10 anchors as MTS predictions; scoring WEP/R10 without tau/source/readout/full-curve/parent-alpha inputs; claiming local GR while w_A or lambda hair survives."
                ),
            ]
        )


def append_spine_and_packet() -> None:
    spine_block = f"""

## PPC4161 4357 transition common-mode grammar gate and first finite inputs

Marker: `{MARKER}`

4357 identifies the live coupling gremlin as the pre-variation source/action weight:

```text
S_matter -> sum_A w_A S_A.
```

The exact zero route is no `w_A`, one action-measure owner, quotient source-normalization silence, Hilbert current before readout and no range pole. If those close on the transition branch, `Y_species_frame_source=Y_lambda=0`.

They do not close yet. Progress is finite input plumbing: MICROSCOPE gives `abs(Delta_w_TiPt*tau_WEP)<=2.8e-15` as a bound-only anchor, and Eot-Wash gives `alpha=1` threshold anchors at 38.6um and 56um. These are not predictions or passes; they are the first real inputs for the finite route.
"""
    packet_block = f"""

## PPC4161 packet update 4357 common-mode grammar and finite inputs

Marker: `{PACKET_MARKER}`

Packet update: source-label forgetting now reduces to defeating pre-variation `w_A` through a parent action-measure/grammar theorem. Since that theorem is unsigned, 4357 imports nonclaim WEP and R10 finite anchors instead of pretending the row is zero.
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
    checks.append(("wa_counterexample_present", "S_matter -> sum_A w_A S_A" in formal_text, "w_A counterexample"))
    checks.append(("grammar_formula_present", "Allowed[S_matter]" in formal_text, "allowed matter grammar"))
    checks.append(("wep_anchor_present", "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15" in formal_text, "WEP bound anchor"))
    checks.append(("r10_anchor_present", "alpha_bound(lambda=3.86e-5 m) = 1" in formal_text, "R10 anchor"))
    checks.append(("y_species_present", "Y_species_frame_source = 0" in formal_text, "Y species zero route"))
    checks.append(("y_lambda_present", "Y_lambda = 0" in formal_text, "Y lambda zero route"))
    checks.append(("all_sources_exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source paths"))
    checks.append(("all_needles_found", all(row["needle_found"] == "True" for row in tables["sources"]), "source needles"))
    checks.append(("grammar_rows_present", len(tables["grammar"]) >= 6, str(len(tables["grammar"]))))
    checks.append(("counterexample_rows_present", len(tables["counterexamples"]) >= 4, str(len(tables["counterexamples"]))))
    checks.append(("finite_inputs_present", len(tables["finite_inputs"]) >= 3, str(len(tables["finite_inputs"]))))
    checks.append(("updated_hair_present", len(tables["updated_hair"]) >= 3, str(len(tables["updated_hair"]))))
    checks.append(("theorem_rows_present", len(tables["theorems"]) >= 4, str(len(tables["theorems"]))))
    checks.append(("arena_rows_present", len(tables["arenas"]) == len(ARENAS), str(len(tables["arenas"]))))
    checks.append(("no_score_ready_inputs", all(row.get("score_ready", "False") == "False" for row in tables["finite_inputs"]), "finite inputs remain non-score"))
    checks.append(("no_valid_claim_rows", all(row.get("valid_for_claim") == "False" for rows in tables.values() for row in rows if "valid_for_claim" in row), "all generated claim flags false"))
    checks.append(("claim_row_recorded", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID))
    checks.append(("spine_marker_recorded", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER))
    checks.append(("packet_marker_recorded", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER))
    for filename in [
        "P8_Y5_R2FR_4357_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4357_GRAMMAR_GATE_ROWS.csv",
        "P8_Y5_R2FR_4357_COUNTEREXAMPLE_ROWS.csv",
        "P8_Y5_R2FR_4357_FINITE_INPUT_ROWS.csv",
        "P8_Y5_R2FR_4357_UPDATED_HAIR_ROWS.csv",
        "P8_Y5_R2FR_4357_THEOREM_ROWS.csv",
        "P8_Y5_R2FR_4357_ARENA_ROWS.csv",
        "P8_Y5_R2FR_4357_RUNNER.csv",
        "P8_Y5_R2FR_4357_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4357_DECISION.csv",
        "P8_Y5_R2FR_4357_STATUS.csv",
        "P8_Y5_R2FR_4357_NEXT_TARGET.csv",
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
