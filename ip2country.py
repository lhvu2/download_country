import pandas as pd
import requests
import argparse
import ipinfo


def find_country(infile='crawler.csv', debug=False):
    access_token = '9882e61a1e4aa2'
    handler = ipinfo.getHandler(access_token)
    outfile = infile.replace('.csv', "_countries.csv")
    df = pd.read_csv(infile)
    # ips = df['IP'].unique()
    ips = df['IP']
    countries = set()
    ip_list, countries_list = list(), list()
    for idx, ip in enumerate(ips):
        ip_list.append(ip)
        try:
            details = handler.getDetails(ip)
            countries.add(details.country_name)
            countries_list.append(details.country_name)
            print(f"{idx}, ip: {ip}, country: {details.country_name}, number of unique countries: {len(countries)}")
            if debug and idx > 30:
                break
        except Exception as e:
            print(f"{idx}. Fail to get response from ip: {ip}, exception: {e}")
            countries_list.append("no response")
            continue

    df = pd.DataFrame()
    df['IP'] = ip_list
    df['country'] = countries_list
    df.to_csv(outfile, index=False)
    print(f"Saving output file: {outfile}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Get Country from IP")
    parser.add_argument("-i", "--infile", help="input file name", type=str, default="crawler.csv")
    args = parser.parse_args()
    print(f"Infile: {args.infile}")

    # we can assign infile to some file name we want to check
    infiles = ['crawler.csv', 'uim.csv', 'connectivity.csv', 'snapshot.csv']
    for infile in infiles:
        find_country(infile=infile, debug=False)
    print('Done')