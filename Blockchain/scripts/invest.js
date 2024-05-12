const express = require('express');
const { Web3 } = require('web3');
const fs = require('fs');
const cors = require('cors'); 

const app = express();
const web3 = new Web3('http://localhost:7545');

app.use(express.json());
app.use(cors());



const abiFile = fs.readFileSync('D:/blockchain/build/contracts/Investing.json');
const abiJson = JSON.parse(abiFile);
const abi = abiJson.abi;
const contractAddress = '0x810672a5eE0E46F27Ca8b92E92F22e215d8dc88f'; 
const contract = new web3.eth.Contract(abi, contractAddress);

app.post('/register', async (req, res) => {
    const {startupName, expectedAmount} = req.body;
    const accounts = await web3.eth.getAccounts();

    await contract.methods.register(startupName, expectedAmount)
        .send({ from: accounts[0], gas: 2000000 })
        .on('receipt', function(receipt){
            console.log("Startup Registered. Receipt: " + receipt);
            const startupAddress = receipt.events.StartupRegistered.returnValues.owner;
            res.status(200).json({ startupAddress })
        })
        .on('error', function(error) {
            console.error("Registration failed:", error);
            res.status(500).send({ error: 'Registration failed' });
        });
});

app.post('/invest', async (req, res) => {
    const { startupAddress, investorName, amount } = req.body;
    const accounts = await web3.eth.getAccounts();

    await contract.methods.invest(startupAddress, investorName, amount)
        .send({ from: accounts[0], gas: 2000000 })
        .on('receipt', function(receipt){
            const receiptString = JSON.stringify(receipt, (key, value) =>
                typeof value === 'bigint' ? value.toString() : value
            );
            console.log("Receipt: " + receiptString);
            res.json(receiptString); 

        })
        .on('error', function(error) {
            console.error("Investment failed:", error);
            res.status(500).send({ error: 'Investment failed' });
        });
});



app.listen(3000, '192.168.21.231', () => {
    console.log('Server running on http://192.168.21.231:3000');
});

