# wall design as per AS3600
import math
import numpy as np
import pandas as pd


def get_number(dimension_of_wall):
    while True:
        try:
            value_m = float(input(f"Please enter your numbers:{dimension_of_wall}"))
            if value_m > 0:
                return value_m
            else:
                print("Dimensions of the walls must be positive come on be serious if you want to proceed!!!")
        except ValueError:
            print("Please enter correct syntax a number is expected here !!!")


# above functions is what gemini suggested to me so my script becomes unbreakable I had inputs only this makes it robust
length_m = get_number("Wall length (m): ")  # user enters the length of wall in m I am calling my function here
thickness_m = get_number("Wall thickness (m): ")  # user enters the thickness of wall in m I am calling my function here
height_m = get_number("Wall height (m): ")  # user enters the height of wall in m I am calling my function here

# dictionary for concrete grade of the wall
concrete_grades_MPa = {
    "M20": 20,
    "M32": 32,
    "M40": 40,
    "M50": 50,
    "M65": 65,
    "M80": 80,
    "M100": 100,
}
height_mm = height_m * 1000  # convert height into mm
length_mm = length_m * 1000  # convert length into mm
thickness_mm = thickness_m * 1000  # convert thickness into mm

"----------------------------------now getting input parameters----------------------------------------"
while True:
    try:
        input_grade_concrete_MPa = int(input("Enter concrete grade in MPa "))
        # user enters the grade of concrete of wall
        grade_key = f"M{input_grade_concrete_MPa}"
        # the above line is good as it makes us add M so in case user adds 32 for my grade it adds M before it '''
        if grade_key in concrete_grades_MPa:
            # above line is we access value from the dictionary and store it in variable fc_prime
            fc_prime = concrete_grades_MPa[grade_key]
            break
        else:
            print(f"The grade that you have entered is incorrect choose it from "
                  f"{list(concrete_grades_MPa.keys())} ")
            # above line is important helps in getting you a list to choose from remember this syntax
    except ValueError:
        print(f"Invalid syntax please enter a number which is concrete grade from this list of "
              f"grades we have {list(concrete_grades_MPa.keys())}")

"-------lets add in what way the wall is restrained by the user both ends or one or both ends---------------"
k_base_restraints = {"both ends": 0.75, "one or both ends": 1.0,
                     }
while True:
    try:
        base_condition = str(input("Can you please enter if wall is restrained at 'both ends' or"
                                   " 'one or both ends': ")).strip().lower()
        restrain = base_condition
        if restrain in k_base_restraints:
            # above line is how we access value from the dictionary of k_base
            k_base = k_base_restraints[base_condition]
            break
        else:
            print(f"Invalid syntax please type how the wall is retrained top and bottom"
                  f"from this options {list(k_base_restraints.keys())}")
    except ValueError:
        print(f"Invalid syntax please type how the wall is retrained top and bottom"
              f"from this options {list(k_base_restraints.keys())}")

k_final = k_base

while True:
    buckling_of_wall = str(input("wall buckling at 'one way' or 'two way' : ").strip().lower())
    if buckling_of_wall == 'one way':
        k_final = k_base
        print(f"k for one way wall is: {k_base}")
        break
    elif buckling_of_wall == 'two way':
        while True:
            lateral_support = str(input("Does floors and walls support walls"
                                        " 'three sides' or 'four sides' : ").strip().lower())
            if lateral_support == 'three sides':
                k_three_sides = (1 / (1 + (height_m / (3 * length_m)) ** 2))
                k_final = min(k_base, max(0.3, k_three_sides))  # as k min should be minimum 0.3 for k_final
                print(f"k is as follows: {k_final: 0.3f} 'wall is"
                      f" supported on"f" three sides by floors and intersecting walls'")
                break  # this will break the loop here in this location
            elif lateral_support == 'four sides':
                if height_m <= length_m:  # means wall is squat wall as length is greater than height
                    k_four_sides = (1 / (1 + (height_m / length_m) ** 2))
                    k_final = min(k_base, max(0.3, k_four_sides))
                else:  # means wall is tall not a squat wall
                    k_four_sides = (length_m / (2 * height_m))
                    k_final = min(k_base, max(0.3, k_four_sides))  # as k min should be minimum 0.3 for k_final
                    print(f"k is as follows: {k_final: 0.3f}")
                    # wall is supported on four sides by floors and intersecting walls'"
                break
            else:
                print("Invalid syntax, Please enter three or four sides to continue")
    break
