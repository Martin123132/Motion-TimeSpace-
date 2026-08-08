from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3754"
BRANCH = "MTS_R2FR_Y5_SOURCE_WARD_POISSON_CALIBRATION_LAW_3754"
PCW = Path(__file__).resolve().parents[1]
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3754-Y5-R2FR-source-Ward-Poisson-calibration-law.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": False,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3754_0_3753_next": RESIDUALS / "P8_Y5_R2FR_3753_NEXT_TARGET.csv",
        "SRC3754_1_3753_checks": RESIDUALS / "P8_Y5_R2FR_3753_PROJECTOR_THEOREM_CHECKS.csv",
        "SRC3754_2_3753_coupling": RESIDUALS / "P8_Y5_R2FR_3753_REDUCED_HOP_AND_SOURCE_COUPLING.csv",
        "SRC3754_3_flux_contract": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "SRC3754_4_source_ward": RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv",
        "SRC3754_5_ward_owner": RESIDUALS / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "SRC3754_6_poisson_gauss": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "SRC3754_7_hilbert_monopole": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "SRC3754_8_global_coupling": RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv",
        "SRC3754_9_meff_flux": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "SRC3754_10_residual_map": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "SRC3754_11_poisson_gates": RESIDUALS / "P8_Y5_R2FR_3530_POISSON_PPN_GATES.csv",
        "SRC3754_12_newton_bounds": RESIDUALS / "P8_Y5_R2FR_3530_NEWTON_PPN_BOUND_ROWS.csv",
        "SRC3754_13_completion_gates": RESIDUALS / "P8_Y5_R2FR_3624_NEWTON_PPN_COMPLETION_GATES.csv",
        "SRC3754_14_constant_gm": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
    }


def source_register(ts: str) -> list[dict[str, object]]:
    purpose = {
        "SRC3754_0_3753_next": "imports 3754 objective",
        "SRC3754_1_3753_checks": "imports open Ward/Newton gaps",
        "SRC3754_2_3753_coupling": "imports M_eff and mu_obs coupling interface",
        "SRC3754_3_flux_contract": "imports Pi_M flux closure requirements",
        "SRC3754_4_source_ward": "imports Hilbert source Ward universality contract",
        "SRC3754_5_ward_owner": "imports owned-divergence/source residual contract",
        "SRC3754_6_poisson_gauss": "imports Hamiltonian/Poisson/Gauss calibration contract",
        "SRC3754_7_hilbert_monopole": "imports Hilbert monopole calibration contract",
        "SRC3754_8_global_coupling": "imports constant universal coupling contract",
        "SRC3754_9_meff_flux": "imports source-measure/Meff flux theorem",
        "SRC3754_10_residual_map": "imports residual map if flux theorem fails",
        "SRC3754_11_poisson_gates": "imports 3530 Newton/Poisson gates",
        "SRC3754_12_newton_bounds": "imports local bound rows for source-normalized Newton",
        "SRC3754_13_completion_gates": "imports 3624 local GR/Newton completion gates",
        "SRC3754_14_constant_gm": "imports constant-GM residual matrix",
    }
    return [
        {
            **base(ts),
            "source_id": key,
            "source_path": str(path),
            "purpose": purpose[key],
            "exists": path.exists(),
            "claim_allowed": False,
        }
        for key, path in source_paths().items()
    ]


