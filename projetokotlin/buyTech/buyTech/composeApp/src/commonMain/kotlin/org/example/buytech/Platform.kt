package org.example.buytech

expect class Platform() {
    val name: String
}

expect fun getPlatform(): Platform
