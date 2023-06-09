# Basic moneyline arbitrage bet finder program 
# calculates the discrepancies in odds across different bookmakers provided by user input and returns the arbitrage opportunities
# for more info on arbitrage betting: https://en.wikipedia.org/wiki/Arbitrage_betting
import bet_space
import betting_odds_calculator
import arbitrage_calculator

# switches false first time after title is displayed, so no reappearance
first_run = True # 

# list of bet spaces
bet_spaces = []

# dummy bet space for sake of testing
bet_spaces.append(bet_space.BetSpace("Djokovic vs. Nadal", "decimal", [3, 4], 100))

# entering the create bet space menu and handling
def create_bet_space_menu():
    # declaring local variables
    name_not_duplicate = True # default value
    odds_type = "decimal"
    stake = 0
    odds_list = []
    float_odds_list = []

    # loops
    name_loop = True
    odds_type_loop = True
    stake_loop = True
    odds_list_loop = True

    # ask for bet space name, or let user exit 
    print('\nWhat would you like your Bet Space to be named?\n\u001b[90m(type "exit" to leave)\u001b[0m')
    while name_loop:
        try:
            name = input("\u001b[90m> \u001b[0m").strip()
        except: pass
        if name == "exit":
            print("\n[1] Create Bet Space\n[2] Visit Bet Spaces\n[3] Betting Calculators\n[4] Quit\n")
            return
        # validates the odds in the user-input list
        for bet_space in bet_spaces:
            if name == bet_space.name:
                name_not_duplicate = False 
        if name != "" and name_not_duplicate == True:
            name_loop = False
            break
        else:
            if name_not_duplicate == False:
                print("\nA Bet Space with this name already exists.")
                name_not_duplicate = True # reset to default value
            print('\nPlease enter a valid name for the Bet Space or type "exit"')

    # confirm type of odds
    print("\nPlease enter the type of all odds for this Bet Space ('american' or 'decimal'):")
    while odds_type_loop:
        try:
            odds_type = input("\u001b[90m> \u001b[0m")
        except: pass
        if odds_type == "american" or odds_type == 'a':
            odds_type = "american"
            odds_type_loop = False
        elif odds_type == 'decimal' or odds_type == 'd':
            odds_type = "decimal"
            odds_type_loop = False
        else: print("\nInvalid type of odds (must be 'american' or 'decimal'). Please try again:")

    # confirm list of odds
    print("\nPlease enter the odds in a comma-separated list (e.g. 2.5, 3.2, ...)")
    while odds_list_loop:
        try:
            odds_string = input("\u001b[90m> \u001b[0m")
        except: pass
        # convert string to list
        odds_list = odds_string.split(", ")
        if len(odds_list) == 1:
            print(f"\nSet must contain at least 2 odds.")
        # validate each element of the list before proceeding
        num_of_odds = 0
        for odd in odds_list:
            try:
                odd_float = float(odd)
                if (odds_type == "decimal" and odd_float > 1) or (odds_type == 'american' and (odd_float < -100 or 100 < odd_float)):
                    num_of_odds += 1
                    float_odds_list.append(odd_float)
                    if num_of_odds > 1:
                        if num_of_odds == len(odds_list): # if all elements (odds) valid
                            # confirm stake
                            print("\nPlease enter the stake:")
                            while stake_loop:
                                tried_stake = -1
                                try:
                                    tried_stake = float(input("\u001b[90m> \u001b[0m"))
                                except: pass
                                if tried_stake > 0:
                                    stake = tried_stake
                                    stake_loop = False
                                else: print("\nInvalid stake (must be greater than 0). Please try again:")

                            # success message
                            print("\n\u001b[32mBet Space Successfully Created!\u001b[0m")

                            # format attributes
                            formatted_odds_list = list_to_string(float_odds_list)
                            formatted_stake = "${:.2f}".format(stake)

                            # display attributes of bet space 
                            print("\nBet Space Name:", name)
                            print("Odds Type:", odds_type)
                            print("Odds List:", formatted_odds_list) 
                            print("Stake:", formatted_stake)

                            # create bet space and add to collection
                            new_bet_space = bet_space.BetSpace(name, odds_type, odds_list, stake)
                            bet_spaces.append(new_bet_space)

                            # shows main menu options before going back
                            print("\n[1] Create Bet Space\n[2] Visit Bet Spaces\n[3] Betting Calculators\n[4] Quit\n")
                            return
                else:
                    print(f"\nInvalid set of odds. Must be a valid {odds_type} odd and comma-separated in the list.")
                    if odds_type == 'american':
                        print("(e.g. 300, 340, -140)")
                    if odds_type == 'decimal':
                        print("(e.g. 1.2, 1.63, 3.5)")
                    break  
            except ValueError:
                print(f"\nInvalid odd value: {odd}. Must be a valid {odds_type} odd and comma-separated in the list.")
                if odds_type == 'american':
                    print("(e.g. 300, 340, -140)")
                if odds_type == 'decimal':
                    print("(e.g. 1.2, 1.63, 3.5)")
                break

