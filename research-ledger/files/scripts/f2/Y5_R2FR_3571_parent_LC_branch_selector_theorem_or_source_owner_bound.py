from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3571-Y5-R2FR-parent-LC-branch-selector-theorem-or-source-owner-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_PARENT_LC_SELECTOR_3571"
CHECKPOINT_ID = "3571"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def sources() -> dict[str, Path]:
    return {
        "handoff_3570": RESIDUALS / "P8_Y5_R2FR_3570_NEXT_TARGET.csv",
        "selector_3570": RESIDUALS / "P8_Y5_R2FR_3570_AXIAL_BRANCH_SELECTOR_CONTRACT.csv",
        "zero_3570": RESIDUALS / "P8_Y5_R2FR_3570_PARENT_AXIAL_ZERO_CERTIFICATE.csv",
        "status_3570": RESIDUALS / "P8_Y5_R2FR_3570_STATUS.csv",
        "signature_3566": RESIDUALS / "P8_Y5_R2FR_3566_PARENT_LOCAL_LC_ACTION_SIGNATURE.csv",
        "variation_3566": RESIDUALS / "P8_Y5_R2FR_3566_NO_GAMMA_VARIATION_DERIVATION.csv",
        "parent_spine_2416": RESIDUALS / "P8_Y5_PARENT_QLOC_2416_PARENT_ACTION_SIGNATURE_SPINE.csv",
        "local_gr_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "source_owner_contract": RESIDUALS / "P8_source_owner_parent_action_terms_CONTRACT.csv",
        "gamma_matrix_3493": RESIDUALS / "P8_Y5_R2FR_3493_SECTOR_GAMMA_SIGNATURE_MATRIX.csv",
        "gamma_verdict_3565": RESIDUALS / "P8_Y5_R2FR_3565_SECTOR_GAMMA_SLOT_VERDICT.csv",
        "hyper_kernel_3496": RESIDUALS / "P8_Y5_R2FR_3496_SOURCE_HYPERMOMENTUM_KERNEL_VECTOR.csv",
        "slot_audit_2375": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_GAMMA_SLOT_SECTOR_AUDIT.csv",
        "theorem_stack_2375": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_NO_GAMMA_THEOREM_STACK.csv",
        "sector_audit_2415": RESIDUALS / "P8_Y5_PARENT_QLOC_2415_SECTOR_GAMMA_SLOT_AUDIT.csv",
        "gamma_import_2414": RESIDUALS / "P8_Y5_PARENT_QLOC_2414_GAMMA_SLOT_SECTOR_AUDIT_IMPORT.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3570": "declares 3571 target",
        "selector_3570": "imports B_LC selector split",
        "zero_3570": "imports axial zero certificate",
        "status_3570": "imports current missing selector status",
        "signature_3566": "imports branch action signature",
        "variation_3566": "imports no-Gamma variation proofs",
        "parent_spine_2416": "imports parent action signature spine",
        "local_gr_blocks": "imports local GR action block requirements",
        "source_owner_contract": "imports source-owner and boundary contracts",
        "gamma_matrix_3493": "imports sector gamma status matrix",
        "gamma_verdict_3565": "imports sector Gamma verdict",
        "hyper_kernel_3496": "imports source-owner/hypermomentum bound formulas",
        "slot_audit_2375": "imports all-sector Gamma slot audit",
        "theorem_stack_2375": "imports exact conditional no-Gamma theorem",
        "sector_audit_2415": "imports sector audit with proof gaps",
        "gamma_import_2414": "imports older Gamma slot import audit",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def selector_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "BLC3571_0_exact_product_gate",
            "parent LC selector",
            "B_LC_selector = product_s I_s, where I_s=1 only when sector s has no independent Gamma_ind/omega_ind action slot and no downstream source-current reentry.",
            "This is an exact no-cancellation theorem: every sector must be individually zero or explicitly bounded.",
            "DERIVED_PRODUCT_GATE",
            "theorem_stack_2375",
        ),
        (
            "BLC3571_1_variable_absence",
            "sector zero lemma",
            "If Arg(S_s) excludes Gamma_ind, then delta S_s/delta Gamma_ind=0 in the reduced field domain.",
            "This is the mathematical engine behind the LC branch; it is not a fit.",
            "EXACT_MATH",
            "variation_3566",
        ),
        (
            "BLC3571_2_coframe_owned_spin",
            "spin transport lemma",
            "omega_spin=omega_LC[e_obs] routes spin variation through the coframe/Hilbert equation, not an independent torsion equation.",
            "This closes axial torsion only after the parent ordinary branch selects the owned-coframe action.",
            "EXACT_IF_PARENT_SPIN_SIGNATURE_SELECTED",
            "parent_spine_2416",
        ),
        (
            "BLC3571_3_same_frame_EM",
            "Maxwell/Poynting lemma",
            "A_Q,F_Q,*_obs(e_obs) have no affine Gamma slot; Poynting energy belongs in J_H/H_tau or in an explicit collar-flux residual.",
            "This prevents the Poynting vector from being ignored while keeping it out of the axial torsion source.",
            "DERIVED_CONDITIONAL_PUBLIC_HODGE_AND_FLUX_BOUND_OPEN",
            "signature_3566",
        ),
        (
            "BLC3571_4_readout_no_reentry",
            "readout no-reentry lemma",
            "Clock/light/orbit/R10/PPN readouts do not source Gamma if they are downstream functors of solved e_obs,A_Q,J_H,M_H,tau,theta and do not define extra source-labelled currents.",
            "This blocks readout-as-force smuggling; remaining gaps become explicit bound rows.",
            "CONDITIONAL_CONTRACT",
            "theorem_stack_2375",
        ),
        (
            "BLC3571_5_public_selector_result",
            "3571 selector verdict",
            "The parent LC selector is mathematically reduced to a finite product gate, but the public product is not 1 because projector/domain, boundary/source-owner, GM/reference and Poynting/collar clauses are not parent-signed.",
            "This is progress: local-GR closure is now a small leakage ledger rather than an undefined coupling fog.",
            "PARTIAL_THEOREM_PUBLIC_CLAIM_BLOCKED",
            "status_3570",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, claim_piece, statement, derivation, status, source_key in specs
    ]


