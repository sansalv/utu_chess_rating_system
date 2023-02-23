import save_and_load as sl
import player
import game
"""
Library for data input methods:

input_tournament() 
input_games()
"""

#_______________________________________________________________________
# Tournament data input. Creates games and players from csv data and updated databases.

# TODO: Comment the end section of this
def input_tournament(source_file, level):
	#___________________________________
	# Info of the tournament

	print(f"\nInput tournament from file {source_file} started.")
	file_location = f"tournament_data/{source_file}"
	date = source_file.split("_")[0]
	#___________________________________
	# Load old players from database
	all_players = sl.load_players() # After this old players but later also new players will be appended

	#___________________________________
	# Check and create new players:

	# Creates lists of player names from database and list of names from csv table
	old_players_names = [p.name for p in all_players]
	tournament_player_names = player.get_players_from_table(file_location)	

	# Check if new players
	if not all(p in old_players_names for p in tournament_player_names):
		# New players found. Creates list of new names and prints
		new_player_names = []
		print(f"\nNew level {level} players found:")
		for name in tournament_player_names:
			if name not in old_players_names:
				new_player_names.append(name)
				print(name)
		for name in new_player_names:
			new_player = player.newPlayer(name, level)
			all_players.append(new_player)
	#___________________________________

	# Filter all players to tournament players
	tournament_players = [p for p in all_players if p.name in tournament_player_names]

	# csv to list of Game instances and save games to json database
	raw_game_list = game.from_table_to_games_list(file_location)
	games = game.game_lists_to_game_instances(date, raw_game_list, tournament_players, source_file)
	sl.save_new_games(games)
	print("\nSaved games to game_database.json successfully.")

	# Calculate and update Elos and Elo histories
	for p in tournament_players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)

	# Save all players back into json database
	sl.save_players(all_players)
	print("Updated players to players_database.json successfully.")
	input("\nPress enter to continue.")


def input_games(free_games_csv_pair):

	source_file = free_games_csv_pair[0]
	source_file_location = f"free_rated_games_data/{source_file}"
	new_players_file = free_games_csv_pair[1]
	new_players_file_location = f"free_rated_games_data/{new_players_file}"

	#___________________________________
	# Info of the free rated games

	print(f"\nInput free rated games from file {source_file} started.")
	date = source_file.split("_")[0]
	#___________________________________

	# Load old players from database
	all_players = sl.load_players() # After this old players but later also new players will be appended
	#___________________________________
	# Create new players:

	# TODO: Eliaksen koodista nämä
	new_player_names_with_level = player.get_new_players_with_level_from_games_csv(new_players_file_location)

	print("\nNew players:")
	for name_level in new_player_names_with_level:
		name = name_level[0]
		level = name_level[1]
		print(f"{name}, starting level: {level}")
		all_players.append(player.newPlayer(name, level))
	#___________________________________

	# Filter all players to present players
	present_player_names = player.get_unique_players_from_games_csv(source_file_location)
	present_players = [p for p in all_players if p.name in present_player_names]

	# csv to list of Game instances and save games to json database
	raw_game_list = game.from_games_csv_to_games_list(source_file_location)
	games = game.game_lists_to_game_instances(date, raw_game_list, present_players, source_file)
	sl.save_new_games(games)
	print("\nSaved games to game_database.json successfully.")

	# Calculate and update Elos and Elo histories
	for p in present_players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)

	# Save all players back into json database
	sl.save_players(all_players)
	print("Updated players to players_database.json successfully.")
	input("\nPress enter to continue.")