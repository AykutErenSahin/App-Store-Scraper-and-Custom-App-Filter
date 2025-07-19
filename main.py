import pandas as pd, requests, csv, json, time, argparse
from datetime import datetime, timedelta

def terminal():
  parser = argparse.ArgumentParser(description="Filter iOS app data using API")
  parser.add_argument("app_list", help="Path to the app list CSV file")
  parser.add_argument("deal_list", help="Path to the deal list CSV file")
  return parser.parse_args()

def filter_apps(apidata):
  now = datetime.now()
  result_count = apidata['resultCount']
  reached_developer_ids = set(Deal_List['developer_id'])

  for i in reversed(range(result_count)):

    developer_id = apidata['results'][i]["artistId"]
    release_date = datetime.strptime(apidata['results'][i]["releaseDate"], "%Y-%m-%dT%H:%M:%SZ")
    last_update_date = datetime.strptime(apidata['results'][i]["currentVersionReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")

    if developer_id in reached_developer_ids:
      del apidata['results'][i]
      continue

    if (now - release_date).days > 365:
      del apidata['results'][i]
      continue

    if (now - last_update_date).days > 90:
      del apidata['results'][i]
      continue

    reached_developer_ids.add(developer_id)

  apidata['resultCount'] = len(apidata['results'])
  return apidata

def set_dataframe(apidata,df):
  result_count = apidata['resultCount']

  for i in range(result_count):
    data = [
        {"app_id": apidata['results'][i]["trackId"],
        "app_name": apidata['results'][i]["trackName"],
        "developer_id": apidata['results'][i]["artistId"],
        "developer_account_name": apidata['results'][i]["artistName"],
        "price": apidata['results'][i]["price"],
        "rating": apidata['results'][i]["averageUserRating"],
        "rating_count": apidata['results'][i]["userRatingCount"],
        "primary_category": apidata['results'][i]["primaryGenreName"],
        "version": apidata['results'][i]["version"],
        "release_date": apidata['results'][i]["releaseDate"],
        "description": apidata['results'][i]["description"],
        "last_update_date": apidata['results'][i]["currentVersionReleaseDate"]}
    ]
    df_data =pd.DataFrame(data)
    df = pd.concat([df, df_data], ignore_index=True)
  return df

def save_to_csv(df):
  with open('Filtered Apps.csv', 'w', newline='') as csvfile:
    df.to_csv(csvfile, index=False)

args = terminal()
App_List = pd.read_csv(args.app_list, sep=";")
Deal_List = pd.read_csv(args.deal_list, sep=";")
api_url = "https://itunes.apple.com/lookup?id="

df = pd.DataFrame()

for i in range(0, len(App_List), 200):
  ids_batch = App_List[i:i+200]['app_id']

  ids_string = ','.join([str(id) for id in ids_batch])
  url = "https://itunes.apple.com/lookup?id=" + ids_string
  response = requests.get(url)
  apidata = response.json()

  apidata = filter_apps(apidata)

  df = set_dataframe(apidata,df)
  time.sleep(1)

save_to_csv(df)
