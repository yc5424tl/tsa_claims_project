import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import requests
import os
import matplotlib
from pandas import ExcelWriter
from pandas import ExcelFile

# Claim Number
# Date Received
# Incident Date
# Airport Code
# Airport Name
# Claim Type
# Claim Site
# Item
# Claim Amount
# Status
# Close Amount
# Disposition

# print('Python version' + sys.version)
# print('Pandas version' + pd.__version__)
# print('Matplotlib version ' + matplotlib.__version__)

df = pd.read_excel('E:/Code/Python/TSA Claims Project/DataSets/claims-2002-2006.xls')
df = df[(df['Airport Name'] != 'Civil Aviation, Non TSA manned Airport') &
        (df['Airport Name'] != 'Insurance Subrogation Claim') &
        (df['Airport Name'] != 'Non TSA Airport (motor vehicle)') &
        (df['Airport Name'] != 'TSA - Non-Specified Airport')]
airport_geocodes = {}
google_maps_api_key = os.environ.get('google_maps_api_key')


def get_airport_names():

    airport_name_array = []

    for i in df.index:

        airport_name = df['Airport Name'][i]

        if airport_name_array.__contains__(airport_name):
            continue
        if pd.isnull(df['Airport Name'][i]):
            continue
        else:
            airport_name_array.append(airport_name)
    for airport in sorted(airport_name_array):
        print(airport)
    return sorted(airport_name_array)


def build_airport_geocodes():

    airports = get_airport_names()
    for airport in airports:
        if airport == 'Albert J Ellis, Jacksonville':
            airport = 'Albert J Ellis'
        if airport == 'Southwest Georgia Regional Airport ,Albany':
            airport = 'Southwest Georgia Regional'
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&amp;key={}'\
            .format(airport + ' airport', google_maps_api_key)
        r = requests.get(url).json()
        lat = r['results'][0]['geometry']['location']['lat']
        lng = r['results'][0]['geometry']['location']['lng']
        # code = get_airport_code_by_airport_name(airport)
        airport_geocodes['airport'] = [lat, lng]  # should include airport code here
        print('=========================')
        print(airport)
        print(lat)
        print(lng)
        print('=========================')
        # print(lng)
        # print(code)


def get_total_claims_by_airport_per_airline():

    df['count'] = 1
    df_group_totals = df.groupby(['Airport Name', 'Airline Name'])['count'].sum()
    # https://stackoverflow.com/a/38503561
    df_sorted_group_totals = df_group_totals.reset_index()\
        .sort_values(['Airport Name', 'count'], ascending=False)\
        .set_index(['Airport Name', 'Airline Name'])
    print(df_sorted_group_totals)


def get_total_claims_by_airline_per_airport():

    df['count'] = 1
    df_group_totals = df.groupby(['Airline Name', 'Airport Name'])['count'].sum()
    df_sorted_group_totals = df_group_totals.reset_index()\
        .sort_values(['Airline Name', 'count'], ascending=False)\
        .set_index(['Airline Name', 'Airport Name'])                             # https://stackoverflow.com/a/42252577
    print(df_sorted_group_totals)


def get_status_approved_by_airport():

    df['count'] = 1
    df_approved_totals = df.groupby(['Airport Name', df['Status'] == 'Approved'])['count'].sum()
    print(df_approved_totals)
    # def get_approved_by_each_airport():
    #
    #     df['count'] = 1
    #     df_approved = df[df['Status'] == 'Approved']
    #     df_approved_totals = df_approved.groupby(['Airport Name', 'Status'])['count'].sum()
    #     print(df_approved_totals)
    # df_approved = df.groupby(['Airport Name', df['Status'] == 'Approved'])
    # df_approved_true = df_approved.apply(lambda g: g[g['Status'] == 'Approved'])
    # print(df.apply(lambda g: g['Status' == 'Approved']))
    # df_approved = df.groupby(['Airport Name', 'Status']).apply(lambda g: g[g['Status'] == 'Approved']).sum()
    # print(df_approved)
    # print(df_approved_true)


def get_status_for_airport(status, airport):
    df['count'] = 1
    # below works but with a warning
    # df_airport = (df[df['Airport Name'] == airport][df['Status'] == 'Approved']).groupby(['Status'])['count'].sum()
    # #df_airport_total = df_airport.groupby(['Status'])['count'].sum()
    # print(df_airport)
    df1 = df.loc[(df['Status'] == status) & (df['Airport Name'] == airport)]
    df2 = df1.groupby(['Status'])['count'].sum()
    print(df2)
    # Below works but with a different warning
    # df_airport = df[df['Airport Name'] == airport]
    # df_airport_status = df_airport[df_airport['Status'] == 'Approved']
    # df_airport_status['count'] = 1
    # df_airport_totals = df_airport_status.groupby(['Status'])['count'].sum()
    # print(df_airport_totals)


def get_total_claims_by_airport():
    df_all_airport_groups = df['Airport Name'].value_counts()
    print(df_all_airport_groups)


def get_total_claims_by_airline():
    df_all_occurrences_by_airline = df['Airline Name'].value_counts()
    print(df_all_occurrences_by_airline)


def get_occurrences_for_airport_by_name(airport_name):
    print(len(df[df['Airport Name'] == airport_name]))


def get_airport_codes():

    airport_code_array = []
    for i in df.index:
        airport_code = df['Airport Code'][i]
        if airport_code_array.__contains__(airport_code):
            continue
        if pd.isnull(df['Airport Code'][i]):
            continue
        else:
            airport_code_array.append(airport_code)
    for airport_code in sorted(airport_code_array):
        print(airport_code)


def get_airport_code_by_airport_name(airport_name):

    for index in range(len(df)):
        if df['Airport Name'][index] == airport_name:
            return df['Airport Code'][index]


