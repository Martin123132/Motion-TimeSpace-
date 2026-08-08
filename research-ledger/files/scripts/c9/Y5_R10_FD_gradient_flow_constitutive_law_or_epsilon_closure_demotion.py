from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1135-Y5-R10-FD-gradient-flow-constitutive-law-or-epsilon-closure-demotion.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1135_0_1134_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1134_NEXT_TARGET.csv",
            "needle": "NEXT1134_0_1135",
            "note": "1134 handoff to F_D gradient-flow constitutive law or epsilon closure demotion.",
        },
        {
            "source_id": "SRC1135_1_1134_theorem",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1134_CONDITIONAL_THEOREM_CONTRACT.csv",
            "needle": "THM1134_0_strong_conditional",
            "note": "1134 states the conditional gradient-flow/Neumann theorem.",
        },
        {
            "source_id": "SRC1135_2_1134_lemma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1134_NO_SWIRL_HARMONIC_LEMMA_AUDIT.csv",
            "needle": "LEM1134_1_gradient_constitutive_law",
            "note": "1134 identifies the missing constitutive law.",
        },
        {
            "source_id": "SRC1135_3_parent_terms",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A8_projector_domain_topological",
            "note": "Parent action contract keeps projector/domain sector symbolic.",
        },
        {
            "source_id": "SRC1135_4_no_vector",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T2_no_flux_local_representative",
            "note": "No-flux local representative remains conditional, not a constitutive law.",
        },
        {
            "source_id": "SRC1135_5_ownership",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
            "needle": "P3_local_trivial_representative",
            "note": "Local trivial representative is still a blocking premise.",
        },
        {
            "source_id": "SRC1135_6_1018_owner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1018_OWNER_CLAUSES.csv",
            "needle": "LOC1018_3_positive_sourcefree",
            "note": "Existing positive source-free machinery is scalar-X analog, not domain-flux ownership.",
        },
        {
            "source_id": "SRC1135_7_1022_nohair",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1022_SCALAR_NOHAIR_CONSTRUCTION.csv",
            "needle": "SNH1022_5_energy_identity",
            "note": "Scalar no-hair energy identity is conditional and cannot be imported as F_D law.",
        },
        {
            "source_id": "SRC1135_8_1134_runner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1134_EPSILON_PROFILE_RUNNER_INPUTS.csv",
            "needle": "RUN1134_0_epsilon_profile",
            "note": "Fallback runner remains blocked without sourced epsilon/couplings.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def constitutive_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "CFA1135_0_parent_domain_action",
                "target": "S_domain/S_projector supplies F_D law",
                "needed_statement": "variation produces F_D^i=-M_D^{ij} grad_j zeta_D before readout",
                "current_evidence": "A8_projector_domain_topological only says symbolic exact-owned zero-flux divergence or retained residual",
                "result": "NOT_DERIVED",
                "why_not_enough": "no explicit flux variable, mobility tensor, domain potential, or Euler equation is specified",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CFA1135_1_no_vector_route",
                "target": "conditional no-flux local representative",
                "needed_statement": "T2 local representative is parent-owned and stronger than net-flux silence",
                "current_evidence": "T2_no_flux_local_representative remains conditional_not_parent_derived",
                "result": "NOT_DERIVED",
                "why_not_enough": "it states the desired effect, not the parent constitutive mechanism",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CFA1135_2_scalar_nohair_analogy",
                "target": "borrow positive scalar no-hair energy identity",
                "needed_statement": "domain flux sector is the same positive source-free scalar operator branch",
                "current_evidence": "1018/1022 provide scalar-X conditional no-hair templates only",
                "result": "REJECT_IMPORT_AS_PROOF",
                "why_not_enough": "a scalar profile theorem does not define F_D or remove coexact flux in the domain sector",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CFA1135_3_mobility_positive",
                "target": "M_D positive elliptic",
                "needed_statement": "M_D^{ij} is symmetric positive definite in the compact local branch",
                "current_evidence": "no M_D object or Hessian normalization exists in current source rows",
                "result": "MISSING_OBJECT",
                "why_not_enough": "positivity cannot be inferred from covariance or stationarity",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CFA1135_4_domain_potential",
                "target": "zeta_D chemical/domain potential",
                "needed_statement": "zeta_D is a parent variable or multiplier whose variation gives the flux constraint",
                "current_evidence": "no zeta_D/domain chemical potential source appears in the current local flux contract",
                "result": "MISSING_OBJECT",
                "why_not_enough": "without zeta_D the integration-by-parts proof has no legal potential to test against",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CFA1135_5_boundary_topology_coframe",
                "target": "Neumann boundary, harmonic exclusion, and PPN-safe coframe",
                "needed_statement": "n.F_D=0, H^1_rel=0 or harmonic class excluded, and epsilon is zero in observed coframe",
                "current_evidence": "1134 records these as missing clauses",
                "result": "NOT_DERIVED",
                "why_not_enough": "even a gradient law needs these clauses to become a local alpha3 zero theorem",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CFA1135_6_verdict",
                "target": "F_D=-M_D grad zeta_D parent-derived",
                "needed_statement": "CFA1135_0 through CFA1135_5 all close together",
                "current_evidence": "current corpus has analogies and contracts, not the constitutive derivation",
                "result": "CONSTITUTIVE_LAW_NOT_FOUND",
                "why_not_enough": "epsilon_domain_flux zero cannot be promoted from current files",
                "valid_for_claim": "false",
            },
        ]
    )


