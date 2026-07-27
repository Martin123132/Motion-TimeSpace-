from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4257"
CLAIM_ID = "L-098"
BRANCH = "MTS_R2FR_Y5_PROJECTOR_CERTIFICATE_AND_SPECTRAL_GAP_RUNNER_4257"
DECISION = "PROJECTOR_SOURCE_AUDIT_PARTIAL_SPECTRAL_GAP_MATRIX_RUNNER_STAGED_NONCLAIM"
MARKER = "PPC4161_PROJECTOR_CERTIFICATE_AND_SPECTRAL_GAP_RUNNER_4257"
PACKET_MARKER = "PPC4161_PACKET_PROJECTOR_CERTIFICATE_AND_SPECTRAL_GAP_RUNNER_4257"
NEXT_TARGET = "4258-Y5-R2FR-fill-physical-Dq-gap-matrix-or-component-zero-certificates.md"

FORMAL_PATH = FORMAL / "273-PPC4161-projector-certificate-and-spectral-gap-runner.md"
DOC_PATH = POST / "4257-Y5-R2FR-projector-certificate-and-spectral-gap-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4257_VALIDATION.csv"

MATRIX_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4257_DQ_GAP_MATRIX_CANDIDATE.csv"
MATRIX_TEMPLATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4257_DQ_GAP_MATRIX_TEMPLATE.csv"
RUNNER_RESULT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4257_DQ_GAP_RUNNER_RESULT.csv"

PROBES = (
    "Dq_geom",
    "Dq_tau",
    "Dq_matter",
    "Dq_source_readout",
    "Dq_theta_marker",
    "Dq_boundary_projector",
    "Dq_EM",
    "Dq_coeff",
)
HBASIS = tuple(f"Hbasis_{idx}" for idx in range(8))
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4257_00_4239_Hq_kernel": SourceSpec(
        "SRC4257_00_4239_Hq_kernel",
        FORMAL / "255-PPC4161-parent-source-orthogonality-or-M2-profile-sampler-dry-run.md",
        "H_q in ker(Dq)",
        "4239 source-signs q-basic annihilation for the H_q part.",
    ),
    "SRC4257_01_4243_Hperp_def": SourceSpec(
        "SRC4257_01_4243_Hperp_def",
        FORMAL / "259-PPC4161-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md",
        "Hperp := (1 - Pi_kerDq) H_L",
        "4243 defines the Hperp branch through Pi_kerDq.",
    ),
    "SRC4257_02_4244_adoption_guard": SourceSpec(
        "SRC4257_02_4244_adoption_guard",
        FORMAL / "260-PPC4161-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md",
        "every `H_L` argument certificate is still unsigned",
        "4244 prevents treating component zero theorems as already adopted.",
    ),
    "SRC4257_03_4245_strip": SourceSpec(
        "SRC4257_03_4245_strip",
        FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md",
        "Dq_i[H_L]",
        "4245 strips the q-basic part and leaves Dq_i[Hperp] as live rows.",
    ),
    "SRC4257_04_4256_gap": SourceSpec(
        "SRC4257_04_4256_gap",
        FORMAL / "272-PPC4161-Dq-projection-spectral-gap-bridge.md",
        "C_HDq = 1/sigma_0",
        "4256 identifies the spectral-gap constant.",
    ),
    "SRC4257_05_4256_contract": SourceSpec(
        "SRC4257_05_4256_contract",
        SOURCE_DIR / "P8_Y5_R2FR_4256_BRIDGE_CONTRACT.csv",
        "UNSIGNED_SPECTRAL_GAP_OR_COERCIVITY",
        "4256 bridge contract lists the unsigned gap clauses.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if CLAIM_ID in text:
        return
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = next(csv.reader(handle))
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": (
            "4257 audits the Pi_kerDq route and stages an executable spectral-gap certificate. H_q in ker(Dq) "
            "and the Hperp split are source-backed, but idempotence/range of Pi_kerDq and the physical "
            "Dq gap matrix are not yet signed. No local-GR claim is made."
        ),
        "current_evidence": (
            "4257 source register, projector certificate audit, finite-dimensional gap theorem, Dq gap "
            "matrix template, runner result, decision and firewall."
        ),
        "status": "private_projector_partial_gap_runner_ready_nonclaim",
        "next_test": (
            "Fill the physical metric G_H, Dq Jacobian J, weights W, and projector P matrix rows, or prove "
            "the eight Dq_i component zeros directly."
        ),
        "key_risk": (
            "Calling Pi_kerDq a projector by notation alone would smuggle the kernel-zero and spectral-gap "
            "requirements."
        ),
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "valid_for_claim": "False",
            }
        )
    return rows


