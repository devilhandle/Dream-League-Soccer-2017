# Dream League Soccer 2017 — ARM64 compatibility investigation

## Finding

The checked-in file is an APK binary, not the original game/engine source project. Its native libraries are **32-bit only**:

| APK path | ELF architecture |
| --- | --- |
| `lib/armeabi-v7a/libDLS17.so` | ELF32 / ARM |
| `lib/armeabi-v7a/libadcolony.so` | ELF32 / ARM |
| `lib/armeabi-v7a/libjs.so` | ELF32 / ARM |
| `lib/x86/libDLS17.so` | ELF32 / Intel 80386 |
| `lib/x86/libadcolony.so` | ELF32 / Intel 80386 |
| `lib/x86/libjs.so` | ELF32 / Intel 80386 |

There is no `arm64-v8a` native-library directory in this APK. The game library exports JNI entry points under `com.firsttouchgames.ftt.FTTJNI`. The x86 inspection report lists dependencies on Android system libraries including `libandroid.so`, `liblog.so`, `libGLESv2.so`, `libEGL.so`, `libOpenSLES.so`, `libdl.so`, `libm.so`, `libc.so` and `libstdc++.so`. A corrected workflow now preserves each ABI directory while collecting both ARM and x86 details.

## Decision

A **native ARM64 conversion cannot be responsibly produced from this repository alone**: it contains the APK, not the C/C++ source or an AArch64 build of the proprietary game libraries. Changing the folder name, ELF header, or APK ABI metadata would not convert ARM32 machine instructions into AArch64 and would produce a broken package.

The closest route to the requested Shadowgun-Bridge approach is a **separate 32-bit ARM compatibility runtime**, not an ABI conversion. The reference bridge is a substantial game-specific system (ARM user-mode emulation, Android/JNI shims, graphics forwarding, audio/input integration and APK wrapper). DLS has its own JNI entry points and dependencies, so copying or renaming its libraries into that bridge is not enough. It needs compatibility work and on-device validation; the available evidence does not yet establish that the bridge's graphics/audio/JNI behavior matches DLS.

## Changes made on branch `arm64-compat-analysis`

- Added `.github/workflows/analyze-apk.yml` to inventory APK ABIs.
- Added `arm64-compat/inspect_apk.py` to read ELF class and machine fields without modifying the APK.
- Added `.github/workflows/deep-apk-inspection.yml` to report ELF headers, dynamic dependencies, JNI exports and undefined imports for each ABI. It uploads the report as the `dls-elf-inspection` Actions artifact.
- No game binary was altered, no fake `arm64-v8a` library was created, and no converted APK is claimed.

## Next engineering gate

Use the full per-ABI report to compare ARM and x86 imports and identify which bridge interfaces DLS actually calls. Then prototype the smallest compatibility test in a separate wrapper and validate it on a 64-bit-only Android device. A usable release requires that runtime work plus packaging, signing, and real device testing; CI static inspection alone cannot certify that the game launches.
