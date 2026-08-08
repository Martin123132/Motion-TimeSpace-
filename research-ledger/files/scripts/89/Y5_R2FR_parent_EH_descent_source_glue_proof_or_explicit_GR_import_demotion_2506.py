from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_EH_DESCENT_SOURCE_GLUE_2506"
CHECKPOINT_ID = "2506"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"

DOC = ROOT / "2506-Y5-R2FR-parent-EH-descent-source-glue-proof-or-explicit-GR-import-demotion.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2506_SOURCE_REGISTER.csv",
    "conditional_theorem": OUT / "P8_Y5_NO_SHADOW_2506_CONDITIONAL_EH_DESCENT_THEOREM.csv",
    "live_signature_audit": OUT / "P8_Y5_NO_SHADOW_2506_LIVE_PARENT_SIGNATURE_AUDIT.csv",
    "source_glue_contract": OUT / "P8_Y5_NO_SHADOW_2506_SOURCE_GLUE_CONTRACT.csv",
    "residual_interface": OUT / "P8_Y5_NO_SHADOW_2506_GR_IMPORT_RESIDUAL_INTERFACE.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2506_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2506_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2506_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2506_VALIDATION.csv",
}

BRANCH_COPIES = {
    "conditional_theorem": LOCAL_BOUNDS / "Parent_EH_descent_conditional_theorem_2506_NONCLAIM.csv",
    "source_glue_contract": LOCAL_BOUNDS / "Source_glue_contract_2506_NONCLAIM.csv",
    "residual_interface": QUEUE / "JR2506_GR_IMPORT_RESIDUAL_INTERFACE_NONCLAIM.csv",
    "next_target": QUEUE / "JR2506_PARENT_SIGNATURE_SYNTHESIS_NEXT.csv",
    "live_signature_audit": BETA_DOCS / "Live_parent_signature_audit_2506_NONCLAIM.csv",
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
            "SRC2506_00_2505_handoff",
            ROOT / "2505-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
            ["NEXT2505_0_selected", "parent EH descent/source glue", "VAL2505_OVERALL"],
            "2505 selects parent EH descent/source glue or GR-import demotion as the next target.",
        ),
        (
            "SRC2506_01_2505_validation",
            OUT / "P8_Y5_BRR545_2505_VALIDATION.csv",
            ["VAL2505_OVERALL", "PASS"],
            "2505 validation passed before 2506 continues the private chain.",
        ),
        (
            "SRC2506_02_2505_guard",
            OUT / "P8_Y5_NO_SHADOW_2505_GR_IMPORT_GUARD.csv",
            ["GUARD2505_1_parent_action", "MTS_PARENT_ACTION_DESCENT_UNSIGNED", "GUARD2505_4_import_guard"],
            "2505 guard says coefficients are EH-derived but not yet MTS-owned.",
        ),
        (
            "SRC2506_03_2504_contract",
            OUT / "P8_Y5_NO_SHADOW_2504_MINIMAL_PARENT_ACTION_CHARGE_CONTRACT.csv",
            ["PAC2504_7_current_verdict", "COHERENT_CONTRACT_CURRENT_CLAIM_FAILS"],
            "2504 gives the parent-action clauses that must be signed.",
        ),
        (
            "SRC2506_04_2504_noether",
            OUT / "P8_Y5_NO_SHADOW_2504_NOETHER_HAMILTONIAN_CHARGE_CHAIN.csv",
            ["NHC2504_4_PiM_identification", "CORE_MISSING_IDENTITY_NOT_DERIVED"],
            "2504 identifies PiM/Hilbert/Hamiltonian equality as the source-glue obstruction.",
        ),
        (
            "SRC2506_05_2503_worldtube",
            ROOT / "2503-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R-eq-fill.md",
            ["WHS2503_6_current_verdict", "BZF2503_4_current_verdict", "VAL2503_OVERALL"],
            "2503 proves the selector route is clean conditionally but leaves source and boundary signatures unsigned.",
        ),
        (
            "SRC2506_06_2186_descent",
            ROOT / "2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md",
            ["DEG2186_7_verdict", "RGC2186_5_resolution", "VAL2186_OVERALL"],
            "2186 resolves the 2PN issue as readout debt but keeps EH descent unsigned.",
        ),
        (
            "SRC2506_07_local_blocks",
            OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            ["A511_0_EH_core", "A511_2_universal_matter", "A511_6_metric_readout"],
            "Minimal local-GR action blocks give the EH, matter, boundary and readout ingredients.",
        ),
        (
            "SRC2506_08_fixed_point_conditions",
            OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            ["FP511_1_double_zero_nonEH_coupling", "FP511_5_parent_PiM_lock", "FP511_6_boundary_no_flux"],
            "Fixed-point conditions specify the exact local silence clauses needed for descent.",
        ),
        (
            "SRC2506_09_hamiltonian_source",
            OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            ["HSM541_0_adopt_Hamiltonian_PiM", "HSM541_2_observed_worldtube_source", "HSM541_4_zero_extra_source_channels"],
            "Hamiltonian source contract gives the source-measure and extra-channel lock conditions.",
        ),
        (
            "SRC2506_10_symbol_map",
            OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            ["g_obs / g_readout", "Pi_M", "q_loc^nu"],
            "Symbol map ties MTS objects to local-GR action blocks and residual rows.",
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


def conditional_theorem_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "THM2506_0_parent_split",
            "parent action split",
            "Assume S_parent = S_EH[g_obs,kappa0] + S_matter[psi,g_obs] + S_extra[Xi,g_obs] + S_boundary[g_obs,Xi,B_ref].",
            "conditional premise",
            "This is sufficient only if all non-EH terms are locally silent to first variation.",
            "OPEN_IN_CURRENT_MTS",
        ),
        (
            "THM2506_1_fixed_point",
            "local fixed point",
            "There is a stationary local branch Xi=Xi0 with E_Xi[Xi0]=0 and L_tau Xi0=0.",
            "conditional premise",
            "Extra fields are not allowed to carry local source charge at the exterior fixed point.",
            "OPEN_IN_CURRENT_MTS",
        ),
        (
            "THM2506_2_double_zero",
            "non-EH double zero",
            "For every non-EH metric/source coupling C_i(Xi): C_i(Xi0)=0 and partial_A C_i(Xi0)=0.",
            "conditional premise",
            "Then delta_g S_extra and linear source-normalization drift vanish at the local fixed point.",
            "OPEN_IN_CURRENT_MTS",
        ),
        (
            "THM2506_3_universal_matter",
            "universal observed coframe",
            "All matter species couple to the same g_obs/coframe and not to independent MTS markers at leading local order.",
            "conditional premise",
            "Hilbert stress from S_matter is the same source seen by clocks, orbits and PPN.",
            "OPEN_IN_CURRENT_MTS",
        ),
        (
            "THM2506_4_variation",
            "EH descent variation",
            "On the fixed branch, delta S_parent = delta S_EH[g_obs] + delta S_matter[psi,g_obs] + delta B_silent.",
            "conditional proof step",
            "If delta B_silent=0, the parent Euler equation is the EH equation with the observed matter stress.",
            "CONDITIONAL_PROOF_CLOSED",
        ),
        (
            "THM2506_5_source_glue",
            "Hamiltonian/Hilbert source equality",
            "(4*pi*G_ref)^-1 int_S Pi_M J_H = H_tau[S]-H_tau[reference] = M_Hilbert[S] on the same worldtube.",
            "conditional premise",
            "This identifies the mass in the v-Poisson equation with the measured gravitational source mass.",
            "OPEN_IN_CURRENT_MTS",
        ),
        (
            "THM2506_6_boundary",
            "boundary/reference silence",
            "S_boundary = S_GHY[g_obs] + exact/topological terms whose local variation and charge flux vanish for the chosen reference.",
            "conditional premise",
            "No hidden boundary charge may renormalize G, M, beta, gamma, or the 2PN vector.",
            "OPEN_IN_CURRENT_MTS",
        ),
        (
            "THM2506_7_readout",
            "radial/coframe readout ownership",
            "Parent-owned map relates areal/isotropic/reciprocal readouts so the +1/2 reciprocal 2PN coefficient is gauge/readout debt, not physical hair.",
            "conditional premise",
            "The 2PN warning from 2505 is harmless only after this map is signed.",
            "OPEN_IN_CURRENT_MTS",
        ),
        (
            "THM2506_8_conditional_result",
            "conditional theorem",
            "If THM2506_0 through THM2506_7 hold, MTS inherits EH local equations, Newton/Poisson normalization, beta=gamma=1 at 1PN, and no independent local fifth-force/source channel.",
            "CONDITIONAL_DESCENT_THEOREM_PROVED",
            "The theorem is valid as a sufficient contract, but it is not yet a proof that current MTS satisfies the contract.",
            "VALID_CONDITIONAL_NOT_LIVE_CLAIM",
        ),
    ]
    return [
        base_row(
            theorem_id=theorem_id,
            clause=clause,
            mathematical_statement=statement,
            role=role,
            implication=implication,
            live_status=live_status,
        )
        for theorem_id, clause, statement, role, implication, live_status in specs
    ]


