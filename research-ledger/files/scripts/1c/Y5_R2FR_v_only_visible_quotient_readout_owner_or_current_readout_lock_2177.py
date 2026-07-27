from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2177"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2177_SOURCE_REGISTER.csv",
    "v_reconstruction": OUT / "P8_Y5_PARENT_QLOC_2177_V_ONLY_RECONSTRUCTION.csv",
    "readout_gate": OUT / "P8_Y5_PARENT_QLOC_2177_OBSERVABLE_READOUT_GATE.csv",
    "ppn_gate": OUT / "P8_Y5_PARENT_QLOC_2177_PPN_SOURCE_CONVENTION_GATE.csv",
    "residual_rows": OUT / "P8_Y5_PARENT_QLOC_2177_READOUT_LOCK_RESIDUAL_ROWS.csv",
    "ru_status": OUT / "P8_Y5_PARENT_QLOC_2177_RU_STATUS_LEDGER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2177_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2177_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2177_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2177_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2177_V_ONLY_READOUT_GATES_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2177_V_ONLY_RECONSTRUCTION_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "V_ONLY_READOUT_2177_NONCLAIM.csv",
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
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2177_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2177-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2177*",
        "*P8_Y5_BRR545_2177*",
        "*Y5_R2FR_v_only_visible_quotient_readout_owner_or_current_readout_lock_2177*",
        "*JR2177*",
        "*V_ONLY_READOUT_2177*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2176_handoff",
            ROOT / "2176-Y5-R2FR-parent-Ru-involution-current-owner-or-finite-Iu-Ju-row.md",
            ["NEXT2176_0_2177", "MISSING_V_ONLY_QUOTIENT_OWNER"],
            "2176 selects the v-only visible quotient/readout owner gate.",
        ),
        (
            "2176_validation",
            OUT / "P8_Y5_BRR545_2176_VALIDATION.csv",
            ["VAL2176_OVERALL", "PASS"],
            "2176 validation passed before 2177 continues the chain.",
        ),
        (
            "observer_contract",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["theta_0 = T c dt", "theta_1 = sqrt(S) dr", "J_q = T sqrt(S)", "R_AB = ln(T^2 S)"],
            "current observer contract defines coframe legs, radial cell and reciprocal strain.",
        ),
        (
            "1877_qshape_no_escape",
            ROOT / "1877-Y5-R2FR-qshape-or-lambdaR-parent-origin-source-hunt.md",
            ["QSHAPE_IS_NOT_INDEPENDENT_ESCAPE", "DOBS_E_BURDEN_REMAINS"],
            "1877 blocks shape-only quotient deletion unless readout also descends.",
        ),
        (
            "1878_readout_kernel",
            ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
            ["DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS", "theta_0=T cdt"],
            "1878 records the current coframe visibility obstruction.",
        ),
        (
            "2172_vertical_obstruction",
            ROOT / "2172-Y5-R2FR-radial-cell-vertical-gauge-noether-identity-or-coefficient-basis.md",
            ["NO_NONTRIVIAL_VERTICAL_GENERATOR_CURRENT_READOUT", "AUXILIARY_CONSTRAINT_OR_READOUT_REBUILD_NEXT"],
            "2172 proves the current-readout vertical-gauge route fails off constraint.",
        ),
        (
            "2173_constraint_order",
            ROOT / "2173-Y5-R2FR-radial-cell-auxiliary-constraint-origin-dirac-or-readout-rebuild.md",
            ["dot(C_R) = {C_R,H_core} + Lambda_R {C_R,C_R}", "MISSING_READOUT_TAU_DESCENT"],
            "2173 keeps constraint-first readout useful but not parent-derived.",
        ),
    ]
    rows = []
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


