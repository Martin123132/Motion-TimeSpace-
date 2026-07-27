from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2186"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2186_SOURCE_REGISTER.csv",
    "gauge_calculation": OUT / "P8_Y5_PARENT_QLOC_2186_2PN_READOUT_GAUGE_CALCULATION.csv",
    "descent_gate": OUT / "P8_Y5_PARENT_QLOC_2186_MTS_EH_DESCENT_GATE.csv",
    "readout_owner": OUT / "P8_Y5_PARENT_QLOC_2186_RADIAL_READOUT_OWNER_GATE.csv",
    "residual_rows": OUT / "P8_Y5_PARENT_QLOC_2186_RESIDUAL_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2186_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2186_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2186_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2186_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2186_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2186_MTS_EH_DESCENT_2PN_RESIDUAL_ROWS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2186_2PN_GAUGE_AUDIT_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MTS_EH_DESCENT_2PN_READOUT_GATE_2186_NONCLAIM.csv",
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


def formalization_has_2186_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2186-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2186*",
        "*P8_Y5_BRR545_2186*",
        "*Y5_R2FR_MTS_EH_fixed_point_descent_and_2PN_readout_residual_gate_2186*",
        "*JR2186*",
        "*MTS_EH_DESCENT_2PN_READOUT_GATE_2186*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2185_handoff",
            ROOT / "2185-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
            ["NEXT2185_0_2186", "MTS_EH_DESCENT_AND_2PN_READOUT_GATE_NEXT", "VAL2185_OVERALL"],
            "2185 selects MTS EH fixed-point descent and 2PN readout residual resolution as next gate.",
        ),
        (
            "2185_validation",
            OUT / "P8_Y5_BRR545_2185_VALIDATION.csv",
            ["VAL2185_OVERALL", "PASS"],
            "2185 validation passed before 2186 continues the chain.",
        ),
        (
            "2177_readout_shape",
            ROOT / "2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md",
            ["PPN2177_0_metric_shape", "A=exp(v), B=exp(-v)", "theta_1=exp(-v/2)dr"],
            "2177 supplies the reciprocal radial coframe/readout branch and its order guard.",
        ),
        (
            "2185_residuals",
            OUT / "P8_Y5_PARENT_QLOC_2185_RESIDUAL_ROWS.csv",
            ["CER2185_6_spatial_2PN", "sigma_spatial_2PN_recip_minus_iso", "1/2"],
            "2185 records the mixed isotropic/reciprocal 2PN warning.",
        ),
        (
            "local_gr_blocks",
            OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            ["A511_0_EH_core", "A511_5_boundary_reference", "A511_6_metric_readout"],
            "local-GR blocks define EH core, boundary reference, and readout/PiM double-zero requirements.",
        ),
        (
            "fixed_point_conditions",
            OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            ["FP511_1_double_zero_nonEH_coupling", "FP511_5_parent_PiM_lock", "FP511_8_local_cosmology_transition_control"],
            "fixed-point conditions define extra-sector double zero, PiM lock, and local/cosmology transition guard.",
        ),
        (
            "derived_chain",
            OUT / "P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv",
            ["DC511_2", "DC511_3", "DC511_5"],
            "derived chain records conditional EH metric equation, Hamiltonian charge, and readout steps.",
        ),
        (
            "hamiltonian_source",
            OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            ["HSM541_0_adopt_Hamiltonian_PiM", "HSM541_2_observed_worldtube_source", "HSM541_4_zero_extra_source_channels"],
            "Hamiltonian source contract carries PiM adoption, observed source worldtube, and extra-source silence debts.",
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


def gauge_calculation_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RGC2186_0_mixed_warning",
            "mixed isotropic/reciprocal comparison",
            "In isotropic radius x=GM/(c^2 r_iso), A_iso=((1-x/2)/(1+x/2))^2 and B_iso=(1+x/2)^4, while imposing B_recip=1/A_iso gives B_recip-B_iso=+1/2*x^2+O(x^3).",
            "MIXED_GAUGE_2PN_WARNING_REPRODUCED",
            "the 2185 warning is real as a same-coordinate isotropic comparison.",
        ),
        (
            "RGC2186_1_areal_map",
            "isotropic to areal radius map",
            "R=r_iso(1+x/2)^2, y=GM/(c^2 R)=x/(1+x/2)^2, so x=y+y^2+5*y^3/4+O(y^4).",
            "EXACT_RADIUS_MAP_SERIES",
            "the same Schwarzschild geometry uses different weak-field expansion variables in isotropic and areal gauges.",
        ),
        (
            "RGC2186_2_A_areal",
            "lapse in areal radius",
            "A_iso expressed in y is exactly A_areal=1-2y.",
            "AREAL_LAPSE_MATCH_EXACT",
            "the reciprocal branch belongs naturally to areal Schwarzschild gauge.",
        ),
        (
            "RGC2186_3_B_areal",
            "reciprocal spatial radial coefficient",
            "B_areal=(1-2y)^-1=1+2y+4y^2+8y^3+O(y^4), and transformed isotropic g_RR equals B_areal.",
            "AREAL_GAUGE_RESOLVES_2PN_SPATIAL_RESIDUAL",
            "the +1/2 isotropic residual vanishes after the proper radial gauge transformation.",
        ),
        (
            "RGC2186_4_kappa_gauge",
            "kappa_v is radial-gauge dependent",
            "In isotropic x, v=log(A_iso)=-2x+0*x^2+O(x^3), but in areal y, v=log(1-2y)=-2y-2y^2+O(y^3).",
            "KAPPA_V_GAUGE_DEPENDENT",
            "kappa_v=0 is the isotropic/PPN-gauge statement; reciprocal readout is the areal-gauge statement.",
        ),
        (
            "RGC2186_5_resolution",
            "2PN status",
            "The 2PN issue is demoted from physical failure to radial-gauge/readout-owner debt if MTS parent-owns the areal-isotropic map and the angular coframe.",
            "GAUGE_RESOLUTION_CONDITIONAL_NOT_PARENT_SIGNED",
            "without a parent radial gauge owner, keep finite readout residual rows.",
        ),
    ]
    return [
        base_row(
            calc_id=calc_id,
            calculation=calculation,
            equation=equation,
            status=status,
            implication=implication,
        )
        for calc_id, calculation, equation, status, implication in specs
    ]


