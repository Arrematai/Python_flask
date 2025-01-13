function fipe_veiculos_shortcode_Rafael() {
    ob_start(); 
    ?>
    <!DOCTYPE html>
<html lang="pt">
<head>
	<!-- Include base CSS (optional) -->
    <link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/choices.js/public/assets/styles/base.min.css"
/>
    <!-- Include Choices CSS -->
    <link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/choices.js/public/assets/styles/choices.min.css"
/>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
     /* Estilo básico */
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
            color: #404040,
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

			
		.content{
            max-width:1360px;
            display: flex;
    		flex-direction: column;
        }

        .form select{
            color: #404040;
            font-size: 15px;
            height: 45px;
        }

        .button-div{
            display: flex;
            justify-content: center;
            margin-top: 15px;
        }

         .button-div #pesquisar_fipe{
            margin-right: 8px;
         }

        .card-container{
            margin-top: 36px;
            padding: 16px;
            border: 1px solid #D9D9DA;
            border-radius: 8px;
            color: #404040;
            width: 50%;
        }

        .card-container .chave_valor{
            display: flex;
            height: 35px;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            border-bottom: 1px solid #D9D9DA;
            padding-left: 5px;
            padding-right: 16px;
        }

        .card-container .chave_valor.final{
            background: var(--wp--preset--color--primary);
            font-size: 16px;
            height: 45px;
        }

        .card-container .chave_valor .chave{
            font-weight: bold;
        }

        .card-container .chave_valor .valor{
            
        }

        /**choice */
        .choices[data-type*=select-one] .choices__input{
            color: #404040;
        }
        .choices__item{
            color: #404040;
        }
        .choices__item--selectable{
            color: #303030;
        }

        .choices__list--single .choices__item{
            color: #404040;
        }

        .is-open .choices__list--dropdown, .is-open .choices__list[aria-expanded]{
            color: #404040;
        }

        .choices__list--single{
             color: #404040;
        }

        button:disabled {
            background-color: #ddd;
            color: #999;
            cursor: not-allowed;
        }
		
		/* Dispostivios Móveis */
		@media (max-width: 768px) {
			.card-container{
                margin-top: 36px;
                padding: 16px;
                border: 1px solid #D9D9DA;
                border-radius: 8px;
                color: #404040;
                width: 100%;
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
			<div class="form">
				<div class="marcas">
                    <label for="marcas">Marcas</label>
                    <select class="input-group padrao" name="marcas" id="marcas" required>
                        <option value="" disabled selected>Digite ou selecione a marca do veiculo</option>
                    </select>
				</div>
                <div class="modelos">
                    <label for="modelos">Modelos</label>
                    <select class="input-group padrao" name="modelos" id="modelos" required disabled>
                        <option value="" disabled selected>Digite ou selecione o modelo do veiculo</option>
                    </select>
				</div>
                <div class="anos">
                    <label for="anosmodelos">Anos Modelos</label>
                    <select class="input-group padrao" name="anosmodelos" id="anosmodelos" required disabled>
                        <option value="" disabled selected>Digite ou selecione o ano modelo do veiculo</option>
                    </select>
				</div>

                <div class="button-div">
                    <button id="pesquisar_fipe" disabled>PESQUISAR</button>
                    <button id="limpar_dados" disabled>LIMPAR PESQUISA</button>
                </div>
			</div>	

			<div class="main-content"> 
                <div id="loader"></div>
                <div id="result" class="card-container hidden">
                </div>
			</div>
		</div>

    <!-- Include Choices JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/choices.js/public/assets/scripts/choices.min.js"></script>
    <script>
		const URL = 'https://api.arremataisolucoes.com.br:5001/fipe'
        const selectMarcas = document.querySelector("#marcas")
        const selectModelos = document.querySelector("#modelos")
        const selectAnosModelos = document.querySelector("#anosmodelos")
        const buttonPesquisar = document.querySelector("#pesquisar_fipe")
        const buttonLimpar = document.querySelector("#limpar_dados")
        const divResult = document.querySelector("#result")
        const divLoader = document.querySelector("#loader")
        const choiceMarcas = new Choices(selectMarcas, {
                allowHTML: false,
                placeholder: true,
                removeItemButton: true,
                searchPlaceholderValue: 'Digite ou selecione a marca do veiculo',
                loadingText: 'Carregando Marcas...',
                noResultsText: 'Nem um resultado encontrado.',
                noChoicesText: 'Não foram encontradas marcas.',
            })
        const choiceModelos = new Choices(selectModelos, {
            allowHTML: false,
            placeholder: true,
            removeItemButton: true,
            searchPlaceholderValue: 'Digite ou selecione o modelo do veiculo',
            loadingText: 'Carregando Modelos...',
            noResultsText: 'Nem um resultado encontrado.',
            noChoicesText: 'Não foi encontrado modelos.',
        })
        const choiceAnosModelos = new Choices(selectAnosModelos, {
            allowHTML: false,
            placeholder: true,
            removeItemButton: true,
            searchPlaceholderValue: 'Digite ou selecione o ano modelo do veiculo',
            loadingText: 'Carregando anos dos modelos...',
            noResultsText: 'Nem um resultado encontrado.',
            noChoicesText: 'Não foi encontrado anos.',
        })
        let marcaId = undefined;
        let modeloId = undefined;
        let codigoAno = undefined;
        let resultFipe = undefined;

        document.addEventListener('DOMContentLoaded', () => {
            seedSelectMarcas()

            // change select marcas
            selectMarcas.addEventListener("change", () => {
                const value = selectMarcas.value

                if(value && value !== marcaId){
                    // reset valores
                    modeloId = undefined
                    codigoAno = undefined
                    selectModelos.value = undefined
                    selectAnosModelos.value = undefined
                    selectAnosModelos.setAttribute("disabled",true)
                    choiceModelos.clearStore();
                    choiceAnosModelos.clearStore();

                    // set
                    marcaId = selectMarcas.value
                    seedSelectModelos()
                    return;
                }

            })

            // change select modelos
            selectModelos.addEventListener("change", () => {
                const value = selectModelos.value

                if(value && value !== modeloId){
                    // reset valores
                    codigoAno = undefined
                    selectAnosModelos.value = undefined
                    selectAnosModelos.setAttribute("disabled",false)
                    choiceAnosModelos.clearStore();

                    // set
                    modeloId = selectModelos.value
                    seedSelectAnosModelos()
                    return;
                }
            })

            // change select anos
            selectAnosModelos.addEventListener("change", () => {
                if(selectAnosModelos.value){
                    codigoAno = selectAnosModelos.value
                    // habilita botao pesquisar
                    buttonPesquisar.removeAttribute("disabled")
                    return
                }
            })

            // Click Button Pesquisar
            buttonPesquisar.addEventListener("click", () => {
                loading(true)
                fetchFipe().then(result => {

                    if(result && result.data && result.data.success){
                        resultFipe = result.data.dados[0]
                        handleResult()
                    }
                }).finally(() => loading(false));
            })


            buttonLimpar.addEventListener("click", () => {
                let marcaId = undefined;
                let modeloId = undefined;
                let codigoAno = undefined;
                let resultFipe = undefined;
                selectAnosModelos.value = ""
                selectModelos.value = ""
                selectMarcas.value = ""
                choiceMarcas.removeActiveItems(); // Remove item selecionado
                choiceModelos.clearStore(); // remove todos os elementos
                choiceAnosModelos.clearStore(); // remove todos os elementos
                buttonLimpar.setAttribute("disabled",true)
                buttonPesquisar.setAttribute("disabled",true)
            })

        });


        function loading(loading){
            if(loading){
                divLoader.style.display = 'block';
            }else{
                divLoader.style.display = 'none';
            }
        }



        async function fetchMarcas(){
            const response = await fetch(URL+'/marcas', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });

            const results = await response.json();
            return results;
        }

        async function fetchModelosByMarcaId(){
            const response = await fetch(URL+`/marcas/${marcaId}/modelos`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });

            const results = await response.json();
            return results;
        }

        async function fetchAnosModelosByModeloId(){
            const response = await fetch(URL+`/marcas/modelos/${modeloId}/anos`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });

            const results = await response.json();
            return results;
        }

        async function fetchFipe(){
            const response = await fetch(URL+`/marcas/${marcaId}/modelos/${modeloId}/anos/${codigoAno}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });

            const results = await response.json();
            return results;
        }


        function seedSelectMarcas(){
            choiceMarcas.setChoices(function() {

                return fetchMarcas().then(results => {

                    if(results && results.data && results.data.success){
                        //  {codigo: '1', id: 2, nome: 'Acura'}[]
                        return results.data.dados.map(function(marca) {
                            return { label: marca.nome, value: marca.id };
                        });
                    }

                    return []
                }).catch((error) => {
                    console.log(error)
                    return []
                })
            })
        }


        function seedSelectModelos(){
            choiceModelos.setChoices(function() {

                return fetchModelosByMarcaId().then(results => {

                    if(results && results.data && results.data.success){
                        //  {codigo: '1', id: 2, nome: 'Acura'}[]
                        console.log(results)
                        return results.data.dados.map(function(modelo) {
                            return { label: modelo.nome, value: modelo.id };
                        });
                    }

                    return []
                }).catch((error) => {
                    console.log(error)
                    return []
                })
            })
        }

        function seedSelectAnosModelos(){
            choiceAnosModelos.setChoices(function() {

                return fetchAnosModelosByModeloId().then(results => {

                    if(results && results.data && results.data.success){
                        return results.data.dados.map(function(modelo) {
                            return { label: modelo.nome, value: modelo.codigo };
                        });
                    }

                    return []
                }).catch((error) => {
                    console.log(error)
                    return []
                })
            })
        }


        function handleResult(){
            const options = { 
                weekday: 'long', 
                day: 'numeric', 
                month: 'long', 
                year: 'numeric', 
                hour: '2-digit', 
                minute: '2-digit' 
            };

            const now = new Date();
            const nowFormatted = now.toLocaleDateString('pt-BR', options);
            divResult.classList.remove("hidden")
            buttonLimpar.removeAttribute("disabled")

            if(!resultFipe) {
                divResult.innerHTML = `<h4>Nem um resultado encontrado.</h4>`
                return
            }

            divResult.innerHTML = `
                <div class="chave_valor">
                    <div class="chave">Mês de referência</div>
                    <div class="valor">${resultFipe.MesReferencia}</div>
                </div>
                    <div class="chave_valor">
                    <div class="chave">Código Fipe</div>
                    <div class="valor">${resultFipe.CodigoFipe}</div>
                </div>
                <div class="chave_valor">
                    <div class="chave">Marca</div>
                    <div class="valor">${resultFipe.Marca}</div>
                </div>
                <div class="chave_valor">
                    <div class="chave">Modelo</div>
                    <div class="valor">${resultFipe.Modelo}</div>
                </div>
                <div class="chave_valor">
                    <div class="chave">Ano Modelo</div>
                    <div class="valor">${resultFipe.AnoModelo} ${resultFipe.Combustivel}</div>
                </div>
                <div class="chave_valor">
                    <div class="chave">Data Consulta</div>
                    <div class="valor">${nowFormatted}</div>
                </div>
                <div class="chave_valor final">
                    <div class="chave final" style="font-weight: bold;">Preço Médio</div>
                    <div class="valor final" style="font-weight: bold;">${resultFipe.Valor}</div>
                </div>
            `
        }



            
    </script>
    
</body>
</html>
		
		
    <?php
    return ob_get_clean(); // Retorna o conteúdo do buffer
}
add_shortcode('fipe_veiculos_Rafael', 'fipe_veiculos_shortcode_Rafael');
