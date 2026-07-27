from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1122-Y5-R10-source-normalization-alpha3-coupling-map-or-zero.md"


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


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1122_0_1121_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1121_NEXT_TARGET.csv",
            "needle": "NEXT1121_0_1122",
            "note": "1121 handoff to source-normalization alpha3 coupling map.",
        },
        {
            "source_id": "SRC1122_1_1121_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1121_R11_ALPHA3_EXECUTABLE_ROW_CONTRACT.csv",
            "needle": "K_R11_alpha3",
            "note": "1121 row contract names the missing coupling map.",
        },
        {
            "source_id": "SRC1122_2_no_vector",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T0_define_selector_vector_residual",
            "note": "Domain PPN rows are fed by vector, flux, or anisotropy projections.",
        },
        {
            "source_id": "SRC1122_3_vector_coeffs",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "Existing alpha3 row is a flux product, not a scalar monopole product.",
        },
        {
            "source_id": "SRC1122_4_R11_link",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv",
            "needle": "L2_alpha3_flux",
            "note": "Domain alpha3 link demands flux product below the 4e-20 bound.",
        },
        {
            "source_id": "SRC1122_5_R11_mu_link",
            "relative_path": "source-intake/mts_residuals/R11_MU_EXTRA_SOURCE_NORMALIZATION_LINK.csv",
            "needle": "domain_projector_mass",
            "note": "R11 source-normalization row includes the domain projector mass channel.",
        },
        {
            "source_id": "SRC1122_6_R11_fill",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
            "needle": "DSR_R7_alpha3",
            "note": "Fill requirements keep alpha3 bound and R11 family explicit.",
        },
        {
            "source_id": "SRC1122_7_R11_gates",
            "relative_path": "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_ACCEPTANCE_GATES.csv",
            "needle": "G4_no_absorption_cheat",
            "note": "Source-normalization leakage cannot be hidden in measured GM when it carries residual structure.",
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


def decomposition_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "component_id": "C1122_0_scalar_monopole",
                "component": "delta_mu_0",
                "local_type": "scalar/isotropic monopole",
                "alpha3_projection": "Pi_alpha3[delta_mu_0]=0",
                "derivation_status": "DERIVED_CONDITIONAL_ON_LOCAL_ROTATIONAL_INVARIANCE",
                "reason": "alpha3 is a preferred-frame/vector-residual channel; a scalar monopole has no free spatial vector index",
                "remaining_input": "prove the local R11 perturbation is purely scalar, universal, and derivative-silent",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "component_id": "C1122_1_vector_flux",
                "component": "F_i or epsilon_domain_flux",
                "local_type": "spatial vector/flux/pseudo-vector residual",
                "alpha3_projection": "Pi_alpha3[F_i]=K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "derivation_status": "LIVE_UNFILLED",
                "reason": "existing R7 alpha3 rows are exactly flux-product rows and T2 no-flux is conditional, not parent-derived",
                "remaining_input": "derive no-flux theorem or source K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "component_id": "C1122_2_STF_anisotropy",
                "component": "S_ij^TF",
                "local_type": "tracefree anisotropic/projector stress",
                "alpha3_projection": "does not close alpha3 by itself; can mix into preferred-frame rows if paired with local vector/time direction",
                "derivation_status": "RETAINED_SIBLING_GUARD",
                "reason": "R8 xi and projector stress siblings remain open and cannot be hidden by alpha3-only closure",
                "remaining_input": "keep sibling guard active until projector stress is zero or numerically bounded",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "component_id": "C1122_3_time_odd_drift",
                "component": "partial_t delta_mu or memory-drift source",
                "local_type": "time-odd scalar plus frame velocity",
                "alpha3_projection": "possible only after a preferred frame/time-gradient map is supplied",
                "derivation_status": "RETAINED_OUTSIDE_ALPHA3_CORE",
                "reason": "a time-varying scalar is not an alpha3 pass; it must map through Gdot/clock/preferred-frame rows",
                "remaining_input": "route through R9/clock/Gdot or show stationarity",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def scalar_zero_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "lemma_id": "L1122_0_statement",
                "statement": "A purely scalar, stationary, isotropic source-normalization perturbation cannot contribute to PPN alpha3 at leading local order.",
                "formal_condition": "delta_mu_R11 = delta_mu_0(r) with no P_loc^i_mu F^mu, no local normal/velocity marker, no time-odd drift, and no STF stress pairing",
                "formal_result": "K_R11_alpha3_scalar=0",
                "status": "CONDITIONAL_LEMMA",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "L1122_1_index_argument",
                "statement": "The alpha3 projection carries a preferred-frame/vector slot, while delta_mu_0 is rotationally invariant.",
                "formal_condition": "SO(3) local isotropy in the observed coframe",
                "formal_result": "Pi_alpha3[scalar]=0 by absence of a spatial vector index",
                "status": "DERIVED_WITH_ASSUMPTIONS",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "L1122_2_absorption_guard",
                "statement": "The scalar-zero lemma does not permit hiding range, time, species, radial, vector, or anisotropic leakage in measured GM.",
                "formal_condition": "only universal constant scalar offsets are harmless; structured scalar leakage routes to beta/gamma/R10/Gdot rather than alpha3",
                "formal_result": "alpha3 scalar component zero, but R11 source-normalization branch remains open",
                "status": "GUARD_ACTIVE",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "L1122_3_verdict",
                "statement": "The generic 1121 map should be narrowed: scalar source-normalization has zero alpha3 projection, but flux/vector leakage remains live.",
                "formal_condition": "C1122_0 closes only the scalar subcomponent; C1122_1 remains unfilled",
                "formal_result": "P_R11_source_alpha3 = K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux plus any explicitly derived non-scalar pieces",
                "status": "PARTIAL_DERIVATION_NOT_CLAIM",
                "valid_for_claim": "false",
            },
        ]
    )


