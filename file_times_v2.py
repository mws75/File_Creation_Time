#getts the time between files 
#V2 Full working version, file_times_v2.py does not need to be 
#in the same directory as the folder being analyzed 
from os import listdir
from os.path import isfile, join, getctime, getmtime
import pandas as pd

def create_file_list(dir_path):
	"""creates a list of file paths from dir_path"""
	file_list = list()
	file_list = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
	return file_list

def create_file_dict(file_list, dir_path):
	'''Create a Dict of key(file_list) value(mTime)
	Not sure if I should us ctime or mtime, but it seems
	mtime is more accurate in terms of when the file was completed'''
	
	file_dict = dict()
	for file in file_list:
		key = file
		value = getmtime(join(dir_path, file))
		print(value)
		file_dict.update({key:value})
	return file_dict


def dict_to_df(file_dict):
	'''Create a dataframe from the dict'''
	#create df	  
	file_df = pd.DataFrame(list(file_dict.items()), columns=['FileName', 'TimeCreated'])
	file_df_sort = file_df.sort_values(by=['TimeCreated'])
	#reset the index
	file_df_sort = file_df_sort.reset_index(drop=True)

	#get CreationTime
	CreationTime = list()
	for ind in file_df_sort.index:
		#first file modified in dir
		if ind == 0:
			time_diff = 0
			# c_time = getctime(str(file_df_sort['FileName'][ind]))
			# m_time = getmtime(str(file_df_sort['FileName'][ind]))
			# time_diff = m_time - c_time
			CreationTime.append(time_diff)
		#all other files
		else:
			time_diff = (file_df_sort['TimeCreated'][ind] - file_df_sort['TimeCreated'][ind-1])
			CreationTime.append(time_diff)

	#add CreationTime to dataFrame		  
	file_df_sort['CreationTime'] = CreationTime
	
	return file_df_sort

def df_to_csv(df):
	"""Convert df to CSV"""
	with open("File_Creation_Times.csv", 'w') as f:
		df.to_csv(f, header = True, index=False)
		f.close()


'''Practice Stuff'''
def main():
	dir_path = r"D:\Data\MapBooks\MiamiDade_Mapbook_20180409_Color"

	file_list = create_file_list(dir_path)

	file_dict = create_file_dict(file_list, dir_path)

	file_df = dict_to_df(file_dict)

	df_to_csv(file_df)

	print("Time Analysis Completed")

if __name__ == "__main__":
	main()