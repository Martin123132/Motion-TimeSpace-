from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2187"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2187-Y5-R2FR-parent-owned-radial-gauge-map-and-EH-descent-signature.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2187_SOURCE_REGISTER.csv",
    "gauge_contract": OUT / "P8_Y5_PARENT_QLOC_2187_PARENT_RADIAL_GAUGE_CONTRACT.csv",
    "branch_rules": OUT / "P8_Y5_PARENT_QLOC_2187_AREAL_ISOTROPIC_BRANCH_RULES.csv",
    "descent_signature": OUT / "P8_Y5_PARENT_QLOC_2187_EH_DESCENT_SIGNATURE_MATRIX.csv",
    "residual_rows": OUT / "P8_Y5_PARENT_QLOC_2187_RESIDUAL_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2187_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2187_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2187_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2187_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2187_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2187_RADIAL_GAUGE_EH_DESCENT_RESIDUAL_ROWS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2187_RADIAL_GAUGE_CONTRACT_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_RADIAL_GAUGE_EH_DESCENT_2187_NONCLAIM.csv",
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


def formalization_has_2187_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2187-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2187*",
        "*P8_Y5_BRR545_2187*",
        "*Y5_R2FR_parent_owned_radial_gauge_map_and_EH_descent_signature_2187*",
        "*JR2187*",
        "*PARENT_RADIAL_GAUGE_EH_DESCENT_2187*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2186_handoff",
            ROOT / "2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md",
            ["NEXT2186_0_2187", "PARENT_RADIAL_GAUGE_AND_EH_DESCENT_SIGNATURE_NEXT", "VAL2186_OVERALL"],
            "2186 selects parent-owned radial gauge map and EH descent signatures as the next gate.",
        ),
        (
            "2186_validation",
            OUT / "P8_Y5_BRR545_2186_VALIDATION.csv",
            ["VAL2186_OVERALL", "PASS"],
            "2186 validation passed before 2187 continues the chain.",
        ),
        (
            "2186_gauge_calc",
            OUT / "P8_Y5_PARENT_QLOC_2186_2PN_READOUT_GAUGE_CALCULATION.csv",
            ["MIXED_GAUGE_2PN_WARNING_REPRODUCED", "AREAL_GAUGE_RESOLVES_2PN_SPATIAL_RESIDUAL", "KAPPA_V_GAUGE_DEPENDENT"],
            "2186 provides the gauge calculation this checkpoint turns into a parent-owned readout contract.",
        ),
        (
            "2186_readout_owner",
            OUT / "P8_Y5_PARENT_QLOC_2186_RADIAL_READOUT_OWNER_GATE.csv",
            ["RADIAL_COORDINATE_OWNER_MISSING", "ANGULAR_COFAME_OWNER_MISSING", "RECIPROCAL_BRANCH_AREAL_GAUGE_CONDITIONAL_PASS"],
            "2186 records that radial and angular coframe ownership are the live readout debts.",
        ),
        (
            "2177_v_readout",
            ROOT / "2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md",
            ["theta_1=exp(-v/2)dr", "A=exp(v), B=exp(-v)", "MISSING_COMMON_V_SOURCE_MAP"],
            "2177 supplies the v-only reciprocal coframe after u=0 and its source/readout caveats.",
        ),
        (
            "descent_gate",
            OUT / "P8_Y5_PARENT_QLOC_2186_MTS_EH_DESCENT_GATE.csv",
            ["REQUIRED_NOT_PROVED", "PIM_LOCK_OPEN", "READOUT_GAUGE_OWNER_OPEN"],
            "2186 records descent, PiM, and readout-gauge debts.",
        ),
        (
            "local_gr_blocks",
            OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            ["A511_0_EH_core", "A511_5_boundary_reference", "A511_6_metric_readout"],
            "local-GR blocks identify EH core, boundary reference, and readout/PiM double-zero structure.",
        ),
        (
            "fixed_point_conditions",
            OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            ["FP511_1_double_zero_nonEH_coupling", "FP511_5_parent_PiM_lock", "FP511_8_local_cosmology_transition_control"],
            "fixed-point conditions define the remaining local descent and transition-control requirements.",
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


def gauge_contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RGC2187_0_parent_object",
            "radial coordinate is an observable functional",
            "The parent readout must define either R_areal := sqrt(Area(S^2)/(4*pi)) from the angular coframe, or r_iso by conformal-flat spatial PPN gauge.",
            "PARENT_GAUGE_OBJECT_DEFINED_AS_CONTRACT",
            "radial gauge is no longer allowed to float silently between calculations.",
        ),
        (
            "RGC2187_1_areal_branch",
            "areal reciprocal branch",
            "If R=R_areal, the local EH fixed-point line element may use A=exp(v)=1-2GM/(c^2 R), B=exp(-v)=A^-1, and angular area R^2 dOmega^2.",
            "AREAL_RECIPROCAL_BRANCH_ALLOWED_CONDITIONAL",
            "the reciprocal branch is legitimate in Schwarzschild/areal gauge.",
        ),
        (
            "RGC2187_2_isotropic_branch",
            "isotropic PPN branch",
            "If r=r_iso, then A=A_iso and spatial factor B_iso=(1+x/2)^4; PPN beta/gamma are scored in this gauge.",
            "ISOTROPIC_PPN_BRANCH_ALLOWED_CONDITIONAL",
            "kappa_v=0 and beta=1 belong to the isotropic lapse expansion.",
        ),
        (
            "RGC2187_3_transform",
            "required transform",
            "The parent map must carry R=r_iso(1+x/2)^2 and y=x/(1+x/2)^2 between branches before comparing 2PN coefficients.",
            "AREAL_ISOTROPIC_TRANSFORM_REQUIRED",
            "mixing A_iso with B=1/A_iso in the same coordinate is forbidden.",
        ),
        (
            "RGC2187_4_angular_coframe",
            "angular coframe owner",
            "Areal gauge requires the angular area coframe theta_angular=R dOmega; isotropic gauge requires a conformal spatial factor for both radial and angular legs.",
            "ANGULAR_COFAME_REQUIRED",
            "radial leg alone is insufficient for full local-GR/PPN scoring.",
        ),
        (
            "RGC2187_5_order",
            "constraint before gauge readout",
            "The u=0/v-only reduction must be imposed before the radial gauge functional is scored against clocks, rods, light, orbit endpoints, and source mass.",
            "CONSTRAINT_BEFORE_READOUT_RETAINED",
            "this keeps the 2177 readout-order guard active.",
        ),
        (
            "RGC2187_6_current_status",
            "current parent ownership status",
            "This is a parent-readout contract, not a proof that MTS already supplies the angular/radial gauge functional.",
            "RADIAL_GAUGE_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "local-GR claim remains blocked until the contract is derived from the parent action/readout.",
        ),
    ]
    return [
        base_row(contract_id=contract_id, contract=contract, statement=statement, status=status, implication=implication)
        for contract_id, contract, statement, status, implication in specs
    ]