def live_signature_audit_rows() -> list[dict[str, Any]]:
    specs = [
        ("SIG2506_0_parent_action", "single parent action with EH local fixed point", "PAC2504_7_current_verdict", "not_signed", "current corpus has a coherent contract but not a parent-signed action"),
        ("SIG2506_1_double_zero", "extra-sector value and first variation vanish", "FP511_1_double_zero_nonEH_coupling", "required_not_proved", "F_1/double-zero route remains a theorem target, not a derived fact"),
        ("SIG2506_2_universal_matter", "same g_obs/coframe for all matter species", "A511_2_universal_matter", "contract_anchor_not_full_derivation", "universal coupling is required but not yet derived from primitive MTS"),
        ("SIG2506_3_PiM", "PiM equals EH/Hamiltonian/Hilbert mass charge", "NHC2504_4_PiM_identification", "not_derived", "source mass equality is the main local-GR ownership gap"),
        ("SIG2506_4_boundary", "boundary/reference/topological terms have zero local charge flux", "BZF2503_4_current_verdict", "not_derived", "zero boundary flux is still unsigned"),
        ("SIG2506_5_readout", "parent-owned radial/coframe gauge map", "RGC2186_5_resolution", "conditional_not_parent_signed", "2PN mismatch is not fatal but still needs parent readout ownership"),
        ("SIG2506_6_kappa", "constant universal kappa/G on connected local domain", "HSM541_6_constant_universal_G", "contract_not_live_proof", "G drift/source dependence must be killed or bounded"),
        ("SIG2506_7_live_verdict", "live MTS local-GR ownership", "all signatures", "claim_blocked", "2506 proves the sufficient contract, not that live MTS already satisfies it"),
    ]
    return [
        base_row(
            signature_id=signature_id,
            required_signature=required,
            source_anchor=source_anchor,
            current_status=status,
            obstruction=obstruction,
        )
        for signature_id, required, source_anchor, status, obstruction in specs
    ]


