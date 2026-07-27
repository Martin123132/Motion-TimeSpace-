from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4148-Y5-R2FR-local-phi-freeze-no-scalar-charge-or-coupling-drift-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_PHI_FREEZE_OR_COUPLING_DRIFT_4148"
CHECKPOINT_ID = "4148"
DECISION = "PHI_FREEZE_THEOREM_CONDITIONS_DERIVED_CURRENT_SOURCE_ZERO_UNSIGNED_COUPLING_DRIFT_BOUNDS_EMITTED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4148_00_4147_doc": (
        ROOT / "4147-Y5-R2FR-Jordan-frame-Geff-calibration-or-second-order-source-closure.md",
        "local phi freeze/no scalar charge",
        "4147 selected local phi freeze as the next root problem.",
    ),
    "SRC4148_01_4147_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4147_NEXT_TARGET.csv",
        "delta_phi=0",
        "Machine-readable 4147 handoff.",
    ),
    "SRC4148_02_4147_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4147_COUPLING_BOUND_ROWS.csv",
        "Q_phi",
        "4147 coupling drift and scalar charge bound rows.",
    ),
    "SRC4148_03_4028_phi_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4028_TRACEFREE_IMPROVEMENT_DERIVATION.csv",
        "OWNER_TEMPLATE_CONSTRUCTED_NOT_ADOPTED",
        "4028 staged phi owner template.",
    ),
    "SRC4148_04_4142_scalar_hair": (
        ROOT / "4142-Y5-R2FR-scalar-hair-U2-orthogonality-or-beta-overlap-bound.md",
        "Generic scalar-hair orthogonality is rejected",
        "4142 rejected generic scalar-hair safety.",
    ),
    "SRC4148_05_1024_nohair_inputs": (
        ROOT / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
        "MISSING_SOURCE_ZERO_PROOF",
        "Prior scalar no-hair input pack with source-zero blocker.",
    ),
    "SRC4148_06_1025_hessian": (
        ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "Z_X>0 and M_X^2>0",
        "Prior Hessian/range contract.",
    ),
    "SRC4148_07_source_owner_contract": (
        SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv",
        "A7_bulk_X_nohair_or_curve",
        "Parent action term for no-hair or executable curve.",
    ),
    "SRC4148_08_script": (
        SCRIPT_PATH,
        "PHI_FREEZE_THEOREM_CONDITIONS_DERIVED_CURRENT_SOURCE_ZERO_UNSIGNED",
        "This generator records the 4148 phi-freeze theorem attempt.",
    ),
}


def common() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def write_csv(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4148_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4148_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4148_PHI_FREEZE_THEOREM_ATTEMPT": SOURCE_DIR / "P8_Y5_R2FR_4148_PHI_FREEZE_THEOREM_ATTEMPT.csv",
        "P8_Y5_R2FR_4148_PHI_SOURCE_LEDGER": SOURCE_DIR / "P8_Y5_R2FR_4148_PHI_SOURCE_LEDGER.csv",
        "P8_Y5_R2FR_4148_COUPLING_DRIFT_BOUND": SOURCE_DIR / "P8_Y5_R2FR_4148_COUPLING_DRIFT_BOUND.csv",
        "P8_Y5_R2FR_4148_LOCAL_GR_IMPACT": SOURCE_DIR / "P8_Y5_R2FR_4148_LOCAL_GR_IMPACT.csv",
        "P8_Y5_R2FR_4148_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4148_DECISION_GATES.csv",
        "P8_Y5_R2FR_4148_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4148_STATUS.csv",
        "P8_Y5_R2FR_4148_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4148_NEXT_TARGET.csv",
    }


