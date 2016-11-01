# BlackJack-Logic
The code for the game logic

#### Game Rules
Field | Description | Possible Values
--|--|--
name | the name of the game | anything
deal | how many cards to deal at the start of the game | integer value, "divide" (divides the deck by number of player)
hit | how many cards to hit each player with each turn | integer value
hit_req | whether or not you have to take a card | true or false
hit_until | whether or not the player can be hit mutliple times per turn | "dealt" (once), "done" (until the player no longer wants to be hit), integer value (optional up until this amount)
 
