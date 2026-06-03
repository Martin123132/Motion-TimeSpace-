from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Andersen-HFGW-EM-charge-relevance-audit"
CHECKPOINT_DOC = "459A-Andersen-HFGW-EM-charge-relevance-audit.md"
STATUS = "Andersen_HFGW_EM_charge_relevance_audit_written_useful_charge_clues_retained_speculative_no_MTS_claim_or_priority_claim_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "external_charge_paper_intake_only_no_MTS_priority_EM_derivation_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "459-PG-calibration-residual-mapper.md"
CONTRACT_PATH = Path("source-intake/external_papers/Andersen_2026_HFGW_EM_charge_relevance_AUDIT.csv")

PAPER_PATH = Path("[external-paper]/emergent-electromagnetism-from-high-frequency-gravitational-relics.pdf")
IMAGE_ONE_PATH = Path("[external-image]/ea326bb9-a1bf-46f3-b47d-19e3942cf197.png")
IMAGE_TWO_PATH = Path("[external-image]/c7f0378f-66d7-4634-9346-d5a96dee749a.png")


AUDIT_COLUMNS = [
    "audit_id",
    "paper_feature",
    "possible_MTS_use",
    "required_derivation_or_check",
    "risk_if_used_uncritically",
    "status",
    "next_action",
]


SOURCE_DOCS = [
    {
        "path": str(PAPER_PATH),
        "role": "primary external paper being audited for charge-sector clues",
    },
    {
        "path": str(IMAGE_ONE_PATH),
        "role": "screenshot context for public post; not physics evidence",
    },
    {
        "path": str(IMAGE_TWO_PATH),
        "role": "screenshot context for author/profile; not physics evidence",
    },
    {
        "path": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "role": "current Hamiltonian/charge route needing clean charge/current mapping",
    },
    {
        "path": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "current measured-GM/Poisson/Gauss charge calibration gate",
    },
    {
        "path": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "role": "PG rows that must not be bypassed by external EM speculation",
    },
    {
        "path": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "role": "constant coupling caution for any charge-strength formula",
    },
    {
        "path": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "measured source calibration caution",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "residual rows that external charge ideas must map into if not derived",
    },
]


PAPER_FEATURES = [
    {
        "feature": "uncharged_Kerr_relic_as_electron",
        "paper_content": "electron modelled as an uncharged overspun Kerr ring/naked singularity",
        "MTS_relevance": "suggests charge might be emergent from geometry/topology rather than a primitive U(1) label",
        "usable_status": "interesting_speculative_clue",
        "caution": "overspun naked singularity stability, source regularity, and quantum electron data are not derived in MTS",
    },
    {
        "feature": "high_frequency_metric_carrier",
        "paper_content": "metric perturbation carrier at a Schwarzschild-scale frequency is averaged into macroscopic EM-like behaviour",
        "MTS_relevance": "could inspire an MTS carrier/envelope split for EM where observable fields are coarse-grained motion-time-space phases",
        "usable_status": "useful_structural_clue",
        "caution": "frequency, amplitude, and coarse-graining scale must be parent-derived and not fitted after the fact",
    },
    {
        "feature": "Coulomb_as_radiation_pressure",
        "paper_content": "inverse-square force arises from high-frequency gravitational-wave flux and absorption cross-section",
        "MTS_relevance": "gives a possible charge-amplitude law: charge strength as flux times interaction cross-section",
        "usable_status": "candidate_derivation_template",
        "caution": "radiation pressure sign, normalization, and cross-section law require a full stress-energy/force derivation",
    },
    {
        "feature": "charge_sign_as_relative_phase",
        "paper_content": "attraction and repulsion are assigned to relative phase of coherent oscillators",
        "MTS_relevance": "very relevant to MTS if charge polarity becomes a phase/state of the motion field rather than a separate substance",
        "usable_status": "promising_but_unproved",
        "caution": "phase rule must derive both signs, charge conservation, quantization, and Lorentz-covariant force law",
    },
    {
        "feature": "magnetism_from_frame_dragging",
        "paper_content": "magnetic-like effects are tied to Kerr frame dragging and a double-copy style map",
        "MTS_relevance": "could help an EM branch connect spin/vorticity/current to gauge-like vector potential",
        "usable_status": "formal_bridge_clue",
        "caution": "double-copy analogy is not automatically Maxwell theory or a matter-coupling theorem",
    },
    {
        "feature": "tiny_strain_large_effect",
        "paper_content": "very small metric strain is argued to create Coulomb-scale force because the carrier frequency is extreme",
        "MTS_relevance": "could help MTS separate locally tiny metric disturbance from strong effective charge coupling",
        "usable_status": "scale_separation_clue",
        "caution": "dimensional consistency and amplitude/cross-section degeneracy need a ruthless audit",
    },
]


