from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_915_Hilbert_topological_mass_current_equality_attempted_not_parent_derived_Delta_HT_current_retained_nonclaim"
CLAIM_CEILING = "Hilbert_topological_mass_current_equality_attempt_only_no_closed_PiM_flux_no_measured_GM_no_Newton_PPN_or_local_GR_claim"
DOC_NAME = "915-Y5-R10-Hilbert-topological-mass-current-equality-or-projector-bound-pack-fill.md"
NEXT_TARGET = "916-Y5-R10-parent-BF-mass-current-sector-or-Delta-HT-bound-input.md"

SOURCE_SPECS = [
    {
        "source_id": "914_doc",
        "path": ROOT / "914-Y5-R10-topological-absolute-PiM-parent-clause-or-projector-source-bound-pack.md",
        "needle": "the topological absolute `Pi_M` route remains the cleanest local-GR-facing route, but it is not parent-signed",
        "role": "immediate handoff selecting Hilbert/topological equality",
    },
    {
        "source_id": "914_validation",
        "path": OUT / "P8_Y5_BRR545_914_VALIDATION.csv",
        "needle": "V914_10_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "914_topological_clauses",
        "path": OUT / "P8_Y5_R10_914_TOPOLOGICAL_PARENT_CLAUSE_AUDIT.csv",
        "needle": "TPC914_5_Hilbert_topological_equality",
        "role": "unsigned topological PiM parent clauses",
    },
    {
        "source_id": "914_bound_pack",
        "path": OUT / "P8_Y5_R10_914_PROJECTOR_SOURCE_BOUND_PACK.csv",
        "needle": "PSB914_5_Delta_HT_current",
        "role": "Delta_HT_current fallback source row",
    },
    {
        "source_id": "455_flux_doc",
        "path": ROOT / "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "needle": "topological_current_route",
        "role": "topological current route and warning",
    },
    {
        "source_id": "455_flux_contract",
        "path": OUT / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "needle": "FC5_topological_mass_current_origin",
        "role": "topological current contract",
    },
    {
        "source_id": "449_source_current_doc",
        "path": ROOT / "449-source-current-Ward-universality-theorem-attempt.md",
        "needle": "conditional_Hilbert_source_current_theorem",
        "role": "Hilbert current/source Ward sublemma",
    },
    {
        "source_id": "449_source_current_contract",
        "path": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
        "needle": "SC6_closed_calibrated_mass_projector",
        "role": "Hilbert mass projector calibration contract",
    },
    {
        "source_id": "450_monopole_doc",
        "path": ROOT / "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "needle": "conditional_measured_monopole_theorem",
        "role": "Hilbert source to measured monopole gate",
    },
    {
        "source_id": "450_monopole_contract",
        "path": OUT / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "needle": "HM2_mass_flux_closure",
        "role": "Hilbert monopole closure/calibration contract",
    },
    {
        "source_id": "451_flux_euler_doc",
        "path": ROOT / "451-mass-flux-projector-Euler-calibration-attempt.md",
        "needle": "conditional_Euler_flux_closure",
        "role": "Euler/multiplier closure route and no-cheat warning",
    },
    {
        "source_id": "451_flux_euler_contract",
        "path": OUT / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "needle": "MF2_Euler_flux_closure",
        "role": "mass-flux Euler closure contract",
    },
    {
        "source_id": "457_hamiltonian_doc",
        "path": ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "needle": "conditional_Hamiltonian_boundary_charge_theorem",
        "role": "GR-like Hamiltonian equality comparison route",
    },
    {
        "source_id": "457_hamiltonian_contract",
        "path": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "needle": "HC4_charge_equals_PiM_Hilbert_mass",
        "role": "Hamiltonian charge equals Hilbert mass contract",
    },
    {
        "source_id": "458_pg_doc",
        "path": ROOT / "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "needle": "conditional_Poisson_Gauss_calibration_theorem",
        "role": "Poisson/Gauss measured-GM calibration comparison",
    },
    {
        "source_id": "458_pg_contract",
        "path": OUT / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "needle": "PG1_charge_equals_projected_Hilbert_source",
        "role": "Poisson/Gauss charge-current equality contract",
    },
    {
        "source_id": "460_newton_stack_doc",
        "path": ROOT / "460-source-normalized-Newton-branch-theorem-stack.md",
        "needle": "SN3_charge_equals_Hilbert_mass_current",
        "role": "source-normalized Newton stack equality rung",
    },
    {
        "source_id": "460_newton_stack_csv",
        "path": OUT / "P8_source_normalized_Newton_branch_STACK.csv",
        "needle": "SN3_charge_equals_Hilbert_mass_current",
        "role": "machine Newton stack equality rung",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [stringify(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "attempted the equality J_M^top = Pi_M J_H + dB_zero and compared it against Ward, Euler, and Hamiltonian charge routes",
            "best_partial_result": "if a parent topological/BF sector supplies a closed J_M^top and an independently owned equality to Pi_M J_H up to zero-flux exact terms, then d(Pi_M J_H)=0 follows cleanly",
            "hard_blockers": "the corpus does not currently contain the independent topological mass-current sector, equality Euler equation, zero-flux B_zero theorem, or Hamiltonian charge-current identity needed to sign the equality",
            "what_is_not_claimed": "closed projected Hilbert mass flux, measured-GM calibration, Newtonian source closure, PPN pass, local-GR reduction, or topological current equality",
            "decision": "equality is a sharp theorem target but remains unproved; Delta_HT_current and related source rows stay retained and invalid for claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def equality_derivation_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "step_id": "EDA915_0_define_two_currents",
            "claim_attempted": "define a closed topological mass current and the observed projected Hilbert mass current in the same degree/frame",
            "mathematical_form": "dJ_M^top=0; J_H from delta S_m/delta e_obs; Pi_M J_H in same exterior source-current complex",
            "what_would_close": "both currents are comparable before readout",
            "current_status": "conditional_Hilbert_current_available_topological_current_not_parent_constructed",
            "blocker": "no independent parent BF/closed-form mass-current sector is present",
        },
        {
            "step_id": "EDA915_1_equality_up_to_exact_term",
            "claim_attempted": "prove the topological current equals the projected Hilbert mass current up to an exact zero-flux improvement",
            "mathematical_form": "J_M^top = Pi_M J_H + dB_zero",
            "what_would_close": "d(Pi_M J_H)=dJ_M^top=0 because d^2B_zero=0",
            "current_status": "not_parent_derived_key_blocker",
            "blocker": "existing sources name this as FC5/HC4/PG1/SN3 but do not derive it",
        },
        {
            "step_id": "EDA915_2_boundary_zero_flux",
            "claim_attempted": "show the exact improvement does not shift compact or measured boundary mass",
            "mathematical_form": "integral_boundary dB_zero=0 and delta integral_boundary B_zero=0",
            "what_would_close": "prevents boundary improvements from becoming mu_extra or radial/source hair",
            "current_status": "fail_open",
            "blocker": "no class-only/no-hair theorem for B_zero or boundary owner flux",
        },
        {
            "step_id": "EDA915_3_variation_ownership",
            "claim_attempted": "vary the equality before readout without dropping projector/domain terms",
            "mathematical_form": "delta J_M^top = delta(Pi_M J_H)+d(delta B_zero), with delta Pi_M=0 theorem-zero or retained",
            "what_would_close": "stops the equality constraint from hiding projector stress",
            "current_status": "not_parent_derived",
            "blocker": "Pi_M topological silence and domain variation remain unsigned from 914",
        },
        {
            "step_id": "EDA915_4_no_exchange_projection",
            "claim_attempted": "prove hidden/projector/domain/boundary/range/coupling exchanges have zero mass projection",
            "mathematical_form": "Pi_M(F_X+F_P+F_B+F_D+F_nm+T d kappa)=0",
            "what_would_close": "makes the Hilbert current separately closed rather than only total-stress conserved",
            "current_status": "not_parent_derived",
            "blocker": "Ward conservation alone does not imply mass-channel closure",
        },
        {
            "step_id": "EDA915_5_Hamiltonian_crosscheck",
            "claim_attempted": "cross-check equality through a GR-like boundary charge",
            "mathematical_form": "B_xi/G_eff = M_eff[Pi_M J_H] and delta B_xi=delta integral_S Pi_M J_H",
            "what_would_close": "ties conserved geometric charge to observed Hilbert source mass",
            "current_status": "conditional_downstream_not_parent_derived",
            "blocker": "requires EH exterior, observed time generator, integrable charge, no extra charge, and PG calibration",
        },
        {
            "step_id": "EDA915_6_measured_GM_after_equality",
            "claim_attempted": "calibrate the closed current to measured Newtonian GM",
            "mathematical_form": "mu_obs=G_eff M_eff, M_eff proportional to integral_S Pi_M J_H, mu_extra=0",
            "what_would_close": "turns current closure into Newton source normalization",
            "current_status": "not_parent_derived",
            "blocker": "absolute calibration, constant G_eff, and zero residual monopoles remain open",
        },
    ]
    for row in rows:
        row.update(
            {
                "parent_derived": False,
                "claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def route_comparison_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "route_id": "RC915_0_topological_BF_mass_current",
            "route": "independent topological/BF mass-current sector",
            "core_identity": "dJ_M^top=0 and J_M^top = Pi_M J_H + dB_zero",
            "strength": "would close mass flux without Hodge metric stress if equality and no-flux are parent-owned",
            "failure": "no explicit parent sector/equality equation currently in corpus",
            "verdict": "best_next_derivation_target_not_claimed",
        },
        {
            "route_id": "RC915_1_Ward_mass_channel",
            "route": "separate Hilbert/Ward mass-channel conservation",
            "core_identity": "nabla_mu T_H^{mu nu}=0 plus zero exchange implies d(Pi_M J_H)=0",
            "strength": "standard GR-like source-current logic",
            "failure": "total Ward conservation allows hidden exchange and does not pick the Pi_M mass channel alone",
            "verdict": "conditional_sublemma_not_enough",
        },
        {
            "route_id": "RC915_2_Euler_lambda_closure",
            "route": "lambda_M source-normalization Euler equation",
            "core_identity": "delta_lambdaM S=0 gives d(Pi_M J_H)=0 or equality constraint",
            "strength": "mathematically direct",
            "failure": "closure-only unless lambda_M/equality constraint has independent gauge/topological/Ward origin",
            "verdict": "not_explanatory_without_parent_origin",
        },
        {
            "route_id": "RC915_3_Hamiltonian_boundary_charge",
            "route": "GR-like Hamiltonian/Iyer-Wald/ADM charge",
            "core_identity": "B_xi/G_eff = M_eff[Pi_M J_H]",
            "strength": "strongest familiar route if EH exterior and boundary integrability are already derived",
            "failure": "downstream of EH-only local branch, observed time generator, no extra charges, and PG calibration",
            "verdict": "powerful_crosscheck_not_current_topological_proof",
        },
        {
            "route_id": "RC915_4_retained_mismatch",
            "route": "do not prove equality; retain current mismatch",
            "core_identity": "Delta_HT_current := J_M^top - Pi_M J_H - dB_zero",
            "strength": "honest and testable if coefficients/projections are later supplied",
            "failure": "not a local-GR or Newtonian source claim",
            "verdict": "active_fallback",
        },
    ]
    for row in rows:
        row.update(
            {
                "claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def mismatch_residual_pack_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "residual_id": "MRP915_0_Delta_HT_current",
            "symbol": "Delta_HT_current",
            "definition": "mismatch current J_M^top - Pi_M J_H - dB_zero",
            "feeds": "d(Pi_M J_H), dln_Meff_dt, partial_r_ln_mu_obs, mu_extra",
            "needed_inputs": "explicit J_M^top sector, Pi_M J_H source map, B_zero improvement, boundary integral convention",
            "current_status": "MISSING_PARENT_HILBERT_TOPOLOGICAL_EQUALITY",
        },
        {
            "residual_id": "MRP915_1_d_Delta_HT",
            "symbol": "dDelta_HT",
            "definition": "exterior derivative/divergence of the Hilbert-topological mismatch",
            "feeds": "mass-flux nonclosure and radial/time drift",
            "needed_inputs": "current degree, exterior derivative convention, source-current domain, chain-map proof or violation",
            "current_status": "MISSING_CURRENT_DOMAIN_AND_CHAIN_MAP",
        },
        {
            "residual_id": "MRP915_2_B_zero_flux",
            "symbol": "B_zero_flux",
            "definition": "boundary flux of the exact improvement in the equality",
            "feeds": "compact boundary mu_extra and measured-GM offset/hair",
            "needed_inputs": "B_zero formula, boundary orientation, class-only/no-hair theorem or bound",
            "current_status": "MISSING_ZERO_BOUNDARY_FLUX_PROOF",
        },
        {
            "residual_id": "MRP915_3_c_HT",
            "symbol": "c_HT",
            "definition": "coefficient mapping Hilbert-topological mismatch into weak-field/source observables",
            "feeds": "PPN/source-normalization residual vector",
            "needed_inputs": "weak-field source map, normalization to GM, local-bound arena projection",
            "current_status": "MISSING_COEFFICIENT_AND_UNITS",
        },
        {
            "residual_id": "MRP915_4_mu_extra_HT",
            "symbol": "mu_extra_HT",
            "definition": "extra measured monopole sourced by equality mismatch or boundary improvement",
            "feeds": "measured GM calibration and Newtonian source closure",
            "needed_inputs": "Gauss/Poisson conversion, orbital readout convention, constant G_eff branch",
            "current_status": "MISSING_GAUSS_ORBITAL_CALIBRATION",
        },
        {
            "residual_id": "MRP915_5_dln_Meff_dt",
            "symbol": "dln_Meff_dt",
            "definition": "time drift in effective source mass if projected Hilbert flux is not closed",
            "feeds": "clock/orbital/source-normalization bounds",
            "needed_inputs": "time generator, local exterior foliation, observed frame, residual coefficient",
            "current_status": "MISSING_TIME_GENERATOR_AND_FLUX_CLOSURE",
        },
        {
            "residual_id": "MRP915_6_partial_r_ln_mu_obs",
            "symbol": "partial_r_ln_mu_obs",
            "definition": "radial source hair from nonclosed current or boundary mismatch",
            "feeds": "R10, fifth-force/range, orbital residual tests",
            "needed_inputs": "annulus integration, radial domain selector, finite-range mapping, bound curve",
            "current_status": "MISSING_RADIAL_NO_HAIR_OR_BOUND_INPUT",
        },
    ]
    for row in rows:
        row.update(
            {
                "score_ready": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD915_0_equality_attempt",
            "verdict": "not_parent_derived",
            "reason": "all existing equality routes are conditional: topological FC5, Hamiltonian HC4/PG1, and Newton stack SN3 name the needed identity but do not derive it",
            "action": "do not promote d(Pi_M J_H)=0, measured GM, Newton, PPN, or local GR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD915_1_residual_pack",
            "verdict": "Delta_HT_current_retained",
            "reason": "current mismatch is now the clean fallback variable connecting topological equality failure to mass-flux nonclosure and measured-GM residuals",
            "action": "keep residual rows score_ready=false until parent BF sector or coefficient/bound inputs exist",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD915_2_next_derivation_target",
            "verdict": "select_parent_BF_mass_current_sector",
            "reason": "the least-scrutiny derivation route is to build an independently motivated closed-form/BF mass-current sector that earns the equality rather than imposing it as a lambda_M repair",
            "action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "CGATE915_0_Hilbert_topological_equality",
            "claim": "J_M^top = Pi_M J_H + dB_zero is parent-derived",
            "blocker": "no explicit parent BF/closed-form sector or equality Euler/Ward identity",
        },
        {
            "gate_id": "CGATE915_1_closed_PiM_flux",
            "claim": "d(Pi_M J_H)=0 is derived",
            "blocker": "equality, chain-map, zero exchange, and boundary no-flux clauses remain unsigned",
        },
        {
            "gate_id": "CGATE915_2_Hamiltonian_charge_current_identity",
            "claim": "B_xi/G_eff equals M_eff[Pi_M J_H]",
            "blocker": "EH exterior, observed time generator, integrability, no extra charge, and PG calibration remain downstream",
        },
        {
            "gate_id": "CGATE915_3_Delta_HT_scored",
            "claim": "Delta_HT_current residual is numerically bounded/scored",
            "blocker": "coefficient, units, current formulas, and arena projections missing",
        },
        {
            "gate_id": "CGATE915_4_measured_GM_Newton",
            "claim": "measured Newtonian GM/source normalization is derived",
            "blocker": "closed flux, absolute calibration, constant G_eff, and zero mu_extra are not derived",
        },
        {
            "gate_id": "CGATE915_5_local_GR",
            "claim": "local exterior reduces to GR/PPN-safe metric branch",
            "blocker": "projector/current/source residuals remain retained and unbounded",
        },
    ]
    for row in rows:
        row.update(
            {
                "claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to construct an independently motivated parent BF/closed-form mass-current sector that yields J_M^top = Pi_M J_H + dB_zero; if not, fill Delta_HT_current bound inputs",
            "include": "BF/topological current sector, equality variation, no-cheat lambda test, boundary B_zero no-flux, Delta_HT coefficient/source rows",
            "exclude": "declaring equality by naming, using Hodge/DeWitt zero-stress, measured-GM promotion, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    guarded_fields = ("valid_for_claim", "claim_allowed", "score_ready", "parent_derived")
    for rows in tables:
        for row in rows:
            for field in guarded_fields:
                if field in row and stringify(row[field]).lower() != "false":
                    return False
    return True


def validation_rows(
    generated_utc: str,
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    routes: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    generated_tables: list[list[dict[str, object]]],
) -> list[dict[str, object]]:
    prior_rows = read_csv(OUT / "P8_Y5_BRR545_914_VALIDATION.csv")
    formalization_count = formalization_changed_after_cutoff()
    checks = [
        {
            "check_id": "V915_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in sources) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V915_1_prior_914_clean",
            "result": "pass" if prior_rows and all(row.get("result") == "pass" for row in prior_rows) else "fail",
            "detail": "P8_Y5_BRR545_914_VALIDATION.csv clean",
        },
        {
            "check_id": "V915_2_equality_not_parent_derived",
            "result": "pass" if attempts and all(not row["parent_derived"] for row in attempts) else "fail",
            "detail": "all Hilbert/topological equality derivation steps remain unsigned",
        },
        {
            "check_id": "V915_3_key_identity_recorded",
            "result": "pass" if any(row["step_id"] == "EDA915_1_equality_up_to_exact_term" and row["current_status"] == "not_parent_derived_key_blocker" for row in attempts) else "fail",
            "detail": "J_M^top = Pi_M J_H + dB_zero is recorded as the decisive missing identity",
        },
        {
            "check_id": "V915_4_route_comparison_nonclaim",
            "result": "pass" if routes and all(not row["claim_allowed"] for row in routes) else "fail",
            "detail": "topological, Ward, Euler, and Hamiltonian routes remain nonclaim",
        },
        {
            "check_id": "V915_5_residual_pack_nonclaim",
            "result": "pass" if residuals and all(not row["score_ready"] and not row["valid_for_claim"] and str(row["current_status"]).startswith("MISSING_") for row in residuals) else "fail",
            "detail": "all Delta_HT residual rows remain missing-input and invalid for claim",
        },
        {
            "check_id": "V915_6_claim_gates_false",
            "result": "pass" if gates and all(not row["claim_allowed"] for row in gates) else "fail",
            "detail": "all equality/flux/Newton/local-GR claim gates remain false",
        },
        {
            "check_id": "V915_7_all_generated_rows_nonclaim",
            "result": "pass" if all_nonclaim(generated_tables) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
        },
        {
            "check_id": "V915_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V915_9_next_target_selected",
            "result": "pass" if next_rows and next_rows[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V915_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    summary: list[dict[str, object]],
    attempts: list[dict[str, object]],
    routes: list[dict[str, object]],
    residuals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    path = ROOT / DOC_NAME
    content = f"""# 915 - Y5/R10 Hilbert-Topological Mass-Current Equality Or Projector Bound-Pack Fill

Private post-checkpoint-work note. This is not a public Newtonian, PPN, WEP, fifth-force, local-GR, measured-GM, or unified-field claim.

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the equality route is exact but not parent-derived.** If a parent topological/BF sector supplied a closed `J_M^top` and proved `J_M^top = Pi_M J_H + dB_zero` with zero boundary flux, then the projected Hilbert mass flux would close without a Hodge-projector stress trick. The current corpus does not contain that parent sector or equality theorem. The Hamiltonian route says the same thing in GR language: a conserved charge is not the source mass until `B_xi/G_eff = M_eff[Pi_M J_H]` is proven.

## Exact 915 Finding

The target theorem is:

```text
dJ_M^top = 0,
J_M^top = Pi_M J_H + dB_zero,
integral_boundary dB_zero = 0
=> d(Pi_M J_H) = 0.
```

The algebra is easy; the physics is not. The parent action must explain why the topological current is the observed Hilbert mass current, rather than a parallel silent label. Without that, the mismatch

```text
Delta_HT_current := J_M^top - Pi_M J_H - dB_zero
```

is the honest retained object.

Practical read: this is still alive, but it needs an actual parent mass-current sector next. Calling something topological is not enough; the topological current has to shake hands with the Hilbert current in the parent action.

## Non-Claim Summary
{md_table(summary)}

## Source Register
{md_table(sources)}

## Equality Derivation Attempt
{md_table(attempts)}

## Route Comparison
{md_table(routes)}

## Current-Mismatch Residual Pack
{md_table(residuals)}

## Branch Decision
{md_table(decisions)}

## Claim Gate
{md_table(gates)}

## Next Target
{md_table(next_rows)}

## Validation
{md_table(validation)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    sources = source_register_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    attempts = equality_derivation_attempt_rows(generated_utc)
    routes = route_comparison_rows(generated_utc)
    residuals = mismatch_residual_pack_rows(generated_utc)
    decisions = branch_decision_rows(generated_utc)
    gates = claim_gate_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)

    generated_tables = [sources, summary, attempts, routes, residuals, decisions, gates, next_rows]
    validation = validation_rows(generated_utc, sources, attempts, routes, residuals, gates, next_rows, generated_tables)
    generated_tables.append(validation)

    write_csv(OUT / "P8_Y5_R10_915_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_915_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_R10_915_EQUALITY_DERIVATION_ATTEMPT.csv", attempts)
    write_csv(OUT / "P8_Y5_R10_915_ROUTE_COMPARISON.csv", routes)
    write_csv(OUT / "P8_Y5_R10_915_CURRENT_MISMATCH_RESIDUAL_PACK.csv", residuals)
    write_csv(OUT / "P8_Y5_R10_915_BRANCH_DECISION.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_915_CLAIM_GATE.csv", gates)
    write_csv(OUT / "P8_Y5_R10_915_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_915_VALIDATION.csv", validation)
    write_doc(generated_utc, sources, summary, attempts, routes, residuals, decisions, gates, next_rows, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
