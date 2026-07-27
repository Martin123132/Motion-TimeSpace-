from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2185"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2185-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2185_SOURCE_REGISTER.csv",
    "weak_action": OUT / "P8_Y5_PARENT_QLOC_2185_EH_TO_V_WEAK_ACTION_EXTRACTION.csv",
    "ppn_readout": OUT / "P8_Y5_PARENT_QLOC_2185_LAPSE_PPN_READOUT_EXTRACTION.csv",
    "inheritance_gate": OUT / "P8_Y5_PARENT_QLOC_2185_INHERITANCE_OR_GR_IMPORT_GATE.csv",
    "residual_rows": OUT / "P8_Y5_PARENT_QLOC_2185_RESIDUAL_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2185_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2185_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2185_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2185_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2185_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2185_EH_TO_V_RESIDUAL_ROWS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2185_EH_TO_V_EXTRACTION_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "EH_FIXED_POINT_TO_V_COEFFICIENT_EXTRACTION_2185_NONCLAIM.csv",
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


def formalization_has_2185_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2185-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2185*",
        "*P8_Y5_BRR545_2185*",
        "*Y5_R2FR_EH_fixed_point_to_v_action_coefficient_extraction_or_GR_import_demotion_2185*",
        "*JR2185*",
        "*EH_FIXED_POINT_TO_V_COEFFICIENT_EXTRACTION_2185*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2184_handoff",
            ROOT / "2184-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md",
            ["NEXT2184_0_2185", "EH_FIXED_POINT_TO_V_COEFFICIENT_EXTRACTION_NEXT", "VAL2184_OVERALL"],
            "2184 selects EH fixed-point to v coefficient extraction and GR-import demotion as the next gate.",
        ),
        (
            "2184_validation",
            OUT / "P8_Y5_BRR545_2184_VALIDATION.csv",
            ["VAL2184_OVERALL", "PASS"],
            "2184 validation passed before 2185 continues the chain.",
        ),
        (
            "2179_coefficients",
            ROOT / "2179-Y5-R2FR-parent-v-field-action-normalization-and-beta-quadratic-zero-or-finite-row.md",
            ["delta_v_source_norm=(C_v c^4/(16piG K_v))-1", "K_v=c^4/(32piG)", "beta=1+kappa_v/2"],
            "2179 gives the coefficient targets and beta/kappa map that 2185 must extract or demote.",
        ),
        (
            "2178_readout",
            ROOT / "2178-Y5-R2FR-constraint-before-readout-ordering-and-v-PPN-source-convention-or-readout-lock.md",
            ["Phi_N=(c^2/2)v", "laplacian(v)=8piG rho/c^2", "beta=1+kappa_v/2"],
            "2178 fixes the v-to-Newton potential convention and PPN readout relation.",
        ),
        (
            "minimal_local_gr_blocks",
            OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            ["A511_0_EH_core", "A511_2_universal_matter", "A511_6_metric_readout"],
            "minimal local-GR blocks supply EH core, universal matter, and readout/PiM double-zero conditions.",
        ),
        (
            "fixed_point_conditions",
            OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            ["FP511_1_double_zero_nonEH_coupling", "FP511_5_parent_PiM_lock", "FP511_7_metric_PPN_readout"],
            "fixed-point conditions define extra-sector double zeros, PiM lock, and PPN readout requirements.",
        ),
        (
            "noether_closure",
            OUT / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
            ["T505_conditional_Noether_mass_charge_closure", "T505_source_measure_matching", "T505_Newton_limit_corollary"],
            "Noether theorem gives the conditional mass-charge closure and Newton/Gauss corollary.",
        ),
        (
            "v_action_audit",
            OUT / "P8_Y5_PARENT_QLOC_2179_V_ACTION_COEFFICIENT_AUDIT.csv",
            ["VAC2179_1_target_coefficients", "VAC2179_2_parent_origin_test", "VAC2179_5_current_verdict"],
            "v action audit records the exact target coefficients and the prior missing parent origin.",
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


def weak_action_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "WAE2185_0_EH_weak_action",
            "EH fixed-point weak Newton action",
            "L_Phi = -(8*pi*G_ref)^-1 (grad Phi_N)^2 - rho Phi_N.",
            "STANDARD_EH_WEAK_FIELD_INHERITANCE",
            "Phi_N has the usual Poisson normalization inside the EH fixed point.",
            "not_a_standalone_MTS_claim",
        ),
        (
            "WAE2185_1_substitute_v",
            "v lapse substitution",
            "Phi_N = c^2 v/2, so (grad Phi_N)^2 = c^4 (grad v)^2/4 and rho Phi_N = rho c^2 v/2.",
            "EXACT_SUBSTITUTION",
            "the weak action becomes L_v = -c^4/(32*pi*G_ref)(grad v)^2 - rho c^2 v/2.",
            "conditional_on_EH_fixed_point",
        ),
        (
            "WAE2185_2_Kv",
            "K_v extraction",
            "Compare L_v = -K_v(grad v)^2 - C_v rho c^2 v.",
            "K_V_EXTRACTED_CONDITIONAL",
            "K_v = c^4/(32*pi*G_ref).",
            "conditional_value",
        ),
        (
            "WAE2185_3_Cv",
            "C_v extraction",
            "Compare the matter source term -rho c^2 v/2 with -C_v rho c^2 v.",
            "C_V_EXTRACTED_CONDITIONAL",
            "C_v = 1/2.",
            "conditional_value",
        ),
        (
            "WAE2185_4_delta",
            "source normalization residual",
            "delta_v_source_norm = C_v c^4/(16*pi*G_ref K_v)-1 = (1/2)c^4/(16*pi*G_ref*c^4/(32*pi*G_ref))-1.",
            "DELTA_V_SOURCE_NORM_ZERO_CONDITIONAL",
            "delta_v_source_norm = 0.",
            "conditional_zero",
        ),
        (
            "WAE2185_5_Euler",
            "Euler-Lagrange check",
            "Varying L_v gives 2K_v laplacian(v)-C_v rho c^2=0, hence laplacian(v)=8*pi*G_ref rho/c^2.",
            "POISSON_NORMALIZATION_MATCHES_2178",
            "the EH fixed point reproduces the 2178 Newton source convention.",
            "conditional_on_same_source_measure",
        ),
    ]
    return [
        base_row(
            extraction_id=extraction_id,
            object=object_name,
            equation=equation,
            status=status,
            result=result,
            claim_grade=claim_grade,
        )
        for extraction_id, object_name, equation, status, result, claim_grade in rows
    ]


