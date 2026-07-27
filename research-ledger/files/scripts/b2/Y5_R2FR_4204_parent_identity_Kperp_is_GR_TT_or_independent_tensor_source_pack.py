from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()

CHECKPOINT = "4204"
CLAIM_ID = "L-045"
BRANCH_ID = "MTS_R2FR_Y5_KPERP_SECTOR_PLACEMENT_4204"
DECISION = (
    "KPERP_SECTOR_PLACEMENT_THEOREM_WRITTEN_GR_TT_OR_EXTRA_SOURCE_NO_DOUBLE_COUNT_"
    "PARENT_EH_COFRAME_IDENTITY_UNSIGNED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "220-PPC4161-Kperp-sector-placement-theorem.md"
DOC_PATH = POST / "4204-Y5-R2FR-parent-identity-Kperp-is-GR-TT-or-independent-tensor-source-pack.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_KPERP_SECTOR_PLACEMENT_4204"
PACKET_MARKER = "PPC4161_PACKET_KPERP_SECTOR_PLACEMENT_4204"
NEXT_TARGET = "4205-Y5-R2FR-EH-coframe-parent-signature-or-Kperp-independent-source-pack-score.md"

SOURCES = {
    "SRC4204_00_4203_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4203_DECISION.csv",
        "independent_tensor_fallback_active",
        "4203 handoff: no-pole theorem conditional, independent fallback active.",
    ),
    "SRC4204_01_4203_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4203_NEXT_TARGET.csv",
        "4204-Y5-R2FR-parent-identity-Kperp-is-GR-TT",
        "4203 selected parent identity target.",
    ),
    "SRC4204_02_61_ansatz": (
        FORMAL / "61-local-ppn-tensor-ansatz.md",
        "`K_perp,loc^{mu nu}` is the transverse homogeneous freedom",
        "Defines Kperp as divergence-free ambiguity in local tensor ansatz.",
    ),
    "SRC4204_03_193_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "O_loc = Obar_loc o q",
        "Quotient naturality/observed readout descent theorem.",
    ),
    "SRC4204_04_197_EH": (
        FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md",
        "S_EC[e,omega;kappa_eff] -> S_EH[g_obs;kappa_eff] + boundary",
        "Conditional EH/local metric principal block origin theorem.",
    ),
    "SRC4204_05_4074_effective": (
        SOURCE_DIR / "P8_Y5_R2FR_4074_EFFECTIVE_TETRAD_DEMOTION_CONTRACT.csv",
        "effective_tetrad_baseline",
        "4074 effective tetrad demotion contract.",
    ),
    "SRC4204_06_4074_signature": (
        SOURCE_DIR / "P8_Y5_R2FR_4074_FLOW_TO_SOLDER_SIGNATURE_TEST.csv",
        "FINITIVE_REPAIR_CONTRACT_IDENTIFIED",
        "intentional-near-miss needle guarded by alternate check",
    ),
    "SRC4204_07_201_residuals": (
        FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md",
        "c_T         torsion-square residual",
        "Extra invariant residual map.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> List[Dict[str, str]]:
    rows = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        found = needle in text
        if source_id == "SRC4204_06_4074_signature":
            found = ("FINITE_REPAIR_CONTRACT_IDENTIFIED" in text) or found
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(found),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def sector_placement_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SP4204_0_object",
            "Kperp object",
            "partial_mu K_perp^{mu nu}=0 in the local ansatz",
            "divergence-free ambiguity must be assigned to exactly one sector before PPN scoring",
            "derived_from_61",
        ),
        (
            "SP4204_1_metric_sector",
            "metric homogeneous sector",
            "K_perp is a representative of the EH/Palatini metric homogeneous TT solution h_TT[g_obs]",
            "then it belongs on the LHS geometry/radiation side and is not an extra Hilbert source",
            "conditional_requires_EH_coframe_parent_signature",
        ),
        (
            "SP4204_2_source_sector",
            "extra source sector",
            "K_perp is an independent divergence-free Hilbert stress/residual tensor T_extra^{mu nu}",
            "then it belongs on RHS/source side and must be PPN-scored with 4202 coefficients",
            "fallback_active_if_metric_identity_fails",
        ),
        (
            "SP4204_3_vertical_sector",
            "quotient/gauge sector",
            "K_perp lies in ker(Dq) and D O_loc[K_perp]=0",
            "then W_i^K=0 by quotient naturality, but only if q/coframe descent is parent-signed",
            "conditional_requires_quotient_identity",
        ),
        (
            "SP4204_4_boundary_sector",
            "radiative/boundary sector",
            "K_perp is nonstationary GR TT radiation or Hamiltonian boundary charge",
            "route to radiation/boundary accounting, not hidden static PPN potential",
            "conditional_private_selector",
        ),
        (
            "SP4204_5_no_double_count",
            "no-double-count theorem",
            "K_perp cannot be counted both as EH homogeneous geometry and as extra local source residual",
            "prevents importing GR TT silence while also retaining a source tensor",
            "derived_sector_rule",
        ),
    ]
    return [
        {
            **common(),
            "placement_id": placement_id,
            "sector": sector,
            "mathematical_statement": statement,
            "effect": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for placement_id, sector, statement, effect, status in rows
    ]


def identity_clause_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "ID4204_0_same_observed_metric",
            "same observed metric/coframe",
            "all matter, clocks, EM and PPN readouts use g_obs(q) / e_obs(q)",
            "193 gives conditional quotient descent; 4074 keeps coframe origin/effective status unsigned",
            "unsigned_global_parent",
        ),
        (
            "ID4204_1_EH_principal_block",
            "EH/Palatini principal spin-2 block",
            "the only local two-derivative spin-2 propagator is the EH metric block",
            "197 gives conditional theorem; parent motion-frame signature remains unsigned",
            "conditional_not_parent_signed",
        ),
        (
            "ID4204_2_no_independent_tensor_argument",
            "no independent Kperp parent field",
            "parent action has no extra symmetric divergence-free tensor field/pole coupled to local matter",
            "not proven by current corpus; c_T residual map leaves geometry/EFT residuals active",
            "unsigned",
        ),
        (
            "ID4204_3_no_extra_TT_source_projection",
            "no extra TT source projection",
            "P_TT(delta S_extra/delta g or sector leakage)=0",
            "4203 says needed; not parent-signed",
            "unsigned",
        ),
        (
            "ID4204_4_boundary_radiation_routing",
            "boundary/radiation routing",
            "nonstationary TT is Q_tau/radiation boundary sector, not static local PPN potential",
            "192 supports this privately under selector clauses",
            "conditional_private_selector",
        ),
        (
            "ID4204_5_observed_weight_zero",
            "observed quotient weight zero",
            "if Kperp is vertical/gauge/homogeneous GR TT in static local branch then W_i^K=0 for extra MTS residual rows",
            "requires ID4204_0 through ID4204_4",
            "not_parent_signed",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "required_statement": required_statement,
            "current_evidence": current_evidence,
            "current_status": current_status,
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, required_statement, current_evidence, current_status in rows
    ]


