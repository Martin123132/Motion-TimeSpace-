from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4355"
CLAIM_ID = "L-196"
BRANCH = "MTS_R2FR_Y5_TRANSITION_SHELL_SAME_WORLDTUBE_NONHILBERT_RESIDUE_OR_BOUNDED_SOURCE_HAIR_4355"
DECISION = "TRANSITION_SOURCE_KERNEL_HAIR_LAW_DERIVED_OWNER_CHANNEL_IMPORTED_FINITE_HAIR_VECTOR_RETAINED_NONCLAIM"
MARKER = "PPC4161_TRANSITION_SHELL_SAME_WORLDTUBE_NONHILBERT_RESIDUE_OR_BOUNDED_SOURCE_HAIR_4355"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SHELL_SAME_WORLDTUBE_NONHILBERT_RESIDUE_OR_BOUNDED_SOURCE_HAIR_4355"
NEXT_TARGET = "4356-Y5-R2FR-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md"

FORMAL_PATH = FORMAL / "371-PPC4161-transition-shell-same-worldtube-nonHilbert-residue-or-bounded-source-hair.md"
DOC_PATH = POST / "4355-Y5-R2FR-transition-shell-same-worldtube-nonHilbert-residue-or-bounded-source-hair.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4355_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4355_00_4354_next": (
        FORMAL / "370-PPC4161-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md",
        "4355-Y5-R2FR-transition-shell-same-worldtube-nonHilbert-residue-or-bounded-source-hair.md",
        "4354 handoff to transition source hair.",
    ),
    "SRC4355_01_310_kernel_zero": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "P_leak q_tr = 0.",
        "Conditional transition source-kernel zero theorem.",
    ),
    "SRC4355_02_310_kernel_definition": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "P_kernel := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube,",
        "Kernel projector definition.",
    ),
    "SRC4355_03_310_source_dressing": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "then the transition residue is only a common static Hilbert monopole before readout",
        "If the kernel clauses hold, transition is source dressing.",
    ),
    "SRC4355_04_306_epsilon_mu": (
        FORMAL / "306-PPC4161-transition-Hilbert-monopole-source-lock-or-first-residual-bound-row.md",
        "epsilon_mu_tr = mu_extra_tr/(G_cal M_H^dress).",
        "Transition non-EH monopole residual definition.",
    ),
    "SRC4355_05_308_hair_vector": (
        FORMAL / "308-PPC4161-transition-membership-and-nonEH-monopole-zero-or-shared-residual-vector.md",
        "Q_l>=1_tr,",
        "Shared residual vector includes multipole/source hair.",
    ),
    "SRC4355_06_4293_empirical_fail": (
        POST / "4293-Y5-R2FR-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md",
        "Unit projection into WEP, PPN gamma/beta, clock, orbital and one-year Gdot rows fails.",
        "Rough epsilon_mu_tr is far too large for local precision if not structurally killed.",
    ),
    "SRC4355_07_354_pleak": (
        FORMAL / "354-PPC4161-cGamma-transition-source-kernel-coefficient-fill-or-metric-null-proof.md",
        "P_leak   := I - P_kernel",
        "Seven-component leak projector definition.",
    ),
    "SRC4355_08_354_components": (
        FORMAL / "354-PPC4161-cGamma-transition-source-kernel-coefficient-fill-or-metric-null-proof.md",
        "P_time_multipole",
        "Remaining source-hair component list.",
    ),
    "SRC4355_09_358_qtr_split": (
        FORMAL / "358-PPC4161-KL-generator-for-KGamma-and-CRI-CDeltaKdiv-zero-branch.md",
        "q_tr = -div Delta_K + C_RI + C_conn + B_boundary",
        "Non-Hilbert route reduced to DeltaK divergence and commutators.",
    ),
    "SRC4355_10_358_CRI_zero": (
        FORMAL / "358-PPC4161-KL-generator-for-KGamma-and-CRI-CDeltaKdiv-zero-branch.md",
        "C_RI^flat = 0",
        "Fixed flat-patch right-inverse commutator zero branch.",
    ),
    "SRC4355_11_369_owner_deleted": (
        FORMAL / "369-PPC4161-full-clean-owner-tail-to-local-residual-vector-or-finite-score.md",
        "epsilon_owner_tail_Kperp=0",
        "Owner-tail/Kperp channel deleted from the compact private vector.",
    ),
    "SRC4355_12_4339_trace": (
        POST / "4339-Y5-R2FR-PnonHilbert-and-worldtube-transition-leak-zero-proof-or-bound-runner.md",
        "P_off_worldtube -> N_inner <= ||mu_tr|| + ||B_src^A||",
        "Worldtube/readout-order leakage reduced to trace-defect bound.",
    ),
    "SRC4355_13_356_full_domain": (
        FORMAL / "356-PPC4161-DvKhat-DeltaK-and-worldtube-trace-defect-input-fill.md",
        "P_off_worldtube_readout_order=0 on the full-domain/post-solve restriction branch.",
        "Full-domain-before-readout branch kills off-worldtube leakage conditionally.",
    ),
    "SRC4355_14_4354_Gsrc": (
        FORMAL / "370-PPC4161-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md",
        "Delta_worldtube_species.",
        "4354 finite source/coupling envelope receives transition source hair.",
    ),
}

