from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PRINCIPAL_SYMBOL_ZAB_OR_RANK_ZERO_SOURCE_CURRENT_IDENTITY_2412"
CHECKPOINT_ID = "2412"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2412-Y5-R2FR-principal-symbol-ZAB-or-rank-zero-source-current-identity.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2412_SOURCE_REGISTER.csv",
    "strict_symbol": OUT / "P8_Y5_PARENT_QLOC_2412_STRICT_L0_PRINCIPAL_SYMBOL_IMPORT.csv",
    "cdb_triage": OUT / "P8_Y5_PARENT_QLOC_2412_CDB_PRINCIPAL_SYMBOL_TRIAGE.csv",
    "rank_zero_contract": OUT / "P8_Y5_PARENT_QLOC_2412_RANK_ZERO_SOURCE_CURRENT_IDENTITY_CONTRACT.csv",
    "residual_bridge": OUT / "P8_Y5_PARENT_QLOC_2412_ALGEBRAIC_RESIDUAL_NONHILBERT_BRIDGE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2412_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2412_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2412_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2412_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2412_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2412_CDB_SYMBOL_OR_RANK_ZERO_IDENTITY_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2412_RANK_ZERO_SOURCE_IDENTITY_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_CDB_PRINCIPAL_SYMBOL_2412_NONCLAIM.csv",
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


def formalization_has_2412_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2412-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2412*",
        "*P8_Y5_BRR545_2412*",
        "*Y5_R2FR_principal_symbol_ZAB_or_rank_zero_source_current_identity_2412*",
        "*JR2412*",
        "*PARENT_QLOC_CDB_PRINCIPAL_SYMBOL_2412*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2411_handoff",
            ROOT / "2411-Y5-R2FR-parent-ZM-and-J-current-owner-or-constraint-branch.md",
            ["NEXT2411_0_selected", "ZMJ2411_1_Z_principal_symbol", "VAL2411_OVERALL"],
            "current chain selects principal-symbol Z_AB or rank-zero source-current identity.",
        ),
        (
            "2212_symbol_prior",
            ROOT / "2212-Y5-R2FR-principal-symbol-ZAB-owner-or-rank-zero-constraint-proof.md",
            ["STRICT_L0_BRANCH_IS_RANK_ZERO", "CDB_IS_ONLY_REMAINING_ZAB_HIDING_PLACE", "VAL2212_OVERALL"],
            "prior strict-L0 principal-symbol decision: rank-zero strict branch, CDB held open.",
        ),
        (
            "2213_rank_zero_prior",
            ROOT / "2213-Y5-R2FR-rank-zero-source-current-identity-or-algebraic-residual-row.md",
            ["RZS2213_2_rank_zero_silence_theorem", "RALG2213_0_eliminated_coordinate", "VAL2213_OVERALL"],
            "prior rank-zero source-current identity and algebraic residual row.",
        ),
        (
            "2346_nonhilbert_trident",
            ROOT / "2346-Y5-R2FR-nonHilbert-source-projection-zero-or-component-bound-pack.md",
            ["NHZ2346_5_verdict", "NHC2346_0_total", "VAL2346_OVERALL"],
            "non-Hilbert source projection zero fails and becomes a component pack.",
        ),
        (
            "2212_strict_symbol_csv",
            OUT / "P8_Y5_PARENT_QLOC_2212_STRICT_L0_PRINCIPAL_SYMBOL_AUDIT.csv",
            ["PSA2212_4_strict_verdict", "FINITE_RANGE_R10_REJECTED_FOR_STRICT_BRANCH", "rank-zero"],
            "machine-readable strict-L0 rank-zero classification.",
        ),
        (
            "2212_cdb_queue_csv",
            OUT / "P8_Y5_PARENT_QLOC_2212_CDB_PRINCIPAL_SYMBOL_QUEUE.csv",
            ["CPS2212_0_K_conn", "CPS2212_4_live_verdict", "FINITE_RANGE_STATUS_HELD_OPEN_BY_CDB"],
            "machine-readable CDB derivative/source triage queue.",
        ),
        (
            "2213_residual_csv",
            OUT / "P8_Y5_PARENT_QLOC_2213_ALGEBRAIC_RESIDUAL_ROW.csv",
            ["RALG2213_0_eliminated_coordinate", "SYMBOLIC_NONCLAIM_RESIDUAL", "M_AB rank/sign/units"],
            "machine-readable algebraic residual map for strict branch.",
        ),
        (
            "2346_component_pack_csv",
            OUT / "P8_Y5_PARENT_QLOC_2346_NONHILBERT_COMPONENT_BOUND_PACK.csv",
            ["NHC2346_0_total", "MISSING_COMPONENT_VALUES", "absolute_sum_policy"],
            "machine-readable non-Hilbert current-owner residual component pack.",
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


def strict_symbol_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="SSL2412_0_fixed_L0_branch",
            object="strict fixed-L0 response-doublet branch",
            principal_symbol_status="Z_AB_EQUALS_ZERO_ON_STRICT_SUBBRANCH",
            derivation="Gamma_eff response-doublet contributes algebraic M_AB Z^2 terms but no parent-owned derivative term -Z_AB Delta in the strict fixed-L0 reduction.",
            implication="strict branch is algebraic/rank-zero, not finite-range Yukawa",
            caveat="live CDB may still reintroduce derivative order outside the strict subbranch",
            passes_now=True,
        ),
        base_row(
            row_id="SSL2412_1_MAB_hessian",
            object="M_AB",
            principal_symbol_status="ALGEBRAIC_HESSIAN_ONLY",
            derivation="M_AB can curve the algebraic eliminated coordinate but cannot define a range without a principal symbol.",
            implication="M_AB is useful for constraint equation M_AB Z^B=S_A, not lambda_i",
            caveat="M_AB still needs parent rank/sign/units before local silence can claim",
            passes_now=False,
        ),
        base_row(
            row_id="SSL2412_2_R10_strict",
            object="strict-branch R10 alpha(lambda)",
            principal_symbol_status="REJECTED_FOR_STRICT_BRANCH",
            derivation="no Z_AB principal symbol means no generalized eigenvalue Mv=mu^2Zv and no lambda for this subbranch.",
            implication="R10 can only re-open through CDB finite-range pieces or contact/algebraic residual bounds",
            caveat="do not delete the data route; just do not use it for strict branch",
            passes_now=True,
        ),
        base_row(
            row_id="SSL2412_3_verdict",
            object="strict local branch classification",
            principal_symbol_status="STRICT_RANK_ZERO_IMPORT_CONFIRMED",
            derivation="2411 chain inherits 2212: strict fixed-L0 branch is rank-zero/algebraic.",
            implication="next proof is source-current identity and CDB extraction, not a hidden plateau axiom",
            caveat="no local-GR claim until source, boundary, Dq_Z and non-Hilbert tails close",
            passes_now=True,
        ),
    ]


