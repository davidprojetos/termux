package org.example.buytech

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform