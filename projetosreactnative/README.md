termux

npx @react-native-community/cli init novoappnativeexemplo --version 0.80.0



npx create-expo-app@latest novoAppNative
npx expo prebuild

cd novoAppNative/
npx expo prebuild
npm start
cd android/
./gradlew assembleDebug

adb devices
adb connect 192.168.18.4:36259

keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
mv my-release-key.keystore app/

adb install /home/david/Documentos/apps/novoAppNative/android/app/build/outputs/apk/debug/app-x86-debug.apk

android.aapt2FromMavenOverride=/data/data/com.termux/files/usr/opt/Android/sdk/build-tools/34.0.4/aapt2

versao compativel 

gradle.wrapper.properties


distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.14.1-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists




gradle.properties


org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m
android.useAndroidX=true
reactNativeArchitectures=armeabi-v7a,arm64-v8a,x86,x86_64
newArchEnabled=false
hermesEnabled=true
android.suppressUnsupportedCompileSdk=34
android.aapt2FromMavenOverride=/data/data/com.termux/files/usr/opt/Android/sdk/build-tools/34.0.4/aapt2


build.gradle


buildscript {
    ext {
    buildToolsVersion = "34.0.4"
    minSdkVersion = 24
    compileSdkVersion = 34
    targetSdkVersion = 34
    ndkVersion = "27.1.12297006"
    }
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath("com.android.tools.build:gradle")
        classpath("com.facebook.react:react-native-gradle-plugin")
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin")
    }
}

apply plugin: "com.facebook.react.rootproject"


app/build.gradle


./gradlew assembleDebug && adb install app/build/outputs/apk/debug/app-debug.apk
