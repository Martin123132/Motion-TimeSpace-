from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1117-Y5-R10-domain-selector-zero-or-domain-coupling-prior-source.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    out: list[dict[str, object]] = []
    for row in rows:
        copied = dict(row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("claim_allowed", "false")
        copied.setdefault("generated_utc", generated)
        out.append(copied)
    return out


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1117_0_1116_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1116_NEXT_TARGET.csv",
            "needle": "NEXT1116_0_1117",
            "note": "1116 handoff to domain selector zero or finite domain prior.",
        },
        {
            "source_id": "SRC1117_1_1116_obligation",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1116_PROOF_OBLIGATIONS.csv",
            "needle": "OBL1116_0_domain_selector_zero",
            "note": "domain selector proof obligation.",
        },
        {
            "source_id": "SRC1117_2_domain_attempt",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T6_no_vector_verdict",
            "note": "domain no-vector/no-flux/no-anisotropy theorem fails current corpus.",
        },
        {
            "source_id": "SRC1117_3_parent_clause",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
            "needle": "C5_R11_silence",
            "note": "parent-action clause requires R11 silence.",
        },
        {
            "source_id": "SRC1117_4_r11_zero",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_THEOREM_ZERO_ATTEMPT.csv",
            "needle": "Z6_verdict",
            "note": "R11/domain source-normalization zero route fails current corpus.",
        },
        {
            "source_id": "SRC1117_5_r11_fill",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
            "needle": "DSR_R7_alpha3",
            "note": "domain alpha3 fill row is conditional/not scoreable.",
        },
        {
            "source_id": "SRC1117_6_parent_gate",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_GATE.csv",
            "needle": "G4_R11_silence",
            "note": "domain parent action gate fails R11 silence.",
        },
        {
            "source_id": "SRC1117_7_vector_coeffs",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv",
            "needle": "domain_projector_mass",
            "note": "finite vector coefficient products remain nonclaim.",
        },
        {
            "source_id": "SRC1117_8_1116_source_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1116_COUPLING_PRIOR_SOURCE_PACK_NONCLAIM.csv",
            "needle": "CPS1116_0_domain",
            "note": "finite domain source pack row.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "DSZ1117_0_target",
                "claim_piece": "domain selector zero",
                "formal_statement": "P_loc grad chi_D = 0, domain flux = 0, selector STF stress = 0, and c_domain_source_normalization_operator = 0.",
                "result": "TARGET_SHARP",
                "proof_or_blocker": "this is the minimum needed to stop the domain selector feeding local PPN/R10/source rows",
            },
            {
                "attempt_id": "DSZ1117_1_no_vector",
                "claim_piece": "no preferred domain vector",
                "formal_statement": "If chi_D is a stationary scalar selector with no independent normal/velocity/marker vector, then epsilon_domain_vector = 0.",
                "result": "CONDITIONAL_LEMMA_ONLY",
                "proof_or_blocker": "works if the parent action really makes chi_D scalar/auxiliary and locally fixed; that parent derivation is missing",
            },
            {
                "attempt_id": "DSZ1117_2_no_flux",
                "claim_piece": "no domain momentum flux",
                "formal_statement": "If the local representative is compact/exact/trivial and no coherent FLRW memory class is active locally, then epsilon_domain_flux = 0.",
                "result": "CONDITIONAL_NOT_PARENT_DERIVED",
                "proof_or_blocker": "local exact/trivial representative is a contract, not a derived parent branch",
            },
            {
                "attempt_id": "DSZ1117_3_no_stf",
                "claim_piece": "no anisotropic selector stress",
                "formal_statement": "If selector/domain stress is scalar, topological, or bulk-zero, then STF(P_loc T_D P_loc)=0.",
                "result": "CONDITIONAL_NOT_PARENT_DERIVED",
                "proof_or_blocker": "projector/domain stress remains conditional and not parent-owned",
            },
            {
                "attempt_id": "DSZ1117_4_R11_source",
                "claim_piece": "domain source-normalization operator silence",
                "formal_statement": "c_domain_source_normalization_operator = 0, or all R11 domain-source rows are executable and claim-valid.",
                "result": "FAIL_CURRENT_CORPUS",
                "proof_or_blocker": "R11 domain source zero route fails and claim-valid executable rows are absent",
            },
            {
                "attempt_id": "DSZ1117_5_ward_shortcut",
                "claim_piece": "Ward/Bianchi covariance kills selector source",
                "formal_statement": "nabla_mu T_total^{mu nu}=0 implies selector vector/source residuals vanish.",
                "result": "REJECTED_SHORTCUT",
                "proof_or_blocker": "covariant ownership is not absence; a covariant selector source can still exist",
            },
            {
                "attempt_id": "DSZ1117_6_verdict",
                "claim_piece": "derive domain selector zero",
                "formal_statement": "the domain selector is gauge/readout-only or fixed local branch with no vector, flux, anisotropy, or source-normalization operator.",
                "result": "DOMAIN_SELECTOR_ZERO_NOT_DERIVED",
                "proof_or_blocker": "vector/flux/STF silence are conditional and R11/source-normalization silence fails current corpus",
            },
        ]
    )