def source_glue_contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "GLUE2506_0_same_worldtube",
            "same source worldtube",
            "The worldtube W used for Hilbert stress, Hamiltonian charge and Pi_M projection must be identical up to parent-owned deformation.",
            "prevents using one mass in Newton and another mass in MTS charge language",
            "not_signed",
        ),
        (
            "GLUE2506_1_same_generator",
            "same local time generator",
            "The tau generator in H_tau must be the stationary generator used by local clocks and the weak-field lapse.",
            "prevents hidden clock normalization or preferred-frame leakage",
            "not_signed",
        ),
        (
            "GLUE2506_2_same_metric",
            "same observed metric/coframe",
            "The metric in S_matter, the metric in S_EH, and the readout metric in PPN/orbits are the same g_obs on the fixed branch.",
            "prevents source/readout split and WEP leakage",
            "not_signed",
        ),
        (
            "GLUE2506_3_charge_identity",
            "PiM-Hilbert-Hamiltonian equality",
            "(4*pi*G_ref)^-1 int_S Pi_M J_H = H_tau[S]-H_tau[ref] = int_W T^H_{mu nu} tau^mu n^nu dSigma.",
            "turns the MTS mass projector into the actual measured source mass",
            "not_derived",
        ),
        (
            "GLUE2506_4_no_extra_channels",
            "no independent extra source channel",
            "J_extra, J_boundary, J_memory, J_projector and J_domain either vanish or enter only at second order around Xi0.",
            "kills fifth-force/source-normalization residuals without tuning them case by case",
            "not_derived",
        ),
        (
            "GLUE2506_5_result_if_signed",
            "source glue result",
            "If GLUE2506_0 through GLUE2506_4 are signed, the rho in L_v is the same mass sourcing Newtonian acceleration and PPN observables.",
            "makes the 2505 EH coefficients MTS-owned rather than GR-imported",
            "conditional_only",
        ),
    ]
    return [
        base_row(
            glue_id=glue_id,
            clause=clause,
            mathematical_statement=statement,
            why_it_matters=why,
            live_status=status,
        )
        for glue_id, clause, statement, why, status in specs
    ]