def descent_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEG2186_0_EH_core",
            "EH core descent",
            "S_parent local compact branch must reduce to S_EH[e_obs,kappa_eff] plus locally silent sectors.",
            "CONDITIONAL_FROM_A511_0_NOT_CURRENTLY_SIGNED",
            "coefficient extraction remains GR import unless this is parent-derived.",
        ),
        (
            "DEG2186_1_kappa",
            "constant kappa/G",
            "d kappa_eff=0 on connected compact local domains from topological/superselection sector.",
            "CONDITIONAL_FROM_A511_1",
            "local G drift is not the active blocker if the kappa sector is adopted, but still needs parent signoff.",
        ),
        (
            "DEG2186_2_extra_double_zero",
            "extra-sector double zeros",
            "For each non-EH MTS coupling C_i, require C_i(Phi0)=0 and partial_A C_i(Phi0)=0 with positive source-free operator.",
            "REQUIRED_NOT_PROVED",
            "this is the main no-fifth-force/local-GR descent debt.",
        ),
        (
            "DEG2186_3_universal_coframe",
            "universal observed coframe",
            "All matter species, clocks, and orbital readout use the same g_obs/e_obs at leading local order.",
            "OPEN_SOURCE_FRAME_DEBT",
            "WEP/source-measure closure remains live.",
        ),
        (
            "DEG2186_4_PiM_lock",
            "Hamiltonian PiM lock",
            "Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0 at the fixed point.",
            "PIM_LOCK_OPEN",
            "mass projector calibration freedom remains live.",
        ),
        (
            "DEG2186_5_boundary",
            "boundary/reference zero",
            "GHY/reference/exact/topological boundary terms must produce no extra compact local mass flux.",
            "BOUNDARY_ZERO_OPEN",
            "source-measure equality can still shift by boundary bookkeeping.",
        ),
        (
            "DEG2186_6_readout",
            "metric/readout descent",
            "g_readout=g_obs+O((Phi-Phi0)^2), plus parent-owned radial gauge map chooses areal or isotropic coordinates before PPN scoring.",
            "READOUT_GAUGE_OWNER_OPEN",
            "1PN survives conditionally; full readout requires coordinate/gauge ownership.",
        ),
        (
            "DEG2186_7_verdict",
            "MTS EH descent status",
            "2186 resolves the 2PN warning as a gauge debt, but does not prove the MTS EH fixed-point descent.",
            "DESCENT_GATE_CURRENT_CLAIM_FAILS",
            "local-GR claim remains blocked; route is now sharper.",
        ),
    ]
    return [
        base_row(
            gate_id=gate_id,
            gate=gate,
            statement=statement,
            status=status,
            implication=implication,
        )
        for gate_id, gate, statement, status, implication in specs
    ]


