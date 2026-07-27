from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4138-Y5-R2FR-tracefree-Khat-improvement-sign-or-beta-projection-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_TRACEFREE_KHAT_IMPROVEMENT_SIGN_OR_BETA_BOUND_4138"
CHECKPOINT_ID = "4138"
DECISION = "TRACEFREE_KHAT_IMPROVEMENT_FORMAL_ROUTE_UNSIGNED_BETA_BOUND_ROW_FILLED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4138_00_4137_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4137_NEXT_TARGET.csv",
        "4138-Y5-R2FR-tracefree-Khat-improvement-sign-or-beta-projection-bound.md",
        "4137 selected the trace-free Khat improvement or beta-projection fork.",
    ),
    "SRC4138_01_4137_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4137_STATUS.csv",
        "GK_QLOC_RESPONSE_BRANCH_PROVED_CURRENT_BRANCH_RETAINS_DELTAK_PROFILE_BOUND",
        "4137 status: response branch proved, current branch remains Delta_K/D_GK bound only.",
    ),
    "SRC4138_02_4137_profile": (
        SOURCE_DIR / "P8_Y5_R2FR_4137_QLOC_PROFILE_BOUND_ROWS.csv",
        "D_A_grad",
        "4137 D_A_grad profile row that trace-free improvement is supposed to close or bound.",
    ),
    "SRC4138_03_4137_projection": (
        SOURCE_DIR / "P8_Y5_R2FR_4137_PROJECTION_REQUIREMENTS.csv",
        "C_beta_qloc",
        "4137 projection requirement for beta if the trace-free route remains unsigned.",
    ),
    "SRC4138_04_4027_component": (
        SOURCE_DIR / "P8_Y5_R2FR_4027_KHAT_COMPONENT_COMPLETION_GATE.csv",
        "KCG4027_0_tracefree_improvement",
        "4027 component gate: K_L algebraic shape exists but parent signing is missing.",
    ),
    "SRC4138_05_4027_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4027_CONDITIONAL_COMPLETION_PATHS.csv",
        "S_imp=int sqrt|g| c_I phi R",
        "4027 exact completion contract for the trace-free route.",
    ),
    "SRC4138_06_4027_norm": (
        SOURCE_DIR / "P8_Y5_R2FR_4027_DGK_BOUND_NORMALIZATION_ROWS.csv",
        "NORM4027_2_A_grad",
        "4027 D_A_grad normalization row.",
    ),
    "SRC4138_07_4028_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4028_DGK_FIRST_BOUND_ROW.csv",
        "A_TF/L_TF <=",
        "4028 first trace-free residual bound formula.",
    ),
    "SRC4138_08_2220_birth": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
        "TIB2220_9_verdict",
        "2220 birth certificate: trace-free route fails current corpus, retains coefficient envelope.",
    ),
    "SRC4138_09_3025_beta": (
        SOURCE_DIR / "P8_Y5_R2FR_3025_C_BETA_CORE_BOUND_ROWS.csv",
        "7.8e-05",
        "3025 beta core numeric lock, nonclaim because parent source rows are missing.",
    ),
    "SRC4138_10_beta_gates": (
        SOURCE_DIR / "P8_Y5_BETA_QLOC_ACCEPTANCE_GATES.csv",
        "q_loc U2 coefficient has same normalization",
        "Acceptance gate blocking beta promotion without same-normalization proof.",
    ),
    "SRC4138_11_833_amplitude": (
        SOURCE_DIR / "P8_Y5_R10_833_HESSIAN_KHAT_AMPLITUDE_LAW.csv",
        "sqrt(n/(n-1))",
        "Hessian Khat amplitude warning: no parametric suppression from tensor shape alone.",
    ),
    "SRC4138_12_2380_boundary": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2380_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv",
        "exact",
        "Boundary/improvement cancellation source; useful but still conditional on local readout clauses.",
    ),
    "SRC4138_13_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4138_tracefree_Khat_improvement_sign_or_beta_projection_bound.py",
        "Reproducible generator for this 4138 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def tracefree_signing_audit_rows() -> List[dict]:
    data = [
        (
            "TF4138_0_tensor_shape",
            "four-dimensional trace-free Hessian shape",
            "K_L^{mu nu}=2[nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi]",
            "Trace vanishes in four dimensions and matches the derivative trace-free channel.",
            "PASS_FORMAL_SHAPE",
            "shape equality alone is not parent ownership",
        ),
        (
            "TF4138_1_parent_variation",
            "improvement action response",
            "delta int sqrt|g| phi R -> phi G_{mu nu}+(g_{mu nu}Box-nabla_mu nabla_nu)phi plus boundary",
            "The route is a genuine parent-action candidate: the Hessian tensor is not being inserted by hand.",
            "PASS_CONDITIONAL_VARIATION",
            "S_imp is still candidate/staged, not live-adopted in the current corpus",
        ),
        (
            "TF4138_2_tracefree_projection",
            "projected response law",
            "Pi_TF[K_imp]^{mu nu}=2*sigma_resp*c_I[(nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi)-phi G_TF^{mu nu}]",
            "Exact K_L closure requires coefficient matching and routing/silence of the curvature channel.",
            "CONDITIONAL_EXACT_MATCH",
            "sigma_resp*c_I and Pi_TF(phi G) are not source-signed together",
        ),
        (
            "TF4138_3_coefficient_sign",
            "coefficient and sign convention",
            "sigma_resp*c_I=1",
            "This is the local extremum/amplitude law needed for the trace-free component to vanish as a residual.",
            "DERIVED_VALUE_NOT_SOURCE_FIXED",
            "current source hierarchy does not own sigma_resp and c_I as live parent coefficients",
        ),
        (
            "TF4138_4_phi_owner",
            "local phi owner",
            "phi must be a local parent field or constrained auxiliary field whose Euler equation supplies the old Box phi relation",
            "A local-owner template exists, avoiding naked inverse-Box magic.",
            "STAGED_NOT_ADOPTED",
            "owner action adds stress/zero-mode/boundary clauses not closed in the live branch",
        ),
        (
            "TF4138_5_boundary_improvement",
            "boundary and collar silence",
            "B_imp and exact-improvement cancellation must be silent under the local readout collar",
            "Exact cancellation evidence helps, but only under fixed surface/readout/no-corner clauses.",
            "HELPFUL_BUT_UNSIGNED",
            "boundary silence is not mapped to PPN/R10/source units",
        ),
        (
            "TF4138_6_live_Khat_adoption",
            "live Khat adoption",
            "Khat_current^{TF}=Pi_TF[K_imp]",
            "Without live adoption this remains a constructed response branch, not the current MTS Khat.",
            "FAIL_CURRENT_BRANCH",
            "current Khat still has Delta_K/D_GK profile terms",
        ),
        (
            "TF4138_7_amplitude_warning",
            "no automatic smallness",
            "||K_L|| = sqrt(n/(n-1))||Gamma|| in the Hessian carrier normalization",
            "The trace-free shape gives exact matching if signed; it does not by itself suppress amplitude.",
            "BOUND_REQUIRED_IF_UNSIGNED",
            "need A_TF/L_TF and C_beta_qloc or a theorem-zero certificate",
        ),
    ]
    rows: List[dict] = []
    for audit_id, clause, formula, result, status, blocker in data:
        row = row_base()
        row.update(
            {
                "audit_id": audit_id,
                "clause": clause,
                "formula": formula,
                "result": result,
                "status": status,
                "blocker": blocker,
                "tracefree_component_signed": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def theorem_or_bound_rows() -> List[dict]:
    data = [
        (
            "TB4138_0_zero_theorem",
            "trace-free zero theorem",
            "D_TF=0 if sigma_resp*c_I=1, Pi_TF(phi G)=0/channel-routed, D_owner=0, D_boundary=0, and live Khat adoption is signed",
            "exact theorem certificate, not numeric",
            "THEOREM_EXISTS_CONDITIONALLY",
            "not satisfied by the current corpus",
        ),
        (
            "TB4138_1_live_verdict",
            "current-branch verdict",
            "D_TF_current != 0 is retained until all theorem clauses close",
            "current branch remains profile-bound only",
            "ZERO_NOT_CLAIMED",
            "sigma_resp*c_I, phi owner, boundary and live adoption are unsigned",
        ),
        (
            "TB4138_2_master_bound",
            "trace-free residual amplitude law",
            "A_TF/L_TF <= |1-sigma_resp*c_I|A_KL/L_KL + 2|sigma_resp*c_I|A_phiG/L_phiG + A_owner/L_owner + A_boundary/L_boundary + A_adoption/L_adoption",
            "stress-divergence units relative to EH/source normalization",
            "BOUND_LAW_FILLED",
            "symbolic only; no score-ready numeric A_i/L_i rows",
        ),
        (
            "TB4138_3_DA_grad_insert",
            "D_A_grad insertion",
            "D_A_grad <= D_TF + D_conn + D_projector + D_source_normalization",
            "stress-divergence units before PPN/R10 projection",
            "FIRST_DA_GRAD_REDUCTION",
            "trace-free piece is isolated but connection/projector/source-normalization remnants remain",
        ),
        (
            "TB4138_4_projection_need",
            "observable projection need",
            "delta_beta_q_loc = C_beta_qloc * C_Ploc * D_A_grad_envelope",
            "dimensionless beta after same-normalization proof",
            "BETA_BOUND_INTERFACE_FILLED",
            "C_beta_qloc is not source-backed or same-normalized yet",
        ),
    ]
    rows: List[dict] = []
    for theorem_id, item, formula, units, status, blocker in data:
        row = row_base()
        row.update(
            {
                "theorem_id": theorem_id,
                "item": item,
                "formula": formula,
                "units": units,
                "status": status,
                "blocker": blocker,
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def da_grad_beta_bound_rows() -> List[dict]:
    data = [
        (
            "DB4138_0_DA_grad_master",
            "D_A_grad_beta_master",
            "|delta_beta_q_loc| <= |C_beta_qloc|*C_Ploc*(A_TF/L_TF + A_conn/L_conn + A_proj/L_proj + A_srcnorm/L_srcnorm)",
            "dimensionless beta after EH/source same-normalization",
            "NONNUMERIC_BOUND_INTERFACE",
            "C_beta_qloc,C_Ploc,A_TF/L_TF,A_conn/L_conn,A_proj/L_proj,A_srcnorm/L_srcnorm",
        ),
        (
            "DB4138_1_tracefree_piece",
            "A_TF/L_TF",
            "A_TF/L_TF <= |1-sigma_resp*c_I|A_KL/L_KL + 2|sigma_resp*c_I|A_phiG/L_phiG + A_owner/L_owner + A_boundary/L_boundary + A_adoption/L_adoption",
            "stress-divergence units relative to EH/source normalization",
            "SYMBOLIC_COMPONENT_READY",
            "A_KL/L_KL,A_phiG/L_phiG,A_owner/L_owner,A_boundary/L_boundary,A_adoption/L_adoption",
        ),
        (
            "DB4138_2_beta_core_lock_reference",
            "C_beta_core",
            "abs(C_beta_core) <= 7.8e-05",
            "dimensionless",
            "REFERENCE_LOCK_NONCLAIM",
            "same normalization to q_loc U2 coefficient, parent sigma_H/f_psi/A_source rows",
        ),
        (
            "DB4138_3_same_normalization_gate",
            "C_beta_qloc",
            "q_loc U2 coefficient must have same normalization as beta residual or an explicit conversion factor",
            "dimensionless conversion into PPN beta",
            "BLOCKED_BY_ACCEPTANCE_GATE",
            "derive weak-field metric solution sourced by q_loc and extract U^2 coefficient",
        ),
        (
            "DB4138_4_minimum_numeric_pack",
            "first score-ready pack",
            "score_ready only if D_TF components and C_beta_qloc have numeric values, units, source paths and no MISSING markers",
            "mixed symbolic/numeric source pack",
            "NOT_SCORE_READY",
            "parent-owned numeric/source rows absent",
        ),
    ]
    rows: List[dict] = []
    for bound_id, symbol, formula, units, status, required_inputs in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "status": status,
                "required_inputs": required_inputs,
                "score_ready": "False",
                "valid_prediction_row": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_gate_rows() -> List[dict]:
    data = [
        (
            "DG4138_0_actual_derivation",
            "TRACEFREE_ROUTE_HAS_REAL_PARENT_VARIATION",
            "The K_L tensor can be generated by a phi R metric response; this is a real derivation route, not an arbitrary closure axiom.",
            "keep as best local-GR completion path",
        ),
        (
            "DG4138_1_no_live_signing",
            "TRACEFREE_ROUTE_NOT_LIVE_SIGNED",
            "The current corpus still lacks live adoption of S_imp, source-fixed sigma_resp*c_I=1, phi owner, curvature routing and boundary silence.",
            "no D_TF=0 claim",
        ),
        (
            "DG4138_2_bound_filled",
            "D_A_GRAD_BETA_BOUND_ROW_FILLED",
            "The first beta-priority D_A_grad bound interface is now explicit, including A_TF/L_TF and C_beta_qloc requirements.",
            "use for PPN projector normalization next",
        ),
        (
            "DG4138_3_no_score",
            "NO_PPN_OR_LOCAL_GR_SCORE",
            "The beta lock 7.8e-05 is only a nonclaim reference until q_loc has same-normalized U2 projection and parent-owned numeric rows.",
            "all claim flags remain false",
        ),
        (
            "DG4138_4_next",
            "NEXT_CBETA_QLOC_PROJECTOR_SELECTED",
            "The remaining obstruction is no longer the tensor shape; it is converting D_A_grad into a same-normalized beta residual or proving that projection zero.",
            "4139-Y5-R2FR-Cbeta-qloc-projector-normalization-or-first-beta-bound.md",
        ),
    ]
    rows: List[dict] = []
    for gate_id, decision, rationale, next_action in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "decision": decision,
                "rationale": rationale,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4138_0",
            "result": DECISION,
            "summary": (
                "4138 rederives the trace-free Khat improvement route from the phi R metric-response identity, "
                "then refuses to promote it because sigma_resp*c_I, phi owner, curvature routing, boundary silence "
                "and live Khat adoption remain unsigned in the current corpus. The exact zero theorem and the "
                "A_TF/L_TF residual law are recorded, and the first D_A_grad/C_beta_qloc beta-bound interface is filled."
            ),
            "tracefree_parent_variation_derived": "True",
            "tracefree_current_branch_signed": "False",
            "DA_grad_beta_bound_row_filled": "True",
            "score_ready": "False",
            "claim_state": "no D_TF zero, q_loc zero, PPN beta pass, local-GR pass, R10 pass, Newton limit claim, or public evidence claim",
            "next_target": "4139 C_beta_qloc projector normalization or first beta bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4138_0",
            "target_doc": "4139-Y5-R2FR-Cbeta-qloc-projector-normalization-or-first-beta-bound.md",
            "target_script": "scripts/Y5_R2FR_4139_Cbeta_qloc_projector_normalization_or_first_beta_bound.py",
            "objective": (
                "derive the weak-field PPN projector C_beta_qloc for the D_A_grad/q_loc residual, including same-normalization to the beta U2 coefficient; "
                "if the projector cannot be derived, emit the first source-ready numeric acquisition pack for C_beta_qloc and D_A_grad amplitudes"
            ),
            "success_gate": "C_beta_qloc is either theorem-zero/same-normalized or has source-backed units and a nonclaim numeric acquisition ledger",
            "reason": (
                "4138 shows the tensor-shape problem is not the primary obstruction; the next testable bottleneck is the observable projector from D_A_grad to PPN beta."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4138_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4138_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv",
        "P8_Y5_R2FR_4138_TRACEFREE_ZERO_THEOREM_OR_BOUND": SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_ZERO_THEOREM_OR_BOUND.csv",
        "P8_Y5_R2FR_4138_DA_GRAD_BETA_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4138_DA_GRAD_BETA_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4138_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4138_DECISION_GATES.csv",
        "P8_Y5_R2FR_4138_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4138_STATUS.csv",
        "P8_Y5_R2FR_4138_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4138_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4138 - Tracefree Khat Improvement Sign Or Beta Projection Bound",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- The trace-free Khat shape is derivable from a `phi R` metric-response term.",
        "- The current MTS branch is not promoted because the parent-signing clauses are still unsigned.",
        "- The fallback is now a concrete `D_A_grad/C_beta_qloc` beta-bound interface.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(
        [
            "",
            "## Exact Route",
            "",
            "`K_L^{mu nu}=2[nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi]` is the derivative trace-free channel of the metric response of `int sqrt|g| phi R`.",
            "",
            "The projected response law is",
            "",
            "`Pi_TF[K_imp]^{mu nu}=2*sigma_resp*c_I[(nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi)-phi G_TF^{mu nu}]`.",
            "",
            "So exact closure requires `sigma_resp*c_I=1`, `Pi_TF(phi G)=0` or channel routing, parent-owned `phi`, boundary silence, and live Khat adoption.",
            "",
            "## Signing Audit",
            "",
            "| clause | status | blocker |",
            "|---|---|---|",
        ]
    )
    for row in tracefree_signing_audit_rows():
        sections.append(f"| {row['clause']} | {row['status']} | {row['blocker']} |")
    sections.extend(
        [
            "",
            "## Bound Interface",
            "",
            "| symbol | status | required inputs |",
            "|---|---|---|",
        ]
    )
    for row in da_grad_beta_bound_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['required_inputs']} |")
    sections.extend(
        [
            "",
            "## Claim Ceiling",
            "",
            "- No `D_TF=0`, `q_loc=0`, PPN beta, local-GR, R10, Newton-limit, or public evidence claim follows from 4138.",
            "- The useful movement is narrower but real: the tensor-shape objection has been converted into named coefficient/owner/boundary/projector obligations.",
            "",
            "## Next Target",
            "",
            "- `4139-Y5-R2FR-Cbeta-qloc-projector-normalization-or-first-beta-bound.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4138_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT": tracefree_signing_audit_rows,
        "P8_Y5_R2FR_4138_TRACEFREE_ZERO_THEOREM_OR_BOUND": theorem_or_bound_rows,
        "P8_Y5_R2FR_4138_DA_GRAD_BETA_BOUND_ROWS": da_grad_beta_bound_rows,
        "P8_Y5_R2FR_4138_DECISION_GATES": decision_gate_rows,
        "P8_Y5_R2FR_4138_STATUS": status_rows,
        "P8_Y5_R2FR_4138_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4138_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4138_1_doc",
        "checkpoint markdown exists and names decision",
        DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"),
        str(DOC_PATH),
    )

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4138_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT"]])
    audit_ok = all(
        token in audit_text
        for token in [
            "K_L^{mu nu}",
            "phi R",
            "sigma_resp*c_I=1",
            "local phi owner",
            "boundary",
            "live Khat adoption",
            "sqrt(n/(n-1))",
        ]
    )
    add("VAL4138_3_audit", "signing audit covers K_L, phi R response, coefficient, phi owner, boundary, adoption and amplitude warning", audit_ok, "audit tokens checked")

    theorem_text = flatten_rows([outputs["P8_Y5_R2FR_4138_TRACEFREE_ZERO_THEOREM_OR_BOUND"]])
    theorem_ok = all(
        token in theorem_text
        for token in [
            "D_TF=0",
            "A_TF/L_TF <=",
            "D_A_grad <=",
            "delta_beta_q_loc = C_beta_qloc",
            "ZERO_NOT_CLAIMED",
        ]
    )
    add("VAL4138_4_theorem_bound", "zero theorem and residual bound law are present with no zero claim", theorem_ok, "theorem/bound tokens checked")

    beta_text = flatten_rows([outputs["P8_Y5_R2FR_4138_DA_GRAD_BETA_BOUND_ROWS"]])
    beta_ok = all(
        token in beta_text
        for token in [
            "D_A_grad_beta_master",
            "C_beta_qloc",
            "A_TF/L_TF",
            "7.8e-05",
            "same normalization",
            "NOT_SCORE_READY",
        ]
    )
    add("VAL4138_5_beta_rows", "beta-bound rows include D_A_grad master, C_beta_qloc, A_TF/L_TF, beta lock and same-normalization gate", beta_ok, "beta tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4138_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "TRACEFREE_ROUTE_HAS_REAL_PARENT_VARIATION",
            "TRACEFREE_ROUTE_NOT_LIVE_SIGNED",
            "D_A_GRAD_BETA_BOUND_ROW_FILLED",
            "NO_PPN_OR_LOCAL_GR_SCORE",
            "NEXT_CBETA_QLOC_PROJECTOR_SELECTED",
        ]
    )
    add("VAL4138_6_decisions", "decisions record derivation, non-promotion, bound fill, no-score and next projector target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4138_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("tracefree_parent_variation_derived") == "True"
        and status[0].get("tracefree_current_branch_signed") == "False"
        and status[0].get("DA_grad_beta_bound_row_filled") == "True"
    )
    add("VAL4138_7_status", "status records derived parent variation, unsigned current branch and filled beta bound row", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4138_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4139-Y5-R2FR-Cbeta-qloc-projector-normalization-or-first-beta-bound.md"
    add("VAL4138_8_next_target", "next target is C_beta_qloc projector normalization or first beta bound", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4138_9_no_claim_flags", "all generated rows remain no-claim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4138*")) or any(FORMALIZATION.rglob("4138-Y5-R2FR*"))
    add(
        "VAL4138_10_scope",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        in_scope and not formalization_output and not formalization_touched,
        f"doc={DOC_PATH}; csv_count={len(outputs)}",
    )

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4138_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4138_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
