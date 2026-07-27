from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_911_parent_symplectic_current_contract_built_Delta_symp_bound_input_staged_nonclaim"
CLAIM_CEILING = "parent_symplectic_current_contract_and_Delta_symp_input_only_no_Htau_no_PiM_H_no_Newton_no_local_GR_claim"
NEXT_TARGET = "912-Y5-R10-EH-core-symplectic-baseline-vs-extra-sector-omega-ledger.md"

SOURCE_SPECS = [
    {
        "source_id": "910_doc",
        "path": ROOT / "910-Y5-R10-Hamiltonian-PiM-integrability-reference-subgate-or-retained-source-pack-fill.md",
        "needle": "the exact integrability obstruction is derived, but not zeroed",
        "role": "handoff demanding parent Theta/omega or retained Delta_symp",
    },
    {
        "source_id": "910_validation",
        "path": OUT / "P8_Y5_BRR545_910_VALIDATION.csv",
        "needle": "V910_10_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "910_obstruction_pack",
        "path": OUT / "P8_Y5_R10_910_OBSTRUCTION_PACK.csv",
        "needle": "OBS910_0_Delta_symp",
        "role": "Delta_symp and related obstruction rows",
    },
    {
        "source_id": "382_parent_action",
        "path": ROOT / "382-parent-local-action-minimal-contract.md",
        "needle": "S_parent =",
        "role": "minimal parent action sectors requiring variation",
    },
    {
        "source_id": "439_EH_ladder",
        "path": ROOT / "439-EH-only-exterior-parent-premise-ladder.md",
        "needle": "P6_second_order_metric_equations",
        "role": "EH-only premise ladder and metric-core dependencies",
    },
    {
        "source_id": "457_hamiltonian_contract",
        "path": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "needle": "HC2_differentiable_integrable_Hxi",
        "role": "Hamiltonian charge integrability and reference obligations",
    },
    {
        "source_id": "655_EH_audit",
        "path": OUT / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
        "needle": "EHP655_P6_second_order",
        "role": "current local-EH blockers that prevent borrowing EH charge machinery wholesale",
    },
    {
        "source_id": "789_Ward_Bianchi",
        "path": OUT / "P8_Y5_R10_789_VARIATION_WARD_IDENTITY_GATE.csv",
        "needle": "VWI789_3_Bianchi",
        "role": "Bianchi/Ward source compatibility",
    },
    {
        "source_id": "790_exchange_stress",
        "path": OUT / "P8_Y5_R10_790_EXCHANGE_STRESS_DECOMPOSITION.csv",
        "needle": "ESD790_1_exchange_longitudinal",
        "role": "exchange-current and hidden flux decomposition",
    },
    {
        "source_id": "908_retained_projector_vector",
        "path": OUT / "P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv",
        "needle": "RPV908_1_projector_divergence",
        "role": "retained q_P/T_projector source vector",
    },
    {
        "source_id": "909_retained_source_pack",
        "path": OUT / "P8_Y5_R10_909_RETAINED_PROJECTOR_SOURCE_PACK.csv",
        "needle": "RSP909_0_symplectic_integrability_residual",
        "role": "prior retained source pack that includes Delta_symp",
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
            "what_changed": "split the parent symplectic-current requirement into sector-by-sector Theta/omega obligations and staged a Delta_symp bound-input template",
            "best_partial_result": "the EH metric-core can be treated as a known baseline only after the parent action selects EH locally; every MTS/projector/domain/boundary/source sector still needs zero/gauge/topological/no-flux proof or a retained omega residual",
            "hard_blockers": "explicit parent Lagrangian by sector, sector symplectic potentials, boundary/corner terms, allowed variation space, hidden-sector omega silence, tau/reference rules, and source calibration",
            "what_is_not_claimed": "parent symplectic current, integrable H_tau, parent-owned Pi_M^H, EH local exterior, measured GM, Newtonian limit, PPN pass, or local GR",
            "decision": "use 911 as the formal contract for future parent-action work; proceed by evaluating EH-core omega separately from extra-sector omega",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def symplectic_current_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "sector_id": "PSC911_0_EH_metric_core",
            "parent_block": "S_EH_or_metric_core[g/e]",
            "must_supply": "Theta_EH and omega_EH for the observed metric/coframe core",
            "contract_form": "delta L_EH = E_EH^{mu nu} delta g_mu_nu + d Theta_EH; omega_EH=delta_1 Theta_EH(delta_2)-delta_2 Theta_EH(delta_1)",
            "current_status": "baseline_known_if_EH_parent_selected_not_currently_parent_derived",
            "if_failed_or_extra": "R11 non-EH operator vector and Delta_symp remain active",
        },
        {
            "sector_id": "PSC911_1_matter_one_coframe",
            "parent_block": "S_matter[Psi_A, ehat]",
            "must_supply": "Theta_matter and proof matter uses one observed coframe with no direct MTS spurions",
            "contract_form": "delta S_matter = E_Psi delta Psi + T_a^mu delta e_mu^a + d Theta_matter; no delta Z_I matter source outside ehat",
            "current_status": "MISSING_PARENT_MATTER_UNIVERSALITY_AND_THETA",
            "if_failed_or_extra": "WEP, clock, frame, and source-charge residuals remain active",
        },
        {
            "sector_id": "PSC911_2_selector_class",
            "parent_block": "S_selector_liftedC_class[g/e,C,P_D,class data]",
            "must_supply": "Theta_selector and Euler equations making selector/class data gauge/topological/owned",
            "contract_form": "delta S_selector = E_C delta C + E_class delta class + d Theta_selector",
            "current_status": "MISSING_SELECTOR_PARENT_LAGRANGIAN_AND_OMEGA",
            "if_failed_or_extra": "domain, preferred-location, and projected-metric residuals remain active",
        },
        {
            "sector_id": "PSC911_3_projector",
            "parent_block": "S_projector[P_D, relative chains, boundary data]",
            "must_supply": "Theta_projector and omega_projector or theorem that projector is topological/gauge with zero local flux",
            "contract_form": "delta S_projector = E_P delta P_D + d Theta_projector; integral_S i_tau omega_projector=0 or retained",
            "current_status": "MISSING_PROJECTOR_THETA_OMEGA_OR_ZERO_FLUX",
            "if_failed_or_extra": "q_P^nu, c_PiM_g, gamma/beta/alpha3/xi rows remain active",
        },
        {
            "sector_id": "PSC911_4_bulk_X_memory",
            "parent_block": "S_X[g/e,X,P,J_eff]",
            "must_supply": "Theta_X, mass-gap/no-hair theorem, or sourced finite-range force law",
            "contract_form": "delta S_X = E_X delta X + d Theta_X; exterior E_X=0/no-hair or alpha_X(lambda_X) residual",
            "current_status": "MISSING_BULK_X_THETA_MASS_GAP_AND_SOURCE_NORMALIZATION",
            "if_failed_or_extra": "bulk residual, fifth-force, gamma/beta, and Delta_symp rows remain active",
        },
        {
            "sector_id": "PSC911_5_boundary_corner",
            "parent_block": "S_boundary[g/e|partialD,Q_rel,M_eff,X,P_D,Y_partialD]",
            "must_supply": "Theta_boundary, corner terms, and class-only reference rule",
            "contract_form": "delta S_boundary = boundary equations + d Theta_boundary + corner terms; H_ref fixed by class",
            "current_status": "MISSING_BOUNDARY_CORNER_REFERENCE_RULE",
            "if_failed_or_extra": "Delta_ref, boundary beta/xi, radial hair, and Gdot rows remain active",
        },
        {
            "sector_id": "PSC911_6_domain_selector",
            "parent_block": "S_domain[chi_D,n_mu,L_cg,class/domain data]",
            "must_supply": "Theta_domain and covariance/no preferred-normal leakage",
            "contract_form": "delta S_domain = E_chi delta chi_D + E_n delta n + d Theta_domain; no unowned delta domain flux",
            "current_status": "MISSING_DOMAIN_THETA_AND_COVARIANT_SELECTOR_THEOREM",
            "if_failed_or_extra": "alpha1, alpha2, xi, domain-homology drift, and Delta_symp rows remain active",
        },
        {
            "sector_id": "PSC911_7_source_normalization",
            "parent_block": "S_source_norm[kappa,G_eff,M_eff,Pi_M J]",
            "must_supply": "Theta_source_norm or proof source-normalization variables are constants/constraints with no symplectic flux",
            "contract_form": "delta S_source_norm = E_kappa delta kappa + E_M delta M_eff + E_Pi delta(Pi_M J) + d Theta_source",
            "current_status": "MISSING_SOURCE_NORMALIZATION_THETA_OR_SUPERSELECTION",
            "if_failed_or_extra": "dln_Geff_dt, dln_Meff_dt, epsilon_charge, epsilon_orbit, and R10 rows remain active",
        },
        {
            "sector_id": "PSC911_8_connection_torsion",
            "parent_block": "connection/spin-connection sector",
            "must_supply": "Theta_connection and Euler equation forcing Levi-Civita/no torsion or retained spin/torsion residual",
            "contract_form": "delta S_connection = E_omega delta omega + d Theta_connection; torsion/nonmetricity zero or retained",
            "current_status": "MISSING_CONNECTION_VARIATION_AND_THETA",
            "if_failed_or_extra": "spin, clock, WEP, light-cone, and R11 connection rows remain active",
        },
    ]
    for row in rows:
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def eh_vs_extra_omega_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "split_id": "EVE911_0_EH_baseline",
            "piece": "omega_EH",
            "status": "usable_as_baseline_only_if_parent_selects_EH_core",
            "why": "standard GR charge machinery can define a baseline symplectic current, but MTS must first prove the local exterior really reduces to the EH metric core",
            "next_use": "compare EH-core obstruction with extra-sector omega in 912",
        },
        {
            "split_id": "EVE911_1_matter_baseline",
            "piece": "omega_matter",
            "status": "conditional_on_one_observed_coframe",
            "why": "matter symplectic flux is harmless for local GR only when matter uses the same observed frame and no direct MTS spurions",
            "next_use": "feed WEP/clock/source-frame gates if not parent-signed",
        },
        {
            "split_id": "EVE911_2_extra_sector_sum",
            "piece": "omega_extra = omega_selector + omega_projector + omega_X + omega_boundary + omega_domain + omega_source + omega_connection",
            "status": "active_primary_obstruction",
            "why": "every extra sector can contribute to integral_S i_tau omega unless it is gauge/topological/no-haired/boundary-silent or retained",
            "next_use": "turn into Delta_symp_extra and q_P/source residual rows",
        },
        {
            "split_id": "EVE911_3_total_obstruction",
            "piece": "Delta_symp_total",
            "status": "retained_unfilled",
            "why": "Delta_symp_total must envelope EH-reference, matter-frame, and all extra-sector symplectic flux until parent omega is evaluated",
            "next_use": "bound-input row if derivation route stalls",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def delta_symp_input_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "input_id": "DSI911_0_total_Delta_symp",
            "symbol": "Delta_symp_total",
            "definition": "mass-normalized envelope of all non-EH or non-integrable boundary symplectic obstruction terms",
            "formula": "(|int_S i_tau omega_total| + |delta_tau_terms| + |delta H_ref|)/M_ref",
            "units": "dimensionless",
            "observable_link": "measured GM drift; beta source; Gdot/G; boundary/reference residuals",
            "bound_or_target": "derived_zero_or_local_source_normalization_bound",
            "required_input": "parent omega_total and allowed phase space, or source-backed upper bound",
            "current_value": "MISSING_PARENT_OMEGA_OR_BOUND",
        },
        {
            "input_id": "DSI911_1_extra_sector_Delta_symp",
            "symbol": "Delta_symp_extra",
            "definition": "mass-normalized symplectic obstruction from projector/domain/boundary/bulk/source/connection sectors",
            "formula": "|int_S i_tau omega_extra|/M_ref",
            "units": "dimensionless",
            "observable_link": "q_P^nu; c_PiM_g; mu_extra; alpha3; xi; R11 operator ledger",
            "bound_or_target": "derived_zero_or_channelwise_local_bound",
            "required_input": "sector omega rows or coefficient map",
            "current_value": "MISSING_EXTRA_SECTOR_OMEGA",
        },
        {
            "input_id": "DSI911_2_reference_shift",
            "symbol": "Delta_ref",
            "definition": "class/reference subtraction drift contaminating H_tau",
            "formula": "|delta H_ref|/M_ref",
            "units": "dimensionless",
            "observable_link": "radial source hair; measured GM offset; beta/xi boundary rows",
            "bound_or_target": "fixed_reference_theorem_or_bound",
            "required_input": "class-only H_ref rule or numeric reference-shift bound",
            "current_value": "MISSING_FIXED_REFERENCE_RULE",
        },
        {
            "input_id": "DSI911_3_tau_frame",
            "symbol": "Delta_tau_frame",
            "definition": "observed-time generator/frame mismatch contribution to Hamiltonian charge variation",
            "formula": "|delta_tau_terms|/M_ref",
            "units": "dimensionless",
            "observable_link": "clock redshift; preferred-frame PPN; frame calibration split",
            "bound_or_target": "tau_fixed_theorem_or_clock_frame_bound",
            "required_input": "same-frame tau normalization theorem or residual value",
            "current_value": "MISSING_TAU_FRAME_INPUT",
        },
        {
            "input_id": "DSI911_4_calibration_tail",
            "symbol": "Delta_cal",
            "definition": "post-integrability source/orbital calibration tail",
            "formula": "|epsilon_charge|+|epsilon_orbit|+|epsilon_Gauss|",
            "units": "dimensionless",
            "observable_link": "source-normalized Newton; R10; radial hair; PPN source stability",
            "bound_or_target": "derived_zero_or_filled_source_normalization_scorecard",
            "required_input": "charge-current equality and Gauss/orbital calibration rows",
            "current_value": "MISSING_SOURCE_CALIBRATION_INPUTS",
        },
    ]
    for row in rows:
        row["score_ready"] = False
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD911_0_contract",
            "branch": "parent_symplectic_current_contract",
            "verdict": "contract_built_not_satisfied",
            "reason": "sector-by-sector Theta/omega obligations are explicit, but no explicit parent Lagrangian or sector symplectic potentials are supplied",
            "policy": "do not claim integrable H_tau or Pi_M^H from formal identities alone",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "BD911_1_next_derivation",
            "branch": "EH_core_vs_extra_omega_split",
            "verdict": "selected_next",
            "reason": "the most surgical next move is to isolate the known EH-core baseline and audit every extra sector as an omega contribution or theorem-zero",
            "policy": "if extra omega cannot be zeroed, fill Delta_symp_extra and q_P/source residual rows",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE911_0_parent_Theta", "parent symplectic potential Theta supplied", "blocked: no explicit parent Lagrangian variation by sector"),
        ("CGATE911_1_parent_omega", "parent symplectic current omega supplied", "blocked: sector omega rows are contractual, not evaluated"),
        ("CGATE911_2_integrable_Htau", "integrable H_tau", "blocked: Delta_symp_total is missing parent omega or bound"),
        ("CGATE911_3_PiM_H", "parent-owned Pi_M^H", "blocked: integrability and source equality are not proven"),
        ("CGATE911_4_EH_local_exterior", "EH local exterior", "blocked: EH-core baseline is not parent-selected and extra sectors are active"),
        ("CGATE911_5_Newton_local_GR", "measured GM/Newton/PPN/local GR", "blocked: source calibration and PPN rows remain unfilled"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "claim_allowed": False,
            "blocker": blocker,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for gate_id, claim, blocker in gates
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "separate the EH metric-core symplectic baseline from all extra-sector omega contributions, then decide whether extra omega is theorem-zero/gauge/topological/no-flux or retained as Delta_symp_extra",
            "include": "EH-core Theta/omega baseline, matter-frame omega, projector/domain/boundary/source/connection omega ledger, Delta_symp_extra normalization, claim gates",
            "exclude": "claiming parent action exists, assuming extra omega vanishes, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_910_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_910_VALIDATION.csv")
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > CUTOFF:
            count += 1
    return count