MTS_USE_AUDIT = [
    {
        "audit_id": "A0_cite_as_external_inspiration",
        "paper_feature": "overall HFGW/Kerr relic EM proposal",
        "possible_MTS_use": "cite Andersen as an external speculative parallel if MTS develops a geometric/emergent charge branch",
        "required_derivation_or_check": "separate MTS derivation from paper's claims and cite only for inspiration/comparison",
        "risk_if_used_uncritically": "confusing external speculative model with an MTS theorem or priority claim",
        "status": "allowed_with_citation_and_scope",
        "next_action": "keep as source-intake reference, not as proof",
    },
    {
        "audit_id": "A1_charge_amplitude_law",
        "paper_feature": "e^2 proportional to omega_s^2 sigma_abs h0^2 / G style relation",
        "possible_MTS_use": "candidate law connecting effective charge to carrier frequency, cross-section, and strain/amplitude",
        "required_derivation_or_check": "dimensional audit, unit convention check, independent origin for frequency/amplitude/cross-section",
        "risk_if_used_uncritically": "turning charge into a fitted product with too many knobs",
        "status": "candidate_not_derived",
        "next_action": "write a charge-amplitude dimensional ledger if EM branch is opened",
    },
    {
        "audit_id": "A2_phase_polarity",
        "paper_feature": "relative oscillator phase maps to attraction/repulsion",
        "possible_MTS_use": "candidate route for charge sign as phase orientation in an MTS carrier field",
        "required_derivation_or_check": "derive phase-force sign from a stress tensor or action; prove charge conservation and quantization",
        "risk_if_used_uncritically": "phase labels become a renamed positive/negative charge axiom",
        "status": "promising_but_unproved",
        "next_action": "test whether MTS has an existing phase/current variable that can carry a conserved sign class",
    },
    {
        "audit_id": "A3_Isaacson_effective_stress",
        "paper_feature": "high-frequency gravitational perturbations averaged into effective energy-momentum",
        "possible_MTS_use": "technical clue for deriving an effective EM stress/current after coarse-graining",
        "required_derivation_or_check": "covariant averaging, gauge control, conservation law, and backreaction ledger",
        "risk_if_used_uncritically": "averaging hides non-conservation or gauge artefacts",
        "status": "useful_method_clue",
        "next_action": "map to future MTS EM stress tensor only after parent action is explicit",
    },
    {
        "audit_id": "A4_Kerr_frame_dragging_vector_potential",
        "paper_feature": "frame-dragging term mapped to magnetic/vector potential behaviour",
        "possible_MTS_use": "possible route from spin/vorticity/motion flow to magnetic sector",
        "required_derivation_or_check": "derive Maxwell-like equations and Lorentz force from one observed matter frame",
        "risk_if_used_uncritically": "double-copy or analogy replaces a real gauge/matter-coupling theorem",
        "status": "formal_clue_only",
        "next_action": "hold for EM branch; do not use to close GR/Newton mass gates",
    },
    {
        "audit_id": "A5_not_a_PG_gate_closer",
        "paper_feature": "emergent EM force from metric relics",
        "possible_MTS_use": "may inform charge sector, not measured-GM/Poisson-Gauss closure",
        "required_derivation_or_check": "PG0-PG10 still need their own parent-derived evidence",
        "risk_if_used_uncritically": "using EM analogy to bypass measured mass/source-normalization gates",
        "status": "does_not_close_current_GR_Newton_gate",
        "next_action": "continue PG residual mapper for mass/Newton route",
    },
]


