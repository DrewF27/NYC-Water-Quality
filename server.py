from flask import Flask
from flask import render_template
import json
import statistics

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    f = open("data/macro.json", "r")
    data = json.load(f)
    f.close()

    brs = []
    for b in data:
            if b not in brs:
                brs.append(b)

    return render_template('about.html', brs = brs, b = b)


@app.route('/macro')
def macro():
    f = open("data/macro.json", "r")
    data = json.load(f)
    f.close()

    brs = []
    for b in data:
            if b not in brs:
                brs.append(b)
    
    f = open("data/micro.json", "r")
    data2 = json.load(f)
    f.close()
   
    bronx_list = []
    brooklyn_list = []
    manhattan_list = []
    queens_list = []
    staten_island_list = []

    #Formats zip code data
    copper = 0
    lead = 0
    for zipcode, boroughs in data2.items():
        for borough, data in boroughs.items():
            if borough == "Bronx":
                for i in data:
                    copper = float(data[i][1])
                    lead = float(data[i][0])
                    bronx_list.append({zipcode: {'lead': lead, 'copper': copper}})
                    
            if borough == "Brooklyn":
                for i in data:
                    copper = float(data[i][1])
                    lead = float(data[i][0])
                    brooklyn_list.append({zipcode: {'lead': lead, 'copper': copper}})
            if borough == "Manhattan":
                for i in data:
                    copper = float(data[i][1])
                    lead = float(data[i][0])
                    manhattan_list.append({zipcode: {'lead': lead, 'copper': copper}})
            if borough == "Queens":
                for i in data:
                    copper = float(data[i][1])
                    lead = float(data[i][0])
                    queens_list.append({zipcode: {'lead': lead, 'copper': copper}})
            if borough == "Staten Island":
                for i in data:
                    copper = float(data[i][1])
                    lead = float(data[i][0])
                    staten_island_list.append({zipcode: {'lead': lead, 'copper': copper}})
    borough_lists = {
        "Bronx": bronx_list,
        "Brooklyn": brooklyn_list,
        "Manhattan": manhattan_list,
        "Queens": queens_list,
        "Staten Island": staten_island_list
    }




    borough_averages = {}
    for borough in borough_lists:
        lead_sum = 0
        copper_sum = 0
        zip_count = len(borough_lists[borough]) 
        for entry in borough_lists[borough]:
            for _, metals in entry.items():
                lead_sum += float(metals['lead'])
                copper_sum += float(metals['copper'])
            lead_avg = lead_sum / zip_count
            copper_avg = copper_sum / zip_count
            combined_avg = round(lead_avg + copper_avg, 3)
        borough_averages[borough] = combined_avg
    return render_template('macro.html', brs = brs, b=b, borough_averages = borough_averages)


@app.route('/micro/<borough_name>')