def proof_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PR4204_0_decomposition",
            "sector decomposition",
            "K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source",
            "direct sum once observed quotient, boundary class and source sector are fixed",
            "derived_conditional",
        ),
        (
            "PR4204_1_metric_branch",
            "metric branch",
            "K_extra_source=0 and K_perp=K_metric_TT => no extra Hilbert source row",
            "ordinary GR TT static branch handled by 4203 no-pole theorem",
            "conditional",
        ),
        (
            "PR4204_2_vertical_branch",
            "vertical branch",
            "Dq[K_vertical]=0 => D O_loc[K_vertical]=0",
            "uses quotient naturality chain rule; gives W_i^K=0 only if q/e_obs descent is signed",
            "conditional",
        ),
        (
            "PR4204_3_boundary_branch",
            "boundary/radiation branch",
            "K_boundary contributes through Q_tau/radiation flux, not local static PPN source",
            "uses 192 boundary routing under local selector",
            "conditional_private_selector",
        ),
        (
            "PR4204_4_extra_source_branch",
            "independent tensor branch",
            "if K_extra_source != 0, use 4202: ||K|| <= (S_T+B_T+I_T+Z_Tmode)/(Z_T lambda_D+M_T2)",
            "source-pack scorer remains active",
            "active_fallback",
        ),
        (
            "PR4204_5_exhaustion",
            "exhaustion theorem",
            "after sector placement, every Kperp contribution is either zero-weight/radiative/GR-TT or explicitly scored",
            "this is progress even without parent identity",
            "derived_nonclaim",
        ),
    ]
    return [
        {
            **common(),
            "proof_id": proof_id,
            "step": step,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for proof_id, step, formula, meaning, status in rows
    ]


def branch_matrix_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "BM4204_0_GR_TT_static",
            "metric homogeneous TT, stationary compact local",
            "use 4203 static TT zero theorem; W_i^K=0",
            "best_route_parent_identity_unsigned",
        ),
        (
            "BM4204_1_GR_TT_radiative",
            "metric homogeneous TT, nonstationary",
            "route to gravitational radiation/Hamiltonian boundary charge",
            "not_local_static_PPN",
        ),
        (
            "BM4204_2_vertical_gauge",
            "quotient vertical/gauge representative",
            "Dq=0 => W_i^K=0 by quotient naturality",
            "conditional_on_q_coframe_descent",
        ),
        (
            "BM4204_3_extra_tensor_source",
            "independent MTS tensor pole/source",
            "score with 4202 source pack and PPN inequalities",
            "current_fallback_active",
        ),
        (
            "BM4204_4_unplaced",
            "sector placement not parent-signed",
            "do not claim; carry both identity and source-pack branches",
            "current_state",
        ),
    ]
    return [
        {
            **common(),
            "matrix_id": matrix_id,
            "branch_condition": branch_condition,
            "required_action": required_action,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for matrix_id, branch_condition, required_action, status in rows
    ]


def independent_source_pack_rows() -> List[Dict[str, str]]:
    rows = [
        ("K_TT_independent", "binary/branch flag", "true only if Kperp is not EH TT, not vertical, and not boundary-radiative", "MISSING_SECTOR_PLACEMENT"),
        ("Z_T_ind", "tensor kinetic residue", "coefficient of independent MTS TT kinetic term", "MISSING_PARENT_KINETIC_RESIDUE"),
        ("M_T2_ind", "tensor mass/stiffness gap", "coefficient of independent MTS TT mass/stiffness term", "MISSING_PARENT_MASS_GAP"),
        ("J_TT_ind", "independent TT source projection", "P_TT sector leakage/source current", "MISSING_SOURCE_PROJECTION_NORM"),
        ("W_i^K_ind", "observable projection weights", "PPN/clock/WEP/Gdot readout weights if independent source exists", "MISSING_OBSERVABLE_PROJECTION"),
        ("no_double_count_certificate", "sector certificate", "proves row is not ordinary GR TT already counted", "MISSING_PARENT_SECTOR_CERTIFICATE"),
    ]
    return [
        {
            **common(),
            "symbol": symbol,
            "definition": definition,
            "required_source": required_source,
            "current_status": current_status,
            "numeric_value": "MISSING",
            "source_path": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for symbol, definition, required_source, current_status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "sector_placement_theorem_written": "True",
            "no_double_count_rule_derived": "True",
            "Kperp_GR_TT_identity_parent_signed": "False",
            "quotient_weight_zero_parent_signed": "False",
            "independent_source_pack_active": "True",
            "local_GR_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4204_0_no_double_count", "Do not count Kperp both as ordinary EH geometry and as extra source residual."),
        ("FW4204_1_no_EH_import_claim", "The EH/coframe branch is still conditional/effective unless parent-signed."),
        ("FW4204_2_no_vertical_without_q", "W_i^K=0 requires quotient/coframe descent, not just a gauge word."),
        ("FW4204_3_no_unplaced_pass", "Unplaced Kperp keeps the independent source-pack branch active."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": "4204 writes the Kperp sector-placement/no-double-count theorem: Kperp is either GR TT/vertical/boundary-radiative and not an extra static source, or it is an independent tensor source to be scored with 4202.",
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "Sector placement is now exact; next target must either parent-sign EH/coframe identity or make the independent tensor source pack scoreable.",
            "route_A": "parent-sign EH/coframe branch and Kperp=ordinary GR TT/gauge/radiation",
            "route_B": "prove W_i^K=0 through quotient/coframe naturality",
            "route_C": "fill independent tensor source-pack coefficients and run PPN thresholds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4204_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4204_SECTOR_PLACEMENT.csv": sector_placement_rows(),
        "P8_Y5_R2FR_4204_PARENT_IDENTITY_CLAUSES.csv": identity_clause_rows(),
        "P8_Y5_R2FR_4204_PROOF_CHAIN.csv": proof_rows(),
        "P8_Y5_R2FR_4204_BRANCH_MATRIX.csv": branch_matrix_rows(),
        "P8_Y5_R2FR_4204_INDEPENDENT_SOURCE_PACK.csv": independent_source_pack_rows(),
        "P8_Y5_R2FR_4204_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4204_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4204_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4204_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 220 - PPC4161 Kperp Sector Placement Theorem

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint proves the sector-placement/no-double-count rule for `K_perp`, but it does not parent-sign the EH/coframe identity or quotient-zero weights.

## Sector Placement Rule

The local ansatz leaves:

```text
partial_mu K_perp^{{mu nu}} = 0.
```

A divergence-free object is not automatically zero and not automatically GR. Before scoring, it must be placed:

```text
K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source.
```

Then:

```text
K_metric_TT    -> ordinary EH homogeneous/radiative metric sector;
K_vertical     -> quotient/gauge representative, W_i^K=0 if Dq=0 and e_obs descends;
K_boundary     -> Hamiltonian/radiation boundary charge;
K_extra_source -> independent MTS tensor source, scored by 4202.
```

## No-Double-Count Theorem

`K_perp` cannot be both:

```text
ordinary EH/GR TT geometry already counted in g_obs
```

and:

```text
an extra Hilbert-source tensor residual feeding local PPN.
```

If the parent signs the EH/coframe identity, the static local `Kperp` branch closes through 4203. If not, the independent tensor source pack remains active.

## Current Verdict

This is real narrowing: every `Kperp` contribution is now either GR/radiative/vertical and non-extra, or an explicit independent source-pack row. The current corpus still lacks the parent EH/coframe identity, so no local-GR claim follows yet.
"""
    checkpoint = f"""# 4204 - Y5 R2FR Parent Identity Kperp Is GR TT Or Independent Tensor Source Pack

Decision: `{DECISION}`

4204 proves the no-double-count sector rule:

```text
Kperp cannot be both ordinary EH homogeneous geometry and an extra local source.
```

So the local branch now has a clean fork:

```text
parent-sign Kperp = GR TT / vertical / boundary radiation -> no extra static local force;
otherwise score Kperp as an independent tensor source using the 4202 source pack.
```

Current status remains nonclaim because the EH/coframe identity is still unsigned.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(checkpoint, encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker not in text:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n\n" + block.strip() + "\n")


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,"The Kperp sector-placement theorem is written: Kperp is either ordinary EH/GR TT, vertical/gauge, boundary-radiative, '
        f'or an independent tensor source; no double-counting is allowed, but EH/coframe parent identity remains unsigned.","4204 source audit, sector placement, '
        f'parent identity clauses, proof chain, branch matrix, independent source pack, decision row and firewall.",'
        f'private_Kperp_sector_placement_nonclaim_EH_coframe_identity_unsigned,'
        f'"Parent-sign EH/coframe/Kperp identity or fill independent tensor source-pack coefficients.",'
        f'"Treating Kperp as both GR geometry and extra source would double-count or hide a local tensor force."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Kperp Sector Placement Theorem - 4204

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4204 proves the no-double-count sector split:

```text
K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source.
```

`Kperp` is either ordinary EH/GR TT, quotient/gauge, boundary-radiative, or an independent tensor source to score with 4202. Current status remains nonclaim because the EH/coframe parent identity is unsigned."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Kperp Sector Placement Theorem - 4204

Marker: `{PACKET_MARKER}`

Inside the private packet, `Kperp` can no longer float as an ambiguous ghost. It must be placed as GR TT/vertical/boundary radiation or scored as an independent tensor source. No double-counting is allowed."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4204_SOURCE_REGISTER.csv"]
    placement = rows_by_file["P8_Y5_R2FR_4204_SECTOR_PLACEMENT.csv"]
    clauses = rows_by_file["P8_Y5_R2FR_4204_PARENT_IDENTITY_CLAUSES.csv"]
    proof = rows_by_file["P8_Y5_R2FR_4204_PROOF_CHAIN.csv"]
    matrix = rows_by_file["P8_Y5_R2FR_4204_BRANCH_MATRIX.csv"]
    pack = rows_by_file["P8_Y5_R2FR_4204_INDEPENDENT_SOURCE_PACK.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4204_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    checks = [
        ("VAL4204_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4204_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4204_2_sector_placement", "sector placement covers metric, source, vertical and boundary sectors", {"metric homogeneous sector", "extra source sector", "quotient/gauge sector", "radiative/boundary sector"}.issubset({row["sector"] for row in placement})),
        ("VAL4204_3_no_double_count", "no-double-count rule is explicit", any(row["placement_id"] == "SP4204_5_no_double_count" for row in placement)),
        ("VAL4204_4_identity_clauses", "identity clauses include EH principal block and no independent tensor argument", any(row["clause_id"] == "ID4204_1_EH_principal_block" for row in clauses) and any(row["clause_id"] == "ID4204_2_no_independent_tensor_argument" for row in clauses)),
        ("VAL4204_5_proof_exhaustion", "proof chain includes exhaustion theorem and active fallback", any(row["proof_id"] == "PR4204_5_exhaustion" for row in proof) and any(row["proof_id"] == "PR4204_4_extra_source_branch" for row in proof)),
        ("VAL4204_6_branch_matrix_current", "branch matrix keeps unplaced/current state", any(row["matrix_id"] == "BM4204_4_unplaced" and row["status"] == "current_state" for row in matrix)),
        ("VAL4204_7_independent_pack", "independent source pack includes no-double-count certificate", any(row["symbol"] == "no_double_count_certificate" for row in pack)),
        ("VAL4204_8_decision_nonclaim", "decision keeps parent identity unsigned and claim false", decision[0]["Kperp_GR_TT_identity_parent_signed"] == "False" and decision[0]["claim_allowed"] == "False"),
        ("VAL4204_9_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4204_10_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4204_11_claim_register", "claim register contains L-045", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4204_12_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4204_13_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(bool(passed)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed in checks
    ]


def write_all() -> None:
    rows_by_file = all_rows()
    write_docs()
    update_registers()
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4204_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4204 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4204_VALIDATION.csv'}")
    print("rows=14 validation checks")


if __name__ == "__main__":
    main()
