from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1349"
TITLE = "1349-Y5-R10-RAB-KMTS-trace-projection-owner-or-memory-closure-declaration"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
KMTS_OWNER_PATH = OUT_DIR / f"{PACK_ID}_KMTS_TRACE_PROJECTION_OWNER_ATTEMPT.csv"
RESPONSE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_GAMMA_KHAT_RESPONSE_AUDIT.csv"
CLOSURE_DECLARATION_PATH = OUT_DIR / f"{PACK_ID}_MEMORY_CLOSURE_DECLARATION.csv"
RESIDUAL_BRANCH_PATH = OUT_DIR / f"{PACK_ID}_FINITE_BMEM_RESIDUAL_BRANCH.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1349_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def falsey(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "n", ""}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not falsey(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not falsey(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1349*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1349_0_1348_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1348_NEXT_TARGET.csv",
            "needle": "NEXT1348_0_1349",
            "role": "selected 1349 target",
        },
        {
            "source_id": "SRC1349_1_1348_Bmem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1348_BMEM_EXTREMUM_TEST.csv",
            "needle": "BEXT1348_5_verdict",
            "role": "B_mem parent ownership failure",
        },
        {
            "source_id": "SRC1349_2_826_Ward",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_WARD_BIANCHI_AUDIT.csv",
            "needle": "W826_3_Khat_required",
            "role": "Ward/Bianchi Khat requirement",
        },
        {
            "source_id": "SRC1349_3_827_Khat",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_827_KHAT_RESPONSE_CONTRACT.csv",
            "needle": "KH827_3_Khat_owner_contract",
            "role": "Khat owner contract",
        },
        {
            "source_id": "SRC1349_4_828_Khat_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_828_KHAT_OWNER_AUDIT.csv",
            "needle": "KO828_1_baseline_without_lock",
            "role": "Khat owner audit",
        },
        {
            "source_id": "SRC1349_5_GK_match",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            "needle": "MA515_1_Khat_metric_response",
            "role": "Gamma/Khat metric response match audit",
        },
        {
            "source_id": "SRC1349_6_GK_passfail",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_PASS_FAIL.csv",
            "needle": "PF515_2_Khat_response_found",
            "role": "Gamma/Khat pass-fail gate",
        },
        {
            "source_id": "SRC1349_7_GK_contract",
            "local_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
            "needle": "GK513_0_action_existence",
            "role": "Gamma/Khat first variation contract",
        },
        {
            "source_id": "SRC1349_8_GK_demote",
            "local_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
            "needle": "QR513_0_nonvariational_stress",
            "role": "residual/demotion path",
        },
        {
            "source_id": "SRC1349_9_1284_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1284_GAMMA_KHAT_OWNER_EXTRACTION_AUDIT.csv",
            "needle": "GKO1284_5_verdict",
            "role": "Gamma/Khat owner extraction verdict",
        },
        {
            "source_id": "SRC1349_10_1348_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1348_VALIDATION.csv",
            "needle": "VAL1348_10_overall",
            "role": "1348 pass gate",
        },
    ]
    source_register: list[dict[str, object]] = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    kmts_owner = [
        {
            "attempt_id": "KMTS1349_0_required_object",
            "needed_for_theorem": "K_MTS-owned Gamma_eff trace projection",
            "required_statement": "Gamma_eff is obtained from a local covariant parent scalar density or trace projection of K_MTS, not chosen as a post-hoc ansatz.",
            "current_evidence": "826 gives a Gamma_eff ansatz and says trace projection must be derived from K_MTS",
            "status": "TARGET_DEFINED_NOT_DERIVED",
            "consequence": "F1=0 remains conditional calculus only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "KMTS1349_1_scalar_density_owner",
            "needed_for_theorem": "Gamma_eff scalar-density owner",
            "required_statement": "Gamma_eff(g,Phi,nablaPhi,...) has units, metric dependence, and parent action placement.",
            "current_evidence": "MA515_0 and GKO1284_0 report generic/contract-only Gamma_eff with no current formula",
            "status": "NOT_FOUND",
            "consequence": "no parent variation can certify the trace projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "KMTS1349_2_Khat_metric_response",
            "needed_for_theorem": "K_hat is metric response of the same density",
            "required_statement": "K_hat^{mu nu}=metric variation response of sqrt(-g)Gamma_eff under a fixed sign convention.",
            "current_evidence": "MA515_1 and PF515_2 fail; KH827 rejects setting div Khat by definition",
            "status": "NOT_FOUND",
            "consequence": "cannot infer q_loc cancellation from Gamma_eff alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "KMTS1349_3_Ward_closure",
            "needed_for_theorem": "Ward identity closes q_loc",
            "required_statement": "all fields building Gamma_eff/Khat are varied and on shell, including X_B ancestors, bath/open-system variables, and boundary terms.",
            "current_evidence": "W826_0 possible only for full variable list; W826_1/2 fail for external spurion/open-system memory",
            "status": "NOT_DERIVED",
            "consequence": "external X_B/L_cg gradients and bath exchange remain source terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "KMTS1349_4_response_template",
            "needed_for_theorem": "response-field repair path",
            "required_statement": "Gamma_eff and Khat are conjugate scalar/tensor projections of one parent response/displacement field.",
            "current_evidence": "MA515_2 and GKO1284_1 mark this as promising but not current-MTS-derived",
            "status": "PROMISING_TEMPLATE_NOT_DERIVED",
            "consequence": "possible future derivation route, not current claim support",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "KMTS1349_5_verdict",
            "needed_for_theorem": "B_mem=0 as theorem",
            "required_statement": "KMTS1349_0 through KMTS1349_4 close with source paths",
            "current_evidence": "scalar-density owner, Khat response, Ward closure, and response template are not derived",
            "status": "KMTS_TRACE_PROJECTION_OWNER_NOT_DERIVED",
            "consequence": "B_mem=0 cannot be promoted beyond private closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    response_audit = [
        {
            "audit_id": "RESP1349_0_do_not_define_Khat",
            "issue": "setting div Khat=nabla Gamma_eff by definition",
            "evidence": "KH827_0 rejects this as hiding the local-GR problem in a counterterm",
            "decision": "FORBIDDEN_AS_THEOREM",
            "residual_policy": "derive Khat from parent variation or carry q_loc residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "RESP1349_1_scalar_memory_stress",
            "issue": "using scalar memory Hilbert stress as Khat",
            "evidence": "KH827_1 says scalar-gradient anisotropic stress does not automatically cancel baseline X_B/L_cg drift",
            "decision": "INSUFFICIENT_BY_ITSELF",
            "residual_policy": "include X_B ancestors, L_cg variation, bath/source stress, and boundary data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "RESP1349_2_external_profiles",
            "issue": "treating X_B/L_cg as external",
            "evidence": "W826_1 and KH827_2 flag external profiles as spurion sources",
            "decision": "FAILS_PARENT_GATE",
            "residual_policy": "derive profiles from covariant fields or bound spurion response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "RESP1349_3_metric_response_contract",
            "issue": "Gamma/Khat match",
            "evidence": "PF515_1 and PF515_2 fail for current corpus",
            "decision": "MATCH_NOT_FOUND",
            "residual_policy": "fallback to residual branch QR513_0..QR513_4",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_declaration = [
        {
            "declaration_id": "MDECL1349_0_theorem_branch",
            "branch": "theorem route",
            "statement": "B_mem=0 is theorem-credit only if Gamma_eff trace projection is derived from K_MTS/parent variation, R(m;X_B) and m_L are parent-owned, and Khat/Ward/boundary response closes.",
            "current_status": "NOT_AVAILABLE_CURRENT_CORPUS",
            "allowed_use": "future target only",
            "forbidden_use": "cannot support local GR, R10, PPN, or no-hair claim now",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "declaration_id": "MDECL1349_1_private_closure_branch",
            "branch": "private closure route",
            "statement": "One may privately assume the 826 Gamma_eff projection and m_L extremum, giving B_mem=0 as a closure axiom for algebra development.",
            "current_status": "PRIVATE_CLOSURE_ONLY",
            "allowed_use": "internal derivation scaffolding clearly labelled closure",
            "forbidden_use": "must not be presented as derived or used to pass local-GR/R10/PPN gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "declaration_id": "MDECL1349_2_default_residual_branch",
            "branch": "finite residual route",
            "statement": "Absent the K_MTS owner, the disciplined default is to retain B_mem as finite symbolic residual input.",
            "current_status": "DEFAULT_NONCLAIM_PUBLIC_DISCIPLINE",
            "allowed_use": "source/units/bound acquisition and future runner preparation",
            "forbidden_use": "do not infer B_mem=0 from missing source rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    residual_branch = [
        {
            "residual_id": "BMR1349_0_symbolic_input",
            "symbol": "B_mem",
            "meaning": "curvature-linear memory vertex in the finite memory branch",
            "equation": "(-Z_mem nabla^2 + M2_mem) delta m = B_mem R_obs + C_mem T + J_mem + boundary",
            "required_for_execution": "units; parent source path or bound; branch convention; source/test normalization; R10/PPN projection",
            "current_status": "SYMBOLIC_NONCLAIM_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "BMR1349_1_q_loc_policy",
            "symbol": "q_loc^nu",
            "meaning": "local residual vector if Gamma/Khat does not close",
            "equation": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu Khat^{mu nu})",
            "required_for_execution": "Gamma_eff owner or finite residual components; Khat response; P_loc owner; boundary flux",
            "current_status": "RESIDUAL_BRANCH_REQUIRED_IF_OWNER_FAILS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gate = [
        {
            "gate_id": "GATE1349_0_KMTS_owner",
            "claim": "K_MTS owns the Gamma_eff trace projection",
            "allowed_if": "source-backed scalar density, Khat metric response, Ward closure, and boundary terms all pass",
            "current_status": "BLOCKED",
            "reason": "no live Gamma_eff scalar-density owner or Khat metric-response derivation found",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1349_1_Bmem_zero",
            "claim": "B_mem=0 is derived",
            "allowed_if": "K_MTS trace projection owner plus R/m_L branch owner plus response locks pass",
            "current_status": "BLOCKED",
            "reason": "F1=0 is conditional but parent ownership fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1349_2_local_GR",
            "claim": "local q_loc/local-GR silence follows",
            "allowed_if": "B_mem zero, C/J/boundary silence, Khat response, and P_loc owner all close",
            "current_status": "BLOCKED",
            "reason": "q_loc residual branch remains required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1349_0_owner_result",
            "decision": "K_MTS trace-projection owner is not derived",
            "because": "Gamma_eff scalar-density owner and Khat metric-response derivation are absent in current source trail",
            "effect": "B_mem=0 cannot receive theorem credit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1349_1_closure_result",
            "decision": "B_mem=0 is now explicitly private closure if used",
            "because": "the calculus route is clean but not parent-owned",
            "effect": "future documents must label the branch as closure or keep finite B_mem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1349_2_default_result",
            "decision": "finite B_mem residual is the disciplined default for public/nonclaim work",
            "because": "claim gates require derived ownership, not missing-source silence",
            "effect": "next work should prepare finite B_mem/q_loc residual acquisition or try response-field construction separately",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1349_0_1350",
            "target_file": "1350-Y5-R10-RAB-finite-Bmem-and-qloc-residual-runner-contract.md",
            "target_script": "scripts/Y5_R10_RAB_finite_Bmem_and_qloc_residual_runner_contract.py",
            "task": "turn the finite B_mem/q_loc branch into a strict nonclaim runner contract with required units, source paths, projection owner, and R10/PPN/local residual observables",
            "success_condition": "a runnable schema rejecting all rows until B_mem, Gamma_eff, Khat, P_loc, boundary, and source/test maps are source-backed",
            "do_not": "do not score symbolic-only B_mem; do not revive B_mem=0 theorem without K_MTS owner evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables = [
        source_register,
        kmts_owner,
        response_audit,
        closure_declaration,
        residual_branch,
        claim_gate,
        decision_ledger,
        next_target,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(KMTS_OWNER_PATH, kmts_owner)
    write_csv(RESPONSE_AUDIT_PATH, response_audit)
    write_csv(CLOSURE_DECLARATION_PATH, closure_declaration)
    write_csv(RESIDUAL_BRANCH_PATH, residual_branch)
    write_csv(CLAIM_GATE_PATH, claim_gate)
    write_csv(DECISION_PATH, decision_ledger)
    write_csv(NEXT_PATH, next_target)

    sources_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in source_register)
    owner_not_derived = kmts_owner[-1]["status"] == "KMTS_TRACE_PROJECTION_OWNER_NOT_DERIVED"
    response_match_missing = any(row["decision"] == "MATCH_NOT_FOUND" for row in response_audit)
    closure_declared = len(closure_declaration) == 3 and closure_declaration[1]["current_status"] == "PRIVATE_CLOSURE_ONLY"
    residual_retained = residual_branch[0]["current_status"] == "SYMBOLIC_NONCLAIM_RETAINED"
    claims_blocked = all(row["current_status"] == "BLOCKED" for row in claim_gate)
    formalization_hits = generated_inside_formalization()
    overall_ok = (
        sources_ok
        and owner_not_derived
        and response_match_missing
        and closure_declared
        and residual_retained
        and claims_blocked
        and all_nonclaim(tables)
        and len(formalization_hits) == 0
    )

    validation = [
        validation_row(
            "VAL1349_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1349_1_KMTS_owner_not_derived",
            "K_MTS trace projection owner is not promoted",
            owner_not_derived,
            kmts_owner[-1]["status"],
        ),
        validation_row(
            "VAL1349_2_response_match_missing",
            "Gamma/Khat metric-response match remains missing",
            response_match_missing,
            "PF515/MA515/GKO1284 fail owner extraction",
        ),
        validation_row(
            "VAL1349_3_closure_declared",
            "B_mem=0 private closure declaration is explicit",
            closure_declared,
            "theorem, private closure, and finite residual branches separated",
        ),
        validation_row(
            "VAL1349_4_residual_retained",
            "finite B_mem residual branch is retained as default nonclaim discipline",
            residual_retained,
            residual_branch[0]["current_status"],
        ),
        validation_row(
            "VAL1349_5_claims_blocked",
            "K_MTS owner, B_mem zero, and local-GR claims remain blocked",
            claims_blocked,
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in claim_gate),
        ),
        validation_row(
            "VAL1349_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1349_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_hits) == 0,
            f"formalization_generated_output_count={len(formalization_hits)}",
        ),
        validation_row(
            "VAL1349_8_next_target_1350",
            "next target routes to finite Bmem/q_loc residual runner contract",
            next_target[0]["next_id"] == "NEXT1349_0_1350",
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1349_9_overall",
            "overall 1349 validation",
            overall_ok,
            "1349 demotes B_mem=0 to private closure unless K_MTS owner is later derived and retains finite B_mem residual by default",
        ),
    ]
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1349 does not derive the `K_MTS` trace-projection owner. The `F1=0` / `B_mem=0` route remains mathematically clean but only conditional; it is not a theorem of current MTS.

**Main progress:** the branch is now officially separated into three lanes: theorem route, private closure route, and finite residual route. The disciplined default for nonclaim/public work is finite symbolic `B_mem` and `q_loc` residual until `Gamma_eff`, `K_hat`, and `P_loc` are parent-owned.

**Decision:** move to `1350`: build the finite `B_mem/q_loc` residual runner contract. No local-GR/R10/PPN claim is made, and `B_mem=0` cannot be used as more than private closure without new `K_MTS` owner evidence.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## KMTS Trace Projection Owner Attempt
{markdown_table(kmts_owner, ["attempt_id", "needed_for_theorem", "required_statement", "current_evidence", "status", "consequence", "valid_for_claim", "claim_allowed"])}

## Gamma Khat Response Audit
{markdown_table(response_audit, ["audit_id", "issue", "evidence", "decision", "residual_policy", "valid_for_claim", "claim_allowed"])}

## Memory Closure Declaration
{markdown_table(closure_declaration, ["declaration_id", "branch", "statement", "current_status", "allowed_use", "forbidden_use", "valid_for_claim", "claim_allowed"])}

## Finite Bmem Residual Branch
{markdown_table(residual_branch, ["residual_id", "symbol", "meaning", "equation", "required_for_execution", "current_status", "valid_for_claim", "claim_allowed"])}

## Claim Gate
{markdown_table(claim_gate, ["gate_id", "claim", "allowed_if", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision_ledger, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
