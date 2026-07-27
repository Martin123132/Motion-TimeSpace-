from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_EH_FIXED_POINT_TO_V_COEFFICIENT_EXTRACTION_2505"
CHECKPOINT_ID = "2505"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"

DOC = ROOT / "2505-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2505_SOURCE_REGISTER.csv",
    "extraction": OUT / "P8_Y5_NO_SHADOW_2505_EH_TO_V_EXTRACTION_LIVE_PORT.csv",
    "ppn_readout": OUT / "P8_Y5_NO_SHADOW_2505_PPN_READOUT_VECTOR.csv",
    "ownership_guard": OUT / "P8_Y5_NO_SHADOW_2505_GR_IMPORT_GUARD.csv",
    "residual_rows": OUT / "P8_Y5_NO_SHADOW_2505_RESIDUAL_ROWS.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2505_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2505_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2505_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2505_VALIDATION.csv",
}

BRANCH_COPIES = {
    "extraction": LOCAL_BOUNDS / "EH_to_v_extraction_2505_NONCLAIM.csv",
    "ppn_readout": BETA_DOCS / "PPN_readout_vector_2505_NONCLAIM.csv",
    "residual_rows": QUEUE / "JR2505_PARENT_EH_DESCENT_RESIDUAL_ROWS_NONCLAIM.csv",
    "next_target": QUEUE / "JR2505_PARENT_EH_DESCENT_SOURCE_GLUE_NEXT.csv",
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


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC2505_00_2504_handoff",
            ROOT / "2504-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md",
            ["NEXT2504_0_selected", "EH-to-v coefficient extraction", "VAL2504_OVERALL"],
            "2504 selects EH-to-v coefficient extraction and insists on a GR-import guard.",
        ),
        (
            "SRC2505_01_2504_validation",
            OUT / "P8_Y5_BRR545_2504_VALIDATION.csv",
            ["VAL2504_OVERALL", "PASS"],
            "2504 validation passed before 2505 continues the current private chain.",
        ),
        (
            "SRC2505_02_2185_extraction",
            ROOT / "2185-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
            ["WAE2185_2_Kv", "PPE2185_2_beta", "VAL2185_OVERALL"],
            "2185 contains the older EH fixed-point calculation that 2505 live-ports into the current branch.",
        ),
        (
            "SRC2505_03_2186_descent_warning",
            ROOT / "2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md",
            ["RGC2186_5_resolution", "DEG2186_7_verdict", "VAL2186_OVERALL"],
            "2186 says the 2PN issue is gauge/readout debt but MTS EH descent is still unsigned.",
        ),
        (
            "SRC2505_04_2504_contract",
            OUT / "P8_Y5_NO_SHADOW_2504_MINIMAL_PARENT_ACTION_CHARGE_CONTRACT.csv",
            ["PAC2504_7_current_verdict", "COHERENT_CONTRACT_CURRENT_CLAIM_FAILS"],
            "2504 contract gives the parent-action ownership clauses still missing.",
        ),
        (
            "SRC2505_05_2504_noether",
            OUT / "P8_Y5_NO_SHADOW_2504_NOETHER_HAMILTONIAN_CHARGE_CHAIN.csv",
            ["NHC2504_4_PiM_identification", "CORE_MISSING_IDENTITY_NOT_DERIVED"],
            "2504 noether chain identifies the PiM/Hilbert equality as the central unsigned source charge.",
        ),
        (
            "SRC2505_06_2504_v_bridge",
            OUT / "P8_Y5_NO_SHADOW_2504_V_LAPSE_READOUT_BRIDGE.csv",
            ["VBR2504_2_EH_to_v_coefficients", "VBR2504_5_status"],
            "2504 v bridge says EH-to-v inheritance is coherent but not yet parent-signed.",
        ),
        (
            "SRC2505_07_2504_binding",
            OUT / "P8_Y5_NO_SHADOW_2504_LIVE_DESCENT_BINDING_STATUS.csv",
            ["LDB2504_3_local_GR", "not claimable"],
            "2504 binding status blocks local GR/Newton promotion until the descent/source/boundary clauses close.",
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
                source_pass=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def extraction_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "EX2505_0_EH_weak_action",
            "EH weak Newton action",
            "L_Phi = -(8*pi*G_ref)^-1 |grad Phi_N|^2 - rho Phi_N",
            "STANDARD_EH_FIXED_POINT_INPUT",
            "This is a GR/EH fixed-point result, not yet a free-standing MTS result.",
        ),
        (
            "EX2505_1_v_substitution",
            "lapse variable substitution",
            "Phi_N = c^2 v/2",
            "EXACT_READOUT_SUBSTITUTION",
            "L_v = -c^4/(32*pi*G_ref)|grad v|^2 - rho c^2 v/2.",
        ),
        (
            "EX2505_2_Kv",
            "kinetic coefficient",
            "Compare L_v = -K_v |grad v|^2 - C_v rho c^2 v",
            "K_V_EXTRACTED_INSIDE_EH",
            "K_v = c^4/(32*pi*G_ref).",
        ),
        (
            "EX2505_3_Cv",
            "source coefficient",
            "Compare -rho c^2 v/2 with -C_v rho c^2 v",
            "C_V_EXTRACTED_INSIDE_EH",
            "C_v = 1/2.",
        ),
        (
            "EX2505_4_delta_v_source_norm",
            "Newton source normalization",
            "delta_v_source_norm = C_v c^4/(16*pi*G_ref K_v)-1",
            "DELTA_V_SOURCE_NORM_ZERO_INSIDE_EH",
            "delta_v_source_norm = 0.",
        ),
        (
            "EX2505_5_Euler_Poisson",
            "Euler-Lagrange check",
            "2 K_v laplacian(v) - C_v rho c^2 = 0",
            "POISSON_NORMALIZATION_MATCHES",
            "laplacian(v)=8*pi*G_ref rho/c^2.",
        ),
    ]
    return [
        base_row(
            extraction_id=extraction_id,
            object=object_name,
            equation=equation,
            status=status,
            result=result,
            claim_grade="conditional_EH_fixed_point_not_MTS_owned",
        )
        for extraction_id, object_name, equation, status, result in specs
    ]


