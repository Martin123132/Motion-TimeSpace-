from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2189"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2189-Y5-R2FR-parent-extra-sector-inventory-and-coupling-map-or-leakage-bounds.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2189_SOURCE_REGISTER.csv",
    "inventory": OUT / "P8_Y5_PARENT_QLOC_2189_EXTRA_SECTOR_COUPLING_INVENTORY.csv",
    "double_zero_matrix": OUT / "P8_Y5_PARENT_QLOC_2189_DOUBLE_ZERO_STATUS_MATRIX.csv",
    "residual_rows": OUT / "P8_Y5_PARENT_QLOC_2189_LEAKAGE_RESIDUAL_ROWS.csv",
    "priority": OUT / "P8_Y5_PARENT_QLOC_2189_PRIORITY_RANKING.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2189_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2189_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2189_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2189_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2189_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2189_EXTRA_SECTOR_COUPLING_INVENTORY_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2189_LEAKAGE_RESIDUALS_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_EXTRA_SECTOR_INVENTORY_2189_NONCLAIM.csv",
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
            values.append(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2189_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2189-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2189*",
        "*P8_Y5_BRR545_2189*",
        "*Y5_R2FR_parent_extra_sector_inventory_and_coupling_map_or_leakage_bounds_2189*",
        "*JR2189*",
        "*PARENT_EXTRA_SECTOR_INVENTORY_2189*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2188_handoff",
            ROOT / "2188-Y5-R2FR-extra-sector-double-zero-and-PiM-lock-signature-or-residual-fill.md",
            ["NEXT2188_0_2189", "actual C_i/O_i inventory", "VAL2188_OVERALL"],
            "2188 demands an actual C_i/O_i inventory rather than another generic double-zero theorem.",
        ),
        (
            "1009_sector_contract",
            ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            ["PCS1009_4_Gamma_Khat_extra", "PCS1009_5_domain_projector_selector", "PCS1009_7_memory_response_doublet"],
            "1009 lists the dangerous non-EH sectors and names Gamma/Khat/q_loc as the hard block.",
        ),
        (
            "1010_GK_gate",
            ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            ["GKT1010_4_double_zero", "MISSING_PARENT_SIGNED_DOUBLE_ZERO_CERTIFICATE", "RETAIN_Q_LOC_AS_EXPLICIT_RESIDUAL"],
            "1010 gives the action/metric-response/Helmholtz/Euler/double-zero requirements for q_loc.",
        ),
        (
            "symbol_action_map",
            OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            ["Gamma_eff", "q_loc", "Pi_M"],
            "symbol-to-action placement map identifies local readout/projector dangerous variables.",
        ),
        (
            "response_doublet_contract",
            OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            ["response", "doublet"],
            "response doublet route supplies a candidate mechanism for even/double-zero memory response.",
        ),
        (
            "pim_projector_contract",
            OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            ["Pi_M", "projector"],
            "PiM projector algebra gives the mass-projector residual family and commutator problem.",
        ),
        (
            "species_contract",
            OUT / "P8_no_species_source_charge_CONTRACT.csv",
            ["species", "source"],
            "species/source contract defines the WEP/composition leakage clauses.",
        ),
        (
            "constant_kappa",
            OUT / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv",
            ["kappa", "constant"],
            "constant-kappa theorem is a conditional local-G drift repair route, not a full local-GR proof.",
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


def inventory_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EI2189_0_GK",
            "Gamma/Khat/q_loc",
            "C_GK(Phi)",
            "O_GK = metric-response stress built from Gamma_eff and K_hat",
            "Gamma_eff;K_hat;q_loc^nu;P_loc",
            "direct PPN/local force residual and source-normalization leakage",
            "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "HARD_BLOCK_DERIVATION_FIRST",
            "T_GK(Phi0)=0",
            "partial_A T_GK(Phi0)=0",
            "S_GK positive/Helmholtz/Euler closure",
            "theta_GK/Q_GK no-flux",
            "epsilon_C0_GammaKhat;epsilon_dC_GammaKhat;q_loc^nu",
            "PPN;R10;local_GR",
            "take as 2190 first target",
        ),
        (
            "EI2189_1_response_memory",
            "response/memory doublet",
            "C_mem(Z)",
            "O_mem = even response density / memory stress",
            "R_+^A;R_-^A;Z^A;memory variables",
            "compact-local memory hair, clock drift, source normalization, PPN leakage",
            "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "CANDIDATE_NOT_MATCHED_TO_PHYSICAL_LOCK",
            "Gamma_eff even/background-subtracted",
            "odd/linear response source zero",
            "positive Z operator",
            "boundary no-flux still open",
            "epsilon_C0_memory_response;epsilon_dC_memory_response",
            "clocks;PPN;orbital;cosmology_transition",
            "map doublet components to physical q_loc/PPN residual vector",
        ),
        (
            "EI2189_2_domain_projector",
            "domain/projector selector",
            "C_D(Phi)",
            "O_D = selector/projector stress and preferred-frame load",
            "u;h;X;Qcoh;chi_D;lambda_D;P_loc",
            "preferred-frame PPN, WEP/source selection, local/cosmology branch switching",
            "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "PARTIAL_CLAUSE_NOT_PARENT_CLOSED",
            "local selector stress zero",
            "selector derivative/commutator zero",
            "domain operator positive or topological",
            "domain boundary no-flux missing",
            "epsilon_domain_projector_stress;P_loc_commutator",
            "PPN_alpha_i;WEP;local_GR",
            "derive P_loc/domain before readout or keep explicit residual",
        ),
        (
            "EI2189_3_metric_readout",
            "metric/readout protection",
            "D_A g_readout|Phi0",
            "O_readout = metric/coframe perturbation seen by clocks, rods and light",
            "g_obs;g_readout;e_obs;radial/angle gauge",
            "PPN beta/gamma/light-time/orbital mismatch even if source charge works",
            "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "READOUT_PROTECTION_OPEN",
            "g_readout(Phi0)=g_obs",
            "D_A g_readout(Phi0)=0",
            "not a bulk gap; readout functional lock",
            "radial/angle boundary coframe owner open",
            "epsilon_readout_gauge_owner;epsilon_metric_readout_linear",
            "2PN;PPN;light_time;orbital",
            "link to 2187 areal/isotropic parent readout owner",
        ),
        (
            "EI2189_4_PiM",
            "PiM/source-measure projector",
            "Pi_M(Phi)-Pi_EH",
            "O_PiM = Hamiltonian mass-current projector and source charge",
            "Pi_M;J_H;omega_M;Sigma_ext;M_H_ref",
            "Newton source normalization, R10/R11 alpha rows, measured GM calibration",
            "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "PARALLEL_BLOCKER_NOT_PARENT_DERIVED",
            "Pi_M(Phi0)=Pi_EH",
            "partial_A Pi_M(Phi0)=0",
            "projector Ward/Euler closure",
            "I_commutator/R_eq/B_zero no-flux open",
            "epsilon_PiM_value;epsilon_DPiM;I_commutator;R_eq_integral",
            "Newton;R10;R11;PPN",
            "keep parallel with GK; do not absorb into measured G",
        ),
        (
            "EI2189_5_species",
            "universal matter/species source",
            "partial_A ln m_species(Phi0)",
            "O_species = matter/source charge slope and composition current",
            "psi_A;e_obs;theta_A;J_univ",
            "WEP, clock composition, source mass split",
            "P8_no_species_source_charge_CONTRACT.csv",
            "UNIVERSALITY_OPEN",
            "species constants source-blind",
            "partial_A species/source charges zero",
            "matter factorization through e_obs",
            "bulk/boundary composition charge zero open",
            "epsilon_species_coupling;eta_source_AB",
            "WEP;clocks;source_mass",
            "derive species-blind matter action or source WEP residuals",
        ),
        (
            "EI2189_6_boundary",
            "boundary/reference/exact/topological",
            "C_B(Phi)",
            "O_B = theta_boundary, Q_tau_boundary, exact/topological improvement",
            "B_ref;Q_tau;theta;edge classes;counterterms",
            "hidden mass flux, reference drift, PPN/source-charge shift",
            "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "BOUNDARY_ZERO_OPEN",
            "fixed reference or zero extra boundary term",
            "boundary derivative silent",
            "not applicable unless edge dynamics exist",
            "compact linking-sphere flux zero open",
            "epsilon_boundary_reference_zero;B_zero_flux",
            "Newton;PPN;R10;R11",
            "derive fixed-before-readout boundary/reference class",
        ),
        (
            "EI2189_7_kappa",
            "kappa_eff/G_eff topological sector",
            "D_A kappa_eff",
            "O_kappa = local Newton coupling / EH normalization",
            "kappa_eff;A_3;G_eff",
            "Gdot, radial G drift, source normalization",
            "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv",
            "CONDITIONAL_SUPERSELECTION_NOT_ADOPTED_HERE",
            "d kappa_eff=0 on connected local domains",
            "no species/range/frame/domain labels",
            "topological zero-form/three-form pair",
            "boundary level convention open",
            "epsilon_kappa_drift;epsilon_G_eff_source",
            "Gdot;Newton;PPN",
            "adopt or demote kappa topological sector explicitly",
        ),
        (
            "EI2189_8_transition",
            "local/cosmology transition activation",
            "A_tr(Phi,source_scale)",
            "O_tr = activation/suppression functional between compact local and cosmological branches",
            "ell_tr;L_cg;source scale;operator spectrum",
            "hand switching between GR local branch and MTS galaxy/cosmology branch",
            "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            "TRANSITION_CONTROL_OPEN",
            "A_tr local compact limit zero",
            "derivative zero below compact activation threshold",
            "derived from spectrum/source scale",
            "boundary/domain transition flux open",
            "epsilon_transition_leak;ell_tr_over_Lcg",
            "local_GR;galaxies;cosmology",
            "derive activation scale from operator spectrum, not a fit knob",
        ),
        (
            "EI2189_9_worldtube_source",
            "worldtube/source glue",
            "C_W(Phi)",
            "O_W = Hilbert current/topological current/worldtube charge equality",
            "W_source;J_H;J_M_top;B_zero;R_eq",
            "conserved wrong object, measured source mass mismatch",
            "2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md",
            "SOURCE_GLUE_OPEN",
            "same Hilbert source class",
            "R_eq derivative/annulus variation zero",
            "source current Ward/Euler closure",
            "B_zero flux zero open",
            "R_eq_integral;B_zero_flux;epsilon_M",
            "Newton;R10;R11;source_mass",
            "keep as parallel source-measure gate after GK/PiM",
        ),
    ]
    return [
        base_row(
            sector_id=sector_id,
            parent_sector=parent_sector,
            coupling_symbol=coupling_symbol,
            operator_symbol=operator_symbol,
            fields=fields,
            local_effect=local_effect,
            evidence_source=evidence_source,
            classification=classification,
            C0_test=C0_test,
            dC_test=dC_test,
            gap_or_closure_test=gap_or_closure_test,
            boundary_test=boundary_test,
            residual_symbols=residual_symbols,
            observable_link=observable_link,
            next_action=next_action,
        )
        for (
            sector_id,
            parent_sector,
            coupling_symbol,
            operator_symbol,
            fields,
            local_effect,
            evidence_source,
            classification,
            C0_test,
            dC_test,
            gap_or_closure_test,
            boundary_test,
            residual_symbols,
            observable_link,
            next_action,
        ) in rows
    ]


