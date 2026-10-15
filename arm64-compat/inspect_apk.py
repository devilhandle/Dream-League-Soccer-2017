#!/usr/bin/env python3
"""Read-only ABI and ELF header inspector for the DLS 2017 APK.

This deliberately does not rewrite ELF files or pretend ARM32 code is ARM64.
"""
from __future__ import annotations
import struct
import sys
import zipfile
from pathlib import PurePosixPath

EM_NAMES = {
    3: "x86",
    40: "ARM",
    62: "x86-64",
    183: "AArch64",
}

def inspect_elf(name: str, data: bytes) -> list[str]:
    out = [f"\n[{name}]"]
    if len(data) < 20 or data[:4] != b"\x7fELF":
        return out + ["Not an ELF shared object (or truncated)."]
    elf_class = data[4]
    endian_id = data[5]
    endian = {1: "<", 2: ">"}.get(endian_id)
    if endian is None:
        return out + [f"Invalid ELF byte order id: {endian_id}"]
    class_name = {1: "ELF32", 2: "ELF64"}.get(elf_class, f"unknown class {elf_class}")
    try:
        machine = struct.unpack_from(endian + "H", data, 18)[0]
    except struct.error:
        return out + ["Could not read ELF header."]
    out.append(f"ELF class: {class_name}")
    out.append(f"e_machine: {machine} ({EM_NAMES.get(machine, 'unknown')})")
    if machine == 40:
        out.append("Result: 32-bit ARM; not an arm64-v8a binary.")
    elif machine == 183:
        out.append("Result: AArch64 machine code.")
    elif machine == 3:
        out.append("Result: 32-bit x86 machine code.")
    elif machine == 62:
        out.append("Result: x86-64 machine code.")
    else:
        out.append("Result: architecture needs manual review.")
    return out

def main(path: str) -> int:
    report: list[str] = [f"APK: {path}"]
    try:
        apk = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        print(f"Cannot open APK: {exc}", file=sys.stderr)
        return 2
    with apk:
        names = apk.namelist()
        libs = sorted(n for n in names if n.startswith("lib/") and n.endswith(".so"))
        report.append(f"APK entries: {len(names)}")
        report.append("Native library paths:")
        report.extend(f"  {name}" for name in libs)
        if not libs:
            report.append("  (none found)")
        for name in libs:
            report.extend(inspect_elf(name, apk.read(name)))
        report.append("\nPotential engine/runtime markers:")
        markers = ("libunity", "libil2cpp", "unityplayer", "global-metadata.dat",
                   "libmono", "libdls17", "libadcolony", "libjs")
        matched = [n for n in names if any(m in n.lower() for m in markers)]
        report.extend(f"  {n}" for n in matched) if matched else report.append("  (none found)")
    print("\n".join(report))
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} path/to/game.apk", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
