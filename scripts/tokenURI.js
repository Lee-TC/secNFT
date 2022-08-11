const {ethers} = require("hardhat");
async function main(tokenId) {  
    contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
    const MyContract = await ethers.getContractAt("MyNFT", contractAddress);   

    const result = await MyContract.tokenURI(tokenId);
    console.log(result);
}

main(tokenId)
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });