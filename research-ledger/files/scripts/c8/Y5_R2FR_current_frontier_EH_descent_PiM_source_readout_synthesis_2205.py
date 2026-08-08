from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2205"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2205-Y5-R2FR-current-frontier-EH-descent-PiM-source-readout-synthesis.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2205_SOURCE_REGISTER.csv",
    "frontier_synthesis": OUT / "P8_Y5_PARENT_QLOC_2205_FRONTIER_SYNTHESIS.csv",
    "conditional_wins": OUT / "P8_Y5_PARENT_QLOC_2205_CONDITIONAL_WINS.csv",
    "blocker_priority": OUT / "P8_Y5_PARENT_QLOC_2205_BLOCKER_PRIORITY_MATRIX.csv",
    "selected_contract": OUT / "P8_Y5_PARENT_QLOC_2205_SELECTED_TARGET_CONTRACT.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2205_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2205_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2205_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2205_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2205_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2205_FRONTIER_SELECTED_GK_QLOC_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2205_SELECTED_TARGET_CONTRACT_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_FRONTIER_SYNTHESIS_2205_NONCLAIM.csv",
}


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
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2205_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2205-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2205*",
        "*P8_Y5_BRR545_2205*",
        "*Y5_R2FR_current_frontier_EH_descent_PiM_source_readout_synthesis_2205*",
        "*JR2205*",
        "*PARENT_QLOC_FRONTIER_SYNTHESIS_2205*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2204_handoff",
            ROOT / "2204-Y5-R2FR-topological-Hilbert-equality-or-R-eq-first-row.md",
            ["NEXT2204_0_2205", "FR2204_2_parent_action_descent", "VAL2204_OVERALL"],
            "2204 selects current-frontier EH descent/PiM/source/readout synthesis.",
        ),
        (
            "2185_eh_to_v",
            ROOT / "2185-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
            ["WAE2185_4_delta", "IHG2185_5_verdict", "VAL2185_OVERALL"],
            "EH fixed-point to v coefficient extraction: conditional coefficient win, MTS descent unsigned.",
        ),
        (
            "2186_2pn_gauge",
            ROOT / "2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md",
            ["DEG2186_7_verdict", "ROG2186_4_parent_choice", "VAL2186_OVERALL"],
            "2PN warning demoted to radial-gauge owner debt; EH descent still unsigned.",
        ),
        (
            "2187_radial_contract",
            ROOT / "2187-Y5-R2FR-parent-owned-radial-gauge-map-and-EH-descent-signature.md",
            ["RGC2187_6_current_status", "DEC2187_3_next", "VAL2187_OVERALL"],
            "radial/angle gauge readout contract written; extra double-zero and PiM lock selected next.",
        ),
        (
            "2188_double_zero",
            ROOT / "2188-Y5-R2FR-extra-sector-double-zero-and-PiM-lock-signature-or-residual-fill.md",
            ["DEC2188_0_gain", "DEC2188_2_limit", "VAL2188_OVERALL"],
            "conditional F1 double-zero law and PiM lock contract.",
        ),
        (
            "2189_inventory",
            ROOT / "2189-Y5-R2FR-parent-extra-sector-inventory-and-coupling-map-or-leakage-bounds.md",
            ["DEC2189_2_best_route", "NEXT2189_0_2190", "VAL2189_OVERALL"],
            "extra-sector inventory selects Gamma/Khat/q_loc as first surgical derivation target.",
        ),
        (
            "2190_gk_qloc",
            ROOT / "2190-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
            ["CR2190_F_residual_lock", "DEC2190_1_limit", "VAL2190_OVERALL"],
            "q_loc theorem-zero contract written but not proved; residual lock selected.",
        ),
        (
            "2191_qloc_runner",
            ROOT / "2191-Y5-R2FR-q_loc-component-projection-runner-and-theorem-zero-certificate.md",
            ["DEC2191_0_gain", "DEC2191_1_limit", "VAL2191_OVERALL"],
            "q_loc residual interface made executable, all arenas still blocked.",
        ),
        (
            "2198_component_vector",
            ROOT / "2198-Y5-R2FR-beta-source-zero-or-bounded-component-pack.md",
            ["DEC2198_1_component_vector", "DEC2198_3_next", "VAL2198_OVERALL"],
            "surviving coupling loopholes consolidated into a component vector and Cassini pressure row.",
        ),
        (
            "2199_ppn_vector",
            ROOT / "2199-Y5-R2FR-no-hidden-visible-hom-or-PPN-vector-envelope.md",
            ["DEC2199_1_vector", "NEXT2199_0_2200", "VAL2199_OVERALL"],
            "PPN vector envelope promoted as honest fallback object.",
        ),
        (
            "2200_vector_source",
            ROOT / "2200-Y5-R2FR-hidden-invariant-algebra-triviality-or-PPN-vector-source-row.md",
            ["HRS2200_3_route_selection", "NEXT2200_0_2201", "VAL2200_OVERALL"],
            "hidden route not repeated; first PPN vector source contract staged.",
        ),
        (
            "2203_readout_obstruction",
            ROOT / "2203-Y5-R2FR-fixed-before-readout-PPN-map-or-measured-GM-obstruction-row.md",
            ["FBR2203_7_verdict", "ARW2203_0_alpha_readout", "VAL2203_OVERALL"],
            "fixed-before-readout map failed; alpha_readout and measured-GM obstruction retained.",
        ),
        (
            "2204_validation",
            OUT / "P8_Y5_BRR545_2204_VALIDATION.csv",
            ["VAL2204_OVERALL", "PASS"],
            "2204 validation passed before 2205 synthesis.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def conditional_win_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            win_id="WIN2205_0_EH_to_v_coefficients",
            result="EH fixed point gives K_v=c^4/(32*pi*G_ref), C_v=1/2 and delta_v_source_norm=0",
            evidence="2185 WAE2185_2 through WAE2185_5",
            claim_grade="CONDITIONAL_ON_MTS_EH_DESCENT",
            what_still_blocks="MTS parent action must sign EH fixed point, source measure, PiM lock, boundary zero and extra-sector silence",
        ),
        base_row(
            win_id="WIN2205_1_beta_gamma_1PN",
            result="EH lapse readout gives kappa_v=0, beta=1 and gamma=1 at 1PN in the proper gauge",
            evidence="2185 PPE2185 and 2186 RGC2186",
            claim_grade="CONDITIONAL_ON_GAUGE_OWNER_AND_EH_DESCENT",
            what_still_blocks="radial/angle/PPN gauge readout must be parent-owned before scoring",
        ),
        base_row(
            win_id="WIN2205_2_2PN_warning_demoted",
            result="+1/2 spatial 2PN warning is a mixed-gauge debt, not an automatic physical failure",
            evidence="2186 RGC2186_5_resolution",
            claim_grade="CONDITIONAL_GAUGE_RESOLUTION",
            what_still_blocks="parent must choose areal reciprocal gauge plus PPN transform, or isotropic non-reciprocal branch",
        ),
        base_row(
            win_id="WIN2205_3_double_zero_law",
            result="F1 local leakage vanishes if every non-EH coupling has C_i(Phi0)=0 and partial_A C_i(Phi0)=0",
            evidence="2188 DEC2188_0_gain",
            claim_grade="CONDITIONAL_OPERATOR_THEOREM",
            what_still_blocks="actual parent C_i inventory and sector-by-sector double-zero signatures",
        ),
        base_row(
            win_id="WIN2205_4_residual_interfaces",
            result="q_loc, PPN vector, alpha_readout and measured-GM obstruction are explicit nonclaim interfaces",
            evidence="2191;2199;2200;2203",
            claim_grade="DISCIPLINED_NONCLAIM_TEST_PLUMBING",
            what_still_blocks="source-backed response operators and parent zero theorems",
        ),
    ]