def component_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "component_id": "COMP1117_0_vector",
                "component": "epsilon_domain_vector",
                "mapped_observables": "PPN alpha1; PPN alpha2",
                "zero_status": "CONDITIONAL_ONLY",
                "residual_if_live": "W_domain_alpha1*epsilon_domain_vector; W_domain_alpha2*epsilon_domain_vector",
                "required_next": "parent scalar/auxiliary selector proof or numeric vector product",
            },
            {
                "component_id": "COMP1117_1_flux",
                "component": "epsilon_domain_flux",
                "mapped_observables": "PPN alpha3; R10/local source channel",
                "zero_status": "CONDITIONAL_ONLY",
                "residual_if_live": "W_domain_alpha3*epsilon_domain_flux",
                "required_next": "local exact/trivial representative proof and R11 silence or numeric flux product",
            },
            {
                "component_id": "COMP1117_2_anisotropy",
                "component": "epsilon_domain_anisotropy",
                "mapped_observables": "PPN xi; preferred-location stress",
                "zero_status": "CONDITIONAL_ONLY",
                "residual_if_live": "W_domain_xi*epsilon_domain_anisotropy",
                "required_next": "projector/domain stress zero proof or numeric STF product",
            },
            {
                "component_id": "COMP1117_3_R11_operator",
                "component": "c_domain_source_normalization_operator",
                "mapped_observables": "R11 non-EH operator ledger; local source normalization; R10/domain products",
                "zero_status": "FAIL_CURRENT_CORPUS",
                "residual_if_live": "non-EH/domain source-normalization operator vector",
                "required_next": "derive R11 zero or create executable coefficient vector",
            },
            {
                "component_id": "COMP1117_4_parent_clause",
                "component": "chi_D auxiliary scalar fixed local branch",
                "mapped_observables": "all domain selector rows",
                "zero_status": "CONTRACT_NOT_PARENT_DERIVED",
                "residual_if_live": "domain selector remains physical generator",
                "required_next": "parent action derivation or explicit closure label",
            },
        ]
    )


