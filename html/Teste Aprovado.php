function busca_veiculos_shortcode_Rafael() {
    ob_start(); 
    ?>
    <!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
        .view-toggle {
            margin: 10px 0;
        }
        .buscaveiculos {
			margin: 10px 0;
			padding: 10px 20px;
			text-align: center;
			display: flex;
			gap: 32px;
		}
				
		
		.content{
            max-width:1360px;
            display: flex;
    		flex-direction: column;

        }
		
		.content .main-content {
			display: flex;
			flex: 1;
			margin-top: 20px; 
		}
		
		.search {
			flex: 1;
			margin-left: 20px;
		}

       
        
        .card {
            box-shadow: 5px 5px 15px #00000040;
            display: flex;
            flex-direction: column;
            border-radius: 10px;
            width: 100%;
            max-width: 280px;
            height: 500px;
            background: #fff;
            margin-right: 11px;
            overflow: hidden;
            text-align: center;
            box-sizing: border-box;
            margin-bottom:50px;

        }

        .h3{
            font-size: 1.2rem;
            line-height: 1;
            overflow: hidden;
        }


        .card img {
            width: 100%;
            height: 50%;
            object-fit: cover;
            flex-shrink: 0;
            display:block;
			cursor:pointer

        }
        
        .card-body {
            padding: 15px;
            font-size: 0.9rem;
            color: #333;
            text-align: left;
        }

        .card-footer {
            padding: 15px;
            background-color: #f8f9fa; /* Cinza claro */
            border-top: 1px solid #ddd;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-direction: column-reverse;
            margin-top: auto;

        }

        .card-footer .card-status {
            background-color: #28a745; /* Verde escuro */
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.9rem;
        }
        .card-body .card-owner {
            float: right;
            font-size: 0.8rem;
            color: white;
        }

        .card-header{
            background-color: #0056b3;
            color: white;
            width: 100%;
            text-align: left;
            box-sizing: border-box;
            font-size: 0.9rem;
            display: flex;
            padding-left: 10px;
            display: flex;
            justify-content: space-between;
        }

        .card-header p {
            margin: 0;
            margin-right: 10px;
        }

        .card-owner  {
            margin: 0;
            text-align: right;
        }
        #queryInput, #modelFilter, #montaFilter{
            color:black;
            }

        .card-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            align-items: flex-start; 
            margin: 0 auto;
            padding: 0;
            max-width: 100%;
            row-gap:30px;
        }
        
        /* Filtros */
        /* Sidebar  */
        .sidebar-filters {
            width: 250px;
            max-width: 20%;
            top: 60px; /* Espaço para o cabeçalho */
            left: 0;
            height: calc(100vh - 60px); /* Reduz altura do cabeçalho */
            background-color: #f8f9fa;
            border-right: 1px solid #ddd;
            overflow-y: auto;
            padding: 20px;
            box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
            position: sticky;
        }
       
        .sidebar-filters h3 {
            margin-top: 0;
            font-size: 1.2rem;
            margin-bottom: 15px;
        }

        .filter-group {
            margin-bottom: 20px;
        }

        .filter-group h4 {
            margin-bottom: 10px;
            font-size: 1rem;
            font-weight: bold;
        }

        .filter-group label {
            display: block;
            margin-bottom: 5px;
            font-size: 0.9rem;
        }

        .filter-group input[type="checkbox"] {
            margin-right: 10px;
        }
		
		/*Search Bar*/
		.search-bar {
			position: relative;
			margin: 0 auto;
			top: 6px; 
      right:2px;
			display: flex;
			flex-direction: row;
		}

				
		.search-bar button {
			transition: background-color 0.3s ease;
			display: flex;
			align-items: center;
			justify-content:center;
		}

		.search-bar button:hover {
			background-color: #004494;
		}
			
		.search-bar input {
			height:52px;
			width:570px;
		}

		/*Filtro Móvel*/
        /* Botão Filtros - Mobile */
        .filtersbtn{
            display: none;
            padding: 0px 20px;

        }
        .mobile-filters-btn {
            display: none;
            background-color: #0056b3;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;           
            top: 0;
            z-index: 100;
            width: 50%;
        }

        /* Overlay de Filtros - Tela Cheia */
        .mobile-filters-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 999;
            justify-content: center;
            align-items: center;
            overflow-y: auto;
        }

        .mobile-filters-content {
            background-color: white;
            width: 90%;
            max-width: 400px;
            max-height: 90vh; 
            overflow-y: auto; 
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            text-align: left;
            display: none;
        }

        .mobile-filters-content h3 {
            margin-bottom: 15px;
        }

        .filter-group {
            margin-bottom: 20px;
        }

        .filter-group h4 {
            margin-bottom: 10px;
        }

        .filter-group label {
            display: block;
            margin-bottom: 5px;
        }

        .mobile-filters-content button {
            display: block;
            width: 100%;
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
        }

        /* Botão Limpar Filtros */
        .clear-filters-btn {
            display: block;
            width: 50%;
            background-color: #dc3545; /* Cor vermelha para destaque */
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
            text-align: center;
            
        }

        .clear-filters-btn:hover {
            background-color: #c82333;
        }

		/* Dispostivios Móveis */
		@media (max-width: 768px) {
			.sidebar-filters {
				display:none; 
			}
			.buscaveiculos{
				flex-direction: column;
				gap: 20px;
				width:100%;			
			}
			.search-bar{
				margin:0;
			}
			.search-bar input{
				width:100%;
			}
			.mobile-filters-btn {
                display: block;
            }
            .filtersbtn{
                position: sticky;
                display: flex;
                
            }
			
			
			
		}

		/* Classe para ocultar elementos */
		.hidden {
			display: none;
		}
		


       
    </style>
    </head>
