# Copyright (c) 2025/2026 by ZAINAL AB <robert.mailcat@gmail.com>


import uuid
import xml.etree.ElementTree as ET
import copy
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import pkgutil

import numpy as np
import math
	
def get_position(r, angle_deg):

    angle_rad = math.radians(angle_deg)  # konversi derajat ke radian
    x = r * math.cos(angle_rad)
    y = r * math.sin(angle_rad)
    return x, y

def caripos(el_bone_p,sud=0):

	el_r = el_bone_p.find(".//scalelx/")
	r = float(el_r.get('value'))
	el_angle = el_bone_p.find(".//angle/")
	angle = float(el_angle.get('value'))

	return get_position(r,angle+sud)


def rotate_point_np(point, angle_deg, center=(0, 0)):
    angle_rad = np.radians(angle_deg)
    rot_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ])
    shifted_point = np.array(point) - np.array(center)
    rotated_point = rot_matrix @ shifted_point + np.array(center)
    return rotated_point


def save_print_log(list_text):
	with open("log.dat", "w") as file:
		file.write("info !\n")
		for text in list_text:
			file.write(text+"\n")

		file.write("\n")
		#file.write("please close this info first !"+"\n")

def replace(parent, el_new):
	parent.remove(parent[0])
	parent.append(el_new)

def hapus_kode(el_kode):
	el_string = el_kode[0][0][0] # hapus grey code
	replace(el_kode,el_string)


def add_converteradd(el_bone_pole,el_bone_target,main_template,el_bones):

	ganti(el_bone_pole,main_template,el_bones)
	ganti(el_bone_target,main_template,el_bones)

def ganti(el_bone,main_template,el_bones):

	el_ori = el_bone.find(".//origin")
	guid_this = el_ori[0].get('guid')
	el_vec_copy = copy.deepcopy(el_ori[0])
	el_vec_copy.attrib.pop('guid')

	el_ori_t = load_template(".//*[@kunci='IK_addorigin']",main_template)
	el_ori_t[0].set('guid',guid_this)
	el_lhs = el_ori_t.find(".//lhs")

	replace(el_lhs,el_vec_copy)
	replace(el_ori,el_ori_t[0])

	#untukk menghindari ada link yg tidak update, ganti semua element dgn guid ini(guid_this) menjadi add converter

	for el_ori in el_bones.findall(".//*[@guid='{no}']/..".format(no= guid_this)):
		replace(el_ori,el_ori_t[0])

def load_template(kunci_tag,main_template):
	el_temp = main_template.find(kunci_tag)
	return copy.deepcopy(el_temp)

