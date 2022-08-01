import requests
import json

# How to use:
# Change the TO_SCRAPE dictionary to remove/add categories and brands. 
# format:
# <subdepartment url> : [<1st brand>, <2nd brand>]
# NOTE: subdepartment url should lead to a site containing item listings

GRAPHQL_PAGE_SIZE = 40  # Max number of items to retrieve from GQL in one request
GRAPHQL_MAX_START_INDEX = 720  # Max index that the GQL API supports

STORES = [
    '6177',  # Manhattan 59th Street, NY
    '0589'  # Lemmon Ave, TX
]

TO_SCRAPE = {
    'https://www.homedepot.com/b/Appliances-Dishwashers-Built-In-Dishwashers/N-5yc1vZc3nj': [
        'LG Electronics', # LG SIGNATURE and LG STUDIO have to be specified separately
        'Samsung'
    ],
    'https://www.homedepot.com/b/Appliances-Refrigerators/N-5yc1vZc3pi': [
        'Whirlpool',
        'GE' # GE Profile has to be specified separately
    ],
    'https://www.homedepot.com/b/Furniture-Bedroom-Furniture-Mattresses/N-5yc1vZc7oe': [
        'Sealy' 
    ]
}

HEADERS = {'accept': '*/*',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
           'apollographql-client-name': 'major-appliances',
           'apollographql-client-version': '0.0.0',
           'content-length': '9409',
           'content-type': 'application/json',
           'origin': 'https://www.homedepot.com',
           'referer': 'https://www.homedepot.com/b/Appliances-Refrigerators/N-5yc1vZc3pi?catStyle=ShowProducts&Nao=24',
           'sec-ch-ua': '"Chromium";v="102", "Opera GX";v="88", ";Not A Brand";v="99"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'same-origin',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.85',
           'x-api-cookies': '{"x-user-id":"b190e51a-da74-c10a-32c0-5d32ae23aad9"}',
           'x-current-url': '/b/Appliances-Refrigerators/N-5yc1vZc3pi',
           'x-debug': 'false',
           'x-experience-name': 'major-appliances',
           'x-hd-dc': 'origin'}