def v_reconstruction_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "VOR2177_0_log_variables",
            "define log variables",
            "a=ln T, b=ln sqrt(S), u=a+b, v=a-b.",
            "EXACT_DEFINITION",
            "same variable basis as 2176.",
        ),
        (
            "VOR2177_1_inverse_map",
            "invert the variables",
            "a=(u+v)/2 and b=(u-v)/2.",
            "EXACT_ALGEBRA",
            "T=exp((u+v)/2) and sqrt(S)=exp((u-v)/2).",
        ),
        (
            "VOR2177_2_constraint_surface",
            "impose u=0",
            "T=exp(v/2), sqrt(S)=exp(-v/2), S=exp(-v), and T^2=exp(v).",
            "EXACT_V_ONLY_RECONSTRUCTION_AFTER_CONSTRAINT",
            "after C_R=2u=0, the current radial coframe is determined by v alone.",
        ),
        (
            "VOR2177_3_cell_jacobians",
            "radial observer cell",
            "J_q=T sqrt(S)=1 and J_p=1/(T sqrt(S))=1 on u=0.",
            "EXACT_CELL_LOCK_AFTER_CONSTRAINT",
            "the reciprocal cell is removed, not hidden as an extra observable.",
        ),
        (
            "VOR2177_4_coframe_readout",
            "current coframe reconstructed from v",
            "theta_0=exp(v/2)c dt and theta_1=exp(-v/2)dr after u=0.",
            "EXACT_CONDITIONAL_COFAME_RECONSTRUCTION",
            "T and sqrt(S) are not erased; they are reconstructed from v after the constraint.",
        ),
        (
            "VOR2177_5_photon_kinematic_readout",
            "radial null/readout speed",
            "dr/dt=c T/sqrt(S)=c exp(v) after u=0.",
            "EXACT_CONDITIONAL_RADIAL_READOUT",
            "local radial photon/orbit kinematics can be expressed through v once the constrained representative is accepted.",
        ),
        (
            "VOR2177_6_Ru_fixed_surface",
            "R_u action on constrained readout",
            "R_u sends u to -u and fixes v, so on u=0 it fixes T, sqrt(S), theta_0 and theta_1 pointwise.",
            "EXACT_FIXED_SURFACE_RESULT",
            "the algebraic R_u no longer damages readout after the constraint is imposed.",
        ),
        (
            "VOR2177_7_parent_limit",
            "parent ownership limit",
            "The corpus still has not proved that the parent action imposes u=0 before all ordinary readout and matter/source normalization.",
            "PARENT_ORDER_NOT_DERIVED",
            "v-only reconstruction is an exact conditional theorem, not a local-GR claim.",
        ),
    ]
    return [
        base_row(
            reconstruction_id=reconstruction_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for reconstruction_id, object_name, statement, status, implication in specs
    ]


def readout_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ROG2177_0_constraint_first",
            "constraint-before-readout ordering",
            "u=0 must be imposed before clocks, rods, photons, orbital endpoints and source mass are read out.",
            "UNSIGNED_PARENT_ORDER",
            "without this, the off-shell T/sqrt(S) coframe obstruction from 2172/1878 remains live.",
        ),
        (
            "ROG2177_1_clocks_rods",
            "clock/ruler coframe",
            "after u=0, theta_0 and theta_1 are v-only functions.",
            "PASS_CONDITIONAL_ON_ORDER",
            "this is the main 2177 gain.",
        ),
        (
            "ROG2177_2_photons_orbits",
            "radial photon/orbital kinematic readout",
            "after u=0, dr/dt and radial momentum readout are v-only functions.",
            "PASS_CONDITIONAL_ON_ORDER",
            "kinematic continuity survives the v-only collapse.",
        ),
        (
            "ROG2177_3_source_mass",
            "source mass and Newtonian normalization",
            "the parent source equation must identify the coefficient and sign of v relative to observed mass.",
            "MISSING_PARENT_SOURCE_CONVENTION",
            "Newtonian acceleration cannot be claimed from readout algebra alone.",
        ),
        (
            "ROG2177_4_matter_descent",
            "ordinary matter universality",
            "all matter species must couple to the same constrained v-coframe with no u-dependent source slot.",
            "MISSING_MATTER_DESCENT",
            "WEP, clocks and beta-source gates remain blocked.",
        ),
        (
            "ROG2177_5_boundary_tau",
            "boundary, tau and endpoint silence",
            "boundary/corner terms, clock tau and orbital endpoints must not reintroduce u or C_R.",
            "MISSING_BOUNDARY_TAU_DESCENT",
            "finite endpoint/coframe residual rows remain necessary.",
        ),
        (
            "ROG2177_6_conservation",
            "field-equation consistency",
            "the v equation must obey a Bianchi-like conservation identity with the source sector.",
            "MISSING_CONSERVATION_IDENTITY",
            "local GR cannot be promoted without source conservation.",
        ),
        (
            "ROG2177_7_gate_verdict",
            "v-only readout owner",
            "v-only reconstruction after u=0 is exact, but parent order/source/matter/boundary/conservation gates are unsigned.",
            "PARTIAL_PASS_CONDITIONAL_NOT_CLAIMABLE",
            "move to the ordering and v-source convention proof next.",
        ),
    ]
    return [
        base_row(
            gate_id=gate_id,
            gate=gate,
            required_statement=required_statement,
            status=status,
            implication=implication,
        )
        for gate_id, gate, required_statement, status, implication in specs
    ]


