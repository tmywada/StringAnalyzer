# =================================================================================
#                             String Analyzer
# =================================================================================
#
import pandas as pd
import argparse

# --- version
version = '0.0.1'

class Utilities:

    def __init__(self):
        """
        https://www.ascii-code.com/
        https://www.williamrobertson.net/documents/ascii.shtml
        """
        self.idx_null = 0
        self.idx_numeric = 1
        self.idx_alphabet = 2
        self.idx_alphabet_lower = 3
        self.idx_ascii = 4
        self.idx_ascii_control = 5
        self.idx_extended_ascii = 6
        self.idx_extended_ascii_non_printable = 7
        self.idx_other = 8
        self.idx_other_non_printable = 9
        self.idx_unknown = 99

        # =============================================
        #   exceptions within ASCII (0-127)
        # =============================================
        self.code_point_dollar = 36

        # =============================================
        #   Latin lower
        # =============================================
        self.code_points_latin_lower = [
            181, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 
            234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 
            246, 248, 249, 250, 251, 252, 253, 254, 255
        ]
        self.idx_latin_lower = 11

        # =============================================
        #   Latin upper
        # =============================================
        self.code_points_latin_upper = [
            192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 
            204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 216, 
            217, 218, 219, 220, 221, 222
        ]
        self.idx_latin_upper = 12

        # =============================================
        #   Currency (Dollar sign is code point of 36)
        # =============================================
        self.code_points_currency = [
            162, 163, 164, 165, 8364
        ]
        self.idx_currency = 10

        # =============================================
        #   Math
        # =============================================
        self.code_points_math = [177, 172, 215, 247]
        self.idx_math = 13

    def categorize_character(self, ch:str):
        """
        Categorize character by types.
        """
        # --- null
        if pd.isnull(ch):
            return self.idx_null

        # --- numeric
        elif ch.isnumeric():
            return self.idx_numeric

        # --- alphabet (both upper and lower letters)
        elif ch.isalpha():
            return self.idx_alphabet

        # --- code point: 0-127
        elif ch.isascii():

            # --- 32-126
            if ch.isprintable() or ord(ch) == 127:
                return self.idx_ascii

            # --- 0-31
            else:
                return self.idx_ascii_control

        # --- code point: 128-
        else:
            return self.idx_other

    def categorize_character_comprehensive(self, ch:str):
        """
        Categorize character by comprehensive types.
        """
        # --- null
        if pd.isnull(ch):
            return self.idx_null

        # --- numeric
        elif ch.isnumeric():
            return self.idx_numeric

        # --- alphabet
        elif ch.isalpha():
            if ch.isupper():
                return self.idx_alphabet
            else:
                return self.idx_alphabet_lower

        # --- get code point
        try:
            code_point = ord(ch)
        except:
            return self.idx_unknown

        # =============================================
        #   exceptions within ASCII (32-127)
        # =============================================
        # --- dollar sign
        if code_point == self.code_point_dollar:
            return self.idx_currency

        # =============================================
        #   ASCII (32-127)
        # =============================================
        if 32 <= code_point <= 127:
            return self.idx_ascii

        # =============================================
        #   ASCII Control (0-31)
        # =============================================
        elif code_point <= 31:
            return self.idx_ascii_control

        # =============================================
        #   exceptions (128-)
        # =============================================    
        idx_category = categorize_unicode_code_point(code_point)

        if idx_category != 99:
            return idx_category

        else:
            # =============================================
            #   Extended ASCII (128-255)
            # =============================================
            if code_point <= 255:
                if ch.isprintable():
                    return self.idx_extended_ascii
                else:
                    return self.idx_extended_ascii_non_printable

            # =============================================
            #   Other (non-ascii, 256-)
            # =============================================
            else:
                if ch.isprintable():
                    return self.idx_other
                else:
                    return self.idx_other_non_printable

    def serach_known_code_point(self, code_point:int):
        """
        Search known code points defined.
        Code points can be obtain using `ord(str)`.
        Note that "$" (dollar sign) has the code point of 36. 
        Define a list of code points and assign an integer (14-98).
        99 is reserved for unknown code point (i.e., not listed code_point).
        """
        # --- currency
        if code_point in self.code_points_currency:
            return self.idx_currency

        # --- latin lower
        elif code_point in self.code_points_latin_lower:
            return self.idx_latin_lower

        # --- latin upper
        elif code_point in self.code_points_latin_upper:
            return self.idx_latin_upper

        # --- math
        elif code_point in self.code_points_math:
            return self.idx_math

        # --- additional criteria (14-97). Add list above first! 
        #

        # --- other
        else:
            return 99    

