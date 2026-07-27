from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4378"
CLAIM_ID = "L-219"
MARKER = "PPC4161_TRANSITION_TOPOLOGICAL_PROFILE_MOMENT_ZERO_OR_FIRST_MULTIPOLE_BOUND_ROW_4378"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_TOPOLOGICAL_PROFILE_MOMENT_ZERO_OR_FIRST_MULTIPOLE_BOUND_ROW_4378"
DECISION = "HARMONIC_NULL_MOMENT_ZERO_THEOREM_DERIVED_CONDITIONAL_FIRST_TOPOLOGICAL_MULTIPOLE_BOUND_ROWS_STAGED_NONCLAIM"
NEXT_TARGET = "4379-Y5-R2FR-transition-harmonic-null-parent-signature-or-first-numeric-topological-moment-input.md"

FORMAL_PATH = FORMAL / "394-PPC4161-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"
DOC_PATH = POST / "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4378_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SUPPORT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4378_00_4377_formal": (
        FORMAL / "393-PPC4161-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md",
        "all zero-monopole moments must vanish",
        "4377 selected the topological moment-zero or first multipole bound target.",
    ),
    "SRC4378_01_4377_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4377_NEXT_TARGET.csv",
        "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md",
        "4377 handoff naming this checkpoint.",
    ),
    "SRC4378_02_4377_moment": (
        SOURCE_DIR / "P8_Y5_R2FR_4377_TEST_FUNCTION_MOMENT_GATE.csv",
        "MOM4377_2_dipole",
        "4377 creates the dipole moment gate.",
    ),
    "SRC4378_03_4377_topology": (
        SOURCE_DIR / "P8_Y5_R2FR_4377_TOPOLOGICAL_PROFILE_EQUALITY.csv",
        "TPE4377_2_distributional_equality",
        "4377 reduces profile equality to a distributional all-test-function gate.",
    ),
    "SRC4378_04_4371_support": (
        SUPPORT_PATH,
        "SUP4371_2_Sun_Earth_average",
        "source-backed support geometry rows used for multipole scoring examples.",
    ),
    "SRC4378_05_4370_KN": (
        FORMAL / "386-PPC4161-transition-epsilon-Gsrc-coefficient-bound-or-Xi-owner-edge-proof.md",
        "K_N(s)=min((1-s)^-2, 2s(1-s)^-3)",
        "4370 supplies the coarse zero-monopole K_N gate.",
    ),
    "SRC4378_06_hamiltonian_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "Same-Object Glue",
        "Hamiltonian/worldtube glue avoids a post-readout topological mask but is not a profile proof.",
    ),
    "SRC4378_07_newton_density": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "int_W rho_H dV = M_H^dress[W_H;tau].",
        "Poisson/Gauss readout uses the integrated Hilbert density.",
    ),
    "SRC4378_08_selector_topology": (
        SOURCE_DIR / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv",
        "WSC2577_4_R_eq_zero_lemma",
        "same Hilbert/topological class route remains conditional.",
    ),
    "SRC4378_09_boundary_topological": (
        FORMAL / "143-boundary-topological-backup-gate.md",
        "bulk metric-nullity passes formally, but is insufficient.",
        "boundary/topological nullity alone is insufficient for local profile safety.",
    ),
    "SRC4378_10_transition_monopole": (
        FORMAL / "305-PPC4161-transition-monopole-absorption-or-residual-profile-gate.md",
        "Only `q_tr^Hilbert-monopole` is absorbable.",
        "monopole absorption already separates residual multipoles from source dressing.",
    ),
    "SRC4378_11_transition_kernel": (
        FORMAL / "371-PPC4161-transition-shell-same-worldtube-nonHilbert-residue-or-bounded-source-hair.md",
        "Q_l>=1_tr=0",
        "transition source-kernel work requires non-monopole moments to vanish.",
    ),
    "SRC4378_12_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "EM/Poynting energy must not be double-counted as topological profile hair.",
    ),
    "SRC4378_13_charge_status": (
        SOURCE_DIR / "P8_charge_current_equality_STATUS.csv",
        "charge-current equality parent-derived,fail",
        "charge-current equality remains nonclaim in the wider corpus.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def harmonic_null_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "HN4378_0_harmonic_moment_gate",
            "claim_piece": "exterior multipole safety",
            "formal_statement": "For delta rho_top with compact support in W_H and zero monopole, exterior Newton response vanishes iff all harmonic moments M_lm=int_W delta rho_top r^l Y_lm dV vanish for l>=1.",
            "derivation_result": "EXACT_EXTERIOR_GREEN_GATE",
            "effect_if_signed": "E_top_profile can be replaced by a zero exterior Green response for Newton/orbital scoring",
            "current_blocker": "all moments are not parent-signed in the current corpus",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HN4378_1_laplacian_null_sufficient_condition",
            "claim_piece": "harmonic-null source profile",
            "formal_statement": "If delta rho_top=Delta u_top on W_H and u_top plus its normal boundary term is silent on partial W_H, then int_W h_lm delta rho_top dV=0 for every harmonic h_lm=r^lY_lm.",
            "derivation_result": "CONDITIONAL_THEOREM_DERIVED",
            "effect_if_signed": "all exterior topological multipoles vanish even if the interior density representative is not pointwise equal",
            "current_blocker": "parent action has not shown rho_top-rho_H is a compact Laplacian/exterior-Green-kernel-null defect",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HN4378_2_proof_identity",
            "claim_piece": "Green identity proof",
            "formal_statement": "int_W h Delta u dV = int_W u Delta h dV + boundary[h partial_n u - u partial_n h]; Delta h_lm=0 and boundary silence imply M_lm=0.",
            "derivation_result": "PROOF_WRITTEN",
            "effect_if_signed": "the moment-zero proof is mathematical, not a fitted cancellation",
            "current_blocker": "boundary silence and Laplacian form are not signed by MTS parent grammar",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HN4378_3_exact_divergence_insufficient",
            "claim_piece": "why generic exact/topological current is not enough",
            "formal_statement": "If delta rho_top=div V, then int_W h div V dV = boundary - int_W V dot grad h dV, which is not zero for generic V and harmonic h.",
            "derivation_result": "SHORTCUT_REJECTED",
            "effect_if_signed": "prevents closed/exact/topological wording from being sold as moment silence",
            "current_blocker": "need Laplacian/harmonic-null structure or explicit moment bounds",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HN4378_4_metric_null_insufficient",
            "claim_piece": "metric-nullity is not profile safety",
            "formal_statement": "delta_g S_top=0 or dJ_top=0 does not imply int_W h_lm(rho_top-rho_H)dV=0.",
            "derivation_result": "FIREWALL_DERIVED",
            "effect_if_signed": "blocks a boundary/topological backup shortcut already flagged by 143",
            "current_blocker": "topological profile moments remain open",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HN4378_5_current_verdict",
            "claim_piece": "topological moment-zero theorem",
            "formal_statement": "Topological profile safety is exact if the defect is exterior-harmonic-null; current corpus has not signed that, so multipole rows are retained.",
            "derivation_result": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "effect_if_signed": "topological component of exterior E_profile/Newton residual closes",
            "current_blocker": "must prove harmonic-null parent signature or source numeric moments",
            "valid_for_claim": "False",
        },
    ]