BLOCKERS = [
    {
        "blocker": "Maxwell_equations_not_derived",
        "why_it_matters": "emergent charge must reproduce Gauss law, Faraday law, Ampere-Maxwell law, and no-monopole constraint in one frame",
        "MTS_requirement": "derive gauge-like field equations or a tested residual vector",
    },
    {
        "blocker": "U1_charge_conservation_missing",
        "why_it_matters": "charge cannot just be force strength; it needs a conserved current and continuity equation",
        "MTS_requirement": "derive a conserved charge current or exact topological phase class",
    },
    {
        "blocker": "charge_quantization_missing",
        "why_it_matters": "electron charge magnitude and sign class must be discrete, not an arbitrary amplitude product",
        "MTS_requirement": "derive a quantization/topology condition or mark the amplitude fitted",
    },
    {
        "blocker": "force_sign_derivation_missing",
        "why_it_matters": "radiation pressure is naturally repulsive; attraction needs exact phase/stress proof",
        "MTS_requirement": "derive attractive and repulsive branches from a single action/stress tensor",
    },
    {
        "blocker": "regularity_and_source_model_missing",
        "why_it_matters": "naked singularity/ring source is physically dangerous and can hide infinities",
        "MTS_requirement": "regularize the carrier source or move to topological/defect variables with finite observables",
    },
    {
        "blocker": "not_a_local_GR_promotion",
        "why_it_matters": "an EM emergence idea does not close measured-GM, PPN, or EH-source normalization gates",
        "MTS_requirement": "keep GR/Newton PG rows separate from EM/charge branch rows",
    },
]


CITATION_POLICY = [
    {
        "rule": "cite_if_used",
        "policy": "If any MTS EM/charge document uses the HFGW/Kerr carrier, phase-polarity, or frame-dragging analogy, cite Andersen 2026 explicitly.",
    },
    {
        "rule": "no_priority_claim",
        "policy": "Do not claim influence, priority, or copying from screenshots/likes; treat provenance as outside the physics audit.",
    },
    {
        "rule": "not_authority_proof",
        "policy": "Breakthrough-prize/profile context is not evidence that the model is correct; only equations and derivations count.",
    },
    {
        "rule": "speculative_label",
        "policy": "Classify the paper as an external speculative clue unless a peer-reviewed or internally derived theorem later supports it.",
    },
]


GATE_RESULTS_STATIC = [
    {
        "gate": "paper_text_extracted",
        "status": "pass",
        "evidence": "4 PDF pages extracted with pypdf for private source-intake audit",
    },
    {
        "gate": "charge_relevance_identified",
        "status": "pass",
        "evidence": "carrier flux, phase polarity, frame dragging, and charge-amplitude clues recorded",
    },
    {
        "gate": "citation_policy_written",
        "status": "pass",
        "evidence": "Andersen cite-if-used and no-priority-claim rules recorded",
    },
    {
        "gate": "PG_gate_not_bypassed",
        "status": "pass",
        "evidence": "A5 and not_a_local_GR_promotion blocker preserve PG0-PG10 gates",
    },
    {
        "gate": "usable_as_MTS_theorem",
        "status": "fail",
        "evidence": "paper is external/speculative and does not derive MTS parent action or EM branch",
    },
    {
        "gate": "EM_charge_branch_promoted",
        "status": "fail",
        "evidence": "Maxwell equations, charge conservation, quantization, and force sign derivation remain open",
    },
    {
        "gate": "Newton_or_local_GR_promoted",
        "status": "fail",
        "evidence": "external EM paper intake only",
    },
]


