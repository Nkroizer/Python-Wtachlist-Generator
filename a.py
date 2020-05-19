# Save a dictionary into a pickle file.
import pickle

# favorite_color = {}

# favorite_color["lion"] = "yellow" 
# favorite_color["kitty"] = "red" 

# # { "lion": "yellow", "kitty": "red" }

# pickle.dump( favorite_color, open( "save.p", "wb" ) )

favorite_color = pickle.load( open( "save.p", "rb" ) ) 
# favorite_color is now { "lion": "yellow", "kitty": "red" }
print(favorite_color["lion"])