slenderness = (k_final * height_mm) / thickness_mm

"now that we have clearly followed the k effective length logic lets jump onto minimum eccentricity now"
resultant_eccentricity_m = 0.05 * thickness_m
eccentricity_m = 0.0
e_calc_m = 0.0
while True:
    try:
        floor_condition = int(input("Please type how the floor is connected to wall type 1 for 'continuous'"
                                    ", 2 for 'discontinuous' and 3 for 'number of floors above'"))
        if floor_condition == 1:  # this is for continuous case
            eccentricity_m = 0
            e_calc_m = eccentricity_m  # this is needed otherwise the code will break
            # no floors above the wall, so I don't need to worry in this case
            break
        elif floor_condition == 2:  # this is for discontinuous case
            distance_of_load = float(input("Please enter distance of load in mm from edge of slab 'a': "))
            eccentricity_m = ((thickness_m / 2) - ((1 / 3) * distance_of_load / 1000))
            e_calc_m = eccentricity_m  # this is needed otherwise the code will break
            # no floors above the wall, so I don't need to worry in this case
            break
        elif floor_condition == 3:  # this is in case user selects number of floors above
            load_above_floors = float(input("Please enter loads from all the floors above in kN: "))
            load_current_floor = float(input("Please enter loads from current floor in kN: "))
            floor_at_top = int(input("Please enter 1 if top floor above slab is continuous, 2 if it's discontinuous"
                                     "\nas AS3600 commentary states we need to consider eccentricity from floor siting"
                                     " on top slab on walls while taking in N from floor above refer"
                                     " Figure 'C' Cl11.5.4: "))
            if floor_at_top == 1:  # this is for continuous case in number of floors above
                e_this_floor = 0.0
            else:
                a_this_floor = float(input("Please enter distance of load in mm from edge of slab 'a': "))
                e_this_floor = ((thickness_m / 2) - ((1 / 3) * a_this_floor / 1000))
                e_calc_m = ((e_this_floor * load_current_floor) / (load_above_floors + load_current_floor))
                break
            break
        else:
            print("We will default to minimum eccentricity of (0.05tw)")
            e_calc_m = 0.0
    except ValueError:
        print("Invalid syntax please enter 1 for continuous case\n 2 for discontinuous case\n 3 for number of floors"
              "above if you entered something else its wrong")

final_eccentricity_e_m = max(e_calc_m, resultant_eccentricity_m)

final_eccentricity_e_mm = final_eccentricity_e_m * 1000  # convert final eccentricity into mm
print(f"The final eccentricity 'e' is: {final_eccentricity_e_mm: 0.2f} mm")
accidental_eccentricity_ea_mm = (height_mm ** 2 / (2500 * thickness_mm))
print(f"The accidental eccentricity 'ea' is: {accidental_eccentricity_ea_mm: 0.2f} mm")

print("There are some limitations on the method used in this section, as provided in Clause 11.5.3:")
print(
    "The design axial stress in the member must be less than 3 MPa\n"
    "unless vertical and horizontal reinforcements are provided on both wall faces\n"
    "such that the stress is divided equally between them")
print(
    "Ratio of effective height (Hw) and thickness (Tw) of the wall must be less than 20 if singly reinforced\n"
    "less than 30 if doubly reinforced\n(i.e. if there are more reinforcements, the wall may be taller")
print(
    "The wall cannot be constructed on soils with soil classification Dc or Ec, as defined in AS 1170.4"
    "\nnot to use in a building which may be subject to seismic loads")

