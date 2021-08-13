import smartpy as sp
# TODO: Code needs to be fixed.
class Cryptobot(sp.Contract):
    
    # you need to accept market_address while initializing the Cryptobot.
    def __init__(self, manager_address, life_state, initial_mutez, market_address):
        
        self.init(
            bot_manager = manager_address,
            name = "terminator",
            is_alive = life_state,
            plasma_bullet_count = 5,

            record_alien_kills = {
                "simple_alien": sp.nat(0), 
                "boss_alien": sp.nat(0), 
            },
            mutez_points = sp.mutez(initial_mutez),
            # add market_address over here.
            market_address = market_address,
            
            #add active_powerup over here.
            active_powerup = sp.record(power = "", duration = 0)

        )

        
    @sp.entry_point
    def shoot_alien(self, alien_type):
        
        sp.verify(
            self.data.bot_manager == sp.sender, 
            message = "Error: non manager call"
        )

        sp.if self.data.plasma_bullet_count >= 1:
            self.data.plasma_bullet_count -= 1
            self.data.record_alien_kills[alien_type] += 1
        sp.else:
            sp.failwith("Error: you ran out of bullets! Please buy more!")
            

    @sp.entry_point
    def buy_powerup(self, powerup):
        # 1. Define the data_type to be sent - a record that holds a variable of type string.
        data_type = sp.TRecord(powerup = sp.TString)
        # 2. Define the market_contract.
        market_contract = sp.contract(data_type, self.data.market_address).open_some()
        # 3. Reduce 3000 mutez from mutez_points
        self.data.mutez_points -= sp.mutez(3000)
        # 4. Define data_to_be_sent - record that holds a variable powerup which is equal to powerup accepted in the parameter.
        data_to_be_sent = sp.record(powerup = powerup)
        # 5. Call the market_contract with powerup and 0 mutez.
        sp.transfer(data_to_be_sent, sp.mutez(0), market_contract)
        
        
    @sp.entry_point
    def recieve_powerup(self, params):
        # will implement this in the next chapter
        pass
    
class Market(sp.Contract):
    def __init__(self):
        self.init(
            
            powerups = [
                sp.record(power = "freeze_bullet", duration = 3), 
                sp.record(power = "one_shot_kill", duration = 4)
            ]
        )
    
    @sp.entry_point
    def send_powerup(self, params):
        # will implement this in the next chapter
        pass
        
    
@sp.add_test(name = "inter-contract")
def test():
    scenario = sp.test_scenario()
    
    my_account = sp.test_account("Cryptobot Owner")
    
    market = Market()
    scenario += market
    
    test_bot =  Cryptobot(manager_address = my_account.address,life_state = True, initial_mutez=5000, market_address = market.address)
    scenario += test_bot
    
    # test code over here.
    scenario += test_bot.buy_powerup("time_freeze")
    scenario.verify(test_bot.data.mutez_points == sp.mutez(2000))
    
Sub-entry point, loops and local variables 
Implement the sub entry point find_powerup in the Market contract.
Define a local variable called powerup_to_send which should be a record which holds a variable called power(equal to an empty string) and another variable called duration(equal to 0).
Loop through the powerups in the contract storage.
Inside the loop, if it matches the powerup we’re looking for set powerup_to_send equal to the powerup.
Return the value of powerup_to_send(remember to use sp.result).
    
 import smartpy as sp
# TODO: Code needs to be fixed.
class Cryptobot(sp.Contract):

    def __init__(self, manager_address, life_state, initial_mutez, market_address):
        
        self.init(
            bot_manager = manager_address,
            name = "terminator",
            is_alive = life_state,
            plasma_bullet_count = 5,

            record_alien_kills = {
                "simple_alien": sp.nat(0), 
                "boss_alien": sp.nat(0), 
            },
            mutez_points = sp.mutez(initial_mutez),
            market_address = market_address,
            active_powerup = sp.record(power = "", duration = 0)
        )

        
    @sp.entry_point
    def shoot_alien(self, alien_type):
        
        sp.verify(
            self.data.bot_manager == sp.sender, 
            message = "Error: non manager call"
        )

        sp.if self.data.plasma_bullet_count >= 1:
            self.data.plasma_bullet_count -= 1
            self.data.record_alien_kills[alien_type] += 1
        sp.else:
            sp.failwith("Error: you ran out of bullets! Please buy more!")
            
    @sp.entry_point
    def buy_powerup(self, powerup):
        data_type = sp.TRecord(powerup = sp.TString)
        market_contract = sp.contract(data_type, self.data.market_address).open_some()
        
        self.data.mutez_points -= sp.mutez(3000)
        
        data_to_be_sent = sp.record(powerup = powerup)
        sp.transfer(data_to_be_sent, sp.mutez(0), market_contract)
        
    
    @sp.entry_point
    def recieve_powerup(self, params):
        # will implement this in the next chapter
        pass
    
class Market(sp.Contract):
    def __init__(self):
        self.init(
            
            powerups = [
                sp.record(power = "freeze_bullet", duration = 3), 
                sp.record(power = "one_shot_kill", duration = 4)
            ]
        )
        
    
    # implement the sub entry point `find_powerup` over here.
    @sp.sub_entry_point
    def find_powerup(self, powerup):
        # define a local variable called `powerup_to_send`
        # powerup should be a record which holds a variable called power(equal to an empty string) and another variable called duration(equal to 0).
        powerup_to_send = sp.local("powerup_to_send", sp.record(power = "", duration = 0))
        
        sp.for p in self.data.powerups:
            sp.if p.power == powerup:
                powerup_to_send.value.power = p.power
                powerup_to_send.value.duration = p.duration

        
        # loop through the powerups in the contract storage.
        # inside the loop, if it matches the powerup we're looking for set `powerup_to_send` equal to the powerup.
        # remember, local variables are accessed with `<var>.value`
        sp.result(powerup_to_send.value)
        
        
        #return the value of powerup_to_send
        
    
    @sp.entry_point
    def send_powerup(self, params):
        # will implement this in the next chapter
        pass
        
    