ARENAS = [
    ("PPN_gamma_beta", "gamma/beta/preferred-frame response to transition source hair"),
    ("WEP_species", "species-dependent transition source weights"),
    ("R10_range", "finite-range transition hair in alpha(lambda) rows"),
    ("clock_Gdot", "time-dependent transition source charge or G_cal drift"),
    ("orbital_GM", "transition source dressing versus measured orbital GM"),
    ("local_Newton_GR", "whether q_tr enters M_Hdress or a separate local metric residual"),
    ("EM_Poynting", "whether transition current double-counts visible EM/Poynting stress"),
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


def kernel_membership_rows() -> List[Dict[str, str]]:
    return [
        {
            "kernel_id": "KM4355_0_Hilbert_action_domain",
            "projector_leg": "P_Hilbert",
            "zero_condition": "q_tr = delta S_tr^H[g_obs,chi;tau]/delta g_obs inside the same Hilbert source block with no representative-only source slot",
            "clean_output": "P_nonHilbert_action_domain q_tr = 0",
            "fallback_residual": "Y_nonHilbert <= C_NH(C_DeltaKdiv + C_RI + C_conn + C_boundary)",
            "current_status": "OWNER_CHANNEL_IMPORTED_PRIVATE_ZERO_BRANCH_NOT_GLOBAL",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KM4355_1_same_worldtube_readout",
            "projector_leg": "same-worldtube",
            "zero_condition": "transition support is included in W_H before variation and exterior restriction is post-solve readout",
            "clean_output": "P_off_worldtube_readout_order q_tr = 0",
            "fallback_residual": "Delta_Wtr <= N_inner/M_H_ref <= (||mu_tr||+||B_src^A||)/M_H_ref",
            "current_status": "FULL_DOMAIN_BRANCH_CONDITIONAL_TRACE_DEFECT_BOUND_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KM4355_2_static_monopole",
            "projector_leg": "l=0 static",
            "zero_condition": "partial_tau q_tr=0 and Q_l>=1_tr=0 on the source-kernel branch",
            "clean_output": "no time or multipole transition hair",
            "fallback_residual": "Y_time_l >= |partial_tau q_tr|/M_H_ref + sum_l>=1 |Q_l,tr|/M_H_ref",
            "current_status": "OPEN_NEXT_PROOF_TARGET",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KM4355_3_universal_species_frame",
            "projector_leg": "universal/species/frame/source-weight blind",
            "zero_condition": "D_species q_tr = D_frame q_tr = D_source_weight q_tr = 0",
            "clean_output": "no WEP/preferred-frame/source-label transition hair",
            "fallback_residual": "Y_species_frame >= |D_species q_tr| + |D_frame q_tr| + |Delta_source_weight_tr|",
            "current_status": "OPEN_NEXT_PROOF_TARGET",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KM4355_4_range_free",
            "projector_leg": "range-free/common long-range monopole",
            "zero_condition": "transition source is not a finite-range Yukawa or lambda-dependent test/source leg",
            "clean_output": "no R10/range transition hair",
            "fallback_residual": "Y_range >= |D_lambda q_tr| + |q_range_tail|",
            "current_status": "OPEN_NEXT_PROOF_TARGET",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KM4355_5_same_metric_EH",
            "projector_leg": "same-metric/EH readout",
            "zero_condition": "q_tr uses the same observed metric/coframe/EH readout as matter, EM, clocks and local tests",
            "clean_output": "P_nonEH_metric_readout q_tr = 0",
            "fallback_residual": "Y_nonEH >= ||Pi_arena Sigma_nonEH[q_tr]||",
            "current_status": "OPEN_BUT_CONSTRAINED_BY_PRIVATE_EH_COFRAME_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KM4355_6_boundary_nonlocal_owner",
            "projector_leg": "boundary/nonlocal owner",
            "zero_condition": "boundary/nonlocal part is owned before variation and either routed to Hamiltonian boundary charge or proved projection-null",
            "clean_output": "P_boundary_nonlocal_owner q_tr = 0",
            "fallback_residual": "Y_boundary_nonlocal >= |B_tr_nonlocal|/M_H_ref",
            "current_status": "OPEN_NEXT_PROOF_TARGET",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KM4355_7_total_kernel",
            "projector_leg": "P_kernel",
            "zero_condition": "KM4355_0 through KM4355_6 all hold on the same branch",
            "clean_output": "q_tr=P_kernel q_tr, P_leak q_tr=0, epsilon_mu_tr=0, Q_l>=1_tr=0",
            "fallback_residual": "epsilon_tr_hair finite no-cancellation vector",
            "current_status": "CONDITIONAL_THEOREM_NOT_PUBLIC_CLAIM",
            "valid_for_claim": "False",
        },
    ]


def cleanup_import_rows() -> List[Dict[str, str]]:
    return [
        {
            "import_id": "CI4355_0_Khat_Gamma_split",
            "imported_result": "q_tr = -div Delta_K + C_RI + C_conn + B_boundary",
            "effect_on_4355": "P_nonHilbert no longer needs to score standalone D_v Gamma_eff if the Khat/KGamma right-inverse branch is adopted",
            "remaining_condition": "projected div Delta_K, C_RI, C_conn and boundary terms must be zero or bounded",
            "status": "REAL_NARROWING",
            "valid_for_claim": "False",
        },
        {
            "import_id": "CI4355_1_CRI_flat",
            "imported_result": "C_RI^flat = 0 on fixed flat boundary/projection branch",
            "effect_on_4355": "right-inverse commutator is not a mystery on the fixed weak-field patch",
            "remaining_condition": "curved/boundary/projection variations reopen C_RI unless signed or bounded",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "import_id": "CI4355_2_Kperp_owner_deleted",
            "imported_result": "epsilon_owner_tail_Kperp=0 in the compact private clean branch",
            "effect_on_4355": "the Kperp/RI owner-tail channel is no longer the active transition-source blocker inside that branch",
            "remaining_condition": "raw transition source-kernel membership and other P_leak hairs remain unsigned",
            "status": "PRIVATE_BRANCH_ZERO_IMPORTED",
            "valid_for_claim": "False",
        },
        {
            "import_id": "CI4355_3_full_domain_readout",
            "imported_result": "P_off_worldtube_readout_order=0 on the full-domain/post-solve restriction branch",
            "effect_on_4355": "off-worldtube leakage can be killed by ordering variation before exterior readout",
            "remaining_condition": "exterior-first readouts retain mu_tr and B_src^A trace-defect rows",
            "status": "CONDITIONAL_ZERO_WITH_BOUND_FALLBACK",
            "valid_for_claim": "False",
        },
        {
            "import_id": "CI4355_4_rough_epsilon_fail",
            "imported_result": "epsilon_AJ_seed=0.08394692185032419 fails unit projection into WEP/PPN/clock/orbital/Gdot rows",
            "effect_on_4355": "finite transition hair must be structurally zeroed or strongly projection-suppressed; rough direct scoring is not enough",
            "remaining_condition": "source-backed projection constants and much stronger suppression if any hair survives",
            "status": "EMPIRICAL_PRESSURE_RETAINED",
            "valid_for_claim": "False",
        },
    ]


def source_hair_bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "HB4355_0_nonHilbert",
            "hair_component": "Y_nonHilbert",
            "formula": "Y_nonHilbert <= C_NH(C_DeltaKdiv + C_RI + C_conn + C_boundary)",
            "zero_if": "Hilbert action-domain ownership plus imported Khat/KGamma/Kperp clean branch closes",
            "feeds": "epsilon_tr_hair; epsilon_Gsrc; PPN/R10/clock/orbital/WEP projections",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4355_1_worldtube",
            "hair_component": "Delta_Wtr",
            "formula": "Delta_Wtr <= N_inner/M_H_ref <= (||mu_tr||+||B_src^A||)/M_H_ref",
            "zero_if": "same W_H full-domain-before-readout branch is parent-signed",
            "feeds": "Delta_worldtube_species; source normalization",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4355_2_time_multipole",
            "hair_component": "Y_time_l",
            "formula": "Y_time_l >= |partial_tau q_tr|/M_H_ref + sum_l>=1 |Q_l,tr|/M_H_ref",
            "zero_if": "q_tr is static l=0 in the local source kernel",
            "feeds": "PPN preferred-frame, clock, orbital, radiation/source hair",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4355_3_species_frame_source",
            "hair_component": "Y_species_frame",
            "formula": "Y_species_frame >= |D_species q_tr| + |D_frame q_tr| + |Delta_source_weight_tr|",
            "zero_if": "transition current forgets species/frame/source labels before variation",
            "feeds": "WEP, PPN preferred-frame, source normalization",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4355_4_range",
            "hair_component": "Y_range",
            "formula": "Y_range >= |D_lambda q_tr| + |q_range_tail|",
            "zero_if": "transition source is range-free/common-monopole rather than finite-range",
            "feeds": "R10 alpha(lambda), orbital range tests",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4355_5_nonEH_metric",
            "hair_component": "Y_nonEH",
            "formula": "Y_nonEH >= ||Pi_arena Sigma_nonEH[q_tr]||",
            "zero_if": "same EH/same-metric readout branch owns the transition response",
            "feeds": "PPN gamma/beta/preferred-frame and local Newton metric residuals",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4355_6_boundary_nonlocal",
            "hair_component": "Y_boundary_nonlocal",
            "formula": "Y_boundary_nonlocal >= |B_tr_nonlocal|/M_H_ref",
            "zero_if": "boundary/nonlocal owner is routed to Hamiltonian boundary charge or projection-null",
            "feeds": "clocks, orbital, PPN, local closure",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HB4355_7_total",
            "hair_component": "epsilon_tr_hair",
            "formula": "epsilon_tr_hair <= Y_nonHilbert + Delta_Wtr + Y_time_l + Y_species_frame + Y_range + Y_nonEH + Y_boundary_nonlocal",
            "zero_if": "q_tr=P_kernel q_tr and imported owner/readout branches close on one selector",
            "feeds": "epsilon_Gsrc <- epsilon_Gsrc + epsilon_tr_hair",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4355_0_clean_transition_source",
            "statement": "If q_tr=P_kernel q_tr with Hilbert, same-worldtube, static l=0, universal, range-free, same-metric and boundary-owned clauses, then P_leak q_tr=0.",
            "consequence": "transition residue renormalizes M_Hdress rather than creating a separate local metric/source leak; epsilon_mu_tr=0 and Q_l>=1_tr=0",
            "status": "CONDITIONAL_THEOREM_IMPORTED_AND_ASSEMBLED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4355_1_nonHilbert_owner_cleanup",
            "statement": "Inside the compact private clean branch, the Khat/Gamma/Kperp owner leg is not the active transition blocker after 4340-4353.",
            "consequence": "4355 can focus on source-kernel membership and remaining hair rather than re-scoring the deleted owner-tail/Kperp channel",
            "status": "PRIVATE_BRANCH_NARROWING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4355_2_finite_hair_fallback",
            "statement": "If any kernel clause fails, the residual is epsilon_tr_hair with absolute no-cancellation component rows.",
            "consequence": "transition hair feeds epsilon_Gsrc and local arena projections; rough epsilon_mu_tr scoring already fails ordinary precision rows",
            "status": "FINITE_BOUND_VECTOR_RETAINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4355_3_no_raw_shell_pass",
            "statement": "Raw transition-shell direct projection remains nonclaim unless the source-kernel clauses are parent-signed or finite rows are sourced and pass.",
            "consequence": "no public local-GR, R10, PPN, WEP, clock or orbital claim fires from 4355",
            "status": "FIREWALL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for arena, observable in ARENAS:
        rows.append(
            {
                "arena_id": f"AR4355_{arena}",
                "arena": arena,
                "observable": observable,
                "clean_branch": "epsilon_tr_hair=0; transition current enters only M_Hdress as common Hilbert monopole",
                "finite_branch": "project Pi_arena epsilon_tr_hair components with source-backed constants fixed before scoring",
                "current_status": "NO_PASS_FROM_4355_ALONE",
                "valid_for_claim": "False",
            }
        )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4355_0_clean",
            "input": "all KM4355 kernel clauses plus imported 4353/4354 private source branch",
            "action": "ROUTE_TRANSITION_TO_COMMON_SOURCE_DRESSING",
            "result": "P_leak q_tr=0, epsilon_tr_hair=0, epsilon_mu_tr=0, Q_l>=1_tr=0",
            "claim_policy": "private conditional theorem only; global parent adoption and empirical projections still required",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4355_1_partial_owner",
            "input": "Khat/Kperp owner channel clean but source-kernel hair clauses unsigned",
            "action": "DELETE_OWNER_CHANNEL_ONLY_RETAIN_HAIR_VECTOR",
            "result": "do not re-score owner-tail/Kperp; keep time/multipole/species/frame/range/nonEH/boundary hair",
            "claim_policy": "no local-GR claim",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4355_2_finite",
            "input": "any transition kernel clause open",
            "action": "KEEP_EPSILON_TR_HAIR_BOUND",
            "result": "epsilon_Gsrc receives epsilon_tr_hair with no cancellation",
            "claim_policy": "requires numeric/theorem-zero component rows and arena projections before scoring",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4355_3_next",
            "input": "first two leak channels narrowed; remaining hair open",
            "action": "ATTACK_STATIC_MONOPOLE_UNIVERSAL_RANGEFREE_HAIR",
            "result": NEXT_TARGET,
            "claim_policy": "derive source-kernel membership or fill finite hair rows",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4355_0",
            "rule": "Do not treat raw transition shells as local-GR safe because compact-collar owner channels are clean.",
            "reason": "raw q_tr still needs source-kernel membership or finite hair bounds.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4355_1",
            "rule": "Do not call epsilon_mu_tr=0 unless q_tr=P_kernel q_tr on the same branch.",
            "reason": "the transition residue must be Hilbert, same-worldtube, static l=0, universal, range-free, same-metric and boundary-owned.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4355_2",
            "rule": "Do not use the rough epsilon_mu_tr=0.08394692185032419 as evidence of local safety.",
            "reason": "4293 shows unit projection fails WEP/PPN/clock/orbital/Gdot rows.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4355_3",
            "rule": "Do not cancel transition hair components across sectors.",
            "reason": "epsilon_tr_hair is an absolute no-cancellation envelope.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4355_4",
            "rule": "Do not define source-kernel membership after seeing local-test residuals.",
            "reason": "P_kernel clauses must be parent/readout selected before variation and empirical scoring.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4355_0",
            "decision": DECISION,
            "reason": "4355 assembles the transition source-kernel law and imports the 4340-4353 owner-channel progress. In the compact private branch, the Khat/Gamma/Kperp owner leg is no longer the main active source blocker. The remaining clean route is exact: q_tr must be Hilbert, same-worldtube, static l=0, universal, range-free, same-metric and boundary-owned, so q_tr=P_kernel q_tr and P_leak q_tr=0. Then the transition only dresses M_Hdress and epsilon_mu_tr=Q_l>=1_tr=epsilon_tr_hair=0. The current corpus does not parent-sign all those source-kernel clauses for raw transition shells, so 4355 retains epsilon_tr_hair as a finite no-cancellation vector feeding epsilon_Gsrc.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4355_0",
            "item": "transition owner channel",
            "status": "NARROWED_PRIVATE_CLEAN_BRANCH",
            "note": "Khat/Gamma/Kperp owner leg is imported as clean only inside the compact private branch.",
        },
        {
            "status_id": "STAT4355_1",
            "item": "source kernel",
            "status": "CONDITIONAL_THEOREM_ASSEMBLED",
            "note": "q_tr=P_kernel q_tr gives P_leak q_tr=0 and source dressing.",
        },
        {
            "status_id": "STAT4355_2",
            "item": "raw transition shell",
            "status": "NOT_PARENT_SIGNED_INTO_KERNEL",
            "note": "No public local-GR claim; finite source-hair vector remains.",
        },
        {
            "status_id": "STAT4355_3",
            "item": "epsilon_tr_hair",
            "status": "FINITE_NO_CANCELLATION_BOUND",
            "note": "Feeds epsilon_Gsrc if any kernel leg opens.",
        },
        {
            "status_id": "STAT4355_4",
            "item": "next target",
            "status": "STATIC_MONOPOLE_UNIVERSAL_RANGEFREE",
            "note": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4355_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the remaining transition source-kernel hair be killed by proving static l=0, universal/species-frame blind, range-free, same-metric and boundary-owned membership?",
            "preferred_route": "derive partial_tau q_tr=0, Q_l>=1_tr=0, D_species/frame/source q_tr=0 and D_lambda q_tr=0 from the parent Hamiltonian/Hilbert source selector",
            "fallback_route": "fill finite source-backed rows for time/multipole, species/frame/source-weight, range, nonEH metric and boundary/nonlocal hair",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "kernel": kernel_membership_rows(),
        "cleanup": cleanup_import_rows(),
        "hair": source_hair_bound_rows(),
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
        "sources": "P8_Y5_R2FR_4355_SOURCE_REGISTER.csv",
        "kernel": "P8_Y5_R2FR_4355_KERNEL_MEMBERSHIP_ROWS.csv",
        "cleanup": "P8_Y5_R2FR_4355_CLEANUP_IMPORT_ROWS.csv",
        "hair": "P8_Y5_R2FR_4355_SOURCE_HAIR_BOUND_ROWS.csv",
        "theorems": "P8_Y5_R2FR_4355_THEOREM_ROWS.csv",
        "arenas": "P8_Y5_R2FR_4355_ARENA_ROWS.csv",
        "runner": "P8_Y5_R2FR_4355_RUNNER.csv",
        "firewall": "P8_Y5_R2FR_4355_CLAIM_FIREWALL.csv",
        "decision": "P8_Y5_R2FR_4355_DECISION.csv",
        "status": "P8_Y5_R2FR_4355_STATUS.csv",
        "next": "P8_Y5_R2FR_4355_NEXT_TARGET.csv",
    }
    for key, filename in mapping.items():
        write_csv(SOURCE_DIR / filename, tables[key])


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 371 PPC4161 transition shell same-worldtube nonHilbert residue or bounded source hair

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4355 does not prove public local GR, Newton, R10, PPN, WEP, clock, orbital, EM, or transition-shell safety.

