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
DOC_PATH = ROOT / "4143-Y5-R2FR-tracefree-coefficient-adoption-or-phi-nohair-route-selector.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_TRACEFREE_COEFFICIENT_OR_PHI_NOHAIR_SELECTOR_4143"
CHECKPOINT_ID = "4143"
DECISION = "COEFFICIENT_ADOPTION_SELECTED_AS_LOWER_SCRUTINY_TRACEFREE_ZERO_ROUTE_NONCLAIM"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4143_00_4142_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4142_NEXT_TARGET.csv",
        "4143-Y5-R2FR-tracefree-coefficient-adoption-or-phi-nohair-route-selector.md",
        "4142 selected coefficient adoption or phi no-hair route selector.",
    ),
    "SRC4143_01_4142_derivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4142_SCALAR_OVERLAP_DERIVATION.csv",
        "NO_GENERIC_ZERO",
        "4142 rejects generic scalar-hair U2 orthogonality.",
    ),
    "SRC4143_02_4142_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4142_ZERO_ROUTE_AUDIT.csv",
        "UNSIGNED_STRONG_THEOREM",
        "4142 marks phi no-hair as strong unsigned theorem.",
    ),
    "SRC4143_03_4141_current": (
        SOURCE_DIR / "P8_Y5_R2FR_4141_TRACEFREE_CURRENT_DERIVATION.csv",
        "epsilon_TF:=1-sigma_resp*c_I",
        "4141 current law exposes coefficient mismatch as the multiplier of the trace-free current.",
    ),
    "SRC4143_04_4138_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv",
        "sigma_resp*c_I=1",
        "4138 coefficient/sign route for trace-free Khat improvement.",
    ),
    "SRC4143_05_4138_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_ZERO_THEOREM_OR_BOUND.csv",
        "D_TF=0",
        "4138 exact trace-free zero theorem under coefficient/adoption clauses.",
    ),
    "SRC4143_06_1526_contract": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1526_COEFFICIENT_SIGN_CONTRACT.csv",
        "COEFFICIENT_MATCH_LAW_DERIVED",
        "1526 coefficient law source.",
    ),
    "SRC4143_07_1527_aux": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv",
        "CONDITIONAL_LOCAL_ROUTE_NOT_PROMOTED",
        "1527 local phi auxiliary route remains conditional.",
    ),
    "SRC4143_08_1527_nonlocal": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1527_NONLOCALITY_GUARD.csv",
        "REJECT_FOR_LOCAL_FIELD_THEORY_CLAIM",
        "1527 rejects inverse-Box shortcut for local field-theory claims.",
    ),
    "SRC4143_09_2220_birth": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
        "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
        "2220 birth certificate remains failed for current corpus.",
    ),
    "SRC4143_10_833_amplitude": (
        SOURCE_DIR / "P8_Y5_R10_833_HESSIAN_KHAT_AMPLITUDE_LAW.csv",
        "no_parametric_amplitude_suppression",
        "833 amplitude warning: coefficient/adoption or bound needed; shape gives no smallness.",
    ),
    "SRC4143_11_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4143_tracefree_coefficient_adoption_or_phi_nohair_route_selector.py",
        "Reproducible generator for this 4143 checkpoint.",
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