def frontier_synthesis_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            synthesis_id="SYN2205_0_frontier_position",
            object="local_GR_reduction_frontier",
            status="CONDITIONAL_EH_INHERITANCE_PLUS_UNSIGNED_MTS_DESCENT",
            summary="The numbers line up inside EH; MTS ownership depends on parent descent and residual silence.",
            consequence="work should target parent-signature clauses, not broad re-audits",
        ),
        base_row(
            synthesis_id="SYN2205_1_main_tension",
            object="EH_import_vs_MTS_descent",
            status="NOT_RESOLVED",
            summary="EH-to-v coefficient extraction is a win only if MTS proves the compact local branch descends to EH with silent extra sectors.",
            consequence="no local-GR claim until descent certificates exist",
        ),
        base_row(
            synthesis_id="SYN2205_2_coupling_tension",
            object="Gamma/Khat/q_loc sector",
            status="FIRST_LIVE_EXTRA_SECTOR_OBSTRUCTION",
            summary="2189/2190 identify GK/q_loc as the most surgical live extra-sector source of local residuals.",
            consequence="derive or demote this sector before pretending all extra fields are silent",
        ),
        base_row(
            synthesis_id="SYN2205_3_source_tension",
            object="PiM/source/readout",
            status="PARALLEL_BLOCKER",
            summary="PiM/Hamiltonian lock, same source measure, boundary zero and fixed-before-readout map remain unsigned.",
            consequence="even a q_loc win would still need source/readout closure",
        ),
        base_row(
            synthesis_id="SYN2205_4_empirical_tension",
            object="PPN/R10 residual vector",
            status="TEST_PLUMBING_AVAILABLE_NOT_SCORE_READY",
            summary="Cassini/R10 pressure rows exist, but theory-side coefficients, response operators and source paths are missing.",
            consequence="empirical tests should follow parent-signature or source-backed rows, not placeholders",
        ),
    ]


