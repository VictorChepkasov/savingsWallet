import { walletsFactory, signer, wethFactoryAddress } from "./helpers.js";

// Получаем элементы из вёрстки
const connect = document.getElementById("connectBtn");
const createSavingWallet = document.getElementById("btnCreateWallet");
const accountMetamsk = document.getElementById("account")

// Над объектом ethereum внутри объекта окна при каждой загрузке проверяется, установлен ли метамаск. Если метамаск не установлен, предупреждаем пользователя о необходимости его установки
function init() {
    if (typeof window.ethereum !== "undefined") {
        console.log("MetaMask is installed!");
    } else {
        alert("Please install Meta Mask");
    }
}

createSavingWallet.onclick = async (event) => {
    event.preventDefault();
    const partyB = document.getElementById('partyB').value;
    const amount = document.getElementById('amount').value;
    console.log(partyB, amount);

    try {
        await walletsFactory.connect(signer)
        console.log(walletsFactory)
        await walletsFactory.createWallet(wethFactoryAddress, signer, partyB, amount);
    } catch (error) {
        await console.log("Saving wallet not create!", error);
    }
};

// Подключение к метамаск
connect.onclick = async () => {
    try {
        const conectedAccount = await window.ethereum.request({method: "eth_requestAccounts"});
        connect.innerHTML = "Connected";
        const activeChainId = await window.ethereum.request({ method: 'eth_chainId' });
        accountMetamsk.innerHTML = `Chain Id: ${activeChainId} <br/> Account: ${conectedAccount}`;
    } catch (error) {
        console.log("Couldn't get a wallet connection", error);
    }
};

window.addEventListener("load", () => {
    init();
});