def sector_product_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("SELP3571_0_matter", "ordinary matter", "I_matter", "S_m[Psi,e_obs,omega_LC[e_obs],A_Q,theta] no Gamma_ind", "CONDITIONAL_SUPPORTED_PRIVATE", "parent action/spurion exclusion still private", "parent_spine_2416"),
        ("SELP3571_1_spin", "spin transport", "I_spin", "omega_spin=omega_LC[e_obs], no torsionful omega_ind", "CONDITIONAL_SUPPORTED_PRIVATE", "metric-affine counterbranch not parent-excluded publicly", "parent_spine_2416"),
        ("SELP3571_2_EM", "EM and Poynting", "I_EM", "A_Q,F_Q,*_obs(e_obs), Poynting included in Hilbert/source charge", "PARTIAL_SUPPORTED", "scalar lambda_A/alpha owner and boundary flux norms open", "signature_3566"),
        ("SELP3571_3_source", "source worldtube/current", "I_source", "J_H[tau]=delta(S_m+S_EM)/delta e_obs and regular support", "PRIVATE_CONDITIONAL", "support/reference/projector and finite-source boundary open", "variation_3566"),
        ("SELP3571_4_projector", "projector/domain", "I_projector", "Pi_M q/e_obs/tau/topology-natural before variation", "LIVE_WEAK_LINK", "delta_Gamma Pi_M operator norm or theorem missing", "hyper_kernel_3496"),
        ("SELP3571_5_clocks", "clock/frequency readout", "I_clock", "downstream matter/gauge/e_obs clock standards", "UNSIGNED_READOUT_SLOT", "clock protocol argument list not parent-signed", "slot_audit_2375"),
        ("SELP3571_6_light", "light/optical readout", "I_light", "metric/public-Hodge ray/detector readout, no affine probe", "PARTIAL_READOUT_SLOT", "Shapiro/ray/detector downstream proof not signed", "slot_audit_2375"),
        ("SELP3571_7_orbit", "orbital/test-body readout", "I_orbit", "metric geodesic/GM transfer downstream of source charge", "UNSIGNED_READOUT_SLOT", "test-body limit and GM transfer not parent-signed", "slot_audit_2375"),
        ("SELP3571_8_boundary", "boundary/source-owner", "I_boundary", "GHY/exact/topological/fixed-reference boundary with no local flux", "LIVE_PRIMARY_LEAK", "boundary flux, H_ref/M_H, owner current not parent-derived", "source_owner_contract"),
        ("SELP3571_9_total", "total selector", "B_LC_selector", "product of all I_s", "FALSE_PUBLICLY_CURRENTLY", "one live leak is enough to keep public selector false", "gamma_verdict_3565"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "sector_gate_id": gate_id,
            "sector": sector,
            "indicator": indicator,
            "zero_condition": condition,
            "current_status": status,
            "open_gap": gap,
            "source_path": str(source_paths[source_key]),
            "parent_signed_public": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, sector, indicator, condition, status, gap, source_key in specs
    ]