# function for entering the vbs menu and handling
def visit_bet_space_menu():
    # declaring local variables
    bet_space_names = [] 
    selected_bet_space = ""
    bet_space_options_loop = True

    # check if no Bet Spaces made
    if bet_spaces == []:
        print("\nYou have no Bet Spaces, you must create at least one to visit.")
        print("\n[1] Create Bet Space\n[2] Visit Bet Spaces\n[3] Betting Calculators\n[4] Quit\n")
        return
    
    # display names of all Bet Spaces
    print("\nYou have the following Bet Spaces:")
    for bs in bet_spaces:
        bet_space_names.append(bs.name)
    print(list_to_string(bet_space_names))

    # selection of bet space
    print('\nWhich Bet Space would you like to select?\n\u001b[90m(type "exit" to leave)\u001b[0m')
    while True:
        try:
            selected = (input("\u001b[90m> \u001b[0m"))
        except: pass
        for bs in bet_spaces:
            if selected == bs.name:
                selected_bet_space = bs
        if selected == "exit":
            print("\n[1] Create Bet Space\n[2] Visit Bet Spaces\n[3] Betting Calculators\n[4] Quit\n")
            return
        elif selected == "view":
            print("\nYou have the following Bet Spaces:")
            print(list_to_string(bet_space_names))
            print('\nWhich Bet Space would you like to select?\n\u001b[90m(type "exit" to leave)\u001b[0m')
        elif selected == "":
            print('\nThat Bet Space does not exist, please try again.\n\u001b[90m(type "exit" to leave or "view" to see the list)\u001b[0m')
                # selects the bet space from list based off name
        else:
            # handling of the bet space once its been selected
            if type(selected_bet_space) == bet_space.BetSpace:
                # bet space options
                print('\nWhat would you like to do with the\u001b[35m', selected_bet_space.name, '\u001b[0mBet Space?')
                print("\n[1] Find Arbitrage Opportunity\n[2] Leave\n")
                
                fao_options = ["find arbitrage opportunity", "arb", "1", "one"]
                leave_options = ["quit", "2", "two", "leave", "exit"]
                
                while bet_space_options_loop:
                    # creating new calculator with the given bet space's stake and odds list
                    arb_calc = arbitrage_calculator.ArbitrageCalculator(selected_bet_space.stake, selected_bet_space.odds_list) 

                    # user input for the main menu option
                    try:
                        selected_main_option = (input("\u001b[90m> \u001b[0m"))
                    except: pass
                    if selected_main_option in fao_options: # find arbitrage opportunity
                        # perform the necessary arbitrage calculations
                        tip = arb_calc.calc_total_implied_probability()
                        formatted_tip = "{:.2%}".format(tip)

                        hedged_stakes = arb_calc.calculate_hedged_stakes()
                        formatted_hedged_stakes = list_to_string(format_list_to_dollar(hedged_stakes))

                        pnl = arb_calc.calculate_pnl()
                        formatted_pnl = "${:.2f}".format(pnl)

                        roi = arb_calc.calculate_roi()
                        formatted_roi = "{:.2%}".format(roi)

                        # display list of odds and the tip
                        print("\nList of Odds for\u001b[35m", selected_bet_space.name + f"\u001b[0m: {list_to_string(selected_bet_space.odds_list)}")
                        print(f"\nThe Total Implied Probability of these odds is {formatted_tip}")

                        if tip < 1: # if tip shows an arbitrage opportunity
                            print(f"It is under 100%, so there is an \u001b[32marbitrage opportunity\u001b[0m. You can hedge accordingly:")
                            print(formatted_hedged_stakes)
                            print(f"\nYour profits would be \u001b[32m{formatted_pnl}\u001b[0m, with an ROI of {formatted_roi}")
                        elif tip > 1: # if tip shows no arbitrage opportunity
                            print(f"It is over 100%, so there is \u001b[31mno arbitrage opportunity\u001b[0m. You can still hedge accordingly:")
                            print(formatted_hedged_stakes)
                            print(f"\nBut your loss would be \u001b[31m{formatted_pnl}\u001b[0m, with an ROI of {formatted_roi}")
                        elif tip == 1: # if tip is 100%
                            print(f"It is exactly 100%, so there is no profit or loss to be made. You can still hedge accordingly:")
                            print(formatted_hedged_stakes)
                            print(f"\nBut you would gain nothing.")
                        
                        print("\n[1] Find Arbitrage Opportunity\n[2] Leave\n")

                    elif selected_main_option in leave_options: # resets selected option, goes back to previous loop
                        selected_bet_space = ""
                        bet_space_options_loop = False
                        print("\nYou have the following Bet Spaces:")
                        print(list_to_string(bet_space_names))
                        print('\nWhich Bet Space would you like to select?\n\u001b[90m(type "exit" to leave)\u001b[0m')
                    else:
                        print("\nThat is not a valid option. Please try again.")
                        print("\n[1] Find Arbitrage Opportunity\n[2] Leave\n")
            else:
                print('\nThat Bet Space does not exist, please try again.\n\u001b[90m(type "exit" to leave or "view" to see the list)\u001b[0m')
        
    





















