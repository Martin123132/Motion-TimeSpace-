from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4341"
CLAIM_ID = "L-182"
BRANCH = "MTS_R2FR_Y5_KHAT_RIGHT_INVERSE_PARENT_SIGNATURE_OR_DELTAK_DIVERGENCE_BOUND_4341"
DECISION = "KHAT_RIGHT_INVERSE_PARENT_SIGNATURE_NOT_SIGNED_DELTAK_DIVERGENCE_BOUND_CONTRACT_DERIVED_NONCLAIM"
MARKER = "PPC4161_KHAT_RIGHT_INVERSE_PARENT_SIGNATURE_OR_DELTAK_DIVERGENCE_BOUND_4341"
PACKET_MARKER = "PPC4161_PACKET_KHAT_RIGHT_INVERSE_PARENT_SIGNATURE_OR_DELTAK_DIVERGENCE_BOUND_4341"
NEXT_TARGET = "4342-Y5-R2FR-CdeltaKdiv-profile-row-and-right-inverse-commutator-zero.md"

FORMAL_PATH = FORMAL / "357-PPC4161-Khat-right-inverse-parent-signature-or-DeltaK-divergence-bound.md"
DOC_PATH = POST / "4341-Y5-R2FR-Khat-right-inverse-parent-signature-or-DeltaK-divergence-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4341_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

Y_GAMMA_LIMIT = 0.0002739826487147268
Y_BETA_LIMIT = 0.0009529831259642674
Y_CLOCK_LIMIT = 0.0006134828873394971
RAW_TRANSITION_RESPONSE_LIMIT = 4.212667126774669e-17


SOURCES = [
    (
        "SRC4341_00_4340_route",
        FORMAL / "356-PPC4161-DvKhat-DeltaK-and-worldtube-trace-defect-input-fill.md",
        "PPC4161_DVKHAT_DELTAK_AND_WORLDTUBE_TRACE_DEFECT_INPUT_FILL_4340",
        "4340 handoff: paired Gamma/Khat cancellation is the clean route.",
    ),
    (
        "SRC4341_01_4340_KGamma_identity",
        FORMAL / "356-PPC4161-DvKhat-DeltaK-and-worldtube-trace-defect-input-fill.md",
        "nabla_mu K_Gamma[Gamma_eff]^(mu nu) = nabla^nu Gamma_eff.",
        "Right-inverse identity selected by 4340.",
    ),
    (
        "SRC4341_02_121_packet_Khat",
        FORMAL / "121-local-PPN-repair-route.md",
        "Khat=K_Gamma",
        "Older packet route already named the Khat=KGamma clause.",
    ),
    (
        "SRC4341_03_121_packet_fallback",
        FORMAL / "121-local-PPN-repair-route.md",
        "Delta_K^{mu nu}=K_Gamma^{mu nu}-Khat^{mu nu}",
        "Fallback residual tensor if Khat=KGamma is unsigned.",
    ),
    (
        "SRC4341_04_133_parent_not_signed",
        FORMAL / "133-exact-transition-cancellation-or-projector-theorem.md",
        "exact_Khat_cancellation_parent_derived = false",
        "Earlier red-team result: exact Khat cancellation was not parent-derived.",
    ),
    (
        "SRC4341_05_133_divergence_not_fixed",
        FORMAL / "133-exact-transition-cancellation-or-projector-theorem.md",
        "Current `K_hat` is a tracefree residual target. Its divergence is not fixed by the trace split alone.",
        "Why tracefree Khat does not automatically give div Khat=grad Gamma.",
    ),
    (
        "SRC4341_06_298_unowned_inverse_rejected",
        FORMAL / "298-PPC4161-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md",
        "K_hat = Div^-1(grad Gamma_eff)",
        "Shortcut closure explicitly rejected unless parent-owned.",
    ),
    (
        "SRC4341_07_298_raw_severity",
        FORMAL / "298-PPC4161-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md",
        "normalized_local_transition_response <= 4.212667126774669e-17.",
        "Raw transition-shell suppression remains severe if no cancellation/kernel theorem is signed.",
    ),
    (
        "SRC4341_08_315_DvKhat_split",
        FORMAL / "315-PPC4161-DvGamma-DvKhat-first-source-coefficient-or-QAP-parent-signature.md",
        "D_v K_hat = D_v Delta_K + D_v K_metric[Gamma_eff].",
        "Existing vertical Khat split feeding the new DeltaK divergence target.",
    ),
    (
        "SRC4341_09_352_KL_identity",
        FORMAL / "352-PPC4161-open-tail-PiPPN-metric-transfer-derivation-or-R10-parent-alpha-fill.md",
        "partial_mu K_L^{mu nu}=-q_loc^nu",
        "Algebraic longitudinal-owner precedent for a parent-owned divergence equation.",
    ),
    (
        "SRC4341_10_353_qprofile",
        FORMAL / "353-PPC4161-source-Sq-qprofile-kernel-and-metric-green-coupling-or-R10-alpha-parent-pivot.md",
        "q_loc^nu=P_loc[nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}]",
        "Observable q-profile that receives the Khat/DeltaK bound.",
    ),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, path, needle, role in SOURCES:
        line_number = find_line(path, needle)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
            }
        )
    return rows


