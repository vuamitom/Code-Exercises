/* test script */
const fs = require('fs');
// load abi
const contractABI = JSON.parse(fs.readFileSync('./build/contracts/KyberNetwork.json', {flag: 'r', encoding: 'utf-8'}))['abi'];
// console.log(contractABI)
// https://developer.kyber.network/docs/NetworksAppendix#kybernetwork
// https://developer.kyber.network/docs/TokensAppendix#ether-eth
const contractAddress = '0x91a502C678605fbCe581eae053319747482276b9'
const eth_add ='0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
const knc_add ='0xdd974D5C2e2928deA5F71b9825b8b646686BD200'

var web3 = require('web3');
var web3_provider = 'https://mainnet.infura.io/v3/29e29451bfe54bb2a83df3944bbff78a';
var web3_port = '8545';
var _web3 = new web3();
_web3.setProvider(new web3.providers.HttpProvider(`${web3_provider}`));


_web3.eth.getBlock(48  , function(error, result){
    if(!error)
        console.log(JSON.stringify(result));
    else
        console.error(error);


    const contract = new _web3.eth.Contract(contractABI, contractAddress, {
      from: '0x13f126aDc69609FfA4B8acBa58b74cB48a034923'
    });
    // const contractInstance = contract.at();
    // console.log(contract);
    contract.methods.getExpectedRate(eth_add, knc_add, 1).call({}, function(err, result) {
      console.log(err);
      console.log(result);
    })
})