## Result

4355 assembles the exact transition source-kernel fork.

Clean branch:

```text
P_kernel := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube
P_leak   := I - P_kernel

q_tr = P_kernel q_tr
=> P_leak q_tr = 0
=> epsilon_mu_tr = 0
=> Q_l>=1_tr = 0
=> epsilon_tr_hair = 0.
```

On this branch the transition residue is not a separate local metric/source leak. It is common Hilbert monopole source dressing and belongs inside `M_H^dress`.

What moved since the old transition wall:

```text
q_tr = -div Delta_K + C_RI + C_conn + B_boundary,
C_RI^flat = 0 on fixed flat boundary/projection branch,
epsilon_owner_tail_Kperp = 0 inside the compact private clean branch.
```

So the Khat/Gamma/Kperp owner leg is no longer the active private clean-branch blocker. The surviving problem is sharper: prove the raw transition shell is in the same source kernel, or carry the remaining hair as finite residuals.

If any kernel clause opens, the fallback is:

```text
epsilon_tr_hair <=
  Y_nonHilbert
  + Delta_Wtr
  + Y_time_l
  + Y_species_frame
  + Y_range
  + Y_nonEH
  + Y_boundary_nonlocal,

epsilon_Gsrc <- epsilon_Gsrc + epsilon_tr_hair.
```