def contract_rows() -> List[Dict[str, str]]:
    return [
        {
            "contract_id": "KRI4341_0_parent_owner",
            "clause": "parent owner field",
            "required_statement": "The parent action contains a constrained owner field/operator A_Gamma or equivalent whose Euler-Lagrange equation fixes K_Gamma before local scoring.",
            "mathematical_form": "L_RI A_Gamma = grad Gamma_eff; K_Gamma = R_RI[Gamma_eff]",
            "current_status": "NOT_PARENT_SIGNED",
            "why_it_matters": "Without an owner equation this is just the rejected Div^-1 shortcut.",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "KRI4341_1_right_inverse_identity",
            "clause": "right-inverse identity",
            "required_statement": "The owned lift satisfies nabla_mu K_Gamma^(mu nu)=nabla^nu Gamma_eff on the local collar.",
            "mathematical_form": "div K_Gamma = grad Gamma_eff",
            "current_status": "FORMULA_DERIVED_PARENT_SIGNATURE_MISSING",
            "why_it_matters": "This is the exact line that cancels the Gamma trace leg in q_tr.",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "KRI4341_2_same_geometry",
            "clause": "same geometry",
            "required_statement": "The same metric/coframe/connection defines nabla, K_Gamma, the source readout, and the local PPN/R10/clock/orbital projection.",
            "mathematical_form": "nabla_parent = nabla_readout = nabla_local to the stated perturbative order",
            "current_status": "MISSING_CONNECTION_COMMUTATOR_ZERO_OR_BOUND",
            "why_it_matters": "Changing geometry between the lift and readout reopens C_conn.",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "KRI4341_3_variation_domain",
            "clause": "gauge/domain fixed before variation",
            "required_statement": "Gauge, boundary conditions, and the local collar domain are fixed before the vertical variation used in D_v q_tr.",
            "mathematical_form": "C_RI^nu=[D_v,nabla_mu R_RI]Gamma_eff = 0 or bounded",
            "current_status": "MISSING_C_RI_ZERO_OR_BOUND",
            "why_it_matters": "The cancellation can fail through right-inverse/domain commutators even if div K_Gamma=grad Gamma holds pointwise.",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "KRI4341_4_DeltaK_kernel",
            "clause": "DeltaK projected divergence",
            "required_statement": "The mismatch Delta_K=K_hat-K_Gamma has zero or finite projected divergence in each local arena.",
            "mathematical_form": "P_loc nabla_mu D_v Delta_K^(mu nu)=0 or ||P_loc div D_v Delta_K|| <= C_DeltaK_div a_ref",
            "current_status": "MISSING_KERNEL_CERTIFICATE_OR_BOUND",
            "why_it_matters": "The tested channel sees div Delta_K, not the full Delta_K tensor.",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "KRI4341_5_metric_null_owner",
            "clause": "no hidden metric stress",
            "required_statement": "The owner block does not add an independent local metric response, or its response is metric-null/PPN-null after projection.",
            "mathematical_form": "Sigma_metric[S_RI]=0 or Pi_arena Sigma_metric[S_RI] bounded",
            "current_status": "MISSING_METRIC_NULL_OR_TRANSFER_BOUND",
            "why_it_matters": "A right-inverse owner that cancels q_tr but sources the metric elsewhere has not solved the local test problem.",
            "valid_for_claim": "False",
        },
    ]


