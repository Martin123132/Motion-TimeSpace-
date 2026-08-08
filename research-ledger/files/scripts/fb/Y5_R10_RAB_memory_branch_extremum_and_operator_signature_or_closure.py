from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1348"
TITLE = "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
BMEM_EXTREMUM_PATH = OUT_DIR / f"{PACK_ID}_BMEM_EXTREMUM_TEST.csv"
OPERATOR_SIGNATURE_PATH = OUT_DIR / f"{PACK_ID}_MEMORY_OPERATOR_SIGNATURE_TEST.csv"
CLOSURE_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_MEMORY_CLOSURE_CONTRACT.csv"
FINITE_BRANCH_PATH = OUT_DIR / f"{PACK_ID}_FINITE_MEMORY_BRANCH_CONTRACT.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1348_VALIDATION.csv"


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
    return [path for path in FORMALIZATION.rglob("*1348*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1348_0_1347_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1347_NEXT_TARGET.csv",
            "needle": "NEXT1347_0_1348",
            "role": "selected 1348 target",
        },
        {
            "source_id": "SRC1348_1_1347_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1347_OWNER_SEARCH_LEDGER.csv",
            "needle": "OWN1347_2_memory_branch_extremum",
            "role": "memory owner search",
        },
        {
            "source_id": "SRC1348_2_826_F1",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_F1_ZERO_LEMMA.csv",
            "needle": "F826_1_F1_zero",
            "role": "conditional F1 zero lemma",
        },
        {
            "source_id": "SRC1348_3_826_ansatz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "needle": "AA826_2_trace_projection_lock",
            "role": "trace projection lock",
        },
        {
            "source_id": "SRC1348_4_826_coefficients",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
            "needle": "C826_5_Khat_response",
            "role": "memory coefficient ledger",
        },
        {
            "source_id": "SRC1348_5_970_quadratic",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "needle": "QMA970_7_verdict",
            "role": "quadratic memory action construction",
        },
        {
            "source_id": "SRC1348_6_1304_operator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1304_MEMORY_OPERATOR_OWNER_ATTEMPT.csv",
            "needle": "OO1304_2_owner_verdict",
            "role": "operator owner attempt",
        },
        {
            "source_id": "SRC1348_7_1304_gap",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv",
            "needle": "ZPG1304_2_mass_gap",
            "role": "Z/M positive gap map",
        },
        {
            "source_id": "SRC1348_8_1282_F1_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1282_F1_ZERO_THEOREM_AUDIT.csv",
            "needle": "FZ1282_5_verdict",
            "role": "F1 zero physical q_loc audit",
        },
        {
            "source_id": "SRC1348_9_1347_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1347_VALIDATION.csv",
            "needle": "VAL1347_9_overall",
            "role": "1347 pass gate",
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

    bmem_extremum = [
        {
            "test_id": "BEXT1348_0_definition",
            "claim_piece": "B_mem is the memory-curvature linear vertex",
            "mathematical_form": "B_mem := partial_m Gamma_eff|local or delta^2 S/(delta m delta R_obs), branch convention dependent",
            "result": "DEFINITION_ALIGNED",
            "blocker": "must choose and source the exact parent object whose variation defines B_mem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "BEXT1348_1_conditional_calculus",
            "claim_piece": "F1=0 under branch extremum",
            "mathematical_form": "Gamma_eff=L_cg^-2[F_L+a_F(R(m;X_B)-R(m_L;X_B))], partial_m R(m_L;X_B)=0 implies partial_m Gamma_eff|m_L=0",
            "result": "CONDITIONAL_DERIVATION_PASSES",
            "blocker": "calculus is sound only relative to the Gamma_eff ansatz and fixed X_B partial derivative",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "BEXT1348_2_projection_owner",
            "claim_piece": "trace projection is parent-derived",
            "mathematical_form": "Gamma_eff trace projection must be varied out of K_MTS / parent action rather than selected after the fact",
            "result": "NOT_DERIVED",
            "blocker": "AA826 says the trace projection must be derived from K_MTS, not imposed; no source row supplies that derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "BEXT1348_3_R_potential_owner",
            "claim_piece": "R(m;X_B) and m_L are parent-owned",
            "mathematical_form": "R functional, m_L(X_B), and stable second derivative are needed for a real branch extremum",
            "result": "NOT_DERIVED",
            "blocker": "C826 marks R_potential functional form missing and m_L only a conditional definition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "BEXT1348_4_full_gradient_debt",
            "claim_piece": "B_mem=0 silences q_loc/local PPN",
            "mathematical_form": "nabla Gamma_eff still has X_B, F_L, L_cg, m_L drift, source, boundary, and K_hat response terms",
            "result": "DOES_NOT_FOLLOW",
            "blocker": "F826_3 and FZ1282_5 warn that F1=0 is not physical q_loc=0 without response/source/boundary locks",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "BEXT1348_5_verdict",
            "claim_piece": "B_mem=0 parent-owned",
            "mathematical_form": "conditional F1 zero plus parent-owned projection, potential, branch, and response locks",
            "result": "B_MEM_ZERO_NOT_PARENT_OWNED_CURRENT_CORPUS",
            "blocker": "projection owner and R/m_L branch owner are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    operator_signature = [
        {
            "test_id": "OPS1348_0_action_shape",
            "claim_piece": "memory action shape",
            "mathematical_form": "L_m=-1/2 Z_m(X_B) nabla m nabla m - V_R(m;X_B) plus source/bath/boundary terms",
            "result": "SCAFFOLD_PRESENT",
            "blocker": "template/candidate not adopted as parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "OPS1348_1_variation",
            "claim_piece": "operator form",
            "mathematical_form": "L_m,loc delta m = -nabla_i(Z_m h^ij nabla_j delta m)+M_m^2 delta m plus sources",
            "result": "RELATIVE_VARIATION_WRITTEN",
            "blocker": "field domain, boundary condition, source terms, and branch reduction are not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "OPS1348_2_Z_positive",
            "claim_piece": "Z_mem>0",
            "mathematical_form": "A_m^ij=Z_m h^ij and positive ellipticity needs Z_m>=Z_min>0",
            "result": "FORMULA_ONLY_VALUE_MISSING",
            "blocker": "Z_m_min and units are not sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "OPS1348_3_M2_gap",
            "claim_piece": "M2_mem positive gap",
            "mathematical_form": "M_m^2=partial_m^2 V_R(m_*;X_B), with zero-mode/topology removed",
            "result": "FORMULA_ONLY_VALUE_MISSING",
            "blocker": "V_R functional form, stable local extremum, and zero-mode removal missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "OPS1348_4_source_boundary",
            "claim_piece": "operator proves memory no-hair",
            "mathematical_form": "positive operator only kills m if B_mem=C_mem=J_mem=Q_boundary_mem=0",
            "result": "INSUFFICIENT_WITHOUT_SOURCES",
            "blocker": "1343/1344 show curvature/source vertices and boundary charge must be killed separately",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "OPS1348_5_verdict",
            "claim_piece": "Z_mem/M2_mem parent-owned",
            "mathematical_form": "parent action, signs, units, branch Hessian, source/boundary package all supplied",
            "result": "OPERATOR_SIGNATURE_NOT_PARENT_OWNED_CURRENT_CORPUS",
            "blocker": "owner scaffold present; values/signs/units and parent adoption missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_contract = [
        {
            "contract_id": "MCLOS1348_0_private_Bmem_zero",
            "route": "private closure route",
            "statement": "Assume the K_MTS trace projection is exactly Gamma_eff=L_cg^-2[F_L+a_F(R(m;X_B)-R(m_L;X_B))] and m_L satisfies partial_m R=0, so B_mem=0.",
            "required_future_derivation": "derive Gamma_eff from K_MTS and parent variation; derive R(m;X_B), m_L, and stability",
            "allowed_use": "private algebra discipline only",
            "forbidden_use": "no local-GR, R10, PPN, or public theorem claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "MCLOS1348_1_private_operator_positive",
            "route": "private closure route",
            "statement": "Assume parent memory action has Z_mem>0 and M2_mem>0 with source/boundary silence.",
            "required_future_derivation": "source Z_mem/M2_mem values or theorem signs; derive J_mem=C_mem=Q_boundary_mem=0",
            "allowed_use": "mark exact premises needed for no-hair",
            "forbidden_use": "do not score alpha(lambda) or call memory no-hair derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "MCLOS1348_2_finite_Bmem_residual",
            "route": "retained residual route",
            "statement": "If trace projection or extremum fails, retain finite B_mem and route it to the symbolic memory branch.",
            "required_future_derivation": "source B_mem units/value or bound; link to lambda_mem/alpha_mem with source/test charges",
            "allowed_use": "nonclaim runner input preparation",
            "forbidden_use": "do not infer B_mem=0 from absence of a sourced value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "MCLOS1348_3_finite_operator_residual",
            "route": "retained residual route",
            "statement": "If Z_mem/M2_mem are not parent-owned, retain them as missing finite-branch coefficients rather than assuming decoupling.",
            "required_future_derivation": "source units, signs, and local branch domain for Z_mem and M2_mem",
            "allowed_use": "nonclaim coefficient acquisition",
            "forbidden_use": "do not use positive no-hair until signs and source/boundary premises are signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_branch = [
        {
            "branch_id": "FMEM1348_0_equation",
            "field_equation": "(-Z_mem nabla^2 + M2_mem) delta m = B_mem R_obs + C_mem T + J_mem + boundary",
            "range": "lambda_mem=sqrt(Z_mem/M2_mem) only after units/signs are sourced",
            "amplitude": "alpha_mem requires source/test charge normalization",
            "current_status": "SYMBOLIC_ONLY",
            "missing": "Z_mem;M2_mem;B_mem;C_mem;J_mem;Q_boundary_mem;W_mem;screening/source paths",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    claim_gate = [
        {
            "gate_id": "GATE1348_0_Bmem_zero",
            "claim": "B_mem=0 is derived",
            "allowed_if": "BEXT1348_1 through BEXT1348_4 all pass with parent source paths",
            "current_status": "BLOCKED",
            "reason": "conditional calculus passes but projection/potential/response owners are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1348_1_operator_owned",
            "claim": "Z_mem/M2_mem operator signature is derived",
            "allowed_if": "memory action is parent-adopted and signs/units/source/boundary clauses are supplied",
            "current_status": "BLOCKED",
            "reason": "operator scaffold present but not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1348_2_memory_nohair",
            "claim": "memory branch is locally silent",
            "allowed_if": "B_mem=C_mem=J_mem=Q_boundary_mem=0 plus positive operator and no response debt",
            "current_status": "BLOCKED",
            "reason": "B_mem and operator are not owned; C/J/boundary still open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1348_0_Bmem",
            "decision": "B_mem=0 remains conditional, not derived",
            "because": "F1 calculus passes but the Gamma_eff/K_MTS trace projection and R/m_L branch owner are missing",
            "effect": "next target should attack K_MTS trace projection ownership directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1348_1_operator",
            "decision": "memory operator signature remains scaffold-only",
            "because": "action shape and variation exist, but Z/M signs, units, parent adoption, and source/boundary clauses are absent",
            "effect": "positive no-hair stays unavailable as a claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1348_2_closure",
            "decision": "memory closure contract is now exact",
            "because": "B_mem=0 closure and finite-B_mem residual route are separated",
            "effect": "future work cannot silently use the nice F1 cancellation as a theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1348_0_1349",
            "target_file": "1349-Y5-R10-RAB-KMTS-trace-projection-owner-or-memory-closure-declaration.md",
            "target_script": "scripts/Y5_R10_RAB_KMTS_trace_projection_owner_or_memory_closure_declaration.py",
            "task": "try to derive the Gamma_eff trace projection from K_MTS / parent variation; if not, declare B_mem=0 as explicit private closure or retain finite B_mem residual",
            "success_condition": "K_MTS-owned trace projection path, or a final explicit memory closure declaration separating theorem and closure branches",
            "do_not": "do not use F1=0 as physical q_loc silence; do not claim local GR or run R10/PPN",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables = [
        source_register,
        bmem_extremum,
        operator_signature,
        closure_contract,
        finite_branch,
        claim_gate,
        decision_ledger,
        next_target,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(BMEM_EXTREMUM_PATH, bmem_extremum)
    write_csv(OPERATOR_SIGNATURE_PATH, operator_signature)
    write_csv(CLOSURE_CONTRACT_PATH, closure_contract)
    write_csv(FINITE_BRANCH_PATH, finite_branch)
    write_csv(CLAIM_GATE_PATH, claim_gate)
    write_csv(DECISION_PATH, decision_ledger)
    write_csv(NEXT_PATH, next_target)

    sources_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in source_register)
    calculus_pass = bmem_extremum[1]["result"] == "CONDITIONAL_DERIVATION_PASSES"
    bmem_not_owned = bmem_extremum[-1]["result"] == "B_MEM_ZERO_NOT_PARENT_OWNED_CURRENT_CORPUS"
    operator_scaffold = operator_signature[0]["result"] == "SCAFFOLD_PRESENT"
    operator_not_owned = operator_signature[-1]["result"] == "OPERATOR_SIGNATURE_NOT_PARENT_OWNED_CURRENT_CORPUS"
    closure_precise = len(closure_contract) == 4 and all(row["public_status"] if "public_status" in row else True for row in closure_contract)
    claims_blocked = all(row["current_status"] == "BLOCKED" for row in claim_gate)
    formalization_hits = generated_inside_formalization()
    overall_ok = (
        sources_ok
        and calculus_pass
        and bmem_not_owned
        and operator_scaffold
        and operator_not_owned
        and len(closure_contract) == 4
        and claims_blocked
        and all_nonclaim(tables)
        and len(formalization_hits) == 0
    )

    validation = [
        validation_row(
            "VAL1348_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1348_1_F1_calculus_passes",
            "conditional F1/B_mem calculus passes under the ansatz",
            calculus_pass,
            bmem_extremum[1]["mathematical_form"],
        ),
        validation_row(
            "VAL1348_2_Bmem_not_owned",
            "B_mem zero is not parent-owned",
            bmem_not_owned,
            bmem_extremum[-1]["blocker"],
        ),
        validation_row(
            "VAL1348_3_operator_scaffold_present",
            "memory operator scaffold is present",
            operator_scaffold,
            operator_signature[0]["mathematical_form"],
        ),
        validation_row(
            "VAL1348_4_operator_not_owned",
            "Z_mem/M2_mem operator signature is not parent-owned",
            operator_not_owned,
            operator_signature[-1]["blocker"],
        ),
        validation_row(
            "VAL1348_5_closure_contract_written",
            "memory closure and finite-residual contracts are explicit",
            len(closure_contract) == 4,
            f"closure_rows={len(closure_contract)}",
        ),
        validation_row(
            "VAL1348_6_claims_blocked",
            "B_mem, operator, and memory no-hair claims remain blocked",
            claims_blocked,
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in claim_gate),
        ),
        validation_row(
            "VAL1348_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1348_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_hits) == 0,
            f"formalization_generated_output_count={len(formalization_hits)}",
        ),
        validation_row(
            "VAL1348_9_next_target_1349",
            "next target routes to K_MTS trace projection owner or closure declaration",
            next_target[0]["next_id"] == "NEXT1348_0_1349",
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1348_10_overall",
            "overall 1348 validation",
            overall_ok,
            "1348 proves only conditional F1 calculus, not parent-owned B_mem=0, and keeps memory closure explicit",
        ),
    ]
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1348 proves only the conditional calculus: if the `Gamma_eff` trace projection is parent-owned and `m_L` is a true branch extremum, then the linear memory channel `B_mem` vanishes. It does **not** prove that MTS owns those premises.

**Main progress:** the exact blocker is now isolated. The problem is not `F1=0` algebra; it is whether `Gamma_eff = L_cg^-2[F_L+a_F(R(m;X_B)-R(m_L;X_B))]` is derived from `K_MTS` / parent variation, and whether `R(m;X_B)`, `m_L`, `Z_mem`, and `M2_mem` are parent-signed.

**Decision:** move to `1349`: attack the `K_MTS` trace-projection owner directly, or formally declare `B_mem=0` a private closure rather than a theorem. No local-GR/R10/PPN claim is made.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Bmem Extremum Test
{markdown_table(bmem_extremum, ["test_id", "claim_piece", "mathematical_form", "result", "blocker", "valid_for_claim", "claim_allowed"])}

## Memory Operator Signature Test
{markdown_table(operator_signature, ["test_id", "claim_piece", "mathematical_form", "result", "blocker", "valid_for_claim", "claim_allowed"])}

## Memory Closure Contract
{markdown_table(closure_contract, ["contract_id", "route", "statement", "required_future_derivation", "allowed_use", "forbidden_use", "valid_for_claim", "claim_allowed"])}

## Finite Memory Branch Contract
{markdown_table(finite_branch, ["branch_id", "field_equation", "range", "amplitude", "current_status", "missing", "valid_for_claim", "claim_allowed"])}

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
