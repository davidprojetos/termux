package org.example.buytech

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat

class MainActivity : ComponentActivity() {

    private val CHANNEL_ID = "buytech_channel"
    private val NOTIFICATION_PERMISSION_REQUEST = 100

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        createNotificationChannel()

        setContent {
            NotificationScreen()
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = "BuyTech Channel"
            val descriptionText = "Canal de notificações do BuyTech"
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(CHANNEL_ID, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager =
                getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }
    }

    @Composable
    fun NotificationScreen() {
        var hasPermission by remember { mutableStateOf(checkNotificationPermission()) }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            if (!hasPermission) {
                Button(
                    onClick = { requestNotificationPermission() },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Ativar notificações")
                }
            } else {
                Button(
                    onClick = {
                        postNotification(
                            this@MainActivity,
                            "BuyTech Notification",
                            "Notificações estão ativas!"
                        )
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Enviar Notificação")
                }

                Button(
                    onClick = { openNotificationSettings() },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Desativar notificações")
                }
            }
        }

        // Atualiza estado ao voltar das configs ou após permissão
        LaunchedEffect(Unit) {
            hasPermission = checkNotificationPermission()
        }
    }

    private fun checkNotificationPermission(): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.POST_NOTIFICATIONS
            ) == PackageManager.PERMISSION_GRANTED
        } else {
            // Para Android <= 12, só precisa verificar se está habilitado no sistema
            NotificationManagerCompat.from(this).areNotificationsEnabled()
        }
    }

    private fun requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                NOTIFICATION_PERMISSION_REQUEST
            )
        } else {
            openNotificationSettings()
        }
    }

    private fun openNotificationSettings() {
    val intent = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
        // Android 8.0 (API 26) ou superior
        Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS).apply {
            putExtra(Settings.EXTRA_APP_PACKAGE, packageName)
        }
    } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
        // Android 5.0 a 7.1
        Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS).apply {
            putExtra("app_package", packageName)
            putExtra("app_uid", applicationInfo.uid)
        }
    } else {
        // Fallback para versões antigas
        Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = Uri.parse("package:$packageName")
        }
    }

    try {
        startActivity(intent)
    } catch (e: Exception) {
        // Caso alguma ROM/customização falhe, abre tela geral do app
        val fallbackIntent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = Uri.parse("package:$packageName")
        }
        startActivity(fallbackIntent)
    }
}

    private fun postNotification(context: Context, title: String, message: String) {
        val builder = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_dialog_info) // Ícone padrão do sistema
            .setContentTitle(title)
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)

        with(NotificationManagerCompat.from(context)) {
            notify(1, builder.build())
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == NOTIFICATION_PERMISSION_REQUEST) {
            setContent { NotificationScreen() }
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                postNotification(this, "Permissão Concedida", "Agora você receberá notificações!")
            }
        }
    }
}