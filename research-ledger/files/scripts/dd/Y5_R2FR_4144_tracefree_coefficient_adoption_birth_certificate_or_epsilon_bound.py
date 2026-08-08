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
DOC_PATH = ROOT / "4144-Y5-R2FR-tracefree-coefficient-adoption-birth-certificate-or-epsilon-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_TRACEFREE_COEFFICIENT_BIRTH_CERT_OR_EPSILON_BOUND_4144"
CHECKPOINT_ID = "4144"
DECISION = "MINIMAL_TRACEFREE_PARENT_CLAUSE_CONSTRUCTED_CURRENT_CORPUS_UNSIGNED_EPSILON_BOUND_EMITTED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4144_00_4143_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4143_NEXT_TARGET.csv",
        "4144-Y5-R2FR-tracefree-coefficient-adoption-birth-certificate-or-epsilon-bound.md",
        "4143 selected coefficient adoption birth certificate or epsilon bound.",
    ),
    "SRC4144_01_4143_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4143_COEFFICIENT_ADOPTION_CONTRACT.csv",
        "sigma_resp*c_I=1",
        "4143 coefficient adoption contract.",
    ),
    "SRC4144_02_4143_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4143_STATUS.csv",
        "coefficient_adoption",
        "4143 selected coefficient adoption as route.",
    ),
    "SRC4144_03_4028_derivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4028_TRACEFREE_IMPROVEMENT_DERIVATION.csv",
        "TRACEFREE_FORMULA_DERIVED",
        "4028 trace-free phi R response derivation.",
    ),
    "SRC4144_04_4028_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4028_TRACEFREE_SIGN_AND_PROJECTION_GATE.csv",
        "sigma_resp*c_I=1",
        "4028 trace-free sign/projection gate.",
    ),
    "SRC4144_05_4028_phi": (
        SOURCE_DIR / "P8_Y5_R2FR_4028_PHI_OWNER_LOCAL_ACTION_TEMPLATE.csv",
        "CONSTRUCTED_NOT_ADOPTED",
        "4028 local phi owner candidate.",
    ),
    "SRC4144_06_4138_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv",
        "DERIVED_VALUE_NOT_SOURCE_FIXED",
        "4138 coefficient sign remains source-unsigned.",
    ),
    "SRC4144_07_1526_contract": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1526_COEFFICIENT_SIGN_CONTRACT.csv",
        "COEFFICIENT_MATCH_LAW_DERIVED",
        "1526 coefficient law.",
    ),
    "SRC4144_08_1527_aux": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv",
        "PHI_CONSTRAINT_LOCALIZED",
        "1527 local auxiliary phi contract.",
    ),
    "SRC4144_09_2220_birth": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
        "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
        "2220 current birth certificate fails.",
    ),
    "SRC4144_10_gk_contract": (
        SOURCE_DIR / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
        "K_hat is exactly",
        "GK metric response contract.",
    ),
    "SRC4144_11_gk_candidates": (
        SOURCE_DIR / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
        "best_candidate_not_matched_to_existing_MTS",
        "GK stress action candidate list.",
    ),
    "SRC4144_12_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4144_tracefree_coefficient_adoption_birth_certificate_or_epsilon_bound.py",
        "Reproducible generator for this 4144 checkpoint.",
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