@sp.add_test(name = "find-power")
def test():
    scenario = sp.test_scenario()
    
    ## Class Invokation
    my_account = sp.test_account("Cryptobot Owner")
    market = Market()
    scenario += market
    
    test_bot =  Cryptobot(manager_address = my_account.address,life_state = True, initial_mutez=5000, market_address = market.address)
    scenario += test_bot
    
   Inter-contract calling, part-2
   You’ve told Market which powerup you want, but don’t you want to get the powerup back!? After all, powerups will help you destroy the aliens.
So far, we’ve implemented only one inter-contract call. But to complete the whole process of buying a powerup, we’re going to need one more from Market to Cryptobot to send the real powerup.
This loose term is called cyclic inter-contract calls.

First contract calls the Second contract and then the Second contract calls the First contract.
There’s a last piece in the puzzle that you need to understand to implement the full functionality - sp.to_address.
sp.to_address accepts a contract(sp.TContract) and returns the address(sp.TAddress) of that contract.
It can be used in combination with sp.self to generate the address of the currenty smart contract inside an entry point.
    
    
    import smartpy as sp
# TODO: Code needs to be fixed.
class Cryptobot(sp.Contract):

    def __init__(self, manager_address, life_state, initial_mutez, market_address):
        
        self.init(
            bot_manager = manager_address,
            name = "terminator",
            is_alive = life_state,
            plasma_bullet_count = 5,

            record_alien_kills = {
                "simple_alien": sp.nat(0), 
                "boss_alien": sp.nat(0), 
            },
            mutez_points = sp.mutez(initial_mutez),
            market_address = market_address,
            active_powerup = sp.record(power = "", duration = 0)
        )

        
    @sp.entry_point
    def shoot_alien(self, alien_type):
        
        sp.verify(
            self.data.bot_manager == sp.sender, 
            message = "Error: non manager call"
        )

        sp.if self.data.plasma_bullet_count >= 1:
            self.data.plasma_bullet_count -= 1
            self.data.record_alien_kills[alien_type] += 1
        sp.else:
            sp.failwith("Error: you ran out of bullets! Please buy more!")
            
    @sp.entry_point
    def buy_powerup(self, powerup):
        
        # modify data_type to also hold another variable called cryptobot_address.
        # cryptobot_address is of type `sp.TContract` which accepts a record that has the same variables as `active_powerup`.
        data_type = sp.TRecord(powerup = sp.TString, cryptobot_contract = sp.TContract(sp.TRecord(power = sp.TString, duration = sp.TNat)))
            
        market_contract = sp.contract(data_type, self.data.market_address).open_some()
        self.data.mutez_points -= sp.mutez(3000)
        
        # define self_contract -
        # 1. Accepts a record with two variables - power(string), duration(nat)
        # 2. Points to the Cryptobot( use sp.to_address() ) 
        # 3. Specifies receive_powerup entry point
        self_contract = sp.contract(sp.TRecord(power = sp.TString, duration = sp.TNat), sp.to_address(sp.self), "receive_powerup").open_some()
        
        
        # modify data_to_be_sent to also hold cryptobot_contract which is assigned self_contract
        data_to_be_sent = sp.record(powerup = powerup, cryptobot_contract = self_contract)
        sp.transfer(data_to_be_sent, sp.mutez(0), market_contract)
        
    
    @sp.entry_point
    def receive_powerup(self, powerup):
        # set active_powerup as the powerup being accepted as a parameter
        self.data.active_powerup.power = powerup.power
        self.data.active_powerup.duration = powerup.duration
        
    
    
class Market(sp.Contract):

    def __init__(self):
        self.init(
            powerups = [
                sp.record(power = "time_freeze", duration = 3), 
                sp.record(power = "one_shot_kill", duration = 4)
            ]
        )
    
    
    @sp.sub_entry_point
    def find_powerup(self, powerup):
        powerup_to_send = sp.local("powerup_to_send", sp.record(power = "", duration = sp.nat(0)))
        
        sp.for p in self.data.powerups:
            
            sp.if p.power == powerup:
    
                powerup_to_send.value.power = p.power
                powerup_to_send.value.duration = p.duration
        
        sp.result(powerup_to_send.value)
    
    @sp.entry_point
    def send_powerup(self, params):
        # define a variable powerup_to_send the which is equal to the result of `find_powerup`. 
        # remember to pass find_powerup the powerup sent in params.
        powerup_to_send = self.find_powerup(params.powerup)
        
        # transfer powerup_to_sent with 0 mutez to the cryptobot_contract sent through the params.
        sp.transfer(powerup_to_send, sp.mutez(0), params.cryptobot_contract)
    
@sp.add_test(name = "inter-contract")
def test():
    scenario = sp.test_scenario()
    
    ## Class Invokation
    my_account = sp.test_account("Cryptobot Owner")
    market = Market()
    scenario += market
    
    test_bot =  Cryptobot(manager_address = my_account.address,life_state = True, initial_mutez=5000, market_address = market.address)
    scenario += test_bot
    
    # test our code over here.
    scenario += test_bot.buy_powerup("time_freeze")
    scenario.verify(test_bot.data.mutez_points == sp.mutez(2000))
    scenario.verify(test_bot.data.active_powerup.power == "time_freeze")


    
    