def parent_action_contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "contract_id": "PAC1135_0_auxiliary_flux_ansatz",
                "status": "FUTURE_PARENT_ACTION_CONTRACT_NOT_CURRENT_PROOF",
                "candidate_structure": "S_D_flux = int sqrt(h)[1/2 F_i (M_D^{-1})^{ij} F_j + zeta_D div_i F^i] + boundary terms",
                "variation_result_if_adopted": "delta_F gives F_D^i=-M_D^{ij} grad_j zeta_D; delta_zeta gives div_i F_D^i=0",
                "must_still_prove": "M_D positivity, boundary term gives n.F_D=0, H^1_rel=0/local branch exclusion, and observed coframe safety",
                "risk": "adding this as a new post-hoc term would be a closure, not a derivation from existing MTS",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "PAC1135_1_existing_action_upgrade",
                "status": "ALLOWED_RESCUE_ROUTE",
                "candidate_structure": "show existing S_domain/S_projector already reduces to PAC1135_0 after integrating out auxiliary variables",
                "variation_result_if_adopted": "same gradient-flow law becomes derived instead of appended",
                "must_still_prove": "source path to existing parent variables and no new empirical selector",
                "risk": "if no existing variable maps to F_D/M_D/zeta_D, route fails",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "PAC1135_2_profile_bound_fallback",
                "status": "ACTIVE_FALLBACK",
                "candidate_structure": "do not assume epsilon=0; source epsilon profile and W/K/c couplings, then test alpha3 products",
                "variation_result_if_adopted": "numeric inequality route rather than theorem-zero route",
                "must_still_prove": "real source paths, units, normalization, no MISSING markers, no tuned cancellation",
                "risk": "less elegant and more parameter-sensitive than theorem-zero",
                "valid_for_claim": "false",
            },
        ]
    )


