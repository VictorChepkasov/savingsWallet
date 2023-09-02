import { ethers } from './node_modules/ethers/dist/ethers.js';

const responseSavingWallet = await fetch('../build/contracts/SavingWallet.json')
const abi = await responseSavingWallet.json()
const responseMap = await fetch('../build/deployments/map.json')
const mapJSON = await responseMap.json()

const contractAddress = mapJSON[Object.keys(mapJSON)[0]].WalletsFactory[0];
const provider = new ethers.BrowserProvider(window.ethereum);
const signer = provider.getSigner();
const walletsFactory = new ethers.Contract(contractAddress, JSON.stringify(abi.abi), signer);

export { walletsFactory };