const {ethers} = require("hardhat");
async function main() {    
    contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
    const MyContract = await ethers.getContractAt("MyNFT", contractAddress);   

    const tx = await MyContract.mintNFT("0x70997970c51812dc3a010c7d01b50e0d17dc79c8",'hducyperspace');
    console.log(tx);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });