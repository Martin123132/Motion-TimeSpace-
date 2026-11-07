from common import *
import numpy as np


def coefficients(model):
    report = read(ADJOINT / (model + "-build.json"))
    require(digest(report["packet"]) == report["sha256"], "retained coefficient packet")
    with np.load(report["packet"]) as archive:
        if "base_rows" in archive.files:
            return {name: archive[name].copy() for name in archive.files}
        packet = {name: archive[name].copy() for name in archive.files if name != "base"}
    size = int(packet["core_size"])
    structural = np.zeros((size, size), dtype=bool)
    for chunk in report["chunks"]:
        guard()
        require(digest(chunk["path"]) == chunk["sha256"], "retained dense chunk")
        with np.load(chunk["path"]) as archive:
            structural |= np.any(archive["base"] != 0., axis=0)
    rows, columns = np.nonzero(structural)
    base = np.empty((len(packet["efold"]), len(rows)))
    for chunk in report["chunks"]:
        guard()
        with np.load(chunk["path"]) as archive:
            dense = archive["base"]
            packed = dense[:, rows, columns]
            restored = np.zeros_like(dense)
            restored[:, rows, columns] = packed
            require(np.array_equal(dense, restored), "lossless central repack")
            base[chunk["start"]:chunk["stop"]] = packed
    packet.update(base=base, base_rows=rows, base_columns=columns)
    path = ROOT / (model + "-central-packed.npz")
    np.savez_compressed(path, **packet)
    write(ROOT / (model + "-central-packing.json"), dict(passed=True, packet=str(path), sha256=digest(path),
          input=report["packet"], input_sha256=report["sha256"], exact_zero_only=True, every_chunk_roundtrip=True))
    return packet

