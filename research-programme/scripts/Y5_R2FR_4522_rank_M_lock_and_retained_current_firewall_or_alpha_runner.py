from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4522"
CLAIM_ID = "L-364"
MARKER = "PPC4161_RANK_M_LOCK_AND_RETAINED_CURRENT_FIREWALL_OR_ALPHA_RUNNER_4522"
PACKET_MARKER = "PPC4161_PACKET_RANK_M_LOCK_AND_RETAINED_CURRENT_FIREWALL_OR_ALPHA_RUNNER_4522"
DECISION = "FULL_RANK_ZERO_ROUTE_DERIVED_AS_CONDITIONAL_THEOREM_PARENT_SIGNATURE_UNSIGNED_ALPHA_RUNNER_STAGED"
NEXT_TARGET = "4523-Y5-R2FR-same-branch-parent-signature-audit-or-first-alpha-runner.md"

FORMAL_PATH = FORMAL / "538-PPC4161-rank-M-lock-and-retained-current-firewall-or-alpha-runner.md"
DOC_PATH = POST / "4522-Y5-R2FR-rank-M-lock-and-retained-current-firewall-or-alpha-runner.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4522_SOURCE_REGISTER.csv"
THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4522_RANK_M_LOCK_THEOREM.csv"
CURRENT_FIREWALL = SOURCE_DIR / "P8_Y5_R2FR_4522_RETAINED_CURRENT_FIREWALL.csv"
DECISION_MATRIX = SOURCE_DIR / "P8_Y5_R2FR_4522_RANK_ZERO_DECISION_MATRIX.csv"
BOUND_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4522_FINITE_BOUND_OR_ALPHA_RUNNER.csv"
CLAUSE_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4522_CLAUSE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4522_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4522_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4522_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4522_VALIDATION.csv"

FORMAL_4521 = FORMAL / "537-PPC4161-boundary-CDB-readout-silence-or-alpha-input-fill.md"
DOC_4521 = POST / "4521-Y5-R2FR-boundary-CDB-readout-silence-or-alpha-input-fill.md"
RHS_4521 = SOURCE_DIR / "P8_Y5_R2FR_4521_RANK_ZERO_RHS_UPDATE.csv"
BRANCH_4521 = SOURCE_DIR / "P8_Y5_R2FR_4521_BRANCH_DECISION.csv"
ALPHA_4521 = SOURCE_DIR / "P8_Y5_R2FR_4521_ALPHA_INPUT_FILL_DECISION.csv"

CLASSIFIER_4519 = SOURCE_DIR / "P8_Y5_R2FR_4519_FINITE_RANGE_OR_RANK_ZERO_BRANCH_CLASSIFIER.csv"
RESIDUAL_4519 = SOURCE_DIR / "P8_Y5_R2FR_4519_RANK_ZERO_ALGEBRAIC_RESIDUAL_VECTOR.csv"
RZ_CONTRACT_2212 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2212_RANK_ZERO_CONSTRAINT_CONTRACT.csv"
RZ_THEOREM_2213 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2213_RANK_ZERO_SOURCE_CURRENT_THEOREM_ATTEMPT.csv"
CONSTRAINT_GATES_2263 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2263_CONSTRAINT_ALGEBRA_GATES.csv"
CONSTRAINT_THEOREM_2264 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2264_CONDITIONAL_CONSTRAINT_THEOREM.csv"
LOCAL_RANK_901 = SOURCE_DIR / "P8_Y5_R10_901_LOCAL_RANK_ZERO_CERTIFICATE.csv"

