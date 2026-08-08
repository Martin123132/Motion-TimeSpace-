from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3721"
BRANCH_ID = "MTS_R2FR_Y5_RESPONSE_DOUBLET_TO_GIBBS_BATH_PARITY_MAP_OR_DEMOTION_3721"
DOC = ROOT / "3721-Y5-R2FR-response-doublet-to-Gibbs-bath-parity-map-or-demotion.md"

DOC_3720 = ROOT / "3720-Y5-R2FR-corpus-hunt-parent-bath-scale-parity-clauses.md"
NEXT_3720 = RESIDUALS / "P8_Y5_R2FR_3720_NEXT_TARGET.csv"
BRIDGE_3720 = RESIDUALS / "P8_Y5_R2FR_3720_BRIDGE_CONTRACT_ROWS.csv"
ADJ_3720 = RESIDUALS / "P8_Y5_R2FR_3720_CLAUSE_ADJUDICATION_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
GAMMA_ACTION_516 = RESIDUALS / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv"
DOUBLET_VARIATION_517 = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv"
DOUBLET_CONTRACT_516 = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
ODD_THEOREM = RESIDUALS / "P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv"
DOC_3719 = ROOT / "3719-Y5-R2FR-parent-bath-normalization-and-z-parity-proof.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3720", DOC_3720, "PARTIAL_CORPUS_SUPPORT_BRIDGE_REQUIRED", "3720 status"),
        ("next_3720", NEXT_3720, "z=Z", "bridge handoff"),
        ("bridge_3720", BRIDGE_3720, "Theta_H I_H equals the quadratic operator M_AB", "bridge contract"),
        ("adjudication_3720", ADJ_3720, "ADJ3720_4_parity_involution", "corpus adjudication"),
        ("fisher_3708", FISHER_3708, "Delta F_cg=T_eff D_KL", "positive KL penalty route"),
        ("gamma_action_516", GAMMA_ACTION_516, "Gamma_eff = Gamma0 + 1/2", "even quadratic action candidate"),
        ("doublet_variation_517", DOUBLET_VARIATION_517, "AV517_2_first_variation_Z", "double-zero variation"),
        ("doublet_contract_516", DOUBLET_CONTRACT_516, "RD516_4_zero_odd_source", "boundary/source obstruction"),
        ("odd_theorem", ODD_THEOREM, "E3_even_action", "exchange-even theorem attempt"),
        ("doc_3719", DOC_3719, "F_B(q,z)=-Theta_H(q) log Z(q,z)", "raw Gibbs free-energy template to refine"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(ts),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
        })
    return rows


def bridge_theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "THM3721_0_coordinate_identification",
            "Assume z^A := Z^A=(R_+^A-R_-^A)/2 for every active local leakage component.",
            "Then exchange E:R_+<->R_- acts as z^A -> -z^A.",
            "CONDITIONAL_EXACT",
        ),
        (
            "THM3721_1_quotient_invisibility",
            "Assume q=q(R_even) and R_even=(R_++R_-)/2.",
            "Then Dq[partial_z]=0: z is a vertical/fibre coordinate, not an observed local matter/clock/EM variable.",
            "CONDITIONAL_EXACT",
        ),
        (
            "THM3721_2_even_action_double_zero",
            "Assume Gamma_eff(q,z)=Gamma0(q)+0.5 M_AB(q)z^A z^B+O(z^4) and no odd source/boundary term.",
            "Then partial_z Gamma_eff|0=0 and partial_q partial_z Gamma_eff|0=0 over the q patch.",
            "CONDITIONAL_EXACT",
        ),
        (
            "THM3721_3_KL_penalty_hessian",
            "For Psi_KL(q,z)=Theta_H(q) D_KL(p_z||p_0), Hessian_z Psi_KL|0=Theta_H I_H.",
            "This gives a positive information-geometric fibre penalty if I_H has a positive local floor.",
            "DERIVED_FOR_KL_EFFECTIVE_ACTION",
        ),
        (
            "THM3721_4_operator_match",
            "If M_AB = Theta_H I_AB + DeltaM_map in the same G_H/U_H basis, then Xi_H >= lambda_min(M)-||DeltaM_map||-R_boundary.",
            "This is the executable bridge from response-doublet operator to Fisher gap.",
            "DERIVED_BOUND",
        ),
        (
            "THM3721_5_raw_free_energy_warning",
            "For raw F=-Theta log integral exp[-A/Theta]dmu, partial_AB F=<A_AB>-(1/Theta)Cov(A_A,A_B).",
            "Raw partition free energy is not automatically the positive KL penalty; using it blindly can flip the sign.",
            "ANTI_SHORTCUT_GUARD",
        ),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "assumption_or_formula": assumption_or_formula,
            "result": result,
            "status": status,
            "claim_allowed": False,
        }
        for theorem_id, assumption_or_formula, result, status in rows
    ]


