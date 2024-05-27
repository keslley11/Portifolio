var vez = 1;

main = () => {
    const socket = new WebSocket('ws://192.168.142.220:81/'); // IP da ESP32

    //=====================================================================================
    //============= Botão Led (teste de conexão) =========================================
    //=====================================================================================

    function enviarComando(comando) {
        socket.send(comando);
    }

    document.getElementById('vent').addEventListener('click', function () {
        if (vez == 1) {
            socket.send('ligar');
            vez = 2;
        }
        else {
            socket.send('desligar');
            vez = 1;
        }
    });

    document.addEventListener('DOMContentLoaded', function () {
        const buttons = document.querySelectorAll('button');

        buttons.forEach(button => {
            button.addEventListener('touchstart', function () {
                const command = this.getAttribute('data-command');
                enviarComando(command);
            });

            button.addEventListener('touchend', function () {
                enviarComando('apaga');
            });

            button.addEventListener('mousedown', function () {
                const command = this.getAttribute('data-command');
                enviarComando(command);
            });

            button.addEventListener('mouseup', function () {
                enviarComando('apaga');
            });
        });
    });

    //=====================================================================================
    //=============  Firebase  =========================================
    //=====================================================================================


    const firebaseConfig = {
        apiKey: "AIzaSyCANViYls5wjQWClI8ZX8yShFPnrQHDafU",
        authDomain: "temp-semb2.firebaseapp.com",
        databaseURL: "https://temp-semb2-default-rtdb.firebaseio.com",
        projectId: "temp-semb2",
        storageBucket: "temp-semb2.appspot.com",
        messagingSenderId: "232172842431",
        appId: "1:232172842431:web:cd505d97e454b1f406850a"
    };
    //link Hospedagem Firebase:
    //  https://temp-semb2.web.app/
    //  https://temp-semb2.firebaseapp.com/


    // Inicializar o Firebase
    firebase.initializeApp(firebaseConfig); //versão namespace compat
    //const app = initializeApp(firebaseConfig); //versão do firebase (modular)



    //versão namespace compat
    //===============================
    ///*
    // Acessar o Realtime Database
    const database = firebase.database();


    function sendFirebase(valor) {
        // Enviar mensagem recebida para o Firebase Realtime Database
        const timestamp = new Date().toISOString();
        const mensagem = {
            timestamp: timestamp,
            comando: valor
        };
        // Armazenar mensagem no Firebase
        database.ref('mensagens').push(mensagem)
            .then(() => {
                console.log('Mensagem enviada para o Firebase:', mensagem);
            })
            .catch((error) => {
                console.error('Erro ao enviar mensagem para o Firebase:', error);
            });

    }

    //=====================================================================================
    //============= receber valores da ESP32 ================================================
    //=====================================================================================

    const tempElement = document.getElementById('lida');
    const sp = document.getElementById("desejada");
    const duty = document.getElementById("duty");

    // Conexão bem sucedida
    socket.onopen = function (event) {
        console.log('Conexão estabelecida com o servidor WebSocket');

        // Configurando um intervalo para enviar requisições a cada 1 segundo
        setInterval(function () {
            // Enviar uma mensagem para solicitar o dado
            socket.send('temp'); // Envie uma mensagem para solicitar o dado
        }, 5000); // Intervalo de 5 segundo (5000 milissegundos)
    };

    // Recebendo mensagens do servidor WebSocket
    socket.onmessage = function (event) {
        console.log('Mensagem recebida do servidor:', event.data);
        const respostaServidor = event.data; // O valor recebido é o dado

        // Atualizar a variável na página HTML
        resposta = respostaServidor.split("|");

        tempElement.textContent = resposta[0]; // Atualiza o conteúdo do elemento HTML com o dado
        sp.textContent = resposta[1];
        duty.textContent = resposta[2];
        document.getElementById("vent").style.color = "rgba(255,0,0," + resposta[2] / 100 + ")";

        //String resposta = String(Temperatura)+"° |"+String(sp)+"° |"+String(duty_cycle*100/255);
        //String resposta = String(32)+"° |"+String(40)+"° |"+String(10);


        //envia para firebase
        //
        sendFirebase(respostaServidor);
        //teste1 --> fail
        /*
        window.addEventListener("load", function () {
            if (nome == "") { sendFirebase(respostaServidor); }
        });
        */
        //teste2 -->fail
        /*
        $(document).ready(function () {
            sendFirebase(respostaServidor);
        });
        */


    };

    // Tratando erros de conexão
    socket.onerror = function (error) {
        console.error('Erro WebSocket:', error);
    };

    // Tratando o fechamento da conexão
    socket.onclose = function (event) {
        console.log('Conexão WebSocket fechada');
    };
}

window.addEventListener("load", main);