def audit_rows() -> List[Dict[str, str]]:
    return [
        {
            "audit_id": "AUD4341_0_exact_Khat_claim",
            "question": "Can current files claim K_hat=K_Gamma as parent-signed?",
            "finding": "No. 133 says exact_Khat_cancellation_parent_derived=false and 298 rejects unowned Div^-1 closure.",
            "status": "FAIL_ZERO_PROOF",
            "next_action": "write parent owner equation or keep finite bound branch",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AUD4341_1_tracefree_is_enough",
            "question": "Does tracefree K_hat fix div K_hat?",
            "finding": "No. 133 states the divergence is not fixed by trace split alone.",
            "status": "FAIL_ZERO_PROOF",
            "next_action": "derive divergence equation, not only a trace condition",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AUD4341_2_algebraic_precedent",
            "question": "Is a divergence-owner construction mathematically alien to the corpus?",
            "finding": "No. 352 has K_L with partial_mu K_L^(mu nu)=-q_loc^nu, so an owned longitudinal/divergence construction is allowed in principle.",
            "status": "OPEN_PROMISING_PRECEDENT",
            "next_action": "map K_Gamma to a parent-owned analogue of K_L, not a post-hoc inverse",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AUD4341_3_projected_weaker_route",
            "question": "Must Delta_K vanish?",
            "finding": "No. 4340 reduces the observable channel to projected div Delta_K plus commutators.",
            "status": "DERIVED_WEAKER_ROUTE",
            "next_action": "attempt kernel membership for P_loc div D_v Delta_K",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AUD4341_4_raw_shell_fallback",
            "question": "How harsh is the no-cancellation fallback?",
            "finding": f"298 records normalized_local_transition_response <= {RAW_TRANSITION_RESPONSE_LIMIT}.",
            "status": "SEVERE_DIRECT_BOUND_RETAINED",
            "next_action": "avoid this branch if possible by proving the owner/kernel theorem",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "BND4341_0_qtr_reduction",
            "quantity": "q_tr^nu",
            "formula": "q_tr^nu=-nabla_mu Delta_K^(mu nu)+C_RI^nu+C_conn^nu+B_boundary^nu",
            "required_inputs": "Delta_K divergence, C_RI, C_conn, B_boundary",
            "status": "DERIVED_FORMULA_INPUTS_OPEN",
            "claim_gate": "all inputs zero or finite and source-backed",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4341_1_vertical_projected",
            "quantity": "P_loc D_v q_tr^nu",
            "formula": "P_loc D_v q_tr^nu=-P_loc nabla_mu D_v Delta_K^(mu nu)+P_loc(C_RI^nu+C_conn^nu+B_boundary^nu)",
            "required_inputs": "P_loc kernel or norm for div D_v Delta_K; projected commutator norms",
            "status": "DERIVED_PROJECTED_BOUND_INPUTS_OPEN",
            "claim_gate": "P_loc div D_v Delta_K=0 and commutators zero, or finite arena projections",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4341_2_CDeltaKdiv",
            "quantity": "C_DeltaK_div",
            "formula": "C_DeltaK_div := ||P_loc nabla_mu D_v Delta_K^(mu nu)||_obs / a_ref",
            "required_inputs": "local profile, observation norm, reference acceleration/response normalization",
            "status": "NEW_FIRST_PROFILE_ROW_TO_FILL",
            "claim_gate": "numeric, sourced, fixed before scoring",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4341_3_CRI",
            "quantity": "C_RI",
            "formula": "C_RI := ||P_loc [D_v,nabla_mu R_RI]Gamma_eff||_obs / a_ref",
            "required_inputs": "right-inverse operator, boundary/gauge/domain variation, local projection",
            "status": "NEW_COMMUTATOR_ROW_TO_PROVE_ZERO_OR_FILL",
            "claim_gate": "zero theorem or numeric source-backed bound",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4341_4_arena_vector",
            "quantity": "Y_a^Khat",
            "formula": "Y_a^Khat <= ||Pi_a^Delta|| C_DeltaK_div + ||Pi_a^RI|| C_RI + ||Pi_a^conn|| C_conn + ||Pi_a^bdry|| C_boundary",
            "required_inputs": "arena projection norms for PPN, R10, clocks, orbital, WEP",
            "status": "FORMULA_READY_NUMERIC_PROJECTIONS_OPEN",
            "claim_gate": f"PPN_gamma<={Y_GAMMA_LIMIT}; PPN_beta<={Y_BETA_LIMIT}; clock<={Y_CLOCK_LIMIT}; R10/orbital/WEP sourced separately",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4341_5_direct_shell_fallback",
            "quantity": "raw transition shell",
            "formula": f"normalized_local_transition_response <= {RAW_TRANSITION_RESPONSE_LIMIT}",
            "required_inputs": "direct shell response if no cancellation/kernel theorem is signed",
            "status": "SEVERE_FALLBACK_RETAINED_NOT_PREFERRED",
            "claim_gate": "only usable with source-backed normalization and no hidden tuning",
            "valid_for_claim": "False",
        },
    ]


