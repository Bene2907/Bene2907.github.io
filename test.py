from multiprocessing import Pool
from windfinder_scrape_copy import execute
from spot_lists import get_spot_lists

if __name__ == "__main__":
    all_spots_lists = get_spot_lists()
    p = Pool(processes=int(input("How many cpus: ")))
    # for quiz, solved1 in zip(string_sudoku_list, solved_string_sudoku_list):
    result = p.map(execute, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], )
    p.close()
    p.join()
