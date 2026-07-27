from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3221-Y5-R2FR-EM-source-root-owner-hunt-or-finite-coefficient-row-promotion-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3221_INPUTS.csv"
OWNER = OUT / "P8_Y5_R2FR_3221_EM_OWNER_CANDIDATE_AUDIT.csv"
DEFECT = OUT / "P8_Y5_R2FR_3221_DEFECT_NORM_SOURCE_ROOT_THEOREM.csv"
PHASE = OUT / "P8_Y5_R2FR_3221_PHASE_CURRENT_TO_EM_SOURCE_ROOT_GATE.csv"
FINITE = OUT / "P8_Y5_R2FR_3221_FINITE_COEFFICIENT_PROMOTION_ROWS.csv"
DECISION = OUT / "P8_Y5_R2FR_3221_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3221_VALIDATION.csv"


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


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:190]}")
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
        "input_id": "SRC3221_00_3220_doc",
        "location": "post_checkpoint",
        "relative_path": "3220-Y5-R2FR-parent-source-root-for-EM-F2-or-finite-double-zero-coefficient-input-under-AX1090.md",
        "role": "3220 handoff and wave/Poynting guard",
        "terms": ["EM_F2_SOURCE_ROOT_NOT_PARENT_SIGNED", "Poynting", "Branch A", "Branch B"],
    },
    {
        "input_id": "SRC3221_01_1055_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
        "role": "single parent action and EM owner contract",
        "terms": ["PAC1055_1_EM_owner", "PAC1055_3_no_mixed_coefficients", "PAC1055_6_single_parent_action"],
    },
    {
        "input_id": "SRC3221_02_990_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
        "role": "minimal parent EM-lock contract",
        "terms": ["PAC990_3_EM_lock", "PAC990_5_Ward_Bianchi"],
    },
    {
        "input_id": "SRC3221_03_988_emlock",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
        "role": "EM lock theorem clauses",
        "terms": ["EMLOCK988_1_unique_Maxwell_F2", "EMLOCK988_3_readout_descent", "EMLOCK988_5_theorem_verdict"],
    },
    {
        "input_id": "SRC3221_04_765_mki",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "role": "Maxwell kinetic inheritance gates",
        "terms": ["MKI765_1_norm", "MKI765_2_unique_F2", "MKI765_5_total"],
    },
    {
        "input_id": "SRC3221_05_642_descent",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
        "role": "Maxwell descent status",
        "terms": ["MD642_1_Gauss_Ampere", "MD642_2_current_conservation", "MD642_4_alpha_constant"],
    },
    {
        "input_id": "SRC3221_06_1057_unique",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
        "role": "unique Maxwell subblock attempt",
        "terms": ["UMS1057_2_no_independent_F2", "UMS1057_3_no_hidden_coefficient", "UMS1057_5_verdict"],
    },
    {
        "input_id": "SRC3221_07_1058_domain",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
        "role": "visible operator-domain exhaustion",
        "terms": ["VOE1058_0_target", "VOE1058_3_no_hidden_visible_hom", "VOE1058_5_verdict"],
    },
    {
        "input_id": "SRC3221_08_1091_domain",
        "location": "post_checkpoint",
        "relative_path": "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md",
        "role": "operator-domain theorem and scalar obstruction",
        "terms": ["ODH1091_2_scalar_obstruction", "ODH1091_4_product_functor_limit", "ODH1091_6_verdict"],
    },
    {
        "input_id": "SRC3221_09_459B_phase",
        "location": "post_checkpoint",
        "relative_path": "459B-Andersen-charge-amplitude-phase-current-gate.md",
        "role": "phase-current route clue",
        "terms": ["phase-current", "PC1_conserved_current", "PC4_Maxwell_limit", "Poynting"],
    },
    {
        "input_id": "SRC3221_10_287_current",
        "location": "post_checkpoint",
        "relative_path": "287-boundary-current-charge-owner-attempt.md",
        "role": "relative boundary-current conservation support",
        "terms": ["J_B", "d_rel J_B", "Q_B", "No promotion yet"],
    },
    {
        "input_id": "SRC3221_11_288_level",
        "location": "post_checkpoint",
        "relative_path": "288-k9-Ward-index-level-attempt.md",
        "role": "level/index attempt and charge-unit obstruction",
        "terms": ["k=9", "rank is not a Ward identity", "Q_*", "integral periods"],
    },
    {
        "input_id": "SRC3221_12_3219_hessian",
        "location": "post_checkpoint",
        "relative_path": "3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md",
        "role": "Hessian correction and strict double-zero law",
        "terms": ["G_eff", "HES3219_1_coercivity_floor", "F_Q^2"],
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

    owner_rows = [
        {
            "candidate_id": "OWN3221_0_unique_parent_Maxwell_subblock",
            "candidate_owner": "unique parent Maxwell curvature norm",
            "would_give_source_root": "only if the allowed correction to Z_A is absent or forced into a parent defect norm",
            "current_evidence": "1057/1058/1091 keep operator-domain exhaustion unsigned and scalar coefficient maps legal",
            "status": "NOT_DERIVED",
            "failure_mode": "lambda_A F_Q^2 and f(I_hid)F_Q^2 remain legal",
            "next_if_kept": "derive operator-domain exhaustion or use defect-norm restriction instead of total ban",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "OWN3221_1_compact_phase_current",
            "candidate_owner": "compact phase/current theta_Q, J_Q",
            "would_give_source_root": "charge/current conservation and sign route; EM coefficient root only if kinetic deformation is a squared Ward-current defect",
            "current_evidence": "459B/287 support phase-current conservation route; 288 says level/charge unit not derived",
            "status": "PARTIAL_CURRENT_OWNER_NOT_KINETIC_OWNER",
            "failure_mode": "current conservation does not fix Z_A or alpha normalization",
            "next_if_kept": "construct Ward-current defect R_Q and test whether Delta Z_A = lambda_Q ||R_Q||^2 is parent-owned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "OWN3221_2_Hodge_stress_descent",
            "candidate_owner": "observed Hodge/coframe/current stress descent",
            "would_give_source_root": "full Maxwell stress/Poynting safety if Hodge star and stress tensor descend through q or a squared defect",
            "current_evidence": "3220 records F_Q^2 null-wave guard; 988/990 keep readout/Hodge descent unsigned",
            "status": "NEEDED_FOR_STRESS_NOT_SOURCE_ROOT_YET",
            "failure_mode": "F_Q^2 silence does not silence T_EM or Poynting vector",
            "next_if_kept": "separate Hodge/stress residual bound or descent theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "OWN3221_3_defect_norm_owner",
            "candidate_owner": "squared parent defect norm",
            "would_give_source_root": "if Delta Z_A = lambda_D ||R_Q(Phi)||_P^2 and R_Q(Phi_*)=0, then partial_m Delta Z_A|m_*=0 automatically",
            "current_evidence": "not source-signed, but it is a constructive theorem weaker than no-extra-F2 and compatible with phase-current/Ward machinery",
            "status": "BEST_NEW_THEOREM_TARGET_NOT_CLAIM",
            "failure_mode": "without a parent R_Q in the action, it is only a contract",
            "next_if_kept": "write exact parent-action contract for R_Q and variation/Hessian/stress gates",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "OWN3221_4_verdict",
            "candidate_owner": "promote EM source-root owner",
            "would_give_source_root": "one candidate must supply parent-owned F_EM for the EM kinetic vertex and survive readout/stress gates",
            "current_evidence": "defect-norm mechanism is the cleanest constructive route, but current files do not yet provide parent R_Q",
            "status": "SOURCE_ROOT_OWNER_NOT_PROMOTED_DEFECT_NORM_TARGET_CREATED",
            "failure_mode": "b_alpha_m zero remains nonclaim; finite coefficient rows remain required",
            "next_if_kept": "3222 defect-norm parent-action contract or finite coefficient runner inputs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    defect_rows = [
        {
            "theorem_id": "DN3221_0_setup",
            "claim_piece": "defect-norm coefficient form",
            "statement": "Let Delta Z_A(Phi)=lambda_D <R_Q(Phi),R_Q(Phi)>_P, where R_Q is a parent Ward/phase/Hodge defect and R_Q(Phi_*)=0 on the local branch.",
            "proof_status": "SETUP",
            "derivation": "defines a parent-owned route where the EM coefficient depends on a squared residual rather than an arbitrary scalar f(m)",
            "missing_for_claim": "parent action must contain R_Q and couple its squared norm specifically to the EM F_Q^2 coefficient",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "DN3221_1_first_derivative_zero",
            "claim_piece": "automatic double-zero",
            "statement": "For any local parameter m, partial_m Delta Z_A|m_* = 2 lambda_D <R_Q(Phi_*), partial_m R_Q(Phi_*)>_P = 0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "derivation": "the first variation vanishes because the defect itself vanishes, not because the coefficient was manually set to zero",
            "missing_for_claim": "R_Q(Phi_*)=0 must be an Euler/Ward/nohair result, not a fitted readout root",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "DN3221_2_second_variation_debt",
            "claim_piece": "Hessian correction remains",
            "statement": "partial_m^2 Delta Z_A|m_* = 2 lambda_D <partial_m R_Q, partial_m R_Q>_P + 2 lambda_D <R_Q, partial_m^2 R_Q>_P|m_*.",
            "proof_status": "EXACT_CONDITIONAL_GUARD",
            "derivation": "at the root the second term drops, but the positive/negative effect depends on sign(lambda_D) and the operator norm of partial_m R_Q",
            "missing_for_claim": "lambda_D sign/value, ||partial_m R_Q||, and G_mem floor for G_eff >= G_mem - eta_D > 0",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "DN3221_3_why_better_than_no_extra_F2",
            "claim_piece": "less brittle coupling rule",
            "statement": "No-extra-F2 forbids the coupling; defect-norm ownership allows a coupling but forces its linear local source to vanish on the solved parent branch.",
            "proof_status": "ROUTE_ADVANCE",
            "derivation": "this is a constructive route for MTS if coupling is real but locally protected",
            "missing_for_claim": "parent object R_Q and proof that all EM memory dependence enters through ||R_Q||^2 plus fixed constants",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "DN3221_4_not_full_Maxwell_stress",
            "claim_piece": "Poynting/stress guard",
            "statement": "Even if Delta Z_A is a defect norm, null EM waves can have F_Q^2=0 while T_EM and Poynting flux are nonzero.",
            "proof_status": "SEPARATE_CHANNEL_GUARD",
            "derivation": "F2 coefficient source-root is one scalar gate, not a full stress-energy descent theorem",
            "missing_for_claim": "Hodge/current/stress defect norm or finite stress residual row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "DN3221_5_verdict",
            "claim_piece": "promote defect-norm EM owner",
            "statement": "DN3221_0 through DN3221_4 define a viable source-root mechanism but do not prove it is present in the parent MTS action.",
            "proof_status": "THEOREM_TARGET_CREATED_NOT_PARENT_SIGNED",
            "derivation": "this moves the hunt from a vague missing coupling to an exact parent-action clause",
            "missing_for_claim": "source path for R_Q, action term, local zero theorem, Hessian bound, and stress/readout closure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    phase_rows = [
        {
            "gate_id": "PC3221_0_phase_current_support",
            "route_piece": "theta_Q compact phase and J_Q current",
            "what_it_can_derive": "charge conservation/sign structure if Noether/Ward current is parent-owned",
            "what_it_cannot_derive_alone": "the continuous Maxwell kinetic coefficient Z_A or alpha normalization",
            "source_basis": "459B PC0-PC2; 287 J_B conservation; 288 k/level obstruction",
            "status": "KEEP_AS_CURRENT_ROUTE_NOT_ALPHA_OWNER",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "PC3221_1_defect_bridge",
            "route_piece": "Ward-current defect R_Q",
            "what_it_can_derive": "if R_Q=d*_{obs}(Z_*F_Q)-J_Q or a parent equivalent vanishes on shell, ||R_Q||^2 gives a source-root",
            "what_it_cannot_derive_alone": "requires a parent action term and must avoid changing Maxwell equations incorrectly",
            "source_basis": "642 current conservation support plus 1055/990 parent-action contracts",
            "status": "NEW_CONTRACT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "PC3221_2_no_penalty_cheat",
            "route_piece": "avoid post-hoc penalty term",
            "what_it_can_derive": "a real parent residual only if R_Q is varied/owned before local tests",
            "what_it_cannot_derive_alone": "an after-the-fact penalty ||R_Q||^2 would be closure, not derivation",
            "source_basis": "990 single parent action and 3220 no-multiplier/readout-cheat guard",
            "status": "GUARD_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "PC3221_3_wave_channel",
            "route_piece": "Poynting/stress residual",
            "what_it_can_derive": "full EM stress safety only if current/Hodge/stress residual also has descent or norm-bound",
            "what_it_cannot_derive_alone": "F_Q^2 source-root does not control radiation stress",
            "source_basis": "3220 wave guard; 988 readout descent unsigned",
            "status": "SEPARATE_REQUIRED_GATE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    finite_rows = [
        {
            "row_id": "FCP3221_0_lambda_D",
            "quantity": "lambda_D",
            "definition": "coefficient of the squared EM parent defect norm in Delta Z_A=lambda_D ||R_Q||^2",
            "required_source": "parent action term and units",
            "current_value": "MISSING",
            "promote_if": "numeric/source-backed or theorem-fixed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FCP3221_1_RQ_owner",
            "quantity": "R_Q(Phi)",
            "definition": "parent Ward/phase/Hodge defect whose zero defines EM source-root stationarity",
            "required_source": "definition before observed readout, varied in parent action",
            "current_value": "MISSING",
            "promote_if": "source path identifies R_Q and local branch zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FCP3221_2_dRQ_norm",
            "quantity": "||partial_m R_Q||",
            "definition": "linearized defect response controlling the second variation of Z_A",
            "required_source": "operator norm or support bound",
            "current_value": "MISSING",
            "promote_if": "finite bound and units are supplied",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FCP3221_3_Geff_guard",
            "quantity": "G_eff >= G_mem - eta_D - eta_EM_stress",
            "definition": "corrected local memory Hessian after defect-norm EM coupling and stress/readout terms",
            "required_source": "G_mem floor, eta_D bound, stress/readout residual bounds",
            "current_value": "MISSING",
            "promote_if": "strict positivity proved or bounded",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FCP3221_4_stress_Poynting_residual",
            "quantity": "T_EM/Poynting residual",
            "definition": "radiation stress/current channel not controlled by F_Q^2 alone",
            "required_source": "Hodge/current/stress descent theorem or finite bound",
            "current_value": "MISSING",
            "promote_if": "bound connects to local PPN/WEP/clock arenas without transfer shortcut",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FCP3221_5_balpha_runner_row",
            "quantity": "b_alpha_m or theorem-zero switch",
            "definition": "final local EM coupling input passed to clock/WEP/R10 product runners",
            "required_source": "either DN3221 theorem signed or finite lambda_D/R_Q/Delta m/Z_min row",
            "current_value": "MISSING",
            "promote_if": "all parent/source rows real and validation has no placeholders",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3221_0_result",
            "decision": "DEFECT_NORM_SOURCE_ROOT_MECHANISM_DERIVED_CONDITIONALLY_NOT_PARENT_SIGNED",
            "because": "a squared parent EM defect norm automatically gives the required double-zero, but current files do not yet supply the parent defect object R_Q in the action",
            "claim_status": "NO_BALPHA_M_ZERO_NO_LOCAL_GR_NO_MAXWELL_STRESS_CLAIM",
            "next_action": "write 3222 exact parent-action defect-norm contract; if no R_Q source is found, promote finite coefficient/input runner rows instead",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3221_1_best_route",
            "decision": "3222-Y5-R2FR-defect-norm-parent-action-contract-or-finite-alpha-coefficient-runner-under-AX1090",
            "because": "this is a real constructive coupling mechanism, not just another missing-source ledger",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "test whether R_Q can be defined from Ward-current mismatch, Hodge descent defect, or parent Maxwell-subblock residual before demoting to finite inputs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, owner_rows, defect_rows, phase_rows, finite_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    defect_rows: list[dict[str, object]],
    phase_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, OWNER, DEFECT, PHASE, FINITE, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    exact_dn = any(row["theorem_id"] == "DN3221_1_first_derivative_zero" for row in defect_rows)
    hessian = any(row["theorem_id"] == "DN3221_2_second_variation_debt" for row in defect_rows)
    poynting = any(row["theorem_id"] == "DN3221_4_not_full_Maxwell_stress" for row in defect_rows)
    verdict = next(row for row in owner_rows if row["candidate_id"] == "OWN3221_4_verdict")
    claim_true_count = 0
    for rows in [input_rows, owner_rows, defect_rows, phase_rows, finite_rows, decision_rows]:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
    no_fw_outputs = all(FW not in [path, *path.parents] for path in out_paths + [DOC])

    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in out_paths:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {
            "check_id": "VAL3221_00_inputs_exist",
            "pass": b(all_inputs_exist),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3221_01_defect_norm_theorem",
            "pass": b(exact_dn),
            "detail": "partial_m ||R_Q||^2 = 2<R_Q,partial_m R_Q> = 0 at R_Q=0",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3221_02_hessian_debt_retained",
            "pass": b(hessian),
            "detail": "second variation requires lambda_D and ||partial_m R_Q|| bound",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3221_03_poynting_guard_retained",
            "pass": b(poynting),
            "detail": "F2 source-root is not full Maxwell stress/Poynting descent",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3221_04_owner_not_promoted",
            "pass": b(verdict["status"] == "SOURCE_ROOT_OWNER_NOT_PROMOTED_DEFECT_NORM_TARGET_CREATED"),
            "detail": str(verdict["status"]),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3221_05_finite_rows_staged",
            "pass": b(len(finite_rows) >= 6),
            "detail": f"finite_rows={len(finite_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3221_06_claims_blocked",
            "pass": b(claim_true_count == 0),
            "detail": f"claim_rows_true={claim_true_count}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3221_07_no_formalization_workbench_edit",
            "pass": b(no_fw_outputs),
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3221_08_csv_parse",
            "pass": b(csv_parse_ok),
            "detail": ";".join(csv_parse_detail),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3221_09_next_target",
            "pass": b(decision_rows[-1]["decision"].startswith("3222-")),
            "detail": str(decision_rows[-1]["decision"]),
            "generated_utc": now,
        },
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    defect_rows: list[dict[str, object]],
    phase_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3221 - EM Source-Root Owner Hunt Or Finite Coefficient Row Promotion under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3221 does make a forward move.

The previous route kept asking whether ordinary covariance, compact `U(1)`, or generic double-zero algebra could kill the EM coupling. They cannot. The better route is:

```text
Do not forbid every EM memory coupling.
Allow only couplings that are squared norms of parent defects which vanish on the local branch.
```

Concrete mechanism:

```text
Delta Z_A(Phi) = lambda_D <R_Q(Phi), R_Q(Phi)>_P
R_Q(Phi_*) = 0

=> partial_m Delta Z_A|m_* = 2 lambda_D <R_Q, partial_m R_Q>|m_* = 0.
```

That is the exact local source-root mechanism we wanted. It is weaker and more physically plausible than a blanket no-extra-`F^2` ban: the coupling can exist, but the parent equations force its linear local source to vanish.

But this is still **not a claim**, because current files do not yet provide the parent defect object `R_Q` inside the MTS action. The most plausible identities for `R_Q` are:

```text
Ward-current mismatch,
phase-current conservation defect,
Hodge/current/stress descent defect,
or unique-Maxwell-subblock residual.
```

The wave/Poynting guard remains: a scalar `F_Q^2` source-root cannot by itself prove full Maxwell stress-energy descent.

Current verdict: `DEFECT_NORM_SOURCE_ROOT_MECHANISM_DERIVED_CONDITIONALLY_NOT_PARENT_SIGNED`.

## EM Owner Candidate Audit

{md_table(owner_rows, ["candidate_id", "candidate_owner", "would_give_source_root", "status", "failure_mode", "next_if_kept", "valid_for_claim"])}

## Defect-Norm Source-Root Theorem

{md_table(defect_rows, ["theorem_id", "claim_piece", "statement", "proof_status", "derivation", "missing_for_claim", "valid_for_claim"])}

## Phase-Current To EM Source-Root Gate

{md_table(phase_rows, ["gate_id", "route_piece", "what_it_can_derive", "what_it_cannot_derive_alone", "source_basis", "status", "valid_for_claim"])}

## Finite Coefficient Promotion Rows

{md_table(finite_rows, ["row_id", "quantity", "definition", "required_source", "current_value", "promote_if", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3221_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3221_EM_OWNER_CANDIDATE_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3221_DEFECT_NORM_SOURCE_ROOT_THEOREM.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3221_PHASE_CURRENT_TO_EM_SOURCE_ROOT_GATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3221_FINITE_COEFFICIENT_PROMOTION_ROWS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3221_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3221_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, owner_rows, defect_rows, phase_rows, finite_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (OWNER, owner_rows),
        (DEFECT, defect_rows),
        (PHASE, phase_rows),
        (FINITE, finite_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, owner_rows, defect_rows, phase_rows, finite_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, owner_rows, defect_rows, phase_rows, finite_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()