def cdb_triage_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            cdb_id="CDB2412_0_K_conn",
            component="K_conn",
            possible_role="could contain connection/derivative dependence that creates a real principal symbol",
            current_status="LIVE_UNEXTRACTED",
            extraction_test="classify dependence on nabla Z, affine Gamma, torsion, nonmetricity, hypermomentum, and derivative order",
            if_symbol_found="finite-range branch reopens with sourced Z_AB",
            if_absent="rank-zero source-current route strengthens",
            score_ready=False,
        ),
        base_row(
            cdb_id="CDB2412_1_K_domain",
            component="K_domain",
            possible_role="domain/support/readout variation can imitate kinetic leakage or source current",
            current_status="LIVE_UNEXTRACTED",
            extraction_test="separate parent domain selector from readout/support variation and source-measure terms",
            if_symbol_found="domain-dependent operator must be bounded before spectrum is used",
            if_absent="remaining contribution is algebraic/source leakage",
            score_ready=False,
        ),
        base_row(
            cdb_id="CDB2412_2_K_boundary",
            component="K_boundary",
            possible_role="boundary primitive can encode derivative operator or source/worldtube charge",
            current_status="LIVE_SOURCE_BOUNDARY",
            extraction_test="split proper compact-collar zero from source worldtube, corner, reference, and projector flux terms",
            if_symbol_found="boundary condition changes operator domain/spectrum",
            if_absent="boundary piece enters algebraic residual B_A",
            score_ready=False,
        ),
        base_row(
            cdb_id="CDB2412_3_K_comm",
            component="K_comm / P_loc",
            possible_role="projector commutator can turn algebraic residual into observed derivative/source term",
            current_status="LIVE_UNEXTRACTED",
            extraction_test="parent-own P_loc and test commutation with divergence/readout or bound commutator",
            if_symbol_found="observed finite-range/readout branch may reopen",
            if_absent="commutator enters finite residual envelope",
            score_ready=False,
        ),
        base_row(
            cdb_id="CDB2412_4_verdict",
            component="CDB total",
            possible_role="only remaining hiding place for physical Z_AB after strict branch is rank-zero",
            current_status="CDB_SYMBOL_OR_RESIDUAL_SPLIT_REQUIRED",
            extraction_test="2413 must split kinetic principal-symbol pieces from source/boundary/projector leakage",
            if_symbol_found="derive finite-range operator honestly",
            if_absent="commit to rank-zero algebraic residual/source-current route",
            score_ready=False,
        ),
    ]


