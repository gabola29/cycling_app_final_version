# Created by Gabriel Letty

import streamlit as st
import pandas as pd
import plotly.express as px
import random


# Title + property + intro
st.set_page_config(
    page_title="2020 cycling app",
    layout="wide"
)

st.title("2020 Best Cycling Riders")

st.write("This app, allow you to have an overview on 2020 Men Cycling season and do some visualisation of riders "
         "characteristics and riders performances.")

st.write("To avoid a too long page, most of the graphs and statistics are hidden with expanders : click on the + to "
         "fully displaying it. More infos, about how to use the app, are written on the left sidebar !")

st.write("Hope you enjoy it !!")

st.write("--------")


# data loading
@st.cache
def loading_data():

    loaded_data = pd.read_csv("./data/final_db_cyling2020.csv", sep=',', encoding='utf8')

    return loaded_data


df = loading_data()

# Creating the sidebar :

st.sidebar.subheader("More information :")

st.sidebar.write("All the graph are made with plotly, this mean they are all interactive : you can zoom in (or out),"
                 "select only a part of the graph and by moving the mouse over you'll have information about the data")

st.sidebar.write("For the select box (simple or multiselect), click on it to show the drop-down list and select what "
                 "you want."
                 "Also, you can just type the value you're looking for, "
                 "instead of scrolling indefinitely")

st.sidebar.write('----------------------')

st.sidebar.write('Choose one rider in the selectbox: ')


# All the functions and dataframe manipulations :

numerical_columns = list(df.columns.values)
numerical_columns.remove('Team')
numerical_columns.remove('Cycliste')
numerical_columns.remove('Nationality')
numerical_columns.remove('All_time_rank')


@st.cache
def filling_tab_comparison(col, df_rider_a, df_rider_b):

    # on recupère la col qui nous faut
    ra_value = round(df_rider_a[col].iloc[0], 2)
    rb_value = round(df_rider_b[col].iloc[0], 2)

    # comparaison des resultats
    if ra_value > rb_value:
        sign = '>'
        real_ra_value = "**{}**".format(ra_value)
        real_rb_value = rb_value
    elif ra_value == rb_value:
        sign = '='
        real_ra_value = ra_value
        real_rb_value = rb_value
    else:
        sign = '<'
        real_rb_value = "**{}**".format(rb_value)
        real_ra_value = ra_value

    # on stock dans un truc que l'on renvoit
    final_dico = {
        "ra_value": real_ra_value,
        "rb_value": real_rb_value,
        "sign": sign
    }

    return final_dico


@st.cache
def show_rider_stats(rider, data=df):

    rider_data = data[data["Cycliste"] == rider]

    return rider_data


@st.cache
def show_team_stats(team, data=df):

    team_data = data[data["Team"] == team]
    team_data.sort_values(by=['Points', 'Wins'], ascending=False, inplace=True)
    team_data.reset_index(drop=True, inplace=True)

    return team_data


@st.cache
def show_nation_stats(nation, data=df):

    nation_data = data[data["Nationality"] == nation]
    nation_data['win_rank'] = nation_data['Wins'].rank(method='min', ascending=False)
    nation_data['point_rank'] = nation_data['Points'].rank(method='min', ascending=False)
    nation_data['top_10_rank'] = nation_data['Top_10'].rank(method='min', ascending=False)

    return nation_data


