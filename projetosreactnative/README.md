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