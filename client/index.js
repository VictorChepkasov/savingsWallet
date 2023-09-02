import { walletsFactory } from "./helpers.js"

// Получаем элементы из вёрстки
const connect = document.getElementById("connectBtn");
const createSavingWallet = document.getElementById("btnCreateWallet");

// Над объектом ethereum внутри объекта окна при каждой загрузке проверяется, установлен ​​ли метамаск. Если метамаск не установлен, предупреждаем пользователя о необходимости его установки
function init() {
    if (typeof window.ethereum !== "undefined") {
        console.log("MetaMask is installed!");
    } else {
        alert("Please install Meta Mask");
    }
}

createSavingWallet.onclick = (event) => {
    event.preventDefault();
    const partyB = document.getElementById('partyB').value
    const amount = document.getElementById('amount').value
    console.log(partyB, amount)

    try {
        // await 
    } catch (error) {
        console.log("Saving wallet not create!", error);
    }
}

// Подключение к метамаск
connect.onclick = async () => {
    try {
        await ethereum.request({method: "eth_requestAccounts"});
        connect.innerHTML = "Connected";
    } catch (error) {
        console.log("Couldn't get a wallet connection", error);
    }
};

window.addEventListener("load", () => {
    init();
});