N_kN = float(input("Please enter Axial load N* kN/m to check against phiNu: "))


# let's add function for calculation of axial capacity----------------------------------------------------------
def axial_load_kn_per_m(t_mm, final_ecc_e_mm, acc_ecc_ea_mm, fc_mpa):
    phi = 0.65
    phi_Nu_kN = (phi * (t_mm - 1.2 * final_ecc_e_mm -
                        2 * acc_ecc_ea_mm) * (0.6 * fc_mpa))
    print(f"Design Axial strength phiNu of the wall per m is: {phi_Nu_kN: 0.3f} kN/m")
    return phi_Nu_kN


axial_load_calculation = axial_load_kn_per_m(thickness_mm, final_eccentricity_e_mm, accidental_eccentricity_ea_mm,
                                             fc_prime)

if N_kN > axial_load_calculation:
    print("Please change the grade or thickness of wall as your axial force N* is greater than phiNu")
else:
    print("The geometry of wall and grade used is good as our phiNu/m is greater than N*/m")

"-------------------------------------------------------------------------------------------------------"
ratio = height_mm / thickness_mm
print("Following conditions need to be met for simple wall design")
if ratio > 30:
    print("Please design as a column you cant design using simplified method as per clause 11.5.2 (c)")
elif 30 >= ratio >= 20:
    print("The wall must be doubly reinforced and can be designed using simplified method mentioned in 11.5.2 a")
else:
    print("The wall can be singly or doubly reinforced and designed using simplified method as mentioned in 11.5.2 b")
"---------------------------------------------------------------------------------------------------------------------"
"now lets calculate axial stress in the wall"

axial_stress_MPa = (N_kN / thickness_mm)  # as N/mm2 is MPa for stress calculation
"the units wherein we have load in kN turn into N and thickness mm x 1000mm width of wall"
print(f"Axial stress in the wall is as follows: {axial_stress_MPa: 0.2f} MPa")
"-----------------------------------------------------------------------------------------------------------"
if axial_stress_MPa >= 3.0:
    reo_both_face = ("since axial stress is greater than 3.0 MPa you must use reo on both faces of the wall"
                     " as per clause 11.5.3(a)")
    print(reo_both_face)
elif axial_stress_MPa <= 3.0:
    reo_single_face = "since axial stress is less than 3.0 MPa you can use reo central as well"
    print(reo_single_face)
"----------now checking conditions of clause 11.7 Reinforcement requirements in walls--------------------------"
if thickness_m > 0.2:  # As per 11.7.3(a)
    print("since the thickness of wall is greater than 200mm reinforcement must be provided on both faces of the wall")
else:
    print("since thickness is less than 200mm you can use reo central")  # As per 11.7.3(a)
if buckling_of_wall == 'two way':
    print("Reinforcement should be provided on both faces of the as per 11.7.3(b)")
else:
    print("Reinforcement can be provided central since you have one way buckling not two way buckling"
          " as per 11.7.3(c)")
if height_m > 20:
    print("Reinforcement should be provided on both faces of the as per 11.7.3(d)")
elif slenderness > 20:
    print("Reinforcement should be provided on both faces of the as per 11.7.3(d)")
else:
    print("Reinforcement can be central as per 11.7.3(d)")
"-------------------------------------------------------------------------------------------------------------"

layers = int(input("Please enter number of layers in the wall '1' for one face reo and '2' for both face reo: "))
if layers == 1:
    print(f"Layer of reinforcements used in the wall is: {layers} layer")
else:
    print(f"Layer of reinforcements used in the wall is: {layers} layers")
"--------------------------------------------------------------------------------------------------------------"
'''now lets get to shear calculations as per clause 11.6.2'''
phi_shear = 0.7
vu_max_kN = phi_shear * 0.2 * fc_prime * (0.8 * length_m * thickness_m) * 1000  # to get answer in kN
print(f"Vu_max for the wall is as follows: {vu_max_kN: 0.3f} kN")
'''For shear strength excluding wall reinforcement as per Cl.11.6.3'''
"This means shear due to just concrete not steel"