WARD_CONTRACT = SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv"
OWNER_CONTRACT = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"
NO_MARKER_2623 = SOURCE_DIR / "P8_Y5_PRIMITIVE_QUOTIENT_GATE_2623_NO_NATURAL_MARKER_AUDIT.csv"
NO_TOWER_2623 = SOURCE_DIR / "P8_Y5_PRIMITIVE_QUOTIENT_GATE_2623_NO_INTEGRATED_OUT_TOWER_AUDIT.csv"
PQT_2623 = SOURCE_DIR / "P8_Y5_PRIMITIVE_QUOTIENT_GATE_2623_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv"
NO_LINEAR_3888 = SOURCE_DIR / "P8_Y5_R2FR_3888_QUOTIENT_NO_LINEAR_SOURCE_DERIVATION.csv"
NO_MARKER_3676 = SOURCE_DIR / "P8_Y5_R2FR_3676_NO_NATURAL_MARKER_THEOREM_AUDIT.csv"
DESCENT_3764 = SOURCE_DIR / "P8_Y5_R2FR_3764_PARENT_QUOTIENT_DESCENT_THEOREM.csv"


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


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + body.strip() + "\n")


def source_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC4522_00_formal4521", "4521 formal handoff", FORMAL_4521, "PPC4161_BOUNDARY_CDB_READOUT_SILENCE_OR_ALPHA_INPUT_FILL_4521", "boundary/CDB/readout handoff"),
        ("SRC4522_01_post4521", "4521 post handoff", DOC_4521, "4522-Y5-R2FR-rank-M-lock-and-retained-current-firewall-or-alpha-runner.md", "declared next target"),
        ("SRC4522_02_rhs4521", "4521 RHS update", RHS_4521, "RHU4521_4_combined", "remaining rank-zero RHS"),
        ("SRC4522_03_branch4521", "4521 branch decision", BRANCH_4521, "BD4521_3_rank_zero", "rank-zero not closed"),
        ("SRC4522_04_alpha4521", "4521 alpha decision", ALPHA_4521, "AFD4521_0_Z", "alpha fallback still deferred"),
        ("SRC4522_05_classifier4519", "4519 branch classifier", CLASSIFIER_4519, "FRC4519_2_rank_zero", "rank-zero branch law"),
        ("SRC4522_06_residual4519", "4519 residual vector", RESIDUAL_4519, "RZR4519_0_normal_form", "MZ residual equation"),
        ("SRC4522_07_contract2212", "rank-zero contract", RZ_CONTRACT_2212, "RZC2212_4_invertible_algebraic_lock", "M_AB lock clause"),
        ("SRC4522_08_theorem2213", "rank-zero theorem attempt", RZ_THEOREM_2213, "RZS2213_2_rank_zero_silence_theorem", "conditional silence theorem"),
        ("SRC4522_09_gates2263", "constraint algebra gates", CONSTRAINT_GATES_2263, "CAG2263_6_verdict", "constraint algebra not closed"),
        ("SRC4522_10_theorem2264", "conditional constraint theorem", CONSTRAINT_THEOREM_2264, "THM2264_0_constraint_statement", "nonpropagating constraint theorem"),
        ("SRC4522_11_rank901", "local rank-zero certificate", LOCAL_RANK_901, "LRZ901_3_verdict", "rank certificate failure"),
        ("SRC4522_12_ward", "source current Ward contract", WARD_CONTRACT, "SC4_no_nonHilbert_source_current", "retained current clause"),
        ("SRC4522_13_owner", "source owner contract", OWNER_CONTRACT, "A2_no_retained_source_constraint", "no retained source owner"),
        ("SRC4522_14_marker2623", "primitive no-marker audit", NO_MARKER_2623, "MRK2623_6_overall", "marker residual not eliminated"),
        ("SRC4522_15_tower2623", "no integrated-out tower audit", NO_TOWER_2623, "TOW2623_4_overall", "tower countermodels"),
        ("SRC4522_16_pqt2623", "primitive quotient theorem", PQT_2623, "PQT2623_5_current_verdict", "primitive parent lock not proved"),
        ("SRC4522_17_nls3888", "no-linear-source derivation", NO_LINEAR_3888, "NLS3888_5_verdict", "partial source neutrality"),
        ("SRC4522_18_nmm3676", "no natural marker theorem audit", NO_MARKER_3676, "NMM3676_6_verdict", "no-marker theorem audit"),
        ("SRC4522_19_qdt3764", "parent quotient descent theorem", DESCENT_3764, "QDT3764_5_failure_mode", "sector factorization failure modes"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        body = text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": needle in body,
            "line": line_of(path, needle),
            "note": note,
            "valid_for_claim": False,
        })
    return rows


def theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "RML4522_0_operator_branch",
            "piece": "finite-rank versus rank-zero split",
            "statement": "For L_AB=-Z_AB Delta+M_AB on the physical source-coupled quotient, rank(Z_AB)>0 gives a finite-range/spectral branch, while rank(Z_AB)=0 gives an algebraic branch.",
            "formula": "rank(Z_AB)>0 -> alpha(lambda); rank(Z_AB)=0 -> M_AB Z^B=R_A^tot",
            "status": "DERIVED_FROM_4519",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RML4522_1_rank_zero_certificate",
            "piece": "rank-zero certificate",
            "statement": "Rank-zero requires the principal symbol in the Z directions to vanish on the physical quotient after gauge/constraint reduction; a missing or hidden derivative tower routes to finite residual/alpha scoring.",
            "formula": "sigma_pr(L_Z)=Z_AB |xi|^2; rank_Z sigma_pr=0 on Q_phys",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RML4522_2_M_lock",
            "piece": "algebraic lock",
            "statement": "If M_AB is invertible/coercive on the algebraic complement with m_min>0, then M_AB Z^B=0 implies Z=0; if RHS is finite, ||Z|| <= m_min^-1 ||RHS||.",
            "formula": "||Z|| <= ||M^{-1}|| ||RHS|| <= m_min^-1(||J_ret||+||B||+||CDB||+||R||)",
            "status": "DERIVED_CONDITIONAL_BOUND",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RML4522_3_constraint_lock",
            "piece": "first/second-class alternative",
            "statement": "If M_AB has null directions, they are safe only when owned by a first-class gauge constraint or second-class auxiliary elimination with differentiable generator, no boundary charge, bracket preservation, and reduced nondegeneracy.",
            "formula": "ker(M) safe iff ker(M)=gauge/constraint orbit and reduced Omega or algebraic Schur complement is nondegenerate",
            "status": "DERIVED_CONDITIONAL_CONSTRAINT_ROUTE",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RML4522_4_retained_current",
            "piece": "retained current firewall",
            "statement": "J_A^retained=0 only if no non-Hilbert source, marker, memory/kernel, integrated-out tower, reduced action, calibration feedback, species/source weight, or moving source-worldtube projector couples to v_A before variation.",
            "formula": "J_ret = J_nonH + J_marker + J_kernel + J_tower + J_red + J_cal + J_species + J_worldtube",
            "status": "DERIVED_FIREWALL",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RML4522_5_full_conditional_closure",
            "piece": "complete conditional rank-zero route",
            "statement": "If 4520 source-current silence, 4521 B/CDB/R silence, J_retained=0, rank(Z_AB)=0, and M_AB is locked in one same parent branch, then Z=0 and the rank-zero local residual vanishes termwise.",
            "formula": "rank(Z)=0, M locked, RHS=0 => Z=0 => E_local<=K_obs||Z||+direct tails=0",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RML4522_6_verdict",
            "piece": "4522 verdict",
            "statement": "The mathematical route is now complete as a conditional theorem, but current evidence does not parent-sign the rank certificate, constraint algebra, no-retained-current firewall, or same-branch adoption.",
            "formula": "theorem complete; claim blocked",
            "status": "CONDITIONAL_ROUTE_COMPLETE_PARENT_SIGNATURE_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def current_rows() -> list[dict[str, object]]:
    return [
        {"current_id": "RCF4522_0_nonHilbert", "retained_channel": "non-Hilbert source current", "zero_route": "single q-basic Hilbert-current functor plus no q_retained", "current_status": "CONTRACT_NOT_PARENT_SIGNED", "fallback": "finite J_nonH or alpha/source-current branch", "valid_for_claim": False},
        {"current_id": "RCF4522_1_marker", "retained_channel": "material/species/source marker", "zero_route": "primitive no-natural-marker theorem and universal constants", "current_status": "UNSIGNED", "fallback": "WEP/clock/source-charge vector", "valid_for_claim": False},
        {"current_id": "RCF4522_2_kernel", "retained_channel": "memory/nonlocal/source kernel", "zero_route": "positive source-free no-hair or q-basic kernel absence", "current_status": "UNSIGNED", "fallback": "kernel norm/source profile bound", "valid_for_claim": False},
        {"current_id": "RCF4522_3_tower", "retained_channel": "integrated-out curvature/source tower", "zero_route": "no integrated-out tower theorem or universal auxiliary elimination with no visible source vertex", "current_status": "COUNTERMODELS_LIVE", "fallback": "EFT coefficient/alpha branch", "valid_for_claim": False},
        {"current_id": "RCF4522_4_readout", "retained_channel": "reduced action/readout reentry", "zero_route": "variation-before-readout and pure postprocessing only", "current_status": "FIREWALL_READY_NOT_GLOBAL", "fallback": "readout reentry bound", "valid_for_claim": False},
        {"current_id": "RCF4522_5_calibration", "retained_channel": "source calibration/species weights", "zero_route": "constant universal kappa and closed Hilbert mass projector", "current_status": "CONDITIONAL", "fallback": "calibration drift/source-weight residual", "valid_for_claim": False},
        {"current_id": "RCF4522_6_worldtube", "retained_channel": "moving source-worldtube/projector", "zero_route": "fixed q-basic support and no projector stress", "current_status": "CONDITIONAL", "fallback": "chainmap readout/source-worldtube bound", "valid_for_claim": False},
        {"current_id": "RCF4522_7_verdict", "retained_channel": "J_A^retained", "zero_route": "all retained channels excluded in the same parent branch", "current_status": "NOT_CLOSED", "fallback": "finite residual/alpha runner", "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {"decision_id": "RZD4522_0_finite_rank", "condition": "rank(Z_AB)>0 with positive generalized eigenvalues", "mathematical_consequence": "finite-range/spectral field exists", "route": "run alpha(lambda)/residual scorer", "current_status": "NOT_SELECTED", "valid_for_claim": False},
        {"decision_id": "RZD4522_1_rank_zero_locked", "condition": "rank(Z_AB)=0 and M_AB invertible/coercive or constraint-owned", "mathematical_consequence": "algebraic rank-zero route exists", "route": "prove RHS zero termwise", "current_status": "CONDITIONAL_NOT_SIGNED", "valid_for_claim": False},
        {"decision_id": "RZD4522_2_rhs_zero", "condition": "J_retained=B=CDB=R=0 in same branch", "mathematical_consequence": "Z=0 if M lock holds", "route": "local residual zero theorem", "current_status": "CONDITIONAL_NOT_SIGNED", "valid_for_claim": False},
        {"decision_id": "RZD4522_3_null_M", "condition": "M_AB has null/wrong-sign directions not gauge/constraint-owned", "mathematical_consequence": "rank-zero route fails or becomes unstable/underdetermined", "route": "reject branch or score finite residuals", "current_status": "NOT_EXCLUDED", "valid_for_claim": False},
        {"decision_id": "RZD4522_4_current_verdict", "condition": "current corpus", "mathematical_consequence": "conditional theorem complete but parent signature absent", "route": NEXT_TARGET, "current_status": "NO_CLAIM", "valid_for_claim": False},
    ]


def bound_rows() -> list[dict[str, object]]:
    alpha_inputs = read_csv(ALPHA_4521)
    rows: list[dict[str, object]] = [
        {"runner_id": "FBA4522_0_rank_zero_bound", "case": "rank-zero with nonzero finite RHS", "required_inputs": "m_min(M_AB), norms for J_retained,B,CDB,R and projection K_obs", "bound_formula": "||E_local|| <= K_obs m_min^-1 (||J_ret||+||B||+||CDB||+||R||)+direct_tails", "current_status": "SYMBOLIC_READY_INPUTS_MISSING", "valid_for_claim": False},
        {"runner_id": "FBA4522_1_finite_rank_alpha", "case": "rank(Z_AB)>0", "required_inputs": "Z eigenvalues,M eigenvalues,Q_source,q_test,calibration,bound curve", "bound_formula": "alpha_X(lambda_X)=[Q_X^S q_X^T/(4*pi Z_X)]/[G_N M_S m_T]", "current_status": "CONTRACT_READY_INPUTS_MISSING", "valid_for_claim": False},
        {"runner_id": "FBA4522_2_spectral", "case": "spectral/nonlocal memory", "required_inputs": "spectral measure d rho(mu), source/test charges, arena transfer", "bound_formula": "alpha envelope = integral d rho(mu) alpha(mu) exp(-mu r)(1+mu r)", "current_status": "NOT_SELECTED", "valid_for_claim": False},
    ]
    for row in alpha_inputs:
        rows.append({
            "runner_id": row["alpha_decision_id"].replace("AFD4521", "FBA4522"),
            "case": "alpha input inherited from 4521",
            "required_inputs": row["required_evidence"],
            "bound_formula": row["source_quantity"],
            "current_status": row["current_status"],
            "valid_for_claim": False,
        })
    return rows


def clause_rows() -> list[dict[str, object]]:
    return [
        {"clause_id": "CLA4522_0_rank", "requirement": "rank(Z_AB)=0 on the physical source-coupled quotient", "current_evidence": "4519 classifier and 901 certificate; certificate fails for claim", "status": "UNSIGNED", "valid_for_claim": False},
        {"clause_id": "CLA4522_1_no_hidden_derivative", "requirement": "no derivative/tower/spectral kinetic term returns after elimination", "current_evidence": "2623 no-tower audit has live countermodels", "status": "UNSIGNED", "valid_for_claim": False},
        {"clause_id": "CLA4522_2_M_invertible", "requirement": "M_AB coercive/invertible with m_min>0 on algebraic complement", "current_evidence": "2212 lock clause, no numeric m_min", "status": "CONDITIONAL", "valid_for_claim": False},
        {"clause_id": "CLA4522_3_constraint_nulls", "requirement": "any null M directions are first/second-class owned and removed from physical quotient", "current_evidence": "2263 constraint gates not closed", "status": "UNSIGNED", "valid_for_claim": False},
        {"clause_id": "CLA4522_4_Jretained", "requirement": "J_retained=0", "current_evidence": "source owner/ward contracts plus no-marker/no-tower audits; not parent-signed", "status": "UNSIGNED", "valid_for_claim": False},
        {"clause_id": "CLA4522_5_B_CDB_R", "requirement": "4521 B/CDB/R zero clauses hold in same branch", "current_evidence": "4521 conditional theorem, not same-branch signed", "status": "CONDITIONAL", "valid_for_claim": False},
        {"clause_id": "CLA4522_6_same_branch", "requirement": "all clauses are active together, not stitched from incompatible closure branches", "current_evidence": "not yet audited", "status": "NEXT_TARGET", "valid_for_claim": False},
        {"clause_id": "CLA4522_7_empirical", "requirement": "local PPN/R10/WEP/clock/orbital evidence accepts resulting residuals", "current_evidence": "not score-ready", "status": "PENDING_AFTER_PARENT_OR_ALPHA", "valid_for_claim": False},
    ]


def claim_rows() -> list[dict[str, object]]:
    return [
        {"gate_id": "CG4522_0_rank", "claim": "rank(Z_AB)=0 selected", "passed": False, "blocker": "local rank-zero certificate fails for claim; hidden derivative/tower countermodels remain", "valid_for_claim": False},
        {"gate_id": "CG4522_1_M", "claim": "M_AB locked/invertible", "passed": False, "blocker": "no parent-signed m_min or constraint-owned null-direction proof", "valid_for_claim": False},
        {"gate_id": "CG4522_2_Jretained", "claim": "J_retained=0", "passed": False, "blocker": "no-retained-current/no-marker/no-tower firewall not parent-signed", "valid_for_claim": False},
        {"gate_id": "CG4522_3_full_conditional", "claim": "conditional theorem exists", "passed": False, "blocker": "theorem exists but not parent-signed; valid_for_claim remains false", "valid_for_claim": False},
        {"gate_id": "CG4522_4_local_GR", "claim": "local GR/Newton/PPN pass", "passed": False, "blocker": "conditional route lacks parent adoption and empirical scoring", "valid_for_claim": False},
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "complete conditional rank-zero closure theorem plus coercive finite residual bound and alpha fallback switch",
            "not_derived": "rank certificate,M_AB m_min/constraint lock,J_retained zero,same-branch parent signature,empirical local scoring",
            "claim_status": "NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": now(),
        }
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NT4522_0",
            "target_file": NEXT_TARGET,
            "task": "audit whether all conditional clauses can be parent-signed in one branch; if not, trigger the first finite alpha/residual runner with explicit missing inputs",
        }
    ]