def double_zero_matrix_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    status_by_sector = {
        "EI2189_0_GK": ("not_signed", "not_signed", "not_signed", "not_signed", "highest"),
        "EI2189_1_response_memory": ("candidate_only", "candidate_only", "candidate_only", "open", "high"),
        "EI2189_2_domain_projector": ("open", "open", "open", "open", "high"),
        "EI2189_3_metric_readout": ("open", "open", "readout_lock_not_gap", "open", "high"),
        "EI2189_4_PiM": ("not_signed", "not_signed", "Ward_or_Euler_open", "open", "highest_parallel"),
        "EI2189_5_species": ("open", "open", "matter_factorization_open", "open", "medium_high"),
        "EI2189_6_boundary": ("open", "open", "fixed_reference_open", "open", "medium_high"),
        "EI2189_7_kappa": ("conditional", "conditional", "topological_candidate", "open", "medium"),
        "EI2189_8_transition": ("open", "open", "operator_spectrum_open", "open", "medium"),
        "EI2189_9_worldtube_source": ("open", "open", "Ward_or_topology_open", "open", "high_parallel"),
    }
    rows = []
    for row in inventory:
        c0_status, dc_status, gap_status, boundary_status, priority = status_by_sector[row["sector_id"]]
        rows.append(
            base_row(
                sector_id=row["sector_id"],
                parent_sector=row["parent_sector"],
                C0_status=c0_status,
                dC_status=dc_status,
                gap_or_closure_status=gap_status,
                boundary_status=boundary_status,
                priority=priority,
                promotion_status="not_promoted",
                reason="inventory row is current evidence only; no full parent signature with source/equation path is present",
            )
        )
    return rows


