from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4055-Y5-R2FR-Hilbert-owner-DGK-zero-and-trace-background-subtraction.md"

SOURCES = {
    "SRC4055_00_4053_reduction": (
        ROOT / "4053-Y5-R2FR-q-loc-Khat-projector-silence-reduction.md",
        "D_GK=0",
    ),
    "SRC4055_01_4054_hinge": (
        ROOT / "4054-Y5-R2FR-scalar-charge-zero-and-improvement-normalization.md",
        "unit-response scalar",
    ),
    "SRC4055_02_metric_contract": (
        SOURCE_DIR / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
        "K_hat is exactly the metric response",
    ),
    "SRC4055_03_stress_candidate": (
        SOURCE_DIR / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
        "S_GK = - integral sqrt(-g) Gamma_eff",
    ),
    "SRC4055_04_first_variation": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
        "There exists a local diffeomorphism-invariant scalar action",
    ),
    "SRC4055_05_stress_rewrite": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
        "T_GK^{mu nu} := Gamma_eff g^{mu nu} - K_hat^{mu nu}",
    ),
    "SRC4055_06_integrability": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv",
        "metric variation of a scalar density",
    ),
    "SRC4055_07_ward": (
        SOURCE_DIR / "P8_Y5_R2FR_3950_GK_WARD_QLOC_ZERO_THEOREM.csv",
        "If K_hat is the metric response",
    ),
    "SRC4055_08_gamma_variation": (
        SOURCE_DIR / "P8_Y5_R2FR_3953_MINIMAL_GAMMA_VARIATION.csv",
        "Gamma_quad = Gamma0",
    ),
    "SRC4055_09_canonical_sgk": (
        SOURCE_DIR / "P8_Y5_R2FR_4023_CANONICAL_SGK_ACTION_ATTEMPT.csv",
        "D_GK^{mu nu}:=Gamma_eff",
    ),
    "SRC4055_10_symbol_match": (
        SOURCE_DIR / "P8_Y5_R2FR_4024_GK_SYMBOL_MATCH_MATRIX.csv",
        "current_evidence",
    ),
    "SRC4055_11_density_candidate": (
        SOURCE_DIR / "P8_Y5_R2FR_4026_EXPLICIT_GAMMA_DENSITY_CANDIDATE.csv",
        "vacuum subtraction",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4055_SOURCE_REGISTER.csv",
    "hilbert_definition": SOURCE_DIR / "P8_Y5_R2FR_4055_HILBERT_RESPONSE_DEFINITION.csv",
    "dgk_zero": SOURCE_DIR / "P8_Y5_R2FR_4055_DGK_ZERO_CERTIFICATE.csv",
    "trace_subtraction": SOURCE_DIR / "P8_Y5_R2FR_4055_TRACE_BACKGROUND_SUBTRACTION_LAW.csv",
    "helmh_double_zero": SOURCE_DIR / "P8_Y5_R2FR_4055_HELMHOLTZ_DOUBLE_ZERO_GATE.csv",
    "fallback_bounds": SOURCE_DIR / "P8_Y5_R2FR_4055_FALLBACK_BOUND_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4055_EVALUATOR_RESULTS.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4055_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4055_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4055_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4055_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle) in SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_present": contains(path, needle),
                "use_in_4055": "Hilbert_owner_DGK_zero_trace_subtraction",
                "timestamp_utc": ts,
            }
        )
    return rows


