from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SECTOR_GAMMA_SLOT_AUDIT_AND_PRIVATE_SRNG_LOCK_2415"
CHECKPOINT_ID = "2415"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2415-Y5-R2FR-sector-Gamma-slot-audit-and-private-SRNG-lock.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2415_SOURCE_REGISTER.csv",
    "sector_audit": OUT / "P8_Y5_PARENT_QLOC_2415_SECTOR_GAMMA_SLOT_AUDIT.csv",
    "private_srng_lock": OUT / "P8_Y5_PARENT_QLOC_2415_PRIVATE_SRNG_LOCK.csv",
    "p4_stack": OUT / "P8_Y5_PARENT_QLOC_2415_PUBLIC_PRIVATE_P4_COMPONENT_STACK.csv",
    "gap_ledger": OUT / "P8_Y5_PARENT_QLOC_2415_LOCAL_GR_GAP_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2415_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2415_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2415_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2415_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2415_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2415_SECTOR_GAMMA_SLOT_AUDIT_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2415_PUBLIC_PRIVATE_P4_STACK_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_SECTOR_GAMMA_DECISION_2415_NONCLAIM.csv",
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
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2415_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2415-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2415*",
        "*P8_Y5_BRR545_2415*",
        "*Y5_R2FR_sector_Gamma_slot_audit_and_private_SRNG_lock_2415*",
        "*JR2415*",
        "*PARENT_QLOC_SECTOR_GAMMA_DECISION_2415*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2414_kconn_gate",
            ROOT / "2414-Y5-R2FR-Kconn-LC-parent-signature-or-affine-P4-residual-row.md",
            ["LCS2414_5_verdict", "GSI2414_9_sector_sum_verdict", "NEXT2414_0_selected", "VAL2414_OVERALL"],
            "immediate handoff: Kconn LC zero is exact conditional; sector Gamma-slot audit selected.",
        ),
        (
            "2334_sector_no_gamma",
            ROOT / "2334-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md",
            ["NGSA2334_9_verdict", "NGT2334_4_result", "P4DQ2334_0_total", "VAL2334_OVERALL"],
            "first sector-sum no-Gamma audit and P4 Delta component queue.",
        ),
        (
            "2335_source_readout_certificate",
            ROOT / "2335-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md",
            ["SRNG2335_6_verdict", "THM2335_3_SRNG_sum", "P4S2335_6_reduced_total", "VAL2335_OVERALL"],
            "source/readout no-Gamma certificate and SRNG theorem attempt.",
        ),
        (
            "2336_private_srng",
            ROOT / "2336-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md",
            ["OFC2336_5_status", "ADM2336_3_decision", "P4A2336_0_SRNG_effect", "VAL2336_OVERALL"],
            "private SRNG/OFC adoption with public proof debt retained.",
        ),
        (
            "2347_srng_scope",
            ROOT / "2347-Y5-R2FR-noGamma-SRNG-adoption-or-P4-hypermomentum-component-row.md",
            ["SRNG2347_0_private_scope", "P4H2347_0_total_public", "SPIN2347_0_target", "VAL2347_OVERALL"],
            "private/public SRNG scope split and public P4 hypermomentum stack.",
        ),
        (
            "2348_spin_connection",
            ROOT / "2348-Y5-R2FR-spin-connection-coframe-owned-or-axial-torsion-P4-row.md",
            ["SPIN2348_6_verdict", "P4S2348_0_spin_total", "CHAIN2348_5_parent_contract", "VAL2348_OVERALL"],
            "coframe-owned spin connection exact conditional; spin P4 row retained.",
        ),
        (
            "2349_projective_trace",
            ROOT / "2349-Y5-R2FR-projective-trace-silence-or-P4-projective-component-row.md",
            ["PROJ2349_5_verdict", "P4P2349_0_projective_total", "PSTACK2349_4_parent_contract", "VAL2349_OVERALL"],
            "projective trace private zero and public P4 projective fallback.",
        ),
        (
            "2350_boundary",
            ROOT / "2350-Y5-R2FR-boundary-improvement-current-zero-or-P4-boundary-row.md",
            ["BIC2350_7_verdict", "P4B2350_0_boundary_total", "NEXT2350_0", "VAL2350_OVERALL"],
            "boundary/improvement is the primary private-branch leak and needs parent charge extraction.",
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


def sector_audit_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="SGA2415_0_total", sector="total_local_branch", gamma_slot_status="NO_PUBLIC_SECTOR_SUM_YET", private_status="private reductions available but nonclaim", public_residual="Delta_abs_public", proof_gap="parent ordinary/source/readout object-language signature", next_action="parent action signature spine or P4 residual stack"),
        base_row(row_id="SGA2415_1_ordinary_matter", sector="ordinary_matter", gamma_slot_status="CONDITIONAL_NO_GAMMA_IN_OWNED_COFRAME_BRANCH", private_status="usable in private owned-coframe branch", public_residual="Delta_matter_guard", proof_gap="global Arg(S_ord) signature not published as parent theorem", next_action="sign ordinary matter variable list"),
        base_row(row_id="SGA2415_2_spin_connection", sector="spin_connection", gamma_slot_status="EXACT_CONDITIONAL_COFAME_OWNED_NOT_PUBLIC", private_status="can be zero only if omega_obs=omega_LC[e_obs] is locked", public_residual="Delta_spin_abs", proof_gap="independent torsion/metric-affine counterbranch not excluded", next_action="parent action signature or axial torsion P4 row"),
        base_row(row_id="SGA2415_3_em_gauge", sector="em_gauge", gamma_slot_status="AUDIT_REQUIRED_NOT_PUBLICLY_SIGNED", private_status="standard exterior/gauge branch likely no affine Gamma but must be stated", public_residual="Delta_EM_affine_guard", proof_gap="EM/gauge action argument list and light readout split", next_action="show A_mu/F=dA uses g_obs/Hodge only, or assign affine response row"),
        base_row(row_id="SGA2415_4_source_worldtube", sector="source_worldtube", gamma_slot_status="PRIVATE_SRNG_ZERO_ONLY", private_status="Delta_source=0 inside private SRNG/OFC", public_residual="Delta_source_public", proof_gap="source support/worldtube selector not public parent theorem", next_action="derive q-natural source selector or keep source P4 row"),
        base_row(row_id="SGA2415_5_clocks", sector="clocks", gamma_slot_status="PRIVATE_SRNG_ZERO_ONLY", private_status="Delta_clock=0 inside private SRNG/OFC", public_residual="Delta_clock_public", proof_gap="clock/readout action-argument certificate not public theorem", next_action="derive downstream clock functor"),
        base_row(row_id="SGA2415_6_lightcone", sector="lightcone", gamma_slot_status="PRIVATE_SRNG_ZERO_ONLY", private_status="Delta_light=0 inside private SRNG/OFC", public_residual="Delta_light_public", proof_gap="light/ray/readout separation not public theorem", next_action="derive lightcone readout from q-natural EM/metric branch"),
        base_row(row_id="SGA2415_7_orbital_readout", sector="orbital_readout", gamma_slot_status="PRIVATE_SRNG_ZERO_ONLY", private_status="Delta_orbit=0 inside private SRNG/OFC", public_residual="Delta_orbit_public", proof_gap="test-body/trajectory readout cannot import GR geodesics", next_action="derive test-body limit or keep orbit P4 row"),
        base_row(row_id="SGA2415_8_projective_trace", sector="projective_trace", gamma_slot_status="PRIVATE_OWNED_COFRAME_ZERO_ONLY", private_status="Delta_projective_private=0 in owned-coframe+SRNG branch", public_residual="P_projective_abs", proof_gap="all-sector projective invariance/gauge fixation missing", next_action="parent action signature or projective component bounds"),
        base_row(row_id="SGA2415_9_boundary_improvement", sector="boundary_improvement", gamma_slot_status="LIVE_PRIMARY_LEAK", private_status="not killed by SRNG/spin/projective switches", public_residual="epsilon_boundary_abs", proof_gap="theta_MTS/Q_tau/H_tau/H_ref/M_H_ref and boundary object exhaustion missing", next_action="parent theta/Q_tau/H_tau/H_ref extraction"),
        base_row(row_id="SGA2415_10_verdict", sector="sector_sum_verdict", gamma_slot_status="PUBLIC_NO_GAMMA_NOT_CLOSED", private_status="private branch narrows to boundary plus parent-signature/source-current guards", public_residual="Delta_abs_public", proof_gap="sector signatures plus boundary charge/source-current identity", next_action="2416 parent action signature spine; parallel theta/Q_tau extraction"),
    ]


