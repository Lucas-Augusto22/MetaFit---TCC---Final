// Adicione este script no final do my_level.html

document.addEventListener('DOMContentLoaded', function() {
    // Formulário de treino
    const formTreino = document.querySelector('.sign-in-container form');
    formTreino.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = {
            peso: this.querySelector('input[placeholder="Peso * kg"]').value,
            altura: this.querySelector('input[placeholder="Altura * m"]').value,
            experiencia: this.querySelector('input[type="checkbox"]:checked')?.parentElement?.textContent.trim() || 'a menos de 1 ano',
            objetivo: this.querySelector('input[type="checkbox"]:checked')?.parentElement?.querySelector('.inner')?.textContent || 'Perder peso',
            sexo: 'male' // Você pode adicionar um campo para isso
        };

        fetch('/api/salvar_treino', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Treino salvo com sucesso!');
                window.location.href = '/all_my_training';
            } else {
                alert('Erro ao salvar treino: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Erro ao salvar treino');
        });
    });

    // Formulário de agenda
    const formAgenda = document.querySelector('.sign-up-container form');
    formAgenda.addEventListener('submit', function(e) {
        e.preventDefault();

        const nomeTreino = this.querySelector('input[placeholder="Nome do treino/dieta"]').value;
        const horario = this.querySelector('input[placeholder="Horário"]').value;
        const diasSelecionados = Array.from(this.querySelectorAll('input[type="checkbox"]:checked'))
            .map(cb => cb.parentElement.textContent.trim());

        const itensAgenda = diasSelecionados.map(dia => ({
            horario: horario,
            dia_semana: dia
        }));

        fetch('/api/salvar_agenda', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ itens_agenda: itensAgenda })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Agenda salva com sucesso!');
            } else {
                alert('Erro ao salvar agenda: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Erro ao salvar agenda');
        });
    });
});