def all_generated_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for group in row_groups:
        for row in group:
            if "valid_for_claim" in row and stringify(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and stringify(row["claim_allowed"]).lower() != "false":
                return False
            if "score_ready" in row and stringify(row["score_ready"]).lower() != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    contract_rows_: list[dict[str, object]],
    split_rows_: list[dict[str, object]],
    input_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        contract_rows_,
        split_rows_,
        input_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V911_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V911_1_prior_910_clean",
            "result": "pass" if prior_910_clean() else "fail",
            "detail": "P8_Y5_BRR545_910_VALIDATION.csv clean",
        },
        {
            "check_id": "V911_2_all_parent_sectors_have_contract_rows",
            "result": "pass" if len(contract_rows_) >= 8 else "fail",
            "detail": f"sector_contract_rows={len(contract_rows_)}",
        },
        {
            "check_id": "V911_3_EH_baseline_not_promoted",
            "result": "pass"
            if any(row["piece"] == "omega_EH" and "only_if_parent_selects_EH_core" in stringify(row["status"]) for row in split_rows_)
            else "fail",
            "detail": "EH symplectic baseline is conditional, not borrowed as a full MTS proof",
        },
        {
            "check_id": "V911_4_extra_omega_active",
            "result": "pass"
            if any(row["piece"].startswith("omega_extra") and row["status"] == "active_primary_obstruction" for row in split_rows_)
            else "fail",
            "detail": "extra-sector omega remains the primary obstruction",
        },
        {
            "check_id": "V911_5_Delta_symp_inputs_nonclaim",
            "result": "pass"
            if input_rows_
            and all(row["valid_for_claim"] is False and row["score_ready"] is False and "MISSING_" in stringify(row["current_value"]) for row in input_rows_)
            else "fail",
            "detail": "Delta_symp bound-input rows remain missing-input and invalid for claim",
        },
        {
            "check_id": "V911_6_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all Theta/omega/Htau/PiM/Newton/local-GR claim gates remain false",
        },
        {
            "check_id": "V911_7_all_generated_rows_nonclaim",
            "result": "pass" if all_generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed/score_ready false where present",
        },
        {
            "check_id": "V911_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V911_9_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V911_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows_: list[dict[str, object]],
    source_rows_: list[dict[str, object]],
    contract_rows_: list[dict[str, object]],
    split_rows_: list[dict[str, object]],
    input_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 911 - Y5/R10 Parent Symplectic Current Minimal Contract Or Delta Symp Bound Input

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the parent `Theta/omega` bill is now sector-by-sector.** The EH metric-core symplectic current can serve as a baseline only after the parent action actually selects an EH local exterior. It cannot silence the MTS/projector/domain/boundary/source sectors. Those extra sectors must either have zero/gauge/topological/no-flux symplectic current or appear inside `Delta_symp`/local residual rows.

## Exact 911 Finding
The integrability obstruction from 910 becomes the concrete contract:

```text
omega_total =
  omega_EH
  + omega_matter
  + omega_selector
  + omega_projector
  + omega_X
  + omega_boundary
  + omega_domain
  + omega_source
  + omega_connection.
```

For `H_tau` and `Pi_M^H` to be parent-owned, the parent theory must evaluate `integral_S i_tau omega_total`. If only `omega_EH` is known, the proof is incomplete. The next derivation fork is therefore clean: separate EH-core baseline from extra-sector omega, then zero or retain the extras.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Parent Symplectic Current Contract
{md_table(contract_rows_)}

## EH Core vs Extra-Sector Omega Split
{md_table(split_rows_)}

## Delta Symp Bound Input Template
{md_table(input_rows_)}

## Branch Decision
{md_table(decision_rows_)}

## Claim Gate
{md_table(claim_rows_)}

## Next Target
{md_table(next_rows_)}

## Validation
{md_table(validation_rows_)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    contract_rows_ = symplectic_current_contract_rows(generated_utc)
    split_rows_ = eh_vs_extra_omega_rows(generated_utc)
    input_rows_ = delta_symp_input_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        contract_rows_,
        split_rows_,
        input_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_911_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_911_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_911_PARENT_SYMPLECTIC_CURRENT_CONTRACT.csv": contract_rows_,
        "P8_Y5_R10_911_EH_CORE_VS_EXTRA_OMEGA_SPLIT.csv": split_rows_,
        "P8_Y5_R10_911_DELTA_SYMP_BOUND_INPUT_TEMPLATE.csv": input_rows_,
        "P8_Y5_R10_911_BRANCH_DECISION.csv": decision_rows_,
        "P8_Y5_R10_911_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_911_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_BRR545_911_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "911-Y5-R10-parent-symplectic-current-minimal-contract-or-Delta-symp-bound-input.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        contract_rows_,
        split_rows_,
        input_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_911_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
