from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3629"
BRANCH_ID = "MTS_R2FR_Y5_RESPONSE_DOUBLET_SOURCE_COUPLING_ZERO_OR_COEFFICIENT_3629"
DOC = ROOT / "3629-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3629_SOURCE_REGISTER.csv",
        "coupling_law": RESIDUALS / "P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv",
        "zero_routes": RESIDUALS / "P8_Y5_R2FR_3629_JZ_ZERO_ROUTE_AUDIT.csv",
        "coefficient_rows": RESIDUALS / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3629_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3629_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3629_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_response_doublet_coupling_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3629_VALIDATION.csv",
    }


def source_map() -> list[dict[str, str]]:
    return [
        {
            "source_id": "handoff_3628",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3628_NEXT_TARGET.csv"),
            "needle": "proving J_Z=0",
            "role": "3628 selected source coupling as the next bottleneck after the even response doublet gave F1=0.",
        },
        {
            "source_id": "scalar_density_candidates_3628",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3628_EXPLICIT_SCALAR_DENSITY_CANDIDATES.csv"),
            "needle": "BEST_CONDITIONAL_ROUTE_F1_ZERO_BY_EVENNESS_PARENT_MAPPING_MISSING",
            "role": "explicit response-doublet scalar density and fixed-point route.",
        },
        {
            "source_id": "fixed_point_3628",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3628_FIXED_POINT_DOUBLE_ZERO_GATE.csv"),
            "needle": "HARD_BLOCK_REMAINS_COUPLING_NOT_DERIVED",
            "role": "3628 isolates J_Z as the hard block.",
        },
        {
            "source_id": "response_doublet_contract",
            "path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
            "needle": "RD516_4_zero_odd_source",
            "role": "original response-doublet source and PPN lock contract.",
        },
        {
            "source_id": "quotient_matter_626",
            "path": str(ROOT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md"),
            "needle": "Lie_v S_matter = 0",
            "role": "quotient descent criterion that would kill vertical source coupling.",
        },
        {
            "source_id": "double_zero_memory_origin",
            "path": str(RESIDUALS / "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv"),
            "needle": "f(0)=0 and f_prime(0)=0",
            "role": "memory/source activation double-zero condition and p>=2 requirement.",
        },
        {
            "source_id": "domain_parent_clause",
            "path": str(RESIDUALS / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv"),
            "needle": "S_mem,D = integral sqrt(-g) chi_D^2 L_mem,D",
            "role": "candidate parent action clause where source coupling becomes quadratic in local selector.",
        },
        {
            "source_id": "domain_coefficients",
            "path": str(RESIDUALS / "P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv"),
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "role": "existing coefficient fallback rows for preferred-frame/domain leakage.",
        },
        {
            "source_id": "constant_gm_gate",
            "path": str(RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv"),
            "needle": "epsilon_mu := mu_extra/(G_eff M_eff)",
            "role": "source-normalization derivative gate for Newton/local-GR coupling leakage.",
        },
        {
            "source_id": "charge_current_attempt",
            "path": str(RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv"),
            "needle": "Pi_M(Q_nonEH + Q_boundary + Q_domain + Q_memory + Q_range + Q_connection + Q_delta_kappa)=0",
            "role": "charge/current route for killing extra mass-source channels.",
        },
        {
            "source_id": "residual_prediction_template",
            "path": str(RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv"),
            "needle": "R11_EH_operator_ledger",
            "role": "R0-R11 local residual scorecard targets.",
        },
        {
            "source_id": "ppn_envelope_3625",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv"),
            "needle": "ENV3625_6_total",
            "role": "component-complete local-GR envelope that coefficient rows must eventually feed.",
        },
    ]


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in source_map():
        path = Path(source["path"])
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source["source_id"],
                "path": source["path"],
                "exists": exists,
                "needle": source["needle"],
                "needle_found": exists and contains(path, source["needle"]),
                "role": source["role"],
            }
        )
    return rows


def coupling_law_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "law_id": "CL3629_0_total_action_split",
            "statement": "Split the candidate local sector into an even response-doublet bulk action plus matter, source-normalization, and boundary pieces.",
            "formula": "S_total=S_even[Z,g]+S_matter[g,Psi,Z]+S_source_norm[g,Z,Pi_M]+S_boundary[g,Z]",
            "meaning": "F1=0 in S_even is not enough; any term linear in Z from matter/source/boundary re-sources the local residual.",
            "status": "DERIVED_STRUCTURE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "law_id": "CL3629_1_linearized_Z_Euler",
            "statement": "The local response equation linearized around Z=0 has a source vector J_Z.",
            "formula": "L_AB Z^B + J_A + O(Z^2)=0, with L_AB=-nabla_mu(H_AB nabla^mu)+M_AB and J_A=(1/sqrt(-g)) delta(S_matter+S_source_norm+S_boundary)/delta Z^A|0",
            "meaning": "Z=0 is an on-shell local solution only if J_A=0 and the boundary natural source also vanishes/fixes.",
            "status": "EXACT_CONDITIONAL_COUPLING_LAW",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "law_id": "CL3629_2_residual_profile",
            "statement": "If J_Z is not zero, the positive operator turns it into a finite local profile rather than a plateau.",
            "formula": "Z^A(x)=-(L^{-1})^{AB}J_B + boundary Green terms + O(J^2)",
            "meaning": "This is the bridge from a missing coupling theorem to executable PPN/Newton/R10 coefficient rows.",
            "status": "PROFILE_BOUND_ROUTE_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "law_id": "CL3629_3_zero_theorem_contract",
            "statement": "The exact zero route is a theorem about the total action, not just the response-doublet action.",
            "formula": "J_A=0 follows if every Z-coupled non-response piece descends to the quotient, is even in Z, or starts at order p>=2 with zero boundary source.",
            "meaning": "This is the contract a future parent action must satisfy to make the local branch derivable.",
            "status": "ZERO_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def zero_route_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "JZR3629_0_quotient_descent",
            "zero_condition": "Z^A is vertical to the quotient map and ordinary matter descends to Q_MTS.",
            "test": "for every vertical v_A, Lie_vA S_matter=0 up to owned gauge/boundary terms",
            "result_if_pass": "J_A^matter=0 without tuning; representative Weyl/disformal coupling is excluded",
            "current_evidence": "626 gives the descent criterion but explicitly does not parent-sign the matter action, vertical rule, measure/connection descent, or boundary projection.",
            "current_status": "BEST_MATTER_ZERO_ROUTE_NOT_SIGNED",
            "source_path": str(ROOT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "JZR3629_1_Z2_even_total_action",
            "zero_condition": "the total local action is invariant under Z -> -Z while matter/source observables are even",
            "test": "S_matter[g,Psi,Z]=S_matter[g,Psi,-Z] and S_source_norm[g,Z]=S_source_norm[g,-Z]",
            "result_if_pass": "all linear source terms vanish: J_A^matter=J_A^source=0",
            "current_evidence": "3628 constructs even S_GK, but no source/matter evenness theorem exists in the inspected corpus.",
            "current_status": "CANDIDATE_SYMMETRY_NOT_PARENT_DERIVED",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3628_EXPLICIT_SCALAR_DENSITY_CANDIDATES.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "JZR3629_2_quadratic_activation",
            "zero_condition": "memory/domain/source coupling begins at order p>=2 in the local selector or response amplitude",
            "test": "f(0)=0 and f_prime(0)=0, e.g. f=chi_D^2 or norm-square/topological pairing",
            "result_if_pass": "local zero kills both stress value and the Euler source lambda/J at first order",
            "current_evidence": "p>=2 is derived as a requirement and quadratic is sufficient, but its parent origin remains missing.",
            "current_status": "SUFFICIENT_CLAUSE_WRITTEN_NOT_ORIGIN_DERIVED",
            "source_path": str(RESIDUALS / "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "JZR3629_3_charge_current_orthogonality",
            "zero_condition": "extra charge/source channels have zero projection into the observed Hamiltonian mass current",
            "test": "Pi_M(Q_nonEH+Q_boundary+Q_domain+Q_memory+Q_range+Q_connection+Q_delta_kappa)=0",
            "result_if_pass": "mu_extra=0 and source-normalization leakage is killed before measured-GM fitting",
            "current_evidence": "charge-current file states the required zero but marks it not parent-derived.",
            "current_status": "MASS_SOURCE_ZERO_ROUTE_NOT_SIGNED",
            "source_path": str(RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "JZR3629_4_boundary_natural_source",
            "zero_condition": "variation of S_boundary gives no natural boundary source for Z and no linked-surface force flux",
            "test": "n_mu H_AB nabla^mu Z^B + B_A =0 with B_A=0/fixed-reference on the local collar",
            "result_if_pass": "bulk J_Z=0 is not spoiled by boundary alpha3/source-normalization leakage",
            "current_evidence": "boundary handoff remains open across 3627/3628 and prior source-normalization ledgers.",
            "current_status": "BOUNDARY_SOURCE_OPEN",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3628_QLOC_TGK_BOUND_RUNNER_ROWS.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "JZR3629_5_verdict",
            "zero_condition": "all matter, source-normalization, domain, memory, charge-current, and boundary J_Z sources vanish as parent consequences",
            "test": "JZR3629_0 through JZR3629_4 all pass simultaneously",
            "result_if_pass": "response-doublet branch becomes a real local-GR derivation route rather than closure",
            "current_evidence": "no route currently passes as parent-signed; coefficient rows are required.",
            "current_status": "JZ_ZERO_NOT_CLAIMED_COEFFICIENT_BRANCH_REQUIRED",
            "source_path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("JZC3629_0_gamma", "R3_gamma", "gamma_minus_1", "K_gamma_JZ * ||L^{-1}J_Z||_gamma", "MISSING_K_GAMMA_JZ_AND_L_INV_PROFILE", "PPN gamma bound row"),
        ("JZC3629_1_beta", "R4_beta", "beta_minus_1", "K_beta_JZ * ||L^{-1}J_Z||_beta + delta_beta_source", "MISSING_SECOND_ORDER_JZ_PROJECTION", "PPN beta/perihelion/LLR bound row"),
        ("JZC3629_2_preferred_frame", "R5_R6_R7_R8", "alpha1;alpha2;alpha3;xi", "P_PF(L^{-1}J_Z + boundary flux)", "MISSING_PREFERRED_FRAME_PROJECTION_AND_BOUNDS", "alpha_i/xi component bounds"),
        ("JZC3629_3_Newton_source", "R10_R11_Newton", "delta_Newton_MTS;alpha(lambda);mu_extra", "delta_mu_JZ = K_mu_JZ * Pi_M(L^{-1}J_Z)", "MISSING_SOURCE_MASS_AND_RANGE_PROFILE", "Newton/R10/source-normalization bounds"),
        ("JZC3629_4_clock", "R2_clock", "alpha_clock_redshift", "K_clock_JZ * frame_clock_projection(L^{-1}J_Z)", "MISSING_CLOCK_FRAME_PROJECTION", "clock/redshift bounds"),
        ("JZC3629_5_WEP_source", "R1_WEP_source_charge", "eta_source_AB", "Delta_AB ln mu_obs[J_Z]", "MISSING_SPECIES_SOURCE_COUPLING", "source-charge WEP bounds"),
        ("JZC3629_6_Gdot", "R9_Gdot", "Gdot_over_G", "partial_t ln mu_obs[J_Z]", "MISSING_TIME_DRIFT_SOURCE_PROJECTION", "local Gdot/ephemeris bounds"),
        ("JZC3629_7_EM_flux", "ENV3625_5_EM_source", "w_EM;Phi_EM_boundary", "K_EM_JZ * Poynting_or_bound_flux_projection", "MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION", "EM/WEP/clock/orbital flux rows"),
        ("JZC3629_8_R11_operator", "R11_EH_operator_ledger", "non_EH_operator_coefficients", "c_JZ_operator_vector from retained L^{-1}J_Z operator family", "MISSING_EXECUTABLE_OPERATOR_VECTOR", "R11 coefficient vector bounds"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coupling_id": coupling_id,
            "target_row": target_row,
            "observable": observable,
            "prediction_template": prediction,
            "zero_theorem_condition": "J_Z=0 from quotient descent/even total action/quadratic activation/charge-current orthogonality/boundary no-flux",
            "missing_input": missing_input,
            "required_bound_source": bound_source,
            "score_status": "not_scoreable",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for coupling_id, target_row, observable, prediction, missing_input, bound_source in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3629_0_coupling_law",
            "decision": "The exact coupling obstruction is now isolated: an even S_GK still fails if the total action has a linear J_Z source.",
            "status": "DERIVATION_PROGRESS",
            "next_action": "use J_Z, not vague coupling language, as the canonical local source block",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3629_1_best_zero_route",
            "decision": "The least-scrutiny zero route is quotient descent plus even/quadratic activation: matter sees q(Phi), while local residual variables enter only at order Z^2.",
            "status": "BEST_ROUTE_SELECTED_NOT_SIGNED",
            "next_action": "attempt to parent-sign quotient verticality and total-action evenness/quadratic activation together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3629_2_current_claim",
            "decision": "J_Z=0 is not claimed because quotient matter descent, source-normalization charge-current orthogonality, and boundary no-flux remain unsigned.",
            "status": "NO_CLAIM",
            "next_action": "retain coefficient rows for every local residual channel",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3629_3_next_target",
            "decision": "Next target should merge the quotient descent and quadratic activation routes into one parent action clause, or deliberately demote J_Z to coefficient testing.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3630-Y5-R2FR-parent-action-total-evenness-quotient-descent-or-JZ-bound-runner.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3629_0",
            "result": "JZ_COUPLING_LAW_DERIVED_ZERO_ROUTE_UNSIGNED_COEFFICIENT_ROWS_STAGED",
            "summary": "3629 derives the exact source-coupling obstruction for the response-doublet local branch: L_AB Z^B + J_A=0, so the double-zero action only gives local silence if the total matter/source/boundary action has J_Z=0. Quotient descent, total Z-evenness, quadratic activation, charge-current orthogonality, and boundary no-flux are sufficient routes, but none is parent-signed yet; coefficient rows are staged for PPN, Newton/R10, clocks, WEP, Gdot, EM flux, and R11.",
            "coupling_law_derived": True,
            "JZ_zero_claimed": False,
            "coefficient_rows_staged": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3629_0",
            "target_doc": "3630-Y5-R2FR-parent-action-total-evenness-quotient-descent-or-JZ-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_3630_parent_action_total_evenness_quotient_descent_or_JZ_bound_runner.py",
            "objective": "try to write the single parent-action clause that simultaneously signs quotient matter descent, total Z-evenness/quadratic activation, charge-current orthogonality, and boundary no-flux; if not, run J_Z coefficient-bound scaffolding",
            "success_gate": "J_Z=0 is parent-signed for matter, source-normalization, domain/memory, and boundary pieces, or every J_Z channel has a source-ready coefficient row with units, projection, and local bound",
            "reason": "3629 shows the coupling is the live bottleneck; 3630 must either turn the best route into a parent action clause or stop pretending it is derivable yet.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "response_doublet_source_coupling",
            "canonical_status": "JZ_LAW_DERIVED_ZERO_UNSIGNED",
            "usable_result": "local response profile is Z=-L^{-1}J_Z plus boundary terms; J_Z=0 is the exact source-silence theorem target",
            "hard_block": "parent-sign quotient matter descent, total Z-evenness/quadratic activation, charge-current orthogonality, and boundary no-flux",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, object]],
    coupling_law: list[dict[str, object]],
    zero_routes: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 3629 Y5 R2FR response-doublet source coupling zero or coefficient",
            f"**Status:** {status[0]['summary']}",
            "**Claim ceiling:** no `J_Z=0`, local-GR, Newton, PPN, R10/R11, WEP, clock, Gdot, or EM-source claim is allowed from 3629.",
            "## Core result",
            (
                "This checkpoint pins the coupling down instead of waving at it. For the even response-doublet action, the linearized local equation is:\n\n"
                "```text\n"
                "L_AB Z^B + J_A + O(Z^2)=0\n"
                "L_AB = -nabla_mu(H_AB nabla^mu) + M_AB\n"
                "J_A = (1/sqrt(-g)) delta(S_matter + S_source_norm + S_boundary)/delta Z^A |_{Z=0}\n"
                "```\n\n"
                "So the double-zero mechanism from 3628 is real but conditional: `Z=0` is derived only if the total action has `J_Z=0` and no boundary natural source. "
                "If not, the physical profile is `Z=-L^{-1}J_Z` plus boundary terms, which must be scored through PPN/Newton/R10/clock/WEP/EM/R11 rows."
            ),
            "## Source register",
            md_table(source_register, ["source_id", "path", "exists", "needle_found", "role"]),
            "## Coupling law",
            md_table(coupling_law, ["law_id", "statement", "formula", "meaning", "status"]),
            "## J_Z zero route audit",
            md_table(zero_routes, ["route_id", "zero_condition", "test", "result_if_pass", "current_status"]),
            "## Coefficient rows",
            md_table(
                coefficients,
                [
                    "coupling_id",
                    "target_row",
                    "observable",
                    "prediction_template",
                    "missing_input",
                    "required_bound_source",
                    "score_status",
                ],
            ),
            "## Decisions",
            md_table(decisions, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            md_table(next_target, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate_outputs(paths: dict[str, Path], source_register: list[dict[str, object]]) -> list[dict[str, object]]:
    timestamp = utc_now()
    validation: list[dict[str, object]] = []

    def add(validation_id: str, result: bool, detail: str) -> None:
        validation.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if result else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3629_0_sources_exist", all(row["exists"] for row in source_register), "all sources exist")
    add("VAL3629_1_needles_found", all(row["needle_found"] for row in source_register), "all source anchors found")

    pre_validation_outputs = {name: path for name, path in paths.items() if name != "validation"}
    add("VAL3629_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()) and DOC.exists(), "all pre-validation outputs written")

    parse_details: list[str] = []
    csv_parse_ok = True
    for name, path in pre_validation_outputs.items():
        try:
            row_count = len(read_csv(path))
            parse_details.append(f"{name}:{row_count}")
            csv_parse_ok = csv_parse_ok and row_count > 0
        except Exception as exc:
            parse_details.append(f"{name}:ERR:{exc}")
            csv_parse_ok = False
    add("VAL3629_3_csv_parse", csv_parse_ok, "; ".join(parse_details))

    coupling_rows = read_csv(paths["coupling_law"])
    zero_rows = read_csv(paths["zero_routes"])
    coeff_rows = read_csv(paths["coefficient_rows"])
    decision_rows_loaded = read_csv(paths["decision_gates"])
    status_rows_loaded = read_csv(paths["status"])
    next_rows = read_csv(paths["next_target"])

    add(
        "VAL3629_4_coupling_law_written",
        any("L_AB Z^B + J_A" in row["formula"] for row in coupling_rows),
        "linearized J_Z coupling law written",
    )
    add(
        "VAL3629_5_profile_bound_written",
        any("L^{-1}" in row["formula"] for row in coupling_rows),
        "nonzero J_Z profile/bound route written",
    )
    add(
        "VAL3629_6_zero_routes_cover_descent_evenness_quadratic_boundary",
        all(
            any(token in row["zero_condition"] or token in row["route_id"] for row in zero_rows)
            for token in ["quotient", "even", "p>=2", "boundary"]
        ),
        "zero-route audit covers quotient, evenness, quadratic activation, and boundary source",
    )
    add(
        "VAL3629_7_coefficient_rows_cover_local_scorecard",
        len(coeff_rows) >= 8
        and any(row["target_row"] == "R11_EH_operator_ledger" for row in coeff_rows)
        and any(row["target_row"] == "R5_R6_R7_R8" for row in coeff_rows),
        "J_Z coefficient rows cover PPN/Newton/R10/clock/WEP/Gdot/EM/R11",
    )
    add(
        "VAL3629_8_JZ_zero_not_claimed",
        all(row["valid_for_claim"].lower() == "false" for row in zero_rows)
        and any("NOT_CLAIMED" in row["current_status"] for row in zero_rows),
        "J_Z zero remains unsigned",
    )
    add(
        "VAL3629_9_coefficients_nonclaim",
        all(row["valid_for_claim"].lower() == "false" and row["score_status"] == "not_scoreable" for row in coeff_rows),
        "all coefficient rows remain nonclaim/not scoreable",
    )
    add(
        "VAL3629_10_status_decision_nonclaim",
        all(row["valid_for_claim"].lower() == "false" for row in status_rows_loaded + decision_rows_loaded + next_rows),
        "status, decision, and next rows remain nonclaim",
    )
    formalization_leak = list(FORMALIZATION.rglob("*3629*")) if FORMALIZATION.exists() else []
    add("VAL3629_11_no_formalization_leak", not formalization_leak, "no 3629 files in formalization-workbench")
    add("VAL3629_12_next_target_written", bool(next_rows) and "3630" in next_rows[0]["target_doc"], "3630 parent-action target written")
    add(
        "VAL3629_13_canonical_status_written",
        paths["canonical_status"].exists() and "JZ_LAW_DERIVED_ZERO_UNSIGNED" in paths["canonical_status"].read_text(encoding="utf-8", errors="replace"),
        "canonical response-doublet coupling status written",
    )
    return validation


def main() -> None:
    timestamp = utc_now()
    paths = output_paths()

    source_register = source_register_rows(timestamp)
    coupling_law = coupling_law_rows(timestamp)
    zero_routes = zero_route_rows(timestamp)
    coefficients = coefficient_rows(timestamp)
    decisions = decision_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_target_rows(timestamp)
    canonical_status = canonical_status_rows(timestamp)

    write_csv(paths["source_register"], source_register)
    write_csv(paths["coupling_law"], coupling_law)
    write_csv(paths["zero_routes"], zero_routes)
    write_csv(paths["coefficient_rows"], coefficients)
    write_csv(paths["decision_gates"], decisions)
    write_csv(paths["status"], status)
    write_csv(paths["next_target"], next_target)
    write_csv(paths["canonical_status"], canonical_status)

    write_doc(source_register, coupling_law, zero_routes, coefficients, decisions, status, next_target)

    validation = validate_outputs(paths, source_register)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3629 validation failed: {failed}")
    print(f"wrote 3629 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