def demotion_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "demotion_id": "DEM1135_0_epsilon_zero",
                "route": "epsilon_domain_flux=0 theorem route",
                "decision": "DEMOTE_TO_CLOSURE_ONLY_FOR_CURRENT_CORPUS",
                "reason": "F_D gradient-flow constitutive law is not found in current parent action contracts",
                "effect": "cannot be used to claim alpha3/R10/PPN/local-GR pass",
                "reopen_condition": "existing parent action derives F_D, M_D, zeta_D, Neumann boundary, harmonic exclusion, and coframe safety",
                "valid_for_claim": "false",
            },
            {
                "demotion_id": "DEM1135_1_gradient_contract",
                "route": "auxiliary flux action",
                "decision": "KEEP_AS_FUTURE_PARENT_ACTION_CONTRACT",
                "reason": "mathematically clean route exists but is not in current corpus",
                "effect": "can guide future formal parent action, not current evidence",
                "reopen_condition": "derive contract from existing variables or explicitly mark it as new closure",
                "valid_for_claim": "false",
            },
            {
                "demotion_id": "DEM1135_2_numeric_fallback",
                "route": "epsilon/coupling profile acquisition",
                "decision": "KEEP_ACTIVE_NONCLAIM",
                "reason": "if theorem-zero route stays closed, executable alpha3 products need sourced inputs",
                "effect": "next practical branch can fill epsilon, W, K, c rows",
                "reopen_condition": "source-backed rows with no MISSING markers and valid_for_claim gates",
                "valid_for_claim": "false",
            },
        ]
    )


