# ARM32-on-ARM64 runtime research for DLS 2017

## Best technical match found: ZettaBridge

Repository: https://github.com/ZailoxTT/ZettaBridge

ZettaBridge translates ARM32 A32/T32 native instructions to AArch64 with Dynarmic, runs an ARM32 Android/Bionic guest environment, bridges JNI, and provides EGL / OpenGL ES 2.0/3.0 passthrough. Its README reports selected older games running, but describes the project as early development and says it is not yet usable by end users. Unity 4.5 test games can start and render, but still have stability issues.

## Findings from the supplied DLS APK

The APK was inspected locally; it is not stored in this repository.

- Native ABIs present: `armeabi-v7a` and `x86`.
- No `arm64-v8a` native libraries are packaged.
- ARM `libDLS17.so` is ELF32 / ARM.
- `libDLS17.so` imports Android NDK APIs including `libandroid.so`, `liblog.so`, `libGLESv2.so`, `libEGL.so`, and `libOpenSLES.so`.
- Its imports include Android asset APIs, JNI-related calls and OpenGL ES entry points.

This makes ZettaBridge's general design relevant: it has corresponding ARM32 execution, JNI, EGL/GLES, and Android-native API bridging. It does **not** prove DLS will work: the exact DLS JNI lifecycle, imported symbols, asset access, audio path, threading, and rendering calls still need runtime testing.

## Critical license restriction

ZettaBridge's repository states that it is licensed cumulatively under PolyForm Noncommercial 1.0.0 and PolyForm Perimeter 1.0.1. The author says commercial use and providing a competing product (even free) require a separate written licence.

Therefore, do **not** copy, vendor, or merge ZettaBridge code into this repository as if it were permissively licensed. Before integrating it into a DLS compatibility product, request written permission from the author and confirm the intended use is covered. This note intentionally does not vendor third-party code.

## Recommended next steps

1. Ask the ZettaBridge author whether DLS 2017 can be tested with their runtime and whether a licence for this use is available.
2. Build and test their project only in a way permitted by its current licence; keep the game APK and proprietary libraries local.
3. Capture launch logs and identify missing syscalls, JNI methods, Android APIs, graphics calls, and audio behavior.
4. If permission or compatibility is unavailable, evaluate a separate implementation using components with licences compatible with this project's goals. A translator alone is insufficient; JNI, Bionic/system-library, EGL/GLES, asset, audio, input, and lifecycle bridges are also needed.

## Status

This is research, not an integrated runtime. No DLS compatibility claim or runnable APK is provided by this repository yet.
