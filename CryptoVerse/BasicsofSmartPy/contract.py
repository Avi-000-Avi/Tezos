import smartpy as sp

class Cryptobot(sp.Contract):
    #2. Add life_state as a parameter to the the __init__ function:
    def __init__(self,life_state):
        self.init(
            name = "terminator",
            #1. add is_alive state variable beneath
            
            #3.^Give is_alive the value of life_state
            is_alive = life_state
        )
        
    @sp.entry_point
    def change_name(self, new_name):
        self.data.name = new_name
        
@sp.add_test(name = "Test whether Cryptobot is alive or not")
def test():
    scenario = sp.test_scenario()
    
    #4. Pass life_state = True to Cryptobot’s class invocation:
    test_bot =  Cryptobot(life_state = True)
    
    scenario += test_bot
    
    scenario.verify(test_bot.data.is_alive == True)
    #5. Test for whether the Cryptobot is alive or not beneath: 


Tinkering with integers and basic math in SmartPy


import smartpy as sp

class Cryptobot(sp.Contract):
    def __init__(self, is_alive):
        self.init(
            name = "terminator",
            is_alive = is_alive,

            ## Add coordinate_x and coordinate_y variables
            ## Init both with 0 using sp.int and sp.nat respectively 
            coordinate_x = sp.int(0), 
            coordinate_y = sp.nat(0)
        )
        
    @sp.entry_point
    def change_name(self, new_name):
        self.data.name = new_name

    # Define move_horizontally entry point function
    @sp.entry_point
    def move_horizontally(self, update_to):
        self.data.coordinate_x += update_to
    
    # Define move_vertically entry point function
    @sp.entry_point
    def move_vertically(self,update_to):
        self.data.coordinate_y += update_to
        
@sp.add_test(name = "Test Cryptobot movement")
def test():
    scenario = sp.test_scenario()
    
    test_bot =  Cryptobot(is_alive = True)
    
    scenario += test_bot
            
    # Test your movement entry functions below
    # Move Cryptobot forward by 2 and vertically by 1
    scenario += test_bot.move_horizontally(2)
    scenario += test_bot.move_vertically(1)
    
    
    Tinkering with maps in SmartPy
    import smartpy as sp

class Cryptobot(sp.Contract):
    def __init__(self, life_state):
        self.init(
            name = "terminator",
            is_alive = life_state,
            coordinate_x = sp.int(0), 
            coordinate_y = sp.nat(0), 
            
            # Add plasma_bullet_count with 5 bullets:
            plasma_bullet_count = 5,
            
            # Add record_alien_kills below:
            record_alien_kills = {
                "simple_alien": sp.nat(0),
                "boss_alien": sp.nat(0)
            }

        )
        
    @sp.entry_point
    def change_name(self, new_name):
        self.data.name = new_name
      
    @sp.entry_point
    def move_horizontally(self, update_to):
        self.data.coordinate_x += update_to
        
    @sp.entry_point
    def move_vertically(self, update_to):
        self.data.coordinate_y += update_to

            
    # Add shoot_alien function below
    @sp.entry_point
    def shoot_alien(self, alien_type): 
        # Reduce plasma_bullet_count by 1
        self.data.plasma_bullet_count -= 1
            
        # Record the alien that was shot
        # and then increase it by 1 below
        self.data.record_alien_kills[alien_type] += 1
    
        
@sp.add_test(name = "Test shooting")
def test():
    scenario = sp.test_scenario()
    
    test_bot =  Cryptobot(life_state = True)
    
    scenario += test_bot

    # Use shoot_alien to kill 1 simple aliens and 1 boss alien
    scenario += test_bot.shoot_alien("simple_alien")
    scenario += test_bot.shoot_alien("boss_alien")
    
    Tinkering with addresses in SmartPy
    
    import smartpy as sp

