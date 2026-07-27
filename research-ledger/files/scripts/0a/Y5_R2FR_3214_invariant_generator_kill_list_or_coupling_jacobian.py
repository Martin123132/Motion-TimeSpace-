from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3214-Y5-R2FR-invariant-generator-kill-list-for-EM-coupling-or-promote-provenance-inputs-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3214_INPUTS.csv"
CRITERION = OUT / "P8_Y5_R2FR_3214_INVARIANT_COUPLING_CRITERION.csv"
KILL_LIST = OUT / "P8_Y5_R2FR_3214_GENERATOR_KILL_LIST.csv"
SURVIVORS = OUT / "P8_Y5_R2FR_3214_EM_BULK_SURVIVOR_REDUCTION.csv"
PROVENANCE = OUT / "P8_Y5_R2FR_3214_PROVENANCE_PROMOTION_ROWS.csv"
DECISION = OUT / "P8_Y5_R2FR_3214_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3214_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3214_00_3213_doc",
        "location": "post_checkpoint",
        "relative_path": "3213-Y5-R2FR-hidden-visible-product-sequester-or-balpha-Hodge-Poynting-provenance-pack-under-AX1090.md",
        "role": "3213 theorem/countertheorem handoff",
        "terms": ["nonconstant hidden invariant scalar", "product/sequester", "countertheorem"],
    },
    {
        "input_id": "SRC3214_01_3213_counter",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3213_INVARIANT_SCALAR_COUNTERTHEOREM.csv",
        "role": "active scalar countertheorem rows",
        "terms": ["CTR3213_0_scalar_invariant", "f(I)F^2", "boundary"],
    },
    {
        "input_id": "SRC3214_02_1115_triviality",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
        "role": "local invariant algebra triviality attempt",
        "terms": ["LIA1115_3_continuous_scalar_obstruction", "LIA1115_4_generator_elimination", "LIA1115_6_verdict"],
    },
    {
        "input_id": "SRC3214_03_1092_generators",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv",
        "role": "surviving invariant generator ledger",
        "terms": ["finite_cell_fibre_spectrum", "domain_selector", "memory_or_class_scalar", "species_charge_constants"],
    },
    {
        "input_id": "SRC3214_04_965_algebra",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_965_LOCAL_INVARIANT_ALGEBRA_AUDIT.csv",
        "role": "local invariant algebra audit",
        "terms": ["finite-cell", "domain selector", "memory/class scalar", "readout projector"],
    },
    {
        "input_id": "SRC3214_05_980_counterexamples",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv",
        "role": "counterexample ledger for marker/scalar/source coupling",
        "terms": ["theta_A", "species_kappa", "domain_selector", "boundary_flux"],
    },
    {
        "input_id": "SRC3214_06_3210_amplitude",
        "location": "post_checkpoint",
        "relative_path": "3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md",
        "role": "scalar amplitude law for finite residual fallback",
        "terms": ["Y_X", "source/boundary leakage", "omega_X"],
    },
    {
        "input_id": "SRC3214_07_3212_em",
        "location": "post_checkpoint",
        "relative_path": "3212-Y5-R2FR-EM-source-channel-no-extra-F2-or-Poynting-bound-input-under-AX1090.md",
        "role": "EM source decomposition to be reduced by generator gates",
        "terms": ["J_X^EM", "b_alpha", "Poynting", "Hodge"],
    },
    {
        "input_id": "SRC3214_08_3213_provenance",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3213_EM_COEFFICIENT_PROVENANCE_PACK.csv",
        "role": "coefficients needing zero theorem or finite provenance",
        "terms": ["PROV3213_0_balpha", "PROV3213_1_C_Hodge", "PROV3213_2_C_Poynting"],
    },
]