def residual_interface_rows() -> list[dict[str, Any]]:
    specs = [
        ("RI2506_0", "epsilon_EH_descent", "parent action fails to reduce to EH local fixed-point variation", "MISSING_PARENT_ACTION_SIGNATURE", "local_GR;Newton", "core_blocker"),
        ("RI2506_1", "epsilon_double_zero", "non-EH value/first-variation leakage at local fixed point", "MISSING_X_SECTOR_DOUBLE_ZERO_PROOF", "PPN;WEP;R10;clock", "core_blocker"),
        ("RI2506_2", "epsilon_source_glue", "PiM/Hilbert/Hamiltonian source mismatch", "MISSING_PIM_HILBERT_HAMILTONIAN_IDENTITY", "Newton;orbital;PPN", "core_blocker"),
        ("RI2506_3", "epsilon_boundary", "boundary/reference/topological source shift", "MISSING_ZERO_BOUNDARY_FLUX_PROOF", "orbital;PPN;R10", "core_blocker"),
        ("RI2506_4", "epsilon_readout_2PN", "unowned reciprocal/isotropic radial-coframe map", "MISSING_PARENT_READOUT_GAUGE_MAP", "2PN;light_time;perihelion", "finite_residual_until_mapped"),
        ("RI2506_5", "epsilon_kappa", "G/kappa not proven constant/source-blind locally", "MISSING_CONSTANT_UNIVERSAL_KAPPA_PROOF", "Newton;WEP;clock", "core_blocker"),
        ("RI2506_6", "epsilon_GR_import_label", "EH coefficients used before parent signatures are signed", "GR_IMPORT_PLUS_RESIDUAL_INTERFACE", "all_local_tests", "honest_current_label"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            current_value=value,
            observable_link=observable,
            blocker_class=blocker,
            score_ready=False,
            source_path=str(DOC),
        )
        for row_id, symbol, definition, value, observable, blocker in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2506_0_gain",
            "CONDITIONAL_DESCENT_THEOREM_NOW_EXACT",
            "2506 proves the sufficient theorem: if the parent action signs EH descent, universal matter, source glue, boundary silence, double zeros and readout ownership, then the 2505 EH coefficients become MTS-owned.",
            "selected",
        ),
        (
            "DEC2506_1_live_status",
            "LIVE_MTS_OWNERSHIP_NOT_YET_PROVED",
            "The live corpus has contracts for the needed clauses, but the parent signatures remain unsigned; local GR/Newton is therefore not yet claimable.",
            "selected",
        ),
        (
            "DEC2506_2_label",
            "CURRENT_LABEL_IS_GR_IMPORT_PLUS_RESIDUAL_INTERFACE",
            "Until the parent signatures are derived, the honest local branch label is EH/GR import with explicit MTS residual interfaces.",
            "selected",
        ),
        (
            "DEC2506_3_best_next",
            "PARENT_SIGNATURE_SYNTHESIS_NEXT",
            "The next leap is to derive the missing signatures from MTS primitives: quotient naturality, universal source coupling, topological kappa, and no-extra-source/double-zero clauses.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2506_0_selected",
            selection_status="selected",
            target_file="2507-Y5-R2FR-parent-signature-synthesis-quotient-source-glue-or-GR-import-lock.md",
            target_script="scripts/Y5_R2FR_parent_signature_synthesis_quotient_source_glue_or_GR_import_lock_2507.py",
            objective="try to derive the live parent signatures from MTS primitives: quotient naturality of g_obs, universal matter coupling/source-label forgetting, topological kappa constancy, PiM/Hilbert/Hamiltonian charge equality, no-extra-source double zeros, and boundary silence",
            success_condition="at least one currently unsigned clause becomes parent-signed without fitting G or adding a closure axiom; otherwise lock the local branch as explicit GR import plus residual interface",
            do_not_do="do not claim local GR from conditional theorem alone, do not hide unsigned source glue, do not treat a contract as a derivation, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2506_1_parallel_residual_bounds",
            selection_status="held_parallel",
            target_file="2507b-Y5-R2FR-local-GR-residual-interface-bound-pack.md",
            target_script="scripts/Y5_R2FR_local_GR_residual_interface_bound_pack_2507b.py",
            objective="convert the residual interface into explicit bound-ready rows for PPN, WEP, R10, clocks and orbital systems if derivation stalls",
            success_condition="each residual has units, projection, source path, and valid_for_claim=false until numeric/source-backed",
            do_not_do="do not score placeholders or call bound survival a derivation",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("conditional_theorem", OUTPUTS["conditional_theorem"], BRANCH_COPIES["conditional_theorem"]),
        ("source_glue_contract", OUTPUTS["source_glue_contract"], BRANCH_COPIES["source_glue_contract"]),
        ("residual_interface", OUTPUTS["residual_interface"], BRANCH_COPIES["residual_interface"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
        ("live_signature_audit", OUTPUTS["live_signature_audit"], BRANCH_COPIES["live_signature_audit"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=f"COPY2506_{copy_id}", source_path=str(source), target_path=str(target), copied=target.exists()))
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

    add("VAL2506_00_sources_exist", all(row["path_exists"] for row in rows_by_name["source_register"]), "all cited source paths exist")
    add("VAL2506_01_source_needles", all(row["source_pass"] for row in rows_by_name["source_register"]), "all required source needles are present")

    theorem_statuses = {row["live_status"] for row in rows_by_name["conditional_theorem"]}
    add(
        "VAL2506_02_conditional_theorem",
        "VALID_CONDITIONAL_NOT_LIVE_CLAIM" in theorem_statuses and "OPEN_IN_CURRENT_MTS" in theorem_statuses,
        "conditional descent theorem exists but is not a live claim",
    )

    live_statuses = {row["current_status"] for row in rows_by_name["live_signature_audit"]}
    add(
        "VAL2506_03_live_signature_audit",
        "claim_blocked" in live_statuses and "not_derived" in live_statuses,
        "live audit keeps unsigned signatures visible",
    )

    glue_statuses = {row["live_status"] for row in rows_by_name["source_glue_contract"]}
    add(
        "VAL2506_04_source_glue_contract",
        "conditional_only" in glue_statuses and "not_derived" in glue_statuses,
        "source glue contract is explicit and not promoted",
    )

    residual_values = {row["current_value"] for row in rows_by_name["residual_interface"]}
    required_residuals = {
        "MISSING_PARENT_ACTION_SIGNATURE",
        "MISSING_X_SECTOR_DOUBLE_ZERO_PROOF",
        "MISSING_PIM_HILBERT_HAMILTONIAN_IDENTITY",
        "MISSING_ZERO_BOUNDARY_FLUX_PROOF",
        "GR_IMPORT_PLUS_RESIDUAL_INTERFACE",
    }
    add("VAL2506_05_residual_interface", required_residuals.issubset(residual_values), "GR-import residual interface keeps all core blockers")

    decision_text = " ".join(row["decision"] for row in rows_by_name["decision_ledger"])
    add("VAL2506_06_decision", "CURRENT_LABEL_IS_GR_IMPORT_PLUS_RESIDUAL_INTERFACE" in decision_text, "decision ledger gives honest current label")
    add("VAL2506_07_next_target", any(row["route_id"] == "NEXT2506_0_selected" for row in rows_by_name["next_target"]), "2507 signature synthesis target selected")
    add("VAL2506_08_no_claim_flags", no_claim_flags(rows_by_name), "all rows keep valid_for_claim=false and claim_allowed=false")
    add("VAL2506_09_branch_copies", all(row["copied"] for row in rows_by_name["branch_copies"]), "branch copies were written")

    formalization_artifacts: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*2506*", "*P8_Y5_NO_SHADOW_2506*", "*JR2506*"):
            formalization_artifacts.extend(path for path in FORMALIZATION.rglob(pattern) if path.is_file())
    add("VAL2506_10_no_formalization_artifacts", not formalization_artifacts, "no 2506 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for path in OUTPUTS.values():
        if path == OUTPUTS["validation"]:
            continue
        parsed, count, detail = csv_rows_parse(path)
        add(f"VAL2506_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", detail)

    for key, path in BRANCH_COPIES.items():
        parsed, count, detail = csv_rows_parse(path)
        add(f"VAL2506_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", detail)

    remove_pycache()
    add("VAL2506_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts pycache removed")

    overall = all(row["status"] == "PASS" for row in validations)
    add(
        "VAL2506_OVERALL",
        overall,
        "2506 proves the conditional EH-descent/source-glue contract, keeps live MTS nonclaim, and selects parent signature synthesis next",
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2506 Y5 R2FR Parent EH Descent Source Glue Proof Or Explicit GR Import Demotion

## Current Verdict

2506 makes the local-GR bridge sharper, not magically finished.

The good news: there is now an exact **conditional descent theorem**.

If the parent MTS action locally splits into an EH block plus universal matter, and all non-EH channels have double-zero silence at the stationary local fixed point, and the PiM/Hilbert/Hamiltonian source charges are the same object on the same worldtube, and boundary/reference/topological fluxes vanish, then the 2505 EH-to-`v` coefficients become MTS-owned:

`K_v = c^4/(32*pi*G_ref)`, `C_v=1/2`, `delta_v_source_norm=0`, `kappa_v=0`, `beta=1`, and `gamma=1` at first PPN order.

The bad news, or rather the honest engineering news: the current live corpus does **not** yet sign those parent clauses. So the live label remains:

**GR/EH import plus explicit MTS residual interface.**

That is not a collapse. It is the exact lock we need to pick next.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "source_pass", "role", "valid_for_claim"])}

## Conditional EH Descent Theorem

{md_table(rows_by_name["conditional_theorem"], ["theorem_id", "clause", "mathematical_statement", "role", "implication", "live_status", "valid_for_claim"])}

## Live Parent Signature Audit

{md_table(rows_by_name["live_signature_audit"], ["signature_id", "required_signature", "source_anchor", "current_status", "obstruction", "valid_for_claim"])}

## Source Glue Contract

{md_table(rows_by_name["source_glue_contract"], ["glue_id", "clause", "mathematical_statement", "why_it_matters", "live_status", "valid_for_claim"])}

## GR Import Residual Interface

{md_table(rows_by_name["residual_interface"], ["row_id", "symbol", "definition", "current_value", "observable_link", "blocker_class", "score_ready", "valid_for_claim"])}

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
        "conditional_theorem": conditional_theorem_rows(),
        "live_signature_audit": live_signature_audit_rows(),
        "source_glue_contract": source_glue_contract_rows(),
        "residual_interface": residual_interface_rows(),
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
