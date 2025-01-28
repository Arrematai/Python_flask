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
            <div class="col col-lg-3">
                <button type="button" id="buscar" onclick="searchWordKey(this)" disabled>Buscar</button>
                <button type="button" id="clear" class="btn btn-outline-secondary">Limpar</button>
            </div>
        </div>

        <div class="row">
            <div id="loader"></div>
            <div id="alert" class="alert alert-warning" role="alert" style="display: none;">
            </div>
        </div>

        <div class="row"><div id="resultados"></div></div>


    </div>
			

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <script>
        let resultFiltrados = []
        let resultNotFiltrados = []
        let filtred = false

        const wordKeyEl = document.getElementById("palavra_chave")
        const content = document.querySelector("#resultados")
        const button = document.getElementById('buscar');
        const clearButton = document.getElementById('clear');

		var URL = "https://api.arremataisolucoes.com.br:5001"

        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('loader').style.display = 'block';
            getLeiloeiros().then(leiloeiros => {
                resultNotFiltrados = leiloeiros
                renderTableLeiloeiros(leiloeiros)

            }).finally(() => document.getElementById('loader').style.display = 'none')

            wordKeyEl.addEventListener("change", () => {
                button.removeAttribute('disabled');
                filtred = false

                if(!wordKeyEl.value || wordKeyEl.value === ""){
                    button.setAttribute('disabled', true);
                }

            })


            clearButton.addEventListener("click", () => {
                document.getElementById('loader').style.display = 'block';
                renderTableLeiloeiros(resultNotFiltrados)
                document.getElementById('loader').style.display = 'none'
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

        if(wordKeyEl.value){
            const response = await fetch(URL+'/leiloeiros/palavra/'+wordKeyEl.value);
            const result = await response.json();

            if(result && result.data.success){
                const [tipo, dados] = result.data.dados


                if(dados.length > 0){
                    resultFiltrados = dados
                    filtred = true
                    renderTableLeiloeiros(dados)
                }


                return dados
            }
        }




        el.setAttribute("disabled", "false")
    }



    function renderTableLeiloeiros(leiloeiros){

      if(!leiloeiros || leiloeiros.length === 0){
        return
      }

      // Remove todas as tabelas se tiver
      document.querySelectorAll("table").forEach(el => el.remove())


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


            
    </script>
    
</body>
</html>
		
		
    <?php
    return ob_get_clean(); // Retorna o conteúdo do buffer
}
add_shortcode('lista_leiloeiros_Rafael', 'lista_leiloeiros_shortcode_Rafael');