def ward_law_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "WL3754_0_same_frame_source",
            "J_H[tau] is the Hilbert/coframe source current from the same observed matter action and same observed time generator tau.",
            "definition_bridge",
            "requires same-frame matter/source theorem",
            "source current is not fitted after orbital readout",
        ),
        (
            "WL3754_1_noether_identity",
            "For a diffeomorphism-invariant parent matter action on matter shell, nabla_mu T_H^{mu nu}=q_exchange^nu, with q_exchange^nu=0 only when all non-Hilbert/exchange owners are absent or mapped.",
            "conditional_ward_law",
            "requires explicit source action and exchange owner ledger",
            "does not hide q_exchange",
        ),
        (
            "WL3754_2_observed_time_current",
            "If tau or xi is an observed stationary/Killing/Hamiltonian generator, j_M^mu=T_H^{mu nu}xi_nu obeys nabla_mu j_M^mu = xi_nu q_exchange^nu plus generator-normalization terms.",
            "conditional_mass_current_law",
            "requires stationary/Hamiltonian local branch",
            "converts tensor Ward law to scalar mass-current law",
        ),
        (
            "WL3754_3_projected_current",
            "With the 3753 topological projector, J_M=Pi_M J_H has dJ_M=Pi_M dJ_H because dPi_M=0 in the parent topological block.",
            "projector_step_derived",
            "requires 3753 topology signature",
            "projector no longer creates its own flux term",
        ),
        (
            "WL3754_4_charge_rate",
            "For a worldtube slab C between two linking surfaces, Delta ell_M(J_H)=int_C dJ_M = -Phi_side + int_C Pi_M q_exchange.",
            "stokes_balance_law",
            "requires fixed homology/worldtube orientation",
            "exactly identifies what must vanish or be bounded",
        ),
        (
            "WL3754_5_conservation_condition",
            "d ell_M(J_H)=0 follows if Phi_side=0 and Pi_M q_exchange=0.",
            "exact_conditional_closure",
            "requires no side flux and no projected exchange current",
            "mass flux closure is now a two-clause theorem, not an axiom",
        ),
        (
            "WL3754_6_flux_bound",
            "|d ln M_eff/dt| <= (|Phi_side|+int|Pi_M q_exchange|)/(abs(ell_M(J_H))*Delta t)",
            "fallback_bound",
            "requires source flux units and normalization",
            "feeds Gdot/orbital/source residual rows if nonzero",
        ),
    ]
    return [
        {
            **base(ts),
            "law_id": law_id,
            "law_or_derivation": law,
            "status": status,
            "required_inputs": required,
            "impact": impact,
            "claim_allowed": False,
        }
        for law_id, law, status, required, impact in rows
    ]


def poisson_calibration_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "PC3754_0_parent_field_equation",
            "G_mn + Lambda g_mn = kappa_eff T_H_mn + DeltaE_res_mn",
            "conditional_field_equation",
            "requires EH dominance and residual tensor mapped",
            "starts Newton calibration only after local operator side is controlled",
        ),
        (
            "PC3754_1_weak_field_00",
            "In the same observed frame and nonrelativistic limit, G_00 ~= 2 nabla^2 Phi/c^2 and T_00 ~= rho_H c^2.",
            "standard_weak_field_bridge",
            "requires same-frame metric/readout and slow-source limit",
            "comparator grammar for Newton limit",
        ),
        (
            "PC3754_2_poisson_coefficient",
            "nabla^2 Phi = (kappa_eff c^4/2) rho_H + Delta_Poisson = 4 pi G_eff rho_H + Delta_Poisson.",
            "derived_coefficient_law",
            "defines G_eff := kappa_eff c^4/(8 pi)",
            "this is the clean GR-to-Newton coefficient bridge",
        ),
        (
            "PC3754_3_topological_mass_density",
            "M_eff := k_M ell_M(J_H), rho_eff := k_M q_M where q_M is the local density of the projected charge current.",
            "source_charge_definition",
            "requires k_M source normalization from parent matter/source units",
            "ties 3753 topological charge to source density",
        ),
        (
            "PC3754_4_gauss_monopole",
            "For a closed source with zero residual flux, surface_integral grad Phi dot dS = 4 pi G_eff M_eff.",
            "conditional_gauss_law",
            "requires Delta_Poisson volume term and boundary/source residuals vanish or are bounded",
            "turns closed charge into exterior monopole",
        ),
        (
            "PC3754_5_orbital_readout",
            "a_r=-partial_r Phi=-G_eff M_eff/r^2 + a_res, so mu_obs=G_eff M_eff + mu_extra.",
            "derived_readout_identity",
            "requires slow-body geodesic limit and no fifth-force/source hair",
            "keeps measured GM separate from fitted readout",
        ),
        (
            "PC3754_6_G_value_policy",
            "The numerical value of G_eff is not derived unless kappa_eff or k_M is predicted by the parent action; otherwise only universality and derivative silence can be claimed.",
            "anti_overclaim_policy",
            "requires parent absolute coupling normalization to predict G itself",
            "matches how GR uses kappa rather than deriving measured G",
        ),
    ]
    return [
        {
            **base(ts),
            "calibration_id": calibration_id,
            "equation_or_statement": equation,
            "status": status,
            "required_inputs": required,
            "impact": impact,
            "claim_allowed": False,
        }
        for calibration_id, equation, status, required, impact in rows
    ]


