package com.exemplo;

import java.util.Properties;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

public class App {
    public static void main(String[] args) {
        // Configurações do servidor SMTP
        String host = "smtp.gmail.com";
        final String username = "davidk1k3kk@gmail.com"; // Coloque seu email
        final String password = "hmpsxqjasdvsxtqu";           // Coloque sua senha

        // Configurações das propriedades
        Properties props = new Properties();
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");
        props.put("mail.smtp.host", host);
        props.put("mail.smtp.port", "587");

        // Criação da sessão
        Session session = Session.getInstance(props,
            new javax.mail.Authenticator() {
                protected PasswordAuthentication getPasswordAuthentication() {
                    return new PasswordAuthentication(username, password);
                }
            });

        try {
            // Criação da mensagem de e-mail
            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress("davidk1k3kk@gmail.com")); // Remetente
            message.setRecipients(Message.RecipientType.TO,
                InternetAddress.parse("davidk1k3k@gmail.com")); // Destinatário
            message.setSubject("Assunto do E-mail"); // Assunto
            message.setText("Este é o conteúdo do e-mail."); // Corpo do e-mail

            // Envio da mensagem
            Transport.send(message);

            System.out.println("E-mail enviado com sucesso!");

        } catch (MessagingException e) {
            throw new RuntimeException(e);
        }
    }
}
