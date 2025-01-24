function lista_leiloeiros_shortcode_Rafael() {
    ob_start(); 
    ?>
    <!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

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
      
	
    </style>
    </head>
<body>

    <div class="container">
        <div class="row">
            <div class="col">
                <input type="text" id="palavra_chave" placeholder="Digite o leiloeiro desejado.">
            </div>
            <div class="col col-lg-2">
                <button id="buscar" onclick="fetchResults()" disabled>Buscar</button>
            </div>
        </div>

        <div class="row">
            <div id="loader"></div>
        </div>

        <div class="row"><div id="resultados"></div></div>


    </div>
			

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <script>
        let allResults = []; // Guarda todos os resultados acumulados
		var URL = "https://api.arremataisolucoes.com.br:5001"

        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('loader').style.display = 'block';
            getLeiloeiros().then(leiloeiros => renderTableLeiloeiros(leiloeiros))

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
        const result = await fetch(URL+'/leiloeiros');
        const leiloeiros = await result.json();
        return leiloeiros
    }


    function renderTableLeiloeiros(leiloeiros){

      if(!leiloeiros || leiloeiros.length === 0){
        return
      }


      const content = document.querySelector("#resultados")


      const table = document.createElement("table")
      table.classList.add("table")
      table.appendChild(`
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">First</th>
            <th scope="col">Last</th>
            <th scope="col">Handle</th>
          </tr>
        </thead>
      `)

      table.appendChild(`
        <tbody>
          <tr>
            <th scope="row">1</th>
            <td>Mark</td>
            <td>Otto</td>
            <td>@mdo</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>Jacob</td>
            <td>Thornton</td>
            <td>@fat</td>
          </tr>
          <tr>
            <th scope="row">3</th>
            <td colspan="2">Larry the Bird</td>
            <td>@twitter</td>
          </tr>
        </tbody>
      `)


      content.appendChild(table)


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
