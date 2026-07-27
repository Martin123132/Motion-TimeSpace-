from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "757-Y5-R10-response-doublet-physical-lock-or-real-q_loc-component-input.md"
NEXT_TARGET = "758-Y5-R10-full-residual-vector-parent-action-contract-or-component-input-acquisition.md"
STATUS = "Y5_R10_757_response_doublet_physical_lock_not_proved_full_residual_vector_contract_written_q_loc_component_input_still_required"
CLAIM_CEILING = "physical_lock_contract_and_component_input_decision_only_no_q_loc_zero_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_757_SOURCE_REGISTER.csv"
PHYSICAL_LOCK_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_757_PHYSICAL_LOCK_CONTRACT.csv"
PHYSICAL_LOCK_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_757_PHYSICAL_LOCK_ATTEMPT.csv"
RESIDUAL_BASIS_PATH = RESIDUALS / "P8_Y5_R10_757_RESIDUAL_VECTOR_BASIS.csv"
COMPONENT_DECISION_PATH = RESIDUALS / "P8_Y5_R10_757_QLOC_COMPONENT_INPUT_DECISION.csv"
CLAIM_STATUS_PATH = RESIDUALS / "P8_Y5_R10_757_ALPHA3_LOCAL_CLAIM_STATUS.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_757_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_757_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_757_VALIDATION.csv"

