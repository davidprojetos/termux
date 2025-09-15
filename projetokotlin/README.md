./gradlew clean
./gradlew assembleDebug

adb devices

#Ligue a depuração WI-FI
adb connect 100.98.16

adb install -r composeApp/build/outputs/apk/debug/composeApp-debug.apk