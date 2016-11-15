from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)
import ast
import time
import csv
import os
from font_helper import f_helper
import shutil
import timeit
from intersect_lists import intersect_lists


first_key = 'name'
second_key = 'registry_name'
cheat = [{first_key: 'Bodoni MT Condensed', second_key: ['Bodoni MT Condensed (TrueType)',
                                                         'Bodoni MT Condensed Bold (TrueType)',
                                                         'Bodoni MT Condensed Bold Italic (TrueType)',
                                                         'Bodoni MT Condensed Italic (TrueType)']},
         {first_key: 'Stencil', second_key: ['Stencil (TrueType)']},
         {first_key: 'Arial Unicode MS', second_key: ['Arial Unicode MS (TrueType)']},
         {first_key: 'Perpetua Titling MT', second_key: ['Perpetua Titling MT Bold (TrueType)',
                                                         'Perpetua Titling MT Light (TrueType)']},
         {first_key: 'Haettenschweiler', second_key: ['Haettenschweiler (TrueType)']},
         {first_key: 'Matura MT Script Capitals', second_key: ['Matura MT Script Capitals (TrueType)']},
         {first_key: 'Lucida Sans Typewriter', second_key: ['Lucida Sans Typewriter Bold (TrueType)',
                                                            'Lucida Sans Typewriter Bold Oblique (TrueType)',
                                                            'Lucida Sans Typewriter Oblique (TrueType)',
                                                            'Lucida Sans Typewriter Regular (TrueType)']},
         {first_key: 'Brush Script Std', second_key: ['BrushScriptStd (OpenType)']},
         {first_key: 'Trajan Pro', second_key: ['Trajan Pro',
                                                'TrajanPro-Bold (TrueType)',
                                                'TrajanPro-Regular (OpenType)',
                                                'TrajanPro-Regular (TrueType)']},
         {first_key: 'Arial Narrow', second_key: ['Arial Narrow (TrueType)',
                                                  'Arial Narrow Bold (TrueType)',
                                                  'Arial Narrow Bold Italic (TrueType)',
                                                  'Arial Narrow Italic (TrueType)']},
         {first_key: 'Nueva Std', second_key: ['NuevaStd-Bold (OpenType)',
                                               'NuevaStd-BoldCond (OpenType)',
                                               'NuevaStd-BoldCondItalic (OpenType)',
                                               'NuevaStd-Cond (OpenType)',
                                               'NuevaStd-CondItalic (OpenType)',
                                               'NuevaStd-Italic (OpenType)']},
         {first_key: 'Adobe Arabic', second_key: ['AdobeArabic-Bold (OpenType)',
                                                  'AdobeArabic-Bold (TrueType)',
                                                  'AdobeArabic-BoldItalic (OpenType)',
                                                  'AdobeArabic-BoldItalic (TrueType)',
                                                  'AdobeArabic-Italic (OpenType)',
                                                  'AdobeArabic-Italic (TrueType)',
                                                  'AdobeArabic-Regular (OpenType)',
                                                  'AdobeArabic-Regular (TrueType)']},
         {first_key: 'Rosewood Std Regular', second_key: ['RosewoodStd-Regular (OpenType)']},
         {first_key: 'Elephant', second_key: ['Elephant (TrueType)',
                                              'Elephant Italic (TrueType)']},
         {first_key: 'HelvLight', second_key: ['HelvLight Regular (TrueType)']},
         {first_key: 'Open Sans', second_key: ['Open Sans (TrueType)',
                                               'Open Sans Bold (TrueType)',
                                               'Open Sans Bold Italic (TrueType)',
                                               'Open Sans Extrabold (TrueType)',
                                               'Open Sans Extrabold Italic (TrueType)',
                                               'Open Sans Italic (TrueType)',
                                               'Open Sans Light (TrueType)',
                                               'Open Sans Light Italic (TrueType)',
                                               'Open Sans Semibold (TrueType)',
                                               'Open Sans Semibold Italic (TrueType)']},
         {first_key: 'Hobo Std', second_key: ['HoboStd (OpenType)']},
         {first_key: 'Perpetua', second_key: ['Perpetua (TrueType)',
                                              'Perpetua Bold (TrueType)',
                                              'Perpetua Bold Italic (TrueType)',
                                              'Perpetua Italic (TrueType)',
                                              'Perpetua Titling MT Bold (TrueType)',
                                              'Perpetua Titling MT Light (TrueType)']},
         {first_key: 'Myriad Hebrew', second_key: ['Myriad Hebrew (OpenType)',
                                                   'Myriad Hebrew Bold (OpenType)',
                                                   'Myriad Hebrew Bold Italic (OpenType)',
                                                   'Myriad Hebrew Italic (OpenType)']},
         {first_key: 'Adobe Caslon Pro', second_key: ['ACaslonPro-Italic (OpenType)',
                                                      'ACaslonPro-Regular (OpenType)',
                                                      'ACaslonPro-Semibold (OpenType)',
                                                      'ACaslonPro-SemiboldItalic (OpenType)']},
         {first_key: 'Mesquite Std', second_key: ['MesquiteStd (OpenType)']},
         {first_key: 'Adobe Kaiti Std R', second_key: ['AdobeKaitiStd-Regular (OpenType)']},
         {first_key: 'Kozuka Gothic Pr6N R', second_key: ['KozGoPr6N-Regular (OpenType)']},
         {first_key: 'Tekton Pro', second_key: ['TektonPro-Bold (OpenType)',
                                                'TektonPro-BoldCond (OpenType)',
                                                'TektonPro-BoldExt (OpenType)',
                                                'TektonPro-BoldObl (OpenType)']},
         {first_key: 'Bell MT', second_key: ['Bell MT (TrueType)',
                                             'Bell MT Bold (TrueType)',
                                             'Bell MT Italic (TrueType)']},
         {first_key: 'Lucida Sans', second_key: ['Lucida Sans Demibold Italic (TrueType)',
                                                 'Lucida Sans Demibold Roman (TrueType)',
                                                 'Lucida Sans Italic (TrueType)',
                                                 'Lucida Sans Regular (TrueType)',
                                                 'Lucida Sans Typewriter Bold (TrueType)',
                                                 'Lucida Sans Typewriter Bold Oblique (TrueType)',
                                                 'Lucida Sans Typewriter Oblique (TrueType)',
                                                 'Lucida Sans Typewriter Regular (TrueType)',
                                                 'Lucida Sans Unicode (TrueType)']},
         # Gothic
         {first_key: 'Kozuka Gothic Pr6N B', second_key: ['KozGoPr6N-Bold (OpenType)']},
         {first_key: 'Kozuka Gothic Pr6N M', second_key: ['KozGoPr6N-Medium (OpenType)']},
         {first_key: 'Kozuka Gothic Pr6N L', second_key: ['KozGoPr6N-Light (OpenType)']},
         {first_key: 'Kozuka Gothic Pr6N H', second_key: ['KozGoPr6N-Heavy (OpenType)']},
         {first_key: 'Kozuka Gothic Pr6N EL', second_key: ['KozGoPr6N-ExtraLight (OpenType)']},
         # Mincho
         {first_key: 'Kozuka Mincho Pr6N M', second_key: ['KozMinPr6N-Medium (OpenType)']},
         {first_key: 'Kozuka Mincho Pr6N L', second_key: ['KozMinPr6N-Light (OpenType)']},
         {first_key: 'Kozuka Mincho Pr6N B', second_key: ['KozMinPr6N-Bold (OpenType)']},
         {first_key: 'Kozuka Mincho Pr6N R', second_key: ['KozMinPr6N-Regular (OpenType)']},
         {first_key: 'Kozuka Mincho Pr6N EL', second_key: ['KozMinPr6N-ExtraLight (OpenType)']},
         {first_key: 'Kozuka Mincho Pr6N H', second_key: ['KozMinPr6N-Heavy (OpenType)']},
         # mincho PRO
         {first_key: 'Kozuka Mincho Pro B', second_key: ['KozMinPro-Bold (TrueType)']},
         {first_key: 'Kozuka Gothic Pro L', second_key: ['KozGoPro-Light (OpenType)']},
         {first_key: 'Kozuka Gothic Pro R', second_key: ['KozGoPro-Regular (OpenType)']},
         {first_key: 'Kozuka Gothic Pro B', second_key: ['KozGoPro-Bold (OpenType)']},
         {first_key: 'Kozuka Gothic Pro M', second_key: ['KozGoPro-Medium (OpenType)']},
         {first_key: 'Kozuka Gothic Pro H', second_key: ['KozGoPro-Heavy (OpenType)']},
         {first_key: 'Franklin Gothic Heavy', second_key: ['Franklin Gothic Heavy (TrueType)',
                                                           'Franklin Gothic Heavy Italic (TrueType)']},
         {first_key: 'Franklin Gothic Demi', second_key: ['Franklin Gothic Demi (TrueType)',
                                                           'Franklin Gothic Demi Cond (TrueType)',
                                                           'Franklin Gothic Demi Italic (TrueType)']},
         {first_key: 'Franklin Gothic Book', second_key: ['Franklin Gothic Book (TrueType)',
                                                           'Franklin Gothic Book Italic (TrueType)']},
         {first_key: 'Vivaldi', second_key: ['Vivaldi Italic (TrueType)']},
         {first_key: 'Myriad Pro Light', second_key: ['MyriadPro-Light (OpenType)']},
         {first_key: 'Adobe Gothic Std B', second_key: ['AdobeGothicStd-Bold (OpenType)']},
         {first_key: 'Agency FB', second_key: ['Agency FB (TrueType)',
                                               'Agency FB Bold (TrueType)']},
         {first_key: 'Adobe Naskh Medium', second_key: ['Adobe Naskh Medium (OpenType)']},
         {first_key: 'Orator Std', second_key: ['OratorStd (OpenType)',
                                                'OratorStd-Slanted (OpenType)']},
         {first_key: 'Adobe Song Std L', second_key: ['AdobeSongStd-Light (OpenType)']},
         {first_key: 'Lucida Calligraphy', second_key: ['Lucida Calligraphy Italic (TrueType)']},
         {first_key: 'Tekton Pro Cond', second_key: ['TektonPro-BoldCond (OpenType)']},
         {first_key: 'Adobe Devanagari', second_key: ['AdobeDevanagari-Bold (OpenType)',
                                                      'AdobeDevanagari-BoldItalic (OpenType)',
                                                      'AdobeDevanagari-Italic (OpenType),'
                                                      'AdobeDevanagari-Regular (OpenType)']},
         {first_key: 'Gill Sans MT', second_key: ['Gill Sans MT (TrueType)',
                                                  'Gill Sans MT Bold (TrueType)',
                                                  'Gill Sans MT Bold Italic (TrueType)',
                                                  'Gill Sans MT Condensed (TrueType)',
                                                  'Gill Sans MT Ext Condensed Bold (TrueType)',
                                                  'Gill Sans MT Italic (TrueType)',
                                                  'Gill Sans Ultra Bold (TrueType)',
                                                  'Gill Sans Ultra Bold Condensed (TrueType)']},
         {first_key: 'Charlemagne Std', second_key: ['CharlemagneStd-Bold (OpenType)']},
         {first_key: 'Tekton Pro Ext', second_key: ['TektonPro-BoldExt (OpenType)']},
         {first_key: 'Letter Gothic Std', second_key: ['LetterGothicStd (OpenType)',
                                                       'LetterGothicStd-Bold (OpenType)',
                                                       'LetterGothicStd-BoldSlanted (OpenType)',
                                                       'LetterGothicStd-Slanted (OpenType)']},
         {first_key: 'Nueva Std Cond', second_key: ['NuevaStd-BoldCond (OpenType)',
                                                    'NuevaStd-BoldCondItalic (OpenType)',
                                                    'NuevaStd-Cond (OpenType)',
                                                    'NuevaStd-CondItalic (OpenType)']},
         {first_key: 'Adobe Myungjo Std M', second_key: ['AdobeMyungjoStd-Medium (OpenType)']},
         {first_key: 'Stencil Std', second_key: ['StencilStd (OpenType)']},
         {first_key: 'Berlin Sans FB Demi', second_key: ['Berlin Sans FB Demi Bold (TrueType)']},
         {first_key: 'Minion Pro', second_key: ['MinionPro-Bold (OpenType)',
                                                'MinionPro-BoldIt (OpenType)',
                                                'MinionPro-It (OpenType)',
                                                'MinionPro-Regular (OpenType)']},
         {first_key: 'Minion Pro Med', second_key: ['MinionPro-Medium (OpenType)',
                                                    'MinionPro-MediumIt (OpenType)']},
         {first_key: 'Minion Pro SmBd', second_key: ['MinionPro-Semibold (OpenType)',
                                                     'MinionPro-SemiboldIt (OpenType)']},
         {first_key: 'Minion Pro Cond', second_key: ['MinionPro-BoldCn (OpenType)',
                                                     'MinionPro-BoldCnIt (OpenType)',]},
         {first_key: 'Chaparral Pro Light', second_key: ['ChaparralPro-LightIt (OpenType)']},
         {first_key: 'Cooper Std Black', second_key: ['CooperBlackStd (OpenType)']},
         {first_key: 'Lithos Pro Regular', second_key: ['LithosPro-Regular (OpenType)']},
         {first_key: 'Myriad Arabic', second_key: ['Myriad Arabic Bold (OpenType)',
                                                   'Myriad Arabic Bold Italic (OpenType)',
                                                   'Myriad Arabic Italic (OpenType)',
                                                   'Myriad Arabic (OpenType)']},
         {first_key: 'High Tower Text', second_key: ['High Tower Text (TrueType)',
                                                     'High Tower Text Italic (TrueType)']},
         {first_key: 'Salina', second_key: ['Salina (TrueType)',
                                            'Salina Regular (TrueType)']}, {first_key: ''},
         {first_key: 'Bodoni MT Black', second_key: ['Bodoni MT Black (TrueType)',
                                                     'Bodoni MT Black Italic (TrueType)']},
         {first_key: 'Lucida Handwriting', second_key: ['Lucida Handwriting Italic (TrueType)']},
         {first_key: 'Myriad Pro Cond', second_key: ['MyriadPro-BoldCond (OpenType)',
                                                     'MyriadPro-BoldCondIt (OpenType)',
                                                     'MyriadPro-Cond (OpenType)',
                                                     'MyriadPro-CondIt (OpenType)']},
         {first_key: 'Myriad Pro', second_key: ['MyriadPro-Bold (OpenType)',
                                                'MyriadPro-BoldIt (OpenType)',
                                                'MyriadPro-It (OpenType)',
                                                'MyriadPro-Regular (OpenType)',
                                                'MyriadPro-Semibold (OpenType)',
                                                'MyriadPro-SemiboldIt (OpenType)']},
         {first_key: 'Adobe Heiti Std R', second_key: ['AdobeHeitiStd-Regular (OpenType)']},
         {first_key: 'Garamond', second_key: ['Garamond (TrueType)',
                                              'Garamond Bold (TrueType)',
                                              'Garamond Italic (TrueType)']},
         {first_key: 'Brush Script MT', second_key: ['Brush Script MT Italic (TrueType)']},
         {first_key: 'Blackoak Std', second_key: ['BlackoakStd (TrueType)',
                                                  'BlackoakStd (OpenType)']},
         {first_key: 'Adobe Ming Std L', second_key: ['AdobeMingStd-Light (OpenType)']},
         {first_key: 'Adobe Caslon Pro Bold', second_key: ['ACaslonPro-Bold (OpenType)',
                                                           'ACaslonPro-BoldItalic (OpenType)']},
         {first_key: 'Tw Cen MT Condensed', second_key: ['Tw Cen MT Condensed (TrueType)',
                                                         'Tw Cen MT Condensed Bold (TrueType)',
                                                         'Tw Cen MT Condensed Extra Bold (TrueType)']},
         {first_key: 'Open Sans Light', second_key: ['Open Sans Light (TrueType)',
                                                     'Open Sans Light Italic (TrueType)']},
         {first_key: 'Adobe Fangsong Std R', second_key: ['AdobeFangsongStd-Regular (OpenType)']},
         {first_key: 'Giddyup Std', second_key: ['GiddyupStd (OpenType)',
                                                 'GiddyupStd (TrueType)']},
         {first_key: 'Magneto', second_key: ['Magneto Bold (TrueType)']},
         {first_key: 'Tw Cen MT', second_key: ['Tw Cen MT (TrueType)',
                                               'Tw Cen MT Bold (TrueType)',
                                               'Tw Cen MT Bold Italic (TrueType)',
                                               'Tw Cen MT Italic (TrueType)']},
         {first_key: 'Lucida Bright', second_key: ['Lucida Bright (TrueType)',
                                                   'Lucida Bright Demibold (TrueType)',
                                                   'Lucida Bright Demibold Italic (TrueType)',
                                                   'Lucida Bright Italic (TrueType)']},
         {first_key: 'Open Sans Extrabold', second_key: ['Open Sans Extrabold (TrueType)',
                                                         'Open Sans Extrabold Italic (TrueType)']},
         {first_key: 'Poplar Std', second_key: ['PoplarStd (OpenType)']},
         {first_key: 'Adobe Garamond Pro Bold', second_key: ['AGaramondPro-Bold (OpenType)',
                                                             'AGaramondPro-BoldItalic (OpenType)']},
         {first_key: 'Rockwell Condensed', second_key: ['Rockwell Condensed (TrueType)',
                                                        'Rockwell Condensed Bold (TrueType)']},
         {first_key: 'Adobe Hebrew', second_key: ['AdobeHebrew-Bold (OpenType)',
                                                  'AdobeHebrew-BoldItalic (OpenType)',
                                                  'AdobeHebrew-Italic (OpenType)',
                                                  'AdobeHebrew-Regular (OpenType)']},
         {first_key: 'Chaparral Pro', second_key: ['ChaparralPro-Bold (OpenType)',
                                                   'ChaparralPro-BoldIt (OpenType)',
                                                   'ChaparralPro-Italic (OpenType)',
                                                   'ChaparralPro-LightIt (OpenType)',
                                                   'ChaparralPro-Regular (OpenType)']},
         {first_key: 'Prestige Elite Std', second_key: ['PrestigeEliteStd-Bd (OpenType)']},
         {first_key: 'FlemishScript BT', second_key: ['Flemish Script BT (TrueType)']},
         {first_key: 'Tiranti Solid LET', second_key: ['Tiranti Solid LET (TrueType)',
                                                       'Tiranti Solid LET Plain:1.0 (TrueType)']},
         {first_key: 'Rockwell', second_key: ['Rockwell (TrueType)',
                                              'Rockwell Bold (TrueType)',
                                              'Rockwell Bold Italic (TrueType)',
                                              'Rockwell Condensed (TrueType)',
                                              'Rockwell Condensed Bold (TrueType)',
                                              'Rockwell Extra Bold (TrueType)',
                                              'Rockwell Italic (TrueType)']},
         {first_key: 'Bodoni MT', second_key: ['Bodoni MT (TrueType)',
                                               'Bodoni MT Black (TrueType)',
                                               'Bodoni MT Black Italic (TrueType)',
                                               'Bodoni MT Bold (TrueType)',
                                               'Bodoni MT Bold Italic (TrueType)',
                                               'Bodoni MT Condensed (TrueType)',
                                               'Bodoni MT Condensed Bold (TrueType)',
                                               'Bodoni MT Condensed Bold Italic (TrueType)',
                                               'Bodoni MT Condensed Italic (TrueType)',
                                               'Bodoni MT Italic (TrueType)',
                                               'Bodoni MT Poster Compressed (TrueType)']},
         {first_key: 'Bookman Old Style', second_key: ['Bookman Old Style (TrueType)',
                                                       'Bookman Old Style Bold (TrueType)',
                                                       'Bookman Old Style Bold Italic (TrueType)',
                                                       'Bookman Old Style Italic (TrueType)']},
         {first_key: 'Californian FB', second_key: ['Californian FB (TrueType)',
                                                    'Californian FB Bold (TrueType)',
                                                    'Californian FB Italic (TrueType)']},
         {first_key: 'Goudy Old Style', second_key: ['Goudy Old Style (TrueType)',
                                                     'Goudy Old Style Bold (TrueType)',
                                                     'Goudy Old Style Italic (TrueType)']},
         {first_key: 'OCR A Std', second_key: ['OCRAStd (OpenType)']},
         {first_key: 'Adobe Garamond Pro', second_key: ['AGaramondPro-Italic (OpenType)',
                                                        'AGaramondPro-Regular (OpenType)']},
         {first_key: 'Open Sans Semibold', second_key: ['Open Sans Semibold (TrueType)',
                                                        'Open Sans Semibold Italic (TrueType)']},
         {first_key: 'Adobe Fan Heiti Std B', second_key: ['AdobeFanHeitiStd-Bold (OpenType)']},
         {first_key: 'Berlin Sans FB', second_key: ['Berlin Sans FB (TrueType)',
                                                    'Berlin Sans FB Bold (TrueType)',
                                                    'Berlin Sans FB Demi Bold (TrueType)']},
         {first_key: 'Lucida Fax', second_key: ['Lucida Fax Demibold (TrueType)',
                                                'Lucida Fax Demibold Italic (TrueType)',
                                                'Lucida Fax Italic (TrueType)',
                                                'Lucida Fax Regular (TrueType)']},
         {first_key: 'Century Schoolbook', second_key: ['Century Schoolbook (TrueType)',
                                                        'Century Schoolbook Bold (TrueType)',
                                                        'Century Schoolbook Bold Italic (TrueType)',
                                                        'Century Schoolbook Italic (TrueType)']}]