ratio_shear_m = height_m / length_m
v_scale_kN = (0.8 * length_m * thickness_m)
v_concrete_base_kN = 0.17 * math.sqrt(fc_prime) * v_scale_kN * 1000
print(f"minVuc is: {v_concrete_base_kN: 0.3f} kN")
sqrt_fc = math.sqrt(fc_prime)
v_con_1_kN = ((0.66 * sqrt_fc - 0.21 * ratio_shear_m * sqrt_fc) * v_scale_kN * 1000)
if ratio_shear_m <= 1.0:  # means wall is a squat wall
    v_concrete_kN = v_con_1_kN
else:  # means wall is a tall wall
    v_con_2_kN = (0.05 * sqrt_fc + (0.1 * sqrt_fc / (ratio_shear_m - 1.0))) * v_scale_kN * 1000
    v_concrete_kN = min(v_con_1_kN, v_con_2_kN)

v_final_concrete_kN = max(v_concrete_base_kN, v_concrete_kN)
phi_v_final_concrete_kN = v_final_concrete_kN * phi_shear

print(f"The shear strength of the wall excluding wall reinforcement Vuc is: {v_final_concrete_kN: 0.3f} kN")
print(f"The shear strength of the wall excluding wall reinforcement phiVuc is: {phi_v_final_concrete_kN: 0.3f} kN")
"------------------------------------------------------------------------------------------------------------------"
'''shear strength due to reinforcements'''
fsy_MPa = 500  # reinforcement grade in MPa
"--Now lets define a function that would be generalised and can be used in both vertical and horizontal direction---"


def get_reo_diameter_mm2(dia_of_reo):  # I have passed dia of reo as argument in my script which I will use later
    steel_reo_diameters = {
        "N10": 78,
        "N12": 113,
        "N16": 201,
        "N20": 314,
        "N24": 452,
        "N28": 616,
        "N32": 804,
        "N36": 1020,
        "N40": 1260,
    }  # I defined a dictionary inside a function
    while True:
        try:
            dia_of_reo_directions_mm2 = float(input(f"Please enter diameter of reo for example 12,16,"
                                                    f"20 etc {dia_of_reo} "))
            dia_steel_reo = f"N{int(dia_of_reo_directions_mm2)}"
            area_mm2 = steel_reo_diameters[dia_steel_reo]
            return area_mm2, dia_steel_reo
        except KeyError:  # we will except a key error as we are using a dictionary with values
            print(f"Please enter {dia_of_reo} properly a number is expected here!!!!"
                  f"pick something from: {list(steel_reo_diameters.keys())} ")


# the above code for except is idea gemini helped me with bloody just memorise it

reo_direction = str(input("Do you plan to provide same dia bars in vertical and horizontal direction 'yes' or 'no'"
                          ": ").strip().lower())
if reo_direction == 'yes':
    area_both_direction, name_both_direction = get_reo_diameter_mm2("both directions: ")
    final_area_vertical_mm2 = final_area_horizontal_mm2 = area_both_direction
    final_name_vertical = final_name_horizontal = name_both_direction
# python lets you declare two variable simultaneously
else:
    area_vertical_mm2, vertical_bar = get_reo_diameter_mm2("in vertical direction: ")
    area_horizontal_mm2, horizontal_bar = get_reo_diameter_mm2("in horizontal direction: ")
    final_area_vertical_mm2 = area_vertical_mm2
    final_area_horizontal_mm2 = area_horizontal_mm2
    final_name_vertical = vertical_bar
    final_name_horizontal = horizontal_bar

"-------------------------------------------------------------------------------------------------------------------"
'''lets do spacing of the reinforcement now since we did the area of reinforcement properly with functions'''


def get_reo_spacing_mm(spacing_reo):
    while True:
        try:
            reinforcement_spacing_mm = float(input(f"Please enter spacing {spacing_reo}"))
            return reinforcement_spacing_mm
        except ValueError:
            print("Invalid syntax please enter correct spacing in mm example 100,200,300mm etc")


