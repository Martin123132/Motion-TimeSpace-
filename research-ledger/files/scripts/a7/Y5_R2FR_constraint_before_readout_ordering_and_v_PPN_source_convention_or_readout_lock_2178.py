from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2178"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2178-Y5-R2FR-constraint-before-readout-ordering-and-v-PPN-source-convention-or-readout-lock.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2178_SOURCE_REGISTER.csv",
    "order_contract": OUT / "P8_Y5_PARENT_QLOC_2178_CONSTRAINT_BEFORE_READOUT_ORDER_CONTRACT.csv",
    "v_source": OUT / "P8_Y5_PARENT_QLOC_2178_V_NEWTON_SOURCE_CONVENTION_DERIVATION.csv",
    "ppn_expansion": OUT / "P8_Y5_PARENT_QLOC_2178_V_PPN_EXPANSION_GATE.csv",
    "residual_rows": OUT / "P8_Y5_PARENT_QLOC_2178_V_SOURCE_ORDER_RESIDUAL_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2178_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2178_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2178_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2178_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2178_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2178_V_SOURCE_ORDER_RESIDUAL_ROWS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2178_CONSTRAINT_ORDER_CONTRACT_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "V_NEWTON_SOURCE_CONVENTION_2178_NONCLAIM.csv",
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


def formalization_has_2178_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2178-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2178*",
        "*P8_Y5_BRR545_2178*",
        "*Y5_R2FR_constraint_before_readout_ordering_and_v_PPN_source_convention_or_readout_lock_2178*",
        "*JR2178*",
        "*V_NEWTON_SOURCE_CONVENTION_2178*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2177_handoff",
            ROOT / "2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md",
            ["NEXT2177_0_2178", "CONSTRAINT_BEFORE_READOUT_AND_V_SOURCE_CONVENTION_NEXT"],
            "2177 selects constraint-before-readout plus v source convention as the next gate.",
        ),
        (
            "2177_validation",
            OUT / "P8_Y5_BRR545_2177_VALIDATION.csv",
            ["VAL2177_OVERALL", "PASS"],
            "2177 validation passed before 2178 continues the chain.",
        ),
        (
            "2174_second_class",
            ROOT / "2174-Y5-R2FR-Hcore-canonical-bracket-closure-or-auxiliary-route-demotion.md",
            ["CONTROLLED_SECOND_CLASS_PATTERN_FOUND", "u≈0 and p_u≈0"],
            "2174 supplies the conditional second-class u-sector elimination pattern.",
        ),
        (
            "2175_even_u",
            ROOT / "2175-Y5-R2FR-parent-even-u-sector-no-source-theorem-or-Iu-Ju-residuals.md",
            ["EXACT_EVEN_U_THEOREM_WRITTEN", "SOURCE_WEIGHT_SEAM_REMAINS_LIVE"],
            "2175 shows the I_u/J_u zero route is exact conditional but source seams remain live.",
        ),
        (
            "observer_contract",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["T^2 = 1 - 2U/c^2", "gamma - 1 = 0 after R_AB=0", "beta - 1 = 0"],
            "observer contract states the Newton, gamma and beta completion requirements.",
        ),
        (
            "hamiltonian_cell",
            ROOT / "09-hamiltonian-radial-cell-derivation.md",
            ["The Newtonian slow-particle limit fixes the clock/load side", "PPN gamma=1 and beta=1"],
            "09 records that Newton fixes the clock/load side first and PPN still needs beta.",
        ),
        (
            "motion_load_reduction",
            ROOT / "02-motion-load-local-GR-reduction.md",
            ["These are the correct weak-field lanes.", "derive or reject T^2 S = 1 from a parent principle"],
            "02 supplies the older weak-field target and parent-principle warning.",
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


def order_contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ORD2178_0_reduced_phase_space_rule",
            "Dirac/reduced readout ordering",
            "If u≈0 and p_u≈0 form a stable second-class pair and all ordinary observables descend to the reduced phase space, local readout is evaluated after imposing u=0.",
            "EXACT_CONDITIONAL_REDUCTION_RULE",
            "this is the formal ordering route that makes 2177 useful.",
        ),
        (
            "ORD2178_1_current_mechanism",
            "current auxiliary mechanism",
            "2174 gives a controlled second-class pattern only when A_u is admissible and I_u, J_u, matter, boundary and readout leaks vanish.",
            "CONDITIONAL_ONLY_FROM_2174",
            "the corpus has a mechanism shape but not a parent theorem.",
        ),
        (
            "ORD2178_2_even_source_support",
            "even/source-free u sector",
            "2175 proves I_u=J_u=0 only under parent-owned R_u/evenness/no-source-slot premises.",
            "CONDITIONAL_ONLY_FROM_2175",
            "the source seam is still the biggest danger.",
        ),
        (
            "ORD2178_3_v_readout_link",
            "v-only coframe after reduction",
            "2177 proves T=exp(v/2) and sqrt(S)=exp(-v/2) on u=0, so current readout can be reconstructed from v after reduction.",
            "EXACT_CONDITIONAL_LINK",
            "no readout rebuild is needed if ordering is parent-signed.",
        ),
        (
            "ORD2178_4_order_gap",
            "parent order status",
            "Current corpus does not yet prove stable reduced phase-space ordering for matter, clocks, photons, orbits, sources and boundary endpoints.",
            "UNSIGNED_PARENT_ORDER",
            "no local-GR or Newton claim is allowed from ordering alone.",
        ),
        (
            "ORD2178_5_failure_mode",
            "current readout lock",
            "If any ordinary observable reads off-shell T or sqrt(S) before u=0, the 2172/1878 coframe obstruction returns.",
            "READOUT_LOCK_RESIDUAL_REQUIRED_IF_ORDER_FAILS",
            "finite residual rows remain live.",
        ),
    ]
    return [
        base_row(
            order_id=order_id,
            gate=gate,
            statement=statement,
            status=status,
            implication=implication,
        )
        for order_id, gate, statement, status, implication in specs
    ]


