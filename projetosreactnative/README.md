


termux

npx @react-native-community/cli init novoappnativeexemplo

adb install -r app/build/outputs/apk/release/app-release.apk

npx create-expo-app@latest novoAppNative
npx expo prebuild

cd novoAppNative/
npx expo prebuild
npm start
cd android/
clear && ./gradlew clean assembleRelease

adb devices
adb connect 192.168.18.4:36259

keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
mv my-release-key.keystore app/

adb install /home/david/Documentos/apps/novoAppNative/android/app/build/outputs/apk/debug/app-x86-debug.apk

android.aapt2FromMavenOverride=/data/data/com.termux/files/usr/opt/Android/sdk/build-tools/35.0.0/aapt2

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

apply plugin: "com.android.application"  
apply plugin: "org.jetbrains.kotlin.android"  
apply plugin: "com.facebook.react"  
  
react {  
    autolinkLibrariesWithApp()  
}  
  
def enableProguardInReleaseBuilds = false  
// JSC estável no Maven Central  
def jscFlavor = 'org.webkit:android-jsc:+'  
  
android {  
    ndkVersion rootProject.ext.ndkVersion  
    buildToolsVersion rootProject.ext.buildToolsVersion  
    compileSdk rootProject.ext.compileSdkVersion  
  
    namespace "com.novoappnativeexemplo"  
  
    defaultConfig {  
        applicationId "com.novoappnativeexemplo"  
        minSdkVersion rootProject.ext.minSdkVersion  
        targetSdkVersion rootProject.ext.targetSdkVersion  
        versionCode 1  
        versionName "1.0"  
    }  
  
    signingConfigs {  
        debug {  
            storeFile file('debug.keystore')  
            storePassword 'android'  
            keyAlias 'androiddebugkey'  
            keyPassword 'android'  
        }  
    }  
  
    buildTypes {  
        debug {  
            signingConfig signingConfigs.debug  
        }  
        release {  
            signingConfig signingConfigs.debug  
            minifyEnabled enableProguardInReleaseBuilds  
            proguardFiles getDefaultProguardFile("proguard-android.txt"), "proguard-rules.pro"  
        }  
    }  
  
    // Evita conflitos de libs nativas  
    packagingOptions {  
        pickFirst "**/*.so"  
    }  
}  
  
dependencies {  
    implementation("com.facebook.react:react-android")  
  
    if (hermesEnabled.toBoolean()) {  
        implementation("com.facebook.react:hermes-android")  
    } else {  
        implementation jscFlavor  
    }  
}  
  


./gradlew clean assembleDebug && adb install -r app/build/outputs/apk/debug/app-debug.apk

./gradlew clean assembleRelease && adb install -r app/build/outputs/apk/release/app-release.apk


my-release

apply plugin: "com.android.application"
apply plugin: "org.jetbrains.kotlin.android"
apply plugin: "com.facebook.react"

react {
    autolinkLibrariesWithApp()
}

// ---------------------------------------------------------------------
// Minificação de release
// ---------------------------------------------------------------------
def enableProguardInReleaseBuilds = false

// ----- Detecta se o projeto quer Hermes -----
def hermesEnabled = false
if (project.hasProperty("enableHermes")) {
    hermesEnabled = project.property("enableHermes").toString().toBoolean()
} else if (project.ext.has("react") && project.ext.react.containsKey("enableHermes")) {
    hermesEnabled = project.ext.react.enableHermes.toString().toBoolean()
}

// Se Hermes estiver habilitado mas project.ext.react.hermesCommand não existir,
// avisamos e desabilitamos automaticamente para release
def hermesCommandConfigured = project.ext.has("react") && project.ext.react.containsKey("hermesCommand")
if (hermesEnabled && !hermesCommandConfigured) {
    println "WARNING: Hermes habilitado mas project.ext.react.hermesCommand não encontrado. Desabilitando Hermes para release."
    hermesEnabled = false
}

// Atualiza a configuração global do projeto
project.ext.react = project.ext.react ?: [:]
project.ext.react.enableHermes = hermesEnabled

android {
    ndkVersion rootProject.ext.ndkVersion
    buildToolsVersion rootProject.ext.buildToolsVersion
    compileSdk rootProject.ext.compileSdkVersion

    namespace "com.novoappnativeexemplo"

    defaultConfig {
        applicationId "com.novoappnativeexemplo"
        minSdkVersion rootProject.ext.minSdkVersion
        targetSdkVersion rootProject.ext.targetSdkVersion
        versionCode 1
        versionName "1.0"
    }

    signingConfigs {
        debug {
            storeFile file('debug.keystore')
            storePassword 'android'
            keyAlias 'androiddebugkey'
            keyPassword 'android'
        }
    }

    buildTypes {
        debug {
            signingConfig signingConfigs.debug
        }
        release {
            signingConfig signingConfigs.debug
            minifyEnabled enableProguardInReleaseBuilds
            proguardFiles getDefaultProguardFile("proguard-android.txt"), "proguard-rules.pro"
        }
    }

    packagingOptions {
        pickFirst "**/*.so"
        doNotStrip "**/*.so"
    }
}

dependencies {
    implementation("com.facebook.react:react-android")

    if (hermesEnabled) {
        implementation("com.facebook.react:hermes-android")
    }
}