# now time to call functions in both directions vertical and horizontal
reo_spacing_mm = str(input("Do you plan to use same spacing of bars in vertical and horizontal direction 'yes' or 'no'"
                           ": "))

if reo_spacing_mm == 'yes':
    spacing_vertical_mm = spacing_horizontal_mm = get_reo_spacing_mm("in both directions: ")
    final_spacing_vert = final_spacing_horizontal = spacing_vertical_mm
else:
    spacing_vertical_mm = get_reo_spacing_mm("in vertical direction: ")
    spacing_horizontal_mm = get_reo_spacing_mm("in horizontal direction ")
    final_spacing_vert = spacing_vertical_mm
    final_spacing_horizontal = spacing_horizontal_mm

pw_vertical_direction = (final_area_vertical_mm2 / (final_spacing_vert * thickness_mm))
pw_vertical_direction_final = layers * pw_vertical_direction
print(f"The reinforcement ratio in vertical direction is as follows: {pw_vertical_direction_final: 0.4f}")

"-----------------now same logic for horizontal direction will be as follows----------------------------------"

pw_horizontal_direction = (final_area_horizontal_mm2 / (final_spacing_horizontal * thickness_mm))
pw_horizontal_direction_final = layers * pw_horizontal_direction
print(f"the reinforcement ratio in horizontal direction is as follows: {pw_horizontal_direction_final: 0.4f}")

if ratio_shear_m <= 1.0:
    pw = min(pw_vertical_direction_final, pw_horizontal_direction_final)  # as per Cl 11.6.4 a
    print(f"The pw for the wall is as follows: {pw: 0.4f}")
else:
    pw = pw_horizontal_direction_final  # as per Cl 11.6.4 b
    print(f"The pw for the wall is as follows: {pw: 0.4f}")
"-----------------now to find Vus shear force due to steel reinforcements-----------------------------------------"
Vus = (pw * fsy_MPa * (0.8 * length_m * 1000 * thickness_mm)) / 1000
print(f"The shear strength of the wall by reinforcement Vus is: {Vus: 0.3f} kN")
phiVus = 0.7 * Vus
print(f"The shear strength of the wall by reinforcement phiVus is: {phiVus: 0.3f} kN")
"--------------------SHEAR STRENGTH OF THE WALL IS AS FOLLOWS------------------------------------"
phiVu_kN = min(vu_max_kN, (phiVus + phi_v_final_concrete_kN))
print(f"The shear strength of wall is as follows: {phiVu_kN: 0.3f} kN total for {length_m}m length of the wall")

"-------Lets do minimum reo requirements for the wall as per Cl 11.7-------------------------------------------"
"As per 11.7.1 requirements on minimum reinforcement"
pw_vertical_minimum = 0.0025  # As per AS cl. 11.7.1
pw_horizontal_minimum = 0.0025  # As per AS cl. 11.7.1
axial_comp_stress_limit = min(0.03 * fc_prime, 2.0)  # code says force but this gets nullified when you multiply by 1m
# width of wall as 1000 gets deleted from both ends 'and' we gets stress in the walls for 2MPa limit
if axial_stress_MPa > axial_comp_stress_limit:
    target_pw_vertical_minimum = 0.0025
else:
    target_pw_vertical_minimum = 0.0015
if pw_vertical_direction_final > target_pw_vertical_minimum:
    print("You dont need to add more reo in your wall as you have min reo needed in vertical direction")
else:
    print("You need to add more reo in the vertical direction of the wall as your min reo that "
          "you added is less than what is need in the wall"
          "\nrefer clause Cl 11.7.1(a)")
while True:
    restrain_of_wall = str(input("Is the wall restrained in the horizontal direction 'yes' or 'no': ")).strip().lower()
    if restrain_of_wall == 'yes':
        target_pw_horizontal_minimum = 0.0015
        break
    elif restrain_of_wall == 'no':
        target_pw_horizontal_minimum = 0.0025
        break
    else:
        print("Invalid syntax, Please enter yes or no to continue")
