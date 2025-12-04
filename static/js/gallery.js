document.addEventListener('DOMContentLoaded', function() {
    const selectElement = document.getElementById('mounth');

    // Criar estrutura do select customizado
    const selectWrapper = document.createElement('div');
    selectWrapper.className = 'select';

    const selectStyled = document.createElement('div');
    selectStyled.className = 'select-styled';
    selectStyled.textContent = 'Escolha quem você deseja substituir';

    const selectOptions = document.createElement('ul');
    selectOptions.className = 'select-options';

    // Adicionar opções baseadas no select original
    Array.from(selectElement.options).forEach(option => {
        const li = document.createElement('li');
        li.textContent = option.textContent;
        li.setAttribute('data-value', option.value);

        if (option.value === 'hide') {
            li.setAttribute('rel', 'hide');
        }

        li.addEventListener('click', function() {
            selectStyled.textContent = this.textContent;
            selectElement.value = this.getAttribute('data-value');
            selectStyled.classList.remove('active');
            selectOptions.style.display = 'none';

            // Disparar evento change no select original
            const event = new Event('change', { bubbles: true });
            selectElement.dispatchEvent(event);
        });

        selectOptions.appendChild(li);
    });

    // Adicionar eventos de clique
    selectStyled.addEventListener('click', function(e) {
        e.stopPropagation();
        selectStyled.classList.toggle('active');
        selectOptions.style.display = selectOptions.style.display === 'block' ? 'none' : 'block';
    });

    // Fechar select quando clicar fora
    document.addEventListener('click', function() {
        selectStyled.classList.remove('active');
        selectOptions.style.display = 'none';
    });

    // Montar estrutura
    selectWrapper.appendChild(selectStyled);
    selectWrapper.appendChild(selectOptions);
    selectElement.parentNode.insertBefore(selectWrapper, selectElement);
    selectElement.classList.add('select-hidden');
});