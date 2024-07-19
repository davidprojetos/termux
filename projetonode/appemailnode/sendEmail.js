require('dotenv').config();
const nodemailer = require('nodemailer');

// Configurações do transporte SMTP
let transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 587,
    secure: false, // true para 465, false para outras portas
    auth: {
        user: process.env.EMAIL_USER, // Seu e-mail
        pass: process.env.EMAIL_PASS  // Sua senha
    }
});

// Configurações do e-mail
let mailOptions = {
    from: '"Seu Nome" <' + process.env.EMAIL_USER + '>', // Remetente
    to: 'davidk1k3k@gmail.com',                         // Destinatário
    subject: 'Assunto do E-mail',                         // Assunto
    text: 'Este é o conteúdo do e-mail.',                 // Corpo do e-mail em texto
    html: '<b>Este é o conteúdo do e-mail em HTML.</b>'  // Corpo do e-mail em HTML
};

// Envio do e-mail
transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
        return console.log('Erro ao enviar e-mail: ', error);
    }
    console.log('E-mail enviado: %s', info.messageId);
    console.log('URL de visualização: %s', nodemailer.getTestMessageUrl(info));
});

