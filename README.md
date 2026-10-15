# Dream League Soccer 2017 — ARM64 compatibility work

> **Status: ARM64 diagnostic scaffold only, not a working game port.** The APK inspection and native source scaffold are committed on this branch; ARM32 instruction emulation and Android API/graphics/audio integration are not implemented.

## APK inspection results

The user-provided APK `Dream-League-v4-162.1.apk` was inspected locally and is not included in this repository.

| ABI directory | Libraries found |
| --- | --- |
| `armeabi-v7a` | `libDLS17.so`, `libjs.so`, `libadcolony.so` |
| `x86` | `libDLS17.so`, `libjs.so`, `libadcolony.so` |
| `arm64-v8a` | None |

The ARM build of `libDLS17.so` was confirmed as ELF32 / ARM. The APK therefore does not include a 64-bit ARM native game build.

## What this branch adds

- `scripts/inspect-apk.sh`: repeatable ABI/package inventory for a locally owned APK.
- `android/compat/src/main/cpp/CMakeLists.txt` and `compat_probe.cpp`: an Android NDK JNI library intended to compile for `arm64-v8a`. It reports the compatibility state; it does **not** execute the ARM32 game.
- `android/compat/src/main/java/org/dls17/compat/CompatProbe.java`: Java declaration for the diagnostic JNI method.
- `android/compat/README.md`: integration notes and remaining engineering requirements.

## Important distinction

Adding `arm64-v8a` to an APK or Gradle ABI filters does not translate 32-bit ARM machine code into AArch64. A real port requires either:

1. a compatible 64-bit native build from source, or
2. a user-space ARM32 compatibility/emulation runtime plus loader, Android/Bionic and JNI bridging, and graphics/audio/input integration for this specific game.

This is substantial work. The Shadowgun Bridge approach cannot be copied blindly: DLS's engine, JNI entry points, graphics API and Android dependencies need further investigation and testing.

## Next steps

1. Build and integrate the diagnostic module in an Android host project with NDK/CMake and `arm64-v8a` selected.
2. Collect Android version, device SoC/GPU and launch logs from the target device.
3. Identify the native engine/dependencies and decide whether a genuine 64-bit rebuild is possible or an ARM32 runtime must be integrated.
4. Implement and test the runtime/bridge, including rendering, audio, touch input, lifecycle and stability.

Do not commit or redistribute the APK, game assets or proprietary native libraries. This branch does not yet provide a runnable APK or claim that the game works on 64-bit-only Android devices.
