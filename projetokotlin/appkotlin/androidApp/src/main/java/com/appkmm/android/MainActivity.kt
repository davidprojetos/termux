package com.appkmm.android

import android.app.Activity
import android.os.Bundle
import android.widget.TextView
import com.appkmm.shared.Greeting

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val textView = TextView(this)
        textView.text = Greeting().greet()
        setContentView(textView)
    }
}