def private_srng_lock_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="SRNGL2415_0_scope", clause="private SRNG/OFC branch", allowed_use="internal nonclaim derivation branch only", forbidden_use="public local-GR/Newton theorem, GitHub claim, R10 reopening, or empirical pass", locked_status="PRIVATE_LOCKED_NONCLAIM"),
        base_row(row_id="SRNGL2415_1_zero_switch", clause="source/readout zero switch", allowed_use="set Delta_source=Delta_clock=Delta_light=Delta_orbit=0 only inside the tagged private branch", forbidden_use="export these zeros to public parent theory without a proof", locked_status="ZERO_SWITCH_PRIVATE_ONLY"),
        base_row(row_id="SRNGL2415_2_spin_limit", clause="spin not closed by SRNG", allowed_use="combine with separate owned-coframe spin condition if parent signature is stated", forbidden_use="say SRNG kills torsion/spin current", locked_status="SPIN_SEPARATE"),
        base_row(row_id="SRNGL2415_3_projective_limit", clause="projective trace", allowed_use="zero inside owned-coframe+SRNG private branch if no independent Gamma variable exists", forbidden_use="claim global projective gauge silence across all sectors", locked_status="PROJECTIVE_PRIVATE_ONLY"),
        base_row(row_id="SRNGL2415_4_boundary_limit", clause="boundary/improvement", allowed_use="carry epsilon_boundary_abs as primary private-branch leak", forbidden_use="let SRNG eat boundary/corner/reference/improvement currents", locked_status="BOUNDARY_REMAINS_LIVE"),
        base_row(row_id="SRNGL2415_5_labeling_rule", clause="documentation rule", allowed_use="every private zero must carry valid_for_claim=false and claim_allowed=false", forbidden_use="unlabeled transfer of private rows into public claims", locked_status="CLAIM_FLAGS_FALSE"),
    ]


