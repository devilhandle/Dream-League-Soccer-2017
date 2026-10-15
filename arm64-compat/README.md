# ARM64 compatibility investigation

The repository contains an APK binary, not the game's original engine/game source project. The first inspection workflow found these packaged native libraries:

- `lib/armeabi-v7a/libDLS17.so`
- `lib/armeabi-v7a/libadcolony.so`
- `lib/armeabi-v7a/libjs.so`
- `lib/x86/libDLS17.so`
- `lib/x86/libadcolony.so`
- `lib/x86/libjs.so`

There are no packaged `arm64-v8a` libraries in that listing, and the quick filename scan did not find conventional `libunity.so` or `libil2cpp.so` names. This is not enough to identify the engine or prove how `libDLS17.so` is structured; the ELF and dependency report is the next evidence-gathering step.

## Work completed

1. Added a CI workflow to inventory native library paths.
2. Added a read-only Python inspector that reports ELF class and machine type.
3. Added a deeper workflow to collect ELF headers, dynamic dependencies and JNI exports.

## Why this is not a simple ARM64 rebuild

The packaged libraries are 32-bit ARM and 32-bit x86 variants, not AArch64 binaries. Renaming a library or placing it under `lib/arm64-v8a` does not translate machine code. A native ARM64 port generally needs compatible AArch64 libraries and suitable source/build inputs. A Shadowgun-Bridge-style route is instead a separate compatibility runtime: the exact DLS library's ABI, imports, JNI behavior, graphics API, audio path and startup flow must be checked against the bridge before adapting anything.

## Next engineering gate

Review the `dls-elf-inspection` artifact. Only after checking the actual ELF headers, `DT_NEEDED` entries, exports and manifest should we choose between a native port (if source/dependencies exist) and a compatibility runtime. This workflow does not modify the APK and does not claim to produce a working converted APK.