def micro(borough_name):
    f = open("data/macro.json", "r")
    data = json.load(f)
    f.close()

    brs = []
    for b in data:
            if b not in brs:
                brs.append(b)
    

    f = open("data/micro.json", "r")
    data2 = json.load(f)
    f.close()

    borough_lists = {
    "Bronx": [],
    "Brooklyn": [],
    "Manhattan": [],
    "Queens": [],
    "Staten Island": []
    }
    # Process data for each borough
    for zipcode, boroughs in data2.items():
        for borough, data in boroughs.items():
            for i in data:
                copper = float(data[i][1])
                lead = float(data[i][0])
                borough_lists[borough].append({zipcode: {'lead': lead, 'copper': copper}})
    
    #Calculates averages for each borough
    borough_averages = {}
    for borough in borough_lists:
        lead_sum = 0
        copper_sum = 0
        zip_sum = len(borough_lists[borough])
        for i in borough_lists[borough]:
            for outer, metals in i.items():
                lead_sum += (float(metals['lead']))
                copper_sum += (float(metals['copper']))
            lead_avg = round(lead_sum / zip_sum, 3)
            copper_avg = round(copper_sum / zip_sum, 3)
        borough_averages[borough] = {'lead': lead_avg, 'copper': copper_avg}
    



    #Gets zip codes with top 5 largest lead values per borough
    t5_lead_zips = {}
    used_zip_codes = set()
    total_lead_sum = 0
    total_copper_sum = 0
    borough_count = 0
    
    for borough, borough_list in borough_lists.items():
        zips = []
        
        for b in borough_list:
            for zipcode, metals in b.items():
                if zipcode not in used_zip_codes:
                    zips.append((metals['lead'], zipcode))

        #lambda defined as function that finds lead value. zips.sort then sorts by lead value
        zips.sort(reverse=True, key=lambda x: x[0])
        top_5 = []
        for _, zip in zips:
            if zip not in used_zip_codes:
                top_5.append(zip)
                used_zip_codes.add(zip)
            if len(top_5) == 5:
                break 


        t5_lead_zips[borough] = top_5
        total_lead_sum += lead_avg
        total_copper_sum += copper_avg
        borough_count += 1
    #Gets zip codes with top 5 largest lead values per borough
    t5_copper_zips = {}
    used_zip_codes = set()
    total_lead_sum = 0
    total_copper_sum = 0
    borough_count = 0
   
   
    for borough, borough_list in borough_lists.items():
        zips = []
        
        for b in borough_list:
            for zipcode, metals in b.items():
                if zipcode not in used_zip_codes:
                    zips.append((metals['copper'], zipcode))
        #lambda defined as function that finds copper value. zips.sort then sorts by copper value
        zips.sort(reverse=True, key=lambda x: x[0])
        top_5 = []
        for _, zip in zips:
            if zip not in used_zip_codes:
                top_5.append(zip)
                used_zip_codes.add(zip)
            if len(top_5) == 5:
                break 


        t5_copper_zips[borough] = top_5
        total_lead_sum += lead_avg
        total_copper_sum += copper_avg
        borough_count += 1



    #Averages across all boroughs
    ny_lead_avg = float(round(total_lead_sum / borough_count, 3))
    ny_copper_avg = float(round(total_copper_sum / borough_count, 3))

    



    #Gets bar data for top 5 copper and lead zips needed for svg graphs
    all_borough_lead_bars = {}
   
    all_borough_copper_bars = {}
    for borough, borough_list in borough_lists.items():
        borough_data = {}
       
       
        for i in borough_list:
            for zipcode, metals in i.items():
                if zipcode not in borough_data:
                    borough_data[zipcode] = {'lead': 0, 'copper': 0}
                borough_data[zipcode]['lead'] = max(borough_data[zipcode]['lead'], metals['lead'])
                borough_data[zipcode]['copper'] = max(borough_data[zipcode]['copper'], metals['copper'])
        top_5_lead = sorted(borough_data.items(), key=lambda item: item[1]['lead'], reverse=True)[:5]
        top_5_copper = sorted(borough_data.items(), key=lambda item: item[1]['copper'], reverse=True)[:5]
        all_borough_lead_bars[borough] = {zipcode: data for zipcode, data in top_5_lead}
        all_borough_copper_bars[borough] = {zipcode: data for zipcode, data in top_5_copper}

    #Gets bar data for top five lead  and copper zip codes
    lead_percentage_diffs = {}
    copper_percentage_diffs = {}
    for borough in all_borough_lead_bars:
        lead_zip_diffs = {}
        copper_zip_diffs = {}
        for zip_code, data in all_borough_lead_bars[borough].items():
            lead_val = float(data['lead'])
            lead_p_diff = round(((lead_val - ny_lead_avg) / ny_lead_avg) * 100, 2)
            lead_zip_diffs[zip_code] = lead_p_diff
        for zip_code, data in all_borough_copper_bars[borough].items():
            copper_val = float(data['copper'])
            copper_p_diff = round(((copper_val - ny_copper_avg) / ny_copper_avg) * 100, 2)
            copper_zip_diffs[zip_code] = copper_p_diff
        lead_percentage_diffs[borough] = lead_zip_diffs
        copper_percentage_diffs[borough] = copper_zip_diffs
    boroughs_pl_dict = {
    'Bronx': lead_percentage_diffs.get('Bronx', {}),
    'Brooklyn': lead_percentage_diffs.get('Brooklyn', {}),
    'Manhattan': lead_percentage_diffs.get('Manhattan', {}),
    'Queens': lead_percentage_diffs.get('Queens', {}),
    'Staten Island': lead_percentage_diffs.get('Staten Island', {})
    }
    boroughs_pc_dict = {
    'Bronx': copper_percentage_diffs.get('Bronx', {}),
    'Brooklyn': copper_percentage_diffs.get('Brooklyn', {}),
    'Manhattan': copper_percentage_diffs.get('Manhattan', {}),
    'Queens': copper_percentage_diffs.get('Queens', {}),
    'Staten Island': copper_percentage_diffs.get('Staten Island', {})
    }
    borough_t5_pl_diff_avgs={}
    for borough in boroughs_pl_dict:
        lead_sum = 0
        for zip in boroughs_pl_dict[borough]:
                    lead_sum += float(boroughs_pl_dict[borough][zip])
                    
                    if borough == "Manhattan":
                        lead_avg = round(lead_sum /3,3)

                    else: lead_avg = round(lead_sum /5,3)
        borough_t5_pl_diff_avgs[borough] = lead_avg

    borough_t5_pc_diff_avgs={}


    for borough in boroughs_pc_dict:
        copper_sum = 0
        for zip in boroughs_pc_dict[borough]:
                    copper_sum += float(boroughs_pc_dict[borough][zip])
                    if borough == "Manhattan":
                        copper_avg = round(copper_sum /3, 3)

                    else: copper_avg = round(copper_sum /5, 3)

        borough_t5_pc_diff_avgs[borough] = copper_avg
    #print(borough_t5_pc_diff_avgs['Manhattan'])


    boroughs_lead_max_values = {
        'Manhattan': 220,
        'Bronx': 225,
        'Brooklyn': 290.5,
        'Staten Island': 300,
        'Queens': 270.5
    }
    boroughs_copper_max_values = {
        'Bronx': 440,
        'Brooklyn': 245,
        'Manhattan': 875,
        'Queens': 295,
        'Staten Island': 307
    }
    # Scale factors for lead graphs
    scale_factors_lead = {}
    for borough in boroughs_pl_dict:
        lead_diffs = boroughs_pl_dict[borough].values()
        max_lead_diff = max(lead_diffs)
        borough_max_lead = boroughs_lead_max_values[borough]
        scale_factors_lead[borough] = borough_max_lead / max(max_lead_diff, 100)

    # Scale factors for copper graphs
    scale_factors_copper = {}
    for borough in boroughs_pc_dict:
        copper_diffs = boroughs_pc_dict[borough].values()
        max_copper_diff = max(copper_diffs)
        borough_max_copper = boroughs_copper_max_values[borough]
        scale_factors_copper[borough] = borough_max_copper / max(max_copper_diff, 100)

    return render_template('micro.html',  brs = brs, scale_factors_copper=scale_factors_copper, scale_factors_lead=scale_factors_lead,borough_t5_pc_diff_avgs=borough_t5_pc_diff_avgs, borough_t5_pl_diff_avgs=borough_t5_pl_diff_avgs, borough_name = borough_name, borough_averages = borough_averages,  boroughs_pl_dict=boroughs_pl_dict, boroughs_pc_dict=boroughs_pc_dict)
    #return render_template('micro.html', brs = brs, borough_t5_pc_diff_avgs=borough_t5_pc_diff_avgs, borough_t5_pl_diff_avgs=borough_t5_pl_diff_avgs, borough_name = borough_name, borough_averages = borough_averages,  scale_factor_copper_staten_island= scale_factor_copper_staten_island,scale_factor_copper_queens=scale_factor_copper_queens,scale_factor_copper_manhattan=scale_factor_copper_manhattan,scale_factor_copper_bk=scale_factor_copper_bk,scale_factor_copper=scale_factor_copper,scale_factor_lead_queens = scale_factor_lead_queens, scale_factor_lead_manhattan=scale_factor_lead_manhattan, scale_factor_lead_bronx=scale_factor_lead_bronx, scale_factor_lead_bk=scale_factor_lead_bk, scale_factor_lead_si=scale_factor_lead_si,scale_factor_copper_bronx=scale_factor_copper_bronx, boroughs_pl_dict=boroughs_pl_dict, boroughs_pc_dict=boroughs_pc_dict)

if __name__ == "__main__": 
    app.run(debug=True)