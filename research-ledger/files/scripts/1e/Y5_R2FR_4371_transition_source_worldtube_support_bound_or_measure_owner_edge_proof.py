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
MICRO_RESIDUALS = POST / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"

CHECKPOINT = "4371"
CLAIM_ID = "L-212"
BRANCH = "MTS_R2FR_Y5_TRANSITION_SOURCE_WORLDTUBE_SUPPORT_BOUND_OR_MEASURE_OWNER_EDGE_PROOF_4371"
MARKER = "PPC4161_TRANSITION_SOURCE_WORLDTUBE_SUPPORT_BOUND_OR_MEASURE_OWNER_EDGE_PROOF_4371"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SOURCE_WORLDTUBE_SUPPORT_BOUND_OR_MEASURE_OWNER_EDGE_PROOF_4371"
DECISION = "SOURCE_SUPPORT_GEOMETRY_ANCHORS_FILLED_MEASURE_OWNER_EDGE_CONDITIONAL_EPERP_STILL_UNSOURCED_NONCLAIM"
NEXT_TARGET = "4372-Y5-R2FR-transition-Eperp-envelope-decomposition-or-measure-owner-action-line-proof.md"

FORMAL_PATH = FORMAL / "387-PPC4161-transition-source-worldtube-support-bound-or-measure-owner-edge-proof.md"
DOC_PATH = POST / "4371-Y5-R2FR-transition-source-worldtube-support-bound-or-measure-owner-edge-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4371_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NASA_SOLAR_SYSTEM_PDF = "https://d2pn8kiwq2w21t.cloudfront.net/documents/scaless_reference_xJvjKH2.pdf"
NASA_MOON_FACTS = "https://science.nasa.gov/moon/facts/"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4371_00_4370_formal": (
        FORMAL / "386-PPC4161-transition-epsilon-Gsrc-coefficient-bound-or-Xi-owner-edge-proof.md",
        "K_N(s)=min((1-s)^-2, 2s(1-s)^-3)",
        "4370 coefficient gate to be populated with source/worldtube support inputs.",
    ),
    "SRC4371_01_4370_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4370_NEXT_TARGET.csv",
        "4371-Y5-R2FR-transition-source-worldtube-support-bound-or-measure-owner-edge-proof.md",
        "4370 selected source support inputs or measure-owner proof.",
    ),
    "SRC4371_02_4370_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4370_OWNER_EDGE_AUDIT.csv",
        "EDGE4370_0_measure_owner",
        "measure owner edge was checked and remains unsigned.",
    ),
    "SRC4371_03_4361_premise": (
        SOURCE_DIR / "P8_Y5_R2FR_4361_PREMISE_AUDIT.csv",
        "P4361_2_measure_owner",
        "measure/Jacobian owner premise needed for the zero route.",
    ),
    "SRC4371_04_1606_edges": (
        MICRO_RESIDUALS / "R2FR_parent_owned_edge_audit_nonclaim_1606.csv",
        "EDGE1606_5_measure",
        "parent-owned graph edge audit does not certify the measure owner.",
    ),
    "SRC4371_05_4178_guards": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_ANTI_CIRCULARITY_GUARDS.csv",
        "AC4178_2_no_source_label_absorption",
        "source labels cannot be absorbed into G_cal.",
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


def k_factor(s: float) -> Tuple[float, float, float]:
    coarse = (1.0 - s) ** -2
    zero_monopole = 2.0 * s * (1.0 - s) ** -3
    return coarse, zero_monopole, min(coarse, zero_monopole)


def source_rows() -> List[Dict[str, str]]:
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


def external_source_rows() -> List[Dict[str, str]]:
    return [
        {
            "external_id": "EXT4371_0_NASA_solar_system_sizes",
            "url": NASA_SOLAR_SYSTEM_PDF,
            "values_used": "Sun diameter 1,391,400 km; Mercury distance 57,900,000 km; Venus distance 108,200,000 km; Earth distance 149,600,000 km; Mars distance 227,900,000 km; Earth diameter 12,756 km",
            "source_lines": "web open lines 13-19",
            "role": "source-backed average support geometry examples for Sun/planet and Earth/Moon rows",
            "valid_for_claim": "False",
        },
        {
            "external_id": "EXT4371_1_NASA_moon_facts",
            "url": NASA_MOON_FACTS,
            "values_used": "Moon average distance 384,400 km",
            "source_lines": "web open lines 360-365",
            "role": "Earth-Moon support geometry example",
            "valid_for_claim": "False",
        },
    ]


