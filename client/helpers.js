import { ethers } from './node_modules/ethers/dist/ethers.js';

//node_modules/ethers/dist/ethers.js

const responseSavingWallet = await fetch('../build/contracts/WalletsFactory.json');
const abi = await responseSavingWallet.json();
const responseMap = await fetch('../build/deployments/map.json');
const mapJSON = await responseMap.json();

const wethFactoryAddress = await mapJSON[Object.keys(mapJSON)[0]].WETHFactory[0];
const contractAddress = mapJSON[Object.keys(mapJSON)[0]].WalletsFactory[0];
const provider = new ethers.BrowserProvider(window.ethereum);
const signer = await provider.getSigner();
const walletsFactory = await new ethers.Contract(contractAddress, JSON.stringify(abi.abi), signer);

export { walletsFactory, signer, wethFactoryAddress };