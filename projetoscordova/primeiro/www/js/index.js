
document.addEventListener('deviceready', onDeviceReady, false);

function onDeviceReady() {
    // Cordova is now initialized. Have fun!

    console.log('Running cordova-' + cordova.platformId + '@' + cordova.version);
    document.getElementById('deviceready').classList.add('ready');
}

const API_URL = "https://davidsousaplay.pythonanywhere.com";

// Função para cadastrar usuário
$("#registerForm").on("submit", async function (event) {
    event.preventDefault();

    const nome = $("#name").val();
    const email = $("#email").val();
    const senha = $("#password").val();
    const confirmarSenha = $("#confirm_password").val();

    if (senha !== confirmarSenha) {
        mostrarNotificacao("As senhas não coincidem!",{posicao: "bottom-right"} );
        return;
    }

    try {
        const response = await fetch(`${API_URL}/cadastrar`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ nome, email, senha }),
        });

        const data = await response.json();
        if (response.ok) {
            mostrarNotificacao(data.mensagem);
            $.mobile.changePage("#loginPage");
        } else {
            mostrarNotificacao(data.erro,{posicao: "bottom-right"});
        }
    } catch (error) {
        mostrarNotificacao("Erro ao conectar à API.",{posicao: "bottom-right"});
        console.error(error);
    }
});

// Função para logar usuário
$("#loginForm").on("submit", async function (event) {
    event.preventDefault();

    const email = $("#login_email").val();
    const senha = $("#login_password").val();

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, senha }),
        });

        const data = await response.json();
        if (response.ok) {
            mostrarNotificacao(data.mensagem,{posicao: "bottom-right"});
            // Redirecionar para a página de espaço logado
            $.mobile.changePage("#loggedInPage");
        } else {
            mostrarNotificacao(data.erro,{posicao: "bottom-right"});
        }
    } catch (error) {
        mostrarNotificacao("Erro ao conectar à API.",{posicao: "bottom-right"});
        console.error(error);
    }
});
