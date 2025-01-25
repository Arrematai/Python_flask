function lista_leiloeiros_shortcode_Rafael() {
    ob_start(); 
    ?>
    <!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <style>
     /* Estilo básico */
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
        }
		body.no-scroll {
            overflow: hidden;
        }

                
        #loader {
            display: none;
            border: 8px solid #f3f3f3;
            border-top: 8px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        table{
            margin-top: 60px;
        }

        .sortable{
            cursor: pointer;
        }
        
        .sort-icon {
        margin-left: 5px;
        display: inline-block;
        }

        .asc::after {
        content: "▲"; /* Ícone para ordem ascendente */
        }

        .desc::after {
        content: "▼"; /* Ícone para ordem descendente */
        }

        input{
            color: #404040 !important
        }
	
    </style>
    </head>
<body>

    <div class="container">
        <div class="row">
            <div class="col">
                <input type="text" id="palavra_chave" placeholder="Digite o leiloeiro desejado." min="3" max="30">
            </div>
            <div class="col col-lg-2">
                <button id="buscar" onclick="searchWordKey(this)" disabled>Buscar</button>
            </div>
        </div>

        <div class="row">
            <div id="loader"></div>
        </div>

        <div class="row"><div id="resultados"></div></div>


    </div>
			

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <script>
        let allResults = []; // Guarda todos os resultados acumulados
		var URL = "https://api.arremataisolucoes.com.br:5001"

        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('loader').style.display = 'block';
            getLeiloeiros().then(leiloeiros => renderTableLeiloeiros(leiloeiros)).finally(() => document.getElementById('loader').style.display = 'none')

            const input = document.querySelector("#palavra_chave")

            input.addEventListener("change", () => {
            const button = document.getElementById('buscar');
            button.removeAttribute('disabled');

            if(!input.value || input.value === ""){
                button.setAttribute('disabled', true);
            }

            })
        });

    async function getLeiloeiros(){
        const response = await fetch(URL+'/leiloeiros');
        const result = await response.json();

        if(result && result.data.success){
          return result.data.dados
        }

        return []
    }

    async function getLeiloeirosByFilter(){
        const response = await fetch(URL+'/leiloeiros');
        const result = await response.json();

        if(result && result.data.success){
          return result.data.dados
        }

        return []
    }


    async function searchWordKey(el){
        el.setAttribute("disabled", "true")

        wordKeyEl = document.getElementById("palavra_chave")


        if(wordKeyEl.value){
            const response = await fetch(URL+'/leiloeiros/'+wordKeyEl.value);
            const result = await response.json();

            if(result && result.data.success){
                console.log(result.data.dados)
                return result.data.dados
            }
        }




        el.setAttribute("disabled", "false")
    }



    function renderTableLeiloeiros(leiloeiros){

      if(!leiloeiros || leiloeiros.length === 0){
        return
      }


      const content = document.querySelector("#resultados")


      const table = document.createElement("table")
      table.setAttribute("id", "sortableTable")
      table.setAttribute("data-order", "asc")
      table.classList.add("table")
      table.classList.add("table-striped")
      table.classList.add("table-hover")
      table.classList.add("table-responsive")
      const thead = document.createElement("thead");
      const tbody = document.createElement("tbody");
      thead.innerHTML = `
          <tr>
            <th onclick="sortTable(this, 0)" scope="col" class="sortable desc">Nome</th>
            <th onclick="sortTable(this, 1)" scope="col" class="sortable">Email</th>
            <th onclick="sortTable(this, 2)" scope="col" class="sortable">Site</th>
            <th onclick="sortTable(this, 3)" scope="col" class="sortable">Estado</th>
            <th scope="col">Confiavel</th>
            <th scope="col">Status</th>
          </tr>
      `

      leiloeiros.map(leiloeiro => tbody.innerHTML += `
          <tr>
            <th scope="row">${leiloeiro.nome.trim()}</th>
            <td>${leiloeiro.email.trim()}</td>
            <td><a target="_blank" href="https://${leiloeiro.site.trim().toLowerCase()}">${leiloeiro.site.trim().toLowerCase()}</a></td>
            <td>${leiloeiro.estado}</td>
            <td>${leiloeiro.confiavel ? '<span class="badge text-bg-primary">Confiável</span>' : '<span class="badge text-bg-warning">Perigoso</span>'}</td>
            <td>${leiloeiro.status_site ? '<span class="badge text-bg-success">Online</span>' : '<span class="badge text-bg-danger">Offline</span>'}</td>
          </tr>
      `)

      table.appendChild(thead)
      table.appendChild(tbody)
      content.appendChild(table)


    }


    function sortTable(el, columnIndex) {
        const table = document.getElementById("sortableTable");
        const headers = table.querySelectorAll("thead th.sortable");

        const isAsc = el.classList.contains("asc");

        console.log("isAsc", isAsc)

        // Remove as classes "asc" e "desc" de todos os cabeçalhos
        headers.forEach(h => h.classList.remove("asc", "desc"));


        const rows = Array.from(table.rows).slice(1); // Exclui o cabeçalho

        console.log("rows", rows.length)

        rows.sort((a, b) => {
            const cellA = a.cells[columnIndex].textContent.trim().toLowerCase();
            const cellB = b.cells[columnIndex].textContent.trim().toLowerCase();


            if(!isAsc){
                // Verifica se é numérico
                return isNaN(cellA) || isNaN(cellB)
                    ? cellA.localeCompare(cellB) // Comparação alfabética
                    : cellA - cellB; // Comparação numérica
            }else if(isAsc){
                return isNaN(cellA) || isNaN(cellB)
                    ? cellB.localeCompare(cellA) // Comparação alfabética
                    : cellB - cellA; // Comparação numérica
            }


        });

        console.log(rows)

        // Reorganiza as linhas na tabela
        rows.forEach(row => table.tBodies[0].appendChild(row));
        
        // Atualiza a ordem do cabeçalho
        el.classList.toggle("asc", !isAsc);
        el.classList.toggle("desc", isAsc);
      

    }

    
    //   async function fetchResults() {
    //     const button = document.getElementById('buscar');
    //     button.setAttribute('disabled',true);
    //     const cardsContainer = document.getElementById('resultsCards');
    //     cardsContainer.innerHTML = '';
    //     allResults = []; // Limpa os resultados anteriores

    //     const query = document.getElementById('queryInput').value;
    //     document.getElementById('loader').style.display = 'block';

    //     try {
    //         const result = await fetch(URL+'/apis');
    //         const arrays = await result.json();

    //         await Promise.all(arrays.apis.map(async (api) => {
    //             const response = await fetch(URL+'/search', {
    //                 method: 'POST',
    //                 headers: { 'Content-Type': 'application/json' },
    //                 body: JSON.stringify({ query: query, api })
    //             });

    //             const results = await response.json();
	// 			console.log(`Resultados: ${results.length} na api ${api} com a query ${query}`)
	// 			if(results && results.length > 0){
	// 				allResults = [...allResults, ...results]; // Acumula resultados
	// 			}
                
    //             populateFilters(allResults); // Atualiza filtros dinamicamente
    //             populateCards(results, cardsContainer); // Renderiza novos cards
    //             document.getElementById('resultados').innerText = `${allResults.length} resultados encontrados.`
    //         }));

    //         document.getElementById('loader').style.display = 'none';
    //     } catch (error) {
    //       console.error("Erro ao buscar os dados:", error);
    //       document.getElementById('loader').style.display = 'none';
    //     } finally {
    //       button.removeAttribute("disabled")
    //     }
    //   }

 
			

        // function populateCards(results, cardsContainer) {
        //     results.forEach(item => {
        //         const card = document.createElement('div');
        //         card.className = 'card';
        //         card.onclick = () => window.open(item.link, '_blank');

        //         card.innerHTML = `
        //             <img src="${item.thumb}" alt="Imagem">
        //             <div class="card-header">
        //                 <p><strong>Lote:</strong> ${item.lote} <span>${item.leiloeiro}</span></p>
        //             </div>
        //             <div class="card-body">
        //                 <p>${item.marca} ${item.modelo} - Ano ${item.ano}</p>
        //                 <p>${item.monta}</p>
        //             </div>
        //             <div class="card-footer">
        //                 <div class="card-status">ABERTO PARA LANCES</div>
        //             </div>
        //         `;
        //         cardsContainer.appendChild(card);
        //     });
        // }

        // function populateFilters(results) {
        //     const filters = {
        //         model: document.getElementById('modelFilter'),
        //         monta: document.getElementById('montaFilter'),
        //         leiloeiro: document.getElementById('leiloeiroFilter')
        //     };

        //     const uniqueValues = {
        //         model: [...new Set(results.map(item => item.modelo))],
        //         monta: [...new Set(results.map(item => item.monta))],
        //         leiloeiro: [...new Set(results.map(item => item.leiloeiro))]
        //     };

        //     Object.keys(filters).forEach(key => {
        //         filters[key].innerHTML = ''; // Limpa filtros
        //         uniqueValues[key].forEach(value => {
        //             let qnt = ""
        //             const checkbox = document.createElement('input');
        //             checkbox.type = 'checkbox';
        //             checkbox.value = value;
        //             checkbox.onchange = applyFilters;

        //             if(key === "leiloeiro" || key === "monta"){
        //                 qnt = allResults.filter(e => e[key] === value)
        //                 console.log(qnt, value)
        //                 const label = document.createElement('label');
        //                 label.appendChild(checkbox);
        //                 label.append(value + ` (${qnt.length})`);
        //                 filters[key].appendChild(label);
        //             }else{
        //                 const label = document.createElement('label');
        //                 label.appendChild(checkbox);
        //                 label.append(value);
        //                 filters[key].appendChild(label);
        //             }

        //         });
        //     });
        // }

        // function applyFilters() {
        //     const selected = {
        //         model: [...document.querySelectorAll('#modelFilter input:checked')].map(c => c.value),
        //         monta: [...document.querySelectorAll('#montaFilter input:checked')].map(c => c.value),
        //         leiloeiro: [...document.querySelectorAll('#leiloeiroFilter input:checked')].map(c => c.value)
        //     };

        //     const filteredResults = allResults.filter(item =>
        //         (selected.model.length === 0 || selected.model.includes(item.modelo)) &&
        //         (selected.monta.length === 0 || selected.monta.includes(item.monta)) &&
        //         (selected.leiloeiro.length === 0 || selected.leiloeiro.includes(item.leiloeiro))
        //     );

        //     const cardsContainer = document.getElementById('resultsCards');
        //     cardsContainer.innerHTML = '';

             
        //     populateCards(filteredResults, cardsContainer);
        
        // }
	
        // //Functions para filtro móvel

        //         // Função para abrir os filtros no modal
        // function openMobileFilters() {
        //     const overlay = document.getElementById('mobileFiltersOverlay');
        //     const content = document.querySelector('.mobile-filters-content');

        //     overlay.style.display = 'flex'; // Mostra o overlay
        //     content.style.display = 'block'; // Mostra o conteúdo dos filtros
        //     document.body.classList.add('no-scroll'); // Desativa a rolagem do body

        //     populateMobileFilters();
        // }

        // // Função para fechar o modal e aplicar os filtros
        // function confirmMobileFilters() {
        //     const overlay = document.getElementById('mobileFiltersOverlay');
        //     const content = document.querySelector('.mobile-filters-content');

        //     overlay.style.display = 'none'; // Oculta o overlay
        //     content.style.display = 'none'; // Oculta o conteúdo dos filtros
        //     document.body.classList.remove('no-scroll'); // Reativa a rolagem do body

        //     applyMobileFilters();
        // }

        // // Preenche os filtros no modal
        // function populateMobileFilters() {
        //     const filters = {
        //         model: document.getElementById('mobileModelFilter'),
        //         monta: document.getElementById('mobileMontaFilter'),
        //         leiloeiro: document.getElementById('mobileLeiloeiroFilter')
        //     };

        //     const uniqueValues = {
        //         model: [...new Set(allResults.map(item => item.modelo))],
        //         monta: [...new Set(allResults.map(item => item.monta))],
        //         leiloeiro: [...new Set(allResults.map(item => item.leiloeiro))]
        //     };

        //     Object.keys(filters).forEach(key => {
        //         filters[key].innerHTML = ''; // Limpa filtros
        //         uniqueValues[key].forEach(value => {
        //             const checkbox = document.createElement('input');
        //             checkbox.type = 'checkbox';
        //             checkbox.value = value;
        //             checkbox.name = `mobile-${key}`;

        //             const label = document.createElement('label');
        //             label.appendChild(checkbox);
        //             label.append(value);

        //             filters[key].appendChild(label);
        //         });
        //     });
        // }

        // // Aplica os filtros selecionados no modal
        // function applyMobileFilters() {
        //     const selected = {
        //         model: [...document.querySelectorAll('#mobileModelFilter input:checked')].map(c => c.value),
        //         monta: [...document.querySelectorAll('#mobileMontaFilter input:checked')].map(c => c.value),
        //         leiloeiro: [...document.querySelectorAll('#mobileLeiloeiroFilter input:checked')].map(c => c.value)
        //     };

        //     const filteredResults = allResults.filter(item =>
        //         (selected.model.length === 0 || selected.model.includes(item.modelo)) &&
        //         (selected.monta.length === 0 || selected.monta.includes(item.monta)) &&
        //         (selected.leiloeiro.length === 0 || selected.leiloeiro.includes(item.leiloeiro))
        //     );

        //     const cardsContainer = document.getElementById('resultsCards');
        //     cardsContainer.innerHTML = '';

        //     populateCards(filteredResults, cardsContainer);
        // }

        // //Limpa Filtros Aplicados
        // // Função para limpar os filtros no mobile
        // function clearMobileFilters() {
        //     // Desmarca todas as checkboxes no modal
        //     document.querySelectorAll('.mobile-filters-content input[type="checkbox"]').forEach(checkbox => {
        //         checkbox.checked = false;
        //     });

        //     // Aplica os filtros no modal com tudo desmarcado
        //     applyMobileFilters();
        // }
            
    </script>
    
</body>
</html>
		
		
    <?php
    return ob_get_clean(); // Retorna o conteúdo do buffer
}
add_shortcode('lista_leiloeiros_Rafael', 'lista_leiloeiros_shortcode_Rafael');
