Contexto do Projeto:

- Projeto Android Multiplatform (Kotlin + Compose) rodando no Termux.
- Estrutura principal:
  - composeApp/src/commonMain → lógica comum (App(), etc).
  - composeApp/src/androidMain → código específico Android (MainActivity, notificações, etc).
- Função implementada: Notificações locais usando NotificationChannel + NotificationCompat.
- Status atual:
  - Botão "Ativar notificações" aparece se permissão estiver desativada.
  - Botão "Enviar notificação" envia push local para a barra de notificações.
  - Botão "Desativar notificações" abre as configurações do app corretamente.
- Problema resolvido: agora o app identifica corretamente se a permissão de POST_NOTIFICATIONS foi concedida ou não.
- Próximo passo: integrar Firebase Cloud Messaging (FCM) para receber notificações remotas.
- Repositório: Projeto rodando via Termux, compilado com Gradle no Android SDK instalado dentro do Termux.

Objetivo das próximas conversas:
- Expandir sistema de notificações locais para integrar com FCM.
- Manter compatibilidade com Android 13+ (POST_NOTIFICATIONS).
- Garantir que notificações funcionem mesmo com o app em segundo plano.