if target_pw_horizontal_minimum > pw_horizontal_direction_final:
    print("You need to add more reo in the horizontal direction of the wall as your min reo that "
          "you added is less than what is need in the wall"
          "\nrefer clause Cl 11.7.1(b)")
else:
    print("You dont need to add more reo in your wall as you have min reo needed in horizontal direction")
max_spacing_limit = min(2.5 * thickness_mm, 350)
print("As per Cl 11.7.3 spacing rules for walls: centre to centre spacing between parallel"
      "bars to max 2.5*tw or 350mm max")
if max_spacing_limit < final_spacing_vert:
    print("Please increase the spacing between the bars in vertical direction as it "
          "does not pass the requirements")
else:
    print("vertical spacing between bars"
          " pass the requirements of max spacing as outlined by code!!!!")
"----------------------------now same logic in horizontal direction---------------------------"
if max_spacing_limit < final_spacing_horizontal:
    print("Please increase the spacing between the bars in horizontal direction as it "
          "does not pass the requirements")
else:
    print("Horizontal spacing between bars"
          " pass the requirements of max spacing as outlined by code!!!!")

# dictionary for concrete exposure types
exposure_classification = {("A1", "minor"): 0.0025,
                           ("A2", "minor"): 0.0025,
                           ("A1", "moderate"): 0.0035,
                           ("A2", "moderate"): 0.0035,
                           ("A1", "strong"): 0.006,
                           ("A2", "strong"): 0.006,
                           ("B1", "minor"): 0.006,
                           ("B2", "minor"): 0.006,
                           ("C1", "minor"): 0.006,
                           ("C2", "minor"): 0.006,
                           }

while True:
    try:
        horizontal_crack_control = str(input("Please enter if exposure classification like 'A1','A2','B1',"
                                             "'B2','C1','C2': ")).strip().upper()
        if horizontal_crack_control in ['A1', 'A2']:  # gemini gave me this logic to use in the code
            degree_crack_control = str(input("Please enter your degree of crack control that you plan to use eg"
                                             " minor , moderate , strong ??: ")).strip().lower()
            target_crack_control = exposure_classification[(horizontal_crack_control, degree_crack_control)]
        else:
            degree_crack_control = 'minor'
            target_crack_control = exposure_classification[(horizontal_crack_control, degree_crack_control)]
        if pw_horizontal_direction_final >= target_crack_control:
            print(f"Since the provided {pw_horizontal_direction_final} is more than the required"
                  f" {target_crack_control}\nwe have enough crack control reo in horizontal direction")
        else:
            print(f"Since the provided {pw_horizontal_direction_final} is less than the required"
                  f" {target_crack_control} we don't have enough crack control reo "
                  f"in horizontal direction\nplease increase bar size or spacing")
        break
    except KeyError:
        print("Invalid syntax, Please enter exposure classification and degree of crack control from the list "
              f"below {list(exposure_classification.keys())}")
if length_m >= 8.0:
    print("CRITICAL NOTE - Wall length exceeds 8m, so as per As 3600 Cl 11.7.2 Note\n"
          "standard horizontal reinforcement ratio may be insufficient at the base so please consider\n"
          "increasing horizontal reo or adding trimmers bars at the base of the wall")

"---------Now the last thing in section 11 for Dowel connection in prefabricated concrete walls---------------"
vertical_Ast_mm2 = pw_vertical_direction_final * thickness_mm * 1000  # calculates total Ast in vertical direction
print(f"The Total area of steel in vertical direction is as follows: {vertical_Ast_mm2:0.3f}")
wall_compression = str(input("Please enter if the wall is in net compression (yes/no):")).strip().upper().lower()
mu = float(input("Please enter structural ductility factor mu = 1 , 2 or 3 ?: "))

if mu > 1.0:
    print("Dowels should be able to transfer yield force greater than vertical reo in the wall at the joint")
    required_Ast_mm2 = 1.0 * vertical_Ast_mm2