def branch_rule_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "BR2187_0_no_mixing",
            "no mixed-gauge scoring",
            "Do not use isotropic lapse A_iso and reciprocal spatial factor B=1/A_iso in the same coordinate for 2PN scoring.",
            "FORBIDDEN_MIXED_GAUGE",
            "this is exactly the source of the +1/2 warning.",
        ),
        (
            "BR2187_1_areal_scoring",
            "areal internal branch",
            "Areal reciprocal branch may be used for internal Schwarzschild/EH descent checks, with R fixed by sphere area and B=A^-1.",
            "CONDITIONAL_PASS_IF_AREAL_OWNER",
            "valid only if the angular area coframe is parent-owned.",
        ),
        (
            "BR2187_2_ppn_scoring",
            "PPN scoring branch",
            "For PPN beta/gamma reporting, transform to isotropic/PPN gauge and use A_iso plus conformal spatial factor B_iso.",
            "PPN_GAUGE_REQUIRED_FOR_BETA_GAMMA",
            "beta=1 comes from isotropic lapse, not areal kappa_v.",
        ),
        (
            "BR2187_3_kappa_label",
            "kappa_v label discipline",
            "kappa_v must carry a gauge label: kappa_v_isotropic=0, kappa_v_areal=-2 for Schwarzschild expansions.",
            "GAUGE_LABEL_REQUIRED",
            "unlabelled kappa_v claims are not admissible beyond leading order.",
        ),
        (
            "BR2187_4_residual_rule",
            "residual activation",
            "If no parent radial/angle owner is supplied, activate epsilon_radial_gauge_owner and retain the 2PN residual row as nonclaim.",
            "RESIDUAL_ROW_IF_OWNER_MISSING",
            "conditional gauge resolution cannot be treated as local-GR evidence without ownership.",
        ),
    ]
    return [
        base_row(rule_id=rule_id, rule=rule, statement=statement, status=status, implication=implication)
        for rule_id, rule, statement, status, implication in specs
    ]