class AnalyzeString(Utilities):

    def count_string_categories(self, input_string:str):
        """
        Count categories of string
        """
        # --- initialization
        num_numeric          = 0
        num_alphabet         = 0
        num_non_alphanumeric = 0
        num_other            = 0

        # --- 
        categories_other = [
            self.idx_null,
            self.idx_ascii_control,
            self.idx_other
        ]

        # --- check value-by-value
        categories = [self.categorize_character(v) for v in input_string]
        num_numeric          = categories.count(self.idx_numeric)
        num_alphabet         = categories.count(self.idx_alphabet)
        num_non_alphanumeric = categories.count(self.idx_ascii)
        num_other            = sum([categories.count(v) for v in categories_other])

        res =  {
            'numeric': num_numeric, 
            'alphabet': num_alphabet, 
            'non_alphanumeric': num_non_alphanumeric,
            'other': num_other
        }

        return res

    def count_string_categories_comprehensive(self, input_string:str):
        """
        """
        # --- initialization
        num_null             = 0
        num_numeric          = 0
        num_upper_letter     = 0
        num_lower_letter     = 0
        num_non_alphanumeric = 0
        num_other            = 0

        # --- define aggregated categories
        categories_non_alphanumeric = [
            self.idx_ascii,
            self.idx_extended_ascii,
            self.idx_latin_lower,
            self.idx_latin_upper,
            self.idx_currency,
            self.idx_math,
            self.idx_other                  
        ]

        categories_other = [
            self.idx_ascii_control,
            self.idx_extended_ascii_non_printable,
            self.idx_other_non_printable,
            self.idx_unknown
        ]

        # ---
        categories = [self.categorize_character_comprehensive(v) for v in input_string]
        num_null             = categories.count(self.idx_null)
        num_numeric          = categories.count(self.idx_numeric)
        num_lower_letter     = categories.count(self.idx_alphabet_lower)
        num_upper_letter     = categories.count(self.idx_alphabet)
        num_non_alphanumeric = sum([categories.count(v) for v in categories_non_alphanumeric])
        num_other            = sum([categories.count(v) for v in categories_other])

    
        res = {
            'null': num_null,
            'numeric': num_numeric,
            'lower_letter': num_lower_letter, 
            'upper_letter': num_upper_letter,
            'non_alphanumeric': num_non_alphanumeric,
            'other': num_other
        }

        return res

def analyze_string(input_string:str, is_comprehensive:bool):
    """
    """
    # --- initialization
    obj = AnalyzeString()

    # ---
    if is_comprehensive:
        return obj.count_string_categories_comprehensive(input_string)
    else:
        return obj.count_string_categories(input_string)

if __name__ == '__main__':

    # --- initialization
    arg_parser = argparse.ArgumentParser()

    # --- load parameters
    arg_parser.add_argument('--input_string', type = str)
    arg_parser.add_argument('--is_comprehensive', default = False, action = 'store_true')

    # --- parser arguments
    options = arg_parser.parse_args()

    # --- process
    res = analyze_string(
        input_string = options.input_string,
        is_comprehensive = options.is_comprehensive
    )

    print(f'input_string: {options.input_string}')
    print(res)