@app.route('/ports', methods=['POST'])
def get_ports():
    # Find open ports from this system
    import psutil
    
    connections = psutil.net_connections()
    temp_connections = []
    open_ports = []
    print len(connections)
    for index, connection in enumerate(connections):
        if connection[5] != 'NONE' \
                and connection[5] != 'CLOSE_WAIT' \
                and connection[5] != 'TIME_WAIT' \
                and connection[3][0] != '127.0.0.1' \
                and connection[3][0] != '::' \
                and connection[3][0] != '::1' \
                and connection[3][0] != '0.0.0.0':
            temp_connections.append(connection)
            open_ports.append(connection[3][1])

    # Convert to set to avoid duplicate values
    # Then back to a list and sort it
    sorted_ports = sorted(list(set(open_ports)))
    return jsonify(ports=sorted_ports)


'''
  This part will only work for Window systems.
  Accepts two sets of fonts, one of the client and one 
  from the target profile. The function will attempt
  to discover the intersection between those two lists
  and the basic font list of Windows (stored in a .csv format)
  which is extracted from Wikipedia. The current .csv list 
  contains the basic fonts for Windows 7.
  After that the server will attempt to try and uninstall all 
  the other fonts located in the client's system.
'''
@app.route('/fonts', methods=['POST'])
def modify_fonts():
    # Start the timer
    start_time = timeit.default_timer()
    # Receive data from POST request
    fonts = request.form.getlist('fonts')
    target_fonts = request.form.getlist('target_fonts')
    # Transform fonts to a literal form in order to be accessible
    fonts = ast.literal_eval(fonts[0])
    # Do the same for the common fonts
    target_fonts = ast.literal_eval(target_fonts[0])

    common_fonts, count = intersect_lists.simple_intersect(fonts, target_fonts)

    temp = []
    # Transform the fonts into a list containing only the name of the font
    for x in range(len(fonts)):
        temp.append(fonts[x]['fontId'])
    fonts = temp
    # Read the core OS fonts from the CSV
    core_fonts = f_helper.read_csv()
    # Remove the common and core fonts from the initial set of fonts.
    # The remaining fonts are the surplus and should be removed

    fonts_to_remove = list(set(fonts) - set(common_fonts) - set(core_fonts))

    # At this moment we have to extract the list of fonts from the user's registry
    # Using the find_fonts function a list of tuples containing the font filename, displayname
    # and a value identifying the value data
    # Temp font list will hold the triplet font name, file name and the other one
    registry_fonts = f_helper.find_fonts()


    font_list = []
    for i in range(len(registry_fonts)):
        font_list.append(registry_fonts[i][0])
    temp = []

    for i in range(len(fonts_to_remove)):
        temp1 = [y for y in font_list if fonts_to_remove[i] + " (TrueType)" in y]
        if temp1:
            temp.append(temp1)
    small_list = [item for sublist in temp for item in sublist]
    small_list_without_truetype = []

    # Filter the font_list list and keep the tuple with the fonts to delete
    # At this moment we can only delete the TrueType fonts
    fonts_to_go_with_paths = []
    for i in range(len(registry_fonts)):
        for y in range(len(small_list)):
            if str(small_list[y]) == str(registry_fonts[i][0]):
                fonts_to_go_with_paths.append(registry_fonts[i])

    list_to_fuzzy_search = list(set(fonts_to_remove) - set(small_list_without_truetype))

    # Associate the fuzzy list ( the non Truetype or the list of fonts with multiple files)
    # With their equivalent on the cheat table
    fonts_to_go_with_paths_fuzzy_part = []
    for i in range(len(list_to_fuzzy_search)):
        for j in range(len(cheat)):
            if list_to_fuzzy_search[i] == cheat[j][first_key]:
                fonts_to_go_with_paths_fuzzy_part.append(cheat[j])

    # Now we need to associate the cheat values with the appropriate value names from the registry table
    for i in range(len(fonts_to_go_with_paths_fuzzy_part)):
        for y in range(len(fonts_to_go_with_paths_fuzzy_part[i][second_key])):
            for j in range(len(registry_fonts)):
                if fonts_to_go_with_paths_fuzzy_part[i][second_key][y] == registry_fonts[j][0]:
                    fonts_to_go_with_paths.append(registry_fonts[j])

    # Remove duplicate values in the list
    fonts_to_go_with_paths = list(set(fonts_to_go_with_paths))
    print len(fonts_to_go_with_paths)
    print fonts_to_go_with_paths
    # Remove the unnecessary fonts
    success_count = 0
    fail_count = 0
    # Uncomment the following snippet to make a backup of your fonts before deleting them
    # make notice that this will slow down the process!
    # for i in range(len(fonts_to_go_with_paths)):
    #     shutil.copy2('C:\Windows\Fonts\\' + fonts_to_go_with_paths[i][1], 'C:\temp\la\\')
    for i in range(len(fonts_to_go_with_paths)):
        try:
            result = f_helper.delete_font(fonts_to_go_with_paths[i][1])
            # print result
            if result:
                print 'The font ' + fonts_to_go_with_paths[i][1] + ' was removed successfully'
                success_count += 1
            else:
                print 'The font ' + fonts_to_go_with_paths[i][1] + ' failed to be removed'
                fail_count += 1

        except WindowsError as e:
            print 'Font ' + fonts_to_go_with_paths[i][1] + ' failed to copy'
            print e

    print 'Total fonts removed ' + str(success_count)
    print 'Fonts not removed  ' + str(fail_count)
    # Calculate elapsed time and print it to the console
    elapsed = timeit.default_timer() - start_time
    # print "Elapsed time: " + str(elapsed) + " seconds"
    return jsonify(success_count=success_count,
                   fail_count=fail_count,
                   elapsed_time=elapsed)


if __name__ == '__main__':
    app.run(threaded=True)


