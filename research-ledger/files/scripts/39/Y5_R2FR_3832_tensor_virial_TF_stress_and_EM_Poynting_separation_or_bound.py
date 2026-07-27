from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3832"
BRANCH = "MTS_R2FR_Y5_TENSOR_VIRIAL_TF_STRESS_AND_EM_POYNTING_SEPARATION_OR_BOUND_3832"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3832-Y5-R2FR-tensor-virial-TF-stress-and-EM-Poynting-separation-or-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3831 = PCW / "3831-Y5-R2FR-effective-anisotropic-stress-silence-or-SigmaTF-bound-fill.md"
CSV_3831_DECOMP = OUT / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv"
CSV_3831_TV = OUT / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv"
CSV_3831_BOUNDS = OUT / "P8_Y5_R2FR_3831_SIGMATF_BOUND_ROWS.csv"
CSV_3831_VALIDATION = OUT / "P8_Y5_BRR545_3831_VALIDATION.csv"
CSV_3830_GAMMA = OUT / "P8_Y5_R2FR_3830_GAMMA_BOUND_SOURCE_ROWS.csv"
CSV_3809_MAXWELL = OUT / "P8_Y5_R2FR_3809_MAXWELL_NORMALIZATION_THEOREM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3832_SOURCE_REGISTER.csv",
    "separation": OUT / "P8_Y5_R2FR_3832_TF_VIRIAL_EM_SEPARATION.csv",
    "em_poynting": OUT / "P8_Y5_R2FR_3832_EM_POYNTING_TF_STRESS_ROWS.csv",
    "tensor_virial": OUT / "P8_Y5_R2FR_3832_TENSOR_VIRIAL_TF_BOUND_ROWS.csv",
    "gamma_update": OUT / "P8_Y5_R2FR_3832_GAMMA_BOUND_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3832_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3832_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3832_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3832_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3832_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3832_0_3831_doc", P_3831, "Effective Anisotropic Stress Silence Or SigmaTF Bound Fill"),
    ("SRC3832_1_3831_decomp", CSV_3831_DECOMP, "SIGMATF3831_3_EM_Poynting"),
    ("SRC3832_2_3831_tensor_virial", CSV_3831_TV, "TV3831_3_EM_radiation_separation"),
    ("SRC3832_3_3831_bounds", CSV_3831_BOUNDS, "BTF3831_0_matter_total"),
    ("SRC3832_4_3831_validation", CSV_3831_VALIDATION, "VAL3831_2_components"),
    ("SRC3832_5_3830_gamma", CSV_3830_GAMMA, "GB3830_1_gamma_total"),
    ("SRC3832_6_3809_Maxwell", CSV_3809_MAXWELL, "MNT3809_0_parent_inner_product"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input_for_TF_virial_EM_Poynting_separation_or_bound",
                "claim_use": "source_separation_and_bound_contract_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def separation_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "separation_id": "SEP3832_0_total_TF_split",
            "statement": "Separate tensor-virial material TF stress from electromagnetic/radiative TF stress before using no-slip.",
            "formula": "Sigma_TF_matter = Sigma_TF_virial + Sigma_TF_EM_Poynting + Sigma_TF_apparatus + Sigma_TF_quad",
            "why": "otherwise Poynting/radiation stress can be hidden inside a vague anisotropic-stress residual",
            "status": "PASS_SEPARATION_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "separation_id": "SEP3832_1_tensor_virial_side",
            "statement": "Tensor virial controls closed stationary material/binding TF stress only after surface/exchange/radiation terms are included.",
            "formula": "epsilon_tensor_virial_TF <= ||d2I_TF/dt2 + surface_TF + exchange_TF + flux_TF||/(M c^2)",
            "why": "closed-source bookkeeping prevents partial-source stress cancellation from being faked",
            "status": "CONDITIONAL_BOUND_FORM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "separation_id": "SEP3832_2_EM_Poynting_side",
            "statement": "EM fields carry a genuine traceless stress tensor and Poynting momentum flux that must be absent, included, cancelled, or bounded.",
            "formula": "epsilon_EM_Poynting_TF <= ||P_TF T_EM||/(rho c^2) + ||P_TF(S_i S_j/c^2)||/(rho c^2)",
            "why": "this preserves the EM/Poynting intuition while stopping it from bypassing local-GR no-slip gates",
            "status": "CONDITIONAL_BOUND_FORM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def em_poynting_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "EMTF3832_0_field_stress",
            "term": "P_TF T_ij^EM",
            "formula": "P_TF[epsilon0 E_i E_j + mu0^-1 B_i B_j]",
            "zero_route": "E and B absent in exterior, isotropically averaged below order, or parent-sequestered from visible metric slip",
            "bound_needed": "sup ||P_TF T_ij^EM||/(rho_source c^2)",
            "status": "SOURCE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMTF3832_1_poynting_flux",
            "term": "Poynting momentum/radiation stress",
            "formula": "S = mu0^-1 E x B; radiation_TF ~ P_TF[S_i n_j/c]",
            "zero_route": "no net radiative flux crossing annulus or flux included in closed total tensor-virial source",
            "bound_needed": "sup ||P_TF radiation stress||/(rho_source c^2)",
            "status": "SOURCE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMTF3832_2_parent_cancellation",
            "term": "parent EM coupling/sequestration",
            "formula": "P_TF T_ij^EM + P_TF T_ij^parent_counter = 0",
            "zero_route": "parent action proves same-current EM stress is cancelled/sequestered in the no-slip scalar equation",
            "bound_needed": "residual parent EM TF mismatch row",
            "status": "MISSING_PARENT_CANCELLATION_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMTF3832_3_total",
            "term": "epsilon_EM_Poynting_TF",
            "formula": "epsilon_EM_Poynting_TF <= B_EM_field_TF + B_Poynting_flux_TF + B_parent_EM_mismatch_TF",
            "zero_route": "all three EM/Poynting rows vanish on the same compact exterior domain",
            "bound_needed": "numeric/source-backed EM field, flux, and parent mismatch bounds",
            "status": "FIRST_EM_POYNTING_TF_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def tensor_virial_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "TVTF3832_0_inertia",
            "term": "d2I_TF/dt2",
            "formula": "epsilon_inertia_TF = ||d2I_TF/dt2||/(M c^2)",
            "zero_route": "stationary/period-averaged source with declared averaging window",
            "status": "BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TVTF3832_1_surface_exchange",
            "term": "surface_TF + exchange_TF",
            "formula": "epsilon_surface_exchange_TF = ||surface_TF + exchange_TF||/(M c^2)",
            "zero_route": "fixed closed boundary and no parent/matter exchange across it",
            "status": "BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TVTF3832_2_flux_correction",
            "term": "flux_TF",
            "formula": "epsilon_flux_TF = ||radiative/Poynting/gravitational flux_TF||/(M c^2)",
            "zero_route": "no radiative flux or included in closed total source accounting",
            "status": "BOUND_REQUIRED_LINKED_TO_EM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TVTF3832_3_total",
            "term": "epsilon_tensor_virial_TF",
            "formula": "epsilon_tensor_virial_TF <= epsilon_inertia_TF + epsilon_surface_exchange_TF + epsilon_flux_TF",
            "zero_route": "all tensor-virial TF residuals vanish",
            "status": "FIRST_TENSOR_VIRIAL_TF_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gamma_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "GUP3832_0_matter_TF_update",
            "observable": "B_gamma_matter_TF",
            "formula": "B_gamma_matter_TF <= K_TF*(epsilon_ext_TF + epsilon_quad_TF + epsilon_apparatus_TF + epsilon_tensor_virial_TF + epsilon_EM_Poynting_TF)",
            "new_detail": "epsilon_tensor_virial_TF and epsilon_EM_Poynting_TF now have separate source-bound ledgers",
            "status": "UPDATED_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GUP3832_1_gamma_total",
            "observable": "gamma-1",
            "formula": "abs(gamma-1) <= B_gamma_matter_TF + B_gamma_parent_extra + B_gamma_boundary + B_gamma_readout + abs(eps_spatial/Phi)",
            "new_detail": "EM/Poynting appears only through B_gamma_matter_TF unless parent action proves sequestration",
            "status": "NONCLAIM_GAMMA_BOUND_REFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3832_0_separation",
            "gate": "tensor-virial and EM/Poynting TF stress separated",
            "status": "PASS_SEPARATION_NONCLAIM",
            "claim_allowed": False,
            "reason": "separate ledgers emitted for tensor-virial TF and EM/Poynting TF terms",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3832_1_EM_zero",
            "gate": "EM/Poynting TF zero claim",
            "status": "BLOCKED_PARENT_OR_SOURCE_BOUND_REQUIRED",
            "claim_allowed": False,
            "reason": "field stress, flux stress, and parent cancellation rows are not source-backed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3832_2_tensor_virial_zero",
            "gate": "tensor-virial TF zero claim",
            "status": "BLOCKED_SOURCE_BOUND_REQUIRED",
            "claim_allowed": False,
            "reason": "inertia, surface/exchange, and flux corrections are not signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3832_3_gamma",
            "gate": "gamma/no-slip claim",
            "status": "BLOCKED_REFINED_BOUND_ONLY",
            "claim_allowed": False,
            "reason": "gamma bound is refined but still lacks numeric/source-backed local rows",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3832_4_next_target",
            "gate": "next target moves to parent-extra/readout slip",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "matter/EM side is now decomposed; next no-slip term is parent extra scalar/readout mismatch",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3832_0_poynting_included_not_magic",
            "decision": "Poynting stress is now part of the formal no-slip source ledger",
            "basis": "EM field stress and radiative flux are explicitly traceless/anisotropic source terms",
            "consequence": "the intuition is preserved, but it must be bounded/cancelled rather than invoked freely",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3832_1_tensor_virial_not_EM",
            "decision": "tensor virial and EM/radiative flux are separate ledgers",
            "basis": "radiative flux can appear as a surface/flux term in tensor virial accounting",
            "consequence": "future tests can isolate whether a gamma residual comes from matter, EM, boundary, or parent readout",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3832_2_next_no_slip_source",
            "decision": "move next to parent-extra scalar/readout mismatch",
            "basis": "Sigma_TF_parent_extra remains the next major no-slip source after matter/EM decomposition",
            "consequence": "3833 should attack single-metric readout/naturality before returning to numeric local tests",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3832_0",
            "next_checkpoint": "3833-Y5-R2FR-parent-extra-scalar-slip-readout-naturality-or-bound.md",
            "script": "scripts/Y5_R2FR_3833_parent_extra_scalar_slip_readout_naturality_or_bound.py",
            "objective": "try to prove Sigma_TF_parent_extra=0 from single-metric readout/naturality and no representative scalar morphism, or emit a parent-extra gamma bound row",
            "reason": "3832 separates matter/EM/Poynting TF stress; the next no-slip source is parent/readout-generated scalar slip",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_TF_EM_POYNTING_SEPARATION",
            "claim": "no EM/gamma/no-slip/local-GR claim",
            "summary": "3832 separates tensor-virial TF stress from EM/Poynting TF stress and refines the nonclaim gamma bound ledger.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(sources, separation, em_poynting, tensor_virial, gamma_update, gates, decisions, timestamp: str) -> None:
    text = f"""# 3832 — Tensor-Virial TF Stress And EM/Poynting Separation Or Bound

Private checkpoint. This places EM/Poynting stress inside the no-slip source ledger. It does not claim no-slip, EM emergence, or local GR.

Generated: `{timestamp}`

## Result

3832 separates the traceless-stress ledger:

`Sigma_TF_matter = Sigma_TF_virial + Sigma_TF_EM_Poynting + Sigma_TF_apparatus + Sigma_TF_quad`.

The EM/Poynting piece is not motivational decoration; it is a possible source of slip:

`epsilon_EM_Poynting_TF <= B_EM_field_TF + B_Poynting_flux_TF + B_parent_EM_mismatch_TF`.

The updated matter contribution is:

`B_gamma_matter_TF <= K_TF*(epsilon_ext_TF + epsilon_quad_TF + epsilon_apparatus_TF + epsilon_tensor_virial_TF + epsilon_EM_Poynting_TF)`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## TF Virial/EM Separation

{markdown_table(separation, ["separation_id", "statement", "formula", "status"])}

## EM/Poynting TF Stress Rows

{markdown_table(em_poynting, ["row_id", "term", "formula", "zero_route", "status"])}

## Tensor-Virial TF Bound Rows

{markdown_table(tensor_virial, ["row_id", "term", "formula", "zero_route", "status"])}

## Gamma Bound Update

{markdown_table(gamma_update, ["row_id", "observable", "formula", "new_detail", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is the clean way to use the Poynting intuition: EM/radiative stress is now represented as a traceless source term that can be absent, included in a closed total source, parent-cancelled, or bounded. It is not allowed to sneak around the no-slip/gamma gate.

Next target: `3833-Y5-R2FR-parent-extra-scalar-slip-readout-naturality-or-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3831", "Current State After 3832", 1)
    paragraph = (
        "`3832` separates tensor-virial TF stress from EM/Poynting TF stress in the no-slip source ledger. "
        "`Sigma_TF_matter=Sigma_TF_virial+Sigma_TF_EM_Poynting+Sigma_TF_apparatus+Sigma_TF_quad`, with "
        "`epsilon_EM_Poynting_TF <= B_EM_field_TF+B_Poynting_flux_TF+B_parent_EM_mismatch_TF`. "
        "This keeps the Poynting/vector-wave intuition alive but makes it a bounded/cancelled source term rather than a shortcut around `gamma`.\n\n"
    )
    anchor = "`3831` separates"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3832-Y5-R2FR-tensor-virial-TF-stress-and-EM-Poynting-separation-or-bound.md`

Target: separate tensor-virial TF stress from EM/Poynting/radiative TF stress, then try to prove cancellation/sequestration or emit source-bound rows for `epsilon_EM_Poynting_TF` and `epsilon_tensor_virial_TF`.

This is the best next move because 3831 shows `Sigma_TF_matter` is the first no-slip blocker and that EM/Poynting stress is a real possible source term, not a shortcut."""
    new_gate = """`3833-Y5-R2FR-parent-extra-scalar-slip-readout-naturality-or-bound.md`

Target: try to prove `Sigma_TF_parent_extra=0` from single-metric readout/naturality and no representative scalar morphism, or emit a parent-extra gamma bound row.

This is the best next move because 3832 separates matter/EM/Poynting TF stress; the next no-slip source is parent/readout-generated scalar slip."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3832_TF_VIRIAL_EM_SEPARATION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3832_EM_POYNTING_TF_STRESS_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3832_TENSOR_VIRIAL_TF_BOUND_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3832_GAMMA_BOUND_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3832_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3832_TF_VIRIAL_EM_SEPARATION.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3832 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3832 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(sources, separation, em_poynting, tensor_virial, gamma_update, gates, timestamp: str):
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "timestamp_utc": timestamp})

    all_text = " ".join(str(row) for row in separation + em_poynting + tensor_virial + gamma_update + gates)
    add("VAL3832_0_sources", "all cited source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3832_1_separation", "tensor-virial and EM/Poynting ledgers are separated", all(token in all_text for token in ["Sigma_TF_virial", "Sigma_TF_EM_Poynting", "epsilon_tensor_virial_TF", "epsilon_EM_Poynting_TF"]), "separation tokens present")
    add("VAL3832_2_em_rows", "EM field, Poynting flux, parent mismatch, and total rows exist", len(em_poynting) == 4 and any(row["row_id"] == "EMTF3832_3_total" for row in em_poynting), f"{len(em_poynting)} EM rows")
    add("VAL3832_3_nonclaim", "all 3832 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in separation + em_poynting + tensor_virial + gamma_update + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3832_4_gamma_update", "gamma bound update includes EM/Poynting contribution", any("epsilon_EM_Poynting_TF" in row["formula"] for row in gamma_update), "gamma update includes epsilon_EM_Poynting_TF")
    add("VAL3832_5_claims_blocked", "EM/gamma claims remain blocked", any(row["gate_id"] == "GATE3832_1_EM_zero" and row["status"].startswith("BLOCKED") for row in gates), "EM zero gate blocked")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3832_6_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3832_7_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "Poynting" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3832*", "P8_Y5_BRR545_3832*", "*Y5_R2FR_3832*", "3832-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3832_8_formalization_clean", "formalization-workbench has no 3832 files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3832 file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3832_9_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    separation = separation_rows(timestamp)
    em_poynting = em_poynting_rows(timestamp)
    tensor_virial = tensor_virial_rows(timestamp)
    gamma_update = gamma_update_rows(timestamp)
    gates = claim_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["separation"], separation)
    write_csv(OUTPUTS["em_poynting"], em_poynting)
    write_csv(OUTPUTS["tensor_virial"], tensor_virial)
    write_csv(OUTPUTS["gamma_update"], gamma_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, separation, em_poynting, tensor_virial, gamma_update, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, separation, em_poynting, tensor_virial, gamma_update, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_TF_EM_POYNTING_SEPARATION")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