def func1():

    # to avoid weird message, with drop na
    df_bis = df.dropna()

    cols_for_random_comparison = ['Km', 'Racedays', 'Points', 'Weight', 'GT_Classic_Participation']
    random_riders = random.sample(list(df_bis['Cycliste']), 2)

    selected_col = random.choice(cols_for_random_comparison)

    r_value_1 = df_bis[selected_col].loc[df_bis['Cycliste'] == random_riders[0]].iloc[0]
    r_value_2 = df_bis[selected_col].loc[df_bis['Cycliste'] == random_riders[1]].iloc[0]

    rider1 = df_bis['Cycliste'][df_bis['Cycliste'] == random_riders[0]].iloc[0]
    rider2 = df_bis['Cycliste'][df_bis['Cycliste'] == random_riders[1]].iloc[0]

    diff_value = r_value_1 - r_value_2
    if diff_value > 0:
        operateur = 'more'
        msg_value = diff_value
    elif diff_value == 0:
        operateur = 'more'
        msg_value = diff_value
    else:
        operateur = 'less'
        msg_value = abs(diff_value)

    if selected_col == 'Km':
        msg = "{} rode {} km {} than {} in 2020 !".format(rider1, msg_value, operateur, rider2)
    elif selected_col == 'Racedays':
        msg = "{} rode {} days {} than {} in 2020 !".format(rider1, msg_value, operateur, rider2)
    elif selected_col == 'Points':
        msg = "{} score {} points {} than {} in 2020 !".format(rider1, msg_value, operateur, rider2)
    elif selected_col == 'Weight':
        msg = "{} weighs {} kg {} than {} !".format(rider1, msg_value, operateur, rider2)
    else:
        msg = "{} have {} {} GT + classic participation than {} !".format(rider1, msg_value, operateur, rider2)

    return msg


# Intro :

# global overview

st.write("A total of ", len(df), "riders are present in the dataset, from ", len(list(set(df['Nationality']))),
         " countries and ", len(list(set(df['Team']))), " Teams.")

st.write("The average rider is :", round(df['Age'].mean(), 2), "years old", ", weight", round(df['Weight'].mean(), 2),
         "kilos,", "and height", round(df['Height'].mean(), 2), "meter.")

st.write("All riders combine, rode a total of ", df['Km'].sum(), "kms in 2020.")

st.write("------")
st.write("Here is an quick overview of riders characteristics :")

fig3 = px.scatter_3d(data_frame=df, x='Age', y='Weight', z="Height", color='Points', size='Wins',
                     hover_name='Cycliste', title='This graph represent the type of riders in 3 axis : their age, '
                                                  'weight and height.')
st.plotly_chart(fig3, use_container_width=True)


st.write("-------")
st.subheader(" Below you'll have a quick overview of the top rider in several statistics :")

best = df[df['Points'] > 300]

fig = px.scatter(data_frame=best, x='top10_percent', y='Racedays', color='Points', size='Wins',
                 hover_name='Cycliste', title='This graph represent the best riders performance in 2020')
st.plotly_chart(fig, use_container_width=True)

# stats calculation:

# max points
id_max_points = df['Points'].idxmax()
st.write(df['Cycliste'].iloc[id_max_points], 'is the rider who scores the maximum points in 2020, with a total of :',
         df['Points'].max(), ' points !')

# max wins
id_max_wins = df['Wins'].idxmax()
st.write(df['Cycliste'].iloc[id_max_wins], 'is the rider with the most wins in 2020, with a total of :',
         df['Wins'].max(), ' wins !')

# max kms
id_max_kms = df['Km'].idxmax()
st.write(df['Cycliste'].iloc[id_max_kms], 'is the rider who rode the maximum kilometers in 2020, with a total of :',
         df['Km'].max(), ' kms !')

# max top 10
id_max_top10 = df['Top_10'].idxmax()
st.write(df['Cycliste'].iloc[id_max_top10], 'is the rider with the most top 10 finish in 2020, with a total of :',
         df['Top_10'].max(), ' top 10 !')

# max racedays
id_max_racedays = df['Racedays'].idxmax()
st.write(df['Cycliste'].iloc[id_max_racedays], 'is the rider with the most racedays in 2020, with a total of :',
         df['Racedays'].max(), ' racedays !')


st.write("-------")
st.subheader("For the folowing parts, click on the message or on the + to expand and see more charts and statistics")


# Part 1 : Rider Comparison :

