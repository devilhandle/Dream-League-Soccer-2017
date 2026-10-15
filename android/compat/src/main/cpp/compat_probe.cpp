#include <jni.h>
#include <string>

namespace {
constexpr const char* kStatus =
    "DLS17 ARM64 compatibility scaffold: native ARM32 game libraries detected "
    "in the supplied APK are not executable as arm64-v8a. This library only "
    "reports the state; it does not translate ARM instructions or emulate "
    "32-bit Android/Bionic, JNI, graphics, audio, or input.";
}

extern "C" JNIEXPORT jstring JNICALL
Java_org_dls17_compat_CompatProbe_nativeStatus(JNIEnv* env, jclass) {
    return env->NewStringUTF(kStatus);
}
