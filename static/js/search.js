document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search");
    const resultsContainer = document.getElementById("results");

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.trim();

        if (query.length > 0) {
            fetch(`/users/api/search-users/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    resultsContainer.innerHTML = ""; // Limpa os resultados anteriores

                    if (data.users.length === 0 && data.addresses.length === 0) {
                        resultsContainer.innerHTML = "<p>Nenhum usuário encontrado.</p>";
                        return;
                    }

                    // Exibir usuários encontrados
                    if (data.users.length > 0) {
                        const usersTitle = document.createElement("h3");
                        usersTitle.textContent = "Usuários encontrados:";
                        resultsContainer.appendChild(usersTitle);

                        data.users.forEach(user => {
                        const item = document.createElement("div");
                        item.innerHTML = `
                        <a href="/users/profile/${user.id}/" style="font-weight: bold;">
                            <div style="display: flex; align-items: center; margin-bottom: 10px;" class='sear-user'>
                            <img src="${user.image_url}" alt="Foto de ${user.username}" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;">
                            <div>
                                ${user.username}
                                <p style="margin: 0; font-size: 12px; color: gray;">${user.group}</p>
                                </div>
                            </div>
                        </a>
                    `;
                        resultsContainer.appendChild(item);
                    });
                    }

                    // Exibir endereços encontrados
                    if (data.addresses.length > 0) {
                        const addressesTitle = document.createElement("h3");
                        addressesTitle.textContent = "Endereços encontrados:";
                        resultsContainer.appendChild(addressesTitle);

                        data.addresses.forEach(address => {
                            const item = document.createElement("div");
                            item.textContent = `Nome: ${address.username} | Rua: ${address.rua} | Cidade: ${address.cidade}`;
                            resultsContainer.appendChild(item);
                        });
                    }
                })
                .catch(error => console.error("Erro na busca:", error));
        } else {
            resultsContainer.innerHTML = ""; // Esconde os resultados se o input estiver vazio
        }
    });
});