def current_bridge_audit_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("AUD3721_0_z_equals_Z", "z^A=Z^A", "PARTIAL", "3708 has z; 516/517 have Z; no source yet proves they are the same coordinate."),
        ("AUD3721_1_exchange_parity", "R_z=exchange", "PARTIAL", "odd theorem has exchange candidate, but exact parent symmetry for all active channels is not derived."),
        ("AUD3721_2_q_even", "q=q(R_even)", "PARTIAL", "matter/even observed geometry is written as a route, not parent-derived for all readouts."),
        ("AUD3721_3_action_hessian", "M_AB=Theta_H I_AB", "NOT_SIGNED", "response-doublet quadratic density and KL Hessian remain separate objects."),
        ("AUD3721_4_unit_basis", "same G_H/U_H basis", "MISSING", "no same-basis unit map turns Fisher/operator Hessian into m^-2 local residual units."),
        ("AUD3721_5_source_boundary", "J_Z=B_Z=0", "BLOCKED", "516/517/1011 identify source-current and boundary work as hard blockers."),
        ("AUD3721_6_positive_floor", "lambda_min(I_H)>0", "NOT_PROVED", "iota_H is defined but identifiability/eigenfloor is not parent-signed."),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "bridge_clause": bridge_clause,
            "current_status": current_status,
            "evidence": evidence,
            "claim_allowed": False,
        }
        for audit_id, bridge_clause, current_status, evidence in rows
    ]