def ppn_readout_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PPE2185_0_isotropic_lapse",
            "EH isotropic lapse",
            "For x=G_ref M/(c^2 r_iso), A_iso=((1-x/2)/(1+x/2))^2 = 1-2x+2x^2-3x^3/2+O(x^4).",
            "EXACT_SERIES_TO_3PN",
            "g_tt=-A_iso c^2 has PPN beta=1.",
        ),
        (
            "PPE2185_1_v_log",
            "v logarithm",
            "v=log(A_iso)=-2x+0*x^2-x^3/6+O(x^4).",
            "KAPPA_V_ZERO_CONDITIONAL",
            "kappa_v=0 for the EH isotropic lapse readout.",
        ),
        (
            "PPE2185_2_beta",
            "beta extraction",
            "A_iso=exp(v)=1-2x+2x^2+O(x^3), and 2 beta is the x^2 coefficient.",
            "BETA_ONE_CONDITIONAL",
            "beta=1.",
        ),
        (
            "PPE2185_3_gamma",
            "gamma first-order extraction",
            "Both reciprocal B=exp(-v) and isotropic GR spatial factor B_iso=(1+x/2)^4 have 1+2x+O(x^2).",
            "GAMMA_ONE_CONDITIONAL_FIRST_ORDER",
            "gamma=1 at first PPN order once v source amplitude is fixed.",
        ),
        (
            "PPE2185_4_spatial_2PN_warning",
            "reciprocal branch 2PN spatial warning",
            "B_recip=exp(-v)=1+2x+2x^2+O(x^3), while B_iso=(1+x/2)^4=1+2x+3x^2/2+O(x^3).",
            "TWO_PN_SPATIAL_RESIDUAL_LIVE",
            "reciprocal branch differs from isotropic GR by +1/2*x^2 in the spatial coefficient.",
        ),
        (
            "PPE2185_5_no_gamma_shortcut",
            "no gamma-only promotion",
            "gamma=1 and beta=1 under the EH lapse extraction do not by themselves prove full local GR if the constrained reciprocal spatial readout is kept through 2PN.",
            "LOCAL_GR_BEYOND_1PN_NOT_CLAIMED",
            "2PN/spatial/readout residual must be resolved or bounded.",
        ),
    ]
    return [
        base_row(
            ppn_id=ppn_id,
            object=object_name,
            equation=equation,
            status=status,
            result=result,
        )
        for ppn_id, object_name, equation, status, result in rows
    ]