def route_comparison_rows() -> List[dict]:
    data = [
        (
            "RC4143_0_coefficient_route",
            "coefficient adoption",
            "epsilon_TF=1-sigma_resp*c_I=0",
            "action/sign/adoption problem already tied to phi R response",
            "requires live parent coefficient/sign row, boundary convention, curvature routing, phi owner, live Khat adoption",
            "LOWER_SCRUTINY_SELECTED_NONCLAIM",
            "one algebraic coefficient condition kills the whole trace-free current if parent-signed",
        ),
        (
            "RC4143_1_nohair_route",
            "phi no-hair",
            "phi=0 or S_phi=0 with homogeneous boundary data",
            "strong local scalar theorem",
            "requires live phi action, source silence, boundary zero, lambda_phi stress silence, no hidden scalar charge",
            "HIGHER_SCRUTINY_RETAINED_AS_BOUND",
            "4142 shows generic scalar-hair U2 overlap is not zero",
        ),
        (
            "RC4143_2_weighted_orthogonality",
            "weighted source orthogonality",
            "int chi_U S_phi d^3x + B_phi_chi=0",
            "would zero H_phiU2 without phi=0",
            "requires parent symmetry or universal selection theorem; otherwise looks like tuned boundary/source calibration",
            "NOT_SELECTED",
            "too easy to become post-hoc domain fitting",
        ),
        (
            "RC4143_3_numeric_bound",
            "numeric overlap bound",
            "|delta_beta_TF| <= (|B_TF|+|I_TF|+|I_rem_TF|)/(2N_U2)",
            "fallback empirical/sourced route",
            "requires U, chi_U, phi, S_phi, boundary values, N_U2 and all remnant integrals",
            "FALLBACK_IF_ADOPTION_FAILS",
            "testable but data-heavy; does not derive local GR",
        ),
    ]
    rows: List[dict] = []
    for route_id, route, zero_condition, route_type, required_clauses, status, rationale in data:
        row = row_base()
        row.update(
            {
                "route_id": route_id,
                "route": route,
                "zero_condition": zero_condition,
                "route_type": route_type,
                "required_clauses": required_clauses,
                "status": status,
                "rationale": rationale,
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def coefficient_adoption_contract_rows() -> List[dict]:
    data = [
        (
            "CA4143_0_parent_term",
            "parent improvement term",
            "S_imp=int sqrt|g| c_I phi R + B_imp",
            "term is present in live parent action and not only candidate prose",
            "UNSIGNED",
        ),
        (
            "CA4143_1_response_sign",
            "response sign convention",
            "sigma_resp fixed by Khat=-2/sqrt|g| delta S/delta g or declared equivalent",
            "single live convention used across Khat, T_GK and PPN source rows",
            "UNSIGNED",
        ),
        (
            "CA4143_2_coefficient_match",
            "coefficient law",
            "sigma_resp*c_I=1",
            "sets epsilon_TF=0 and kills J_TF, I_TF and H_phiU2 dependence in the trace-free derivative channel",
            "DERIVED_NOT_SOURCE_FIXED",
        ),
        (
            "CA4143_3_boundary_convention",
            "boundary/improvement convention",
            "B_imp cancels normal derivative variation and is silent on the PPN collar",
            "prevents coefficient adoption from leaking through B_TF or boundary stress",
            "UNSIGNED",
        ),
        (
            "CA4143_4_curvature_routing",
            "curvature channel",
            "Pi_TF(phi G) is zero in local vacuum or routed into EH/matter response rather than K_L",
            "prevents hiding genuine curvature source in trace-free closure",
            "UNSIGNED",
        ),
        (
            "CA4143_5_phi_owner",
            "local phi owner",
            "Box phi=S_Gamma is local auxiliary/constraint branch, not naked inverse-Box",
            "needed for field-theory legitimacy even if epsilon_TF kills the trace-free current",
            "STAGED_NONCLAIM",
        ),
        (
            "CA4143_6_live_adoption",
            "live Khat adoption",
            "Khat_current^TF=Pi_TF[K_imp]",
            "turns constructed response branch into current MTS branch",
            "UNSIGNED",
        ),
        (
            "CA4143_7_result",
            "adoption result",
            "if CA4143_0..6 pass, then D_TF^derivative=0 and delta_beta_TF derivative channel is zero",
            "local beta still needs remnant/total PPN vector gates",
            "CONDITIONAL_TARGET",
        ),
    ]
    rows: List[dict] = []
    for contract_id, clause, formula, pass_condition, status in data:
        row = row_base()
        row.update(
            {
                "contract_id": contract_id,
                "clause": clause,
                "formula": formula,
                "pass_condition": pass_condition,
                "status": status,
                "adoption_signed": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def phi_nohair_audit_rows() -> List[dict]:
    data = [
        (
            "NH4143_0_live_phi_action",
            "live phi action",
            "S_phiK adopted as parent action",
            "STAGED_NONCLAIM",
            "1527 auxiliary route not promoted",
        ),
        (
            "NH4143_1_source_silence",
            "source silence",
            "S_phi=(2/3)(Gamma_eff+C)+remnants=0 in PPN collar",
            "UNSIGNED_STRONG_REQUIREMENT",
            "Gamma_eff/source profile not shown zero",
        ),
        (
            "NH4143_2_boundary_homogeneous",
            "homogeneous boundary",
            "phi=0 and partial_n phi=0 or energy/no-flux condition on collar",
            "UNSIGNED_BOUNDARY",
            "boundary conventions remain open",
        ),
        (
            "NH4143_3_lambda_silence",
            "lambda_phi stress silence",
            "lambda_phi=nabla lambda_phi=0 or stress is routed/bounded",
            "UNSIGNED_REMAINDER",
            "2220 keeps lambda_phi stress blocked",
        ),
        (
            "NH4143_4_no_scalar_charge",
            "no scalar charge",
            "no hidden scalar monopole/tail survives outside compact support",
            "UNSIGNED_NOHAIR",
            "4142 generic nonzero guard blocks shortcut",
        ),
        (
            "NH4143_5_verdict",
            "phi no-hair route",
            "phi no-hair is not the next route unless coefficient adoption fails and a strong scalar theorem is targeted",
            "DEMOTED_TO_BOUND_BACKSTOP",
            "higher-scrutiny than coefficient adoption",
        ),
    ]
    rows: List[dict] = []
    for audit_id, gate, pass_condition, status, blocker in data:
        row = row_base()
        row.update(
            {
                "audit_id": audit_id,
                "gate": gate,
                "pass_condition": pass_condition,
                "status": status,
                "blocker": blocker,
                "gate_passed": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def rejected_branch_bound_rows() -> List[dict]:
    data = [
        (
            "RB4143_0_phi_nohair_backstop",
            "H_phiU2",
            "|H_phiU2| <= ||chi_U||_2 ||S_phi||_2 + |B_phi_chi|",
            "scalar overlap units",
            "chi_U; S_phi; B_phi_chi; source paths",
            "PHI_NOHAIR_BOUND_BACKSTOP",
        ),
        (
            "RB4143_1_coefficient_residual",
            "epsilon_TF",
            "epsilon_TF=1-sigma_resp*c_I",
            "dimensionless",
            "live sigma_resp and c_I rows or bounded residual |epsilon_TF|",
            "COEFFICIENT_ACQUISITION_NEEDED",
        ),
        (
            "RB4143_2_tracefree_beta",
            "delta_beta_TF",
            "|delta_beta_TF| <= |lambda_00^TF epsilon_TF|/(4N_U2)(|B_phi_gradchi|+|H_phiU2|)+|I_rem_TF|/(2N_U2)",
            "dimensionless beta",
            "lambda_00^TF; epsilon_TF; H_phiU2; boundary/remnant terms; N_U2",
            "NONCLAIM_COMBINED_BOUND",
        ),
        (
            "RB4143_3_total_ppn_guard",
            "delta_beta_total",
            "|delta_beta_total| <= |delta_beta_source|+|delta_beta_R11|+|delta_beta_TF|+|delta_beta_boundary|+|delta_beta_readout|",
            "dimensionless beta",
            "all beta channels theorem-zero or source-backed",
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
            "DG4143_0_route_selected",
            "COEFFICIENT_ADOPTION_SELECTED",
            "Coefficient adoption is the lower-scrutiny trace-free zero route because it kills the current by parent action/sign convention rather than requiring scalar no-hair.",
            "pursue parent coefficient adoption next",
        ),
        (
            "DG4143_1_no_public_claim",
            "ROUTE_SELECTED_NOT_SIGNED",
            "The route is selected but not promoted: live parent action, sign, boundary, curvature routing, phi owner and Khat adoption remain unsigned.",
            "all claim flags stay false",
        ),
        (
            "DG4143_2_nohair_demoted",
            "PHI_NOHAIR_DEMOTED_TO_BOUND_BACKSTOP",
            "4142 rejected generic U2 orthogonality, so no-hair is retained as a strong theorem/backstop, not the main next path.",
            "keep H_phiU2 bound rows",
        ),
        (
            "DG4143_3_bound_pack",
            "REJECTED_BRANCH_BOUND_ROWS_FILLED",
            "The rejected/backstop branch has explicit H_phiU2, epsilon_TF, delta_beta_TF and total beta bound rows.",
            "use if adoption fails",
        ),
        (
            "DG4143_4_next",
            "NEXT_COEFFICIENT_BIRTH_CERTIFICATE_SELECTED",
            "The next concrete task is the parent coefficient/adoption birth certificate for epsilon_TF=0.",
            "4144-Y5-R2FR-tracefree-coefficient-adoption-birth-certificate-or-epsilon-bound.md",
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
            "status_id": "STATUS4143_0",
            "result": DECISION,
            "summary": (
                "4143 compares the two clean trace-free beta zero routes. Phi no-hair/weighted-source orthogonality is higher scrutiny because 4142 shows generic scalar hair is not U2-orthogonal and current phi owner rows are staged nonclaim. "
                "Coefficient adoption is selected as the lower-scrutiny next route: source-sign epsilon_TF=1-sigma_resp*c_I=0 through the parent phi R response, boundary convention, curvature routing, phi owner and live Khat adoption. "
                "No trace-free beta zero or local-GR claim is made."
            ),
            "route_selected": "coefficient_adoption",
            "route_signed": "False",
            "phi_nohair_demoted_to_bound": "True",
            "bound_rows_filled": "True",
            "score_ready": "False",
            "claim_state": "no epsilon_TF zero claim, trace-free beta zero, q_loc beta pass, total PPN pass, local-GR pass, Newton limit claim, or public evidence claim",
            "next_target": "4144 tracefree coefficient adoption birth certificate or epsilon bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4143_0",
            "target_doc": "4144-Y5-R2FR-tracefree-coefficient-adoption-birth-certificate-or-epsilon-bound.md",
            "target_script": "scripts/Y5_R2FR_4144_tracefree_coefficient_adoption_birth_certificate_or_epsilon_bound.py",
            "objective": (
                "attempt the parent coefficient/adoption birth certificate for epsilon_TF=1-sigma_resp*c_I=0: live S_imp term, fixed response sign, c_I value, boundary convention, curvature routing, phi owner and live Khat adoption; "
                "if any clause remains unsigned, emit a source-ready |epsilon_TF| bound/acquisition row"
            ),
            "success_gate": "epsilon_TF=0 is parent-signed for the trace-free derivative channel, or |epsilon_TF| has a nonclaim source-ready bound row",
            "reason": "4143 selects coefficient adoption as the lower-scrutiny route over a strong phi no-hair theorem.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4143_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4143_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4143_ROUTE_COMPARISON": SOURCE_DIR / "P8_Y5_R2FR_4143_ROUTE_COMPARISON.csv",
        "P8_Y5_R2FR_4143_COEFFICIENT_ADOPTION_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4143_COEFFICIENT_ADOPTION_CONTRACT.csv",
        "P8_Y5_R2FR_4143_PHI_NOHAIR_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4143_PHI_NOHAIR_AUDIT.csv",
        "P8_Y5_R2FR_4143_REJECTED_BRANCH_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4143_REJECTED_BRANCH_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4143_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4143_DECISION_GATES.csv",
        "P8_Y5_R2FR_4143_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4143_STATUS.csv",
        "P8_Y5_R2FR_4143_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4143_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4143 - Tracefree Coefficient Adoption Or Phi Nohair Route Selector",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- Selected route: coefficient adoption, because `epsilon_TF=0` kills the trace-free current without needing scalar no-hair.",
        "- Demoted route: phi no-hair / weighted-source orthogonality, retained only as a bound backstop.",
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
            "## Route Comparison",
            "",
            "| route | status | rationale |",
            "|---|---|---|",
        ]
    )
    for row in route_comparison_rows():
        sections.append(f"| {row['route']} | {row['status']} | {row['rationale']} |")
    sections.extend(
        [
            "",
            "## Coefficient Adoption Contract",
            "",
            "| clause | status | pass condition |",
            "|---|---|---|",
        ]
    )
    for row in coefficient_adoption_contract_rows():
        sections.append(f"| {row['clause']} | {row['status']} | {row['pass_condition']} |")
    sections.extend(
        [
            "",
            "## Phi Nohair Backstop",
            "",
            "| gate | status | blocker |",
            "|---|---|---|",
        ]
    )
    for row in phi_nohair_audit_rows():
        sections.append(f"| {row['gate']} | {row['status']} | {row['blocker']} |")
    sections.extend(
        [
            "",
            "## Claim Ceiling",
            "",
            "- No `epsilon_TF=0` claim, trace-free beta zero, `q_loc` beta pass, total PPN pass, local-GR pass, Newton-limit claim, or public evidence claim follows from 4143.",
            "- The useful movement is strategic: stop chasing generic scalar no-hair and try to parent-sign the coefficient/adoption birth certificate.",
            "",
            "## Next Target",
            "",
            "- `4144-Y5-R2FR-tracefree-coefficient-adoption-birth-certificate-or-epsilon-bound.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4143_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4143_ROUTE_COMPARISON": route_comparison_rows,
        "P8_Y5_R2FR_4143_COEFFICIENT_ADOPTION_CONTRACT": coefficient_adoption_contract_rows,
        "P8_Y5_R2FR_4143_PHI_NOHAIR_AUDIT": phi_nohair_audit_rows,
        "P8_Y5_R2FR_4143_REJECTED_BRANCH_BOUND_ROWS": rejected_branch_bound_rows,
        "P8_Y5_R2FR_4143_DECISION_GATES": decision_gate_rows,
        "P8_Y5_R2FR_4143_STATUS": status_rows,
        "P8_Y5_R2FR_4143_NEXT_TARGET": next_target_rows,
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
        "VAL4143_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4143_1_doc",
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
    add("VAL4143_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    route_text = flatten_rows([outputs["P8_Y5_R2FR_4143_ROUTE_COMPARISON"]])
    route_ok = all(
        token in route_text
        for token in [
            "coefficient adoption",
            "LOWER_SCRUTINY_SELECTED_NONCLAIM",
            "phi no-hair",
            "HIGHER_SCRUTINY_RETAINED_AS_BOUND",
            "numeric overlap bound",
        ]
    )
    add("VAL4143_3_route_comparison", "route comparison selects coefficient route and retains nohair/numeric routes as backstops", route_ok, "route tokens checked")

    contract_text = flatten_rows([outputs["P8_Y5_R2FR_4143_COEFFICIENT_ADOPTION_CONTRACT"]])
    contract_ok = all(
        token in contract_text
        for token in [
            "S_imp",
            "sigma_resp",
            "sigma_resp*c_I=1",
            "B_imp",
            "Pi_TF(phi G)",
            "Box phi=S_Gamma",
            "Khat_current^TF",
            "CONDITIONAL_TARGET",
        ]
    )
    add("VAL4143_4_adoption_contract", "coefficient adoption contract covers parent term, sign, coefficient, boundary, curvature, phi owner, Khat adoption and result", contract_ok, "contract tokens checked")

    nohair_text = flatten_rows([outputs["P8_Y5_R2FR_4143_PHI_NOHAIR_AUDIT"]])
    nohair_ok = all(
        token in nohair_text
        for token in [
            "live phi action",
            "source silence",
            "homogeneous boundary",
            "lambda_phi stress silence",
            "no scalar charge",
            "DEMOTED_TO_BOUND_BACKSTOP",
        ]
    )
    add("VAL4143_5_nohair_audit", "phi nohair audit covers live action, source silence, boundary, lambda stress, scalar charge and demotion", nohair_ok, "nohair tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4143_REJECTED_BRANCH_BOUND_ROWS"]])
    bound_ok = all(
        token in bound_text
        for token in [
            "H_phiU2",
            "epsilon_TF",
            "delta_beta_TF",
            "delta_beta_total",
        ]
    )
    add("VAL4143_6_bound_rows", "bound rows retain H_phiU2, epsilon_TF, delta_beta_TF and total beta guard", bound_ok, "bound tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4143_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "COEFFICIENT_ADOPTION_SELECTED",
            "ROUTE_SELECTED_NOT_SIGNED",
            "PHI_NOHAIR_DEMOTED_TO_BOUND_BACKSTOP",
            "REJECTED_BRANCH_BOUND_ROWS_FILLED",
            "NEXT_COEFFICIENT_BIRTH_CERTIFICATE_SELECTED",
        ]
    )
    add("VAL4143_7_decisions", "decisions record selected route, nonclaim, nohair demotion, bound rows and next birth certificate", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4143_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("route_selected") == "coefficient_adoption"
        and status[0].get("route_signed") == "False"
        and status[0].get("phi_nohair_demoted_to_bound") == "True"
        and status[0].get("bound_rows_filled") == "True"
    )
    add("VAL4143_8_status", "status records coefficient route selected, unsigned, nohair demoted and bounds filled", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4143_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4144-Y5-R2FR-tracefree-coefficient-adoption-birth-certificate-or-epsilon-bound.md"
    add("VAL4143_9_next_target", "next target is trace-free coefficient adoption birth certificate or epsilon bound", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4143_10_no_claim_flags", "all generated rows remain no-claim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4143*")) or any(FORMALIZATION.rglob("4143-Y5-R2FR*"))
    add(
        "VAL4143_11_scope",
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
    add("VAL4143_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4143_VALIDATION.csv"
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