def create_test_data_0206(number=1):
    output = []

    for i in range(number):
        print('in loop')
        date_rec_rng = range(41640, 42004)
        rand_date_rec = np.random.choice(date_rec_rng)

        date_inc_rng = pd.date_range(start='1/1/2002', end='12/31/2006')
        rand_date_inc = np.random.choice(date_inc_rng)

        airport = {
                    'ABE': 'Lehigh Valley International Airport, Allentown',
                    'ABI': 'Abilene Regional',
                    'ABQ': 'Albuquerque International Sunport Airport',
                    'ABR': 'Aberdeen Regional Airport',
                    'ABY': 'Southwest Georgia Regional Airport, Albany',
                    'ACK': 'Nantucket Memorial Airport',
                    'ACT': 'Waco Regional Airport;',
                    'ACV': 'Arcata-Eureka',
                    'ACY': 'Atlantic City International',
                    'ADQ': 'Kodiak State Airport',
                    'AEX': 'Alexandria International Airport',
                    'AGS': 'Bush Field',
                    'AKN': 'King Salmon',
                    'ALB': 'Albany International',
                    'ALO': 'Waterloo Municipal Airport',
                    'ALS': 'Alamosa-San Luis Valley Bergman Airport',
                    'AWL': 'Walla Walla Regional Airport',
                    'AMA': 'Rick Husband Amarillo International Airport',
                    'ANC': 'Ted Stevens Anchorage International Airport',
                    'AOO': 'Altoona Blair County',
                    'APF': 'Naples Municipal Airport',
                    'APN': 'Alpena County Regional Airport',
                    'ASE': 'Aspen Pitkin County Sardy Field',
                    'ATL': 'Hartsfield-Jackson Atlanta International Airport',
                    'ATW': 'Outagamie County',
                    'ATY': 'Watertown Municipal Airport',
                    'AUG': 'Augusa State Airport',
                    'AUS': 'Austin-Bergstrom International Airpoirt',
                    'AVL': 'Asheville Regional Airport',
                    'AVP': 'Wilkes-Barre/Scranton International',
                    'AZO': 'Kalamazoo/Battle Creek International',
                    'BDL': 'Bradley International Airport',
                    'BET': 'Bethel Airport',
                    'BFD': 'Bradford Regional',
                    'BFF': 'West Nebraska Regional - William Heilig Field',
                    'BFL': 'Meadows Field, Bakersfield Airport'
                    }
        rand_airport = {airport.get(np.random.random())}

        airline = [
                    'Air Lingus',
                    'Aero California',
                    'Aero Flot',
                    'Aero Lloyd',
                    'Aero Mexico',
                    'Air Canada',
                    'Air China',
                    'Air France',
                    'Air Jamaica',
                    'Air New Zealand',
                    'Air Pacific',
                    'Air Portugal',
                    'Air Tran Airlines(do not use)',
                    'AirTran Airlines',
                    'Alaska Airlines',
                    'Alitalia',
                    'Allegiant Air'
                    ]
        rand_airline = [airline[np.random.randint(low=0, high=len(airline))]]

        claim_type = [
                    'Employee Loss (MPCECA)',
                    'Motor Vehicle',
                    'Passenger Property Loss',
                    'Personal Injury',
                    'Property Damage',
                    ]
        rand_type = [claim_type[np.random.randint(low=0, high=len(claim_type))]]

        claim_site = [
                    'Checked Baggage',
                    'Checkpoint',
                    'Motor Vehicle',
                    'Other'
                    ]
        rand_site = [claim_site[np.random.randint(low=0, high=len(claim_site))]]

        item = [
                'Alcoholic Beverages',
                "Audio - CD's",
                'Clothing - Shoes, belts, accessories, etc.',
                'Bags - Fabric, plastic, etc.(not purses)',
                'Books - Other(Hardcover non-fiction)',
                'Reference books, cookbooks, etc.',
                'Cameras - Digital',
                'Jewelry - Fine',
                "Electrical and Gas Appliances Minor - $200 or less (humidifiers, tv's, etc)",
                "Dishes, Pottery, Glassware, Plasticware"
                ]
        rand_item = [item[np.random.randint(low=0, high=len(item))]]

        claim_amount = range(0, 10000)
        rand_amount = np.random.choice(claim_amount)

        status = [
                'Canceled',
                'Denied',
                'In Litigation',
                'Settled',
                'Insufficient',
                'In Review',
                'Closed as a contractor claim',
                'Approved'
                 ]
        rand_status = [status[np.random.randint(low=0, high=len(status))]]

        output.append(rand_date_inc)
        output.append(rand_date_rec)
        output.append(rand_airline)
        output.append(rand_airport)
        output.append(rand_item)
        output.append(rand_site)
        output.append(rand_status)
        output.append(rand_type)
        output.append(rand_amount)
        print('output = ' + str(output))

    return output


# def read_data_0206():
    # print("Column headings: " + df.columns)
    # get_occurrences_for_airport_by_name('Los Angeles International Airport')
    # get_airport_names()
    # get_airport_codes()
    # get_total_claims_by_airport()
    # get_total_claims_by_airline()
    # get_total_claims_by_airport_per_airline()
    # get_total_claims_by_airline_per_airport()
    # get_status_approved_by_airport()
    # get_approved_by_each_airport()
    # get_status_for_airport('Denied', 'Akron-Canton Regional')
    # get_airport_code_by_airport_name('Rochester, MN')
    #
    # for i in df.index:
    #     #print(df['Airport Code'][i])
    #     if pd.isnull(df['Airport Code'][i]):
    #
    #         print("Airport Name = " + str(df['Item'][i]))
    #
    # print('done with iteration')
    # print(df['Airport Code'])

build_airport_geocodes()