def hilbert_definition_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "definition_id": "HRD4055_0_renormalized_density",
            "object": "Gamma_ren",
            "formula": "Gamma_ren := Gamma_eff - Gamma_0 - Gamma_ref, with Gamma_ren(Phi0)=0 and dGamma_ren|Phi0=0",
            "meaning": "The compact local branch sees only deviations from the fixed vacuum/reference density.",
            "status": "PARENT_PACKET_DEFINITION_CANDIDATE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "definition_id": "HRD4055_1_parent_action",
            "object": "S_GK",
            "formula": "S_GK[g,Y] := - int_M sqrt|g| Gamma_ren(g,Y,nablaY,D) + B_GK[g,Y]",
            "meaning": "This makes Gamma/Khat a variational sector rather than a bookkeeping pair.",
            "status": "LOCAL_DIFFEOMORPHIC_ACTION_CANDIDATE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "definition_id": "HRD4055_2_Hilbert_stress",
            "object": "T_Hilbert_GK",
            "formula": "T_Hilbert_GK^{mu nu}:=(-2/sqrt|g|) delta S_GK/delta g_{mu nu}",
            "meaning": "Because it is a Hilbert stress of a scalar action, the Helmholtz/integrability condition is automatic for this candidate.",
            "status": "HILBERT_OWNER_DEFINED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "definition_id": "HRD4055_3_metric_response_Khat",
            "object": "K_Gamma",
            "formula": "K_Gamma^{mu nu}:=Gamma_ren g^{mu nu}-T_Hilbert_GK^{mu nu}",
            "meaning": "This is the sign-safe definition of the Khat metric-response convention.",
            "status": "RESPONSE_CONVENTION_FIXED_FOR_CANDIDATE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "definition_id": "HRD4055_4_live_adoption_clause",
            "object": "Khat adoption",
            "formula": "Khat^{mu nu} := K_Gamma^{mu nu} through local <=2PN order",
            "meaning": "If adopted, D_GK is not a free residual; it is exactly zero by definition of the parent response.",
            "status": "ADOPTION_CLAUSE_NOT_YET_MAIN_CORPUS_SIGNED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def dgk_zero_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "certificate_id": "DGK4055_0_residual_definition",
            "object": "D_GK",
            "formula": "D_GK^{mu nu}:=Gamma_ren g^{mu nu}-Khat^{mu nu}-T_Hilbert_GK^{mu nu}",
            "result": "D_GK measures only failure of live Khat to equal the parent metric response.",
            "status": "EXACT_RESIDUAL_SPLIT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "certificate_id": "DGK4055_1_zero_if_adopted",
            "object": "D_GK",
            "formula": "if Khat=K_Gamma, then D_GK=Gamma_ren g-(Gamma_ren g-T_Hilbert_GK)-T_Hilbert_GK=0",
            "result": "The nonvariational Helmholtz defect is killed inside the candidate parent packet.",
            "status": "ALGEBRAIC_ZERO_UNDER_ADOPTION",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "certificate_id": "DGK4055_2_Ward_consequence",
            "object": "q_loc",
            "formula": "q_loc^nu=P_loc nabla_mu T_Hilbert_GK^{mu nu}=P_loc(sum_A E_A nabla^nu Y^A + boundary/source identities)",
            "result": "With Euler/no-source/no-boundary clauses from 4054 and PPC4048, q_loc bulk leakage vanishes.",
            "status": "CONDITIONAL_WARD_REDUCTION",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "certificate_id": "DGK4055_3_what_remains",
            "object": "live symbol match",
            "formula": "current corpus symbol Khat ?= K_Gamma",
            "result": "4055 supplies the exact parent-adoption contract; it does not claim older Khat symbols were already this object.",
            "status": "PRIVATE_CANDIDATE_NOT_PUBLIC_MATCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def trace_subtraction_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "law_id": "TBS4055_0_constant_background",
            "object": "Gamma_0",
            "formula": "nabla^nu Gamma_0=0 and delta Gamma_0=0 in compact local variations",
            "result": "A constant vacuum/background density cannot create a local q_loc force.",
            "status": "TRACE_FORCE_ZERO",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "law_id": "TBS4055_1_cosmological_channel",
            "object": "volume trace",
            "formula": "delta int sqrt|g| Gamma_0 gives pure trace proportional to Gamma_0 g^{mu nu}",
            "result": "The pure trace is routed to fixed Lambda/background subtraction, not to compact source mass.",
            "status": "BACKGROUND_CHANNEL_NOT_LOCAL_SOURCE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "law_id": "TBS4055_2_renormalized_fixed_point",
            "object": "Gamma_ren",
            "formula": "Gamma_ren=O(Y^2,nablaY^2) and dGamma_ren|Y=0=0",
            "result": "The local fixed point has no linear trace prefactor and no F_1 source-normalization hair.",
            "status": "DOUBLE_ZERO_TRACE_LAW",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "law_id": "TBS4055_3_forbidden_drift",
            "object": "trace drift",
            "formula": "D_source Gamma_0=D_range Gamma_0=D_domain Gamma_0=D_memory Gamma_0=0",
            "result": "Measured GM, radial range, source selection, or readout success cannot re-fit the background trace.",
            "status": "READOUT_FIREWALL_TRACE_RULE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def helmh_double_zero_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "HDZ4055_0_Helmholtz",
            "gate": "inverse-variational integrability",
            "result": "pass inside candidate packet because T_Hilbert_GK is defined by second variation of S_GK",
            "remaining": "live corpus must adopt Khat=K_Gamma",
            "status": "CANDIDATE_PASS_NOT_LIVE_MATCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "HDZ4055_1_double_zero",
            "gate": "T_GK(Phi0)=0 and first variation zero",
            "result": "pass for Gamma_ren quadratic/fixed-point branch after Gamma_0 subtraction",
            "remaining": "parent-sign that local response carriers Y vanish/no-hair in compact exterior",
            "status": "CANDIDATE_PASS_IF_4054_AND_NOHAIR_CLAUSES_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "HDZ4055_2_trace",
            "gate": "constant trace cannot be local source",
            "result": "pass if Gamma_0 is fixed background/Lambda data before variation and readout",
            "remaining": "formal adoption in parent packet",
            "status": "CANDIDATE_TRACE_PASS",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "HDZ4055_3_q_loc",
            "gate": "PPC4048_7 closure pressure",
            "result": "PPC4048_7 is reduced to formal adoption of this Hilbert-response packet plus prior boundary/source/projector clauses",
            "remaining": "integrate clauses into one formal parent packet and retain fallback if rejected",
            "status": "REDUCED_TO_ADOPTION_GATE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def fallback_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "FB4055_0_live_Khat_mismatch",
            "if_clause_fails": "live Khat is not K_Gamma",
            "formula": "Delta_K^{mu nu}:=K_Gamma^{mu nu}-Khat^{mu nu}; |q_loc| <= ||P_loc|| |nabla_mu Delta_K^{mu nu}| plus Euler/boundary terms",
            "observable_map": "PPN beta/gamma q_loc tail; R10 alpha(lambda); source-exchange",
            "needed_inputs": "Delta_K component profile, length scale, PPN/R10 projector coefficients",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "FB4055_1_trace_drift",
            "if_clause_fails": "Gamma_0 or trace subtraction depends on source/range/readout",
            "formula": "|q_loc|_trace <= ||P_loc|| |nabla Gamma_trace_drift|",
            "observable_map": "Gdot/G, radial G, clock/orbital source-normalization residual",
            "needed_inputs": "trace drift derivatives and same-frame normalization",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "FB4055_2_nonquadratic_linear_term",
            "if_clause_fails": "Gamma_ren has a linear term around the fixed point",
            "formula": "Gamma_ren = a_A Y^A + O(Y^2) gives F_1 proportional to a_A",
            "observable_map": "linear fifth-force/source-normalization leakage",
            "needed_inputs": "a_A coefficients, carrier field profile, no-hair constants",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def static_rows(ts: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "evaluator": [
            {
                "case_id": "CASE4055_0",
                "verdict": "DGK_ZERO_ROUTE_CONSTRUCTED_CONDITIONALLY",
                "result": "If the parent packet adopts Khat as the metric response K_Gamma of the renormalized Gamma density, D_GK is algebraically zero.",
                "what_moved": "The nonvariational defect is no longer vague; it is exactly the live-symbol mismatch Delta_K.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            },
            {
                "case_id": "CASE4055_1",
                "verdict": "TRACE_BACKGROUND_LAW_CONSTRUCTED",
                "result": "Gamma_0 is routed to fixed background/Lambda subtraction; Gamma_ren carries only quadratic local deviations.",
                "what_moved": "The trace sector is prevented from becoming a hidden radial/source prefactor.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            },
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4055_0_private_progress",
                "claim": "D_GK=0 and trace subtraction have conditional parent-packet derivations",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "parent adoption is not yet formalized as the live MTS action",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4055_1_live_q_loc_closed",
                "claim": "q_loc/Khat is fully closed for current live MTS symbols",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "4055 defines the adoption contract; it does not prove old Khat symbols already matched it",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4055_2_local_GR",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "formal parent-packet adoption and unified no-boundary/source/projector clause integration remain",
                "timestamp_utc": ts,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4055_0",
                "next_doc": "4056-Y5-R2FR-parent-local-action-packet-integration-or-DeltaK-bound.md",
                "next_script": "scripts/Y5_R2FR_4056_parent_local_action_packet_integration_or_DeltaK_bound.py",
                "reason": "The local route now needs one integrated parent packet: EH + matter/EM + Gamma_ren/K_Gamma + no-source-boundary/projector clauses, or a Delta_K bound if adoption is rejected.",
                "timestamp_utc": ts,
            }
        ],
        "status": [
            {
                "status_id": "STAT4055",
                "status": "HILBERT_RESPONSE_DGK_ZERO_AND_TRACE_SUBTRACTION_CONDITIONAL_ROUTE_BUILT",
                "public_claim": False,
                "formalization_modified_by_4055": False,
                "timestamp_utc": ts,
            }
        ],
    }


def script_compiles() -> bool:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def csv_parse_ok(path: Path) -> Tuple[bool, str]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"rows={len(rows)}"
    except Exception as exc:
        return False, repr(exc)


def validation_rows(
    sources: List[Dict[str, object]],
    generated_csvs: List[Path],
    all_rows: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    parse_results = [csv_parse_ok(path) for path in generated_csvs]
    flat_rows = [row for table in all_rows for row in table]
    serialized = "\n".join(str(value) for row in flat_rows for value in row.values())
    outputs_in_formalization = [path for path in OUTPUTS.values() if FORMALIZATION in path.parents]
    return [
        {
            "check_id": "VAL4055_00_sources_exist",
            "passed": all(bool(row["exists"]) for row in sources),
            "detail": "all cited local source paths exist",
        },
        {
            "check_id": "VAL4055_01_needles_present",
            "passed": all(bool(row["needle_present"]) for row in sources),
            "detail": "all source needles present",
        },
        {
            "check_id": "VAL4055_02_csv_parse",
            "passed": all(result for result, _detail in parse_results),
            "detail": "; ".join(f"{path.name}:{detail}" for path, (_ok, detail) in zip(generated_csvs, parse_results)),
        },
        {
            "check_id": "VAL4055_03_no_public_claim",
            "passed": "allowed_public': True" not in serialized and "valid_for_public_claim': True" not in serialized,
            "detail": "all claim-bearing rows preserve public false",
        },
        {
            "check_id": "VAL4055_04_no_missing_markers",
            "passed": "MISSING_" not in serialized,
            "detail": "outputs use explicit open/blocker language instead of MISSING markers",
        },
        {
            "check_id": "VAL4055_05_no_formalization_outputs",
            "passed": len(outputs_in_formalization) == 0,
            "detail": "4055 writes only post-checkpoint/source-intake outputs",
        },
        {
            "check_id": "VAL4055_06_script_compiles",
            "passed": script_compiles(),
            "detail": "script compiles",
        },
    ]


def doc_text(ts: str) -> str:
    return """# 4055 - Hilbert Owner, D_GK Zero, and Trace/Background Subtraction

- Timestamp: `__TS__`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## What Actually Moved

4053 left `D_GK=0` and trace/background subtraction as the sharp remaining `q_loc` blockers. 4055 turns them into a parent-action contract.

Define the renormalized local density:

```text
Gamma_ren := Gamma_eff - Gamma_0 - Gamma_ref,
Gamma_ren(Phi0)=0,    d Gamma_ren|Phi0=0.
```

Then define the parent sector:

```text
S_GK[g,Y] := - int sqrt|g| Gamma_ren(g,Y,nablaY,D) + B_GK[g,Y],
T_Hilbert_GK^{mu nu}:=(-2/sqrt|g|) delta S_GK/delta g_{mu nu},
K_Gamma^{mu nu}:=Gamma_ren g^{mu nu}-T_Hilbert_GK^{mu nu}.
```

If the live local branch adopts

```text
Khat^{mu nu}:=K_Gamma^{mu nu},
```

then the mismatch is algebraically zero:

```text
D_GK^{mu nu}
= Gamma_ren g^{mu nu}-Khat^{mu nu}-T_Hilbert_GK^{mu nu}
= 0.
```

That means the Helmholtz/integrability issue is not a handwave: inside this candidate packet, `T_GK` is a Hilbert stress by construction.

## Trace Rule

The constant piece `Gamma_0` is fixed background/Lambda/reference data:

```text
nabla Gamma_0 = 0,
delta_local Gamma_0 = 0,
D_source Gamma_0 = D_range Gamma_0 = D_readout Gamma_0 = 0.
```

So it cannot be used as compact local mass, radial `G`, or a source-dependent prefactor. The only local `q_loc` carrier is `Gamma_ren`, and the quadratic/fixed-point rule makes its first variation vanish.

## Honest Status

This is a real derivation path, not another missing-list. But it is still conditional: 4055 defines the exact parent adoption contract. It does not prove the older live `Khat` symbols were already `K_Gamma`.

If adoption is rejected, the fallback is now exact:

```text
Delta_K^{mu nu}:=K_Gamma^{mu nu}-Khat^{mu nu},
|q_loc| <= ||P_loc|| |nabla_mu Delta_K^{mu nu}| + Euler/boundary/source terms.
```

## Next Target

Build the integrated local parent packet: EH + same-source matter/EM + `Gamma_ren/K_Gamma` + no-source-boundary/projector clauses. If the packet cannot be adopted cleanly, run the `Delta_K` bound branch.
""".replace("__TS__", ts)


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(ts)
    hilbert_definition = hilbert_definition_rows(ts)
    dgk_zero = dgk_zero_rows(ts)
    trace_subtraction = trace_subtraction_rows(ts)
    helmh_double_zero = helmh_double_zero_rows(ts)
    fallback = fallback_rows(ts)
    static = static_rows(ts)

    DOC_PATH.write_text(doc_text(ts), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["hilbert_definition"], hilbert_definition)
    write_csv(OUTPUTS["dgk_zero"], dgk_zero)
    write_csv(OUTPUTS["trace_subtraction"], trace_subtraction)
    write_csv(OUTPUTS["helmh_double_zero"], helmh_double_zero)
    write_csv(OUTPUTS["fallback_bounds"], fallback)
    write_csv(OUTPUTS["evaluator"], static["evaluator"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["hilbert_definition"],
        OUTPUTS["dgk_zero"],
        OUTPUTS["trace_subtraction"],
        OUTPUTS["helmh_double_zero"],
        OUTPUTS["fallback_bounds"],
        OUTPUTS["evaluator"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    all_rows = [
        sources,
        hilbert_definition,
        dgk_zero,
        trace_subtraction,
        helmh_double_zero,
        fallback,
        static["evaluator"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, all_rows)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