def ppn_readout_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PPN2505_0_A_iso",
            "EH isotropic lapse",
            "x=G_ref M/(c^2 r_iso); A_iso=((1-x/2)/(1+x/2))^2=1-2x+2x^2-3x^3/2+O(x^4)",
            "BETA_ONE_INSIDE_EH",
            "g_tt=-A_iso c^2 gives beta=1.",
        ),
        (
            "PPN2505_1_v_log",
            "log-lapse readout",
            "v=log(A_iso)=-2x+0*x^2-x^3/6+O(x^4)",
            "KAPPA_V_ZERO_INSIDE_EH",
            "kappa_v=0.",
        ),
        (
            "PPN2505_2_beta_law",
            "MTS v beta relation",
            "A=exp(v)=1-2x+2 beta x^2+O(x^3); beta=1+kappa_v/2",
            "BETA_LAW_MATCHES_EH",
            "kappa_v=0 implies beta=1 inside the EH fixed point.",
        ),
        (
            "PPN2505_3_gamma_first_order",
            "spatial first PPN",
            "B_recip=exp(-v)=1+2x+O(x^2); B_iso=(1+x/2)^4=1+2x+O(x^2)",
            "GAMMA_ONE_FIRST_ORDER_CONDITIONAL",
            "gamma=1 at first PPN order once source amplitude is fixed.",
        ),
        (
            "PPN2505_4_spatial_2PN_warning",
            "reciprocal spatial 2PN residue",
            "B_recip=1+2x+2x^2+O(x^3); B_iso=1+2x+3x^2/2+O(x^3)",
            "FINITE_2PN_READOUT_WARNING_CONDITIONAL_GAUGE_DEBT",
            "reciprocal minus isotropic spatial x^2 coefficient is +1/2 unless parent-owned radial gauge/readout map removes it.",
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
        for ppn_id, object_name, equation, status, result in specs
    ]


def ownership_guard_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "GUARD2505_0_inside_EH",
            "EH internal coefficient extraction",
            "K_v, C_v, delta_v_source_norm, kappa_v, beta and gamma are fixed inside the EH local fixed point.",
            "DERIVED_INSIDE_EH_FIXED_POINT",
            "This is a real mathematical reduction, but only within the imported EH sector.",
        ),
        (
            "GUARD2505_1_parent_action",
            "MTS parent action ownership",
            "A single parent action must descend to EH locally with universal observed coframe and no extra source channel.",
            "MTS_PARENT_ACTION_DESCENT_UNSIGNED",
            "MTS does not yet own the EH coefficients.",
        ),
        (
            "GUARD2505_2_PiM",
            "Hamiltonian mass charge equality",
            "(4*pi*G_ref)^-1 int_S Pi_M J_H = H_tau[S]-H_tau[reference]",
            "PIM_HILBERT_IDENTITY_UNSIGNED",
            "The observed source mass still needs parent signing.",
        ),
        (
            "GUARD2505_3_boundary",
            "boundary/reference silence",
            "Boundary, topological and reference terms must not shift the local source mass or PPN vector.",
            "ZERO_BOUNDARY_FLUX_UNSIGNED",
            "Local GR/Newton cannot be promoted from the coefficient algebra alone.",
        ),
        (
            "GUARD2505_4_import_guard",
            "GR import guard",
            "If EH is simply assumed as a local subtheory, label the result GR import rather than MTS derivation.",
            "GUARDRAIL_ACTIVE_NO_LOCAL_GR_CLAIM",
            "No public/local-GR claim is allowed from 2505.",
        ),
    ]
    return [
        base_row(
            guard_id=guard_id,
            gate=gate,
            statement=statement,
            status=status,
            implication=implication,
        )
        for guard_id, gate, statement, status, implication in specs
    ]