def validate(sources: list[dict[str, object]], theorem: list[dict[str, object]], current: list[dict[str, object]], decision: list[dict[str, object]], bound: list[dict[str, object]], clauses: list[dict[str, object]], claims: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append({"validation_id": validation_id, "status": "PASS" if ok else "FAIL", "detail": detail})

    add("VAL4522_00_sources", all(row["exists"] and row["needle_found"] for row in sources), "all source paths exist and source needles are found")
    add("VAL4522_01_full_theorem", any(row["theorem_id"] == "RML4522_5_full_conditional_closure" for row in theorem), "full conditional closure theorem row exists")
    add("VAL4522_02_firewall", any(row["current_id"] == "RCF4522_7_verdict" and row["current_status"] == "NOT_CLOSED" for row in current), "retained current firewall remains not closed")
    add("VAL4522_03_decision", any(row["decision_id"] == "RZD4522_4_current_verdict" and row["current_status"] == "NO_CLAIM" for row in decision), "current verdict is no-claim")
    add("VAL4522_04_runner", any(row["runner_id"] == "FBA4522_0_rank_zero_bound" for row in bound) and any(row["runner_id"] == "FBA4522_1_finite_rank_alpha" for row in bound), "rank-zero bound and finite-rank alpha runner rows exist")
    add("VAL4522_05_clauses", len(clauses) == 8 and any(row["clause_id"] == "CLA4522_6_same_branch" for row in clauses), "eight clause rows including same-branch next target")
    add("VAL4522_06_claims_blocked", all(str(row["passed"]).lower() == "false" and str(row["valid_for_claim"]).lower() == "false" for row in claims), "all claim gates remain blocked")
    csv_paths = [SOURCE_REGISTER, THEOREM, CURRENT_FIREWALL, DECISION_MATRIX, BOUND_ALPHA, CLAUSE_AUDIT, CLAIM_GATES, STATUS_CSV, NEXT_CSV]
    parse_ok = True
    detail = []
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            detail.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # noqa: BLE001
            parse_ok = False
            detail.append(f"{path.name}:{exc}")
    add("VAL4522_07_csv_parse", parse_ok, ";".join(detail))
    add("VAL4522_08_next_target", NEXT_TARGET in text(NEXT_CSV), NEXT_TARGET)
    add("VAL4522_09_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after cleanup")
    add("VAL4522_OVERALL", all(row["status"] == "PASS" for row in rows), "4522 rank/M lock and retained current firewall or alpha runner")
    return rows


def build_doc(sources: list[dict[str, object]], theorem: list[dict[str, object]], current: list[dict[str, object]], decision: list[dict[str, object]], bound: list[dict[str, object]], clauses: list[dict[str, object]], claims: list[dict[str, object]], status: list[dict[str, object]], next_target: list[dict[str, object]], validation: list[dict[str, object]]) -> str:
    return f"""# 4522 - Rank/M Lock And Retained Current Firewall Or Alpha Runner

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4522 is the first point where the rank-zero route becomes a complete conditional theorem rather than a stack of loose gates.

Starting from:

`M_AB Z^B = J_A^retained + B_A + C_A^CDB + R_A`

the exact theorem is:

`rank(Z_AB)=0`, locked `M_AB`, `J_A^retained=0`, and the 4520/4521 termwise RHS zeros in the same parent branch imply

`Z=0`, hence the rank-zero local residual vanishes termwise.

The useful bound is also now explicit:

`||Z|| <= m_min^-1 (||J_retained|| + ||B|| + ||CDB|| + ||R||)`.

That is progress, but not a claim. The current corpus still does not parent-sign the rank-zero certificate, `M_AB` lock, no-retained-current firewall, or same-branch adoption. If those fail, the theory must go to finite alpha/residual scoring, not closure prose.

## Source Register

{table(sources)}

## Rank/M Lock Theorem

{table(theorem)}

## Retained Current Firewall

{table(current)}

## Rank-Zero Decision Matrix

{table(decision)}

## Finite Bound Or Alpha Runner

{table(bound)}

## Clause Audit

{table(clauses)}

## Claim Gates

{table(claims)}

## Status

{table(status)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def append_claim_once() -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_rank_zero_lock",
        "claim": "4522 derives the complete conditional rank-zero closure theorem: rank(Z_AB)=0, M_AB lock, J_retained=0 and termwise RHS silence imply Z=0; otherwise a coercive residual/alpha fallback is required.",
        "current_evidence": "Generated theorem RML4522_0-6, retained-current firewall, rank-zero decision matrix, finite bound/alpha runner rows and validation P8_Y5_BRR545_4522_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Rank-zero certificate, M_AB lock, retained-current zero and same-branch parent signature are not parent-signed.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Mistaking a complete conditional theorem for a completed local-GR derivation; finite alpha/residual scorer still required if adoption fails.",
    }
    if not CLAIMS_PATH.exists():
        write_csv(CLAIMS_PATH, [row])
        return
    existing = read_csv(CLAIMS_PATH)
    if any(existing_row.get("claim_id") == CLAIM_ID for existing_row in existing):
        return
    headers = list(existing[0].keys()) if existing else list(row.keys())
    with CLAIMS_PATH.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writerow({header: row.get(header, "") for header in headers})


def main() -> None:
    sources = source_rows()
    theorem = theorem_rows()
    current = current_rows()
    decision = decision_rows()
    bound = bound_rows()
    clauses = clause_rows()
    claims = claim_rows()
    status = status_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM, theorem)
    write_csv(CURRENT_FIREWALL, current)
    write_csv(DECISION_MATRIX, decision)
    write_csv(BOUND_ALPHA, bound)
    write_csv(CLAUSE_AUDIT, clauses)
    write_csv(CLAIM_GATES, claims)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, theorem, current, decision, bound, clauses, claims)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, theorem, current, decision, bound, clauses, claims, status, next_target, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4522 Rank/M Lock And Retained Current Firewall Or Alpha Runner

Marker: `{MARKER}`  
4522 completes the rank-zero route as a conditional theorem: if `rank(Z_AB)=0`, `M_AB` is locked, `J_retained=0`, and the 4520/4521 RHS components vanish termwise in one parent branch, then `Z=0` and the local rank-zero residual vanishes. If any clause fails, the branch must use `||Z|| <= m_min^-1(||J_ret||+||B||+||CDB||+||R||)` or finite `alpha(lambda)` scoring.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4522 Packet Integration

Marker: `{PACKET_MARKER}`  
The private local packet now has a complete conditional rank-zero theorem and a clean fallback switch. The next step is no longer another generic missing ledger: audit same-branch parent signature, or activate the first finite alpha/residual runner. Next target: `{NEXT_TARGET}`.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
