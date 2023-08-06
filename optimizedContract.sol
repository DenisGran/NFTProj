// SPDX-License-Identifier: MIT
//Coded by Denis
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract GGG is ERC721Enumerable, Ownable
{
    using Strings for uint256;

    uint256 public saleGiraffePrice = 0.05 ether;
    uint256 public presaleGiraffePrice = 0.032 ether;
    
    uint256 public currentGiraffeId = 100;
    uint256 public presaleDate = 1633104000;
    uint256 public saleDate = 1717580480;

    address payable public creator = payable( 0x2CA4570ff0cBa9655e4CaD7d3dBAB7600958b336 );

    constructor() ERC721( "Grumpy Giraffe Gang", "GGG" ) {}

    function mint(uint256 amountRequested) external payable
    {
        uint256 _currentGiraffeId = currentGiraffeId;
        if(_currentGiraffeId >= 211)
        {
            uint256 _saleDate = saleDate;
            require( block.timestamp >= _saleDate , "Sale has not started yet! :s" );
            require( msg.value == saleGiraffePrice * amountRequested, "Ether sent is not correct :s" );
        }
        else
        {
            require( block.timestamp >= presaleDate , "Presale has not started yet! :s" );
            require( msg.value == presaleGiraffePrice * amountRequested, "Ether sent is not correct :s" );
        }
        require( amountRequested > 0, "Invalid amount of giraffes requested :s" );
        require( _currentGiraffeId + amountRequested <= 10000, "Purchase would exceed max available giraffes :/ Please try a lower amount." );
        creator.transfer( msg.value );
        for( uint256 i = 1; i <= amountRequested; i++ )
        {
            _safeMint( msg.sender, _currentGiraffeId + i );
        }
        currentGiraffeId += amountRequested;
    }

    function changeSalePrice(uint256 newPrice) external onlyOwner
    {
        saleGiraffePrice = newPrice;
    }

    function changeSaleDate(uint256 newDate) external onlyOwner
    {
        saleDate = newDate;
    }

    function gift(uint256 amount, address[] memory recipients, uint256[] memory nftsIds) external onlyOwner
    {
        for( uint256 i = 0; i < amount; i++ )
        {
            _safeMint( recipients[i], nftsIds[i] );
        }
    }

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory)
    {
        return string( abi.encodePacked('https://mint.grumpygiraffegang.com/db/?id=', tokenId.toString()) );
    }

}