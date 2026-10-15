# DLS 2015 ARM64 APK: compatibility-layer forensic notes

## File examined

The APK supplied for analysis was inspected locally. It is not copied into this repository.

## Confirmed ABI layout

The APK contains exactly these packaged native libraries under `lib/`:

- `lib/arm64-v8a/libDLS2.so` — ELF64, AArch64, approximately 3.38 MB.
- `lib/arm64-v8a/libandroidoyunclub.so` — ELF64, AArch64.
- `lib/arm64-v8a/libandroidoyunclub1.so` — ELF64, AArch64.

A second copy at `assets/androidoyunclub/libDLS2.so` is ELF32 / ARM (approximately 5.64 MB). This is the strongest evidence that the app bundles a guest ARM32 game library alongside a separate ARM64 host implementation.

## Compatibility layer identification

The ARM64 `lib/arm64-v8a/libDLS2.so` is not simply a recompiled game library. Its exported/dynamic symbols and strings include:

- Dynarmic A32 CPU translation symbols (`Dynarmic::A32`), consistent with ARM32 instruction translation/JIT.
- A custom namespace `absw::` with components such as `CpuContext`, `GuestMemory`, `GuestThread`, `ElfLoader`, `Thunks`, and `GuestModule`.
- `absw::bridge::Load(JavaVM*)`, `kGameName` and guest-library / JNI registration tables.
- JNI entry points matching the original app package, including `Java_com_firsttouchgames_dlsa_JNI_*`.
- EGL/OpenGL ES forwarding functions and Android native interfaces such as `ANativeWindow_fromSurface`, `AAssetManager_fromJava`, and asset read/open functions.
- OpenSL ES / `libOpenSLES.so` support in the ARM32 guest dependency model.

The embedded guest binary's dynamic dependencies include `libc.so`, `libstdc++.so`, `libandroid.so`, `liblog.so`, `libGLESv2.so`, `libEGL.so`, `libOpenSLES.so`, `libdl.so`, `libm.so`, and `libGLESv1_CM.so`.

**Conclusion:** the compatibility layer is implemented inside the ARM64 `libDLS2.so` as a custom ARM32 guest runtime using Dynarmic, with custom ELF loading, guest memory/thread/context support, JNI bridging, Android asset bridging, and EGL/GLES forwarding. The APK does not appear to rely on a separate generic emulator APK/library; the bridge and game-specific configuration are bundled into this native library.

## What this means for DLS 2017

This is a much more useful reference than a generic ABI-only wrapper. DLS 2017's ARM32 library and dependencies still need their own compatibility work. Reusing the DLS 2015 ARM64 binary as a drop-in bridge is unlikely to work because it contains game-specific JNI mappings, export tables, library names, and behavior assumptions. It is also a proprietary third-party binary; do not copy it into our repository or redistribute it.

A clean implementation path is to use Dynarmic under its own licence and independently implement the required guest ELF loader, ARM32 runtime/syscall behavior, JNI handle/call bridge, and EGL/GLES/asset/audio/input adapters. Then validate each missing symbol and runtime behavior against DLS 2017 logs. The exact bridge source for this mod was not found in public GitHub search, so its full implementation details cannot be confirmed from source.

## Status

Static analysis only. The APK was not launched in an Android device/emulator during this inspection, and this document does not claim the DLS 2017 port is working.
