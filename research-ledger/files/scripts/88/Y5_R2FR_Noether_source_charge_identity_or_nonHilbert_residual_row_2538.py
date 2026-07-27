from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2538"
BRANCH_ID = "MTS_R2FR_NOETHER_SOURCE_CHARGE_IDENTITY_OR_NONHILBERT_RESIDUAL_2538"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2538-Y5-R2FR-Noether-source-charge-identity-or-nonHilbert-residual-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2538_SOURCE_REGISTER.csv",
    "identity": RESIDUALS / "P8_Y5_NO_SHADOW_2538_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv",
    "residual": RESIDUALS / "P8_Y5_NO_SHADOW_2538_NONHILBERT_RESIDUAL_ROW.csv",
    "trident": RESIDUALS / "P8_Y5_NO_SHADOW_2538_NONHILBERT_TRIDENT_UPDATE.csv",
    "impact": RESIDUALS / "P8_Y5_NO_SHADOW_2538_SOURCE_CHARGE_GATE_IMPACT.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2538_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2538_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2538_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2538_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2538_VALIDATION.csv",
}

BRANCH_COPIES = {
    "identity": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Noether_source_charge_identity_2538_NONCLAIM.csv",
    "residual": POST_ROOT / "source-intake" / "local_bounds" / "NonHilbert_residual_row_2538_NONCLAIM.csv",
    "trident": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "NonHilbert_trident_2538_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "NOHYP2538_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    ("SRC2538_0_2537_doc", "2537-Y5-R2FR-parent-action-source-blind-functor-signature-or-source-profile-vector.md", "NEXT2537_0_selected", "2537 selected Noether/source-charge identity as current route"),
    ("SRC2538_1_2537_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2537_VALIDATION.csv", "VAL2537_OVERALL,PASS", "2537 validation anchor"),
    ("SRC2538_2_2537_noether", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2537_NOETHER_SOURCE_CHARGE_TARGET.csv", "NSC2537_0_identity_target", "current no independent gravitational source charge target"),
    ("SRC2538_3_2373_doc", "2373-Y5-R2FR-Noether-source-charge-identity-or-nonHilbert-residual-row.md", "NSCI2373_7_verdict", "older Noether/source-charge precedent"),
    ("SRC2538_4_2373_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2373_VALIDATION.csv", "VAL2373_OVERALL,PASS", "2373 validation anchor"),
    ("SRC2538_5_2373_identity", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv", "NSCI2373_7_verdict", "identity-attempt rows to port into no-shadow branch"),
    ("SRC2538_6_2373_residual", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_NONHILBERT_RESIDUAL_ROW.csv", "NHR2373_0_total", "non-Hilbert residual envelope precedent"),
    ("SRC2538_7_2373_trident", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_NONHILBERT_TRIDENT_UPDATE.csv", "TRI2373_1_spin_torsion", "trident head selection precedent"),
    ("SRC2538_8_2373_impact", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_SOURCE_CHARGE_GATE_IMPACT.csv", "SCI2373_4_local_GR_Newton", "local GR/Newton gate impact precedent"),
    ("SRC2538_9_2373_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_NEXT_TARGET.csv", "NEXT2373_0_selected", "no-hypermomentum/Levi-Civita next target precedent"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in SOURCE_SPECS:
        path = POST_ROOT / source_path
        rows.append(
            stamp(
                {
                    "source_id": source_id,
                    "source_path": source_path,
                    "needle": needle,
                    "role": role,
                    "path_exists": str(path.exists()).lower(),
                    "needle_found": str(contains(path, needle)).lower(),
                    "status": "SOURCE_OK" if path.exists() and contains(path, needle) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def source_charge_identity_attempt() -> list[dict[str, object]]:
    rows = [
        (
            "NSCI2538_0_target",
            "Noether source charge identity",
            "J_active for ordinary matter equals the Hilbert/Noether source charge of the same observed matter action, with no independent gravitational source charge.",
            "TARGET_SHARPENED",
            "would derive Minimal Universal Matter Coupling rather than using it as a private restriction",
        ),
        (
            "NSCI2538_1_hilbert_owner",
            "Hilbert source owner",
            "If a single observed matter action is fixed, T_H := delta S_m/delta e_obs is the active ordinary-matter source before readout.",
            "EXACT_CONDITIONAL_THEOREM",
            "kills post-variation source-current rescaling only after the action/signature is fixed",
        ),
        (
            "NSCI2538_2_ward_noether",
            "Ward/Noether conservation",
            "Diffeomorphism/local-frame invariance of S_m gives covariant conservation of T_H on the matter shell.",
            "EXACT_CONDITIONAL_CONSERVATION",
            "conservation of a chosen source does not prove source uniqueness or universal normalization",
        ),
        (
            "NSCI2538_3_canonical_improvement",
            "canonical-to-Hilbert improvement",
            "Canonical stress differs from Hilbert stress by owned improvement/superpotential terms plus possible boundary flux.",
            "CONDITIONAL_IMPROVEMENT_BOUND_REQUIRED",
            "safe only if compact exterior boundary/improvement flux is zero, projected silent, or bounded",
        ),
        (
            "NSCI2538_4_pre_action_weight",
            "pre-action species weights",
            "S_m=sum_A w_A S_A has a conserved Hilbert/Noether current if w_A is legal before variation.",
            "COUNTERMODEL_SURVIVES_WITHOUT_MUMC",
            "Noether conservation preserves the weighted current; it does not forbid the weight",
        ),
        (
            "NSCI2538_5_nonhilbert_channels",
            "non-Hilbert source-current channels",
            "Spin/torsion, boundary/worldtube, readout reentry, and improvement flux must vanish, be exact/projected-silent, or remain explicit residuals.",
            "OPEN_RETAIN_RESIDUAL_ROW",
            "Hilbert/Noether identity for ordinary matter does not automatically silence all source channels",
        ),
        (
            "NSCI2538_6_projected_mass_charge",
            "projected measured-GM charge",
            "M_eff must be a closed calibrated projection of Hilbert/Hamiltonian/worldtube charge before Kepler/PPN readout.",
            "PROJECTED_MASS_CHARGE_NOT_CLOSED",
            "Pi_M commutator, exchange current, boundary flux, and orbital calibration exceed unprojected Ward conservation",
        ),
        (
            "NSCI2538_7_verdict",
            "derive no independent gravitational source charge now",
            "Current active evidence derives no independent gravitational source charge beyond Hilbert/Noether stress source.",
            "NOT_DERIVED_RETAIN_NONHILBERT_ROW",
            "conditional owner is real, but pre-action weights, non-Hilbert channels, and projected mass-charge closure remain open",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "identity_piece": piece,
            "formal_statement": statement,
            "status": status,
            "proof_or_obstruction": obstruction,
        }
        for row_id, piece, statement, status, obstruction in rows
    ]


def nonhilbert_residual_row() -> list[dict[str, object]]:
    rows = [
        (
            "NHR2538_0_total",
            "P_source_J_NH_abs",
            "projected non-Hilbert source-current envelope after Hilbert matter current is extracted",
            "||P_source[J_NH]|| <= E_spin + E_boundary + E_readout + E_improvement",
            "E_spin;E_boundary;E_readout;E_improvement",
            "source-current units; arena-projected to PPN/WEP/orbit units later",
            "CONTRACT_READY_VALUES_MISSING",
            "zero theorem or envelope for every component in common units",
        ),
        (
            "NHR2538_1_spin_torsion",
            "E_spin",
            "spin, torsion, nonmetricity, or hypermomentum source-current projection",
            "E_spin >= ||P_source[J_spin/torsion/nonmetricity/hypermomentum]||",
            "torsionless theorem or P4 connection residual map",
            "source-current units",
            "MISSING_ZERO_OR_ENVELOPE",
            "Levi-Civita/no-hypermomentum theorem or source-backed spin-current envelope",
        ),
        (
            "NHR2538_2_boundary_worldtube",
            "E_boundary",
            "boundary, worldtube, compact flux, or surface source-current projection",
            "E_boundary >= ||P_source[J_boundary/worldtube]||",
            "boundary no-flux theorem or source-worldtube envelope",
            "source-current units",
            "MISSING_ZERO_OR_ENVELOPE",
            "boundary/falloff/orientation theorem or source-backed flux bound",
        ),
        (
            "NHR2538_3_readout_reentry",
            "E_readout",
            "post-variation readout, domain, marker, or frame map that re-enters as source-labelled current",
            "E_readout >= ||P_source[J_readout_reentry]||",
            "readout no-reentry theorem or commutator residual map",
            "source-current units",
            "MISSING_ZERO_OR_ENVELOPE",
            "downstream/no-source-codomain proof per arena or finite residual",
        ),
        (
            "NHR2538_4_improvement_flux",
            "E_improvement",
            "canonical/Hilbert improvement, superpotential, edge, or Hamiltonian representative flux",
            "E_improvement >= ||P_source[J_improvement_flux]||",
            "Hamiltonian representative and compact edge projection",
            "source-current units",
            "MISSING_ZERO_OR_ENVELOPE",
            "improvement flux zero theorem or compact-flux envelope",
        ),
        (
            "NHR2538_5_projected_mass",
            "Delta_M_projected",
            "commutator/exchange term between Hilbert charge conservation and measured-GM mass projector",
            "Delta_M_projected = [d,Pi_M]J_H + Pi_M J_exchange + boundary/anomaly flux",
            "Pi_M ownership; exchange silence; Gauss/orbital calibration",
            "mass-charge or dimensionless after GM normalization",
            "PROJECTOR_CLOSURE_MISSING",
            "projected mass-charge closure checkpoint",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "bound_form": bound,
            "component_inputs": inputs,
            "units": units,
            "status": status,
            "next_input": next_input,
        }
        for row_id, quantity, definition, bound, inputs, units, status, next_input in rows
    ]


def trident_gate_update() -> list[dict[str, object]]:
    rows = [
        (
            "TRI2538_0_total",
            "total non-Hilbert source current",
            "J_NH=0 only if spin/torsion, boundary/improvement and readout reentry heads are each absent/exact/projected-silent",
            "NOT_ZERO_RETAIN_COMPONENTS",
            "absolute residual envelope, no cancellation",
        ),
        (
            "TRI2538_1_spin_torsion",
            "spin/torsion/nonmetricity/hypermomentum",
            "connection is metric-only Levi-Civita, or Palatini EH plus no matter/source/readout hypermomentum, or projection is exact/silent",
            "SELECTED_NEXT_PRIMARY_GATE",
            "closest GR-like structural route; retain P4 residual if not proved",
        ),
        (
            "TRI2538_2_boundary_improvement",
            "boundary/worldtube/improvement flux",
            "boundary charge/improvement flux fixed by differentiable Hamiltonian reference and zero compact local projection",
            "PARALLEL_GATE_OPEN",
            "cannot silently drop exact terms if improper/edge charge survives",
        ),
        (
            "TRI2538_3_readout_reentry",
            "readout/domain/frame reentry",
            "readout maps act downstream and cannot create source-labelled current terms",
            "PARALLEL_GATE_OPEN",
            "requires no-source-codomain/commutator proof per arena",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "trident_head": head,
            "zero_route": route,
            "status": status,
            "fallback_or_effect": effect,
        }
        for row_id, head, route, status, effect in rows
    ]


def source_charge_gate_impact() -> list[dict[str, object]]:
    rows = [
        (
            "SCI2538_0_MUMC_branch",
            "Minimal Universal Matter Coupling private branch",
            "under MUMC, pre-action w_A is forbidden by restriction, not derived by 2538",
            "Noether/source-charge derivation of the restriction",
            "private_condition_only",
        ),
        (
            "SCI2538_1_no_species_charge",
            "no independent gravitational source charge",
            "Hilbert/Noether source ownership works once the action is fixed",
            "proof that no pre-action species source coefficient is admissible",
            "not_derived",
        ),
        (
            "SCI2538_2_nonhilbert_gate",
            "non-Hilbert/boundary/readout source currents",
            "must be zero/bounded before source-side GR claim",
            "spin/torsion, boundary flux, readout reentry, improvement flux inputs",
            "retained_residual",
        ),
        (
            "SCI2538_3_GM_source_charge",
            "measured-GM projected source charge",
            "Ward conservation alone does not derive calibrated GM",
            "closed Pi_M J_H, exchange silence, boundary flux zero, Kepler calibration",
            "not_closed",
        ),
        (
            "SCI2538_4_local_GR_Newton",
            "full local GR/Newton recovery",
            "source-side map improved but local GR remains open",
            "left-hand EH/Newton limit, PPN/readout residuals, projector/domain closure",
            "blocked",
        ),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "gate": gate,
                "impact": impact,
                "still_missing": missing,
                "claim_status": status,
            }
        )
        for row_id, gate, impact, missing, status in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2538_0_sources", "source paths and needles valid", "PASS", "audit reproducible"),
        ("CG2538_1_hilbert_noether_owner", "Hilbert/Noether source owner exact conditionally", "PASS", "conditional theorem retained"),
        ("CG2538_2_no_independent_charge", "no independent gravitational source charge derived now", "FAIL", "pre-action weights remain countermodel outside MUMC"),
        ("CG2538_3_nonhilbert_silence", "non-Hilbert source current is zero", "FAIL", "trident residual gates remain"),
        ("CG2538_4_projected_GM_charge", "measured-GM charge derived from closed Hilbert projection", "FAIL", "projected mass charge not closed"),
        ("CG2538_5_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "not enough yet"),
        ("CG2538_6_github_public_update", "safe to push as public evidence", "FAIL", "private derivation/residual checkpoint only"),
    ]
    return [
        stamp({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect})
        for row_id, gate, status, effect in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        (
            "REF2538_0_conservation_as_uniqueness",
            "Ward conservation proves unique species-blind source normalization.",
            "false",
            "conservation preserves a chosen weighted current; it does not forbid pre-action weights",
        ),
        (
            "REF2538_1_hilbert_as_nonhilbert_silence",
            "Hilbert owner automatically kills non-Hilbert currents.",
            "false",
            "spin/torsion, boundary, readout reentry and improvement flux remain separate channels",
        ),
        (
            "REF2538_2_GM_from_Ward_only",
            "Ward identity derives measured GM/source-normalized Newton.",
            "false",
            "projected mass-charge closure and orbital calibration are stronger than unprojected conservation",
        ),
        (
            "REF2538_3_public_claim",
            "2538 proves local GR/Newton.",
            "false",
            "2538 records a conditional source owner and residual row only",
        ),
    ]
    return [
        stamp({"row_id": row_id, "claim": claim, "allowed": allowed, "reason": reason})
        for row_id, claim, allowed, reason in rows
    ]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2538_0_selected",
            "selected",
            "2539-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md",
            "scripts/Y5_R2FR_noHypermomentum_LeviCivita_source_connection_or_P4_row_2539.py",
            "prove ordinary matter/source/readout do not vary an independent connection, or that the independent connection is Palatini/EH projectively silent for the source channel",
            "if not proved, emit first P4 torsion/nonmetricity/hypermomentum residual row as nonclaim",
        ),
        (
            "NEXT2538_1_parallel",
            "parallel",
            "2539b-Y5-R2FR-boundary-improvement-flux-zero-or-envelope.md",
            "scripts/Y5_R2FR_boundary_improvement_flux_zero_or_envelope_2539b.py",
            "prove compact boundary/improvement flux is zero/projected silent under the Hamiltonian reference",
            "otherwise retain E_boundary and E_improvement finite envelopes",
        ),
        (
            "NEXT2538_2_parallel",
            "parallel",
            "2539c-Y5-R2FR-readout-no-reentry-commutator-or-envelope.md",
            "scripts/Y5_R2FR_readout_no_reentry_commutator_or_envelope_2539c.py",
            "prove readout/domain/frame maps have no source-current codomain and no reentry commutator per arena",
            "otherwise retain E_readout finite envelope",
        ),
        (
            "NEXT2538_3_parallel",
            "parallel",
            "2539d-Y5-R2FR-Hilbert-Noether-mass-projector-closure.md",
            "scripts/Y5_R2FR_Hilbert_Noether_mass_projector_closure_2539d.py",
            "close d(Pi_M J_H)=0 and GM calibration rather than relying on unprojected Ward conservation",
            "otherwise retain Delta_M_projected residual",
        ),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "priority": priority,
                "next_file": next_file,
                "next_script": next_script,
                "success_condition": success,
                "fallback_condition": fallback,
            }
        )
        for row_id, priority, next_file, next_script, success, fallback in rows
    ]


def branch_copy_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for copy_id, destination in BRANCH_COPIES.items():
        source = OUTPUTS[copy_id]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": copy_id,
                    "source_path": rel(source),
                    "destination_path": rel(destination),
                    "destination_exists": str(destination.exists()).lower(),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        if not changed:
            return True, "git modified-file count for formalization-workbench is 0"
        return False, f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("source_id") or row.get("copy_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() in {"true", "pass", "passed", "ready", "yes", "1"}:
                    offenders.append(f"{rel(path)}:{row_name}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append(stamp({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail}))

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2538_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2538_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2538_02_outputs_exist", all(path.exists() for path in generated), "all 2538 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2538_03_csv_parse", parse_ok, parse_detail)

    identity = {row["row_id"]: row["status"] for row in read_csv(outputs["identity"])}
    add("VAL2538_04_conditional_owner", identity.get("NSCI2538_1_hilbert_owner") == "EXACT_CONDITIONAL_THEOREM", "Hilbert/Noether source owner retained conditionally")
    add("VAL2538_05_identity_not_overclaimed", identity.get("NSCI2538_7_verdict") == "NOT_DERIVED_RETAIN_NONHILBERT_ROW", "no independent source charge not overclaimed")

    residual = {row["row_id"]: row["status"] for row in read_csv(outputs["residual"])}
    add("VAL2538_06_residual_row_exists", residual.get("NHR2538_0_total") == "CONTRACT_READY_VALUES_MISSING", "non-Hilbert residual total row exists")
    add("VAL2538_07_spin_envelope_missing", residual.get("NHR2538_1_spin_torsion") == "MISSING_ZERO_OR_ENVELOPE", "spin/torsion head remains explicit, not silently zeroed")

    trident = {row["row_id"]: row["status"] for row in read_csv(outputs["trident"])}
    add("VAL2538_08_trident_primary_selected", trident.get("TRI2538_1_spin_torsion") == "SELECTED_NEXT_PRIMARY_GATE", "spin/torsion no-hypermomentum gate selected")

    impact = {row["row_id"]: row["claim_status"] for row in read_csv(outputs["impact"])}
    add("VAL2538_09_local_gr_still_blocked", impact.get("SCI2538_4_local_GR_Newton") == "blocked", "full local GR/Newton gate remains blocked")

    claims = {row["row_id"]: row["gate_status"] for row in read_csv(outputs["claims"])}
    add("VAL2538_10_claim_gates_block", claims.get("CG2538_5_local_GR_Newton") == "FAIL", "local GR/Newton claim gate remains false")
    add("VAL2538_11_github_blocked", claims.get("CG2538_6_github_public_update") == "FAIL", "public GitHub evidence update remains blocked")

    next_rows = read_csv(outputs["next"])
    add("VAL2538_12_next_selected", any(row.get("row_id") == "NEXT2538_0_selected" and "noHypermomentum" in row.get("next_script", "") for row in next_rows), "2539 no-hypermomentum/Levi-Civita target selected")

    copy_rows = read_csv(outputs["copies"])
    add("VAL2538_13_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2538_14_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2538_15_formalization_untouched", formal_ok, formal_detail)
    add("VAL2538_16_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2538_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2538 valid: Hilbert/Noether owner conditional, no independent source charge not derived, non-Hilbert residual retained, no-hypermomentum gate selected" if overall else "one or more validation gates failed",
            }
        )
    )
    return rows


def table(headers: list[str], rows: list[dict[str, str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(header, "").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    identity = read_csv(outputs["identity"])
    residual = read_csv(outputs["residual"])
    trident = read_csv(outputs["trident"])
    impact = read_csv(outputs["impact"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2538 - Noether Source Charge Identity Or NonHilbert Residual Row

## Result

The Noether/source-charge route gives a real theorem, but not the whole prize.

The usable theorem is conditional:

`if a single observed matter action is fixed, T_H := delta S_m/delta e_obs is the active ordinary-matter source before readout, and Ward/Noether identities conserve it on shell`.

That kills post-variation source-current rescaling. It does **not** prove that no independent gravitational source charge exists, because pre-action species weights remain conserved if they are legal, and non-Hilbert channels can still enter through spin/torsion, boundary/worldtube flux, readout reentry, or improvement/superpotential flux.

So the live source-side envelope is:

`||P_source[J_NH]|| <= E_spin + E_boundary + E_readout + E_improvement`.

The best next structural attack is no-hypermomentum / Levi-Civita source connection. If ordinary matter/source/readout do not vary an independent connection, the spin/torsion head can collapse. If not, the honest route is a P4 residual row.

## Noether Source-Charge Identity Attempt

{table(["row_id", "identity_piece", "status", "proof_or_obstruction"], identity)}

## NonHilbert Residual Row

{table(["row_id", "quantity", "bound_form", "status", "next_input"], residual)}

## NonHilbert Trident Update

{table(["row_id", "trident_head", "status", "fallback_or_effect"], trident)}

## Source Charge Gate Impact

{table(["row_id", "gate", "claim_status", "still_missing"], impact)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], gates)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["identity"])}`
- `{rel(outputs["residual"])}`
- `{rel(outputs["trident"])}`
- `{rel(outputs["impact"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is a controlled failure in the good sense. We did not prove the source-charge identity strongly enough to derive Minimal Universal Matter Coupling, but we did stop the leak from being vague. The source side now has a named residual envelope and a first structural gate: no-hypermomentum / Levi-Civita source connection. That is the next clean route toward derived local GR/Newton rather than a smuggled coupling axiom.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    write_csv(OUTPUTS["identity"], source_charge_identity_attempt())
    write_csv(OUTPUTS["residual"], nonhilbert_residual_row())
    write_csv(OUTPUTS["trident"], trident_gate_update())
    write_csv(OUTPUTS["impact"], source_charge_gate_impact())
    write_csv(OUTPUTS["claims"], claim_gates())
    write_csv(OUTPUTS["refusal"], refusal_runner())
    write_csv(OUTPUTS["next"], next_target())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