def multipole_definition_rows() -> List[Dict[str, str]]:
    return [
        {
            "moment_id": "MP4378_0_defect_density",
            "quantity": "delta rho_top",
            "definition": "delta rho_top := rho_top-rho_H on W_H",
            "units": "mass_density",
            "zero_condition": "rho_top=rho_H as distributions, or exterior-harmonic-null defect for exterior scoring",
            "current_status": "SYMBOLIC_DEFECT_DEFINED",
            "valid_for_claim": "False",
        },
        {
            "moment_id": "MP4378_1_monopole",
            "quantity": "M_0",
            "definition": "M_0 := int_W delta rho_top dV_H",
            "units": "mass",
            "zero_condition": "same total Hamiltonian/topological/Hilbert source charge",
            "current_status": "CONDITIONAL_MONOPOLE_ONLY_NOT_PROFILE_EQUALITY",
            "valid_for_claim": "False",
        },
        {
            "moment_id": "MP4378_2_dipole",
            "quantity": "M_1m",
            "definition": "M_1m := int_W delta rho_top r Y_1m dV_H",
            "units": "mass*length",
            "zero_condition": "harmonic-null theorem, symmetry/same-center theorem, or source-backed value zero",
            "current_status": "FIRST_BOUND_ROW_STAGED_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "moment_id": "MP4378_3_quadrupole",
            "quantity": "M_2m",
            "definition": "M_2m := int_W delta rho_top r^2 Y_2m dV_H",
            "units": "mass*length^2",
            "zero_condition": "harmonic-null theorem, spherical/profile equality theorem, or source-backed value zero",
            "current_status": "BOUND_ROW_STAGED_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "moment_id": "MP4378_4_dimensionless_envelope",
            "quantity": "E_l^top",
            "definition": "E_l^top := ((l+1)4pi/(2l+1)) sum_m |M_lm|/(M_H R^l)",
            "units": "dimensionless",
            "zero_condition": "all M_lm=0 for that l",
            "current_status": "NORMALIZATION_CHOSEN_FOR_SCORING_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "moment_id": "MP4378_5_transfer",
            "quantity": "multipole acceleration transfer",
            "definition": "|delta a_l|/|a_N| <= E_l^top (R/r)^l",
            "units": "dimensionless",
            "zero_condition": "E_l^top=0 or below arena threshold",
            "current_status": "TRANSFER_DERIVED",
            "valid_for_claim": "False",
        },
    ]


