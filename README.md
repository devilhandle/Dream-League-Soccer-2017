# Dream League Soccer 2017 — ARM64 compatibility work

> Status: initial compatibility scaffold only. This repository does not currently contain the original game's APK/native libraries or a runnable port, so this commit does **not** claim that DLS 2017 runs on 64-bit-only Android devices.

## Goal

Investigate a Shadowgun-Bridge-style route for running the original 32-bit ARM game on ARM64-only Android devices without redistributing copyrighted game assets.

## Important distinction

Adding `arm64-v8a` to an APK's manifest or Gradle ABI filters does not translate 32-bit ARM machine code into AArch64. A real port requires either:

1. a compatible 64-bit native build from source (if the required source is available), or
2. a user-space ARM32 compatibility/emulation runtime, plus loader, JNI/Android API and graphics/audio/input integration appropriate to this specific game.

The second option is a substantial engineering project. The Shadowgun Bridge implementation cannot be copied blindly: DLS's engine version, native libraries, graphics calls and Android dependencies must first be identified.

## Current phase: inspect before implementing

1. Obtain an APK legally from a copy the user owns; do not commit the APK, game assets, proprietary `.so` files, or other copyrighted game data here.
2. Run `scripts/inspect-apk.sh /path/to/DLS2017.apk` to inventory native ABI directories and Android package metadata using locally installed Android tools.
3. Record Android version, device SoC/GPU, launch crash/logcat output, and whether the target device supports 32-bit apps.
4. Based on those facts, choose between a native ARM64 rebuild (if source exists) and a separately licensed ARM32 runtime/bridge.

## Repository status

- [x] Create an ARM64 porting plan
- [ ] Inspect a real APK and enumerate `lib/` contents
- [ ] Identify engine, JNI entry points, graphics API and required system libraries
- [ ] Select and integrate a suitable runtime/bridge
- [ ] Add Android build configuration and runtime tests
- [ ] Validate launch, gameplay, rendering, audio, touch controls and stability on target hardware

## Build status

There is no runnable APK or compatibility runtime in this scaffold yet. Do not treat this branch as a completed port.