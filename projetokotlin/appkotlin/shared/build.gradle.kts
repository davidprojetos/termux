plugins {
    kotlin("multiplatform")
    id("com.android.library")
}

kotlin {
    android() // <-- substitua androidTarget() por android() nas versões recentes
    sourceSets {
        val commonMain by getting
        val androidMain by getting
    }
}

android {
    namespace = "com.appkmm.shared"
    compileSdk = 34
    buildToolsVersion = "34.0.4"

    defaultConfig {
        minSdk = 24
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    // Remova kotlinOptions daqui do shared
}