def p4_stack_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="P4STACK2415_0_public_total", stack="public", formula="Delta_abs_public := ||Delta_matter|| + ||Delta_spin|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary|| + ||Delta_projective||", status="LIVE_NONCLAIM", score_ready=False),
        base_row(row_id="P4STACK2415_1_private_SRNG_reduced", stack="private_SRNG_only", formula="Delta_abs_private_SRNG := ||Delta_matter_guard|| + ||Delta_spin|| + ||Delta_boundary|| + ||Delta_projective|| + parent_signature_guard", status="PRIVATE_NONCLAIM_REDUCTION", score_ready=False),
        base_row(row_id="P4STACK2415_2_private_owned_coframe_projective", stack="private_owned_coframe_SRNG_projective", formula="epsilon_private_connection_abs := epsilon_boundary_abs + parent_signature_guard + source_current_guard + Khat_improvement_guard", status="PRIVATE_BRANCH_NARROWED_NOT_CLOSED", score_ready=False),
        base_row(row_id="P4STACK2415_3_boundary_primary", stack="boundary", formula="epsilon_boundary_abs := abs(B_zero_flux)/M_H_ref + abs(Delta_symp)/M_H_ref + abs(R_eq)/M_H_ref + abs(I_commutator) + abs(worldtube_domain) + abs(corner) + abs(K_improvement)", status="PRIMARY_LIVE_LEAK_INPUTS_MISSING", score_ready=False),
        base_row(row_id="P4STACK2415_4_no_cancellation", stack="policy", formula="all public/private residual stacks use absolute sums unless a parent-signed identity proves cancellation", status="GUARD_READY", score_ready=False),
    ]