elif mu <= 1.0 and wall_compression == 'no':
    required_Ast_mm2 = 0.50 * vertical_Ast_mm2
else:
    print("since the wall is in net compressions Cl 11.7.5 b(i) says no special requirement is needed\n"
          " just follow minimum reinforcement ratio ")
    required_Ast_mm2 = target_pw_vertical_minimum * 1000 * thickness_mm

"lets create a numpy array consisting of bar size and spacing so we can suggest the user what he can use for his wall"

bar_areas_mm2 = np.array([78, 113, 201, 314, 452, 616, 804, 1020, 1260])
bar_spacing_mm = np.array([100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400])
bar_spacing_transpose_mm = bar_spacing_mm.reshape(-1, 1)  # this transposes the spacing, so I can use it for reo table

cs_area_per_m_width_mm2 = (bar_areas_mm2 * 1000) / bar_spacing_transpose_mm
np.set_printoptions(precision=0, suppress=True)

"---------------------------lets use pandas to make this table neat------------------------------"

bar_diameters_mm = ["N10", "N12", "N16", "N20", "N24", "N28", "N32", "N36", "N40"]
bars_spacing_mm = ["100mm", "125mm", "150mm", "175mm", "200mm", "225mm", "250mm", "275mm", "300mm", "350mm", "400mm"]
table = pd.DataFrame(data=cs_area_per_m_width_mm2, index=bars_spacing_mm, columns=bar_diameters_mm)

suggestion_for_user = table[table >= required_Ast_mm2].stack().dropna().head(10)
for (spacing, bar), area in suggestion_for_user.items():
    print(f"below are the options you can adopt {bar} with {spacing} spacing with {area:0.1f} mm2/m ")

# what stack does is turns a 2D table into a 1D list of pairs
# what drop na does is removes the NAN entries from print
# what head (5) gives you is top 5 entries
# items() is command that tells python to give us a key:value like what we have in a normal dictionary
# in our example index is (spacing,dia) then you unpack both of them

# let's add the above input to a dictionary so, I can loop them through my dictionary
print("\nBelow are the inputs you have added for the wall script in a summary: ")

input_summary = {"wall height (m)": height_m,
                 "wall length (m)": length_m,
                 "wall thickness (m)": thickness_m,
                 "concrete grade f'c (MPa)": fc_prime,
                 "Floor type above wall": floor_condition,
                 "Buckling type": buckling_of_wall,
                 "Axial load (kN/m)": N_kN,
                 "eccentricity(mm)": final_eccentricity_e_mm,
                 "accidental eccentricity(mm)": accidental_eccentricity_ea_mm,
                 }
result_summary = {"Axial capacity phi Nu (kN/m)": axial_load_calculation,
                  "Axial stress (MPa)": axial_stress_MPa,
                  "Max shear force Vu max (kN)": vu_max_kN,
                  "shear force Vuc due to concrete (kN)": v_final_concrete_kN,
                  "phi Vuc shear force due to concrete (kN)": phi_v_final_concrete_kN,
                  "phi Vus shear force due to steel (kN)": phiVus,
                  "Design strength of wall in plan shear phiVu (kN)": phiVu_kN,
                  "Diameter of reo in vertical direction (mm)": final_name_vertical,
                  "Diameter of reo in horizontal direction (mm)": final_name_horizontal,
                  "Spacing of reo in vertical direction (mm)": final_spacing_vert,
                  "Spacing of reo in horizontal direction (mm)": final_spacing_horizontal,
                  "Reinforcement ratio in vertical direction (pw)": pw_vertical_direction_final,
                  "Reinforcement ratio in horizontal direction (pw)": pw_horizontal_direction_final,
                  }
for labels, values in input_summary.items():
    print(f"{labels.ljust(40)}: {values}")

print("\nbelow are the results for the wall based on the input: ")
for results, answers in result_summary.items():
    print(f"{results.ljust(50)}: {answers:0.4f}")
