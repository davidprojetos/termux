package org.example.buytech

actual class Platform actual constructor() {
    actual val name: String = "Android"
}

actual fun getPlatform(): Platform = Platform()