def readout_owner_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ROG2186_0_radial_leg",
            "radial coframe leg",
            "2177 gives theta_1=exp(-v/2)dr after u=0, but it does not by itself identify dr as areal, isotropic, or another parent-owned radial coordinate.",
            "RADIAL_COORDINATE_OWNER_MISSING",
            "this is why the 2PN comparison can be mixed-gauge.",
        ),
        (
            "ROG2186_1_angular_leg",
            "angular coframe/area radius",
            "Areal Schwarzschild gauge requires angular area element R^2 dOmega^2 while reciprocal radial leg has B=(1-2GM/(c^2R))^-1.",
            "ANGULAR_COFAME_OWNER_MISSING",
            "MTS must state whether r is area radius or supply the isotropic-to-areal map.",
        ),
        (
            "ROG2186_2_PPN_gauge",
            "PPN isotropic gauge",
            "PPN beta/gamma are normally read in isotropic-like coordinates; kappa_v=0 belongs to that lapse gauge.",
            "PPN_GAUGE_CONTRACT_REQUIRED",
            "beta=1 cannot be inferred from an areal-coordinate x^2 coefficient without transforming gauge.",
        ),
        (
            "ROG2186_3_reciprocal_gauge",
            "reciprocal branch gauge",
            "B=exp(-v)=1/A is exact Schwarzschild radial gauge when r is areal and A=1-2GM/(c^2r).",
            "RECIPROCAL_BRANCH_AREAL_GAUGE_CONDITIONAL_PASS",
            "the reciprocal branch is not killed by the isotropic 2PN warning.",
        ),
        (
            "ROG2186_4_parent_choice",
            "parent readout choice",
            "The parent action/readout must choose either: areal reciprocal gauge plus PPN transform, or isotropic gauge with non-reciprocal spatial factor.",
            "READOUT_BRANCH_FORK_EXPLICIT",
            "choosing both in the same coordinate causes the +1/2 residual.",
        ),
    ]
    return [
        base_row(
            owner_id=owner_id,
            owner_gate=owner_gate,
            statement=statement,
            status=status,
            implication=implication,
        )
        for owner_id, owner_gate, statement, status, implication in specs
    ]


