import sys
import os
import os.path as path
import csv
import json
import tkinter as tk
from tkinter import filedialog

class dic(dict): #extending dictionary with a function to search through the dictionary's keys to return a value
    def get_value_from_key(self, key:str):
        if (none_check(key) in self.keys()):
            return self[key]

def none_check(var_to_check: any): #utility function that checks if a variable is not assigned. if it is not, then we replace the reference with an empty string
    if var_to_check is None:
        return ""
    else:
        return var_to_check

def build_string_from_list(list_in:list[str]) -> str: #takes a list of strings and concatenates them
    item_list: str = ""
    for item in none_check(list_in):
        item_list += item + ", "
    return item_list[:-2]

class beer_stat: #data class for each of the 5 stats, which all contain "low", "high", and "flexible"
    def __init__(self) -> None:
        self.flexible:str = ""
        self.low: str = ""
        self.high: str = ""

class stats:    #data class for beer stats, since the JSON file gives them their own data structure I figured I might as well do that too
    def __init__(self, og: beer_stat, fg: beer_stat, ibu: beer_stat, srm: beer_stat, abv: beer_stat):
        self.og = og
        self.fg = fg
        self.ibu = ibu
        self.srm = srm
        self.abv = abv

    @staticmethod #makes this method a CLASS method, meaning you can't call this method on an instance of a 'stats' object, you must instead call 'stats.my_static_method()'
    def create_stats(json_stats: dic) -> 'stats': #a constructor method to create a new instance of stats. Must have a JSON data object passed to it
        og: beer_stat = beer_stat()
        fg: beer_stat = beer_stat()
        ibu: beer_stat = beer_stat()
        srm: beer_stat = beer_stat()
        abv: beer_stat = beer_stat()

        bog = dic(none_check(json_stats.get_value_from_key("og")))
        og.flexible = bog.get_value_from_key("flexible")
        og.high = bog.get_value_from_key("high")
        og.low = bog.get_value_from_key("low")
        bfg = dic(none_check(json_stats.get_value_from_key("fg")))
        fg.flexible = bfg.get_value_from_key("flexible")
        fg.high = bfg.get_value_from_key("high")
        fg.low = bfg.get_value_from_key("low")
        bibu = dic(none_check(json_stats.get_value_from_key("ibu")))
        ibu.flexible = bibu.get_value_from_key("flexible")
        ibu.high = bibu.get_value_from_key("high")
        ibu.low = bibu.get_value_from_key("low")
        bsrm = dic(none_check(json_stats.get_value_from_key("srm")))
        srm.flexible = bsrm.get_value_from_key("flexible")
        srm.high = bsrm.get_value_from_key("high")
        srm.low = bsrm.get_value_from_key("low")
        babv = dic(none_check(json_stats.get_value_from_key("abv")))
        abv.flexible = babv.get_value_from_key("flexible")
        abv.high = babv.get_value_from_key("high")
        abv.low = babv.get_value_from_key("low")
        bso = stats(og, fg, ibu, srm, abv)
        return bso

class beer_style: #meat and potatoes baybeeeee
    def __init__(self, category, id, name, impression, aroma, appearance, flavor, mouthfeel, comments, history, ingredients, comparison, examples, stats: stats):
        self.category = category
        self.id = id
        self.name = name
        self.impression = impression
        self.aroma = aroma
        self.appearance = appearance
        self.flavor = flavor
        self.mouthfeel = mouthfeel
        self.comments = comments
        self.history = history
        self.ingredients = ingredients
        self.comparison = comparison
        self.examples = examples
        self.stats = stats

    @staticmethod
    def build_examples(json_examples:list[str]) -> str: #implementation of the string builder method ^^^
        ex: str = build_string_from_list(json_examples)
        return ex

    @staticmethod
    def create_beer_style(new_item: dic, category_name: str) -> 'beer_style': #construction construction construction
        cat = none_check(category_name)
        id = none_check(new_item.get_value_from_key("id"))
        name = none_check(new_item.get_value_from_key("name"))
        impression = none_check(new_item.get_value_from_key("impression"))
        aroma = none_check(new_item.get_value_from_key("aroma"))
        appearance = none_check(new_item.get_value_from_key("appearance"))
        flavor = none_check(new_item.get_value_from_key("flavor"))
        mouthfeel = none_check(new_item.get_value_from_key("mouthfeel"))
        comments = none_check(new_item.get_value_from_key("comments"))
        history = none_check(new_item.get_value_from_key("history"))
        ingredients = none_check(new_item.get_value_from_key("ingredients"))
        comparison = none_check(new_item.get_value_from_key("comparison"))
        examples = none_check(beer_style.build_examples(new_item.get_value_from_key("examples")))
        beerstats = none_check(stats.create_stats(dic(new_item.get_value_from_key('stats'))))
        new_beer = beer_style(cat, id, name, impression, aroma, appearance, flavor, mouthfeel, comments, history, ingredients, comparison, examples, beerstats)
        return new_beer

