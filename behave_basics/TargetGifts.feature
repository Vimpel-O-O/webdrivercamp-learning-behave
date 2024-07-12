Feature: Target Gifts
  Background: Open needed page
    Given Navigate to https://www.target.com/

  #Scenario: Navigate to the page
    #Given Search for Gift Ideas

  #Scenario Outline: Verify searched page's headers
    #When Search for <search_item>
    #Then Verify header of the page contains <search_item>

    #Examples:
     # | search_item |
      #| Gift Ideas  |
      #| iphone      |

  Scenario: Gifts - Price validation
    When Search for Gift Ideas
    When Select Her in Who are you shopping for? section
    And Wait 5 sec
    When Select Gifts under $15 in Great gifts for any budget section
    Then Collect all items on the first page into collected_items on the feature level
    Then Verify all collected results' price is < 15
      | context.feature.collected_items |

  @no_background
  Scenario: Gifts - Shipment validation
    Then Verify all collected results' shipment is Free shipping
      | context.feature.collected_items |

  Scenario Outline: Gifts - All Price validation
    When Search for Gift Ideas
    When Select <option_1> in Who are you shopping for? section
    And Wait 5 sec
    When Select <option_2> in Great gifts for any budget section
    Then Collect all items on the first page into collected_items
    Then Verify all collected results' price is <condition>
      | context.collected_items |
    Examples: Her
      | option_1 | option_2         | condition |
      | Her      | Gifts under $15  | < 15      |
      | Her      | Gifts under $25  | < 25      |
      | Her      | Gifts under $50  | < 50      |
      | Her      | Gifts under $100 | < 100     |
    Examples: Him
      | option_1 | option_2         | condition |
      | Him      | Gifts under $15  | < 15      |
      | Him      | Gifts under $25  | < 25      |
      | Him      | Gifts under $50  | < 50      |
      | Him      | Gifts under $100 | < 100     |