The rough direct residual is not good enough: `epsilon_AJ_seed=0.08394692185032419` fails ordinary unit projection into WEP, PPN, clock, orbital and one-year `Gdot/G` rows. Transition hair therefore needs structural zero or source-backed strong suppression before any local claim.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Kernel Membership Rows

{md_table(tables["kernel"], ["kernel_id", "projector_leg", "zero_condition", "clean_output", "fallback_residual", "current_status", "valid_for_claim"])}

## Cleanup Imports

{md_table(tables["cleanup"], ["import_id", "imported_result", "effect_on_4355", "remaining_condition", "status", "valid_for_claim"])}

## Source Hair Bounds

{md_table(tables["hair"], ["bound_id", "hair_component", "formula", "zero_if", "feeds", "valid_for_claim"])}

## Theorem Rows

{md_table(tables["theorems"], ["theorem_id", "statement", "consequence", "status", "claim_allowed", "valid_for_claim"])}

## Arena Rows

{md_table(tables["arenas"], ["arena_id", "arena", "observable", "clean_branch", "finite_branch", "current_status", "valid_for_claim"])}

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
    post = f"""# 4355 Y5-R2FR transition shell same-worldtube nonHilbert residue or bounded source hair

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4355 turns transition-source hair into a clean fork:

```text
q_tr=P_kernel q_tr
=> P_leak q_tr=0
=> epsilon_mu_tr=0
=> Q_l>=1_tr=0
=> epsilon_tr_hair=0.
```

The private Khat/Gamma/Kperp owner channel is narrowed by 4340-4353, but raw transition shells still need source-kernel membership. If any kernel leg opens:

```text
epsilon_Gsrc <- epsilon_Gsrc + epsilon_tr_hair
```

with no cancellation.

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
                    "4355 assembles the transition source-kernel hair law. If q_tr is Hilbert, same-worldtube, static l=0, universal/species-frame blind, range-free, same-metric and boundary-owned on the same branch, then q_tr=P_kernel q_tr and P_leak q_tr=0, so epsilon_mu_tr=0, Q_l>=1_tr=0 and epsilon_tr_hair=0; the transition residue is ordinary Hilbert monopole dressing inside M_Hdress rather than a separate local metric/source leak. The checkpoint imports 4340-4353 progress: q_tr is reduced to -div Delta_K plus commutators, C_RI has a fixed-flat zero branch, and epsilon_owner_tail_Kperp=0 in the compact private clean branch. Current raw transition shells are not parent-signed into the kernel, so epsilon_tr_hair remains as an absolute finite source-hair envelope feeding epsilon_Gsrc."
                ),
                (
                    "4355 source register, kernel membership rows, cleanup import rows, source-hair bound rows, theorem rows, arena rows, runner, firewall, decision, status, next-target and validation CSV."
                ),
                "conditional_transition_source_kernel_hair_zero_or_finite_epsilon_tr_hair_nonclaim",
                (
                    "Attack static l=0, universal/species-frame blind, range-free, same-metric and boundary-owned transition kernel membership, or fill finite source-backed hair rows."
                ),
                (
                    "Treating raw transition shells as safe because compact-collar owner channels are clean; setting epsilon_mu_tr=0 without P_kernel membership; using rough epsilon_mu_tr=0.0839469 as evidence; cancelling transition hair components; choosing source-kernel clauses after seeing residuals."
                ),
            ]
        )


def append_spine_and_packet() -> None:
    spine_block = f"""