def gap_ledger_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="GAP2415_0_known_exact", item="variable-absence/no-Gamma theorem", current_status="exact conditional lemma", why_it_matters="this is the right route to LC rather than importing GR", needed_to_close="parent action variable-domain signature"),
        base_row(row_id="GAP2415_1_known_exact", item="K_conn LC zero", current_status="exact conditional lemma", why_it_matters="kills connection residual if sector sum is signed", needed_to_close="no independent affine Gamma in every relevant sector"),
        base_row(row_id="GAP2415_2_private_gain", item="SRNG/OFC", current_status="private nonclaim lock", why_it_matters="source/readout leakage can be removed internally", needed_to_close="public downstream observation theorem"),
        base_row(row_id="GAP2415_3_spin", item="coframe-owned spin connection", current_status="exact conditional, public blocked", why_it_matters="torsion/spin is the obvious critic target", needed_to_close="ordinary matter/spin parent signature or P4 coefficients"),
        base_row(row_id="GAP2415_4_projective", item="projective trace", current_status="private zero only, public live", why_it_matters="Palatini/affine branch can hide a trace coupling", needed_to_close="all-sector projective invariance or bound rows"),
        base_row(row_id="GAP2415_5_boundary", item="boundary/improvement current", current_status="primary private-branch leak", why_it_matters="boundary terms can reintroduce local source/current residuals", needed_to_close="theta_MTS/Q_tau/H_tau/H_ref/M_H_ref extraction and object exhaustion"),
        base_row(row_id="GAP2415_6_rank_zero", item="rank-zero source-current identity", current_status="not closed", why_it_matters="strict branch has no finite-range R10 escape hatch", needed_to_close="M lock + J/B/DqZ/CDB/NH source-current identities"),
        base_row(row_id="GAP2415_7_claim_status", item="local GR/Newton reduction", current_status="closer but unclaimed", why_it_matters="this is the central competitiveness gate", needed_to_close="sector signature plus boundary/source-current bridge"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2415_0_variable_absence_theorem", gate="no-Gamma variable-absence theorem exact conditional", passed=True, claim_effect="lemma can be used under explicit parent-domain assumptions"),
        base_row(gate_id="CG2415_1_public_sector_sum", gate="public no-Gamma sector sum", passed=False, claim_effect="Delta_abs_public remains live"),
        base_row(gate_id="CG2415_2_private_SRNG_lock", gate="private SRNG/OFC lock", passed=True, claim_effect="internal branch may zero source/readout residuals with nonclaim flags"),
        base_row(gate_id="CG2415_3_spin_public_zero", gate="spin connection public zero", passed=False, claim_effect="Delta_spin_abs/P4 row retained"),
        base_row(gate_id="CG2415_4_projective_public_zero", gate="projective trace public zero", passed=False, claim_effect="P_projective_abs retained"),
        base_row(gate_id="CG2415_5_boundary_public_zero", gate="boundary/improvement current zero", passed=False, claim_effect="epsilon_boundary_abs primary leak retained"),
        base_row(gate_id="CG2415_6_p4_score_ready", gate="P4 component stack has numeric values/maps/source paths", passed=False, claim_effect="not empirical evidence yet"),
        base_row(gate_id="CG2415_7_local_GR_Newton", gate="local GR/Newton reduction derived", passed=False, claim_effect="blocked pending parent signature and boundary/source-current closure"),
        base_row(gate_id="CG2415_8_R10_reopen", gate="finite-range R10 reopened", passed=False, claim_effect="strict branch remains rank-zero/algebraic"),
        base_row(gate_id="CG2415_9_GitHub", gate="public/GitHub update", passed=False, claim_effect="private checkpoint only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2415_0_result", decision="NO_PUBLIC_SECTOR_GAMMA_SUM_YET", rationale="every important zero is exact conditional or private, not globally parent-signed", consequence="no local-GR/Newton claim"),
        base_row(decision_id="DEC2415_1_private_lock", decision="PRIVATE_SRNG_LOCKED", rationale="SRNG/OFC is useful and disciplined if kept private/nonclaim", consequence="source/readout zeros can be used only inside tagged branch"),
        base_row(decision_id="DEC2415_2_boundary", decision="BOUNDARY_IS_PRIMARY_PRIVATE_BRANCH_LEAK", rationale="after SRNG/spin/projective private switches, boundary/improvement plus parent charges survive", consequence="theta/Q_tau/H_tau/H_ref extraction is unavoidable"),
        base_row(decision_id="DEC2415_3_public_route", decision="PARENT_ACTION_SIGNATURE_SPINE_IS_HIGHEST_LEVERAGE", rationale="one parent variable-domain signature can promote multiple conditional no-Gamma lemmas", consequence="next main derivation target is parent ordinary action signature"),
        base_row(decision_id="DEC2415_4_no_claim", decision="NO_GITHUB_NO_R10_NO_LOCAL_PASS", rationale="all component stacks are non-score-ready and strict branch is rank-zero", consequence="continue private derivation work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2415_0_selected",
            selection_status="selected",
            target_file="2416-Y5-R2FR-parent-ordinary-action-variable-signature-spine.md",
            target_script="scripts/Y5_R2FR_parent_ordinary_action_variable_signature_spine_2416.py",
            objective="write the parent action variable-domain contract that would promote owned-coframe/no-Gamma/spin/projective private switches into an explicit public theorem if the corpus supports it",
            success_condition="each local sector has Arg(S_i) stated; independent affine Gamma is either excluded, private-only, or assigned a P4 residual row; no hidden import from GR",
            do_not_do="do not use LC/geodesics because GR uses them; do not claim local GR/Newton; do not push GitHub",
        ),
        base_row(
            route_id="NEXT2415_1_parallel",
            selection_status="held_parallel",
            target_file="2416b-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md",
            target_script="scripts/Y5_R2FR_parent_theta_Qtau_Htau_Href_extraction_or_source_row_2416b.py",
            objective="extract or source parent boundary charge objects needed by the surviving boundary/improvement residual",
            success_condition="theta_MTS, Q_tau, H_tau, H_ref and M_H_ref are either parent-derived or explicit source rows with claim flags false",
            do_not_do="do not borrow EH/Newton denominators without MTS parent current extraction",
        ),
    ]


