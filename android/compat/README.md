# Android ARM64 compatibility scaffold

This directory contains a small **arm64-v8a diagnostic JNI library**, not a
finished ARM32 compatibility runtime.

## What the APK inspection found

The supplied Dream League Soccer 2017 APK packages these native libraries
under `lib/armeabi-v7a/` and `lib/x86/`:

- `libDLS17.so` (main game library)
- `libjs.so`
- `libadcolony.so`

The ARM library was inspected as ELF32 / ARM. The APK has no
`lib/arm64-v8a/` directory.

## Build integration

Add this directory's `src/main/cpp/CMakeLists.txt` as the CMake project for
an Android library module and configure the NDK ABI filter to
`arm64-v8a`. The module must also use the Java source at
`src/main/java/org/dls17/compat/CompatProbe.java`.

Example module settings:

```gradle
android {
    defaultConfig {
        ndk {
            abiFilters 'arm64-v8a'
        }
        externalNativeBuild {
            cmake {
                cppFlags '-std=c++17'
            }
        }
    }
    externalNativeBuild {
        cmake {
            path 'src/main/cpp/CMakeLists.txt'
        }
    }
}
```

Call `CompatProbe.nativeStatus()` from the host app to display the current
diagnostic status. This library itself can be built for ARM64, but it does
**not** make the original 32-bit game runnable.

## Work still required for real compatibility

A runnable solution needs an ARM32 user-space execution engine or a genuine
64-bit port of the game's native code, plus Android/Bionic and JNI bridging,
graphics (EGL/GLES), audio, input, threading, filesystem, and lifecycle
integration. The original game libraries are closed-source binaries in the
APK; an ABI folder rename or linker shim cannot translate ARM machine code.
Those components must be implemented and tested before claiming compatibility.

Do not commit or redistribute the APK, game assets, or proprietary native
libraries. Keep testing with a copy you are authorized to use.