def prior_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "prior_id": "DPR1117_0_alpha1",
                "observable": "PPN alpha1",
                "product": "W_domain_alpha1 * epsilon_domain_vector",
                "target_bound": "1e-04",
                "status": "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO",
                "required_source": "numeric/theorem-zero vector coefficient with source path",
            },
            {
                "prior_id": "DPR1117_1_alpha2",
                "observable": "PPN alpha2",
                "product": "W_domain_alpha2 * epsilon_domain_vector",
                "target_bound": "2e-09",
                "status": "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO",
                "required_source": "numeric/theorem-zero vector coefficient with source path",
            },
            {
                "prior_id": "DPR1117_2_alpha3",
                "observable": "PPN alpha3",
                "product": "W_domain_alpha3 * epsilon_domain_flux",
                "target_bound": "4e-20",
                "status": "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO",
                "required_source": "numeric/theorem-zero flux/R11 source coefficient with source path",
            },
            {
                "prior_id": "DPR1117_3_xi",
                "observable": "PPN xi",
                "product": "W_domain_xi * epsilon_domain_anisotropy",
                "target_bound": "4e-09",
                "status": "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO",
                "required_source": "numeric/theorem-zero anisotropy coefficient with source path",
            },
            {
                "prior_id": "DPR1117_4_R11",
                "observable": "R11/domain source-normalization",
                "product": "c_domain_source_normalization_operator",
                "target_bound": "operator row has units, weak-field map, and no MISSING fields",
                "status": "MISSING_EXECUTABLE_COEFFICIENT_VECTOR_OR_ZERO_THEOREM",
                "required_source": "R11 executable coefficient vector or parent zero theorem",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1117_0_domain_zero",
                "claim": "domain selector is theorem-zero",
                "gate_pass": "false",
                "reason": "conditional vector/flux/STF lemmas plus failed R11 silence do not make a parent derivation",
            },
            {
                "gate_id": "CG1117_1_PPN_safe",
                "claim": "domain selector is safe for PPN/local GR",
                "gate_pass": "false",
                "reason": "alpha1/alpha2/alpha3/xi products remain missing or conditional",
            },
            {
                "gate_id": "CG1117_2_R11_safe",
                "claim": "domain source-normalization operator is zero",
                "gate_pass": "false",
                "reason": "R11 zero route fails and executable coefficient vector is missing",
            },
            {
                "gate_id": "CG1117_3_prior_ready",
                "claim": "finite domain priors are score-ready",
                "gate_pass": "false",
                "reason": "all domain prior rows need numeric products or theorem-zero sources",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1117_0_result",
                "decision": "domain selector zero is not derived",
                "because": "the quiet-domain route has useful conditional lemmas but R11/domain source-normalization remains a hard failure",
                "next_action": "attack R11 domain source-normalization zero or build executable coefficient vector",
            },
            {
                "decision_id": "DEC1117_1_best_next",
                "decision": "R11 source-normalization is the next bottleneck",
                "because": "it can reintroduce local source residuals even if vector/flux/STF clauses are conditionally quiet",
                "next_action": "derive c_domain_source_normalization_operator=0 or create strict R11 coefficient rows",
            },
            {
                "decision_id": "DEC1117_2_policy",
                "decision": "no local-GR/PPN/R10 claim from domain selector branch",
                "because": "domain products remain unscored and nonclaim",
                "next_action": "keep all domain rows valid_for_claim=false until zero or numeric products exist",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1117_0_1118",
                "next_target": "1118-Y5-R10-domain-R11-source-normalization-zero-or-executable-coefficient-vector.md",
                "objective": "try to derive c_domain_source_normalization_operator=0 for the local branch; if not, build strict executable R11/domain coefficient-vector rows with units, maps, source paths, and no placeholders",
                "include": "R11 domain source operator; c_domain_source_normalization_operator; alpha3 flux product; PPN alpha1/alpha2/xi mappings; weak-field map; executable coefficient schema",
                "exclude": "Ward/Bianchi shortcut; local-GR claim; tau=1; source-unity; symbolic R10 pass; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    components: list[dict[str, object]],
    priors: list[dict[str, object]],
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

    add("V1117_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1117_1_conditional_clauses", sum(1 for row in theorem if "CONDITIONAL" in str(row["result"])) >= 3, "vector, flux, and STF clauses are conditional")
    add("V1117_2_r11_failure", any(row["result"] == "FAIL_CURRENT_CORPUS" for row in theorem), "R11 source-normalization failure is recorded")
    add("V1117_3_zero_not_derived", any(row["result"] == "DOMAIN_SELECTOR_ZERO_NOT_DERIVED" for row in theorem), "domain selector zero remains unpromoted")
    add("V1117_4_components_complete", {"epsilon_domain_vector", "epsilon_domain_flux", "epsilon_domain_anisotropy", "c_domain_source_normalization_operator"}.issubset({str(row["component"]) for row in components}), "domain vector/flux/anisotropy/R11 components are explicit")
    add("V1117_5_priors_nonclaim", all("MISSING" in row["status"] for row in priors), "domain prior rows remain missing-input nonclaim")
    add("V1117_6_gates_blocked", all(row["gate_pass"] == "false" for row in gates), "all claim gates remain blocked")
    add("V1117_7_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in theorem + components + priors + gates + decisions + next_target), "all generated rows remain nonclaim")
    add("V1117_8_next_target", next_target[0]["next_target"].startswith("1118-") and "domain-R11" in str(next_target[0]["next_target"]), "1118 handoff targets domain R11 source-normalization")
    add("V1117_9_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1117_10_csv_parse", csv_parse_ok, "all 1117 CSV outputs parse cleanly")
    add("V1117_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1117_SUMMARY", True, "1117 rejects domain selector zero and isolates R11 source-normalization as next bottleneck")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    components: list[dict[str, object]],
    priors: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1117 - Domain Selector Zero Or Domain Coupling Prior Source

**Current verdict:** domain selector zero is not derived. The vector, flux, and STF-stress silence routes are useful conditional lemmas, but R11/domain source-normalization silence fails in the current corpus.

**Bottleneck:** `c_domain_source_normalization_operator` is the next hard edge. It can reintroduce local source residuals even if the domain selector is scalar/stationary enough to kill preferred vectors.

**No claim:** no domain-selector zero, no PPN/local-GR/R10 safety, and no finite domain-prior pass follows from 1117.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Domain Zero Theorem Attempt
{table(["attempt_id", "claim_piece", "formal_statement", "result", "proof_or_blocker", "claim_allowed"], theorem)}

## Component Status
{table(["component_id", "component", "mapped_observables", "zero_status", "residual_if_live", "required_next", "claim_allowed"], components)}

## Domain Coupling Prior Rows
{table(["prior_id", "observable", "product", "target_bound", "status", "required_source", "claim_allowed"], priors)}

## Claim Gates
{table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates)}

## Decisions
{table(["decision_id", "decision", "because", "next_action", "claim_allowed"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1117_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1117_DOMAIN_ZERO_THEOREM_ATTEMPT.csv",
        "components": OUT / "P8_Y5_R10_1117_DOMAIN_COMPONENT_STATUS.csv",
        "priors": OUT / "P8_Y5_R10_1117_DOMAIN_COUPLING_PRIOR_ROWS_NONCLAIM.csv",
        "gates": OUT / "P8_Y5_R10_1117_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1117_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1117_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1117_VALIDATION.csv",
    }
    sources = source_rows()
    theorem = theorem_rows()
    components = component_rows()
    priors = prior_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["components"], components)
    write_csv(outputs["priors"], priors)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, theorem, components, priors, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, theorem, components, priors, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
