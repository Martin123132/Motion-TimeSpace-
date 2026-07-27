from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "930-Y5-R10-KBFH-coupling-origin-minimal-input-contract-or-first-scoreable-bound-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def is_float(value: str) -> bool:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(parsed)


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "924_doc",
            "path": "924-Y5-R10-Hamiltonian-mass-charge-normalization-contract-or-FM-bound-row-expansion.md",
            "role": "symbolic BF/source variation and K_BF_H ratio origin",
            "needle": "k_M dB_M = K_BF_H J_H^H",
        },
        {
            "source_id": "925_doc",
            "path": "925-Y5-R10-KBFH-over-kM-ratio-from-source-worldtube-or-FM-bound-row-fill.md",
            "role": "R_BJ symbolic ratio isolation and blocker list",
            "needle": "R_BJ :=",
        },
        {
            "source_id": "926_doc",
            "path": "926-Y5-R10-BM-charge-unit-quantization-or-source-worldtube-equality-proof.md",
            "role": "conditional compact BF lattice theorem",
            "needle": "K_BF_H/k_M = R_BJ = N_B/N_H",
        },
        {
            "source_id": "927_doc",
            "path": "927-Y5-R10-compact-BF-lattice-parent-action-contract-or-JHH-source-proof.md",
            "role": "normalized compact BF parent-action contract",
            "needle": "S_M = 2*pi*k_M",
        },
        {
            "source_id": "928_doc",
            "path": "928-Y5-R10-instantiate-compact-BF-lattice-or-retain-KBFH-residual-bound-row.md",
            "role": "current compact BF instantiation failure and residual fallback",
            "needle": "compact BF lattice route does not instantiate",
        },
        {
            "source_id": "929_doc",
            "path": "929-Y5-R10-KBFH-residual-bound-runner-smoke-or-compact-period-proof.md",
            "role": "strict smoke runner contract",
            "needle": "scoreable(row) requires",
        },
        {
            "source_id": "929_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_929_VALIDATION.csv",
            "role": "proves 929 runner validation passed",
            "needle": "V929_12_validation_rows_ready",
        },
        {
            "source_id": "537_worldtube_contract",
            "path": "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
            "role": "same Hilbert/topological worldtube source glue contract",
            "needle": "PAC537_5_Hilbert_topological_charge_equality",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def derivation_chain() -> list[dict[str, str]]:
    rows = [
        {
            "chain_id": "KD930_0_parent_variation",
            "step": "vary mass-gauge source action",
            "mathematical_form": "S_M = k_M int B_M wedge dA_M + K_BF_H int A_M wedge J_H^H; delta_A S_M => k_M dB_M = K_BF_H J_H^H",
            "derived_if_true": "K_BF_H is tied to source-current normalization rather than fit after the fact",
            "current_status": "symbolic_action_written_not_current_parent_signed",
            "missing_input": "MTS parent action with A_M, B_M, J_H^H units and orientation fixed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "KD930_1_chain_integral",
            "step": "integrate over linked source chain",
            "mathematical_form": "K_BF_H/k_M = R_BJ = (int_boundaryC B_M)/(int_C J_H^H)",
            "derived_if_true": "the coupling bottleneck becomes a boundary/source charge ratio",
            "current_status": "exact_symbolic_ratio_lock",
            "missing_input": "numeric/unit-complete B_M boundary charge and Hilbert source charge",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "KD930_2_compact_lattice",
            "step": "normalize compact BF fields",
            "mathematical_form": "a_M=A_M/(2*pi), b_M=B_M/(2*pi), int_boundaryC b_M=N_B, int_C j_H^H=N_H",
            "derived_if_true": "K_BF_H/k_M = N_B/N_H up to orientation",
            "current_status": "conditional_theorem_only",
            "missing_input": "compact periods, large-gauge invariance, integral source lattice",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "KD930_3_same_worldtube",
            "step": "tie BF charge to observed Hilbert worldtube",
            "mathematical_form": "partial C links W_source=supp(J_H[e_obs]); Pi_M J_H = J_M_top + dB_zero with R_eq=0 or bounded",
            "derived_if_true": "the topological charge is the measured source charge, not the wrong conserved object",
            "current_status": "not_derived",
            "missing_input": "same observed coframe, source support certificate, Hilbert-topological charge equality",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "KD930_4_minimal_source_special_case",
            "step": "single minimal same-class source",
            "mathematical_form": "if N_B=N_H=1 then K_BF_H/k_M=+/-1",
            "derived_if_true": "the coupling becomes a normalization theorem",
            "current_status": "reference_target_not_evidence",
            "missing_input": "minimal source normalization and no hidden extra charge sectors",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "KD930_5_weak_field_residual_amplitude",
            "step": "translate coupling to local residual pressure",
            "mathematical_form": "epsilon_FM = |K_BF_H| X_FM, X_FM := |A_M||dPiMJ_leak|/N_FM + |B_zero_flux|/N_B",
            "derived_if_true": "local tests can bound or score the coupling without absorbing it into G or M",
            "current_status": "not_numeric",
            "missing_input": "A_M norm, dPiMJ leak, B_zero_flux, N_FM, N_B, units",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def minimal_input_contract() -> list[dict[str, str]]:
    specs = [
        ("MIN930_0_parent_action_block", "own the mass-gauge sector in the parent action", "S_M with A_M, B_M, J_H^H and orientation", "prevents K_BF_H being an inserted fit constant"),
        ("MIN930_1_compact_periods", "fix compact periods or explicitly reject compact route", "int da_M, int b_M lattice with large-gauge invariance", "decides whether N_B/N_H theorem is available"),
        ("MIN930_2_BM_boundary_unit", "define B_M boundary charge unit", "int_boundaryC B_M = q_B N_B", "sets numerator of R_BJ"),
        ("MIN930_3_JHH_source_unit", "define Hilbert source lattice unit", "int_C J_H^H = q_H N_H = Q_tau = M_source", "sets denominator of R_BJ"),
        ("MIN930_4_same_worldtube_certificate", "prove B_M and J_H link the same source worldtube", "partial C links W_source and no extra charge sector contributes", "blocks wrong-charge topological credit"),
        ("MIN930_5_Gauss_Poisson_readout", "derive measured weak-field GM from same charge", "g_00=-1+2G_ref M_source/r+O(r^-2)", "connects Newton limit to source normalization"),
        ("MIN930_6_XFM_amplitude", "compute X_FM in epsilon_FM=|K_BF_H|X_FM", "A_M norm, dPiMJ leak, B_zero_flux, N_FM, N_B", "turns coupling into local residual amplitude"),
        ("MIN930_7_arena_projection", "compute C_arena_FM for at least one local observable", "Delta O_i = C_i epsilon_FM", "makes a first bound row scoreable"),
    ]
    return [
        {
            "input_id": input_id,
            "requirement": requirement,
            "mathematical_object": obj,
            "why_needed": why,
            "current_status": "missing_or_contract_only",
            "acceptable_evidence": "parent derivation, source-backed coefficient row, or explicit bounded residual with units",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for input_id, requirement, obj, why in specs
    ]


def symbolic_bound_envelope(smoke_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in smoke_rows:
        local = row["local_bound_row"]
        numeric_bound = is_float(row["upper_bound"])
        if local == "R10_fifth_force":
            epsilon_bound = "|epsilon_FM(lambda)| <= alpha_bound(lambda)/|C_R10_FM(lambda)|"
            kbfh_bound = "|K_BF_H(lambda)| <= alpha_bound(lambda)/(|C_R10_FM(lambda)| X_FM(lambda))"
            first_score_rank = "not_candidate_until_curve_and_range_law_exist"
        else:
            epsilon_bound = f"|epsilon_FM| <= {row['upper_bound']}/|C_{local}_FM|"
            kbfh_bound = f"|K_BF_H| <= {row['upper_bound']}/(|C_{local}_FM| X_FM)"
            first_score_rank = {
                "R3_gamma": "selected_first_candidate_direct_metric_PPN",
                "R4_beta": "second_candidate_direct_metric_PPN",
                "R2_clock_redshift": "third_candidate_clock_readout",
                "R1_WEP_source_charge": "powerful_but_species_projection_harder",
            }.get(local, "later_candidate_specialized_projection")
        rows.append(
            {
                "envelope_id": row["smoke_id"].replace("SMOKE929", "ENV930"),
                "local_bound_row": local,
                "observable": row["observable"],
                "bound_numeric": b(numeric_bound),
                "epsilon_bound_form": epsilon_bound,
                "KBFH_bound_form": kbfh_bound,
                "first_score_rank": first_score_rank,
                "missing_before_score": row["missing_inputs"],
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def first_scoreable_row_audit(envelopes: list[dict[str, str]]) -> list[dict[str, str]]:
    candidates = [
        ("R3_gamma", "selected", "direct metric PPN coefficient; numeric bound; avoids species-composition WEP map and R10 curve digitization"),
        ("R4_beta", "backup", "also direct metric PPN but second order/nonlinear source terms make it slightly harder"),
        ("R2_clock_redshift", "backup", "clock readout is valuable but coframe/frequency projection adds an extra layer"),
        ("R1_WEP_source_charge", "defer", "strongest bound but needs differential source-charge map between materials"),
        ("R10_fifth_force", "defer", "needs alpha(lambda), range law, and real curve before even symbolic scoring is clean"),
    ]
    available = {row["local_bound_row"]: row for row in envelopes}
    rows = []
    for row_id, decision, reason in candidates:
        envelope = available.get(row_id)
        rows.append(
            {
                "audit_id": f"FS930_{len(rows)}_{row_id}",
                "local_bound_row": row_id,
                "decision": decision,
                "reason": reason,
                "bound_form": envelope["KBFH_bound_form"] if envelope else "missing_envelope",
                "next_needed": "derive C_gamma_FM and X_FM" if row_id == "R3_gamma" else "not selected first",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC930_0_coupling_not_solved",
            "decision": "K_BF_H remains explicit residual",
            "reason": "symbolic ratio and conditional compact theorem exist, but parent units/source lattice are not signed",
            "consequence": "no local-GR, Newton, WEP, PPN, or R10 pass is claimed",
            "next_action": "derive C_gamma_FM and X_FM or close compact-period source theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC930_1_first_scoreable_row",
            "decision": "target R3_gamma first if derivation stalls",
            "reason": "gamma is a direct metric PPN observable with numeric bound and fewer species/range complications",
            "consequence": "next empirical fallback becomes a symbolic K_BF_H bound envelope, not a pass claim",
            "next_action": "931-Y5-R10-gamma-PPN-projection-coefficient-or-KBFH-bound-envelope.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC930_2_derivation_priority",
            "decision": "prefer parent derivation over empirical fitting",
            "reason": "a unified-field claim needs K_BF_H derived or sharply bounded without hidden G/M absorption",
            "consequence": "compact/source-worldtube proof remains live but cannot be promoted without new parent clauses",
            "next_action": "write gamma projection theorem and keep compact proof as parallel route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE930_0_KBFH_derived",
            "claim": "K_BF_H/k_M is derived numerically",
            "evidence": "R_BJ symbolic only; compact N_B/N_H theorem conditional only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE930_1_first_row_scoreable",
            "claim": "at least one local bound row is scoreable",
            "evidence": "R3_gamma selected as target, but C_gamma_FM and X_FM are not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE930_2_Newton_GR_reduction",
            "claim": "Newton/local GR reduction follows from the coupling branch",
            "evidence": "Gauss/Poisson readout and PPN projection remain in the minimal input contract",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            count += 1
    return count


def validation(
    sources: list[dict[str, str]],
    chain: list[dict[str, str]],
    contract: list[dict[str, str]],
    envelopes: list[dict[str, str]],
    first_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": stamp()})

    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    v929 = read_csv(OUT / "P8_Y5_BRR545_929_VALIDATION.csv")
    v929_clean = v929 and all(row.get("result") == "pass" for row in v929)
    ratio_chain_ok = any(row["chain_id"] == "KD930_1_chain_integral" and "R_BJ" in row["mathematical_form"] for row in chain)
    no_chain_claim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in chain)
    contract_complete = len(contract) == 8 and all(row["valid_for_claim"] == "false" for row in contract)
    envelope_complete = len(envelopes) == 10 and all(row["claim_allowed"] == "false" for row in envelopes)
    gamma_selected = any(row["local_bound_row"] == "R3_gamma" and row["decision"] == "selected" for row in first_rows)
    r10_deferred = any(row["local_bound_row"] == "R10_fifth_force" and row["decision"] == "defer" for row in first_rows)
    decisions_nonclaim = decision_rows and all(row["valid_for_claim"] == "false" for row in decision_rows)
    gates_false = gates and all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates)
    fw_changed = formalization_changed_after_start()
    next_ok = any("931-Y5-R10-gamma-PPN" in row["next_action"] for row in decision_rows)

    add("V930_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present" if source_ok else "missing source path or needle")
    add("V930_1_prior_929_clean", v929_clean, "P8_Y5_BRR545_929_VALIDATION.csv clean")
    add("V930_2_ratio_chain_written", ratio_chain_ok, "K_BF_H/k_M = R_BJ chain is explicit")
    add("V930_3_no_chain_claim", no_chain_claim, "derivation chain remains nonclaim")
    add("V930_4_minimal_contract_complete", contract_complete, "eight minimal coupling inputs are listed")
    add("V930_5_symbolic_envelope_complete", envelope_complete, "ten symbolic local-bound envelopes written without scoring")
    add("V930_6_gamma_selected_first", gamma_selected, "R3_gamma selected as least-messy first scoreable row")
    add("V930_7_R10_deferred", r10_deferred, "R10 deferred until range law and real curve exist")
    add("V930_8_decisions_nonclaim", decisions_nonclaim, "decision rows are explicit nonclaim")
    add("V930_9_claim_gates_false", gates_false, "all claim gates remain false")
    add("V930_10_formalization_workbench_untouched", fw_changed == 0, f"formalization_changed_after_start={fw_changed}")
    add("V930_11_next_target_selected", next_ok, "931-Y5-R10-gamma-PPN-projection-coefficient-or-KBFH-bound-envelope.md")
    add("V930_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    chain: list[dict[str, str]],
    contract: list[dict[str, str]],
    envelopes: list[dict[str, str]],
    first_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    gates: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 930 - Y5/R10 KBFH Coupling Origin Minimal Input Contract Or First Scoreable Bound Row

Generated: `{stamp()}`

Status: `Y5_R10_930_KBFH_coupling_origin_contract_written_gamma_selected_first_scoreable_target_no_claim`

Claim ceiling: `minimal_input_contract_and_symbolic_bound_envelope_only_no_numeric_KBFH_no_local_GR_or_R10_pass`

## Result

The coupling problem is now pinned down to a small contract rather than a fog bank.

The current derivation chain gets as far as

```text
K_BF_H/k_M = R_BJ = (int_boundaryC B_M)/(int_C J_H^H),
```

and conditionally, if the compact BF lattice and same-worldtube source lattice are parent-signed,

```text
K_BF_H/k_M = N_B/N_H.
```

But current MTS still lacks the parent-signed compact periods, Hilbert source lattice, same-worldtube certificate, weak-field residual amplitude `X_FM`, and arena projection coefficients. So the coupling remains explicit and nonclaim.

If the derivation route stalls, the least-messy first empirical row is `R3_gamma`, because it is a direct metric PPN readout with a numeric bound and avoids both species-composition WEP ambiguity and R10 range-curve machinery.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Coupling Derivation Chain

{md_table(chain, ["chain_id", "step", "mathematical_form", "current_status", "missing_input", "claim_allowed"])}

## Minimal Input Contract

{md_table(contract, ["input_id", "requirement", "mathematical_object", "why_needed", "current_status", "valid_for_claim"])}

## Symbolic Bound Envelope

{md_table(envelopes, ["envelope_id", "local_bound_row", "bound_numeric", "KBFH_bound_form", "first_score_rank", "valid_for_claim"])}

## First Scoreable Row Audit

{md_table(first_rows, ["audit_id", "local_bound_row", "decision", "reason", "next_needed", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

`931-Y5-R10-gamma-PPN-projection-coefficient-or-KBFH-bound-envelope.md`

Try to derive `C_gamma_FM` and `X_FM` from the weak-field metric response. If that fails, write a nonclaim symbolic bound envelope:

```text
|K_BF_H| <= 2.3e-05 / (|C_R3_gamma_FM| X_FM).
```
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    smoke_rows = read_csv(OUT / "P8_Y5_R10_929_SMOKE_EVALUATION.csv")
    chain = derivation_chain()
    contract = minimal_input_contract()
    envelopes = symbolic_bound_envelope(smoke_rows)
    first_rows = first_scoreable_row_audit(envelopes)
    decision_rows = decisions()
    gates = claim_gates()
    validation_rows = validation(sources, chain, contract, envelopes, first_rows, decision_rows, gates)

    write_csv(
        OUT / "P8_Y5_R10_930_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_930_COUPLING_DERIVATION_CHAIN.csv",
        chain,
        ["chain_id", "step", "mathematical_form", "derived_if_true", "current_status", "missing_input", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_930_MINIMAL_INPUT_CONTRACT.csv",
        contract,
        ["input_id", "requirement", "mathematical_object", "why_needed", "current_status", "acceptable_evidence", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_930_SYMBOLIC_BOUND_ENVELOPE.csv",
        envelopes,
        ["envelope_id", "local_bound_row", "observable", "bound_numeric", "epsilon_bound_form", "KBFH_bound_form", "first_score_rank", "missing_before_score", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_930_FIRST_SCOREABLE_ROW_AUDIT.csv",
        first_rows,
        ["audit_id", "local_bound_row", "decision", "reason", "bound_form", "next_needed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_930_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_930_CLAIM_GATE.csv",
        gates,
        ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_930_NEXT_TARGET.csv",
        [
            {
                "next_target": "931-Y5-R10-gamma-PPN-projection-coefficient-or-KBFH-bound-envelope.md",
                "objective": "derive C_gamma_FM and X_FM for the direct metric PPN gamma row, or retain a symbolic K_BF_H bound envelope",
                "include": "weak-field metric response, PPN gamma projection coefficient, epsilon_FM amplitude inputs, no hidden G/M absorption",
                "exclude": "R10 range claim, WEP species claim, numeric K_BF_H without parent units, GitHub action, formalization-workbench edits",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        ],
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_930_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, chain, contract, envelopes, first_rows, decision_rows, gates, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")
    print("Y5_R10_930_KBFH_coupling_origin_contract_written_gamma_selected_first_scoreable_target_no_claim")
    print(f"wrote {DOC}")
    print("next target: 931-Y5-R10-gamma-PPN-projection-coefficient-or-KBFH-bound-envelope.md")


if __name__ == "__main__":
    main()
