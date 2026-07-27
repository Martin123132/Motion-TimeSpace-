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
DOC_PATH = ROOT / "4146-Y5-R2FR-finite-source-support-theorem-or-matter-routing-coupling-gate.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_FINITE_SOURCE_SUPPORT_OR_MATTER_ROUTING_4146"
CHECKPOINT_ID = "4146"
DECISION = "SUPPORT_ONLY_THEOREM_REJECTED_MATTER_ROUTING_CONSTRUCTED_NOT_LIVE_SIGNED_FINITE_SOURCE_BOUND_ROWS_EMITTED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4146_00_4145_doc": (
        ROOT / "4145-Y5-R2FR-tracefree-boundary-curvature-routing-or-live-adoption-gate.md",
        "finite-source support",
        "4145 selected finite-source support theorem or matter routing as next target.",
    ),
    "SRC4146_01_4145_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4145_NEXT_TARGET.csv",
        "support theorem removes matter overlap",
        "Machine-readable 4145 handoff.",
    ),
    "SRC4146_02_4145_curvature": (
        SOURCE_DIR / "P8_Y5_R2FR_4145_CURVATURE_ROUTING.csv",
        "MATTER_ROUTING_REQUIRED_NOT_OPTIONAL",
        "4145 curvature split exposing finite-source phi G_TF.",
    ),
    "SRC4146_03_4139_projector_doc": (
        ROOT / "4139-Y5-R2FR-Cbeta-qloc-projector-normalization-or-first-beta-bound.md",
        "C_beta_qloc[D]",
        "4139 same-normalized PPN beta projector.",
    ),
    "SRC4146_04_4140_divergence_doc": (
        ROOT / "4140-Y5-R2FR-q-loc-PPN-source-density-extraction-or-projector-zero-proof.md",
        "L_00^dagger chi_U=U^2",
        "4140 adjoint projector identity.",
    ),
    "SRC4146_05_source_norm_stack": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "G_EH = kappa c^4/(8 pi)",
        "Existing source-normalization theorem stack.",
    ),
    "SRC4146_06_newton_stack": (
        SOURCE_DIR / "P8_source_normalized_Newton_branch_STACK.csv",
        "SN11_second_order_PPN_source_stability",
        "Existing Newton/local-GR source stack with second-order PPN source closure.",
    ),
    "SRC4146_07_source_owner_contract": (
        SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv",
        "A10_second_order_source_closure",
        "Parent source-owner action terms for matter/source coupling.",
    ),
    "SRC4146_08_script": (
        SCRIPT_PATH,
        "SUPPORT_ONLY_THEOREM_REJECTED_MATTER_ROUTING_CONSTRUCTED",
        "This generator records the 4146 support theorem rejection and matter-routing construction.",
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
        "P8_Y5_R2FR_4146_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4146_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4146_SUPPORT_THEOREM_ATTEMPT": SOURCE_DIR / "P8_Y5_R2FR_4146_SUPPORT_THEOREM_ATTEMPT.csv",
        "P8_Y5_R2FR_4146_MATTER_ROUTING_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4146_MATTER_ROUTING_CONTRACT.csv",
        "P8_Y5_R2FR_4146_FINITE_SOURCE_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4146_FINITE_SOURCE_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4146_RESIDUAL_UPDATE": SOURCE_DIR / "P8_Y5_R2FR_4146_RESIDUAL_UPDATE.csv",
        "P8_Y5_R2FR_4146_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4146_DECISION_GATES.csv",
        "P8_Y5_R2FR_4146_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4146_STATUS.csv",
        "P8_Y5_R2FR_4146_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4146_NEXT_TARGET.csv",
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


def support_rows() -> List[dict]:
    return [
        {
            **common(),
            "attempt_id": "ST4146_0_projector_split",
            "claim_tested": "vacuum readout support kills finite-source phi G_TF",
            "identity": "delta_beta_phiG=-1/(2N_U2)<L_00^{-1}S_phiG,U^2 W_out>_Omega_out",
            "derivation": "Introduce the adjoint field L_00^dagger chi_out=U^2 W_out; then delta_beta_phiG=-1/(2N_U2)<S_phiG,chi_out>_B plus boundary terms.",
            "result": "SUPPORT_ONLY_NOT_ENOUGH",
            "reason": "S_phiG can be supported inside the body B while chi_out is nonzero there.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "attempt_id": "ST4146_1_green_memory",
            "claim_tested": "exterior annulus makes the Green response local",
            "identity": "chi_out(x')=int_Omega_out G_00(x,x') U(x)^2 W_out(x) d^3x",
            "derivation": "For the elliptic weak-field operator, an exterior window generates an adjoint kernel that reaches interior source points x' in B.",
            "result": "GENERIC_NONZERO_INTERIOR_ADJOINT_WEIGHT",
            "reason": "A positive Newtonian Green kernel does not vanish inside the body merely because the readout window is outside it.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "attempt_id": "ST4146_2_zero_conditions",
            "claim_tested": "support theorem can still pass under stronger clauses",
            "identity": "<S_phiG,chi_out>_B=0 if S_phiG=0 in B, chi_out|_B=0, or the weighted trace-free source moment vanishes",
            "derivation": "These are the actual zero conditions exposed by the adjoint projection.",
            "result": "STRONGER_ZERO_CONDITIONS_IDENTIFIED_NOT_SIGNED",
            "reason": "None follows from exterior support alone; each requires matter routing, projector design, or a source moment theorem.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "attempt_id": "ST4146_3_verdict",
            "claim_tested": "support-only route",
            "identity": "vacuum tensor zero on Omega_out does not imply <L_00^{-1}S_B,U^2>_Omega_out=0",
            "derivation": "Local vanishing of phi G_TF on the readout annulus is weaker than vanishing of the Green-solved metric sourced by the body interior.",
            "result": "SUPPORT_ONLY_THEOREM_REJECTED",
            "reason": "PPN beta is a sourced metric coefficient, not just pointwise tensor evaluation on the exterior annulus.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def matter_routing_rows() -> List[dict]:
    return [
        {
            **common(),
            "contract_id": "MR4146_0_jordan_frame_route",
            "route": "absorb phi R into the gravitational LHS",
            "formula": "S_grav=(1/2)int sqrt|g| M_eff(phi)^2 R with M_eff(phi)^2=M0^2+2 c_I phi",
            "derivation": "The phi G_mn term is then part of M_eff(phi)^2 G_mn, not an independent fifth-force source.",
            "required_signature": "same observed frame and one parent-selected M_eff/G_eff convention",
            "status": "CONSTRUCTED_ROUTE_NOT_LIVE_SIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "contract_id": "MR4146_1_source_normalization",
            "route": "measured Newton constant calibration",
            "formula": "G_ref=1/(8 pi M_eff(phi_*)^2) and partial_t,r,A,lambda G_ref=0 in the local branch",
            "derivation": "If the nonminimal coupling only renormalizes the local Planck mass, Newton's G is calibrated once rather than fitted per source.",
            "required_signature": "constant universal G_eff and no hidden source/range/species dependence",
            "status": "REQUIRES_SOURCE_NORMALIZATION_STACK",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "contract_id": "MR4146_2_tracefree_source_routing",
            "route": "route 16 pi G phi T_TF into EH/source ledger",
            "formula": "2 phi G_TF is absorbed by M_eff(phi)^2 G_TF before splitting field equations into source and residual parts",
            "derivation": "The finite-source term is not deleted; it is reclassified as the same gravitational coupling that defines the observed EH source.",
            "required_signature": "second-order PPN source closure and no-retuning guard",
            "status": "CONSTRUCTED_NOT_ADOPTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "contract_id": "MR4146_3_residual_after_routing",
            "route": "remaining residuals if Jordan routing is adopted",
            "formula": "D_TF -> D_owner + D_adoption + D_Geff_mismatch + D_deltaF_gradient + D_second_order_source",
            "derivation": "Routing moves the problem from a raw phi G_TF source to measurable coupling drift/source-normalization residuals.",
            "required_signature": "phi owner, live Khat adoption, constant G_eff, and second-order source closure",
            "status": "NEXT_GATE_DEFINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[dict]:
    return [
        {
            **common(),
            "bound_id": "FB4146_0_adjoint_support_weight",
            "symbol": "chi_out|_B",
            "formula": "chi_out(x')=int_Omega_out G_00(x,x') U^2(x) W_out(x)d^3x for x' in body B",
            "units": "adjoint projector weight",
            "required_inputs": "G_00 Green kernel, exterior window W_out, source-normalized U, body domain B",
            "status": "MISSING_ADJOINT_SUPPORT_PROFILE",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "FB4146_1_weighted_source_moment",
            "symbol": "M_phiG_TF",
            "formula": "M_phiG_TF=<Pi_00^PPN[16 pi G_ref phi T_TF],chi_out>_B",
            "units": "PPN source-projection numerator",
            "required_inputs": "phi profile, T_TF profile, PPN projection, chi_out, G_ref frame",
            "status": "MISSING_WEIGHTED_TRACEFREE_SOURCE_MOMENT",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "FB4146_2_beta_phiG_bound",
            "symbol": "delta_beta_phiG",
            "formula": "|delta_beta_phiG| <= |M_phiG_TF|/(2 N_U2) + |B_support|/(2 N_U2)",
            "units": "dimensionless beta",
            "required_inputs": "M_phiG_TF, boundary/support correction B_support, N_U2",
            "status": "NONCLAIM_BOUND_ROW",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "FB4146_3_jordan_mismatch",
            "symbol": "D_Geff_mismatch",
            "formula": "D_Geff_mismatch ~ delta(M_eff^-2)/M_eff^-2 plus source/range/species derivatives of G_eff",
            "units": "dimensionless coupling residual",
            "required_inputs": "M_eff(phi), local phi_*, dlnG_eff/dt, dlnG_eff/dr, dlnG_eff/dA, dlnG_eff/dlambda",
            "status": "MISSING_CONSTANT_UNIVERSAL_GEFF_CERTIFICATE",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> List[dict]:
    return [
        {
            **common(),
            "residual_id": "RU4146_0_after_4145",
            "formula": "D_TF=2 phi G_TF + D_owner + D_adoption",
            "meaning": "4145 boundary/coefficient closure leaves finite-source curvature, owner and adoption residuals.",
            "status": "INPUT_FROM_4145",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RU4146_1_support_rejection",
            "formula": "delta_beta_phiG=-1/(2N_U2)<Pi_00[16 pi G phi T_TF],chi_out>_B + boundary/support terms",
            "meaning": "Exterior readout does not generically erase interior finite-source curvature through the Green solve.",
            "status": "SUPPORT_ONLY_ROUTE_REJECTED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RU4146_2_jordan_route",
            "formula": "if M_eff(phi)^2 R is adopted live: D_TF=D_owner+D_adoption+D_Geff_mismatch+D_deltaF_gradient+D_second_order_source",
            "meaning": "Matter routing is possible as a parent-action route, but it shifts the proof to constant G_eff and second-order source closure.",
            "status": "CONSTRUCTED_ROUTE_NONCLAIM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DG4146_0_support",
            "decision": "SUPPORT_ONLY_THEOREM_REJECTED",
            "evidence": "adjoint Green projection gives interior source weight chi_out|_B even when the observation window is exterior",
            "claim_state": "no PPN/local-GR pass from vacuum readout support alone",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4146_1_matter_routing",
            "decision": "JORDAN_FRAME_MATTER_ROUTING_CONSTRUCTED",
            "evidence": "phi R can be interpreted as M_eff(phi)^2 R so phi G_TF is part of gravitational coupling rather than a separate force",
            "claim_state": "constructed route only; needs live source-normalization adoption",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4146_2_bounds",
            "decision": "FINITE_SOURCE_BOUND_ROWS_EMITTED",
            "evidence": "M_phiG_TF, chi_out|_B, delta_beta_phiG and D_Geff_mismatch rows define the remaining computation",
            "claim_state": "not score-ready",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4146_3_next",
            "decision": "NEXT_TARGET_GEFF_CALIBRATION_OR_SECOND_ORDER_SOURCE_CLOSURE",
            "evidence": "the nonclaim Jordan route needs one constant universal G_eff and beta-order source closure",
            "claim_state": "derive coupling calibration or bound it",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "status_id": "STATUS4146_0",
            "result": DECISION,
            "summary": "4146 rejects the tempting support-only theorem: an exterior/vacuum readout annulus does not generically kill finite-source phi G_TF because the weak-field Green/adjoint projector weights the body interior. The better route is constructed but not live-signed: absorb phi R into a Jordan-frame M_eff(phi)^2 R gravitational coupling, so phi G_TF is routed through the same EH/source-normalization ledger. This requires constant universal G_eff, live Khat adoption, phi owner stress accounting and second-order PPN source closure.",
            "support_only_theorem_passed": "False",
            "matter_routing_constructed": "True",
            "matter_routing_live_signed": "False",
            "finite_source_bound_rows_filled": "True",
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
            "next_id": "NEXT4146_0",
            "target_doc": "4147-Y5-R2FR-Jordan-frame-Geff-calibration-or-second-order-source-closure.md",
            "target_script": "scripts/Y5_R2FR_4147_Jordan_frame_Geff_calibration_or_second_order_source_closure.py",
            "objective": "try to derive the live constant-universal G_eff calibration for the M_eff(phi)^2 R route and show second-order PPN source stability; if not, emit D_Geff_mismatch and delta_beta_source bound rows",
            "success_gate": "one parent-owned M_eff/G_eff convention in the same observed frame, no source/range/species/time drift, live Khat adoption compatibility, and beta-order source closure or explicit bounds",
            "reason": "4146 rejects support-only zero and constructs the matter-routing route; now the theory must own the coupling calibration rather than hide it in measured G.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4146 - Finite-source support theorem or matter-routing coupling gate

## Decision
- Decision: `{DECISION}`.
- Support-only route: rejected.
- Matter-routing route: constructed, but not live-signed.
- Claim ceiling: no local-GR, Newton, PPN, R10, WEP, clock, orbital, or public evidence claim follows from 4146.

## Why exterior readout is not enough
4145 showed `phi G_TF=0` on a genuine vacuum annulus. That is useful, but PPN beta is not only a pointwise exterior tensor test; it is a Green-solved metric coefficient.

For the finite-source curvature channel,

`delta_beta_phiG=-1/(2N_U2)<L_00^-1 S_phiG,U^2 W_out>_Omega_out`.

Introduce the adjoint readout field:

`L_00^dagger chi_out=U^2 W_out`.

Then

`delta_beta_phiG=-1/(2N_U2)<S_phiG,chi_out>_B + boundary/support terms`.

So an exterior readout window still carries an interior body weight

`chi_out(x')=int_Omega_out G_00(x,x') U(x)^2 W_out(x)d^3x`.

That is generically nonzero for source points `x'` inside the body. Therefore vacuum support alone does not prove finite-source beta safety.

## Matter-routing route
The better route is not to delete `2 phi G_TF`. It is to stop treating it as a stray RHS force.

Adopt a Jordan-frame parent gravitational term:

`S_grav=(1/2)int sqrt|g| M_eff(phi)^2 R`, with `M_eff(phi)^2=M0^2+2 c_I phi`.

Then the `phi G_mn` term is part of `M_eff(phi)^2 G_mn`, i.e. part of the gravitational coupling/Planck-mass side. The finite-source term is routed into the same source-normalization ledger that defines measured `G_ref`, not hidden as a separate force.

This is only legal if the live theory supplies:
- one observed frame for matter, clocks, rods and EH/source variation;
- `G_ref=1/(8 pi M_eff(phi_*)^2)` with no time, range, species, frame, or source dependence;
- live `Khat_current^TF` adoption of the parent response;
- phi owner stress and zero-mode accounting;
- second-order PPN source closure so beta is not spoiled after Newtonian calibration.

## Updated residual
After 4145:

`D_TF=2 phi G_TF + D_owner + D_adoption`.

The support-only route gives:

`delta_beta_phiG=-1/(2N_U2)<Pi_00[16 pi G phi T_TF],chi_out>_B + boundary/support terms`.

The constructed Jordan route gives:

`D_TF -> D_owner + D_adoption + D_Geff_mismatch + D_deltaF_gradient + D_second_order_source`.

So the hard problem has moved from "why is finite-source `phi G_TF` zero?" to "can MTS derive one constant universal coupling and second-order source closure?"

## Outputs
- `{outputs["P8_Y5_R2FR_4146_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4146_SUPPORT_THEOREM_ATTEMPT"]}`
- `{outputs["P8_Y5_R2FR_4146_MATTER_ROUTING_CONTRACT"]}`
- `{outputs["P8_Y5_R2FR_4146_FINITE_SOURCE_BOUND_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4146_RESIDUAL_UPDATE"]}`
- `{outputs["P8_Y5_R2FR_4146_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4146_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4146_NEXT_TARGET"]}`

## Next Target
- `4147-Y5-R2FR-Jordan-frame-Geff-calibration-or-second-order-source-closure.md`
- Try to derive the live constant-universal `G_eff` calibration for the `M_eff(phi)^2 R` route and show beta-order source stability; otherwise emit `D_Geff_mismatch` and `delta_beta_source` bounds.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4146_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4146_SUPPORT_THEOREM_ATTEMPT"], support_rows())
    write_csv(outputs["P8_Y5_R2FR_4146_MATTER_ROUTING_CONTRACT"], matter_routing_rows())
    write_csv(outputs["P8_Y5_R2FR_4146_FINITE_SOURCE_BOUND_ROWS"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4146_RESIDUAL_UPDATE"], residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4146_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4146_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4146_NEXT_TARGET"], next_rows())
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
        "VAL4146_0_sources",
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
    add("VAL4146_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "delta_beta_phiG=-1/(2N_U2)<L_00^-1 S_phiG,U^2 W_out>_Omega_out",
        "chi_out(x')=int_Omega_out",
        "M_eff(phi)^2=M0^2+2 c_I phi",
        "D_Geff_mismatch",
        "4147-Y5-R2FR-Jordan-frame-Geff-calibration-or-second-order-source-closure.md",
    ]
    add("VAL4146_2_doc_tokens", "document records support rejection, Jordan route, residual update and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    support_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4146_SUPPORT_THEOREM_ATTEMPT"]))
    support_tokens = ["SUPPORT_ONLY_THEOREM_REJECTED", "chi_out|_B", "GENERIC_NONZERO_INTERIOR_ADJOINT_WEIGHT", "vacuum tensor zero"]
    add("VAL4146_3_support", "support-only theorem is rejected by adjoint Green support", all(token in support_text for token in support_tokens), "support tokens checked")

    matter_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4146_MATTER_ROUTING_CONTRACT"]))
    matter_tokens = ["M_eff(phi)^2=M0^2+2 c_I phi", "G_ref=1/(8 pi M_eff(phi_*)^2)", "second-order PPN source closure", "CONSTRUCTED_NOT_ADOPTED"]
    add("VAL4146_4_matter_route", "matter routing route is constructed as Jordan-frame coupling but not adopted", all(token in matter_text for token in matter_tokens), "matter tokens checked")

    bound_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4146_FINITE_SOURCE_BOUND_ROWS"]))
    bound_tokens = ["chi_out|_B", "M_phiG_TF", "delta_beta_phiG", "D_Geff_mismatch"]
    add("VAL4146_5_bounds", "finite-source bound rows cover support weight, source moment, beta and Geff mismatch", all(token in bound_text for token in bound_tokens), "bound tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4146_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("support_only_theorem_passed") == "False"
        and status[0].get("matter_routing_constructed") == "True"
        and status[0].get("matter_routing_live_signed") == "False"
        and status[0].get("finite_source_bound_rows_filled") == "True"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4146_6_status", "status records rejected support-only theorem, constructed route, no claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4146_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4147-Y5-R2FR-Jordan-frame-Geff-calibration-or-second-order-source-closure.md"
    add("VAL4146_7_next", "next target attacks Geff calibration and second-order source closure", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4146_8_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4146-Y5-R2FR" in item.name or "R2FR_4146" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4146_9_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4146_10_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4146_VALIDATION.csv"
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