with st.expander("Click here to expand and see a comparison between two rider"):

    rider_a = st.selectbox('Rider 1 :', options=df['Cycliste'], key='rider1')
    rider_b = st.selectbox('Rider 2:', options=df['Cycliste'], key='rider2')

    stat_for_comparison = st.multiselect(label="Select between 1 and unlimited features for comparison. You can add to"
                                               "the defaults ones, note that too many features at the time will"
                                               "decrease loading time performances.",
                                         options=numerical_columns, default=['Age', 'Wins', 'Points',
                                                                             'Top_10', 'top10_percent',
                                                                             'Points_per_days', 'Racedays',
                                                                             'Gt_Participation',
                                                                             'Classic_Participation'])

    comparison_cols = st.columns(4)
    comparison_cols[0].write(".")
    comparison_cols[2].write(rider_a)
    comparison_cols[3].write(rider_b)

    data_copy = df.copy()
    ra_df = data_copy.loc[df['Cycliste'] == rider_a]
    rb_df = data_copy.loc[df['Cycliste'] == rider_b]

    for i in stat_for_comparison:
        comparison_cols[0].write(i)
        calculation_dict = filling_tab_comparison(col=i, df_rider_a=ra_df, df_rider_b=rb_df)
        with comparison_cols[2]:
            st.markdown(calculation_dict['ra_value'])
        with comparison_cols[3]:
            st.markdown(calculation_dict['rb_value'])


# Part 2 : Team description :

with st.expander("To see an unique team stats, see below and select the on you want"):

    selected_team = st.selectbox(label='Select a team', options=list(set(df['Team'])))

    team_stats = show_team_stats(team=selected_team)
    st.write(team_stats)

    nationality_repartition = px.pie(data_frame=team_stats, names='Nationality')

    st.subheader('Nationality repartition in the team:')
    st.plotly_chart(nationality_repartition, use_container_width=True)

    # some stats :
    st.subheader("Some stats about the team :")
    # we create 2 cols
    team_c1, team_c2 = st.columns(2)

    # aggregated statistics:

    # the first col :
    with team_c1:
        st.write('Total wins in 2020 :', team_stats['Wins'].sum())
        # total gt participation
        st.write('Total GT participation :', team_stats['Gt_Participation'].sum())
        # average wins rider
        st.write("Average wins per rider :", round(team_stats['Wins'].mean(), 2))
        # average number of top 10
        st.write("Average number of 10 per rider :", round(team_stats['Top_10'].mean(), 2))

    # the second col
    with team_c2:
        # total top 10
        st.write('Total top 10 in 2020 :', team_stats['Top_10'].sum())
        # total classic participation
        st.write('Total Classics participation :', team_stats['Classic_Participation'].sum())
        # average racedays
        st.write('Average racedays by rider :', team_stats['Racedays'].mean())
        # average age
        st.write("Average rider's age :", round(team_stats['Age'].mean(), 2))

    best_rider = px.bar(team_stats, x='Points', y='Cycliste', orientation='h')

    st.subheader('Best riders in 2020 :')
    st.plotly_chart(best_rider, use_container_width=True)

    # best riders (below the graph)
    # we recreating 2 cols:
    st.write("------")
    c1_team_br, c2_team_br = st.columns(2)

    with c1_team_br:
        st.write("Rider with the most wins :", team_stats['Cycliste'].iloc[team_stats['Wins'].idxmax()], '(',
                 team_stats['Wins'].max(), ' )')

        st.write("Rider with most points scored :", team_stats['Cycliste'].iloc[team_stats['Points'].idxmax()], '(',
                 team_stats['Points'].max(), ' )')

        st.write("Youngest rider :", team_stats['Cycliste'].iloc[team_stats['Age'].idxmin()], '(',
                 team_stats['Age'].min(), ' )')

    with c2_team_br:
        st.write("Rider with the most top 10 :", team_stats['Cycliste'].iloc[team_stats['Top_10'].idxmax()], '(',
                 team_stats['Top_10'].max(), ' )')

        st.write('Rider with the most racedays :', team_stats['Cycliste'].iloc[team_stats['Racedays'].idxmax()], '(',
                 team_stats['Racedays'].max(), ' )')

        st.write("Oldest rider : ", team_stats['Cycliste'].iloc[team_stats['Age'].idxmax()], '(',
                 team_stats['Age'].max(), ' )')

