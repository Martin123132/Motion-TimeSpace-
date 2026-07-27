from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC_NAME = "918-Y5-R10-nonpropagating-mass-gauge-constraint-sector-or-DeltaHT-scorepack.md"
STATUS = "Y5_R10_918_nonpropagating_mass_gauge_constraint_sector_attempted_matter_silence_unproved_DeltaHT_scorepack_retained"
CLAIM_CEILING = "constraint_sector_attempt_only_no_parent_mass_gauge_symmetry_no_matter_silence_no_Newton_PPN_or_local_GR_claim"
NEXT_TARGET = "919-Y5-R10-matter-current-silence-lemma-or-DeltaHT-bound-runner.md"
GENERATED = datetime.now(timezone.utc).isoformat()
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "917_doc",
            "path": "917-Y5-R10-BF-mass-current-gauge-Noether-source-identity-or-DeltaHT-bound-fill.md",
            "role": "sets E_M target and selects nonpropagating mass-gauge constraint sector",
            "needle": "Owned first-class E_M equation",
        },
        {
            "source_id": "917_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_917_VALIDATION.csv",
            "role": "proves 917 handoff is clean and formalization workbench remains untouched",
            "needle": "V917_10_validation_rows_ready",
        },
        {
            "source_id": "223_constraint_algebra",
            "path": "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
            "role": "prior multiplier/constraint algebra template for zero local degrees",
            "needle": "zero X degrees: conditional",
        },
        {
            "source_id": "270_Cperp_first_class",
            "path": "270-Cperp-residual-shift-constraint-attempt.md",
            "role": "first-class route condition: physical action must be independent of gauge variable",
            "needle": "Cperp can be gauge only if it is absent from physical dynamics",
        },
        {
            "source_id": "07_nonpropagating_constraint",
            "path": "07-nonpropagating-reciprocity-constraint.md",
            "role": "nonpropagating constraint removes exterior hair but parent origin remains open",
            "needle": "no R_AB kinetic term;",
        },
        {
            "source_id": "505_mass_charge_closure",
            "path": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
            "role": "conditional local GR/Newton bridge if EH plus silent sectors are parent-derived",
            "needle": "derive the EH-plus-silent local exterior reduction from MTS itself",
        },
        {
            "source_id": "446_source_owner_contract",
            "path": "446-source-owner-current-parent-action-contract.md",
            "role": "anti-cheat rule against adding multipliers solely to kill dangerous residuals",
            "needle": "a multiplier that simply sets every dangerous residual to zero is not a derivation",
        },
        {
            "source_id": "source_owner_terms",
            "path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "role": "parent source-owner decomposition requirement",
            "needle": "A1_source_owner_decomposition",
        },
        {
            "source_id": "mass_flux_projector_contract",
            "path": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
            "role": "no ad hoc multiplier rule for mass-flux projector calibration",
            "needle": "MF3_no_ad_hoc_multiplier",
        },
        {
            "source_id": "PiM_flux_closure_contract",
            "path": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
            "role": "topological mass-current origin must be absolute and not merely fitted",
            "needle": "FC5_topological_mass_current_origin",
        },
        {
            "source_id": "500_topological_PiM",
            "path": "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md",
            "role": "topological current can close itself but is not yet the observed Hilbert channel",
            "needle": "not yet the observed Hilbert/measured mass channel",
        },
    ]


