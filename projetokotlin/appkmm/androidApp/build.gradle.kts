plugins {
    id("com.android.application") version "8.6.0"
    kotlin("android") version "2.2.0"
}

android {
    namespace = "com.appkmm.android"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.appkmm.android"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        getByName("release") {
            isMinifyEnabled = false
        }
        getByName("debug") {
            isMinifyEnabled = false
        }
    }
}

repositories {
    google()
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))
}