# Part 3 : Team Comparison:
with st.expander("Click here to see teams comparison"):

    st.subheader('Here is some visualisations of teams differences :')

    age_disparity_by_teams = px.box(df, y='Age', x='Team', color="Team")
    age_disparity_by_teams.update_layout(showlegend=False)
    st.write('Age dispersion, among the several teams')
    st.plotly_chart(age_disparity_by_teams, use_container_width=True)

    team_sum = df.groupby('Team').sum()
    team_sum.reset_index(drop=False, inplace=True)
    team_sum.sort_values(by=['Points'], ascending=False, inplace=True)

    team_point_rank = px.bar(team_sum, x='Points', y='Team', orientation='h')
    st.write("Teams total points :")
    st.plotly_chart(team_point_rank, use_container_width=True)

    point_sorted = team_sum.copy().sort_values(by=['Wins'], ascending=False)
    team_win_rank = px.bar(point_sorted, x='Wins', y='Team', orientation='h')
    st.write("Teams total wins :")
    st.plotly_chart( team_win_rank, use_container_width=True)

# Part 4 : Nation Description :

with st.expander("To see an unique nation stats, see below and select the one you want"):

    selected_nation = st.selectbox(label='Select a nationality', options=list(set(df['Nationality'])))

    nation_stats = show_nation_stats(nation=selected_nation)

    st.write(nation_stats)

    # global stats:
    # we create to cols for a better display

    nation_c1, nation_c2 = st.columns(2)

    with nation_c1:
        st.write('Total of Riders :', len(nation_stats))
        st.write('Total wins :', nation_stats['Wins'].sum())
        st.write('Total points :', nation_stats['Points'].sum())
        st.write('Total top 10:', nation_stats['Top_10'].sum())

    with nation_c2:
        st.write('Average wins :', round(nation_stats['Wins'].mean(), 2))
        st.write('Average points :', round(nation_stats['Points'].mean(), 2))
        st.write('Average Top 10 :', round(nation_stats['Top_10'].mean(), 2))

    team_repartition = px.pie(data_frame=nation_stats, names='Team')

    st.write('Rider repartition by team :')
    st.plotly_chart(team_repartition, use_container_width=True)
    # rajouter histogramme customable des différentes stats

    st.write('Rider with the most wins :', nation_stats['Cycliste'].loc[nation_stats['win_rank'] == 1].iloc[0],
             ' (', nation_stats['Wins'].loc[nation_stats['win_rank'] == 1].iloc[0], ')')
    st.write('Rider with the most Points :', nation_stats['Cycliste'].loc[nation_stats['point_rank'] == 1].iloc[0],
             ' (', nation_stats['Points'].loc[nation_stats['point_rank'] == 1].iloc[0], ')')
    st.write('Rider with the most Top 10 :', nation_stats['Cycliste'].loc[nation_stats['top_10_rank'] == 1].iloc[0],
             ' (', nation_stats['Top_10'].loc[nation_stats['top_10_rank'] == 1].iloc[0], ')')


# Part 4 : The custom scatter plot :

st.write('----------')

st.write("Below, you can create a completely custom scatter plot. You can change both axis, add color to the points or "
         "adjust the size of the points according to columns value.""Also, with slidebar below the graph, you can "
         "filter the rider you want to display !")

# Adding "None" to the numerical columns

optionnal_columns = numerical_columns.copy()
optionnal_columns.append('None')
none_pos = optionnal_columns.index('None')

x_axis = st.selectbox(label='Select a feature for X axis', options=numerical_columns, key="x_axis_graph")
y_axis = st.selectbox(label='Select a feature for Y axis', options=numerical_columns, key="y_axis_graph")

color_choice = st.selectbox(label='Select a feature for the color', options=optionnal_columns,
                            key="color_graph", index=none_pos)

size_choice = st.selectbox(label='Select a feature for the size', options=optionnal_columns, key="size_graph",
                           index=none_pos)

container = st.container()
container.write("Here is the graph : more filter options are available below")