def leakage_bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "LEAK3571_0_projector_comm",
            "epsilon_projector_comm",
            "||delta_Gamma Pi_M|| * ||J_H|| / abs(M_H_ref)",
            "dimensionless source-tail envelope",
            "projector/domain/boundary descent certificate or operator norm for delta_Gamma Pi_M",
            "COUNTERMODEL_ACTIVE_BOUND_REQUIRED",
            "hyper_kernel_3496",
        ),
        (
            "LEAK3571_1_boundary_flux",
            "epsilon_boundary_flux",
            "abs(int_partialSigma n_i K_owner^{i0} dS) / abs(M_H_ref)",
            "dimensionless source-tail envelope",
            "boundary class, K_owner current, no shear/vector/radial boundary source theorem or flux norm",
            "BOUND_ROW_FORMULA_DERIVED_INPUTS_MISSING",
            "source_owner_contract",
        ),
        (
            "LEAK3571_2_MHref_reference",
            "epsilon_MHref",
            "abs(delta_Gamma(H_tau-H_ref)) / abs(M_H_ref)",
            "dimensionless reference drift",
            "H_tau, H_ref, N_G, tau, positivity, integrability and reference lock",
            "REFERENCE_LOCK_UNSIGNED",
            "hyper_kernel_3496",
        ),
        (
            "LEAK3571_3_Poynting_worldtube",
            "epsilon_Poynting_worldtube",
            "mu0^-1 ||E_T||_L2(B)||B_T||_L2(B)/abs(M_H_ref) + collar_flux/abs(M_H_ref)",
            "dimensionless EM/source-tail envelope",
            "unit system, E/B norms, boundary measure, collar normal, public-Hodge certificate",
            "PLACED_BUT_INPUT_NORMS_MISSING",
            "hyper_kernel_3496",
        ),
        (
            "LEAK3571_4_GM_transfer",
            "epsilon_GM_transfer",
            "abs(delta_Gamma(G_ref M_H)+delta_cal GM_obs)/abs(G_ref M_H)",
            "dimensionless source calibration leakage",
            "G_ref branch constant, Poisson/Gauss calibration, orbit/GM no-fitted-G guard",
            "GM_TRANSFER_UNSIGNED",
            "hyper_kernel_3496",
        ),
        (
            "LEAK3571_5_total_selector_tail",
            "epsilon_selector_leak",
            "epsilon_projector_comm + epsilon_boundary_flux + epsilon_MHref + epsilon_Poynting_worldtube + epsilon_GM_transfer + clock/light/orbit readout tails",
            "dimensionless parent selector leakage envelope",
            "all component bounds or zero theorems above, in same frame and no-cancellation convention",
            "EXECUTABLE_SYMBOLIC_NONCLAIM",
            "gamma_verdict_3565",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "leak_id": leak_id,
            "symbol": symbol,
            "bound_formula": formula,
            "units": units,
            "required_inputs": required_inputs,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for leak_id, symbol, formula, units, required_inputs, status, source_key in specs
    ]