class Cryptobot(sp.Contract):
    # Pass manager_address as a parameter to the initialization function
    def __init__(self, life_state, manager_address):
        self.init(
            # Add bot_manager variable below
            bot_manager = manager_address,

            name = "terminator",
            is_alive = life_state,
            
            coordinate_x = sp.int(0), 
            coordinate_y = sp.nat(0), 
            
            plasma_bullet_count = 5,
            
            record_alien_kills = {
                "simple_alien": sp.nat(0),
                "boss_alien": sp.nat(0)
            }
        )
        
    @sp.entry_point
    def change_name(self, new_name):
        self.data.name = new_name
             
    @sp.entry_point
    def move_horizontally(self, update_to):
        self.data.coordinate_x += update_to
    
    @sp.entry_point
    def move_vertically(self, update_to):
        self.data.coordinate_y += update_to

    @sp.entry_point
    def shoot_alien(self, alien_type): 
        self.data.plasma_bullet_count -= 1
        self.data.record_alien_kills[alien_type] += 1
     
@sp.add_test(name = "Simulating ownership")
def test():
    scenario = sp.test_scenario()
   
    # Define my_address variable below
    # and give it the address value of tz1Syu3KacZ8cy4286a4vaCeoMtwqVKHkaoj
    my_address = sp.address("tz1Syu3KacZ8cy4286a4vaCeoMtwqVKHkaoj")

    
    # Pass my_address as value to manager_address
    # and then use it to invoke the class
    
    test_bot =  Cryptobot(life_state = True ,manager_address = my_address)
   
    scenario += test_bot
          
    scenario += test_bot.shoot_alien("simple_alien")
   
    scenario += test_bot.shoot_alien("boss_alien")
    
    
    Tinkering with conditional code in SmartPy - sp.verify
    import smartpy as sp

class Cryptobot(sp.Contract):
    def __init__(self, manager_address):
        self.init(
            bot_manager = manager_address,

            plasma_bullet_count = 5, 
            
            record_alien_kills = {
                "simple_alien": sp.nat(0), 
                "boss_alien": sp.nat(0), 
            }
        )

    @sp.entry_point
    def shoot_alien(self, alien_type):
        # Use sp.verify to check 
        # whether caller's address is equal 
        # to bot_manager's address
        sp.verify(self.data.bot_manager == sp.sender,message = "Error: non manager call" )
        
        self.data.plasma_bullet_count -= 1
        self.data.record_alien_kills[alien_type] += 1

@sp.add_test(name = "Testing entry functions only callable by cryptobot manager")
def test():
    scenario = sp.test_scenario()
    
    my_address = sp.address("tz1Syu3KacZ8cy4286a4vaCeoMtwqVKHkaoj")
    
    test_bot =  Cryptobot(manager_address = my_address)
    
    scenario += test_bot
    
    # Use run method on both functions below and pass sender = my_address to it. 
    scenario += test_bot.shoot_alien("simple_alien").run(sender = my_address)
    scenario += test_bot.shoot_alien("boss_alien").run(sender = my_address)
    
Tinkering with decision making via if & sp.if in SmartPy
   
  
    import smartpy as sp

class Cryptobot(sp.Contract):
    def __init__(self, manager_address):
        self.init(
            bot_manager = manager_address,
           
            plasma_bullet_count = 5,
           
            record_alien_kills = {
                "simple_alien": sp.nat(0), 
                "boss_alien": sp.nat(0), 
            }
        )

    @sp.entry_point
    def shoot_alien(self, alien_type):
        sp.verify(
            self.data.bot_manager == sp.sender, 
            message = "Error: non manager call"
        )
        
        
        # Using sp.if add a condition to check plasma_bullet_count >= 1
        sp.if self.data.plasma_bullet_count >= 1:    
            self.data.plasma_bullet_count -= 1
            self.data.record_alien_kills[alien_type] += 1
        # Use sp.else to run code when the above condition fails. 
        # Use sp.failwith to return an error message.
        sp.else:
            sp.failwith("Error: you ran out of bullets! Please buy more!")



@sp.add_test(name = "Testing with sp if")
def test():
    scenario = sp.test_scenario()
    
    my_address = sp.address("tz1Syu3KacZ8cy4286a4vaCeoMtwqVKHkaoj")
    
    test_bot =  Cryptobot(manager_address = my_address)
    
    scenario += test_bot
    
    scenario += test_bot.shoot_alien("simple_alien").run(sender = my_address)
    scenario += test_bot.shoot_alien("boss_alien").run(sender = my_address)





    
 