def input_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "IN4341_0_parent_owner_action",
            "symbol": "S_RI or A_Gamma",
            "definition": "parent action block or constrained field whose E-L equation owns K_Gamma",
            "status": "MISSING_PARENT_ACTION_SIGNATURE",
            "next_action": "derive the owner equation from the parent action or declare closure-only",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4341_1_RRI",
            "symbol": "R_RI",
            "definition": "right-inverse operator mapping Gamma_eff to K_Gamma with fixed boundary/gauge/domain data",
            "status": "MISSING_OPERATOR_DEFINITION",
            "next_action": "map to K_L-like longitudinal operator or provide a variational constraint",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4341_2_CDeltaKdiv",
            "symbol": "C_DeltaK_div",
            "definition": "projected divergence norm of the Delta_K mismatch",
            "status": "MISSING_PROFILE_ROW",
            "next_action": "derive kernel zero or build first source-backed profile/bound row",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4341_3_CRI",
            "symbol": "C_RI",
            "definition": "right-inverse variation/domain commutator norm",
            "status": "MISSING_ZERO_THEOREM_OR_BOUND",
            "next_action": "prove gauge/domain stability or source a finite bound",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4341_4_Cconn_Cboundary",
            "symbol": "C_conn, C_boundary",
            "definition": "connection and boundary residuals introduced by local projection and collar restriction",
            "status": "MISSING_ZERO_THEOREM_OR_BOUND",
            "next_action": "tie to same-geometry and full-domain/readout-order contracts",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4341_5_Pi_arena",
            "symbol": "Pi_a^Delta, Pi_a^RI, Pi_a^conn, Pi_a^bdry",
            "definition": "arena projection constants from Khat residuals into PPN/R10/clocks/orbital/WEP observables",
            "status": "MISSING_ARENA_PROJECTION_CONSTANTS",
            "next_action": "keep nonclaim until fixed before scoring",
            "valid_for_claim": "False",
        },
    ]


