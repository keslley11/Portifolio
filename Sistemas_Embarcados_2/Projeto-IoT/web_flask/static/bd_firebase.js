main = () => {

    // Import the functions you need from the SDKs you need

    //import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js"; //API modular (https://firebase.google.com/docs/database/web/start?hl=pt-br#web-namespaced-api)
    //import firebase from "firebase/compat/app"; //API compat
    //import "firebase/compat/database";



    // TODO: Add SDKs for Firebase products that you want to use
    // https://firebase.google.com/docs/web/setup#available-libraries

    // Your web app's Firebase configuration
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

    //function sendFirebase(valor) { //problema: https://pt.stackoverflow.com/questions/26347/chamar-fun%C3%A7%C3%A3o-js-em-outro-arquivo-depend%C3%AAncia-entre-scripts-javascript

    //window.exibirModal = function () { // fail

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
    //export {sendFirebase};  //não da pra exportar :/


    //*/
    //===============================


    /*
        // Ler dados em tempo real
        database.ref('dados').on('value', (snapshot) => {
            const dados = snapshot.val();
            console.log(dados);
        });
    */
}