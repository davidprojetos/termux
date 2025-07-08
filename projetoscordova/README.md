# Config TERMUX
- ~/.bashrc or ~/.zshrc
```sh
  export ANDROID_HOME="$PREFIX/opt/Android/sdk"
  export PATH="$PATH:$ANDROID_HOME/cmdline-tools/latest/bin"
  export JAVA_HOME=/data/data/com.termux/files/usr/lib/jvm/java-17-openjdk
  export "PATH=$PATH:$PREFIX/opt/gradle/bin"
```

# Criar corretamente

## Criar projeto
```sh
  cordova create nome-do-app br.com.app "Nome do app"
```

## Adicionar android
```sh
cd nome-do-app
cordova platform add android@13.0.0 # Com suporte a aarch64 
cordova platform add browser
```


# Add gradle.properties
```sh
org.gradle.jvmargs=-Xmx2048m
android.useAndroidX=true
android.enableJetifier=true

android.aapt2FromMavenOverride=/data/data/com.termux/files/usr/opt/Android/sdk/build-tools/34.0.4/aapt2
```

# Criar o local.properties

```sh

echo "sdk.dir=/data/data/com.termux/files/usr/opt/Android/sdk" > platforms/android/local.properties

```

# Build
```sh
  cordova build android
```
# Mensagem de saida esperada

Checking Java JDK and Android SDK versions
ANDROID_HOME=/data/data/com.termux/files/usr/opt/Android/sdk (recommended setting)                                    ANDROID_SDK_ROOT=undefined (DEPRECATED)
Using Android SDK: /data/data/com.termux/files/usr/opt/Android/sdk
                                                           Welcome to Gradle 8.10.2!

Here are the highlights of this release:
 - Support for Java 23
 - Faster configuration cache
 - Better configuration cache reports                      
For more details see https://docs.gradle.org/8.10.2/release-notes.html
                                                           Starting a Gradle Daemon (subsequent builds will be faster)
> Task :wrapper

BUILD SUCCESSFUL in 33s
1 actionable task: 1 executed
Subproject Path: CordovaLib
Subproject Path: app
Starting a Gradle Daemon (subsequent builds will be faster)

> Configure project :app
WARNING: The option setting 'android.aapt2FromMavenOverride=/data/data/com.termux/files/usr/opt/Android/sdk/build-tools/34.0.0/aapt2' is experimental.
Observed package id 'platform-tools' in inconsistent location '/data/data/com.termux/files/usr/opt/Android/sdk/platform-tools-2' (Expected '/data/data/com.termux/files/usr/opt/Android/sdk/platform-tools')

> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:generateDebugBuildConfig UP-TO-DATE
> Task :app:javaPreCompileDebug UP-TO-DATE
> Task :CordovaLib:preBuild UP-TO-DATE
> Task :CordovaLib:preDebugBuild UP-TO-DATE
> Task :CordovaLib:writeDebugAarMetadata UP-TO-DATE
> Task :app:checkDebugAarMetadata UP-TO-DATE
> Task :app:generateDebugResValues UP-TO-DATE
> Task :CordovaLib:generateDebugResValues UP-TO-DATE
> Task :CordovaLib:generateDebugResources UP-TO-DATE
> Task :CordovaLib:packageDebugResources UP-TO-DATE
> Task :app:mapDebugSourceSetPaths UP-TO-DATE
> Task :app:generateDebugResources UP-TO-DATE
> Task :app:mergeDebugResources UP-TO-DATE
> Task :app:packageDebugResources UP-TO-DATE
> Task :app:parseDebugLocalResources UP-TO-DATE
> Task :app:createDebugCompatibleScreenManifests UP-TO-DATE
> Task :app:extractDeepLinksDebug UP-TO-DATE
> Task :CordovaLib:extractDeepLinksDebug UP-TO-DATE
> Task :CordovaLib:processDebugManifest UP-TO-DATE
> Task :app:processDebugMainManifest UP-TO-DATE
> Task :app:processDebugManifest UP-TO-DATE
> Task :app:processDebugManifestForPackage UP-TO-DATE
> Task :CordovaLib:compileDebugLibraryResources UP-TO-DATE
> Task :CordovaLib:parseDebugLocalResources UP-TO-DATE
> Task :CordovaLib:generateDebugRFile UP-TO-DATE
> Task :app:processDebugResources UP-TO-DATE
> Task :CordovaLib:javaPreCompileDebug UP-TO-DATE
> Task :CordovaLib:compileDebugJavaWithJavac UP-TO-DATE
> Task :CordovaLib:bundleLibCompileToJarDebug UP-TO-DATE
> Task :app:compileDebugJavaWithJavac UP-TO-DATE
> Task :app:mergeDebugShaders UP-TO-DATE
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :CordovaLib:mergeDebugShaders UP-TO-DATE
> Task :CordovaLib:compileDebugShaders NO-SOURCE
> Task :CordovaLib:generateDebugAssets UP-TO-DATE
> Task :CordovaLib:packageDebugAssets UP-TO-DATE
> Task :app:mergeDebugAssets UP-TO-DATE
> Task :app:compressDebugAssets UP-TO-DATE
> Task :app:processDebugJavaRes NO-SOURCE
> Task :CordovaLib:processDebugJavaRes UP-TO-DATE
> Task :app:mergeDebugJavaResource UP-TO-DATE
> Task :app:checkDebugDuplicateClasses UP-TO-DATE
> Task :app:desugarDebugFileDependencies UP-TO-DATE
> Task :app:mergeExtDexDebug UP-TO-DATE
> Task :CordovaLib:bundleLibRuntimeToDirDebug UP-TO-DATE
> Task :app:dexBuilderDebug UP-TO-DATE
> Task :app:mergeProjectDexDebug UP-TO-DATE
> Task :app:mergeDebugJniLibFolders UP-TO-DATE
> Task :CordovaLib:mergeDebugJniLibFolders UP-TO-DATE
> Task :app:mergeLibDexDebug UP-TO-DATE
> Task :CordovaLib:mergeDebugNativeLibs NO-SOURCE
> Task :CordovaLib:copyDebugJniLibsProjectOnly UP-TO-DATE
> Task :app:mergeDebugNativeLibs UP-TO-DATE
> Task :app:stripDebugDebugSymbols UP-TO-DATE
> Task :app:validateSigningDebug UP-TO-DATE
> Task :app:writeDebugAppMetadata UP-TO-DATE
> Task :app:writeDebugSigningConfigVersions UP-TO-DATE
> Task :app:packageDebug UP-TO-DATE
> Task :app:createDebugApkListingFileRedirect UP-TO-DATE
> Task :app:assembleDebug UP-TO-DATE
> Task :app:cdvBuildDebug UP-TO-DATE

BUILD SUCCESSFUL in 1m 6s
52 actionable tasks: 52 up-to-date
Built the following apk(s):
        /data/data/com.termux/files/home/termux/projetoscordova/x/platforms/android/app/build/outputs/apk/debug/app-debug.apk
        
# Copiar para downloads

```sh
cp platforms/android/app/build/outputs/apk/debug/app-debug.apk ~/storage/downloads

```

# Atualizar os pacotes

```sh
npm update
npm install -g npm-check-updates
npx npm-check-updates
npx npm-check-updates -u
npm install
npm list --depth=0
npm cache verify
npm cache clean --force
npm cache verify
```
