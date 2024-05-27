main = () => {
	/*CRIANDO CLASSE DE COLETA DE DADOS*/
	class coleta {
		constructor(hora, estado, temperatura) {
			this.hora = hora;
			this.estado = estado;
			this.temperatura = temperatura;
		}
	}

	/*PEGANDO HTML*/
	desejada = document.getElementById('desejada');
	lida = document.getElementById('lida');
	duty = document.getElementById("duty");

	/*FUNÇÃO PARA INSERIR DADOS*/
	function inserirDados(objeto) {
		//PEGANDO HTML
		const hora = document.getElementById('horarios');
		const ventilador = document.getElementById('Ventilador');
		const temperatura = document.getElementById('Temperatura');

		//CONSTRUINDO ELEMENTO
		var novaHora = document.createElement("span");
		novaHora.innerHTML = objeto.hora;
		var novoEstado = document.createElement("span");
		novoEstado.innerHTML = objeto.estado;
		var novaTemperatura = document.createElement("span");
		novaTemperatura.innerHTML = objeto.temperatura;

		//ADICIONANDO AO HMTL
		hora.appendChild(novaHora);
		ventilador.appendChild(novoEstado);
		temperatura.appendChild(novaTemperatura);

	}

	/*DECLARANDO VETOR*/
	dados = [];

	/*INSERINDO DADOS*/
	novoValor = lida.textContent;
	novaHora = new Date().toLocaleTimeString();
	novoEstado = duty.textContent;
	dados.push(new coleta(novaHora, novoEstado, novoValor));

	/*CHAMANDO FUNÇÃO*/
	inserirDados(dados[0]);

	/*INICIANDO CONSTRUÇÃO DO GRAFICO*/
	am5.ready(function () {

		// Create root element
		var root = am5.Root.new("chartdiv");

		// Set themes (Inserindo temas)
		root.setThemes([
			am5themes_Animated.new(root)
		]);

		// Create chart
		// https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
		var chart = root.container.children.push(
			am5percent.PieChart.new(root, {
				startAngle: 160, endAngle: 380
			})
		);

		// Create serie 0
		// https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
		var series0 = chart.series.push(
			am5percent.PieSeries.new(root, {
				valueField: "litres",
				categoryField: "country",
				startAngle: 160,
				endAngle: 380,
				radius: am5.percent(70),
				innerRadius: am5.percent(65)
			})
		);

		/*INSERINDO CORES*/
		var colorSet = am5.ColorSet.new(root, {

			colors: [am5.color(0x481F67)],
			passOptions: {
				//lightness: -0.05,
				lightness: -10,
				hue: 0
			}
		});

		/*MUDANDO CORES E DEFININDO TEMPLATES*/
		series0.set("colors", colorSet);
		series0.ticks.template.set("forceHidden", true);
		series0.labels.template.set("forceHidden", true);

		/*CRIANDO SERIE 1*/
		var series1 = chart.series.push(
			am5percent.PieSeries.new(root, {
				startAngle: 160,
				endAngle: 380,
				valueField: "bottles",
				innerRadius: am5.percent(80),
				categoryField: "country"
			})
		);

		/*MUDANDO CORES E DEFININDO TEMPLATES*/
		series1.set("colors", colorSet);
		series1.ticks.template.set("forceHidden", true);
		series1.labels.template.set("forceHidden", true);

		/*criando container de texto*/
		var label = chart.seriesContainer.children.push(
			am5.Label.new(root, {
				textAlign: "center",
				centerY: am5.p100,
				centerX: am5.p50,
				text: "[fontSize:18px #fff]Temperatura:[/]" +
					"\n[bold fontSize:30px #fff]" + lida.textContent + "[/]"
			})
		);

		/*Alterando dados coletados*/
		var valor1 = (parseInt(lida.textContent) * 100) / parseInt(desejada.innerHTML);
		var valor2 = ((parseInt(desejada.innerHTML) - parseInt(lida.textContent)) * 100) / parseInt(desejada.innerHTML);

		var data = [
			{
				country: "Planta",
				litres: 0,
				bottles: valor1
			},
			{
				country: "Distancia",
				litres: 100,
				bottles: valor2
			}
		];

		// Set data (alterando dados)
		// https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
		series0.data.setAll(data);
		series1.data.setAll(data);

		/*FUNÇÃO PARA ALTERAR DADOS DO GRAFICO*/
		alterar = () => {
			/*LIMPANDO TELA ANTERIOR*/
			chart.seriesContainer.children.pop();

			/*CRIANDO NOVA TELA*/
			var label = chart.seriesContainer.children.push(
				am5.Label.new(root, {
					textAlign: "center",
					centerY: am5.p100,
					centerX: am5.p50,
					text: "[fontSize:18px #fff]Temperatura:[/]" +
						"\n[bold fontSize:30px #fff]" + lida.textContent + "[/]"
				})
			);

			/*ATUALIAZNDO DADOS*/
			//console.log(am5.Label.remove);
			var valor1 = (parseInt(lida.textContent) * 100) / parseInt(desejada.innerHTML);
			var valor2 = ((parseInt(desejada.innerHTML) - parseInt(lida.textContent)) * 100) / parseInt(desejada.innerHTML);

			//VERIFICANDO SE PASSOU DO VALOR
			execedente = 0;
			if (valor2 < 0) {
				execedente = valor2 * -1;
				valor2 = 0;
			}

			/*ATUALIZANDO GRAFICO*/
			var data = [
				{
					country: "Planta",
					litres: execedente,
					bottles: valor1
				},
				{
					country: "Distancia",
					litres: 100,
					bottles: valor2
				}
			];
			series0.data.setAll(data);
			series1.data.setAll(data);
		}

		// Função de callback a ser executada quando ocorrer uma mutação
		const callback = function (mutationsList, observer) {
			for (let mutation of mutationsList) {
				// Se houver uma mutação no conteúdo do span (inserção, remoção ou alteração de texto)
				if (mutation.type === 'childList'
					|| mutation.type === 'characterData') {
					// Aqui você pode executar qualquer ação desejada em resposta à alteração
					//Alterar dados do grafico
					alterar();

					/*Alterando dados coletados*/
					novoValor = lida.textContent;
					novaHora = new Date().toLocaleTimeString();
					novoEstado = duty.textContent + "%";
					novoDado = new coleta(novaHora, novoEstado, novoValor);
					dados.push(novoDado);

					/*Alterando historico*/
					inserirDados(novoDado);
				}
			}
		};

		// Cria um novo MutationObserver
		const observer = new MutationObserver(callback);

		// Configura o MutationObserver para observar alterações no conteúdo do span
		observer.observe(lida, { childList: true, characterData: true, subtree: true });
	}); // end am5.ready()
}

window.addEventListener("load", main);