def generate_form_data(search_item_id: str, store_id: str, start_index: int) -> dict:
    """
    Separate out the generation of form data to make the main block of code more readable.

    Takes relevant arguments necessary to perform GraphQL query.
    """
    return {
        'operationName': 'searchModel',
        'variables': {
            'skipInstallServices': 'false',
            'skipKPF': 'false',
            'skipSpecificationGroup': 'false',
            'skipSubscribeAndSave': 'false',
            'storefilter': 'ALL',
            'channel': 'DESKTOP',
            'additionalSearchParams': {
                'sponsored': 'false',
                'mcvisId': "49585623440004146380324386480083213512",
                'plp': 'true',
                'deliveryZip': '04401'
            },
            'filter': {},
            'navParam': search_item_id,
            'orderBy': {
                'field': 'TOP_SELLERS',
                'order': 'ASC'
            },
            'pageSize': GRAPHQL_PAGE_SIZE,
            'startIndex': start_index,
            'storeId': store_id
        },
        'query': 'query searchModel($storeId: String, $zipCode: String, $skipInstallServices: Boolean = true, $startIndex: Int, $pageSize: Int, $orderBy: ProductSort, $filter: ProductFilter, $skipKPF: Boolean = false, $skipSpecificationGroup: Boolean = false, $skipSubscribeAndSave: Boolean = false, $keyword: String, $navParam: String, $storefilter: StoreFilter = ALL, $itemIds: [String], $channel: Channel = DESKTOP, $additionalSearchParams: AdditionalParams, $loyaltyMembershipInput: LoyaltyMembershipInput) {\n  searchModel(keyword: $keyword, navParam: $navParam, storefilter: $storefilter, storeId: $storeId, itemIds: $itemIds, channel: $channel, additionalSearchParams: $additionalSearchParams, loyaltyMembershipInput: $loyaltyMembershipInput) {\n    metadata {\n      categoryID\n      analytics {\n        semanticTokens\n        dynamicLCA\n        __typename\n      }\n      canonicalUrl\n      searchRedirect\n      clearAllRefinementsURL\n      contentType\n      isStoreDisplay\n      productCount {\n        inStore\n        __typename\n      }\n      stores {\n        storeId\n        storeName\n        address {\n          postalCode\n          __typename\n        }\n        nearByStores {\n          storeId\n          storeName\n          distance\n          address {\n            postalCode\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    products(startIndex: $startIndex, pageSize: $pageSize, orderBy: $orderBy, filter: $filter) {\n      identifiers {\n        storeSkuNumber\n        canonicalUrl\n        brandName\n        itemId\n        productLabel\n        modelNumber\n        productType\n        parentId\n        isSuperSku\n        __typename\n      }\n      installServices(storeId: $storeId, zipCode: $zipCode) @skip(if: $skipInstallServices) {\n        scheduleAMeasure\n        gccCarpetDesignAndOrderEligible\n        __typename\n      }\n      itemId\n      dataSources\n      media {\n        images {\n          url\n          type\n          subType\n          sizes\n          __typename\n        }\n        __typename\n      }\n      pricing(storeId: $storeId) {\n        value\n        alternatePriceDisplay\n        alternate {\n          bulk {\n            pricePerUnit\n            thresholdQuantity\n            value\n            __typename\n          }\n          unit {\n            caseUnitOfMeasure\n            unitsOriginalPrice\n            unitsPerCase\n            value\n            __typename\n          }\n          __typename\n        }\n        original\n        mapAboveOriginalPrice\n        message\n        preferredPriceFlag\n        promotion {\n          type\n          description {\n            shortDesc\n            longDesc\n            __typename\n          }\n          dollarOff\n          percentageOff\n          savingsCenter\n          savingsCenterPromos\n          specialBuySavings\n          specialBuyDollarOff\n          specialBuyPercentageOff\n          dates {\n            start\n            end\n            __typename\n          }\n          __typename\n        }\n        specialBuy\n        unitOfMeasure\n        __typename\n      }\n      reviews {\n        ratingsReviews {\n          averageRating\n          totalReviews\n          __typename\n        }\n        __typename\n      }\n      availabilityType {\n        discontinued\n        type\n        __typename\n      }\n      badges(storeId: $storeId) {\n        name\n        __typename\n      }\n      details {\n        collection {\n          collectionId\n          name\n          url\n          __typename\n        }\n        __typename\n      }\n      favoriteDetail {\n        count\n        __typename\n      }\n      fulfillment(storeId: $storeId, zipCode: $zipCode) {\n        backordered\n        backorderedShipDate\n        bossExcludedShipStates\n        excludedShipStates\n        seasonStatusEligible\n        fulfillmentOptions {\n          type\n          fulfillable\n          services {\n            type\n            hasFreeShipping\n            freeDeliveryThreshold\n            locations {\n              curbsidePickupFlag\n              isBuyInStoreCheckNearBy\n              distance\n              inventory {\n                isOutOfStock\n                isInStock\n                isLimitedQuantity\n                isUnavailable\n                quantity\n                maxAllowedBopisQty\n                minAllowedBopisQty\n                __typename\n              }\n              isAnchor\n              locationId\n              storeName\n              state\n              type\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      info {\n        hasSubscription\n        isBuryProduct\n        isSponsored\n        isGenericProduct\n        isLiveGoodsProduct\n        sponsoredBeacon {\n          onClickBeacon\n          onViewBeacon\n          __typename\n        }\n        sponsoredMetadata {\n          campaignId\n          placementId\n          slotId\n          __typename\n        }\n        globalCustomConfigurator {\n          customExperience\n          __typename\n        }\n        returnable\n        hidePrice\n        productSubType {\n          name\n          link\n          __typename\n        }\n        categoryHierarchy\n        samplesAvailable\n        customerSignal {\n          previouslyPurchased\n          __typename\n        }\n        productDepartmentId\n        productDepartment\n        augmentedReality\n        ecoRebate\n        quantityLimit\n        sskMin\n        sskMax\n        unitOfMeasureCoverage\n        wasMaxPriceRange\n        wasMinPriceRange\n        swatches {\n          isSelected\n          itemId\n          label\n          swatchImgUrl\n          url\n          value\n          __typename\n        }\n        totalNumberOfOptions\n        paintBrand\n        dotComColorEligible\n        __typename\n      }\n      keyProductFeatures @skip(if: $skipKPF) {\n        keyProductFeaturesItems {\n          features {\n            name\n            refinementId\n            refinementUrl\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      specificationGroup @skip(if: $skipSpecificationGroup) {\n        specifications {\n          specName\n          specValue\n          __typename\n        }\n        specTitle\n        __typename\n      }\n      subscription @skip(if: $skipSubscribeAndSave) {\n        defaultfrequency\n        discountPercentage\n        subscriptionEnabled\n        __typename\n      }\n      sizeAndFitDetail {\n        attributeGroups {\n          attributes {\n            attributeName\n            dimensions\n            __typename\n          }\n          dimensionLabel\n          productType\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    id\n    searchReport {\n      totalProducts\n      didYouMean\n      correctedKeyword\n      keyword\n      pageSize\n      searchUrl\n      sortBy\n      sortOrder\n      startIndex\n      __typename\n    }\n    relatedResults {\n      universalSearch {\n        title\n        __typename\n      }\n      relatedServices {\n        label\n        __typename\n      }\n      visualNavs {\n        label\n        imageId\n        webUrl\n        categoryId\n        imageURL\n        __typename\n      }\n      visualNavContainsEvents\n      relatedKeywords {\n        keyword\n        __typename\n      }\n      __typename\n    }\n    taxonomy {\n      brandLinkUrl\n      breadCrumbs {\n        browseUrl\n        creativeIconUrl\n        deselectUrl\n        dimensionId\n        dimensionName\n        label\n        refinementKey\n        url\n        __typename\n      }\n      __typename\n    }\n    templates\n    partialTemplates\n    dimensions {\n      label\n      refinements {\n        refinementKey\n        label\n        recordCount\n        selected\n        imgUrl\n        url\n        nestedRefinements {\n          label\n          url\n          recordCount\n          refinementKey\n          __typename\n        }\n        __typename\n      }\n      collapse\n      dimensionId\n      isVisualNav\n      isVisualDimension\n      nestedRefinementsLimit\n      visualNavSequence\n      __typename\n    }\n    orangeGraph {\n      universalSearchArray {\n        pods {\n          title\n          description\n          imageUrl\n          link\n          __typename\n        }\n        info {\n          title\n          __typename\n        }\n        __typename\n      }\n      productTypes\n      __typename\n    }\n    appliedDimensions {\n      label\n      refinements {\n        label\n        refinementKey\n        url\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n'
    }


