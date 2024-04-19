Feature: Everything about your Houses
  As user I wand to add, update, and delete houses in the house store

#  Scenario: I successfully create new empty house
#    When I make POST request to "/houses/" with body
#    """
#      {
#        "cadastral_number": "12:12:1234567:12",
#        "longitude": 10.0,
#        "latitude": 12.3
#      }
#    """
#    Then Response is 200

  Scenario: I get n error if I try to create new house
    When I make POST request to "/houses/" with body
    """
      {
        "cadastral_number": "12:12:1234567",
        "longitude": 10.0,
        "latitude": 12.3
      }
    """
    Then Response is 422