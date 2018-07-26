/* test script */
const fs = require('fs');
// load abi
const BN = require('bn.js')
const pad = require('pad')
const kyberNetworkABI = JSON.parse(fs.readFileSync('./build/contracts/KyberNetwork.json', {flag: 'r', encoding: 'utf-8'}))['abi'];
const wrapperABI = JSON.parse(fs.readFileSync('./build/contracts/Wrapper.json', {flag: 'r', encoding: 'utf-8'}))['abi'];
// console.log(contractABI)
// https://developer.kyber.network/docs/NetworksAppendix#kybernetwork
// https://developer.kyber.network/docs/TokensAppendix#ether-eth
const kyberNetwrokAddress = '0x91a502C678605fbCe581eae053319747482276b9'
const wrapperAddress = '0x6172afc8c00c46e0d07ce3af203828198194620a'
const kyberNetworkProxy = '0x818E6FECD516Ecc3849DAf6845e3EC868087B755'
const eth_add ='0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
const knc_add ='0xdd974D5C2e2928deA5F71b9825b8b646686BD200'
const dai_add = '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359'
const omg_add = '0xd26114cd6EE289AccF82350c8d8487fedB8A0C07'
const mana_add = '0x0f5d2fb29fb7d3cfee444a200298f468908cc942'
const enig_add = '0xf0ee6b27b759c9893ce4f094b49ad28fd15a23e4'
var web3 = require('web3');
var web3_provider = 'https://mainnet.infura.io/v3/29e29451bfe54bb2a83df3944bbff78a';
var web3_port = '8545';
var _web3 = new web3();
_web3.setProvider(new web3.providers.HttpProvider(`${web3_provider}`));


// function pad(str, len) {
//   if (str.length < len) {
//     return ' ' * (len - str.length) + str;
//   }
//   return str;
// }
  
function trans(add) {
  if (add === eth_add)
    return 'ETH';
  if (add === knc_add)
    return 'KNC';
  if (add === omg_add)
    return 'OMG';
  if (add === dai_add)
    return "DAI";
  if (add === mana_add)
    return 'MANA'
  if (add === enig_add)
    return 'ENG'
}

function printResult(result, qty, src, dest) {
  let expectedrates = result[0],
    sliprate = result[1];
  console.log(result);
  for (let i = 0; i < qty.length; i++) {

    let o = []
    let v = qty[i] + ''
    v = pad(v, 6)
    o.push(v)
    // if (i < 5) {
    //   o.push('ETH -> KNC')
    // }
    // else {
    //   o.push('KNC -> ETH')
    // }
    o.push(trans(src[i]));
    o.push('->')
    o.push(trans(dest[i]));
    o.push(pad(expectedrates[i], 20))
    o.push(pad(sliprate[i], 20))
    console.log(o.join(' '))
  }
}

function printResult2(rs, src,dest, qty) {
  let o = []
  let v = qty + ''
  v = pad(v, 6)
  o.push(v)
  // if (i < 5) {
  //   o.push('ETH -> KNC')
  // }
  // else {
  //   o.push('KNC -> ETH')
  // }
  o.push(trans(src));
  o.push('->')
  o.push(trans(dest));
  o.push(pad(rs.expectedRate, 20))
  o.push(pad(rs.slippageRate, 20))
  console.log(o.join(' '))
}

_web3.eth.getBlock(48  , function(error, result){
    if(!error)
        console.log(JSON.stringify(result));
    else
        console.error(error);

    let start = new Date().getTime();
    const contract = new _web3.eth.Contract(wrapperABI, wrapperAddress, {
      from: '0x13f126aDc69609FfA4B8acBa58b74cB48a034923'
    });
    // const contractInstance = contract.at();
    // console.log(contract);
    let tokens = [knc_add, dai_add, omg_add, mana_add, enig_add],
      src = [],
      dest = [],
      qty = [];

    for (let i =0; i < tokens.length;i++) {
      // let src1 = [eth_add, eth_add, eth_add, eth_add, eth_add, knc_add, knc_add, knc_add, knc_add, knc_add],
      // dest1 = [knc_add, knc_add, knc_add, knc_add, knc_add, eth_add, eth_add, eth_add, eth_add, eth_add],
      let qty1 = [1, 5, 10, 50, 100, 490, 2000, 8000, 16000, 49000];
      let src1 = [], dest1 = [];
      for (let j = 0; j < 5; j++) {
        src1.push(eth_add);dest1.push(tokens[i]);
      }
      for (let j = 5; j <10;j++) {
        src1.push(tokens[i]); dest1.push(eth_add);
      }
      src = src.concat(src1);
      dest = dest.concat(dest1);
      qty = qty.concat(qty1);
    }

    // console.log(src)
    // console.log(dest)
    // for (let t = 0; t < 0; t++) {
    //   src =src.concat(src.slice());
    //   dest =dest.concat(dest.slice());
    //   qty =qty.concat(qty.slice());
    // }

    if (false) {
      console.log('Prepare data ' + src.length + ' pairs ' + (new Date().getTime() - start) + ' ms');
      start = new Date().getTime();
      var t = 0;
      let fn = (srcA, destA, qtyA) => {
        contract.methods.getExpectedRate(srcA, destA, (_web3.utils.toWei('' +qtyA, 'ether'))).call({}, function(err, result) {
          if (err)
          console.error(err);
          console.log(result); 
          printResult2(result, srcA, destA, qtyA);

          // console.log('Request return ' + (new Date().getTime() - start) + ' ms')
          start = new Date().getTime();
          t++;
          if (t < src.length) {
            fn(src[t], dest[t], qty[t]);
          }
          // printResult(result, qty, src, dest);
          // contract.methods.getExpectedRates('0x91a502C678605fbCe581eae053319747482276b9', src, dest, qty).call({}, (err, result) => {
          //   console.log('===================================================');
          //   printResult(result, qty, src, dest);

          //   contract.methods.getExpectedRates('0x91a502C678605fbCe581eae053319747482276b9', src, dest, qty).call({}, (err, result) => {
          //     console.log('===================================================');
          //     printResult(result, qty, src, dest);
          //   })
          // })
          
        })
      }
      fn (src[t], dest[t], qty[t]);
    }
    else {
      contract.methods.getExpectedRates(kyberNetwrokAddress, src, dest, 
        qty.map(q => _web3.utils.toWei('' + q, 'ether'))).call({}, function(err, result) {
        // console.log(result);
        if (err) console.error(err);
        printResult(result, qty, src, dest);
      })
    }
})