def projector_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "PCLAUSE4257_0_Hq_kernel",
            "H_q in ker(Dq)",
            "SIGNED_SOURCE_BACKED_FOR_Hq_BRANCH",
            "255-PPC4161-parent-source-orthogonality-or-M2-profile-sampler-dry-run.md",
            "Dq[H_q]=0 is usable for stripping the q-basic source piece.",
        ),
        (
            "PCLAUSE4257_1_Hperp_split",
            "Hperp=(I-Pi_kerDq)H_L",
            "SIGNED_SOURCE_BACKED_AS_DEFINITION",
            "259/261 split rows",
            "Defines the non-q defect branch but does not prove P is a full physical projector.",
        ),
        (
            "PCLAUSE4257_2_P_idempotent",
            "Pi_kerDq^2=Pi_kerDq",
            "UNSIGNED_PARENT_PROJECTOR_CLAUSE",
            "needs operator definition or matrix row P",
            "Required before eta_Dq_kernel can be set to zero.",
        ),
        (
            "PCLAUSE4257_3_range_kernel",
            "range(Pi_kerDq)=ker(Dq)",
            "UNSIGNED_PARENT_PROJECTOR_CLAUSE",
            "needs Dq Jacobian and rank/nullity check",
            "Required before Hperp complement has no hidden Dq-kernel residue.",
        ),
        (
            "PCLAUSE4257_4_complement_intersection",
            "im(I-Pi_kerDq) cap ker(Dq)={0}",
            "DERIVED_IF_CLAUSES_2_AND_3_PASS",
            "4256 theorem",
            "Would give eta_Dq_kernel=0.",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "status": status,
            "evidence": evidence,
            "consequence": consequence,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, status, evidence, consequence in raw
    ]


def theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "GAP4257_0_matrix_certificate",
            "finite-dimensional physical gap certificate",
            "For a finite residual basis h_a with physical Gram matrix G_ab=<h_a,h_b>_F, Dq Jacobian J_ia=Dq_i[h_a], and positive weight matrix W, the squared gap is sigma_0^2=lambda_min(G^{-1/2} J^T W J G^{-1/2}). If this minimum is positive then C_HDq=1/sigma_0.",
            "DERIVED_EXECUTABLE_CONTRACT",
            "Requires numeric/source-backed G, J, W rows.",
        ),
        (
            "GAP4257_1_projector_matrix_check",
            "projector certificate check",
            "For a candidate projector matrix P on the same basis, check ||P^2-P||=0 and ||J P||=0. Rank(P)=nullity(J) then certifies range(P)=ker(J).",
            "DERIVED_EXECUTABLE_CONTRACT",
            "Requires numeric/source-backed P and J rows.",
        ),
        (
            "GAP4257_2_no_operator_no_claim",
            "notation guard",
            "The string Pi_kerDq is not enough. Until P or an equivalent operator definition is supplied, the route has only H_q annihilation and Hperp splitting, not eta_Dq_kernel=0.",
            "NO_SMUGGLE_GUARD",
            "Prevents closing local-GR by notation.",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "name": name,
            "statement": statement,
            "status": status,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, name, statement, status, guard in raw
    ]