def residual_row_rows() -> list[dict[str, Any]]:
    rows = [
        ("RES2186_0_sigma_mixed", "sigma_spatial_2PN_mixed_isotropic", "same-coordinate residual B_recip(A_iso)-B_iso in isotropic radius", "1/2", "FINITE_MIXED_GAUGE_WARNING", "dimensionless_2PN_coefficient", "2PN;light_time;perihelion", str(DOC)),
        ("RES2186_1_sigma_areal", "sigma_spatial_2PN_areal_gauge", "residual after transforming isotropic Schwarzschild to areal radius", "0", "ZERO_IN_AREAL_GAUGE_CONDITIONAL", "dimensionless_2PN_coefficient", "2PN;local_GR", str(DOC)),
        ("RES2186_2_kappa_iso", "kappa_v_isotropic", "x^2 coefficient in v=log(A_iso) with x=GM/(c^2 r_iso)", "0", "ZERO_IN_ISOTROPIC_PPN_GAUGE_CONDITIONAL", "dimensionless", "PPN_beta", str(DOC)),
        ("RES2186_3_kappa_areal", "kappa_v_areal", "y^2 coefficient in v=log(1-2y) with y=GM/(c^2 R_areal)", "-2", "GAUGE_DEPENDENT_NOT_BETA_FAILURE", "dimensionless", "PPN_beta;coordinate_gauge", str(DOC)),
        ("RES2186_4_radius_owner", "epsilon_radial_gauge_owner", "failure to parent-own areal/isotropic radial coordinate and angular coframe", "MISSING_PARENT_RADIAL_GAUGE_MAP", "MISSING_RADIAL_GAUGE_OWNER", "dimensionless_or_declared", "2PN;PPN;local_GR", "MISSING_SOURCE_PATH"),
        ("RES2186_5_EH_descent", "epsilon_EH_fixed_point_descent", "failure to parent-derive EH fixed point and extra-sector double zeros", "MISSING_PARENT_DESCENT_PROOF", "MISSING_MTS_EH_DESCENT", "dimensionless_or_declared", "local_GR;WEP;PPN", "MISSING_SOURCE_PATH"),
        ("RES2186_6_PiM", "epsilon_PiM_lock", "failure of Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0", "MISSING_PARENT_PIM_LOCK", "MISSING_PIM_LOCK_PROOF", "dimensionless_or_GM_flux", "Newton;R10;R11;PPN", "MISSING_SOURCE_PATH"),
        ("RES2186_7_boundary", "epsilon_boundary_flux", "unresolved GHY/reference/exact/topological compact local boundary flux", "MISSING_BOUNDARY_ZERO_PROOF", "MISSING_BOUNDARY_ZERO", "dimensionless_or_GM_flux", "Newton;local_GR;R11", "MISSING_SOURCE_PATH"),
        ("RES2186_8_extra", "epsilon_extra_mass_charge", "non-EH MTS extra-sector mass charge at compact local fixed point", "MISSING_EXTRA_DOUBLE_ZERO_OR_BOUND", "MISSING_EXTRA_SECTOR_ZERO", "dimensionless_or_GM_flux", "WEP;PPN;local_GR", "MISSING_SOURCE_PATH"),
        ("RES2186_9_total", "Delta_local_GR_descent_abs", "absolute envelope of descent, PiM, boundary, extra-sector, and radial-gauge residuals", "MISSING_COMPONENT_INPUTS", "MISSING_COMPONENT_INPUTS", "dimensionless", "local_GR;PPN;Newton", "MISSING_SOURCE_PATH"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            value=value,
            status=status,
            units=units,
            observable_link=observable_link,
            source_path=source_path,
            score_ready=False,
        )
        for row_id, symbol, definition, value, status, units, observable_link, source_path in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2186_0_2PN_gauge", "2PN reciprocal/isotropic warning is gauge-resolved conditionally", "CONDITIONAL_PASS", "areal gauge map removes the +1/2 residual if parent-owned"),
        ("CG2186_1_radial_owner", "parent owns radial/areal/isotropic readout map", "BLOCKED_NONCLAIM", "2177 supplies radial coframe but not full radial/angular gauge ownership"),
        ("CG2186_2_EH_descent", "MTS parent derives EH fixed point and extra double zeros", "BLOCKED_NONCLAIM", "fixed-point descent remains not parent-signed"),
        ("CG2186_3_PiM_source", "PiM lock and same Hilbert/Hamiltonian source measure are proved", "BLOCKED_NONCLAIM", "Hamiltonian PiM adoption and source glue remain open"),
        ("CG2186_4_boundary", "compact boundary/reference flux is zero", "BLOCKED_NONCLAIM", "boundary flux remains open"),
        ("CG2186_5_local_GR", "full local-GR reduction can be claimed", "BLOCKED_NONCLAIM", "needs descent, PiM/source, boundary, and radial gauge ownership"),
        ("CG2186_6_guardrail", "no mixed-gauge or GR-import promotion", "PASS_GUARDRAIL", "2186 labels the win as conditional and keeps all claims false"),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2186_0_gain",
            "TWO_PN_WARNING_IS_GAUGE_CONDITIONAL",
            "The +1/2 isotropic residual is a mixed-gauge comparison; in areal Schwarzschild gauge reciprocal B=exp(-v) is exact.",
            "selected",
        ),
        (
            "DEC2186_1_caution",
            "RADIAL_READOUT_OWNER_NOW_CRITICAL",
            "MTS must parent-own whether r is areal, isotropic, or mapped before PPN scoring; otherwise the same branch can be misread.",
            "selected",
        ),
        (
            "DEC2186_2_limit",
            "MTS_EH_DESCENT_STILL_UNSIGNED",
            "The coefficient and 2PN gauge pieces look promising, but EH fixed-point descent/PiM/source/boundary clauses remain open.",
            "selected",
        ),
        (
            "DEC2186_3_next",
            "PARENT_RADIAL_GAUGE_AND_EH_DESCENT_SIGNATURE_NEXT",
            "Next target should construct the parent readout gauge map and tie it to EH descent/PiM/source signatures.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2186_0_2187",
            selection_status="selected",
            target_file="2187-Y5-R2FR-parent-owned-radial-gauge-map-and-EH-descent-signature.md",
            target_script="scripts/Y5_R2FR_parent_owned_radial_gauge_map_and_EH_descent_signature_2187.py",
            objective="derive or specify the parent-owned radial gauge/readout map linking reciprocal areal branch, isotropic PPN gauge, angular coframe, PiM lock, and EH fixed-point descent signatures",
            success_condition="parent action/readout owns r_areal or r_iso plus transform, angular area coframe, PiM(Phi0)=Pi_EH, same source measure, zero boundary flux, and extra-sector double zeros; otherwise residual rows remain nonclaim",
            do_not_do="do not mix isotropic lapse with reciprocal spatial readout in the same coordinate, do not claim local GR from gauge equivalence alone, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2186_1_empirical_parallel",
            selection_status="held_parallel",
            target_file="2187b-Y5-R2FR-radial-gauge-2PN-bound-acquisition.md",
            target_script="scripts/Y5_R2FR_radial_gauge_2PN_bound_acquisition_2187b.py",
            objective="if derivation stalls, acquire source-backed 2PN/readout/orbital bounds for any retained radial-gauge residual",
            success_condition="at least one 2PN/readout residual has source path, units, normalization, arena projection, and valid_for_claim=false",
            do_not_do="do not score placeholders or unsourced PPN bounds",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["residual_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["gauge_calculation"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["descent_gate"], BRANCH_COPIES["source_weight"]),
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
    validations.append(base_row(validation_id="VAL2186_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2186_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    gauge_statuses = {row["status"] for row in rows_by_name["gauge_calculation"]}
    gauge_pass = {"MIXED_GAUGE_2PN_WARNING_REPRODUCED", "AREAL_GAUGE_RESOLVES_2PN_SPATIAL_RESIDUAL", "KAPPA_V_GAUGE_DEPENDENT", "GAUGE_RESOLUTION_CONDITIONAL_NOT_PARENT_SIGNED"}.issubset(gauge_statuses)
    validations.append(base_row(validation_id="VAL2186_02_gauge_calculation", status="PASS" if gauge_pass else "FAIL", detail="2PN warning reproduced, areal gauge resolution and kappa gauge dependence recorded"))

    descent_statuses = {row["status"] for row in rows_by_name["descent_gate"]}
    descent_pass = {"REQUIRED_NOT_PROVED", "PIM_LOCK_OPEN", "DESCENT_GATE_CURRENT_CLAIM_FAILS"}.issubset(descent_statuses)
    validations.append(base_row(validation_id="VAL2186_03_descent_gate", status="PASS" if descent_pass else "FAIL", detail="MTS EH descent debts remain explicit and nonclaim"))

    owner_statuses = {row["status"] for row in rows_by_name["readout_owner"]}
    owner_pass = {"RADIAL_COORDINATE_OWNER_MISSING", "ANGULAR_COFAME_OWNER_MISSING", "RECIPROCAL_BRANCH_AREAL_GAUGE_CONDITIONAL_PASS"}.issubset(owner_statuses)
    validations.append(base_row(validation_id="VAL2186_04_readout_owner", status="PASS" if owner_pass else "FAIL", detail="radial/angular readout ownership gate written"))

    residuals = rows_by_name["residual_rows"]
    has_mixed = any(row.get("symbol") == "sigma_spatial_2PN_mixed_isotropic" and row.get("value") == "1/2" for row in residuals)
    has_areal = any(row.get("symbol") == "sigma_spatial_2PN_areal_gauge" and row.get("value") == "0" for row in residuals)
    has_missing = any(str(row.get("value", "")).startswith("MISSING_") or str(row.get("status", "")).startswith("MISSING_") for row in residuals)
    validations.append(base_row(validation_id="VAL2186_05_residual_rows", status="PASS" if has_mixed and has_areal and has_missing else "FAIL", detail=f"mixed warning, areal zero and missing descent rows represented; rows={len(residuals)}"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2186_06_claim_gate", status="PASS" if "CONDITIONAL_PASS" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses and "PASS_GUARDRAIL" in claim_statuses else "FAIL", detail="claim gate separates conditional gauge pass from blocked local-GR claim"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2186_07_decision", status="PASS" if "PARENT_RADIAL_GAUGE_AND_EH_DESCENT_SIGNATURE_NEXT" in decision_text else "FAIL", detail="decision selects parent radial gauge and EH descent signature next"))

    validations.append(base_row(validation_id="VAL2186_08_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2187" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2187 radial gauge/EH descent target selected"))

    validations.append(base_row(validation_id="VAL2186_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2186_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2186_11_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2186_artifacts()
    validations.append(base_row(validation_id="VAL2186_12_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2186 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2186_13_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2186_OVERALL", status="PASS" if overall else "FAIL", detail="2186 demotes 2PN warning to parent radial-gauge debt while keeping MTS EH descent/local-GR nonclaim"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2186 - Y5/R2FR MTS EH Fixed-Point Descent And 2PN Readout Residual Gate

## Current Verdict

2186 improves the situation again: the `+1/2*x^2` 2PN warning from 2185 is **not automatically a physical failure**.

It is a mixed-gauge warning.

In isotropic radius `x=GM/(c^2 r_iso)`:

`A_iso=((1-x/2)/(1+x/2))^2`,

`B_iso=(1+x/2)^4`,

and if we force the reciprocal branch in that same isotropic coordinate,

`B_recip=1/A_iso`,

then:

`B_recip-B_iso=+1/2*x^2+O(x^3)`.

But Schwarzschild's areal radius is

`R=r_iso(1+x/2)^2`,

with

`y=GM/(c^2 R)=x/(1+x/2)^2`.

In that areal gauge:

`A=1-2y`,

`B=(1-2y)^-1`,

and the transformed isotropic radial coefficient is exactly the same `B`. So the reciprocal branch `B=exp(-v)=1/A` is not killed; it is the natural Schwarzschild areal-gauge readout.

The catch is equally important:

`kappa_v=0` is the isotropic/PPN-gauge lapse statement, while in areal gauge

`v=log(1-2y)=-2y-2y^2+O(y^3)`.

So `kappa_v` is gauge/readout dependent unless the radial coordinate is parent-owned.

That means the next real blocker is not "2PN mismatch = death". It is:

**does MTS parent-own the radial/angle readout map and EH fixed-point descent?**

Current answer: not yet.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## 2PN Readout Gauge Calculation

{md_table(rows_by_name["gauge_calculation"], ["calc_id", "calculation", "equation", "status", "implication", "valid_for_claim"])}

## MTS EH Descent Gate

{md_table(rows_by_name["descent_gate"], ["gate_id", "gate", "statement", "status", "implication", "valid_for_claim"])}

## Radial Readout Owner Gate

{md_table(rows_by_name["readout_owner"], ["owner_id", "owner_gate", "statement", "status", "implication", "valid_for_claim"])}

## Residual Rows

{md_table(rows_by_name["residual_rows"], ["row_id", "symbol", "definition", "value", "status", "units", "observable_link", "source_path", "score_ready", "valid_for_claim"])}

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

This is a good result. The local branch is not dead at 2PN just because the isotropic comparison gave `+1/2`.

The sharper statement is:

`reciprocal v-readout + areal radius = Schwarzschild radial gauge`,

while

`kappa_v=0 + beta=1 = isotropic/PPN lapse gauge`.

Those are connected by a coordinate/readout map. MTS now needs to own that map instead of letting us switch gauges by hand.

So the project position is:

1. EH fixed point gives the right `K_v`, `C_v`, beta and gamma conditionally.
2. The 2PN reciprocal warning is gauge-resolvable conditionally.
3. Full local-GR still requires parent-owned EH descent, radial/angle readout ownership, PiM lock, source measure glue, and zero boundary flux.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "gauge_calculation": gauge_calculation_rows(),
        "descent_gate": descent_gate_rows(),
        "readout_owner": readout_owner_rows(),
        "residual_rows": residual_row_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in [
        "source_register",
        "gauge_calculation",
        "descent_gate",
        "readout_owner",
        "residual_rows",
        "claim_gate",
        "decision",
        "next_target",
    ]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
