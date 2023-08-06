# About
This is an NFT project I coded within a month. It is separated into 2 main parts:
1. **Art generation** - I used Python, successfully generating 10,000 unique art pieces with traits based on rarity.
2. **Smart contract** - I used solidity and ERC-721 standard for simplicity and efficiency.
  
## Background
In the holidays of September month, I was approached by a friend who pitched me the idea of NFTs and told me he has an idea for one.
<br>
So we took upon ourselves a challenge. To research and deploy an NFT within a month.
<br><br>
My friend was responsible for the art, I was responsible for the whole backend.
<br>
I began by trying to understand how NFTs work behind the scenes. As it was the most important aspect of the project, it took a long
time and a few failed attempts to understand it.
<br><br>
After this was done - I started working on a system to generate the art. **It was very important to make sure that there are
no duplicates** of NFTs!
<br>
And finally, I wrote a basic website in the time we had left.

## What is included in this repo?
* Art Generator
* Solidity Contract

## What is not included
* The art
* The website

## Art Generator
*Files: girrafegenerator.py, classes.py, raritygenerator.py, settings.py, nftsrarities.json, autosave.db*
<br><br>
The art of the project was of giraffes, therefore the word `giraffe` appears quite often in the code.
<br>
<br>
The idea for the art generator is to combine existing art pieces (traits) into one image, each image is completely unique and each trait has its own rarity.
<br><br>
Each trait had a predefined rarity (rare, common, uncommon, etc..) which was translated into numbers and saved in the settings file.
<br>
<br>
In order to maintain uniqueness, for each generated NFT I used MD5 hash to hash all the traits' names and save them in a DB. In case of a duplicate, it was re-generated.
<br>
<br>

## Smart Contract
*File: optimizedContract.sol*
<br><br>
In a nutshell: A smart contract is code that runs on the blockchain. Gas price is the price you pay in order to get your code up on the blockchain.
<br>
<br>
You can see that the filename is **`optimizedContract`** and that is because previously we had a different contract that we wanted to deploy, however, the gas price was very high!
<br>
<br>
In order to change that, I looked online for ways to reduce the gas price and found out that there are multiple gas optimization techniques and they are important. Here is a [link](https://www.alchemy.com/overviews/solidity-gas-optimization) to a great guide.
<br><br>
After minting an NFT, you can see the art (image) of the NFT you minted. In order to preserve the art for the future, I imported all the generated (10,000) NFTs to [IPFS](https://ipfs.tech) and saved their CID's in a DB.
<br><br>
