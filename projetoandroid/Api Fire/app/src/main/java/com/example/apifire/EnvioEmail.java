package com.example.apifire;

import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import java.util.Properties;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

public class EnvioEmail {
    
    private EditText editTextRecipient, editTextName, editTextSubject, editTextMessage;
    private Button buttonSend;
    
    public EnvioEmail (EditText editTextRecipient, EditText editTextName, EditText editTextSubject, EditText editTextMessage, Button buttonSend){
        this.editTextRecipient = editTextRecipient;
        this.editTextName = editTextName;
        this.editTextSubject = editTextSubject;
        this.editTextMessage = editTextMessage;
        this.buttonSend = buttonSend;
        
        buttonSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String recipient = editTextRecipient.getText().toString();
                String name = editTextName.getText().toString();
                String subject = editTextSubject.getText().toString();
                String message = editTextMessage.getText().toString();

                if (!recipient.isEmpty() && !subject.isEmpty() && !message.isEmpty()) {
                    sendEmail(recipient, name, subject, message);
                } else {
                    Toast.makeText(buttonSend.getContext(), "Por favor, preencha todos os campos", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }
    
    private void sendEmail(final String recipient, final String name, final String subject, final String message) {
        final String username = "davidk1k3kk@gmail.com";
        final String password = "hmpsxqjasdvsxtqu";

        // Configurações do servidor SMTP
        Properties props = new Properties();
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");
        props.put("mail.smtp.host", "smtp.gmail.com");
        props.put("mail.smtp.port", "587");

        Session session = Session.getInstance(props, new javax.mail.Authenticator() {
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(username, password);
            }
        });

        AsyncTask<Void, Void, Void> task = new AsyncTask<Void, Void, Void>() {
            @Override
            protected Void doInBackground(Void... voids) {
                try {
                    Message mimeMessage = new MimeMessage(session);
                    mimeMessage.setFrom(new InternetAddress(username));
                    mimeMessage.setRecipients(Message.RecipientType.TO, InternetAddress.parse(recipient));
                    mimeMessage.setSubject(subject);

                    // Conteúdo HTML do e-mail
                    String htmlContent = "<!DOCTYPE html>" +
                     "<html lang=\"pt-BR\">" +
                     "<head>" +
                     "<meta charset=\"UTF-8\">" +
                     "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">" +
                     "<title>Contato</title>" +
                     "<style>" +
                     "body { font-family: Arial, sans-serif; }" +
                     ".container { padding: 20px; }" +
                     ".header { background-color: #4CAF50; color: white; padding: 10px; text-align: center; }" +
                     ".content { margin: 20px 0; }" +
                     ".footer { background-color: #f1f1f1; color: #333; padding: 10px; text-align: center; }" +
                     "</style>" +
                     "</head>" +
                     "<body>" +
                     "<div class=\"container\">" +
                     "<div class=\"header\">" +
                     "<h1>Mensagem de Contato</h1>" +
                     "</div>" +
                     "<div class=\"content\">" +
                     "<p>Prezado(a) " + name + ",</p>" +
                     "<p>" + message + "</p>" +
                     "</div>" +
                     "<div class=\"footer\">" +
                     "<p>Atenciosamente,<br/>Sua Empresa</p>" +
                     "</div>" +
                     "</div>" +
                     "</body>" +
                     "</html>";

                    mimeMessage.setContent(htmlContent, "text/html; charset=utf-8");

                    Transport.send(mimeMessage);
                } catch (MessagingException e) {
                    e.printStackTrace();
                }
                return null;
            }

            @Override
            protected void onPostExecute(Void aVoid) {
                super.onPostExecute(aVoid);
                Toast.makeText(buttonSend.getContext(), "E-mail enviado com sucesso!", Toast.LENGTH_SHORT).show();
                
                // Limpar campos após o envio do e-mail
                editTextRecipient.setText("");
                editTextName.setText("");
                editTextSubject.setText("");
                editTextMessage.setText("");
            }
        };

        task.execute();
    }
}