def residual_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "RES3754_0_mass_flux",
            "dln_Meff_dt",
            "(Phi_side + Pi_M q_exchange volume)/M_eff",
            "Gdot/orbital/source-normalization",
            "score against Gdot or zero theorem",
        ),
        (
            "RES3754_1_poisson_residual",
            "Delta_Poisson",
            "DeltaE_res_00 plus non-Hilbert/source residual terms in weak-field limit",
            "Newton/PPN gamma beta",
            "requires operator residual projection",
        ),
        (
            "RES3754_2_mu_extra",
            "mu_extra/(G_eff M_eff)",
            "boundary + bulk + domain + memory + range + connection monopole corrections",
            "Kepler, R10, PPN, source normalization",
            "absolute no-cancellation residual",
        ),
        (
            "RES3754_3_Gdot",
            "dln_Geff_dt",
            "dln kappa_eff_dt plus any source-unit drift",
            "LLR/Gdot",
            "bound target 9.6e-15 yr^-1 from existing local bound rows",
        ),
        (
            "RES3754_4_species",
            "eta_source_AB",
            "composition dependence of k_M, kappa_eff, or ell_M source weighting",
            "WEP/source charge",
            "bound target 2.8e-15 dimensionless from existing local bound rows",
        ),
        (
            "RES3754_5_range_radial",
            "partial_r ln mu_obs and alpha(lambda)",
            "radial/range dependence of coupling or extra source channel",
            "inverse-square/R10",
            "needs no-range theorem or alpha(lambda) curve",
        ),
        (
            "RES3754_6_frame",
            "Delta_frame_source",
            "source frame differs from orbital/clock frame",
            "WEP/clocks/preferred-frame",
            "same observed coframe theorem or residual bound",
        ),
        (
            "RES3754_7_beta_source",
            "delta_beta_source",
            "second-order source-normalization correction",
            "PPN beta",
            "cannot promote Newton-only result to local GR without this",
        ),
    ]
    return [
        {
            **base(ts),
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "test_arena": arena,
            "required_bound_or_zero": required,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for residual_id, symbol, definition, arena, required in rows
    ]


def ladder_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("LAD3754_0_projector", "Pi_M topological projector", "closed by 3753 signature conditionally", "PASSED_CONDITIONAL"),
        ("LAD3754_1_ward", "d ell_M(J_H)=0", "derived iff no side flux and no projected exchange", "CONDITIONAL_NOT_PARENT_SIGNED"),
        ("LAD3754_2_mass", "M_eff=k_M ell_M(J_H)", "definition requires parent source units k_M", "DEFINITION_READY_KM_OPEN"),
        ("LAD3754_3_EH", "EH left-hand dominance", "needed before Poisson coefficient counts", "CONDITIONAL_NOT_PARENT_SIGNED"),
        ("LAD3754_4_poisson", "nabla^2 Phi=4*pi*G_eff rho_eff", "coefficient law derived if EH/source residuals vanish", "DERIVED_CONDITIONAL"),
        ("LAD3754_5_G", "G_eff=kappa_eff c^4/(8*pi)", "universality/constancy not yet parent-derived", "GLOBAL_COUPLING_OPEN"),
        ("LAD3754_6_orbit", "mu_obs=G_eff M_eff", "requires zero mu_extra and no radial/range hair", "OPEN"),
        ("LAD3754_7_ppn", "gamma,beta,etc.", "requires second-order residual vector", "OPEN"),
    ]
    return [
        {
            **base(ts),
            "ladder_id": ladder_id,
            "rung": rung,
            "current_result": result,
            "status": status,
            "claim_allowed": False,
        }
        for ladder_id, rung, result, status in rows
    ]