def descent_signature_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "EDS2187_0_EH_core",
            "EH operator core",
            "S_parent local compact branch contains S_EH[e_obs,kappa_eff] with locally constant kappa_eff.",
            "CONDITIONAL_SOURCE_EXISTS_NOT_FULLY_SIGNED",
            "required for coefficient inheritance rather than GR import.",
        ),
        (
            "EDS2187_1_extra_double_zero",
            "extra-sector double zero",
            "For all local non-EH couplings C_i: C_i(Phi0)=0 and partial_A C_i(Phi0)=0 with positive source-free operator.",
            "REQUIRED_NOT_PROVED",
            "main fifth-force/PPN/source-normalization descent debt.",
        ),
        (
            "EDS2187_2_universal_matter",
            "universal observed coframe",
            "All matter species couple to g_obs/e_obs at leading local order and define the same Hilbert source current.",
            "OPEN_SOURCE_FRAME_DEBT",
            "WEP/source measure still needs proof.",
        ),
        (
            "EDS2187_3_PiM_lock",
            "PiM Hamiltonian lock",
            "Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0.",
            "PIM_LOCK_OPEN",
            "mass projector calibration remains a live residual.",
        ),
        (
            "EDS2187_4_boundary_zero",
            "boundary/reference zero",
            "GHY/reference/exact/topological boundary terms carry no extra compact local mass flux.",
            "BOUNDARY_ZERO_OPEN",
            "source-measure equality can still shift by boundary bookkeeping.",
        ),
        (
            "EDS2187_5_readout_gauge",
            "radial/angle readout owner",
            "Parent readout chooses areal reciprocal branch plus PPN transform or isotropic PPN branch plus non-reciprocal spatial factor.",
            "READOUT_GAUGE_CONTRACT_WRITTEN_NOT_DERIVED",
            "2187 closes the contract shape, not the parent derivation.",
        ),
        (
            "EDS2187_6_transition",
            "local/cosmology transition control",
            "Same action must suppress MTS extra sectors in compact local systems while allowing cosmological/galaxy behaviour through a derived activation scale.",
            "TRANSITION_CONTROL_OPEN",
            "avoid hand switching between GR local branch and MTS large-scale branch.",
        ),
        (
            "EDS2187_7_verdict",
            "descent signature status",
            "The typed EH descent signature matrix is now explicit, but only the gauge contract is sharpened; extra/PiM/boundary/source signatures remain unsigned.",
            "SIGNATURE_MATRIX_WRITTEN_CURRENT_CLAIM_FAILS",
            "next work should attack extra double zeros and PiM lock.",
        ),
    ]
    return [
        base_row(signature_id=signature_id, signature=signature, statement=statement, status=status, implication=implication)
        for signature_id, signature, statement, status, implication in specs
    ]