# starts program
def run():
    main_menu()

# function for displaying the first menu's options
def main_menu():
    global first_run
    # title which only appears the very first time the program is ran
    if first_run == True:
        print("\nARBITRAGE BOT\nSelect one of the following options:")
        first_run = False

    # display main menu options
    print("\n[1] Create Bet Space\n[2] Visit Bet Spaces\n[3] Betting Calculators\n[4] Quit\n")

    # list of valid inputs for each of the three options
    cbs_options = ["create bet space", "create", "1", "one"]
    vbs_options = ["visit bet space", "visit", "2", "two"]
    bet_options = ["3", "three", "bet", "bet calculator", "calculator", "calc"]
    quit_options = ["quit", "4", "four", "leave", "exit"]

    # forever loop prompts user input for the options, handles each option and repeats prompt on invalid input
    while True:
        # user input for the main menu option
        selected_main_option = (input("\u001b[90m> \u001b[0m"))

        if selected_main_option in cbs_options:
            create_bet_space_menu()
        elif selected_main_option in vbs_options:
            visit_bet_space_menu()
        elif selected_main_option in bet_options:
            bet_calculator_menu()
        elif selected_main_option in quit_options:
            print("\nGoodbye.\n")
            quit()
        else:
            print("\nThat is not a valid option. Please try again.")
            print("\n[1] Create Bet Space\n[2] Visit Bet Spaces\n[3] Betting Calculators\n[4] Quit\n")
    
# function for bet calculator
def bet_calculator_menu():
    # display title with options
    print("\nBETTING CALCULATORS\nSelect one of the following options:")
    print("\n[1] Betting Odds Calculator\n[2] Arbitrage Calculator\n[3] Moneyline Converter\n[4] Exit\n")

    # list of valid inputs for each of the three options
    boc_options = ["betting odds calculator", "betting odds", "betting", "bet", "1", "one"]
    ac_options = ["arbitrage calculator", "arbitrage", "arb", "2", "two"]
    ml_options = ["3", "three", "moneyline converter", "moneyline", "ml"]
    quit_options = ["quit", "four", "4", "leave", "exit"]
    # forever loop prompts user input for the options, handles each option and repeats prompt on invalid input
    while True:
        # user input for the calculator options
        selected_calc_option = (input("\u001b[90m> \u001b[0m"))

        # handling user input for respective calculators
        if selected_calc_option in boc_options:
            betting_odds_calculator_menu()
        elif selected_calc_option in ac_options:
            arbitrage_calculator_menu()
        elif selected_calc_option in ml_options:
            moneyline_converter_menu()
        elif selected_calc_option in quit_options:
            # displays main menu options before ending function call and going back to main menu loop 
            print("\n[1] Create Bet Space\n[2] Visit Bet Spaces\n[3] Betting Calculators\n[4] Quit\n")
            return
        else:
            print("\nThat is not a valid option. Please try again.")
            print("\n[1] Betting Odds Calculator\n[2] Arbitrage Calculator\n[3] Moneyline Converter\n[4] Exit\n")

