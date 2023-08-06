import settings

nft_rarities = settings.calc_nfts_rarities()
f = open('nftrarities.json', 'w')
f.write(str(nft_rarities))
f.close()
print(nft_rarities)