def matrix_template_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for row_id in HBASIS:
        for col_id in HBASIS:
            rows.append(
                {
                    **common(),
                    "candidate_id": "TEMPLATE_ONLY",
                    "object_type": "G_physical_metric",
                    "row_id": row_id,
                    "col_id": col_id,
                    "value": "MISSING_G_PHYSICAL_METRIC",
                    "units": "physical_Hperp_inner_product",
                    "source_path": "MISSING_SOURCE_PATH",
                    "valid_for_claim": "False",
                }
            )
            rows.append(
                {
                    **common(),
                    "candidate_id": "TEMPLATE_ONLY",
                    "object_type": "P_projector",
                    "row_id": row_id,
                    "col_id": col_id,
                    "value": "MISSING_PROJECTOR_MATRIX",
                    "units": "dimensionless_operator",
                    "source_path": "MISSING_SOURCE_PATH",
                    "valid_for_claim": "False",
                }
            )
    for probe in PROBES:
        for basis in HBASIS:
            rows.append(
                {
                    **common(),
                    "candidate_id": "TEMPLATE_ONLY",
                    "object_type": "J_Dq_jacobian",
                    "row_id": probe,
                    "col_id": basis,
                    "value": "MISSING_DQ_JACOBIAN",
                    "units": "Dq_probe_per_Hbasis",
                    "source_path": "MISSING_SOURCE_PATH",
                    "valid_for_claim": "False",
                }
            )
    for probe_row in PROBES:
        for probe_col in PROBES:
            rows.append(
                {
                    **common(),
                    "candidate_id": "TEMPLATE_ONLY",
                    "object_type": "W_probe_weight_metric",
                    "row_id": probe_row,
                    "col_id": probe_col,
                    "value": "MISSING_PROBE_WEIGHT_METRIC",
                    "units": "probe_weight",
                    "source_path": "MISSING_SOURCE_PATH",
                    "valid_for_claim": "False",
                }
            )
    return rows


def parse_float(value: str) -> Optional[float]:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def matmul(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: List[List[float]]) -> List[List[float]]:
    return [list(row) for row in zip(*a)]


def max_abs(a: List[List[float]]) -> float:
    return max((abs(item) for row in a for item in row), default=0.0)