def residual_row_rows() -> list[dict[str, Any]]:
    rows = [
        ("RGR2187_0_radial_owner", "epsilon_radial_gauge_owner", "parent ownership failure for areal/isotropic radial coordinate and transform", "MISSING_PARENT_RADIAL_GAUGE_OWNER", "MISSING_RADIAL_GAUGE_OWNER", "dimensionless_or_declared", "2PN;PPN;local_GR", "MISSING_SOURCE_PATH"),
        ("RGR2187_1_angular_owner", "epsilon_angular_coframe_owner", "parent ownership failure for angular area coframe or conformal isotropic spatial factor", "MISSING_PARENT_ANGULAR_COFAME_OWNER", "MISSING_ANGULAR_COFAME_OWNER", "dimensionless_or_declared", "2PN;light_time;orbital", "MISSING_SOURCE_PATH"),
        ("RGR2187_2_mixed", "sigma_spatial_2PN_mixed_forbidden", "residual if isotropic lapse and reciprocal spatial factor are scored in same coordinate", "1/2", "FORBIDDEN_MIXED_GAUGE_RESIDUAL", "dimensionless_2PN_coefficient", "2PN;PPN", str(DOC)),
        ("RGR2187_3_areal", "sigma_spatial_2PN_areal_owned", "spatial residual in parent-owned areal reciprocal gauge", "0", "ZERO_IF_AREAL_GAUGE_PARENT_OWNED", "dimensionless_2PN_coefficient", "2PN;local_GR", str(DOC)),
        ("RGR2187_4_kappa_iso", "kappa_v_isotropic", "PPN-gauge lapse quadratic coefficient", "0", "ZERO_IN_ISOTROPIC_PPN_GAUGE_CONDITIONAL", "dimensionless", "PPN_beta", str(DOC)),
        ("RGR2187_5_kappa_areal", "kappa_v_areal", "areal-gauge lapse quadratic coefficient", "-2", "GAUGE_LABEL_REQUIRED_NOT_BETA_FAILURE", "dimensionless", "coordinate_gauge", str(DOC)),
        ("RGR2187_6_descent", "epsilon_EH_descent_signature", "failure to parent-sign EH core plus extra-sector double zeros", "MISSING_PARENT_DESCENT_SIGNATURE", "MISSING_EH_DESCENT_SIGNATURE", "dimensionless_or_declared", "local_GR;WEP;PPN", "MISSING_SOURCE_PATH"),
        ("RGR2187_7_PiM", "epsilon_PiM_lock", "failure to prove Pi_M(Phi0)=Pi_EH and derivative silence", "MISSING_PARENT_PIM_LOCK", "MISSING_PIM_LOCK_PROOF", "dimensionless_or_GM_flux", "Newton;R10;R11;PPN", "MISSING_SOURCE_PATH"),
        ("RGR2187_8_boundary", "epsilon_boundary_reference_zero", "failure to prove zero compact boundary/reference mass flux", "MISSING_BOUNDARY_ZERO_PROOF", "MISSING_BOUNDARY_ZERO", "dimensionless_or_GM_flux", "Newton;local_GR", "MISSING_SOURCE_PATH"),
        ("RGR2187_9_total", "Delta_local_GR_readout_descent_abs", "absolute envelope of radial, angular, descent, PiM and boundary residuals", "MISSING_COMPONENT_INPUTS", "MISSING_COMPONENT_INPUTS", "dimensionless", "local_GR;PPN;Newton", "MISSING_SOURCE_PATH"),
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
        ("CG2187_0_contract", "parent radial gauge contract shape is written", "PASS_GUARDRAIL", "areal/isotropic branches and transform are explicit"),
        ("CG2187_1_mixed_gauge", "mixed isotropic/reciprocal 2PN scoring is forbidden", "PASS_GUARDRAIL", "the +1/2 row is now a guardrail residual, not a physical claim"),
        ("CG2187_2_radial_owner", "parent owns radial/angle gauge map", "BLOCKED_NONCLAIM", "contract written but not derived from parent action/readout"),
        ("CG2187_3_EH_descent", "EH descent signatures are parent-signed", "BLOCKED_NONCLAIM", "extra double-zero, PiM, source and boundary signatures remain open"),
        ("CG2187_4_local_GR", "full local-GR reduction can be claimed", "BLOCKED_NONCLAIM", "requires gauge owner plus EH descent signatures"),
        ("CG2187_5_GitHub", "public/github update is triggered", "BLOCKED_NONCLAIM", "private work only; no GitHub action"),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2187_0_gain",
            "RADIAL_GAUGE_CONTRACT_WRITTEN",
            "Areal reciprocal and isotropic PPN branches are now separated with a required transform and gauge labels.",
            "selected",
        ),
        (
            "DEC2187_1_gain_guard",
            "MIXED_GAUGE_SCORING_FORBIDDEN",
            "The previous +1/2 2PN warning becomes a guardrail against using two gauges at once.",
            "selected",
        ),
        (
            "DEC2187_2_limit",
            "PARENT_OWNERSHIP_AND_EH_DESCENT_STILL_UNSIGNED",
            "Radial/angle map, extra double zeros, PiM lock, universal source and boundary zero are not parent-signed.",
            "selected",
        ),
        (
            "DEC2187_3_next",
            "EXTRA_DOUBLE_ZERO_AND_PIM_LOCK_SIGNATURE_NEXT",
            "The next best route is to attack the two hardest remaining descent signatures: extra-sector double zeros and Hamiltonian PiM lock.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2187_0_2188",
            selection_status="selected",
            target_file="2188-Y5-R2FR-extra-sector-double-zero-and-PiM-lock-signature-or-residual-fill.md",
            target_script="scripts/Y5_R2FR_extra_sector_double_zero_and_PiM_lock_signature_or_residual_fill_2188.py",
            objective="derive or audit the extra-sector double-zero conditions and Hamiltonian PiM lock needed for MTS to own the EH fixed-point local branch",
            success_condition="for each local extra coupling C_i, C_i(Phi0)=0 and partial_A C_i(Phi0)=0 or a finite residual exists; Pi_M(Phi0)=Pi_EH and derivative silence are parent-signed or residualized",
            do_not_do="do not claim local GR from radial gauge contract alone, do not absorb PiM residual into G, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2187_1_empirical_parallel",
            selection_status="held_parallel",
            target_file="2188b-Y5-R2FR-readout-gauge-2PN-bound-source-acquisition.md",
            target_script="scripts/Y5_R2FR_readout_gauge_2PN_bound_source_acquisition_2188b.py",
            objective="if derivation stalls, acquire source-backed PPN/2PN bounds for retained radial/angle readout residuals",
            success_condition="at least one residual row has source path, units, normalization, arena projection and valid_for_claim=false",
            do_not_do="do not score placeholders or unsourced 2PN bounds",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["residual_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["gauge_contract"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["descent_signature"], BRANCH_COPIES["source_weight"]),
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
    validations.append(base_row(validation_id="VAL2187_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2187_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    contract_statuses = {row["status"] for row in rows_by_name["gauge_contract"]}
    contract_pass = {"AREAL_RECIPROCAL_BRANCH_ALLOWED_CONDITIONAL", "ISOTROPIC_PPN_BRANCH_ALLOWED_CONDITIONAL", "AREAL_ISOTROPIC_TRANSFORM_REQUIRED", "RADIAL_GAUGE_CONTRACT_WRITTEN_NOT_PARENT_SIGNED"}.issubset(contract_statuses)
    validations.append(base_row(validation_id="VAL2187_02_gauge_contract", status="PASS" if contract_pass else "FAIL", detail="areal/isotropic branch contract and transform are explicit"))

    rule_statuses = {row["status"] for row in rows_by_name["branch_rules"]}
    rules_pass = {"FORBIDDEN_MIXED_GAUGE", "PPN_GAUGE_REQUIRED_FOR_BETA_GAMMA", "GAUGE_LABEL_REQUIRED"}.issubset(rule_statuses)
    validations.append(base_row(validation_id="VAL2187_03_branch_rules", status="PASS" if rules_pass else "FAIL", detail="mixed-gauge scoring forbidden and kappa labels required"))

    sig_statuses = {row["status"] for row in rows_by_name["descent_signature"]}
    sig_pass = {"REQUIRED_NOT_PROVED", "PIM_LOCK_OPEN", "BOUNDARY_ZERO_OPEN", "SIGNATURE_MATRIX_WRITTEN_CURRENT_CLAIM_FAILS"}.issubset(sig_statuses)
    validations.append(base_row(validation_id="VAL2187_04_descent_signature", status="PASS" if sig_pass else "FAIL", detail="EH descent signature matrix is explicit and nonclaim"))

    residuals = rows_by_name["residual_rows"]
    has_mixed = any(row.get("symbol") == "sigma_spatial_2PN_mixed_forbidden" and row.get("value") == "1/2" for row in residuals)
    has_areal = any(row.get("symbol") == "sigma_spatial_2PN_areal_owned" and row.get("value") == "0" for row in residuals)
    has_missing = any(str(row.get("value", "")).startswith("MISSING_") or str(row.get("status", "")).startswith("MISSING_") for row in residuals)
    validations.append(base_row(validation_id="VAL2187_05_residual_rows", status="PASS" if has_mixed and has_areal and has_missing else "FAIL", detail=f"mixed warning, owned-areal zero, and missing descent rows represented; rows={len(residuals)}"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2187_06_claim_gate", status="PASS" if "PASS_GUARDRAIL" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses else "FAIL", detail="claim gate keeps local-GR and GitHub blocked"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2187_07_decision", status="PASS" if "EXTRA_DOUBLE_ZERO_AND_PIM_LOCK_SIGNATURE_NEXT" in decision_text else "FAIL", detail="decision selects extra double-zero and PiM lock next"))

    validations.append(base_row(validation_id="VAL2187_08_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2188" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2188 double-zero/PiM target selected"))

    validations.append(base_row(validation_id="VAL2187_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2187_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2187_11_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2187_artifacts()
    validations.append(base_row(validation_id="VAL2187_12_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2187 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2187_13_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2187_OVERALL", status="PASS" if overall else "FAIL", detail="2187 writes parent radial gauge/readout contract and keeps EH descent/local-GR nonclaim"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2187 - Y5/R2FR Parent-Owned Radial Gauge Map And EH Descent Signature

## Current Verdict

2187 turns the 2PN gauge fix into a rule, not a vibe.

The local branch now has two allowed readout branches:

1. **Areal reciprocal branch.** The parent readout defines `R_areal=sqrt(Area(S^2)/(4*pi))`, uses angular area coframe `R dOmega`, and the Schwarzschild/EH fixed-point form

`A=exp(v)=1-2GM/(c^2 R)`,

`B=exp(-v)=A^-1`.

2. **Isotropic PPN branch.** The parent readout defines `r_iso` by conformal-flat spatial PPN gauge, uses `A_iso=((1-x/2)/(1+x/2))^2`, and scores beta/gamma in that gauge.

The required map is:

`R=r_iso(1+x/2)^2`,

`y=GM/(c^2 R)=x/(1+x/2)^2`.

This means the old `+1/2*x^2` row is not a physical local-GR failure if the parent owns the areal/isotropic transform. It is a forbidden mixed-gauge residual: isotropic lapse plus reciprocal spatial readout in the same coordinate.

But the parent ownership is still not derived. 2187 gives the contract:

- do not mix gauges;
- label `kappa_v` by gauge;
- use areal reciprocal readout internally if that is the MTS branch;
- transform to isotropic/PPN gauge before beta/gamma scoring;
- derive or residualize the angular coframe and radial coordinate map.

So local-GR is healthier, but still nonclaim.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Parent Radial Gauge Contract

{md_table(rows_by_name["gauge_contract"], ["contract_id", "contract", "statement", "status", "implication", "valid_for_claim"])}

## Areal/Isotropic Branch Rules

{md_table(rows_by_name["branch_rules"], ["rule_id", "rule", "statement", "status", "implication", "valid_for_claim"])}

## EH Descent Signature Matrix

{md_table(rows_by_name["descent_signature"], ["signature_id", "signature", "statement", "status", "implication", "valid_for_claim"])}

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

This is exactly the kind of discipline the framework needed. The reciprocal branch survives, but only as a parent-owned areal readout or with a declared transform to PPN gauge.

That means the next bottleneck is not the 2PN gauge scare. It is the true descent theorem:

`MTS parent action -> EH fixed point -> extra-sector double zeros -> PiM lock -> source/boundary silence -> parent-owned readout gauge`.

The most valuable next attack is therefore the double-zero/PiM lock signature.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "gauge_contract": gauge_contract_rows(),
        "branch_rules": branch_rule_rows(),
        "descent_signature": descent_signature_rows(),
        "residual_rows": residual_row_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in [
        "source_register",
        "gauge_contract",
        "branch_rules",
        "descent_signature",
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
