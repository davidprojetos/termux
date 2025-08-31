const admin = require('firebase-admin');
const serviceAccount = require('./firebase.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const registrationToken = 'fbvOfiARTw6SanQDj_G2XJ:APA91bElGoHQCeej3EN1VRnYWPaRcFjgXf6WAm1-vtv3HQ7-WlUY0Kdddqz-GGqo-xjfxtHctG9-4MX4gWrCq3S6GNzsPJfk8bAXbRqPDcQdxnHzKOUzFM8';

const message = {
  notification: {
    title: 'Nova Mensagem',
    body: 'Você recebeu uma nova mensagem!',
  },
  data: {
    tipo: 'mensagem',        // indica que é mensagem para abrir ChatActivity
    id_mensagem: '789',      // id da mensagem
    //url: 'https://meu-portifolio-david.vercel.app/' // opcional, abre no navegador
  },
  android: {
    priority: 'high',
    notification: {
      sound: 'default',
      color: '#0000FF',
      channelId: 'mensagens_importantes',
      clickAction: 'CHAT_ACTIVITY' // abre ChatActivity
    },
  },
  token: registrationToken,
};

admin.messaging().send(message)
  .then((response) => {
    console.log('✅ Notificação enviada com sucesso:', response);
  })
  .catch((error) => {
    console.error('❌ Erro ao enviar notificação:', error);
  });