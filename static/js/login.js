// document.getElementById('meuArquivo').addEventListener('change', function(event) {
//     const input = event.target;
//     const imagemPreview = document.getElementById('imagemPreview');
//
//     // Verifica se algum arquivo foi selecionado e se é uma imagem
//     if (input.files && input.files[0]) {
//         const file = input.files[0];
//
//         // 1. Cria um novo objeto FileReader
//         const reader = new FileReader();
//
//         // 2. Define a função que será executada quando o arquivo for lido
//         reader.onload = function(e) {
//             // e.target.result contém o URL de dados (Data URL) da imagem
//             imagemPreview.src = e.target.result;
//             imagemPreview.style.display = 'block'; // Mostra a imagem
//         };
//
//         // 3. Lê o arquivo como um Data URL
//         reader.readAsDataURL(file);
//
//     } else {
//         // Se nenhum arquivo foi selecionado ou a seleção foi cancelada
//         imagemPreview.src = '#';
//         imagemPreview.style.display = 'none'; // Esconde a imagem
//     }
// });

document.getElementById('meuArquivo').addEventListener('change', function(event) {
    const input = event.target;
    const imagemPreview = document.getElementById('imagemPreview');

    if (input.files && input.files[0]) {
        const file = input.files[0];

        // Validação adicional do tipo de arquivo
        if (!file.type.startsWith('image/')) {
            alert('Por favor, selecione um arquivo de imagem.');
            input.value = ''; // Limpa o input
            imagemPreview.style.display = 'none';
            return;
        }

        // Verificação de tamanho (exemplo: 5MB)
        if (file.size > 5 * 1024 * 1024) {
            alert('A imagem deve ter no máximo 5MB.');
            input.value = '';
            imagemPreview.style.display = 'none';
            return;
        }

        const reader = new FileReader();

        reader.onload = function(e) {
            imagemPreview.src = e.target.result;
            imagemPreview.style.display = 'block';
        };

        reader.onerror = function() {
            alert('Erro ao ler a imagem.');
            imagemPreview.style.display = 'none';
        };

        reader.readAsDataURL(file);

    } else {
        imagemPreview.style.display = 'none';
        // imagemPreview.src = '#'; // Esta linha é opcional
    }
});

const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});