import pandas as pd



def load_games(input_file):

    def make_dict(input_colours):
        color_dict = {}
        colors = input_colours.split(',')
        for color in colors:
            split_color = color.split(' ')
            color_dict[split_color[-1]] = int(split_color[1])
        return color_dict
    
  

    with open(input_file) as f:
        lines = f.readlines()

    games_list =[]
    for line in lines:
        games = {}
        colon_split = line.strip("\n").split(":")
        games['game_id'] = int(colon_split[0].split(" ")[-1])
        games['unedited_turns'] = colon_split[-1].split(';')
        games['turns'] = [make_dict(x) for x in games['unedited_turns']]
        games_list.append(games)
        #print(games_list)
    games_df = pd.DataFrame(games_list)
    return games_df

def find_possible_games(games, bag):
    def _game_is_possible(x,bag):
        output = 0
        for item in x:
            for key in item.keys():
                if item[key] > bag[key]:
                    output += 1
                else:
                    output += 0
        return output

    games['possible_games'] = games.turns.apply( lambda x :_game_is_possible(x, bag))

def find_cube_count(turns):
    cubes = {'blue':[], 'red': [], 'green':[]}
    for item in turns:
        for key in item.keys():
            cubes[key].append(item[key])
    return cubes

if __name__ == '__main__':

    #Part 1
    bag = {'red': 12, 'blue': 14, 'green': 13 }
    games = load_games('./game_inputs')
    find_possible_games(games, bag)
    possible_games = games[games.possible_games == 0]
    
    print('* part one *')
    print(games.columns)  
    print(possible_games.head())
    print(possible_games.game_id.sum())

    #Part 2
    # Create a column for each color with a list of the no. cubes drawn each turn for all turns in a game
    games['cube_count']= games.turns.apply(find_cube_count)
    games[['blue', 'red', 'green']] = games.cube_count.apply(pd.Series)

    # find the max of each colour
    games['blue_max'] = games.blue.apply(lambda x: max(x))
    games['red_max'] = games.red.apply(lambda x: max(x))
    games['green_max'] = games.green.apply(lambda x: max(x))

    # find the power
    games['power'] = games.blue_max*games.red_max*games.green_max

    print('* part 2 *')
    print(games[['turns','cube_count']])
    print(games.power.sum())

  