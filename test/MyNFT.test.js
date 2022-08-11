const { expect } = require("chai");

describe("MyCryptoLions", function () {
  it("Should return the right name and symbol", async function () {
    const MyCryptoLions = await hre.ethers.getContractFactory("MyNFT");
    const myCryptoLions = await MyCryptoLions.deploy();

    await myCryptoLions.deployed();
    expect(await myCryptoLions.name()).to.equal("MyNFT");
    expect(await myCryptoLions.symbol()).to.equal("NFT");
  });
});