__author__ = 'zdj'
class Evaluator:
    def __init__(self, result_path, test_path):
        self.result_path = result_path
        self.test_path = test_path
        self.result_token_list = []
        self.test_token_list = []
        self.match_num = 0

    def get_token_list(self, path, token_list):
        file = open(path)
        r_list = file.readlines()
        file.close()
        for r in r_list:
            tokens = r.split()
            token_list.__iadd__(tokens)

    def get_match_number(self):
        test_l = 0
        result_l = 0
        i = 0
        j = 0
        match_num = 0
        while True:
            if i >= len(self.test_token_list) or j >= len(self.result_token_list):
                break
            if test_l == result_l:
                if self.result_token_list[j] == self. result_token_list:
                    self.match_num += 1
                test_l += len(self.test_token_list[i])
                result_l += len(self.result_token_list[j])
                i += 1
                j += 1

            elif test_l > result_l:
                result_l += len(self.result_token_list[j])
                j += 1
            elif result_l > test_l:
                test_l += len(self.test_token_list[i])
                i += 1
        return self.match_num

    def get_recall_rate(self):
        rate = (float)(self.match_num) / (float)(len(self.test_token_list))
        return  rate

    def get_precision_rate(self):
        rate = (float)(self.match_num) / (float)(len(self.test_token_list))
        return rate

if __name__ == "__main__":
    e_tor = Evaluator()