def first_bound_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source in read_csv(SUPPORT_PATH):
        support_id = source["support_id"]
        s = float(source["s_R_over_r"])
        source_body = source["source_body"]
        readout = source["test_body_or_readout"]
        rows.extend(
            [
                {
                    "bound_id": f"TB4378_{support_id}_dipole",
                    "support_id": support_id,
                    "source_body": source_body,
                    "test_body_or_readout": readout,
                    "multipole_l": "1",
                    "s_R_over_r": f"{s:.12g}",
                    "geometry_factor_s_l": f"{s:.12g}",
                    "dimensionless_moment": "E_1^top := (8pi/3) sum_m |M_1m|/(M_H R)",
                    "score_formula": f"|deltaa_top,l=1|/|a_N| <= {s:.12g} E_1^top",
                    "pass_formula": f"E_1^top <= delta_N/{s:.12g}",
                    "current_status": "MOMENT_VALUE_MISSING_NONCLAIM",
                    "valid_for_claim": "False",
                    "claim_allowed": "False",
                },
                {
                    "bound_id": f"TB4378_{support_id}_quadrupole",
                    "support_id": support_id,
                    "source_body": source_body,
                    "test_body_or_readout": readout,
                    "multipole_l": "2",
                    "s_R_over_r": f"{s:.12g}",
                    "geometry_factor_s_l": f"{s * s:.12g}",
                    "dimensionless_moment": "E_2^top := (12pi/5) sum_m |M_2m|/(M_H R^2)",
                    "score_formula": f"|deltaa_top,l=2|/|a_N| <= {s * s:.12g} E_2^top",
                    "pass_formula": f"E_2^top <= delta_N/{s * s:.12g}",
                    "current_status": "MOMENT_VALUE_MISSING_NONCLAIM",
                    "valid_for_claim": "False",
                    "claim_allowed": "False",
                },
            ]
        )
    return rows