def source_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        text = read_text(path) if exists and path.is_file() else ""
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "role": role,
                "exists": str(exists),
                "needle_found": str(bool(exists and needle in text)),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def freeze_rows() -> List[dict]:
    return [
        {
            **common(),
            "theorem_id": "PF4148_0_local_operator",
            "statement": "local phi perturbation operator",
            "formula": "delta_phi:=phi-phi_*; O_phi delta_phi=J_phi; O_phi=-nabla_i(Z_phi nabla^i)+M_phi^2",
            "derivation": "Linearize the local phi owner around the candidate branch phi_*.",
            "result": "OPERATOR_FORM_DERIVED_CONDITIONAL",
            "current_corpus_status": "Z_phi/M_phi^2/J_phi not parent-signed for this branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "PF4148_1_energy_identity",
            "statement": "positive no-hair identity",
            "formula": "int_A[Z_phi|grad delta_phi|^2+M_phi^2 delta_phi^2]=int_A delta_phi J_phi + B_phi",
            "derivation": "Multiply the Euler equation by delta_phi and integrate over the local annulus/worldtube domain.",
            "result": "ENERGY_IDENTITY_DERIVED",
            "current_corpus_status": "conditional until signs, source and boundary are owned",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "PF4148_2_freeze_theorem",
            "statement": "exact local freeze/no scalar charge",
            "formula": "if Z_phi>0, M_phi^2>0, J_phi=0, B_phi=0, then delta_phi=0 and Q_phi=0",
            "derivation": "The LHS is positive definite and equals zero, so both grad delta_phi and delta_phi vanish.",
            "result": "CONDITIONAL_THEOREM",
            "current_corpus_status": "J_phi=0 and boundary flux zero are unsigned; no live freeze claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "PF4148_3_failure_mode",
            "statement": "source term blocks exact freeze",
            "formula": "J_phi=(2 zeta_phi/3)delta(Gamma_eff+C)+J_matter+J_domain+J_boundary+J_memory+J_mixed",
            "derivation": "The 4028 owner template sources phi through Gamma_eff+C unless that source is locked to zero.",
            "result": "SOURCE_ZERO_REQUIRED",
            "current_corpus_status": "current branch has source template, not source-zero theorem",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def source_ledger_rows() -> List[dict]:
    return [
        {
            **common(),
            "source_id": "PS4148_0_gamma_eff",
            "symbol": "J_Gamma",
            "formula": "(2 zeta_phi/3)delta(Gamma_eff+C)",
            "zero_route": "Gamma_eff+C is at a parent extremum and source-blind in the local branch",
            "current_status": "MISSING_GAMMA_EXTREMUM_LOCK",
            "residual_if_nonzero": "Q_phi; D_Geff_mismatch; D_deltaF_gradient",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "source_id": "PS4148_1_matter",
            "symbol": "J_matter",
            "formula": "delta_phi S_matter or induced trace/source coupling in the observed frame",
            "zero_route": "matter quotient/no-marker theorem or minimal matter action independent of phi at fixed g_obs",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "residual_if_nonzero": "scalar_charge; WEP/source dependence; beta source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "source_id": "PS4148_2_domain_memory",
            "symbol": "J_domain+J_memory",
            "formula": "domain/projector/memory variation of the phi owner or Gamma_eff branch",
            "zero_route": "quotient/superselection map makes these vertical or topological",
            "current_status": "UNSIGNED",
            "residual_if_nonzero": "range/radial/source hair and R10/R11 rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "source_id": "PS4148_3_boundary",
            "symbol": "B_phi",
            "formula": "int_partialA delta_phi Z_phi n.grad(delta_phi) + owner/corner/projector boundary terms",
            "zero_route": "self-adjoint no-flux boundary class with same readout collar",
            "current_status": "MISSING_BOUNDARY_FLUX_ZERO",
            "residual_if_nonzero": "boundary scalar charge and coupling drift",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "source_id": "PS4148_4_mixed_hessian",
            "symbol": "J_mixed",
            "formula": "metric/phi/projector cross-Hessian terms evaluated on the local branch",
            "zero_route": "block-diagonal or positive coupled Hessian theorem",
            "current_status": "MISSING_CROSS_HESSIAN_CONTROL",
            "residual_if_nonzero": "D_deltaF_gradient; D_adoption; beta source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[dict]:
    return [
        {
            **common(),
            "bound_id": "PB4148_0_L2_phi",
            "symbol": "||delta_phi||_2",
            "formula": "||delta_phi||_2 <= (||J_phi||_2 + sqrt(||J_phi||_2^2 + 4 M_phi^2 |B_phi|))/(2 M_phi^2)",
            "units": "phi field units times volume^1/2",
            "required_inputs": "positive M_phi^2, J_phi norm, boundary flux magnitude, domain measure",
            "status": "NONCLAIM_ENERGY_BOUND",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "PB4148_1_gradient",
            "symbol": "||grad delta_phi||_2",
            "formula": "Z_phi ||grad delta_phi||_2^2 <= ||delta_phi||_2 ||J_phi||_2 + |B_phi|",
            "units": "phi field units per length times volume^1/2",
            "required_inputs": "Z_phi, J_phi, B_phi and delta_phi bound",
            "status": "NONCLAIM_GRADIENT_BOUND",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "PB4148_2_Geff",
            "symbol": "D_Geff_mismatch",
            "formula": "|deltaG/G| <= (2|c_I|/F_*) ||delta_phi||_infty + O(delta_phi^2)",
            "units": "dimensionless",
            "required_inputs": "c_I, F_*, Linf phi bound or Sobolev constant from the local domain",
            "status": "COUPLING_DRIFT_BOUND_FORM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "PB4148_3_scalar_charge",
            "symbol": "Q_phi",
            "formula": "|Q_phi| <= ||J_phi||_1 + |B_phi_flux|, with Yukawa exterior delta_phi~Q_phi exp(-r/lambda_phi)/r",
            "units": "phi charge in declared units",
            "required_inputs": "source current integral, boundary flux, lambda_phi=sqrt(Z_phi/M_phi^2)",
            "status": "SCALAR_CHARGE_BOUND_FORM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "PB4148_4_beta",
            "symbol": "delta_beta_source",
            "formula": "|delta_beta_source| <= |C_Geff|D_Geff_mismatch + |C_Fgrad|D_deltaF_gradient + |C_Q| |Q_phi| + |C_boundary||B_phi|",
            "units": "dimensionless beta",
            "required_inputs": "projector constants, Geff mismatch, F-gradient, scalar charge, boundary flux",
            "status": "SECOND_ORDER_SOURCE_BOUND_FORM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def impact_rows() -> List[dict]:
    return [
        {
            **common(),
            "impact_id": "LI4148_0_if_freeze_passes",
            "condition": "Z_phi>0, M_phi^2>0, J_phi=0, B_phi=0 and live Khat/Jordan adoption",
            "consequence": "delta_phi=0, Q_phi=0, D_Geff_mismatch=0, D_deltaF_gradient=0 and the 4147 constant-G theorem can be promoted",
            "claim_state": "conditional route only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "LI4148_1_current_branch",
            "condition": "current files have phi owner template but source-zero/boundary/Hessian ownership unsigned",
            "consequence": "local GR/Newton/PPN remain blocked by scalar charge and coupling drift rows",
            "claim_state": "no local claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "LI4148_2_best_next_attack",
            "condition": "source term is the first live obstruction after the theorem identity",
            "consequence": "attack Gamma_eff+C extremum/source-zero before numeric residual scoring",
            "claim_state": "derivation-first route selected",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DG4148_0_theorem",
            "decision": "PHI_FREEZE_THEOREM_CONDITIONS_DERIVED",
            "evidence": "positive energy identity proves delta_phi=0 if Z_phi>0, M_phi^2>0, J_phi=0 and B_phi=0",
            "claim_state": "conditional theorem only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4148_1_current_corpus",
            "decision": "CURRENT_SOURCE_ZERO_UNSIGNED",
            "evidence": "4028 phi owner sources phi through Gamma_eff+C and prior scalar packs keep J_X/source-zero missing",
            "claim_state": "no phi freeze/no scalar charge claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4148_2_bounds",
            "decision": "COUPLING_DRIFT_BOUNDS_EMITTED",
            "evidence": "energy inequality gives nonclaim bounds for delta_phi, Q_phi, D_Geff_mismatch and delta_beta_source",
            "claim_state": "not score-ready",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4148_3_next",
            "decision": "NEXT_TARGET_GAMMA_EXTREMUM_OR_SOURCE_ZERO_LOCK",
            "evidence": "J_phi is the first obstruction after the positive identity",
            "claim_state": "derive source-zero/extremum lock or keep scalar charge bounds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "status_id": "STATUS4148_0",
            "result": DECISION,
            "summary": "4148 derives the exact local phi-freeze theorem: for O_phi=-nabla_i(Z_phi nabla^i)+M_phi^2, positive Z_phi and M_phi^2 plus J_phi=0 and B_phi=0 force delta_phi=0 and Q_phi=0. Current MTS does not yet sign J_phi=0 or boundary flux zero; the 4028 owner template explicitly sources phi through Gamma_eff+C unless an extremum/source-zero lock is proved. Coupling-drift and beta-source bounds are emitted instead of a local-GR claim.",
            "phi_freeze_conditions_derived": "True",
            "source_zero_live_signed": "False",
            "boundary_flux_zero_live_signed": "False",
            "no_scalar_charge_claimed": "False",
            "coupling_drift_bounds_filled": "True",
            "local_gr_claimed": "False",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4148_0",
            "target_doc": "4149-Y5-R2FR-Gamma-eff-extremum-source-zero-lock-or-phi-charge-bound.md",
            "target_script": "scripts/Y5_R2FR_4149_Gamma_eff_extremum_source_zero_lock_or_phi_charge_bound.py",
            "objective": "try to prove J_phi=0 by showing Gamma_eff+C is at a parent-owned local extremum/source-blind quotient in the local branch; if not, fill source-channel bounds for J_Gamma, J_matter, J_domain and J_boundary",
            "success_gate": "source-zero/extremum lock is parent-signed and not fitted per source, or phi charge/coupling-drift source bounds remain explicit and nonclaim",
            "reason": "4148 shows phi freeze is exactly equivalent to positive operator plus source-zero and boundary-zero; source-zero is the first unsolved obstruction.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4148 - Local phi freeze, no scalar charge, or coupling drift bound

## Decision
- Decision: `{DECISION}`.
- Real movement: the local `phi` freeze condition is now an exact positive-operator theorem, not a vibe.
- Current corpus status: theorem conditions are not live-signed, so no local-GR/Newton/PPN claim follows.

## Phi-freeze theorem
Let

`delta_phi:=phi-phi_*`

and write the local linearized owner equation as

`O_phi delta_phi=J_phi`, with `O_phi=-nabla_i(Z_phi nabla^i)+M_phi^2`.

Multiplying by `delta_phi` and integrating gives

`int_A[Z_phi|grad delta_phi|^2+M_phi^2 delta_phi^2]=int_A delta_phi J_phi + B_phi`.

Therefore, if

`Z_phi>0`, `M_phi^2>0`, `J_phi=0`, and `B_phi=0`,

then

`delta_phi=0` and `Q_phi=0`.

That is the exact condition required by 4147 for `F(phi)=M_eff(phi)^2` to be locally constant and for `G_ref=1/(8 pi F_*)` to be a one-time coupling rather than a hidden fit.

## Why the current corpus does not close it yet
The 4028 owner template sources the scalar:

`J_phi=(2 zeta_phi/3)delta(Gamma_eff+C)+J_matter+J_domain+J_boundary+J_memory+J_mixed`.

So freeze does not follow from positivity alone. It also needs a source-zero/extremum lock:

- `Gamma_eff+C` must be at a parent-owned local extremum or source-blind quotient;
- matter must not source `phi` in the observed frame;
- domain/projector/memory terms must be vertical/topological/silent;
- boundary flux must vanish under the same local collar;
- mixed Hessian terms must be block-positive or zero.

## Nonclaim bounds if source-zero fails
The energy identity gives

`||delta_phi||_2 <= (||J_phi||_2 + sqrt(||J_phi||_2^2 + 4 M_phi^2 |B_phi|))/(2 M_phi^2)`.

Then

`|deltaG/G| <= (2|c_I|/F_*) ||delta_phi||_infty + O(delta_phi^2)`,

and

`|delta_beta_source| <= |C_Geff|D_Geff_mismatch + |C_Fgrad|D_deltaF_gradient + |C_Q||Q_phi| + |C_boundary||B_phi|`.

## Current verdict
| Gate | Result | Meaning |
|---|---|---|
| positive operator theorem | CONDITIONAL_DERIVED | exact no-hair logic exists |
| `J_phi=0` | UNSIGNED | first live obstruction |
| boundary flux zero | UNSIGNED | collar/no-flux not signed for phi owner |
| no scalar charge | NOT_CLAIMED | `Q_phi` bound retained |
| local GR/Newton | NOT_CLAIMED | coupling drift rows remain active |

## Outputs
- `{outputs["P8_Y5_R2FR_4148_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4148_PHI_FREEZE_THEOREM_ATTEMPT"]}`
- `{outputs["P8_Y5_R2FR_4148_PHI_SOURCE_LEDGER"]}`
- `{outputs["P8_Y5_R2FR_4148_COUPLING_DRIFT_BOUND"]}`
- `{outputs["P8_Y5_R2FR_4148_LOCAL_GR_IMPACT"]}`
- `{outputs["P8_Y5_R2FR_4148_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4148_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4148_NEXT_TARGET"]}`

## Next Target
- `4149-Y5-R2FR-Gamma-eff-extremum-source-zero-lock-or-phi-charge-bound.md`
- Try to prove `J_phi=0` by showing `Gamma_eff+C` is at a parent-owned local extremum/source-blind quotient in the local branch; if not, fill source-channel bounds for `J_Gamma`, `J_matter`, `J_domain`, and `J_boundary`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4148_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4148_PHI_FREEZE_THEOREM_ATTEMPT"], freeze_rows())
    write_csv(outputs["P8_Y5_R2FR_4148_PHI_SOURCE_LEDGER"], source_ledger_rows())
    write_csv(outputs["P8_Y5_R2FR_4148_COUPLING_DRIFT_BOUND"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4148_LOCAL_GR_IMPACT"], impact_rows())
    write_csv(outputs["P8_Y5_R2FR_4148_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4148_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4148_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, requirement: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "requirement": requirement,
                "passed": str(bool(passed)),
                "detail": detail,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    add(
        "VAL4148_0_sources",
        "all cited source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']} exists={row['exists']} needle={row['needle_found']}" for row in sources),
    )

    csv_ok = True
    csv_detail: List[str] = []
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            csv_detail.append(f"{name}:{len(rows)}")
            csv_ok = csv_ok and bool(rows)
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{name}:ERR {exc!r}")
    add("VAL4148_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "O_phi=-nabla_i(Z_phi nabla^i)+M_phi^2",
        "J_phi=(2 zeta_phi/3)delta(Gamma_eff+C)",
        "||delta_phi||_2 <=",
        "Q_phi",
        "4149-Y5-R2FR-Gamma-eff-extremum-source-zero-lock-or-phi-charge-bound.md",
    ]
    add("VAL4148_2_doc_tokens", "document records freeze theorem, source obstruction, bounds and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    freeze_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4148_PHI_FREEZE_THEOREM_ATTEMPT"]))
    freeze_tokens = ["O_phi=-nabla_i", "ENERGY_IDENTITY_DERIVED", "J_phi=0", "SOURCE_ZERO_REQUIRED"]
    add("VAL4148_3_freeze", "freeze theorem attempt derives operator, energy identity and source-zero requirement", all(token in freeze_text for token in freeze_tokens), "freeze tokens checked")

    source_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4148_PHI_SOURCE_LEDGER"]))
    source_tokens = ["J_Gamma", "J_matter", "J_domain+J_memory", "B_phi", "J_mixed"]
    add("VAL4148_4_source_ledger", "source ledger covers gamma, matter, domain/memory, boundary and mixed Hessian channels", all(token in source_text for token in source_tokens), "source ledger tokens checked")

    bound_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4148_COUPLING_DRIFT_BOUND"]))
    bound_tokens = ["||delta_phi||_2", "||grad delta_phi||_2", "D_Geff_mismatch", "Q_phi", "delta_beta_source"]
    add("VAL4148_5_bounds", "coupling drift bounds cover phi norm, gradient, Geff, scalar charge and beta", all(token in bound_text for token in bound_tokens), "bound tokens checked")

    impact_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4148_LOCAL_GR_IMPACT"]))
    impact_tokens = ["D_Geff_mismatch=0", "local GR/Newton/PPN remain blocked", "attack Gamma_eff+C"]
    add("VAL4148_6_impact", "impact rows distinguish conditional pass from current blocked branch", all(token in impact_text for token in impact_tokens), "impact tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4148_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("phi_freeze_conditions_derived") == "True"
        and status[0].get("source_zero_live_signed") == "False"
        and status[0].get("boundary_flux_zero_live_signed") == "False"
        and status[0].get("no_scalar_charge_claimed") == "False"
        and status[0].get("coupling_drift_bounds_filled") == "True"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4148_7_status", "status records theorem conditions, unsigned source zero and no local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4148_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4149-Y5-R2FR-Gamma-eff-extremum-source-zero-lock-or-phi-charge-bound.md"
    add("VAL4148_8_next", "next target attacks Gamma_eff extremum/source-zero lock", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4148_9_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4148-Y5-R2FR" in item.name or "R2FR_4148" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4148_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4148_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4148_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