def branch_rows() -> List[Dict[str, str]]:
    return [
        {
            "branch_id": "BR4341_0_parent_signed_zero",
            "branch": "exact parent-signed right-inverse",
            "conditions": "S_RI owns K_Gamma; div K_Gamma=grad Gamma_eff; C_RI=C_conn=B_boundary=0; P_loc div D_v Delta_K=0",
            "output": "P_nonHilbert Khat/Gamma channel zero",
            "status": "BEST_ROUTE_NOT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4341_1_projected_kernel",
            "branch": "DeltaK divergence kernel",
            "conditions": "Delta_K may be nonzero but P_loc nabla_mu D_v Delta_K^(mu nu)=0 in tested arenas",
            "output": "local tests blind to DeltaK through this channel",
            "status": "PROMISING_WEAKER_ZERO_TARGET",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4341_2_finite_bound",
            "branch": "source-backed finite bound",
            "conditions": "C_DeltaK_div, C_RI, C_conn, C_boundary and Pi_arena are numeric/source-backed",
            "output": "score Y_a^Khat without claiming cancellation",
            "status": "NEXT_SMOKE_ROUTE_IF_ZERO_PROOF_FAILS",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4341_3_rejected_shortcut",
            "branch": "post-hoc inverse closure",
            "conditions": "K_hat=Div^-1(grad Gamma_eff) inserted after the fact",
            "output": "blocked by 298 unless parent-owned",
            "status": "REJECTED",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4341_0_current_corpus",
            "branch_input": "current corpus through 4340",
            "action": "BLOCK_CLAIM_KEEP_BOUND_CONTRACT",
            "output": "parent signature not signed; finite C_DeltaK_div/C_RI bound contract generated",
            "claim_policy": "no local-GR/R10/PPN/clock/orbital/WEP claim",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4341_1_zero_future",
            "branch_input": "parent owner plus kernel clauses all signed",
            "action": "ALLOW_CONDITIONAL_ZERO_FOR_THIS_CHANNEL_ONLY",
            "output": "P_nonHilbert Khat/Gamma leg can be set to zero inside the private local packet",
            "claim_policy": "still needs other P_leak/source/projection gates",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4341_2_bound_future",
            "branch_input": "source-backed finite residual rows",
            "action": "RUN_NONCLAIM_LOCAL_VECTOR_SCORE",
            "output": "compare Y_a^Khat to PPN/R10/clock/orbital budgets",
            "claim_policy": "claim only if all rows are numeric, sourced and fixed before scoring",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4341_0",
            "forbidden_shortcut": "Using K_hat=Div^-1(grad Gamma_eff) without a parent owner equation",
            "reason": "298 explicitly rejected this as unowned closure.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4341_1",
            "forbidden_shortcut": "Claiming tracefree Khat fixes div Khat",
            "reason": "133 states Khat divergence is not fixed by trace split alone.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4341_2",
            "forbidden_shortcut": "Deleting Delta_K instead of proving projected div Delta_K silence",
            "reason": "4340 made the weaker local condition explicit; full tensor zero is overstrong and currently unsigned.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4341_3",
            "forbidden_shortcut": "Treating C_RI, C_conn or boundary terms as notation-only",
            "reason": "they are the exact failure modes of the right-inverse cancellation under variation/readout.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4341_4",
            "forbidden_shortcut": "Promoting this channel closure to full local GR",
            "reason": "other P_leak, source-readout and empirical projection gates remain open.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4341_0",
            "decision": DECISION,
            "reason": "the right-inverse cancellation is a real derivation route, but the current corpus still lacks the parent owner equation and commutator/kernel zeros needed to claim it",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4341_0",
            "item": "Khat right-inverse",
            "status": "CONTRACT_EXACT_PARENT_SIGNATURE_MISSING",
            "notes": "we now know exactly what the future parent action must sign",
        },
        {
            "status_id": "STAT4341_1",
            "item": "DeltaK divergence",
            "status": "FIRST_PROFILE_BOUND_TARGET",
            "notes": "C_DeltaK_div is the next concrete row if the zero proof remains unsigned",
        },
        {
            "status_id": "STAT4341_2",
            "item": "commutators",
            "status": "C_RI_CCONN_CBNDY_OPEN",
            "notes": "right-inverse, connection and boundary commutators are explicit scoreable tails",
        },
        {
            "status_id": "STAT4341_3",
            "item": "claim posture",
            "status": "NONCLAIM",
            "notes": "no local-GR or empirical local test claim fires from 4341",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4341_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the Khat owner be constructed as a K_L-like parent vertical generator, or must C_DeltaK_div/C_RI be filled as first source-backed finite rows?",
            "preferred_route": "derive S_RI/A_Gamma and prove C_RI=C_conn=B_boundary=0 with P_loc div D_v Delta_K=0",
            "fallback_route": "build a nonclaim profile runner for C_DeltaK_div, C_RI, C_conn and C_boundary against PPN/R10/clock/orbital budgets",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 357 PPC4161 Khat right-inverse parent signature or DeltaK divergence bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, or a public Khat cancellation theorem.

## Result

4341 does not let the theory smuggle in a magic inverse. It turns 4340 into an exact contract:

```text
K_hat = K_Gamma[Gamma_eff] + Delta_K
nabla_mu K_Gamma^(mu nu) = nabla^nu Gamma_eff

q_tr^nu
  = nabla^nu Gamma_eff - nabla_mu K_hat^(mu nu)
  = -nabla_mu Delta_K^(mu nu)
    + C_RI^nu + C_conn^nu + B_boundary^nu.
```

The corpus has a useful precedent for owned divergence equations in the `K_L` construction, but it does not yet parent-sign `K_hat=K_Gamma`. Earlier checkpoints explicitly reject the post-hoc closure:

```text
K_hat = Div^-1(grad Gamma_eff)
```

unless a parent action or constrained field equation owns it before scoring.

The honest next formula is therefore:

```text
C_DeltaK_div := ||P_loc nabla_mu D_v Delta_K^(mu nu)||_obs / a_ref
C_RI         := ||P_loc [D_v,nabla_mu R_RI]Gamma_eff||_obs / a_ref

Y_a^Khat
  <= ||Pi_a^Delta|| C_DeltaK_div
   + ||Pi_a^RI||    C_RI
   + ||Pi_a^conn||  C_conn
   + ||Pi_a^bdry||  C_boundary.
```

So the leap forward is sharp: either construct the parent right-inverse owner and kernel theorem, or score the first finite `Delta_K` divergence/commutator rows. No middle option is allowed.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Parent-Signature Contract

{md_table(tables["contract"], ["contract_id", "clause", "required_statement", "mathematical_form", "current_status", "why_it_matters", "valid_for_claim"])}

## Zero-Proof Audit

{md_table(tables["audit"], ["audit_id", "question", "finding", "status", "next_action", "valid_for_claim"])}

## Bound Rows

{md_table(tables["bounds"], ["bound_id", "quantity", "formula", "required_inputs", "status", "claim_gate", "valid_for_claim"])}

## Required Inputs

{md_table(tables["inputs"], ["input_id", "symbol", "definition", "status", "next_action", "valid_for_claim"])}

## Branch Runner

{md_table(tables["branches"], ["branch_id", "branch", "conditions", "output", "status", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4341 Y5-R2FR Khat right-inverse parent signature or DeltaK divergence bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4341 keeps the useful 4340 route but blocks the cheat version. `K_hat=K_Gamma` is only usable if a parent owner equation signs the right-inverse before scoring.

Current state:

```text
q_tr^nu=-nabla_mu Delta_K^(mu nu)+C_RI^nu+C_conn^nu+B_boundary^nu
```

The next concrete target is to either derive the parent-owned right-inverse and projected `div Delta_K` kernel, or fill the finite nonclaim rows `C_DeltaK_div`, `C_RI`, `C_conn`, and `C_boundary`.

## Handoff

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4341 turns the 4340 Gamma/Khat cancellation into an exact parent-signature contract. "
                    "The useful local identity is K_hat=K_Gamma+Delta_K with div K_Gamma=grad Gamma_eff, giving q_tr=-div Delta_K plus right-inverse, connection and boundary commutators. "
                    "However, current sources still do not parent-sign K_hat=K_Gamma; older checkpoints explicitly reject the unowned Div^-1(grad Gamma_eff) shortcut and state that tracefree Khat does not fix div Khat. "
                    "The checkpoint therefore derives the finite nonclaim bound vector Y_a^Khat<=Pi_Delta C_DeltaK_div+Pi_RI C_RI+Pi_conn C_conn+Pi_bdry C_boundary and selects C_DeltaK_div/C_RI as the next concrete proof-or-bound target."
                ),
                "4341 source register, parent-signature contract, zero-proof audit, bound rows, required inputs, branch runner, runner, firewall, decision, status, next-target and validation CSV.",
                "private_Khat_right_inverse_parent_signature_contract_and_DeltaK_divergence_bound_nonclaim",
                "Construct the parent-owned right-inverse/K_L-like vertical generator and prove projected div Delta_K plus commutator silence, or fill source-backed C_DeltaK_div/C_RI/C_conn/C_boundary rows.",
                "Using unowned Div^-1 closure; treating tracefree Khat as divergence control; deleting Delta_K instead of proving projected divergence silence; ignoring right-inverse/connection/boundary commutators; or claiming local GR while other gates remain open.",
            ]
        )


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH,
                "generated_utc": GENERATED_UTC,
                "decision": DECISION,
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
            }
        )

    add("VAL4341_sources_exist", "all source paths exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4341_needles_found", "all source anchors found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4341_contract_complete", "parent signature contract has six clauses", len(tables["contract"]) == 6, "contract")
    add("VAL4341_parent_not_signed", "current corpus keeps Khat parent signature unsigned", any(row["current_status"] == "NOT_PARENT_SIGNED" for row in tables["contract"]), "contract")
    add("VAL4341_unowned_inverse_blocked", "unowned Div inverse shortcut blocked", any("Div^-1" in row["forbidden_shortcut"] for row in tables["firewall"]), "firewall")
    add("VAL4341_tracefree_not_enough", "tracefree Khat is not treated as divergence control", any("tracefree" in row["question"].lower() and row["status"] == "FAIL_ZERO_PROOF" for row in tables["audit"]), "audit")
    add("VAL4341_CDeltaKdiv_bound", "C_DeltaK_div row exists", any(row["quantity"] == "C_DeltaK_div" for row in tables["bounds"]), "bounds")
    add("VAL4341_CRI_bound", "C_RI row exists", any(row["quantity"] == "C_RI" for row in tables["bounds"]), "bounds")
    add("VAL4341_arena_vector", "arena residual vector exists", any(row["quantity"] == "Y_a^Khat" for row in tables["bounds"]), "bounds")
    add("VAL4341_no_claim_flags", "all valid_for_claim flags false", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table if "valid_for_claim" in row), "all_tables")
    add("VAL4341_current_runner_blocks", "current runner blocks claim", any(row["runner_id"] == "RUN4341_0_current_corpus" and "BLOCK_CLAIM" in row["action"] for row in tables["runner"]), "runner")
    add("VAL4341_next_target", "next target is 4342 CdeltaKdiv/CRI", any("CdeltaKdiv" in row["next_target"] for row in tables["next"]), "next")
    add("VAL4341_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4341_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4341_post_handoff", "post doc contains handoff", "C_DeltaK_div" in read_text(DOC_PATH) and NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4341_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4341_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4341_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4341_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4341_SOURCE_REGISTER.csv",
        "contract": SOURCE_DIR / "P8_Y5_R2FR_4341_PARENT_SIGNATURE_CONTRACT.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4341_ZERO_PROOF_AUDIT.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4341_BOUND_ROWS.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4341_REQUIRED_INPUTS.csv",
        "branches": SOURCE_DIR / "P8_Y5_R2FR_4341_BRANCH_RUNNER.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4341_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4341_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4341_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4341_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4341_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "contract": contract_rows(),
        "audit": audit_rows(),
        "bounds": bound_rows(),
        "inputs": input_rows(),
        "branches": branch_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4341 Khat right-inverse parent signature

Marker: `{MARKER}`

4341 makes the Khat route exact and blocks the cheat version. The needed parent contract is:

```text
K_hat = K_Gamma[Gamma_eff] + Delta_K
div K_Gamma = grad Gamma_eff
q_tr = -div Delta_K + C_RI + C_conn + B_boundary.
```

Current status: the corpus has not parent-signed `K_hat=K_Gamma`, and prior checkpoints explicitly reject unowned `Div^-1(grad Gamma_eff)`. The forward route is either a parent-owned right-inverse/K_L-like generator with commutator silence, or finite source-backed rows for `C_DeltaK_div`, `C_RI`, `C_conn`, and `C_boundary`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4341 packet Khat right-inverse parent signature

Marker: `{PACKET_MARKER}`

Packet update: 4341 does not claim the Gamma/Khat cancellation. It formalizes the exact parent-action contract needed to claim it and turns the fallback into a scoreable local vector: `Y_a^Khat <= Pi_Delta C_DeltaK_div + Pi_RI C_RI + Pi_conn C_conn + Pi_bdry C_boundary`.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} :: {row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