def build_source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": bool_string(exists),
                "needle_found": bool_string(needle_found),
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "current_result": "a nonpropagating first-class mass-gauge constraint can be written as a precise ansatz, but the parent mass symmetry and matter-current silence are not derived",
            "technical_verdict": "zero local DOF is conditionally available; no fifth-force/no source-distortion is the live blocker",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def constraint_sector_rows() -> list[dict[str, object]]:
    return [
        {
            "ansatz_id": "MGC918_0_target_residual",
            "object": "E_M",
            "proposed_form": "E_M := J_M^top - Pi_M J_H - dB_zero",
            "variation_result": "must be imposed as an owned Euler/Gauss equation, not as a named closure condition",
            "local_dof_result": "none by itself; E_M is a constraint target",
            "blocker": "parent action has not derived E_M as the equation of a mass-gauge variable",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "ansatz_id": "MGC918_1_multiplier_connection",
            "object": "A_M one-form multiplier",
            "proposed_form": "S_A = integral A_M wedge E_M",
            "variation_result": "delta A_M gives E_M=0",
            "local_dof_result": "zero only if A_M is pure multiplier/first-class and carries no kinetic term",
            "blocker": "delta matter of A_M wedge Pi_M J_H generically changes matter equations unless silence is derived",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "ansatz_id": "MGC918_2_BF_topological_pair",
            "object": "A_M, B_M",
            "proposed_form": "S_BF = integral k_M B_M wedge dA_M + A_M wedge (J_M^top - Pi_M J_H)",
            "variation_result": "delta B_M gives dA_M=0; delta A_M gives k_M dB_M = J_M^top - Pi_M J_H",
            "local_dof_result": "4D BF sector is topological if gauge symmetries survive the source coupling",
            "blocker": "this enforces exactness/equality only after B_M is identified with B_zero and boundary flux is fixed",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "ansatz_id": "MGC918_3_first_class_constraint",
            "object": "C_M approx 0",
            "proposed_form": "primary pi_A approx 0, secondary E_M approx 0",
            "variation_result": "constraint chain can remove A_M local degrees",
            "local_dof_result": "zero if {E_M,E_M} closes and {E_M,H_parent} closes weakly",
            "blocker": "matter/Hilbert current bracket is not computed from a parent symplectic structure",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "ansatz_id": "MGC918_4_universal_source_charge",
            "object": "Pi_M J_H",
            "proposed_form": "ordinary matter enters only through observed-frame Hilbert source current",
            "variation_result": "would give a universal mass charge if it is the Noether/Hamiltonian generator",
            "local_dof_result": "not a new local field if it is already the diffeo/Hamiltonian source",
            "blocker": "Pi_M J_H is not yet proven equal to the topological/BF mass current",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "ansatz_id": "MGC918_5_level_and_GM_calibration",
            "object": "k_M, G_ref, M_eff",
            "proposed_form": "integral_S Q_M = M_eff and weak-field Poisson normalization fixes G_ref",
            "variation_result": "would connect the topological charge to measured GM",
            "local_dof_result": "calibration is algebraic rather than propagating",
            "blocker": "level/normalization is not derived before orbital/PPN readout",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def algebra_rows() -> list[dict[str, object]]:
    return [
        {
            "test_id": "ALG918_0_primary_constraint",
            "condition": "A_M has no velocity in the parent Lagrangian",
            "calculation": "pi_A approx 0",
            "required_for_pass": "no Maxwell/Proca/gradient kinetic term for A_M",
            "current_status": "conditional_support_from_nonpropagating_templates",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "ALG918_1_secondary_constraint",
            "condition": "Hamiltonian preservation of pi_A",
            "calculation": "dot(pi_A) = -delta H/delta A_M = E_M approx 0",
            "required_for_pass": "E_M is produced by variation, not declared after the fact",
            "current_status": "ansatz_written_not_parent_derived",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "ALG918_2_self_bracket",
            "condition": "constraint is first-class",
            "calculation": "{E_M(x), E_M(y)} approx 0 or closes on existing constraints",
            "required_for_pass": "parent symplectic brackets for topological and Hilbert currents",
            "current_status": "missing_parent_symplectic_structure",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "ALG918_3_Hamiltonian_preservation",
            "condition": "E_M remains zero under evolution",
            "calculation": "{E_M,H_parent} approx 0",
            "required_for_pass": "source-owner Ward identity plus boundary flux silence",
            "current_status": "not_computed",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "ALG918_4_matter_current_bracket",
            "condition": "matter coupling does not create composition force",
            "calculation": "delta(A_M wedge Pi_M J_H)/delta psi must be boundary, gauge, or existing diffeo equation",
            "required_for_pass": "matter-current silence lemma",
            "current_status": "main_blocker",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "ALG918_5_boundary_bracket",
            "condition": "B_zero and BF improvements carry no compact exterior leakage",
            "calculation": "integral_boundary delta B_zero = 0 and integral_shell dB_zero fixed",
            "required_for_pass": "exact no-flux theorem or sourced bound row",
            "current_status": "missing_boundary_input",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "ALG918_6_degree_count",
            "condition": "mass-gauge sector adds zero local propagating DOF",
            "calculation": "N_DOF = half(phase variables - 2 first_class - second_class)",
            "required_for_pass": "complete first-class chain including source coupling",
            "current_status": "zero_DOF_conditional_not_promoted",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def force_rows() -> list[dict[str, object]]:
    return [
        {
            "force_id": "F918_0_direct_multiplier_force",
            "coupling": "A_M wedge Pi_M J_H",
            "dangerous_variation": "A_M wedge Pi_M delta J_H",
            "required_zero_condition": "A_M is pure gauge with zero physical holonomy or the variation is exactly an existing Ward/diffeo equation",
            "status": "not_derived",
            "residual_symbol": "F_M_force",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "force_id": "F918_1_species_charge",
            "coupling": "mass-gauge charge assignment for matter",
            "dangerous_variation": "species-dependent source response or clock/composition dependence",
            "required_zero_condition": "one coframe/one Hilbert current universality before any mass-gauge readout",
            "status": "not_parent_signed",
            "residual_symbol": "Q_BF_extra",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "force_id": "F918_2_topological_holonomy_force",
            "coupling": "flat A_M with nonzero compact holonomy",
            "dangerous_variation": "Aharonov-Bohm-like mass phase or boundary impulse",
            "required_zero_condition": "compact local holonomy trivial or source-backed bound below local tests",
            "status": "missing_boundary_holonomy_input",
            "residual_symbol": "B_zero_flux",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "force_id": "F918_3_wrong_GM_normalization",
            "coupling": "k_M maps topological charge to measured mass",
            "dangerous_variation": "constant but wrong mass normalization masquerades as Newton pass",
            "required_zero_condition": "parent level calibration to measured G_ref and M_eff",
            "status": "not_derived",
            "residual_symbol": "k_M",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def scorepack_rows() -> list[dict[str, object]]:
    return [
        {
            "score_id": "DHT918_0_DeltaHT_current",
            "symbol": "Delta_HT_current",
            "definition": "J_M^top - Pi_M J_H - dB_zero after the mass-gauge route fails to derive exact equality",
            "needed_input": "parent variation or measured residual map",
            "candidate_formula": "Delta_HT_current = E_M",
            "arena": "local_GR_PPN_source_normalization",
            "status": "MISSING_PARENT_EQUATION",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "score_id": "DHT918_1_K_BF_H",
            "symbol": "K_BF_H",
            "definition": "coefficient multiplying Hilbert/source current inside the BF or multiplier equation",
            "needed_input": "parent mass-gauge coupling coefficient and sign",
            "candidate_formula": "S contains K_BF_H A_M wedge Pi_M J_H",
            "arena": "R10_PPN_clock_orbital",
            "status": "MISSING_PARENT_COEFFICIENT",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "score_id": "DHT918_2_C_M",
            "symbol": "C_M",
            "definition": "constraint-algebra closure defect for E_M",
            "needed_input": "{E_M,E_M} and {E_M,H_parent} from parent symplectic form",
            "candidate_formula": "C_M = norm({E_M,E_M},{E_M,H})",
            "arena": "local_GR_PPN",
            "status": "MISSING_CONSTRAINT_ALGEBRA",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "score_id": "DHT918_3_F_M_force",
            "symbol": "F_M_force",
            "definition": "local fifth-force/source-distortion term induced by mass-gauge coupling",
            "needed_input": "weak-field variation with respect to matter variables",
            "candidate_formula": "F_M_force proportional to delta(A_M wedge Pi_M J_H)/delta psi",
            "arena": "WEP_clock_PPN_orbital",
            "status": "MISSING_MATTER_SILENCE_LEMMA",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "score_id": "DHT918_4_B_zero_flux",
            "symbol": "B_zero_flux",
            "definition": "compact-boundary leakage of the exact improvement B_zero",
            "needed_input": "boundary no-flux theorem or source-backed bound",
            "candidate_formula": "B_zero_flux = integral_boundary B_zero",
            "arena": "R10_orbital_PPN",
            "status": "MISSING_BOUNDARY_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "score_id": "DHT918_5_k_M",
            "symbol": "k_M",
            "definition": "BF level or mass-gauge normalization connecting topological charge to M_eff",
            "needed_input": "quantization/normalization rule and measured-GM calibration",
            "candidate_formula": "Q_M = k_M integral B_M or equivalent Hamiltonian charge",
            "arena": "Newton_PPN_orbital",
            "status": "MISSING_LEVEL_CALIBRATION",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "score_id": "DHT918_6_Q_BF_extra",
            "symbol": "Q_BF_extra",
            "definition": "extra BF/topological mass charge not equal to the observed Hilbert source",
            "needed_input": "charge equality theorem or observational bound row",
            "candidate_formula": "Q_BF_extra = Q_BF - integral Pi_M J_H",
            "arena": "source_normalization_PPN_orbital",
            "status": "MISSING_CHARGE_EQUALITY",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD918_0_constraint_sector",
            "branch": "nonpropagating_mass_gauge_constraint",
            "verdict": "precise_ansatz_not_parent_derived",
            "reason": "A_M/B_M can make a zero-DOF constraint machine, but source coupling silence and first-class algebra are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD918_1_main_blocker",
            "branch": "matter_current_silence",
            "verdict": "selected_next_derivation_target",
            "reason": "if A_M wedge Pi_M J_H has non-boundary matter variation, local branch gets a fifth-force/source-distortion residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD918_2_scorepack",
            "branch": "DeltaHT_scorepack",
            "verdict": "retained_nonclaim",
            "reason": "all missing clauses are now executable residual symbols, but no coefficient is source-ready",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE918_0_parent_mass_gauge_symmetry",
            "claim": "MTS derives a mass-gauge symmetry whose Gauss equation is E_M=0",
            "blocker": "symmetry and parent action are ansatz-level",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE918_1_first_class_algebra",
            "claim": "mass-gauge constraint is first-class with zero local DOF",
            "blocker": "source-current Poisson brackets and Hamiltonian preservation are not computed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE918_2_no_fifth_force",
            "claim": "mass-gauge coupling creates no local fifth force or matter-source distortion",
            "blocker": "matter-current silence lemma is missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE918_3_GM_calibration",
            "claim": "topological/BF charge is the measured Newtonian mass with fixed G_ref",
            "blocker": "level and source-measure calibration are not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE918_4_local_GR",
            "claim": "R10/local-GR/PPN branch passes from this sector",
            "blocker": "EH-plus-silent exterior reduction and DeltaHT coefficients remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "prove that the A_M wedge Pi_M J_H coupling is variation-silent because it is boundary/gauge/diffeomorphism-owned; if not, turn F_M_force and K_BF_H into sourced bound rows",
            "include": "matter variation, coframe/Hilbert current ownership, Ward identity, flat A_M holonomy, no species charge, weak-field force readout",
            "exclude": "new fitted fifth force, multiplier magic, measured-GM promotion, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def formalization_changed_count() -> int:
    formalization = ROOT.parent / "formalization-workbench"
    if not formalization.exists():
        return 0
    count = 0
    for path in formalization.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > FORMALIZATION_CUTOFF:
                count += 1
    return count


def all_false(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bool:
    for row in rows:
        for field in fields:
            value = str(row.get(field, "")).strip().lower()
            if value == "true":
                return False
    return True


def validation_rows(
    source_register: list[dict[str, object]],
    constraint: list[dict[str, object]],
    algebra: list[dict[str, object]],
    force: list[dict[str, object]],
    scorepack: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_register)
    prior_917_clean_path = OUT / "P8_Y5_BRR545_917_VALIDATION.csv"
    prior_917_clean = prior_917_clean_path.exists() and "V917_10_validation_rows_ready" in text(prior_917_clean_path)
    no_claim_fields = ("parent_signed", "claim_allowed", "valid_for_claim", "passes_as_claim", "score_ready")
    generated_sets = constraint + algebra + force + scorepack + decisions + gates
    scorepack_symbols = {row["symbol"] for row in scorepack}
    required_symbols = {"Delta_HT_current", "K_BF_H", "C_M", "F_M_force", "B_zero_flux", "k_M", "Q_BF_extra"}
    rows = [
        {
            "check_id": "V918_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "one or more source paths or needles missing",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_1_prior_917_clean",
            "result": "pass" if prior_917_clean else "fail",
            "detail": "P8_Y5_BRR545_917_VALIDATION.csv clean" if prior_917_clean else "917 validation handoff missing or incomplete",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_2_constraint_sector_attempted_not_parent_signed",
            "result": "pass" if all_false(constraint, no_claim_fields) else "fail",
            "detail": "mass-gauge/BF constraint sector written but all parent-signed claim fields remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_3_constraint_algebra_blocks_claim",
            "result": "pass" if all_false(algebra, no_claim_fields) else "fail",
            "detail": "constraint algebra rows identify first-class and Hamiltonian-preservation blockers",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_4_matter_force_silence_missing",
            "result": "pass" if all_false(force, no_claim_fields) and any(row["residual_symbol"] == "F_M_force" for row in force) else "fail",
            "detail": "matter-current silence is explicitly the live no-fifth-force blocker",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_5_DeltaHT_scorepack_nonclaim",
            "result": "pass" if all_false(scorepack, no_claim_fields) and required_symbols <= scorepack_symbols else "fail",
            "detail": "DeltaHT scorepack has required residual symbols and no claim-ready rows",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_6_claim_gates_false",
            "result": "pass" if all_false(gates, no_claim_fields) else "fail",
            "detail": "all mass-gauge/local-GR/Newton/PPN claim gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_7_branch_decision_nonclaim",
            "result": "pass" if all_false(decisions, no_claim_fields) else "fail",
            "detail": "branch decision selects matter-current silence lemma without promoting a pass",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_8_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated_sets, no_claim_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_9_formalization_workbench_untouched",
            "result": "pass" if formalization_changed_count() == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_changed_count()}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_10_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("919-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V918_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]
    return rows


def write_doc(
    source_register: list[dict[str, object]],
    summary: list[dict[str, object]],
    constraint: list[dict[str, object]],
    algebra: list[dict[str, object]],
    force: list[dict[str, object]],
    scorepack: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    doc = ROOT / DOC_NAME
    body = f"""# 918 - Y5/R10 Nonpropagating Mass-Gauge Constraint Sector Or DeltaHT Scorepack

Private derivation checkpoint. This is not a public R10, local-GR, Newton, PPN, WEP, clock, orbital, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **the nonpropagating constraint machine can be written cleanly, but it is not yet parent-derived.**

The best candidate machine is:

```text
E_M := J_M^top - Pi_M J_H - dB_zero,
S_A = integral A_M wedge E_M,
or S_BF = integral k_M B_M wedge dA_M + A_M wedge (J_M^top - Pi_M J_H).
```

This can make `E_M=0` look like a Gauss/constraint equation and can keep the new sector zero local DOF if the full first-class algebra closes.

The problem is the coupling. Once `A_M` touches `Pi_M J_H`, variation with respect to matter generically produces:

```text
delta S / delta psi contains A_M wedge Pi_M delta J_H / delta psi.
```

So the branch only survives if that term is exactly boundary/gauge/Ward-owned, or if it is bounded as a real residual. That is not a defeat; it is the sharpest version of the missing coupling problem.

## Non-Claim Summary

{markdown_table(summary, ["status", "claim_ceiling", "current_result", "technical_verdict", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## Constraint Sector Ansatz

{markdown_table(constraint, ["ansatz_id", "object", "proposed_form", "variation_result", "local_dof_result", "blocker", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Constraint Algebra Audit

{markdown_table(algebra, ["test_id", "condition", "calculation", "required_for_pass", "current_status", "passes_as_claim", "valid_for_claim", "generated_utc"])}

## Matter-Force Silence Audit

{markdown_table(force, ["force_id", "coupling", "dangerous_variation", "required_zero_condition", "status", "residual_symbol", "claim_allowed", "valid_for_claim", "generated_utc"])}

## DeltaHT Scorepack

{markdown_table(scorepack, ["score_id", "symbol", "definition", "needed_input", "candidate_formula", "arena", "status", "score_ready", "valid_for_claim", "generated_utc"])}

## Branch Decision

{markdown_table(decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Claim Gate

{markdown_table(gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Next Target

{markdown_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail", "generated_utc"])}
"""
    doc.write_text(body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_register = build_source_register()
    summary = nonclaim_summary_rows()
    constraint = constraint_sector_rows()
    algebra = algebra_rows()
    force = force_rows()
    scorepack = scorepack_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    next_rows = next_target_rows()
    validation = validation_rows(source_register, constraint, algebra, force, scorepack, decisions, gates)

    write_csv(OUT / "P8_Y5_R10_918_SOURCE_REGISTER.csv", source_register, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_918_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "technical_verdict", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_918_CONSTRAINT_SECTOR_ANSATZ.csv", constraint, ["ansatz_id", "object", "proposed_form", "variation_result", "local_dof_result", "blocker", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_918_CONSTRAINT_ALGEBRA_AUDIT.csv", algebra, ["test_id", "condition", "calculation", "required_for_pass", "current_status", "passes_as_claim", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_918_MATTER_FORCE_SILENCE_AUDIT.csv", force, ["force_id", "coupling", "dangerous_variation", "required_zero_condition", "status", "residual_symbol", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_918_DELTAHT_SCOREPACK.csv", scorepack, ["score_id", "symbol", "definition", "needed_input", "candidate_formula", "arena", "status", "score_ready", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_918_BRANCH_DECISION.csv", decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_918_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_918_NEXT_TARGET.csv", next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_918_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_register, summary, constraint, algebra, force, scorepack, decisions, gates, next_rows, validation)
    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