DECISION = [
    {
        "decision": "Andersen's paper is useful as a charge-sector clue, not as a theorem we can import. The strongest MTS-relevant ideas are charge as a high-frequency metric/carrier flux, charge polarity as oscillator phase, and magnetism as spin/vorticity/frame-dragging. These could help build an EM branch later, especially a charge-amplitude and phase-current ledger. But the paper does not close the current Hamiltonian-to-Poisson/Gauss mass gate, and it does not by itself derive Maxwell equations, charge conservation, quantization, or local-GR reduction. If we use any of these ideas, cite Andersen 2026 clearly and keep it labelled as external speculative inspiration until MTS derives it independently.",
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "459-PG-calibration-residual-mapper.md",
        "why_next": "the core GR/Newton route still needs failed PG0-PG10 rows mapped into executable P8/R11 residuals",
    },
    {
        "rank": 2,
        "target": "EM-charge-amplitude-dimensional-ledger",
        "why_next": "if opening the EM branch, first test the Andersen-like charge-amplitude law for units, knobs, and derivability",
    },
    {
        "rank": 3,
        "target": "phase-current-charge-conservation-gate",
        "why_next": "phase polarity is only useful if it becomes a conserved charge current rather than renamed +/- charge",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    csv_fieldnames = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    table_fieldnames = fieldnames or list(rows[0].keys())
    lines = [
        "| " + " | ".join(table_fieldnames) + " |",
        "| " + " | ".join(["---"] * len(table_fieldnames)) + " |",
    ]
    for row in rows:
        values = []
        for fieldname in table_fieldnames:
            value = str(row.get(fieldname, "")).replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_exists(path_text: str) -> bool:
    path = Path(path_text)
    if path.is_absolute():
        return path.exists()
    return (ROOT / path).exists()


def build_source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_file": source_doc["path"],
            "exists": source_exists(source_doc["path"]),
            "role": source_doc["role"],
        }
        for source_doc in SOURCE_DOCS
    ]


def build_gate_results(source_register: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in source_register if not row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all cited source paths exist" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "audit_schema_matches",
            "status": "pass" if list(MTS_USE_AUDIT[0].keys()) == AUDIT_COLUMNS else "fail",
            "evidence": "external paper audit columns match schema",
        },
        *GATE_RESULTS_STATIC,
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 459A - Andersen HFGW EM Charge Relevance Audit

Private external-paper charge-sector intake. This is not a public MTS priority, authorship, plagiarism, EM derivation, measured-GM, Newtonian-limit, PPN, local-GR, cosmology, or unified-field claim.

## 1. Purpose

The user supplied Andersen's February 2026 paper on emergent electromagnetism from high-frequency Kerr/gravitational relics and asked whether it can help the current charge work.

This checkpoint answers narrowly: what clues are useful for MTS, what must be cited, and what cannot be imported as proof.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Andersen_HFGW_EM_charge_relevance_audit.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Audit CSV | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Paper Features

{markdown_table(PAPER_FEATURES)}

## 5. MTS Use Audit

The external charge-paper audit has been written to `{CONTRACT_PATH}`.

{markdown_table(MTS_USE_AUDIT, AUDIT_COLUMNS)}

## 6. Main Blockers

{markdown_table(BLOCKERS)}

## 7. Citation and Attribution Policy

{markdown_table(CITATION_POLICY)}

## 8. Gate Results

{markdown_table(gate_results)}

## 9. Decision

{DECISION[0]["decision"]}

Practical read: yes, this paper can give us a clue, but not a shortcut. The useful punch is: charge could be a phase/coherence/flux property of an underlying geometric carrier. For MTS, the next honest version would be to ask whether charge is a conserved phase-current of the motion-time-space carrier, with a derived amplitude law. The paper does not get the GR/Newton mass gates over the line.

## 10. Next Queue

{markdown_table(NEXT_QUEUE)}
"""


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_register = build_source_register()
    gate_results = build_gate_results(source_register)
    missing_sources = [row["source_file"] for row in source_register if not row["exists"]]

    write_csv(results_dir / "source_register.csv", source_register)
    write_csv(results_dir / "paper_features.csv", PAPER_FEATURES)
    write_csv(results_dir / "MTS_use_audit.csv", MTS_USE_AUDIT, AUDIT_COLUMNS)
    write_csv(results_dir / "blockers.csv", BLOCKERS)
    write_csv(results_dir / "citation_policy.csv", CITATION_POLICY)
    write_csv(results_dir / "gate_results.csv", gate_results)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / CONTRACT_PATH, MTS_USE_AUDIT, AUDIT_COLUMNS)

    doc_text = render_doc(run_dir, source_register, gate_results)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    status_payload = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "charge_relevance_identified": True,
        "citation_policy_written": True,
        "PG_gate_not_bypassed": True,
        "usable_as_MTS_theorem": False,
        "EM_charge_branch_promoted": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "audit_rows": len(MTS_USE_AUDIT),
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\n{datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the Andersen HFGW EM charge relevance audit.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-185500.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