def theorem_vs_bound_router_rows() -> List[Dict[str, str]]:
    return [
        {
            "route_id": "ROUTE4378_0_parent_harmonic_null",
            "input": "delta rho_top=Delta u_top with boundary-silent u_top",
            "action": "set all E_l^top=0 for exterior Newton/local orbital scoring",
            "output": "topological exterior profile residual zero",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4378_1_distributional_equality",
            "input": "rho_top=rho_H as distributions",
            "action": "set E_top_profile=0, stronger than exterior moment silence",
            "output": "topological profile component closed",
            "current_status": "NOT_PROVED",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4378_2_multipole_bound",
            "input": "source-backed M_1m, M_2m or E_l^top values",
            "action": "score through |deltaa_l|/|a_N| <= E_l^top s^l",
            "output": "finite nonclaim topological multipole row",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4378_3_coarse_KN",
            "input": "only coarse E_top_profile norm known",
            "action": "use |deltaa_top|/|a_N| <= K_N(s) E_top_profile",
            "output": "safe but usually weaker profile-norm bound",
            "current_status": "FALLBACK_AVAILABLE_VALUE_MISSING",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4378_0_harmonic_null_zero",
            "claim_tested": "all topological exterior moments vanish",
            "required_inputs": "delta rho_top=Delta u_top or equivalent exterior-Green-kernel-null parent signature plus boundary silence",
            "status": "BLOCKED_PARENT_SIGNATURE_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4378_1_multipole_bound",
            "claim_tested": "finite topological dipole/quadrupole pass",
            "required_inputs": "source-backed M_1m/M_2m or E_l^top values plus delta_N arena bound",
            "status": "BOUND_ROWS_READY_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4378_2_profile_component",
            "claim_tested": "topological component of E_profile/exterior Newton residual closes",
            "required_inputs": "harmonic-null theorem or all relevant multipole/profile rows below thresholds",
            "status": "BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4378_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "topological profile route plus E_shadow/E_nonHilbert/E_readout and all other E_perp components closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4378_0",
            "decision": DECISION,
            "summary": (
                "4378 derives the precise topological-profile safety theorem for exterior Newton/source scoring: a topological/Hamiltonian profile defect is harmless only if it is exterior-harmonic-null, for example delta rho_top=Delta u_top with boundary-silent u_top, which kills every harmonic moment by Green's identity. "
                "Generic closed, exact, metric-null or same-charge topological language is rejected as insufficient. "
                "Because the parent harmonic-null signature is not currently signed, 4378 stages the first topological multipole bound rows: dipole and quadrupole gates for each existing 4371 support geometry, using |deltaa_l|/|a_N| <= E_l^top (R/r)^l."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "it asks for the exact parent signature that would activate the theorem, or the first real numeric/source-backed moment input.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4378_0_harmonic_null",
            "object": "topological exterior moment zero",
            "status": "CONDITIONAL_THEOREM_DERIVED",
            "note": "Laplacian/exterior-Green-kernel-null defects with boundary silence have zero exterior harmonic moments.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4378_1_shortcuts",
            "object": "closed/exact/topological/metric-null shortcuts",
            "status": "REJECTED_AS_INSUFFICIENT",
            "note": "generic div V or metric-null topological action does not imply moment silence.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4378_2_multipole_rows",
            "object": "first topological dipole/quadrupole bound rows",
            "status": "STAGED_NONCLAIM",
            "note": "geometry factors are source-backed; moment values and delta_N are missing.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4378_3_next",
            "object": "next derivation",
            "status": "HARMONIC_NULL_SIGNATURE_OR_NUMERIC_MOMENT_INPUT_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4378_0",
            "target": NEXT_TARGET,
            "question": "Can the parent action prove the topological profile defect is exterior-harmonic-null, or must a real M_1m/M_2m/E_l^top source input be filled?",
            "preferred_route": "derive delta rho_top=Delta u_top or an equivalent Green-kernel-null identity with boundary silence from the parent topological/Hamiltonian source construction.",
            "fallback_route": "fill the first source-backed dipole/quadrupole moment value or upper bound, then score it through the 4378 multipole rows and an arena delta_N.",
            "avoid": "using closed current, same total mass, topological class, metric-nullity, or exact divergence alone as moment-zero evidence.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    harmonic: List[Dict[str, str]],
    moments: List[Dict[str, str]],
    bounds: List[Dict[str, str]],
    routes: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: topological profile moment zero or first multipole bound row

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4378 turns the topological wrong-distribution issue into an exterior Green-kernel theorem plus scoreable multipole rows.

The clean theorem is:

```text
delta rho_top := rho_top-rho_H,
M_lm := int_W delta rho_top r^l Y_lm dV_H.

M_lm=0 for all l>=1,m
=> no exterior Newton multipole from the topological profile defect.
```

A sufficient parent mechanism is stronger than "topological" or "closed":

```text
delta rho_top = Delta u_top,
u_top and boundary terms silent on partial W_H.
```

For every harmonic test function `h_lm=r^lY_lm`,

```text
int_W h_lm Delta u_top dV
= int_W u_top Delta h_lm dV
  + boundary[h_lm partial_n u_top - u_top partial_n h_lm]
= 0.
```

That kills all exterior moments. A generic exact divergence does not:

```text
int_W h div V dV = boundary - int_W V dot grad h dV,
```

which is not zero without an extra harmonic-null condition.

Because the parent harmonic-null signature is not yet signed, 4378 stages the first multipole bounds:

```text
E_l^top := ((l+1)4pi/(2l+1)) sum_m |M_lm|/(M_H R^l),
|delta a_l|/|a_N| <= E_l^top (R/r)^l.
```

Dipole and quadrupole rows are generated for the existing 4371 support geometries. This is not a pass; it is the first concrete topological multipole scoring contract.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Harmonic-Null Theorem

{md_table(harmonic, ["theorem_id", "claim_piece", "formal_statement", "derivation_result", "effect_if_signed", "current_blocker"])}

## Multipole Definitions

{md_table(moments, ["moment_id", "quantity", "definition", "units", "zero_condition", "current_status"])}

## First Topological Multipole Bound Rows

{md_table(bounds, ["bound_id", "support_id", "source_body", "test_body_or_readout", "multipole_l", "s_R_over_r", "geometry_factor_s_l", "dimensionless_moment", "score_formula", "pass_formula", "current_status"])}

## Theorem/Bound Router

{md_table(routes, ["route_id", "input", "action", "output", "current_status"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4378: topological profile moment zero or first multipole bound row

Marker: `{MARKER}`

## What changed

- Derived the conditional harmonic-null theorem: `delta rho_top=Delta u_top` with silent boundary terms kills all exterior harmonic moments.
- Rejected generic closed/exact/topological/metric-null shortcuts as insufficient for moment silence.
- Added first topological dipole/quadrupole bound rows for every 4371 support geometry.
- Routed the next fork to parent harmonic-null signature or real source-backed moment values.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4378 Transition topological profile moment gate

Marker: `{MARKER}`

4378 sharpens the topological wrong-distribution problem. Same total charge only kills the monopole. Exterior Newton safety requires all non-monopole harmonic moments to vanish:

```text
M_lm := int_W (rho_top-rho_H) r^l Y_lm dV_H = 0, l>=1.
```

A real theorem route exists if the defect is exterior-harmonic-null:

```text
rho_top-rho_H = Delta u_top
```

with silent boundary terms. Green's identity then kills every harmonic moment. Generic exact, closed, topological, or metric-null language is not enough. Since the parent signature is unsigned, 4378 stages dipole/quadrupole rows:

```text
|delta a_l|/|a_N| <= E_l^top (R/r)^l.
```

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4378 packet update: topological profile moments become score rows

Marker: `{PACKET_MARKER}`

Packet update: topological/Hamiltonian profile safety is now a harmonic-moment problem. Same charge is only the monopole. A compact Laplacian or equivalent exterior-Green-kernel-null defect with boundary silence kills all exterior moments; a generic exact divergence or metric-null topological term does not. Until that parent signature is derived, the packet carries dipole/quadrupole `E_l^top` rows scored by `|delta a_l|/|a_N| <= E_l^top (R/r)^l`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4378 derives the conditional harmonic-null theorem for the topological profile defect: if rho_top-rho_H=Delta u_top with boundary-silent u_top, then Green's identity kills every exterior harmonic moment M_lm and the topological defect has no exterior Newton multipole. "
                "It rejects generic closed, exact, metric-null or same-charge topological language as insufficient, because an exact divergence need not be orthogonal to harmonic test functions. "
                "Since the parent harmonic-null signature is unsigned, 4378 stages first nonclaim dipole/quadrupole bound rows using |delta a_l|/|a_N| <= E_l^top (R/r)^l. No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4378 source register, harmonic-null theorem rows, multipole definitions, topological multipole bound rows, theorem/bound router, claim gates, decision, status, next target and validation CSV.",
            "harmonic_null_moment_zero_theorem_conditional_first_topological_multipole_rows_nonclaim",
            "Prove the parent harmonic-null signature for the topological/Hamiltonian source defect, or fill the first real M_1m/M_2m/E_l^top numeric input.",
            "Claiming moment silence from same charge, topological class, closed current, exact divergence, or metric-nullity alone.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4378_SOURCE_REGISTER.csv")
    harmonic = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4378_HARMONIC_NULL_THEOREM.csv")
    moments = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4378_MULTIPOLE_DEFINITIONS.csv")
    bounds = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4378_TOPOLOGICAL_MULTIPOLE_BOUND_ROWS.csv")
    routes = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4378_THEOREM_BOUND_ROUTER.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4378_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4378_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4378_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4378_2_harmonic_null_theorem",
        any(row["theorem_id"] == "HN4378_1_laplacian_null_sufficient_condition" and "Delta u_top" in row["formal_statement"] for row in harmonic),
        "Laplacian/harmonic-null theorem row exists",
    )
    add(
        "VAL4378_3_divergence_rejected",
        any(row["theorem_id"] == "HN4378_3_exact_divergence_insufficient" and row["derivation_result"] == "SHORTCUT_REJECTED" for row in harmonic),
        "generic exact divergence shortcut is rejected",
    )
    add(
        "VAL4378_4_multipole_definitions",
        any(row["moment_id"] == "MP4378_2_dipole" for row in moments)
        and any(row["moment_id"] == "MP4378_3_quadrupole" for row in moments),
        "dipole and quadrupole definitions exist",
    )
    add(
        "VAL4378_5_bound_rows",
        any(row["multipole_l"] == "1" for row in bounds)
        and any(row["multipole_l"] == "2" for row in bounds)
        and all(float(row["s_R_over_r"]) > 0 and float(row["geometry_factor_s_l"]) > 0 for row in bounds),
        "dipole/quadrupole bound rows have positive geometry factors",
    )
    add(
        "VAL4378_6_router",
        any(row["route_id"] == "ROUTE4378_0_parent_harmonic_null" for row in routes)
        and any(row["route_id"] == "ROUTE4378_2_multipole_bound" for row in routes),
        "theorem and bound routes are both present",
    )
    add("VAL4378_7_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4378_8_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4378_9_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4378_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4378_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4378_12_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4378_13_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4378_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    return validations


def main() -> None:
    sources = source_register_rows()
    harmonic = harmonic_null_theorem_rows()
    moments = multipole_definition_rows()
    bounds = first_bound_rows()
    routes = theorem_vs_bound_router_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4378_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4378_HARMONIC_NULL_THEOREM.csv": harmonic,
        "P8_Y5_R2FR_4378_MULTIPOLE_DEFINITIONS.csv": moments,
        "P8_Y5_R2FR_4378_TOPOLOGICAL_MULTIPOLE_BOUND_ROWS.csv": bounds,
        "P8_Y5_R2FR_4378_THEOREM_BOUND_ROUTER.csv": routes,
        "P8_Y5_R2FR_4378_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4378_DECISION.csv": decisions,
        "P8_Y5_R2FR_4378_STATUS.csv": statuses,
        "P8_Y5_R2FR_4378_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, harmonic, moments, bounds, routes, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