def convert(root_file):

	joint = 1
	el_bone_pole = None
	negatif_flip = False
	angle = 0 # angle bone1
	angle2 = 0 # angle bone2
	#print(rotate_point_np((1, 0), 90))  # Output: [0. 1.]

	print("")
	print(">>>>>>>> processing <<<<<<<<")
	template_filename = os.path.join(os.path.dirname(sys.argv[0]), 'template.xml')
	tree_convert = ET.parse(template_filename)
	main_template = tree_convert.getroot()

	el_bones = root_file.find(".//bones")
	if el_bones != None:
		el_boneroot = el_bones.find(".//bone_root")
		id_boneroot = el_boneroot.get('guid')

		el_kodereverse = el_bones.find(".//reverse/link/../..")
		if el_kodereverse == None:
			print("!! not found kode reverse/ pole bone")

		el_kodegreyed = el_bones.find(".//greyed/link/../..") 

		if el_kodegreyed == None:
			print("!! not found kode greyed/ target bone")
			return False

		el_kodegreyed.set('target','bone')
		el_bone_target = el_bones.find(".//*[@target='bone']/..")# bone target
		el_kodegreyed.attrib.pop('target') # hapus kode

		#make non parent if target still parented
		el_parent = el_bone_target.find(".//parent/") 
		guid_target = el_parent.get('guid')

		ada_parent = False
		if not guid_target == id_boneroot: # parent to bone must delete// menjadi tanpa parent dan  guid ke arah root bone
			el_parent.set('guid',id_boneroot)
			ada_parent = True

		# jika diberinama maka tentukan joint bone
		if el_kodereverse == None:
			if not ada_parent:
				print("!! can't make ik bone too money bones")

				return False

			el_name = el_bone_target.find(".//greyed/link/") 
			if el_name.text == "2":
				joint = 2
				el_parent1 = el_bones.find(".//*[@guid='{no}']".format(no= guid_target)) # cari parent target
				if el_parent1 != None:
					el_this = el_parent1.find(".//parent/") 
					el_thisguid = el_this.get('guid')
					el_bone_pole = el_bones.find(".//*[@guid='{no}']".format(no= el_thisguid)) # cari pole
					if el_bone_pole == None:
						print("!! not found pole bone")
						return False

			if el_name.text == "3":
				joint = 3
				el_parent1 = el_bones.find(".//*[@guid='{no}']".format(no= guid_target)) # cari parent target
				if el_parent1 != None:
					el_this = el_parent1.find(".//parent/") 
					el_thisguid = el_this.get('guid')
					el_bone_2 = el_bones.find(".//*[@guid='{no}']".format(no= el_thisguid)) # cari parent2
					if el_bone_2 == None:
						print("!! not found pole bone")
						return False

					el_this = el_bone_2.find(".//parent/") 
					el_thisguid = el_this.get('guid')
					el_bone_pole = el_bones.find(".//*[@guid='{no}']".format(no= el_thisguid)) # cari pole
					if el_bone_pole == None:
						print("!! not found pole bone")
						return False

			if joint == 1:
				el_parent1 = el_bones.find(".//*[@guid='{no}']".format(no= guid_target)) # cari parent target
				if el_parent1 != None:
					el_this = el_parent1.find(".//parent/") 
					el_thisguid = el_this.get('guid')
					
					el_bone_pole_temp = el_bones.find(".//*[@guid='{no}']".format(no= el_thisguid)) # bone pole

					if el_bone_pole_temp == None:
						print("!! not found pole")
						return False

					el_this2 = el_bone_pole_temp.find(".//parent/") 
					el_thisguid2 = el_this2.get('guid')

					if el_thisguid2 == id_boneroot:
						el_bone_pole =el_bone_pole_temp

					else:# IK 3 joint apakah ada bone lg

						el_bone_pole2 = el_bones.find(".//*[@guid='{no}']".format(no= el_thisguid2)) # cari pole
						if el_bone_pole2 != None:
							el_bone_pole =el_bone_pole2
					# jika pole memiliki parent

			el_name.text = 'Bone Target'

		else:
			hapus_kode(el_kodereverse)# # hapus reverse code
		hapus_kode(el_kodegreyed)# hapus grey code

		if el_bone_pole == None:
			el_kodereverse.set('pole','bone')
			el_bone_pole = el_bones.find(".//*[@pole='bone']/..")  # bone pole
			el_kodereverse.attrib.pop('pole') # hapus kode

			#set pos target
		# jika pole memiliki parent segerah delete parent

		pos_pole_x = 0
		pos_pole_y = 0

		el_this = el_bone_pole.find(".//parent/") 
		el_thisguid = el_this.get('guid')
		
		if not id_boneroot == el_thisguid: # jika pole memiliki parent
			el_this.set('guid',id_boneroot)
			el_bone_p = el_bones.find(".//*[@guid='{no}']".format(no= el_thisguid)) # cari parent
			el_vec = el_bone_p.find(".//origin/") 
			pos_p_x = float(el_vec[0].text)
			pos_p_y = float(el_vec[1].text)

			pos_x,pos_y = caripos(el_bone_p)
			
			pos_pole_x= pos_x+pos_p_x
			pos_pole_y= pos_y+pos_p_y

			el_origin = el_bone_pole.find(".//origin/") 
			el_origin[0].text = str(pos_pole_x)
			el_origin[1].text = str(pos_pole_y)

		else: # jika base/pole tidak ada parent lagi
			el_origin = el_bone_pole.find(".//origin/") 
			pos_pole_x = float(el_origin[0].text)
			pos_pole_y = float(el_origin[1].text)

		id_this = el_bone_pole.get('guid')
		el_child1 = el_bones.find(".//*bone_valuenode[@guid='{no}']/../..".format(no= id_this)) # ini element child 1
		id_child1 = el_child1.get('guid')

		pos_x,pos_y = caripos(el_child1)
		el_origin_target = el_bone_target.find(".//origin/") 
		
		if ada_parent:
			el_angle = el_bone_pole.find(".//angle/")
			angle = float(el_angle.get('value'))

			el_angle2 = el_child1.find(".//angle/")
			angle2 = float(el_angle2.get('value'))

			pos_x,pos_y = caripos(el_child1,angle)
			pos_bone2_x,pos_bone2_y = caripos(el_bone_pole)
			pos_elbow_x = pos_bone2_x+pos_pole_x
			pos_elbow_y = pos_bone2_y+pos_pole_y

			#get_position()
			el_origin_target[0].text = str(pos_x+pos_elbow_x)
			el_origin_target[1].text = str(pos_y+pos_elbow_y)

		el_child2 = el_bones.find(".//*bone_valuenode[@guid='{no}']/../..".format(no= id_child1)) # cari apa ada child 2

		# ini berarti 2 joint bone
		el_angle1_t = load_template(".//*[@kunci='IK2bone']",main_template)

		id_pole_origin = str(uuid.uuid4())
		el_origin_pole = el_bone_pole.find(".//origin") 
		el_origin_pole[0].set('guid',id_pole_origin)
		el_guid_ori = el_angle1_t.find(".//*[@guid='GUID_POLE']/..")
		replace(el_guid_ori,el_origin_pole[0])

		el_guid_ori_target = el_angle1_t.find(".//*[@guid='GUID_TARGET']/..")
		id_target_origin = str(uuid.uuid4())
		el_origin_target = el_bone_target.find(".//origin") 
		el_origin_target[0].set('guid',id_target_origin)
		replace(el_guid_ori_target,el_origin_target[0])

		id_pole_scalelx = str(uuid.uuid4())
		el_scalelx_pole = el_bone_pole.find(".//scalelx") 
		el_scalelx_pole[0].set('guid',id_pole_scalelx)
		el_length_bone1 = el_angle1_t.find(".//*[@guid='GUID_L1']/..")

		replace(el_length_bone1,el_scalelx_pole[0])

		id_child1_scalelx = str(uuid.uuid4())
		el_scalelx_child1 = el_child1.find(".//scalelx") 
		el_scalelx_child1[0].set('guid',id_child1_scalelx)
		el_length_bone2 = el_angle1_t.find(".//*[@guid='GUID_L2']/..")
		replace(el_length_bone2,el_scalelx_child1[0])

		id_child1_bone_2_3 = str(uuid.uuid4())
		el_bone_2_3_child1 = el_angle1_t.find(".//joint_bone/")
		el_bone_2_3_child1.set('guid',id_child1_bone_2_3)

		id_child1_t_bone = str(uuid.uuid4())
		el_t_bone_child1 = el_angle1_t.find(".//t_bone/")
		el_t_bone_child1.set('guid',id_child1_t_bone)

		id_child1_weight= str(uuid.uuid4())
		el_weight_child1 = el_angle1_t.find(".//weight/")
		el_weight_child1.set('guid',id_child1_weight)
		#ganti origin ke 60 x 0 px
		el_origin_this = el_child1.find(".//origin/vector") 
		el_origin_this[0].text = str(1.0)
		el_origin_this[1].text = str(0.0)

		id_flip = str(uuid.uuid4())
		el_flip = el_angle1_t.find(".//*[@guid='GUID_FLIP']/..")
		el_flip[0].set('guid',id_flip)

		el_bone_idx = el_angle1_t.find(".//*[@value='BONE_IDX']")
		el_bone_idx.set('value','1')
		el_angle_pole = el_bone_pole.find(".//angle") 
		
		# untukk angle bone child
		el_angle2_t= copy.deepcopy(el_angle1_t)
		el_bone_idx = el_angle2_t.find(".//f_bone/")
		el_bone_idx.set('value','2')
		el_angle_child1 = el_child1.find(".//angle")
		val_angle = float(el_angle_child1[0].get('value'))

		if val_angle < 0:
			negatif_flip = True
			el_flipchild1 = el_angle2_t.find(".//flip/")
			el_flipchild1.set('value','true')
			el_flipcpole = el_angle1_t.find(".//flip/")
			el_flipcpole.set('value','true')

		replace(el_angle_child1,el_angle2_t[0])
		replace(el_angle_pole,el_angle1_t[0])

		#<convert to elastic lenght bone# BEGIN
		el_length_bone1_elastic = copy.deepcopy(el_angle1_t)
		el_length_bone1_elastic[0].set("type","real")
		replace(el_scalelx_pole,el_length_bone1_elastic[0])

		el_length_bone2_elastic = copy.deepcopy(el_angle2_t)
		el_length_bone2_elastic[0].set("type","real")
		replace(el_scalelx_child1,el_length_bone2_elastic[0])
		#>convert to elastic lenght bone# END

		if el_child2 == None: 
			add_converteradd(el_bone_pole,el_bone_target,main_template,el_bones)
			return True
		else: # ini berarti 3 joint bone
		
			#ganti posisi origin target
			pos_ch2_x,pos_ch2_y = caripos(el_child2)
			el_origin_target = el_bone_target.find(".//origin/") 

			if ada_parent: #pindahkan origin target sesua rotasi dua bone di atasnya
				pos_bone3_x,pos_bone3_y = caripos(el_child2,angle+angle2)
				target_awal_x = float(el_origin_target[0].text)
				target_awal_y = float(el_origin_target[1].text)
				el_origin_target[0].text = str(pos_bone3_x+target_awal_x)
				el_origin_target[1].text = str(pos_bone3_y+target_awal_y)
			
			#ganti origin ke 60 x 0 px
			el_origin_this = el_child2.find(".//origin/vector") 
			el_origin_this[0].text = str(1.0)
			el_origin_this[1].text = str(0.0)

			id_child2_scalelx = str(uuid.uuid4())
			el_scalelx_child2 = el_child2.find(".//scalelx") 
			el_scalelx_child2[0].set('guid',id_child2_scalelx)

			el_angle3_t = copy.deepcopy(el_angle1_t)

			# isi length bone 1 dan bone 2 dan bone3 dengan nilai yang sama
			el_length_bone3 = el_angle3_t.find(".//length_bone3")
			replace(el_length_bone3,el_scalelx_child2[0])
			el_length_bone1 = el_angle1_t.find(".//length_bone3")
			replace(el_length_bone1,el_scalelx_child2[0])
			el_length_bone2 = el_angle2_t.find(".//length_bone3")
			replace(el_length_bone2,el_scalelx_child2[0])

			el_bone_idx = el_angle3_t.find(".//f_bone/")
			el_bone_idx.set('value','3')

			# ganti nilai bone2_3 jadi bukan lagi 2 bone tapi 3 bone
			el_bone_2_3_child2 = el_angle3_t.find(".//joint_bone/")
			el_bone_2_3_child2.set('value','2')
			el_bone_2_3_pole = el_angle1_t.find(".//joint_bone/")
			el_bone_2_3_pole.set('value','2')
			el_bone_2_3_child1 = el_angle2_t.find(".//joint_bone/")
			el_bone_2_3_child1.set('value','2')

			el_angle_child2 = el_child2.find(".//angle")
			#cari rotasi child2 untuk isi flip
			negatif_flip2 = False
			val_angle = float(el_angle_child2[0].get('value'))
			if val_angle < 0:
				negatif_flip2 = True
			else:
				negatif_flip2 = False

			if negatif_flip2 != negatif_flip:
				el_tbone = el_angle3_t.find(".//t_bone/")
				el_tbone.set('value','1')

				el_ch = el_angle_child1.find(".//t_bone/")
				el_ch.set('value','1')
				el_pol = el_angle_pole.find(".//t_bone/")
				el_pol.set('value','1')
				
			replace(el_angle_child2,el_angle3_t[0])

			#<convert to elastic lenght bone# BEGIN

			el_length_bone1 = el_scalelx_pole.find(".//length_bone3")
			replace(el_length_bone1,el_scalelx_child2[0])

			el_length_bone2 = el_scalelx_child1.find(".//length_bone3")
			replace(el_length_bone2,el_scalelx_child2[0])

			el_length_bone3_elastic = copy.deepcopy(el_angle3_t)
			el_length_bone3_elastic[0].set("type","real")
			replace(el_scalelx_child2,el_length_bone3_elastic[0])

			add_converteradd(el_bone_pole,el_bone_target,main_template,el_bones)
			return True

def jalankan(root_file):
	
	ada = convert(root_file)
	
	if ada :

		print("Convert IK Done.....")

	else:
		print("Convert IK error.....")
	
	
def main():
	
	onsynfig = len(sys.argv) # tes 
	if onsynfig == 1:
		namafile = "data.sif"
		template_filename = os.path.join(os.path.dirname(sys.argv[0]), namafile)
		tree_convert = ET.parse(template_filename)
		akar_file = tree_convert.getroot()
		jalankan(akar_file)

	else:
		namafile =""
		if len(sys.argv) < 2:
			pass
		else:
			namafile = os.path.basename(sys.argv[1])

		root_file = ET.parse(sys.argv[1]).getroot()
		jalankan(root_file)
		writeTo = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
		with open(writeTo, "wb") as files:
			files.write(ET.tostring(root_file, encoding="utf-8", xml_declaration=True))

if __name__ == "__main__":
	main()