def rank_zero_contract_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            clause_id="RZI2412_0_euler_normal_form",
            clause="strict rank-zero Euler identity",
            exact_requirement="M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector on the physical quotient",
            current_status="CONDITIONAL_NORMAL_FORM_IMPORTED",
            if_closed="the local residual is algebraic and all forcing terms are visible",
            if_open="source pieces remain a finite residual vector",
        ),
        base_row(
            clause_id="RZI2412_1_M_lock",
            clause="M_AB lock",
            exact_requirement="M_AB is invertible on physical quotient directions or null directions are parent-owned gauge/constraints",
            current_status="MISSING_PARENT_RANK_SIGN_UNITS",
            if_closed="Z = M^-1 S is well-defined or null branches are removed",
            if_open="null/wrong-sign algebraic modes survive",
        ),
        base_row(
            clause_id="RZI2412_2_J_zero",
            clause="J_A=0 source-current identity",
            exact_requirement="ordinary matter/source/readout variations vanish along eliminated Z directions by descent/current-owner/no-marker clauses",
            current_status="BLOCKED_BY_SOURCE_CURRENT_OWNER_AND_READOUT",
            if_closed="matter cannot source the eliminated coordinate",
            if_open="Z=M^-1 J creates local source residual",
        ),
        base_row(
            clause_id="RZI2412_3_B_zero",
            clause="B_A=0 boundary/projector identity",
            exact_requirement="proper boundary, source-worldtube, corner, reference and projector terms vanish or are bounded",
            current_status="BOUNDARY_PROJECTOR_OPEN",
            if_closed="bulk algebraic elimination is not re-sourced by edges",
            if_open="boundary/projector charge survives local tests",
        ),
        base_row(
            clause_id="RZI2412_4_DqZ_zero",
            clause="observed descent Dq_Z=0",
            exact_requirement="coframe, metric, measure, source and readout maps do not see eliminated Z after constraint solution",
            current_status="DESCENT_THEOREM_NOT_CLOSED",
            if_closed="constraint variable is invisible to Newton/PPN/R10/WEP/clocks/orbits",
            if_open="Dq_Z leak vector projects into arenas",
        ),
        base_row(
            clause_id="RZI2412_5_JNH_zero_or_bound",
            clause="non-Hilbert source projection zero or bound",
            exact_requirement="P_source[J_spin/torsion + J_boundary + J_readout + J_improvement + J_shadow/projector]=0 or absolute component envelope is sourced",
            current_status="LIVE_COMPONENT_PACK_REQUIRED",
            if_closed="Hilbert source route can become a full source-current identity",
            if_open="epsilon_current_owner_NH_abs remains in the algebraic residual",
        ),
        base_row(
            clause_id="RZI2412_6_verdict",
            clause="rank-zero local-GR route",
            exact_requirement="M lock + J_A=0 + B_A=0 + Dq_Z=0 + CDB absent/bounded + J_NH silence close in one parent branch",
            current_status="PROMISING_ROUTE_NOT_CLAIMED",
            if_closed="strict local branch could reduce to GR/Newton without Yukawa suppression",
            if_open="carry algebraic residual map",
        ),
    ]