QLOC_COMPONENT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_CANDIDATE.csv"
PFLUX_PROJECTOR_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_755_PFLUX_PROJECTOR_INPUT.csv"
ALPHA3_RESPONSE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_755_ALPHA3_RESPONSE_OPERATOR_INPUT.csv"
ALPHA3_PRODUCT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_755_ALPHA3_PRODUCT_INPUT.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "756_doc": {
        "path": POST_CHECKPOINT / "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md",
        "needles": [
            "Current result: **the metric-response symbol match still fails for the current corpus**",
            "757-Y5-R10-response-doublet-physical-lock-or-real-q_loc-component-input.md",
        ],
        "role": "immediate 757 handoff",
    },
    "756_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_756_VALIDATION.csv",
        "needles": ["V756_16_validation_rows_ready", "V756_13_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "756_response_doublet": {
        "path": RESIDUALS / "P8_Y5_R10_756_RESPONSE_DOUBLET_REPAIR_ATTEMPT.csv",
        "needles": ["RDR756_3_verdict", "not_promoted_physical_lock_missing"],
        "role": "physical lock blocker",
    },
    "756_builder_schema": {
        "path": RESIDUALS / "P8_Y5_R10_756_QLOC_COMPONENT_CANDIDATE_BUILDER_SCHEMA.csv",
        "needles": ["QCB756_0_builder_schema", "no scalar q_proxy-only substitution"],
        "role": "component input fallback",
    },
    "756_dryrun": {
        "path": RESIDUALS / "P8_Y5_R10_756_QLOC_COMPONENT_CANDIDATE_DRYRUN.csv",
        "needles": ["QCD756_1_candidate_input_absent", "blocked_as_expected"],
        "role": "no fake component rows guard",
    },
    "517_doc": {
        "path": POST_CHECKPOINT / "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md",
        "needles": [
            "Z^A must equal the actual local residual vector through PPN/source-normalization order.",
            "The active blockers are still `Y5_source_normalization`, `Y6_stress_Bianchi`, boundary metric-response flux, and the full PPN lock.",
        ],
        "role": "response-doublet physical-lock target",
    },
    "518_doc": {
        "path": POST_CHECKPOINT / "518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "needles": [
            "ES518_2_physical_lock",
            "Y5 remains an active local-GR blocker",
        ],
        "role": "Y5 source-normalization blocker",
    },
    "519_doc": {
        "path": POST_CHECKPOINT / "519-fill-Y5-bound-runner-or-source-owner-clause.md",
        "needles": [
            "D519_3_source_measure",
            "Y5_owner_false_for_current_MTS",
        ],
        "role": "source-owner partial route and remaining source-measure gap",
    },
    "response_obstruction_ledger": {
        "path": RESIDUALS / "P8_RESPONSE_DOUBLET_OBSTRUCTION_LEDGER.csv",
        "needles": ["OB517_0_Y5_even_scalar", "OB517_2_PPN_lock"],
        "role": "physical residual lock obstructions",
    },
    "component_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_SCHEMA.csv",
        "needles": ["QIN750_3_q_loc_components", "component-resolved q_loc field/profile"],
        "role": "q_loc component row requirements",
    },
    "hodge_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_HODGE_COMPONENT_RUNNER_SCHEMA.csv",
        "needles": ["HRS750_3_fqV", "blocked_no_Palpha3_or_q_field"],
        "role": "component/Hodge runner requirements",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def physical_lock_contract_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PLC757_0_physical_residual_bundle",
            "required_clause": "Define the physical residual vector, not only an auxiliary exchange doublet.",
            "mathematical_form": "R_phys^I := (q_loc^nu/q_*, epsilon_mu, Delta T_extra^{mu nu}/T_*, Delta PPN_A, q_H/q_*, Delta_matter_coupling_A)",
            "why_needed": "Z=0 must mean the measured local deviations vanish, not merely an internal shadow variable.",
            "current_status": "contract_written_not_parent_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PLC757_1_lock_map",
            "required_clause": "The doublet variable is a full-rank local coordinate on R_phys.",
            "mathematical_form": "Z^A = N^A_I R_phys^I + O(R_phys^2), with rank(N)=dim(R_phys) on the tested local branch.",
            "why_needed": "No residual channel may sit in ker(N) while Z=0.",
            "current_status": "not_shown",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PLC757_2_norm_equivalence",
            "required_clause": "The quadratic action norm controls every physical channel.",
            "mathematical_form": "c_- ||R_phys||^2 <= Z^A M_AB Z^B <= c_+ ||R_phys||^2 for c_->0 in the local regime.",
            "why_needed": "A positive auxiliary norm must be coercive on q_loc, source normalization, stress, PPN, and boundary/matter-coupling residuals.",
            "current_status": "not_shown",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PLC757_3_no_linear_work",
            "required_clause": "The compact local equations contain no unsourced linear work term.",
            "mathematical_form": "L_IJ R_phys^J = J_I + B_I, with J_I=0 and B_I=0 in the compact local vacuum branch.",
            "why_needed": "A linear source or boundary term drives a residual even when the quadratic double-zero is formal.",
            "current_status": "not_shown_for_Y5_Y6_boundary",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PLC757_4_coupling_owner",
            "required_clause": "Matter, clocks, source charge, photons, and orbit readout couple through one parent-owned observed structure.",
            "mathematical_form": "S_matter = Sbar[g_obs or e_obs, Psi] with no independent species/frame/source/readout labels through weak-field order.",
            "why_needed": "This is where the coupling issue bites: uncoupled readout sectors can hide Y5, WEP, clock, PPN, or orbital residuals outside Z.",
            "current_status": "partial_same_coframe_clause_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PLC757_5_zero_theorem",
            "required_clause": "Only after PLC757_0..PLC757_4 close may the response-doublet imply local silence.",
            "mathematical_form": "positive action + full-rank lock + no source/boundary work => R_phys=0 => q_loc=epsilon_mu=DeltaT=DeltaPPN=q_H=DeltaCoupling=0",
            "why_needed": "This would be the serious route to derived local GR rather than a plateau axiom.",
            "current_status": "conditional_theorem_not_current_MTS_claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def residual_basis_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "RVB757_0_q_loc_vector",
            "physical_channel": "observed local leakage vector",
            "representative_quantity": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "parity_or_type": "vector / preferred-frame sensitive",
            "required_lock": "Z_q^nu equals normalized q_loc^nu components in the observed frame",
            "current_gap": "Gamma/Khat/P_loc owner and component input are absent",
            "test_arenas": "alpha3, PPN, R10/local force, compact-orbit residuals",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "basis_id": "RVB757_1_Y5_source_normalization",
            "physical_channel": "measured source strength / Newton normalization",
            "representative_quantity": "epsilon_mu = mu_extra/(G_eff M_H)",
            "parity_or_type": "exchange-even scalar",
            "required_lock": "Z_mu equals epsilon_mu and every mu_extra subchannel through weak-field order",
            "current_gap": "source current closure, no-extra-mass projection, Gauss/orbital calibration, and PPN stability are not derived",
            "test_arenas": "Newton limit, clocks, WEP/source universality, orbital systems",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "basis_id": "RVB757_2_Y6_extra_stress",
            "physical_channel": "non-EH local stress",
            "representative_quantity": "Delta T_extra^{mu nu}",
            "parity_or_type": "exchange-even/conserved tensor possible",
            "required_lock": "Z_T controls every conserved or topological extra stress component",
            "current_gap": "Bianchi-conserved stress can sit in q_loc kernel unless explicitly included or proven invisible",
            "test_arenas": "PPN beta/gamma, lensing, local exterior metric, stress-energy conservation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "basis_id": "RVB757_3_PPN_vector",
            "physical_channel": "weak-field metric coefficients",
            "representative_quantity": "Delta PPN_A = {gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta_i,Gdot,R11}",
            "parity_or_type": "mixed scalar/vector/tensor response",
            "required_lock": "Z_PPN has an invertible linear response to the full PPN residual vector",
            "current_gap": "no sourced response operator maps response-doublet components to PPN coefficients",
            "test_arenas": "solar-system PPN, pulsars, preferred-frame tests, time drift",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "basis_id": "RVB757_4_boundary_harmonic_flux",
            "physical_channel": "boundary/harmonic local flux",
            "representative_quantity": "q_H and P_flux P_Hodge q_loc",
            "parity_or_type": "boundary/topological/harmonic",
            "required_lock": "Z_H controls the harmonic boundary piece or a no-flux theorem kills it",
            "current_gap": "proper representative boundary silence does not yet imply observed reduced boundary silence",
            "test_arenas": "alpha3 product, local force residuals, compact-shell leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "basis_id": "RVB757_5_matter_coupling",
            "physical_channel": "universal matter/readout coupling",
            "representative_quantity": "Delta_matter_coupling_A = species/frame/source/photon/clock/orbit pullback residuals",
            "parity_or_type": "coupling/responsivity vector",
            "required_lock": "Z_coupling controls all departures from one observed matter/coframe coupling",
            "current_gap": "same-coframe clause is partial; full quotient-invariant matter action and source/readout descent remain unsigned",
            "test_arenas": "WEP, clocks, EM, orbital readout, source calibration",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def physical_lock_attempt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "PLA757_0_formal_auxiliary_zero",
            "target": "Z auxiliary fixed point",
            "test": "Does response-doublet action give delta Gamma_eff/delta Z=0 at Z=0?",
            "result": "pass_formal_only",
            "reason": "517/756 already establish the formal quadratic double-zero under no linear source/boundary terms",
            "consequence": "useful parent-action shape retained",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PLA757_1_q_loc_lock",
            "target": "Z_q == q_loc components",
            "test": "Can q_loc components be identified with a full-rank subset of Z?",
            "result": "not_proved",
            "reason": "756 failed Gamma/Khat metric-response ownership and no component-resolved q_loc input exists",
            "consequence": "alpha3 theorem-zero and numeric component route both remain blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PLA757_2_Y5_lock",
            "target": "Z_mu == source-normalization residual",
            "test": "Can the exchange-doublet zero force epsilon_mu=0?",
            "result": "fails_current_route",
            "reason": "Y5 is an observed exchange-even scalar; same-coframe helps but source current closure, mu_extra=0, Gauss calibration, and PPN stability are not derived",
            "consequence": "source-normalized Newton remains blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PLA757_3_Y6_lock",
            "target": "Z_T == extra-stress residual",
            "test": "Can q_loc or exchange-odd Z kill all non-EH stress?",
            "result": "not_proved",
            "reason": "a conserved exchange-even extra stress can be Bianchi-silent and still alter local metric coefficients",
            "consequence": "EH-only local exterior and PPN beta/gamma remain blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PLA757_4_PPN_lock",
            "target": "Z_PPN == full weak-field residual vector",
            "test": "Can Z=0 be shown equivalent to gamma=beta=1, alpha_i=xi=zeta_i=Gdot=R11=0?",
            "result": "not_proved",
            "reason": "no sourced linear response operator from Z to the PPN coefficient vector exists",
            "consequence": "preferred-frame and post-Newtonian claims remain blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PLA757_5_boundary_coupling_lock",
            "target": "Z_H and Z_coupling",
            "test": "Can boundary/harmonic flux and matter-coupling residuals be forced into the same positive norm?",
            "result": "not_proved",
            "reason": "observed boundary silence and full quotient-invariant matter/source/readout descent are not signed",
            "consequence": "local force, clock, WEP, EM/readout coupling checks remain explicit residual gates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PLA757_6_verdict",
            "target": "promote response-doublet to physical residual zero theorem",
            "test": "Do PLA757_1..PLA757_5 close?",
            "result": "physical_lock_not_proved",
            "reason": "the formal double-zero does not yet control the full measured residual vector",
            "consequence": "write full residual-vector contract; require real q_loc component input if theorem route is not closed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def component_decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "QCI757_0_no_q_loc_candidate_written",
            "artifact": str(QLOC_COMPONENT_CANDIDATE_PATH),
            "decision": "do not fabricate component rows",
            "required_before_claim": "real q_loc^nu field/profile or theorem-zero certificate sourced to parent equations",
            "current_status": f"exists={bool_string(QLOC_COMPONENT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "QCI757_1_projector_operator_missing",
            "artifact": str(PFLUX_PROJECTOR_CANDIDATE_PATH),
            "decision": "do not compute f_qV",
            "required_before_claim": "Hodge/flux projector and boundary operator in the same domain/frame as q_loc components",
            "current_status": f"projector_exists={bool_string(PFLUX_PROJECTOR_CANDIDATE_PATH.exists())}; response_exists={bool_string(ALPHA3_RESPONSE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "QCI757_2_product_not_scoreable",
            "artifact": str(ALPHA3_PRODUCT_CANDIDATE_PATH),
            "decision": "retain alpha3 product gate only",
            "required_before_claim": f"abs(W_q_alpha3*f_qV) <= {WF_LIMIT:.15g} with sourced W and f",
            "current_status": f"exists={bool_string(ALPHA3_PRODUCT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_status_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLS757_0_local_GR",
            "arena": "local GR reduction",
            "status": "blocked",
            "reason": "full residual-vector lock not proved",
            "minimum_exit": "PLC757_0..PLC757_5 parent-signed or all residual channels bounded below tests",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim_id": "CLS757_1_Newton_Y5",
            "arena": "source-normalized Newton",
            "status": "blocked",
            "reason": "Y5 exchange-even source residual not controlled by exchange-odd doublet",
            "minimum_exit": "derive source current closure, mu_extra=0, Gauss calibration, and PPN source stability",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim_id": "CLS757_2_alpha3",
            "arena": "preferred-frame alpha3",
            "status": "blocked",
            "reason": "no q_loc theorem-zero and no component/operator product",
            "minimum_exit": f"P_flux P_Hodge q_loc=0 theorem or abs(W_q_alpha3*f_qV) <= {WF_LIMIT:.15g}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "claim_id": "CLS757_3_coupling",
            "arena": "matter/source/readout coupling",
            "status": "blocked",
            "reason": "same-coframe clause is useful but not full quotient-invariant matter action/source descent",
            "minimum_exit": "one parent-owned matter/coframe/source/orbit action with no species, frame, or source-charge leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU757_0_allowed",
            "allowed_after_757": "say the response-doublet gives a formal auxiliary double-zero",
            "forbidden_after_757": "say that formal Z=0 proves observed local residuals vanish",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU757_1_allowed",
            "allowed_after_757": "use the full residual-vector contract as the stricter parent-action target",
            "forbidden_after_757": "hide Y5, Y6, PPN, boundary, or coupling residuals in an unobserved auxiliary kernel",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU757_2_allowed",
            "allowed_after_757": "build real q_loc component inputs if the theorem route does not close",
            "forbidden_after_757": "fill q_loc rows with placeholders, q_proxy-only rows, or unsourced response operators",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "physical lock not proved; stricter full residual-vector parent-action contract written",
            "hard_blocker": "Z must be full-rank/coercive on q_loc, Y5, Y6, PPN, boundary, and coupling residuals",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    basis: list[dict[str, Any]],
    attempt: list[dict[str, Any]],
    component: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V757_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V757_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_756 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_756_VALIDATION.csv")
    validation.append({"check_id": "V757_2_prior_756_clean", "result": "pass" if prior_756 and all(row.get("result") == "pass" for row in prior_756) else "fail", "detail": "756 validation has no failures"})
    validation.append({"check_id": "V757_3_contract_written", "result": "pass" if len(contract) == 6 and any(row["contract_id"] == "PLC757_5_zero_theorem" for row in contract) else "fail", "detail": "full residual-vector lock contract recorded"})
    validation.append({"check_id": "V757_4_residual_basis_complete", "result": "pass" if len(basis) >= 6 and all(row["valid_for_claim"] == "false" for row in basis) else "fail", "detail": "q_loc/Y5/Y6/PPN/boundary/coupling basis rows present"})
    validation.append({"check_id": "V757_5_physical_lock_not_proved", "result": "pass" if any(row["attempt_id"] == "PLA757_6_verdict" and row["result"] == "physical_lock_not_proved" for row in attempt) else "fail", "detail": "formal Z route not promoted"})
    validation.append({"check_id": "V757_6_component_input_absent", "result": "pass" if not QLOC_COMPONENT_CANDIDATE_PATH.exists() else "fail", "detail": str(QLOC_COMPONENT_CANDIDATE_PATH)})
    validation.append({"check_id": "V757_7_no_candidate_artifacts_faked", "result": "pass" if not any(path.exists() for path in [QLOC_COMPONENT_CANDIDATE_PATH, PFLUX_PROJECTOR_CANDIDATE_PATH, ALPHA3_RESPONSE_CANDIDATE_PATH, ALPHA3_PRODUCT_CANDIDATE_PATH]) else "fail", "detail": "no claim-input artifacts fabricated"})
    validation.append({"check_id": "V757_8_alpha3_claim_blocked", "result": "pass" if any(row["claim_id"] == "CLS757_2_alpha3" and row["status"] == "blocked" for row in claims) else "fail", "detail": "alpha3 remains blocked"})
    all_generated = contract + basis + attempt + component + claims + routes + summary
    validation.append({"check_id": "V757_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V757_10_no_local_arena_claim", "result": "pass" if "no_q_loc_zero_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "local claims remain blocked"})
    validation.append({"check_id": "V757_11_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        PHYSICAL_LOCK_CONTRACT_PATH,
        PHYSICAL_LOCK_ATTEMPT_PATH,
        RESIDUAL_BASIS_PATH,
        COMPONENT_DECISION_PATH,
        CLAIM_STATUS_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V757_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V757_13_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V757_14_coupling_gap_explicit", "result": "pass" if any(row["basis_id"] == "RVB757_5_matter_coupling" for row in basis) and any(row["contract_id"] == "PLC757_4_coupling_owner" for row in contract) else "fail", "detail": "matter/source/readout coupling included as hard channel"})
    validation.append({"check_id": "V757_15_route_forbids_auxiliary_kernel_hiding", "result": "pass" if any("auxiliary kernel" in row["forbidden_after_757"] for row in routes) else "fail", "detail": "no hidden-kernel overclaim allowed"})
    validation.append({"check_id": "V757_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    basis: list[dict[str, Any]],
    attempt: list[dict[str, Any]],
    component: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 757 - Y5 R10 Response-Doublet Physical Lock Or Real q_loc Component Input

Start point: 756 kept the response-doublet as the cleanest formal mechanism, but refused to promote it because `Z^A` was not physically locked to observed residuals.

Current result: **the physical lock is not proved**. The formal double-zero survives, but only as an auxiliary construction. To make it serious, the parent action must control the whole measured residual vector: `q_loc`, Y5 source normalization, Y6 extra stress, PPN coefficients, boundary/harmonic flux, and matter/source/readout coupling. This is the coupling problem showing its teeth.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Physical Lock Contract

{markdown_table(contract, ["contract_id", "required_clause", "mathematical_form", "why_needed", "current_status", "valid_for_claim"])}

## Residual Vector Basis

{markdown_table(basis, ["basis_id", "physical_channel", "representative_quantity", "parity_or_type", "required_lock", "current_gap", "test_arenas", "valid_for_claim"])}

## Physical Lock Attempt

{markdown_table(attempt, ["attempt_id", "target", "test", "result", "reason", "consequence", "valid_for_claim"])}

## q_loc Component Input Decision

{markdown_table(component, ["decision_id", "artifact", "decision", "required_before_claim", "current_status", "valid_for_claim"])}

## Alpha3 And Local Claim Status

{markdown_table(claims, ["claim_id", "arena", "status", "reason", "minimum_exit", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_757", "forbidden_after_757", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

The response-doublet is not dead; it is too narrow unless it is upgraded. The correct version is not simply `Z` as a pretty exchange-odd variable. It is a full residual-vector norm with a full-rank lock to the actual measured channels. That is the least-cheaty theorem route. If we cannot parent-sign that contract, the honest fallback is the data route: real component-resolved `q_loc`, real Hodge/flux projector, real PPN response operator, and only then an alpha3 product.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    contract = physical_lock_contract_rows(generated_utc)
    basis = residual_basis_rows(generated_utc)
    attempt = physical_lock_attempt_rows(generated_utc)
    component = component_decision_rows(generated_utc)
    claims = claim_status_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, contract, basis, attempt, component, claims, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(PHYSICAL_LOCK_CONTRACT_PATH, contract, ["contract_id", "required_clause", "mathematical_form", "why_needed", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUAL_BASIS_PATH, basis, ["basis_id", "physical_channel", "representative_quantity", "parity_or_type", "required_lock", "current_gap", "test_arenas", "valid_for_claim", "generated_utc"])
    write_csv(PHYSICAL_LOCK_ATTEMPT_PATH, attempt, ["attempt_id", "target", "test", "result", "reason", "consequence", "valid_for_claim", "generated_utc"])
    write_csv(COMPONENT_DECISION_PATH, component, ["decision_id", "artifact", "decision", "required_before_claim", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_STATUS_PATH, claims, ["claim_id", "arena", "status", "reason", "minimum_exit", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_757", "forbidden_after_757", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, contract, basis, attempt, component, claims, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        print(f"wrote {OUTPUT_DOC}")
        print(f"wrote {VALIDATION_PATH}")
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
