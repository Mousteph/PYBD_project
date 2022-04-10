import pandas as pd
import glob



def inside_outside(line: str):
    line = line.split("/")[-1]
    inside = ["RESIDENCE", "INSIDE", "DOMESTIC", "COMMERCIAL"]
    outside = ["OUTSIDE", "TRANSIT"]
    
    if any(ext in line for ext in inside):
        return "INSIDE"
    elif any(ext in line for ext in outside):
        return "OUTSIDE"
    return "UNKNOWNED"


def generate_data_NYPD_calls(file_format: str, save_path: str) -> None:
	all_files = glob.glob(file_format)

	dataset = pd.concat([pd.read_csv(file,
									 parse_dates=["INCIDENT_DATE"],
									 index_col=["INCIDENT_DATE"],
									 usecols=["INCIDENT_DATE", "TYP_DESC", "CIP_JOBS"],
		   							 compression="zip") for file in all_files])

	dataset.index.name = "date"
	dataset = dataset.rename(columns={"TYP_DESC": "typDesc", "CIP_JOBS": "cipJobs"})
	dataset = dataset[dataset.cipJobs != "Non CIP"]

	dataset['desc'] = dataset.typDesc.apply(lambda x: x.split(':')[0].split(" (IN PROGRESS)")[0].capitalize())
	dataset['place'] = dataset.typDesc.apply(lambda x: inside_outside(x).capitalize())
	dataset = dataset.drop(columns=["typDesc"])

	dataset.to_pickle(save_path)


def generate_data_weather(file_format: str, save_path: str) -> None:
	dataset = pd.read_csv(file_format,
                          parse_dates=["date"],
                          index_col=["date"],
                          compression='zip')

	dataset = dataset.drop(columns=['tsun', 'wpgt']).ffill()

	dataset.to_pickle(save_path)


def generate_data():
	generate_data_NYPD_calls("data/NYPD_calls_*.csv.zip", "data/NYPD_calls.pkl")
	generate_data_weather("data/weather.csv.zip", "data/weather.pkl")


if __name__ == '__main__':
	generate_data()