def inheritance_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "IHG2185_0_EH_internal",
            "inside EH fixed point",
            "K_v, C_v, delta_v_source_norm, kappa_v, beta and gamma are extracted from EH weak-field/lapse readout.",
            "EH_FIXED_POINT_EXTRACTION_PASS",
            "the coefficient problem is solved inside the EH local fixed point.",
        ),
        (
            "IHG2185_1_MTS_descent",
            "MTS to EH descent",
            "MTS must parent-derive the EH fixed point, universal observed coframe, extra-sector double zeros, PiM lock, and zero boundary flux.",
            "MTS_DESCENT_NOT_YET_PARENT_SIGNED",
            "without this, the result is GR import rather than MTS derivation.",
        ),
        (
            "IHG2185_2_PiM",
            "Hamiltonian PiM lock",
            "Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0 must hold at the local fixed point.",
            "PIM_LOCK_OPEN",
            "mass projector calibration freedom remains live.",
        ),
        (
            "IHG2185_3_source",
            "same source measure",
            "rho in the v action must be the same Hilbert/Hamiltonian source measure used by M_source[W].",
            "SOURCE_MEASURE_GLUE_OPEN",
            "otherwise the coefficient extraction can have the right algebra but wrong mass.",
        ),
        (
            "IHG2185_4_boundary",
            "boundary/readout silence",
            "GHY/reference/exact/topological boundary terms and reciprocal readout corrections must not shift the local mass or PPN vector.",
            "BOUNDARY_AND_2PN_READOUT_OPEN",
            "2PN spatial and boundary residuals remain nonclaim rows.",
        ),
        (
            "IHG2185_5_verdict",
            "inheritance verdict",
            "2185 is a conditional win for the EH fixed-point coefficient extraction, not a full MTS local-GR claim.",
            "CONDITIONAL_INHERITANCE_WIN_CURRENT_MTS_CLAIM_BLOCKED",
            "push next to MTS descent and 2PN readout audit.",
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
        for gate_id, gate, statement, status, implication in rows
    ]


