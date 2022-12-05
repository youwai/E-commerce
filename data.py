import pandas as pd

data = pd.read_excel('/Users/youwai/Desktop/Final Year Project/Dreamshop Master_list (Jan-Jul).xlsx', header=0)

def locate_data(user):
    try:
        temp = data.set_index('Contact Name')

        return temp.loc[[user]][['Order Code', 'SKU', 'Product Category', 'Name']]
    except:
        return None

def transform_matrix(matrix):

    for index, row in matrix.iterrows():
        matrix.loc[index] = row/row.sum()

    return matrix

def pearson_method(selected_users, user_item_matrix):
    users_similarity = user_item_matrix.T.corr()

    selected_users_similarity = users_similarity.loc[selected_users]

    selected_users_similarity.dropna(inplace=True)

    selected_users_similarity.drop(index=selected_users, inplace=True)

    return selected_users_similarity.sort_values(ascending=False)

def filter_item(matrix_with_potential_items, similar_users):
    item_score = {}

    for i in matrix_with_potential_items.columns:
        demand_rating = matrix_with_potential_items[i]

        total = 0

        count = 0

        for user in similar_users.index:
            if pd.isna(demand_rating[user]) == False:
                score = similar_users[user] * demand_rating[user]

                total = total + score
                count = count + 1

        item_score[i] = total/count

    demand_ratings_score = pd.DataFrame(item_score.items(), columns=['SKU', 'demand_ratings_score'])

    ranked_demand_ratings_score = demand_ratings_score.sort_values(by='demand_ratings_score', ascending=False)

    return ranked_demand_ratings_score.head(10)


def recommendation(user):
    df = pd.read_csv('./data.csv')

    df['count'] = 1
    df = df.groupby(['Contact Name', 'SKU']).count()

    df.reset_index(inplace=True)

    matrix = df.pivot_table(index='Contact Name', columns='SKU', values='count')

    matrix_transform = transform_matrix(matrix)

    # Validation Purpose
    print('Calculating...')

    similarity_selected_users = pearson_method(user, matrix_transform)

    if len(similarity_selected_users) > 10:
        thres = similarity_selected_users[9]

        similar_users = similarity_selected_users[similarity_selected_users >= thres]
    
    else:
        similar_users = similarity_selected_users

    matrix_similar_users = matrix_transform.loc[similar_users.index]

    matrix_with_potential_items = matrix_similar_users.dropna(axis=1, how='all')    

    top_items = filter_item(matrix_with_potential_items, similar_users)

    return top_items

def pass_recommendation(user):
    try:
        items = recommendation(user)

        print('Done...')

        temp = data.set_index('SKU')

        result = temp.loc[items['SKU'].tolist()].reset_index()

        return result[['SKU', 'Product Category', 'Name']].drop_duplicates()

    except:
        return None