def v_source_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "VS2178_0_constrained_readout",
            "metric/readout shape",
            "On u=0, A=T^2=exp(v) and B=S=exp(-v).",
            "EXACT_FROM_2177",
            "the local branch has one visible scalar readout variable.",
        ),
        (
            "VS2178_1_slow_particle",
            "Newtonian acceleration from readout",
            "For g_tt=-exp(v)c^2 at weak field and low speed, Phi_N=(c^2/2)v and a=-grad Phi_N=-(c^2/2)grad v.",
            "EXACT_WEAK_FIELD_READOUT",
            "Newton requires a parent source equation for v, not just reciprocal geometry.",
        ),
        (
            "VS2178_2_required_solution",
            "observed mass convention",
            "For a positive U=GM/r convention, Newton requires v=-2U/c^2+O(U^2/c^4), equivalently Phi_N=-U.",
            "REQUIRED_SOURCE_NORMALIZATION",
            "this fixes the sign and amplitude target.",
        ),
        (
            "VS2178_3_action_contract",
            "minimal weak-field v action",
            "If L_v=-(c^4/32piG)(grad v)^2 and L_matter=-rho c^2 v/2 at leading order, variation gives laplacian(v)=8piG rho/c^2.",
            "EXACT_CONDITIONAL_ACTION_DERIVATION",
            "this is the clean non-GR-import source-normalization contract to hunt for in the parent action.",
        ),
        (
            "VS2178_4_point_mass",
            "exterior solution",
            "laplacian(v)=8piG rho/c^2 gives v=-2GM/(c^2 r) outside a point source with v(infinity)=0.",
            "EXACT_CONDITIONAL_POINT_SOURCE",
            "the Newton amplitude follows if the action normalization is parent-derived.",
        ),
        (
            "VS2178_5_current_parent_status",
            "parent v action",
            "Current corpus has not parent-derived the coefficient c^4/32piG, the matter coupling -rho c^2 v/2, or the conservation identity for the same source.",
            "MISSING_PARENT_V_ACTION_NORMALIZATION",
            "2178 cannot claim Newton; it turns the missing piece into an exact coefficient target.",
        ),
    ]
    return [
        base_row(
            source_id=source_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for source_id, object_name, statement, status, implication in specs
    ]


def ppn_expansion_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PPN2178_0_parameterize_v",
            "weak-field v expansion",
            "Let x=U/c^2 and v=-2x+kappa_v x^2+O(x^3).",
            "EXACT_PARAMETERIZATION",
            "kappa_v captures the first nonlinear source/readout drift.",
        ),
        (
            "PPN2178_1_A_expansion",
            "time component",
            "A=exp(v)=1-2x+(2+kappa_v)x^2+O(x^3).",
            "EXACT_EXPANSION",
            "compare with A=1-2x+2 beta x^2+O(x^3).",
        ),
        (
            "PPN2178_2_beta_law",
            "PPN beta law",
            "beta=1+kappa_v/2 in the constrained v-readout branch.",
            "EXACT_BETA_DRIFT_LAW",
            "beta=1 requires kappa_v=0 or a compensating parent gauge theorem, not wishful thinking.",
        ),
        (
            "PPN2178_3_B_expansion",
            "radial component",
            "B=exp(-v)=1+2x+(2-kappa_v)x^2+O(x^3).",
            "EXACT_EXPANSION",
            "the first-order spatial coefficient gives gamma=1 once v source normalization is fixed.",
        ),
        (
            "PPN2178_4_gamma_law",
            "PPN gamma law",
            "gamma=1 at first order for any finite kappa_v if v=-2U/c^2+O(U^2/c^4).",
            "GAMMA_CONDITIONAL_PASS",
            "gamma is no longer the hardest gate; beta/source/conservation are.",
        ),
        (
            "PPN2178_5_beta_gate",
            "beta and nonlinear source gate",
            "kappa_v must be parent-derived as zero, gauge-removable, or finite-and-tested.",
            "MISSING_KAPPA_V_ZERO_THEOREM",
            "next target should hunt the parent v action normalization and nonlinear beta drift.",
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
        ("VRR2178_0_order", "epsilon_order_u_readout", "residual if readout happens before u=0 reduction", "MISSING_ORDER_THEOREM_OR_BOUND", "dimensionless_log_readout_leak", "clock;PPN;orbital;local_GR"),
        ("VRR2178_1_source_norm", "delta_v_source_norm", "relative mismatch in laplacian(v)=8piG rho/c^2 normalization", "MISSING_PARENT_SOURCE_NORMALIZATION_OR_VALUE", "dimensionless_relative_source_coefficient", "Newton;PPN;orbital"),
        ("VRR2178_2_kappa", "kappa_v", "quadratic weak-field drift in v=-2U/c^2+kappa_v U^2/c^4", "MISSING_KAPPA_V_ZERO_OR_VALUE", "dimensionless", "PPN_beta;local_GR"),
        ("VRR2178_3_matter", "epsilon_v_matter_nonuniversal", "species/source mismatch in the v matter coupling", "MISSING_MATTER_UNIVERSALITY_ZERO_OR_BOUND", "dimensionless_species_norm", "WEP;clock;R10;PPN"),
        ("VRR2178_4_boundary", "epsilon_v_boundary_endpoint", "boundary or endpoint re-entry after v reduction", "MISSING_BOUNDARY_ENDPOINT_ZERO_OR_BOUND", "boundary_projection_norm", "orbital;light_time;PPN"),
        ("VRR2178_5_conservation", "epsilon_v_conservation", "Bianchi-like source conservation failure in the v equation", "MISSING_CONSERVATION_IDENTITY_OR_BOUND", "dimensionless_divergence_norm", "local_GR;PPN;cosmology"),
        ("VRR2178_6_total", "epsilon_v_source_order_abs", "absolute no-cancellation envelope for order/source/kappa/matter/boundary/conservation residuals", "MISSING_COMPONENT_VALUES", "declared_common_norm", "all_local_arenas"),
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


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2178_0_order", "constraint-before-readout is parent-signed", "UNSIGNED", "no claim until reduced phase-space ordering covers ordinary observables"),
        ("CG2178_1_source", "v source normalization derives laplacian(v)=8piG rho/c^2", "UNSIGNED", "no Newton claim until field coefficient and matter coupling are parent-derived"),
        ("CG2178_2_gamma", "gamma=1 shape after source normalization", "CONDITIONAL_PASS", "useful but not independently sufficient"),
        ("CG2178_3_beta", "beta=1 through kappa_v=0 or parent gauge theorem", "UNSIGNED", "beta remains a hard gate"),
        ("CG2178_4_matter", "same v couples to all ordinary matter/readout sectors", "UNSIGNED", "WEP and clock gates remain blocked"),
        ("CG2178_5_conservation", "Bianchi-like source conservation identity", "UNSIGNED", "field theory status remains incomplete"),
        ("CG2178_6_verdict", "Newton/local-GR claim", "BLOCKED_NONCLAIM", "2178 supplies exact conditional laws, not a claim"),
    ]
    return [
        base_row(
            gate_id=gate_id,
            gate=gate,
            status=status,
            implication=implication,
        )
        for gate_id, gate, status, implication in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2178_0_gain_order",
            "ORDERING_THEOREM_CONTRACT_EXACT",
            "If the u,p_u constraints are parent-stable and observables descend to the reduced phase space, readout-after-u=0 is mathematically legitimate.",
            "selected",
        ),
        (
            "DEC2178_1_gain_source",
            "V_NEWTON_SOURCE_CONVENTION_CONTRACT_DERIVED",
            "A non-GR-import weak-field action with -(c^4/32piG)(grad v)^2 and -rho c^2 v/2 gives laplacian(v)=8piG rho/c^2 and v=-2GM/(c^2r).",
            "selected",
        ),
        (
            "DEC2178_2_gain_ppn",
            "BETA_DRIFT_LAW_DERIVED",
            "With v=-2U/c^2+kappa_v U^2/c^4, the constrained branch gives beta=1+kappa_v/2 while gamma=1 at first order.",
            "selected",
        ),
        (
            "DEC2178_3_no_claim",
            "PARENT_V_ACTION_AND_KAPPA_ZERO_UNSIGNED",
            "The parent source coefficient, matter universality, conservation identity and kappa_v=0 theorem are missing.",
            "selected",
        ),
        (
            "DEC2178_4_next",
            "PARENT_V_ACTION_NORMALIZATION_AND_BETA_ZERO_NEXT",
            "The next leap is to derive the v kinetic/source action and nonlinear beta zero, not to rerun the same readout gate.",
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
            route_id="NEXT2178_0_2179",
            selection_status="selected",
            target_file="2179-Y5-R2FR-parent-v-field-action-normalization-and-beta-quadratic-zero-or-finite-row.md",
            target_script="scripts/Y5_R2FR_parent_v_field_action_normalization_and_beta_quadratic_zero_or_finite_row_2179.py",
            objective="derive the parent weak-field v action normalization, matter source coupling and nonlinear kappa_v=0 beta condition, or demote them to finite residual rows",
            success_condition="parent action yields L_v coefficient c^4/32piG, matter coupling -rho c^2 v/2, conservation identity and kappa_v=0 or sourced finite kappa_v row",
            do_not_do="do not import Einstein equations, do not fit G or beta from tests, do not claim local GR from gamma shape alone",
        ),
        base_row(
            route_id="NEXT2178_1_finite_parallel",
            selection_status="held_parallel",
            target_file="2179b-Y5-R2FR-first-v-source-beta-finite-row-acquisition.md",
            target_script="scripts/Y5_R2FR_first_v_source_beta_finite_row_acquisition_2179b.py",
            objective="if derivation fails, acquire one finite source-backed delta_v_source_norm or kappa_v row with units and arena projection",
            success_condition="one finite row has source path, units, convention, projection and remains nonclaim",
            do_not_do="do not score placeholder residual rows",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["residual_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["order_contract"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["v_source"], BRANCH_COPIES["source_weight"]),
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
    validations.append(base_row(validation_id="VAL2178_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2178_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    order_statuses = {row["status"] for row in rows_by_name["order_contract"]}
    order_pass = "EXACT_CONDITIONAL_REDUCTION_RULE" in order_statuses and "UNSIGNED_PARENT_ORDER" in order_statuses
    validations.append(base_row(validation_id="VAL2178_02_order_contract", status="PASS" if order_pass else "FAIL", detail="constraint-before-readout rule is exact conditional but parent order remains unsigned"))

    source_statuses = {row["status"] for row in rows_by_name["v_source"]}
    source_pass = "EXACT_CONDITIONAL_ACTION_DERIVATION" in source_statuses and "MISSING_PARENT_V_ACTION_NORMALIZATION" in source_statuses
    validations.append(base_row(validation_id="VAL2178_03_v_source_derivation", status="PASS" if source_pass else "FAIL", detail="v Newton source convention derived as a parent-action coefficient contract"))

    ppn_statuses = {row["status"] for row in rows_by_name["ppn_expansion"]}
    ppn_pass = "EXACT_BETA_DRIFT_LAW" in ppn_statuses and "MISSING_KAPPA_V_ZERO_THEOREM" in ppn_statuses and "GAMMA_CONDITIONAL_PASS" in ppn_statuses
    validations.append(base_row(validation_id="VAL2178_04_ppn_expansion", status="PASS" if ppn_pass else "FAIL", detail="beta drift law beta=1+kappa_v/2 derived; gamma is conditional"))

    residual_rows_local = rows_by_name["residual_rows"]
    residuals_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) for row in residual_rows_local)
    validations.append(base_row(validation_id="VAL2178_05_residual_rows", status="PASS" if residuals_ok else "FAIL", detail=f"v source/order residual rows={len(residual_rows_local)} remain score_ready=false"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2178_06_claim_gate", status="PASS" if "BLOCKED_NONCLAIM" in claim_statuses and "CONDITIONAL_PASS" in claim_statuses else "FAIL", detail="local claim remains blocked despite conditional gamma/source gains"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2178_07_decision", status="PASS" if "PARENT_V_ACTION_NORMALIZATION_AND_BETA_ZERO_NEXT" in decision_text else "FAIL", detail="decision selects parent v-action and beta-zero target next"))

    validations.append(base_row(validation_id="VAL2178_08_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2179" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2179 parent v-action normalization target selected"))

    validations.append(base_row(validation_id="VAL2178_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2178_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2178_11_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2178_artifacts()
    validations.append(base_row(validation_id="VAL2178_12_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2178 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2178_13_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2178_OVERALL", status="PASS" if overall else "FAIL", detail="2178 derives the v Newton source convention contract and beta drift law while keeping local-GR claim blocked"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2178 - Y5/R2FR Constraint-Before-Readout Ordering And V PPN Source Convention Or Readout Lock

## Current Verdict

2178 makes a real forward cut: it derives the **exact source-normalization contract** that the parent theory must satisfy for the `v` branch to become Newton/PPN rather than a pretty readout shape.

After 2177, the constrained readout is:

`A=T^2=exp(v)`, `B=S=exp(-v)`.

The weak slow-particle readout gives:

`Phi_N=(c^2/2)v`, so `a=-(c^2/2) grad(v)`.

Therefore, with positive `U=GM/r`, Newton requires:

`v=-2U/c^2+O(U^2/c^4)`.

The clean non-GR-import parent-action contract is:

`L_v=-(c^4/32piG)(grad v)^2`, and `L_matter=-rho c^2 v/2`.

Varying that weak-field action gives:

`laplacian(v)=8piG rho/c^2`,

so a point source gives `v=-2GM/(c^2 r)` with `v(infinity)=0`.

That is a sharp target, not a claim. The corpus still has to derive those coefficients from the parent action and prove the same source obeys conservation and matter universality.

The PPN sting in the tail is also now exact. If:

`v=-2x+kappa_v x^2+O(x^3)`, with `x=U/c^2`,

then:

`beta=1+kappa_v/2`.

So gamma is the easier part now; beta lives or dies on whether `kappa_v=0` is derived, gauge-owned, or finite-and-tested.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Constraint-Before-Readout Order Contract

{md_table(rows_by_name["order_contract"], ["order_id", "gate", "statement", "status", "implication", "valid_for_claim"])}

## V Newton Source Convention Derivation

{md_table(rows_by_name["v_source"], ["source_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## V PPN Expansion Gate

{md_table(rows_by_name["ppn_expansion"], ["ppn_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## V Source/Order Residual Rows

{md_table(rows_by_name["residual_rows"], ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim"])}

## Claim Gate

{md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is a good kind of narrowing. We are not asking the theory to magically "be GR". We now have a concrete parent-action target:

1. reduce first, so `u=0` is imposed before ordinary readout;
2. produce the weak-field `v` kinetic coefficient `c^4/32piG`;
3. produce the universal matter coupling `-rho c^2 v/2`;
4. prove the nonlinear beta drift coefficient `kappa_v` is zero, gauge, or finite.

That is the leap-forward route. If it works, the local branch starts looking serious. If it fails, the failure is crisp: `delta_v_source_norm` and `kappa_v` become finite residuals that have to face PPN/Newton tests.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "order_contract": order_contract_rows(),
        "v_source": v_source_rows(),
        "ppn_expansion": ppn_expansion_rows(),
        "residual_rows": residual_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "order_contract", "v_source", "ppn_expansion", "residual_rows", "claim_gate", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