def activation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3571_0_sources", "source audit", "PASS", "all required 3571 source paths exist"),
        ("GATE3571_1_product_gate", "B_LC product theorem", "PASS_CONDITIONAL", "exact product/no-cancellation selector theorem derived"),
        ("GATE3571_2_matter_spin", "matter/spin clauses", "PASS_PRIVATE_NOT_PUBLIC", "ordinary/coframe spin clauses are written but not public parent selector"),
        ("GATE3571_3_projector", "projector naturality", "FAIL_CURRENT_PUBLIC_CLAIM", "delta_Gamma Pi_M theorem/operator norm missing"),
        ("GATE3571_4_boundary_source_owner", "boundary/source-owner", "FAIL_CURRENT_PUBLIC_CLAIM", "boundary flux, H_ref/M_H and owner current not parent-derived"),
        ("GATE3571_5_poynting_flux", "Poynting/collar flux", "FAIL_NUMERIC_BOUND_READY_ONLY", "formula retained; E/B/collar norms missing"),
        ("GATE3571_6_public_BLC", "public B_LC_selector", "FAIL_CURRENT_PUBLIC_CLAIM", "product gate has live non-signed factors"),
        ("GATE3571_7_axial_consequence", "axial C_A=0 public consequence", "FAIL_CURRENT_PUBLIC_CLAIM", "axial zero remains private until B_LC is public or leaks are bounded"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths["status_3570"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3571_0_selector_reduction",
            "treat B_LC as a finite product gate",
            "This prevents hidden cancellations and identifies exactly which sectors still block public local GR.",
            "future work attacks named leak rows instead of restarting the torsion discussion",
            "ADOPTED",
            "theorem_stack_2375",
        ),
        (
            "DEC3571_1_poynting_kept",
            "keep Poynting as source-owner/boundary flux, not axial torsion",
            "The Poynting vector is real source energy, but in the same-frame Maxwell branch it enters Hilbert/Noether charge or a collar-flux residual.",
            "EM stress remains in the GR source route while its boundary leakage gets a bound formula",
            "ADOPTED",
            "hyper_kernel_3496",
        ),
        (
            "DEC3571_2_next_target",
            "attack projector naturality first",
            "Projector/domain reentry is the sharpest single weak link: if Pi_M is q/e_obs/tau-natural, one major source-owner leak collapses.",
            "3572 should try to prove delta_Gamma Pi_M=0 or source its operator norm",
            "NEXT_TARGET_SELECTED",
            "signature_3566",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "valid_for_claim": False,
        }
        for decision_id, decision, reason, consequence, status, source_key in specs
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "BLC_SELECTOR_REDUCED_TO_PRODUCT_GATE_AND_LEAKAGE_BOUND_LEDGER",
            "strongest_result": "B_LC_selector=product_s I_s exact no-cancellation gate; axial C_A=0 follows if all I_s=1, otherwise selector leakage is bounded by projector, boundary, H_ref, Poynting and GM-transfer rows.",
            "still_missing": "projector naturality or norm; boundary/source-owner closure; H_ref/M_H lock; Poynting/collar norms; GM/Poisson-Gauss transfer; clock/light/orbit downstream action certificates",
            "public_claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3571_0",
            "target_doc": "3572-Y5-R2FR-projector-naturality-deltaGammaPi-zero-or-operator-norm.md",
            "target_script": "scripts/Y5_R2FR_3572_projector_naturality_deltaGammaPi_zero_or_operator_norm.py",
            "objective": "try to prove Pi_M is q/e_obs/tau-natural so delta_Gamma Pi_M=0; if not, create a source-backed operator-norm row for epsilon_projector_comm",
            "success_gate": "delta_Gamma Pi_M=0 theorem in the selected branch, or a numeric/theorem-sourced bound for ||delta_Gamma Pi_M||",
            "reason": "projector reentry is the sharpest remaining weak link in the parent LC selector product gate",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "parent_LC_branch_selector_product_gate",
            "status": "PARTIAL_THEOREM_WITH_EXPLICIT_LEAKAGE_BOUND_ROWS",
            "selector_formula": "B_LC_selector=product_s I_s",
            "leakage_formula": "epsilon_selector_leak=sum named projector/boundary/reference/Poynting/GM/readout tails",
            "axial_consequence": "C_A=0 only if B_LC_selector is publicly derived",
            "next_action": "prove or bound delta_Gamma Pi_M",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    sectors: list[dict[str, object]],
    leaks: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3571_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3571 source paths exist"))
    needles = {
        "handoff_3570": "NEXT3570_0",
        "selector_3570": "SEL3570_2_response_split",
        "zero_3570": "AZC3570_7_total",
        "status_3570": "B_LC_selector",
        "signature_3566": "SIG3566_10_total_signature",
        "variation_3566": "VAR3566_0_total_noGamma",
        "parent_spine_2416": "PAS2416_2_no_independent_gamma",
        "local_gr_blocks": "A511_5_boundary_reference",
        "source_owner_contract": "A4_mass_flux_projector",
        "gamma_matrix_3493": "SEC3493_7_boundary_improvement",
        "gamma_verdict_3565": "SECT3565_0_total",
        "hyper_kernel_3496": "KHS3496_6_projector_comm",
        "slot_audit_2375": "NGSA2375_0_stack_target",
        "theorem_stack_2375": "NGT2375_2_sector_sum",
        "sector_audit_2415": "SGA2415_0_total",
        "gamma_import_2414": "GSI2414_7_boundary_nonhilbert",
    }
    validations.append(("VAL3571_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected selector/leak source needles found"))
    validations.append(("VAL3571_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3571 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3571_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3571_4_product_gate_present", any(row["theorem_id"] == "BLC3571_0_exact_product_gate" and "product_s" in str(row["statement"]) for row in theorem), "B_LC product gate theorem present"))
    validations.append(("VAL3571_5_sector_matrix_present", any(row["indicator"] == "B_LC_selector" for row in sectors) and len(sectors) >= 10, "sector product matrix includes total selector"))
    validations.append(("VAL3571_6_leak_bounds_present", {"epsilon_projector_comm", "epsilon_boundary_flux", "epsilon_Poynting_worldtube", "epsilon_GM_transfer"}.issubset({str(row["symbol"]) for row in leaks}), "key leakage bound formulas present"))
    validations.append(("VAL3571_7_public_claim_blocked", any(row["gate_id"] == "GATE3571_6_public_BLC" and row["status"] == "FAIL_CURRENT_PUBLIC_CLAIM" for row in gates), "public B_LC selector remains blocked"))
    validations.append(("VAL3571_8_projector_next_selected", any(row["decision_id"] == "DEC3571_2_next_target" for row in decisions), "projector naturality selected as next target"))
    validations.append(("VAL3571_9_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in theorem + sectors + leaks + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in theorem + sectors + leaks + gates + decisions)
    validations.append(("VAL3571_10_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3571*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3571_11_formalization_workbench_untouched", not formalization_touched, "no 3571 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    sectors: list[dict[str, object]],
    leaks: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3571 - Parent LC branch selector theorem or source-owner bound",
        "",
        "## Verdict",
        "3571 reduces the parent LC selector to an exact finite product gate: `B_LC_selector = product_s I_s`.  Every active sector must either exclude `Gamma_ind/omega_ind` by argument-domain exhaustion or carry an explicit bound.  This is the no-smuggling rule in theorem form.",
        "",
        "The selector is not public yet.  The live blockers are now narrow and named: projector/domain reentry, boundary/source-owner flux, `H_ref/M_H` reference lock, Poynting/collar flux, GM transfer, and clock/light/orbit downstream certificates.  Crucially, Poynting is not ignored: it is kept as Hilbert/Noether source energy or as `epsilon_Poynting_worldtube` if boundary flux survives.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Selector theorem"])
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['statement']} ({row['status']})")
    lines.extend(["", "## Sector product gates"])
    for row in sectors:
        lines.append(f"- `{row['sector_gate_id']}` `{row['indicator']}`: {row['current_status']} ({row['open_gap']})")
    lines.extend(["", "## Leakage bounds"])
    for row in leaks:
        lines.append(f"- `{row['leak_id']}` `{row['symbol']}`: {row['bound_formula']} ({row['status']})")
    lines.extend(["", "## Activation gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} -> {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target", f"- `{next_target[0]['target_doc']}`", f"- Objective: {next_target[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    theorem = selector_theorem_rows(source_paths)
    sectors = sector_product_rows(source_paths)
    leaks = leakage_bound_rows(source_paths)
    gates = activation_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3571_SOURCE_REGISTER.csv",
        "selector_theorem": RESIDUALS / "P8_Y5_R2FR_3571_BLC_SELECTOR_THEOREM.csv",
        "sector_product_matrix": RESIDUALS / "P8_Y5_R2FR_3571_BLC_SECTOR_PRODUCT_MATRIX.csv",
        "leakage_bound_rows": RESIDUALS / "P8_Y5_R2FR_3571_SOURCE_OWNER_LEAKAGE_BOUND_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3571_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3571_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3571_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3571_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_parent_LC_branch_selector_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3571_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["selector_theorem"], theorem)
    write_csv(outputs["sector_product_matrix"], sectors)
    write_csv(outputs["leakage_bound_rows"], leaks)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, theorem, sectors, leaks, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, theorem, sectors, leaks, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3571 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