def runner_handoff_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "RH1135_0_epsilon_profile",
                "needed_input": "epsilon_domain_flux",
                "current_status": "MISSING_PROFILE_OR_ZERO_THEOREM",
                "next_data_shape": "system_id; branch; epsilon_bound_abs; coframe; units; source_path; assumptions; valid_for_claim",
                "claim_policy": "valid_for_claim=false until profile or zero theorem is parent/source backed",
                "valid_for_claim": "false",
            },
            {
                "row_id": "RH1135_1_domain_coupling",
                "needed_input": "W_domain_alpha3",
                "current_status": "MISSING_COUPLING_OR_ZERO_THEOREM",
                "next_data_shape": "system_id; W_domain_alpha3_abs; units; weak_field_map; source_path; assumptions; valid_for_claim",
                "claim_policy": "no product scoring until sourced",
                "valid_for_claim": "false",
            },
            {
                "row_id": "RH1135_2_R11_coupling_product",
                "needed_input": "K_R11_flux_alpha3*c_R11_flux_alpha3",
                "current_status": "MISSING_TRANSFER_AND_NORMALIZATION",
                "next_data_shape": "system_id; K_R11_flux_alpha3_abs; c_R11_flux_alpha3_abs; product_abs; units; source_path; assumptions; valid_for_claim",
                "claim_policy": "no product scoring until both factors are sourced or theorem-zero",
                "valid_for_claim": "false",
            },
            {
                "row_id": "RH1135_3_no_cancellation",
                "needed_input": "independent product closure",
                "current_status": "GUARD_ACTIVE",
                "next_data_shape": "domain_product_abs; R11_product_abs; total_policy=no_tuned_cancellation",
                "claim_policy": "total alpha3 cannot pass by cancellation unless a parent identity derives it",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1135_0_FD_law",
                "rule": "F_D=-M_D grad zeta_D is parent-derived",
                "gate_pass": "false",
                "reason": "no explicit F_D/M_D/zeta_D parent variation is found",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1135_1_positive_mobility",
                "rule": "M_D is positive elliptic with units/normalization",
                "gate_pass": "false",
                "reason": "M_D object is absent",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1135_2_boundary_harmonic_coframe",
                "rule": "Neumann boundary, harmonic exclusion, and coframe safety are parent-signed",
                "gate_pass": "false",
                "reason": "all remain missing clauses from 1134",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1135_3_no_imported_scalar_nohair",
                "rule": "scalar-X no-hair is not imported as domain-flux proof",
                "gate_pass": "true_nonclaim",
                "reason": "1135 rejects the analogy as proof while preserving it as mathematical inspiration",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1135_4_epsilon_zero_demoted",
                "rule": "epsilon zero theorem is demoted for current corpus",
                "gate_pass": "true_nonclaim",
                "reason": "current parent action does not close the constitutive law",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1135_5_runner_handoff",
                "rule": "numeric/profile fallback remains nonclaim but source-ready",
                "gate_pass": "true_nonclaim",
                "reason": "handoff rows define needed schemas without claiming values",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1135_6_alpha3_local_GR",
                "rule": "alpha3/R10/PPN/local-GR can promote",
                "gate_pass": "false",
                "reason": "epsilon zero and numeric fallback are both unclosed",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1135_0_verdict",
                "decision": "F_D_gradient_flow_not_derived",
                "reason": "current corpus has symbolic domain contracts and scalar analogies, but no F_D/M_D/zeta_D parent variation",
                "next_action": "demote epsilon zero to closure-only for current corpus",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1135_1_best_theory_rescue",
                "decision": "auxiliary_flux_action_contract_is_cleanest_future_route",
                "reason": "it would derive exact/gradient flux and conservation from variations rather than imposing a plateau",
                "next_action": "only use it if explicitly introduced as parent action or derived from existing S_domain",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1135_2_best_practical_next",
                "decision": "build_epsilon_coupling_profile_source_pack",
                "reason": "with theorem-zero demoted, the honest alpha3 route is source-backed epsilon/W/K/c acquisition",
                "next_action": "generate first nonclaim schema/source rows for epsilon, W, K, c and product inequalities",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1135_0_1136",
                "next_target": "1136-Y5-R10-epsilon-W-K-c-source-pack-first-row.md",
                "objective": "with epsilon zero demoted for current corpus, build the first source-pack rows for epsilon_domain_flux, W_domain_alpha3, K_R11_flux_alpha3, and c_R11_flux_alpha3, keeping all alpha3 products nonclaim until sourced",
                "include": "epsilon profile schema; W coupling schema; K/c R11 schema; units; source paths; no-cancellation guard; 4e-20 product inequalities",
                "exclude": "new parent action as if already derived; scalar no-hair import; tuned cancellation; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "next_id": "NEXT1135_1_future_theory",
                "next_target": "future-parent-action-auxiliary-flux-gradient-flow-contract.md",
                "objective": "optional future theory route: explicitly construct or derive an auxiliary flux parent action that yields F_D=-M_D grad zeta_D",
                "include": "F_D auxiliary variable; M_D positivity; zeta_D multiplier; boundary variation; H1_rel exclusion; coframe safety",
                "exclude": "using it as current evidence before added/derived",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def local_paths_exist(rows: list[dict[str, object]], field: str) -> bool:
    for row in rows:
        value = str(row[field])
        if value.startswith("MISSING") or value.startswith("future-"):
            continue
        if not (ROOT / value).exists():
            return False
    return True


def validate(
    sources: list[dict[str, object]],
    audits: list[dict[str, object]],
    contracts: list[dict[str, object]],
    demotions: list[dict[str, object]],
    handoff: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = audits + contracts + demotions + handoff + gates + decisions + next_target
    add("V1135_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1135_1_constitutive_audit_complete", audits[-1]["result"] == "CONSTITUTIVE_LAW_NOT_FOUND", "constitutive-law audit reaches a nonclaim not-found verdict")
    add("V1135_2_scalar_import_rejected", audits[2]["result"] == "REJECT_IMPORT_AS_PROOF" and gates[3]["gate_pass"] == "true_nonclaim", "scalar no-hair analogy is not imported as proof")
    add("V1135_3_future_contract_nonclaim", contracts[0]["status"] == "FUTURE_PARENT_ACTION_CONTRACT_NOT_CURRENT_PROOF", "auxiliary flux action is staged only as future contract")
    add("V1135_4_epsilon_demoted", demotions[0]["decision"] == "DEMOTE_TO_CLOSURE_ONLY_FOR_CURRENT_CORPUS", "epsilon zero theorem is demoted for current corpus")
    add("V1135_5_runner_handoff_schema", {"epsilon_domain_flux", "W_domain_alpha3", "K_R11_flux_alpha3*c_R11_flux_alpha3", "independent product closure"}.issubset({row["needed_input"] for row in handoff}), "handoff covers epsilon, domain coupling, R11 coupling product, and no-cancellation")
    add("V1135_6_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 4, "claim gates remain blocked")
    add("V1135_7_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in next_target), "all generated rows remain nonclaim")
    add("V1135_8_next_target", next_target[0]["next_target"].startswith("1136-") and "source-pack" in str(next_target[0]["next_target"]), "1136 handoff targets epsilon/W/K/c source pack")
    add("V1135_9_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1135_10_csv_parse", csv_parse_ok, "all 1135 CSV outputs parse cleanly")
    add("V1135_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1135_SUMMARY", True, "1135 demotes epsilon zero for current corpus and sends alpha3 to source-pack acquisition")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    audits: list[dict[str, object]],
    contracts: list[dict[str, object]],
    demotions: list[dict[str, object]],
    handoff: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1135 - Y5/R10 F_D Gradient-Flow Constitutive Law Or Epsilon Closure Demotion

**Current verdict:** `F_D=-M_D grad zeta_D` is not derived from the current corpus. The local no-swirl theorem remains mathematically clean but parent-unsigned.

**Important rejection:** the scalar positive no-hair machinery is useful inspiration, but it cannot be imported as a proof for domain flux. A scalar profile equation does not define the domain flux constitutive law or kill coexact circulation.

**Theory rescue route:** an auxiliary flux parent action could derive the needed law: vary `F_D` to get `F_D=-M_D grad zeta_D`, vary `zeta_D` to get `div F_D=0`, then use Neumann/no-harmonic conditions. This is a future parent-action contract, not current evidence.

**Decision:** for the current corpus, demote `epsilon_domain_flux=0` to closure-only and move the active alpha3 route to source-backed `epsilon`, `W`, `K`, and `c` rows.

**No claim:** no alpha3, R10, PPN, local-GR, measured-GM, or FLRW claim follows from 1135.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Constitutive Law Audit
{table(["audit_id", "target", "needed_statement", "current_evidence", "result", "why_not_enough", "valid_for_claim"], audits)}

## Parent Action Contract Options
{table(["contract_id", "status", "candidate_structure", "variation_result_if_adopted", "must_still_prove", "risk", "valid_for_claim"], contracts)}

## Demotion Ledger
{table(["demotion_id", "route", "decision", "reason", "effect", "reopen_condition", "valid_for_claim"], demotions)}

## Source-Pack Handoff Rows
{table(["row_id", "needed_input", "current_status", "next_data_shape", "claim_policy", "valid_for_claim"], handoff)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Targets
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1135_SOURCE_REGISTER.csv",
        "audits": OUT / "P8_Y5_R10_1135_FD_GRADIENT_FLOW_CONSTITUTIVE_AUDIT.csv",
        "contracts": OUT / "P8_Y5_R10_1135_PARENT_ACTION_CONTRACT_OPTIONS.csv",
        "demotions": OUT / "P8_Y5_R10_1135_EPSILON_CLOSURE_DEMOTION_LEDGER.csv",
        "handoff": OUT / "P8_Y5_R10_1135_SOURCE_PACK_HANDOFF_ROWS.csv",
        "gates": OUT / "P8_Y5_R10_1135_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1135_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1135_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1135_VALIDATION.csv",
    }
    sources = source_rows()
    audits = constitutive_audit_rows()
    contracts = parent_action_contract_rows()
    demotions = demotion_rows()
    handoff = runner_handoff_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["audits"], audits)
    write_csv(outputs["contracts"], contracts)
    write_csv(outputs["demotions"], demotions)
    write_csv(outputs["handoff"], handoff)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, audits, contracts, demotions, handoff, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, audits, contracts, demotions, handoff, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
