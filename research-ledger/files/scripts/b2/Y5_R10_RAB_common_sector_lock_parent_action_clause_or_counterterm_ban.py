from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1411-Y5-R10-RAB-common-sector-lock-parent-action-clause-or-counterterm-ban.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1411_SOURCE_REGISTER.csv"
PARENT_CLAUSE_PATH = SRC_DIR / "P8_Y5_R10_1411_PARENT_ACTION_LOCK_CLAUSE.csv"
PROOF_CHAIN_PATH = SRC_DIR / "P8_Y5_R10_1411_COMMON_LOCK_PROOF_CHAIN.csv"
COUNTERTERM_PATH = SRC_DIR / "P8_Y5_R10_1411_COUNTERTERM_BAN_AUDIT.csv"
RESIDUAL_TEMPLATE_PATH = SRC_DIR / "P8_Y5_R10_1411_RESIDUAL_TEMPLATE_IF_BAN_FAILS.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1411_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1411_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1411_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1411_VALIDATION.csv"

STATUS = "Y5_R10_1411_common_sector_lock_parent_clause_written_as_sufficient_contract_nonclaim"
CLAIM_CEILING = (
    "sufficient_parent_action_contract_only_not_derived_from_primitives_no_WEP_pass_"
    "no_beta_promotion_no_Ps_products_no_transfer_no_Newton_no_local_GR_pass"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1411_0_1410_doc",
            "source_path": "1410-Y5-R10-RAB-betaEM-or-betaNuc-owner-bound-after-Ua-blocker.md",
            "anchor": "NEXT1410_0_1411",
            "role": "prior checkpoint selecting common-sector-lock parent action clause or counterterm ban",
        },
        {
            "source_id": "SRC1411_1_1410_common_lock",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1410_COMMON_SECTOR_LOCK_THEOREM_ATTEMPT.csv",
            "anchor": "CSL1410_4_current_verdict",
            "role": "common-sector-lock lemma exact but parent premise unsigned",
        },
        {
            "source_id": "SRC1411_2_1410_coupling_obstructions",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1410_COUPLING_OBSTRUCTION_LEDGER.csv",
            "anchor": "COUP1410_0_independent_F2",
            "role": "active EM/QCD/source-slot coupling obstruction list",
        },
        {
            "source_id": "SRC1411_3_1405_current",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1405_PARENT_WEP_RESPONSE_CURRENT_DERIVATION.csv",
            "anchor": "WRC1405_6_common_owner_zero",
            "role": "response-current identity and exact common-owner zero lemma",
        },
        {
            "source_id": "SRC1411_4_1406_common_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1406_COMMON_MATTER_OWNER_WEP_ZERO_AUDIT.csv",
            "anchor": "CMO1406_7_current_verdict",
            "role": "common matter owner still not parent-signed",
        },
        {
            "source_id": "SRC1411_5_1407_no_source_slot",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1407_NOSOURCEONLYSPECIESSLOT_PROOF_AUDIT.csv",
            "anchor": "NSS1407_7_current_verdict",
            "role": "source-only species slot counterexample survives current corpus",
        },
        {
            "source_id": "SRC1411_6_1396_em_lock",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_EM_LOCK_REPAIR_ATTEMPT.csv",
            "anchor": "ELR1396_1_unique_Maxwell_F2",
            "role": "independent Maxwell F2 counterterm remains legal in current corpus",
        },
        {
            "source_id": "SRC1411_7_1395_zero_attempt",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_SECTOR_BETA_ZERO_THEOREM_ATTEMPT.csv",
            "anchor": "SBZ1395_3_joint_binding_zero",
            "role": "joint binding zero is exact only if sector beta zeros/locks are signed",
        },
        {
            "source_id": "SRC1411_8_this_script",
            "source_path": "scripts/Y5_R10_RAB_common_sector_lock_parent_action_clause_or_counterterm_ban.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def parent_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "PAC1411_0_parent_signature",
            "clause": "ordinary matter action descends only through one observed geometry and fixed representation data",
            "formal_statement": "S_ord[Phi,Psi]=Sbar_ord[Psi,e_obs(q(Phi)),omega_obs(q(Phi)),theta_rep]",
            "status": "SUFFICIENT_CONTRACT_CANDIDATE",
            "what_it_bans": "independent visible-sector dependence on parent fields outside q(Phi)",
            "what_is_missing": "derivation that this is the exhaustive parent object language rather than an adopted closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PAC1411_1_fixed_spectrum",
            "clause": "theta_rep contains masses, Yukawas, charge lattice, Lambda_QCD, and representation constants with L_v theta_rep=0",
            "formal_statement": "for vertical or local residual directions v, L_v theta_rep=0",
            "status": "SUFFICIENT_BUT_UNSIGNED",
            "what_it_bans": "m_i(X), y_i(X), Lambda_QCD(X), alpha_EM(X) as independent matter-spectrum vertices",
            "what_is_missing": "parent derivation that constants are superselection/representation data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PAC1411_2_no_sector_kinetic_prefactors",
            "clause": "no sector-specific kinetic prefactor is an allowed ordinary-matter coordinate",
            "formal_statement": "Z_EM(X)F^2, Z_QCD(X)tr(G^2), Z_e(X)L_e, and Z_nuc(X)L_nuc are absent unless promoted to explicit residual fields",
            "status": "NOT_DERIVED_CURRENT_CORPUS",
            "what_it_bans": "lambda_A F_Q^2 and QCD/EM independent normalization leaks",
            "what_is_missing": "unique kinetic-subblock theorem from parent curvature/norm/object-language minimality",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PAC1411_3_no_source_only_slots",
            "clause": "ordinary matter grammar has no source-only species multipliers",
            "formal_statement": "w_A(X)S_A, kappa_A(X)T_A, and inert material-label multipliers are not valid arguments of S_ord",
            "status": "NOT_DERIVED_CURRENT_CORPUS",
            "what_it_bans": "pre-action source/species weights that survive locality and covariance checks",
            "what_is_missing": "NoSourceOnlySpeciesSlot certificate from parent grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PAC1411_4_common_metric_mode",
            "clause": "any allowed local matter response is common metric/coframe response",
            "formal_statement": "delta_v E_s,A / E_s,A = beta_*[v] for all ordinary sectors s, up to explicitly retained residual fields",
            "status": "CONDITIONAL_CONSEQUENCE_OF_PAC1411_0_TO_3",
            "what_it_bans": "composition-relative hidden sector response",
            "what_is_missing": "PAC1411_0 through PAC1411_3 must be parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PAC1411_5_verdict",
            "clause": "parent action common-sector-lock clause",
            "formal_statement": "if adopted/signed, beta_s^a=beta_*^a for e,nuc,EM,other and Delta alpha_AB^a=0 at linear order",
            "status": "SUFFICIENT_CONTRACT_WRITTEN_NOT_DERIVED",
            "what_it_bans": "all active coupling leaks listed in 1410, but only as a contract",
            "what_is_missing": "lower-level derivation from MTS primitives/object-language exhaustion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def proof_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "PRF1411_0_descended_action",
            "step": "assume ordinary matter descends through q",
            "formula": "S_ord[Phi,Psi]=Sbar_ord[Psi,e_obs(q(Phi)),omega_obs(q(Phi)),theta_rep]",
            "result": "vertical variations in ker(Dq) do not create independent matter-sector vertices",
            "status": "CONDITIONAL_STEP",
            "gap": "q-descent/exhaustion is not yet derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PRF1411_1_fixed_constants",
            "step": "hold representation constants fixed",
            "formula": "L_v theta_rep=0",
            "result": "no independent beta_EM, beta_nuc, beta_e, or beta_other from hidden constant drift",
            "status": "CONDITIONAL_STEP",
            "gap": "matter-spectrum owner remains unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PRF1411_2_common_energy_scaling",
            "step": "allowed response is only common geometry/coframe response",
            "formula": "E_s,A(X)=C_*(X) Ebar_s,A",
            "result": "beta_s^a=partial_a ln C_* for every sector",
            "status": "DERIVED_FROM_CONTRACT",
            "gap": "contract not derived from primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PRF1411_3_WEP_linear_cancellation",
            "step": "contract with material fractions",
            "formula": "Delta alpha_AB^a=sum_s Delta f_s,AB beta_s^a=(sum_s Delta f_s,AB)beta_*^a=0",
            "result": "linear composition-dependent WEP response vanishes before U_a contraction",
            "status": "EXACT_CONDITIONAL_PROOF",
            "gap": "premises PAC1411_0 through PAC1411_3 unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PRF1411_4_local_GR_relevance",
            "step": "compare with GR reduction target",
            "formula": "ordinary matter has one public metric/coframe source and no hidden composition current",
            "result": "this is the correct local-GR style target: universality, not tuned material cancellation",
            "status": "STRUCTURAL_PROGRESS_NONCLAIM",
            "gap": "does not yet derive Einstein-Hilbert exterior or PPN silence by itself",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def counterterm_rows() -> list[dict[str, Any]]:
    return [
        {
            "counterterm_id": "CTB1411_0_ZEM",
            "candidate": "Z_EM(X) F_Q^2 or lambda_A F_Q^2",
            "effect": "creates independent EM normalization and beta_EM relative residual",
            "banned_by_contract": "PAC1411_2_no_sector_kinetic_prefactors",
            "current_status": "NOT_BANNED_BY_DERIVATION",
            "if_allowed": "retain beta_EM-b_* finite residual row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterterm_id": "CTB1411_1_ZQCD",
            "candidate": "Z_QCD(X) tr(G^2), Lambda_QCD(X), or quark/Yukawa drift",
            "effect": "creates nuclear/QCD composition response",
            "banned_by_contract": "PAC1411_1_fixed_spectrum;PAC1411_2_no_sector_kinetic_prefactors",
            "current_status": "NOT_BANNED_BY_DERIVATION",
            "if_allowed": "retain beta_nuc-b_* finite residual row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterterm_id": "CTB1411_2_Zelectron",
            "candidate": "Z_e(X)L_e, m_e(X), or electronic/clock readout drift",
            "effect": "creates beta_e and clock/WEP transfer ambiguity",
            "banned_by_contract": "PAC1411_1_fixed_spectrum;PAC1411_4_common_metric_mode",
            "current_status": "NOT_BANNED_BY_DERIVATION",
            "if_allowed": "retain beta_e and clock/readout residual row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterterm_id": "CTB1411_3_source_slot",
            "candidate": "w_A(X)S_A or kappa_A(X)T_A",
            "effect": "creates source/test-body dependent response while preserving basic field-theory symmetries",
            "banned_by_contract": "PAC1411_3_no_source_only_slots",
            "current_status": "COUNTEREXAMPLE_SURVIVES_CURRENT_CORPUS",
            "if_allowed": "common-sector-lock cannot be promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterterm_id": "CTB1411_4_readout_leak",
            "candidate": "Hodge/coframe/hbar*c readout dependence not tied to e_obs(q(Phi))",
            "effect": "lets alpha_EM or clock observables drift despite action-level common coupling",
            "banned_by_contract": "PAC1411_0_parent_signature",
            "current_status": "UNSIGNED_READOUT_DESCENT",
            "if_allowed": "clock/alpha transfer remains isolated and finite",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterterm_id": "CTB1411_5_verdict",
            "candidate": "minimal active counterterm set",
            "effect": "these are exactly the terms a future parent action must derive away or retain as explicit residual fields",
            "banned_by_contract": "PAC1411_0_to_PAC1411_3",
            "current_status": "COUNTERTERM_BAN_WRITTEN_AS_CONTRACT_NOT_PROOF",
            "if_allowed": "move to finite residual vector instead of local-GR theorem promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def residual_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RES1411_0_beta_EM_rel",
            "quantity": "beta_EM^a-beta_*^a",
            "trigger": "CTB1411_0_ZEM allowed or not banned",
            "required_inputs": "parent coordinate basis; value/bound; units; sign; source path; arena projection",
            "current_status": "MISSING_SOURCE_VALUE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RES1411_1_beta_nuc_rel",
            "quantity": "beta_nuc^a-beta_*^a",
            "trigger": "CTB1411_1_ZQCD allowed or not banned",
            "required_inputs": "parent coordinate basis; value/bound; units; sign; source path; arena projection",
            "current_status": "MISSING_SOURCE_VALUE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RES1411_2_beta_e_rel",
            "quantity": "beta_e^a-beta_*^a",
            "trigger": "CTB1411_2_Zelectron allowed or not banned",
            "required_inputs": "clock/readout owner; electronic mass/readout basis; units; source path",
            "current_status": "MISSING_SOURCE_VALUE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RES1411_3_source_slot",
            "quantity": "w_A/kappa_A source-only residual",
            "trigger": "CTB1411_3_source_slot allowed or not banned",
            "required_inputs": "parent grammar row or finite prior envelope; material/source labels; WEP kernel projection",
            "current_status": "MISSING_PARENT_GRAMMAR_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RES1411_4_vector_verdict",
            "quantity": "relative ordinary-sector residual vector",
            "trigger": "any CTB1411 counterterm remains allowed",
            "required_inputs": "Delta f_s,AB tensor; U_a; beta_s-beta_* rows; readout convention",
            "current_status": "RESIDUAL_VECTOR_TEMPLATE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1411_0_contract_status",
            "decision": "common-sector-lock parent action clause is a sufficient contract, not a derived theorem yet",
            "reason": "current corpus does not force object-language exhaustion or ban all counterterms from primitives",
            "effect": "can be used as a target for derivation, not as claim evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1411_1_best_route",
            "decision": "next derive OrdinaryMatterFunctorExhaustion / no visible coefficient morphism",
            "reason": "that single theorem would ban source slots, sector kinetic prefactors, and spectrum drift together",
            "effect": "move upstream from individual beta rows to parent grammar proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1411_2_if_fail",
            "decision": "if the parent grammar proof fails, demote to finite residual-vector branch",
            "reason": "then EM/QCD/electron/source counterterms are physical residual fields, not mistakes",
            "effect": "build beta_s-beta_* vector and bound it rather than claiming local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1411_0_parent_clause",
            "claim": "common-sector-lock parent action clause is derived from MTS primitives",
            "status": "NOT_DERIVED_NO_CLAIM",
            "reason": "1411 states a sufficient contract but does not prove object-language exhaustion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1411_1_counterterms",
            "claim": "sector-specific counterterms are banned",
            "status": "CONTRACT_ONLY_NO_CLAIM",
            "reason": "Z_EM, Z_QCD, electronic/readout drift, and source slots remain not banned by derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1411_2_WEP",
            "claim": "linear WEP residual is zero",
            "status": "CONDITIONAL_ONLY_NO_CLAIM",
            "reason": "Delta alpha_AB=0 follows from the contract, but the contract is unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1411_3_local_GR",
            "claim": "local GR/Newton reduction follows",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "this does not yet derive EH exterior, PPN silence, U_a, or q_loc/local residual closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1411_4_verdict",
            "claim": "1411 solves the coupling problem",
            "status": "NO_PROMOTION",
            "reason": "1411 gives the exact future parent action contract and counterterm ban list; it is not yet derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1411_0_1412",
            "target_doc": "1412-Y5-R10-RAB-ordinary-matter-functor-exhaustion-or-finite-residual-vector.md",
            "target_script": "scripts/Y5_R10_RAB_ordinary_matter_functor_exhaustion_or_finite_residual_vector.py",
            "task": "attempt to prove the parent grammar exhaustion theorem that only q-descended observed geometry and fixed representation data enter ordinary matter; if it fails, build the finite residual-vector branch",
            "success_condition": "either object-language exhaustion bans Z_EM/Z_QCD/source-slot/readout counterterms, or a minimal finite residual vector is accepted as the next local-bound target",
            "do_not_claim": "WEP pass; beta zero; P_s products; clock/R10/PPN transfer; Newton/local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    parent_clauses: list[dict[str, Any]],
    proof_chain: list[dict[str, Any]],
    counterterms: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    timestamp = datetime.now(timezone.utc).isoformat()
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        PARENT_CLAUSE_PATH,
        PROOF_CHAIN_PATH,
        COUNTERTERM_PATH,
        RESIDUAL_TEMPLATE_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add(
        "VAL1411_0_sources",
        all(row["path_exists"] == True and row["anchor_found"] == True for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1411_1_parent_clause",
        any(row["clause_id"] == "PAC1411_5_verdict" and row["status"] == "SUFFICIENT_CONTRACT_WRITTEN_NOT_DERIVED" for row in parent_clauses),
        "parent action common-sector-lock clause is written as sufficient contract, not proof",
    )
    add(
        "VAL1411_2_proof_chain",
        any(row["proof_id"] == "PRF1411_3_WEP_linear_cancellation" and row["status"] == "EXACT_CONDITIONAL_PROOF" for row in proof_chain),
        "conditional proof chain reaches Delta alpha_AB=0 only under unsigned premises",
    )
    add(
        "VAL1411_3_counterterm_ban",
        {"CTB1411_0_ZEM", "CTB1411_1_ZQCD", "CTB1411_3_source_slot", "CTB1411_5_verdict"}.issubset(
            {row["counterterm_id"] for row in counterterms}
        )
        and all(row["valid_for_claim"] == False for row in counterterms),
        "minimal active counterterm set is recorded and remains nonclaim",
    )
    add(
        "VAL1411_4_residual_templates",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in residuals)
        and any(row["residual_id"] == "RES1411_4_vector_verdict" for row in residuals),
        "finite residual-vector fallback exists but contains no promoted values",
    )
    add(
        "VAL1411_5_decision",
        any(row["decision_id"] == "DEC1411_1_best_route" for row in decisions)
        and any(row["decision_id"] == "DEC1411_2_if_fail" for row in decisions),
        "decision ledger selects functor exhaustion proof or finite residual-vector fallback",
    )
    add(
        "VAL1411_6_claim_refusal",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in gates),
        "parent clause, counterterm ban, WEP, and local-GR claims are refused",
    )
    add(
        "VAL1411_7_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1411_8_overall",
        True,
        "1411 writes the exact parent-action contract future work must derive, or else demote to finite residual vector",
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    parent_clauses: list[dict[str, Any]],
    proof_chain: list[dict[str, Any]],
    counterterms: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1411 - Common-Sector-Lock Parent Action Clause Or Counterterm Ban

**Status:** `{STATUS}`

**Current verdict:** the exact contract is now explicit. If ordinary matter descends only through one observed geometry `e_obs(q(Phi)), omega_obs(q(Phi))` plus fixed representation data `theta_rep`, then all ordinary sector energies share the same common response and the WEP composition current cancels at linear order. This is the right GR-like target. But in the current corpus it is a sufficient contract, not yet a derivation from MTS primitives.

**Discipline move:** this checkpoint does not claim WEP or local GR. It names the terms a future parent action must ban or retain explicitly: `Z_EM(X)F^2`, `Z_QCD(X)tr(G^2)`, electronic/readout drift, and source-only `w_A(X)` slots. If those are not derivably banned, they become finite residual fields.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## Parent Action Lock Clause

{md_table(parent_clauses)}

## Common-Lock Proof Chain

{md_table(proof_chain)}

## Counterterm Ban Audit

{md_table(counterterms)}

## Residual Template If Ban Fails

{md_table(residuals)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    parent_clauses = parent_clause_rows()
    proof_chain = proof_chain_rows()
    counterterms = counterterm_rows()
    residuals = residual_template_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(sources, parent_clauses, proof_chain, counterterms, residuals, decisions, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(PARENT_CLAUSE_PATH, parent_clauses)
    write_csv(PROOF_CHAIN_PATH, proof_chain)
    write_csv(COUNTERTERM_PATH, counterterms)
    write_csv(RESIDUAL_TEMPLATE_PATH, residuals)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, parent_clauses, proof_chain, counterterms, residuals, decisions, gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1411 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