def residual_rows() -> list[dict[str, Any]]:
    specs = [
        ("RES2505_0_Kv", "K_v", "EH fixed-point v kinetic coefficient", "c^4/(32*pi*G_ref)", "DERIVED_INSIDE_EH_FIXED_POINT_CONDITIONAL", "action_density_length2", "Newton;PPN;local_GR", "not_score_ready_until_MTS_descent"),
        ("RES2505_1_Cv", "C_v", "EH fixed-point matter source coefficient", "1/2", "DERIVED_INSIDE_EH_FIXED_POINT_CONDITIONAL", "dimensionless", "Newton;WEP;PPN", "not_score_ready_until_same_source_measure"),
        ("RES2505_2_delta_v", "delta_v_source_norm", "C_v c^4/(16*pi*G_ref K_v)-1", "0", "ZERO_INSIDE_EH_FIXED_POINT_CONDITIONAL", "dimensionless", "Newton;orbital;PPN", "not_score_ready_until_MTS_owns_EH"),
        ("RES2505_3_kappa_v", "kappa_v", "x^2 coefficient in v=-2x+kappa_v x^2+O(x^3)", "0", "ZERO_INSIDE_EH_ISOTROPIC_READOUT_CONDITIONAL", "dimensionless", "PPN_beta", "not_score_ready_until_readout_owned"),
        ("RES2505_4_beta", "beta", "beta=1+kappa_v/2", "1", "ONE_INSIDE_EH_FIXED_POINT_CONDITIONAL", "dimensionless", "PPN_beta", "not_score_ready_until_import_guard_closed"),
        ("RES2505_5_gamma", "gamma", "first-order spatial PPN coefficient", "1", "ONE_FIRST_ORDER_CONDITIONAL", "dimensionless", "PPN_gamma", "not_score_ready_until_source_amplitude_owned"),
        ("RES2505_6_sigma_2PN", "sigma_spatial_2PN_recip_minus_iso", "B_recip-B_iso spatial x^2 coefficient if reciprocal readout is imposed", "1/2", "FINITE_2PN_READOUT_WARNING_GAUGE_DEBT", "dimensionless_2PN", "2PN;light_time;orbital", "must_be_parent_gauge_mapped_or_bounded"),
        ("RES2505_7_EH_descent", "epsilon_EH_fixed_point_descent", "MTS parent-action failure to derive EH local fixed point", "MISSING_PARENT_FIXED_POINT_DESCENT", "MISSING_PARENT_DESCENT_SIGNATURE", "dimensionless_or_declared", "local_GR;Newton", "core_blocker"),
        ("RES2505_8_PiM_source", "epsilon_PiM_source_glue", "failure of Pi_M/Hilbert/Hamiltonian source equality", "MISSING_HAMILTONIAN_PIM_IDENTITY", "MISSING_PARENT_SOURCE_GLUE", "dimensionless_or_GM_flux", "Newton;R10;R11;PPN", "core_blocker"),
        ("RES2505_9_boundary", "epsilon_boundary_reference", "boundary/reference/topological local source shift", "MISSING_ZERO_BOUNDARY_FLUX", "MISSING_BOUNDARY_SILENCE_PROOF", "dimensionless_or_GM_flux", "local_GR;orbital;PPN", "core_blocker"),
        ("RES2505_10_extra_sector", "epsilon_extra_sector_double_zero", "failure of all non-EH sectors to have value and first variation zero at local fixed point", "MISSING_X_SECTOR_DOUBLE_ZERO", "MISSING_PARENT_DOUBLE_ZERO_PROOF", "dimensionless_or_operator_norm", "WEP;PPN;R10;clock", "core_blocker"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            value=value,
            status=status,
            units=units,
            observable_link=observable,
            source_path=str(DOC),
            score_ready=False,
            blocker_class=blocker_class,
        )
        for row_id, symbol, definition, value, status, units, observable, blocker_class in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2505_0_gain",
            "EH_TO_V_EXTRACTION_LIVE_PORTED",
            "2505 imports the older clean calculation into the current 2504 chain: K_v=c^4/(32*pi*G_ref), C_v=1/2, delta_v_source_norm=0, kappa_v=0, beta=1.",
            "selected",
        ),
        (
            "DEC2505_1_limit",
            "MTS_OWNERSHIP_STILL_BLOCKED",
            "The calculation is derived inside EH, but MTS ownership still needs parent action descent, PiM/Hilbert source equality, zero boundary flux, and extra-sector double zeros.",
            "selected",
        ),
        (
            "DEC2505_2_2PN",
            "TWO_PN_IS_READOUT_DEBT_NOT_FATAL_1PN_FAILURE",
            "The reciprocal spatial +1/2 coefficient is retained as gauge/readout debt unless the parent radial/coframe map removes or bounds it.",
            "selected",
        ),
        (
            "DEC2505_3_next",
            "PARENT_EH_DESCENT_SOURCE_GLUE_NEXT",
            "The next useful step is not another coefficient extraction; it is a direct proof attempt for the parent EH descent/source-glue package.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2505_0_selected",
            selection_status="selected",
            target_file="2506-Y5-R2FR-parent-EH-descent-source-glue-proof-or-explicit-GR-import-demotion.md",
            target_script="scripts/Y5_R2FR_parent_EH_descent_source_glue_proof_or_explicit_GR_import_demotion_2506.py",
            objective="try to prove that the MTS parent action descends to the EH fixed point with the same Hilbert/Hamiltonian source measure, PiM identity, zero boundary flux, and extra-sector double zeros; otherwise explicitly label the local branch as GR import plus residual interface",
            success_condition="one parent package signs EH descent, PiM/Hilbert equality, source measure glue, boundary silence, extra-sector double zeros, and radial/coframe readout ownership",
            do_not_do="do not re-fit G, do not claim beta/gamma as MTS-owned from EH alone, do not hide the 2PN readout warning, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2505_1_parallel_bounds",
            selection_status="held_parallel",
            target_file="2506b-Y5-R2FR-local-GR-residual-bound-interface.md",
            target_script="scripts/Y5_R2FR_local_GR_residual_bound_interface_2506b.py",
            objective="if the proof fails, turn the five missing parent clauses into explicit residual-bound rows for PPN, R10, clocks, WEP and orbital tests",
            success_condition="each residual row has units, source path, arena projection, and valid_for_claim=false until all source inputs are real",
            do_not_do="do not score placeholder rows or treat bound-only survival as derived local GR",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("extraction", OUTPUTS["extraction"], BRANCH_COPIES["extraction"]),
        ("ppn_readout", OUTPUTS["ppn_readout"], BRANCH_COPIES["ppn_readout"]),
        ("residual_rows", OUTPUTS["residual_rows"], BRANCH_COPIES["residual_rows"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=f"COPY2505_{copy_id}", source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        validations.append(base_row(check_id=check_id, status="PASS" if status else "FAIL", notes=notes, detail=detail))

    add("VAL2505_00_sources_exist", all(row["path_exists"] for row in rows_by_name["source_register"]), "all cited source paths exist")
    add("VAL2505_01_source_needles", all(row["source_pass"] for row in rows_by_name["source_register"]), "all required source needles are present")

    extraction_statuses = {row["status"] for row in rows_by_name["extraction"]}
    add(
        "VAL2505_02_extraction",
        {"K_V_EXTRACTED_INSIDE_EH", "C_V_EXTRACTED_INSIDE_EH", "DELTA_V_SOURCE_NORM_ZERO_INSIDE_EH", "POISSON_NORMALIZATION_MATCHES"}.issubset(extraction_statuses),
        "EH-to-v coefficient extraction rows are present",
    )

    ppn_statuses = {row["status"] for row in rows_by_name["ppn_readout"]}
    add(
        "VAL2505_03_ppn_readout",
        {"KAPPA_V_ZERO_INSIDE_EH", "BETA_LAW_MATCHES_EH", "FINITE_2PN_READOUT_WARNING_CONDITIONAL_GAUGE_DEBT"}.issubset(ppn_statuses),
        "PPN readout includes beta/kappa pass and 2PN warning",
    )

    guard_statuses = {row["status"] for row in rows_by_name["ownership_guard"]}
    add(
        "VAL2505_04_import_guard",
        "GUARDRAIL_ACTIVE_NO_LOCAL_GR_CLAIM" in guard_statuses and "MTS_PARENT_ACTION_DESCENT_UNSIGNED" in guard_statuses,
        "GR-import guard blocks promotion to MTS-owned local GR",
    )

    residuals = rows_by_name["residual_rows"]
    has_conditional_values = all(
        any(row["symbol"] == symbol and row["value"] == value for row in residuals)
        for symbol, value in (("K_v", "c^4/(32*pi*G_ref)"), ("C_v", "1/2"), ("delta_v_source_norm", "0"), ("kappa_v", "0"), ("beta", "1"))
    )
    has_blockers = all(
        any(row["value"] == value for row in residuals)
        for value in ("MISSING_PARENT_FIXED_POINT_DESCENT", "MISSING_HAMILTONIAN_PIM_IDENTITY", "MISSING_ZERO_BOUNDARY_FLUX", "MISSING_X_SECTOR_DOUBLE_ZERO")
    )
    add("VAL2505_05_residual_rows", has_conditional_values and has_blockers, "conditional coefficients and missing parent blockers both represented")

    add("VAL2505_06_no_claim_flags", no_claim_flags(rows_by_name), "all generated rows keep valid_for_claim=false and claim_allowed=false")
    add("VAL2505_07_next_target", any(row["route_id"] == "NEXT2505_0_selected" for row in rows_by_name["next_target"]), "2506 parent descent/source glue target selected")
    add("VAL2505_08_branch_copies", all(row["copied"] for row in rows_by_name["branch_copies"]), "branch copies were written")

    formalization_artifacts: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*2505*", "*P8_Y5_NO_SHADOW_2505*", "*JR2505*"):
            formalization_artifacts.extend(path for path in FORMALIZATION.rglob(pattern) if path.is_file())
    add("VAL2505_09_no_formalization_artifacts", not formalization_artifacts, "no 2505 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for path in OUTPUTS.values():
        if path == OUTPUTS["validation"]:
            continue
        parsed, count, detail = csv_rows_parse(path)
        add(f"VAL2505_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", detail)

    for key, path in BRANCH_COPIES.items():
        parsed, count, detail = csv_rows_parse(path)
        add(f"VAL2505_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", detail)

    remove_pycache()
    add("VAL2505_10_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts pycache removed")

    overall = all(row["status"] == "PASS" for row in validations)
    add(
        "VAL2505_OVERALL",
        overall,
        "2505 live-ports EH-to-v coefficients, preserves GR-import guard, and selects parent EH descent/source glue next",
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2505 Y5 R2FR EH Fixed Point To V Action Coefficient Extraction Or GR Import Demotion

## Current Verdict

2505 is a useful step forward, but not a local-GR claim.

The coefficient extraction is clean **inside the EH fixed point**:

`L_Phi = -(8*pi*G_ref)^-1 |grad Phi_N|^2 - rho Phi_N`,

with `Phi_N = c^2 v/2`, gives:

`L_v = -c^4/(32*pi*G_ref)|grad v|^2 - rho c^2 v/2`.

Therefore:

`K_v = c^4/(32*pi*G_ref)`,

`C_v = 1/2`,

`delta_v_source_norm = C_v c^4/(16*pi*G_ref K_v)-1 = 0`.

The lapse/PPN extraction also works inside EH:

`v=log(A_iso)=-2x+0*x^2-x^3/6+O(x^4)`, so `kappa_v=0`, `beta=1`, and `gamma=1` at first PPN order.

But the current MTS branch does **not** own those coefficients yet. It still needs one parent package to sign the EH fixed point, PiM/Hilbert source equality, source measure glue, zero boundary/reference flux, extra-sector double zeros, and radial/coframe readout ownership.

So the honest label is: **conditional EH inheritance; MTS ownership blocked**.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "source_pass", "role", "valid_for_claim"])}

## EH To V Extraction

{md_table(rows_by_name["extraction"], ["extraction_id", "object", "equation", "status", "result", "claim_grade", "valid_for_claim"])}

## PPN Readout Vector

{md_table(rows_by_name["ppn_readout"], ["ppn_id", "object", "equation", "status", "result", "valid_for_claim"])}

## GR Import Guard

{md_table(rows_by_name["ownership_guard"], ["guard_id", "gate", "statement", "status", "implication", "valid_for_claim"])}

## Residual Rows

{md_table(rows_by_name["residual_rows"], ["row_id", "symbol", "definition", "value", "status", "units", "observable_link", "score_ready", "blocker_class", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["check_id", "status", "notes", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "extraction": extraction_rows(),
        "ppn_readout": ppn_readout_rows(),
        "ownership_guard": ownership_guard_rows(),
        "residual_rows": residual_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