# on passe au filtre (d'abord sans faire de graphs juste pour voir si cela fonctionne
# idée filtre : age, Weight, points, wins, racedays,


wins_filter = st.slider(label='You can adjust the slider to filter the number of victories per rider',
                        min_value=int(df['Wins'].min()), max_value=int(df['Wins'].max()), value=(int(df['Wins'].min()),
                                                                                                 int(df['Wins'].max())))
age_filter = st.slider(label="You can adjust the slider to filter rider's age", min_value=int(df['Age'].min()),
                       max_value=int(df['Age'].max()), value=(int(df['Age'].min()), int(df['Age'].max())))

weight_filter = st.slider(label="You can adjust the slider to filter rider's weight (kg)",
                          min_value=int(df['Weight'].min()), max_value=int(df['Weight'].max()),
                          value=(int(df['Weight'].min()), int(df['Weight'].max())))

team_filter = st.multiselect(label="Select rider's team (you can choose multiple)", options=list(set(df['Team'])),
                             key="team_custom_graph")

nation_filter = st.multiselect(label="Select rider's nation (you can choose multiple)",
                               options=list(set(df['Nationality'])), key="nation_custom_graph")


# creating the adjusted df according to the criteria:

custom_df = df.copy()

# adjusting team
if len(team_filter) == 0:
    pass
else:
    custom_df = custom_df[custom_df['Team'].isin(team_filter)]

# adjusting country
if len(nation_filter) == 0:
    pass
else:
    custom_df = custom_df[custom_df['Nationality'].isin(nation_filter)]


# adjusting number of wins
custom_df = custom_df.loc[(custom_df['Wins'] >= wins_filter[0]) & (custom_df['Wins'] <= wins_filter[1])]

# adjusting weights
custom_df = custom_df.loc[(custom_df['Weight'] >= weight_filter[0]) & (custom_df['Weight'] <= weight_filter[1])]

# adjusting age
custom_df = custom_df.loc[(custom_df['Age'] >= age_filter[0]) & (custom_df['Age'] <= age_filter[1])]

# warning if no rider match criteria
if len(custom_df) == 0:
    container.warning('Watch out, no rider match your criteria !')


if color_choice == 'None':
    real_color_choice = None
else:
    real_color_choice = color_choice

if size_choice == 'None':
    real_size_choice = None
else:
    real_size_choice = size_choice

custom_fig = px.scatter(data_frame=custom_df, x=x_axis, y=y_axis, hover_name='Cycliste', color=real_color_choice,
                        size=real_size_choice)
# container.write(custom_fig)
container.plotly_chart(custom_fig, use_container_width=True)

st.write('------')

# rider stats in sidebar

selected_rider = st.sidebar.selectbox(label='Select a rider', options=df['Cycliste'], key="sidebar_rider_selector")

rider_stats = show_rider_stats(rider=selected_rider)

st.sidebar.write('Nationality :', rider_stats['Nationality'].iloc[0])
st.sidebar.write('Team :', rider_stats['Team'].iloc[0])
st.sidebar.write('Age :', rider_stats['Age'].iloc[0])
st.sidebar.write('Height :', rider_stats['Height'].iloc[0])
st.sidebar.write('Weight :', rider_stats['Weight'].iloc[0])
st.sidebar.write('Racedays :', rider_stats['Racedays'].iloc[0])
st.sidebar.write('Kms :', rider_stats['Km'].iloc[0])
st.sidebar.write('Wins :', rider_stats['Wins'].iloc[0])
st.sidebar.write('Top 10 :', rider_stats['Top_10'].iloc[0])
st.sidebar.write('Points :', rider_stats['Points'].iloc[0])

# Final part features description:
with st.expander('Feature description'):

    st.write('soon !')

# place au bouton qui génère des randoms stats :

st.sidebar.write('---------')

st.sidebar.write('Click on the button below to generate random (but true !!) statistic or comparison')

if st.sidebar.button(label="Click here"):

    # func 1 : random comparison
    st.sidebar.write(func1())
    st.sidebar.write('-------')

    # func 2 : random stats

    # func 3 : random first