def copy_branch_rows(sector: list[dict[str, Any]], p4_stack: list[dict[str, Any]], decision: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["sector_audit"], BRANCH_COPIES["queue"], sector),
        ("branch_wep", OUTPUTS["p4_stack"], BRANCH_COPIES["branch_wep"], p4_stack),
        ("beta_docs", OUTPUTS["decision"], BRANCH_COPIES["beta_docs"], decision),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, source_rows in copy_specs:
        write_csv(target_path, source_rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        rows.append(base_row(copy_id=copy_id, source_path=str(source_path), target_path=str(target_path), copied=target_path.exists(), parse_ok=parse_ok, row_count=row_count, parse_detail=parse_detail))
    return rows


def all_generated_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, value in data.items():
        if key != "validation":
            rows.extend(value)
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    sources = data["source_register"]
    rows.append(base_row(validation_id="VAL2415_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2415_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    sector_text = " ".join(str(row) for row in data["sector_audit"])
    required_sectors = ["ordinary_matter", "spin_connection", "em_gauge", "source_worldtube", "clocks", "lightcone", "orbital_readout", "projective_trace", "boundary_improvement"]
    rows.append(base_row(validation_id="VAL2415_02_sector_coverage", status="PASS" if all(sector in sector_text for sector in required_sectors) else "FAIL", detail="all local Gamma-slot sectors represented"))
    rows.append(base_row(validation_id="VAL2415_03_no_public_sector_sum", status="PASS" if "PUBLIC_NO_GAMMA_NOT_CLOSED" in sector_text and "LIVE_PRIMARY_LEAK" in sector_text else "FAIL", detail="public no-Gamma sector sum remains blocked and boundary leak retained"))

    srng_text = " ".join(str(row) for row in data["private_srng_lock"])
    rows.append(base_row(validation_id="VAL2415_04_private_srng_lock", status="PASS" if "PRIVATE_LOCKED_NONCLAIM" in srng_text and "BOUNDARY_REMAINS_LIVE" in srng_text else "FAIL", detail="SRNG locked as private/nonclaim with explicit limits"))

    p4_text = " ".join(str(row) for row in data["p4_stack"])
    rows.append(base_row(validation_id="VAL2415_05_p4_stacks", status="PASS" if "Delta_abs_public" in p4_text and "epsilon_private_connection_abs" in p4_text and "epsilon_boundary_abs" in p4_text else "FAIL", detail="public/private residual stacks written"))
    rows.append(base_row(validation_id="VAL2415_06_p4_nonready", status="PASS" if all(not row["score_ready"] for row in data["p4_stack"]) else "FAIL", detail="P4 stacks remain non-score-ready"))

    gaps = " ".join(str(row) for row in data["gap_ledger"])
    rows.append(base_row(validation_id="VAL2415_07_gap_ledger", status="PASS" if "parent action variable-domain signature" in gaps and "theta_MTS/Q_tau/H_tau/H_ref/M_H_ref" in gaps else "FAIL", detail="main missing derivation objects identified"))

    claim_gate_map = {row["gate_id"]: row for row in data["claim_gates"]}
    blocked_ids = ["CG2415_1_public_sector_sum", "CG2415_3_spin_public_zero", "CG2415_4_projective_public_zero", "CG2415_5_boundary_public_zero", "CG2415_7_local_GR_Newton", "CG2415_8_R10_reopen", "CG2415_9_GitHub"]
    rows.append(base_row(validation_id="VAL2415_08_claim_gates", status="PASS" if all(not claim_gate_map[row_id]["passed"] for row_id in blocked_ids) else "FAIL", detail="public/local/R10/GitHub claims blocked"))

    next_text = " ".join(str(row) for row in data["next_target"])
    rows.append(base_row(validation_id="VAL2415_09_next_target", status="PASS" if "2416-Y5-R2FR-parent-ordinary-action-variable-signature-spine.md" in next_text and "2416b-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md" in next_text else "FAIL", detail="parent action signature selected; theta/charge extraction held parallel"))

    csv_ok = True
    details: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, parse_detail = csv_rows_parse(path)
        csv_ok = csv_ok and parse_ok and row_count > 0
        details.append(f"{path.name}:{row_count}:{parse_detail}")
    rows.append(base_row(validation_id="VAL2415_10_csv_parse", status="PASS" if csv_ok else "FAIL", detail="; ".join(details)))

    copies = data["branch_copies"]
    rows.append(base_row(validation_id="VAL2415_11_branch_copies", status="PASS" if all(row["copied"] and row["parse_ok"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    generated = all_generated_rows(data)
    rows.append(base_row(validation_id="VAL2415_12_no_claim_flags", status="PASS" if all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in generated) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    rows.append(base_row(validation_id="VAL2415_13_formalization_untouched_by_outputs", status="PASS" if not formalization_has_2415_artifacts() else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(base_row(validation_id="VAL2415_OVERALL", status=overall, detail="2415 aggregates the sector Gamma-slot audit, locks SRNG as private/nonclaim, preserves public/P4 residual stacks, and selects parent action signature as the next derivation target"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2415_OVERALL")
    lines = [
        "# 2415 - Y5/R2FR Sector Gamma Slot Audit And Private SRNG Lock",
        "",
        "## Result",
        "",
        "2415 turns the local connection branch into a single scoreboard.",
        "",
        "The good news: the route is no longer woolly. We have exact conditional lemmas for variable absence, owned-coframe Levi-Civita connection, coframe-owned spin connection, private SRNG source/readout silence, and private projective silence.",
        "",
        "The hard news: they are not yet a public sector-sum theorem. The public local-GR/Newton reduction is still blocked because the parent action variable-domain signature is not signed across all sectors, and the boundary/improvement current remains the primary private-branch leak.",
        "",
        "So the private branch is allowed, but locked: it may be used internally with `valid_for_claim=false`, never as a public proof. Publicly, the affine/P4 residual stack remains live.",
        "",
        "## Source Register",
        "",
        md_table(data["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Sector Gamma Slot Audit",
        "",
        md_table(data["sector_audit"], ["row_id", "sector", "gamma_slot_status", "private_status", "public_residual", "proof_gap", "next_action", "valid_for_claim"]),
        "",
        "## Private SRNG Lock",
        "",
        md_table(data["private_srng_lock"], ["row_id", "clause", "allowed_use", "forbidden_use", "locked_status", "valid_for_claim"]),
        "",
        "## Public Private P4 Component Stack",
        "",
        md_table(data["p4_stack"], ["row_id", "stack", "formula", "status", "score_ready", "valid_for_claim"]),
        "",
        "## Local GR Gap Ledger",
        "",
        md_table(data["gap_ledger"], ["row_id", "item", "current_status", "why_it_matters", "needed_to_close", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(data["claim_gates"], ["gate_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(data["decision"], ["decision_id", "decision", "rationale", "consequence", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(data["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(data["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(data["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Practical Status",
        "",
        "This is a useful pivot point. The best next move is not another local-test runner and not GitHub; it is the parent ordinary action variable-signature spine. If that signs, several conditional zero theorems become public structure. If it fails, the P4 stack is already waiting and we know exactly which residuals must be bounded.",
        "",
        f"Validation overall: `{overall['status']}`.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "sector_audit": sector_audit_rows(),
        "private_srng_lock": private_srng_lock_rows(),
        "p4_stack": p4_stack_rows(),
        "gap_ledger": gap_ledger_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["source_register"])
    write_csv(OUTPUTS["sector_audit"], data["sector_audit"])
    write_csv(OUTPUTS["private_srng_lock"], data["private_srng_lock"])
    write_csv(OUTPUTS["p4_stack"], data["p4_stack"])
    write_csv(OUTPUTS["gap_ledger"], data["gap_ledger"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_rows(data["sector_audit"], data["p4_stack"], data["decision"])
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
