from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4530"
CLAIM_ID = "L-372"
MARKER = "PPC4161_SGK_SOURCE_CURRENT_ZERO_OR_FIRST_KVERT_EIGENVALUE_BOUND_4530"
PACKET_MARKER = "PPC4161_PACKET_SGK_SOURCE_CURRENT_ZERO_OR_FIRST_KVERT_EIGENVALUE_BOUND_4530"
DECISION = "SOURCE_CURRENT_ZERO_IS_AN_EXACT_CHAIN_RULE_THEOREM_BUT_CURRENT_MTS_NEEDS_BOUNDARY_WEIGHT_OR_FIRST_EIGENMODE_VALUES"
NEXT_TARGET = "4531-Y5-R2FR-observed-coframe-matter-descent-or-first-eigenmode-local-bound-runner.md"

FORMAL_PATH = FORMAL / "546-PPC4161-SGK-source-current-zero-or-first-Kvert-eigenvalue-bound.md"
DOC_PATH = POST / "4530-Y5-R2FR-SGK-source-current-zero-or-first-Kvert-eigenvalue-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4530_SOURCE_REGISTER.csv"
DESCENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4530_SOURCE_CURRENT_DESCENT_IDENTITY.csv"
BOUNDARY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4530_BOUNDARY_POYNTING_SPLIT.csv"
ZERO_OR_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4530_ZERO_OR_FINITE_BOUND_THEOREM.csv"
EIGENMODE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4530_FIRST_KVERT_EIGENMODE_BOUND_CONTRACT.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4530_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4530_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4530_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4530_VALIDATION.csv"