def residual_row_rows() -> list[dict[str, Any]]:
    rows = [
        ("CER2185_0_Kv", "K_v", "EH fixed-point weak-field v kinetic coefficient", "c^4/(32*pi*G_ref)", "DERIVED_WITHIN_EH_FIXED_POINT_CONDITIONAL", "energy_density_length2_or_declared", "Newton;PPN;local_GR"),
        ("CER2185_1_Cv", "C_v", "EH fixed-point universal matter source coefficient", "1/2", "DERIVED_WITHIN_EH_FIXED_POINT_CONDITIONAL", "dimensionless", "Newton;PPN;WEP"),
        ("CER2185_2_delta", "delta_v_source_norm", "C_v c^4/(16*pi*G_ref K_v)-1", "0", "ZERO_WITHIN_EH_FIXED_POINT_CONDITIONAL", "dimensionless", "Newton;PPN;orbital"),
        ("CER2185_3_kappa", "kappa_v", "x^2 coefficient in v=-2x+kappa_v x^2+O(x^3)", "0", "ZERO_WITHIN_EH_ISOTROPIC_LAPSE_CONDITIONAL", "dimensionless", "PPN_beta;local_GR"),
        ("CER2185_4_beta", "beta", "PPN beta from A=exp(v)=1-2x+2 beta x^2+O(x^3)", "1", "ONE_WITHIN_EH_FIXED_POINT_CONDITIONAL", "dimensionless", "PPN_beta"),
        ("CER2185_5_gamma", "gamma", "PPN gamma at first order from spatial coefficient 1+2 gamma x+O(x^2)", "1", "ONE_FIRST_ORDER_CONDITIONAL", "dimensionless", "PPN_gamma;light_deflection"),
        ("CER2185_6_spatial_2PN", "sigma_spatial_2PN_recip_minus_iso", "x^2 spatial coefficient difference B_recip-B_iso if reciprocal branch is imposed", "1/2", "FINITE_2PN_READOUT_WARNING_NONCLAIM", "dimensionless_2PN_coefficient", "2PN;light_time;perihelion"),
        ("CER2185_7_MTS_descent", "epsilon_EH_fixed_point_descent", "failure of MTS parent action to derive EH fixed-point descent and double-zero extra sectors", "MISSING_PARENT_DESCENT_PROOF", "MISSING_MTS_DESCENT_SIGNATURE", "dimensionless_or_declared", "local_GR;WEP;PPN"),
        ("CER2185_8_PiM", "epsilon_PiM_lock", "failure of Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0", "MISSING_PARENT_PIM_LOCK", "MISSING_PIM_LOCK_PROOF", "dimensionless_or_GM_flux", "Newton;R10;R11;PPN"),
        ("CER2185_9_boundary", "epsilon_boundary_2PN", "boundary/reference/readout residual after EH-to-v extraction", "MISSING_BOUNDARY_AND_2PN_RESOLUTION", "MISSING_SOURCE_PATH", "dimensionless_or_2PN", "local_GR;2PN;orbital"),
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
            source_path=str(DOC) if not str(status).startswith("MISSING_") else "MISSING_SOURCE_PATH",
            score_ready=False,
        )
        for row_id, symbol, definition, value, status, units, observable_link in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2185_0_EH_extraction", "EH fixed-point extracts K_v, C_v, delta_v_source_norm, kappa_v", "CONDITIONAL_PASS", "the coefficient extraction works inside the EH fixed point"),
        ("CG2185_1_MTS_descent", "MTS parent action derives the EH fixed point and double zeros", "BLOCKED_NONCLAIM", "descent clauses remain unsigned in current corpus"),
        ("CG2185_2_source_glue", "rho is the same Hilbert/Hamiltonian source measure", "BLOCKED_NONCLAIM", "PiM/Hamiltonian and worldtube source glue remain open"),
        ("CG2185_3_boundary_2PN", "boundary/reference and reciprocal 2PN spatial residuals are zero or bounded", "BLOCKED_NONCLAIM", "2PN spatial warning and boundary terms remain live"),
        ("CG2185_4_Newton_1PN", "Newton plus 1PN beta/gamma can be promoted for MTS", "BLOCKED_NONCLAIM", "conditional EH extraction is not yet parent-signed by MTS"),
        ("CG2185_5_local_GR", "full local GR reduction can be claimed", "BLOCKED_NONCLAIM", "needs MTS descent, PiM lock, source glue, boundary zero, and 2PN/readout resolution"),
        ("CG2185_6_no_import_guard", "GR import guard retained", "PASS_GUARDRAIL", "EH result is labelled conditional inheritance, not standalone MTS proof"),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2185_0_gain", "EH_TO_V_COEFFICIENT_EXTRACTION_SUCCEEDS_CONDITIONALLY", "Inside the EH fixed point, K_v=c^4/(32*pi*G_ref), C_v=1/2, delta_v_source_norm=0, kappa_v=0, beta=1 and gamma=1 at 1PN.", "selected"),
        ("DEC2185_1_warning", "RECIPROCAL_SPATIAL_2PN_RESIDUAL_EXPOSED", "The reciprocal branch B=exp(-v) differs from isotropic GR spatial readout by +1/2 at x^2, so full local-GR/2PN is not automatically closed.", "selected"),
        ("DEC2185_2_limit", "MTS_DESCENT_STILL_UNSIGNED", "The result is derived inheritance only if MTS parent-signs the EH fixed point, PiM lock, source measure, extra double zeros and boundary zero.", "selected"),
        ("DEC2185_3_next", "MTS_EH_DESCENT_AND_2PN_READOUT_GATE_NEXT", "The next target should prove the MTS-to-EH descent clauses and decide whether reciprocal readout is gauge-equivalent, corrected, or a finite 2PN residual.", "selected"),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2185_0_2186",
            selection_status="selected",
            target_file="2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md",
            target_script="scripts/Y5_R2FR_MTS_EH_fixed_point_descent_and_2PN_readout_residual_gate_2186.py",
            objective="prove the MTS parent descent to the EH fixed point, PiM lock, universal source measure, extra-sector double zeros, and resolve the reciprocal-readout 2PN spatial residual; otherwise keep nonclaim finite rows",
            success_condition="MTS parent-signs EH fixed point plus PiM(Phi0)=Pi_EH, source measure glue, zero boundary/reference flux, no extra mass channels, and either removes/bounds the +1/2 spatial 2PN residual",
            do_not_do="do not claim local GR from EH extraction alone, do not ignore 2PN spatial mismatch, do not absorb source mismatch into measured G, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2185_1_empirical_parallel",
            selection_status="held_parallel",
            target_file="2186b-Y5-R2FR-2PN-PPN-readout-bound-acquisition.md",
            target_script="scripts/Y5_R2FR_2PN_PPN_readout_bound_acquisition_2186b.py",
            objective="if derivation stalls, acquire source-backed bounds/projections for reciprocal spatial 2PN residual, PiM lock residual, and boundary/source glue",
            success_condition="at least one residual row has source path, units, normalization, arena projection, and valid_for_claim=false until all local-GR gates close",
            do_not_do="do not score placeholders, unsourced bounds, or cancellation-only rows",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["residual_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["weak_action"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["ppn_readout"], BRANCH_COPIES["source_weight"]),
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
    validations.append(base_row(validation_id="VAL2185_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2185_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    weak_statuses = {row["status"] for row in rows_by_name["weak_action"]}
    weak_pass = {"K_V_EXTRACTED_CONDITIONAL", "C_V_EXTRACTED_CONDITIONAL", "DELTA_V_SOURCE_NORM_ZERO_CONDITIONAL", "POISSON_NORMALIZATION_MATCHES_2178"}.issubset(weak_statuses)
    validations.append(base_row(validation_id="VAL2185_02_weak_action", status="PASS" if weak_pass else "FAIL", detail="EH weak action extracts K_v, C_v and delta zero conditionally"))

    ppn_statuses = {row["status"] for row in rows_by_name["ppn_readout"]}
    ppn_pass = {"KAPPA_V_ZERO_CONDITIONAL", "BETA_ONE_CONDITIONAL", "TWO_PN_SPATIAL_RESIDUAL_LIVE"}.issubset(ppn_statuses)
    validations.append(base_row(validation_id="VAL2185_03_ppn_readout", status="PASS" if ppn_pass else "FAIL", detail="lapse readout gives kappa/beta conditionally and exposes 2PN spatial residual"))

    inheritance_statuses = {row["status"] for row in rows_by_name["inheritance_gate"]}
    inherit_pass = "CONDITIONAL_INHERITANCE_WIN_CURRENT_MTS_CLAIM_BLOCKED" in inheritance_statuses and "MTS_DESCENT_NOT_YET_PARENT_SIGNED" in inheritance_statuses
    validations.append(base_row(validation_id="VAL2185_04_inheritance_gate", status="PASS" if inherit_pass else "FAIL", detail="EH extraction is labelled conditional inheritance, not final MTS proof"))

    residual_rows = rows_by_name["residual_rows"]
    has_values = any(row.get("symbol") == "delta_v_source_norm" and row.get("value") == "0" for row in residual_rows) and any(row.get("symbol") == "kappa_v" and row.get("value") == "0" for row in residual_rows)
    has_missing = any(str(row.get("status", "")).startswith("MISSING_") or str(row.get("value", "")).startswith("MISSING_") for row in residual_rows)
    has_2pn = any(row.get("symbol") == "sigma_spatial_2PN_recip_minus_iso" and row.get("value") == "1/2" for row in residual_rows)
    validations.append(base_row(validation_id="VAL2185_05_residual_rows", status="PASS" if has_values and has_missing and has_2pn else "FAIL", detail=f"conditional values, missing descent rows, and 2PN warning represented; rows={len(residual_rows)}"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2185_06_claim_gate", status="PASS" if "BLOCKED_NONCLAIM" in claim_statuses and "PASS_GUARDRAIL" in claim_statuses and "CONDITIONAL_PASS" in claim_statuses else "FAIL", detail="claim gate separates conditional EH pass from blocked MTS/local-GR claim"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2185_07_decision", status="PASS" if "MTS_EH_DESCENT_AND_2PN_READOUT_GATE_NEXT" in decision_text else "FAIL", detail="decision selects MTS EH descent and 2PN readout gate next"))

    validations.append(base_row(validation_id="VAL2185_08_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2186" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2186 descent/readout target selected"))

    validations.append(base_row(validation_id="VAL2185_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2185_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2185_11_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2185_artifacts()
    validations.append(base_row(validation_id="VAL2185_12_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2185 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2185_13_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2185_OVERALL", status="PASS" if overall else "FAIL", detail="2185 conditionally extracts EH fixed-point v coefficients and exposes MTS descent/2PN residual gates"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2185 - Y5/R2FR EH Fixed Point To V Action Coefficient Extraction Or GR Import Demotion

## Current Verdict

2185 is a conditional win, not a final local-GR claim.

Inside the EH fixed point, the weak Newton action is:

`L_Phi = -(8*pi*G_ref)^-1 (grad Phi_N)^2 - rho Phi_N`.

Using the 2178 readout convention,

`Phi_N = c^2 v/2`,

gives:

`L_v = -c^4/(32*pi*G_ref)(grad v)^2 - rho c^2 v/2`.

Therefore:

`K_v = c^4/(32*pi*G_ref)`,

`C_v = 1/2`,

`delta_v_source_norm = C_v c^4/(16*pi*G_ref K_v)-1 = 0`.

That is the first clean coefficient extraction we wanted.

For the lapse/PPN side, with `x=G_ref M/(c^2 r_iso)`,

`A_iso=((1-x/2)/(1+x/2))^2 = 1-2x+2x^2-3x^3/2+O(x^4)`,

so

`v=log(A_iso)=-2x+0*x^2-x^3/6+O(x^4)`.

Thus:

`kappa_v=0`, `beta=1`, and `gamma=1` at first PPN order.

But there is one important warning:

`B_recip=exp(-v)=1+2x+2x^2+O(x^3)`,

whereas isotropic GR has

`B_iso=(1+x/2)^4=1+2x+3x^2/2+O(x^3)`.

So the constrained reciprocal spatial branch differs from isotropic GR by `+1/2*x^2` at 2PN spatial order. That is not a standard first-PPN beta/gamma failure, but it is a real local-GR/readout residual that must be resolved, bounded, or gauge-mapped.

Bottom line: the coefficient extraction works **inside EH**. MTS only owns it if the parent action really descends to the EH fixed point with PiM lock, universal source measure, extra-sector double zeros, and zero boundary/reference flux.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## EH To V Weak Action Extraction

{md_table(rows_by_name["weak_action"], ["extraction_id", "object", "equation", "status", "result", "claim_grade", "valid_for_claim"])}

## Lapse PPN Readout Extraction

{md_table(rows_by_name["ppn_readout"], ["ppn_id", "object", "equation", "status", "result", "valid_for_claim"])}

## Inheritance Or GR Import Gate

{md_table(rows_by_name["inheritance_gate"], ["gate_id", "gate", "statement", "status", "implication", "valid_for_claim"])}

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

This is the best result we could reasonably hope for at 2185:

`EH fixed point -> v as lapse -> K_v=c^4/(32*pi*G_ref), C_v=1/2, delta_v_source_norm=0, kappa_v=0`.

So the coefficient side is not looking grim. It is looking conditional.

The remaining hard question is no longer "can the numbers come out right?" They can, inside the EH fixed point. The hard question is:

can MTS derive that EH fixed point locally without smuggling it in, and can it resolve the reciprocal spatial 2PN mismatch?
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "weak_action": weak_action_rows(),
        "ppn_readout": ppn_readout_rows(),
        "inheritance_gate": inheritance_gate_rows(),
        "residual_rows": residual_row_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in [
        "source_register",
        "weak_action",
        "ppn_readout",
        "inheritance_gate",
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