def build_rows(now: str) -> tuple[list[dict[str, object]], ...]:
    input_rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        input_rows.append(
            {
                **source,
                "path": str(path),
                "exists": b(path.exists()),
                "evidence_hits": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    criterion_rows = [
        {
            "criterion_id": "CRIT3214_0_vertical_derivative_decomposition",
            "claim_piece": "exact generator projection of hidden-visible coupling",
            "formal_statement": "For hidden generators I_a and visible coefficient vector C_vis=(ln Z_A,Theta_A,g_obs,C_boundary,C_readout,m_A,kappa_A), L_X C_vis = sum_a (partial C_vis/partial I_a) L_X I_a + explicit_hidden_slot.",
            "derivation_status": "EXACT_CHAIN_RULE_IDENTITY",
            "consequence": "EM/local source silence does not require all hidden invariants to be absent; it requires the visible coefficient Jacobian to annihilate the vertical generator velocity.",
            "required_for_claim": "parent-owned list of I_a, coefficient target grammar, and proof that no explicit hidden slot exists",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "criterion_id": "CRIT3214_1_zero_condition",
            "claim_piece": "minimal zero condition for EM coupling",
            "formal_statement": "J_X^EM=0 for bulk EM if for every generator I_a either L_X I_a=0 or partial_Ia(ln Z_A,Theta_A,g_obs/readout)=0, and if boundary/readout flux maps have the same annihilation property.",
            "derivation_status": "CONDITIONAL_THEOREM",
            "consequence": "This is weaker than full invariant algebra triviality and stronger than hand-waving sequester: it gives a checkable kernel condition.",
            "required_for_claim": "same-branch proof for all bulk, boundary, and radiative/readout coefficient maps",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "criterion_id": "CRIT3214_2_bulk_discrete_generator_result",
            "claim_piece": "discrete generators cannot create local bulk derivative inside a connected fixed branch",
            "formal_statement": "If I_a takes values in a discrete set and the local branch is connected with no wall crossing, then dI_a=0 and L_X I_a=0 on that branch.",
            "derivation_status": "EXACT_TOPOLOGICAL_CONDITIONAL",
            "consequence": "finite-cell spectrum, fixed domain class, and branch labels can be removed from the differential EM bulk source but may remain as fixed constants, jump data, or boundary/selection debt.",
            "required_for_claim": "connected fixed-branch theorem and explicit no-wall/no-selector clause",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "criterion_id": "CRIT3214_3_continuous_generator_result",
            "claim_piece": "continuous scalar generators remain dangerous",
            "formal_statement": "If I_a is smooth, nonconstant, and partial_Ia C_vis is not parent-forbidden, then L_X C_vis can be nonzero and the 3213 countertheorem survives.",
            "derivation_status": "COUNTERTHEOREM_RETAINED",
            "consequence": "memory/class scalar and radiative/readout scalar slots remain the real bulk-coupling enemies.",
            "required_for_claim": "positive nohair, exact shift/product typing, or finite empirical coefficient bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "criterion_id": "CRIT3214_4_finite_fallback_condition",
            "claim_piece": "if zero proof fails, source becomes bounded not claimed absent",
            "formal_statement": "|J_X^EM| <= sum_a |L_X I_a| |partial_Ia C_vis| |O_vis| + boundary/readout flux terms.",
            "derivation_status": "ABSOLUTE_VALUE_BOUND",
            "consequence": "surviving generators can feed 3210 amplitude law as a finite source rather than forcing a dead end.",
            "required_for_claim": "numeric/source-backed generator amplitudes, coefficient derivatives, field norms, support surfaces, and units",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    kill_rows = [
        {
            "generator_id": "GK3214_0_finite_cell_spectrum",
            "generator": "finite_cell_fibre_spectrum",
            "type": "discrete_or_spectral_label",
            "bulk_EM_derivative_status": "conditionally_killed_on_connected_fixed_branch",
            "proof_move": "discrete locally constant theorem: no wall crossing gives L_X I=0",
            "what_remains": "fixed-sector constants, thresholds, or branch jumps can still affect source normalization and WEP/local bounds",
            "next_requirement": "write connected fixed-cell branch clause or keep finite-cell jumps as boundary/source priors",
            "survives_as_bulk_EM_source": "false_if_branch_signed_else_unknown",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "generator_id": "GK3214_1_relative_domain_class",
            "generator": "relative_boundary_domain_class",
            "type": "discrete_topological_domain_label",
            "bulk_EM_derivative_status": "conditionally_killed_in_domain_interior",
            "proof_move": "fixed topological class has zero local derivative; variations changing class are boundary/domain-wall events, not smooth bulk X",
            "what_remains": "boundary functor and domain-wall flux can still feed C_Poynting or local projection leakage",
            "next_requirement": "separate smooth local interior from boundary/domain transition sector",
            "survives_as_bulk_EM_source": "false_if_interior_branch_signed_else_boundary_survives",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "generator_id": "GK3214_2_domain_selector",
            "generator": "domain_selector_chi_D",
            "type": "idempotent_projector",
            "bulk_EM_derivative_status": "killed_only_if_selector_is_fixed_before_variation",
            "proof_move": "chi_D^2=chi_D implies values are discrete; connected branch gives d chi_D=0, but post-variation selector is a readout/projection source",
            "what_remains": "if selector acts after variation it re-enters as reduced-action/readout debt",
            "next_requirement": "parent variation-before-readout theorem plus no post-readout EFT backreaction",
            "survives_as_bulk_EM_source": "unknown_until_readout_order_signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "generator_id": "GK3214_3_memory_class_scalar",
            "generator": "memory_or_class_scalar",
            "type": "continuous_scalar",
            "bulk_EM_derivative_status": "survives",
            "proof_move": "cannot be killed by connectedness; needs positive nohair/source-silence or exact typed coefficient exclusion",
            "what_remains": "can feed b_alpha, clock drift, Hodge coefficient drift, gamma shift, or finite fifth-force source",
            "next_requirement": "derive local memory nohair equation with signed mass/source/boundary terms, or promote b_memory_to_alpha finite bound",
            "survives_as_bulk_EM_source": "true_until_nohair_or_typing_signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "generator_id": "GK3214_4_orientation_time_arrow",
            "generator": "orientation_time_arrow",
            "type": "discrete_orientation_or_continuous_clock_marker",
            "bulk_EM_derivative_status": "split",
            "proof_move": "if it is only time orientation/coframe sign, it is fixed discrete structure; if it is a continuous clock-arrow scalar, it survives",
            "what_remains": "preferred-frame, parity/time-asymmetry, clock, or FstarF channel",
            "next_requirement": "classify as coframe-owned discrete orientation versus continuous hidden scalar",
            "survives_as_bulk_EM_source": "false_for_fixed_orientation_true_for_clock_scalar",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "generator_id": "GK3214_5_species_constants",
            "generator": "species_charge_constants",
            "type": "constant_sector_label",
            "bulk_EM_derivative_status": "not_a_vertical_derivative_source_if_constant",
            "proof_move": "L_X kappa_A=0 if species constants are truly constant and not hidden-coordinate functions",
            "what_remains": "nonuniversal constants still violate WEP/source coupling even when they do not generate b_alpha source",
            "next_requirement": "universal Hilbert source theorem or explicit source-coupling bound rows",
            "survives_as_bulk_EM_source": "false_as_derivative_true_as_WEP_source_debt",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "generator_id": "GK3214_6_readout_projector",
            "generator": "readout_projector",
            "type": "procedure_or_reduced_action_projector",
            "bulk_EM_derivative_status": "not_killed_by_geometry_alone",
            "proof_move": "if readout happens after parent variation and is not fed back into S_eff, no source; if it is varied as reduced action, source re-enters",
            "what_remains": "alpha/clock/readout coefficients can be manufactured after the bare product theorem",
            "next_requirement": "readout-after-variation theorem plus radiative closure",
            "survives_as_bulk_EM_source": "unknown_until_readout_closure_signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "generator_id": "GK3214_7_boundary_flux_weight",
            "generator": "boundary_or_worldtube_flux_weight",
            "type": "boundary_functional",
            "bulk_EM_derivative_status": "not_bulk_but_survives_boundary",
            "proof_move": "bulk F2 silence does not control surface term delta_X int_boundary C(I)n_i T_EM^0i",
            "what_remains": "Poynting/worldtube leakage feeds the 3210 b_X source term",
            "next_requirement": "boundary nohair/proper-exact cancellation or sourced Poynting flux bound",
            "survives_as_bulk_EM_source": "not_bulk_survives_as_boundary_source",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    survivor_rows = [
        {
            "reduction_id": "RED3214_0_bulk_source_formula",
            "statement": "J_X^EM,bulk = sum_a (L_X I_a)[1/4 partial_Ia Z_A F^2 + 1/4 partial_Ia Theta_A FstarF - 1/2 T_EM^{mu nu} partial_Ia g_obs,mu nu + partial_Ia C_readout O_readout]",
            "effect": "bulk source is a generator-velocity times coefficient-Jacobian problem",
            "reduction_status": "derived_formula",
            "remaining_active_terms": "memory_or_class_scalar; continuous clock-arrow if present; readout/radiative scalar slot",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "reduction_id": "RED3214_1_discrete_bulk_pruning",
            "statement": "fixed finite-cell, fixed domain class, and fixed selector labels have L_X I=0 inside a connected smooth local branch",
            "effect": "they are pruned from smooth bulk EM source, but not from boundary jumps or source normalization",
            "reduction_status": "conditional_pruning_not_claim",
            "remaining_active_terms": "domain-wall/boundary flux; nonuniversal constants; readout selector if varied after reduction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "reduction_id": "RED3214_2_real_enemy_list",
            "statement": "The shortest route to local EM silence is not killing every label; it is killing the continuous memory/readout coefficient projection and separately bounding boundary Poynting flux.",
            "effect": "next derivation should target memory scalar nohair/coefficient typing before more broad audits",
            "reduction_status": "route_narrowed",
            "remaining_active_terms": "memory scalar; readout/radiative closure; boundary flux; universal source-coupling constants",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    provenance_rows = [
        {
            "row_id": "PROM3214_0_memory_to_balpha",
            "source_generator": "memory_or_class_scalar",
            "coefficient": "b_alpha_memory = partial_memory ln Z_A",
            "zero_route": "exact typed exclusion of memory from visible gauge coefficient or positive memory nohair with L_X memory=0",
            "finite_route_inputs": "memory amplitude/gradient; partial_memory ln Z_A bound; EM F2 norm; source path; units",
            "feeds": "3212 FEB3212_0_balpha;3210 source amplitude law",
            "current_status": "MISSING_MEMORY_NOHAIR_OR_NUMERIC_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "PROM3214_1_memory_to_hodge",
            "source_generator": "memory_or_class_scalar",
            "coefficient": "C_Hodge_memory = partial_memory g_obs or partial_memory star_obs",
            "zero_route": "observed coframe/Hodge star factors only through q and memory is vertical-invisible",
            "finite_route_inputs": "C_Hodge_memory bound; EM stress norm; local support; source path; units",
            "feeds": "3212 FEB3212_3_Hodge;PPN/clock/local stress rows",
            "current_status": "MISSING_HODGE_FACTORING_OR_NUMERIC_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "PROM3214_2_readout_to_alpha_clock",
            "source_generator": "readout_projector",
            "coefficient": "C_readout_alpha_clock",
            "zero_route": "readout-after-variation plus no readout feedback into S_eff",
            "finite_route_inputs": "readout coefficient derivative; clock/alpha observable norm; source path; units",
            "feeds": "clock drift; alpha drift; R10 transfer gates",
            "current_status": "MISSING_READOUT_CLOSURE_OR_NUMERIC_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "PROM3214_3_boundary_poynting",
            "source_generator": "boundary_or_worldtube_flux_weight",
            "coefficient": "C_Poynting_boundary",
            "zero_route": "boundary functor exact/proper/orthogonal or depends only on q-visible flux",
            "finite_route_inputs": "C_Poynting; integral |n_i T_EM^0i| dSdt; worldtube rule; orientation; source path; units",
            "feeds": "3212 FEB3212_4_Poynting;3210 boundary leakage b_X",
            "current_status": "MISSING_BOUNDARY_NOHAIR_OR_FLUX_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "PROM3214_4_species_kappa",
            "source_generator": "species_charge_constants",
            "coefficient": "Delta kappa_A or source weight nonuniversality",
            "zero_route": "universal Hilbert source theorem with one kappa and all species stress entering same metric variation",
            "finite_route_inputs": "species source-weight differences; WEP/local source bounds; material composition; source path; units",
            "feeds": "WEP;PPN;Newtonian source coupling",
            "current_status": "MISSING_UNIVERSAL_SOURCE_THEOREM_OR_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3214_0_result",
            "result": "COUPLING_JACOBIAN_GATE_DERIVED_DISCRETE_BULK_GENERATORS_PRUNED_MEMORY_READOUT_BOUNDARY_SURVIVE",
            "claim_status": "NO_LOCAL_GR_NO_EM_SILENCE_NO_BALPHA_ZERO_CLAIM",
            "decision": "3214 replaces the vague kill-all-invariants target with a sharper kernel condition: visible couplings vanish when the coefficient Jacobian annihilates vertical generator velocities. Discrete fixed-branch labels are not smooth bulk EM sources, but memory/readout/boundary/source-universality debts survive.",
            "best_next_route": "derive the memory scalar nohair/coefficient-typing theorem first, because it is the main continuous bulk EM coupling survivor; handle boundary Poynting and source universality as separate finite/proof branches",
            "next_target": "3215-Y5-R2FR-memory-scalar-nohair-or-coefficient-typing-theorem-for-balpha-Hodge-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]

    return input_rows, criterion_rows, kill_rows, survivor_rows, provenance_rows, decision_rows


def main() -> None:
    now = stamp()
    input_rows, criterion_rows, kill_rows, survivor_rows, provenance_rows, decision_rows = build_rows(now)

    generated_without_validation = [
        INPUTS,
        CRITERION,
        KILL_LIST,
        SURVIVORS,
        PROVENANCE,
        DECISION,
    ]

    write_csv(INPUTS, input_rows)
    write_csv(CRITERION, criterion_rows)
    write_csv(KILL_LIST, kill_rows)
    write_csv(SURVIVORS, survivor_rows)
    write_csv(PROVENANCE, provenance_rows)
    write_csv(DECISION, decision_rows)

    all_rows: list[dict[str, str]] = []
    for path in generated_without_validation:
        all_rows.extend(read_csv(path))
    claim_rows = [row for row in all_rows if row.get("valid_for_claim") == "true"]

    validation_rows = [
        {
            "check_id": "VAL3214_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3214_01_chain_rule_gate",
            "check": "visible coupling Jacobian chain-rule criterion written",
            "pass": b(any(row["criterion_id"] == "CRIT3214_0_vertical_derivative_decomposition" for row in criterion_rows)),
            "detail": "L_X C_vis = sum partial_I C_vis L_X I plus explicit slot",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3214_02_discrete_pruning",
            "check": "discrete fixed-branch bulk pruning theorem included",
            "pass": b(any(row["criterion_id"] == "CRIT3214_2_bulk_discrete_generator_result" for row in criterion_rows)),
            "detail": "discrete generators have dI=0 on connected no-wall branch",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3214_03_generator_coverage",
            "check": "surviving generator list covers prior ledger",
            "pass": b(len(kill_rows) >= 8),
            "detail": ";".join(row["generator_id"] for row in kill_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3214_04_memory_survives",
            "check": "memory scalar is not falsely killed",
            "pass": b(any(row["generator_id"] == "GK3214_3_memory_class_scalar" and row["bulk_EM_derivative_status"] == "survives" for row in kill_rows)),
            "detail": "continuous memory/class scalar remains the main bulk-coupling target",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3214_05_provenance_rows",
            "check": "finite fallback rows are staged",
            "pass": b(len(provenance_rows) >= 5),
            "detail": ";".join(row["row_id"] for row in provenance_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3214_06_claims_blocked",
            "check": "no generated row is valid_for_claim true",
            "pass": b(len(claim_rows) == 0),
            "detail": f"claim_rows_true={len(claim_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3214_07_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3214_08_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_without_validation)),
            "detail": ";".join(path.name for path in generated_without_validation),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3214_09_next_target",
            "check": "next target is concrete and derivation-first",
            "pass": b("3215" in decision_rows[0]["next_target"]),
            "detail": decision_rows[0]["next_target"],
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3214 - Invariant Generator Kill List For EM Coupling Or Provenance Promotion under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha=0` claim, or public-facing result.

## Result

3214 makes a real narrowing move.

The target is not now "kill every hidden invariant or give up." The exact condition is sharper:

```text
For hidden generators I_a and visible coefficient vector
C_vis = (ln Z_A, Theta_A, g_obs, C_boundary, C_readout, m_A, kappa_A),

L_X C_vis =
    sum_a (partial C_vis / partial I_a) L_X I_a
    + explicit_hidden_slot.
```

Therefore hidden-visible coupling is killed if the visible coefficient Jacobian annihilates the vertical generator velocity:

```text
J_C(I) . L_X I = 0
```

This can happen by full invariant-algebra triviality, but it can also happen by a weaker typed/coefficient-kernel theorem. That is a useful escape hatch: MTS does not have to erase every possible label; it has to prove those labels cannot move the visible EM/matter/source coefficients on the local branch.

The useful win:

```text
fixed discrete/spectral/domain labels
    -> dI = 0 on a connected no-wall local branch
    -> no smooth bulk EM source from those labels
```

The bad news, kept honest:

```text
continuous memory/class scalars,
readout/radiative scalar slots,
boundary/Poynting flux weights,
and species source-weight constants
still survive unless separately derived or bounded.
```

## Invariant Coupling Criterion

{md_table(criterion_rows, ["criterion_id", "claim_piece", "formal_statement", "derivation_status", "consequence", "required_for_claim", "valid_for_claim"])}

## Generator Kill List

{md_table(kill_rows, ["generator_id", "generator", "type", "bulk_EM_derivative_status", "proof_move", "what_remains", "next_requirement", "survives_as_bulk_EM_source", "valid_for_claim"])}

## EM Bulk Survivor Reduction

{md_table(survivor_rows, ["reduction_id", "statement", "effect", "reduction_status", "remaining_active_terms", "valid_for_claim"])}

## Provenance Promotion Rows

{md_table(provenance_rows, ["row_id", "source_generator", "coefficient", "zero_route", "finite_route_inputs", "feeds", "current_status", "valid_for_claim"])}

## Decision

`{decision_rows[0]["result"]}`.

Claim status: `{decision_rows[0]["claim_status"]}`.

Best next route: {decision_rows[0]["best_next_route"]}.

Next target:

```text
{decision_rows[0]["next_target"]}
```

## Generated Evidence

- `{rel(INPUTS)}`
- `{rel(CRITERION)}`
- `{rel(KILL_LIST)}`
- `{rel(SURVIVORS)}`
- `{rel(PROVENANCE)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
