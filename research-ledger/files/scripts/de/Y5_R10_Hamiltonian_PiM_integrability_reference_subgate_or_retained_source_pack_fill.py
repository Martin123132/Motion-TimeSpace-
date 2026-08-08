from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_910_Hamiltonian_integrability_identity_derived_parent_symplectic_current_missing_Delta_symp_retained_nonclaim"
CLAIM_CEILING = "Hamiltonian_integrability_contract_and_Delta_symp_obstruction_only_no_PiM_H_no_measured_GM_no_Newton_no_local_GR_claim"
NEXT_TARGET = "911-Y5-R10-parent-symplectic-current-minimal-contract-or-Delta-symp-bound-input.md"

SOURCE_SPECS = [
    {
        "source_id": "909_doc",
        "path": ROOT / "909-Y5-R10-Hamiltonian-PiM-charge-map-or-retained-projector-PPN-source-pack.md",
        "needle": "the Hamiltonian `Pi_M^H` route is the best derivation skeleton",
        "role": "handoff selecting Hamiltonian integrability/reference as the next subgate",
    },
    {
        "source_id": "909_validation",
        "path": OUT / "P8_Y5_BRR545_909_VALIDATION.csv",
        "needle": "V909_11_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "909_integrability_gate",
        "path": OUT / "P8_Y5_R10_909_INTEGRABILITY_GATE.csv",
        "needle": "HIG909_1_symplectic_integrability",
        "role": "specific integrability/reference blocker",
    },
    {
        "source_id": "909_retained_pack",
        "path": OUT / "P8_Y5_R10_909_RETAINED_PROJECTOR_SOURCE_PACK.csv",
        "needle": "RSP909_0_symplectic_integrability_residual",
        "role": "Delta_symp retained source row to refine",
    },
    {
        "source_id": "457_hamiltonian_doc",
        "path": ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "needle": "differentiable_integrable_Hxi",
        "role": "original Hamiltonian boundary-charge integrability condition",
    },
    {
        "source_id": "457_hamiltonian_contract",
        "path": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "needle": "HC2_differentiable_integrable_Hxi",
        "role": "machine Hamiltonian integrability contract",
    },
    {
        "source_id": "382_parent_action_contract",
        "path": ROOT / "382-parent-local-action-minimal-contract.md",
        "needle": "S_parent =",
        "role": "minimal parent action sectors whose variations must supply the symplectic current",
    },
    {
        "source_id": "439_EH_premise_ladder",
        "path": ROOT / "439-EH-only-exterior-parent-premise-ladder.md",
        "needle": "V2_hidden_Euler_equations",
        "role": "parent variation and hidden-sector ownership dependencies",
    },
    {
        "source_id": "655_EH_premise_audit",
        "path": OUT / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
        "needle": "EHP655_P2_Ward_Euler_ownership",
        "role": "current EH-only blockers feeding the Hamiltonian obstruction",
    },
    {
        "source_id": "789_Ward_Bianchi",
        "path": OUT / "P8_Y5_R10_789_VARIATION_WARD_IDENTITY_GATE.csv",
        "needle": "VWI789_3_Bianchi",
        "role": "total Ward/Bianchi compatibility requirement",
    },
    {
        "source_id": "790_exchange_stress",
        "path": OUT / "P8_Y5_R10_790_EXCHANGE_STRESS_DECOMPOSITION.csv",
        "needle": "ESD790_1_exchange_longitudinal",
        "role": "exchange stress and hidden flux channels that can obstruct integrability",
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
            "what_changed": "derived the exact Hamiltonian integrability obstruction and split fixed-reference proof obligations from retained Delta_symp rows",
            "best_partial_result": "the integrability condition is now precise: the boundary symplectic obstruction integral_S i_tau omega must vanish or be exact on allowed variations, with tau and H_ref fixed",
            "hard_blockers": "explicit parent Lagrangian variation, symplectic potential Theta, symplectic current omega, boundary conditions, tau normalization, reference subtraction, hidden-sector flux silence, and source-frame closure",
            "what_is_not_claimed": "integrable H_tau, parent-owned Pi_M^H, Hamiltonian/Hilbert source equality, measured GM, Newtonian limit, PPN pass, or local GR",
            "decision": "retain Delta_symp and related obstruction rows until a parent symplectic-current contract or real bound input exists",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def symplectic_identity_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "identity_id": "SID910_0_variation_start",
            "identity": "parent action variation",
            "mathematical_form": "delta L_parent = E_A delta Phi^A + d Theta(Phi,delta Phi)",
            "meaning": "Hamiltonian charge cannot be evaluated until the parent symplectic potential Theta is known",
            "current_status": "MISSING_EXPLICIT_PARENT_LAGRANGIAN_VARIATION",
        },
        {
            "identity_id": "SID910_1_noether_current",
            "identity": "diffeomorphism Noether current",
            "mathematical_form": "J_tau = Theta(Phi,L_tau Phi) - i_tau L_parent = C_tau + d Q_tau",
            "meaning": "on shell and with constraints owned, the generator reduces to a boundary charge",
            "current_status": "FORMAL_IDENTITY_CONDITIONAL_ON_PARENT_ACTION",
        },
        {
            "identity_id": "SID910_2_charge_variation",
            "identity": "Hamiltonian variation one-form",
            "mathematical_form": "alpha_tau(delta Phi) := delta H_tau = integral_S(delta Q_tau - i_tau Theta)",
            "meaning": "alpha_tau must be an exact one-form on the allowed phase space for H_tau to exist",
            "current_status": "FORMAL_CANDIDATE_WRITTEN_NOT_INTEGRATED",
        },
        {
            "identity_id": "SID910_3_integrability_obstruction",
            "identity": "boundary symplectic obstruction",
            "mathematical_form": "delta_1 alpha_tau(delta_2)-delta_2 alpha_tau(delta_1) = integral_S i_tau omega(delta_1 Phi,delta_2 Phi) + delta_tau_terms",
            "meaning": "integrability requires this obstruction to vanish, be exact with fixed reference, or be retained as Delta_symp",
            "current_status": "EXACT_OBSTRUCTION_DERIVED_BUT_NOT_ZEROED",
        },
        {
            "identity_id": "SID910_4_conservation_flux",
            "identity": "charge conservation and flux",
            "mathematical_form": "H_tau[S_2]-H_tau[S_1] = integral_Boundary C_tau + integral_N symplectic/source/boundary flux",
            "meaning": "a mass charge is conserved only if constraints and hidden exchange/boundary fluxes vanish or are retained",
            "current_status": "FLUX_ZERO_NOT_PARENT_DERIVED",
        },
    ]
    for row in rows:
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def reference_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "contract_id": "HIR910_0_parent_variation",
            "must_supply": "explicit Theta and omega for all parent fields",
            "pass_condition": "Theta(Phi,delta Phi) and omega=delta Theta are written for metric/coframe, matter, MTS, projector/domain, and boundary sectors",
            "current_status": "missing_parent_symplectic_current",
            "if_failed": "Delta_symp retained; no Pi_M^H claim",
        },
        {
            "contract_id": "HIR910_1_allowed_phase_space",
            "must_supply": "allowed local exterior boundary conditions",
            "pass_condition": "variation space fixes the observed frame, boundary class, source support, falloff/quasilocal boundary data, and excludes unowned domain drift",
            "current_status": "boundary_conditions_not_parent_signed",
            "if_failed": "domain/reference/boundary residual rows retained",
        },
        {
            "contract_id": "HIR910_2_tau_fixed",
            "must_supply": "observed time generator normalization",
            "pass_condition": "delta tau=0 or delta_tau_terms are shown exact/zero in the same matter-clock frame",
            "current_status": "tau_normalization_not_parent_derived",
            "if_failed": "delta_frame_source and preferred-frame rows retained",
        },
        {
            "contract_id": "HIR910_3_integrability_zero",
            "must_supply": "boundary symplectic obstruction zero",
            "pass_condition": "integral_S i_tau omega(delta_1,delta_2)=0 or exact with fixed H_ref for all allowed variations",
            "current_status": "obstruction_not_evaluated",
            "if_failed": "Delta_symp numeric/theorem row required",
        },
        {
            "contract_id": "HIR910_4_reference_rule",
            "must_supply": "single fixed reference/subtraction convention",
            "pass_condition": "H_ref is fixed once by parent boundary class, not fit separately per source/radius/frame",
            "current_status": "fixed_reference_missing",
            "if_failed": "boundary_reference_shift retained",
        },
        {
            "contract_id": "HIR910_5_hidden_flux_silence",
            "must_supply": "hidden/projector/domain/boundary symplectic flux silence or retained carrier",
            "pass_condition": "extra-sector symplectic flux and source exchange vanish, are gauge/topological, or are carried by explicit residual stress",
            "current_status": "hidden_flux_not_zeroed",
            "if_failed": "q_P^nu, c_PiM_g, mu_extra, and c_nonEH_operator_vector remain active",
        },
        {
            "contract_id": "HIR910_6_source_calibration_link",
            "must_supply": "Hamiltonian charge to measured source calibration",
            "pass_condition": "integrable H_tau is then linked to Pi_M^H J_H and orbital GM without epsilon_charge/epsilon_orbit",
            "current_status": "downstream_calibration_unfilled",
            "if_failed": "epsilon_charge and epsilon_orbit retained",
        },
    ]
    for row in rows:
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def obstruction_pack_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "obstruction_id": "OBS910_0_Delta_symp",
            "symbol": "Delta_symp",
            "definition": "dimensionless or mass-normalized envelope of the nonzero boundary symplectic obstruction integral_S i_tau omega",
            "mathematical_form": "|integral_S i_tau omega| / M_ref or route-specific mass-charge normalization",
            "observable_link": "measured GM drift, beta source term, boundary reference drift, Gdot/G",
            "required_input": "parent omega and allowed variation space, or numeric obstruction bound",
            "current_status": "MISSING_PARENT_OMEGA_OR_BOUND",
        },
        {
            "obstruction_id": "OBS910_1_delta_tau_frame",
            "symbol": "Delta_tau",
            "definition": "variation of the observed time generator or mismatch between Hamiltonian time and matter-clock time",
            "mathematical_form": "delta_tau_terms in delta alpha_tau",
            "observable_link": "clock redshift, preferred-frame PPN, source-frame calibration",
            "required_input": "parent tau normalization theorem or frame residual value",
            "current_status": "MISSING_TAU_NORMALIZATION",
        },
        {
            "obstruction_id": "OBS910_2_reference_shift",
            "symbol": "Delta_ref",
            "definition": "reference/subtraction ambiguity in H_ref across source, radius, boundary class, or frame",
            "mathematical_form": "delta H_ref != 0 or H_ref=H_ref[S,A,r,frame]",
            "observable_link": "measured GM offset/drift, radial source hair, boundary beta/xi terms",
            "required_input": "fixed class-only reference rule or bounded reference-shift row",
            "current_status": "MISSING_FIXED_REFERENCE_RULE",
        },
        {
            "obstruction_id": "OBS910_3_extra_symplectic_flux",
            "symbol": "F_extra_symp",
            "definition": "symplectic flux through hidden/projector/domain/boundary sectors not captured by EH/matter source",
            "mathematical_form": "integral_N omega_extra + boundary/source exchange flux",
            "observable_link": "q_P^nu, alpha3, xi, Gdot, mu_extra",
            "required_input": "hidden-sector no-flux theorem or explicit exchange-stress carrier",
            "current_status": "MISSING_HIDDEN_FLUX_SILENCE",
        },
        {
            "obstruction_id": "OBS910_4_charge_calibration_tail",
            "symbol": "Delta_cal",
            "definition": "downstream mismatch between an integrable H_tau and measured Hilbert/orbital source mass",
            "mathematical_form": "epsilon_charge + epsilon_orbit + epsilon_Gauss after H_tau exists",
            "observable_link": "Newtonian source normalization, R10/radial hair, PPN source stability",
            "required_input": "source equality plus Poisson/Gauss/orbital calibration or residual values",
            "current_status": "MISSING_SOURCE_CALIBRATION",
        },
    ]
    for row in rows:
        row["score_ready"] = False
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD910_0_integrability_identity",
            "branch": "derive_integrability_condition",
            "verdict": "exact_obstruction_derived_not_zeroed",
            "reason": "the covariant-phase-space identity reduces the problem to integral_S i_tau omega plus delta_tau/reference/flux terms, but the parent omega is not available",
            "policy": "do not claim H_tau/Pi_M^H; use this as the parent action contract",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "BD910_1_retained_residual",
            "branch": "retain_Delta_symp",
            "verdict": "Delta_symp_pack_staged_unfilled",
            "reason": "without parent omega or a numeric bound, the obstruction must remain a source-normalization/projector residual",
            "policy": "next work must either write the parent symplectic current contract or fill Delta_symp as a bounded input",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE910_0_integrable_Htau", "integrable Hamiltonian charge H_tau", "blocked: parent Theta/omega and boundary variation space are missing"),
        ("CGATE910_1_fixed_reference", "fixed reference/subtraction rule", "blocked: H_ref class-only rule not parent-derived"),
        ("CGATE910_2_tau_normalization", "observed time generator normalization", "blocked: tau/frame variation terms not zeroed"),
        ("CGATE910_3_hidden_flux_zero", "hidden/projector/domain symplectic flux silence", "blocked: extra flux and q_P/T_projector carrier not zeroed"),
        ("CGATE910_4_PiM_H", "parent-owned Pi_M^H", "blocked: integrable H_tau and source equality are not available"),
        ("CGATE910_5_Newton_local_GR", "measured GM/Newton/PPN/local GR", "blocked: downstream source calibration and PPN rows remain unfilled"),
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
            "objective": "write the minimal parent symplectic-current contract needed to evaluate integral_S i_tau omega; if it cannot be parent-specified, turn Delta_symp into a bounded residual input row",
            "include": "Theta, omega, allowed boundary variations, tau normalization, H_ref class rule, hidden-sector symplectic flux terms, Delta_symp normalization",
            "exclude": "assuming omega=0, claiming H_tau integrability, claiming Pi_M^H, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_909_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_909_VALIDATION.csv")
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
    identity_rows_: list[dict[str, object]],
    contract_rows_: list[dict[str, object]],
    obstruction_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        identity_rows_,
        contract_rows_,
        obstruction_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V910_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V910_1_prior_909_clean",
            "result": "pass" if prior_909_clean() else "fail",
            "detail": "P8_Y5_BRR545_909_VALIDATION.csv clean",
        },
        {
            "check_id": "V910_2_integrability_obstruction_written",
            "result": "pass"
            if any(row["identity_id"] == "SID910_3_integrability_obstruction" and row["current_status"] == "EXACT_OBSTRUCTION_DERIVED_BUT_NOT_ZEROED" for row in identity_rows_)
            else "fail",
            "detail": "boundary symplectic obstruction identity is explicit",
        },
        {
            "check_id": "V910_3_reference_contract_not_satisfied",
            "result": "pass" if contract_rows_ and all("missing" in stringify(row["current_status"]).lower() or "not_" in stringify(row["current_status"]).lower() or "obstruction" in stringify(row["current_status"]).lower() or "hidden" in stringify(row["current_status"]).lower() or "downstream" in stringify(row["current_status"]).lower() for row in contract_rows_) else "fail",
            "detail": "parent reference/integrability clauses remain unsigned",
        },
        {
            "check_id": "V910_4_obstruction_pack_nonclaim_missing_inputs",
            "result": "pass"
            if obstruction_rows_
            and all(row["valid_for_claim"] is False and row["score_ready"] is False and "MISSING_" in stringify(row["current_status"]) for row in obstruction_rows_)
            else "fail",
            "detail": "obstruction rows remain missing-input/source-needed and invalid for claim",
        },
        {
            "check_id": "V910_5_Delta_symp_retained",
            "result": "pass"
            if any(row["symbol"] == "Delta_symp" and row["current_status"] == "MISSING_PARENT_OMEGA_OR_BOUND" for row in obstruction_rows_)
            else "fail",
            "detail": "Delta_symp retained until parent omega or bound exists",
        },
        {
            "check_id": "V910_6_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all H_tau/PiM/Newton/local-GR claim gates remain false",
        },
        {
            "check_id": "V910_7_all_generated_rows_nonclaim",
            "result": "pass" if all_generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed/score_ready false where present",
        },
        {
            "check_id": "V910_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V910_9_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V910_10_validation_rows_ready",
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
    identity_rows_: list[dict[str, object]],
    contract_rows_: list[dict[str, object]],
    obstruction_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 910 - Y5/R10 Hamiltonian PiM Integrability Reference Subgate Or Retained Source Pack Fill

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the exact integrability obstruction is derived, but not zeroed.** The charge `H_tau` exists only if the one-form `alpha_tau(delta Phi)=integral_S(delta Q_tau-i_tau Theta)` is exact on the allowed parent phase space. Equivalently, the boundary obstruction `integral_S i_tau omega(delta_1 Phi,delta_2 Phi)` plus time-generator/reference terms must vanish or be exact. Current MTS has not supplied the parent `Theta/omega`, so `Delta_symp` stays retained.

## Exact 910 Finding
The useful derivation is now local and sharp:

```text
delta L_parent = E_A delta Phi^A + d Theta(Phi,delta Phi)
delta H_tau = integral_S(delta Q_tau - i_tau Theta)
d alpha_tau = integral_S i_tau omega + delta_tau/reference terms
```

Therefore the next parent action must either prove `d alpha_tau=0` on its allowed local exterior variations, or give `Delta_symp` as a sourced residual. This is not bad news; it is the lock shape. We now know exactly what key a future parent action must cut.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Symplectic Identity Derivation
{md_table(identity_rows_)}

## Integrability/Reference Contract
{md_table(contract_rows_)}

## Obstruction Pack
{md_table(obstruction_rows_)}

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
    identity_rows_ = symplectic_identity_rows(generated_utc)
    contract_rows_ = reference_contract_rows(generated_utc)
    obstruction_rows_ = obstruction_pack_rows(generated_utc)
    decision_rows_ = branch_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        identity_rows_,
        contract_rows_,
        obstruction_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_910_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_910_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_910_SYMPLECTIC_IDENTITY_DERIVATION.csv": identity_rows_,
        "P8_Y5_R10_910_INTEGRABILITY_REFERENCE_CONTRACT.csv": contract_rows_,
        "P8_Y5_R10_910_OBSTRUCTION_PACK.csv": obstruction_rows_,
        "P8_Y5_R10_910_BRANCH_DECISION.csv": decision_rows_,
        "P8_Y5_R10_910_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_910_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_BRR545_910_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "910-Y5-R10-Hamiltonian-PiM-integrability-reference-subgate-or-retained-source-pack-fill.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        identity_rows_,
        contract_rows_,
        obstruction_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_910_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
