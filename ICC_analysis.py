import argparse
import pandas as pd 
import pingouin as pg
import os

def read_paths_from_txt(file_path):
    with open(file_path, 'r') as f:
        paths = f.readlines()
    return [path.strip() for path in paths]

def ICC_caculate(final_df):
    results = pg.intraclass_corr(data=final_df, targets='scans', raters='rooms', ratings='data')
    pd.set_option('display.max_columns', 8)
    pd.set_option('display.width', 200)
    results.to_csv('result.csv')
    return results

def check_input(dataframes):
    is_header_equal = all(df.columns.equals(dataframes[0].columns) for df in dataframes)
    is_length_equal = all(df.shape[0] == dataframes[0].shape[0] for df in dataframes)
    if is_header_equal & is_length_equal:
        print("Valid Input!!!!")
    else:
        print("ERROR!! Length or Headers of inputs are not equal!!!")

def main(args):
    csv_pths = read_paths_from_txt(args.input_path)
    dataframes = [pd.read_csv(path) for path in csv_pths]

    check_input(dataframes)

    range_values = [int(x) for x in args.rows_number.split(',')]
    col_name = args.col_name
    
    if col_name != 'all':
        extracted_data = [df.iloc[range_values[0]:range_values[1]][[col_name]] for df in dataframes]
        room_names = ['Room2', 'Room4', 'Room6', 'Room9']
        final_df = pd.DataFrame(columns=['scans', 'rooms', 'data'])
        for df, room in zip(extracted_data, room_names):
            temp_df = pd.DataFrame({
                'scans': list(range(1, 16)),
                'rooms': [room] * 15,
                'data': df[col_name].values
            })
            final_df = pd.concat([final_df, temp_df])

        final_df.reset_index(drop=True, inplace=True)
        pd.set_option('display.float_format', '{:.9f}'.format)
        print(final_df)
        res = ICC_caculate(final_df)
        print(res)
    else:
        res_dict = {}

        col_name_list = dataframes[0].columns.to_list()
        col_name_list.remove('Unnamed: 0')
        col_name_list.remove('patient')
        col_name_list.remove('Mask')

        output_folder_name = args.output_path
        if not os.path.exists(output_folder_name):
            os.mkdir(output_folder_name)

        for col_name in col_name_list:
            extracted_data = [df.iloc[range_values[0]:range_values[1]][[col_name]] for df in dataframes]
            subset_number = args.subset_number
            if subset_number == '1':
                room_names = ['Room2', 'Room4', 'Room6', 'Room9']
            elif subset_number == '2':
                room_names = ['GE590', 'GER']
            elif subset_number == '0':
                room_names = ['Room2', 'Room4', 'Room6', 'Room9', 'GE590', 'GER']
            else:
                print("invaild subset_number!!!!!!!!!!!!!!!!")
                break

            final_df = pd.DataFrame(columns=['scans', 'rooms', 'data'])
            for df, room in zip(extracted_data, room_names):
                temp_df = pd.DataFrame({
                    'scans': list(range(1, (range_values[1] - range_values[0]) + 1)),
                    'rooms': [room] * (range_values[1] - range_values[0]),
                    'data': df[col_name].values
                })
                final_df = pd.concat([final_df, temp_df])
                final_df.reset_index(drop=True, inplace=True)
            final_df_csv_name = col_name + '_data.csv'
            final_df_path = os.path.join(output_folder_name, final_df_csv_name)
            final_df.to_csv(final_df_path, index=False)
            pd.set_option('display.float_format', '{:.9f}'.format)
            res = ICC_caculate(final_df)
            icc3 = res.loc[res['Type'] == 'ICC3', 'ICC'].iloc[0]
            icc3k = res.loc[res['Type'] == 'ICC3k', 'ICC'].iloc[0]
            res_dict[col_name] = [icc3, icc3k]
            csv_filename = col_name + '.csv'
            full_path = os.path.join(output_folder_name, csv_filename)
            res.to_csv(full_path, index=False)
        with open('result_dict_test.txt', 'w') as f:
            for k, v in res_dict.items():
                f.write(f'{k} : {v}\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ICC calculate')
    parser.add_argument('--input_path', type=str, required=True, help='Path to the input TXT file' 
                        'containing paths to CSV files.')
    parser.add_argument('--rows_number', type=str, required=True, help="An integer range separated by commas, e.g. 0,15")
    parser.add_argument('--col_name', type=str, required=True, help='Column name to filter.')
    parser.add_argument('--output_path', type=str, default='results', help="ouput folder path")
    parser.add_argument('--subset_number', type=str, required=True, help="0-wholeset, 1-subset1, 2-subset2")
    args = parser.parse_args()
    print(args)
    main(args)