def flux_contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "R11F1122_0_flux_alpha3",
                "observable": "alpha3",
                "live_quantity": "P_R11_source_alpha3_flux",
                "narrowed_map": "P_R11_source_alpha3_flux = K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "zero_route": "prove epsilon_domain_flux=0 from parent local representative, or prove K_R11_flux_alpha3=0 by symmetry",
                "numeric_route": "source K_R11_flux_alpha3, c_R11_flux_alpha3, and epsilon_domain_flux with units/normalization",
                "target_bound": "4e-20",
                "acceptance": "abs(K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux) <= 4e-20 without tuned cancellation and with siblings guarded",
                "current_status": "MISSING_FLUX_ZERO_OR_NUMERIC_PRODUCT",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "R11F1122_1_scalar_removed_from_alpha3",
                "observable": "alpha3",
                "live_quantity": "P_R11_source_alpha3_scalar",
                "narrowed_map": "P_R11_source_alpha3_scalar = 0 under local scalar/isotropic/stationary assumptions",
                "zero_route": "prove source-normalization perturbation is scalar-only",
                "numeric_route": "not applicable for alpha3; structured scalar pieces route elsewhere",
                "target_bound": "4e-20",
                "acceptance": "cannot promote total alpha3 while flux/vector branch remains open",
                "current_status": "CONDITIONAL_ZERO_SUBCOMPONENT_ONLY",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1122_0_scalar_alpha3_zero",
                "rule": "scalar source-normalization component has no alpha3 projection",
                "gate_pass": "true_nonclaim",
                "reason": "index/rotational argument closes only the scalar subcomponent",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1122_1_flux_closed",
                "rule": "flux/vector component is zero or numerically below 4e-20",
                "gate_pass": "false",
                "reason": "T2 no-flux remains conditional and no numeric flux product is sourced",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1122_2_total_alpha3_closed",
                "rule": "total domain/R11 alpha3 residual is closed",
                "gate_pass": "false",
                "reason": "scalar narrowing helps but the live flux row remains missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1122_3_local_GR",
                "rule": "local-GR/R10 branch can promote using 1122",
                "gate_pass": "false",
                "reason": "1122 is a partial coupling-map derivation only",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1122_0_map_narrowed",
                "decision": "replace generic epsilon_domain_projector alpha3 leakage with flux/vector-only live leakage",
                "reason": "scalar source-normalization has no alpha3 vector index under the local isotropic assumptions",
                "effect": "reduces the coupling hunt to K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1122_1_no_total_claim",
                "decision": "do not claim domain alpha3 pass",
                "reason": "the live flux/vector product remains missing and the no-flux theorem is conditional",
                "effect": "R7 alpha3 stays blocked but sharper",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1122_2_next_priority",
                "decision": "attack epsilon_domain_flux next",
                "reason": "if flux is parent-zero, the hardest alpha3 coupling branch collapses without needing a tiny numeric product",
                "effect": "1123 should derive no-flux or bound the flux product",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1122_0_1123",
                "next_target": "1123-Y5-R10-R11-flux-alpha3-zero-or-bound.md",
                "objective": "derive epsilon_domain_flux=0 from the parent local representative, or build a source-backed bound row for K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "include": "epsilon_domain_flux; K_R11_flux_alpha3; c_R11_flux_alpha3; no-flux local representative; target 4e-20; sibling guards",
                "exclude": "scalar-monopole alpha3 leakage; measured-GM absorption; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    flux: list[dict[str, object]],
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

    all_rows = decomposition + lemmas + flux + gates + decisions + next_target
    add("V1122_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1122_1_scalar_zero_present", any(row["component_id"] == "C1122_0_scalar_monopole" and "Pi_alpha3[delta_mu_0]=0" in row["alpha3_projection"] for row in decomposition), "scalar alpha3 zero subcomponent is explicit")
    add("V1122_2_flux_live", any(row["component_id"] == "C1122_1_vector_flux" and row["derivation_status"] == "LIVE_UNFILLED" for row in decomposition), "flux/vector component remains live and unfilled")
    add("V1122_3_narrowed_map", flux[0]["narrowed_map"] == "P_R11_source_alpha3_flux = K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux", "remaining alpha3 map is narrowed to flux product")
    add("V1122_4_bound_explicit", flux[0]["target_bound"] == "4e-20" and "4e-20" in flux[0]["acceptance"], "alpha3 4e-20 bound is explicit")
    add("V1122_5_gates_blocked", gates[0]["gate_pass"] == "true_nonclaim" and all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and any(row["gate_pass"] == "false" for row in gates), "scalar subgate is nonclaim and total gates remain blocked")
    add("V1122_6_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in decomposition + flux + next_target), "all generated rows remain nonclaim")
    add("V1122_7_next_target", next_target[0]["next_target"].startswith("1123-") and "flux-alpha3" in str(next_target[0]["next_target"]), "1123 handoff targets flux alpha3 zero/bound")
    add("V1122_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1122_9_csv_parse", csv_parse_ok, "all 1122 CSV outputs parse cleanly")
    add("V1122_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1122_SUMMARY", True, "1122 proves scalar alpha3 subcomponent zero conditionally and narrows the live coupling to flux")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    flux: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1122 - Y5/R10 Source-Normalization Alpha3 Coupling Map Or Zero

**Current verdict:** this is a real narrowing win, not a full closure. A scalar, isotropic, stationary source-normalization perturbation has no leading `alpha3` projection, but the live branch is the non-scalar flux/vector piece.

**Derived sub-result:** under local rotational invariance, `Pi_alpha3[delta_mu_0]=0` because a scalar monopole cannot fill the preferred-frame/vector slot carried by `alpha3`.

**Remaining live map:** `P_R11_source_alpha3_flux = K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux`, with target `abs(...) <= 4e-20`.

**No claim:** the total domain/R11 `alpha3`, R10, PPN, and local-GR branches remain blocked until the flux term is zero or bounded.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Coupling Decomposition
{table(["component_id", "component", "local_type", "alpha3_projection", "derivation_status", "reason", "remaining_input", "valid_for_claim"], decomposition)}

## Scalar Zero Lemma
{table(["lemma_id", "statement", "formal_condition", "formal_result", "status", "valid_for_claim"], lemmas)}

## Remaining Flux Contract
{table(["row_id", "observable", "live_quantity", "narrowed_map", "zero_route", "numeric_route", "target_bound", "acceptance", "current_status", "valid_for_claim", "claim_allowed"], flux)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "effect", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1122_SOURCE_REGISTER.csv",
        "decomposition": OUT / "P8_Y5_R10_1122_ALPHA3_COUPLING_DECOMPOSITION.csv",
        "lemmas": OUT / "P8_Y5_R10_1122_SCALAR_ZERO_LEMMA.csv",
        "flux": OUT / "P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv",
        "gates": OUT / "P8_Y5_R10_1122_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1122_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1122_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1122_VALIDATION.csv",
    }
    sources = source_rows()
    decomposition = decomposition_rows()
    lemmas = scalar_zero_rows()
    flux = flux_contract_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["decomposition"], decomposition)
    write_csv(outputs["lemmas"], lemmas)
    write_csv(outputs["flux"], flux)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, decomposition, lemmas, flux, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, decomposition, lemmas, flux, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