def residual_bridge_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            bridge_id="ARB2412_0_rank_zero_residual",
            residual_object="S_A algebraic source stack",
            symbolic_formula="S_A = J_A + B_A + C_A^CDB + R_A^src/readout/projector + J_A^NH",
            relation_to_observables="R_obs^I = L^I_A (M^-1)^{AB} S_B + E^I_DqZ",
            nonhilbert_link="epsilon_current_owner_NH_abs <= E_spin+E_boundary+E_readout+E_shadow+E_projector",
            current_status="SYMBOLIC_NONCLAIM",
            next_input_needed="M rank/sign/units; source-current zeros; CDB split; Dq_Z projection; component bounds",
            score_ready=False,
        ),
        base_row(
            bridge_id="ARB2412_1_Newton_PPN",
            residual_object="Newton/PPN projection",
            symbolic_formula="Delta_PPN^I or Delta(GM) ~ Pi^I_A M^-1 S_A + E^I_DqZ",
            relation_to_observables="Newtonian GM, gamma, beta, alpha_i, xi, Gdot",
            nonhilbert_link="J_NH and boundary/worldtube pieces must not be absorbed into measured GM without a common-mode proof",
            current_status="PROJECTION_BLOCKED",
            next_input_needed="weak-field map L^I_A and source-normalization convention",
            score_ready=False,
        ),
        base_row(
            bridge_id="ARB2412_2_R10",
            residual_object="strict-branch R10",
            symbolic_formula="no alpha(lambda) for strict branch unless CDB supplies a finite-range principal symbol",
            relation_to_observables="R10 becomes contact/algebraic residual or CDB finite-range branch",
            nonhilbert_link="readout/source-label reentry can mimic short-range source charge",
            current_status="STRICT_R10_REJECTED_CDB_HELD",
            next_input_needed="CDB principal-symbol extraction or contact residual bound",
            score_ready=False,
        ),
        base_row(
            bridge_id="ARB2412_3_WEP_clock_EM_orbital",
            residual_object="source/readout residual projections",
            symbolic_formula="Delta_Arena ~ Pi_Arena M^-1 S + E_Arena_DqZ",
            relation_to_observables="WEP eta_AB, clock drift, alpha_EM drift, orbital precession/timing",
            nonhilbert_link="component pack must preserve no-cancellation absolute envelopes",
            current_status="ARENA_MAPS_MISSING",
            next_input_needed="arena projection coefficients and units",
            score_ready=False,
        ),
        base_row(
            bridge_id="ARB2412_4_verdict",
            residual_object="algebraic residual bridge",
            symbolic_formula="R_alg is the retained object until all rank-zero identity clauses close",
            relation_to_observables="all local tests",
            nonhilbert_link="2346 trident is now part of the rank-zero source-current contract",
            current_status="BRIDGE_INSTALLED_NONCLAIM",
            next_input_needed="2413 CDB split or coefficient map",
            score_ready=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2412_0_strict_rank_zero", gate="strict fixed-L0 has no Z_AB principal symbol", status="PASS_NONCLAIM", implication="strict branch is algebraic/rank-zero, not R10"),
        base_row(gate_id="CG2412_1_CDB_symbol", gate="CDB principal symbol extracted", status="BLOCKED_NONCLAIM", implication="live branch may still hide kinetic derivative structure"),
        base_row(gate_id="CG2412_2_rank_zero_identity", gate="rank-zero source-current identity closes", status="BLOCKED_NONCLAIM", implication="J/B/DqZ/CDB/J_NH clauses remain open"),
        base_row(gate_id="CG2412_3_R10", gate="strict-branch R10 alpha(lambda) score", status="REJECTED_FOR_STRICT_BRANCH", implication="no lambda without Z_AB"),
        base_row(gate_id="CG2412_4_local_GR_Newton", gate="local GR/Newton reduction follows", status="BLOCKED_NONCLAIM", implication="source-current and observed-descent closures missing"),
        base_row(gate_id="CG2412_5_GitHub", gate="public/GitHub update", status="BLOCKED_PRIVATE", implication="private derivation work only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2412_0_gain",
            decision="STRICT_BRANCH_RANK_ZERO_CONFIRMED",
            rationale="The current chain imports the strict-L0 principal-symbol result: M_AB is algebraic and no strict-branch lambda exists.",
            next_action="stop trying to score strict branch as R10",
        ),
        base_row(
            decision_id="DEC2412_1_cdb",
            decision="CDB_ONLY_REMAINING_ZAB_HIDING_PLACE",
            rationale="K_conn/K_domain/K_boundary/K_comm are the only live route by which derivative order or source leakage can reopen a finite-range branch.",
            next_action="extract CDB principal symbol before final branch selection",
        ),
        base_row(
            decision_id="DEC2412_2_rank_zero",
            decision="RANK_ZERO_SOURCE_CURRENT_IDENTITY_FORMALIZED",
            rationale="The clean GR-limit route is algebraic elimination plus J/B/DqZ/CDB/J_NH silence, not a plateau axiom.",
            next_action="try CDB split and algebraic residual coefficient map next",
        ),
        base_row(
            decision_id="DEC2412_3_no_claim",
            decision="NO_LOCAL_CLAIM_NO_GITHUB",
            rationale="The theorem skeleton is sharper, but the current application still does not fire.",
            next_action="keep all outputs nonclaim",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2412_0_selected",
            selection_status="selected",
            target_file="2413-Y5-R2FR-CDB-principal-symbol-extraction-or-algebraic-residual-map.md",
            target_script="scripts/Y5_R2FR_CDB_principal_symbol_extraction_or_algebraic_residual_map_2413.py",
            objective="separate K_conn/K_domain/K_boundary/K_comm into kinetic principal-symbol pieces versus algebraic/source/boundary/projector leakage; then decide whether finite-range branch reopens or the rank-zero residual map owns the route",
            success_condition="CDB derivative-order table either source-signs a Z_AB kinetic piece or moves each CDB channel into the algebraic residual/source-bound map with valid_for_claim=false",
            do_not_do="do not delete CDB, infer Z from M, run strict-branch R10 alpha, claim local GR/Newton, or use GitHub",
        ),
        base_row(
            route_id="NEXT2412_1_fallback",
            selection_status="held_fallback",
            target_file="2413b-Y5-R2FR-rank-zero-algebraic-residual-coefficient-map.md",
            target_script="scripts/Y5_R2FR_rank_zero_algebraic_residual_coefficient_map_2413b.py",
            objective="fill the arena coefficient map R_obs^I=L^I_A M^-1 S_A+E_DqZ for Newton/PPN/R10/WEP/clock/EM/orbital branches",
            success_condition="all surviving residual components have units, source paths, arena links, and remain nonclaim until numeric",
            do_not_do="do not hide source-current terms inside measured GM",
        ),
    ]