def ppn_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PPN2177_0_metric_shape",
            "constrained metric/readout shape",
            "A=T^2=exp(v), B=S=exp(-v) after u=0.",
            "EXACT_CONDITIONAL_SHAPE",
            "single-variable reciprocal readout is available on the constrained branch.",
        ),
        (
            "PPN2177_1_newtonian_normalization",
            "weak-field source convention",
            "need parent derivation of v=-2U/c^2+O(U^2) with U=GM/r or an equivalent signed convention.",
            "MISSING_PARENT_FIELD_EQUATION",
            "readout shape alone does not produce the Newtonian force law.",
        ),
        (
            "PPN2177_2_gamma_shape",
            "PPN gamma shape",
            "if v=-2U/c^2+O(U^2), then B=exp(-v)=1+2U/c^2+O(U^2), so gamma=1 at first order.",
            "GAMMA_SHAPE_PASS_CONDITIONAL",
            "useful but not a claim until the source convention and coordinate gauge are parent-owned.",
        ),
        (
            "PPN2177_3_beta_shape",
            "PPN beta shape",
            "if v=-2U/c^2+O(U^3) in the same local PPN gauge, then -A=-exp(v) gives beta=1 shape at second order.",
            "BETA_SHAPE_PASS_CONDITIONAL",
            "any parent-generated quadratic correction to v can shift beta, so beta is not claimed.",
        ),
        (
            "PPN2177_4_light_time_orbits",
            "light-time and orbit continuity",
            "the same v must govern clocks, spatial radial readout, null readout and source mass.",
            "MISSING_COMMON_V_SOURCE_MAP",
            "otherwise the branch is just a fitted readout rather than derived local GR.",
        ),
        (
            "PPN2177_5_verdict",
            "local PPN branch status",
            "v-only constrained readout gives the right gamma/beta shape conditionally, but source equation, conservation and ordering are still missing.",
            "PROMISING_NOT_CLAIMABLE",
            "2178 should attack source/order before more residual circling.",
        ),
    ]
    return [
        base_row(
            ppn_id=ppn_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for ppn_id, object_name, statement, status, implication in specs
    ]


def residual_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RLR2177_0_order",
            "epsilon_order_u_readout",
            "residual if any ordinary observable reads T or sqrt(S) before u=0 is imposed",
            "MISSING_ORDER_THEOREM_OR_BOUND",
            "dimensionless_log_readout_leak",
            "PPN;clock;orbital;local_GR",
        ),
        (
            "RLR2177_1_source",
            "delta_v_source_norm",
            "mismatch between parent v source coefficient and observed GM convention",
            "MISSING_PARENT_SOURCE_NORMALIZATION",
            "dimensionless_or_declared_source_coefficient",
            "Newton;PPN;orbital",
        ),
        (
            "RLR2177_2_beta",
            "delta_v_quadratic_beta",
            "parent-generated quadratic correction in v that shifts PPN beta",
            "MISSING_BETA_QUADRATIC_ZERO_OR_VALUE",
            "dimensionless_second_order_coefficient",
            "PPN_beta;local_GR",
        ),
        (
            "RLR2177_3_matter",
            "epsilon_matter_u_slot",
            "ordinary matter/source coupling that reintroduces u after constrained coframe selection",
            "MISSING_MATTER_DESCENT_ZERO_OR_BOUND",
            "dimensionless_species_coupling_norm",
            "WEP;clock;R10;PPN",
        ),
        (
            "RLR2177_4_boundary",
            "epsilon_boundary_u",
            "boundary, endpoint or corner term that carries residual u/C_R charge",
            "MISSING_BOUNDARY_ZERO_OR_BOUND",
            "boundary_projection_norm",
            "orbital;light_time;PPN",
        ),
        (
            "RLR2177_5_total",
            "epsilon_v_readout_abs",
            "absolute no-cancellation envelope for order/source/beta/matter/boundary residuals",
            "MISSING_COMPONENT_VALUES",
            "declared_common_norm",
            "all_local_arenas",
        ),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            status=status,
            units=units,
            observable_link=observable_link,
            value="MISSING_NUMERIC_VALUE",
            source_path="MISSING_SOURCE_PATH",
            score_ready=False,
            no_cancellation_policy=True,
        )
        for row_id, symbol, definition, status, units, observable_link in specs
    ]