def birth_certificate_rows() -> List[dict]:
    data = [
        (
            "BC4144_0_parent_clause_shape",
            "parent trace-free improvement clause",
            "S_TF=int sqrt|g| c_I phi R + B_TF",
            "candidate/action shape exists and can be written as a minimal parent extension",
            "PASS_CONSTRUCTED_CLAUSE",
            "not yet adopted as live current corpus action",
        ),
        (
            "BC4144_1_response_convention",
            "response sign convention",
            "Khat^TF:=Pi_TF[-2/sqrt|g| delta S_TF/delta g]",
            "fixes sigma_resp inside the proposed parent clause",
            "PASS_WITHIN_CLAUSE",
            "not yet shown identical to all existing Khat/T_GK sign conventions",
        ),
        (
            "BC4144_2_coefficient_value",
            "coefficient value",
            "c_I=sigma_resp^{-1}; epsilon_TF=1-sigma_resp*c_I=0",
            "coefficient zero is achieved constructively in the proposed parent clause",
            "PASS_CONSTRUCTED_NOT_SOURCE_SIGNED",
            "current corpus has no live row adopting this value",
        ),
        (
            "BC4144_3_boundary",
            "boundary convention",
            "B_TF cancels phi R normal-derivative variation and is silent on PPN collar",
            "required for coefficient route not to leak through boundary stress",
            "FAIL_UNSIGNED",
            "boundary/no-flux convention remains source-unsigned",
        ),
        (
            "BC4144_4_curvature_routing",
            "curvature routing",
            "Pi_TF(phi G) is zero in local vacuum or routed into EH/matter channel",
            "keeps the trace-free closure from hiding real curvature response",
            "FAIL_UNSIGNED",
            "local-vacuum/EH routing certificate missing",
        ),
        (
            "BC4144_5_phi_owner",
            "phi owner",
            "Box phi=S_Gamma is local auxiliary/constraint branch",
            "prevents inverse-Box/nonlocal shortcut",
            "PARTIAL_STAGED_NONCLAIM",
            "auxiliary route exists but is not parent-adopted and adds lambda_phi stress",
        ),
        (
            "BC4144_6_live_khat_adoption",
            "live Khat adoption",
            "Khat_current^TF=Pi_TF[K_imp]",
            "needed to move from constructed branch to current MTS branch",
            "FAIL_UNSIGNED",
            "current Khat adoption remains staged/not promoted",
        ),
        (
            "BC4144_7_birth_certificate",
            "birth certificate verdict",
            "epsilon_TF=0 is valid in the constructed parent-extension branch but not source-signed for current corpus",
            "do not claim trace-free beta zero yet",
            "CERTIFICATE_FAILS_CURRENT_CORPUS",
            "emit epsilon_TF bound/acquisition row",
        ),
    ]
    rows: List[dict] = []
    for certificate_id, clause, formula, meaning, status, blocker in data:
        row = row_base()
        row.update(
            {
                "certificate_id": certificate_id,
                "clause": clause,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "blocker": blocker,
                "certificate_pass": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def minimal_parent_clause_rows() -> List[dict]:
    data = [
        (
            "MP4144_0_action_clause",
            "minimal parent clause",
            "Add S_TF=int_M sqrt|g| sigma_resp^{-1} phi R + B_TF[phi,g,partial M]",
            "This is the clean future parent-action route that makes epsilon_TF=0 by construction.",
            "CONSTRUCTIVE_EXTENSION_CLAUSE",
        ),
        (
            "MP4144_1_khat_definition",
            "Khat definition",
            "Khat_TF^{mu nu}:=Pi_TF[-2/sqrt|g| delta S_TF/delta g_{mu nu}]",
            "Adoption must define Khat from the action response, not independently tune Khat.",
            "RESPONSE_DEFINITION_REQUIRED",
        ),
        (
            "MP4144_2_no_retuning_guard",
            "no-retuning guard",
            "sigma_resp^{-1} is fixed by the response convention once, not fitted per source, arena, or dataset",
            "Prevents coefficient adoption from becoming a post-hoc local-solar-system patch.",
            "GUARD_ADDED",
        ),
        (
            "MP4144_3_phi_owner_link",
            "phi owner link",
            "Pair the clause with local auxiliary phi owner or explicitly demote to nonlocal closure",
            "Coefficient zero alone is not a full local field theory without phi ownership.",
            "OWNER_LINK_REQUIRED",
        ),
        (
            "MP4144_4_total_ppn_guard",
            "total PPN guard",
            "Even if derivative TF channel closes, total beta/local-GR requires boundary, curvature, source, readout and total vector gates",
            "Prevents a one-channel win being sold as local GR.",
            "NO_OVERCLAIM_GUARD",
        ),
    ]
    rows: List[dict] = []
    for clause_id, item, formula, meaning, status in data:
        row = row_base()
        row.update(
            {
                "clause_id": clause_id,
                "item": item,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "adoption_signed": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def epsilon_bound_rows() -> List[dict]:
    data = [
        (
            "EB4144_0_epsilon",
            "epsilon_TF",
            "epsilon_TF=1-sigma_resp*c_I",
            "dimensionless",
            "live source rows for sigma_resp and c_I, or parent clause adoption",
            "MISSING_SOURCE_SIGNED_VALUE",
        ),
        (
            "EB4144_1_tracefree_current",
            "J_TF^i",
            "(lambda_00^TF*epsilon_TF/2) partial^i phi",
            "source density times length",
            "epsilon_TF; lambda_00^TF; phi profile",
            "BOUND_FORM_ONLY",
        ),
        (
            "EB4144_2_tracefree_beta",
            "delta_beta_TF",
            "|delta_beta_TF| <= |lambda_00^TF epsilon_TF|/(4N_U2)(|B_phi_gradchi|+|H_phiU2|)+|I_rem_TF|/(2N_U2)",
            "dimensionless beta",
            "epsilon_TF, projection coefficient, scalar overlap, remnant terms, N_U2",
            "NONCLAIM_BOUND_ROW",
        ),
        (
            "EB4144_3_epsilon_acceptance",
            "epsilon_TF acceptance",
            "|epsilon_TF| <= 2 N_U2 (beta_lock - residual_budget) / (|lambda_00^TF|(|B_phi_gradchi|+|H_phiU2|))",
            "dimensionless upper bound",
            "positive denominator; residual budget; beta lock; all profile terms",
            "SYMBOLIC_ACCEPTANCE_BOUND",
        ),
        (
            "EB4144_4_total_guard",
            "total local PPN",
            "local_GR requires total beta/gamma/alpha_i/source vector below bounds after absolute no-cancellation sum",
            "dimensionless and arena-specific",
            "all local PPN residual channels",
            "TOTAL_GUARD_RETAINED",
        ),
    ]
    rows: List[dict] = []
    for bound_id, symbol, formula, units, required_inputs, status in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "required_inputs": required_inputs,
                "status": status,
                "numeric_value_present": "False",
                "source_backed": "False",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_gate_rows() -> List[dict]:
    data = [
        (
            "DG4144_0_constructive_progress",
            "MINIMAL_PARENT_CLAUSE_CONSTRUCTED",
            "A future parent action can set epsilon_TF=0 cleanly by defining c_I=sigma_resp^{-1} in the trace-free phi R response clause.",
            "record as constructive extension route",
        ),
        (
            "DG4144_1_current_nonclaim",
            "CURRENT_CORPUS_BIRTH_CERTIFICATE_FAILS",
            "Current corpus still lacks live action adoption, global sign convention, boundary convention, curvature routing, phi owner adoption and live Khat adoption.",
            "no trace-free beta zero claim",
        ),
        (
            "DG4144_2_epsilon_bound",
            "EPSILON_BOUND_ROWS_EMITTED",
            "If adoption remains unsigned, epsilon_TF is now a retained dimensionless residual with beta-bound acceptance formula.",
            "use if parent adoption fails",
        ),
        (
            "DG4144_3_next",
            "NEXT_BOUNDARY_CURVATURE_ROUTING_SELECTED",
            "The coefficient value can be fixed by the constructed clause; the next hard blockers are boundary silence and curvature routing/live adoption.",
            "4145-Y5-R2FR-tracefree-boundary-curvature-routing-or-live-adoption-gate.md",
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
            "status_id": "STATUS4144_0",
            "result": DECISION,
            "summary": (
                "4144 constructs the minimal parent-extension clause that would set epsilon_TF=1-sigma_resp*c_I=0: "
                "S_TF=int sqrt|g| sigma_resp^{-1} phi R plus the correct boundary term, with Khat^TF defined as the metric response. "
                "This is constructive progress, but the current corpus birth certificate still fails because boundary convention, curvature routing, phi owner adoption and live Khat adoption remain unsigned. "
                "A nonclaim epsilon_TF bound/acquisition row is emitted."
            ),
            "minimal_parent_clause_constructed": "True",
            "current_birth_certificate_passed": "False",
            "epsilon_zero_claimed": "False",
            "epsilon_bound_rows_filled": "True",
            "score_ready": "False",
            "claim_state": "no epsilon_TF zero claim, trace-free beta zero, q_loc beta pass, total PPN pass, local-GR pass, Newton limit claim, or public evidence claim",
            "next_target": "4145 tracefree boundary-curvature routing or live adoption gate",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4144_0",
            "target_doc": "4145-Y5-R2FR-tracefree-boundary-curvature-routing-or-live-adoption-gate.md",
            "target_script": "scripts/Y5_R2FR_4145_tracefree_boundary_curvature_routing_or_live_adoption_gate.py",
            "objective": (
                "attempt to close the remaining coefficient-branch blockers after the minimal parent clause: boundary/improvement silence, Pi_TF(phi G) curvature routing, phi owner adoption and live Khat^TF adoption; "
                "if not closed, emit source-ready D_boundary/D_phiG/D_adoption bound rows"
            ),
            "success_gate": "boundary, curvature routing and live adoption are signed for the trace-free branch, or retained bound rows exist for each blocker",
            "reason": "4144 can construct epsilon_TF=0 as a parent-extension clause, but current proof still fails on boundary, curvature routing, phi owner and live adoption.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4144_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4144_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4144_BIRTH_CERTIFICATE": SOURCE_DIR / "P8_Y5_R2FR_4144_BIRTH_CERTIFICATE.csv",
        "P8_Y5_R2FR_4144_MINIMAL_PARENT_CLAUSE": SOURCE_DIR / "P8_Y5_R2FR_4144_MINIMAL_PARENT_CLAUSE.csv",
        "P8_Y5_R2FR_4144_EPSILON_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4144_EPSILON_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4144_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4144_DECISION_GATES.csv",
        "P8_Y5_R2FR_4144_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4144_STATUS.csv",
        "P8_Y5_R2FR_4144_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4144_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4144 - Tracefree Coefficient Adoption Birth Certificate Or Epsilon Bound",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- Constructive route: a minimal parent clause can set `epsilon_TF=0` by defining `c_I=sigma_resp^{-1}` in the `phi R` response branch.",
        "- Current-corpus proof: still unsigned because boundary, curvature routing, phi owner and live Khat adoption remain open.",
        "- No trace-free beta/local-GR/Newton claim is made.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(
        [
            "",
            "## Minimal Parent Clause",
            "",
            "`S_TF=int_M sqrt|g| sigma_resp^{-1} phi R + B_TF[phi,g,partial M]`.",
            "",
            "`Khat_TF^{mu nu}:=Pi_TF[-2/sqrt|g| delta S_TF/delta g_{mu nu}]`.",
            "",
            "This makes `epsilon_TF=1-sigma_resp*c_I=0` in the constructed parent-extension branch.",
            "",
            "## Birth Certificate",
            "",
            "| clause | status | blocker |",
            "|---|---|---|",
        ]
    )
    for row in birth_certificate_rows():
        sections.append(f"| {row['clause']} | {row['status']} | {row['blocker']} |")
    sections.extend(
        [
            "",
            "## Epsilon Bound",
            "",
            "| symbol | status | required inputs |",
            "|---|---|---|",
        ]
    )
    for row in epsilon_bound_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['required_inputs']} |")
    sections.extend(
        [
            "",
            "## Claim Ceiling",
            "",
            "- No `epsilon_TF=0` claim, trace-free beta zero, `q_loc` beta pass, total PPN pass, local-GR pass, Newton-limit claim, or public evidence claim follows from 4144.",
            "- The useful movement is that coefficient zero is constructible in a future parent action, while current proof has exact remaining blockers.",
            "",
            "## Next Target",
            "",
            "- `4145-Y5-R2FR-tracefree-boundary-curvature-routing-or-live-adoption-gate.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4144_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4144_BIRTH_CERTIFICATE": birth_certificate_rows,
        "P8_Y5_R2FR_4144_MINIMAL_PARENT_CLAUSE": minimal_parent_clause_rows,
        "P8_Y5_R2FR_4144_EPSILON_BOUND_ROWS": epsilon_bound_rows,
        "P8_Y5_R2FR_4144_DECISION_GATES": decision_gate_rows,
        "P8_Y5_R2FR_4144_STATUS": status_rows,
        "P8_Y5_R2FR_4144_NEXT_TARGET": next_target_rows,
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
        "VAL4144_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4144_1_doc",
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
    add("VAL4144_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    cert_text = flatten_rows([outputs["P8_Y5_R2FR_4144_BIRTH_CERTIFICATE"]])
    cert_ok = all(
        token in cert_text
        for token in [
            "S_TF",
            "Khat^TF",
            "epsilon_TF",
            "B_TF",
            "Pi_TF(phi G)",
            "Box phi=S_Gamma",
            "Khat_current^TF",
            "CERTIFICATE_FAILS_CURRENT_CORPUS",
        ]
    )
    add("VAL4144_3_birth_certificate", "birth certificate covers action, response, epsilon, boundary, curvature, phi owner, Khat adoption and verdict", cert_ok, "certificate tokens checked")

    clause_text = flatten_rows([outputs["P8_Y5_R2FR_4144_MINIMAL_PARENT_CLAUSE"]])
    clause_ok = all(
        token in clause_text
        for token in [
            "sigma_resp^{-1}",
            "Khat_TF",
            "no-retuning",
            "phi owner",
            "total PPN guard",
        ]
    )
    add("VAL4144_4_minimal_clause", "minimal parent clause records action clause, Khat definition, no-retuning guard, phi owner link and PPN guard", clause_ok, "clause tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4144_EPSILON_BOUND_ROWS"]])
    bound_ok = all(
        token in bound_text
        for token in [
            "epsilon_TF=1-sigma_resp*c_I",
            "J_TF^i",
            "delta_beta_TF",
            "epsilon_TF acceptance",
            "total local PPN",
        ]
    )
    add("VAL4144_5_epsilon_bounds", "epsilon bound rows cover epsilon, current, beta residual, acceptance and total PPN guard", bound_ok, "bound tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4144_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "MINIMAL_PARENT_CLAUSE_CONSTRUCTED",
            "CURRENT_CORPUS_BIRTH_CERTIFICATE_FAILS",
            "EPSILON_BOUND_ROWS_EMITTED",
            "NEXT_BOUNDARY_CURVATURE_ROUTING_SELECTED",
        ]
    )
    add("VAL4144_6_decisions", "decisions record constructive clause, current fail, epsilon bounds and next blocker target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4144_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("minimal_parent_clause_constructed") == "True"
        and status[0].get("current_birth_certificate_passed") == "False"
        and status[0].get("epsilon_zero_claimed") == "False"
        and status[0].get("epsilon_bound_rows_filled") == "True"
    )
    add("VAL4144_7_status", "status records constructed clause, failed current certificate, no epsilon claim and bound rows", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4144_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4145-Y5-R2FR-tracefree-boundary-curvature-routing-or-live-adoption-gate.md"
    add("VAL4144_8_next_target", "next target is trace-free boundary-curvature routing or live adoption gate", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4144_9_no_claim_flags", "all generated rows remain no-claim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4144*")) or any(FORMALIZATION.rglob("4144-Y5-R2FR*"))
    add(
        "VAL4144_10_scope",
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
    add("VAL4144_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4144_VALIDATION.csv"
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