def retained_coefficient_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("RC3721_0_coordinate_mismatch", "Delta_zZ", "||z-Z|| in active local residual basis", "feeds DeltaM_map and residual projection error"),
        ("RC3721_1_operator_mismatch", "DeltaM_map", "M_AB-Theta_H I_AB in same G_H/U_H basis", "reduces Xi_H lower bound"),
        ("RC3721_2_unit_mismatch", "Delta_UH", "basis/unit mismatch between Fisher Hessian and local operator", "blocks R10/PPN conversion"),
        ("RC3721_3_odd_source", "J_Z", "exchange-odd source current", "creates F_1,total"),
        ("RC3721_4_boundary_work", "B_Z+B_boundary", "odd boundary/source work", "creates F_1,total and B_QK,total"),
        ("RC3721_5_identifiability_loss", "iota_loss", "zero-score active fibre directions", "can close Xi_H gap"),
    ]
    return [
        {
            **base(ts),
            "coefficient_id": coefficient_id,
            "quantity": quantity,
            "definition": definition,
            "impact": impact,
            "status": "FINITE_ROW_REQUIRED_UNLESS_THEOREM_ZERO",
            "claim_allowed": False,
        }
        for coefficient_id, quantity, definition, impact in rows
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3721_0_bridge_survives",
            "BRIDGE_THEOREM_CONSTRUCTED_CONDITIONAL",
            "If z=Z, exchange is exact, and M_AB=Theta_H I_H in one basis, the 3719 mechanism becomes a real parent route.",
        ),
        (
            "DEC3721_1_current_not_signed",
            "CURRENT_MTS_NOT_PROMOTED",
            "The corpus does not yet sign the coordinate map, operator equality, unit map, identifiability, or boundary/source silence.",
        ),
        (
            "DEC3721_2_raw_free_energy_refined",
            "RAW_GIBBS_FREE_ENERGY_NOT_ENOUGH",
            "The positive gap should be a KL/Legendre effective action or otherwise prove the sign; naive -Theta log Z is unsafe.",
        ),
        (
            "DEC3721_3_next",
            "ADVANCE_TO_KL_LEGENDRE_EFFECTIVE_ACTION_OWNER",
            "Before further local scoring, lock whether the parent action owns the KL penalty, the Legendre transform, and the M=Theta I operator sign.",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in rows
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    gates = [
        ("CG3721_0_zZ", "BLOCKED", "z=Z component map is parent-signed"),
        ("CG3721_1_parity", "BLOCKED", "exchange is exact fibre parity for all active components"),
        ("CG3721_2_KL_action", "BLOCKED", "positive KL/Legendre effective action is parent-owned"),
        ("CG3721_3_operator", "BLOCKED", "M_AB=Theta_H I_AB in same basis, with units"),
        ("CG3721_4_boundary", "BLOCKED", "J_Z and boundary odd work vanish or are bounded"),
        ("CG3721_5_gap", "BLOCKED", "Xi_H lower bound positive and local-unit converted"),
        ("CG3721_6_claim", "BLOCKED", "local-GR/R10/PPN screening claim allowed"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate_status": gate_status,
            "required_before_claim": required_before_claim,
            "claim_allowed": False,
        }
        for gate_id, gate_status, required_before_claim in gates
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "status_id": "STATUS3721_0",
        "status": "CONDITIONAL_BRIDGE_THEOREM_BUILT_RAW_FREE_ENERGY_GUARD_ADDED",
        "summary": "3721 proves the bridge conditionally and exposes the key sign issue: the positive gap must come from a KL/Legendre effective action, not an unqualified raw -Theta log Z free energy.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3721_0",
        "target_doc": "3722-Y5-R2FR-KL-Legendre-effective-action-sign-owner-or-free-energy-demotion.md",
        "target_script": "scripts/Y5_R2FR_3722_KL_Legendre_effective_action_sign_owner_or_free_energy_demotion.py",
        "objective": "derive whether the parent variational principle owns the positive KL/Legendre effective action Psi_KL=Theta_H D_KL, or reject raw Gibbs free energy as a gap source and retain M_AB as independent nonclaim coefficient",
        "success_gate": "positive Hessian sign, Theta_H units, I_H definition, and M_AB equality are parent-owned or explicitly demoted to finite nonclaim rows",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated_paths = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3721*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    checks = [
        ("sources_exist", "all key sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all key needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all generated outputs exist", all(path.exists() for path in generated_paths)),
        ("csv_parse", "all generated CSV files parse and are nonempty", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("bridge_theorems", "bridge theorem includes z=Z, KL Hessian, and raw free energy warning", all(token in read_text(paths["theorems"]) for token in ["z^A := Z^A", "Theta_H I_H", "Raw partition free energy"])),
        ("audit_blocks", "current audit blocks promotion", all(row["claim_allowed"] == "False" for row in parse_csv(paths["audit"]))),
        ("coefficients_retained", "retained coefficient rows include DeltaM and boundary work", all(token in read_text(paths["coefficients"]) for token in ["DeltaM_map", "B_Z+B_boundary"])),
        ("decisions", "decisions include raw free energy refinement", "RAW_GIBBS_FREE_ENERGY_NOT_ENOUGH" in read_text(paths["decisions"])),
        ("claim_gates_blocked", "all claim gates remain blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3722", "next target advances to KL/Legendre sign owner", "3722" in read_text(paths["next_target"])),
        ("doc_core_terms", "markdown contains conditional bridge and sign guard", all(token in read_text(paths["doc"]) for token in ["z=Z", "KL/Legendre", "raw `-Theta log Z`"])),
        ("no_formalization_leak", "no 3721 files written to formalization-workbench", len(formal_files) == 0),
    ]
    return [
        {
            **base(ts),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3721 — Response Doublet to Gibbs Bath Parity Map or Demotion",
        "",
        "## Status",
        "- `CONDITIONAL_BRIDGE_THEOREM_BUILT_RAW_FREE_ENERGY_GUARD_ADDED`",
        "- The bridge can be made mathematically clean if `z=Z`, exchange is exact parity, and the positive operator is the KL/Legendre Hessian.",
        "- Current MTS is not promoted: component map, unit map, operator equality, identifiability, and boundary/source silence remain unsigned.",
        "",
        "## Main Result",
        "- Conditional bridge: `z=Z=(R_+-R_-)/2`, `R_z=exchange`, and `q=q(R_even)` make the Fisher fibre a vertical response-doublet direction.",
        "- Even action result: if `Gamma_eff=Gamma0+0.5 M_AB z^A z^B+O(z^4)` with no odd source/boundary term, then `F_1=0` and `B_QK=0` over the q patch.",
        "- Positive gap result: `Psi_KL=Theta_H D_KL` gives Hessian `Theta_H I_H`; matching requires `M_AB=Theta_H I_AB+DeltaM_map` in the same unit basis.",
        "- Sign guard: raw `-Theta log Z` is not automatically the positive KL penalty; its Hessian is `<A_AB>-(1/Theta)Cov(A_A,A_B)`.",
        "",
        "## Bridge Theorems",
    ]
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['assumption_or_formula']} Result: {row['result']}")
    lines.extend(["", "## Current Bridge Audit"])
    for row in grouped["audit"]:
        lines.append(f"- `{row['audit_id']}` `{row['current_status']}` — {row['bridge_clause']}: {row['evidence']}")
    lines.extend(["", "## Retained Coefficients"])
    for row in grouped["coefficients"]:
        lines.append(f"- `{row['coefficient_id']}` `{row['quantity']}`: {row['definition']} | impact: {row['impact']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` `{row['gate_status']}` | {row['required_before_claim']}")
    lines.extend(["", "## Source Register"])
    for row in grouped["source_register"]:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend([
        "",
        "## Next Target",
        "- `3722-Y5-R2FR-KL-Legendre-effective-action-sign-owner-or-free-energy-demotion.md`",
        "- Objective: lock the sign and ownership of the positive KL/Legendre effective action before using the Fisher gap in local screening claims.",
        "",
        "## Validation",
        f"- See `{paths['validation']}`.",
    ])
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3721_SOURCE_REGISTER.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3721_BRIDGE_THEOREM_ROWS.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3721_CURRENT_BRIDGE_AUDIT_ROWS.csv",
        "coefficients": RESIDUALS / "P8_Y5_R2FR_3721_RETAINED_COEFFICIENT_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3721_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3721_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3721_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3721_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3721_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(ts),
        "theorems": bridge_theorem_rows(ts),
        "audit": current_bridge_audit_rows(ts),
        "coefficients": retained_coefficient_rows(ts),
        "decisions": decision_rows(ts),
        "claim_gates": claim_gate_rows(ts),
        "status": status_rows(ts),
        "next_target": next_target_rows(ts),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(ts, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3721 validation failed: {failures}")
    print("wrote 3721 checkpoint: conditional z=Z bridge theorem and KL sign guard")


if __name__ == "__main__":
    main()