def blocker_priority_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            priority_rank=1,
            blocker_id="BLK2205_0_GK_q_loc_parent_signature",
            clause="Gamma/Khat/q_loc parent action, metric response, Helmholtz/Euler closure and boundary silence",
            why_ranked_here="2189 selected GK/q_loc as first concrete extra-sector obstruction; 2190 made it official residual interface when theorem-zero failed",
            evidence="2189 DEC2189_2_best_route;2190 CR2190_F_residual_lock",
            if_closed="removes or bounds the live q_loc local-test vector, strengthening EH descent",
            if_failed="q_loc stays official PPN/R10/clock/orbital residual and local-GR branch must be residual-tested",
            selected_next=True,
        ),
        base_row(
            priority_rank=2,
            blocker_id="BLK2205_1_PiM_Hamiltonian_lock",
            clause="Pi_M(Phi0)=Pi_EH and derivative/commutator/projector-stress silence",
            why_ranked_here="source normalization and R_eq require PiM/Hamiltonian identity, but q_loc is the first concrete extra-sector pole to classify",
            evidence="2188 PiM lock contract;2203 measured-GM obstruction",
            if_closed="measured-GM and R_eq routes gain a real source object",
            if_failed="R_eq/M_H_ref rows need finite source-backed residuals",
            selected_next=False,
        ),
        base_row(
            priority_rank=3,
            blocker_id="BLK2205_2_source_measure_glue",
            clause="same observed Hilbert/Hamiltonian source measure for matter, clocks, orbit and readout",
            why_ranked_here="needed for Newton coefficient, but not enough if extra-sector local force survives",
            evidence="2183 selector;2203 fixed-before-readout failure",
            if_closed="reduces measured-GM/readout absorption loophole",
            if_failed="alpha_readout and measured-GM obstruction remain active",
            selected_next=False,
        ),
        base_row(
            priority_rank=4,
            blocker_id="BLK2205_3_boundary_reference_zero",
            clause="B_zero/reference/symplectic compact boundary flux is zero or finite-bounded",
            why_ranked_here="essential for charge equality, but downstream of action/PiM/source owner",
            evidence="2182;2183;2184",
            if_closed="prevents boundary bookkeeping from shifting measured mass",
            if_failed="B_zero_flux remains nonclaim finite row",
            selected_next=False,
        ),
        base_row(
            priority_rank=5,
            blocker_id="BLK2205_4_radial_readout_owner",
            clause="parent owns areal/isotropic radial map, angular coframe and PPN gauge transform",
            why_ranked_here="2PN warning is conditionally gauge-resolved, so this is important but not the first live extra-force obstruction",
            evidence="2186;2187",
            if_closed="locks beta/gamma/2PN readout convention",
            if_failed="2PN/readout residual rows stay active",
            selected_next=False,
        ),
        base_row(
            priority_rank=6,
            blocker_id="BLK2205_5_PPN_vector_components",
            clause="alpha_cg/readout/support/boundary/nonH/disformal vector components zero or bounded",
            why_ranked_here="official comparison object exists but depends on upstream parent signatures and response operators",
            evidence="2199;2200;2201;2202;2203",
            if_closed="Cassini pressure can become a genuine vector score",
            if_failed="no PPN/local-GR claim; keep vector nonclaim",
            selected_next=False,
        ),
    ]