# function for entering the betting odds calculator 
def betting_odds_calculator_menu():
    # declaring the initial odds, odds type, stake, and default enabling the odds loop
    odds = 0.0
    stake = 0.0
    odds_type = "decimal"
    odds_loop = True

    # confirm type of odds
    print("\nPlease enter the type of odds ('american' or 'decimal'):")
    while odds_loop:
        try:
            odds_type = input("\u001b[90m> \u001b[0m")
        except: pass
        # stopping the odds loop if type is either american or decimal
        if odds_type == "american" or odds_type == 'a':
            odds_type = "american"
            odds_loop = False
        elif odds_type == 'decimal' or odds_type == 'd':
            odds_type = "decimal"
            odds_loop = False
        else: print("\nInvalid type of odds (must be 'american' or 'decimal'). Please try again:")

    # enter odds
    print("\nPlease enter the odds:")
    while True:
        try:
            odds = float(input("\u001b[90m> \u001b[0m"))
        except: pass
        # validates the odds in the user-input list
        if (odds_type == "decimal" and odds > 1) or (odds_type == 'american' and (odds < -100 or 100 < odds)):
            # enter stake
            print("\nPlease enter the stake amount:")
            while True:
                try:
                    stake = float(input("\u001b[90m> \u001b[0m"))
                except: pass
                if stake > 0:
                    # convert odds to decimal if odds type is american
                    if odds_type == 'american':
                        odds = american_to_decimal(odds)

                    # create new betting odds calculator object with given odds, stake
                    new_bet = betting_odds_calculator.BettingOddsCalculator(odds, stake)
                    
                    # calculate payout and put it in dollar form
                    payout = new_bet.calculate_payout()
                    formatted_payout = "${:,.2f}".format(payout)

                    # print results
                    print("\nPayout: \u001b[32m" + formatted_payout + "\u001b[0m")

                    # shows main menu options before going back
                    print("\n[1] Betting Odds Calculator\n[2] Arbitrage Calculator\n[3] Moneyline Converter\n[4] Exit\n")
                    return
                else:
                    print("\nInvalid stake (must be a float greater than 0 with no dollar sign). Please try again:\n")
        else:
            if odds_type == "decimal":
                print("\nInvalid odds (decimal odds must be greater than 1). Please try again:")
            elif odds_type == "american":
                print("\nInvalid odds (american odds must be greater than 100 or less than -100). Please try again:")

# converts american odds to decimal odds
def american_to_decimal(odds):
    if odds >= 0:
        decimal_odds = 1 + (odds / 100)
    else:
        decimal_odds = 1 + (100 / abs(odds))
    return decimal_odds

# takes a list and returns new list in dollar form
def format_list_to_dollar(list):
    formatted_list = []
    for num in list:
        formatted_list.append("${:,.2f}".format(num))
    return formatted_list

# takes list and returns string with comma-separated contents
def list_to_string(lst):
    return ", ".join(str(x) for x in lst)