def eye(n: int) -> List[List[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def subtract(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matrix_rank(a: List[List[float]], tol: float = 1.0e-10) -> int:
    mat = [row[:] for row in a]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = max(range(rank, rows), key=lambda r: abs(mat[r][col]), default=rank)
        if pivot >= rows or abs(mat[pivot][col]) <= tol:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        pivot_value = mat[rank][col]
        mat[rank] = [value / pivot_value for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = mat[row][col]
            mat[row] = [mat[row][c] - factor * mat[rank][c] for c in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def jacobi_eigenvalues_symmetric(a: List[List[float]], tol: float = 1.0e-12, max_iter: int = 200) -> List[float]:
    n = len(a)
    mat = [row[:] for row in a]
    for _ in range(max_iter):
        p, q = 0, 1 if n > 1 else 0
        off = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(mat[i][j]) > off:
                    off = abs(mat[i][j])
                    p, q = i, j
        if off <= tol or n <= 1:
            break
        if abs(mat[p][p] - mat[q][q]) <= tol:
            angle = math.pi / 4.0
        else:
            angle = 0.5 * math.atan2(2.0 * mat[p][q], mat[q][q] - mat[p][p])
        c = math.cos(angle)
        s = math.sin(angle)
        for k in range(n):
            apk = mat[p][k]
            aqk = mat[q][k]
            mat[p][k] = c * apk - s * aqk
            mat[q][k] = s * apk + c * aqk
        for k in range(n):
            akp = mat[k][p]
            akq = mat[k][q]
            mat[k][p] = c * akp - s * akq
            mat[k][q] = s * akp + c * akq
    return [mat[i][i] for i in range(n)]


def build_matrix(rows: Iterable[Dict[str, str]], object_type: str) -> Tuple[Optional[List[List[float]]], List[str], List[str], str]:
    selected = [row for row in rows if row.get("object_type") == object_type]
    if not selected:
        return None, [], [], f"MISSING_{object_type}"
    row_ids = sorted({row.get("row_id", "") for row in selected if row.get("row_id", "")})
    col_ids = sorted({row.get("col_id", "") for row in selected if row.get("col_id", "")})
    values: Dict[Tuple[str, str], float] = {}
    for row in selected:
        value = parse_float(row.get("value", ""))
        if value is None:
            return None, row_ids, col_ids, f"NON_NUMERIC_{object_type}"
        values[(row["row_id"], row["col_id"])] = value
    matrix = []
    for row_id in row_ids:
        matrix.append([values.get((row_id, col_id), 0.0) for col_id in col_ids])
    return matrix, row_ids, col_ids, "OK"


def runner_rows() -> List[Dict[str, str]]:
    if not MATRIX_CANDIDATE_PATH.exists():
        return [
            {
                **common(),
                "candidate_id": "NO_GAP_MATRIX_CANDIDATE",
                "status": "BLOCKED_MISSING_GAP_MATRIX_CANDIDATE",
                "projector_residual": "",
                "JP_residual": "",
                "rank_P": "",
                "nullity_J": "",
                "sigma_0": "",
                "C_HDq": "",
                "missing": str(MATRIX_CANDIDATE_PATH),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        ]

    rows = csv_rows(MATRIX_CANDIDATE_PATH)
    candidate_ids = sorted({row.get("candidate_id", "") for row in rows if row.get("candidate_id", "")})
    output: List[Dict[str, str]] = []
    for candidate_id in candidate_ids:
        candidate_rows = [row for row in rows if row.get("candidate_id") == candidate_id]
        g, g_rows, g_cols, g_status = build_matrix(candidate_rows, "G_physical_metric")
        j, j_rows, j_cols, j_status = build_matrix(candidate_rows, "J_Dq_jacobian")
        w, w_rows, w_cols, w_status = build_matrix(candidate_rows, "W_probe_weight_metric")
        p, p_rows, p_cols, p_status = build_matrix(candidate_rows, "P_projector")
        if None in (g, j, w, p):
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "status": "BLOCKED_NONNUMERIC_OR_MISSING_MATRIX",
                    "missing": ";".join(status for status in (g_status, j_status, w_status, p_status) if status != "OK"),
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue
        assert g is not None and j is not None and w is not None and p is not None
        if g_rows != g_cols or w_rows != w_cols or p_rows != p_cols or j_cols != g_rows or j_rows != w_rows:
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "status": "BLOCKED_DIMENSION_MISMATCH",
                    "missing": f"G={len(g_rows)}x{len(g_cols)};J={len(j_rows)}x{len(j_cols)};W={len(w_rows)}x{len(w_cols)};P={len(p_rows)}x{len(p_cols)}",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue
        p_residual = max_abs(subtract(matmul(p, p), p))
        jp_residual = max_abs(matmul(j, p))
        rank_j = matrix_rank(j)
        rank_p = matrix_rank(p)
        nullity_j = len(j_cols) - rank_j
        jt_w_j = matmul(matmul(transpose(j), w), j)
        if max_abs(subtract(g, eye(len(g)))) > 1.0e-10:
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "status": "BLOCKED_NONIDENTITY_G_NOT_YET_SUPPORTED_BY_SIMPLE_RUNNER",
                    "projector_residual": f"{p_residual:.12e}",
                    "JP_residual": f"{jp_residual:.12e}",
                    "rank_P": str(rank_p),
                    "nullity_J": str(nullity_j),
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue
        eigenvalues = jacobi_eigenvalues_symmetric(jt_w_j)
        sigma_sq = max(0.0, min(eigenvalues) if eigenvalues else 0.0)
        sigma_0 = math.sqrt(sigma_sq)
        input_valid = all(row.get("valid_for_claim") == "True" for row in candidate_rows)
        projector_ok = p_residual <= 1.0e-10 and jp_residual <= 1.0e-10 and rank_p == nullity_j
        gap_ok = sigma_0 > 0.0
        output.append(
            {
                **common(),
                "candidate_id": candidate_id,
                "status": "GAP_COMPUTED_NONCLAIM" if projector_ok and gap_ok else "BLOCKED_PROJECTOR_OR_GAP_CONDITION",
                "projector_residual": f"{p_residual:.12e}",
                "JP_residual": f"{jp_residual:.12e}",
                "rank_P": str(rank_p),
                "nullity_J": str(nullity_j),
                "sigma_0": f"{sigma_0:.12e}",
                "C_HDq": f"{(1.0 / sigma_0):.12e}" if sigma_0 > 0.0 else "",
                "claim_allowed": "False",
                "valid_for_claim": str(input_valid and projector_ok and gap_ok),
            }
        )
    return output


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4257_0_partial_sign",
            "The source-backed part is real but limited: H_q in ker(Dq) and the Hperp split are signed; Pi_kerDq idempotence/range is not.",
            "This prevents both defeatism and smuggling.",
            "Fill P matrix/operator rows.",
        ),
        (
            "DEC4257_1_gap_runner",
            "The spectral-gap route is now executable: with G, J, W, and P rows, sigma_0 and C_HDq are computed.",
            "This is the cleanest route because it replaces prose about coupling with a finite matrix certificate.",
            NEXT_TARGET,
        ),
        (
            "DEC4257_2_parallel_zero",
            "The parallel route remains eight component-zero certificates for Dq_i[Hperp].",
            "If all eight close, E_Dq,Hperp=0 and the source branch collapses without needing numeric profiles.",
            "Try direct zero certificates where descent facts already exist.",
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4257_0_projector_notation", "treating Pi_kerDq notation as P^2=P and range(P)=ker(Dq)", "PROJECTOR_OPERATOR_OR_MATRIX_REQUIRED"),
        ("FW4257_1_gap_without_metric", "computing sigma_0 without physical Hperp Gram matrix G", "PHYSICAL_METRIC_G_REQUIRED"),
        ("FW4257_2_gap_without_J", "claiming Dq injectivity without Dq Jacobian/rank evidence", "Dq_JACOBIAN_REQUIRED"),
        ("FW4257_3_component_zero", "setting all epsilon_i=0 without eight argument/descent certificates", "COMPONENT_ZERO_CERTIFICATES_REQUIRED"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden,
            "required_gate": gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, gate in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4257_0",
            "summary": (
                "4257 signs only the clauses current sources truly support, rejects projector-by-notation, "
                "and stages an executable finite-dimensional gap certificate for sigma_0."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": (
                "Fill source-backed G_physical_metric, J_Dq_jacobian, W_probe_weight_metric, and P_projector "
                "rows, or close the eight Dq_i[Hperp] zero certificates one by one."
            ),
            "avoid": "Do not set G=I, P=0, or epsilon_i=0 by convenience.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 273 - PPC4161 projector certificate and spectral-gap runner

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4257 does not prove local GR, PPN safety, R10 safety, clock safety, or EM closure. It separates what the current corpus actually signs from what still needs an operator/matrix certificate.

## What is signed now

Current sources support:

```text
H_q in ker(Dq),
Dq[H_q]=0,
Hperp := (I - Pi_kerDq) H_L.
```

This is enough to strip the q-basic source branch and leave the live `Dq_i[Hperp]` rows. It is not enough to claim that `Pi_kerDq` is a globally defined physical orthogonal projector.

## What is not signed yet

The projector route still needs:

```text
P := Pi_kerDq,
P^2=P,
J_Dq P=0,
rank(P)=nullity(J_Dq).
```

If those pass, then:

```text
range(P)=ker(Dq),
im(I-P) cap ker(Dq) = {{0}},
eta_Dq_kernel=0.
```

## Executable spectral-gap certificate

For a finite local residual basis `h_a`, define:

```text
G_ab := <h_a,h_b>_F,
J_ia := Dq_i[h_a],
W_ij := probe weights.
```

Then:

```text
sigma_0^2 = lambda_min(G^(-1/2) J^T W J G^(-1/2)).
```

If `sigma_0>0`, then:

```text
||Hperp||_F/F_ref <= sigma_0^-1 ||Dq[Hperp]||_W,
C_HDq = 1/sigma_0.
```

4257 writes `P8_Y5_R2FR_4257_DQ_GAP_MATRIX_TEMPLATE.csv` and a runner socket. The runner currently blocks because the physical `G`, `J`, `W`, and `P` rows are not source-backed.

## Parallel zero route

The alternate path is not dead: prove each live row

```text
Dq_geom[Hperp], Dq_tau[Hperp], Dq_matter[Hperp],
Dq_source_readout[Hperp], Dq_theta_marker[Hperp],
Dq_boundary_projector[Hperp], Dq_EM[Hperp], Dq_coeff[Hperp]
```

is zero from descent/argument certificates. If all eight close, then `E_Dq,Hperp=0`.

## Next target

`{NEXT_TARGET}` should fill the finite matrix certificate rows or close the eight component-zero certificates directly.
"""


def checkpoint_doc() -> str:
    return f"""
# 4257 - Y5 R2FR projector certificate and spectral-gap runner

Packet marker: `{PACKET_MARKER}`

## Result

4257 makes the coupling/local-GR bottleneck computational:

```text
sigma_0^2 = lambda_min(G^(-1/2) J^T W J G^(-1/2)),
C_HDq = 1/sigma_0.
```

It also audits the projector:

```text
P^2=P,
J P=0,
rank(P)=nullity(J).
```

## Current verdict

The H_q annihilation and Hperp split are signed. The full projector/range and spectral-gap rows are not. Claim remains false.

## Next action

Fill `P8_Y5_R2FR_4257_DQ_GAP_MATRIX_CANDIDATE.csv` from parent/source rows, or attack the eight Dq component zeros directly.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    projector = csv_rows(paths["projector"])
    theorems = csv_rows(paths["theorems"])
    template = csv_rows(paths["template"])
    runner = csv_rows(paths["runner"])
    rows = [
        ("VAL4257_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4257_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4257_2_partial_signed", any(row["status"].startswith("SIGNED_SOURCE_BACKED") for row in projector), "at least one projector clause is source-backed"),
        ("VAL4257_3_unsigned_guard", any(row["status"].startswith("UNSIGNED") for row in projector), "unsigned projector clauses remain explicit"),
        ("VAL4257_4_gap_theorem", any("sigma_0^2" in row["statement"] for row in theorems), "matrix gap theorem emitted"),
        ("VAL4257_5_template_objects", {row["object_type"] for row in template} == {"G_physical_metric", "P_projector", "J_Dq_jacobian", "W_probe_weight_metric"}, "gap matrix template has all object types"),
        ("VAL4257_6_runner_blocks_or_computes", bool(runner) and runner[0]["status"].startswith(("BLOCKED", "GAP_COMPUTED")), "runner emitted status"),
        ("VAL4257_7_no_claim_runner", all(row.get("claim_allowed") == "False" for row in runner), "runner never claim-allows"),
        ("VAL4257_8_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4257_9_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4257_10_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in rows
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    sources_path = SOURCE_DIR / "P8_Y5_R2FR_4257_SOURCE_REGISTER.csv"
    projector_path = SOURCE_DIR / "P8_Y5_R2FR_4257_PROJECTOR_CERTIFICATE_AUDIT.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4257_GAP_THEOREMS.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4257_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4257_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4257_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4257_NEXT_TARGET.csv"

    write_csv(sources_path, source_rows())
    write_csv(projector_path, projector_audit_rows())
    write_csv(theorem_path, theorem_rows())
    write_csv(MATRIX_TEMPLATE_PATH, matrix_template_rows())
    write_csv(RUNNER_RESULT_PATH, runner_rows())
    write_csv(decision_path, decision_rows())
    write_csv(firewall_path, firewall_rows())
    write_csv(status_path, status_rows())
    write_csv(next_path, next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()

    paths = {
        "sources": sources_path,
        "projector": projector_path,
        "theorems": theorem_path,
        "template": MATRIX_TEMPLATE_PATH,
        "runner": RUNNER_RESULT_PATH,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 10 csv artifacts")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
