document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('content');
    const dataContainer = document.getElementById('data');

    // Função para buscar dados da API
    async function fetchData() {
        try {
            const response = await fetch('https://different-mewing-manchego.glitch.me/items');
            const data = await response.json();

            // Ocultar o skeleton loader
            content.style.display = 'none';

            // Mostrar os dados carregados
            dataContainer.innerHTML = data.map(item => `<div>${item.Nome}</div>`).join('');
        } catch (error) {
            console.error('Erro ao carregar os dados:', error);
            dataContainer.innerHTML = '<div>Erro ao carregar os dados.</div>';
        }
    }

    // Iniciar o carregamento dos dados
    fetchData();
});
