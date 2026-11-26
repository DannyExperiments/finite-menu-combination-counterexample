# Reproduce the checks

From the repository root run the exact rational replay and archive verifier.

```sh
python3 -I verification/src/replay.py
python3 -I scripts/verify_repository.py
```

The replay checks 10,000 opposite-gamble certificates, 2,625 finite-menu exclusions, and the explorer's fixed menu. The manuscript proves the statements for all indices and all finite real-valued menus.

Using an existing Lean 4.30.0 installation, run the partial algebraic check.

```sh
lean -DwarningAsError=true formal/Q735Certificate.lean
```

[Replay output](verification/logs/replay.txt) · [Lean output](verification/logs/lean.txt) · [Manuscript build](paper/BUILD.md) · [Rendering guide](visualization/README.md)