def parse_useful_attributes(item: dict) -> dict:
    """
    Given a raw item response from the GraphQL API, parse out the relevant attributes we're interested in and generate
    a simple dictionary.
    """
    identifiers = item['identifiers']
    reviews = item['reviews']
    fulfillment = item['fulfillment']
    fulfillment_options = fulfillment['fulfillmentOptions']

    new_useful = {
        'brand': identifiers['brandName'],
        'itemId': identifiers['itemId'],
        'label': identifiers['productLabel'],
        'model': identifiers['modelNumber'],
        'url': identifiers['canonicalUrl'],
        'avgRating': reviews['ratingsReviews']['averageRating'],
        'totalRatings': reviews['ratingsReviews']['totalReviews'],
        'awards': [badge['name'] for badge in item['badges']],
        'availability': fulfillment_options[0]['services'][0]['locations'][0]['inventory']['quantity'],
        'returnable': item['info']['returnable'],
        'categories': item['info']['categoryHierarchy'],
        'price': str(item['pricing']['value'])
    }

    for image in item['media']['images']:
        if image['subType'] == 'PRIMARY':
            top_image_size = image['sizes'][-1]
            new_useful['imageUrl'] = image['url'].replace('<SIZE>', top_image_size)
            break

    return new_useful


def generate_output():
    """
    Generates the JSON output as requested for the given STORES and items TO_SCRAPE.
    :return:
    """
    for store in STORES:
        with open(f'data-from-store-{store}.json', 'w') as f:
            f.write('')  # always create the file
        useful = []

        for product, accepted_brands in TO_SCRAPE.items():
            search_item_identifier = product.split('/')[-1]
            search_item_category = product.split('/')[-2].replace('-', ' ')

            print(f'Now scraping results for item category: "{search_item_category}", ID: "{search_item_identifier}"')
            print(f'SHOP ID: {store}')


            for i in range(0, GRAPHQL_MAX_START_INDEX, GRAPHQL_PAGE_SIZE):
                form_data = generate_form_data(search_item_identifier, store, i)
                page = requests.post(
                    url='https://www.homedepot.com/federation-gateway/graphql?opname=searchModel',
                    json=form_data, headers=HEADERS, timeout=30
                )

                # Save a copy of the raw API response to a text file for debugging
                with open(f'raw_text-{store}.txt', 'w') as f:
                    f.write(page.text)

                # Grab JSON data
                data = page.json()
                items = data['data']['searchModel']['products']

                for item in items:
                    # Grab some helpful parts of the large item dictionary
                    if item['identifiers']['brandName'] not in accepted_brands:
                        continue

                    # Parse out useful attributes and append them to our list, ready for output
                    new_useful_dictionary = parse_useful_attributes(item)

                    # Check if this item was already scraped before
                    if new_useful_dictionary not in useful:
                        useful.append(new_useful_dictionary)
                    else:
                        #print('This product was already scraped')
                        pass

                print(f'Amount of items matching requirements: {len(useful)}')

        with open(f'data-from-store-{store}.json', 'a') as f:
            json.dump(useful, f)


if __name__ == '__main__':
    generate_output()