def selected_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            contract_id="SEL2205_0_target",
            target="Gamma/Khat/q_loc parent-signature derivation",
            required_output="prove or reject S_GK owner, Khat metric response, Helmholtz/Euler closure, T_GK double-zero, P_loc projection and boundary no-flux in one branch",
            reason="this is the first concrete extra-sector obstruction preventing MTS from owning the EH fixed point rather than importing GR",
            current_status="SELECTED_NEXT_DERIVATION_TARGET",
        ),
        base_row(
            contract_id="SEL2205_1_success",
            target="q_loc theorem-zero success condition",
            required_output="S_GK exists; Khat=dGamma_eff/dg or equivalent metric response; Helmholtz integrability; Euler/Ward closure; T_GK(Phi0)=0; partial_A T_GK(Phi0)=0; P_loc q=0; boundary flux=0",
            reason="all clauses are needed before q_loc can be removed from local-test residual vector",
            current_status="NOT_CURRENTLY_SATISFIED",
        ),
        base_row(
            contract_id="SEL2205_2_failure",
            target="q_loc official residual demotion",
            required_output="if any clause remains unsigned, keep q_loc as explicit PPN/R10/R11/clock/orbital residual with source-backed acquisition rows",
            reason="residual testing is honest; plateau or silent-zero claims are not",
            current_status="ACTIVE_FALLBACK",
        ),
        base_row(
            contract_id="SEL2205_3_no_shortcuts",
            target="forbidden shortcuts",
            required_output="no plateau axiom, no scalar proxy for vector q_loc, no fitting into measured G, no cancellation against readout/alpha_cg, no local-GR claim",
            reason="these would make the branch look cleaner while making the final theory less true",
            current_status="GUARDRAIL_ACTIVE",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2205_0_conditional_EH_win",
            gate="EH-to-v coefficient extraction is conditionally valid",
            status="PASS_NONCLAIM",
            implication="K_v/C_v/kappa_v are useful only after MTS descent is parent-signed.",
        ),
        base_row(
            gate_id="CG2205_1_MTS_descent",
            gate="MTS parent action derives EH fixed point with silent extra sectors",
            status="BLOCKED_NONCLAIM",
            implication="GK/q_loc and other extra-sector signatures remain unsigned.",
        ),
        base_row(
            gate_id="CG2205_2_GK_q_loc",
            gate="Gamma/Khat/q_loc theorem-zero chain passes",
            status="BLOCKED_NONCLAIM",
            implication="q_loc remains the official local-test residual interface until 2206 closes or demotes it.",
        ),
        base_row(
            gate_id="CG2205_3_PiM_source_readout",
            gate="PiM/source/boundary/readout ownership closes",
            status="BLOCKED_NONCLAIM",
            implication="measured-GM and alpha_readout obstruction remain active.",
        ),
        base_row(
            gate_id="CG2205_4_empirical_score",
            gate="PPN/R10/clock/orbital rows are score-ready",
            status="BLOCKED_NONCLAIM",
            implication="response operators and source-backed component rows are still missing.",
        ),
        base_row(
            gate_id="CG2205_5_local_GR_newton",
            gate="Newton/local-GR reduction can be claimed",
            status="BLOCKED_NONCLAIM",
            implication="no Newton, local-GR, PPN, WEP, R10, clock, orbital or public claim follows from 2205.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2205_0_synthesis",
            decision="CONDITIONAL_EH_WIN_REAL_BUT_NOT_OWNED",
            rationale="2185/2186 show the EH fixed point gives the desired v coefficients and 1PN readout, but MTS descent is unsigned.",
            next_action="do not treat EH extraction as an MTS proof until parent signatures close",
        ),
        base_row(
            decision_id="DEC2205_1_priority",
            decision="GK_QLOC_PARENT_SIGNATURE_SELECTED_FIRST",
            rationale="2189/2190 identify Gamma/Khat/q_loc as the first concrete extra-sector obstruction; closing or demoting it decides whether the local branch has an actual extra force.",
            next_action="2206 should attack S_GK/metric-response/Helmholtz/double-zero/P_loc/boundary clauses",
        ),
        base_row(
            decision_id="DEC2205_2_parallel_debts",
            decision="PIM_SOURCE_BOUNDARY_READOUT_REMAIN_PARALLEL_BLOCKERS",
            rationale="even a q_loc win does not close measured-GM, R_eq, PiM lock, source measure, boundary zero or radial gauge ownership.",
            next_action="keep these in the blocker matrix and return after q_loc classification",
        ),
        base_row(
            decision_id="DEC2205_3_no_claim",
            decision="NO_LOCAL_GR_OR_EMPIRICAL_CLAIM",
            rationale="2205 is a synthesis/target-selection checkpoint, not a proof or score.",
            next_action="all outputs remain nonclaim/private",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2205_0_2206",
            selection_status="selected",
            target_file="2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md",
            target_script="scripts/Y5_R2FR_GammaKhat_q_loc_parent_action_signature_or_official_residual_demotion_2206.py",
            objective="derive or reject the Gamma/Khat/q_loc parent-signature chain: S_GK owner, metric response, Helmholtz/Euler closure, local double-zero, P_loc projection, and boundary no-flux",
            success_condition="either q_loc is parent-signed theorem-zero on the compact local branch, or q_loc is officially demoted to finite residual rows for PPN/R10/R11/clock/orbital testing with no local-GR claim",
            do_not_do="do not use a plateau axiom, scalar proxy, fitted G, readout cancellation, hidden invariant shortcut, or GitHub action",
        ),
        base_row(
            route_id="NEXT2205_1_source_parallel",
            selection_status="held_parallel",
            target_file="2206b-Y5-R2FR-q-loc-source-backed-component-acquisition.md",
            target_script="scripts/Y5_R2FR_q_loc_source_backed_component_acquisition_2206b.py",
            objective="if derivation stalls, acquire one source-backed q_loc component/profile/response row with units and claim=false",
            success_condition="one q_loc residual row has real source path, declared units, arena projection, and valid_for_claim=false",
            do_not_do="do not score placeholders, invent coefficients, or claim q_loc zero from smoke data",
        ),
    ]