def claim_gate_rows(ts: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(bool(row["exists"]) for row in grouped["sources"])
    ward_balance = any(row["law_id"] == "WL3754_4_charge_rate" and row["status"] == "stokes_balance_law" for row in grouped["ward_laws"])
    poisson_coeff = any(row["calibration_id"] == "PC3754_2_poisson_coefficient" and row["status"] == "derived_coefficient_law" for row in grouped["poisson"])
    residuals = len(grouped["residuals"]) == 8
    gates = [
        ("CG3754_0_sources", "all 3754 source paths exist", all_sources, "path hygiene"),
        ("CG3754_1_ward_balance", "mass-charge Stokes/Ward balance derived", ward_balance, "d ell_M law now has explicit flux/exchange terms"),
        ("CG3754_2_flux_zero", "mass flux closure d ell_M=0 fully proved", False, "requires no side flux and no projected exchange theorem"),
        ("CG3754_3_poisson_coeff", "EH-to-Poisson coefficient bridge derived", poisson_coeff, "G_eff := kappa_eff c^4/(8*pi)"),
        ("CG3754_4_constant_G", "constant universal G_eff parent-derived", False, "global coupling superselection still open"),
        ("CG3754_5_mu_obs", "mu_obs=G_eff M_eff with mu_extra=0 proved", False, "mu_extra/range/radial rows remain open"),
        ("CG3754_6_residual_vector", "fallback residual vector emitted", residuals, "keeps failed coupling premises testable"),
        ("CG3754_7_local_newton", "Newton inverse-square source calibration claim allowed", False, "not until CG3754_2,4,5 pass"),
        ("CG3754_8_local_gr", "local GR/PPN claim allowed", False, "second-order PPN and full residual vector still open"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in gates
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3754_0_real_advance",
            "WARD_BALANCE_AND_POISSON_COEFFICIENT_DERIVED_CONDITIONALLY",
            "3754 turns coupling into equations: charge drift equals side flux plus projected exchange, and the EH weak-field coefficient gives G_eff=kappa_eff c^4/(8*pi).",
        ),
        (
            "DEC3754_1_no_magic_G",
            "NUMERICAL_G_NOT_DERIVED",
            "Without a parent absolute kappa/k_M normalization theorem, MTS can aim to derive universality and silence of derivative/source hair, not the measured number of G.",
        ),
        (
            "DEC3754_2_key_blocker",
            "GLOBAL_COUPLING_SUPERSELECTION_AND_NO_FLUX",
            "The next hard pieces are constant universal kappa_eff and no projected source/exchange flux.",
        ),
        (
            "DEC3754_3_testing_path",
            "FAILED_COUPLING_PREMISES_MAP_TO_GDOT_WEP_R10_ORBITAL",
            "If any coupling premise fails, it becomes a residual row rather than a hidden calibration.",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for decision_id, decision, meaning in rows
    ]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3754_0",
            "target_doc": "3755-Y5-R2FR-global-kappa-superselection-or-coupling-residual-vector.md",
            "target_script": "scripts/Y5_R2FR_3755_global_kappa_superselection_or_coupling_residual_vector.py",
            "objective": "prove kappa_eff/G_eff is a global source-blind, range-blind, time/radius/frame independent coupling sector, or emit executable Gdot/WEP/R10/radial/source residual rows",
            "why_this_next": "3754 shows Newton calibration hinges on constant universal coupling once the source charge ladder is written",
            "claim_allowed": False,
        }
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "STATUS3754_0",
            "status": "WARD_BALANCE_POISSON_COEFFICIENT_DERIVED_CONSTANT_COUPLING_OPEN",
            "summary": "3754 derives the source-charge balance law and the EH-to-Poisson coefficient bridge, but leaves no-flux/projected-exchange closure and constant universal coupling open. Newton/local-GR claims remain blocked.",
            "claim_allowed": False,
        }
    ]


