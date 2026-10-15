package org.dls17.compat;

/**
 * Diagnostic entry point for the ARM64 compatibility scaffold.
 *
 * This is not an ARM32 emulator. It deliberately reports the current
 * limitation instead of attempting to load an incompatible 32-bit .so.
 */
public final class CompatProbe {
    static {
        System.loadLibrary("dls17_compat");
    }

    private CompatProbe() {}

    public static native String nativeStatus();
}