def support_rows() -> List[Dict[str, str]]:
    examples = [
        {
            "support_id": "SUP4371_0_Sun_Mercury_average",
            "source_body": "Sun",
            "test_body_or_readout": "Mercury average orbital distance",
            "R_source_km": 1391400.0 / 2.0,
            "r_readout_km": 57900000.0,
            "source_url": NASA_SOLAR_SYSTEM_PDF,
            "source_note": "NASA solar-system sizes/distances reference; average distance row, not perihelion",
        },
        {
            "support_id": "SUP4371_1_Sun_Venus_average",
            "source_body": "Sun",
            "test_body_or_readout": "Venus average orbital distance",
            "R_source_km": 1391400.0 / 2.0,
            "r_readout_km": 108200000.0,
            "source_url": NASA_SOLAR_SYSTEM_PDF,
            "source_note": "NASA solar-system sizes/distances reference; average distance row",
        },
        {
            "support_id": "SUP4371_2_Sun_Earth_average",
            "source_body": "Sun",
            "test_body_or_readout": "Earth average orbital distance",
            "R_source_km": 1391400.0 / 2.0,
            "r_readout_km": 149600000.0,
            "source_url": NASA_SOLAR_SYSTEM_PDF,
            "source_note": "NASA solar-system sizes/distances reference; average distance row",
        },
        {
            "support_id": "SUP4371_3_Sun_Mars_average",
            "source_body": "Sun",
            "test_body_or_readout": "Mars average orbital distance",
            "R_source_km": 1391400.0 / 2.0,
            "r_readout_km": 227900000.0,
            "source_url": NASA_SOLAR_SYSTEM_PDF,
            "source_note": "NASA solar-system sizes/distances reference; average distance row",
        },
        {
            "support_id": "SUP4371_4_Earth_Moon_average",
            "source_body": "Earth",
            "test_body_or_readout": "Moon average orbital distance",
            "R_source_km": 12756.0 / 2.0,
            "r_readout_km": 384400.0,
            "source_url": f"{NASA_SOLAR_SYSTEM_PDF}; {NASA_MOON_FACTS}",
            "source_note": "Earth diameter from NASA solar-system reference; Moon average distance from NASA Moon facts",
        },
    ]
    rows: List[Dict[str, str]] = []
    for example in examples:
        s = example["R_source_km"] / example["r_readout_km"]
        coarse, zero, selected = k_factor(s)
        rows.append(
            {
                **{key: str(value) for key, value in example.items()},
                "s_R_over_r": f"{s:.12g}",
                "coarse_factor": f"{coarse:.12g}",
                "zero_monopole_factor": f"{zero:.12g}",
                "selected_K_N": f"{selected:.12g}",
                "Eperp_gate_per_deltaN": f"E_perp <= delta_N/{selected:.12g}",
                "deltaN_multiplier_for_allowed_Eperp": f"{1.0 / selected:.12g}",
                "geometry_source_backed": "True",
                "Eperp_source_backed": "False",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def measure_owner_lemma_rows() -> List[Dict[str, str]]:
    return [
        {
            "lemma_id": "MO4371_0_measure_zero_lemma",
            "statement": "If the parent matter measure is one q-basic species-blind measure before variation, then the measure/Jacobian contribution to epsilon_Gsrc_perp vanishes.",
            "formula": "dmu_A=dmu_* and D_A ln dmu_*=0 => D_A delta_ZH=0 => epsilon_measure_perp=0",
            "proof_status": "CONDITIONAL_LEMMA_DERIVED",
            "current_activation": "NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "lemma_id": "MO4371_1_hidden_rescaling_countermodel",
            "statement": "A field or species dependent Jacobian/hbar/source normalization can mimic a source-measure edge even when post-variation equations look universal.",
            "formula": "dmu_A = J_A dmu_* or hbar_A != hbar_* gives D_A delta_ZH != 0",
            "proof_status": "COUNTERMODEL_RETAINED",
            "current_activation": "BLOCKS_ZERO_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "lemma_id": "MO4371_2_not_full_epsilon_zero",
            "statement": "Even a signed measure owner would zero only the measure part; same-source mass, transition hair, Xi_open and T_open must still close separately.",
            "formula": "epsilon_Gsrc_perp = epsilon_measure_perp + epsilon_mass_perp + epsilon_transition_perp + epsilon_XiT_perp",
            "proof_status": "DECOMPOSITION_RULE",
            "current_activation": "NONCLAIM_FIREWALL",
            "valid_for_claim": "False",
        },
    ]


def acquisition_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "ACQ4371_0_Eperp_bound",
            "needed_quantity": "E_perp = ||epsilon_Gsrc_perp||_inf",
            "why_needed": "turns the support geometry into a Newton/source-normalization pass/fail row",
            "acceptable_source": "parent theorem E_perp=0; or source-backed finite envelope from measure/source-mass/transition/Xi/T components",
            "current_status": "MISSING",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ACQ4371_1_support_geometry",
            "needed_quantity": "R/r for the source and readout arena",
            "why_needed": "sets K_N(s)",
            "acceptable_source": "source/worldtube radius and observation/readout radius fixed before scoring",
            "current_status": "PARTIAL_EXAMPLES_FILLED_AVERAGE_SOLAR_SYSTEM",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ACQ4371_2_deltaN_bound",
            "needed_quantity": "observed fractional Newton/source residual bound delta_N",
            "why_needed": "sets E_perp <= delta_N/K_N(s)",
            "acceptable_source": "chosen local test with documented observable, uncertainty and convention",
            "current_status": "MISSING",
            "valid_for_claim": "False",
        },
        {
            "input_id": "ACQ4371_3_measure_owner_edge",
            "needed_quantity": "species-blind measure/Jacobian/hbar owner proof",
            "why_needed": "can zero one component of E_perp rather than fitting it",
            "acceptable_source": "parent action grammar proving no species/source measure slot before variation",
            "current_status": "UNSIGNED",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4371_0_support_examples",
            "claim_tested": "source/worldtube support examples are available",
            "required_inputs": "positive R, r and 0<R/r<1",
            "status": "PASS_GEOMETRY_EXAMPLES_NONCLAIM",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4371_1_Eperp_score",
            "claim_tested": "epsilon_Gsrc_perp passes Newton/source-normalization test",
            "required_inputs": "E_perp bound and delta_N bound fixed before scoring",
            "status": "BLOCKED_EPERP_AND_DELTAN_MISSING",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4371_2_measure_owner_zero",
            "claim_tested": "measure owner zeroes source-measure contribution",
            "required_inputs": "species-blind measure/Jacobian/hbar parent proof",
            "status": "CONDITIONAL_LEMMA_ONLY",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4371_3_public_local_GR",
            "claim_tested": "public local-GR/Newton/PPN pass",
            "required_inputs": "E_perp/measure route plus Xi_open/T_open/Bianchi/boundary closure",
            "status": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4371_0",
            "decision": DECISION,
            "summary": (
                "4371 fills source-backed support geometry examples for the epsilon_Gsrc_perp gate using NASA solar-system size/distance rows. "
                "The resulting K_N(s) values show that far-field solar and Earth-Moon source-shape residuals are geometrically suppressed after monopole subtraction. "
                "However E_perp and delta_N are still not sourced, so the rows are gate-ready but nonclaim. The measure-owner route is sharpened to a conditional lemma: "
                "a q-basic species-blind measure/Jacobian/hbar owner would zero the measure component, but 4361/1606 keep that edge unsigned and it would not alone zero all epsilon_Gsrc_perp components."
            ),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4371_0",
            "object": "support geometry",
            "status": "PARTIAL_SOURCE_BACKED_EXAMPLES_FILLED",
            "note": "Sun-planet and Earth-Moon average support ratios now populate K_N(s).",
        },
        {
            "status_id": "STAT4371_1",
            "object": "E_perp",
            "status": "MISSING",
            "note": "no source-backed envelope or parent zero yet.",
        },
        {
            "status_id": "STAT4371_2",
            "object": "measure owner",
            "status": "CONDITIONAL_LEMMA_NOT_SIGNED",
            "note": "species-blind measure owner would help, but the current edge audit does not certify it.",
        },
        {
            "status_id": "STAT4371_3",
            "object": "local GR",
            "status": "NONCLAIM",
            "note": "support geometry alone is not a Newton/local-GR pass.",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4371_0",
            "target": NEXT_TARGET,
            "question": "Can E_perp be decomposed into source-measure, source-mass, transition-hair, Xi and T components, or can the measure-owner action line be proved?",
            "preferred_route": "decompose E_perp into component envelopes and try to zero/source the largest pieces",
            "alternate_zero_route": "prove the species-blind measure/Jacobian/hbar owner edge from the parent action line",
            "avoid": "treating average support geometry as an empirical local-GR pass",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    external_sources: List[Dict[str, str]],
    support: List[Dict[str, str]],
    measure: List[Dict[str, str]],
    acquisition: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: source/worldtube support bound or measure-owner edge proof

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4370 gave the gate:

```text
K_N(s)=min((1-s)^-2, 2s(1-s)^-3),
E_perp <= delta_N/K_N(s),
s=R/r.
```

4371 fills the first source-backed `s=R/r` examples from NASA solar-system size/distance data. This does **not** claim a pass, because `E_perp` and `delta_N` are not sourced yet. It does show that after common-monopole subtraction the far-field source-shape channel can be geometrically suppressed.

The measure-owner zero route is also sharpened. If the parent matter measure is one q-basic, species-blind measure before variation, then the measure/Jacobian contribution to `epsilon_Gsrc_perp` is zero. But current 4361/1606 evidence does not sign that edge, and even signing it would not by itself close same-source-mass, transition-hair, `Xi_open`, or `T_open`.

## Local Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## External Source Register

{md_table(external_sources, ["external_id", "url", "values_used", "source_lines", "role"])}

## Source Support Geometry Rows

{md_table(support, ["support_id", "source_body", "test_body_or_readout", "R_source_km", "r_readout_km", "s_R_over_r", "selected_K_N", "deltaN_multiplier_for_allowed_Eperp", "geometry_source_backed", "Eperp_source_backed"])}

## Measure-Owner Lemma

{md_table(measure, ["lemma_id", "statement", "formula", "proof_status", "current_activation"])}

## Acquisition Rows

{md_table(acquisition, ["input_id", "needed_quantity", "why_needed", "acceptable_source", "current_status"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "valid_for_claim"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_zero_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4371: source/worldtube support bound or measure-owner edge proof

Marker: `{MARKER}`

## What changed

- Filled source-backed `R/r` examples for the 4370 `K_N(s)` gate.
- Converted support geometry into immediate `E_perp <= delta_N/K_N(s)` multipliers.
- Proved a conditional measure-owner lemma, but kept it unsigned.
- Kept the branch nonclaim because `E_perp` and `delta_N` remain missing.

## Decision row

{md_table(decisions, ["decision_id", "decision", "summary", "next_target"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_zero_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4371 Transition source support geometry examples

Marker: `{MARKER}`

4371 populates the 4370 `K_N(s)` gate with source-backed average support ratios for Sun-planet and Earth-Moon examples. The rows are not claims because `E_perp` and `delta_N` are still missing, but they make the Newton/source-normalization gate immediately scoreable once those inputs exist.

The measure-owner route is now a precise conditional lemma: a q-basic species-blind parent measure/Jacobian/hbar owner gives `D_A delta_ZH=0` and kills the measure part of `epsilon_Gsrc_perp`. The current edge audit does not sign that clause, and the lemma alone would not close source mass, transition hair, `Xi_open`, or `T_open`. Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4371 packet update: source support geometry populated

Marker: `{PACKET_MARKER}`

Packet update: average solar-system support ratios now populate `K_N(s)` for the `epsilon_Gsrc_perp` Newton/source gate. This is a pre-score geometry fill, not a pass. The next packet task is to decompose or source `E_perp`, or prove the species-blind measure-owner edge.
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
                "4371 fills source-backed average support geometry examples for the epsilon_Gsrc_perp coefficient gate using NASA solar-system size/distance data. "
                "The gate is now immediately scoreable once E_perp and delta_N are supplied: E_perp<=delta_N/K_N(s), with concrete Sun-planet and Earth-Moon K_N(s) rows. "
                "It also derives a conditional measure-owner lemma: a q-basic species-blind measure/Jacobian/hbar owner would zero the measure contribution to epsilon_Gsrc_perp. "
                "That edge remains unsigned in 4361/1606, E_perp and delta_N remain unsourced, and no local-GR/Newton/PPN/WEP/clock/orbital/R10 claim fires."
            ),
            "4371 local source register, external source register, support geometry rows, measure-owner lemma, acquisition rows, claim gates, decision, status, next target and validation CSV.",
            "source_support_geometry_anchors_filled_measure_owner_lemma_unsigned_Eperp_missing_nonclaim",
            "Decompose E_perp into source-measure/source-mass/transition/Xi/T envelopes or prove the species-blind measure/Jacobian action-line edge.",
            "Treating support geometry as a pass; fitting E_perp or delta_N after data; claiming measure-owner zero without excluding species Jacobian/hbar/field-normalization slots.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_REGISTER.csv")
    external = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_EXTERNAL_SOURCE_REGISTER.csv")
    support = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv")
    measure = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_MEASURE_OWNER_LEMMA.csv")
    acquisition = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_ACQUISITION_ROWS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4371_0_local_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4371_1_local_needles_found", all(row["needle_found"] == "True" for row in sources), "every local source needle resolves")
    add("VAL4371_2_external_urls_present", all(row["url"].startswith("https://") for row in external), "external URLs recorded")
    add(
        "VAL4371_3_support_positive",
        all(float(row["R_source_km"]) > 0 and float(row["r_readout_km"]) > 0 for row in support),
        "support radii and readout distances positive",
    )
    add(
        "VAL4371_4_support_exterior",
        all(0 < float(row["s_R_over_r"]) < 1 for row in support),
        "all support examples satisfy 0<R/r<1",
    )
    add(
        "VAL4371_5_geometry_factors_positive",
        all(float(row["selected_K_N"]) > 0 for row in support),
        "all K_N values positive",
    )
    add(
        "VAL4371_6_Eperp_not_sourced",
        all(row["Eperp_source_backed"] == "False" for row in support),
        "support rows do not pretend E_perp is sourced",
    )
    add(
        "VAL4371_7_measure_lemma_conditional",
        any(row["lemma_id"] == "MO4371_0_measure_zero_lemma" and row["current_activation"] == "NOT_PARENT_SIGNED" for row in measure),
        "measure-owner lemma remains conditional",
    )
    add(
        "VAL4371_8_acquisition_Eperp_missing",
        any(row["input_id"] == "ACQ4371_0_Eperp_bound" and row["current_status"] == "MISSING" for row in acquisition),
        "E_perp acquisition remains explicit",
    )
    add("VAL4371_9_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4371_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4371_11_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4371_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4371_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4371_14_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4371_15_no_valid_claim_rows",
        all("True" not in [row.get("valid_for_claim", ""), row.get("claim_allowed", "")] for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add(
        "VAL4371_16_csv_parse",
        all(len(read_csv(path)) > 0 for path in csv_paths),
        "all generated CSVs parse",
    )
    return validations


def main() -> None:
    sources = source_rows()
    external_sources = external_source_rows()
    support = support_rows()
    measure = measure_owner_lemma_rows()
    acquisition = acquisition_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4371_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4371_EXTERNAL_SOURCE_REGISTER.csv": external_sources,
        "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv": support,
        "P8_Y5_R2FR_4371_MEASURE_OWNER_LEMMA.csv": measure,
        "P8_Y5_R2FR_4371_ACQUISITION_ROWS.csv": acquisition,
        "P8_Y5_R2FR_4371_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4371_DECISION.csv": decisions,
        "P8_Y5_R2FR_4371_STATUS.csv": statuses,
        "P8_Y5_R2FR_4371_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, external_sources, support, measure, acquisition, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()

    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
