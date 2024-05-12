const Investing = artifacts.require("Investing");

module.exports = function (deployer) {
  deployer.deploy(Investing);
};