DOC_4529 = POST / "4529-Y5-R2FR-positive-SGK-parent-signature-map-or-epsilonI-Kvert-value-source.md"
VALIDATION_4529 = SOURCE_DIR / "P8_Y5_BRR545_4529_VALIDATION.csv"
THEOREM_4529 = SOURCE_DIR / "P8_Y5_R2FR_4529_SGK_DESCENT_THEOREM.csv"
SIGNATURE_4529 = SOURCE_DIR / "P8_Y5_R2FR_4529_SGK_PARENT_SIGNATURE_MAP.csv"
VALUE_4529 = SOURCE_DIR / "P8_Y5_R2FR_4529_EPSILONI_KVERT_VALUE_SOURCE_ROWS.csv"
DOC_1620 = POST / "1620-Y5-R2FR-parent-signature-map-and-source-current-zero-or-q_loc-bound-fill.md"
CHAIN_1620 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv"
BRIDGE_1620 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1620_PARENT_SIGNATURE_BRIDGE_CONTRACT.csv"
VERTICAL_1620 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv"
BOUND_1620 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1620_SOURCE_CURRENT_BOUND_FILL_ROWS.csv"
DOC_1086 = POST / "1086-Y5-R10-WEP-source-current-zero-or-parent-DD-map-first-row.md"
SCZ_1086 = SOURCE_DIR / "P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv"
DOC_1079 = POST / "1079-Y5-R10-parent-current-owner-narrow-proof-or-finite-WEP-source-vector.md"
NCO_1079 = SOURCE_DIR / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv"
PREMISE_1079 = SOURCE_DIR / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv"
BAN_1416 = SOURCE_DIR / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv"
VERT_1505 = SOURCE_DIR / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv"
DESCENT_1575 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv"
EM_POYNTING = SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"
MASS_CONTRACT = SOURCE_DIR / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def line_of(path: Path, needle: str) -> int:
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def snippet(path: Path, needle: str) -> str:
    for line in text(path).splitlines():
        if needle in line:
            return line.strip()[:360]
    return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, "")).replace("\n", "<br>")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *body])


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4530_00_doc4529", "4529 SGK handoff", DOC_4529, "4530-Y5-R2FR-SGK-source-current-zero-or-first-Kvert-eigenvalue-bound.md", "immediate target"),
        ("SRC4530_01_val4529", "4529 validation", VALIDATION_4529, "VAL4529_OVERALL", "prior step validated"),
        ("SRC4530_02_theorem4529", "4529 SGK theorem rows", THEOREM_4529, "SGK4529_5_finite_source_bound", "finite-source bound formula"),
        ("SRC4530_03_signature4529", "4529 signature map", SIGNATURE_4529, "SIG4529_2_even_matter_readout", "source-current signature"),
        ("SRC4530_04_values4529", "4529 value rows", VALUE_4529, "VALSRC4529_3_Jnorm", "J/B norm source rows"),
        ("SRC4530_05_doc1620", "1620 chain-rule document", DOC_1620, "CR1620_1_zero_lemma", "exact chain-rule lemma"),
        ("SRC4530_06_chain1620", "1620 chain-rule CSV", CHAIN_1620, "CR1620_1_zero_lemma", "source-current identity"),
        ("SRC4530_07_bridge1620", "1620 bridge contract", BRIDGE_1620, "BRC1620_4_boundary_silence", "boundary/source lock clauses"),
        ("SRC4530_08_vertical1620", "1620 verticality audit", VERTICAL_1620, "QVM1620_5_verdict", "Dq verticality status"),
        ("SRC4530_09_bound1620", "1620 source-current bound rows", BOUND_1620, "SCB1620_0_JZ_bulk", "fallback rows"),
        ("SRC4530_10_doc1086", "1086 WEP source-current zero", DOC_1086, "SCZ1086_5_verdict", "source-current bottleneck"),
        ("SRC4530_11_scz1086", "1086 source-current CSV", SCZ_1086, "SCZ1086_2_pre_action_weight_leak", "pre-action counterexample"),
        ("SRC4530_12_doc1079", "1079 current-owner proof", DOC_1079, "DEC1079_0_partial_win", "Hilbert current subtheorem"),
        ("SRC4530_13_nco1079", "1079 narrow current-owner CSV", NCO_1079, "NCO1079_5_species_action_weight", "species-weight leak"),
        ("SRC4530_14_premise1079", "1079 current-owner premise ledger", PREMISE_1079, "PR1079_4_no_pre_action_species_weight", "unsigned premise"),
        ("SRC4530_15_ban1416", "1416 source-slot ban", BAN_1416, "BAN1416_6_verdict", "source weight ban not proved"),
        ("SRC4530_16_vert1505", "1505 Dq verticality tests", VERT_1505, "DQT1505_8_acceptance", "verticality blocked"),
        ("SRC4530_17_descent1575", "1575 matter descent signature", DESCENT_1575, "MDS1575_5_verdict", "descent not signed"),
        ("SRC4530_18_em_poynting", "EM/Poynting source-flux vector", EM_POYNTING, "EMF3502_1_radiative_poynting_flux", "Poynting boundary split"),
        ("SRC4530_19_mass_boundary", "Hamiltonian boundary charge contract", MASS_CONTRACT, "HC4_charge_equals_PiM_Hilbert_mass", "mass/source boundary identity"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle, role in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "label": label,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "snippet": snippet(path, needle),
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def descent_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "J4530_0_full_variation_decomposition",
            "object": "odd SGK/MTS residual source current J_A",
            "derivation": "Vary the ordinary matter action along a candidate local odd residual vector v_A before readout.",
            "formula": "delta_v S_m = D_q Sbar · Dq[v_A] + sum_r (partial Sbar/partial theta_r) Lie_v theta_r + J_direct[v_A] + delta_v B_m",
            "zero_condition": "Dq[v_A]=0, Lie_v theta_r=0, J_direct[v_A]=0, and delta_v B_m=0/proper.",
            "result": "J_A=0 follows by chain rule, not by wishful symmetry.",
            "status": "EXACT_CONDITIONAL_IDENTITY_DERIVED",
            "valid_for_claim": False,
        },
        {
            "identity_id": "J4530_1_hilbert_owner_subtheorem",
            "object": "post-variation source-current rescaling",
            "derivation": "Once one common matter action is varied with respect to the observed coframe/metric, the Hilbert source is fixed at that variation point.",
            "formula": "T_obs := (2/sqrt(-g_obs)) delta S_matter/delta g_obs; later readout cannot replace T_obs -> c_A T_obs as a variational source.",
            "zero_condition": "common matter action and variation-before-readout are parent-signed.",
            "result": "post-variation selectors are conditionally killed.",
            "status": "CONDITIONAL_SUBTHEOREM_REUSED",
            "valid_for_claim": False,
        },
        {
            "identity_id": "J4530_2_pre_action_weight_counterterm",
            "object": "species/source weights before variation",
            "derivation": "Test whether current ownership alone removes weights already inside the action.",
            "formula": "S_matter=sum_A w_A S_A => T_obs=sum_A w_A T_A",
            "zero_condition": "parent object-language/action-measure theorem forbids w_A and source-only markers.",
            "result": "current ownership alone does not prove J_A=0.",
            "status": "COUNTERMODEL_SURVIVES_WITHOUT_PARENT_GRAMMAR",
            "valid_for_claim": False,
        },
        {
            "identity_id": "J4530_3_verticality_not_enough",
            "object": "Dq[v_A]=0 shortcut",
            "derivation": "Insert Dq[v_A]=0 into the full variation decomposition and keep the other terms.",
            "formula": "J_A = sum_r J_theta^r Lie_v theta_r + J_direct[v_A] + delta_v B_m",
            "zero_condition": "constant-sector silence, no direct/source marker, and boundary silence also hold.",
            "result": "Dq verticality is necessary but not sufficient for local-GR source silence.",
            "status": "BETA_ONLY_SHORTCUT_REJECTED",
            "valid_for_claim": False,
        },
        {
            "identity_id": "J4530_4_sgk_import",
            "object": "SGK zero theorem source premise",
            "derivation": "Feed J_A=0 from the chain-rule identity into the SGK coercive identity.",
            "formula": "J_A=0 and B_A=0 => h0||nabla Z||^2+m0^2||Z||^2<=0 => Z=0",
            "zero_condition": "all J/B clauses and positive operator clauses are parent-signed.",
            "result": "local silence is derivable, but current MTS does not yet satisfy the premises.",
            "status": "LOCAL_ZERO_ROUTE_EXACT_BUT_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def boundary_rows() -> list[dict[str, Any]]:
    return [
        {
            "boundary_id": "B4530_0_sgk_worldtube_flux",
            "channel": "SGK odd residual boundary term",
            "formula": "B_A^SGK = int_{partial Omega} n_mu H_AB nabla^mu Z^B delta Z^A + improvement/corner terms",
            "zero_route": "Dirichlet Z=0, Neumann nHnablaZ=0, compact-support variation, or exact/proper boundary variation",
            "if_not_zero": "retains ||B_SGK||_{H^-1} in the finite source bound",
            "source_anchor": str(DESCENT_1575),
            "current_status": "BOUNDARY_OPEN",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "B4530_1_minimal_EM_bound_stress",
            "channel": "ordinary stationary minimal EM bound fields",
            "formula": "S_EM=-1/(4 mu0) int F wedge *_obs F; T_EM belongs inside total Hilbert source before local mass readout",
            "zero_route": "same observed Hodge/coframe and stationary bound fields mean it is source accounting, not an odd Z boundary force",
            "if_not_zero": "not zero as energy, but not an extra local-GR violation if included in the same Hilbert source",
            "source_anchor": str(EM_POYNTING),
            "current_status": "CONDITIONAL_ZERO_ROUTE_INSIDE_TOTAL_SOURCE",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "B4530_2_radiative_poynting_flux",
            "channel": "radiative/background Poynting flux through local exterior",
            "formula": "Phi_EM_rad = int_{partial Omega} S_Poynting · n dA",
            "zero_route": "stationary isolated local branch with no net radiative/background flux",
            "if_not_zero": "retains Phi_EM_rad as source-time hair or boundary contribution; cannot be hidden in J_A=0",
            "source_anchor": str(EM_POYNTING),
            "current_status": "RETAINED_FLUX_COEFFICIENT_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "B4530_3_nonminimal_EM_cross_term",
            "channel": "hidden/motion/time scalar coupling to F^2 or F*F",
            "formula": "Delta S ~ int sqrt(-g) f_X(Phi) F_{mu nu}F^{mu nu} or g_X(Phi) F_{mu nu}*F^{mu nu}",
            "zero_route": "parent operator grammar forbids hidden-visible EM coefficient morphisms",
            "if_not_zero": "feeds alpha drift, clock/WEP products and source-normalization residuals",
            "source_anchor": str(EM_POYNTING),
            "current_status": "RETAINED_OPERATOR_COEFFICIENT_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "B4530_4_hamiltonian_mass_boundary",
            "channel": "Hamiltonian boundary charge versus Hilbert source current",
            "formula": "B_xi/G_eff = M_eff[Pi_M J_H] + residuals",
            "zero_route": "differentiable/integrable boundary charge equals projected Hilbert mass with no extra hidden charge",
            "if_not_zero": "Newton/G_N calibration remains a boundary/source residual rather than derived local GR",
            "source_anchor": str(MASS_CONTRACT),
            "current_status": "NOT_PARENT_DERIVED",
            "valid_for_claim": False,
        },
    ]


def zero_or_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "ZB4530_0_exact_local_zero",
            "branch": "exact SGK local silence",
            "premises": "Dq[v_A]=0; Lie_v theta=0; J_direct=0; B_A=0; H>=h0>0; M^2>=m0^2>0; gauge zero modes removed",
            "formula": "h0||nabla Z||^2 + m0^2||Z||^2 <= 0",
            "consequence": "Z=0, A_A=0, J_A=0, q_loc^nu=0, F_1=0",
            "current_status": "THEOREM_DERIVED_PREMISES_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZB4530_1_finite_source_response",
            "branch": "finite sourced SGK residual",
            "premises": "H>=h0>0, M^2>=m0^2>0, but J_A or B_A retained",
            "formula": "||Z||_{H1} <= C_L (||J||_{H-1}+||B||_{H-1}) + O((||J||+||B||)^2)",
            "consequence": "local-GR violation becomes a bounded residual vector, not a closure assumption",
            "current_status": "DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZB4530_2_ghost_rejection",
            "branch": "bad kinetic/sign branch",
            "premises": "H has negative physical eigenvalue or M^2 has tachyonic physical eigenvalue",
            "formula": "exists xi: H_AB xi^A xi^B <= 0 or M_AB^2 xi^A xi^B < 0",
            "consequence": "SGK local branch is rejected, not fitted",
            "current_status": "REJECTION_GATE_DEFINED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZB4530_3_constraint_rank_zero_parallel",
            "branch": "constraint/no-pole route",
            "premises": "Kvert=0 from parent no-derivative grammar or second-class constraint before matter coupling",
            "formula": "no physical inverse Green kernel for Z/R_AB",
            "consequence": "exact rank-zero local branch, separate from positive SGK massive branch",
            "current_status": "PARALLEL_ROUTE_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def eigenmode_rows() -> list[dict[str, Any]]:
    return [
        {
            "mode_row_id": "KBE4530_0_first_mode_contract",
            "mode": "i=first physical SGK/Kvert mode",
            "required_inputs": "h_i, m_i^2, K_i, Q_iS, Q_iT, G_N, M_S, m_T, source path, local arena bound",
            "eigen_problem": "M_AB^2 v_i^B = mu_i^2 H_AB v_i^B with H_AB v_i^A v_i^B = h_i > 0",
            "lambda_formula": "lambda_i = 1/mu_i = sqrt(h_i)/m_i",
            "alpha_formula": "alpha_i = K_i Q_iS Q_iT/(G_N M_S m_T m_i^2)",
            "acceptance": "numeric positive h_i,m_i^2 and source-backed K/Q rows; compare abs(alpha_i)<=alpha_bound(lambda_i)",
            "current_value": "MISSING_H_M_K_Q_BOUND",
            "valid_for_claim": False,
        },
        {
            "mode_row_id": "KBE4530_1_JB_source_norm",
            "mode": "finite source/boundary forcing",
            "required_inputs": "||J||_{H^-1}, ||B||_{H^-1}, operator norm C_L, arena projection K_obs",
            "eigen_problem": "Z = L^{-1}(J+B) + nonlinear corrections",
            "lambda_formula": "not a pure Yukawa unless one eigenmode dominates",
            "alpha_formula": "|delta O_a| <= ||K_obs,a|| C_L (||J||+||B||)",
            "acceptance": "all norms source-backed or theorem-zero; no signed cancellation between J and B",
            "current_value": "MISSING_J_B_CL_KOBS",
            "valid_for_claim": False,
        },
        {
            "mode_row_id": "KBE4530_2_EM_flux_component",
            "mode": "Poynting/radiative boundary component",
            "required_inputs": "Phi_EM_rad or proof of stationary no-flux; nonminimal EM coefficient if present",
            "eigen_problem": "boundary/source forcing term, not a pure internal eigenvalue unless projected onto v_i",
            "lambda_formula": "lambda_i only after projection onto the SGK eigenbasis",
            "alpha_formula": "alpha_EM_boundary <= K_EM C_L |Phi_EM_rad| / observed source normalization",
            "acceptance": "minimal bound stress included in Hilbert source; radiative/nonminimal pieces retained separately",
            "current_value": "MISSING_FLUX_OR_ZERO_THEOREM",
            "valid_for_claim": False,
        },
        {
            "mode_row_id": "KBE4530_3_public_claim_gate",
            "mode": "local-GR/Newton/R10 claim",
            "required_inputs": "all exact-zero clauses or all finite numeric rows plus bound curves",
            "eigen_problem": "not applicable",
            "lambda_formula": "not applicable",
            "alpha_formula": "claim_allowed iff exact zero theorem fires or finite rows pass local bounds",
            "acceptance": "no missing parent signature, no missing units, no placeholder values",
            "current_value": "CLAIM_BLOCKED",
            "valid_for_claim": False,
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4530_0_chain_rule_identity",
            "gate": "derive source-current decomposition and zero lemma",
            "status": "PASS_FORMAL",
            "detail": "J_A decomposition and zero conditions are explicitly stated from existing 1620/1086/1079 material.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4530_1_current_MTS_application",
            "gate": "apply J_A=0 to current MTS",
            "status": "BLOCKED_UNSIGNED",
            "detail": "Dq verticality, matter descent, constant/marker silence, pre-action weight ban and boundary silence remain unsigned.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4530_2_boundary_poynting",
            "gate": "separate local boundary and Poynting/wave terms",
            "status": "PASS_SPLIT_NONCLAIM",
            "detail": "minimal bound EM stress is accounting; radiative Poynting and nonminimal F^2 couplings remain finite residuals unless zero-sourced.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4530_3_first_eigenmode_contract",
            "gate": "create first Kvert eigenmode finite-bound contract",
            "status": "PASS_SCHEMA_VALUES_MISSING",
            "detail": "h_i,m_i,K_i,Q_iS,Q_iT contract is now explicit and ready for a runner once sourced.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4530_4_local_GR_claim",
            "gate": "claim local GR/Newton recovery",
            "status": "BLOCKED",
            "detail": "exact zero route is not parent-signed and finite rows have no numeric/source-backed inputs.",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4530_0",
            "decision": DECISION,
            "meaning": "We made forward motion: source-current zero is no longer vague. It is an exact chain-rule theorem with named terms, and the boundary/Poynting leakage is separated from ordinary bound-field stress. Current MTS still cannot claim local GR, so the next decisive fork is observed-coframe matter descent or the first finite eigenmode runner.",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "try to parent-sign observed-coframe matter descent and no pre-action source weights; if it fails, implement the first eigenmode local-bound runner using KBE4530_0 rows",
            "why": "This either closes J_A=0 honestly or moves to the empirical finite-residual comparison without circling.",
            "valid_for_claim": False,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    descent: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    eigenmodes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    source_failures = [row["source_id"] for row in sources if not row["path_exists"] or not row["needle_found"]]
    checks.append(
        {
            "validation_id": "VAL4530_00_sources",
            "status": "PASS" if not source_failures else "FAIL",
            "detail": "all source paths exist and needles found" if not source_failures else ";".join(source_failures),
        }
    )

    descent_ids = {row["identity_id"] for row in descent}
    checks.append(
        {
            "validation_id": "VAL4530_01_descent_identity",
            "status": "PASS" if {"J4530_0_full_variation_decomposition", "J4530_2_pre_action_weight_counterterm", "J4530_4_sgk_import"} <= descent_ids else "FAIL",
            "detail": "source-current decomposition, counterterm, and SGK import rows present",
        }
    )

    boundary_ids = {row["boundary_id"] for row in boundary}
    checks.append(
        {
            "validation_id": "VAL4530_02_boundary_split",
            "status": "PASS" if {"B4530_1_minimal_EM_bound_stress", "B4530_2_radiative_poynting_flux", "B4530_3_nonminimal_EM_cross_term"} <= boundary_ids else "FAIL",
            "detail": "minimal EM, radiative Poynting, and nonminimal EM split rows present",
        }
    )

    eigenmode_ids = {row["mode_row_id"] for row in eigenmodes}
    checks.append(
        {
            "validation_id": "VAL4530_03_eigenmode_contract",
            "status": "PASS" if {"KBE4530_0_first_mode_contract", "KBE4530_1_JB_source_norm"} <= eigenmode_ids else "FAIL",
            "detail": "first Kvert eigenmode and J/B norm contracts present",
        }
    )

    checks.append(
        {
            "validation_id": "VAL4530_04_claims_blocked",
            "status": "PASS" if all(row["valid_for_claim"] is False for row in gates) else "FAIL",
            "detail": "all claim gates remain private nonclaim until parent signatures or numeric finite rows exist",
        }
    )

    csv_files = [
        SOURCE_REGISTER,
        DESCENT_CSV,
        BOUNDARY_CSV,
        ZERO_OR_BOUND_CSV,
        EIGENMODE_CSV,
        GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
    ]
    parse_failures = []
    for path in csv_files:
        try:
            with path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            if not rows:
                parse_failures.append(path.name)
        except Exception as exc:  # pragma: no cover
            parse_failures.append(f"{path.name}:{exc}")
    checks.append(
        {
            "validation_id": "VAL4530_05_csv_parse",
            "status": "PASS" if not parse_failures else "FAIL",
            "detail": "all generated CSV files parse and have rows" if not parse_failures else ";".join(parse_failures),
        }
    )

    checks.append(
        {
            "validation_id": "VAL4530_06_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
        }
    )

    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL4530_OVERALL",
            "status": overall,
            "detail": "4530 source-current theorem fork and first Kvert eigenmode bound contract" if overall == "PASS" else "4530 validation failed",
        }
    )
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    descent: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    zero_or_bound: list[dict[str, Any]],
    eigenmodes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> str:
    return f"""# 4530 — SGK Source-Current Zero Or First Kvert Eigenvalue Bound

Marker: `{MARKER}`  
Packet marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  
Generated: `{now()}`

## What Moved

- The exact source-current route is now written as a chain-rule identity with all terms exposed: quotient, constants, direct source markers, and boundary.
- The old “maybe Poynting/waves matter” worry is split cleanly: stationary minimal EM belongs in the same Hilbert source, but radiative Poynting flux and nonminimal `F^2` couplings remain retained residuals unless proved zero.
- The exact local-GR branch is still not claimed, but it is sharper: if `J_A=0`, `B_A=0`, and the SGK operator is positive, local silence follows.
- If exact silence does not sign, the first `Kvert` eigenmode bound contract is now explicit enough for a runner: `h_i`, `m_i`, `K_i`, `Q_iS`, `Q_iT`, and bound curve.

## Core Derivation

```text
delta_v S_matter
  = D_q Sbar · Dq[v_A]
  + sum_r (partial Sbar/partial theta_r) Lie_v theta_r
  + J_direct[v_A]
  + delta_v B_m

Dq[v_A]=0
Lie_v theta_r=0
J_direct[v_A]=0
delta_v B_m=0/proper
  => J_A=0

J_A=0, B_A=0, H>=h0>0, M^2>=m0^2>0
  => h0||nabla Z||^2 + m0^2||Z||^2 <= 0
  => Z=0
  => q_loc^nu=0 and F_1=0
```

## Source-Current Descent Identity

{md_table(descent)}

## Boundary / Poynting Split

{md_table(boundary)}

## Zero Or Finite Bound Theorem

{md_table(zero_or_bound)}

## First Kvert Eigenmode Bound Contract

{md_table(eigenmodes)}

## Claim Gates

{md_table(gates)}

## Decision

{md_table(decisions)}

## Source Register

{md_table(sources)}

## Validation

{md_table(validation)}
"""


def append_once(path: Path, marker: str, block: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n")
        handle.write(block.strip())
        handle.write("\n")


def append_claim_once() -> None:
    current = text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in current:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_source_current_boundary",
        "claim": "4530 derives the SGK source-current chain-rule zero theorem, separates boundary/Poynting leakage, and creates the first Kvert eigenmode finite-bound contract.",
        "current_evidence": "Generated source-current descent identity, boundary/Poynting split, zero-or-finite theorem, first eigenmode contract, claim gates and validation P8_Y5_BRR545_4530_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_source_current_theorem_values_missing",
        "next_test": NEXT_TARGET,
        "key_risk": "Dq verticality, matter descent, pre-action source-weight exclusion, boundary silence, and finite eigenmode values are not parent-signed.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Using Hilbert-current ownership or minimal EM accounting to hide pre-action species weights, radiative flux, or nonminimal EM source couplings.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    descent = descent_identity_rows()
    boundary = boundary_rows()
    zero_or_bound = zero_or_bound_rows()
    eigenmodes = eigenmode_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DESCENT_CSV, descent)
    write_csv(BOUNDARY_CSV, boundary)
    write_csv(ZERO_OR_BOUND_CSV, zero_or_bound)
    write_csv(EIGENMODE_CSV, eigenmodes)
    write_csv(GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, descent, boundary, eigenmodes, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, descent, boundary, zero_or_bound, eigenmodes, gates, decisions, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4530 SGK Source-Current Zero Or First Kvert Eigenvalue Bound

Marker: `{MARKER}`  
The source-current step is now an explicit chain-rule theorem: `delta_v S_matter = D_q Sbar·Dq[v] + J_theta Lie_v theta + J_direct[v] + delta_v B`. Exact local silence follows if every term vanishes and the SGK operator is positive. Boundary/Poynting leakage is separated: minimal stationary EM stress is part of the Hilbert source, while radiative flux and nonminimal EM cross terms remain retained residuals. If exact zero does not parent-sign, the first `Kvert` eigenmode finite-bound contract is ready.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4530 Packet Integration

Marker: `{PACKET_MARKER}`  
The PPC4161 packet now has a concrete source-current theorem fork and first finite eigenmode contract. Next target: `{NEXT_TARGET}`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