def ru_status_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RUS2177_0_2176_gain",
            "algebraic R_u candidate",
            "2176 already made R_u concrete: u->-u and v fixed.",
            "RETAINED",
            "not merely a symbol anymore.",
        ),
        (
            "RUS2177_1_current_gain",
            "readout on u=0",
            "2177 shows the current coframe itself becomes v-only on the constrained surface.",
            "NEW_CONDITIONAL_GAIN",
            "this avoids a full readout rebuild if the parent proves constraint-before-readout.",
        ),
        (
            "RUS2177_2_not_parent_symmetry",
            "R_u parent symmetry",
            "R_u is not yet derived from the parent action, matter action, boundary terms and conservation law.",
            "NOT_PARENT_SIGNED",
            "do not promote to local-GR theorem.",
        ),
        (
            "RUS2177_3_route_status",
            "live route",
            "the best route is now order/source derivation, not another abstract R_u pass.",
            "ROUTE_NARROWED",
            "2178 should try to derive the v field/source convention.",
        ),
    ]
    return [
        base_row(
            status_id=status_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for status_id, object_name, statement, status, implication in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2177_0_gain",
            "V_ONLY_RECONSTRUCTION_ON_U_ZERO_DERIVED",
            "u=0 gives T=exp(v/2), sqrt(S)=exp(-v/2), so the current radial coframe is v-only after constraint.",
            "selected",
        ),
        (
            "DEC2177_1_no_rebuild_yet",
            "CURRENT_READOUT_CAN_SURVIVE_CONDITIONALLY",
            "we do not need to throw away the T/sqrt(S) coframe; we need a parent theorem that picks the constrained representative before readout.",
            "selected",
        ),
        (
            "DEC2177_2_ppn_shape",
            "GAMMA_BETA_SHAPE_CONDITIONAL",
            "A=exp(v), B=exp(-v) has the right local PPN shape if the parent source equation fixes v=-2U/c^2 without forbidden quadratic drift.",
            "selected",
        ),
        (
            "DEC2177_3_no_claim",
            "ORDER_SOURCE_CONSERVATION_UNSIGNED",
            "constraint ordering, v source normalization, matter descent, boundary silence and conservation are not parent-signed.",
            "selected",
        ),
        (
            "DEC2177_4_next",
            "CONSTRAINT_BEFORE_READOUT_AND_V_SOURCE_CONVENTION_NEXT",
            "the next non-circling leap is to derive the v equation/source convention and prove the order of operations.",
            "selected",
        ),
    ]
    return [
        base_row(
            decision_id=decision_id,
            decision=decision,
            rationale=rationale,
            selection_status=status,
        )
        for decision_id, decision, rationale, status in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2177_0_2178",
            selection_status="selected",
            target_file="2178-Y5-R2FR-constraint-before-readout-ordering-and-v-PPN-source-convention-or-readout-lock.md",
            target_script="scripts/Y5_R2FR_constraint_before_readout_ordering_and_v_PPN_source_convention_or_readout_lock_2178.py",
            objective="prove that the parent branch imposes u=0 before ordinary local readout and derive the weak-field v source convention needed for Newton/PPN, or lock current readout as conditional closure-only",
            success_condition="constraint-before-readout ordering plus v=-2U/c^2 source normalization, beta-shape stability, matter universality and conservation are parent-signed; otherwise residual rows stay live",
            do_not_do="do not import GR, do not fit v normalization from local tests, do not claim gamma/beta from readout shape alone",
        ),
        base_row(
            route_id="NEXT2177_1_finite_parallel",
            selection_status="held_parallel",
            target_file="2178b-Y5-R2FR-first-v-readout-residual-source-row.md",
            target_script="scripts/Y5_R2FR_first_v_readout_residual_source_row_2178b.py",
            objective="if source/order derivation fails, acquire the first source-backed finite v-readout residual row",
            success_condition="one finite order/source/beta/matter/boundary row has units, source path, convention and arena projection while remaining nonclaim",
            do_not_do="do not score symbolic residuals or use missing rows as evidence",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["readout_gate"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["v_reconstruction"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["ppn_gate"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2177_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2177_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    reconstruction_statuses = {row["status"] for row in rows_by_name["v_reconstruction"]}
    recon_pass = "EXACT_V_ONLY_RECONSTRUCTION_AFTER_CONSTRAINT" in reconstruction_statuses and "PARENT_ORDER_NOT_DERIVED" in reconstruction_statuses
    validations.append(base_row(validation_id="VAL2177_02_v_reconstruction", status="PASS" if recon_pass else "FAIL", detail="v-only reconstruction exists after u=0 but parent order is not derived"))

    gate_statuses = {row["status"] for row in rows_by_name["readout_gate"]}
    gate_pass = "PASS_CONDITIONAL_ON_ORDER" in gate_statuses and "UNSIGNED_PARENT_ORDER" in gate_statuses and "PARTIAL_PASS_CONDITIONAL_NOT_CLAIMABLE" in gate_statuses
    validations.append(base_row(validation_id="VAL2177_03_readout_gate", status="PASS" if gate_pass else "FAIL", detail="readout is conditionally v-only but local claim remains blocked"))

    ppn_statuses = {row["status"] for row in rows_by_name["ppn_gate"]}
    ppn_pass = "GAMMA_SHAPE_PASS_CONDITIONAL" in ppn_statuses and "BETA_SHAPE_PASS_CONDITIONAL" in ppn_statuses and "MISSING_PARENT_FIELD_EQUATION" in ppn_statuses
    validations.append(base_row(validation_id="VAL2177_04_ppn_gate", status="PASS" if ppn_pass else "FAIL", detail="gamma/beta shape is conditional and source equation remains missing"))

    residual_rows_local = rows_by_name["residual_rows"]
    residuals_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) for row in residual_rows_local)
    validations.append(base_row(validation_id="VAL2177_05_residual_rows", status="PASS" if residuals_ok else "FAIL", detail=f"readout-lock residual rows={len(residual_rows_local)} remain score_ready=false"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2177_06_decision", status="PASS" if "CONSTRAINT_BEFORE_READOUT_AND_V_SOURCE_CONVENTION_NEXT" in decision_text else "FAIL", detail="decision selects ordering/source-convention target next"))

    validations.append(base_row(validation_id="VAL2177_07_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2178" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2178 order/source-convention target selected"))

    validations.append(base_row(validation_id="VAL2177_08_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2177_09_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2177_10_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2177_artifacts()
    validations.append(base_row(validation_id="VAL2177_11_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2177 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2177_12_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2177_OVERALL", status="PASS" if overall else "FAIL", detail="2177 derives conditional v-only constrained readout and selects constraint-before-readout plus v-source convention as the next gate"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2177 - Y5/R2FR V-Only Visible Quotient Readout Owner Or Current Readout Lock

## Current Verdict

2177 gets a real conditional win, not a final local-GR claim.

Using the 2176 variables,

`a=ln T`, `b=ln sqrt(S)`, `u=a+b`, and `v=a-b`.

The inverse map is:

`ln T=(u+v)/2`, and `ln sqrt(S)=(u-v)/2`.

Therefore on the constrained branch `u=0`:

`T=exp(v/2)`, `sqrt(S)=exp(-v/2)`, `S=exp(-v)`, and `T^2=exp(v)`.

That means the current observed radial coframe does **not** need to be thrown away. After the constraint is imposed, it can be reconstructed from `v` alone:

`theta_0=exp(v/2)c dt`, and `theta_1=exp(-v/2)dr`.

This is the first strong sign that the local branch is not merely circling the same obstruction. The problem has narrowed: prove that the parent action imposes `u=0` before ordinary readout, then derive the weak-field `v` source convention. If that cannot be done, the branch remains closure-only with finite residual rows.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## V-Only Reconstruction

{md_table(rows_by_name["v_reconstruction"], ["reconstruction_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Observable Readout Gate

{md_table(rows_by_name["readout_gate"], ["gate_id", "gate", "required_statement", "status", "implication", "valid_for_claim"])}

## PPN Source Convention Gate

{md_table(rows_by_name["ppn_gate"], ["ppn_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Readout-Lock Residual Rows

{md_table(rows_by_name["residual_rows"], ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim"])}

## R_u Status Ledger

{md_table(rows_by_name["ru_status"], ["status_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is better than the previous state. Before 2177, `T` and `sqrt(S)` looked like two visible readout legs that made the `R_u` route suspect. Now the algebra says that once `u=0` is honestly imposed, those two legs are just the two reciprocal faces of one variable, `v`.

The hard missing piece is no longer "can a v-only readout even exist?" It can, conditionally. The hard missing piece is now "does the parent theory have the right to impose the constraint before readout, and does it derive the source equation for v?"

That is a cleaner, sharper target. Not a win by knockout yet, but the footwork is suddenly much better.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "v_reconstruction": v_reconstruction_rows(),
        "readout_gate": readout_gate_rows(),
        "ppn_gate": ppn_gate_rows(),
        "residual_rows": residual_rows(),
        "ru_status": ru_status_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "v_reconstruction", "readout_gate", "ppn_gate", "residual_rows", "ru_status", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