## PPC4161 4355 transition source-kernel hair law

Marker: `{MARKER}`

4355 assembles the transition shell source-kernel fork:

```text
q_tr=P_kernel q_tr
=> P_leak q_tr=0
=> epsilon_mu_tr=0
=> Q_l>=1_tr=0
=> epsilon_tr_hair=0.
```

The compact private owner channel is narrowed by the 4340-4353 chain, including `epsilon_owner_tail_Kperp=0`, so the live transition problem is source-kernel hair: static monopole, universal/species-frame blind, range-free, same-metric and boundary-owned membership. If any clause fails, the finite no-cancellation vector `epsilon_tr_hair` feeds `epsilon_Gsrc`.
"""
    packet_block = f"""

## PPC4161 packet update 4355 transition source hair

Marker: `{PACKET_MARKER}`

Packet update: transition safety is now a source-kernel membership problem. The old Khat/Gamma/Kperp owner leg is narrowed inside the private compact branch; raw transition shells still need `P_kernel` membership or finite source-hair rows. Next target: static `l=0`, universal, range-free transition hair.
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
    checks.append(("kernel_zero_present", "P_leak q_tr = 0" in formal_text, "kernel zero"))
    checks.append(("epsilon_tr_hair_present", "epsilon_tr_hair <=" in formal_text, "finite transition hair"))
    checks.append(("owner_import_present", "epsilon_owner_tail_Kperp = 0" in formal_text, "owner import"))
    checks.append(("multipole_zero_present", "Q_l>=1_tr = 0" in formal_text, "multipole zero"))
    checks.append(("epsilon_Gsrc_update_present", "epsilon_Gsrc <- epsilon_Gsrc + epsilon_tr_hair" in formal_text, "Gsrc update"))
    checks.append(("all_sources_exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source paths"))
    checks.append(("all_needles_found", all(row["needle_found"] == "True" for row in tables["sources"]), "source needles"))
    checks.append(("kernel_rows_present", len(tables["kernel"]) >= 8, str(len(tables["kernel"]))))
    checks.append(("hair_rows_present", len(tables["hair"]) >= 8, str(len(tables["hair"]))))
    checks.append(("cleanup_rows_present", len(tables["cleanup"]) >= 5, str(len(tables["cleanup"]))))
    checks.append(("theorem_rows_present", len(tables["theorems"]) >= 4, str(len(tables["theorems"]))))
    checks.append(("arena_rows_present", len(tables["arenas"]) == len(ARENAS), str(len(tables["arenas"]))))
    checks.append(("no_valid_claim_rows", all(row.get("valid_for_claim") == "False" for rows in tables.values() for row in rows if "valid_for_claim" in row), "all generated claim flags false"))
    checks.append(("claim_row_recorded", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID))
    checks.append(("spine_marker_recorded", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER))
    checks.append(("packet_marker_recorded", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER))
    for filename in [
        "P8_Y5_R2FR_4355_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4355_KERNEL_MEMBERSHIP_ROWS.csv",
        "P8_Y5_R2FR_4355_CLEANUP_IMPORT_ROWS.csv",
        "P8_Y5_R2FR_4355_SOURCE_HAIR_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4355_THEOREM_ROWS.csv",
        "P8_Y5_R2FR_4355_ARENA_ROWS.csv",
        "P8_Y5_R2FR_4355_RUNNER.csv",
        "P8_Y5_R2FR_4355_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4355_DECISION.csv",
        "P8_Y5_R2FR_4355_STATUS.csv",
        "P8_Y5_R2FR_4355_NEXT_TARGET.csv",
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
    print(f"{CHECKPOINT}: wrote 11 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation_rows)} failed={len(failures)}")
    if failures:
        for row in failures:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
