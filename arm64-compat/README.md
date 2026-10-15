# Dream League Soccer 2017 — ARM64 compatibility investigation

This directory tracks the investigation for running the repository's APK on 64-bit-only Android devices using an approach inspired by [Shadowgun Bridge](https://github.com/JamesCrumble/shadowgun-bridge).

## Current status

- The repository contains the APK binary, not the game's source project.
- Renaming or copying `lib/armeabi-v7a` into `lib/arm64-v8a` does **not** convert ARM32 machine code to ARM64.
- A genuine native ARM64 port normally requires compatible ARM64 versions of every native dependency and, for game-engine code, the appropriate engine/build sources.
- A compatibility-layer approach is a different project: it must emulate/load the 32-bit code and bridge Android/JNI, graphics, audio, and input APIs. Success cannot be assumed from APK metadata alone.

## First milestone: inspect, don't patch blindly

Run the GitHub Actions workflow **Analyze APK native ABIs** from the Actions tab. It produces an artifact named `dls-apk-abi-report` listing native library paths and relevant Unity/IL2CPP filenames found in the APK.

Use that report to establish the actual ABI and native-library layout before deciding whether the Shadowgun Bridge architecture is reusable. The report is an inspection result only; it is not a converted APK.

## Acceptance criteria for a later compatibility build

1. Identify all native libraries, engine/runtime versions, and required packaged assets.
2. Map the target APK's dependencies against the bridge's implemented loader, JNI shims, graphics translation, audio, and input support.
3. Implement only evidence-backed compatibility changes; keep original APK assets intact.
4. Build a separately signed test APK and test launch, menus, rendering, audio, and gameplay on a 64-bit-only Android environment.
5. Publish an APK only after a reproducible build and runtime tests pass.

No converted APK is produced by the analysis workflow.
