android {
    compileSdk = 34
    buildToolsVersion = "34.0.4"

    defaultConfig {
        applicationId = "com.appkmm.android"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlin {
        // Aqui você pode manter kotlinOptions
        // ou migrar para compilerOptions como o aviso recomenda
        kotlinOptions {
            jvmTarget = "17"
        }
    }
}