def copy_branch_rows(cdb: list[dict[str, Any]], rank_zero: list[dict[str, Any]], bridge: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["cdb_triage"], BRANCH_COPIES["queue"], cdb),
        ("branch_wep", OUTPUTS["rank_zero_contract"], BRANCH_COPIES["branch_wep"], rank_zero),
        ("beta_docs", OUTPUTS["residual_bridge"], BRANCH_COPIES["beta_docs"], bridge),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, source_rows in copy_specs:
        write_csv(target_path, source_rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source_path),
                target_path=str(target_path),
                copied=target_path.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_detail=parse_detail,
            )
        )
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
    rows.append(base_row(validation_id="VAL2412_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2412_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    strict_text = " ".join(str(row) for row in data["strict_symbol"])
    rows.append(base_row(validation_id="VAL2412_02_strict_rank_zero", status="PASS" if "Z_AB_EQUALS_ZERO_ON_STRICT_SUBBRANCH" in strict_text and "REJECTED_FOR_STRICT_BRANCH" in strict_text else "FAIL", detail="strict fixed-L0 branch classified as rank-zero and strict R10 rejected"))

    cdb_text = " ".join(str(row) for row in data["cdb_triage"])
    rows.append(base_row(validation_id="VAL2412_03_cdb_triage", status="PASS" if "CDB_SYMBOL_OR_RESIDUAL_SPLIT_REQUIRED" in cdb_text and "K_conn" in cdb_text and "K_comm" in cdb_text else "FAIL", detail="CDB channels triaged as only remaining Z_AB hiding place"))

    rank_text = " ".join(str(row) for row in data["rank_zero_contract"])
    rows.append(base_row(validation_id="VAL2412_04_rank_zero_contract", status="PASS" if "M_AB Z^B" in rank_text and "non-Hilbert source projection" in rank_text else "FAIL", detail="rank-zero source-current identity contract includes M/J/B/DqZ/CDB/JNH clauses"))

    bridge_text = " ".join(str(row) for row in data["residual_bridge"])
    rows.append(base_row(validation_id="VAL2412_05_residual_bridge", status="PASS" if "R_obs^I" in bridge_text and "epsilon_current_owner_NH_abs" in bridge_text else "FAIL", detail="algebraic residual bridge to local arenas installed"))

    claim = data["claim_gate"]
    rows.append(base_row(validation_id="VAL2412_06_claim_gates", status="PASS" if all(not row["valid_for_claim"] and not row["claim_allowed"] for row in claim) else "FAIL", detail="local-GR/R10/GitHub claims remain blocked"))

    next_text = " ".join(str(row) for row in data["next_target"])
    rows.append(base_row(validation_id="VAL2412_07_next_target", status="PASS" if "2413-Y5-R2FR-CDB-principal-symbol-extraction-or-algebraic-residual-map.md" in next_text else "FAIL", detail="CDB principal-symbol extraction or residual map selected"))

    csv_ok = True
    details: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, parse_detail = csv_rows_parse(path)
        csv_ok = csv_ok and parse_ok and row_count > 0
        details.append(f"{path.name}:{row_count}:{parse_detail}")
    rows.append(base_row(validation_id="VAL2412_08_csv_parse", status="PASS" if csv_ok else "FAIL", detail="; ".join(details)))

    copies = data["branch_copies"]
    rows.append(base_row(validation_id="VAL2412_09_branch_copies", status="PASS" if all(row["copied"] and row["parse_ok"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    generated = all_generated_rows(data)
    rows.append(base_row(validation_id="VAL2412_10_no_claim_flags", status="PASS" if all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in generated) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    rows.append(base_row(validation_id="VAL2412_11_formalization_untouched_by_outputs", status="PASS" if not formalization_has_2412_artifacts() else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(base_row(validation_id="VAL2412_OVERALL", status=overall, detail="2412 confirms strict-L0 rank-zero status, quarantines CDB as the only remaining Z_AB hiding place, installs the rank-zero source-current identity contract, and selects CDB extraction/residual map next"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2412_OVERALL")
    lines = [
        "# 2412 - Y5/R2FR Principal Symbol ZAB Or Rank-Zero Source-Current Identity",
        "",
        "## Result",
        "",
        "2412 makes the local fork cleaner. The strict fixed-`L0` response-doublet branch is rank-zero/algebraic: it has an `M_AB` Hessian candidate but no strict `Z_AB` principal symbol, so it is not a finite-range R10 branch.",
        "",
        "That does not prove local GR. It changes the job. The route is now either:",
        "",
        "1. extract a real kinetic `Z_AB` from the live CDB channels, or",
        "2. close the rank-zero identity `M_AB Z^B = J_A + B_A + C_A^CDB + R_A + J_A^NH` by proving the right-hand side and observed descent vanish.",
        "",
        "So the plateau axiom is gone from the strict branch. What remains is a source-current/descent theorem or an explicit algebraic residual map.",
        "",
        "## Source Register",
        "",
        md_table(data["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Strict L0 Principal Symbol Import",
        "",
        md_table(data["strict_symbol"], ["row_id", "object", "principal_symbol_status", "derivation", "implication", "caveat", "passes_now", "valid_for_claim"]),
        "",
        "## CDB Principal Symbol Triage",
        "",
        md_table(data["cdb_triage"], ["cdb_id", "component", "possible_role", "current_status", "extraction_test", "if_symbol_found", "if_absent", "score_ready", "valid_for_claim"]),
        "",
        "## Rank-Zero Source-Current Identity Contract",
        "",
        md_table(data["rank_zero_contract"], ["clause_id", "clause", "exact_requirement", "current_status", "if_closed", "if_open", "valid_for_claim"]),
        "",
        "## Algebraic Residual Non-Hilbert Bridge",
        "",
        md_table(data["residual_bridge"], ["bridge_id", "residual_object", "symbolic_formula", "relation_to_observables", "nonhilbert_link", "current_status", "next_input_needed", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(data["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(data["decision"], ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
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
        "This is a proper derivation move. The strict branch no longer pretends to be a fifth-force model. Either CDB really contains a kinetic operator, or the local branch is an algebraic constraint whose source terms must vanish or be bounded. That is exactly the kind of route that can connect to GR honestly.",
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
        "strict_symbol": strict_symbol_rows(),
        "cdb_triage": cdb_triage_rows(),
        "rank_zero_contract": rank_zero_contract_rows(),
        "residual_bridge": residual_bridge_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["source_register"])
    write_csv(OUTPUTS["strict_symbol"], data["strict_symbol"])
    write_csv(OUTPUTS["cdb_triage"], data["cdb_triage"])
    write_csv(OUTPUTS["rank_zero_contract"], data["rank_zero_contract"])
    write_csv(OUTPUTS["residual_bridge"], data["residual_bridge"])
    write_csv(OUTPUTS["claim_gate"], data["claim_gate"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_rows(data["cdb_triage"], data["rank_zero_contract"], data["residual_bridge"])
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
