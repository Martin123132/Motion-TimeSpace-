from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_912_EH_core_symplectic_baseline_separated_extra_sector_omega_ledger_retained_nonclaim"
CLAIM_CEILING = "EH_core_symplectic_baseline_and_extra_omega_ledger_only_no_parent_action_no_Htau_no_PiM_H_no_local_GR_claim"
NEXT_TARGET = "913-Y5-R10-projector-omega-zero-route-or-Delta-symp-extra-source-row.md"

SOURCE_SPECS = [
    {
        "source_id": "911_doc",
        "path": ROOT / "911-Y5-R10-parent-symplectic-current-minimal-contract-or-Delta-symp-bound-input.md",
        "needle": "the parent `Theta/omega` bill is now sector-by-sector",
        "role": "handoff selecting EH-core versus extra-sector omega split",
    },
    {
        "source_id": "911_validation",
        "path": OUT / "P8_Y5_BRR545_911_VALIDATION.csv",
        "needle": "V911_10_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "911_split",
        "path": OUT / "P8_Y5_R10_911_EH_CORE_VS_EXTRA_OMEGA_SPLIT.csv",
        "needle": "EVE911_2_extra_sector_sum",
        "role": "EH-core and extra-sector split to refine",
    },
    {
        "source_id": "911_contract",
        "path": OUT / "P8_Y5_R10_911_PARENT_SYMPLECTIC_CURRENT_CONTRACT.csv",
        "needle": "PSC911_3_projector",
        "role": "sector-by-sector symplectic current contract",
    },
    {
        "source_id": "439_EH_ladder",
        "path": ROOT / "439-EH-only-exterior-parent-premise-ladder.md",
        "needle": "Lovelock Selection Contract",
        "role": "conditional route for EH-core selection",
    },
    {
        "source_id": "655_EH_audit",
        "path": OUT / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
        "needle": "EHP655_P6_second_order",
        "role": "current EH-core selection blockers",
    },
    {
        "source_id": "908_projector_vector",
        "path": OUT / "P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv",
        "needle": "RPV908_1_projector_divergence",
        "role": "projector/Bianchi residual that should be attacked first",
    },
    {
        "source_id": "790_exchange_stress",
        "path": OUT / "P8_Y5_R10_790_EXCHANGE_STRESS_DECOMPOSITION.csv",
        "needle": "ESD790_1_exchange_longitudinal",
        "role": "exchange-current carrier debt for nonzero extra omega",
    },
    {
        "source_id": "910_obstruction_pack",
        "path": OUT / "P8_Y5_R10_910_OBSTRUCTION_PACK.csv",
        "needle": "OBS910_0_Delta_symp",
        "role": "Delta_symp obstruction normalization",
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
            "what_changed": "separated a conditional EH-core symplectic baseline from the active extra-sector omega ledger",
            "best_partial_result": "standard EH charge machinery can now be used as the comparison baseline, but only after EH-core selection; projector omega is the first active extra-sector target",
            "hard_blockers": "EH-core parent selection, matter one-frame proof, projector omega zero/flux theorem, boundary/corner reference, domain covariance, source-normalization superselection, and connection/torsion silence",
            "what_is_not_claimed": "parent action, EH local exterior, extra-sector omega zero, integrable H_tau, parent-owned Pi_M^H, measured GM, Newtonian limit, PPN pass, or local GR",
            "decision": "attack projector omega first because it is already tied to q_P^nu/T_projector and the Bianchi residual stack",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def eh_core_baseline_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "baseline_id": "EHB912_0_EH_variation",
            "object": "Theta_EH",
            "baseline_form": "delta L_EH = (sqrt(-g)/(2 kappa))(G_mn + Lambda g_mn) delta g^mn + d Theta_EH",
            "what_it_gives": "standard metric-core symplectic potential once EH core and conventions are selected",
            "condition_before_use": "parent derives local EH metric/core branch in the observed frame",
            "current_status": "conditional_baseline_not_parent_selected",
        },
        {
            "baseline_id": "EHB912_1_EH_symplectic_current",
            "object": "omega_EH",
            "baseline_form": "omega_EH(delta_1,delta_2)=delta_1 Theta_EH(delta_2)-delta_2 Theta_EH(delta_1)",
            "what_it_gives": "baseline contribution to integral_S i_tau omega for Hamiltonian charge integrability",
            "condition_before_use": "allowed variations are EH metric variations with fixed boundary/reference class",
            "current_status": "conditional_baseline_not_full_MTS_omega",
        },
        {
            "baseline_id": "EHB912_2_EH_charge_form",
            "object": "k_tau^EH",
            "baseline_form": "delta H_tau^EH = integral_S(delta Q_tau^EH - i_tau Theta_EH)",
            "what_it_gives": "standard boundary charge variation for GR-like local exterior",
            "condition_before_use": "tau fixed, EH constraints on shell, boundary/corner reference fixed",
            "current_status": "conditional_charge_form_only",
        },
        {
            "baseline_id": "EHB912_3_EH_does_not_silence_extras",
            "object": "omega_total",
            "baseline_form": "omega_total = omega_EH + omega_matter + omega_extra",
            "what_it_gives": "explicit warning that EH baseline is not a proof of MTS integrability",
            "condition_before_use": "omega_extra=0/gauge/topological/no-flux or retained with bounds",
            "current_status": "extra_sector_omega_active",
        },
    ]
    for row in rows:
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def extra_sector_omega_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "omega_id": "ESO912_0_projector",
            "sector": "projector/Pi_M",
            "omega_piece": "omega_projector",
            "zero_route": "Pi_M/P_D is parent topological or gauge, delta Pi_M has zero local metric/source flux, and integral_S i_tau omega_projector=0",
            "current_status": "MISSING_PROJECTOR_OMEGA_ZERO_OR_COEFFICIENT",
            "retained_if_open": "Delta_symp_projector; q_P^nu; c_PiM_g",
            "priority": 1,
            "selected_next": True,
        },
        {
            "omega_id": "ESO912_1_boundary",
            "sector": "boundary/corner/reference",
            "omega_piece": "omega_boundary + corner",
            "zero_route": "boundary action is class-only/topological with fixed H_ref and no local hair/flux",
            "current_status": "MISSING_BOUNDARY_CORNER_REFERENCE_RULE",
            "retained_if_open": "Delta_ref; boundary beta/xi; radial source hair",
            "priority": 2,
            "selected_next": False,
        },
        {
            "omega_id": "ESO912_2_domain",
            "sector": "domain/selector",
            "omega_piece": "omega_domain + omega_selector",
            "zero_route": "domain selector is covariant/gauge/topological with no preferred-normal/homology drift",
            "current_status": "MISSING_DOMAIN_SELECTOR_OMEGA_ZERO",
            "retained_if_open": "c_domain; alpha1; alpha2; xi; Delta_symp_domain",
            "priority": 3,
            "selected_next": False,
        },
        {
            "omega_id": "ESO912_3_bulk_X_memory",
            "sector": "bulk X/memory",
            "omega_piece": "omega_X",
            "zero_route": "X has source-free positive operator/no-hair, or sourced force law is carried as alpha_X(lambda_X)",
            "current_status": "MISSING_X_MASS_GAP_OR_FORCE_LAW",
            "retained_if_open": "Delta_symp_X; alpha_X(lambda_X); gamma/beta source residue",
            "priority": 4,
            "selected_next": False,
        },
        {
            "omega_id": "ESO912_4_source_normalization",
            "sector": "kappa/G_eff/M_eff/Pi_M J",
            "omega_piece": "omega_source",
            "zero_route": "source-normalization variables are constants/constraints with no local symplectic flux and no derivative hair",
            "current_status": "MISSING_SOURCE_SUPERSELECTION_OR_THETA",
            "retained_if_open": "dln_Geff_dt; dln_Meff_dt; epsilon_charge; R10 alpha(lambda)",
            "priority": 5,
            "selected_next": False,
        },
        {
            "omega_id": "ESO912_5_connection",
            "sector": "connection/torsion/nonmetricity",
            "omega_piece": "omega_connection",
            "zero_route": "connection variation forces Levi-Civita and no torsion/nonmetricity in observed branch",
            "current_status": "MISSING_CONNECTION_OMEGA_AND_LEVI_CIVITA_PROOF",
            "retained_if_open": "spin/torsion clock/WEP/light-cone/R11 rows",
            "priority": 6,
            "selected_next": False,
        },
        {
            "omega_id": "ESO912_6_matter_frame",
            "sector": "matter one-coframe",
            "omega_piece": "omega_matter_frame",
            "zero_route": "ordinary matter uses one observed coframe and no direct MTS vertices/spurions",
            "current_status": "MISSING_MATTER_NO_SPURION_CERTIFICATE",
            "retained_if_open": "Delta_tau_frame; WEP/source charge; clock/frame rows",
            "priority": 7,
            "selected_next": False,
        },
    ]
    for row in rows:
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def delta_symp_extra_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "DSE912_0_projector",
            "symbol": "Delta_symp_projector",
            "definition": "mass-normalized projector/Pi_M symplectic obstruction contribution",
            "formula": "|int_S i_tau omega_projector|/M_ref",
            "observable_link": "q_P^nu; c_PiM_g; gamma; beta; alpha3; xi",
            "required_input": "projector omega-zero theorem or coefficient/source row",
            "current_value": "MISSING_PROJECTOR_OMEGA_ZERO_OR_COEFFICIENT",
        },
        {
            "row_id": "DSE912_1_boundary",
            "symbol": "Delta_symp_boundary",
            "definition": "boundary/corner/reference symplectic obstruction contribution",
            "formula": "|int_S i_tau omega_boundary + corner/reference terms|/M_ref",
            "observable_link": "Delta_ref; beta; xi; radial source hair; Gdot",
            "required_input": "class-only boundary/reference theorem or bound",
            "current_value": "MISSING_BOUNDARY_REFERENCE_INPUT",
        },
        {
            "row_id": "DSE912_2_domain",
            "symbol": "Delta_symp_domain",
            "definition": "domain/selector/homology symplectic obstruction contribution",
            "formula": "|int_S i_tau(omega_domain+omega_selector)|/M_ref",
            "observable_link": "alpha1; alpha2; xi; domain drift",
            "required_input": "covariant selector theorem or domain coefficient",
            "current_value": "MISSING_DOMAIN_OMEGA_INPUT",
        },
        {
            "row_id": "DSE912_3_bulk_X",
            "symbol": "Delta_symp_X",
            "definition": "bulk-X/memory sector symplectic obstruction contribution",
            "formula": "|int_S i_tau omega_X|/M_ref",
            "observable_link": "bulk fifth force; gamma/beta; R10 alpha(lambda)",
            "required_input": "mass-gap/no-hair theorem or source-normalized force law",
            "current_value": "MISSING_X_OMEGA_OR_FORCE_LAW",
        },
        {
            "row_id": "DSE912_4_source",
            "symbol": "Delta_symp_source",
            "definition": "source-normalization sector symplectic obstruction contribution",
            "formula": "|int_S i_tau omega_source|/M_ref",
            "observable_link": "Gdot/G; dln_Meff_dt; epsilon_charge; epsilon_orbit",
            "required_input": "superselection/constraint theorem or derivative residual rows",
            "current_value": "MISSING_SOURCE_NORMALIZATION_OMEGA",
        },
        {
            "row_id": "DSE912_5_connection",
            "symbol": "Delta_symp_connection",
            "definition": "connection/torsion/nonmetricity symplectic obstruction contribution",
            "formula": "|int_S i_tau omega_connection|/M_ref",
            "observable_link": "clock/WEP/light/spin/R11 connection rows",
            "required_input": "Levi-Civita theorem or torsion/nonmetricity coefficient vector",
            "current_value": "MISSING_CONNECTION_OMEGA_INPUT",
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
            "decision_id": "BD912_0_EH_baseline",
            "branch": "EH_core_baseline",
            "verdict": "conditional_baseline_only",
            "reason": "EH symplectic machinery is useful as a reference track but cannot prove MTS integrability while extra-sector omega is active",
            "policy": "use EH-core equations as comparison, not as a shortcut",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "BD912_1_projector_first",
            "branch": "projector_omega",
            "verdict": "selected_next",
            "reason": "projector omega is already linked to the retained q_P^nu/T_projector Bianchi residual and blocks local EH/PPN most directly",
            "policy": "try projector omega zero/gauge/topological route first; if it fails, stage Delta_symp_projector source row",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE912_0_EH_core_selected", "EH metric-core parent-selected", "blocked: EH premise ladder rungs remain not parent-derived"),
        ("CGATE912_1_EH_baseline_full_MTS", "EH omega equals full MTS omega", "blocked: omega_extra is active and unzeroed"),
        ("CGATE912_2_projector_omega_zero", "projector omega theorem-zero", "blocked: projector theta/omega or topological/gauge/no-flux theorem missing"),
        ("CGATE912_3_Delta_symp_extra_scored", "Delta_symp_extra scored below bounds", "blocked: coefficient/source rows are missing"),
        ("CGATE912_4_Htau_PiM", "integrable H_tau and Pi_M^H", "blocked: total omega integrability and source equality remain open"),
        ("CGATE912_5_local_GR", "Newton/PPN/local GR reduction", "blocked: operator/source/PPN rows remain active"),
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
            "objective": "attack the projector omega term: prove it is zero/gauge/topological/no-flux, or retain Delta_symp_projector with q_P/c_PiM_g source rows",
            "include": "Pi_M/P_D variation, projector topological/gauge route, zero local flux theorem, q_P^nu carrier, c_PiM_g response, Delta_symp_projector normalization",
            "exclude": "assuming projector omega vanishes, claiming EH/local GR, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_911_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_911_VALIDATION.csv")
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
    eh_rows_: list[dict[str, object]],
    extra_rows_: list[dict[str, object]],
    delta_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        eh_rows_,
        extra_rows_,
        delta_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V912_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V912_1_prior_911_clean",
            "result": "pass" if prior_911_clean() else "fail",
            "detail": "P8_Y5_BRR545_911_VALIDATION.csv clean",
        },
        {
            "check_id": "V912_2_EH_baseline_conditional",
            "result": "pass"
            if any("conditional" in stringify(row["current_status"]) for row in eh_rows_)
            else "fail",
            "detail": "EH core is baseline-only, not a parent claim",
        },
        {
            "check_id": "V912_3_extra_omega_rows_active",
            "result": "pass"
            if extra_rows_ and all("MISSING_" in stringify(row["current_status"]) for row in extra_rows_)
            else "fail",
            "detail": "all extra-sector omega rows remain active missing-input rows",
        },
        {
            "check_id": "V912_4_projector_selected_next",
            "result": "pass"
            if any(row["sector"] == "projector/Pi_M" and row["selected_next"] is True and row["priority"] == 1 for row in extra_rows_)
            else "fail",
            "detail": "projector omega selected as the next derivation target",
        },
        {
            "check_id": "V912_5_Delta_symp_extra_nonclaim",
            "result": "pass"
            if delta_rows_ and all(row["valid_for_claim"] is False and row["score_ready"] is False and "MISSING_" in stringify(row["current_value"]) for row in delta_rows_)
            else "fail",
            "detail": "Delta_symp extra rows remain missing-input and invalid for claim",
        },
        {
            "check_id": "V912_6_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all EH/projector/Htau/PiM/local-GR claim gates remain false",
        },
        {
            "check_id": "V912_7_all_generated_rows_nonclaim",
            "result": "pass" if all_generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed/score_ready false where present",
        },
        {
            "check_id": "V912_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V912_9_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V912_10_validation_rows_ready",
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
    eh_rows_: list[dict[str, object]],
    extra_rows_: list[dict[str, object]],
    delta_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 912 - Y5/R10 EH Core Symplectic Baseline vs Extra-Sector Omega Ledger

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **EH-core symplectic machinery is usable as a comparison baseline, not as a full MTS proof.** The full obstruction is `omega_total = omega_EH + omega_matter + omega_extra`. Since `omega_extra` is active, the next useful derivation target is the projector/Pi_M sector: either prove `omega_projector=0` by topological/gauge/no-flux structure, or retain `Delta_symp_projector`, `q_P^nu`, and `c_PiM_g`.

## Exact 912 Finding
The local GR route cannot borrow GR's symplectic current and walk away. It must show:

```text
integral_S i_tau omega_extra = 0
```

or carry the residual. The projector sector is first because it already appears in the Bianchi/projector stress ledger and contaminates PPN/source rows directly.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## EH Core Baseline
{md_table(eh_rows_)}

## Extra-Sector Omega Ledger
{md_table(extra_rows_)}

## Delta Symp Extra Rows
{md_table(delta_rows_)}

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
    eh_rows_ = eh_core_baseline_rows(generated_utc)
    extra_rows_ = extra_sector_omega_rows(generated_utc)
    delta_rows_ = delta_symp_extra_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        eh_rows_,
        extra_rows_,
        delta_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_912_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_912_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_912_EH_CORE_BASELINE.csv": eh_rows_,
        "P8_Y5_R10_912_EXTRA_SECTOR_OMEGA_LEDGER.csv": extra_rows_,
        "P8_Y5_R10_912_DELTA_SYMP_EXTRA_ROWS.csv": delta_rows_,
        "P8_Y5_R10_912_BRANCH_DECISION.csv": decision_rows_,
        "P8_Y5_R10_912_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_912_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_BRR545_912_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "912-Y5-R10-EH-core-symplectic-baseline-vs-extra-sector-omega-ledger.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        eh_rows_,
        extra_rows_,
        delta_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_912_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
