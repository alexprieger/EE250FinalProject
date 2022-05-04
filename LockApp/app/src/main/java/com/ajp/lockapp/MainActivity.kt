package com.ajp.lockapp

import android.media.AudioAttributes
import android.media.MediaPlayer
import android.os.Build
import android.os.Bundle
import android.os.StrictMode
import android.util.Log
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.net.toUri
import java.io.BufferedInputStream
import java.io.File
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        // Allow network requests on the main thread for simplicity (even though it's bad practice!)
        StrictMode.setThreadPolicy(StrictMode.ThreadPolicy.Builder().permitAll().build())

        val fetchDataButton = findViewById<Button>(R.id.fetch_data_button)
        fetchDataButton.setOnClickListener { fetchData() }
        val unlockButton = findViewById<Button>(R.id.unlock_button)
        unlockButton.setOnClickListener { unlock() }
        val lockButton = findViewById<Button>(R.id.lock_button)
        lockButton.setOnClickListener { lock() }
    }

    private fun fetchData() {
        val mediaPlayer = MediaPlayer().apply {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                setAudioAttributes(
                    AudioAttributes.Builder()
                        .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                        .setUsage(AudioAttributes.USAGE_MEDIA)
                        .build()
                )
            }
            setOnErrorListener { _, _, extra ->
                Toast.makeText(
                    this@MainActivity,
                    if (extra == -1015) {
                        "No current request for entry."
                    } else {
                        "Error connecting to server. Please try again."
                    },
                    Toast.LENGTH_LONG
                ).show()
                false
            }
            setDataSource("http://20.125.112.134/app")
            setOnPreparedListener {
                start()
            }
            prepareAsync()
        }
    }

    private fun unlock() {
        val url = URL("http://20.125.112.134/unlock")
        val httpConnection = url.openConnection() as HttpURLConnection
        try {
            if (httpConnection.responseCode != 200) {
                Toast.makeText(
                    this,
                    "Server response code: ${httpConnection.responseCode}",
                    Toast.LENGTH_LONG
                ).show()
            }
        } catch (e: Exception) {
            Toast.makeText(
                this,
                "Error connecting to the server. Please try again.",
                Toast.LENGTH_LONG
            ).show()
        }
    }

    private fun lock() {
        val url = URL("http://20.125.112.134/lock")
        val httpConnection = url.openConnection() as HttpURLConnection
        try {
            if (httpConnection.responseCode != 200) {
                Toast.makeText(
                    this,
                    "Server response code: ${httpConnection.responseCode}",
                    Toast.LENGTH_LONG
                ).show()
            }
        } catch (e: Exception) {
            Toast.makeText(
                this,
                "Error connecting to the server. Please try again.",
                Toast.LENGTH_LONG
            ).show()
        }
    }
}