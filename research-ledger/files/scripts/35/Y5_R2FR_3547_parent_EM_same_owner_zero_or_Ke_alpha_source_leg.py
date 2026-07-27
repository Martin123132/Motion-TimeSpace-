from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3547-Y5-R2FR-parent-EM-same-owner-zero-or-Ke-alpha-source-leg.md"
CANONICAL_STATUS = OUT / "P8_Y5_parent_EM_same_owner_zero_or_Ke_alpha_source_leg_status.csv"

DD_E_CEILING = 1.372549019608e-12
ALPHA_COULOMB_CEILING = 1.407170315973e-12
ETA_BOUND = 2.8e-15


SOURCES: dict[str, dict[str, Any]] = {
    "script_3547": {"path": Path(__file__).resolve(), "role": "3547 generator"},
    "doc_3546": {
        "path": ROOT / "3546-Y5-R2FR-Ke-alpha-balpha-source-value-or-EM-alpha-coupling-bound-intake.md",
        "role": "3546 alpha product law and bound handoff",
    },
    "next_3546": {
        "path": OUT / "P8_Y5_R2FR_3546_NEXT_TARGET.csv",
        "role": "3546 selected same-owner proof target",
    },
    "zero_clauses_3546": {
        "path": OUT / "P8_Y5_R2FR_3546_ZERO_PROOF_CLAUSES.csv",
        "role": "zero-proof clauses for K_e_alpha*b_alpha",
    },
    "alpha_identity_3546": {
        "path": OUT / "P8_Y5_R2FR_3546_ALPHA_IDENTITY_LOCK.csv",
        "role": "exact b_alpha identity lock",
    },
    "vertical_generator_765": {
        "path": OUT / "P8_Y5_R10_765_VERTICAL_GENERATOR_NORM_THEOREM_ATTEMPT.csv",
        "role": "older vertical generator norm theorem attempt",
    },
    "alpha_level_owner_1812": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv",
        "role": "alpha level owner audit",
    },
    "charge_spine_2340": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv",
        "role": "parent charge/current extraction spine",
    },
    "em_alpha_charge_owner_3464": {
        "path": OUT / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv",
        "role": "EM alpha/charge owner audit",
    },
    "poynting_flux_3502": {
        "path": OUT / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
        "role": "Poynting flux and EM stress interface rows",
    },
    "em_owner_bound_vector_3503": {
        "path": OUT / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
        "role": "EM Hodge/Maxwell/current owner bound vector",
    },
    "calibrated_alpha_3528": {
        "path": OUT / "P8_Y5_R2FR_3528_CALIBRATED_ALPHA_CONTRACT.csv",
        "role": "calibrated alpha contract",
    },
    "product_bounds_3546": {
        "path": OUT / "P8_Y5_R2FR_3546_PRODUCT_BOUND_ROWS.csv",
        "role": "3546 finite product bound rows",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local empirical bound source register",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except (csv.Error, OSError, UnicodeDecodeError):
        return False
    return True


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def parent_action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PACT3547_0_fixed_charge_generator",
            "parent_clause": "the local EM field is the connection component A_Q of one fixed compact parent generator T_Q",
            "mathematical_form": "T_Q in Lie(G_parent) or charge lattice L_Q; exp(2 pi T_Q)=1; D_X T_Q=0",
            "implies": "no source/material dependence can enter through the charge label itself",
            "current_status": "SUFFICIENT_CONTRACT_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["vertical_generator_765"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PACT3547_1_fixed_generator_norm",
            "parent_clause": "the parent fibre metric/symplectic/lattice form fixes the norm of T_Q",
            "mathematical_form": "N_Q=<T_Q,T_Q>_P is quotient-fixed; D_X N_Q=0",
            "implies": "the Maxwell kinetic normalization cannot slide with motion/time/source fields",
            "current_status": "SUFFICIENT_CONTRACT_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["vertical_generator_765"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PACT3547_2_unique_curvature_norm",
            "parent_clause": "the observed F_Q^2 term is only the inherited parent curvature norm",
            "mathematical_form": "S_EM=-C_P/4 int <F,F>_P and no independent f_X(Phi) F_Q^2 term exists",
            "implies": "z_lambda=0 unless a common pure-unit line is also explicitly owned",
            "current_status": "CORE_GAP_COUNTERTERM_STILL_LEGAL",
            "source_path": str(SOURCES["alpha_level_owner_1812"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PACT3547_3_same_current_owner",
            "parent_clause": "the source current is the Noether/Ward current of the same parent generator and normalization",
            "mathematical_form": "J_Q = delta S_matter/delta A_Q with fixed representation weights n_A; D_X n_A=0",
            "implies": "z_g=0 and no independent current rescaling appears",
            "current_status": "SUFFICIENT_CONTRACT_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["charge_spine_2340"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PACT3547_4_readout_and_radiative_stability",
            "parent_clause": "readout, clocks, loops, Poynting flux and material binding do not regenerate a hidden alpha coefficient",
            "mathematical_form": "R_readout_alpha=R_rad_alpha=Phi_EM_rad=C_EM_readout=0 or individually bounded",
            "implies": "baseline b_alpha zero survives the lab reduction",
            "current_status": "SUFFICIENT_CONTRACT_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["poynting_flux_3502"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PACT3547_5_factorized_source_leg",
            "parent_clause": "if b_alpha is not zero, K_e_alpha is a factorized source/material/readout projection rather than a fitted knob",
            "mathematical_form": "K_e_alpha=K[Earth, Ti/Pt material tensor, q units, sign, readout]",
            "implies": f"nonzero alpha branch can be tested against {DD_E_CEILING:.6e}",
            "current_status": "FINITE_ROUTE_INPUTS_MISSING",
            "source_path": str(SOURCES["product_bounds_3546"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "THM3547_0_assume_contract",
            "statement": "Assume PACT3547_0 through PACT3547_4 hold as parent action clauses.",
            "derivation": "All EM normalization data descend from a single fixed quotient object before source/material readout.",
            "result": "the only legal local EM action has fixed lambda_0 and fixed current coupling g_0 in the chosen observed convention",
            "status": "CONDITIONAL_THEOREM_STEP",
            "valid_for_claim": "False",
        },
        {
            "step_id": "THM3547_1_kinetic_silence",
            "statement": "The kinetic coefficient has no vertical derivative.",
            "derivation": "lambda_A = C_P N_Q with D_X C_P=0 and D_X N_Q=0; no f_X(Phi)F_Q^2 slot is legal.",
            "result": "z_lambda = D_X ln lambda_A = 0",
            "status": "CONDITIONAL_IF_UNIQUE_F2_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "step_id": "THM3547_2_current_silence",
            "statement": "The current coupling has no vertical derivative.",
            "derivation": "J_Q is varied from the same parent connection and fixed integer representation weights; no c_X(Phi) A.J source slot is legal.",
            "result": "z_g = D_X ln g_J = 0",
            "status": "CONDITIONAL_IF_CURRENT_OWNER_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "step_id": "THM3547_3_alpha_zero",
            "statement": "The invariant alpha residual vanishes.",
            "derivation": "3546 gives b_alpha=2 z_g - z_lambda; with z_g=z_lambda=0, b_alpha=0.",
            "result": "b_alpha=0 and therefore K_e_alpha*b_alpha=0 for any finite K_e_alpha",
            "status": "CONDITIONAL_THEOREM_VALID_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "step_id": "THM3547_4_common_line_variant",
            "statement": "A common pure-unit line can also kill alpha drift if it scales kinetic and current terms with powers lambda~n^2 and g~n.",
            "derivation": "If z_lambda=2 z_g from one parent-owned unit line and the line is not a physical source marker, then b_alpha=0.",
            "result": "common-line cancellation is allowed only as a tracked unit/readout theorem, not as a tuned cancellation",
            "status": "ALTERNATIVE_CONDITIONAL_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "step_id": "THM3547_5_verdict",
            "statement": "The same-owner route is mathematically sufficient but not forced by the current corpus.",
            "derivation": "Gauge/diffeomorphism invariance alone still permits f_X(Phi)F^2 and source-current rescaling countermodels.",
            "result": "parent action must explicitly contain the fixed generator/unique-F2/current-owner contract, or the active alpha branch stays bounded not derived",
            "status": "THEOREM_CONSTRUCTED_AS_CONTRACT_NOT_CLAIM",
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM3547_0_nonminimal_F2",
            "legal_deformation": "Delta S = -1/4 int f_X(Phi) F_Q wedge *F_Q",
            "why_it_survives_generic_symmetry": "gauge invariant and diffeomorphism covariant for scalar f_X",
            "effect": "z_lambda != 0, so b_alpha can be nonzero",
            "what_kills_it": "typed no-Hom/coefficient-domain theorem or unique parent curvature norm",
            "source_path": str(SOURCES["em_owner_bound_vector_3503"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM3547_1_current_prefactor",
            "legal_deformation": "Delta S = int c_X(Phi) A_mu J^mu",
            "why_it_survives_generic_symmetry": "can be written as a source/current normalization if the current is not fixed as a parent Noether current",
            "effect": "z_g != 0 and source/material charge can leak into alpha/source coupling",
            "what_kills_it": "same parent connection/current owner plus fixed representation weights",
            "source_path": str(SOURCES["em_alpha_charge_owner_3464"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM3547_2_readout_regeneration",
            "legal_deformation": "S_eff or clock/material readout contains f_eff(Phi) F^2 after reduction",
            "why_it_survives_generic_symmetry": "effective/readout maps can reintroduce dependence even if the bare parent action is fixed",
            "effect": "calibrated alpha baseline can fail as a lab observable theorem",
            "what_kills_it": "radiative/readout stability theorem or explicit clock/WEP bound row",
            "source_path": str(SOURCES["poynting_flux_3502"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM3547_3_poynting_flux_boundary",
            "legal_deformation": "net exterior Phi_EM_rad = integral S_Poynting dot n dA",
            "why_it_survives_generic_symmetry": "Poynting flux is a real Hilbert stress/boundary-energy channel, not a gauge artifact",
            "effect": "affects source normalization/time hair rather than static alpha itself",
            "what_kills_it": "stationary isolated local branch or finite Gdot/clock/source flux bound",
            "source_path": str(SOURCES["poynting_flux_3502"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def poynting_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "interface_id": "POY3547_0_static_bound_fields",
            "poynting_object": "ordinary bound EM fields inside the source",
            "role_in_alpha_problem": "contribute to total Hilbert stress and material binding sensitivity, not an independent alpha drift",
            "zero_or_bound": "included in M_H/T_total if Maxwell stress owner is fixed",
            "next_action": "keep inside source normalization rather than double-counting as a separate alpha source coefficient",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "POY3547_1_radiative_flux",
            "poynting_object": "net exterior Poynting flux",
            "role_in_alpha_problem": "can regenerate time/source hair even when static alpha is calibrated",
            "zero_or_bound": "zero for stationary isolated branch, otherwise bound by Gdot/clock/source-flux rows",
            "next_action": "do not use Poynting language to prove alpha zero; use it to police radiative reentry",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "POY3547_2_cross_term",
            "poynting_object": "nonminimal hidden-visible F^2 or F*F cross term",
            "role_in_alpha_problem": "is exactly the C_XF2 throat behind z_lambda and b_alpha",
            "zero_or_bound": "requires no-Hom/unique-F2 theorem or finite WEP/clock/R10 bound",
            "next_action": "make C_XF2 the coefficient-domain proof target if same-owner proof is pursued",
            "valid_for_claim": "False",
        },
    ]


def fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "fallback_id": "FB3547_0_parent_zero_path",
            "branch": "derive b_alpha=0",
            "required_next_input": "parent object-language certificate for fixed T_Q, fixed N_Q, unique F2, same current owner and readout stability",
            "acceptance_gate": "no f_X(Phi)F^2 or c_X(Phi)A.J countermodel remains legal",
            "current_status": "BEST_DERIVATION_ROUTE_NOT_CLOSED",
            "valid_for_claim": "False",
        },
        {
            "fallback_id": "FB3547_1_finite_source_leg",
            "branch": "bound nonzero alpha branch",
            "required_next_input": "factorized K_e_alpha source leg and b_alpha parent value/bound",
            "acceptance_gate": f"abs(K_e_alpha*b_alpha) <= {DD_E_CEILING:.12e} in a single declared convention",
            "current_status": "FINITE_ROUTE_READY_FOR_INPUTS",
            "valid_for_claim": "False",
        },
        {
            "fallback_id": "FB3547_2_calibrated_baseline",
            "branch": "use measured alpha locally",
            "required_next_input": "label alpha_0 as calibrated local constant and keep active alpha branch quarantined",
            "acceptance_gate": "not advertised as derived alpha; no cancellation with WEP/source residuals",
            "current_status": "SAFE_FOR_BASELINE_MAXWELL_STRESS",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3547_0_same_owner_proof",
            "question": "Was b_alpha=0 derived outright from existing corpus?",
            "decision": "NO_EXISTING_CORPUS_DOES_NOT_FORCE_IT",
            "basis": "generic gauge/diffeomorphism symmetry still permits nonminimal F2 and current-prefactor countermodels",
            "forward_value": "a sufficient parent action contract is now explicit and narrow",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3547_1_conditional_theorem",
            "question": "Is there a mathematically clean theorem if the parent contract is signed?",
            "decision": "YES",
            "basis": "fixed generator norm plus unique curvature norm gives z_lambda=0; same current owner gives z_g=0; hence b_alpha=0",
            "forward_value": "this is the derivable path, not just a closure statement, but it needs a parent object-language certificate",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3547_2_poynting_role",
            "question": "Does the Poynting vector prove or kill the alpha branch?",
            "decision": "NEITHER",
            "basis": "Poynting stress belongs in total Hilbert source and radiative flux gates; C_XF2 remains the alpha throat",
            "forward_value": "use Poynting to police source/radiative reentry, not as a shortcut alpha proof",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3547_0",
            "checkpoint": "3547",
            "claim_allowed": "False",
            "same_owner_zero_status": "conditional_theorem_constructed_not_parent_signed",
            "countermodels_retained": "nonminimal_F2; current_prefactor; readout_regeneration; poynting_boundary_flux",
            "baseline_policy": "calibrated_alpha_safe_for_local_Maxwell_stress_not_derived_alpha",
            "finite_bound_gate": f"{DD_E_CEILING:.12e}",
            "next_target": "3548-Y5-R2FR-typed-EM-coefficient-domain-no-Hom-certificate-or-alpha-closure-demotion.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3547_0",
            "target_doc": "3548-Y5-R2FR-typed-EM-coefficient-domain-no-Hom-certificate-or-alpha-closure-demotion.md",
            "target_script": "scripts/Y5_R2FR_3548_typed_EM_coefficient_domain_noHom_or_alpha_closure_demotion.py",
            "objective": "try to prove the typed no-Hom certificate forbidding hidden/local fields from coefficient slots F_Q^2 and A.J; if it fails, demote the alpha derivation route to calibrated closure plus finite bound branch",
            "success_gate": "either C_XF2 and current-prefactor countermodels become untypeable, or the alpha route is explicitly separated from the GR/Newton source coupling route as calibrated closure only",
            "reason": "this attacks the exact legal countermodels that block the same-owner zero theorem",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    generated_paths: list[Path],
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_sources_exist = all(row["exists"] == "True" for row in sources)
    generated_csvs = [path for path in generated_paths if path.suffix.lower() == ".csv"]
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    contract_complete = all(row["parent_clause"] and row["mathematical_form"] and row["current_status"] for row in contracts)
    theorem_nonclaim = all(row["valid_for_claim"] == "False" for row in theorem)
    countermodels_retained = all(row["what_kills_it"] and row["valid_for_claim"] == "False" for row in countermodels)
    no_formalization_outputs = all(FORMALIZATION not in path.parents for path in generated_paths)
    return [
        {
            "validation_id": "VAL3547_0_sources_exist",
            "passes": bool_text(required_sources_exist),
            "status": "PASS" if required_sources_exist else "FAIL",
            "detail": "all cited 3547 source paths exist",
        },
        {
            "validation_id": "VAL3547_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3547_2_contract_complete",
            "passes": bool_text(contract_complete),
            "status": "PASS" if contract_complete else "FAIL",
            "detail": "every parent action contract row has a clause, mathematical form, and status",
        },
        {
            "validation_id": "VAL3547_3_theorem_nonclaim",
            "passes": bool_text(theorem_nonclaim),
            "status": "PASS" if theorem_nonclaim else "FAIL",
            "detail": "same-owner theorem rows remain conditional/nonclaim",
        },
        {
            "validation_id": "VAL3547_4_countermodels_retained",
            "passes": bool_text(countermodels_retained),
            "status": "PASS" if countermodels_retained else "FAIL",
            "detail": "blocking countermodels are explicitly retained with kill conditions",
        },
        {
            "validation_id": "VAL3547_5_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3547 generated outputs only inside post-checkpoint-work",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3547 — Parent EM same-owner zero or Ke-alpha source leg",
        "",
        "## Verdict",
        "",
        "- **The same-owner route is mathematically sufficient:** fixed parent charge generator, fixed generator norm, unique `F_Q^2` curvature subblock, and same Noether current owner imply `z_lambda=0`, `z_g=0`, hence `b_alpha=2 z_g-z_lambda=0`.",
        "- **It is not yet a live MTS claim:** generic gauge/diffeomorphism symmetry still allows `f_X(Phi)F^2`, current-prefactor, readout-regeneration, and Poynting-boundary counterbranches unless the parent object language forbids or bounds them.",
        f"- **Finite branch remains ready:** any future nonzero `K_e_alpha*b_alpha` must pass the nonclaim gate `<= {DD_E_CEILING:.6e}` in a declared DD e-basis convention.",
        "- **Poynting role clarified:** Poynting stress is part of the total Hilbert source/radiative flux accounting; it is not a shortcut proof of alpha silence.",
        "",
        "## Parent Action Contract",
        "",
        markdown_table(
            rows_by_name["contracts"],
            ["contract_id", "parent_clause", "mathematical_form", "implies", "current_status"],
        ),
        "",
        "## Theorem Attempt",
        "",
        markdown_table(
            rows_by_name["theorem"],
            ["step_id", "statement", "derivation", "result", "status"],
        ),
        "",
        "## Countermodels",
        "",
        markdown_table(
            rows_by_name["countermodels"],
            ["countermodel_id", "legal_deformation", "why_it_survives_generic_symmetry", "effect", "what_kills_it"],
        ),
        "",
        "## Poynting Interface",
        "",
        markdown_table(
            rows_by_name["poynting"],
            ["interface_id", "poynting_object", "role_in_alpha_problem", "zero_or_bound", "next_action"],
        ),
        "",
        "## Fallback Branches",
        "",
        markdown_table(
            rows_by_name["fallback"],
            ["fallback_id", "branch", "required_next_input", "acceptance_gate", "current_status"],
        ),
        "",
        "## Decisions",
        "",
        markdown_table(
            rows_by_name["decision"],
            ["decision_id", "question", "decision", "basis", "forward_value"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "passes", "status", "detail"],
        ),
        "",
        "## Next target",
        "",
        "Move to `3548-Y5-R2FR-typed-EM-coefficient-domain-no-Hom-certificate-or-alpha-closure-demotion.md`. This attacks the exact countermodels: if `f_X(Phi)F^2` and `c_X(Phi)A.J` are untypeable, the same-owner theorem has teeth; if they remain legal, alpha should be treated as calibrated closure plus finite active-branch bounds while the main GR/Newton source route continues elsewhere.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    contracts = parent_action_contract_rows()
    theorem = theorem_rows()
    countermodels = countermodel_rows()
    poynting = poynting_interface_rows()
    fallback = fallback_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3547_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3547_PARENT_ACTION_CONTRACT.csv": (
            contracts,
            ["contract_id", "parent_clause", "mathematical_form", "implies", "current_status", "source_path", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3547_SAME_OWNER_THEOREM_ATTEMPT.csv": (
            theorem,
            ["step_id", "statement", "derivation", "result", "status", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3547_COUNTERMODEL_LEDGER.csv": (
            countermodels,
            [
                "countermodel_id",
                "legal_deformation",
                "why_it_survives_generic_symmetry",
                "effect",
                "what_kills_it",
                "source_path",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3547_POYNTING_STRESS_INTERFACE.csv": (
            poynting,
            ["interface_id", "poynting_object", "role_in_alpha_problem", "zero_or_bound", "next_action", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3547_KE_ALPHA_SOURCE_LEG_FALLBACK.csv": (
            fallback,
            ["fallback_id", "branch", "required_next_input", "acceptance_gate", "current_status", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3547_DECISION_LEDGER.csv": (
            decisions,
            ["decision_id", "question", "decision", "basis", "forward_value", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3547_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "same_owner_zero_status",
                "countermodels_retained",
                "baseline_policy",
                "finite_bound_gate",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3547_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "same_owner_zero_status",
                "countermodels_retained",
                "baseline_policy",
                "finite_bound_gate",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, contracts, theorem, countermodels)
    validation_path = OUT / "P8_Y5_BRR545_3547_VALIDATION.csv"
    write_csv(
        validation_path,
        validation,
        ["validation_id", "passes", "status", "detail"],
    )
    generated_paths.append(validation_path)

    write_doc(
        {
            "contracts": contracts,
            "theorem": theorem,
            "countermodels": countermodels,
            "poynting": poynting,
            "fallback": fallback,
            "decision": decisions,
            "status": status,
            "validation": validation,
            "next_target": next_target,
        }
    )

    print(f"wrote {DOC}")
    for path in generated_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