def residual_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in inventory:
        rows.append(
            base_row(
                row_id=row["sector_id"].replace("EI", "LR"),
                symbol=row["residual_symbols"],
                definition=f"nonclaim residual family for {row['parent_sector']}: {row['local_effect']}",
                value="MISSING_COMPONENT_INPUTS",
                status=f"MISSING_PARENT_SIGNATURE_{row['classification']}",
                units="dimensionless_or_declared_per_sector",
                observable_link=row["observable_link"],
                source_path="MISSING_SOURCE_PATH",
                score_ready=False,
            )
        )
    rows.append(
        base_row(
            row_id="LR2189_TOTAL",
            symbol="Delta_local_GR_extra_inventory_abs",
            definition="absolute no-cancellation envelope over all inventoried extra-sector leakage residual families",
            value="MISSING_COMPONENT_INPUTS",
            status="MISSING_SECTOR_COMPONENT_INPUTS",
            units="dimensionless_or_declared",
            observable_link="local_GR;Newton;PPN;WEP;R10;R11",
            source_path="MISSING_SOURCE_PATH",
            score_ready=False,
        )
    )
    return rows


def priority_rows() -> list[dict[str, Any]]:
    specs = [
        ("PR2189_0_GK", 1, "Gamma/Khat/q_loc", "direct local force/PPN residual; 1009 and 1010 already identify it as the hard block", "2190 derive C_GK double-zero or lock q_loc residual"),
        ("PR2189_1_PiM", 2, "PiM/source-measure", "even a solved force residual fails Newton if measured GM projector is unowned", "keep parallel but do not absorb into G"),
        ("PR2189_2_domain_readout", 3, "domain/projector plus metric readout", "prevents branch-switching and 2PN/PPN readout leakage", "derive P_loc/readout owner after GK route"),
        ("PR2189_3_response", 4, "response/memory doublet", "possible mechanism for double-zero, but not yet mapped to physical q_loc/PPN vector", "map components only after GK target is explicit"),
        ("PR2189_4_boundary_source", 5, "boundary/worldtube/species/kappa/transition", "important parallel residuals, but less surgical than GK for immediate local-GR survival", "retain as ledger; source or derive in later gates"),
    ]
    return [
        base_row(priority_id=priority_id, rank=rank, target=target, rationale=rationale, next_action=next_action)
        for priority_id, rank, target, rationale, next_action in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2189_0_inventory", "current extra-sector coupling inventory exists", "PASS_GUARDRAIL", "known local leakage suspects are now explicit rows"),
        ("CG2189_1_coverage", "inventory is complete enough for local-GR claim", "BLOCKED_NONCLAIM", "this is a current-evidence inventory, not a proof that the whole corpus has no other operators"),
        ("CG2189_2_double_zero", "each inventoried C_i has parent-signed C0 and dC zero", "BLOCKED_NONCLAIM", "no inventoried sector has a full parent-signed double-zero certificate"),
        ("CG2189_3_gap_boundary", "each sector has positive gap/closure and boundary silence", "BLOCKED_NONCLAIM", "gap, Ward/Euler, readout and boundary clauses remain open"),
        ("CG2189_4_PiM", "PiM/source-measure parallel blocker is closed", "BLOCKED_NONCLAIM", "PiM value/derivative/commutator/stress/equality locks remain live"),
        ("CG2189_5_local_GR", "full local-GR reduction can be claimed", "BLOCKED_NONCLAIM", "inventory improves targeting but does not close descent"),
        ("CG2189_6_GitHub", "public/github update is triggered", "BLOCKED_NONCLAIM", "private goal work only; no GitHub action"),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2189_0_gain",
            "COUPLING_INVENTORY_WRITTEN",
            "The generic 2188 theorem now has concrete sector rows: GK/q_loc, response, domain/projector, readout, PiM, species, boundary, kappa, transition, and worldtube/source glue.",
            "selected",
        ),
        (
            "DEC2189_1_limit",
            "NO_FULL_DOUBLE_ZERO_PROMOTION",
            "No inventoried sector currently carries a full parent-signed C_i(Phi0)=0, partial_A C_i(Phi0)=0, positive closure, and boundary silence proof.",
            "selected",
        ),
        (
            "DEC2189_2_best_route",
            "GAMMA_KHAT_QLOC_FIRST",
            "GK/q_loc is the most surgical next leap because it directly decides whether the local residual is a variational on-shell zero or an explicit residual.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2189_0_2190",
            selection_status="selected",
            target_file="2190-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
            target_script="scripts/Y5_R2FR_GammaKhat_q_loc_coupling_double_zero_or_residual_lock_2190.py",
            objective="take the EI2189_0 Gamma/Khat/q_loc sector and either derive its parent action, metric response, Helmholtz/Euler closure, T_GK(Phi0)=0, partial_A T_GK(Phi0)=0, P_loc and boundary silence, or lock q_loc as an explicit local-test residual",
            success_condition="C_GK/T_GK double-zero is parent-signed with source equations, or q_loc residual rows become the official local PPN/R10 interface with no theorem-zero claim",
            do_not_do="do not repeat a generic double-zero theorem, do not use plateau silence, do not claim q_loc=0 without metric-response and Helmholtz/Euler proof, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2189_1_parallel_PiM",
            selection_status="held_parallel",
            target_file="2190b-Y5-R2FR-PiM-source-measure-lock-or-residual-interface.md",
            target_script="scripts/Y5_R2FR_PiM_source_measure_lock_or_residual_interface_2190b.py",
            objective="parallel route for PiM/source measure if GK route stalls: value lock, derivative silence, commutator, projector stress, R_eq and B_zero rows",
            success_condition="PiM lock is parent-signed or all source-measure residuals are explicit nonclaim rows with units and normalizations",
            do_not_do="do not absorb source-measure mismatch into measured G",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["inventory"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["residual_rows"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["double_zero_matrix"], BRANCH_COPIES["source_weight"]),
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
    sources = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2189_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist"))
    validations.append(base_row(validation_id="VAL2189_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found"))

    sectors = {row["parent_sector"] for row in rows_by_name["inventory"]}
    required = {"Gamma/Khat/q_loc", "response/memory doublet", "domain/projector selector", "metric/readout protection", "PiM/source-measure projector", "universal matter/species source", "boundary/reference/exact/topological", "kappa_eff/G_eff topological sector", "local/cosmology transition activation", "worldtube/source glue"}
    validations.append(base_row(validation_id="VAL2189_02_inventory_coverage", status="PASS" if required.issubset(sectors) else "FAIL", detail=f"inventory rows={len(rows_by_name['inventory'])}; required sectors covered={len(required.intersection(sectors))}/{len(required)}"))

    matrix = rows_by_name["double_zero_matrix"]
    no_promoted = all(row["promotion_status"] == "not_promoted" for row in matrix)
    validations.append(base_row(validation_id="VAL2189_03_no_double_zero_promotion", status="PASS" if no_promoted else "FAIL", detail="all inventory rows remain not_promoted/nonclaim"))

    residuals = rows_by_name["residual_rows"]
    residual_pass = any(row["symbol"] == "Delta_local_GR_extra_inventory_abs" for row in residuals) and all(str(row["source_path"]).startswith("MISSING_") for row in residuals)
    validations.append(base_row(validation_id="VAL2189_04_residual_rows", status="PASS" if residual_pass else "FAIL", detail=f"residual rows={len(residuals)} remain missing/source-free/nonclaim"))

    priority = rows_by_name["priority"]
    validations.append(base_row(validation_id="VAL2189_05_priority", status="PASS" if priority and priority[0]["target"] == "Gamma/Khat/q_loc" else "FAIL", detail="Gamma/Khat/q_loc selected as first derivation target"))

    gate_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2189_06_claim_gate", status="PASS" if "PASS_GUARDRAIL" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses else "FAIL", detail="inventory is a guardrail, not a local-GR claim"))

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2189_07_decision", status="PASS" if "GAMMA_KHAT_QLOC_FIRST" in decisions else "FAIL", detail="decision selects GK/q_loc as the next non-circling derivation target"))

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2189_08_next_target", status="PASS" if "NEXT2189_0_2190" in routes else "FAIL", detail="2190 GK/q_loc double-zero or residual-lock target selected"))

    validations.append(base_row(validation_id="VAL2189_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2189_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2189_11_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    validations.append(base_row(validation_id="VAL2189_12_formalization_clean", status="PASS" if not formalization_has_2189_artifacts() else "FAIL", detail="formalization-workbench has no 2189 artifacts"))

    remove_pycache()
    validations.append(base_row(validation_id="VAL2189_13_pycache_absent", status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2189_OVERALL", status=overall, detail="2189 inventories the current extra-sector coupling suspects and selects GK/q_loc as the next derivation target without local-GR promotion"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        "# 2189 - Y5/R2FR Parent Extra-Sector Inventory And Coupling Map Or Leakage Bounds",
        "",
        "## Current Verdict",
        "",
        "2189 prevents the project from circling the same generic double-zero theorem. The known local-GR leakage suspects are now explicit coupling-map rows.",
        "",
        "The harsh readout is: no sector is promoted. The good readout is: the problem is now targeted. `Gamma/Khat/q_loc` is the next best leap because it directly decides whether the local residual is a variational on-shell zero or a live PPN/R10 residual.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Extra-Sector Coupling Inventory",
        "",
        md_table(rows_by_name["inventory"], ["sector_id", "parent_sector", "coupling_symbol", "operator_symbol", "fields", "local_effect", "classification", "C0_test", "dC_test", "gap_or_closure_test", "boundary_test", "residual_symbols", "observable_link", "next_action", "valid_for_claim"]),
        "",
        "## Double-Zero Status Matrix",
        "",
        md_table(rows_by_name["double_zero_matrix"], ["sector_id", "parent_sector", "C0_status", "dC_status", "gap_or_closure_status", "boundary_status", "priority", "promotion_status", "reason", "valid_for_claim"]),
        "",
        "## Leakage Residual Rows",
        "",
        md_table(rows_by_name["residual_rows"], ["row_id", "symbol", "definition", "value", "status", "units", "observable_link", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Priority Ranking",
        "",
        md_table(rows_by_name["priority"], ["priority_id", "rank", "target", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Interpretation",
        "",
        "This checkpoint says: do not keep proving `if all C_i double-zero then F1=0`. That is done. The real work now is to take one row at a time and either parent-sign it or turn it into a test residual.",
        "",
        "Best next move: `Gamma/Khat/q_loc` first, PiM/source-measure in parallel. That is the shortest route toward a real derived local-GR branch rather than a closure axiom.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = inventory_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "inventory": inventory,
        "double_zero_matrix": double_zero_matrix_rows(inventory),
        "residual_rows": residual_rows(inventory),
        "priority": priority_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])

    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")
    remove_pycache()


if __name__ == "__main__":
    main()
