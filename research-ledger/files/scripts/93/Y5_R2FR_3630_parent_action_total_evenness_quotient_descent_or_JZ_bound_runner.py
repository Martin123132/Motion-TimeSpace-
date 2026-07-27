from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3630"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ACTION_TOTAL_EVENNESS_QUOTIENT_DESCENT_OR_JZ_BOUND_RUNNER_3630"
DOC = ROOT / "3630-Y5-R2FR-parent-action-total-evenness-quotient-descent-or-JZ-bound-runner.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8", errors="replace")


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3630_SOURCE_REGISTER.csv",
        "parent_action_clause": RESIDUALS / "P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv",
        "jz_zero_theorem": RESIDUALS / "P8_Y5_R2FR_3630_JZ_ZERO_THEOREM_DERIVATION.csv",
        "signature_audit": RESIDUALS / "P8_Y5_R2FR_3630_PARENT_SIGNATURE_AUDIT.csv",
        "bound_requirements": RESIDUALS / "P8_Y5_R2FR_3630_JZ_BOUND_REQUIREMENTS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3630_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3630_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3630_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_parent_action_JZ_zero_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3630_VALIDATION.csv",
    }


def source_map() -> list[dict[str, str]]:
    return [
        {
            "source_id": "handoff_3629",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3629_NEXT_TARGET.csv"),
            "needle": "single parent-action clause",
            "role": "3629 selected the parent-action total-evenness/quotient-descent target.",
        },
        {
            "source_id": "coupling_law_3629",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv"),
            "needle": "L_AB Z^B + J_A",
            "role": "exact source-coupling law to be killed or bounded.",
        },
        {
            "source_id": "zero_routes_3629",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3629_JZ_ZERO_ROUTE_AUDIT.csv"),
            "needle": "JZR3629_0_quotient_descent",
            "role": "quotient descent, evenness, quadratic activation, charge-current, and boundary zero routes.",
        },
        {
            "source_id": "coefficient_rows_3629",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv"),
            "needle": "JZC3629_8_R11_operator",
            "role": "fallback coefficient rows if J_Z cannot be theorem-zero.",
        },
        {
            "source_id": "quotient_matter_626",
            "path": str(ROOT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md"),
            "needle": "Lie_v S_matter = 0",
            "role": "matter quotient descent criterion used in the parent-action theorem.",
        },
        {
            "source_id": "response_doublet_contract",
            "path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
            "needle": "RD516_4_zero_odd_source",
            "role": "source-coupling and PPN-lock conditions for the response doublet.",
        },
        {
            "source_id": "double_zero_memory",
            "path": str(RESIDUALS / "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv"),
            "needle": "f(0)=0 and f_prime(0)=0",
            "role": "quadratic activation condition for memory/domain coupling.",
        },
        {
            "source_id": "domain_parent_clause",
            "path": str(RESIDUALS / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv"),
            "needle": "S_D = integral sqrt(-g)",
            "role": "existing domain parent-action clause to be absorbed into the total parent action.",
        },
        {
            "source_id": "charge_current",
            "path": str(RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv"),
            "needle": "Pi_M(Q_nonEH + Q_boundary + Q_domain + Q_memory + Q_range + Q_connection + Q_delta_kappa)=0",
            "role": "source-normalization/extra-charge orthogonality condition.",
        },
        {
            "source_id": "ppn_envelope_3625",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv"),
            "needle": "ENV3625_6_total",
            "role": "local-GR envelope that J_Z bound rows must feed if theorem-zero fails.",
        },
    ]


def source_rows(t: str) -> list[dict[str, object]]:
    rows = []
    for src in source_map():
        path = Path(src["path"])
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": src["source_id"],
                "path": src["path"],
                "exists": exists,
                "needle": src["needle"],
                "needle_found": exists and contains(path, src["needle"]),
                "role": src["role"],
            }
        )
    return rows


def parent_action_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": "PAC3630_0_variables",
            "object": "parent variables and quotient",
            "mathematical_clause": "Phi_parent with q:Phi_parent->Q_MTS; local response basis e_A has Dq[e_A]=0; Z^A are coordinates along this vertical response basis",
            "why_needed": "without Dq[e_A]=0, quotient descent cannot imply delta S/delta Z=0",
            "current_status": "CLAUSE_WRITTEN_VERTICAL_GENERATOR_NOT_PARENT_MAPPED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": "PAC3630_1_total_action",
            "object": "single admissible parent action",
            "mathematical_clause": "S_parent=S_EH[g]+S_even[Z,g]+S_matter[gbar(q),Psi,theta(q)]+S_source[Pi_M(q)J_H(q,Psi)]+S_boundary[B(q),ref]+S_phys_flux[F,Psi,g]",
            "why_needed": "puts response, matter, measured source, boundary, and physical EM/radiation flux into one action instead of separate closure ledgers",
            "current_status": "SUFFICIENT_PARENT_ACTION_CLAUSE_WRITTEN_NOT_CURRENT_CORPUS_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": "PAC3630_2_even_response",
            "object": "response sector",
            "mathematical_clause": "S_even=-int sqrt(-g)[Gamma_0+1/2 M_AB Z^A Z^B+1/2 H_AB nabla Z^A nabla Z^B+O(Z^4)] with no odd Z terms",
            "why_needed": "keeps the 3628 F1=0 mechanism and supplies a positive operator L_AB",
            "current_status": "FORMAL_MECHANISM_FROM_3628_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": "PAC3630_3_matter_descent",
            "object": "ordinary matter action",
            "mathematical_clause": "S_matter depends on Phi_parent only through q(Phi_parent), with no representative Weyl/disformal coefficient and no hidden Z-linear matter spurion",
            "why_needed": "kills J_Z^matter by quotient descent instead of tuning a coupling to zero",
            "current_status": "626_CRITERION_AVAILABLE_BUT_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": "PAC3630_4_source_normalization",
            "object": "measured mass/source current",
            "mathematical_clause": "Pi_M, J_H, G_eff, M_eff, and reference charge are q-data or fixed constants; Pi_M(Q_extra)=0 for non-EH/domain/memory/range/connection charges",
            "why_needed": "prevents measured GM from absorbing a hidden J_Z source and calling it Newton",
            "current_status": "CHARGE_CURRENT_ORTHOGONALITY_NOT_PARENT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": "PAC3630_5_quadratic_activation",
            "object": "domain/memory activation",
            "mathematical_clause": "any local selector/memory coupling enters through f(Z) or f(chi) with f(0)=f_prime(0)=0, e.g. norm-square/determinant/topological pairing",
            "why_needed": "forbids a linear memory/source term from regenerating Z in the local branch",
            "current_status": "SUFFICIENT_REQUIREMENT_KNOWN_PARENT_ORIGIN_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": "PAC3630_6_boundary",
            "object": "boundary and symplectic handoff",
            "mathematical_clause": "boundary variation in the Z direction is zero or fixed-reference: B_A=0 and no linked-surface preferred-frame/source flux remains",
            "why_needed": "bulk J_Z=0 is meaningless if the collar boundary reintroduces alpha3 or source-normalization leakage",
            "current_status": "BOUNDARY_NATURAL_SOURCE_NOT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": "PAC3630_7_physical_flux_separation",
            "object": "Maxwell/Poynting/radiation stress",
            "mathematical_clause": "physical flux fields F enter S_phys_flux with their own Hilbert stress and current; they are counted as matter/EM stress, not hidden in q_loc closure",
            "why_needed": "keeps the Poynting-vector idea useful without using it to fake a vacuum GR plateau",
            "current_status": "ACTION_POLICY_WRITTEN_EM_MAPPING_DEFERRED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def theorem_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "step_id": "THM3630_0_define_source",
            "derivation_step": "Define the response source",
            "formula": "J_A=(1/sqrt(-g)) delta(S_matter+S_source+S_boundary)/delta Z^A |_{Z=0}",
            "result": "J_A is the only linear obstruction to Z=0 after the even response action is chosen.",
            "status": "DERIVED_FROM_3629",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "step_id": "THM3630_1_even_bulk",
            "derivation_step": "Even response bulk has no linear term",
            "formula": "delta S_even/delta Z^A |_{0}=0, delta T_GK/delta Z^A |_{0}=0 after Gamma_0 subtraction",
            "result": "the 3628 F1=0 result survives inside the total parent action.",
            "status": "CONDITIONAL_PASS_FOR_RESPONSE_SECTOR",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "step_id": "THM3630_2_matter_descent",
            "derivation_step": "Quotient matter descent kills matter source",
            "formula": "delta_Z S_matter = (delta Sbar_matter/delta q) Dq[e_A] delta Z^A = 0 because Dq[e_A]=0",
            "result": "J_A^matter=0 if Z is vertical and S_matter descends to Q_MTS.",
            "status": "VALID_THEOREM_STEP_PARENT_PREMISES_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "step_id": "THM3630_3_source_descent",
            "derivation_step": "Source-normalization descent kills measured-mass source",
            "formula": "delta_Z S_source = (delta S_source/delta(Pi_M J_H)) delta_Z[Pi_M(q)J_H(q,Psi)] = 0",
            "result": "mu_extra and J_Z source-normalization terms vanish only if Pi_M and J_H are q-owned and extra charges are orthogonal.",
            "status": "VALID_THEOREM_STEP_CHARGE_CURRENT_PREMISES_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "step_id": "THM3630_4_quadratic_activation",
            "derivation_step": "Quadratic memory/domain activation kills selector source",
            "formula": "delta_Z[f(Z)L_mem]|0 = f_prime(0)L_mem delta Z = 0 when f(0)=f_prime(0)=0",
            "result": "domain/memory coupling does not re-source local Z at first order under the p>=2 activation rule.",
            "status": "VALID_THEOREM_STEP_PARENT_ORIGIN_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "step_id": "THM3630_5_boundary",
            "derivation_step": "Boundary natural source must vanish",
            "formula": "delta S_boundary|collar = int_boundary B_A delta Z^A; require B_A=0 or fixed-reference exact term",
            "result": "bulk J_A=0 promotes only if boundary Z-source and linked preferred-frame/source flux are absent.",
            "status": "BOUNDARY_PREMISE_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "step_id": "THM3630_6_conclusion",
            "derivation_step": "Conditional J_Z theorem",
            "formula": "if THM3630_1..THM3630_5 pass, then J_A=0 and L_AB Z^B+O(Z^2)=0; with positive L_AB and fixed boundary, Z=0",
            "result": "this would derive the local response plateau instead of assuming it.",
            "status": "CONDITIONAL_THEOREM_PROVED_CURRENT_CORPUS_NOT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def audit_rows(t: str) -> list[dict[str, object]]:
    audit_items = [
        ("SIG3630_0_q_map", "q:Phi_parent->Q_MTS parent-defined", "MISSING_PARENT_Q_MAP_IN_THIS_BRANCH", "blocks quotient-descent proof"),
        ("SIG3630_1_vertical_generator", "Z^A basis equals ker(Dq) vertical directions", "MISSING_DQ_VERTICAL_GENERATOR_MAP", "blocks delta_Z S_matter=0"),
        ("SIG3630_2_matter_descent", "S_matter=Sbar_matter[q(Phi),Psi,theta]", "NOT_SIGNED_FROM_626", "blocks J_A^matter zero and c_g zero"),
        ("SIG3630_3_source_descent", "Pi_M,J_H,M_eff,G_eff are q-owned/source-current orthogonal", "NOT_PARENT_DERIVED", "blocks Newton/source-normalization claim"),
        ("SIG3630_4_quadratic_origin", "p>=2 activation follows from symmetry/norm/determinant/topology", "REQUIREMENT_DERIVED_ORIGIN_MISSING", "blocks selector/memory zero promotion"),
        ("SIG3630_5_boundary", "B_A=0 or fixed exact boundary with no local flux", "BOUNDARY_NATURAL_SOURCE_OPEN", "blocks alpha3/source flux silence"),
        ("SIG3630_6_Kmetric", "K_hat equals K_metric for the chosen S_GK", "UNSIGNED_FROM_3628", "blocks Gamma/Khat parent ownership"),
        ("SIG3630_7_Z_physical", "Z^A equals the physical q_loc/PPN/Newton/source residual vector", "MISSING_Z_TO_OBSERVABLE_MAP", "blocks using the theorem as local-GR evidence"),
        ("SIG3630_8_verdict", "all parent-action signature clauses pass", "FAIL_CURRENT_CORPUS_NO_CLAIM", "requires 3631 vertical/q/source map or J_Z coefficients"),
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": audit_id,
            "required_signature": required,
            "current_status": status,
            "blocks": blocks,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for audit_id, required, status, blocks in audit_items
    ]


def bound_rows(t: str) -> list[dict[str, object]]:
    previous = read_csv(RESIDUALS / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv")
    rows: list[dict[str, object]] = []
    for row in previous:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "bound_id": row["coupling_id"].replace("JZC3629", "JZB3630"),
                "target_row": row["target_row"],
                "observable": row["observable"],
                "theorem_zero_condition": "all SIG3630 signature clauses pass",
                "if_theorem_fails_prediction": row["prediction_template"],
                "minimum_inputs": row["missing_input"] + "; MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH",
                "score_status": "not_scoreable",
                "source_path": str(RESIDUALS / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv"),
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def decision_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3630_0_theorem",
            "decision": "A single parent-action clause is now written that is mathematically sufficient for J_Z=0.",
            "status": "CONDITIONAL_THEOREM_PROGRESS",
            "next_action": "try to parent-map Z as a vertical generator of q and prove matter/source descent",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3630_1_current_ceiling",
            "decision": "The current corpus still cannot claim J_Z=0 because q, vertical generator, matter descent, source descent, boundary source, K_metric, and Z-observable map are unsigned.",
            "status": "NO_CLAIM",
            "next_action": "do not promote local GR/Newton/PPN; keep bound rows active",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3630_2_best_next",
            "decision": "The highest-leverage next step is not another broad audit: it is the vertical generator and Z-to-observable map.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3631-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3630_0",
            "result": "PARENT_ACTION_JZ_ZERO_THEOREM_CONDITIONAL_SIGNATURE_UNSIGNED",
            "summary": "3630 writes the single parent-action clause that would genuinely kill the coupling: Z must be a vertical generator of q, matter/source/boundary terms must descend to q or be even/quadratic, extra source charges must be orthogonal, and boundary natural sources must vanish. Under those clauses J_Z=0 follows. Current MTS has this as a strong theorem target, not a claim, because the vertical generator, matter/source descent, boundary source, K_metric match, and Z-to-observable map remain unsigned.",
            "conditional_theorem_written": True,
            "JZ_zero_claimed": False,
            "bound_rows_staged": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3630_0",
            "target_doc": "3631-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md",
            "target_script": "scripts/Y5_R2FR_3631_vertical_generator_Z_map_or_JZ_coefficient_runner.py",
            "objective": "map Z^A/DCdagger-like local residual coordinates to actual parent quotient vertical generators e_A in ker(Dq), then map Z^A to q_loc/PPN/Newton/source observables; if either map fails, prepare J_Z coefficients for scoring",
            "success_gate": "Dq[e_A]=0 is parent-signed, Z^A is the physical local residual coordinate, and delta_Z S_matter/source can be evaluated; otherwise each observable receives an explicit J_Z coefficient row",
            "reason": "3630 proves the theorem conditionally; the first unsigned premise is the vertical generator and physical residual map.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "parent_action_JZ_zero",
            "canonical_status": "CONDITIONAL_THEOREM_WRITTEN_SIGNATURE_UNSIGNED",
            "usable_result": "If Z is vertical to q and all non-response couplings descend/even/quadratic/no-flux, then J_Z=0 and the local response branch is derivable.",
            "hard_block": "parent-map q, vertical generator, matter/source descent, boundary no-flux, K_hat=K_metric, and Z-to-observable residuals",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(rows: list[dict[str, object]], cols: list[str]) -> str:
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows:
        out.append("| " + " | ".join(md(row.get(col, "")) for col in cols) + " |")
    return "\n".join(out)


def write_doc(src: list[dict[str, object]], pac: list[dict[str, object]], thm: list[dict[str, object]], audit: list[dict[str, object]], bounds: list[dict[str, object]], decisions: list[dict[str, object]], status: list[dict[str, object]], nxt: list[dict[str, object]]) -> None:
    text = "\n\n".join(
        [
            "# 3630 Y5 R2FR parent-action total evenness, quotient descent, or J_Z bound runner",
            f"**Status:** {status[0]['summary']}",
            "**Claim ceiling:** no local-GR, Newton, PPN, R10/R11, WEP, clock, Gdot, EM-source, `K_hat=K_metric`, or `J_Z=0` claim is allowed from 3630.",
            "## Core result",
            (
                "This is the clean parent-action theorem target:\n\n"
                "```text\n"
                "S_parent = S_EH[g] + S_even[Z,g] + S_matter[gbar(q),Psi,theta(q)]\n"
                "         + S_source[Pi_M(q)J_H(q,Psi)] + S_boundary[B(q),ref] + S_phys_flux[F,Psi,g]\n"
                "Dq[e_A] = 0,  Z = Z^A e_A\n"
                "J_A = (1/sqrt(-g)) delta(S_matter+S_source+S_boundary)/delta Z^A |_{Z=0}\n"
                "```\n\n"
                "If the non-response terms depend on the parent only through `q`, or enter only through even/quadratic local amplitudes with zero boundary natural source, then `J_A=0`. "
                "With a positive `L_AB`, this derives `Z=0` in the compact local branch. The theorem is good; the present corpus has not yet signed the required parent maps."
            ),
            "## Source register",
            table(src, ["source_id", "path", "exists", "needle_found", "role"]),
            "## Parent-action clause",
            table(pac, ["clause_id", "object", "mathematical_clause", "why_needed", "current_status"]),
            "## J_Z zero theorem derivation",
            table(thm, ["step_id", "derivation_step", "formula", "result", "status"]),
            "## Parent-signature audit",
            table(audit, ["audit_id", "required_signature", "current_status", "blocks"]),
            "## Bound requirements if theorem fails",
            table(bounds, ["bound_id", "target_row", "observable", "if_theorem_fails_prediction", "minimum_inputs", "score_status"]),
            "## Decisions",
            table(decisions, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            table(nxt, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(paths: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = now()
    rows: list[dict[str, object]] = []

    def add(vid: str, ok: bool, detail: str) -> None:
        rows.append({"timestamp_utc": t, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "validation_id": vid, "result": "PASS" if ok else "FAIL", "detail": detail})

    add("VAL3630_0_sources_exist", all(row["exists"] for row in src), "all sources exist")
    add("VAL3630_1_needles_found", all(row["needle_found"] for row in src), "all source anchors found")
    pre = {k: v for k, v in paths.items() if k != "validation"}
    add("VAL3630_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs written")

    details = []
    ok_parse = True
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            ok_parse = ok_parse and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            ok_parse = False
    add("VAL3630_3_csv_parse", ok_parse, "; ".join(details))

    pac = read_csv(paths["parent_action_clause"])
    thm = read_csv(paths["jz_zero_theorem"])
    audit = read_csv(paths["signature_audit"])
    bounds = read_csv(paths["bound_requirements"])
    decisions = read_csv(paths["decision_gates"])
    status = read_csv(paths["status"])
    nxt = read_csv(paths["next_target"])

    add("VAL3630_4_parent_action_written", any("S_parent" in row["mathematical_clause"] for row in pac), "single parent-action clause written")
    add("VAL3630_5_vertical_descent_formula_written", any("Dq[e_A]=0" in row["formula"] for row in thm), "quotient vertical descent derivation written")
    add("VAL3630_6_JZ_zero_conditional_written", any("J_A=0" in row["formula"] for row in thm), "conditional J_Z zero theorem written")
    add("VAL3630_7_signature_audit_blocks_claim", any(row["current_status"] == "FAIL_CURRENT_CORPUS_NO_CLAIM" for row in audit), "current-corpus no-claim audit row present")
    add("VAL3630_8_bound_rows_cover_3629", len(bounds) == 9 and all(row["valid_for_claim"].lower() == "false" for row in bounds), "J_Z bound rows carried forward as nonclaim")
    add("VAL3630_9_all_outputs_nonclaim", all(row["valid_for_claim"].lower() == "false" for row in pac + thm + audit + bounds + decisions + status + nxt), "all outputs remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3630*")) if FORMALIZATION.exists() else []
    add("VAL3630_10_no_formalization_leak", not leaks, "no 3630 files in formalization-workbench")
    add("VAL3630_11_next_target_written", bool(nxt) and "3631" in nxt[0]["target_doc"], "3631 vertical generator target written")
    add("VAL3630_12_canonical_status_written", paths["canonical_status"].exists() and "CONDITIONAL_THEOREM_WRITTEN" in paths["canonical_status"].read_text(encoding="utf-8", errors="replace"), "canonical parent-action status written")
    return rows


def main() -> None:
    t = now()
    paths = outputs()
    src = source_rows(t)
    pac = parent_action_rows(t)
    thm = theorem_rows(t)
    audit = audit_rows(t)
    bounds = bound_rows(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)
    canonical = canonical_rows(t)

    write_csv(paths["source_register"], src)
    write_csv(paths["parent_action_clause"], pac)
    write_csv(paths["jz_zero_theorem"], thm)
    write_csv(paths["signature_audit"], audit)
    write_csv(paths["bound_requirements"], bounds)
    write_csv(paths["decision_gates"], decisions)
    write_csv(paths["status"], status)
    write_csv(paths["next_target"], nxt)
    write_csv(paths["canonical_status"], canonical)
    write_doc(src, pac, thm, audit, bounds, decisions, status, nxt)

    validation = validate(paths, src)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3630 validation failed: {failed}")
    print(f"wrote 3630 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
