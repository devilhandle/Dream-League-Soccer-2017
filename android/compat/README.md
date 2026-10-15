# Android ARM64 compatibility scaffold

This directory contains a small **arm64-v8a diagnostic JNI library**, not a
finished ARM32 compatibility runtime.

## APK inspection findings

The supplied Dream League Soccer 2017 APK packages these native libraries
under `lib/armeabi-v7a/` and `lib/x86/`:

- `libDLS17.so` (main game library)
- `libjs.so`
- `libadcolony.so`

The ARM library was inspected as ELF32 / ARM. The APK has no
`lib/arm64-v8a/` directory.

## Build the diagnostic library

The standalone Android Gradle project is in this `android/` directory.
With Android SDK, NDK, CMake, and a compatible Gradle installation configured:

```sh
cd android
gradle :compat:assembleRelease
```

The module is deliberately configured with `abiFilters 'arm64-v8a'`. The
resulting AArch64 JNI library is a diagnostic shim; it does not load or run
the game's ARM32 `.so` files. From a host app in the same package, call
`CompatProbe.nativeStatus()` to retrieve the current status. If integrating
into another app, include the Java class and the native library in that app
and adapt the JNI package/signature as needed.

## Work still required for real compatibility

A runnable solution needs an ARM32 user-space execution engine or a genuine
64-bit port of the game's native code, plus Android/Bionic and JNI bridging,
graphics (EGL/GLES), audio, input, threading, filesystem, and lifecycle
integration. The original game libraries are closed-source binaries in the
APK; an ABI folder rename or linker shim cannot translate ARM machine code.
Those components must be implemented and tested before claiming compatibility.

Do not commit or redistribute the APK, game assets, or proprietary native
libraries. Keep testing with a copy you are authorized to use.