# lets user figure out arbitrage information based on their bets with any set of odds and stake 
def arbitrage_calculator_menu():
    # declaring local variables
    stake = 0
    odds_list = []
    float_odds_list = []
    odds_type = "decimal"
    odds_type_loop = True
    stake_loop = True

    # confirm type of odds
    print("\nPlease enter the type of all odds ('american' or 'decimal'):")
    while odds_type_loop:
        try:
            odds_type = input("\u001b[90m> \u001b[0m")
        except: pass
        if odds_type == "american" or odds_type == 'a':
            odds_type = "american"
            odds_type_loop = False
        elif odds_type == 'decimal' or odds_type == 'd':
            odds_type = "decimal"
            odds_type_loop = False
        else: print("\nInvalid type of odds (must be 'american' or 'decimal'). Please try again:")

    # confirm stake
    print("\nPlease enter the stake:")
    while stake_loop:
        tried_stake = -1
        try:
            tried_stake = float(input("\u001b[90m> \u001b[0m"))
        except: pass
        if tried_stake > 0:
            stake = tried_stake
            stake_loop = False
        else: print("\nInvalid stake (must be greater than 0). Please try again:")

    # calculate arbitrage
    print("\nPlease enter the odds in a comma-separated list (e.g. 2.5, 3.2, ...)")
    while True:
        try:
            odds_string = input("\u001b[90m> \u001b[0m")
        except: pass
        # convert string to list
        odds_list = odds_string.split(", ")
        if len(odds_list) == 1:
            print(f"\nSet must contain at least 2 odds.")
        # validate each element of the list before proceeding
        num_of_odds = 0
        for odd in odds_list:
            try:
                odd_float = float(odd)
                if (odds_type == "decimal" and odd_float > 1) or (odds_type == 'american' and (odd_float < -100 or 100 < odd_float)):
                    num_of_odds += 1
                    float_odds_list.append(odd_float)
                    if num_of_odds > 1:
                        if num_of_odds == len(odds_list): # if all elements (odds) valid
                            # convert to decimal if american
                            if odds_type == "american":
                                for i in range(len(float_odds_list)):
                                    float_odds_list[i] = american_to_decimal(float_odds_list[i])
                            # create new calculator and calculated variables
                            arb_calc = arbitrage_calculator.ArbitrageCalculator(stake, float_odds_list)
                            
                            # perform the calculations on variables
                            total_implied_probability = arb_calc.calc_total_implied_probability()
                            hedged_stakes = arb_calc.calculate_hedged_stakes()
                            payout = arb_calc.calculate_payout()
                            pnl = arb_calc.calculate_pnl()
                            roi = arb_calc.calculate_roi()

                            # variable for whether arbitrage opportunity or not
                            is_arbitrage = "\u001b[31m(not an arbitrage opportunity)\u001b[0m" # default message
                            if total_implied_probability < 1:
                                is_arbitrage = "\u001b[32m(arbitrage opportunity)\u001b[0m"

                            # display formatted arb results
                            formatted_total_implied_probability = "{:.2%}".format(total_implied_probability)
                            formatted_hedged_stakes = list_to_string(format_list_to_dollar(hedged_stakes))
                            formatted_payout = "${:.2f}".format(payout)
                            formatted_pnl = "${:.2f}".format(pnl)
                            formatted_roi = "{:.2%}".format(roi)

                            print("\nTotal Implied Probability:", formatted_total_implied_probability, is_arbitrage)
                            print("Respective Hedged Stakes:", formatted_hedged_stakes)
                            print("Payout:", formatted_payout)
                            if pnl > 0:
                                print("PNL:\u001b[32m", formatted_pnl, "\u001b[0m")
                            elif pnl < 0:
                                print("PNL:\u001b[31m", formatted_pnl, "\u001b[0m")
                            else:
                                print("PNL:", formatted_pnl)
                            print("ROI:", formatted_roi)

                            # shows main menu options before going back
                            print("\n[1] Betting Odds Calculator\n[2] Arbitrage Calculator\n[3] Moneyline Converter\n[4] Exit\n")
                            return
                else:
                    print(f"\nInvalid set of odds. Must be a valid {odds_type} odd and comma-separated in the list.")
                    if odds_type == 'american':
                        print("(e.g. 300, 340, -140)")
                    if odds_type == 'decimal':
                        print("(e.g. 1.2, 1.63, 3.5)")
                    break  
            except ValueError:
                print(f"\nInvalid odd value: {odd}. Must be a valid {odds_type} odd and comma-separated in the list.")
                if odds_type == 'american':
                    print("(e.g. 300, 340, -140)")
                if odds_type == 'decimal':
                    print("(e.g. 1.2, 1.63, 3.5)")
                break

# finds the implied probability of single given moneyline odds
def moneyline_converter_menu():
    # declaring local variables
    odds = 0.0
    odds_type = "decimal"
    odds_type_loop = True

    # confirm type of odds
    print("\nPlease enter the type of all odds ('american' or 'decimal'):")
    while odds_type_loop:
        try:
            odds_type = input("\u001b[90m> \u001b[0m")
        except: pass
        if odds_type == "american" or odds_type == 'a':
            odds_type = "american"
            odds_type_loop = False
        elif odds_type == 'decimal' or odds_type == 'd':
            odds_type = "decimal"
            odds_type_loop = False
        else: print("\nInvalid type of odds (must be 'american' or 'decimal'). Please try again:")

    print("\nPlease enter the odds:")
    while True:
        try:
            odds = float(input("\u001b[90m> \u001b[0m"))
        except: pass
        # validates the odds in the user-input list
        if (odds_type == "decimal" and odds > 1) or (odds_type == 'american' and (odds < -100 or 100 < odds)):
            # convert odds to decimal if odds type is american
            if odds_type == 'american':
                odds = american_to_decimal(odds)

            ip = 1 / odds
            
            # calculate implied probability and put it in dollar form
            formatted_ip = "{:,.2%}".format(ip)

            # print results
            print("\nImplied Probability:", formatted_ip)

            # shows main menu options before going back
            print("\n[1] Betting Odds Calculator\n[2] Arbitrage Calculator\n[3] Moneyline Converter\n[4] Exit\n")
            return
        else:
            if odds_type == "decimal":
                print("\nInvalid odds (decimal odds must be greater than 1). Please try again:")
            elif odds_type == "american":
                print("\nInvalid odds (american odds must be greater than 100 or less than -100). Please try again:")


    

# starts program
run()
