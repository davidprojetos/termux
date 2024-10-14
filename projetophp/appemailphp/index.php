<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

// Carregar o autoload do Composer
require 'vendor/autoload.php';

// Criação da instância do PHPMailer
$mail = new PHPMailer(true);

try {
    // Configurações do servidor
    $mail->isSMTP();                                            // Enviar usando SMTP
    $mail->Host       = 'smtp.gmail.com';                       // Configurar o servidor SMTP
    $mail->SMTPAuth   = true;                                   // Ativar autenticação SMTP
    $mail->Username   = 'davidk1k3kk@gmail.com';                  // Usuário SMTP
    $mail->Password   = 'hmpsxqjasdvsxtqu';                            // Senha SMTP
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;         // Ativar criptografia TLS
    $mail->Port       = 465;                                    // Porta TCP para se conectar

    // Destinatários
    $mail->setFrom('davidk1k3kk@gmail.com', 'Seu Nome');
    $mail->addAddress('davidk1k3k@gmail.com', 'Nome do Destinatário');     // Adicionar um destinatário

    // Conteúdo do e-mail
    $mail->isHTML(true);                                        // Definir o formato do e-mail como HTML
    $mail->Subject = 'Assunto do e-mail';
    $mail->Body    = 'Este é o conteúdo do e-mail em <b>HTML</b>.';
    $mail->AltBody = 'Este é o conteúdo do e-mail em texto puro para clientes de e-mail que não suportam HTML.';

    $mail->send();
    echo 'E-mail enviado com sucesso!';
} catch (Exception $e) {
    echo "Erro ao enviar e-mail: {$mail->ErrorInfo}";
}
?>