def validation_rows(ts: str, paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    checks = [
        ("sources_exist", "all 3754 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("csv_parse", "all generated CSVs parse", all(len(read_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("ward_balance", "Ward/Stokes balance emitted", any(row["law_id"] == "WL3754_4_charge_rate" for row in grouped["ward_laws"])),
        ("flux_bound", "flux fallback bound emitted", any(row["law_id"] == "WL3754_6_flux_bound" for row in grouped["ward_laws"])),
        ("poisson_coeff", "Poisson coefficient bridge emitted", any(row["calibration_id"] == "PC3754_2_poisson_coefficient" for row in grouped["poisson"])),
        ("G_policy", "no-magic-G policy emitted", any(row["calibration_id"] == "PC3754_6_G_value_policy" for row in grouped["poisson"])),
        ("residual_vector", "eight coupling residual rows emitted", len(grouped["residuals"]) == 8),
        ("claim_blocked", "local GR claim remains false", any(row["gate_id"] == "CG3754_8_local_gr" and row["passed"] is False for row in grouped["claim_gates"])),
        ("next_target", "3755 kappa target emitted", grouped["next_target"][0]["target_doc"] == "3755-Y5-R2FR-global-kappa-superselection-or-coupling-residual-vector.md"),
        ("no_formalization_leak", "no 3754 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3754*"))),
    ]
    return [
        {
            **base(ts),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": "",
        }
        for validation_id, description, passed in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3754 — Source Ward / Poisson Calibration Law",
        "",
        "## Status",
        "",
        "`WARD_BALANCE_POISSON_COEFFICIENT_DERIVED_CONSTANT_COUPLING_OPEN`.",
        "",
        "This checkpoint attacks the coupling issue directly. The projector can define the mass channel, but Newtonian mechanics needs both a source Ward/no-flux law and a same-frame EH/Poisson calibration.",
        "",
        "## Ward / Flux Law",
    ]
    for row in grouped["ward_laws"]:
        lines.append(f"- `{row['law_id']}` `{row['status']}`: {row['law_or_derivation']}")
    lines.extend(["", "## Poisson Calibration"])
    for row in grouped["poisson"]:
        lines.append(f"- `{row['calibration_id']}` `{row['status']}`: {row['equation_or_statement']}")
    lines.extend(["", "## Coupling Ladder"])
    for row in grouped["ladder"]:
        lines.append(f"- `{row['ladder_id']}` `{row['status']}`: {row['rung']} — {row['current_result']}")
    lines.extend(["", "## Residuals If A Rung Fails"])
    for row in grouped["residuals"]:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}`: {row['definition']} -> {row['test_arena']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} — {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}`: {row['meaning']}")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Source Register"])
    for row in grouped["sources"]:
        lines.append(f"- `{row['source_id']}` exists=`{row['exists']}`: `{row['source_path']}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ts = now()
    paths = {
        "doc": DOC_PATH,
        "sources": RESIDUALS / "P8_Y5_R2FR_3754_SOURCE_REGISTER.csv",
        "ward_laws": RESIDUALS / "P8_Y5_R2FR_3754_SOURCE_WARD_FLUX_LAW_ROWS.csv",
        "poisson": RESIDUALS / "P8_Y5_R2FR_3754_POISSON_CALIBRATION_ROWS.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3754_COUPLING_RESIDUAL_ROWS.csv",
        "ladder": RESIDUALS / "P8_Y5_R2FR_3754_COUPLING_LADDER_STATUS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3754_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3754_DECISION_ROWS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3754_NEXT_TARGET.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3754_STATUS.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3754_VALIDATION.csv",
    }
    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(ts),
        "ward_laws": ward_law_rows(ts),
        "poisson": poisson_calibration_rows(ts),
        "residuals": residual_rows(ts),
        "ladder": ladder_rows(ts),
        "decisions": decision_rows(ts),
        "next_target": next_target_rows(ts),
        "status": status_rows(ts),
    }
    grouped["claim_gates"] = claim_gate_rows(ts, grouped)
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(ts, paths, grouped)
    write_csv(paths["validation"], grouped["validation"])
    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3754 validation failed: {failures}")
    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists() and str(cache.resolve()).startswith(str(PCW.resolve())):
        shutil.rmtree(cache)
    print("wrote 3754 checkpoint: Ward balance and Poisson coefficient derived conditionally; constant coupling open")


if __name__ == "__main__":
    main()