def write_branch_copies() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["blocker_priority"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["selected_contract"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["frontier_synthesis"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        parse_ok, row_count, parse_detail = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=target.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_detail=parse_detail,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    synthesis_rows: list[dict[str, Any]],
    win_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    selected_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if passed else "FAIL", detail=detail))

    add("VAL2205_00_sources_exist", all(truthy(r["path_exists"]) for r in source_rows), f"{sum(truthy(r['path_exists']) for r in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2205_01_needles_found", all(truthy(r["needles_found"]) for r in source_rows), f"{sum(truthy(r['needles_found']) for r in source_rows)}/{len(source_rows)} source needle sets found")
    add("VAL2205_02_conditional_wins", len(win_rows) == 5 and any(r["win_id"] == "WIN2205_0_EH_to_v_coefficients" for r in win_rows), "conditional EH/v wins represented")
    add("VAL2205_03_synthesis", any(r["synthesis_id"] == "SYN2205_2_coupling_tension" for r in synthesis_rows), "frontier synthesis names GK/q_loc coupling tension")
    add("VAL2205_04_priority", any(truthy(r["selected_next"]) and r["blocker_id"] == "BLK2205_0_GK_q_loc_parent_signature" for r in blocker_rows), "GK/q_loc parent signature selected first")
    add("VAL2205_05_selected_contract", len(selected_rows) == 4 and any(r["contract_id"] == "SEL2205_1_success" and r["current_status"] == "NOT_CURRENTLY_SATISFIED" for r in selected_rows), "selected target contract is sharp and unsatisfied")
    add("VAL2205_06_claim_gate", any(r["gate_id"] == "CG2205_5_local_GR_newton" and r["status"] == "BLOCKED_NONCLAIM" for r in claim_rows), "local-GR remains blocked")
    add("VAL2205_07_decision", any(r["decision"] == "GK_QLOC_PARENT_SIGNATURE_SELECTED_FIRST" for r in decision_rows_data), "decision selects GK/q_loc parent signature")
    add("VAL2205_08_next_target", any(r["route_id"] == "NEXT2205_0_2206" and r["selection_status"] == "selected" for r in next_rows), "2206 GK/q_loc target selected")

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["frontier_synthesis"],
        OUTPUTS["conditional_wins"],
        OUTPUTS["blocker_priority"],
        OUTPUTS["selected_contract"],
        OUTPUTS["claim_gate"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    parse_ok_all = True
    parse_parts: list[str] = []
    for path in generated_csvs:
        parse_ok, count, detail = csv_rows_parse(path)
        parse_ok_all = parse_ok_all and parse_ok and count > 0
        parse_parts.append(f"{path.name}:{count if parse_ok else detail}")
    add("VAL2205_09_csv_parse", parse_ok_all, "; ".join(parse_parts))
    add("VAL2205_10_branch_copies", len(copy_rows) == 3 and all(truthy(r["copied"]) and truthy(r["parse_ok"]) for r in copy_rows), ";".join(str(r["target_path"]) for r in copy_rows))

    all_generated_rows = [
        *source_rows,
        *synthesis_rows,
        *win_rows,
        *blocker_rows,
        *selected_rows,
        *claim_rows,
        *decision_rows_data,
        *next_rows,
        *copy_rows,
    ]
    add("VAL2205_11_claim_flags_false", all(not truthy(r.get("valid_for_claim", False)) and not truthy(r.get("claim_allowed", False)) for r in all_generated_rows), "all generated rows keep valid_for_claim=false and claim_allowed=false")
    add("VAL2205_12_formalization_clean", not formalization_has_2205_artifacts(), "formalization-workbench has no 2205 artifacts")
    add("VAL2205_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), str(ROOT / "scripts" / "__pycache__"))
    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2205_OVERALL", overall, "2205 synthesizes EH/v wins with residual debts and selects GK/q_loc parent-signature derivation next")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    synthesis_rows: list[dict[str, Any]],
    win_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    selected_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_data: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2205 - Y5/R2FR Current Frontier EH Descent PiM Source Readout Synthesis",
        "",
        "## Current Verdict",
        "",
        "2205 gives the project a sharper map. The coefficient side is no longer the scary bit: inside the EH fixed point, the `v` action gives `K_v=c^4/(32*pi*G_ref)`, `C_v=1/2`, `delta_v_source_norm=0`, and the 1PN lapse readout gives `kappa_v=0`, `beta=1`, `gamma=1` conditionally.",
        "",
        "The hard bit is ownership. MTS only earns that result if the compact local branch parent-signs EH descent, extra-sector double zeros, PiM/Hamiltonian lock, same source measure, boundary/reference zero, and radial readout ownership.",
        "",
        "The first sharp derivation target is the `Gamma/Khat/q_loc` sector. 2189 selected it as the most surgical extra-sector obstruction; 2190 showed the theorem-zero route is not proved and locked `q_loc` as the official residual interface. So 2206 should either derive the parent-signature chain for `q_loc=0`, or demote it fully to finite residual testing. No plateau magic, no scalar proxy, no hiding in measured `G`.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Conditional Wins",
        "",
        md_table(win_rows, ["win_id", "result", "claim_grade", "what_still_blocks", "valid_for_claim"]),
        "",
        "## Frontier Synthesis",
        "",
        md_table(synthesis_rows, ["synthesis_id", "object", "status", "summary", "consequence", "valid_for_claim"]),
        "",
        "## Blocker Priority Matrix",
        "",
        md_table(blocker_rows, ["priority_rank", "blocker_id", "clause", "why_ranked_here", "selected_next", "valid_for_claim"]),
        "",
        "## Selected Target Contract",
        "",
        md_table(selected_rows, ["contract_id", "target", "required_output", "current_status", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_data, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_data, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "This is a genuinely useful checkpoint. It says: the local-GR route is not looking mathematically hopeless, because the EH/v coefficients do come out. But MTS does not own those coefficients until the extra-sector silence and source/readout locks are parent-signed.",
        "",
        "Best next attack: `2206` should go straight at `Gamma/Khat/q_loc`. Either it becomes the first real double-zero local descent proof, or it becomes the official finite residual vector we test against PPN/R10/clocks/orbits. That is progress either way.",
    ]
    DOC.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    synthesis_rows = frontier_synthesis_rows()
    win_rows = conditional_win_rows()
    blocker_rows = blocker_priority_rows()
    selected_rows = selected_target_rows()
    claim_rows = claim_gate_rows()
    decision_rows_data = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["frontier_synthesis"], synthesis_rows)
    write_csv(OUTPUTS["conditional_wins"], win_rows)
    write_csv(OUTPUTS["blocker_priority"], blocker_rows)
    write_csv(OUTPUTS["selected_contract"], selected_rows)
    write_csv(OUTPUTS["claim_gate"], claim_rows)
    write_csv(OUTPUTS["decision"], decision_rows_data)
    write_csv(OUTPUTS["next_target"], next_rows)
    copy_rows = write_branch_copies()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_data = validation_rows(
        source_rows,
        synthesis_rows,
        win_rows,
        blocker_rows,
        selected_rows,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_data)
    write_doc(
        source_rows,
        synthesis_rows,
        win_rows,
        blocker_rows,
        selected_rows,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
        validation_rows_data,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