def generate_entry(entry: beer_style) -> dict: #this pass a beer_style object as an argument and outputs a dictionary that contains all the data for that object, which we will use to populate our CSV
    line_out: dic = {}
    line_out['CATEGORY'] = none_check(entry.category)
    line_out['ID'] = none_check(entry.id)
    line_out['NAME'] = none_check(entry.name)
    line_out['IMPRESSION'] = none_check(entry.impression)
    line_out['AROMA'] = none_check(entry.aroma)
    line_out['APPEARANCE'] = none_check(entry.appearance)
    line_out['FLAVOR'] = none_check(entry.flavor)
    line_out['MOUTHFEEL'] = none_check(entry.mouthfeel)
    line_out['COMMENTS'] = none_check(entry.comments)
    line_out['HISTORY'] = none_check(entry.history)
    line_out['INGREDIENTS'] = none_check(entry.ingredients)
    line_out['COMPARISON'] = none_check(entry.comparison)
    line_out['EXAMPLES'] = none_check(entry.examples)
    line_out['ORIGINAL GRAVITY'] = none_check(entry.stats.og.low) + " - " + none_check(entry.stats.og.high) + ("(" if none_check(entry.stats.og.flexible) == "true" else " (not " + "flexible)")
    line_out['FINAL GRAVITY'] = none_check(entry.stats.fg.low) + " - " + none_check(entry.stats.fg.high) + ("(" if none_check(entry.stats.fg.flexible) == "true" else " (not " + "flexible)")
    line_out['IBUs'] = none_check(entry.stats.ibu.low) + " - " + none_check(entry.stats.ibu.high) + ("(" if none_check(entry.stats.ibu.flexible) == "true" else " (not " + "flexible)")
    line_out['STANDARD REFERENCE METHOD'] = none_check(entry.stats.srm.low) + " - " + none_check(entry.stats.srm.high) + ("(" if none_check(entry.stats.srm.flexible) == "true" else " (not " + "flexible)")
    line_out['ALCOHOL BY VOLUME'] = none_check(entry.stats.abv.low) + " - " + none_check(entry.stats.abv.high) + ("(" if none_check(entry.stats.abv.flexible) == "true" else " (not " + "flexible)")
    return line_out

def main():
    header: list[str] = ["CATEGORY", "ID", "NAME", "IMPRESSION", "AROMA", "APPEARANCE", "FLAVOR", "MOUTHFEEL", "COMMENTS", "HISTORY", "INGREDIENTS", "COMPARISON", "EXAMPLES", "ORIGINAL GRAVITY", "FINAL GRAVITY", "IBUs", "STANDARD REFERENCE METHOD", "ALCOHOL BY VOLUME"] #gross haha
    beer_style_lines = [] #list of dictionaries used for csv
    beer_categories: list[str] = [] #the parent JSON data objects are the categories of beer, so we'll use them to further categorize our beer styles
    beer_styles: list[beer_style] = [] #in japanese, "style (スタイル)" refers to your physique, not your fashion choices. Weird.
    root = tk.Tk() #tkinter sucks but dang is it fast to implement lmao
    root.withdraw()
    file_path = filedialog.askopenfilename()
    write_dir = path.dirname(__file__)
    data_file = path.join(write_dir,"beerstyles_out.csv")

    #I'm using the keyword 'with' here, which makes everything inside it exist within a smaller scope and not generate any garbage. It goes on the heap, not the stack. As soon as the functionality is complete, memory is freed up.
    with open(file_path,'r', encoding="utf8") as in_file:
        datafile = json.load(in_file)
        beer_categories = datafile.get('category')
        for cat in beer_categories: #for every category we ripped
            catname = dic(cat).get_value_from_key('name') #get the name of the category
            catlist = cat.get('subcategory')#this is the list of beer styles in this category
            for beer in catlist: #for every beer style in the list
                new_beer = beer_style.create_beer_style(dic(beer), catname) #make a new beer_style object
                beer_styles.append(new_beer) #and add it to the list of beer_style objects
        for entry in beer_styles: #for every beer_style object we added to our list
            beer_style_lines.append(generate_entry(entry)) #create a new dictionary out of it and store it in the list we'll use to create the CSV
    with open(data_file,'w',newline = '') as out_file: #create the new csv file.
        csvw = csv.DictWriter(out_file, fieldnames = header) #assign our gross header list to the header parameter of the csv instance
        csvw.writeheader() #write the header to the CSV
        for line in beer_style_lines:
            try:
                csvw.writerow(line)
            except:
                csvw.writerow({}) #if something goes wrong, it will write a blank line. This happened 3 times when i ran this, all with czech beers, for some reason. Decided it would be faster to manually update those entries than try and fix it :)
main() #RUN IT BACK