<body>
			
		<div class="content">
			<div class="search-bar">
				<div class="buscaveiculos">
					<input type="text" id="queryInput" placeholder="Digite a marca ou modelo desejado.">
					<button id="buscar" onclick="fetchResults()" disabled>Buscar</button>
				</div>
			</div>	
			
			 <div class="filtersbtn">
                <!-- Botão de Filtros para Mobile -->
                <button id="openFiltersBtn" class="mobile-filters-btn" onclick="openMobileFilters()">Filtros</button>
                <!-- Botão para Limpar Filtros - Mobile -->
                <button id="clearMobileFiltersBtn" class="clear-filters-btn" onclick="clearMobileFilters()">Limpar Filtros</button>
            </div>

            <!-- Overlay de Tela Cheia com Filtros -->
            <div id="mobileFiltersOverlay" class="mobile-filters-overlay">
                <div class="mobile-filters-content">
                    <h3>Filtros</h3>
                    
                    <div class="filter-group">
                        <h4>Leiloeiro</h4>
                        <div id="mobileLeiloeiroFilter"></div>
                    </div>

                    <div class="filter-group">
                        <h4>Monta</h4>
                        <div id="mobileMontaFilter"></div>
                    </div>

                    <div class="filter-group">
                        <h4>Modelo</h4>
                        <div id="mobileModelFilter"></div>
                    </div>

                    <button onclick="confirmMobileFilters()">Confirmar</button>
                </div>
            </div>

			<div class="main-content">
				<div class="sidebar-filters">
					<h3>Filtros</h3>
					<div class="filter-group">
						<h4>Leiloeiro</h4>
						<div id="leiloeiroFilter"></div>
					</div>
					<div class="filter-group">
						<h4>Monta</h4>
						<div id="montaFilter"></div>
					</div>
					<div class="filter-group">
						<h4>Modelo</h4>
						<div id="modelFilter"></div>
						
					</div>
				</div>

				<div class="search">
					<div id="loader"></div>
					<div id="resultados"></div>
					<div id="resultsCards" class="card-container"></div>
				</div>
			</div>
		</div>


    <script>
        let allResults = []; // Guarda todos os resultados acumulados
		var URL = "https://api.arremataisolucoes.com.br:5001"

        function getQuery(param){
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(param);
        }

        document.addEventListener('DOMContentLoaded', () => {
          const queryParam = getQuery('query');
          if (queryParam) {
              document.getElementById('queryInput').value = queryParam;
              fetchResults(); 
          }
        });

        const input = document.querySelector("#queryInput")

        input.addEventListener("change", () => {
          const button = document.getElementById('buscar');
          button.removeAttribute('disabled');

          if(!input.value || input.value === ""){
            button.setAttribute('disabled', true);
          }

        })


      async function fetchResults() {
        const button = document.getElementById('buscar');
        button.setAttribute('disabled',true);
        const cardsContainer = document.getElementById('resultsCards');
        cardsContainer.innerHTML = '';
        allResults = []; // Limpa os resultados anteriores

        const query = document.getElementById('queryInput').value;
        document.getElementById('loader').style.display = 'block';

        try {
            const result = await fetch(URL+'/apis');
            const arrays = await result.json();

            await Promise.all(arrays.apis.map(async (api) => {
                const response = await fetch(URL+'/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query, api })
					
                });
				

                const results = await response.json();
				
				console.log(`Resultados: ${results.length} na api ${api} com a query ${query}`)
				if(results && results.length > 0){
					allResults = [...allResults, ...results]; // Acumula resultados
				}
                
                populateFilters(allResults); // Atualiza filtros dinamicamente
                populateCards(results, cardsContainer); // Renderiza novos cards
                document.getElementById('resultados').innerText = `${allResults.length} resultados encontrados.`
            }));

            document.getElementById('loader').style.display = 'none';
        } catch (error) {
          console.error("Erro ao buscar os dados:", error);
          document.getElementById('loader').style.display = 'none';
        } finally {
          button.removeAttribute("disabled")
        }
      }
			

        function populateCards(results, cardsContainer) {
            results.forEach(item => {
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => window.open(item.link, '_blank');

                lote = item.lote ? `<strong>Lote:</strong> ${item.lote}` : ""

                card.innerHTML = `
                    <img loading="lazy" decoding="sync" src="${item.thumb}" alt="Imagem">
                    <div class="card-header">
                        <span>${item.leiloeiro}</span>  <p>${lote}</p>
                    </div>
                    <div class="card-body">
                        <p>${item.marca} ${item.modelo} - Ano ${item.ano}</p>
                        <p>${item.monta}</p>
                    </div>
                    <div class="card-footer">
                        <div class="card-status">ABERTO PARA LANCES</div>
                    </div>
                `;
                cardsContainer.appendChild(card);
            });
        }

        function populateFilters(results) {
            const filters = {
                model: document.getElementById('modelFilter'),
                monta: document.getElementById('montaFilter'),
                leiloeiro: document.getElementById('leiloeiroFilter')
            };

            const uniqueValues = {
                model: [...new Set(results.map(item => item.modelo))],
                monta: [...new Set(results.map(item => item.monta))],
                leiloeiro: [...new Set(results.map(item => item.leiloeiro))]
            };

            Object.keys(filters).forEach(key => {
                filters[key].innerHTML = ''; // Limpa filtros
                uniqueValues[key].forEach(value => {
                    let qnt = ""
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.value = value;
                    checkbox.onchange = applyFilters;

                    if(key === "leiloeiro" || key === "monta"){
                        qnt = allResults.filter(e => e[key] === value)
                        console.log(qnt, value)
                        const label = document.createElement('label');
                        label.appendChild(checkbox);
                        label.append(value + ` (${qnt.length})`);
                        filters[key].appendChild(label);
                    }else{
                        const label = document.createElement('label');
                        label.appendChild(checkbox);
                        label.append(value);
                        filters[key].appendChild(label);
                    }

                });
            });
        }

        function applyFilters() {
            const selected = {
                model: [...document.querySelectorAll('#modelFilter input:checked')].map(c => c.value),
                monta: [...document.querySelectorAll('#montaFilter input:checked')].map(c => c.value),
                leiloeiro: [...document.querySelectorAll('#leiloeiroFilter input:checked')].map(c => c.value)
            };

            const filteredResults = allResults.filter(item =>
                (selected.model.length === 0 || selected.model.includes(item.modelo)) &&
                (selected.monta.length === 0 || selected.monta.includes(item.monta)) &&
                (selected.leiloeiro.length === 0 || selected.leiloeiro.includes(item.leiloeiro))
            );

            const cardsContainer = document.getElementById('resultsCards');
            cardsContainer.innerHTML = '';

             
            populateCards(filteredResults, cardsContainer);
        
        }
	
        //Functions para filtro móvel

                // Função para abrir os filtros no modal
        function openMobileFilters() {
            const overlay = document.getElementById('mobileFiltersOverlay');
            const content = document.querySelector('.mobile-filters-content');

            overlay.style.display = 'flex'; // Mostra o overlay
            content.style.display = 'block'; // Mostra o conteúdo dos filtros
            document.body.classList.add('no-scroll'); // Desativa a rolagem do body

            populateMobileFilters();
        }

        // Função para fechar o modal e aplicar os filtros
        function confirmMobileFilters() {
            const overlay = document.getElementById('mobileFiltersOverlay');
            const content = document.querySelector('.mobile-filters-content');

            overlay.style.display = 'none'; // Oculta o overlay
            content.style.display = 'none'; // Oculta o conteúdo dos filtros
            document.body.classList.remove('no-scroll'); // Reativa a rolagem do body

            applyMobileFilters();
        }

        // Preenche os filtros no modal
        function populateMobileFilters() {
            const filters = {
                model: document.getElementById('mobileModelFilter'),
                monta: document.getElementById('mobileMontaFilter'),
                leiloeiro: document.getElementById('mobileLeiloeiroFilter')
            };

            const uniqueValues = {
                model: [...new Set(allResults.map(item => item.modelo))],
                monta: [...new Set(allResults.map(item => item.monta))],
                leiloeiro: [...new Set(allResults.map(item => item.leiloeiro))]
            };

            Object.keys(filters).forEach(key => {
                filters[key].innerHTML = ''; // Limpa filtros
                uniqueValues[key].forEach(value => {
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.value = value;
                    checkbox.name = `mobile-${key}`;

                    const label = document.createElement('label');
                    label.appendChild(checkbox);
                    label.append(value);

                    filters[key].appendChild(label);
                });
            });
        }

        // Aplica os filtros selecionados no modal
        function applyMobileFilters() {
            const selected = {
                model: [...document.querySelectorAll('#mobileModelFilter input:checked')].map(c => c.value),
                monta: [...document.querySelectorAll('#mobileMontaFilter input:checked')].map(c => c.value),
                leiloeiro: [...document.querySelectorAll('#mobileLeiloeiroFilter input:checked')].map(c => c.value)
            };

            const filteredResults = allResults.filter(item =>
                (selected.model.length === 0 || selected.model.includes(item.modelo)) &&
                (selected.monta.length === 0 || selected.monta.includes(item.monta)) &&
                (selected.leiloeiro.length === 0 || selected.leiloeiro.includes(item.leiloeiro))
            );

            const cardsContainer = document.getElementById('resultsCards');
            cardsContainer.innerHTML = '';

            populateCards(filteredResults, cardsContainer);
        }

        //Limpa Filtros Aplicados
        // Função para limpar os filtros no mobile
        function clearMobileFilters() {
            // Desmarca todas as checkboxes no modal
            document.querySelectorAll('.mobile-filters-content input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
            });

            // Aplica os filtros no modal com tudo desmarcado
            applyMobileFilters();
        }
            
    </script>
    
</body>
</html>
		
		
    <?php
    return ob_get_clean(); // Retorna o conteúdo do buffer
}
add_shortcode('busca_veiculos_Rafael', 'busca_veiculos_shortcode_Rafael');
